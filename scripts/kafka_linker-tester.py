from sqlite3 import enable_callback_tracebacks
import datetime
import pprint
import uuid
from bluesky_kafka import RemoteDispatcher

try:
    from nslsii import _read_bluesky_kafka_config_file
except ImportError:
    from nslsii.kafka_utils import _read_bluesky_kafka_config_file

from event_model import RunRouter

from pathlib import Path
import event_model
import tqdm


def process_kafka_messages(beamline_acronym, data_source="runengine", target=None):
    """
    Parameters
    ----------
    beamline_acronym : str
        the lowercase TLA

    data_source : str, optional
        The source of the documents on the beamline (e.g. 'runengine' or 'pdfstream')

    target : Callable[(str, Document), None], optional
        Function to pass the documents from kafka to. If not specified, defaults to printing
        the documents
    """

    def print_message(name, doc):
        print(
            f"{datetime.datetime.now().isoformat()} document: {name}\n"
            f"contents: {pprint.pformat(doc)}\n"
        )

    if target is None:
        target = print_message

    kafka_config = _read_bluesky_kafka_config_file(
        config_file_path="/etc/bluesky/kafka.yml"
    )

    # this consumer should not be in a group with other consumers
    #   so generate a unique consumer group id for it
    unique_group_id = f"autosymlink-{beamline_acronym}-{data_source}"
    cconfig = kafka_config["runengine_producer_config"]
    cconfig["auto.offset.reset"] = "latest"
    kafka_dispatcher = RemoteDispatcher(
        topics=[f"{beamline_acronym}.bluesky.{data_source}.documents"],
        bootstrap_servers=",".join(kafka_config["bootstrap_servers"]),
        group_id=unique_group_id,
        consumer_config=cconfig,
    )

    kafka_dispatcher.subscribe(target)
    kafka_dispatcher.start()


def get_symlink_pairs(target_path, *, det_map, root_map=None):
    """
    Coroutine to sort out what to link to what.

    Parameters
    ----------
    target_path : Path
        The base directory to put the symlinks in.  They will be further nested.

    det_map : dict[str, str]
        A dictionaly mapping the detector name (2M, 900KW) to the type of measurement (SAXS, WAXS)
    root_map : dict[str, str], optional
        A mapping of root in the resource document -> a new path as in databroker

    Sends
    -----
    name, doc : str, Document
        The standard event model input!

    Returns
    -------
    list[tuple[str, Path, Path]]
         A tuple of the start uid, the source path and the destination path.
    """
    if root_map is None:
        root_map = {}
    links = []
    target_template: str
    output_path: str
    resource_info = {}
    datum_info = {}
    target_keys = set()
    while True:
        inp = yield
        if inp is None:
            break
        name, doc = inp
        if name == "start":
            start_uid = doc["uid"]
            output_path = Path(*Path(doc["path"]).parts[-2:])

            target_template = f'{output_path}/{{det_name}}/{doc["user_name"]}_{doc["sample_name"]}_id{doc["scan_id"]}_{{N:06d}}_{{det_type}}.tif'

        elif name == "resource":
            # we only handle AD TIFF
            if doc["spec"] != "AD_TIFF":
                continue
            doc_root = doc["root"]
            resource_info[doc["uid"]] = {
                "path": Path(root_map.get(doc_root, doc_root)) / doc["resource_path"],
                "kwargs": doc["resource_kwargs"],
            }
        elif "datum" in name:
            if name == "datum":
                doc = event_model.pack_datum_page(doc)

            for datum_uid, point_number in zip(
                doc["datum_id"], doc["datum_kwargs"]["point_number"]
            ):
                datum_info[datum_uid] = (
                    resource_info[doc["resource"]],
                    point_number,
                )
        elif name == "descriptor":
            for k, v in doc["data_keys"].items():
                if "external" in v:
                    target_keys.add(k)
        elif "event" in name:
            if name == "event":
                doc = event_model.pack_event_page(doc)
            for key in target_keys:
                
                det, _, _ = key.partition("_")
                det_name = det.removeprefix('pil')
                det_type = det_map.get(det_name, det_name)

                if key not in doc["data"]:
                    continue
                for datum_id in doc["data"][key]:
                    resource_vals, point_number = datum_info[datum_id]
                    orig_template = resource_vals["kwargs"]["template"]
                    fpp = resource_vals["kwargs"]["frame_per_point"]

                    base_fname = resource_vals["kwargs"]["filename"]
                    for fr in range(fpp):
                        source_path = Path(
                            orig_template
                            % (
                                str(resource_vals["path"]) + "/",
                                base_fname,
                                point_number * fpp + fr,
                            )
                        )
                        dest_path = target_path / target_template.format(
                            det_name=det_name,
                            N=point_number * fpp + fr,
                            det_type=det_type,
                        )
                        links.append((start_uid, source_path, dest_path))

        elif name == "stop":
            break

    return links


def do_single_header_symlinks(
    header,
    target_path=Path("/nsls2/data/smi/legacy/results/data"),
    *,
    overwrite_dest=False,
    det_map=None,
):
    if det_map is None:
        det_map = {"900KW": "WAXS", "1M": "SAXS"}
    gen = get_symlink_pairs(Path(target_path), det_map=det_map)
    gen.send(None)
    try:
        for name, doc in header.documents():
            gen.send((name, doc))
    except StopIteration as ex:
        links = ex.value

    return do_symlinking(links, overwrite_dest=overwrite_dest)


def get_all_symlinks(headers, target_path, det_map=None):
    """
    Get the symlinks for all of the headers in a catalog.

    Parameters
    ----------
    headers : Catalog
        Needs to support ``obj.values_inedxer``
    target_path : Path
        The base path for the symlinks

    det_map : dict[str, str], optional
        A dictionaly mapping the detector name (1M, 900KW) to the type of measurement (SAXS, WAXS)

    Returns
    -------
    list[tuple[str, Path, Path]]
         A tuple of the start uid, the source path and the destination path.
    """
    if det_map is None:
        det_map = {"900KW": "WAXS", "1M": "SAXS"}
    links = []
    for h in tqdm.tqdm(headers.values_indexer):

        gen = get_symlink_pairs(Path(target_path), det_map=det_map)
        gen.send(None)
        try:
            for name, doc in h.documents():
                gen.send((name, doc))
        except StopIteration as ex:
            links.extend(ex.value)
    return links


def do_symlinking(
    links: list[tuple[str, Path, Path]],
    overwrite_dest=False,
) -> tuple[list[tuple[str, Path, Path]], list[tuple[str, Path, Path]]]:
    """
    Create the symlinks, making target directories as needed.

    Paramaters
    ----------
    links : list of (uid, src, dest) tuples
        The uid, source file and destination files

    overwrite_dest : bool, optional
        If an existing destitation should be unlinked and replaced.

    Returns
    -------
    linked, failed : list of (uid, src, dest) tuples
        The linked (or failed) values.
    """
    failed = []
    linked = []
    for uid, src, dest in tqdm.tqdm(links, leave=False):
        if not src.exists():
            failed.append((uid, src, dest))
            continue
        try:
            dest.parent.mkdir(exist_ok=True, parents=True)
            if overwrite_dest and dest.exists():
                dest.unlink()
            dest.symlink_to(src)
        except Exception:
            tqdm.tqdm.write(f"FAILED: {dest}")
            failed.append((uid, src, dest))
        else:
            tqdm.tqdm.write(f"Linked: {dest}")
            linked.append((uid, src, dest))
    return linked, failed


def symlink_factory_factory(target_path, det_map=None):
    """
    Build a factory to pass to RunRouter bound to the taregt path

    Parameters
    ----------
    target_path : Path
        The base directory to put the symlinks in.  They will be further nested.

    det_map : dict[str, str]
        A dictionaly mapping the detector name (1M, 900KW) to the ftype of measurement (SAXS, WAXS)

    Returns
    -------
    factory
        A function that matches the signature for the input to RunRouter
    """
    if det_map is None:
        det_map = {"900KW": "WAXS", "1M": "SAXS"}

    def symlink_factory(name, doc):
        """
        Set up a callback per run start.
        """
        gen = get_symlink_pairs(Path(target_path), det_map=det_map)
        gen.send(None)  # Prime the pump

        def symlink_callback(name, doc):
            """
            The actual callback that will see the documents
            """
            try:
                gen.send((name, doc))
            except StopIteration as ex:
                _, failed = do_symlinking(
                    # The list of files we need to link
                    ex.value,
                    # YOLO
                    overwrite_dest=True,
                )
                if len(failed):
                    raise Exception(
                        f"failed to link {len(failed)} files: {failed if len(failed) < 5 else '[...]'}"
                    ) from None

        return [symlink_callback], []

    return symlink_factory


if __name__ == "__main__":
    rr = RunRouter(
        [
            symlink_factory_factory("/nsls2/data/smi/legacy/results/test_data"),
        ]
    )

    process_kafka_messages("smi", data_source="runengine", target=rr)

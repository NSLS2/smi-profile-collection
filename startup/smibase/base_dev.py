print(f"Loading {__file__}")

import os
from tiled.client import from_uri
from bluesky_tiled_plugins import TiledWriter
import copy

from IPython import get_ipython
RE = get_ipython().user_ns['RE']
RE.md["tiled_access_tags"] = [RE.md['data_session']]


def patch_descriptor(doc):
    # This was labeled "<f8" but it is actually "<i4".
    if f"pil1M_image" in doc["data_keys"]:
        doc["data_keys"][f"pil1M_image"]["dtype_str"] = "<i4"

    return doc


def patch_resource(doc):

    doc = copy.deepcopy(doc)
    kwargs = doc.get("resource_kwargs", {})

    root = doc.get("root", "")
    if not doc["resource_path"].startswith(root):
        doc["resource_path"] = os.path.join(root, doc["resource_path"])
    doc["root"] = ""  # root is redundant if resource_path is absolute

    doc["resource_path"] = doc["resource_path"].replace("/nsls2/data1/smi", "/nsls2/data/smi")

    if frame_per_point := kwargs.pop('frame_per_point', None):
        kwargs['multiplier'] = frame_per_point

    if doc.get("spec") in ["AD_TIFF"]:
        kwargs["template"] = "/" + kwargs["template"].lstrip("/")    # Ensure leading slash
        kwargs["join_method"] = "concat"   # "stack" was used for old data, but "concat" should be correct if new data has a leading left dimension set to 1

    return doc


# Configure a Tiled writing client
tiled_writing_client_sql = from_uri("https://tiled.nsls2.bnl.gov", api_key=os.environ["TILED_BLUESKY_WRITING_API_KEY_SMI"])["smi/migration"]
tw = TiledWriter(tiled_writing_client_sql, batch_size=1, patches = {'resource': patch_resource, 'descriptor': patch_descriptor})

RE.subscribe(tw)

print("\nInitializing Tiled reading client...\nMake sure you check for duo push.")
tiled_reading_client_sql = from_uri("https://tiled.nsls2.bnl.gov")["smi/migration"]

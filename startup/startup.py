
# Put the smi_beamline package (src/) on the import path.  startup.py lives in <repo>/startup/, so
# the package is at <repo>/src.  Works whether this file is run by IPython --profile-dir=. or exec'd
# by the queueserver; falls back to the profile dir / cwd if __file__ is unavailable.
import os as _os
import sys as _sys
try:
    _repo = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
except NameError:
    _repo = _os.path.dirname(_os.path.abspath(_os.getcwd()))
_src = _os.path.join(_repo, "src")
if _repo not in _sys.path:
    _sys.path.insert(0, _repo)
if _os.path.isdir(_src) and _src not in _sys.path:
    _sys.path.insert(0, _src)

from IPython import get_ipython
ipython = get_ipython()

if '__IPYTHON__' in globals():
    ipython.magic('load_ext autoreload')
    ipython.magic('autoreload 2')

# --- Session Bootstrap (formerly startup/smibase/base.py) ---
#
# In many NSLS-II profile collections this work lives in a separate ``base.py``.  SMI keeps it
# inline here so startup has a single Python entry point and no legacy ``smibase`` package.  This
# section creates the session-level objects and services that downstream startup code expects:
#
# - RE / sd / bec via ``nslsii.configure_base``
# - persistent Redis-backed config/sample stores: mdsave, samplestore
# - ephemeral Redis status store used by GUI/RunEngine liveness helpers
# - primary Tiled writer and optional interactive Tiled reader/databroker
# - olog/prompt/plot defaults for interactive IPython sessions
# - the ``smi_beamline.devices._context`` seam used by package device/instance modules
import copy
import datetime
import logging
import os
import time

import nslsii
import redis
from bluesky.callbacks.buffer import BufferingWrapper
from bluesky_tiled_plugins import TiledWriter
from databroker import Broker
from IPython.terminal.prompts import Prompts
import matplotlib.pyplot as plt
from redis_json_dict import RedisJSONDict
from tiled.client import from_profile, from_uri

try:
    from bluesky_queueserver import is_re_worker_active
    IS_QS_WORKER = bool(is_re_worker_active())
except Exception:
    IS_QS_WORKER = False

# In terminal IPython, configure_base populates the live user namespace.  In the queueserver worker
# there is no real IPython namespace, so use a plain dict and then expose RE/sd/bec/db as globals.
if ipython is not None and not IS_QS_WORKER:
    _user_ns = ipython.user_ns
else:
    _user_ns = {}

with open("/etc/bluesky/redis.secret", "r") as f:
    redis_secret = f.read().strip()

mdclient = redis.Redis("xf12id2-smi-redis1.nsls2.bnl.gov", db=1, ssl=True, port=6380,
                       password=redis_secret)
mdsave = RedisJSONDict(mdclient, "swaxsmetadata")

sampleclient = redis.Redis("xf12id2-smi-redis1.nsls2.bnl.gov", db=2, ssl=True, port=6380,
                           password=redis_secret)
samplestore = RedisJSONDict(sampleclient, "swaxssamples")

# Raw Redis client for ephemeral GUI/status keys such as swaxsstatus:re_busy.
statusclient = redis.Redis("xf12id2-smi-redis1.nsls2.bnl.gov", db=3, ssl=True, port=6380,
                           password=redis_secret)

tiled_writing_client = from_profile(
    "nsls2", api_key=os.environ["TILED_BLUESKY_WRITING_API_KEY_SMI"])["smi"]["raw"]
tiled_writing_client.context.http_client.headers["tiled-qos"] = "acquisition"


class TiledInserter:
    def insert(self, name, doc):
        attempts = 20
        error = None
        for _ in range(attempts):
            try:
                tiled_writing_client.post_document(name, doc)
            except Exception as exc:
                print("Document saving failure:", repr(exc))
                error = exc
            else:
                break
            time.sleep(2)
        else:
            raise error


tiled_inserter = TiledInserter()

nslsii.configure_base(
    _user_ns,
    broker_name="smi",
    bec_derivative=True,
    publish_documents_with_kafka=True,
    magics=not IS_QS_WORKER,
    mpl=not IS_QS_WORKER,
    redis_url="xf12id2-smi-redis1.nsls2.bnl.gov",
    redis_port=6380,
    redis_ssl=True,
)

RE = _user_ns["RE"]
bec = _user_ns["bec"]
sd = _user_ns["sd"]
RE.unsubscribe(0)
RE.subscribe(tiled_inserter.insert)

from smi_beamline.devices import _context as _seam

_seam.configure(run_engine=RE, config_dict=mdsave, sd=sd, bec=bec,
                sample_store=samplestore, status_store=statusclient)

if not IS_QS_WORKER:
    print("\nInitializing Tiled reading client...\nMake sure you check for duo push.")
    tiled_reading_client = from_profile("nsls2", username=None)["smi"]["raw"]
    tiled_reading_client.context.http_client.headers["tiled-qos"] = "acquisition"
    db = Broker(tiled_reading_client)
else:
    tiled_reading_client = None
    db = None
_seam.configure(db=db)

plt.rcParams["figure.dpi"] = 200
assets_path = f"/nsls2/data/smi/proposals/{RE.md['cycle']}/{RE.md['data_session']}/assets/"
bec.disable_baseline()

if ipython is not None and not IS_QS_WORKER:
    nslsii.configure_olog(ipython.user_ns, subscribe=True)

logger = logging.getLogger("bluesky")
logger.setLevel("INFO")


class ProposalIDPrompt(Prompts):
    def in_prompt_tokens(self, cli=None):
        data_session = str(RE.md.get("data_session", "N/A"))
        if data_session.startswith("pass-"):
            data_session = data_session[len("pass-"):]
        project_name = str(RE.md.get("project_name", "N/A"))
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return [(None, f"SMI {data_session} {project_name} {now} "
                       f"[{self.shell.execution_count}]: ")]


if ipython is not None and not IS_QS_WORKER:
    ipython.prompts = ProposalIDPrompt(ipython)

# --- Supplemental Tiled Writer (formerly startup/smibase/base_dev.py) ---
#
# This is the old ``base_dev.py`` payload kept inline for DSSI/operator readability.  It installs a
# second Tiled writer targeting the migration tree and applies the resource/descriptor patches needed
# for SMI detector documents.  It also sets the Tiled access tag from the current data session.  The
# optional interactive reader below is skipped in queueserver workers to avoid a Duo-auth hang.
RE.md["tiled_access_tags"] = [RE.md["data_session"]]


def patch_descriptor(doc):
    # This was labeled "<f8" but it is actually "<i4".
    if "pil1M_image" in doc["data_keys"]:
        doc["data_keys"]["pil1M_image"]["dtype_str"] = "<i4"
    return doc


def patch_resource(doc):
    doc = copy.deepcopy(doc)
    kwargs = doc.get("resource_kwargs", {})
    root = doc.get("root", "")
    if not doc["resource_path"].startswith(root):
        doc["resource_path"] = os.path.join(root, doc["resource_path"])
    doc["root"] = ""
    doc["resource_path"] = doc["resource_path"].replace("/nsls2/data1/smi", "/nsls2/data/smi")
    if frame_per_point := kwargs.pop("frame_per_point", None):
        kwargs["multiplier"] = frame_per_point
    if doc.get("spec") in ["AD_TIFF"]:
        kwargs["template"] = "/" + kwargs["template"].lstrip("/")
        kwargs["join_method"] = "concat"
    return doc


tiled_writing_client_sql = from_uri(
    "https://tiled.nsls2.bnl.gov", api_key=os.environ["TILED_BLUESKY_WRITING_API_KEY_SMI"]
)["smi/migration"]
tw = TiledWriter(tiled_writing_client_sql, batch_size=10000,
                 patches={"resource": patch_resource, "descriptor": patch_descriptor})
tw = BufferingWrapper(tw)
RE.subscribe(tw)

if not IS_QS_WORKER:
    print("\nInitializing Tiled reading client...\nMake sure you check for duo push.")
    tiled_reading_client_sql = from_uri("https://tiled.nsls2.bnl.gov")["smi/migration"]

# --- User metadata cleanup helper (manual only; does not run automatically). ---
try:
    from smi_beamline.plans.metadata_cleanup import RE_MD_WHITELIST, clean_re_md

    print("✓ RE.md cleanup helper exposed (clean_re_md)")
except Exception as _exc:  # noqa: BLE001 -- never let an optional console helper block startup
    print(f"✗ RE.md cleanup helper NOT exposed: "
          f"{type(_exc).__name__}: {_exc}")

# --- Factory: build the beamline devices, with a timed per-module load report (Option C). ---
# make_devices imports the device modules in dependency order, times each, reports ok/fail, and
# returns the namespace they export.  We merge that into globals() so all the device instances and
# plans land in the IPython user namespace for console use and queueserver introspection.
from smi_beamline.devices import _context as _seam
from smi_beamline.instances import make_devices as _make_devices

_ctx = {"RE": _seam.get_re(), "sd": _seam.get_sd(),
        "bec": _seam.get_bec(), "db": _seam.get_db(), "mdsave": mdsave}
_devices_ns = _make_devices(_ctx, verbose=True)
globals().update({_k: _v for _k, _v in _devices_ns.items() if not _k.startswith("_")})

# --- smi-plans queue surface (technique presets + *_from_spec wrappers). ---
# Wire the external smi_plans package: inject THIS namespace (devices + bps/np/Signal/...) into the
# smi_plans modules so their bare-global device references resolve, and merge the curated queue
# surface (smi_plans._qserver.__all__) into globals() so the queueserver introspects the plans and
# the terminal user can call them.  Runs AFTER the factory so the device globals exist; guarded so
# a missing smi-plans package never blocks startup.  See smi-plans/docs/QSERVER_WIRING.md.
try:
    from startup import wire_smi_plans as _wire_smi_plans

    _smi_plans_ns = _wire_smi_plans(globals(), verbose=True)
    globals().update(_smi_plans_ns)
    if _smi_plans_ns:
        print(f"\u2713 smi-plans queue surface exposed ({len(_smi_plans_ns)} plans)")
except Exception as _exc:  # noqa: BLE001 -- never let smi-plans wiring block the session
    print(f"\u2717 smi-plans queue surface NOT exposed: "
          f"{type(_exc).__name__}: {_exc}")

# --- Default scan-naming preprocessor (recorded-field filename templating). ---
# Append the modern replacement for get_scan_md() to RE.preprocessors so EVERY plan run through
# the RunEngine gets its run-scoped sample_name extended with a recorded-field template
# (energy/WAXS-arc/SDD by default), and those fields are read into each data-taking run's primary
# stream for the downstream symlink/readout worker to fill.  The existing RE.md['sample_name']
# (user/proposal prefix) is APPENDED TO, never overwritten.
#
# We pass this module's globals() as the device namespace: tokens are resolved by device VARIABLE
# NAME, so adding/removing signals or whole measurement sets is done entirely in
# smi_beamline.plans.scan_naming (MEASUREMENT_SETS / DEFAULT_SETS) -- THIS call never needs to
# change.  Runs after the factory so the devices exist; guarded so a missing device never blocks
# startup (an unresolved token is simply skipped).
try:
    from smi_beamline.plans.scan_naming import install_default_scan_naming as _install_scan_naming

    _install_scan_naming(_seam.get_re(), globals(), verbose=True)
    print("\u2713 default scan-naming preprocessor installed "
          "(sample_name += recorded-field template)")
except Exception as _exc:  # noqa: BLE001 -- never let naming setup block the session
    print(f"\u2717 default scan-naming preprocessor NOT installed: "
          f"{type(_exc).__name__}: {_exc}")

# --- RE-busy signal (cross-process lock-out flag for the GUI). ---
# Append a preprocessor that holds a "RE is busy" flag high in Redis (db=3, key
# 'swaxsstatus:re_busy') for the duration of every plan, so the out-of-process alignment GUI can
# poll it and disable the small motor moves it would otherwise make while the RunEngine drives the
# beamline.  The flag is heartbeat-refreshed with a short TTL and cleared in a finally, so it can
# never latch (it auto-expires even on a hard kill of the worker).  Plans that hold the RE but do
# NOT move the alignment motors (e.g. pump_waxs/vent_waxs -- minutes of pumping/venting) opt OUT so
# the GUI stays free to align: they yield no_re_busy_lock() first and are also listed in
# DEFAULT_SKIP_PLANS.  Guarded so a Redis hiccup never blocks the session.  See
# smi_beamline.plans.re_status.
try:
    from smi_beamline.plans.re_status import install_re_busy_signal as _install_re_busy

    _install_re_busy(_seam.get_re(), verbose=True)
    print("\u2713 RE-busy signal preprocessor installed "
          "(Redis 'swaxsstatus:re_busy' held while plans run)")
except Exception as _exc:  # noqa: BLE001 -- never let the busy signal block the session
    print(f"\u2717 RE-busy signal preprocessor NOT installed: "
          f"{type(_exc).__name__}: {_exc}")

# --- Managed energy-move preprocessor (feedback-managed large energy moves). ---
# Append a preprocessor so EVERY plan energy move (scans, bps.mv(energy, E), queued multi-edge
# plans) larger than 500 eV is routed through the feedback-managed ``energy_walk`` in 500 eV
# sub-steps -- feedback off -> brake-confirmed move -> per-energy BPM3 range -> flux gate ->
# feedback on -> OVAL settle -> coarse-pitch/roll recentre -- while small moves (<=500 eV, e.g.
# fine scan steps) stay fast as a plain ``set``.  One warning line per large move; silent
# otherwise; leaves feedback ON on any exit.  Live-validated 2.1 -> 16.1 keV up and down.
# Guarded so a BPM3 CA hiccup never blocks the session; ``disable_managed_energy_moves()`` removes
# it at the console.  See smi_beamline.plans.energy_move_preprocessor / smi_beamline.instances.energy.
try:
    from smi_beamline.instances.energy import enable_managed_energy_moves as _enable_managed_energy_moves

    _enable_managed_energy_moves()   # prints its own "energy-move preprocessor installed" line
except Exception as _exc:  # noqa: BLE001 -- never let managed energy moves block the session
    print(f"\u2717 managed energy-move preprocessor NOT installed: "
          f"{type(_exc).__name__}: {_exc}")

# --- Human-run EPU lookup-table calibration plan. ---
# Expose explicitly so terminal users and queueserver introspection can find it.  The plan writes a
# dated candidate table to mdsave only; it never overwrites the production IVU lookup-table config.
try:
    from smi_beamline.plans.epu_calibration import calibrate_epu_lookup, EPUCalibrationLivePlot

    print("\u2713 EPU calibration plan exposed (calibrate_epu_lookup)")
except Exception as _exc:  # noqa: BLE001 -- never let an optional commissioning plan block startup
    print(f"\u2717 EPU calibration plan NOT exposed: "
          f"{type(_exc).__name__}: {_exc}")

# --- Human-run attenuator effective-thickness calibration plan. ---
try:
    from smi_beamline.plans.attenuator_calibration import attenuator_thickness_calibration

    print("\u2713 Attenuator calibration plan exposed (attenuator_thickness_calibration)")
except Exception as _exc:  # noqa: BLE001 -- never let an optional commissioning plan block startup
    print(f"\u2717 Attenuator calibration plan NOT exposed: "
          f"{type(_exc).__name__}: {_exc}")

# --- Optional OAV before/after snapshot wrapper. ---
try:
    from smi_beamline.plans.oav_snapshot import oav_snapshot, with_oav_snapshots

    print("\u2713 OAV snapshot helpers exposed (oav_snapshot, with_oav_snapshots)")
except Exception as _exc:  # noqa: BLE001 -- never let optional camera helpers block startup
    print(f"\u2717 OAV snapshot helpers NOT exposed: "
          f"{type(_exc).__name__}: {_exc}")

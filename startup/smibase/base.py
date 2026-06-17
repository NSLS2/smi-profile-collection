print(f"Loading {__file__}")
# from datetime import datetime
# from ophyd.signal import EpicsSignalBase, EpicsSignal, DEFAULT_CONNECTION_TIMEOUT
# from redis_json_dict import RedisJSONDict

import nslsii
import os

import time
import datetime
from tiled.client import from_profile
from databroker import Broker
import logging

from IPython import get_ipython
from IPython.terminal.prompts import Prompts, Token
import matplotlib.pyplot as plt

import redis
from redis_json_dict import RedisJSONDict

# Are we running inside the bluesky-queueserver worker (a plain-Python / IPython-kernel process,
# NOT the interactive IPython terminal)?  In the worker ``get_ipython()`` (in an imported module
# like this one) is the real function and returns ``None``, so the IPython-only bits below must be
# guarded.  ``is_re_worker_active()`` is the canonical detector.
try:
    from bluesky_queueserver import is_re_worker_active
    IS_QS_WORKER = bool(is_re_worker_active())
except Exception:
    IS_QS_WORKER = False

# The namespace ``configure_base`` populates with RE/db/bec/sd.  In the terminal this is the live
# IPython user namespace (so the names appear for the user); in the worker there is no IPython
# namespace, so we use a plain dict and re-export the objects as module globals -- ``startup.py``'s
# ``from smibase.base import *`` then lands them in the exec'd profile namespace, which is exactly
# where the queueserver worker looks for ``RE`` (worker.py: ``self._re_namespace.get("RE")``).
_ip = get_ipython()
if _ip is not None and not IS_QS_WORKER:
    _user_ns = _ip.user_ns
else:
    _user_ns = {}

with open("/etc/bluesky/redis.secret", "r") as f:
    redis_secret = f.read().strip()

mdclient = redis.Redis('xf12id2-smi-redis1.nsls2.bnl.gov', db=1, ssl=True, port=6380, password=redis_secret)
mdsave = RedisJSONDict(mdclient,'swaxsmetadata')

# Persistent SAMPLE / HOLDER store (separate Redis db so it never collides with RE.md on db=0
# or the beamline config 'mdsave' on db=1).  Mirrors the mdsave construction above.
# See smi-plans/docs/SAMPLE_SYSTEM_PLAN.md (db=2, prefix 'swaxssamples').
sampleclient = redis.Redis('xf12id2-smi-redis1.nsls2.bnl.gov', db=2, ssl=True, port=6380, password=redis_secret)
samplestore = RedisJSONDict(sampleclient, 'swaxssamples')

# EPHEMERAL RunEngine liveness / status store (db=3).  Deliberately a *separate* db from the
# PERSISTENT config (db=1) and sample (db=2) stores: the keys here are volatile session state
# (e.g. the "RE is busy" lock-out flag the GUI polls) that must NEVER outlive a process and must
# never be swept into config dump/restore tooling.  This is a RAW redis.Redis client (NOT a
# RedisJSONDict) on purpose -- the busy flag is written with a short TTL (SETEX) and refreshed by
# a heartbeat while a plan runs, so it auto-expires if the worker is killed (kill -9 / crash /
# power loss), which RedisJSONDict's persistent-dict abstraction cannot express.  See
# smi_beamline.plans.re_status (key 'swaxsstatus:re_busy').
statusclient = redis.Redis('xf12id2-smi-redis1.nsls2.bnl.gov', db=3, ssl=True, port=6380, password=redis_secret)


# Configure a Tiled writing client
tiled_writing_client = from_profile("nsls2", api_key=os.environ["TILED_BLUESKY_WRITING_API_KEY_SMI"])["smi"]["raw"]
tiled_writing_client.context.http_client.headers['tiled-qos'] = 'acquisition'

class TiledInserter:
    def insert(self, name, doc):
        ATTEMPTS = 20
        error = None
        for _ in range(ATTEMPTS):
            try:
                tiled_writing_client.post_document(name, doc)
            except Exception as exc:
                print("Document saving failure:", repr(exc))
                error = exc
            else:
                break
            time.sleep(2)
        else:
            # Out of attempts
            raise error

tiled_inserter = TiledInserter()

# The function below initializes RE and subscribes tiled_inserter to it.  Pass our namespace dict
# (the live user_ns in the terminal, a plain dict in the worker) and disable the IPython/GUI-only
# extras (magics, matplotlib hooks) when running headless in the worker.
nslsii.configure_base(_user_ns,
               broker_name='smi',
               bec_derivative=True, 
               publish_documents_with_kafka=True,
               magics=not IS_QS_WORKER,
               mpl=not IS_QS_WORKER,
               redis_url="xf12id2-smi-redis1.nsls2.bnl.gov",
               redis_port=6380,
               redis_ssl=True)

# # This is a workaround to enable us subscribe to Kafka publisher, which requires a beamline acronym when calling
# # configuration_base above (ideally, we would just pass tiled_inserter there).
# # Here we unsubsribe the default databroker (with token=0) and then subscribe the tiled_inserter instead.
# RE/bec/sd come from the namespace configure_base just populated.  Assign them as MODULE globals
# so `from smibase.base import *` exposes them (terminal: convenient; worker: this is how RE reaches
# the exec'd profile namespace the queueserver reads).
RE = _user_ns['RE']
bec = _user_ns['bec']
sd = _user_ns['sd']
RE.unsubscribe(0)
RE.subscribe(tiled_inserter.insert)

# Wire the device-class dependency seam (smi_beamline.devices._context) so the ophyd classes can
# reach RE.md (proposal metadata / raw-data dir / data-security tags) and the Redis persistent-config
# dict (mdsave) WITHOUT importing smibase.base at module load.  Must run before the
# smi_beamline.devices device modules (pilatus, prosilica, ...) are imported by the factory.  The
# energy source is added later in smibase/energy.py once the `energy` positioner exists.
#
# Also inject sd/bec/db/sample_store so the instance modules register baselines via
# _context.baseline_register(...) and reach the sample store via the seam (Phase 4).
from smi_beamline.devices import _context as _seam
_seam.configure(run_engine=RE, config_dict=mdsave, sd=sd, bec=bec,
                sample_store=samplestore, status_store=statusclient)

# Tiled READING client uses an interactive Duo push (username=None), which a headless worker
# cannot satisfy -- skip it in the worker (the worker writes via the API-keyed writing client and
# does not need the interactive reading client / Broker).  db is None in the worker.
if not IS_QS_WORKER:
    print("\nInitializing Tiled reading client...\nMake sure you check for duo push.")
    tiled_reading_client = from_profile("nsls2", username=None)["smi"]["raw"]
    tiled_reading_client.context.http_client.headers['tiled-qos'] = 'acquisition'
    db = Broker(tiled_reading_client)
else:
    tiled_reading_client = None
    db = None
_seam.configure(db=db)

# set plot properties for 4k monitors
plt.rcParams['figure.dpi']=200

# Setup the path to the secure assets folder for the current proposal
assets_path = f"/nsls2/data/smi/proposals/{RE.md['cycle']}/{RE.md['data_session']}/assets/"

# Disable printing scan info
bec.disable_baseline()

# Populating oLog entries with scans (IPython-only: uses the live user namespace).  Skip headless.
if _ip is not None and not IS_QS_WORKER:
    nslsii.configure_olog(_ip.user_ns, subscribe=True)


logger = logging.getLogger("bluesky")
logger.setLevel("INFO")


class ProposalIDPrompt(Prompts):
    def in_prompt_tokens(self, cli=None):
        data_session = str(RE.md.get('data_session', 'N/A'))
        # strip the leading "pass-" from the data session id
        if data_session.startswith('pass-'):
            data_session = data_session[len('pass-'):]
        project_name = str(RE.md.get('project_name', 'N/A'))
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return [
            (Token.OutPromptNum, "SMI "),          # bold/colored "SMI" tag
            (Token.Prompt, f"{data_session} "),
            (Token.Name.Class, f"{project_name} "),  # project name in its own color
            (Token.Comment, f"{now} "),              # date/time, dimmed
            (Token.Prompt, "["),
            (Token.PromptNum, str(self.shell.execution_count)),
            (Token.Prompt, "]: "),
        ]

# The custom prompt is interactive-terminal chrome -- only install it when there is a real IPython
# shell (skip in the worker / plain Python).
if _ip is not None and not IS_QS_WORKER:
    _ip.prompts = ProposalIDPrompt(_ip)
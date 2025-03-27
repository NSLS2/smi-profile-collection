print(f"Loading {__file__}")
from datetime import datetime
from ophyd.signal import EpicsSignalBase, EpicsSignal
import redis
from redis_json_dict import RedisJSONDict

import nslsii
import redis
import os

import time
from redis_json_dict import RedisJSONDict
from tiled.client import from_profile
from databroker import Broker

timeout = 60
print(f"Setting connection timeout to {timeout}s")
EpicsSignalBase.set_defaults(timeout=timeout, connection_timeout=timeout)

# Configure a Tiled writing client
tiled_writing_client = from_profile("nsls2", api_key=os.environ["TILED_BLUESKY_WRITING_API_KEY_SMI"])["smi"]["raw"]

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

# The function below initializes RE and subscribes tiled_inserter to it
nslsii.configure_base(get_ipython().user_ns,
               "smi",
               bec_derivative=True,
               publish_documents_with_kafka=True)
nslsii.configure_kafka_publisher(RE, "smi")

# This is a workaround to enable us subscribe to Kafka publisher, which requires a beamline acronym when calling
# configuration_base above (ideally, we would just pass tiled_inserter there).
# Here we unsubsribe the default databroker (with token=0) and then subscribe the tiled_inserter instead.
RE.unsubscribe(0)
RE.subscribe(tiled_inserter.insert)

print("\nInitializing Tiled reading client...\nMake sure you check for duo push.")
tiled_reading_client = from_profile("nsls2", username=None)["smi"]["raw"]

db = Broker(tiled_reading_client)

# set plot properties for 4k monitors
plt.rcParams['figure.dpi']=200

# Set the metadata dictionary
RE.md = RedisJSONDict(redis.Redis("info.smi.nsls2.bnl.gov"), prefix="swaxs-")

# Setup the path to the secure assets folder for the current proposal
assets_path = f"/nsls2/data/smi/proposals/{RE.md['cycle']}/{RE.md['data_session']}/assets/"

# Disable printing scan info
bec.disable_baseline()

# Populating oLog entries with scans, comment out to disable
nslsii.configure_olog(get_ipython().user_ns, subscribe=True)

print(f"Loading {__file__}")
# from datetime import datetime
# from ophyd.signal import EpicsSignalBase, EpicsSignal, DEFAULT_CONNECTION_TIMEOUT
# from redis_json_dict import RedisJSONDict

import nslsii
import os

import time
from tiled.client import from_profile
from databroker import Broker
import logging

from IPython import get_ipython
from IPython.terminal.prompts import Prompts, Token
import matplotlib.pyplot as plt




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
               broker_name='smi',
               bec_derivative=True, 
               publish_documents_with_kafka=True,
               redis_url="info.smi.nsls2.bnl.gov",
               redis_prefix="swaxs-")

# # This is a workaround to enable us subscribe to Kafka publisher, which requires a beamline acronym when calling
# # configuration_base above (ideally, we would just pass tiled_inserter there).
# # Here we unsubsribe the default databroker (with token=0) and then subscribe the tiled_inserter instead.
from IPython import get_ipython
RE = get_ipython().user_ns['RE']
bec = get_ipython().user_ns['bec']
RE.unsubscribe(0)
RE.subscribe(tiled_inserter.insert)

print("\nInitializing Tiled reading client...\nMake sure you check for duo push.")
tiled_reading_client = from_profile("nsls2", username=None)["smi"]["raw"]

db = Broker(tiled_reading_client)

# set plot properties for 4k monitors
plt.rcParams['figure.dpi']=200

# Setup the path to the secure assets folder for the current proposal
assets_path = f"/nsls2/data/smi/proposals/{RE.md['cycle']}/{RE.md['data_session']}/assets/"

# Disable printing scan info
bec.disable_baseline()

# Populating oLog entries with scans, comment out to disable
nslsii.configure_olog(get_ipython().user_ns, subscribe=True)


logger = logging.getLogger("bluesky")
logger.setLevel("INFO")


class ProposalIDPrompt(Prompts):
    def in_prompt_tokens(self, cli=None):
        return [
            (
                Token.Prompt,
                f"{RE.md.get('data_session', 'N/A')} {RE.md.get('project_name', 'N/A')} [",
            ),
            (Token.PromptNum, str(self.shell.execution_count)),
            (Token.Prompt, "]: "),
        ]

ip = get_ipython()
ip.prompts = ProposalIDPrompt(ip)
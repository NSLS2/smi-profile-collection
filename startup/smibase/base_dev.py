print(f"Loading {__file__}")

import os
from tiled.client import from_uri
from bluesky.callbacks.tiled_writer import TiledWriter
from copy import deepcopy

from IPython import get_ipython
RE = get_ipython().user_ns['RE']
RE.md["tiled_access_tags"] = [RE.md['data_session']]

# This is a hack to insert a slash in the filepath.
# TODO: Remove this when Bluesky is updated > 1.14.2
def patch_resource(doc):
    doc = deepcopy(doc)
    doc['resource_kwargs']['template'] = '/' + doc['resource_kwargs']['template']
    return doc

# Configure a Tiled writing client
tiled_writing_client_dev = from_uri("https://tiled-dev.nsls2.bnl.gov", api_key=os.environ["TILED_BLUESKY_WRITING_API_KEY_SMI"])#["smi/dev"]
tw = TiledWriter(tiled_writing_client_dev, batch_size=1, patches = {'resource': patch_resource})

RE.subscribe(tw)

print("\nInitializing Tiled reading client...\nMake sure you check for duo push.")
tiled_reading_client_dev = from_uri("https://tiled-dev.nsls2.bnl.gov")#["smi/dev"]

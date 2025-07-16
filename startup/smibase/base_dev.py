print(f"Loading {__file__}")

import os
from tiled.client import from_uri
from bluesky.callbacks.tiled_writer import TiledWriter

# Configure a Tiled writing client
tiled_writing_client_dev = from_uri("https://tiled-dev.nsls2.bnl.gov", api_key=os.environ["TILED_BLUESKY_WRITING_API_KEY_SMI"])#["smi/dev"]
tw = TiledWriter(tiled_writing_client_dev, batch_size=1)

RE.subscribe(tw)

print("\nInitializing Tiled reading client...\nMake sure you check for duo push.")
tiled_reading_client_dev = from_uri("https://tiled-dev.nsls2.bnl.gov")#["smi/dev"]

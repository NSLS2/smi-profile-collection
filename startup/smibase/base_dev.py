# print(f"Loading {__file__}")

# import os
# from tiled.client import from_uri
# from bluesky.callbacks.tiled_writer import TiledWriter
# import copy

# from IPython import get_ipython
# RE = get_ipython().user_ns['RE']
# RE.md["tiled_access_tags"] = [RE.md['data_session']]


# def patch_resource(doc):
#     doc = copy.deepcopy(doc)

#     resource_kwargs = doc['resource_kwargs']
#     resource_kwargs['template'] = '/' + resource_kwargs['template']

#     if frame_per_point := resource_kwargs.pop('frame_per_point', None):
#         resource_kwargs['multiplier'] = frame_per_point

#     if "chunk_shape" not in resource_kwargs.keys():
#         resource_kwargs['chunk_shape'] = (1,)

#     resource_kwargs['join_method'] = 'concat'

#     return doc

# # Configure a Tiled writing client
# tiled_writing_client_dev = from_uri("https://tiled.nsls2.bnl.gov", api_key=os.environ["TILED_BLUESKY_WRITING_API_KEY_SMI"])["smi/migration"]
# tw = TiledWriter(tiled_writing_client_dev, batch_size=1, patches = {'resource': patch_resource})

# RE.subscribe(tw)

# print("\nInitializing Tiled reading client...\nMake sure you check for duo push.")
# tiled_reading_client_dev = from_uri("https://tiled.nsls2.bnl.gov")["smi/migration"]

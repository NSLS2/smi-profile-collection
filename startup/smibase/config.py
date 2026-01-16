print(f"Loading {__file__}")

from nslsii.sync_experiment import switch_redis_proposal
from warnings import warn
from IPython import get_ipython
RE = get_ipython().user_ns['RE']

# things to read at begining and end of every scan


from pathlib import Path


def sample_id(user_name="SMI",sample_name='test'):

    sample_name = f'{user_name}_{sample_name}'.translate(
                {ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ =,"})

    RE.md["sample_name"] = sample_name


def proposal_id(cycle_id, proposal_id, analysis=True,*args, **kwargs):
    warn("WARNING: the proposal_id function is deprecated as of data security 2025.\n"
                  "Use proposal_swap(proposal_id) or project_set(project_name) functions.\n "
                  "This will NOT change the project folder, for that call project_set()"
                  "cycle_id is ignored, and proposal_id must be a valid proposal ID\n")
    #project_set(proposal_id)
    proposal_swap(proposal_id)

def proposal_swap(proposal_id):
    RE.md = switch_redis_proposal(proposal_id, beamline='smi', username=RE.md['username'],prefix='swaxs')
    
    # Ensure tiled_access_tags is always a list
    if tags := RE.md.get('tiled_access_tags'):
        if isinstance(tags, str):
            tags = [tags]
        RE.md['tiled_access_tags'] = tags

def project_set(project_name):
    RE.md["project_name"] = project_name




        #XF:12IDB-BI:2{EM:BPM3}fast_pidX.FBON N




### adding this temporarilly until an updated conda environment includes it

# from nslsii.sync_experiment import validate_proposal

# import httpx
# import datetime

# nslsii_api_client = httpx.Client(base_url="https://api.nsls2.bnl.gov")


# def is_commissioning_proposal(proposal_number, beamline) -> bool:
#     """True if proposal_number is registered as a commissioning proposal; else False."""
#     commissioning_proposals_response = nslsii_api_client.get(
#         f"/v1/proposals/commissioning?beamline={beamline}"
#     ).raise_for_status()
#     commissioning_proposals = commissioning_proposals_response.json()[
#         "commissioning_proposals"
#     ]
#     return proposal_number in commissioning_proposals



# def get_current_cycle() -> str:
#     cycle_response = nslsii_api_client.get(
#         f"/v1/facility/nsls2/cycles/current"
#     ).raise_for_status()
#     return cycle_response.json()["cycle"]



# def should_they_be_here(username, new_data_session, beamline):
#     user_access_json = nslsii_api_client.get(f"/v1/data-session/{username}").json()

#     if "nsls2" in user_access_json["facility_all_access"]:
#         return True

#     elif beamline.lower() in user_access_json["beamline_all_access"]:
#         return True

#     elif new_data_session in user_access_json["data_sessions"]:
#         return True

#     return False

# class AuthorizationError(Exception): ...

# def switch_proposal(
#     proposal_number,
#     beamline='smi',
#     username=None,
#     ):

#     """Update information in RedisJSONDict for a specific beamline

#     Parameters
#     ----------
#     proposal_number : int or str
#         number of the desired proposal, e.g. `123456`
#     beamline : str
#         normalized beamline acronym, case-insensitive, e.g. `SMI` or `sst`
#     username : str or None
#         login name of the user assigned to the proposal; if None, current user will be kept
#     prefix : str
#         optional prefix to identify a specific endstation, e.g. `opls`

#     Returns
#     -------
#     md : RedisJSONDict
#         The updated redis dictionary.
#     """

#     md = RE.md
#     username = username or md.get("username")

#     new_data_session = f"pass-{proposal_number}"
#     if (new_data_session == md.get("data_session")) and (
#         username == md.get("username")
#     ):
#         warn(
#             f"Experiment {new_data_session} was already started by the same user."
#         )

#     else:

#         if not should_they_be_here(username, new_data_session, beamline):
#             raise AuthorizationError(
#                 f"User '{username}' is not allowed to take data on proposal {new_data_session}"
#             )

#         proposal_data = validate_proposal(new_data_session, beamline)
#         users = proposal_data.pop("users")
#         pi_name = ""
#         for user in users:
#             if user.get("is_pi"):
#                 pi_name = (
#                     f'{user.get("first_name", "")} {user.get("last_name", "")}'.strip()
#                 )

#         md["data_session"] = new_data_session
#         md["start_datetime"] = datetime.datetime.now().isoformat()
#         md["cycle"] = (
#             "commissioning"
#             if is_commissioning_proposal(str(proposal_number), beamline)
#             else get_current_cycle()
#         )
#         md["proposal"] = {
#             "proposal_id": proposal_data.get("proposal_id"),
#             "title": proposal_data.get("title"),
#             "type": proposal_data.get("type"),
#             "pi_name": pi_name,
#         }

#         print(f"Started experiment {md['data_session']} by {md['username']}.")

#     return md





# #### end of temporary code - delete when conda environment is updated




print(f"Loading {__file__}")

from genericpath import exists
from ophyd import EpicsMotor, EpicsSignalRO, EpicsSignal, Device, Component as Cpt
import os
from nslsii.sync_experiment import sync_experiment

# things to read at begining and end of every scan
sd.baseline.extend([energy, pil1m_pos, stage,  prs, piezo,  ring.current, xbpm2, xbpm3])

sd.baseline.extend([ls, xbpm1_pos, xbpm2_pos, xbpm3_pos, dcm_config, ivugap, bragg, vfm_voltage, hfm_voltage])
sd.baseline.extend([wbs, ssa, eslit, cslit, dsa, SAXS, SBS, MDrive, thorlabs_su])
sd.baseline.extend([hfm, vdm, vfm, crl, pil1m_bs_pd, pil1m_bs_rod, GV7, chamber_pressure])

sd.baseline.extend([att1_1, att1_2, att1_3, att1_4, att1_5, att1_6, att1_7, att1_8, att1_9, att1_10, att1_11, att1_12])
sd.baseline.extend([att2_1, att2_2, att2_3, att2_4, att2_5, att2_6, att2_7, att2_8, att2_9, att2_10, att2_11, att2_12])


from pathlib import Path



def sample_id(user_name="SMI",sample_name='test'):

    sample_name = f'{user_name}_{sample_name}'.translate(
                {ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ =,"})

    RE.md["sample_name"] = sample_name


### adding this temporarilly until an updated conda environment includes it

from nslsii.sync_experiment import validate_proposal

import httpx
import datetime

nslsii_api_client = httpx.Client(base_url="https://api.nsls2.bnl.gov")


def is_commissioning_proposal(proposal_number, beamline) -> bool:
    """True if proposal_number is registered as a commissioning proposal; else False."""
    commissioning_proposals_response = nslsii_api_client.get(
        f"/v1/proposals/commissioning?beamline={beamline}"
    ).raise_for_status()
    commissioning_proposals = commissioning_proposals_response.json()[
        "commissioning_proposals"
    ]
    return proposal_number in commissioning_proposals



def get_current_cycle() -> str:
    cycle_response = nslsii_api_client.get(
        f"/v1/facility/nsls2/cycles/current"
    ).raise_for_status()
    return cycle_response.json()["cycle"]



def should_they_be_here(username, new_data_session, beamline):
    user_access_json = nslsii_api_client.get(f"/v1/data-session/{username}").json()

    if "nsls2" in user_access_json["facility_all_access"]:
        return True

    elif beamline.lower() in user_access_json["beamline_all_access"]:
        return True

    elif new_data_session in user_access_json["data_sessions"]:
        return True

    return False

class AuthorizationError(Exception): ...

def switch_proposal(
    proposal_number,
    beamline='smi',
    username=None,
    ):

    """Update information in RedisJSONDict for a specific beamline

    Parameters
    ----------
    proposal_number : int or str
        number of the desired proposal, e.g. `123456`
    beamline : str
        normalized beamline acronym, case-insensitive, e.g. `SMI` or `sst`
    username : str or None
        login name of the user assigned to the proposal; if None, current user will be kept
    prefix : str
        optional prefix to identify a specific endstation, e.g. `opls`

    Returns
    -------
    md : RedisJSONDict
        The updated redis dictionary.
    """

    md = RE.md
    username = username or md.get("username")

    new_data_session = f"pass-{proposal_number}"
    if (new_data_session == md.get("data_session")) and (
        username == md.get("username")
    ):
        warnings.warn(
            f"Experiment {new_data_session} was already started by the same user."
        )

    else:

        if not should_they_be_here(username, new_data_session, beamline):
            raise AuthorizationError(
                f"User '{username}' is not allowed to take data on proposal {new_data_session}"
            )

        proposal_data = validate_proposal(new_data_session, beamline)
        users = proposal_data.pop("users")
        pi_name = ""
        for user in users:
            if user.get("is_pi"):
                pi_name = (
                    f'{user.get("first_name", "")} {user.get("last_name", "")}'.strip()
                )

        md["data_session"] = new_data_session
        md["start_datetime"] = datetime.datetime.now().isoformat()
        md["cycle"] = (
            "commissioning"
            if is_commissioning_proposal(str(proposal_number), beamline)
            else get_current_cycle()
        )
        md["proposal"] = {
            "proposal_id": proposal_data.get("proposal_id"),
            "title": proposal_data.get("title"),
            "type": proposal_data.get("type"),
            "pi_name": pi_name,
        }

        print(f"Started experiment {md['data_session']} by {md['username']}.")

    return md





#### end of temporary code - delete when conda environment is updated





def proposal_id(cycle_id, proposal_id, analysis=True,*args, **kwargs):
    warnings.warn("WARNING: the proposal_id function is deprecated as of data security 2025.\n"
                  "Use the new proposal_swap or project_set functions.\n "
                  "This will NOT change the proposal folder, for that call switch_proposal()"
                  "By default, cycle_id is ignored, and proposal_id is interpreted as project_name\n")
    new_project(proposal_id)

def new_project(project_name):
    RE.md["project_name"] = project_name


def beamline_mode(mode=None):
    allowed_modes = ["sulfur", "hard"]
    assert (
        mode in allowed_modes
    ), f'Wrong mode: {mode}, must choose: {" or ".join(allowed_modes)}'
    if mode == "hard":
        hfm.y.move(3.4)  # 3.6 for Rh stripe 11.6 for Pt
        hfm.x.move(-0.0)
        hfm.th.move(-0.1746)  # -0.1746 for Rh stripe
        vfm.x.move(3.9)
        vfm.y.move(-3)
        vfm.th.move(-0.216)
        vdm.x.move(4.5)
        vdm.th.move(-0.2174)
        vdm.y.move(-2.44)
    elif mode == "sulfur":
        hfm.y.move(-12.4)
        hfm.x.move(-0.055)
        hfm.th.move(-0.1751)
        vfm.x.move(-11.7)
        vfm.y.move(-4.7)
        vfm.th.move(-0.35)
        vdm.x.move(-11.7)
        vdm.th.move(-0.36)
        vdm.y.move(-2.014)


def fly_scan(det, motor, cycle=1, cycle_t=10, phi=-0.6):
    start = phi + 40
    stop = phi - 40
    acq_time = cycle * cycle_t
    yield from bps.mv(motor, start)
    # yield from bps.mv(attn_shutter, 'Retract')
    det.stage()
    det.cam.acquire_time.put(acq_time)
    print(f"Acquire time before staging: {det.cam.acquire_time.get()}")
    st = det.trigger()
    for i in range(cycle):
        yield from list_scan([], motor, [start, stop])
    while not st.done:
        pass
    det.unstage()
    print(f"We are done after {acq_time}s of waiting")
    # yield from bps.mv(attn_shutter, 'Insert')


manual_PID_disable_pitch = energy.pitch_feedback_disabled
manual_PID_disable_roll = energy.roll_feedback_disabled


def feedback(action=None):
    allowed_actions = ["on", "off"]
    assert (
        action in allowed_actions
    ), f'Wrong action: {action}, must choose: {" or ".join(allowed_actions)}'
    if action == "off":
        manual_PID_disable_pitch.set("1")
        manual_PID_disable_roll.set("1")
    elif action == "on":
        manual_PID_disable_pitch.set("0")
        manual_PID_disable_roll.set("0")

        #XF:12IDB-BI:2{EM:BPM3}fast_pidX.FBON N


def read_current_config_position():
    current_config = {
        "config_names": "current",
        "hfm_y": hfm.y.position,
        "hfm_x": hfm.x.position,
        "hfm_th": hfm.th.position,
        "vfm_y": vfm.y.position,
        "vfm_x": vfm.x.position,
        "vfm_th": vfm.th.position,
        "vdm_y": vdm.y.position,
        "vdm_x": vdm.x.position,
        "vdm_th": vdm.th.position,
        "ssa_h": ssa.h.position,
        "ssa_hg": ssa.hg.position,
        "ssa_v": ssa.v.position,
        "ssa_vg": ssa.vg.position,
        "cslit_h": cslit.h.position,
        "cslit_hg": cslit.hg.position,
        "cslit_v": cslit.v.position,
        "cslit_vg": cslit.vg.position,
        "eslit_h": eslit.h.position,
        "eslit_hg": eslit.hg.position,
        "eslit_v": eslit.v.position,
        "eslit_vg": eslit.vg.position,
        "crl_lens1": crl.lens1.position,
        "crl_lens2": crl.lens2.position,
        "crl_lens3": crl.lens3.position,
        "crl_lens4": crl.lens4.position,
        "crl_lens5": crl.lens5.position,
        "crl_lens6": crl.lens6.position,
        "crl_lens7": crl.lens7.position,
        "crl_lens8": crl.lens8.position,
        "dsa_x": dsa.x.position,
        "dsa_y": dsa.y.position,
        "energy": energy.energy.position,
        "dcm_height": dcm_config.height.position,
        "dcm_pitch": dcm_config.pitch.position,
        "dcm_roll": dcm_config.roll.position,
        "dcm_theta": dcm_config.theta.position,
        "dcm_harmonic": dcm.target_harmonic.value,
        "ztime": time.ctime(),
    }
    return current_config


def create_config_mode(mode_name):
    SMI_CONFIG_FILENAME = "/home/xf12id/smi/config/smi_setup.csv"

    # collect the current positions of motors
    new_config = read_current_config_position()

    new_config_DF = pds.DataFrame(data=new_config, index=[1])
    new_config_DF.at[1, "config_names"] = mode_name

    # load the previous config file
    smi_config = pds.read_csv(SMI_CONFIG_FILENAME)
    smi_config_update = smi_config.append(new_config_DF, ignore_index=True, sort=False)

    # save to file
    if mode_name not in smi_config.config_names.values:
        smi_config_update.to_csv(SMI_CONFIG_FILENAME, index=False)
    else:
        raise Exception("configuration already existing")


def compare_config(mode_name):
    SMI_CONFIG_FILENAME = "/home/xf12id/smi/config/smi_setup.csv"
    smi_config = pds.read_csv(SMI_CONFIG_FILENAME)
    smi_config = pds.DataFrame(data=smi_config)

    # collect the current positions of motors
    current_config = pds.DataFrame(
        data=read_current_config_position(), index=[1]
    ).sort_index(axis=1)

    if mode_name not in smi_config.config_names.values:
        raise Exception("configuration not existing")
    else:
        new_config = smi_config[smi_config.config_names == mode_name]

    i = 0
    for current_con, new_con, ind in zip(
        current_config.iloc[0], new_config.iloc[0], new_config
    ):
        if ind == "config_names":
            print("The new configuration is %s" % (new_con))
        elif ind != "ztime":
            if abs(current_con - new_con) > 0.001:
                print(
                    "difference in %s: the current value is %4.3f, the new one is %4.3f"
                    % (ind, current_con, new_con)
                )
                i += 1

    if i == 0:
        raise Exception("The configuration is simillar. No motor positions changed")


def update_config_mode(mode_name, motor_name=None, motor_value=None):
    SMI_CONFIG_FILENAME = "/home/xf12id/smi/config/smi_setup.csv"
    smi_config = pds.read_csv(SMI_CONFIG_FILENAME)
    smi_config = pds.DataFrame(data=smi_config)

    if mode_name not in smi_config.config_names.values:
        raise Exception("configuration not existing")
    else:
        # Select the row
        upd_config = smi_config[smi_config.config_names == mode_name]
        print(upd_config)

        # Upload all the motor position by default
        if motor_name is None:
            # upd_config[motor_name]= motor_value
            print("This is not ready yet")
            pass
        else:
            upd_config[motor_name] = motor_value

        # Erase the configuration and save the new one
        smi_config_update = smi_config[smi_config["config_names"] != mode_name]

        # Save the new one
        smi_config_update = smi_config_update.append(upd_config, ignore_index=True)
        smi_config_update.to_csv(SMI_CONFIG_FILENAME, index=False)


def move_new_config(mode_name):
    SMI_CONFIG_FILENAME = "/home/xf12id/smi/config/smi_setup.csv"
    smi_config = pds.read_csv(SMI_CONFIG_FILENAME)
    smi_config = pds.DataFrame(data=smi_config)
    current_config = pds.DataFrame(
        data=read_current_config_position(), index=[1]
    ).sort_index(axis=1)

    if mode_name not in smi_config.config_names.values:
        raise Exception("configuration not existing")

    else:
        smi_new_config = smi_config[smi_config.config_names == mode_name]
        compare_config(mode_name)

        print("Are you sure you really want to move to %s configuration?" % mode_name)
        response = input("    Are you sure? (y/[n]) ")

        if response == "y" or response == "Y":

            feedback("off")

            # load smi new config
            for current_con, new_con, ind in zip(
                current_config.iloc[0], smi_new_config.iloc[0], smi_new_config
            ):
                if ind == "dcm_harmonic" and abs(current_con - new_con) > 0.5:
                    print("dcm_harmonic moved to %s" % new_con)
                    energy.target_harmonic(new_con)

                elif ind == "energy" and abs(current_con - new_con) > 0.5:
                    print("energy moved to %s" % new_con)
                    energy.move(new_con)

                # HFM
                elif ind == "hfm_x" and abs(current_con - new_con) > 0.1:
                    print("hfm_x moved to %s" % new_con)
                    yield from bps.mv(hfm.x, new_con)

                elif ind == "hfm_th" and abs(current_con - new_con) > 0.001:
                    print("hfm_th moved to %s" % new_con)
                    yield from bps.mv(hfm.th, new_con)

                # VFM
                elif ind == "vfm_y" and abs(current_con - new_con) > 0.1:
                    print("vfm_y moved to %s" % new_con)
                    yield from bps.mv(vfm.y, new_con)

                elif ind == "vfm_x" and abs(current_con - new_con) > 0.1:
                    print("vfm_x moved to %s" % new_con)
                    yield from bps.mv(vfm.x, new_con)

                elif ind == "vfm_th" and abs(current_con - new_con) > 0.001:
                    print("vfm_th moved to %s" % new_con)
                    yield from bps.mv(vfm.th, new_con)

                # VDM
                elif ind == "vdm_y" and abs(current_con - new_con) > 0.1:
                    print("vdm_y moved to %s" % new_con)
                    yield from bps.mv(vdm.y, new_con)

                elif ind == "vdm_x" and abs(current_con - new_con) > 0.1:
                    print("vdm_x moved to %s" % new_con)
                    yield from bps.mv(vdm.x, new_con)

                elif ind == "vdm_th" and abs(current_con - new_con) > 0.001:
                    print("vdm_th moved to %s" % new_con)
                    yield from bps.mv(vdm.th, new_con)

                # DCM
                elif ind == "dcm_pitch" and abs(current_con - new_con) > 0.1:
                    print("dcm_pitch moved to %s" % new_con)
                    yield from bps.mv(dcm_config.pitch, new_con)

                elif ind == "dcm_roll" and abs(current_con - new_con) > 0.1:
                    print("dcm_roll moved to %s" % new_con)
                    yield from bps.mv(dcm_config.roll, new_con)

                elif ind == "dcm_height" and abs(current_con - new_con) > 0.1:
                    print("dcm_height moved to %s" % new_con)
                    yield from bps.mv(dcm_config.height, new_con)

                elif ind == "dcm_theta" and abs(current_con - new_con) > 0.1:
                    print("dcm_theta moved to %s" % new_con)
                    yield from bps.mv(dcm_config.theta, new_con)

                # SSA
                elif ind == "ssa_h" and abs(current_con - new_con) > 0.1:
                    print("ssa_h moved to %s" % new_con)
                    yield from bps.mv(ssa.h, new_con)

                elif ind == "ssa_hg" and abs(current_con - new_con) > 0.1:
                    print("ssa_hg moved to %s" % new_con)
                    yield from bps.mv(ssa.hg, new_con)

                elif ind == "ssa_v" and abs(current_con - new_con) > 0.1:
                    print("ssa_v moved to %s" % new_con)
                    yield from bps.mv(ssa.v, new_con)

                elif ind == "ssa_vg" and abs(current_con - new_con) > 0.1:
                    print("ssa_vg moved to %s" % new_con)
                    yield from bps.mv(ssa.vg, new_con)

                # CRLs
                elif ind == "crl_lens1" and abs(current_con - new_con) > 1:
                    print("crl_lens1 moved to %s" % new_con)
                    yield from bps.mv(crl.lens1, new_con)

                elif ind == "crl_lens2" and abs(current_con - new_con) > 1:
                    print("crl_lens2 moved to %s" % new_con)
                    yield from bps.mv(crl.lens2, new_con)

                elif ind == "crl_lens3" and abs(current_con - new_con) > 1:
                    print("crl_lens3 moved to %s" % new_con)
                    yield from bps.mv(crl.lens3, new_con)

                elif ind == "crl_lens4" and abs(current_con - new_con) > 1:
                    print("crl_lens4 moved to %s" % new_con)
                    yield from bps.mv(crl.lens4, new_con)

                elif ind == "crl_lens5" and abs(current_con - new_con) > 1:
                    print("crl_lens5 moved to %s" % new_con)
                    yield from bps.mv(crl.lens5, new_con)

                elif ind == "crl_lens6" and abs(current_con - new_con) > 1:
                    print("crl_lens6 moved to %s" % new_con)
                    yield from bps.mv(crl.lens6, new_con)

                elif ind == "crl_lens7" and abs(current_con - new_con) > 1:
                    print("crl_lens7 moved to %s" % new_con)
                    yield from bps.mv(crl.lens7, new_con)

                elif ind == "crl_lens8" and abs(current_con - new_con) > 1:
                    print("crl_lens8 moved to %s" % new_con)
                    yield from bps.mv(crl.lens8, new_con)

                # cslits
                elif ind == "cslit_h" and abs(current_con - new_con) > 0.01:
                    print("cslit_h moved to %s" % new_con)
                    yield from bps.mv(cslit.h, new_con)

                elif ind == "cslit_hg" and abs(current_con - new_con) > 0.01:
                    print("cslit_hg moved to %s" % new_con)
                    yield from bps.mv(cslit.hg, new_con)

                elif ind == "cslit_v" and abs(current_con - new_con) > 0.01:
                    print("cslit_v moved to %s" % new_con)
                    yield from bps.mv(cslit.v, new_con)

                elif ind == "cslit_vg" and abs(current_con - new_con) > 0.01:
                    print("cslit_vg moved to %s" % new_con)
                    yield from bps.mv(cslit.vg, new_con)

                # eslits
                elif ind == "eslit_h" and abs(current_con - new_con) > 0.01:
                    print("eslit_h moved to %s" % new_con)
                    yield from bps.mv(eslit.h, new_con)

                elif ind == "eslit_hg" and abs(current_con - new_con) > 0.01:
                    print("eslit_hg moved to %s" % new_con)
                    yield from bps.mv(eslit.hg, new_con)

                elif ind == "eslit_v" and abs(current_con - new_con) > 0.01:
                    print("eslit_v moved to %s" % new_con)
                    yield from bps.mv(eslit.v, new_con)

                elif ind == "eslit_vg" and abs(current_con - new_con) > 0.01:
                    print("eslit_vg moved to %s" % new_con)
                    yield from bps.mv(eslit.vg, new_con)

                # dsa
                elif ind == "dsa_x" and abs(current_con - new_con) > 0.1:
                    print("dsa_x moved to %s" % new_con)
                    # yield from bps.mv(dsa.x, new_con)

                elif ind == "dsa_y" and abs(current_con - new_con) > 0.1:
                    print("dsa_y moved to %s" % new_con)
                    # yield from bps.mv(dsa.y, new_con)

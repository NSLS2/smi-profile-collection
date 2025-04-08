
print(f"Loading {__file__}")

from ..smiclasses.beamstop import SAXSBeamStops
from time import ctime



saxs_bs = SAXSBeamStops("XF:12IDC-ES:2{BS:SAXS-Ax:", name="detector_saxs_bs_rod")



def beamstop_save():
    """
    Save the current configuration
    """
    # TODO: ELIOT - change save to redis

    # SMI_CONFIG_FILENAME = os.path.join(
    #     get_ipython().profile_dir.location, "smi_config.csv"
    # )

    # Beamstop position in x and y
    bs_rod_x = saxs_bs.x_rod.position
    bs_rod_y = saxs_bs.y_rod.position

    bs_pin_x = saxs_bs.x_pin.position
    bs_pin_y = saxs_bs.y_pin.position

    # collect the current positions of motors
    current_config = {
        "bs_rod_x": bs_rod_x,
        "bs_rod_y": bs_rod_y,
        "bs_pin_x": bs_pin_x,
        "bs_pin_y": bs_pin_y,
        "time": ctime(),
    }

    # TODO - append config to redis


    print(current_config)


def beamstop_load():
    """
    load the configuration file
    """
    #TODO - load the latest positions from the redis record
    # bs_pos_x = smi_config.bs_pos_x.values[-1]
    # bs_pos_y = smi_config.bs_pos_y.values[-1]
    # pdbs_pos_x = smi_config.pdbs_pos_x.values[-1]
    # pdbs_pos_y = smi_config.pdbs_pos_y.values[-1]
    # positions
    return bs_rod_x, bs_rod_y, bs_pin_x, bs_pin_y


bs_rod_x, bs_rod_y, bs_pin_x, bs_pin_y= beamstop_load()


from .base import sd

sd.baseline.extend([saxs_bs])

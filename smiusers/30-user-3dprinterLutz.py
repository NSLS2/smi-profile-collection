# Do not forget to chang the sample name. Also do not make it too many characters!
names = ["20190425_10mms45psi.5sh0.117w6bar4_5"]
# names=['Kapton_test_25micron_waxs0']
height = 0.117  # mm shift from the nozzle
# waxs arc angle: 0 for the detector centered and 6 for the detctor at 6 degrees
# Do not enter a value
waxs_arc = 6  # 0 or 6 or 12

sleep_time = 0


# No need to be modify
det = [pil300KW]

import sys


def track_printer(exp_t=1, meas_t=1, trigger_num=1):

    if waxs_arc != 0 and waxs_arc != 6 and waxs_arc != 12:
        sys.exit("You entered a wrong value for the waxs arc")

    # Aligne the sample
    yield from sample_alignment()

    monitor_pv = EpicsSignal("XF:11ID-CT{M1}bi2", name="monitor_pv")
    ready_for_trigger_pv = EpicsSignal("XF:11ID-CT{M1}bi3", name="ready_for_trigger_pv")
    trigger_signal_pv = EpicsSignal("XF:11ID-CT{M1}bi4", name="trigger_signal")

    trigger_count = 0
    while monitor_pv.get() == 1:
        if trigger_signal_pv.get() == 1:  # trigger signal to execute
            print('this is "function_triggered"! \nGoing to trigger detector...')

            trigger_count += 1
            experimental_adjustement()

            yield from data_acquisition(exp_t, meas_t)
            # yield from beam_damage_study(exp_t, sleep_time, meas_t)

            print("function_triggered successfully executed...waiting for next call.")

            if trigger_count >= trigger_num:
                yield from bps.mv(trigger_signal_pv, 0)
                break
                print("number of requested triggers reached, stopping monitoring...")
            else:
                pass

        yield from bps.sleep(0.5)
        print("monitoring trigger signal")

    # Post printing WAXS measurment
    # det_exposure_time(1)

    # yield from data_acquisition(1, 1)

    # yield from bps.mv(waxs, 8.8)
    # yield from data_acquisition(1, 1)

    # Come back to the beam on the nozzle
    yield from bps.mvr(stage.y, -height)

    print("Done")


def experimental_adjustement():
    # TODO: What do we want to put in the filename
    name_fmt = "{sample}"

    sample_name = name_fmt.format(sample=names[0])
    sample_id(user_name="EH", sample_name=sample_name)


def sample_alignment():
    """
    Alignement of the height to the substrate film interface
    """
    sample_id(user_name="test", sample_name="test")

    yield from bps.mv(GV7.open_cmd, 1)
    smi = SMI_Beamline()
    yield from smi.modeAlignment()
    if waxs.arc.position < 12:
        yield from bps.mv(waxs, 12)

    yield from smi.setDirectBeamROI()

    # move to the substrate interface
    yield from align_height_hexa(0.40, 30, der=True)

    # Move the beam to the middle of the film
    yield from bps.mvr(stage.y, height)

    if waxs.arc.position > 8:
        yield from bps.mv(waxs, waxs_arc)

    yield from smi.modeMeasurement()
    yield from bps.mv(GV7.close_cmd, 1)

    # Relative move of the nozzle
    # yield from bps.mvr(stage.x, x_offset)


def align_height_hexa(rang=0.3, point=31, der=False):
    det_exposure_time(0.5, 0.5)
    yield from bp.rel_scan([pil1M], stage.y, -rang, rang, point)
    ps(der=der)
    yield from bps.mv(stage.y, ps.cen)
    plt.close("all")


def align_x_hexa(rang=0.3, point=31, der=False):
    det_exposure_time(0.5, 0.5)
    yield from bp.rel_scan([pil1M], stage.x, -rang, rang, point)
    # yield from bps.mv(stage.y, ps.cen)


"""       
def align_theta_hexa(rang = 0.1, point = 20, der=False):   
        det_exposure_time(0.5)
        yield from bp.rel_scan([pil1M], stage.th, 0, rang, point )
        ps(der=der)
        #yield from bps.mv(stage.y, ps.cen)
        #plt.close('all')
"""


def data_acquisition(exp_t, meas_t):
    """
    Meas_t: exposition time in second
    num: number of images
    """

    det_exposure_time(exp_t, meas_t)
    yield from bp.count(det, num=1)


def nozzle_alignment():
    """
    Alignement of the height to the substrate film interface
    """
    sample_id(user_name="test", sample_name="test")

    yield from bps.mv(GV7.open_cmd, 1)
    smi = SMI_Beamline()
    yield from smi.modeAlignment()
    if waxs.arc.position < 12:
        yield from bps.mv(waxs, 12)

    yield from smi.setDirectBeamROI()

    # Find the center of the nozzle
    yield from align_x_hexa(0.8, 40, der=False)

    if waxs.arc.position > 8:
        yield from bps.mv(waxs, waxs_arc)

    yield from smi.modeMeasurement()
    yield from bps.mv(GV7.close_cmd, 1)


def beam_damage_study(exp_time, sleep_time, meas_time):
    """
    exp_time: exposure time
    sleep_time: sleeping time
    """
    it = np.int(meas_time / (exp_time + sleep_time))
    det_exposure_time(exp_t, meas_t)
    yield from bp.count(det, num=it, delay=sleep_time)


# TODO: Try this function
def scan_fil_height(exp_time, rang, nb_point):
    det_exposure_time(exp_time, exp_time)
    yield from bp.rel_scan(det, stage.y, -rang, rang, point)

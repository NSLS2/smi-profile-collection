# Do not forget to chang the sample name. Also do not make it too many characters!

names = ["ECD_2.5mms5psi2_h118w13bar23_8"]
# names=['ECD_2.5mms5psi2_69B_h650w0bar11_3']
height = 0.059  # mm shift from the nozzle this is half the filament width, which we call h in the name
# waxs arc angle: 0 for the detector centered and 6 for the detctor at 6 degrees
# Do not enter a value
waxs_arc = 13

# 0 or 6.5 or 13g

# No need to be modify
det = [pil300KW, pil1M]

import sys
import time


def track_printer(exp_t=1, meas_t=10, trigger_num=1):

    # Align the sample
    # yield from sample_alignment()

    if waxs.arc.position < 6 and waxs.x.position > -20:
        sys.exit("You moved waxs arc and not waxs ")

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


def track_printer_timeRes(exp_t=0.1, meas_t=8, trigger_num=1):

    # Aligne the sample
    # yield from sample_alignment()

    if waxs.arc.position < 6 and waxs.x.position > -20:
        sys.exit("You moved waxs arc and not waxs ")

    monitor_pv = EpicsSignal("XF:11ID-CT{M1}bi2", name="monitor_pv")
    ready_for_trigger_pv = EpicsSignal("XF:11ID-CT{M1}bi3", name="ready_for_trigger_pv")
    trigger_signal_pv = EpicsSignal("XF:11ID-CT{M1}bi4", name="trigger_signal")

    trigger_count = 0
    while monitor_pv.get() == 1:
        if trigger_signal_pv.get() == 1:  # trigger signal to execute
            print('this is "function_triggered"! \nGoing to trigger detector...')

            trigger_count += 1
            experimental_adjustement()

            # initial dynamics
            yield from data_acquisition(
                exp_t, meas_t
            )  # controlled by input to track_printer_timeRes

            # longtime dynamics
            t0 = time.time()
            t1 = time.time()
            waxs_arc = [0, 13, 3]
            dets = [pil300KW, pil1M]
            meas_t = 1
            det_exposure_time(meas_t, meas_t)
            loopNum = 0
            while t1 - t0 <= 1800:  # total experimental time after initial dynamics
                # yield from bps.sleep(sleep_time) #sleep_time is 29 s between exposures
                yield from bp.scan(dets, waxs, *waxs_arc)
                t1 = time.time()
                print("total elapsed time and loop number")
                print(t1 - t0)
                loopNum = loopNum + 1
                print(loopNum)
                # timing = timing + exp_t + sleep_time

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
    sample_id(user_name="ED", sample_name=sample_name)


def sample_alignment():
    """
    Alignement of the height to the substrate film interface
    """
    sample_id(user_name="test", sample_name="test")

    smi = SMI_Beamline()
    yield from smi.modeAlignment()
    if waxs.arc.position < 6:
        yield from bps.mv(waxs, 6)

    yield from smi.setDirectBeamROI()

    # move to the substrate interface
    yield from align_height_hexa(0.40, 30, der=True)

    # Move the beam to the middle of the film
    yield from bps.mvr(stage.y, height)

    yield from bps.mv(waxs, waxs_arc)

    yield from smi.modeMeasurement()

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

    # yield from bps.mv(GV7.open_cmd, 1)
    smi = SMI_Beamline()
    yield from smi.modeAlignment()
    if waxs.arc.position < 12:
        yield from bps.mv(waxs, 12)

    yield from smi.setDirectBeamROI()

    # Find the center of the nozzle
    yield from align_x_hexa(1, 45, der=False)

    if waxs.arc.position > 8:
        yield from bps.mv(waxs, waxs_arc)

    yield from smi.modeMeasurement()
    # yield from bps.mv(GV7.close_cmd, 1 )


def beam_damage_study(exp_time, sleep_time, meas_time):
    """
    exp_time: exposure time
    sleep_time: sleeping time
    """
    it = np.int(meas_time / (exp_time + sleep_time))
    det_exposure_time(exp_time, meas_time)
    yield from bp.count(det, num=it, delay=sleep_time)


# TODO: Try this function
def scan_fil_height(exp_time, rang, nb_point):
    det_exposure_time(exp_time, exp_time)
    yield from bp.rel_scan(det, stage.y, -rang, rang, point)


def ex_situ(meas_t=1):
    x0, y0 = (-61101, 4509.62)  # Bottom left coordinate
    x20, y20 = (52898, 4509.649)  # Bottom right coordinate

    x1, y1 = (x0, 509.610)  # top left coordinate

    sample = "B"
    y_range = [-700, 700, 36]
    waxs_arc = np.linspace(39, 0, 7)
    dets = [pil300KW, pil1M]
    det_exposure_time(meas_t, meas_t)
    name_fmt = "{sample}_{po}_wa{waxs}"  # Sample name _ positions
    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)
        for i, (x, y) in enumerate(
            zip(np.linspace(x0, x20, 20), np.linspace(y0, y20, 20))
        ):
            yield from bps.mv(piezo.x, x)
            yield from bps.mv(piezo.y, y)
            sample_name = name_fmt.format(
                sample=sample, po="%2.2d" % (1 + i), waxs="%2.1f" % wa
            )
            sample_id(user_name="ED", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.rel_scan(dets, piezo.y, *y_range)

        for j, (x, y) in enumerate(
            zip(np.linspace(x0, x20, 20), np.linspace(y0, y20, 20))
        ):
            yield from bps.mv(piezo.x, x - x0 + x1)
            yield from bps.mv(piezo.y, y - y0 + y1)
            sample_name = name_fmt.format(
                sample=sample, po="%2.2d" % (2 + i + j), waxs="%2.1f" % wa
            )
            sample_id(user_name="ED", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.rel_scan(dets, piezo.y, *y_range)


def ex_situ_printer(meas_t=1):
    # x_list = [-32500, -21500, -14500, -3500, 6500, 13500, 21500, 30500, 37500]
    sample_list = ["AK_92_ink_5s_meas_t"]

    # assert len(x_list) == len(sample_list), f'Sample name/position list is borked'

    waxs_arc = [0, 26, 5]
    dets = [pil300KW, pil1M]

    # for x, sample in zip(x_list,sample_list): #loop over samples on bar
    # yield from bps.mv(piezo.x, x)
    det_exposure_time(meas_t, meas_t)

    name_fmt = "{sample}"
    sample_name = name_fmt.format(sample=sample_list[0])
    sample_id(user_name="ED", sample_name=sample_name)
    print(f"\n\t=== Sample: {sample_name} ===\n")

    yield from bp.scan(dets, waxs, *waxs_arc)


def ex_situ_printer_height_profile(meas_t=1):
    y_list = [-2, -2.1, -2.2, -2.3, -2.4, -2.5, -2.6, -2.7, -2.8, -2.9, -2.10, -2.11]
    sample_list = [
        "11_5_hp01",
        "11_5_hp02",
        "11_5_hp03",
        "11_5_hp04",
        "11_5_hp05",
        "11_5_hp06",
        "11_5_hp07",
        "11_5_hp08",
        "11_5_hp09",
        "11_5_hp10",
        "11_5_hp11",
        "11_5_hp012",
    ]

    # assert len(x_list) == len(sample_list), f'Sample name/position list is borked'

    waxs_arc = [0, 13, 3]
    dets = [pil300KW, pil1M]

    for y, sample in zip(y_list, sample_list):  # loop over samples on bar
        yield from bps.mv(stage.y, y)
        det_exposure_time(meas_t, meas_t)

        name_fmt = "{sample}"
        sample_name = name_fmt.format(sample=sample)
        sample_id(user_name="ED", sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")
        yield from bp.scan(dets, waxs, *waxs_arc)


def bkg_bar(meas_t=1):

    sample_list = ["bar23_background"]

    waxs_ar = [0, 13, 3]
    dets = [pil300KW, pil1M]

    det_exposure_time(meas_t, meas_t)

    name_fmt = "{sample}"
    sample_name = name_fmt.format(sample=sample_list[0])
    sample_id(user_name="ED", sample_name=sample_name)
    print(f"\n\t=== Sample: {sample_name} ===\n")

    yield from bp.scan(dets, waxs, *waxs_ar)
    yield from bps.mv(waxs, waxs_arc)

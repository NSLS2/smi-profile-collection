from yaml import scan
from epics import caget, caput


def set_nozzle_0():
    RE.md["nozzle 0"] = [printer.y_bed.user_readback.value, stage.y.user_readback.value]


def get_nozzle_height():
    h = printer.y_bed.user_readback.value - RE.md["nozzle 0"][0]
    return h


def set_platform_0():
    RE.md["platform 0"] = [
        printer.y_bed.user_readback.value,
        stage.y.user_readback.value,
    ]


def get_platform_height():
    h1 = RE.md["platform 0"][0] - printer.y_bed.user_readback.value
    h2 = RE.md["platform 0"][1] - stage.y.user_readback.value
    h = h1 + h2
    return h


def set_nozzle_height(height):
    RE(mv(printer.y_bed, RE.md["nozzle 0"][0] - height))
    RE(mvr(stage.y, height))
    RE.md["nozzle height"] = height


def get_nozzle_height():
    return RE.md["nozzle 0"][0] - printer.y_bed.user_readback.value


def set_beam_height(bheight):
    curr_height = get_platform_height()
    RE(mvr(stage.y, curr_height - bheight))
    RE.md["beam height"] = get_platform_height()


def set_beam_position(beam_x):
    """
    beam_x (float): >0 move to the right (upstream)
                    <0 move to the left (downstream)
    """
    curr_position = RE.md["nozzle_x 0"]
    RE(mv(stage.x, beam_x - curr_position))
    RE.md["beam_x"] = beam_x - curr_position


def set_nozzle_position_0():
    RE.md["nozzle_x 0"] = stage.x.user_readback.value


def get_nozzle_position():
    return stage.x.user_readback.value - RE.md["nozzle_x 0"]


def set_nozzle_position(nozzle_x):
    RE(mv(stage.x, -(RE.md["nozzle_x 0"] - nozzle_x)))
    RE.md["nozzle_x"] = get_nozzle_position()


from ophyd import (
    EpicsMotor,
    PVPositioner,
    Device,
    EpicsSignal,
    EpicsSignalRO,
    PVPositionerPC,
)
from ophyd import Component as Cpt, FormattedComponent, DynamicDeviceComponent as DDC


class Printer_3D(Device):
    """6 axes for 1st gen 3D printer"""

    z_bed = Cpt(EpicsMotor, "Z_bed}Mtr")
    x_bed = Cpt(EpicsMotor, "X_bed}Mtr")
    y_bed = Cpt(EpicsMotor, "Y_bed}Mtr")
    x_head1 = Cpt(EpicsMotor, "X_head1}Mtr")
    x_head2 = Cpt(EpicsMotor, "X_head2}Mtr")
    y_head1 = Cpt(EpicsMotor, "Y_head1}Mtr")


printer = Printer_3D("XF:11IDM2-3D{3D:", name="printer")


def start_acq(dt=0.1, t=5, name="test", sleep=0):
    """
    Start taking images after delay

    Args:
        dt (float): exposure per frame in seconds,
        t (float): total exposure time for all frames, in seconds,
        name (str): sample name,
        sleep (float): delay in seconds between start of the script and data
            aquisition.
    """

    dets = [pil900KW]
    det_exposure_time(dt, t)
    user_name = "RT"
    # Metadata
    e = energy.position.energy / 1000
    wa = waxs.arc.position + 0.001
    wa = str(np.round(float(wa), 2)).zfill(5)

    scan_id = db[-1].start["scan_id"] + 1
    name_fmt = "{sample}_{energy}keV_wa{wax}_id{scan_id}"
    sample_name = name_fmt.format(
        sample=name, energy="%.1f" % e, wax=wa, scan_id=scan_id
    )

    sample_name = sample_name.translate(
        {ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ =,"}
    )
    sample_id(user_name=user_name, sample_name=sample_name)

    yield from bps.sleep(sleep)
    yield from bp.count(dets)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def start_acq_long(dt=0.1, name="test", sleep=0):
    """
    Start taking single images every x seconds

    Press CTRL + C to stop the measurement, then RE.stop() in BlueSky.

    Args:
        dt (float): exposure per frame in seconds,
        name (str): sample name,
        sleep (float): delay in seconds between each image.
    """

    dets = [pil900KW]
    det_exposure_time(dt, dt)
    user_name = "RT"
    # Metadata
    e = energy.position.energy / 1000
    wa = waxs.arc.position + 0.001
    wa = str(np.round(float(wa), 2)).zfill(5)
    t0 = time.time()

    for i in range(500):

        t1 = time.time()
        td = str(np.round(t1 - t0, 1)).zfill(6)
        scan_id = db[-1].start["scan_id"] + 1

        name_fmt = "{sample}_time{td}s_{energy}keV_wa{wax}_id{scan_id}"
        sample_name = name_fmt.format(
            sample=name, td=td, energy="%.1f" % e, wax=wa, scan_id=scan_id
        )
        sample_name = sample_name.translate(
            {ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ =,"}
        )
        sample_id(user_name=user_name, sample_name=sample_name)

        yield from bps.sleep(sleep)
        yield from bp.count(dets)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def triggered_series(dt=0.1, t=5, name="test_print", sleep_=0):
    look_for_trigger = True
    print("waiting for trigger signal")
    while look_for_trigger:
        if caget("XF:11ID-CT{M3}bi2") < 1:
            RE(sleep(0.5))
        else:
            look_for_trigger = False
    caput("XF:11ID-CT{M3}bi2", 0)
    RE(start_acq(dt, t, name, sleep_))


"""EXP 1 - W/IN NOZZLE SECTION"""


def through_nozzle_exp():
    # d_N = 0.222 # "250" um nozzle

    # CAPILLARY SECTION
    radial_resolution = 0.07  # 0.025 for 250um nozzle, 0.07 for 700um nozzle
    height_resolution = 0.10  # 100 um

    height_list = [v * height_resolution for v in range(0, 13)]
    width_list = [v * radial_resolution for v in range(0, 7)]
    exp_time = 0.2  # 0.5 for 250um
    # yield from set_beam_height(0)
    t0 = time.time()
    for h_i in height_list:
        print("moving height to ", h_i, type(h_i))
        yield from bps.mvr(stage.y, -height_resolution)

        for w_j in width_list:
            # - = left, + = right
            x_i = RE.md["nozzle_x 0"] - w_j
            print("moving to x=", x_i)
            yield from bps.mv(stage.x, x_i)
            yield from start_acq_through_nozzle(x_i, h_i, "capillary", exp_time)

    print(f"capillary took {t0 - time.time():.3f} seconds long")

    # TAPERED SECTION
    radial_resolution = 0.1  # 25um
    height_resolution = 0.4  # 100 um

    height_list = [v * height_resolution for v in range(0, 8)]
    width_list = [v * radial_resolution for v in range(0, 13)]

    # yield from set_beam_height(0)
    exp_time = 0.2
    t0 = time.time()
    for h_i in height_list:
        print("moving height to ", h_i, type(h_i))
        yield from bps.mvr(stage.y, -height_resolution)

        for w_j in width_list:
            # - = left, + = right
            x_i = RE.md["nozzle_x 0"] - w_j
            print("moving to x=", x_i)
            yield from bps.mv(stage.x, x_i)
            yield from start_acq_through_nozzle(x_i, h_i, "tapered", exp_time)

    print(f"taper took {t0 - time.time():.3f} seconds long")


def start_acq_through_nozzle(x_i, y_i, section, exp_time):
    """
    Start taking images after delay

    Args:
        dt (float): exposure per frame in seconds,
        t (float): total exposure time for all frames, in seconds,
        name (str): sample name,
        sleep (float): delay in seconds between start of the script and data
            aquisition.
    """

    dets = [pil900KW]
    det_exposure_time(exp_time, exp_time)
    user_name = "RT"
    # Metadata
    e = energy.position.energy / 1000
    wa = waxs.arc.position + 0.001
    wa = str(np.round(float(wa), 2)).zfill(5)

    scan_id = db[-1].start["scan_id"] + 1
    sample_name = f"win_nozzle_wa{wa}_x{x_i:.3f}_y{y_i:.3f}_{section}_id{scan_id}_exp{exp_time:.2f}"

    sample_name = sample_name.translate(
        {ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ =,"}
    )
    sample_id(user_name=user_name, sample_name=sample_name)

    # yield from bps.sleep(0)
    yield from bp.count(dets)

    # ensures no overwrite data
    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


"""EXP - TIME RESOLVED UNDER BEAM"""


def start_printing_below_nozzle(H, beam_x, dt=0.2, t=5):

    assert H > 0

    # assumes print always starts with nozzle on substrate
    set_nozzle_height(H)
    # set_beam_height(-0.3375)
    # set_beam_position(beam_x)
    # RE(sleep(0.5)) # enough time to start deposition macro

    look_for_trigger = True
    # print('waiting for trigger signal')
    # while look_for_trigger:
    #     if caget('XF:11ID-CT{M3}bi2') <1:
    #         RE(sleep(.5))
    #     else: look_for_trigger=False

    # caput('XF:11ID-CT{M3}bi2',0)
    RE(start_acq_below_nozzle(dt, t))


def start_acq_below_nozzle(exp_time, N_imgs, dwell=0):
    """
    Start taking images after delay

    Args:
        dt (float): exposure per frame in seconds,
        t (float): total exposure time for all frames, in seconds,
        name (str): sample name,
        sleep (float): delay in seconds between start of the script and data
            aquisition.
    """

    dets = [pil900KW]
    det_exposure_time(exp_time, exp_time)
    user_name = "RT"
    # Metadata
    e = energy.position.energy / 1000
    wa = waxs.arc.position + 0.001
    wa = str(np.round(float(wa), 2)).zfill(5)
    t0 = time.time()

    for j in range(N_imgs):
        t1 = time.time()
        scan_id = db[-1].start["scan_id"] + 1
        beam_height = RE.md["beam height"]
        nozzle_height = get_nozzle_height()
        beam_x = RE.md["beam_x"]
        td = str(np.round(t1 - t0, 1)).zfill(6)

        print("beam_x", beam_x, type(beam_x))
        # print()
        # sample_name = f'below_nozzle_wa{wa}_id{scan_id}_exp{exp_time:.2f}_bh{beam_height:3.3f}mm_bx{beam_x:3.4f}_nh{get_nozzle_height:3.3f}mm'
        sample_name = f"below_nozzle_wa{wa}_id{scan_id}_exp{exp_time:.2f}_bh{beam_height:3.3f}mm_nh{nozzle_height:3.3f}mm_t{td}"
        print(sample_name)

        sample_name = sample_name.translate(
            {ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ =,"}
        )
        sample_id(user_name=user_name, sample_name=sample_name)

        yield from bps.sleep(dwell)
        yield from bp.count(dets)

    # ensures no overwrite data
    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


"""EXP 2 - ACROSS BEAM"""


def start_acq_across_beam(exp_time, N_imgs, dwell=0):
    """
    Start taking images after delay

    Args:
        dt (float): exposure per frame in seconds,
        t (float): total exposure time for all frames, in seconds,
        name (str): sample name,
        sleep (float): delay in seconds between start of the script and data
            aquisition.
    For SAXS data, add Pil1M detector to dets
    dets = [pil900KW] if waxs.arc.position < 10 else [pil1M, pil900KW]

    """

    dets = [pil900KW]
    det_exposure_time(exp_time, exp_time)
    user_name = "RT"
    # Metadata
    e = energy.position.energy / 1000
    wa = waxs.arc.position + 0.001
    wa = str(np.round(float(wa), 2)).zfill(5)
    t0 = time.time()

    for j in range(N_imgs):
        t1 = time.time()
        scan_id = db[-1].start["scan_id"] + 1
        beam_height = RE.md["beam height"]
        nozzle_height = get_nozzle_height()
        beam_x = RE.md["beam_x"]
        td = str(np.round(t1 - t0, 1)).zfill(6)

        print("beam_x", beam_x, type(beam_x))
        # print()
        # sample_name = f'below_nozzle_wa{wa}_id{scan_id}_exp{exp_time:.2f}_bh{beam_height:3.3f}mm_bx{beam_x:3.4f}_nh{get_nozzle_height:3.3f}mm'
        sample_name = f"acrossBeam_wa{wa}_id{scan_id}_exp{exp_time:.2f}_bh{beam_height:3.3f}mm_nh{nozzle_height:3.3f}mm_t{td}"
        print(sample_name)

        sample_name = sample_name.translate(
            {ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ =,"}
        )
        sample_id(user_name=user_name, sample_name=sample_name)

        yield from bps.sleep(dwell)
        yield from bp.count(dets)

    # ensures no overwrite data
    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


"""EXP 3 - DOWNSTREAM OF NOZZLE"""


def start_acq_downstream_nozzle(exp_time, N_imgs, distance=0, dwell=0):
    """
    Start taking images after delay

    Args:
        dt (float): exposure per frame in seconds,
        t (float): total exposure time for all frames, in seconds,
        name (str): sample name,
        sleep (float): delay in seconds between start of the script and data
            aquisition.
    """

    dets = [pil900KW]
    det_exposure_time(exp_time, exp_time)
    user_name = "RT"
    # Metadata
    e = energy.position.energy / 1000
    wa = waxs.arc.position + 0.001
    wa = str(np.round(float(wa), 2)).zfill(5)
    t0 = time.time()

    for j in range(N_imgs):
        t1 = time.time()
        scan_id = db[-1].start["scan_id"] + 1
        beam_height = RE.md["beam height"]
        nozzle_height = get_nozzle_height()
        beam_x = RE.md["beam_x"]
        td = str(np.round(t1 - t0, 1)).zfill(6)

        print("beam_x", beam_x, type(beam_x))
        # print()
        # sample_name = f'below_nozzle_wa{wa}_id{scan_id}_exp{exp_time:.2f}_bh{beam_height:3.3f}mm_bx{beam_x:3.4f}_nh{get_nozzle_height:3.3f}mm'
        sample_name = f"below_nozzle_wa{wa}_id{scan_id}_exp{exp_time:.2f}_bh{beam_height:3.3f}mm_nh{nozzle_height:3.3f}mm_t{td}"
        print(sample_name)

        sample_name = sample_name.translate(
            {ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ =,"}
        )
        sample_id(user_name=user_name, sample_name=sample_name)

        yield from bps.sleep(dwell)
        yield from bp.count(dets)

    # ensures no overwrite data
    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)

def run_caps_fastRPI(t=1):
    x_list = [6908, 13476, 19764, 26055]  #
    # Detectors, motors:
    dets = [pil1M, pil300KW]
    waxs_range = np.linspace(0, 45.5, 8)
    samples = [
        "LC-O38-6-100Cto40C",
        "LC-O37-7-100Cto40C",
        "LC-O36-9-100Cto40C",
        "LC-O35-8-100Cto40C",
    ]
    #    param   = '16.1keV'
    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    det_exposure_time(t, t)
    for wa in waxs_range:
        yield from bps.mv(waxs, wa)
        for sam, x in zip(samples, x_list):
            yield from bps.mv(piezo.x, x)
            name_fmt = "{sam}_wa{waxs}"
            sample_name = name_fmt.format(sam=sam, waxs="%2.1f" % wa)
            sample_id(user_name=user, sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5)


def run_saxs_linkamRPI(t=1):

    names = ["S66_JA-B5O2-24w-1-04"]
    user = "SL"
    det_exposure_time(t, t)

    y_range = [-4.23, -3.15, 5]

    # Detectors, motors:
    dets = [pil1M]
    # waxs_range = np.linspace(45.5, 0, 8)

    name_fmt = "{sam}"
    sample_name = name_fmt.format(sam=names[0])
    sample_id(user_name=user, sample_name=sample_name)
    print(f"\n\t=== Sample: {sample_name} ===\n")
    yield from bp.scan(dets, stage.y, *y_range)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def run_saxs_cap_temp_2022_2(t=0.5, temp=25):
    """
    Single SAXS measurement

    Linkam capillary stage driven from a laptop with temperature read from Lakeshore.
    Scripts automatically handles attenuators and pin diode current readout.
    """
    y_coord = 1.9
    y_range = [0, 0.6]
    n_points = 1
    name = "A16_NaI"
    user = "HH"
    # name = 'test'
    # user = 'test'

    # Mo 20 um 1x and 2x
    attenuators = [att2_1, att2_2]

    # Insert attenuators, open fast shutter, read pin diode current
    # close fast shutter, remove attenuators
    yield from bps.mv(stage.y, y_coord)

    for att in attenuators:
        yield from bps.mv(att.open_cmd, 1)
        yield from bps.sleep(2)

    fs.open()
    yield from bps.sleep(0.3)
    pd_current = pdcurrent1.get()
    fs.close()

    for att in attenuators:
        yield from bps.mv(att.close_cmd, 1)
        yield from bps.sleep(1)

    det_exposure_time(t, t)
    dets = [pil1M, pdcurrent1]

    # Metadata
    e = energy.position.energy / 1000
    wa = waxs.arc.position
    wa = str(np.round(float(wa), 1)).zfill(4)
    # temp = ls.input_A.get() - 273.15
    # temp = 10
    temp = str(np.round(float(temp), 1)).zfill(5)
    sdd = pil1m_pos.z.position / 1000
    scan_id = db[-1].start["scan_id"] + 1
    # bpm = xbpm3.sumX.get()

    # Sample name
    name_fmt = "{sample}_{energy}keV_{temp}degC_wa{wax}_sdd{sdd}m_id{scan_id}_pd{pd}"
    sample_name = name_fmt.format(
        sample=name,
        energy="%.2f" % e,
        temp=temp,
        wax=wa,
        sdd="%.1f" % sdd,
        scan_id=scan_id,
        pd="%.0f" % pd_current,
    )
    print(f"\n\t=== Sample: {sample_name} ===\n")
    sample_id(user_name=user, sample_name=sample_name)

    yield from bp.rel_scan(dets, stage.y, *y_range, n_points)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def run_contRPI(t=1, numb=100, sleep=5):

    det_exposure_time(t, t)
    dets = [pil1M, pil300KW]
    # dets = [pil300Kw]
    for i in range(numb):
        yield from bp.count(dets, num=1)
        yield from bps.sleep(sleep)


def acq_tem(t=0.2):
    sam = "0122A-11-lk5.5m-1s"

    dets = [pil1M]
    det_exposure_time(t, t)
    temp = ls.ch1_read.value
    name_fmt = "{sam}_{temp}C"
    sample_name = name_fmt.format(sam=sam, temp="%4.1f" % temp)
    sample_id(user_name="LC", sample_name=sample_name)
    yield from bp.scan(dets, stage.y, 5.3, 5.9, 4)


def acq_bd(t=0.2):
    sam = "0122A-10-lk5.5m-0.2s-4"

    dets = [pil1M]
    det_exposure_time(t, t)
    temp = ls.ch1_read.value
    name_fmt = "{sam}_{temp}C"
    sample_name = name_fmt.format(sam=sam, temp="%4.1f" % temp)
    sample_id(user_name="LC", sample_name=sample_name)
    yield from bp.scan(dets, piezo.th, 0, 0, 1)


def run_waxs_linkamRPI_2021_3(t=1):

    names = ["Air"]
    user = "JA"
    det_exposure_time(t, t)

    # Detectors, motors:
    dets = [pil1M]

    name_fmt = "{sam}"
    sample_name = name_fmt.format(sam=names[0])
    sample_id(user_name=user, sample_name=sample_name)
    print(f"\n\t=== Sample: {sample_name} ===\n")

    yield from bp.scan(dets, stage.y, 3.2, 1.9, 6)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def run_waxs_linkamRPI_2022_1(t=1):
    names = ["testtest"]
    time_rec = [0.1, 0.5, 1, 60]
    waxs_range = [20, 0]

    user = "SL"
    det_exposure_time(t, t)

    # Detectors, motors:
    dets = [pil1M, pil900KW]

    t0 = time.time()

    for t in time_rec:
        while (time.time() - t0) < (t * 60):
            yield from bps.sleep(10)

        for wa in waxs_range:
            yield from bps.mv(waxs, wa)
            name_fmt = "{sample}_{time}s"
            sample_name = name_fmt.format(
                sample=names[0], time="%.1f" % (time.time() - t0)
            )
            sample_id(user_name=user, sample_name=sample_name)

            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)

    sample_id(user_name=user, sample_name=sample_name)
    print(f"\n\t=== Sample: {sample_name} ===\n")

    det_exposure_time(0.3, 0.3)

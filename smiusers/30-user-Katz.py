def alignement_katz_2021_1():
    global names, x_piezo, y_piezo, z_piezo, incident_angles, y_piezo_aligned

    names = [
        "sample1",
        "sample2",
        "sample3",
        "sample4",
        "sample5",
        "sample6",
        "sample7",
    ]
    x_piezo = [55000, 42000, 19000, 2000, -16000, -31000, -49000]
    y_piezo = [4800, 2900, 2900, 2900, 2900, 2900, 3300]
    x_hexa = [7, 0, 0, 0, 0, 0, 0]

    incident_angles = [0, 0, 0, 0, 0, 0, 0]
    y_piezo_aligned = [
        4757.703,
        3054.9,
        3133.065,
        3031.989,
        3414.158,
        3546.666,
        3715.74,
    ]

    # sample2: y = 5332.784, th = 0.973826
    # sample 4:: th [2, 0.9738, 2, 0.97, 0.582, 0.297, 0.0655], y: [7100, 5332.784, 5142.4, 4975.875, 5447.996, 5487.398, 5792.193]

    # incident_angles = [2, 0.9738, 2, 0.97, 0.582, 0.297, 0.0655]
    # y_piezo_aligned = [7100, 5332.784, 5142.4, 4975.875, 5447.996, 5487.398, 5792.193]

    smi = SMI_Beamline()
    yield from smi.modeAlignment(technique="gisaxs")

    for name, xs_piezo, ys_piezo, xs_hexa in zip(names, x_piezo, y_piezo, x_hexa):
        yield from bps.mv(stage.x, xs_hexa)

        yield from bps.mv(piezo.x, xs_piezo)
        yield from bps.mv(piezo.y, ys_piezo)
        # yield from alignement_gisaxs(0.3)

        yield from alignement_gisaxs_multisample_special(angle=0.25)

        y_piezo_aligned = y_piezo_aligned + [piezo.y.position]

    yield from smi.modeMeasurement()

    print(incident_angles)


def nexafs_Sedge_Katz(t=1):
    dets = [pil300KW, pil900KW]

    names = [
        "sample1",
        "sample2",
        "sample3",
        "sample4",
        "sample5",
        "sample6",
        "sample7",
    ]
    x_piezo = [55000, 42000, 19000, 2000, -16000, -31000, -49000]
    y_piezo = [4800, 2900, 2900, 2900, 2900, 2900, 3300]
    x_hexa = [7, 0, 0, 0, 0, 0, 0]

    incident_angles = [0, 0, 0, 0, 0, 0, 0]
    y_piezo_aligned = [
        4757.703,
        3054.9,
        3133.065,
        3031.989,
        3414.158,
        3546.666,
        3715.74,
    ]

    energies = 7 + np.asarray(
        np.arange(2445, 2470, 5).tolist()
        + np.arange(2470, 2480, 0.25).tolist()
        + np.arange(2480, 2490, 1).tolist()
        + np.arange(2490, 2501, 5).tolist()
    )
    waxs_arc = [52.5]

    for name, xs, ys, zs, aiss, ys in zip(
        names, x_piezo, y_piezo, z_piezo, incident_angles, y_piezo_aligned
    ):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)
        yield from bps.mv(piezo.th, aiss + 0.7)

        ai0 = piezo.th.position

        yield from bps.mv(waxs, waxs_arc[0])
        det_exposure_time(t, t)
        name_fmt = "nexafs_{sample}_{energy}eV_wa60.0_bpm{xbpm}"
        for e in energies:
            yield from bps.mv(energy, e)
            yield from bps.sleep(1)

            bpm = xbpm2.sumX.value

            sample_name = name_fmt.format(
                sample=name, energy="%6.2f" % e, xbpm="%4.3f" % bpm
            )
            sample_id(user_name="GF", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)

        yield from bps.mv(energy, 2490)
        yield from bps.mv(energy, 2470)
        yield from bps.mv(energy, 2450)


def nexafs_Caedge_Katz(t=1):
    dets = [pil300KW]

    names = ["sample7_1"]

    energies = np.linspace(4030, 4110, 81)
    waxs_arc = [52.5]

    for name in names:

        ai0 = piezo.th.position

        yield from bps.mv(waxs, waxs_arc[0])
        det_exposure_time(t, t)
        name_fmt = "nexafs_{sample}_{energy}eV_wa52.5_ai0.7deg_bpm{xbpm}"
        for e in energies:
            yield from bps.mv(energy, e)
            yield from bps.sleep(1)

            bpm = xbpm2.sumX.value

            sample_name = name_fmt.format(
                sample=name, energy="%6.2f" % e, xbpm="%4.3f" % bpm
            )
            sample_id(user_name="GF", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)

        yield from bps.mv(energy, 4100)
        yield from bps.mv(energy, 4080)
        yield from bps.mv(energy, 4050)


def saxs_14keV_Matt_2021_2(t=1):

    xlocs = [
        44000,
        35000,
        21500,
        11000,
        -1000,
        -12000,
        -23000,
        -36000,
        44000,
        32500,
        21000,
        10000,
        -2000,
        -13500,
    ]
    ylocs = [
        -5000,
        -4500,
        -5000,
        -5000,
        -5000,
        -5000,
        -5000,
        -5000,
        8000,
        8000,
        8000,
        8000,
        8000,
        8000,
    ]
    zlocs = [
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
    ]
    names = [
        "MWET_01",
        "MWET_02",
        "MWET_03",
        "MWET_04",
        "MWET_05",
        "MWET_06",
        "MWET_07a",
        "MWET_07b",
        "MWET_08",
        "MWET_09",
        "MWET_10",
        "MWET_11",
        "MWET_12",
        "MWET_13",
    ]

    user = "ML"
    det_exposure_time(t, t)

    assert len(xlocs) == len(
        names
    ), f"Number of X coordinates ({len(xlocs)}) is different from number of samples ({len(names)})"

    # Detectors, motors:
    dets = [pil300KW, pil900KW, pil1M]
    waxs_range = [0, 2, 19.5, 21.5, 39, 41]

    ypos = [-500, 500, 3]

    for wa in waxs_range[::-1]:
        yield from bps.mv(waxs, wa)
        for sam, x, y, z in zip(names, xlocs, ylocs, zlocs):
            yield from bps.mv(piezo.x, x)
            yield from bps.mv(piezo.y, y)
            yield from bps.mv(piezo.z, z)

            name_fmt = "{sam}_stats1_14.0keV_sdd8.3m_wa{waxs}"
            sample_name = name_fmt.format(sam=sam, waxs="%2.1f" % wa)
            sample_id(user_name=user, sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.rel_scan(dets, piezo.y, *ypos)
            yield from bps.sleep(2)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def saxs_2p4keV_Matt_2021_2(t=1):

    xlocs = [
        44000,
        35000,
        21500,
        11000,
        -1000,
        -12000,
        -23000,
        -36000,
        44000,
        32500,
        21000,
        10000,
        -2000,
        -13500,
    ]
    ylocs = [
        -5000,
        -4500,
        -5000,
        -5000,
        -5000,
        -5000,
        -5000,
        -5000,
        8000,
        8000,
        8000,
        8000,
        8000,
        8000,
    ]
    zlocs = [
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
    ]
    names = [
        "MWET_01",
        "MWET_02",
        "MWET_03",
        "MWET_04",
        "MWET_05",
        "MWET_06",
        "MWET_07a",
        "MWET_07b",
        "MWET_08",
        "MWET_09",
        "MWET_10",
        "MWET_11",
        "MWET_12",
        "MWET_13",
    ]

    user = "ML"
    det_exposure_time(t, t)

    assert len(xlocs) == len(
        names
    ), f"Number of X coordinates ({len(xlocs)}) is different from number of samples ({len(names)})"

    # Detectors, motors:
    dets = [pil300KW, pil900KW, pil1M]
    waxs_range = [0, 2, 19.5, 21.5, 39, 41]

    ypos = [-500, 500, 3]

    for wa in waxs_range[::-1]:
        yield from bps.mv(waxs, wa)
        for sam, x, y, z in zip(names, xlocs, ylocs, zlocs):
            yield from bps.mv(piezo.x, x)
            yield from bps.mv(piezo.y, y)
            yield from bps.mv(piezo.z, z)

            name_fmt = "{sam}_stats1_2.45keV_sdd3.0m_wa{waxs}"
            sample_name = name_fmt.format(sam=sam, waxs="%2.1f" % wa)
            sample_id(user_name=user, sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.rel_scan(dets, piezo.y, *ypos)
            yield from bps.sleep(2)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def nexafs_Sedge_Katz_2021_2(t=1):
    dets = [pil300KW, pil900KW]

    x_piezo = [32500]
    y_piezo = [8000]
    z_piezo = [2700]
    names = ["MWET_09"]

    energies = np.linspace(2450, 2530, 81)
    waxs_arc = [59]

    for name, xs, ys, zs in zip(names, x_piezo, y_piezo, z_piezo):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)

        yield from bps.mv(waxs, waxs_arc[0])
        det_exposure_time(t, t)
        name_fmt = "nexafs_{sample}_{energy}eV_wa59_bpm{xbpm}"
        for e in energies:
            yield from bps.mv(energy, e)
            yield from bps.sleep(2)

            bpm = xbpm2.sumX.value

            sample_name = name_fmt.format(
                sample=name, energy="%6.2f" % e, xbpm="%4.3f" % bpm
            )
            sample_id(user_name="GF", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)

        yield from bps.mv(energy, 2500)
        yield from bps.mv(energy, 2480)
        yield from bps.mv(energy, 2450)


def nexafs_Sedge_Katz_2021_3(t=1):
    dets = [pil300KW, pil900KW]

    x_piezo = [32500]
    y_piezo = [8000]
    z_piezo = [2700]
    names = ["MWET_09"]

    energies = np.linspace(2450, 2530, 81)
    waxs_arc = [59]

    for name, xs, ys, zs in zip(names, x_piezo, y_piezo, z_piezo):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)

        yield from bps.mv(waxs, waxs_arc[0])
        det_exposure_time(t, t)
        name_fmt = "nexafs_{sample}_{energy}eV_wa59_bpm{xbpm}"
        for e in energies:
            yield from bps.mv(energy, e)
            yield from bps.sleep(3)

            bpm = xbpm2.sumX.value

            sample_name = name_fmt.format(
                sample=name, energy="%6.2f" % e, xbpm="%4.3f" % bpm
            )
            sample_id(user_name="GF", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)

        yield from bps.mv(energy, 2500)
        yield from bps.sleep(3)
        yield from bps.mv(energy, 2480)
        yield from bps.sleep(3)
        yield from bps.mv(energy, 2450)
        yield from bps.sleep(3)


def nexafs_Sedge_Katz_2021_2(t=1):
    dets = [pil900KW]

    # names =   ['sample1', 'sample2', 'sample3', 'sample4', 'sample5']
    # x_piezo = [    54000,     38000,     18000,      3000,    -17000]
    # inc_angl = [ -0.6074,   -0.4144,     0.185,   -0.1982,   -2.4638]
    # y_piezo = [  4647.88,   5180.45,   4970.04,    4909.86,  5090.90]

    names = ["sample4_redo"]
    x_piezo = [3200]
    inc_angl = [-0.1982]
    y_piezo = [4890.86]

    energies = 7 + np.asarray(
        np.arange(2445, 2470, 5).tolist()
        + np.arange(2470, 2480, 0.25).tolist()
        + np.arange(2480, 2490, 1).tolist()
        + np.arange(2490, 2501, 5).tolist()
    )
    waxs_arc = 60

    angle_mes = [0.1]

    for name, xs, ys, aiss in zip(names, x_piezo, y_piezo, inc_angl):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.th, aiss)

        yield from bps.mv(waxs, 59)
        det_exposure_time(t, t)

        for angle_me in angle_mes:
            yield from bps.mv(piezo.th, aiss + angle_me)

            name_fmt = "nexafs_{sample}_{energy}eV_wa60_bpm{xbpm}_ai{ai}"
            for e in energies:
                yield from bps.mv(energy, e)
                yield from bps.sleep(2)

                bpm = xbpm2.sumX.value

                sample_name = name_fmt.format(
                    sample=name,
                    energy="%6.2f" % e,
                    xbpm="%4.3f" % bpm,
                    ai="%1.2f" % angle_me,
                )
                sample_id(user_name="GF", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 2490)
            yield from bps.mv(energy, 2470)
            yield from bps.mv(energy, 2450)


def nexafs_Caedge_David(t=1):
    dets = [pil900KW]

    # names =   ['sample1', 'sample2', 'sample3', 'sample4', 'sample5']
    # x_piezo = [    54000,     38000,     18000,      3000,    -17000]
    # inc_angl = [ -0.6074,   -0.4144,     0.185,   -0.1982,   -2.4638]
    # y_piezo = 40 + np.asarray([  4647.88,   5180.45,   4970.04,    4909.86,  5090.90])
    names = ["sample3", "sample4", "sample5"]
    x_piezo = [18000, 3000, -17000]
    inc_angl = [0.185, -0.1982, -2.4638]
    y_piezo = 40 + np.asarray([4970.04, 4909.86, 5090.90])

    # names =   [ 'sample2', 'sample3', 'sample4', 'sample5']
    # x_piezo = [         38000,     18000,      3000,    -17000]
    # inc_angl = [    -0.4144,     0.185,   -0.1982,   -2.4638]
    # y_piezo = 40 + np.asarray([     5180.45,   4970.04,    4909.86,  5090.90])

    # energies = np.linspace(4030, 4110, 81)
    energies = np.asarray(
        np.arange(4020, 4035, 5).tolist()
        + np.arange(4035, 4042, 2).tolist()
        + np.arange(4042, 4070, 0.5).tolist()
        + np.arange(4070, 4080, 2).tolist()
        + np.arange(4080, 4130, 5).tolist()
    )

    for name, xs, ys, aiss in zip(names, x_piezo, y_piezo, inc_angl):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.th, aiss)

        yield from bps.mv(waxs, 59)
        det_exposure_time(t, t)

        angle_mes = [0.1]

        for angle_me in angle_mes:
            yield from bps.mv(piezo.th, aiss + angle_me)

            name_fmt = "nexafs_{sample}_{energy}eV_wa60_ai{ai}_bpm{xbpm}"
            for e in energies:
                yield from bps.mv(energy, e)
                yield from bps.sleep(2)

                bpm = xbpm2.sumX.value

                sample_name = name_fmt.format(
                    sample=name,
                    energy="%6.2f" % e,
                    ai="%1.2f" % angle_me,
                    xbpm="%4.3f" % bpm,
                )
                sample_id(user_name="GF", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 4100)
            yield from bps.mv(energy, 4080)
            yield from bps.mv(energy, 4050)


def nexafs_Caedge_Matt(t=0.5, name="test"):
    yield from bps.mv(waxs, 59)
    dets = [pil900KW]

    energies = np.asarray(
        np.arange(4020, 4035, 5).tolist()
        + np.arange(4035, 4042, 2).tolist()
        + np.arange(4042, 4070, 0.5).tolist()
        + np.arange(4070, 4080, 2).tolist()
        + np.arange(4080, 4140, 5).tolist()
    )

    samples = [
        "mwet_01",
        "mwet_02",
        "mwet_03",
        "mwet_04",
        "mwet_05",
        "mwet_06",
        "mwet_07",
        "mwet_08",
        "mwet_09",
        "mwet_10",
        "mwet_11",
    ]
    x_list = [46000, 35000, 22500, 11000, 0, -12000, -24000, -35000, 24000, 12000, 0]
    y_list = [-8500, -8500, -8500, -8500, -8500, -8500, -8500, -8500, 4500, 4500, 4500]

    for name, x, y in zip(samples, x_list, y_list):
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(piezo.y, y)

        det_exposure_time(t, t)
        name_fmt = "nexafs_{sample}_{energy}eV_wa60_bpm{xbpm}"
        for e in energies:
            yield from bps.mv(energy, e)
            yield from bps.sleep(2)

            bpm = xbpm2.sumX.value
            sample_name = name_fmt.format(
                sample=name, energy="%6.2f" % e, xbpm="%4.3f" % bpm
            )
            sample_id(user_name="GS", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)

        yield from bps.mv(energy, 4110)
        yield from bps.sleep(2)
        yield from bps.mv(energy, 4070)
        yield from bps.sleep(2)
        yield from bps.mv(energy, 4030)
        yield from bps.sleep(2)

        sample_id(user_name="test", sample_name="test")


def saxs_prep_multisample(t=1):
    dets = [pil900KW, pil1M]

    energies = [4030, 4040, 4050, 4055, 4075]
    det_exposure_time(t, t)
    waxs_range = [0, 2, 19.5, 21.5, 39, 41]

    det_exposure_time(t, t)

    xpos = [-500, 500, 3]

    for wa in waxs_range[::-1]:
        yield from bps.mv(waxs, wa)

        samples = [
            "mwet_01",
            "mwet_02",
            "mwet_03",
            "mwet_04",
            "mwet_05",
            "mwet_06",
            "mwet_07",
            "mwet_08",
            "mwet_09",
            "mwet_10",
            "mwet_11",
        ]
        x_list = [
            46000,
            35000,
            22500,
            11000,
            0,
            -12000,
            -24000,
            -35000,
            24000,
            12000,
            0,
        ]
        y_list = 100 + np.asarray(
            [-8500, -8500, -8500, -8500, -8500, -8500, -8500, -8500, 4500, 4500, 4500]
        )

        for name, x, y in zip(samples, x_list, y_list):
            yield from bps.mv(piezo.x, x)
            yield from bps.mv(piezo.y, y)

            for k, e in enumerate(energies):
                yield from bps.mv(energy, e)
                yield from bps.sleep(2)

                yield from bps.mv(piezo.y, y + k * 100)

                name_fmt = "{sample}_{energy}eV_xbpm{xbpm}_wa{wa}"
                bpm = xbpm2.sumX.value

                sample_name = name_fmt.format(
                    sample=name, energy="%6.2f" % e, xbpm="%3.1f" % bpm, wa="%2.1f" % wa
                )
                sample_id(user_name="OS", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.rel_scan(dets, piezo.x, *xpos)

            yield from bps.mv(energy, 4050)
            yield from bps.mv(energy, 4030)


def nexafs_Caedge_Katz_2021_3(t=1):
    dets = [pil900KW]

    # names =   ['ref_calcite', 'ref_cacooh', 'calcium_01', 'calcium_02', 'calcium_03', 'calcium_04', 'calcium_05', 'calcium_06', 'calcium_07', 'calcium_08', 'calcium_09',
    # 'calcium_10', 'calcium_11', 'calcium_12', 'calcium_13','calcium_14']

    # xs = [43000, 33000, 21000, 9500, -1000, -13000, -25000, -36000, 45000, 35000, 29500, 24000, 14000, 2000, -10500, -24000]
    # ys = [ -500,  -500,  -500, -500,  -500,   -500,   -500,  -1500,  2000,  2000,  1500,  1500,  1500, 1500,   1500,   1500]
    # ys_hexa = [-5,  -5,    -5,   -5,    -5,     -5,     -5,     -5,     5,     5,     5,     5,     5,    5,      5,      5]

    names = ["calcium_13"]

    xs = [43000]
    ys = [-500]
    ys_hexa = [-5]

    assert len(xs) == len(
        names
    ), f"Number of X coordinates ({len(xs)}) is different from number of samples ({len(names)})"
    assert len(xs) == len(
        ys
    ), f"Number of X coordinates ({len(xs)}) is different from number of samples ({len(ys)})"
    assert len(xs) == len(
        ys_hexa
    ), f"Number of X coordinates ({len(xs)}) is different from number of samples ({len(ys_hexa)})"

    energies = np.asarray(
        np.arange(4020, 4035, 5).tolist()
        + np.arange(4035, 4042, 2).tolist()
        + np.arange(4042, 4070, 0.5).tolist()
        + np.arange(4070, 4080, 2).tolist()
        + np.arange(4080, 4140, 5).tolist()
    )
    waxs_arc = [50]

    for x, y, y_hexa, name in zip(xs, ys, ys_hexa, names):
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(piezo.y, y)
        yield from bps.mv(stage.y, y_hexa)

        yield from bps.mv(waxs, waxs_arc[0])
        det_exposure_time(t, t)
        name_fmt = "nexafs_{sample}_{energy}eV_wa50_bpm{xbpm}"

        yss = np.linspace(y, y + 500, 80)
        xss = np.linspace(x, x, 1)

        yss, xss = np.meshgrid(yss, xss)
        yss = yss.ravel()
        xss = xss.ravel()

        for e, xsss, ysss in zip(energies, xss, yss):
            yield from bps.mv(energy, e)
            yield from bps.sleep(3)

            yield from bps.mv(piezo.y, ysss)
            yield from bps.mv(piezo.x, xsss)

            bpm = xbpm2.sumX.value

            sample_name = name_fmt.format(
                sample=name, energy="%6.2f" % e, xbpm="%4.3f" % bpm
            )
            sample_id(user_name="GF", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)

        yield from bps.mv(energy, 4100)
        yield from bps.sleep(3)
        yield from bps.mv(energy, 4080)
        yield from bps.sleep(3)
        yield from bps.mv(energy, 4050)
        yield from bps.sleep(3)


def swaxs_Caedge_Katz_2021_3(t=1):
    dets = [pil900KW, pil1M]

    energies = [4030, 4040, 4050, 4055, 4075]
    det_exposure_time(t, t)
    waxs_range = [0, 2, 20, 22, 40, 42]
    det_exposure_time(t, t)

    xpos = [-500, 500, 3]

    # names =   ['ref_calcite', 'ref_cacooh', 'calcium_01', 'calcium_02', 'calcium_03', 'calcium_04', 'calcium_05', 'calcium_06', 'calcium_07', 'calcium_08', 'calcium_09',
    # 'calcium_10', 'calcium_11', 'calcium_12', 'calcium_13','calcium_14']

    # xs = 300 + np.asarray([43000, 33000, 21000, 9500, -1000, -13000, -25000, -36000, 45000, 35000, 29500, 24000, 14000, 2000, -10500, -24000])
    # ys = [ -500,  -500,  -500, -500,  -500,   -500,   -500,  -1500,  2000,  2000,  1500,  1500,  1500, 1500,   1500,   1500]
    # ys_hexa = [-5,  -5,    -5,   -5,    -5,     -5,     -5,     -5,     5,     5,     5,     5,     5,    5,      5,      5]

    names = ["calcium_13"]

    xs = 300 + np.asarray([43000])
    ys = [-500]
    ys_hexa = [-5]

    assert len(xs) == len(
        names
    ), f"Number of X coordinates ({len(xs)}) is different from number of samples ({len(names)})"
    assert len(xs) == len(
        ys
    ), f"Number of X coordinates ({len(xs)}) is different from number of samples ({len(ys)})"
    assert len(xs) == len(
        ys_hexa
    ), f"Number of X coordinates ({len(xs)}) is different from number of samples ({len(ys_hexa)})"

    for wa in waxs_range[::-1]:
        yield from bps.mv(waxs, wa)

        for x, y, y_hexa, name in zip(xs, ys, ys_hexa, names):
            yield from bps.mv(piezo.x, x)
            yield from bps.mv(piezo.y, y)
            yield from bps.mv(stage.y, y_hexa)

            for k, e in enumerate(energies):
                yield from bps.mv(energy, e)
                yield from bps.sleep(3)
                yield from bps.mv(piezo.y, y + k * 100)

                name_fmt = "{sample}_{energy}eV_sdd1.7m_xbpm{xbpm}_wa{wa}"
                bpm = xbpm2.sumX.value

                sample_name = name_fmt.format(
                    sample=name, energy="%6.2f" % e, xbpm="%3.1f" % bpm, wa="%2.1f" % wa
                )
                sample_id(user_name="OS", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.rel_scan(dets, piezo.x, *xpos)

        yield from bps.mv(energy, 4050)
        yield from bps.sleep(3)
        yield from bps.mv(energy, 4030)
        yield from bps.sleep(3)


def night_katz(t=1):
    proposal_id("2021_3", "307898_Katz")
    yield from nexafs_Caedge_Katz_2021_3(t=t)

    proposal_id("2021_3", "307898_Katz2")
    yield from swaxs_Caedge_Katz_2021_3(t=t)


def nexafs_Agedge_Katz_2021_3(t=1):
    dets = [pil900KW]

    names = [
        "silver_01",
        "silver_02",
        "silver_03",
        "silver_04",
        "silver_05",
        "silver_06",
        "silver_07",
        "silver_08",
        "silver_09",
        "silver_10",
    ]

    xs = [33400, 18000, 6000, -4000, -14000, -27000, 30000, 20000, 5000, -9000]
    ys = [-500, -500, -500, -500, -500, -500, 1500, 1500, 1500, 1500]
    ys_hexa = [-5, -5, -5, -5, -5, -5, 5, 5, 5, 5]

    assert len(xs) == len(
        names
    ), f"Number of X coordinates ({len(xs)}) is different from number of samples ({len(names)})"
    assert len(xs) == len(
        ys
    ), f"Number of X coordinates ({len(xs)}) is different from number of samples ({len(ys)})"
    assert len(xs) == len(
        ys_hexa
    ), f"Number of X coordinates ({len(xs)}) is different from number of samples ({len(ys_hexa)})"

    energies = np.asarray(
        np.arange(3300, 3340, 5).tolist()
        + np.arange(3340, 3350, 2).tolist()
        + np.arange(3350, 3390, 1).tolist()
        + np.arange(3390, 3400, 2).tolist()
        + np.arange(3400, 3450, 5).tolist()
    )
    waxs_arc = [40]

    for x, y, y_hexa, name in zip(xs, ys, ys_hexa, names):
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(piezo.y, y)
        yield from bps.mv(stage.y, y_hexa)

        yield from bps.mv(waxs, waxs_arc[0])
        det_exposure_time(t, t)
        name_fmt = "nexafs_{sample}_{energy}eV_wa50_bpm{xbpm}"

        yss = np.linspace(y, y + 500, 68)
        xss = np.linspace(x, x, 1)

        yss, xss = np.meshgrid(yss, xss)
        yss = yss.ravel()
        xss = xss.ravel()

        for e, xsss, ysss in zip(energies, xss, yss):
            yield from bps.mv(energy, e)
            yield from bps.sleep(3)

            yield from bps.mv(piezo.y, ysss)
            yield from bps.mv(piezo.x, xsss)

            bpm = xbpm2.sumX.value

            sample_name = name_fmt.format(
                sample=name, energy="%6.2f" % e, xbpm="%4.3f" % bpm
            )
            sample_id(user_name="GF", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)

        yield from bps.mv(energy, 3410)
        yield from bps.sleep(3)
        yield from bps.mv(energy, 3370)
        yield from bps.sleep(3)
        yield from bps.mv(energy, 3320)
        yield from bps.sleep(3)


def swaxs_Agedge_Katz_2021_3(t=1):
    dets = [pil900KW, pil1M]

    energies = [3300, 3350, 3357, 3367, 3400, 3430]
    det_exposure_time(t, t)
    waxs_range = [0, 20, 40]
    det_exposure_time(t, t)

    xpos = [-500, 500, 3]

    names = [
        "silver_01",
        "silver_02",
        "silver_03",
        "silver_04",
        "silver_05",
        "silver_06",
        "silver_ref",
        "silver_07",
        "silver_08",
        "silver_09",
        "silver_10",
    ]

    xs = [33400, 18000, 6000, -4000, -14000, -27000, 43000, 30000, 20000, 5000, -9000]
    ys = [-500, -500, -500, -500, -500, -500, 1500, 1500, 1500, 1500, 1500]
    ys_hexa = [-5, -5, -5, -5, -5, -5, 5, 5, 5, 5, 5]

    assert len(xs) == len(
        names
    ), f"Number of X coordinates ({len(xs)}) is different from number of samples ({len(names)})"
    assert len(xs) == len(
        ys
    ), f"Number of X coordinates ({len(xs)}) is different from number of samples ({len(ys)})"
    assert len(xs) == len(
        ys_hexa
    ), f"Number of X coordinates ({len(xs)}) is different from number of samples ({len(ys_hexa)})"

    for wa in waxs_range[::-1]:
        if wa == 42:
            dets = [pil1M]
            yield from bps.mv(GV7.open_cmd, 1)
            yield from bps.mv(att2_10.open_cmd, 1)
            yield from bps.mv(att2_11.open_cmd, 1)
        else:
            dets = [pil900KW]
            yield from bps.mv(GV7.close_cmd, 1)
            yield from bps.mv(att2_10.close_cmd, 1)
            yield from bps.mv(att2_11.close_cmd, 1)
            yield from bps.mv(att2_9.open_cmd, 1)

        yield from bps.mv(waxs, wa)

        for x, y, y_hexa, name in zip(xs, ys, ys_hexa, names):
            yield from bps.mv(piezo.x, x)
            yield from bps.mv(piezo.y, y)
            yield from bps.mv(stage.y, y_hexa)

            for k, e in enumerate(energies):
                yield from bps.mv(energy, e)
                yield from bps.sleep(3)
                yield from bps.mv(piezo.y, y + k * 100)

                name_fmt = "{sample}_{energy}eV_sdd6.0m_xbpm{xbpm}_wa{wa}"
                bpm = xbpm2.sumX.value

                sample_name = name_fmt.format(
                    sample=name, energy="%6.2f" % e, xbpm="%3.1f" % bpm, wa="%2.1f" % wa
                )
                sample_id(user_name="OS", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.rel_scan(dets, piezo.x, *xpos)

        yield from bps.mv(energy, 3400)
        yield from bps.sleep(3)
        yield from bps.mv(energy, 3350)
        yield from bps.sleep(3)
        yield from bps.mv(energy, 3300)
        yield from bps.sleep(3)


def alignement_SVA_(t=1):

    global names, x_hexa, y_hexa, incident_angles, y_hexa_aligned

    names = ["sample1", "sample4"]
    x_hexa = [16, 22]
    y_hexa = [0.6, 0.8]

    incident_angles = []
    y_hexa_aligned = []

    # ai01 = 3.1
    # ai02 = 3.1

    for name, xs_hexa, ys_hexa in zip(names, x_hexa, y_hexa):
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(stage.y, ys_hexa)

        yield from alignement_special_hex(angle=0.45)

        incident_angles = incident_angles + [stage.th.position]
        y_hexa_aligned = y_hexa_aligned + [stage.y.position]


def nexafs_Sedge_SVA_Katz_2021_3(t=1):
    humidity = "%3.2f" % readHumidity(verbosity=0)
    dets = [pil900KW]

    energies = 7 + np.asarray(
        np.arange(2445, 2470, 5).tolist()
        + np.arange(2470, 2480, 0.25).tolist()
        + np.arange(2480, 2490, 1).tolist()
        + np.arange(2490, 2501, 5).tolist()
    )
    waxs_arc = 30

    angle_mes = [0.7]

    for name, xs, aiss, ys in zip(["kapton"], x_hexa, incident_angles, y_hexa_aligned):
        # yield from bps.mv(stage.x, xs)
        # yield from bps.mv(stage.y, ys)
        # yield from bps.mv(stage.th, aiss)

        yield from bps.mv(waxs, waxs_arc)
        det_exposure_time(t, t)

        for angle_me in angle_mes:
            # yield from bps.mv(stage.th, aiss + angle_me)

            name_fmt = "nexafs_{sample}_{energy}eV_wa40_bpm{xbpm}_ai{ai}_hum{hum}"
            for e in energies:
                yield from bps.mv(energy, e)
                yield from bps.sleep(2)

                bpm = xbpm2.sumX.value

                sample_name = name_fmt.format(
                    sample=name,
                    energy="%6.2f" % e,
                    xbpm="%4.3f" % bpm,
                    ai="%1.2f" % angle_me,
                    hum=humidity,
                )
                sample_id(user_name="GF", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 2490)
            yield from bps.mv(energy, 2470)
            yield from bps.mv(energy, 2450)

    # # Measure at flow 100 percent
    setDryFlow(0)
    setWetFlow(5)
    yield from bps.sleep(600)

    humidity = "%3.2f" % readHumidity(verbosity=0)
    dets = [pil900KW]

    energies = 7 + np.asarray(
        np.arange(2445, 2470, 5).tolist()
        + np.arange(2470, 2480, 0.25).tolist()
        + np.arange(2480, 2490, 1).tolist()
        + np.arange(2490, 2501, 5).tolist()
    )
    waxs_arc = 40

    angle_mes = [0.1]

    for name, xs, aiss, ys in zip(names, x_hexa, incident_angles, y_hexa_aligned):
        yield from bps.mv(stage.x, xs)
        yield from bps.mv(stage.y, ys)
        yield from bps.mv(stage.th, aiss)

        yield from bps.mv(waxs, 40)
        det_exposure_time(t, t)

        for angle_me in angle_mes:
            yield from bps.mv(stage.th, aiss + angle_me)

            name_fmt = "nexafs_{sample}_{energy}eV_wa40_bpm{xbpm}_ai{ai}_hum{hum}"
            for e in energies:
                yield from bps.mv(energy, e)
                yield from bps.sleep(2)

                bpm = xbpm2.sumX.value

                sample_name = name_fmt.format(
                    sample=name,
                    energy="%6.2f" % e,
                    xbpm="%4.3f" % bpm,
                    ai="%1.2f" % angle_me,
                    hum=humidity,
                )
                sample_id(user_name="GF", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 2490)
            yield from bps.mv(energy, 2470)
            yield from bps.mv(energy, 2450)

    setDryFlow(0)
    setWetFlow(0)


def saxs_2021_3(t=1):

    xlocs = [39500, 28000, 16000, 6000, -6000, -18000, -29000, -41000, 42000, 30000]
    ylocs = [-5200, -5200, -5200, -5200, -5200, -5200, -5200, -5200, 7200, 7200]
    zlocs = [2700, 2700, 2700, 2700, 2700, 2700, 2700, 2700, 2700, 2700]
    names = [
        "sample_01",
        "sample_02",
        "sample_03",
        "sample_04",
        "sample_05",
        "sample_06",
        "sample_07",
        "sample_08",
        "sample_09",
        "sample_10",
    ]

    user = "ML"
    det_exposure_time(t, t)

    assert len(xlocs) == len(
        names
    ), f"Number of X coordinates ({len(xlocs)}) is different from number of samples ({len(names)})"

    # Detectors, motors:
    dets = [pil1M]
    waxs_range = [30]

    ypos = [-200, 200, 3]

    for wa in waxs_range[::-1]:
        yield from bps.mv(waxs, wa)
        for sam, x, y, z in zip(names, xlocs, ylocs, zlocs):
            yield from bps.mv(piezo.x, x)
            yield from bps.mv(piezo.y, y)
            yield from bps.mv(piezo.z, z)

            name_fmt = "{sam}_16.1keV_sdd8.3m_wa{waxs}"
            sample_name = name_fmt.format(sam=sam, waxs="%2.1f" % wa)
            sample_id(user_name=user, sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.rel_scan(dets, piezo.y, *ypos)
            yield from bps.sleep(2)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def waxs_Ca_edge_Katz_2022_2(t=0.2):
    """
    Wide WAXS scan including nexafs at 60 deg 2022_2 cycle

    NEXAFS at WAXS 60 deg scanned with higher resolution
    """

    user_name = "ML"

    names = ["calcium_12_nexafs"]
    piezo_x = [-40000]
    piezo_y = [-1910]

    # waxs_arc = [0, 20, 40, 60]
    waxs_arc = [60]
    # to move piezo x slightly for different waxs angles
    waxs_piezo_x_offset = 100  # um
    det_exposure_time(t, t)

    assert len(piezo_x) == len(
        names
    ), f"Number of piezo x coordinates ({len(piezo_x)}) is different from number of samples ({len(names)})"
    assert len(piezo_x) == len(
        piezo_y
    ), f"Number of piezo x coordinates ({len(piezo_x)}) is different tan number of piezo y coordinates ({len(piezo_y)})"
    assert len(piezo_y) == len(
        names
    ), f"Number of piezo y coordinates ({len(piezo_y)}) is different from number of samples ({len(names)})"

    # Check and correct sample names just in case
    names = [n.translate({ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ "}) for n in names]

    # Energies for calcium K edge, nexafs resolution
    energies_nexafs = np.concatenate(
        (
            np.arange(4030, 4035, 5),
            np.arange(4035, 4042, 2),
            np.arange(4042, 4070, 0.5),
            np.arange(4070, 4080, 2),
            np.arange(4080, 4140, 5),
        )
    )

    # Energies for calcium K edge, coarse resolution
    energies_coarse = np.concatenate(
        (
            np.arange(4030, 4045, 5),
            np.arange(4045, 4060, 1),
            np.arange(4060, 4080, 5),
            np.arange(4080, 4121, 10),
        )
    )

    # Go over WAXS arc positions as the sloest motor
    for i, wa in enumerate(waxs_arc):
        yield from bps.mv(waxs, wa)

        # Do not read SAXS if WAXS is in the way
        dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]

        # Change energies
        energies = energies_coarse if wa < 45 else energies_nexafs

        # Go over samples
        for name, xs, ys in zip(names, piezo_x, piezo_y):

            yield from bps.mv(piezo.x, xs + i * waxs_piezo_x_offset)
            yield from bps.mv(piezo.y, ys)

            # Cover a range of 1.0 mm in y to avoid damage
            yss = np.linspace(ys, ys + 1000, len(energies))

            # Scan over energies
            for e, ysss in zip(energies, yss):
                yield from bps.mv(piezo.y, ysss)
                yield from bps.mv(energy, e)
                yield from bps.sleep(2)

                # Metadata
                bpm = xbpm3.sumX.get()
                sdd = pil1m_pos.z.position / 1000
                wa = str(np.round(float(wa), 1)).zfill(4)

                # Detector file name
                name_fmt = "{sample}_{energy}eV_wa{wax}_sdd{sdd}m_bpm{xbpm}"
                sample_name = name_fmt.format(
                    sample=name,
                    energy="%6.2f" % e,
                    wax=wa,
                    sdd="%.1f" % sdd,
                    xbpm="%4.3f" % bpm,
                )
                sample_id(user_name=user_name, sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")

                yield from bp.count(dets, num=1)

            # Come back gently with energies
            energy_steps = [4100, 4080, 4050]
            for e in energy_steps:
                yield from bps.mv(energy, e)
                yield from bps.sleep(3)


def nexafs_saxs_Ag_edge_Katz_2022_2(t=0.2):
    """
    NEXAFS and SAXS at 40 deg across Ag L3 edge
    """

    user_name = "ML"

    # first bar: samples 01_01 to 07_01 on top, 08_02 to 15_01 on bottom
    # names_top =   ['sample_01_01','sample_02_01', 'sample_03_01', 'sample_04_01', 'sample_05_01', 'sample_06_01','sample_07_01']
    # names_bot =   ['sample_08_01', 'sample_09_01', 'sample_10_01', 'sample_11_01', 'sample_12_01', 'sample_13_01','sample_14_01', 'sample_15_01']
    # piezo_x_top = [   43000,30000,18000, 6000,-7000,-19000,-32000]
    # piezo_y_top = [     -7500,-7900,-7900,-9900,-7900,-7900,-6900 ]
    # piezo_x_bot = [     43000,29000,16000,6000,-6000,-18000,-30000,-41000 ]
    # piezo_y_bot = [      4100,4100,5100,5100,5600,5600, 5600,5600]

    # second bar: samples 16_01 to 06_02 on top, 07_02 to 14_02 on bottom
    # names_top =   ['sample_16_01','sample_01_02', 'sample_02_02', 'sample_03_02', 'sample_04_02', 'sample_05_02', 'sample_06_02']
    # names_bot =   ['sample_07_02','sample_08_02', 'sample_09_02', 'sample_10_02', 'sample_11_02', 'sample_12_02', 'sample_13_02',
    #               'sample_14_02']
    # piezo_x_top = [   45100,32100,19100, 7100,-6900,-16900,-30900]
    # piezo_y_top = [     -8000,-8000,-9000,-8000,-7500,-8500,-8500 ]
    # piezo_x_bot = [     43000,29000,15000,3000,-7000,-18000,-30000,-42000 ]
    # piezo_y_bot = [      4500,4500,4500,4000,5500,5500, 5500,5500]

    # second and a half bar: rerun second bar for duplicates, samples 16_02 to 06_03 on top, 07_03 to 14_03 on bottom
    #  added 500 micron in all x positions so we can get triplicates on all samples
    # names_top =   ['sample_16_02','sample_01_03', 'sample_02_03', 'sample_03_03', 'sample_04_03', 'sample_05_03', 'sample_06_03']
    # names_bot =   ['sample_07_03','sample_08_03', 'sample_09_03', 'sample_10_03', 'sample_11_03', 'sample_12_03', 'sample_13_03',
    #               'sample_14_03']
    # piezo_x_top = [   45600,32600,19600, 7600,-6100,-16400,-30400]
    # piezo_y_top = [     -8000,-8000,-9000,-8000,-7500,-8500,-8500 ]
    # piezo_x_bot = [     43500,29500,15500,3500,-6500,-17500,-29500,-41500 ]
    # piezo_y_bot = [      4500,4500,4500,4000,5500,5500, 5500,5500]

    # third bar: samples 16_02 to 06_03 on top, 07_03 to 14_03 on bottom
    #  added 500 micron in all x positions so we can get triplicates on all samples
    # names_top =   ['sample_15_02','sample_15_03', 'sample_16_03', 'sample_MD_17_01','sample_MD_17_02','sample_MD_17_03','sample_MD_17_04','sample_MD_17_05']
    # names_bot =   ['sample_MD_17_06','sample_MD_17_07','sample_MD_17_08','sample_MD_17_09','sample_MD_17_10','diode']
    # piezo_x_top = [   42500,42500,28500,17500, 4500,-9500,-23500,-36500]
    # piezo_y_top = [     -8000,-7000,-7000,-7000,-7000,-7000,-7000,-7000 ]
    # piezo_x_bot = [     37500,23500,11500,-3500,-18500,-27500]
    # piezo_y_bot = [      4500,4500,4500,4500,4500,4500]

    # fourth bar: final bar, scattering and some additional scans for other edges
    names_top = [
        "silver_NPs",
        "sample_04_window",
        "sample_12_window",
        "sample_13_window",
        "sample_14_window",
        "blank_window",
    ]
    names_bot = ["sample_MD_17_02", "sample_MD_17_03", "sample_MD_17_05"]
    piezo_x_top = [33000, 24200, 16700, 8600, -400, 39500]
    piezo_y_top = [-8600, -8800, -9000, -8400, -8400, -8800]
    piezo_x_bot = [39100, 22100, 9100]
    piezo_y_bot = [4000, 4000, 4000]

    names = names_top + names_bot
    piezo_x = piezo_x_top + piezo_x_bot
    piezo_y = piezo_y_top + piezo_y_bot

    waxs_arc = [20, 40, 60]
    # to move piezo x slightly for different waxs angles
    waxs_piezo_x_offset = 200  # um
    det_exposure_time(t, t)

    assert len(piezo_x) == len(
        names
    ), f"Number of piezo x coordinates ({len(piezo_x)}) is different from number of samples ({len(names)})"
    assert len(piezo_x) == len(
        piezo_y
    ), f"Number of piezo x coordinates ({len(piezo_x)}) is different tan number of piezo y coordinates ({len(piezo_y)})"
    assert len(piezo_y) == len(
        names
    ), f"Number of piezo y coordinates ({len(piezo_y)}) is different from number of samples ({len(names)})"

    # Check and correct sample names just in case
    names = [n.translate({ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ "}) for n in names]

    # Energies for silver L3 edge nexafs resolution
    energies = np.concatenate(
        (
            np.arange(3300, 3340, 5),
            np.arange(3340, 3350, 2),
            np.arange(3350, 3390, 1),
            np.arange(3390, 3400, 2),
            np.arange(3400, 3450, 5),
        )
    )

    # Go over WAXS arc positions as the sloest motor
    for i, wa in enumerate(waxs_arc):
        yield from bps.mv(waxs, wa)

        # Do not read SAXS if WAXS is in the way
        dets = [pil900KW] if wa < 50 else [pil1M, pil900KW]

        # Go over samples
        for name, xs, ys in zip(names, piezo_x, piezo_y):

            yield from bps.mv(piezo.x, xs + i * waxs_piezo_x_offset)
            yield from bps.mv(piezo.y, ys)

            # Cover a range of 1.0 mm in y to avoid damage
            yss = np.linspace(ys, ys + 500, len(energies))

            # Scan over energies
            for e, ysss in zip(energies, yss):
                yield from bps.mv(piezo.y, ysss)
                yield from bps.mv(energy, e)
                yield from bps.sleep(2)

                # Metadata
                bpm = xbpm3.sumX.get()
                sdd = pil1m_pos.z.position / 1000
                wa = str(np.round(float(wa), 1)).zfill(4)

                # Detector file name
                name_fmt = "{sample}_{energy}eV_wa{wax}_sdd{sdd}m_bpm{xbpm}"
                sample_name = name_fmt.format(
                    sample=name,
                    energy="%6.2f" % e,
                    wax=wa,
                    sdd="%.1f" % sdd,
                    xbpm="%4.3f" % bpm,
                )
                sample_id(user_name=user_name, sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")

                yield from bp.count(dets, num=1)

            # Come back gently with energies
            energy_steps = [3410, 3370, 3320]
            for e in energy_steps:
                yield from bps.mv(energy, e)
                yield from bps.sleep(3)


def ca_spectroscopy_scan_mrl(t=0.2):
    """
    Ca K-edge NEXAFS scan on calcium acetate reference
    """
    user_name = "ML"
    sample_name = "calcium_acetate_0pt2sec_1eVres_2_"

    sample_id(user_name=user_name, sample_name=sample_name)
    det_exposure_time(t, t)
    # yield from bps.mv(waxs, 60)      im already at 60 so dont need this line
    yield from bp.scan([pil900KW], energy, 4030, 4120, 91)
    yield from bps.mv(energy, 4100)
    yield from bps.mv(energy, 4075)
    yield from bps.mv(energy, 4050)
    yield from bps.mv(energy, 4030)








def swaxs_2023_2_run1(t=1):


    # names = ["latex_01","latex_02","latex_03","latex_04","latex_05","latex_06","latex_07",
    #          "latex_08","latex_09","latex_10"]
    # xlocs = [     49000,     37000,     23000,     11000,     -3000,    -15000,    -27500, 
    #               48000,     36000,     24000]
    # ylocs = [     -6500,     -6500,     -7000,     -7500,     -7500,     -8000,     -8500, 
    #                6000,      6000,      5500]
    # zlocs = [      4000,      4000,      4000,      4000,      4000,      4000,      4000, 
    #                4000,      4000,      4000]
    
    # names = [  "cam_01",  "cam_02",  "cam_03",  "cam_04",  "cam_05","cam_06", "cam_07"]
    # xlocs = [     13000,      5000,     -2000,     -8000,    -13000,  -25000,   -35000]
    # ylocs = [      5500,      5000,      5000,      4500,      4500,    4500,     3000]
    # zlocs = [      4000,      4000,      4000,      4000,      4000,    6000,     6000]

    # names = [ "cam_08", "cam_09", "cam_10", "cam_11", "cam_12", "cam_13", "cam_14", "cam_15", "cam_16", "cam_17", "cam_18"]
    # xlocs = [    50000,    38000,    25000,    15000,     4000,    -6000,   -15000,   -22500,   -27500,   -32500,   -37500]
    # ylocs = [    -4000,    -2500,    -2500,    -2500,    -2500,    -2500,    -2500,    -5000,    -5000,    -5000,    -4000]
    # zlocs = [     4200,     4200,     4200,     4200,     4200,     4200,     4200,     4200,     4200,     4200,     4300]



   # names = ["Ac_01", "Ac_02", "Ac_03", "Ac_04", "Ac_05","Ac_06","Ac_07","Ac_08",
   #          "Ac_09", "Ac_10", "Ac_11", "Ac_12", "Ac_13", "Ac_14"]
   # xlocs = [  48000,   37000,   25000,   13000,    1000,  -10000,  22000, -34000,
   #            47000,   31000,   18000,       0,  -20000,  -36000]
   # ylocs = [  -7500,   -7500,   -7500,   -7500,   -6300,   -6500,  -6500,  -6500,
   #             5000,    5000,    5000,    5500,    5500,    5500]
   # zlocs = [   4300,    4300,    4300,    4300,    4300,    4300,   4300,   4300,
   #             4300,    4300,    4300,    4300,    4300,    4300]


    names = ["54I-12-CuTF2N-60_pos1", "54I-12-CuTF2N-60_pos2" ]
    xlocs = [                  37500,                   36500 ]
    ylocs = [                   4000,                    6650 ]
    zlocs = [                   4300,                    4300 ]




    # yield from bps.mv(att1_5.open_cmd, 1)


    user = "ML"
    det_exposure_time(t, t)

    assert len(xlocs) == len(names), f"Number of X coordinates ({len(xlocs)}) is different from number of samples ({len(names)})"
    assert len(xlocs) == len(ylocs), f"Number of X coordinates ({len(ylocs)}) is different from number of samples ({len(names)})"
    assert len(xlocs) == len(zlocs), f"Number of X coordinates ({len(zlocs)}) is different from number of samples ({len(names)})"

    # Detectors, motors:
    dets = [pil1M, pil900KW]
    # dets = [pil900KW]

    waxs_range = [20]

    ypos = [-200, 200, 3]

    for wa in waxs_range:
        yield from bps.mv(waxs, wa)
        for sam, x, y, z in zip(names, xlocs, ylocs, zlocs):
            yield from bps.mv(piezo.x, x)
            yield from bps.mv(piezo.y, y)
            yield from bps.mv(piezo.z, z)

            name_fmt = "{sam}_16.1keV_sdd9.2m_wa{waxs}"
            sample_name = name_fmt.format(sam=sam, waxs="%2.1f" % wa)
            sample_id(user_name=user, sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.rel_scan(dets, piezo.y, *ypos)
            yield from bps.sleep(2)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)

    # yield from bps.mv(att1_5.close_cmd, 1)



def giswaxs_2023_2(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    # names = [  'grazing1', 'grazing2', 'grazing3', 'grazing4', 'grazing5', 'grazing6', 'grazing7', 'grazing8', 'grazing9', 
    #           'grazing10','grazing11','grazing12','grazing13','grazing14','grazing15']
    # x_piezo = [    -50000,     -50000,     -43000,     -36000,     -29000,   -20000,   -11000,    -1000,     9000,
    #                 19000,      30000,      40000,      50000,      50000,    57000]
    # y_piezo = [      2500,       4500,       5000,       4500,       4500,     4500,     4500,     4500,     4700,
    #                  5300,       5300,       5400,       5500,       5600,     4100]
    # z_piezo = [      7000,       7000,       7000,       7000,       7000,     7000,     7000,     7000,     7000,
    #                  7000,       7000,       7000,       7000,       7000,     7000]
    # x_hexa =  [       -13,          0,          0,          0,          0,        0,        0,        0,        0,
    #                     0,          0,          0,          0,          8,       10]


    names = [ 'grazing13', 'grazing14', 'grazing15']
    x_piezo = [     48000,       50000,       57000]
    y_piezo = [      5500,        5600,        4100]
    z_piezo = [      7000,        7000,        7000]
    x_hexa =  [         0,           8,          10]

    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(z_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexa)})"

    waxs_arc = [20, 0]
    ai0 = 0
    ai_list = [0.15]

    for name, xs, ys, zs, xs_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa):
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)

        yield from bps.mv(piezo.th, ai0)
        yield from alignement_gisaxs(angle=0.15)

        yield from bps.mv(att1_5.open_cmd, 1)

        ai0 = piezo.th.position
        det_exposure_time(t, t)

        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)
            # Do not take SAXS when WAXS detector in the way
            dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]

            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                name_fmt = "{sample}_ai{ai}_wa{wax}"
                sample_name = name_fmt.format(sample=name, ai="%3.2f"%ais, wax=wa)
                sample_id(user_name="LR", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

            yield from bps.mv(piezo.th, ai0)



from bluesky.utils import short_uid
import bluesky.plan_stubs as bps
import bluesky.preprocessors as bpp

def blading_scan(det, motor, position, md=None):
    md = dict(md) if md is not None else {}

    @bpp.stage_decorator([det])
    @bpp.run_decorator(md=md)
    def inner():
        # name of the group we should wait for
        group=short_uid('reading')

        # trigger the detector
        st = yield from bps.trigger(det, group=group)
        # move the motor 
        yield from bps.mv(motor, position)

        # wait for the detector to really finish
        yield from bps.wait(group=group)
        # put the detector reading in the primary stream
        yield from bps.create(name='primary')
        yield from bps.read(det)
        yield from bps.save()

    yield from inner()


def blade_coating_2022_1(sample_name='test'):
    proposal_id('2023_2', '312762_Katz_04')
    yield from bps.mv(bc_smaract.x1, 70)
    # x2=73.605
    # yield from bps.mv(stage.th, 0.65)

    yield from alignement_gisaxs_hex(angle=0.15)

    yield from bps.mvr(stage.th, 0.12)
    # yield from bps.mvr(stage.y, 0.05)

    yield from bps.mv(bc_smaract.x1, 0)

    det_exposure_time(0.1, 180)
    sample_id(user_name='ML', sample_name=sample_name)

    yield from bps.mv(syringe_pu.x3, 1)
    yield from bps.sleep(3)
    yield from blading_scan(pil1M, bc_smaract.x1, 70)




def alignement_blade_coating():
    proposal_id('2023_2', '312762_Katz_04')
    yield from bps.mv(bc_smaract.x1, 70)
    # x2=73.605
    # yield from bps.mv(stage.th, 0.65)

    yield from alignement_gisaxs_hex(angle=0.15)

    yield from bps.mvr(stage.th, 0.12)
    yield from bps.mvr(stage.y, 0.05)

    yield from bps.mv(bc_smaract.x1, 0)


def button_blade_coating(sample_name='test'):

    det_exposure_time(0.1, 180)
    sample_id(user_name='ML', sample_name=sample_name)
    yield from blading_scan(pil1M, bc_smaract.x1, 70)


def nexafs_cu(t=1, name='test'):
    ener = np.asarray(np.linspace(8960, 8970, 6).tolist() + np.linspace(8970, 9010, 41).tolist() + np.linspace(9010, 9090, 17).tolist())

    for e in ener:
        bpm = xbpm3.sumX.get()
        name_fmt = "{sample}_{energy}eV_wa{wax}_bpm{xbpm}"
        sample_name = name_fmt.format(sample=name,energy="%6.2f" % e,wax=20,xbpm="%4.3f"%bpm)
        sample_id(user_name='ML', sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")

        yield from bp.count([pil900KW], num=1)

        yield from bps.mv(energy, e)
        yield from bps.sleep(3)



def waxs_Ca_edge_Katz_2024_2(t=0.2):
    """
    Wide WAXS scan including nexafs at 60 deg 2022_2 cycle

    NEXAFS at WAXS 60 deg scanned with higher resolution
    """

    user_name = "ML"

    names = ['xle-ctrl', 'xle-01', 'xle-02', 'xle-03', 'xle-04', 'xle-05']
    piezo_x = [   41000,    34000,    27000,    19000,    13000,     6000]
    piezo_y = [   -7000,    -7000,    -7000,    -7000,    -7000,    -7000]

    waxs_arc = [0, 20, 40]
    det_exposure_time(t, t)

    assert len(piezo_x) == len(names), f"Number of piezo x coordinates ({len(piezo_x)}) is different from number of samples ({len(names)})"
    assert len(piezo_x) == len(piezo_y), f"Number of piezo x coordinates ({len(piezo_x)}) is different tan number of piezo y coordinates ({len(piezo_y)})"
    assert len(piezo_y) == len(names), f"Number of piezo y coordinates ({len(piezo_y)}) is different from number of samples ({len(names)})"

    # Check and correct sample names just in case
    names = [n.translate({ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ "}) for n in names]

    # Energies for calcium K edge, nexafs resolution
    energies = np.concatenate((np.arange(4030, 4035, 5),
                                      np.arange(4035, 4042, 2),
                                      np.arange(4042, 4070, 1),
                                      np.arange(4070, 4080, 2),
                                      np.arange(4080, 4140, 5),))

    # Go over WAXS arc positions as the sloest motor
    for i, wa in enumerate(waxs_arc):
        yield from bps.mv(waxs, wa)

        # Do not read SAXS if WAXS is in the way
        dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]

        # Go over samples
        for name, xs, ys in zip(names, piezo_x, piezo_y):

            yield from bps.mv(piezo.x, xs)
            yield from bps.mv(piezo.y, ys)

            # Cover a range of 1.0 mm in y to avoid damage
            yss = np.linspace(ys, ys + 1500, len(energies))

            # Scan over energies
            for e, ysss in zip(energies, yss):
                yield from bps.mv(piezo.y, ysss)
                yield from bps.mv(energy, e)
                yield from bps.sleep(2)
                if xbpm2.sumX.get() < 50:
                    yield from bps.sleep(2)
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)

                # Metadata
                bpm = xbpm3.sumX.get()
                sdd = pil1m_pos.z.position / 1000
                wa = str(np.round(float(wa), 1)).zfill(4)

                # Detector file name
                name_fmt = "{sample}_{energy}eV_wa{wax}_sdd{sdd}m_bpm{xbpm}"
                sample_name = name_fmt.format(
                    sample=name,
                    energy="%6.2f" % e,
                    wax=wa,
                    sdd="%.1f" % sdd,
                    xbpm="%4.3f" % bpm,
                )
                sample_id(user_name=user_name, sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")

                yield from bp.count(dets, num=1)

            # Come back gently with energies
            energy_steps = [4100, 4080, 4050]
            for e in energy_steps:
                yield from bps.mv(energy, e)
                yield from bps.sleep(2)
                if xbpm2.sumX.get() < 50:
                    yield from bps.sleep(2)
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)


    names = ['xle-isolated-ctrl', 'xle-isolated-snomCa' ]
    piezo_x = [   -3000,    -8200]
    piezo_y = [   -7000,    -7000]

    waxs_arc = [0, 20, 40]
    det_exposure_time(t, t)

    assert len(piezo_x) == len(names), f"Number of piezo x coordinates ({len(piezo_x)}) is different from number of samples ({len(names)})"
    assert len(piezo_x) == len(piezo_y), f"Number of piezo x coordinates ({len(piezo_x)}) is different tan number of piezo y coordinates ({len(piezo_y)})"
    assert len(piezo_y) == len(names), f"Number of piezo y coordinates ({len(piezo_y)}) is different from number of samples ({len(names)})"

    # Check and correct sample names just in case
    names = [n.translate({ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ "}) for n in names]

    # Go over WAXS arc positions as the sloest motor
    for i, wa in enumerate(waxs_arc):
        yield from bps.mv(waxs, wa)

        # Do not read SAXS if WAXS is in the way
        dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]

        # Go over samples
        for name, xs, ys in zip(names, piezo_x, piezo_y):

            yield from bps.mv(piezo.x, xs)
            yield from bps.mv(piezo.y, ys)

            # Cover a range of 1.0 mm in y to avoid damage
            yss = np.linspace(ys, ys + 600, len(energies))

            # Scan over energies
            for e, ysss in zip(energies, yss):
                yield from bps.mv(piezo.y, ysss)
                yield from bps.mv(energy, e)
                yield from bps.sleep(2)
                if xbpm2.sumX.get() < 50:
                    yield from bps.sleep(2)
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)

                # Metadata
                bpm = xbpm3.sumX.get()
                sdd = pil1m_pos.z.position / 1000
                wa = str(np.round(float(wa), 1)).zfill(4)

                # Detector file name
                name_fmt = "{sample}_{energy}eV_wa{wax}_sdd{sdd}m_bpm{xbpm}"
                sample_name = name_fmt.format(
                    sample=name,
                    energy="%6.2f" % e,
                    wax=wa,
                    sdd="%.1f" % sdd,
                    xbpm="%4.3f" % bpm,
                )
                sample_id(user_name=user_name, sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")

                yield from bp.count(dets, num=1)

            # Come back gently with energies
            energy_steps = [4100, 4080, 4050]
            for e in energy_steps:
                yield from bps.mv(energy, e)
                yield from bps.sleep(2)
                if xbpm2.sumX.get() < 50:
                    yield from bps.sleep(2)
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
       









def alignement_blade_coating_2024_2(coating_start_pos, measurement_pos,th):

    yield from bps.mv(thorlabs_su, measurement_pos)
    yield from alignement_gisaxs_hex(angle=th)

    yield from bps.mvr(stage.th, th)
    yield from bps.mvr(stage.y, 0.05)

    yield from bps.mv(thorlabs_su, coating_start_pos)




def blade_coating_2024_2(sample_name='test', coating_start_pos=10, measurement_pos=87, th=0.12):

    #proposal_id('2023_2', '312762_Katz_04')
    sample_id(user_name='ML', sample_name=sample_name)
    yield from alignement_blade_coating_2024_2(coating_start_pos, measurement_pos,th)

    yield from bps.mv(syringe_pu.x3, 1) 
    yield from bps.sleep(3)
    
    yield from bps.mv(thorlabs_su, measurement_pos)

    det_exposure_time(0.5,300)
    yield from bp.count([pil1M])
    

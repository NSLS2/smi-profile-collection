def giwaxs_collins_2020_3(t=1):

    # samples = ['PCPDn', 'PCPDt', 'ITICn', 'PBDCBn', 'PBCN3n', 'PCDDn', 'P3t', 'P3n', 'P3N2n', 'HTAZn', 'HTAZt', 'FTAZn']
    # samples = ['P3N2CNn', 'N2n', 'Si', 'PB3n', 'PB0n', 'PBp25n', 'PBp5n', 'PBp75n', 'PB1n']
    # samples = ['HTAZn', 'HTAZt', 'FTAZn']

    samples = [
        "PB3n_2",
        "PB0n_2",
        "PBp25n_2",
    ]
    x_list = [-15500, -6000, 9000]

    waxs_arc = [3, 9.5, 16, 22.5]
    angle = [0.15]

    alpha_0 = []
    y_0 = []

    # Detectors, motors:
    dets = [pil1M, pil300KW]

    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"

    yield from bps.mv(pil1m_pos.x, -2.3)

    for x, sample in zip(x_list, samples):
        yield from bps.mv(piezo.x, x)
        yield from alignement_special(angle=0.15)

        ai0 = piezo.th.position

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)
            det_exposure_time(t, t)
            name_fmt = "{sample}_ai{angle}deg_wa{wax}"

            for an in angle:
                yield from bps.mv(piezo.th, ai0 + an)
                sample_name = name_fmt.format(
                    sample=sample, angle="%3.3f" % an, wax="%2.2d" % wa
                )
                sample_id(user_name="BC", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def giwaxs_collins_2021_1(t=1):
    # samples = [ 'F4', 'F44',  'F3', 'F33', 'F9', 'F41',   'F1',  'F11',   'F2',  'F22',  'P3W', 'C61W']
    # x_piezo = [58500, 51000, 38000, 22000, 9000, -4000, -14000, -25000, -37000, -48000, -58000, -59000]
    # x_hexa =  [    6,     0,     0,     0,    0,     0,      0,      0,      0,     0,      -3,    -11]

    # samples = [ 'BSW', 'BBW']
    # x_piezo = [56000, 44000]
    # x_hexa =  [    0,     0]

    samples = ["F1_redo"]
    x_piezo = [-57000]
    x_hexa = [-6]

    waxs_arc = np.linspace(0, 19.5, 4)
    angle = [0.09, 0.15, 0.20]

    # Detectors, motors:
    dets = [pil300KW]

    assert len(x_piezo) == len(
        samples
    ), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(samples)})"
    assert len(x_piezo) == len(
        x_hexa
    ), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexa)})"

    for xs_piezo, xs_hexa, sample in zip(x_piezo, x_hexa, samples):
        yield from bps.mv(piezo.x, xs_piezo)
        yield from bps.mv(stage.x, xs_hexa)

        yield from alignement_gisaxs(angle=0.14)

        ai0 = piezo.th.position

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)
            det_exposure_time(t, t)
            name_fmt = "{sample}_16.1keV__ai{angle}deg_wa{wax}"

            for an in angle:
                yield from bps.mv(piezo.th, ai0 + an)
                sample_name = name_fmt.format(
                    sample=sample, angle="%3.3f" % an, wax="%2.1f" % wa
                )
                sample_id(user_name="ZG", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def giwaxs_collins_2021_2(t=1):
    # samples = [ 'PM7', 'ITIC',  'PBDB-T2']
    # x_piezo = [-42000, -53000,     -55000]
    # x_hexa =  [     0,      0,        -13]

    # samples = [ 'PCBM', 'PBbin1', 'PBbin2', 'PBbin3', 'PBMbin1', 'PBMbin2', 'PBMbin3',  'H2',  'H10',  'H12',  'H14',   'H8',   'H6',   'H4']
    # x_piezo = [  59000,    59000,    54000,    47000,     37000,     25000,     10000, -2000, -13000, -23000, -33000, -45000, -56000, -56000]
    # x_hexa =  [     14,        4,        0,        0,         0,         0,         0,     0,      0,      0,      0,      0,     -1,    -10]

    samples = ["PBDB-T", "AS60", "C71", "AS10", "AS15", "AS30", "A45", "AS0"]
    x_piezo = [55000, 49000, 37000, 24000, 13000, 2000, -12000, -22000]
    x_hexa = [10, 0, 0, 0, 0, 0, 0, 0]

    waxs_arc = [0, 2, 19.5, 21.5, 39, 41]
    angle = [0.08, 0.15, 0.20]

    # Detectors, motors:
    dets = [pil300KW, pil900KW, pil1M]

    assert len(x_piezo) == len(
        samples
    ), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(samples)})"
    assert len(x_piezo) == len(
        x_hexa
    ), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexa)})"

    for xs_piezo, xs_hexa, sample in zip(x_piezo, x_hexa, samples):
        yield from bps.mv(piezo.x, xs_piezo)
        yield from bps.mv(stage.x, xs_hexa)

        yield from alignement_gisaxs(angle=0.15)

        ai0 = piezo.th.position

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)
            det_exposure_time(t, t)
            name_fmt = "{sample}_16.1keV__ai{angle}deg_wa{wax}"

            for an in angle:
                yield from bps.mv(piezo.th, ai0 + an)
                sample_name = name_fmt.format(
                    sample=sample, angle="%3.3f" % an, wax="%2.1f" % wa
                )
                sample_id(user_name="BC", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

        yield from bps.mv(piezo.th, ai0)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def giwaxs_collins(t=1):
    # samples = ['FCuPcCuI', 'FCuPc', 'Si', 'ITO_pos1', 'ITO_pos2', 'Z5S', 'Z5CS', 'Z5CI_pos1', 'Z5CI_pos2', 'Z5I', 'Z10S']
    # samples = ['Z10CS', 'Z10CI', 'Z10I', 'Z2OS', 'Z20CS', 'Z20CI', 'Z20I', 'Z4Os']
    # samples = ['Z5CI_pos1_2', 'Z5CI_pos2_2', 'Z4Os_2', 'Z40CS', 'Z40CI', 'Z40I', 'CS', 'CI_pos1', 'CI_pos2']
    # x_list = [-45500, -42500, -29500, -17500, -9500, 7500, 25500, 43000, 46000]

    samples = ["Z20I_pos1", "Z20I_pos1", "Z4OI"]
    x_list = [-45700, -40200, -21200]

    waxs_arc = [3, 9.5, 16, 22.5]
    angle = [0.09, 0.15, 0.20]

    alpha_0 = []
    y_0 = []

    # Detectors, motors:
    dets = [pil1M, pil300KW]

    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"

    yield from bps.mv(pil1m_pos.x, -2.3)

    for x, sample in zip(x_list, samples):
        yield from bps.mv(piezo.x, x)
        yield from alignement_special(angle=0.15)

        ai0 = piezo.th.position

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)
            det_exposure_time(t, t)
            name_fmt = "{sample}_ai{angle}deg_wa{wax}"

            for an in angle:
                yield from bps.mv(piezo.th, ai0 + an)
                sample_name = name_fmt.format(
                    sample=sample, angle="%3.3f" % an, wax="%2.2d" % wa
                )
                sample_id(user_name="ZG", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def nexafs_S_edge_terry(t=1):
    dets = [pil300KW]

    names = ["pedotpss_1_gisaxs"]
    x = [0]
    y = [7169.288]

    # names = ['N2200_2_nexafs']
    # x = [34800]
    # y = [2000]
    # energies = np.arange(2450, 2470, 5).tolist() + np.arange(2470, 2480, 0.25).tolist() + np.arange(2480, 2490, 1).tolist()+ np.arange(2490, 2501, 5).tolist()

    energies = (
        np.arange(2450, 2470, 5).tolist()
        + np.arange(2470, 2474, 0.5).tolist()
        + np.arange(2474, 2482, 0.25).tolist()
        + np.arange(2482, 2500, 1).tolist()
        + np.arange(2500, 2531, 5).tolist()
    )
    waxs_arc = [60]

    for name, xs, ys in zip(names, x, y):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)

            det_exposure_time(t, t)
            name_fmt = "{sample}_{energy}eV_bpm{xbpm}"
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

            yield from bps.mv(energy, 2470)
            yield from bps.mv(energy, 2450)


def waxs_S_edge_terry(t=1):
    dets = [pil300KW]

    names = ["c1_03"]
    x = [-23000]

    energies = (
        np.arange(2450, 2470, 5).tolist()
        + np.arange(2470, 2480, 0.25).tolist()
        + np.arange(2480, 2490, 1).tolist()
        + np.arange(2490, 2501, 5).tolist()
    )
    waxs_arc = np.linspace(0, 26, 5)

    for name, xs in zip(names, x):
        yield from bps.mv(piezo.x, xs)

        xss = np.linspace(xs, xs - 8000, 57)
        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)

            det_exposure_time(t, t)
            name_fmt = "{sample}_{energy}eV_wa{wax}_bpm{xbpm}"
            for e, xsss in zip(energies, xss):
                yield from bps.mv(energy, e)
                yield from bps.sleep(2)

                yield from bps.mv(piezo.x, xsss)
                bpm = xbpm2.sumX.value

                sample_name = name_fmt.format(
                    sample=name, energy="%6.2f" % e, wax=wa, xbpm="%4.3f" % bpm
                )
                sample_id(user_name="GF", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 2470)
            yield from bps.mv(energy, 2450)


def waxs_S_edge_terry1(t=1):
    dets = [pil300KW, pil1M]

    names = [
        "p3HT_1_saxs",
        "N2200_1_saxs",
        "PCPDTBT_1_saxs",
        "p3N2CN_1_saxs",
        "P3N2_1_saxs",
        "p3C61BM_1_saxs",
        "AD0_1_saxs",
        "AD1_1_saxs",
        "AD1_2_saxs",
        "AD2_1_saxs",
        "AD3_1_saxs",
        "AD4_1_saxs",
        "AD5_1_saxs",
        "AD6_1_saxs",
        "AD7_1_saxs",
    ]
    x = [
        41600,
        34600,
        28200,
        23200,
        17800,
        12400,
        6500,
        1000,
        2000,
        -3200,
        -9000,
        -13700,
        -19900,
        -24900,
        -29900,
    ]
    y = [
        1400,
        1400,
        1100,
        1100,
        1600,
        1800,
        1900,
        1100,
        2700,
        2000,
        1700,
        2600,
        2400,
        2000,
        1800,
    ]

    energies = [2450, 2474, 2475, 2477, 2484, 2530]
    waxs_arc = np.linspace(0, 78, 13)

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)
        for name, xs, ys in zip(names, x, y):
            yield from bps.mv(piezo.x, xs)
            yield from bps.mv(piezo.y, ys)

            det_exposure_time(t, t)
            name_fmt = "{sample}_{energy}eV_wa{wax}_bpm{xbpm}"
            for e in energies:
                yield from bps.mv(energy, e)
                yield from bps.sleep(2)

                bpm = xbpm2.sumX.value

                sample_name = name_fmt.format(
                    sample=name, energy="%6.2f" % e, wax=wa, xbpm="%4.3f" % bpm
                )
                sample_id(user_name="TM", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 2500)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 2470)
            yield from bps.sleep(2)


def giwaxs_S_edge_terry(t=1):
    dets = [pil300KW, pil1M]

    names = ["pedotpss_1_gisaxs"]
    x = [0]

    energies = [2450, 2474, 2475, 2477, 2484, 2530]
    waxs_arc = np.linspace(0, 78, 13)
    ais0, ys0 = [], []
    for xs in x:
        yield from bps.mv(piezo.x, xs)

        yield from alignement_gisaxs(angle=0.35)
        ais0 = ais0 + [piezo.th.position]
        ys0 = ys0 + [piezo.y.position]
        print(piezo.th.position, piezo.y.position)

    yield from bps.mv(att2_9, "Insert")
    yield from bps.sleep(1)
    yield from bps.mv(att2_9, "Insert")
    yield from bps.sleep(1)

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)
        for name, xs, ai0, ys in zip(names, x, ais0, ys0):
            yield from bps.mv(piezo.x, xs)
            yield from bps.mv(piezo.y, ys)
            yield from bps.mv(piezo.th, ai0)

            yield from bps.mv(piezo.th, ai0 + 0.7)

            det_exposure_time(t, t)
            name_fmt = "{sample}_{energy}eV_ai0.7_wa{wax}_bpm{xbpm}"
            for e in energies:
                yield from bps.mv(energy, e)
                yield from bps.sleep(2)

                bpm = xbpm2.sumX.value

                sample_name = name_fmt.format(
                    sample=name, energy="%6.2f" % e, wax=wa, xbpm="%4.3f" % bpm
                )
                sample_id(user_name="TM", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 2500)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 2470)
            yield from bps.sleep(2)


def WAXS_S_edge_Gomez_night(t=1):
    dets = [pil300KW, pil1M]
    names = ["PA1-3"]
    x_s = [41200]
    y_s = [1300]

    energies = [2456, 2464, 2475, 2477, 2490, 2492]
    det_exposure_time(t, t)

    wa = np.linspace(0, 45.5, 8)

    for x, y, name in zip(x_s, y_s, names):
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(piezo.y, y)

        ys = np.linspace(y, y + 500, 7)

        yield from bps.mv(piezo.y, ys[0])
        yield from NEXAFS_S_edge_Gomez_night(t=0.5, name=name)

    for wax in wa:
        yield from bps.mv(waxs, wax)

        for x, y, name in zip(x_s, y_s, names):
            yield from bps.mv(piezo.x, x)
            yield from bps.mv(piezo.y, y)

            ys = np.linspace(y, y + 500, 7)

            for k, (e, ysss) in enumerate(zip(energies, ys[1:])):
                yield from bps.mv(energy, e)
                yield from bps.mv(piezo.y, ysss)
                name_fmt = "{sample}_{energy}eV_wa{wa}_xbpm{xbpm}"

                sample_name = name_fmt.format(
                    sample=name,
                    energy=e,
                    wa="%2.1f" % wax,
                    xbpm="%3.1f" % xbpm3.sumY.value,
                )
                sample_id(user_name="GZ", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 2470)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 2456)
            yield from bps.sleep(2)

    wa = [0, 6.5, 13.0]
    for wax in wa[::-1]:
        yield from bps.mv(waxs, wax)
        for x, y, name in zip(x_s, y_s, names):
            yield from bps.mv(piezo.x, x)
            yield from bps.mv(piezo.y, y)

            ys = np.linspace(y, y + 500, 7)

            yield from bps.mv(piezo.y, ys[1])

            name_fmt = "{sample}_postmeas_2456eV_wa{wa}_xbpm{xbpm}"
            sample_name = name_fmt.format(
                sample=name, wa="%2.1f" % wax, xbpm="%3.1f" % xbpm3.sumY.value
            )
            sample_id(user_name="GZ", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)

    sample_id(user_name="test", sample_name="test")


def NEXAFS_S_edge_Gomez_night(t=0.5, name="test"):

    yield from bps.mv(waxs, 60)
    dets = [pil300KW]

    energies = np.linspace(2430, 2500, 71)

    det_exposure_time(t, t)
    name_fmt = "nexafs_{sample}_{energy}eV_xbpm{xbpm}"
    for e in energies:
        yield from bps.mv(energy, e)
        sample_name = name_fmt.format(
            sample=name, energy=e, xbpm="%3.1f" % xbpm3.sumY.value
        )
        sample_id(user_name="GZ", sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")
        yield from bp.count(dets, num=1)

    yield from bps.mv(energy, 2470)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 2450)
    yield from bps.sleep(2)

    sample_id(user_name="test", sample_name="test")


def WAXS_S_edge_rad_dmg_test(t=1):
    dets = [pil300KW, pil1M]
    names = ["PA1-3_rad_dmg_test"]

    det_exposure_time(t, t)

    wa = np.linspace(0, 13.0, 3)

    for i in range(0, 5, 1):
        print(i)
        for wax in wa:
            print(wax)
            print(2456)

            yield from bps.mv(waxs, wax)
            yield from bps.mv(energy, 2456)
            name_fmt = "{sample}_{energy}eV_rep{rep}_wa{wa}"

            sample_name = name_fmt.format(
                sample=names[0], energy=2456, rep=i, wa="%2.1f" % wax
            )
            sample_id(user_name="GZ", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)

    sample_id(user_name="test", sample_name="test")


def night_collns():
    # yield from waxs_S_edge_all_energies(t=1)

    # yield from NEXAFS_S_edge_2020_3(t=0.5)

    yield from waxs_S_edge_few_energies(t=1)


def waxs_S_edge_few_energies(t=1):
    dets = [pil300KW, pil1M]

    # names = ['P3t', 'P3N2t', 'P3d', 'ITICd', 'P3N2CNt', 'HTAZd', 'PB1t', 'PB0t', 'PBp25t', 'PBp5t', 'PBp75n', 'PB3t', 'FTAZd', 'PBCBd', 'PBCN3d', 'N2d', 'PCDDd',
    # 'P3n', 'P3N2n', 'PB0n', 'PBp25n', 'PBp5n', 'PB1n', 'PB3n', 'P3N2CNn', 'PCPDd', 'PBp75t', 'PBDCBd', 'Si3N4']
    # x = [43300, 37500, 33000, 27400, 22800, 17800, 12400,  7400,  2200, -3000, -8000, -13000, -19500, -26000, -31200, -36600, -42000,
    # 44500, 39000, 33000, 27000, 21200, 16000, 10000, 4500, -1300, -6600, -12200, -19200]
    # y = [-6500, -6650, -6500, -6700, -6500, -6500, -6500, -6500, -6500, -6500, -6500,  -6500,  -6300,  -5700,  -6000,  -5800,  -5800,
    # 7000,  6800,  7000,  7000,  7000,  7000,  7000,  7000,  7000,  7000,   7000,   7000]

    names = [
        "FTAZd",
        "PBCBd",
        "PBCN3d",
        "N2d",
        "PCDDd",
        "P3n",
        "P3N2n",
        "PB0n",
        "PBp25n",
        "PBp5n",
        "PB1n",
        "PB3n",
        "P3N2CNn",
        "PCPDd",
        "PBp75t",
        "PBDCBd",
        "Si3N4",
    ]
    x = [
        -19500,
        -26000,
        -31200,
        -36600,
        -42000,
        44500,
        39000,
        33000,
        27000,
        21200,
        16000,
        10000,
        4500,
        -1300,
        -6600,
        -12200,
        -19200,
    ]
    y = [
        -6300,
        -5700,
        -6000,
        -5800,
        -5800,
        7000,
        6800,
        7000,
        7000,
        7000,
        7000,
        7000,
        7000,
        7000,
        7000,
        7000,
        7000,
    ]

    energies = [2450, 2474, 2475, 2477, 2484, 2530]
    waxs_arc = np.linspace(0, 26, 5)

    for name, xs, ys in zip(names, x, y):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)

        yss = np.linspace(ys, ys + 500, 6)
        xss = np.array([xs])

        yss, xss = np.meshgrid(yss, xss)
        yss = yss.ravel()
        xss = xss.ravel()

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)

            det_exposure_time(t, t)
            name_fmt = "{sample}_{energy}eV_wa{wax}_bpm{xbpm}"
            for e, xsss, ysss in zip(energies, xss, yss):
                yield from bps.mv(energy, e)
                yield from bps.sleep(1)

                yield from bps.mv(piezo.y, ysss)
                yield from bps.mv(piezo.x, xsss)

                bpm = xbpm3.sumX.value

                sample_name = name_fmt.format(
                    sample=name, energy="%6.2f" % e, wax=wa, xbpm="%4.3f" % bpm
                )
                sample_id(user_name="BC", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 2500)
            yield from bps.mv(energy, 2475)
            yield from bps.mv(energy, 2450)


def giwaxs_S_edge_collins(t=1):
    dets = [pil300KW]

    # names = ['PCPDn', 'PCPDt', 'ITICn', 'PBDCBn', 'PBCN3n', 'PCDDn', 'P3t', 'P3n', 'P3N2n', 'HTAZn', 'HTAZt', 'FTAZn', 'P3N2CNn']
    # x = [53500, 46500, 38500, 31500, 20500, 11800, 3500, -6500, -15500, -24500, -33500, -42200, -50500]

    names = ["N2n", "Si", "PB3n", "PB0n", "PBp25n", "PBp5n", "PBp75n", "PB1n"]
    x = [
        49000,
        39000,
        25000,
        13000,
        4000,
        -5000,
        -17000,
        -30000,
    ]

    energies = [2450, 2474, 2475, 2477, 2484, 2530]
    waxs_arc = np.linspace(0, 26, 5)
    ai0 = 0

    for name, xs in zip(names, x):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.th, ai0)

        yield from bps.mv(GV7.open_cmd, 1)
        yield from bps.sleep(1)
        yield from bps.mv(GV7.open_cmd, 1)
        yield from bps.sleep(1)

        yield from alignement_gisaxs(angle=0.4)

        # yield from bps.mv(att2_9, 'Insert')
        yield from bps.mv(GV7.close_cmd, 1)
        yield from bps.sleep(1)
        # yield from bps.mv(att2_9, 'Insert')
        yield from bps.mv(GV7.close_cmd, 1)
        yield from bps.sleep(1)

        ai0 = piezo.th.position
        yield from bps.mv(piezo.th, ai0 + 0.7)

        xss = np.linspace(xs, xs - 1200, 6)
        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)

            det_exposure_time(t, t)
            name_fmt = "{sample}_{energy}eV_wa{wax}_bpm{xbpm}"
            for e, xsss in zip(energies, xss):
                try:
                    yield from bps.mv(energy, e)
                except:
                    print("energy failed to move, sleep for 30 s")
                    yield from bps.sleep(30)
                    print("Slept for 30 s, try move energy again")
                    yield from bps.mv(energy, e)

                yield from bps.sleep(2)

                yield from bps.mv(piezo.x, xsss)
                bpm = xbpm2.sumX.value

                sample_name = name_fmt.format(
                    sample=name, energy="%6.2f" % e, wax=wa, xbpm="%4.3f" % bpm
                )
                sample_id(user_name="GF", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 2470)
            yield from bps.mv(energy, 2450)


def waxs_S_edge_all_energies(t=1):
    dets = [pil300KW, pil1M]

    names = ["P3N2t", "P3N2CNt"]
    x = [37500, 22800]
    y = [-6650, -6500]

    energies = (
        np.arange(2445, 2470, 5).tolist()
        + np.arange(2470, 2480, 0.25).tolist()
        + np.arange(2480, 2490, 1).tolist()
        + np.arange(2490, 2501, 5).tolist()
    )
    waxs_arc = np.linspace(0, 26, 5)

    for name, xs, ys in zip(names, x, y):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)

        yss = np.linspace(ys, ys + 1200, 32)
        xss = np.linspace(xs, xs + 1000, 3)

        yss, xss = np.meshgrid(yss, xss)
        yss = yss.ravel()
        xss = xss.ravel()

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)

            det_exposure_time(t, t)
            name_fmt = "{sample}_{energy}eV_wa{wax}_bpm{xbpm}"
            for e, xsss, ysss in zip(energies, xss, yss):
                yield from bps.mv(energy, e)
                yield from bps.sleep(1)

                yield from bps.mv(piezo.y, ysss)
                yield from bps.mv(piezo.x, xsss)

                bpm = xbpm3.sumX.value

                sample_name = name_fmt.format(
                    sample=name, energy="%6.2f" % e, wax=wa, xbpm="%4.3f" % bpm
                )
                sample_id(user_name="BC", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 2480)
            yield from bps.mv(energy, 2465)
            yield from bps.mv(energy, 2450)


def NEXAFS_S_edge_2020_3(t=0.5):
    yield from bps.mv(GV7.close_cmd, 1)
    yield from bps.sleep(1)
    yield from bps.mv(GV7.close_cmd, 1)

    yield from bps.mv(waxs, 52)
    dets = [pil300KW]

    energies = (
        np.arange(2450, 2470, 5).tolist()
        + np.arange(2470, 2475.5, 0.25).tolist()
        + np.arange(2475.5, 2478.5, 0.1).tolist()
        + np.arange(2478.5, 2482, 0.25).tolist()
        + np.arange(2482, 2500, 1).tolist()
        + np.arange(2500, 2535, 5).tolist()
    )

    #    names = ['ITICd','HTAZd','FTAZd', 'PBCBd', 'PBCN3d', 'N2d', 'PCDDd', 'PCPDd','PBDCBd']
    #    x = [27400,17800, -19500, -26000, -31200, -36600, -42000, -1300, -12200]
    #    y = [-6700,-6500, -6300,  -5700,  -6000,  -5800,  -5800,  7000,  7000]
    names = ["PCPDd", "PBDCBd"]
    x = [-1300, -12200]
    y = [7000, 7000]

    for name, xs, ys in zip(names, x, y):
        yield from bps.mv(piezo.x, xs + 500)
        yield from bps.mv(piezo.y, ys + 200)

        det_exposure_time(t, t)
        name_fmt = "nexafs_{sample}_{energy}eV_xbpm{xbpm}"
        for e in energies:
            yield from bps.mv(energy, e)
            yield from bps.sleep(1)
            sample_name = name_fmt.format(
                sample=name, energy=e, xbpm="%3.1f" % xbpm3.sumY.value
            )
            RE.md["filename"] = sample_name
            sample_id(user_name="BC", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)

        yield from bps.mv(energy, 2510)
        yield from bps.sleep(1)
        yield from bps.mv(energy, 2490)
        yield from bps.sleep(1)
        yield from bps.mv(energy, 2470)
        yield from bps.sleep(1)
        yield from bps.mv(energy, 2450)

        sample_id(user_name="test", sample_name="test")

    yield from bps.mv(GV7.open_cmd, 1)
    yield from bps.sleep(1)
    yield from bps.mv(GV7.open_cmd, 1)


def NEXAFS_S_edge_2021_2(t=0.5):
    yield from bps.mv(waxs, 59)
    dets = [pil300KW, pil900KW]

    energies = (
        np.arange(2450, 2470, 5).tolist()
        + np.arange(2470, 2475.5, 0.25).tolist()
        + np.arange(2475.5, 2478.5, 0.1).tolist()
        + np.arange(2478.5, 2482, 0.25).tolist()
        + np.arange(2482, 2500, 1).tolist()
        + np.arange(2500, 2535, 5).tolist()
    )

    # names = ['PM7_1',  'PM7_2',   'PCD_1',   'PCD_2',    'PB_1',    'PB_2', 'PCP_1', 'PCP_2', 'PM6_1', 'PM6_2',  'FT_1',
    #         'P3HT_1', 'P3HT_2', 'PTQ10_1', 'PTQ10_2', 'D18Cl_1', 'D18Cl_2',  'HT_1',  'HT_2',  'P7_1',  'P7_2',  'FT_2',
    #           'Y6_1',   'Y6_2',    'IT_1',    'IT_2', 'PBTTT_1', 'PBTTT_2', 'Y11_1', 'Y11_2', 'D18_1', 'D18_2', 'SiN_1']
    # x = [      32100,    25200,     18200,     11200,      4200,     -3200,  -10300,  -16600,  -22800,  -29500,  -36100,
    #            32000,    25200,     17900,     11200,      4200,     -3200,  -10300,  -16600,  -22500,  -29300,  -36100,
    #            32700,    25000,     17300,     11200,      4400,     -3400,  -10300,  -16600,  -22800,  -29300,  -36300]
    # y = [      -6600,    -6700,     -6800,     -6800,     -6900,     -6900,   -6900,   -6900,   -6900,   -6900,   -6900,
    #            -1300,     -900,      -900,      -900,      -900,      -900,   -1000,    -900,   -1000,    -700,    -300,
    #             4800,     4600,      4200,      4500,      4700,      4900,    4700,     4700,    4900,    4800,   5000]

    names = ["Y11_2", "D18_1", "D18_2", "SiN_1"]
    x = [-16600, -22800, -29300, -36300]
    y = [4700, 4900, 4800, 5000]

    for name, xs, ys in zip(names, x, y):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)

        yss = np.linspace(ys, ys + 1000, 95)
        xss = [xs]

        yss, xss = np.meshgrid(yss, xss)
        yss = yss.ravel()
        xss = xss.ravel()

        det_exposure_time(t, t)
        name_fmt = "nexafs_90deg_wa59deg_{sample}_{energy}eV_xbpm{xbpm}"
        for e, xsss, ysss in zip(energies, xss, yss):
            yield from bps.mv(energy, e)
            yield from bps.sleep(1)

            yield from bps.mv(piezo.y, ysss)
            yield from bps.mv(piezo.x, xsss)

            sample_name = name_fmt.format(
                sample=name, energy="%6.2f" % e, xbpm="%3.1f" % xbpm3.sumY.value
            )
            RE.md["filename"] = sample_name
            sample_id(user_name="BC", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)

        yield from bps.mv(energy, 2510)
        yield from bps.sleep(1)
        yield from bps.mv(energy, 2490)
        yield from bps.sleep(1)
        yield from bps.mv(energy, 2470)
        yield from bps.sleep(1)
        yield from bps.mv(energy, 2450)

        sample_id(user_name="test", sample_name="test")


def NEXAFS_S_edge_2021_2_set1(t=0.5):
    yield from bps.mv(waxs, 59)
    dets = [pil300KW, pil900KW]

    energies = (
        np.arange(2450, 2470, 5).tolist()
        + np.arange(2470, 2475.5, 0.25).tolist()
        + np.arange(2475.5, 2478.5, 0.1).tolist()
        + np.arange(2478.5, 2482, 0.25).tolist()
        + np.arange(2482, 2500, 1).tolist()
        + np.arange(2500, 2535, 5).tolist()
    )

    # # # names = ['Y11_1',   'D18_1',   'SiN_1']
    # # # x = [     -10700,    -23500,    -37400]
    # # # y = [       4700,      4900,      5000]

    # # assert len(names) == len(x), f'Number of X coordinates ({len(x)}) is different from number of samples ({len(names)})'
    # # assert len(names) == len(y), f'Number of X coordinates ({len(y)}) is different from number of samples ({len(names)})'

    # # yield from bps.mv(prs, -60)

    # # for name, xs, ys in zip(names, x, y):
    # #     yield from bps.mv(piezo.x, xs)
    # #     yield from bps.mv(piezo.y, ys)

    # #     yss = np.linspace(ys, ys + 1000, 95)
    # #     xss = [xs]

    # #     yss, xss = np.meshgrid(yss, xss)
    # #     yss = yss.ravel()
    # #     xss = xss.ravel()

    #     det_exposure_time(t,t)
    #     name_fmt = 'nexafs_30deg_wa59deg_{sample}_{energy}eV_xbpm{xbpm}'
    #     for e, xsss, ysss in zip(energies, xss, yss):
    #         yield from bps.mv(energy, e)
    #         yield from bps.sleep(2)

    #         yield from bps.mv(piezo.y, ysss)
    #         yield from bps.mv(piezo.x, xsss)

    #         sample_name = name_fmt.format(sample=name, energy='%6.2f'%e, xbpm = '%3.1f'%xbpm3.sumY.value)
    #         RE.md['filename'] = sample_name
    #         sample_id(user_name='BC', sample_name=sample_name)
    #         print(f'\n\t=== Sample: {sample_name} ===\n')
    #         yield from bp.count(dets, num=1)

    # yield from bps.mv(energy, 2510)
    # yield from bps.sleep(2)
    # yield from bps.mv(energy, 2490)
    # yield from bps.sleep(2)
    # yield from bps.mv(energy, 2470)
    # yield from bps.sleep(2)
    # yield from bps.mv(energy, 2450)

    # sample_id(user_name='test', sample_name='test')

    names = ["FT_1", "P3HT_1", "Y6_1"]
    x = [-37700, 31200, 31800]
    y = [-6900, -1300, 4800]

    yield from bps.mv(prs, -20)
    for name, xs, ys in zip(names, x, y):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)

        yss = np.linspace(ys, ys + 1000, 95)
        xss = [xs]

        yss, xss = np.meshgrid(yss, xss)
        yss = yss.ravel()
        xss = xss.ravel()

        det_exposure_time(t, t)
        name_fmt = "nexafs_70deg_wa59deg_{sample}_{energy}eV_xbpm{xbpm}"
        for e, xsss, ysss in zip(energies, xss, yss):
            yield from bps.mv(energy, e)
            yield from bps.sleep(2)

            yield from bps.mv(piezo.y, ysss)
            yield from bps.mv(piezo.x, xsss)

            sample_name = name_fmt.format(
                sample=name, energy="%6.2f" % e, xbpm="%3.1f" % xbpm3.sumY.value
            )
            RE.md["filename"] = sample_name
            sample_id(user_name="BC", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)

        yield from bps.mv(energy, 2510)
        yield from bps.sleep(2)
        yield from bps.mv(energy, 2490)
        yield from bps.sleep(2)
        yield from bps.mv(energy, 2470)
        yield from bps.sleep(2)
        yield from bps.mv(energy, 2450)

        sample_id(user_name="test", sample_name="test")

    # names = ['PM7_1',  'PCD_1',    'PB_1',   'PCP_1',   'PM6_1',    'FT_1',
    #         'P3HT_1','PTQ10_1', 'D18Cl_1',    'HT_1',    'P7_1',
    #           'Y6_1',   'IT_1', 'PBTTT_1',   'Y11_1',   'D18_1',   'SiN_1']
    # x = [      31100,    17000,      3000,    -11800,    -24900,    -38300,
    #            32000,    17200,      3400,    -11400,    -23800,
    #            32700,    17300,      4200,    -10700,    -23500,    -37400]
    # y = [      -6600,    -6800,     -6900,     -6900,     -6900,     -6900,
    #            -1300,     -900,      -900,     -1000,     -1000,
    #             4800,     4200,      4700,      4700,      4900,      5000]

    # yield from bps.mv(prs, -35)
    # for name, xs, ys in zip(names, x, y):
    #     yield from bps.mv(piezo.x, xs)
    #     yield from bps.mv(piezo.y, ys)

    #     yss = np.linspace(ys, ys + 1000, 95)
    #     xss = [xs]

    #     yss, xss = np.meshgrid(yss, xss)
    #     yss = yss.ravel()
    #     xss = xss.ravel()

    #     det_exposure_time(t,t)
    #     name_fmt = 'nexafs_55deg_wa59deg_{sample}_{energy}eV_xbpm{xbpm}'
    #     for e, xsss, ysss in zip(energies, xss, yss):
    #         yield from bps.mv(energy, e)
    #         yield from bps.sleep(2)

    #         yield from bps.mv(piezo.y, ysss)
    #         yield from bps.mv(piezo.x, xsss)

    #         sample_name = name_fmt.format(sample=name, energy='%6.2f'%e, xbpm = '%3.1f'%xbpm3.sumY.value)
    #         RE.md['filename'] = sample_name
    #         sample_id(user_name='BC', sample_name=sample_name)
    #         print(f'\n\t=== Sample: {sample_name} ===\n')
    #         yield from bp.count(dets, num=1)

    #     yield from bps.mv(energy, 2510)
    #     yield from bps.sleep(2)
    #     yield from bps.mv(energy, 2490)
    #     yield from bps.sleep(2)
    #     yield from bps.mv(energy, 2470)
    #     yield from bps.sleep(2)
    #     yield from bps.mv(energy, 2450)

    #     sample_id(user_name='test', sample_name='test')

    # names = ['D18Cl_1',    'HT_1',    'P7_1',
    #           'Y6_1',   'IT_1', 'PBTTT_1',   'Y11_1',   'D18_1']
    # x = [       3400,    -11400,    -23800,
    #            32100,    16900,      3800,    -11000,    -23900,    -37600]
    # y = [       -900,     -1000,     -1000,
    #             4800,     4200,      4700,      4700,      4900]

    # yield from bps.mv(prs, -50)
    # for name, xs, ys in zip(names, x, y):
    #     yield from bps.mv(piezo.x, xs)
    #     yield from bps.mv(piezo.y, ys)

    #     yss = np.linspace(ys, ys + 1000, 95)
    #     xss = [xs]

    #     yss, xss = np.meshgrid(yss, xss)
    #     yss = yss.ravel()
    #     xss = xss.ravel()

    #     det_exposure_time(t,t)
    #     name_fmt = 'nexafs_40deg_wa59deg_{sample}_{energy}eV_xbpm{xbpm}'
    #     for e, xsss, ysss in zip(energies, xss, yss):
    #         yield from bps.mv(energy, e)
    #         yield from bps.sleep(1)

    #         yield from bps.mv(piezo.y, ysss)
    #         yield from bps.mv(piezo.x, xsss)

    #         sample_name = name_fmt.format(sample=name, energy='%6.2f'%e, xbpm = '%3.1f'%xbpm3.sumY.value)
    #         RE.md['filename'] = sample_name
    #         sample_id(user_name='BC', sample_name=sample_name)
    #         print(f'\n\t=== Sample: {sample_name} ===\n')
    #         yield from bp.count(dets, num=1)

    #     yield from bps.mv(energy, 2510)
    #     yield from bps.sleep(2)
    #     yield from bps.mv(energy, 2490)
    #     yield from bps.sleep(2)
    #     yield from bps.mv(energy, 2470)
    #     yield from bps.sleep(2)
    #     yield from bps.mv(energy, 2450)

    #     sample_id(user_name='test', sample_name='test')


def NEXAFS_S_edge_2021_2_set2(t=0.5):
    yield from bps.mv(waxs, 59)
    dets = [pil300KW, pil900KW]

    energies = (
        np.arange(2450, 2470, 5).tolist()
        + np.arange(2470, 2475.5, 0.25).tolist()
        + np.arange(2475.5, 2478.5, 0.1).tolist()
        + np.arange(2478.5, 2482, 0.25).tolist()
        + np.arange(2482, 2500, 1).tolist()
        + np.arange(2500, 2535, 5).tolist()
    )

    names = [
        "PM7_2",
        "PCD_2",
        "PB_2",
        "PCP_2",
        "PM6_2",
        "P3HT_2",
        "PTQ10_2",
        "D18Cl_2",
        "HT_2",
        "P7_2",
        "FT_2",
        "Y6_2",
        "IT_2",
        "PBTTT_2",
        "Y11_2",
        "D18_2",
    ]
    x = [
        24100,
        10000,
        -4500,
        -18300,
        -31800,
        24800,
        10600,
        -4200,
        -17800,
        -30800,
        -37600,
        25400,
        11100,
        -3800,
        -17100,
        -30300,
    ]
    y = [
        -6700,
        -6800,
        -6900,
        -6900,
        -6900,
        -900,
        -900,
        -900,
        -900,
        -700,
        -300,
        4600,
        4500,
        4900,
        4700,
        4800,
    ]

    assert len(names) == len(
        x
    ), f"Number of X coordinates ({len(x)}) is different from number of samples ({len(names)})"
    assert len(names) == len(
        y
    ), f"Number of X coordinates ({len(y)}) is different from number of samples ({len(names)})"

    yield from bps.mv(prs, -60)

    for name, xs, ys in zip(names, x, y):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)

        yss = np.linspace(ys, ys + 1000, 95)
        xss = [xs]

        yss, xss = np.meshgrid(yss, xss)
        yss = yss.ravel()
        xss = xss.ravel()

        det_exposure_time(t, t)
        name_fmt = "nexafs_30deg_wa59deg_{sample}_{energy}eV_xbpm{xbpm}"
        for e, xsss, ysss in zip(energies, xss, yss):
            yield from bps.mv(energy, e)
            yield from bps.sleep(2)

            yield from bps.mv(piezo.y, ysss)
            yield from bps.mv(piezo.x, xsss)

            sample_name = name_fmt.format(
                sample=name, energy="%6.2f" % e, xbpm="%3.1f" % xbpm3.sumY.value
            )
            RE.md["filename"] = sample_name
            sample_id(user_name="BC", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)

        yield from bps.mv(energy, 2510)
        yield from bps.sleep(2)
        yield from bps.mv(energy, 2490)
        yield from bps.sleep(2)
        yield from bps.mv(energy, 2470)
        yield from bps.sleep(2)
        yield from bps.mv(energy, 2450)

        sample_id(user_name="test", sample_name="test")

    yield from bps.mv(prs, -20)
    for name, xs, ys in zip(names, x, y):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)

        yss = np.linspace(ys, ys + 1000, 95)
        xss = [xs]

        yss, xss = np.meshgrid(yss, xss)
        yss = yss.ravel()
        xss = xss.ravel()

        det_exposure_time(t, t)
        name_fmt = "nexafs_70deg_wa59deg_{sample}_{energy}eV_xbpm{xbpm}"
        for e, xsss, ysss in zip(energies, xss, yss):
            yield from bps.mv(energy, e)
            yield from bps.sleep(2)

            yield from bps.mv(piezo.y, ysss)
            yield from bps.mv(piezo.x, xsss)

            sample_name = name_fmt.format(
                sample=name, energy="%6.2f" % e, xbpm="%3.1f" % xbpm3.sumY.value
            )
            RE.md["filename"] = sample_name
            sample_id(user_name="BC", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)

        yield from bps.mv(energy, 2510)
        yield from bps.sleep(2)
        yield from bps.mv(energy, 2490)
        yield from bps.sleep(2)
        yield from bps.mv(energy, 2470)
        yield from bps.sleep(2)
        yield from bps.mv(energy, 2450)

        sample_id(user_name="test", sample_name="test")

    yield from bps.mv(prs, -35)
    for name, xs, ys in zip(names, x, y):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)

        yss = np.linspace(ys, ys + 1000, 95)
        xss = [xs]

        yss, xss = np.meshgrid(yss, xss)
        yss = yss.ravel()
        xss = xss.ravel()

        det_exposure_time(t, t)
        name_fmt = "nexafs_55deg_wa59deg_{sample}_{energy}eV_xbpm{xbpm}"
        for e, xsss, ysss in zip(energies, xss, yss):
            yield from bps.mv(energy, e)
            yield from bps.sleep(2)

            yield from bps.mv(piezo.y, ysss)
            yield from bps.mv(piezo.x, xsss)

            sample_name = name_fmt.format(
                sample=name, energy="%6.2f" % e, xbpm="%3.1f" % xbpm3.sumY.value
            )
            RE.md["filename"] = sample_name
            sample_id(user_name="BC", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)

        yield from bps.mv(energy, 2510)
        yield from bps.sleep(2)
        yield from bps.mv(energy, 2490)
        yield from bps.sleep(2)
        yield from bps.mv(energy, 2470)
        yield from bps.sleep(2)
        yield from bps.mv(energy, 2450)

        sample_id(user_name="test", sample_name="test")

    yield from bps.mv(prs, -50)
    for name, xs, ys in zip(names, x, y):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)

        yss = np.linspace(ys, ys + 1000, 95)
        xss = [xs]

        yss, xss = np.meshgrid(yss, xss)
        yss = yss.ravel()
        xss = xss.ravel()

        det_exposure_time(t, t)
        name_fmt = "nexafs_40deg_wa59deg_{sample}_{energy}eV_xbpm{xbpm}"
        for e, xsss, ysss in zip(energies, xss, yss):
            yield from bps.mv(energy, e)
            yield from bps.sleep(2)

            yield from bps.mv(piezo.y, ysss)
            yield from bps.mv(piezo.x, xsss)

            sample_name = name_fmt.format(
                sample=name, energy="%6.2f" % e, xbpm="%3.1f" % xbpm3.sumY.value
            )
            RE.md["filename"] = sample_name
            sample_id(user_name="BC", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)

        yield from bps.mv(energy, 2510)
        yield from bps.sleep(2)
        yield from bps.mv(energy, 2490)
        yield from bps.sleep(2)
        yield from bps.mv(energy, 2470)
        yield from bps.sleep(2)
        yield from bps.mv(energy, 2450)

        sample_id(user_name="test", sample_name="test")


def NEXAFS_collins_night(t=0.5):
    proposal_id("2021_2", "307835_Collins4")
    yield from NEXAFS_S_edge_2021_2_set1(t=t)

    proposal_id("2021_2", "307835_Collins5")
    yield from NEXAFS_S_edge_2021_2_set2(t=t)

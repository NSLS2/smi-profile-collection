def alignement_gordon_2021_1():
    global names, x_piezo, z_piezo, incident_angles, y_piezo_aligned

    # names =   ['p3ht', 'p3rse', 'p3rt', 'p3rte', 'p3ht_doped', 'p3rse_doped', 'p3rt_doped', 'p3rte_doped']
    # x_piezo = [ 50000,  37000,   25000,   10000,        -7000,        -22000,       -37000,        -48000]
    # y_piezo = [  6800,   6800,   6800,     6800,         6800,          6800,         6800,          6800]
    # z_piezo = [ -1300,  -1300,   -1300,   -1300,          700,           700,          700,           700]

    # incident_angles = [-0.130468, -0.005243, -0.097427, 0.132971,    0.179, -0.008362, 0.036502, 0.020989]
    # y_piezo_aligned = [ 6641.484,  6689.479,   6755.62, 6802.845, 6888.982,  6995.038, 7078.288, 7129.521]

    names = ["p3rse_2", "p3rse_doped_2"]
    x_piezo = [36000, -23000]
    y_piezo = [6800, 6800]
    z_piezo = [-1300, 700]

    incident_angles = [-0.005243, -0.008362]
    y_piezo_aligned = [6689.479, 6995.038]

    # smi = SMI_Beamline()
    # yield from smi.modeAlignment(technique='gisaxs')

    # for name, xs_piezo, ys_piezo, zs_piezo in zip(names, x_piezo, y_piezo, z_piezo):
    #     yield from bps.mv(piezo.x, xs_piezo)
    #     yield from bps.mv(piezo.y, ys_piezo)
    #     yield from bps.mv(piezo.z, zs_piezo)

    #     yield from alignement_gisaxs_multisample(angle = 0.1)

    #     incident_angles = incident_angles + [piezo.th.position]
    #     y_piezo_aligned = y_piezo_aligned + [piezo.y.position]

    # yield from smi.modeMeasurement()

    # print(incident_angles)


def run_gordon_2021_1(t=1):

    waxs_range = np.linspace(0, 26.0, 5)
    dets = [pil300KW, pil1M]

    for name, xs, zs, aiss, ys in zip(
        names, x_piezo, z_piezo, incident_angles, y_piezo_aligned
    ):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)
        yield from bps.mv(piezo.th, aiss)

        ai0 = piezo.th.position

        # yield from bps.mvr(piezo.th, angl)
        name_fmt = "{sample}_16.1keV_ai{angle}deg_wa{wax}"

        det_exposure_time(t, t)
        angl = [0.12, 0.15, 0.2]

        for wa in waxs_range:
            yield from bps.mv(waxs, wa)
            for i, ang in enumerate(angl):
                yield from bps.mv(piezo.th, ai0 + ang)
                yield from bps.mv(piezo.x, xs + i * 200)

                sample_name = name_fmt.format(
                    sample=name, angle="%3.2f" % ang, wax="%2.1f" % wa
                )
                sample_id(user_name="MG", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

        sample_id(user_name="test", sample_name="test")
        det_exposure_time(0.3, 0.3)


def waxs_S_edge_gordon_2021_2(t=1):
    dets = [pil300KW]

    # names = ['pbTTT_neat', 'p3RT_neat', 'pbTTT_dopped', 'p3RT_dopped']
    # x = [   26200, 20400, 14100, 7300]
    # y = [     700,   500,   900,  500]

    names = ["p3RT_dopped"]
    x = [7300]
    y = [500]

    energies = (
        np.arange(2445, 2470, 5).tolist()
        + np.arange(2470, 2480, 0.25).tolist()
        + np.arange(2480, 2490, 1).tolist()
        + np.arange(2490, 2501, 5).tolist()
    )
    waxs_arc = np.linspace(0, 39, 7)

    for name, xs, ys in zip(names, x, y):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)

        yss = np.linspace(ys, ys + 400, 31)
        xss = np.array([xs, xs + 400])

        yss, xss = np.meshgrid(yss, xss)
        yss = yss.ravel()
        xss = xss.ravel()

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)

            det_exposure_time(t, t)

            if wa == 0 and name != "pbTTT_neat":
                yield from bps.mv(energy, 2450)
                name_fmt = "int_cor_{sample}_{energy}eV_wa{wax}_bpm{xbpm}"
                for e, xsss, ysss in zip(energies, xss, yss):
                    yield from bps.sleep(0.5)

                    yield from bps.mv(piezo.y, ysss)
                    yield from bps.mv(piezo.x, xsss)

                    bpm = xbpm2.sumX.value
                    sample_name = name_fmt.format(
                        sample=name, energy="%6.2f" % e, wax=wa, xbpm="%4.3f" % bpm
                    )
                    sample_id(user_name="GF", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")

                    yield from bp.count(dets, num=1)

            name_fmt = "{sample}_{energy}eV_wa{wax}_bpm{xbpm}"
            for e, xsss, ysss in zip(energies, xss, yss):
                yield from bps.mv(energy, e)
                yield from bps.sleep(2)

                yield from bps.mv(piezo.y, ysss)
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


def gordon_saxswaxs_2021_2(t=1):
    dets = [pil300KW, pil1M]

    waxs_arc = np.linspace(0, 32.5, 6)

    # names = ['pbTTT_neat', 'p3RT_neat', 'pbTTT_dopped', 'p3RT_dopped']
    # x = [   24600, 19300, 14500, 7700]
    # y = [    6800,  6800,  6900, 7400]

    names = ["pbTTT_dopped"]
    x = [14500]
    y = [6900]

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)

        for name, xs, ys in zip(names, x, y):
            yield from bps.mv(piezo.x, xs)
            yield from bps.mv(piezo.y, ys)
            xss = [0, -300]

            det_exposure_time(t, t)
            name_fmt = "{sample}_16.1keV_pos{pos}_wa{wax}_sdd1.6m"
            for k, xsss in enumerate(xss):
                yield from bps.mv(piezo.x, xs + xsss)

                sample_name = name_fmt.format(sample=name, pos=k, wax=wa)
                sample_id(user_name="GF", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)


def gisaxs1_gordon_2021_2(t=1):

    names = [
        "sample02",
        "sample03",
        "sample06",
        "sample07",
        "sample10",
        "sample12",
        "sample14",
        "sample15",
        "sample18",
    ]
    x_piezo = [59000, 58000, 45000, 32000, 19000, 5000, -7000, -19000, -30000]
    y_piezo = [6800, 6800, 6800, 6800, 6800, 6800, 6800, 6800, 6800]
    z_piezo = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    x_hexa = [12, 0, 0, 0, 0, 0, 0, 0, 0]

    # names = ['sample20', 'sample21', 'sample23', 'sample24', 'sample27', 'sample28']
    # x_piezo = [   58000,      55000,      42000,      29000,      14000,          0]
    # y_piezo = [    6800,       6800,       6800,       6800,       6800,       6800]
    # z_piezo = [       0,          0,          0,          0,          0,          0]
    # x_hexa =  [      10,          0,          0,          0,          0,          0]

    assert len(x_piezo) == len(
        names
    ), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(
        y_piezo
    ), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(
        z_piezo
    ), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(z_piezo)})"
    assert len(x_piezo) == len(
        x_hexa
    ), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexa)})"

    waxs_arc = [0, 2, 19.5, 21.5, 39, 41]
    angle = [0.1, 0.15, 0.2]

    dets = [pil1M, pil900KW, pil300KW]
    det_exposure_time(t, t)

    for name, xs, zs, ys, xs_hexa in zip(names, x_piezo, z_piezo, y_piezo, x_hexa):
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)
        yield from bps.mv(piezo.th, 0)

        yield from alignement_gisaxs(angle=0.15)

        ai0 = piezo.th.position
        det_exposure_time(t, t)
        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)

            for an in angle:
                yield from bps.mv(piezo.th, ai0 + an)
                name_fmt = "{sample}_sdd1.6m_14keV_ai{angl}deg_wa{waxs}"
                sample_name = name_fmt.format(
                    sample=name, angl="%3.2f" % an, waxs="%2.1f" % wa
                )
                sample_id(user_name="PT", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")

                yield from bp.count(dets, num=1)

            yield from bps.mv(piezo.th, ai0)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.1, 0.1)


def gisaxs2_gordon_2021_2(t=1):

    names = [
        "pedot_EHE_neat",
        "pedot_EHE_FeCl3",
        "pedot_EHE_rosy",
        "pedot_OH_neat",
        "pedot_OH_FeCl3",
        "pedot_OH_rosy",
    ]
    x_piezo = [-13000, -22000, -30000, -38000, -48000, -55000]
    y_piezo = [6800, 6800, 6800, 6800, 6800, 6800]
    z_piezo = [0, 0, 0, 0, 0, 0]
    x_hexa = [0, 0, 0, 0, 0, -2]

    assert len(x_piezo) == len(
        names
    ), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(
        y_piezo
    ), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(
        z_piezo
    ), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(z_piezo)})"
    assert len(x_piezo) == len(
        x_hexa
    ), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexa)})"

    waxs_arc = [0, 2, 19.5, 21.5, 39, 41]
    angle = [0.1, 0.15, 0.2]

    dets = [pil1M, pil900KW, pil300KW]
    det_exposure_time(t, t)

    for name, xs, zs, ys, xs_hexa in zip(names, x_piezo, z_piezo, y_piezo, x_hexa):
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)
        yield from bps.mv(piezo.th, 0)

        yield from alignement_gisaxs(angle=0.15)

        ai0 = piezo.th.position
        det_exposure_time(t, t)
        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)

            for an in angle:
                yield from bps.mv(piezo.th, ai0 + an)
                name_fmt = "{sample}_sdd1.6m_14keV_ai{angl}deg_wa{waxs}"
                sample_name = name_fmt.format(
                    sample=name, angl="%3.2f" % an, waxs="%2.1f" % wa
                )
                sample_id(user_name="PT", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")

                yield from bp.count(dets, num=1)

            yield from bps.mv(piezo.th, ai0)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.1, 0.1)


def giwaxs_several(t=1):
    yield from gisaxs1_gordon_2021_2(t=t)

    yield from bps.sleep(5)
    proposal_id("2021_2", "307830_Su6")
    yield from gisaxs2_gordon_2021_2(t=t)


def gisaxs_gordon_2021_3(t=1):

    # names = ['PBOE-D', 'POH-D', 'PMDE-E', 'POH-E', 'PODE-E2', 'POH-E2', 'PEDOT-EHE', 'PEDOT-OH', 'PBOE-D_FeTos', 'POH-D_FeTos', 'PHDE-E_FeTos', 'POH-E_FeTos', 'PODE-E2_FeTos', 'POH-E2_FeTos',
    # 'PEDOT-EHE_FeTos']
    # x_piezo = [ 56500, 56500, 49000, 39000, 29000, 19000, 9000, -3000, -12000, -23000, -31000, -40000, -49000, -53000, -56000]
    # y_piezo = [  4100,  4100,  4100,  4100,  4100,  4100, 4100,  4100,   4100,   4100,   4100,   4100,   4100,   4100,   4100]
    # z_piezo = [  1000,  1000,  1000,  1000,  1000,  1000, 1000,  1000,   1000,   1000,   1000,   1000,   1000,   1000,   1000]
    # x_hexa =  [    12,     2,     0,     0,     0,     0,    0,     0,      0,      0,      0,      0,      0,     -5,    -10]

    names = [
        "PEDOT-OH_FeTos",
        "PBTTT_pristine",
        "PBTTT_0.9",
        "PBTTT_2.5",
        "PBTTT_50",
        "PEDOT-OE3_pritine",
        "PEDOT-OE3_0.1",
        "PEDOT-OE3_0.5",
        "PEDOT-OE3_5.0",
        "PEDOT-OE3_50",
        "Si_wafer",
    ]
    x_piezo = [
        56500,
        56000,
        42000,
        30000,
        16000,
        4000,
        -8000,
        -20000,
        -34000,
        -46000,
        -48000,
    ]
    y_piezo = [4100, 4100, 4100, 4100, 4100, 4100, 4100, 4100, 4100, 4100, 4100]
    z_piezo = [1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000]
    x_hexa = [10, 0, 0, 0, 0, 0, 0, 0, 0, 0, -10]

    assert len(x_piezo) == len(
        names
    ), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(
        y_piezo
    ), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(
        z_piezo
    ), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(z_piezo)})"
    assert len(x_piezo) == len(
        x_hexa
    ), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexa)})"

    waxs_arc = [0, 2, 20, 22, 40, 42]
    angle = [0.1, 0.15, 0.2]

    dets = [pil900KW, pil1M]
    det_exposure_time(t, t)

    for name, xs, zs, ys, xs_hexa in zip(names, x_piezo, z_piezo, y_piezo, x_hexa):
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)
        yield from bps.mv(piezo.th, 0)

        yield from alignement_gisaxs(angle=0.15)

        ai0 = piezo.th.position
        det_exposure_time(t, t)
        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)

            for i, an in enumerate(angle):
                yield from bps.mv(piezo.x, xs + i * 200)
                yield from bps.mv(piezo.th, ai0 + an)
                name_fmt = "{sample}_sdd1.8m_14keV_ai{angl}deg_wa{waxs}"
                sample_name = name_fmt.format(
                    sample=name, angl="%3.2f" % an, waxs="%2.1f" % wa
                )
                sample_id(user_name="PT", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")

                yield from bp.count(dets, num=1)

            yield from bps.mv(piezo.th, ai0)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.1, 0.1)


def temp_2021_3(tim=0.5):
    temperatures = [30, 40, 50, 60, 70, 80, 90, 100, 110, 120]

    name = "GF"

    samples = [
        "PBOE-D_FeTos",
        "POH-D_FeTos",
        "PEDOT-EHE_FeTos",
        "PEDOT-OH_FeTos",
        "PEDOT-OH_FeCl3",
    ]
    x_list = [-4000, 9000, 20000, 32000, 47000]
    y_list = [-800, -800, -800, -800, -800]

    assert len(x_list) == len(
        y_list
    ), f"Number of X coordinates ({len(x_list)}) is different from number of Y coordinates ({len(y_list)})"
    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"

    # Detectors, motors:
    dets = [pil1M, pil900KW]
    angle = [0.1, 0.15, 0.2]

    waxs_arc = [0, 20, 40]
    name_fmt = "{sample}_14keV_1.8m_{temperature}C_wa{waxs}"

    det_exposure_time(tim, tim)
    for i_t, t in enumerate(temperatures):
        t_kelvin = t + 273.15
        yield from ls.output1.mv_temp(t_kelvin)
        temp = ls.input_A.get()

        while abs(temp - t_kelvin) > 2:
            print(abs(temp - t_kelvin))
            yield from bps.sleep(10)
            temp = ls.input_A.get()

        # yield from bps.sleep(300)
        t_celsius = temp - 273.15

        for name, xs, ys in zip(samples, x_list, y_list):
            yield from bps.mv(piezo.x, xs + i_t * 200)
            # yield from bps.mv(piezo.y, ys)
            # yield from bps.mv(piezo.th, 0)

            yield from alignement_gisaxs_refbeam(angle=0.15)

            ai0 = piezo.th.position
            for wa in waxs_arc:
                yield from bps.mv(waxs, wa)

                for i, an in enumerate(angle):
                    yield from bps.mv(piezo.x, xs)
                    yield from bps.mv(piezo.th, ai0 + an)
                    name_fmt = "{sample}_{temp}C_sdd1.8m_14keV_ai{angl}deg_wa{waxs}"
                    sample_name = name_fmt.format(
                        sample=name,
                        temp="%3.3d" % t,
                        angl="%3.2f" % an,
                        waxs="%2.1f" % wa,
                    )
                    sample_id(user_name="PT", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")

                    yield from bp.count(dets, num=1)

                yield from bps.mv(piezo.th, ai0)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)

    t_kelvin = 25 + 273.15
    yield from ls.output1.mv_temp(t_kelvin)


def gisaxs_gordon_2022_1(t=1):

    # # sample names starting from the bottom of the sample stage
    # names = ['Si_wafer', 'P3RX_copoly_400', 'P3RX_copoly_100', 'P3RX_copoly_25', 'P3RX_copoly_6', 'P3RX_copoly_3',
    #          'P3RX_copoly_1p5', 'P3RX_copoly_pris', 'P3RX_hb_400', 'P3RX_hb_25', 'P3RX_hb_6', 'P3RX_hb_3',
    #          'P3RX_hb_1p5', 'P3RX_hb_pris', 'P3RX_mb_400', 'P3RX_mb_25', 'P3RX_mb_6', 'P3RX_mb_3', 'P3RX_mb_1p5',
    #          'P3RX_mb_pris', 'P3RX_hPT_400', 'P3RX_hPT_100', 'P3RX_hPT_25', 'P3RX_hPT_12', 'P3RX_hPT_6']

    # # bottom samples positions
    # x_piezo_btm = [ 55000, 52000, 42000, 30000, 18000,  2000, -7000, -17000, -29000, -41000, -50000, -49000 ]
    # y_piezo_btm = [  6000,  6000,  6000,  6000,  6000,  6000,  6000,   6000,   6000,   6000,   6000,   6000 ]
    # z_piezo_btm = [     0,     0,     0,     0,     0,     0,     0,      0,      0,      0,      0,      0 ]
    # x_hexa_btm =  [    10,     0,     0,     0,     0,     0,     0,      0,      0,      0,      0,    -10 ]

    # # top samples positions
    # x_piezo_top = [ 55000, 53000, 47000, 36000, 27000, 17000,  7000,  -4000, -17000, -28000, -39000, -52000, -53000 ]
    # y_piezo_top = [ -2600, -2600, -2600, -2600, -2600, -2600, -2600,  -2600,  -2600,  -2600,  -2600,  -2600,  -2600 ]
    # z_piezo_top = [  4000,  4000,  4000,  4000,  4000,  4000,  4000,   4000,   4000,   4000,   4000,   4000,   4000 ]
    # x_hexa_top =  [    10,     5,     0,     0,     0,     0,     0,      0,      0,      0,      0,      0,    -10 ]

    # # sample names starting from the bottom of the sample stage
    # names = ['P3RX_hPT_pris', 'P3RX_mPT_400', 'P3RX_mPT_100', 'P3RX_mPT_25', 'P3RX_mPT_12', 'P3RX_mPT_6',
    #          'P3RX_mPT_pris', 'P3RX_hPTe_400', 'P3RX_hPTe_25', 'P3RX_hPTe_6', 'P3RX_hPTe_3', 'P3RX_hPTe_1p5',
    #          'P3RX_hPTe_pris', 'P3RX_mPTe_400', 'P3RX_mPTe_25', 'P3RX_mPTe_6', 'P3RX_mPTe_3', 'P3RX_mPTe_1p5',
    #          'P3RX_mPTe_pris', 'DPP_16', 'DPP_8', 'DPP_4', 'DPP_2', 'DPP_1', 'DPP_0p75', 'DPP_0p50', 'DPP_0p25']

    # # bottom samples positions
    # x_piezo_btm = [ 55000, 54000, 44000, 34000, 25000, 17000,  9000,  -3000, -15000, -28000, -42000, -50000 ]
    # y_piezo_btm = [  6000,  6000,  6000,  6000,  6000,  6000,  6000,   6000,   6000,   6000,   6000,   6000 ]
    # z_piezo_btm = [     0,     0,     0,     0,     0,     0,     0,      0,      0,      0,      0,      0 ]
    # x_hexa_btm =  [    10,     0,     0,     0,     0,     0,     0,      0,      0,      0,      0,     -6 ]

    # # top samples positions
    # x_piezo_top = [ 54000, 54000, 43000, 35000, 23000, 15000,  7000,  -2000, -12000, -21000, -31000, -39000, -48000, -48000, -55000]
    # y_piezo_top = [ -2600, -2600, -2600, -2600, -2600, -2600, -2600,  -2600,  -2600,  -2600,  -2600,  -2600,  -2600,  -2600,  -2600]
    # z_piezo_top = [  4000,  4000,  4000,  4000,  4000,  4000,  4000,   4000,   4000,   4000,   4000,   4000,   4000,   4000,   4000]
    # x_hexa_top =  [    10,     0,     0,     0,     0,     0,     0,      0,      0,      0,      0,      0,      0,     -8,    -10]

    # # sample names starting from the bottom of the sample stage
    # names = ['DPP_0', 'PE2_1', 'PE2_2', 'PE2_3', 'PE2_4', 'PEDOT_OH_1', 'PEDOT_OH_5', 'PEDOT_OH_10', 'PEDOT_OH_10IL',
    #          'PEDOT_OE3_5', 'PEDOT_OE3_10', 'PEDOT_OE3_10IL', 'PE_16k_1', 'PE_16k_2', 'PE_16k_3', 'PE_16k_4',
    #          'PE_30k_1', 'PE_30k_2', 'PE_30k_3', 'PE_30k_4', 'PE_35p9k_1', 'PE_35p9k_2', 'PE_35p9k_3', 'PE_35p9k_4',
    #          'PE_55k_1', 'PE_55k_2', 'PE_55k_3', 'PE_55k_4', 'PE_24k_1', 'PE_24k_2']

    # # bottom samples positions
    # x_piezo_btm = [ 55000, 55000, 51000, 43000, 36000, 27000, 16000,   5000,  -5000, -14000, -23000, -32000, -42000, -51000, -55000 ]
    # y_piezo_btm = [  6000,  6000,  6000,  6000,  6000,  6000,  6000,   6000,   6000,   6000,   6000,   6000,   6000,   6000,   6000 ]
    # z_piezo_btm = [     0,     0,     0,     0,     0,     0,     0,      0,      0,      0,      0,      0,      0,      0,      0 ]
    # x_hexa_btm =  [    10,     3,     0,     0,     0,     0,     0,      0,      0,      0,      0,      0,      0,      0,     -6 ]

    # # top samples positions
    # x_piezo_top = [ 55000, 55000, 48000, 37000, 27000, 16000,  6000,  -4000, -13000, -21000, -29000, -37000, -45000, -54000, -55000]
    # y_piezo_top = [ -2600, -2600, -2600, -2600, -2600, -2600, -2600,  -2600,  -2600,  -2600,  -2600,  -2600,  -2600,  -2600,  -2600]
    # z_piezo_top = [  4000,  4000,  4000,  4000,  4000,  4000,  4000,   4000,   4000,   4000,   4000,   4000,   4000,   4000,   4000]
    # x_hexa_top =  [    10,     1,     0,     0,     0,     0,     0,      0,      0,      0,      0,      0,      0,      0,     -9]

    # # sample names starting from the bottom of the sample stage
    # names = ['PE_24k_3', 'PE_24k_4', 'PE_21k_1', 'PE_21k_2', 'PE_21k_3', 'PE_21k_4', 'PE_13k_1', 'PE_13k_2', 'PE_13k_3', 'PE_13k_4',
    #          'PE_12p8k_1', 'PE_12p8k_2', 'PE_12p8k_3', 'PE_12p8k_4', 'PE_9p4k_1', 'PE_9p4k_2', 'PE_9p4k_3', 'PE_9p4k_4',
    #          'PE_60k_1', 'PE_60k_2', 'PE_60k_3', 'PE_60k_4', 'PVA_TiO_10', 'PVA_TiO_20', 'PVA_TiO_30', 'PVA_TiO_40',
    #          'PVA_TiO_50', 'PVA_TiO_60']

    # # bottom samples positions
    # x_piezo_btm = [ 55000, 55000, 50000, 41000, 33000, 24000, 15000,   7000,      0,  -8000, -18000, -30000, -40000, -49000, -55000, -55000 ]
    # y_piezo_btm = [  6000,  6000,  6000,  6000,  6000,  6000,  6000,   6000,   6000,   6000,   6000,   6000,   6000,   6000,   6000,   6000 ]
    # z_piezo_btm = [     0,     0,     0,     0,     0,     0,     0,      0,      0,      0,      0,      0,      0,      0,      0,      0 ]
    # x_hexa_btm =  [    11,     3,     0,     0,     0,     0,     0,      0,      0,      0,      0,      0,      0,      0,     -2,    -10 ]

    # # top samples positions
    # x_piezo_top = [ 55000, 55000, 50000, 43000, 34000, 24000, 13000,  -2000, -18000, -31000, -43000, -55000]
    # y_piezo_top = [ -2600, -2600, -2600, -2600, -2600, -2600, -2600,  -2600,  -2600,  -2600,  -2600,  -2600]
    # z_piezo_top = [  4000,  4000,  4000,  4000,  4000,  4000,  4000,   4000,   4000,   4000,   4000,   4000]
    # x_hexa_top =  [    11,     4,     0,     0,     0,     0,     0,      0,      0,      0,      0,     -1]

    #    # sample names starting from the bottom of the sample stage
    #     names = ['PVA_TiO_80', 'PVA_TiO_PVA', 'E71', 'B81', 'E66', 'E72', 'B82', 'E68', 'E74', 'E51', 'E67', 'E73',
    #              'E52', 'E64', 'E75', 'E53', 'E65', 'E76', 'E54', 'B96', 'Bare_Si', 'P3HT_untreated', 'P3HT_0p5hr',
    #              'P3HT_1hr']

    #     # bottom samples positions
    #     x_piezo_btm = [ 52500, 48000, 35000, 24000, 13000,  3000, -7000, -20000, -29000, -38000, -49000, -51000]
    #     y_piezo_btm = [  6000,  6000,  6000,  6000,  6000,  6000,  5800,   5800,   5900,   5900,   6000,   6000]
    #     z_piezo_btm = [     0,     0,     0,     0,     0,     0,     0,      0,      0,      0,      0,      0]
    #     x_hexa_btm =  [    10,     0,     0,     0,     0,     0,     0,      0,      0,      0,      0,    -10]

    #     # top samples positions
    #     x_piezo_top = [ 54000, 51000, 39000, 26000, 14000,  2000, -10000, -21000, -33000, -45000, -54000, -54000]
    #     y_piezo_top = [ -3000, -2800, -2800, -2800, -2800, -2800,  -2800,  -2600,  -2600,  -2600,  -2600,  -2600]
    #     z_piezo_top = [  4000,  4000,  4000,  4000,  4000,  4000,   4000,   4000,   4000,   4000,   4000,   4000]
    #     x_hexa_top =  [    10,     0,     0,     0,     0,     0,      0,      0,      0,      0,      0,    -10]

    #    # sample names starting from the bottom of the sample stage
    #     names = ['P3HT_2hr', 'P3HT_3hr', 'DPP_16', 'DPP_8', 'DPP_4', 'DPP_2', 'DPP_1', 'DPP_0p75', 'DPP_0p50', 'DPP_0p25', 'DPP_0',
    #              'P3RX_hPT_400', 'P3RX_hPT_100', 'P3RX_hPT_25', 'P3RX_hPT_12', 'P3RX_hPT_6', 'P3RX_hPT_pris', 'P3RX_mPT_400',
    #              'P3RX_mPT_100', 'P3RX_mPT_25', 'P3RX_mPT_12', 'P3RX_mPT_6', 'P3RX_mPT_pris', 'P3RX_mPTe_400', 'P3RX_mPTe_25',
    #              'P3RX_mPTe_6', 'P3RX_mPTe_3', 'P3RX_mPTe_1p5', 'P3RX_mPTe_pris'
    #              #'P3RX_hPTe_pris', 'P3RX_mB_pris', 'P3RX_hB_pris', 'P3RX_copoly_pris',
    #              ]

    #     # bottom samples positions
    #     x_piezo_btm = [ 55000, 54000, 41000, 31000, 21000, 12000,  3000,  -3500, -12000, -20000, -29000, -39000, -50000, -52000]
    #     y_piezo_btm = [  6000,  6000,  6000,  6000,  6000,  6000,  6000,   6000,   6000,   6000,   6000,   6000,   6000,   6000]
    #     z_piezo_btm = [     0,     0,     0,     0,     0,     0,     0,      0,      0,      0,      0,      0,      0,      0]
    #     x_hexa_btm =  [    10,     0,     0,     0,     0,     0,     0,      0,      0,      0,      0,      0,      0,    -10]

    #     # top samples positions
    #     x_piezo_top = [ 54000, 53000, 42000, 30000, 20000, 12000,  4000,  -6000, -11000, -21000, -30000, -40000, -49000, -52000,  -56000]
    #     y_piezo_top = [ -2800, -2800, -2800, -2800, -2800, -2800, -2800,  -2800,  -2800,  -2800,  -2800,  -2800,  -2800,  -2600,   -2600]
    #     z_piezo_top = [  4000,  4000,  4000,  4000,  4000,  4000,  4000,   4000,   4000,   4000,   4000,   4000,   4000,   4000,    4000]
    #     x_hexa_top =  [    10,     0,     0,     0,     0,     0,     0,      0,      0,      0,      0,      0,      0,     -5,     -10]

    # sample names starting from the bottom of the sample stage
    names = [
        "P3RX_mB_pris",
        "P3RX_copoly_pris",
        "P3RX_copoly_400",
        "P3RX_hPTe_pris",
        "PE_9p4k_3",
        "PE_13k_4",
        "PE_16k_2",
        "PE_16k_3",
        "PE_24k_2",
    ]

    # bottom samples positions
    x_piezo_btm = [54000, 53000, 36000, 22000, 8000, -2000, -12000, -23000, -32000]
    y_piezo_btm = [6000, 6000, 6000, 6000, 6000, 6000, 6000, 6000, 6000]
    z_piezo_btm = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    x_hexa_btm = [10, 0, 0, 0, 0, 0, 0, 0, 0]

    # combine position lists
    x_piezo = x_piezo_btm  # + x_piezo_top
    y_piezo = y_piezo_btm  # + y_piezo_top
    z_piezo = z_piezo_btm  # + z_piezo_top
    x_hexa = x_hexa_btm  # + x_hexa_top

    assert len(x_piezo) == len(
        names
    ), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(
        y_piezo
    ), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(
        z_piezo
    ), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(z_piezo)})"
    assert len(x_piezo) == len(
        x_hexa
    ), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexa)})"

    waxs_arc = [0, 2, 20, 22]
    angle = [0.1, 0.15, 0.2]

    dets = [pil900KW, pil1M]
    det_exposure_time(t, t)

    for name, xs, zs, ys, xs_hexa in zip(names, x_piezo, z_piezo, y_piezo, x_hexa):
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, xs)
        while abs(piezo.y.position - ys) > 100:
            yield from bps.mv(piezo.y, ys)
            yield from bps.sleep(10)
        yield from bps.mv(piezo.z, zs)
        yield from bps.mv(piezo.th, 0)

        if ys < 0:
            yield from alignement_gisaxs_doblestack(angle=0.15)
        else:
            yield from bps.mv(piezo.th, 0.5)
            yield from alignement_gisaxs(angle=0.15)

        yield from bps.mv(att1_9.open_cmd, 1)
        yield from bps.sleep(1)
        yield from bps.mv(att1_9.open_cmd, 1)

        ai0 = piezo.th.position
        det_exposure_time(t, t)
        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)

            for i, an in enumerate(angle):
                yield from bps.mv(piezo.x, xs + i * 200)
                yield from bps.mv(piezo.th, ai0 + an)

                e = energy.energy.position / 1000  # in keV
                sdd = pil1m_pos.z.position / 1000  # in m

                name_fmt = "{sample}_{sdd}m_{energy}keV_ai{angl}deg_wa{waxs}"
                sample_name = name_fmt.format(
                    sample=name,
                    sdd="%.1f" % sdd,
                    energy="%.1f" % e,
                    angl="%3.2f" % an,
                    waxs="%2.1f" % wa,
                )
                sample_id(user_name="PT", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")

                yield from bp.count(dets, num=1)
            yield from bps.mv(piezo.th, ai0)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.1, 0.1)

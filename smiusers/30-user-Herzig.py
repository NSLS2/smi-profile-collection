def alignement_herzig_2020_3():
    global names, x_piezo, z_piezo, incident_angles, y_piezo_aligned, x_hexa, y_hexa

    names = ["s315h", "s324h", "s325h", "s338h", "s339v", "s339h", "313h"]
    x_piezo = [20000, 50000, 36000, 12000, -14000, -40000, -59000]
    y_piezo = [8000, -2900, -2900, -2900, -2800, -2700, -2670]
    z_piezo = [5000, -500, -500, -500, -500, -500, -500]
    x_hexa = [0, 10, 0, 0, 0, 0, -5]
    y_hexa = [6.5, 0, 0, 0, 0, 0, 0]

    incident_angles = [
        1.11119,
        -0.191966,
        0.598941,
        0.714874,
        0.404448,
        0.569336,
        0.545989,
    ]
    y_piezo_aligned = [
        7934.81,
        -3182.572,
        -3047.423,
        -2976.562,
        -2917.547,
        -2778.959,
        -2602.172,
    ]

    # incident_angles = [ 0.83422 ,  0.168648, -0.315438,  0.538535,  0.5593  ,  0.537955, 0.545215,  0.48137 ]
    # y_piezo_aligned = [ 7919.766,  8172.95 , -3172.044, -3065.634, -2925.553, -2917.084, -2781.573, -2627.836]

    # smi = SMI_Beamline()
    # yield from smi.modeAlignment(technique='gisaxs')

    # for name, xs_piezo, ys_piezo, zs_piezo, xs_hexa, ys_hexa in zip(names[1:], x_piezo[1:], y_piezo[1:], z_piezo[1:], x_hexa[1:], y_hexa[1:]):
    #     yield from bps.mv(piezo.x, xs_piezo)
    #     yield from bps.mv(piezo.y, ys_piezo)
    #     yield from bps.mv(stage.y, ys_hexa)
    #     yield from bps.mv(stage.x, xs_hexa)
    #     yield from bps.mv(piezo.z, zs_piezo)

    #     yield from alignement_gisaxs_multisample(angle = 0.1)

    #     incident_angles = incident_angles + [piezo.th.position]
    #     y_piezo_aligned = y_piezo_aligned + [piezo.y.position]

    # yield from smi.modeMeasurement()

    # print(incident_angles)
    # print(y_piezo_aligned)

    # yield from bps.mv(att1_9, 'Insert')
    # yield from bps.sleep(1)
    # yield from bps.mv(att1_9, 'Insert')
    # yield from bps.sleep(1)

    # yield from bps.mv(stage.x, 0)
    # yield from bps.mv(stage.y, 0)


def run_Herzi_short_2020_3(t=1):

    waxs_range = np.linspace(0, 13, 3)
    dets = [pil300KW, pil1M]

    for name, xs, zs, aiss, ys, xs_hexa, ys_hexa in zip(
        names, x_piezo, z_piezo, incident_angles, y_piezo_aligned, x_hexa, y_hexa
    ):
        yield from bps.mv(stage.y, ys_hexa)
        yield from bps.mv(stage.x, xs_hexa)

        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)
        yield from bps.mv(piezo.th, aiss)

        ai0 = piezo.th.position

        # yield from bps.mvr(piezo.th, angl)
        name_fmt = "{sample}_14keV_exppos1_{num}_ai{angle}deg_wa{wax}"
        if waxs.arc.position > 12:
            wa_ran = waxs_range[::-1]
        else:
            wa_ran = waxs_range

        for wa in wa_ran:
            yield from bps.mv(waxs, wa)
            sample_name = name_fmt.format(
                sample=name, num="%1.1d" % i, angle="%3.2f" % 0.11, wax="%2.1f" % wa
            )
            sample_id(user_name="EH", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=20)

        yield from bps.mv(piezo.th, ai0)
        yield from bps.mv(piezo.x, xs + 1000)

        det_exposure_time(t, t)
        angl = np.linspace(0.05, 0.20, 16)
        name_fmt = "{sample}_14keV_aiscan_ai{angle}deg_wa{wax}"

        for wa in waxs_range:
            yield from bps.mv(waxs, wa)
            for ang in angl:
                yield from bps.mv(piezo.th, ai0 + ang)
                sample_name = name_fmt.format(
                    sample=name, angle="%3.2f" % ang, wax="%2.1f" % wa
                )
                sample_id(user_name="EH", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

        sample_id(user_name="test", sample_name="test")
        det_exposure_time(0.3, 0.3)


def run_hxray_herzig(t=0.5):
    alignement_herzig_2020_3()
    yield from run_Herzi_short_2020_3(t=t)


def run_Herzi_2020_3(t=1):
    # samples = ['sample251', 'sample269', 'sample272', 'sample307h', 'sample319h']
    # x_list  = [-47000, -23000, -1000, 27000, 47000]

    samples = ["sample272", "sample307h", "sample319h"]
    x_list = [-1000, 27000, 47000]

    waxs_range = np.linspace(0, 13, 3)
    dets = [pil300KW, pil1M]

    for x, name in zip(x_list, samples):
        yield from bps.mv(piezo.x, x)

        yield from alignement_gisaxs(0.1)
        yield from bps.mv(att1_9, "Insert")
        yield from bps.sleep(1)
        yield from bps.mv(att1_9, "Insert")

        ai0 = piezo.th.position
        yield from bps.mv(piezo.th, ai0 + 0.11)

        det_exposure_time(t, t)
        yield from bps.mv(piezo.x, x + 500)

        # yield from bps.mvr(piezo.th, angl)
        name_fmt = "{sample}_14keV_exppos1_{num}_ai{angle}deg_wa{wax}"
        for i in range(0, 3, 1):
            if waxs.arc.position > 12:
                wa_ran = waxs_range[::-1]
            else:
                wa_ran = waxs_range

            for wa in wa_ran:
                yield from bps.mv(waxs, wa)
                sample_name = name_fmt.format(
                    sample=name, num="%1.1d" % i, angle="%3.2f" % 0.11, wax="%2.1f" % wa
                )
                sample_id(user_name="EH", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=20)

        yield from bps.mv(piezo.th, ai0)

        yield from bps.mv(piezo.x, x + 1000)

        det_exposure_time(t, t)
        angl = np.linspace(0.05, 0.20, 16)
        name_fmt = "{sample}_14keV_aiscan_ai{angle}deg_wa{wax}"

        for wa in waxs_range:
            yield from bps.mv(waxs, wa)
            for ang in angl:
                yield from bps.mv(piezo.th, ai0 + ang)
                sample_name = name_fmt.format(
                    sample=name, angle="%3.2f" % ang, wax="%2.1f" % wa
                )
                sample_id(user_name="EH", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

        yield from bps.mv(piezo.th, ai0 + 0.11)

        det_exposure_time(t, t)
        yield from bps.mv(piezo.x, x - 500)

        # yield from bps.mvr(piezo.th, angl)
        name_fmt = "{sample}_14keV_exppos2_{num}_ai{angle}deg_wa{wax}"
        for i in range(0, 3, 1):
            if waxs.arc.position > 12:
                wa_ran = waxs_range[::-1]
            else:
                wa_ran = waxs_range

            for wa in wa_ran:
                yield from bps.mv(waxs, wa)
                sample_name = name_fmt.format(
                    sample=name, num="%1.1d" % i, angle="%3.2f" % 0.11, wax="%2.1f" % wa
                )
                sample_id(user_name="EH", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=20)

        sample_id(user_name="test", sample_name="test")
        det_exposure_time(0.3, 0.3)


def run_Herzi_2020_2(t=1):
    # samples = ['Si1', 'P1', 'Y61', 'N41', 'PY61']
    # x_list  = [-46000, -22000, -1000, 23000,  46000]

    samples = ["HF20-181", "HF20-199", "HF20-218", "HF20-228"]
    x_list = [-45000, -19000, 8000, 33000]

    waxs_range = np.linspace(0, 19.5, 4)
    dets = [pil300KW, pil1M]

    for x, name in zip(x_list, samples):
        yield from bps.mv(piezo.x, x)

        # yield from bps.mv(GV7.open_cmd, 1 )
        # yield from bps.sleep(1)
        # yield from bps.mv(GV7.open_cmd, 1 )

        yield from alignement_gisaxs(0.1)

        # yield from bps.mv(GV7.close_cmd, 1 )
        # yield from bps.sleep(1)
        # yield from bps.mv(GV7.close_cmd, 1 )

        ai0 = piezo.th.position
        yield from bps.mv(piezo.th, ai0 + 0.18)

        det_exposure_time(t, t)
        yield from bps.mv(piezo.x, x + 500)

        # yield from bps.mvr(piezo.th, angl)
        name_fmt = "{sample}_exppos1_{num}_ai{angle}deg_wa{wax}"
        for i in range(0, 3, 1):
            if waxs.arc.position > 16:
                wa_ran = waxs_range[::-1]
            else:
                wa_ran = waxs_range

            for wa in wa_ran:
                yield from bps.mv(waxs, wa)
                sample_name = name_fmt.format(
                    sample=name, num="%1.1d" % i, angle="%3.2f" % 0.18, wax="%2.1f" % wa
                )
                sample_id(user_name="EH", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=20)

        yield from bps.mv(piezo.th, ai0)

        yield from bps.mv(piezo.x, x + 1000)

        det_exposure_time(t, t)
        angl = np.linspace(0.05, 0.19, 15)
        name_fmt = "{sample}_aiscan_ai{angle}deg_wa{wax}"

        for wa in waxs_range:
            yield from bps.mv(waxs, wa)
            for ang in angl:
                yield from bps.mv(piezo.th, ai0 + ang)
                sample_name = name_fmt.format(
                    sample=name, angle="%3.2f" % ang, wax="%2.1f" % wa
                )
                sample_id(user_name="EH", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

        yield from bps.mv(piezo.th, ai0 + 0.18)

        det_exposure_time(t, t)
        yield from bps.mv(piezo.x, x - 500)

        # yield from bps.mvr(piezo.th, angl)
        name_fmt = "{sample}_exppos2_{num}_ai{angle}deg_wa{wax}"
        for i in range(0, 3, 1):
            if waxs.arc.position > 16:
                wa_ran = waxs_range[::-1]
            else:
                wa_ran = waxs_range

            for wa in wa_ran:
                yield from bps.mv(waxs, wa)
                sample_name = name_fmt.format(
                    sample=name, num="%1.1d" % i, angle="%3.2f" % 0.18, wax="%2.1f" % wa
                )
                sample_id(user_name="EH", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=20)

        sample_id(user_name="test", sample_name="test")
        det_exposure_time(0.3, 0.3)


def nexafs_herzig(t=1):
    dets = [pil300KW]
    det_exposure_time(t, t)

    waxs_arc = [45.0]

    for name, xs, zs, aiss, ys in zip(
        names, x_piezo, z_piezo, incident_angles, y_piezo_aligned
    ):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)
        yield from bps.mv(piezo.th, aiss + 0.7)

        name_fmt = "nexafs_{sample}_{energy}eV_angle0.8deg_wa{wax}_bpm{xbpm}"

        for wa in waxs_arc:
            for e in energies:
                yield from bps.mv(energy, e)
                yield from bps.sleep(1)

                bpm = xbpm2.sumX.value

                sample_name = name_fmt.format(
                    sample=name, energy="%6.2f" % e, wax=wa, xbpm="%4.3f" % bpm
                )
                sample_id(user_name="EH", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

        yield from bps.mv(energy, 2490)
        yield from bps.mv(energy, 2470)
        yield from bps.mv(energy, 2450)


def nexafs_herzig_glass(t=1):
    dets = [pil300KW]
    det_exposure_time(t, t)

    energies = (
        np.arange(2445, 2470, 5).tolist()
        + np.arange(2470, 2480, 0.25).tolist()
        + np.arange(2480, 2490, 1).tolist()
        + np.arange(2490, 2501, 5).tolist()
    )
    waxs_arc = [45.0]

    # for name, xs, zs, aiss, ys in zip(names, x_piezo, z_piezo, incident_angles, y_piezo_aligned):
    #     yield from bps.mv(piezo.x, xs)
    #     yield from bps.mv(piezo.y, ys)
    #     yield from bps.mv(piezo.z, zs)
    #     yield from bps.mv(piezo.th, aiss + 0.7)

    name_fmt = "nexafs_glass_{energy}eV_angle0.8deg_wa{wax}_bpm{xbpm}"

    for wa in waxs_arc:
        for e in energies:
            yield from bps.mv(energy, e)
            yield from bps.sleep(1)

            bpm = xbpm2.sumX.value

            sample_name = name_fmt.format(
                energy="%6.2f" % e, wax=wa, xbpm="%4.3f" % bpm
            )
            sample_id(user_name="EH", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)

    yield from bps.mv(energy, 2490)
    yield from bps.mv(energy, 2470)
    yield from bps.mv(energy, 2450)


# [7054.818, 6891.486, 6639.453, 6471.627, 6262.9400000000005]
# [0.847336, 0.782651, 0.765316, 0.9306709999999999, 0.8608429999999999]


def run_sedge_herzig(t=0.5):
    yield from alignement_herzig()
    yield from S_edge_measurments_Herzig(t=t)


def alignement_herzig():
    global names, x_piezo, z_piezo, incident_angles, y_piezo_aligned, x_hexa, y_hexa
    # names = ['s332v', 's329v', 's324v', 's340v', 'glass']
    # names = ['s325h', 's325v', 's324h', 's338v', 's335v']
    # names = ['s315h', 's313h', 's307h', 's339h', 's339v', 's338h']
    # names = ['s318v', 's318h', 's319v', 's306v', 's306h', 's307v', 's319h', 's317h']

    names = ["s334h", "s328h", "s340h", "s335h", "s332h", "s329h", "s272", "s270"]

    x_piezo = [18000, -25000, 50000, 43000, 18000, -9000, -32000, -56000]
    y_piezo = [8000, 8000, -2670, -2670, -2670, -2670, -2670, -2670]
    z_piezo = [-1100, -1100, -1100, -1100, -1100, -1100, -1100, -1100]
    x_hexa = [0, 0, 20, 0, 0, 0, 0, 0]
    y_hexa = [6.5, 6.5, 0, 0, 0, 0, 0, 0]

    incident_angles = []
    y_piezo_aligned = []

    smi = SMI_Beamline()
    yield from smi.modeAlignment(technique="gisaxs")

    for name, xs_piezo, ys_piezo, zs_piezo, xs_hexa, ys_hexa in zip(
        names, x_piezo, y_piezo, z_piezo, x_hexa, y_hexa
    ):
        yield from bps.mv(piezo.x, xs_piezo)
        yield from bps.mv(piezo.y, ys_piezo)
        yield from bps.mv(stage.y, ys_hexa)
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.z, zs_piezo)

        yield from alignement_gisaxs_multisample(angle=0.45)

        incident_angles = incident_angles + [piezo.th.position]
        y_piezo_aligned = y_piezo_aligned + [piezo.y.position]

    yield from smi.modeMeasurement()

    print(incident_angles)
    print(y_piezo_aligned)

    yield from bps.mv(att2_9, "Insert")
    yield from bps.sleep(1)
    yield from bps.mv(att2_9, "Insert")
    yield from bps.sleep(1)

    yield from bps.mv(stage.x, 0)
    yield from bps.mv(stage.y, 0)


def S_edge_measurments_Herzig(t=1):

    waxs_arc = np.linspace(0, 19.5, 4)
    ai_list = [0.5, 0.8]

    for name, xs, zs, aiss, ys, xs_hexa, ys_hexa in zip(
        names, x_piezo, z_piezo, incident_angles, y_piezo_aligned, x_hexa, y_hexa
    ):
        yield from bps.mv(stage.y, ys_hexa)
        yield from bps.mv(stage.x, xs_hexa)

        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)
        yield from bps.mv(piezo.th, aiss)

        ai0 = piezo.th.position

        # pre position measurement to check sample inhomogeneity
        yield from bps.mv(waxs, 0)
        yield from bps.mv(energy, 2450)
        yield from bps.mv(piezo.th, ai0 + 0.8)

        dets = [pil1M, pil300KW]
        det_exposure_time(0.2, 0.2)

        xss = np.linspace(xs, xs + 1 * 4500, 26)
        xss1 = np.linspace(xs + 1 * 4500, xs + 2 * 4500, 26)
        xssss = np.concatenate([xss, xss1])
        name_fmt = "{sample}_xscan_{energy}eV_ai{ai}_pos{pos}"
        for i, xxx in enumerate(np.round(xssss, 2)):
            yield from bps.mv(piezo.x, xxx)
            bpm = xbpm2.sumX.value
            sample_name = name_fmt.format(
                sample=name, energy="%6.2f" % 2450.0, ai="%3.2f" % 0.8, pos="%2.2d" % i
            )
            sample_id(user_name="LR", sample_name=sample_name)
            yield from bp.count(dets, num=1)

        energies = [
            2450.0,
            2460.0,
            2470.0,
            2472.0,
            2474.0,
            2474.5,
            2475.0,
            2475.5,
            2476.0,
            2476.5,
            2477.0,
            2477.5,
            2478.0,
            2478.5,
            2479.0,
            2479.5,
            2480.0,
            2481.0,
            2482.0,
            2483.0,
            2484.0,
            2485.0,
            2486.0,
            2487.0,
            2490.0,
            2500.0,
        ]
        det_exposure_time(t, t)
        dets = [pil1M, pil300KW]

        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)

            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)
                yield from bps.mv(piezo.x, xs + k * 4500)

                name_fmt = "{sample}_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"

                xss = np.linspace(xs + k * 4500, xs + (1 + k) * 4500, 27)
                for e, x_ss in zip(energies, xss):
                    yield from bps.mv(piezo.x, x_ss)
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(0.7)
                    bpm = xbpm2.sumX.value
                    sample_name = name_fmt.format(
                        sample=name,
                        energy="%6.2f" % e,
                        ai="%3.2f" % ais,
                        wax=wa,
                        xbpm="%4.3f" % bpm,
                    )
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)

                yield from bps.mv(energy, 2490)
                yield from bps.mv(energy, 2470)
                yield from bps.mv(energy, 2450)

    yield from bps.mv(stage.x, 0)
    yield from bps.mv(stage.y, 0)


def run_Herzi_Sedge_2021_1(t=1):
    # samples = ['glass', '063an', '044an', '061an',  '043', '060', '008an', '030an',  '007',  '028']
    # x_piezo = [  49000,   24000,   -1000,  -28000, -55000, 49000,   24000,   -2000, -28000, -56000]
    # x_hexa =  [      0,       0,       0,       0,     -3,     0,       0,       0,      0,     -3]
    # y_piezo = [   4500,    4500,    4500,    4500,   4500, -4400,   -4400,   -4400,  -4400,  -4400]

    # samples = ['056an',   '055', '020an',   '019', '050an', '049', '024an',  '023', '063ac', '044ac']
    # x_piezo = [  49000,   26000,       0,  -32000,  -55000, 49000,   23000,      0,  -32000,  -55000]
    # x_hexa =  [      5,       0,       0,       0,       0,     4,       0,      0,       0,      0]
    # y_piezo = [   4500,    4500,    4500,    4500,    4500, -4400,   -4400,  -4400,   -4400,  -4400]

    # samples = ['061ac',  '008ac', '030ac','063oa', '044oa','061oa', '008oa','030oa', '047an',  '045']
    # x_piezo = [  48000,   28000,    1000,  -24000,  -52000, 48000,   28000,   1000,  -24000,  -52000]
    # x_hexa =  [      5,       0,       0,       0,       0,     5,       0,      0,       0,      0]
    # y_piezo = [   4500,    4500,    4500,    4500,    4500, -4400,   -4400,  -4400,   -4400,  -4400]

    # samples = ['017an',   '014',  '059an',  '058', '026an', '025', '053an',  '052', '056ac',  '056oa']
    # x_piezo = [  49000,   24000,   -1500,  -27000,  -54000, 48000,   24000,  -1500,  -27000,  -54000]
    # x_hexa =  [      3,       0,       0,       0,       0,     3,       0,      0,       0,      0]
    # y_piezo = [   4500,    4500,    4500,    4500,    4500, -4400,   -4400,  -4400,   -4400,  -4400]

    samples = [
        "020ac",
        "020oa",
        "050ac",
        "050oa",
        "024ac",
        "024oa",
        "010an",
        "009",
        "048an",
        "057an",
    ]
    x_piezo = [49000, 27000, 0, -27000, -54000, 49000, 27000, 0, -27000, -54000]
    x_hexa = [5, 0, 0, 0, 0, 5, 0, 0, 0, 0]
    y_piezo = [4500, 4500, 4500, 4500, 4500, -4400, -4400, -4400, -4400, -4400]

    assert len(x_piezo) == len(
        samples
    ), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(samples)})"
    assert len(x_piezo) == len(
        y_piezo
    ), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(
        x_hexa
    ), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexa)})"

    dets = [pil300KW, pil1M]
    waxs_arc = np.linspace(0, 19.5, 4)
    ai_list = [0.5, 0.8]

    for w, (xs, y, x_hexa, name) in enumerate(zip(x_piezo, y_piezo, x_hexa, samples)):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, y)
        yield from bps.mv(stage.x, x_hexa)

        yield from alignement_gisaxs(0.45)
        yield from bps.mv(att2_9.open_cmd, 1)
        yield from bps.sleep(1)
        yield from bps.mv(att2_9.open_cmd, 1)

        ai0 = piezo.th.position

        # pre position measurement to check sample inhomogeneity
        yield from bps.mv(waxs, 0)
        yield from bps.mv(energy, 2450)

        dets = [pil1M, pil300KW]
        det_exposure_time(0.2, 0.2)
        name_fmt = "{sample}_xscan_{energy}eV_ai{ai}_pos{pos}"

        xss = np.linspace(xs, xs + 1 * 4500, 26)
        yield from bps.mv(piezo.th, ai0 + 0.5)

        for i, xxx in enumerate(np.round(xss, 2)):
            yield from bps.mv(piezo.x, xxx)
            bpm = xbpm2.sumX.value
            sample_name = name_fmt.format(
                sample=name, energy="%6.2f" % 2450.0, ai="%3.2f" % 0.5, pos="%2.2d" % i
            )
            sample_id(user_name="LR", sample_name=sample_name)
            yield from bp.count(dets, num=1)

        xss1 = np.linspace(xs + 1 * 4500, xs + 2 * 4500, 26)
        yield from bps.mv(piezo.th, ai0 + 0.8)

        for i, xxx in enumerate(np.round(xss1, 2)):
            yield from bps.mv(piezo.x, xxx)
            bpm = xbpm2.sumX.value
            sample_name = name_fmt.format(
                sample=name, energy="%6.2f" % 2450.0, ai="%3.2f" % 0.8, pos="%2.2d" % i
            )
            sample_id(user_name="LR", sample_name=sample_name)
            yield from bp.count(dets, num=1)

        energies = [
            2450.0,
            2460.0,
            2470.0,
            2472.0,
            2474.0,
            2474.5,
            2475.0,
            2475.5,
            2476.0,
            2476.5,
            2477.0,
            2477.5,
            2478.0,
            2478.5,
            2479.0,
            2479.5,
            2480.0,
            2481.0,
            2482.0,
            2483.0,
            2484.0,
            2485.0,
            2486.0,
            2487.0,
            2490.0,
            2500.0,
        ]
        det_exposure_time(t, t)
        dets = [pil1M, pil300KW]

        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)

            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)
                yield from bps.mv(piezo.x, xs + k * 4500)

                name_fmt = "{sample}_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"

                xss = np.linspace(xs + k * 4500, xs + (1 + k) * 4500, 27)
                for e, x_ss in zip(energies, xss):
                    yield from bps.mv(energy, e)
                    # yield from bps.sleep(0.4)
                    yield from bps.mv(piezo.x, x_ss)

                    bpm = xbpm2.sumX.value
                    sample_name = name_fmt.format(
                        sample=name,
                        energy="%6.2f" % e,
                        ai="%3.2f" % ais,
                        wax=wa,
                        xbpm="%4.3f" % bpm,
                    )
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)

                yield from bps.mv(energy, 2490)
                yield from bps.sleep(1)
                yield from bps.mv(energy, 2470)
                yield from bps.sleep(1)
                yield from bps.mv(energy, 2450)

        yield from bps.mv(piezo.th, ai0)

    yield from bps.mv(stage.x, 0)


def run_Herzi_2021_1(t=1):

    # samples = ['glass', '063an', '044an', '061an',  '043', '060', '008an', '030an',  '007',  '028']
    # x_piezo = [  55000,   37000,   10000,  -17000, -47000, 55000,   38000,   13000, -15000, -43000]
    # x_hexa =  [      7,       0,       0,       0,      0,     7,       0,       0,      0,      0]
    # y_piezo = [   4500,    4500,    4500,    4500,   4500, -4400,   -4400,   -4400,  -4400,  -4400]

    samples = ["056an", "055", "020an", "019", "050an", "049", "024an", "023"]
    x_piezo = [55000, 34000, 6000, -24000, -50000, 6000, -24000, -50000]
    x_hexa = [7, 0, 0, 0, 0, 7, 0, 0]
    y_piezo = [4500, 4500, 4500, 4500, 4500, -4400, -4400, -4400]

    assert len(x_piezo) == len(
        samples
    ), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(samples)})"
    assert len(x_piezo) == len(
        y_piezo
    ), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(
        x_hexa
    ), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexa)})"

    waxs_range = np.linspace(0, 13, 3)
    dets = [pil300KW, pil1M]

    for x, y, x_hexa, name in zip(x_piezo, y_piezo, x_hexa, samples):
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(piezo.y, y)
        yield from bps.mv(stage.x, x_hexa)

        yield from alignement_gisaxs(0.1)

        ai0 = piezo.th.position
        yield from bps.mv(piezo.th, ai0 + 0.14)

        det_exposure_time(t, t)

        if waxs.arc.position > 12:
            wa_ran = waxs_range[::-1]
        else:
            wa_ran = waxs_range

        name_fmt = "{sample}_14keV_exp_{pos}_ai{angle}deg_wa{wax}"

        for wa in wa_ran:
            yield from bps.mv(waxs, wa)

            yield from bps.mv(piezo.x, x + 500)
            sample_name = name_fmt.format(
                sample=name, pos="pos1", angle="%3.2f" % 0.14, wax="%2.1f" % wa
            )
            sample_id(user_name="EH", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=20)

            yield from bps.mv(piezo.x, x - 500)
            sample_name = name_fmt.format(
                sample=name, pos="pos2", angle="%3.2f" % 0.14, wax="%2.1f" % wa
            )
            sample_id(user_name="EH", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=20)

            yield from bps.mv(piezo.x, x - 1000)
            sample_name = name_fmt.format(
                sample=name, pos="pos3", angle="%3.2f" % 0.14, wax="%2.1f" % wa
            )
            sample_id(user_name="EH", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=20)

        yield from bps.mv(piezo.th, ai0)
        yield from bps.mv(piezo.x, x)

        det_exposure_time(t, t)
        angl = np.linspace(0.05, 0.20, 16)
        name_fmt = "{sample}_14keV_aiscan_ai{angle}deg_wa{wax}"

        for wa in waxs_range:
            yield from bps.mv(waxs, wa)
            for ang in angl:
                yield from bps.mv(piezo.th, ai0 + ang)
                sample_name = name_fmt.format(
                    sample=name, angle="%3.2f" % ang, wax="%2.1f" % wa
                )
                sample_id(user_name="EH", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

        sample_id(user_name="test", sample_name="test")
        det_exposure_time(0.3, 0.3)


def run_test_Herzi_2021_1(t=1):

    # samples = ['glass', '063an', '044an', '061an',  '043', '060', '008an', '030an',  '007',  '028']
    # x_piezo = [  55000,   37000,   10000,  -17000, -47000, 55000,   38000,   13000, -15000, -43000]
    # x_hexa =  [      7,       0,       0,       0,      0,     7,       0,       0,      0,      0]
    # y_piezo = [   4500,    4500,    4500,    4500,   4500, -4400,   -4400,   -4400,  -4400,  -4400]

    samples = ["mono1", "mono2", "mono3", "mono4"]
    x_piezo = [55000, 50500, 38500, 27500]
    x_hexa = [7.5, 0, 0, 0]
    y_piezo = [-4400, -4400, -4400, -4400]

    assert len(x_piezo) == len(
        samples
    ), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(samples)})"
    assert len(x_piezo) == len(
        y_piezo
    ), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(
        x_hexa
    ), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexa)})"

    waxs_range = np.linspace(0, 13, 3)
    dets = [pil300KW, pil1M]

    for x, y, x_hexa, name in zip(x_piezo, y_piezo, x_hexa, samples):
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(piezo.y, y)
        yield from bps.mv(stage.x, x_hexa)

        yield from alignement_gisaxs(0.1)

        ai0 = piezo.th.position
        yield from bps.mv(piezo.th, ai0 + 0.14)

        det_exposure_time(t, t)

        if waxs.arc.position > 12:
            wa_ran = waxs_range[::-1]
        else:
            wa_ran = waxs_range

        name_fmt = "{sample}_14keV_exp_{pos}_ai{angle}deg_wa{wax}"

        for wa in wa_ran:
            yield from bps.mv(waxs, wa)

            yield from bps.mv(piezo.x, x + 1500)
            sample_name = name_fmt.format(
                sample=name, pos="pos1", angle="%3.2f" % 0.14, wax="%2.1f" % wa
            )
            sample_id(user_name="EH", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=20)

            yield from bps.mv(piezo.x, x + 1250)
            sample_name = name_fmt.format(
                sample=name, pos="pos2", angle="%3.2f" % 0.14, wax="%2.1f" % wa
            )
            sample_id(user_name="EH", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=20)

            yield from bps.mv(piezo.x, x + 1000)
            sample_name = name_fmt.format(
                sample=name, pos="pos3", angle="%3.2f" % 0.14, wax="%2.1f" % wa
            )
            sample_id(user_name="EH", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=20)

            yield from bps.mv(piezo.x, x + 750)
            sample_name = name_fmt.format(
                sample=name, pos="pos4", angle="%3.2f" % 0.14, wax="%2.1f" % wa
            )
            sample_id(user_name="EH", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=20)

            yield from bps.mv(piezo.x, x + 500)
            sample_name = name_fmt.format(
                sample=name, pos="pos5", angle="%3.2f" % 0.14, wax="%2.1f" % wa
            )
            sample_id(user_name="EH", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=20)

            yield from bps.mv(piezo.x, x + 250)
            sample_name = name_fmt.format(
                sample=name, pos="pos6", angle="%3.2f" % 0.14, wax="%2.1f" % wa
            )
            sample_id(user_name="EH", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=20)

        yield from bps.mv(piezo.th, ai0)
        yield from bps.mv(piezo.x, x)

        det_exposure_time(t, t)
        angl = np.linspace(0.05, 0.20, 16)
        name_fmt = "{sample}_14keV_aiscan_ai{angle}deg_wa{wax}"

        for wa in waxs_range:
            yield from bps.mv(waxs, wa)
            for ang in angl:
                yield from bps.mv(piezo.th, ai0 + ang)
                sample_name = name_fmt.format(
                    sample=name, angle="%3.2f" % ang, wax="%2.1f" % wa
                )
                sample_id(user_name="EH", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

        sample_id(user_name="test", sample_name="test")
        det_exposure_time(0.3, 0.3)

        yield from bps.mv(piezo.th, ai0 + 0.30)

        if waxs.arc.position > 12:
            wa_ran = waxs_range[::-1]
        else:
            wa_ran = waxs_range

        name_fmt = "{sample}_14keV_exp_{pos}_ai{angle}deg_wa{wax}"

        for wa in wa_ran:
            yield from bps.mv(waxs, wa)

            yield from bps.mv(piezo.x, x - 250)
            sample_name = name_fmt.format(
                sample=name, pos="pos1", angle="%3.2f" % 0.30, wax="%2.1f" % wa
            )
            sample_id(user_name="EH", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=20)

            yield from bps.mv(piezo.x, x - 500)
            sample_name = name_fmt.format(
                sample=name, pos="pos2", angle="%3.2f" % 0.30, wax="%2.1f" % wa
            )
            sample_id(user_name="EH", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=20)

            yield from bps.mv(piezo.x, x - 750)
            sample_name = name_fmt.format(
                sample=name, pos="pos3", angle="%3.2f" % 0.30, wax="%2.1f" % wa
            )
            sample_id(user_name="EH", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=20)

            yield from bps.mv(piezo.x, x - 1000)
            sample_name = name_fmt.format(
                sample=name, pos="pos4", angle="%3.2f" % 0.30, wax="%2.1f" % wa
            )
            sample_id(user_name="EH", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=20)

            yield from bps.mv(piezo.x, x - 1250)
            sample_name = name_fmt.format(
                sample=name, pos="pos5", angle="%3.2f" % 0.30, wax="%2.1f" % wa
            )
            sample_id(user_name="EH", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=20)

            yield from bps.mv(piezo.x, x - 1500)
            sample_name = name_fmt.format(
                sample=name, pos="pos6", angle="%3.2f" % 0.30, wax="%2.1f" % wa
            )
            sample_id(user_name="EH", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=20)


def nigh_test():
    yield from run_test_Herzi_2021_1(t=0.5)
    yield from run_Herzi_2021_1(t=0.5)

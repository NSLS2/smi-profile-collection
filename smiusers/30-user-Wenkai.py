def giwaxs_S_edge_wenkai(t=1):
    dets = [pil300KW]

    names = ["A2", "A3", "A4", "A5", "A6"]
    x = [30000, 16000, 0, -15000, -36000]

    energies = (
        np.arange(2450, 2470, 5).tolist()
        + np.arange(2470, 2480, 0.25).tolist()
        + np.arange(2480, 2490, 1).tolist()
        + np.arange(2490, 2501, 5).tolist()
    )
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


def nexafs_S_edge_wenkai(t=1):
    dets = [pil300KW]
    names = ["PFSA_LSC"]
    x = [41200]
    y = [-8000]
    z = [2700]

    energies = np.linspace(2450, 2500, 51)

    energies = (
        np.arange(2450, 2470, 5).tolist()
        + np.arange(2470, 2480, 0.25).tolist()
        + np.arange(2480, 2490, 1).tolist()
        + np.arange(2490, 2501, 5).tolist()
    )
    energies1 = 10 + np.asarray(
        np.arange(2445, 2470, 5).tolist()
        + np.arange(2470, 2480, 0.25).tolist()
        + np.arange(2480, 2490, 1).tolist()
        + np.arange(2490, 2501, 5).tolist()
    )

    for name, xs in zip(names, x):

        det_exposure_time(t, t)
        name_fmt = "nexafs_{sample}_{energy}eV_wa52.00_bpm{xbpm}"
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

        yield from bps.mv(energy, 2470)
        yield from bps.mv(energy, 2450)


def hardxray_wenkai2020_1(t=1):
    dets = [pil300KW, pil1M]

    names = [
        "PFSA_LSC",
        "PFSA_LSC",
        "N2200_vert",
        "N2200_hori",
        "A1",
        "A2",
        "B1",
        "B2",
        "C1",
        "C2",
        "D1",
        "D2",
        "A3",
        "B3",
        "C3",
        "D3",
    ]
    x = [
        41000,
        29000,
        -8000,
        -30000,
        43800,
        37500,
        32500,
        27500,
        22500,
        17100,
        12100,
        5900,
        -16900,
        -21900,
        -27300,
        -32500,
    ]
    y = [
        -8000,
        -8000,
        -8000,
        -8000,
        3800,
        4000,
        4000,
        4000,
        4000,
        4000,
        4000,
        4000,
        4000,
        4000,
        4000,
        4200,
    ]
    z = [
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
        2700,
        2700,
    ]

    waxs_arc = np.linspace(0, 39, 7)

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)

        for name, xs, ys, zs in zip(names, x, y, z):
            yield from bps.mv(piezo.x, xs)
            yield from bps.mv(piezo.y, ys)
            yield from bps.mv(piezo.z, zs)

            det_exposure_time(t, t)
            name_fmt = "{sample}_16.1keVeV_8.3m_wa{wax}"

            yield from bps.sleep(1)

            sample_name = name_fmt.format(sample=name, wax=wa)
            sample_id(user_name="WZ", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)


def waxs_S_edge_wenkai_2021_1(t=1):

    dets = [pil1M, pil300KW]

    # names = ['PFSA_LSC', 'PFSA_SSC', 'A1', 'A2', 'B1', 'B2', 'C1', 'C2', 'D1', 'D2', 'A3', 'B3', 'C3', 'D3']
    # x = [41000, 28000,  43300, 37600, 32700, 27500, 21700, 16600, 11300, 5900, -17600, -22600, -28100, -33100]
    # y = [-8500, -8500,   3800,  4000,  3900,  4200,  4100,  4100,  3800, 3900,   3900,   4100,   4100,   4200]
    # z = [ 2700,  2700,   2700,  2700,  2700,  2700,  2700,  2700,  2700, 2700,   2700,   2700,   2700,   2700]

    energies = (
        np.arange(2450, 2470, 5).tolist()
        + np.arange(2470, 2480, 0.25).tolist()
        + np.arange(2480, 2490, 1).tolist()
        + np.arange(2490, 2501, 5).tolist()
    )
    # energies1 = 10 + np.asarray(np.arange(2445, 2470, 5).tolist() + np.arange(2470, 2480, 0.25).tolist() + np.arange(2480, 2490, 1).tolist()+ np.arange(2490, 2501, 5).tolist())
    # waxs_arc = np.linspace(13, 19.5, 2)

    # for k, wa in enumerate(waxs_arc):
    #     yield from bps.mv(waxs, wa)

    #     for name, xs, ys, zs in zip(names, x, y, z):
    #         yield from bps.mv(piezo.x, xs)
    #         yield from bps.mv(piezo.y, ys)
    #         yield from bps.mv(piezo.z, zs)

    #         yss = np.linspace(ys, ys + 700, 29)
    #         xss = np.array([xs, xs + 500])

    #         yss, xss = np.meshgrid(yss, xss)
    #         yss = yss.ravel()
    #         xss = xss.ravel()

    #         det_exposure_time(t,t)
    #         name_fmt = '{sample}_{energy}eV_wa{wax}_bpm{xbpm}'
    #         for e, xsss, ysss in zip(energies1, xss, yss):
    #             yield from bps.mv(energy, e)
    #             yield from bps.sleep(1)

    #             yield from bps.mv(piezo.y, ysss)
    #             yield from bps.mv(piezo.x, xsss)

    #             bpm = xbpm2.sumX.value

    #             sample_name = name_fmt.format(sample=name, energy='%6.2f'%e, wax = wa, xbpm = '%4.3f'%bpm)
    #             sample_id(user_name='WZ', sample_name=sample_name)
    #             print(f'\n\t=== Sample: {sample_name} ===\n')
    #             yield from bp.count(dets, num=1)

    #         yield from bps.mv(energy, 2470)
    #         yield from bps.mv(energy, 2450)

    names = ["N2200_vert", "N2200_hori"]
    x = [-8500, -30500]
    y = [-8500, -8000]
    z = [2700, 2700]

    waxs_arc = np.linspace(0, 19.5, 4)

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)
        for name, xs, ys, zs in zip(names, x, y, z):
            yield from bps.mv(piezo.x, xs)
            yield from bps.mv(piezo.y, ys)
            yield from bps.mv(piezo.z, zs)

            yss = np.linspace(ys, ys + 1000, 29)
            xss = np.array([xs, xs + 500])

            yss, xss = np.meshgrid(yss, xss)
            yss = yss.ravel()
            xss = xss.ravel()
            det_exposure_time(t, t)
            name_fmt = "{sample}_{energy}eV_wa{wax}_bpm{xbpm}"
            for e, xsss, ysss in zip(energies, xss, yss):
                yield from bps.mv(energy, e)
                yield from bps.sleep(1)

                yield from bps.mv(piezo.y, ysss)
                yield from bps.mv(piezo.x, xsss)

                bpm = xbpm2.sumX.value

                sample_name = name_fmt.format(
                    sample=name, energy="%6.2f" % e, wax=wa, xbpm="%4.3f" % bpm
                )
                sample_id(user_name="WZ", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 2470)
            yield from bps.mv(energy, 2450)


def wenkai_waxs_tensile_tender_2021_2(t=1):
    # 85s to do the loop
    dets = [pil300KW, pil1M]

    names = "SSC_loop4_waxs"
    t0 = time.time()
    # yield from bps.mvr(stage.y, -0.4)

    for i in range(60):
        det_exposure_time(t, t)
        yield from bps.mvr(stage.y, 0.03)

        if waxs.arc.position > 5:
            wa = [19.5, 13, 6.5, 0]
        else:
            wa = [0, 6.5, 13, 19.5]

        t1 = time.time()
        for wax in wa:
            name_fmt = "{sample}_2455.0eV_sdd3m_{time}s_{i}_wa{wa}"

            yield from bps.mv(waxs, wax)
            sample_name = name_fmt.format(
                sample=names, time="%1.1f" % (t1 - t0), i="%3.3d" % i, wa="%1.1f" % wax
            )
            sample_id(user_name="GF", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)

        yield from bps.sleep(5)

    t2 = time.time()
    print(t2 - t0)


def wenkai_waxsonly_tensile_tender_2021_2(t=1):
    # 85s to do the loop
    dets = [pil300KW]

    names = "LSC_loop5_waxs_kaclamp"
    t0 = time.time()
    # yield from bps.mvr(stage.y, -0.4)

    for i in range(1000):
        det_exposure_time(t, t)
        yield from bps.mvr(stage.y, 0.01)

        t1 = time.time()
        name_fmt = "{sample}_2484.25eV_sdd3m_{time}s_{i}_wa{wa}"

        sample_name = name_fmt.format(
            sample=names, time="%1.1f" % (t1 - t0), i="%3.3d" % i, wa="%1.1f" % 0
        )
        sample_id(user_name="GF", sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")
        yield from bp.count(dets, num=1)

    t2 = time.time()
    print(t2 - t0)


def wenkai_saxsonly_tensile_tender_2021_2(t=1):
    # 85s to do the loop
    dets = [pil300KW, pil1M]

    names = "SSC_loop3_saxs"
    t0 = time.time()
    # yield from bps.mvr(stage.y, -0.4)

    for i in range(1000):
        det_exposure_time(t, t)
        yield from bps.mvr(stage.y, 0.005)

        t1 = time.time()
        name_fmt = "{sample}_2484.24eV_sdd3m_{time}s_{i}_wa{wa}"

        sample_name = name_fmt.format(
            sample=names, time="%1.1f" % (t1 - t0), i="%3.3d" % i, wa="%1.1f" % 8
        )
        sample_id(user_name="GF", sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")
        yield from bp.count(dets, num=1)

        yield from bps.sleep(0.5)

    t2 = time.time()
    print(t2 - t0)


def wenkai_saxs_waxs_tensile_hard(t=1):
    dets = [pil300KW, pil1M]

    names = "PF-T2PO1_loop1"
    t0 = time.time()
    for i in range(2000):
        det_exposure_time(t, t)

        if waxs.arc.position > 5:
            wa = [13, 6.5, 0]
        else:
            wa = [0, 6.5, 13]

        name_fmt = "{sample}_14000eV_{time}s_{i}_wa{wa}"
        t1 = time.time()
        for wax in wa:
            yield from bps.mv(waxs, wax)
            sample_name = name_fmt.format(
                sample=names, time="%1.1f" % (t1 - t0), i="%3.3d" % i, wa="%1.1f" % wax
            )
            sample_id(user_name="GF", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)


def wenkai_waxs_tensile_2021_3(t=0.5):
    names = "LSC_RT_loop1"

    dets = [pil900KW, pil300KW]
    wa = [0]
    yield from bps.mv(stage.y, 0.1)
    t0 = time.time()
    for i in range(2000):
        det_exposure_time(t, t)

        name_fmt = "{sample}_14keV_{time}s_{i}_wa{wa}"
        t1 = time.time()
        for wax in wa:
            yield from bps.mv(waxs, wax)
            sample_name = name_fmt.format(
                sample=names, time="%1.1f" % (t1 - t0), i="%3.3d" % i, wa="%1.1f" % wax
            )
            sample_id(user_name="GF", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)
            yield from bps.mvr(stage.y, 0.01)
            # yield from bps.sleep(2)


def wenkai_saxs_tensile_2021_3(t=0.5):
    names = "LSC_RT_loop6_samesample"

    dets = [pil1M]
    wa = [20]
    yield from bps.mv(stage.y, -0.3)
    t0 = time.time()
    for i in range(2000):
        det_exposure_time(t, t)

        name_fmt = "{sample}_2484.24keV_{time}s_{i}_wa{wa}"
        t1 = time.time()
        for wax in wa:
            yield from bps.mv(waxs, wax)
            sample_name = name_fmt.format(
                sample=names, time="%1.1f" % (t1 - t0), i="%3.3d" % i, wa="%1.1f" % wax
            )
            sample_id(user_name="GF", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)
            yield from bps.mvr(stage.y, 0.01)
            # yield from bps.sleep(2)




def S_edge_measurments_2022_3(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    # names = [    'A1',   'A2',   'A3',   'A4',  'A5',  'A6',  'B1',  'B2',  'B3',  
    #              'B4',   'B5',   'B6',   'C1',  'C2',  'C3',  'C4',  'C5', 'C6']
    # x_piezo = [-49000, -47000, -33000, -20000, -9000,  9000, 23000, 40000, 45000, 
    #            -54000, -51000, -37000, -23000, -4000, 10000, 25000, 40000, 47000]
    # x_hexap = [   -10,      0,      0,      0,     0,     0,     0,     0,    10,
    #               -10,      0,      0,      0,     0,     0,     0,     0,    10]
    # y_piezo = [  4000,   4000,   4000,   4000,  4000,  4000,  4000,  4000,  4000, 
    #             -5000,  -5000,  -5000,  -5000, -5000, -5000, -5000, -5000, -5000,]

    # names = [    'A2',   'A3',   'A4',   'A5',  'A6',  'B1',  'B2',  'B3',  
    #              'B4',   'B5',   'B6',   'C1',  'C2',  'C3',  'C4',  'C5',  'C6']
    # x_piezo = [-47000, -33000, -20000,  -9000,  9000, 23000, 40000, 45000, 
    #            -54000, -51000, -37000, -23000, -4000, 10000, 25000, 40000, 47000]
    # x_hexap = [     0,      0,      0,      0,     0,     0,     0,    10,
    #               -10,      0,      0,      0,     0,     0,     0,     0,    10]
    # y_piezo = [  4000,   4000,   4000,   4000,  4000,  4000,  4000,  4000, 
    #             -5000,  -5000,  -5000,  -5000, -5000, -5000, -5000, -5000, -5000]


    names = [   'C4_redo',  'C5',  'C6']
    x_piezo = [23000, 38000, 47000]
    x_hexap = [    0,     0,    10]
    y_piezo = [-5000, -5000, -5000]

    names = [      'C6']
    x_piezo = [  52000]
    x_hexap = [         10]
    y_piezo = [ -5000]

    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(x_hexap), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexap)})"

    energies = np.arange(2450, 2470, 5).tolist()+ np.arange(2470, 2480, 0.25).tolist()+ np.arange(2480, 2490, 1).tolist()+ np.arange(2490, 2521, 5).tolist()
    waxs_arc = [0, 20, 40]
    ai0 = 1.5
    ai_list = [0.80]

    for name, xs, ys, xs_hexap in zip(names, x_piezo, y_piezo, x_hexap):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(stage.x, xs_hexap)

        yield from bps.mv(piezo.th, ai0)
        yield from alignement_gisaxs_doblestack(0.4)

        ai0 = piezo.th.position
        det_exposure_time(t, t)

        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)
            # Do not take SAXS when WAXS detector in the way
            dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]

            yield from bps.mv(piezo.x, xs)
            counter = 0

            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                name_fmt = "{sample}_pos1_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs + counter * 50)
                    counter += 1

                    bpm = xbpm3.sumX.get()
                    sample_name = name_fmt.format(sample=name, energy="%6.2f" % e,ai="%3.2f" % ais, wax=wa,xbpm="%4.3f" % bpm)
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)

                yield from bps.mv(energy, 2490)
                yield from bps.sleep(3)
                yield from bps.mv(energy, 2470)
                yield from bps.sleep(3)
                yield from bps.mv(energy, 2450)
                yield from bps.sleep(3)

            yield from bps.mv(piezo.th, ai0)




def waxs_S_edge_wenkai_2022_3(t=1):
    dets = [pil900KW, pil1M]

    names = [   'A1',  'A2',  'A3',  'A4',  'A5',  'A6',  'A7',  'A8',  'B1',  'B2',  'B3',  'B4',  'B5',  'B6',  'B7',  'B8',
                'C1',  'C2',  'C3',  'C4',  'C5',  'C6',  'C7',  'C8',  'F1',  'F2',  'F3',  'F4',  'F5',  'F6',  'F7',  'F8']
    x_piezo = [41500, 35500, 30500, 21500, 16000, 11000,  5500,     0, -5000,-10000,-15500,-20800,-25800,-30900,-37300,-42000,
               44500, 39000, 33000, 28000, 23000, 17000, 11500,  5500, -5200,-10200,-15500,-21500,-26000,-31000,-36500,-41700]
    y_piezo = [-8200, -8500, -8300, -8700, -8800, -8500, -8200, -8500, -8600, -8600, -8500, -8800, -8200, -8400, -8200, -8500,
                4000,  4000,  4300,  4300,  4300,  4500,  4600,  4600,  4600,  5100,  4900,  4300,  4600,  4900,  5000,  4900]

    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"

    energies = np.arange(2450, 2470, 5).tolist()+ np.arange(2470, 2480, 0.25).tolist()+ np.arange(2480, 2490, 1).tolist()+ np.arange(2490, 2521, 5).tolist()
    waxs_arc = [0, 20, 40]

    for name, xs, ys in zip(names, x_piezo, y_piezo):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)

        yss = np.linspace(ys, ys + 1000, 61)
        xss = np.array([xs])

        yss, xss = np.meshgrid(yss, xss)
        yss = yss.ravel()
        xss = xss.ravel()

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)

            if wa == 0:
                dets = [pil900KW]
            else:
                dets = [pil900KW, pil1M]

            det_exposure_time(t, t)

            name_fmt = "{sample}_sdd{sdd}_{energy}eV_wa{wax}_bpm{xbpm}"
            for e, xsss, ysss in zip(energies, xss, yss):
                yield from bps.mv(energy, e)
                yield from bps.sleep(2)
                if xbpm2.sumX.get() < 50:
                    yield from bps.sleep(2)
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)

                yield from bps.mv(piezo.y, ysss)
                yield from bps.mv(piezo.x, xsss)

                bpm = xbpm2.sumX.value

                sdd = pil1m_pos.z.position / 1000
                sample_name = name_fmt.format(sample=name, sdd="%.1f"%sdd, energy="%6.2f"%e, wax=wa, xbpm="%4.3f"%bpm)

                sample_id(user_name="GF", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")

                yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 2490)
            yield from bps.sleep(3)
            yield from bps.mv(energy, 2470)
            yield from bps.sleep(3)
            yield from bps.mv(energy, 2450)
            yield from bps.sleep(3)





def hardxray_wenkai_2022_3(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    # names = [ 'ZM_01', 'ZM_02', 'ZM_03', 'ZM_04', 'ZM_05', 'ZM_06', 'ZM_07', 'ZM_08', 
    #           'ZM_09', 'ZM_10', 'ZM_11','XSJ_01','XSJ_02','XSJ_03','XSJ_04',]
    # x_piezo = [-52000,  -45000,  -30000,  -15000,    5000,   25000,   45000,   50000,
    #            -57000,  -50000,  -33000,       0,   18000,   30000,   46000]
    # x_hexap = [   -10,       0,       0,       0,       0,       0,       0,      10,  
    #               -10,       0,       0,       0,       0,       0,       0]
    # y_piezo = [  4400,    4400,    4400,    4400,    4400,    4400,    4400,    4400,    
    #             -4800,   -4800,   -4800,   -4800,   -4800,   -4800,   -4800]

    # names = [ 'ZM_12', 'XSJ_05', 'XSJ_06', 'ZWK_01', 'ZWK_02', 'ZWK_03', 'ZWK_04', 'ZWK_05', 
    #          'ZWK_06', 'ZWK_07', 'ZWK_08', 'ZWK_09', 'ZWK_10', 'ZWK_11', 'ZWK_12',  'ZL_01',  'ZL_02']
    # x_piezo = [-52000,   -43000,   -28000,   -13000,     4000,    20000,    37000,    52000,
    #            -52000,   -47000,   -28000,   -13000,     4000,    20000,    32000,    52000,    55000]
    # x_hexap = [   -10,        0,        0,        0,        0,        0,        0,        0,  
    #               -10,        0,        0,        0,        0,        0,        0,        0,       10]
    # y_piezo = [  4400,     4400,     4400,     4400,     4400,     4400,     4400,     4400,
    #             -4800,    -4800,    -4800,    -4800,    -4800,    -4800,    -4800,    -4800,    -4800]

    # names = ['ZWK_05_redo','ZWK_06_redo','ZL_03','ZL_04','ZL_05','ZL_06', 'ZL_07',  'ZL_08',  'ZL_09', 
    #           'ZL_10',  'ZL_11',  'ZL_12',  'ZL_13',  'ZL_14',  'ZL_15', 'HTY_01', 'HTY_02', 'HTY_03',  'HTY_04']
    # x_piezo = [-50000,   -43000,   -28000,   -15000,        0,    14000,    28000,    42000,    46000,
    #            -55000,   -52000,   -38000,   -23000,   -11000,     5000,    20000,    36000,    52000,     56000]
    # x_hexap = [   -10,        0,        0,        0,        0,        0,        0,        0,       10, 
    #               -10,        0,        0,        0,        0,        0,        0,        0,        0,        10]
    # y_piezo = [  4400,     4400,     4400,     4400,     4400,     4400,     4400,     4400,     4200,
    #             -4800,    -4800,    -4800,    -4800,    -4800,    -4800,    -4800,    -4800,    -4800,     -4800]


    # names = ['ZL_09_redo','HTY_05','HTY_06','LXA_01','LXA_02', 'LXA_03', 'LM_01',   'LM_02',  'LM_03', 
    #           'LM_04',  'LM_05',  'LM_06',  'LM_07',  'LM_08',  'LM_09', 'LM_10',   'LM_11']
    # x_piezo = [-50000,   -44000,   -29000,   -14000,     1000,    19000,    34000,    40000,    52000,
    #            -50000,   -43000,   -29000,   -12000,     6000,    19000,    36000,    42000]
    # x_hexap = [   -10,        0,        0,        0,        0,        0,        0,       10,       10, 
    #               -10,        0,        0,        0,        0,        0,        0,       10]
    # y_piezo = [  4400,     4400,     4300,     4200,     4200,     4100,     4100,     4000,     4000,
    #             -4800,    -4800,    -4800,    -4800,    -4800,    -4800,    -4800,    -4800]


    names = ['LM_09_redo']
    x_piezo = [-53000]
    x_hexap = [   -10]
    y_piezo = [ -4800]

    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(x_hexap), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexap)})"

    waxs_arc = [0, 20]
    ai0 = 0
    ai_list = [0.15]

    for name, xs, ys, xs_hexap in zip(names, x_piezo, y_piezo, x_hexap):
        if name=='ZL_05' or name=='ZL_06':
            ai_list = [0.08, 0.1, 0.15, 0.20]
        else:
          ai_list = [0.15]

        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(stage.x, xs_hexap)
        
        yield from bps.mv(piezo.th, ai0)
        yield from alignement_gisaxs_doblestack(0.15)

        ai0 = piezo.th.position
        det_exposure_time(t, t)

        for i, wa in enumerate(waxs_arc):
            # Do not take SAXS when WAXS detector in the way

            yield from bps.mv(waxs, wa)

            dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]

            yield from bps.mv(piezo.x, xs)
            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                name_fmt = "{sample}_{energy}eV_ai{ai}_wa{wax}"
                yield from bps.sleep(2)
                sample_name = name_fmt.format(sample=name, energy="%5.5d"%16100, ai="%3.2f"%ais, wax=wa)
                sample_id(user_name="WZ", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

            yield from bps.mv(piezo.th, ai0)
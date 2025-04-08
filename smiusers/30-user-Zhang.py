def new_folder(cycle, group):
    proposal_id(cycle, group)


def song_waxs_S_edge_new(t=1):
    dets = [pil300KW]

    yield from bps.mv(GV7.close_cmd, 1)
    yield from bps.sleep(5)
    yield from bps.mv(GV7.close_cmd, 1)

    energies = (
        np.arange(2445, 2470, 5).tolist()
        + np.arange(2470, 2480, 0.25).tolist()
        + np.arange(2480, 2490, 1).tolist()
        + np.arange(2490, 2501, 5).tolist()
    )
    waxs_arc = np.linspace(0, 13, 3)

    yield from bps.mv(stage.th, 1)
    yield from bps.mv(stage.y, -8)
    names = ["C2C8C10_2_0per_2", "C2C8C10_20per_2", "C2C8C10_40per_2"]
    x = [-29200, -34900, -40500]
    y = [-8470, -8620, -9240]

    for name, xs, ys in zip(names, x, y):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)

        yss = np.linspace(ys, ys + 620, 15)
        xss = np.linspace(xs, xs + 1000, 4)

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

                bpm = xbpm2.sumX.value

                sample_name = name_fmt.format(
                    sample=name, energy="%6.2f" % e, wax=wa, xbpm="%4.3f" % bpm
                )
                sample_id(user_name="GF", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 2470)
            yield from bps.mv(energy, 2450)


def song_waxs_S_edge_2022_1(t=1):
    dets = [pil1M, pil900KW]

    energies = (
        np.arange(2445, 2470, 5).tolist()
        + np.arange(2470, 2480, 0.25).tolist()
        + np.arange(2480, 2490, 1).tolist()
        + np.arange(2490, 2501, 5).tolist()
    )
    waxs_arc = [0, 20]

    names = ["sample_18l", "sample_10l", "sample_5l"]
    x = [33000, -2000, -36000]
    y = [-7000, -7000, -7000]

    for name, xs, ys in zip(names, x, y):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)

        yss = np.linspace(ys, ys + 1000, 58)
        xss = np.linspace(xs, xs, 1)

        yss, xss = np.meshgrid(yss, xss)
        yss = yss.ravel()
        xss = xss.ravel()

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)

            det_exposure_time(t, t)
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


def song_waxs_S_edge_2022_1(t=0.5):
    # single energy scan in tensile stage
    dets = [pil1M, pil900KW]

    energies = (
        np.arange(2445, 2470, 5).tolist()
        + np.arange(2470, 2480, 0.25).tolist()
        + np.arange(2480, 2490, 1).tolist()
        + np.arange(2490, 2501, 5).tolist()
    )
    waxs_arc = [0, 20]

    names = ["sample_18l"]
    x = [-0.3]
    y = [-0.06]

    for name, xs, ys in zip(names, x, y):
        yield from bps.mv(stage.x, xs)
        yield from bps.mv(stage.y, ys)

        yss = np.linspace(ys, ys + 1, 58)
        xss = np.linspace(xs, xs, 1)

        yss, xss = np.meshgrid(yss, xss)
        yss = yss.ravel()
        xss = xss.ravel()

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)

            det_exposure_time(t, t)
            name_fmt = "{sample}_{energy}eV_wa{wax}_bpm{xbpm}"
            for e, xsss, ysss in zip(energies, xss, yss):
                yield from bps.mv(energy, e)
                yield from bps.sleep(2)

                yield from bps.mv(stage.y, ysss)
                yield from bps.mv(stage.x, xsss)

                bpm = xbpm2.sumX.get()

                sample_name = name_fmt.format(
                    sample=name, energy="%6.2f" % e, wax=wa, xbpm="%4.3f" % bpm
                )
                sample_id(user_name="SZ", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 2470)
            yield from bps.mv(energy, 2450)


def song_saxs_tensile_hard(t=1):
    dets = [pil1M]

    names = "P3BT_loop2"

    t0 = time.time()
    for i in range(2000):

        det_exposure_time(t, t)
        name_fmt = "{sample}_10_18250eV_sdd1p6_{time}_{i}"
        t1 = time.time()
        sample_name = name_fmt.format(
            sample=names, time="%1.1f" % (t1 - t0), i="%3.3d" % i
        )
        sample_id(user_name="GF", sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")
        yield from bp.count(dets, num=1)

        time.sleep(20)


def song_saxs_waxs_tensile_hard(t=1):
    dets = [pil300KW, pil1M]

    names = "P3BT_loop2"
    t0 = time.time()
    for i in range(2000):
        det_exposure_time(t, t)

        if waxs.arc.position > 5:
            wa = [14, 7.5, 1]
        else:
            wa = [1, 7.5, 14]

        name_fmt = "{sample}_18250eV_{time}s_{i}_wa{wa}"
        t1 = time.time()
        for wax in wa:
            yield from bps.mv(waxs, wax)
            sample_name = name_fmt.format(
                sample=names, time="%1.1f" % (t1 - t0), i="%3.3d" % i, wa="%1.1f" % wax
            )
            sample_id(user_name="GF", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)


def song_tensile_tender_loop(t=1):
    # infinite time loop for contonuous data taking
    dets = [pil1M, pil900KW]

    names = "P77_loop1"
    t0 = time.time()
    for i in range(2000):
        det_exposure_time(t, t)

        if waxs.arc.position > 10:
            wa = [20, 0]
        else:
            wa = [0, 20]

        t1 = time.time()
        for wax in wa:
            if energy.energy.position > 2475:
                ener = [2478, 2470]
            else:
                ener = [2470, 2478]

            for ene in ener:
                name_fmt = "{sample}_{energy}eV_{time}s_{i}_wa{wa}"
                yield from bps.mv(energy, ene)

                yield from bps.mv(waxs, wax)
                sample_name = name_fmt.format(
                    sample=names,
                    energy="%6.2f" % ene,
                    time="%1.1f" % (t1 - t0),
                    i="%3.3d" % i,
                    wa="%1.1f" % wax,
                )
                sample_id(user_name="SZ", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)


def song_tensile_tender(t=0.4):
    # infinite time loop for contonuous data taking
    # dets = [pil1M, pil900KW]

    names = "P75_7_3_thickSEBS_50strain_cycle100_2"
    det_exposure_time(t, t)
    energies = [2470, 2476, 2478]

    if waxs.arc.position > 10:
        wa = [20, 0]
    else:
        wa = [0, 20]

    for wax in wa:
        dets = [pil900KW] if wax < 10 else [pil1M, pil900KW]

        if energy.energy.position > 2475:
            ener = energies[::-1]
        else:
            ener = energies

        for ene in ener:
            name_fmt = "{sample}_{energy}eV_{sdd}m_wa{wa}"
            yield from bps.mv(energy, ene)

            yield from bps.mv(waxs, wax)
            sdd = pil1m_pos.z.position / 1000

            sample_name = name_fmt.format(
                sample=names, energy="%6.2f" % ene, sdd="%.1f" % sdd, wa="%1.1f" % wax
            )
            sample_id(user_name="SZ", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)


def song_saxs_waxs_tensile_hard1(t=1, names="test"):
    dets = [pil300KW, pil1M]

    det_exposure_time(t, t)

    if waxs.arc.position > 5:
        wa = [14, 7.5, 1]
    else:
        wa = [1, 7.5, 14]

    name_fmt = "{sample}_18250eV_wa{wa}"
    for wax in wa:
        yield from bps.mv(waxs, wax)
        sample_name = name_fmt.format(sample=names, wa="%2.1f" % wax)
        sample_id(user_name="GF", sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")
        yield from bp.count(dets, num=1)


def song_waxs_new(t=1):
    dets = [pil300KW, pil1M]

    # yield from bps.mv(GV7.close_cmd, 1 )
    # yield from bps.sleep(5)
    # yield from bps.mv(GV7.close_cmd, 1 )

    waxs_arc = np.linspace(0, 13, 3)
    del_y = [-100, 0, 100]

    # yield from bps.mv(stage.th, 1)
    # yield from bps.mv(stage.y, -8)
    names = [
        "C2C6C8_0per",
        "C2C6C8_20per",
        "C2C6C8_40per",
        "C2C6C8_60per",
        "C2C6C8_80per",
        "C2C8C10_0per",
        "C2C8C10_20per",
        "C2C8C10_40per",
        "C2C8C10_60per",
        "C2C8C10_80per",
        "C2C8C10_100per",
        "C2C10C12_0per",
        "C2C10C12_20per",
        "C2C10C12_40per",
        "C2C10C12_60per",
        "C2C10C12_80per",
        "C2C10C12_100per",
    ]
    x = [
        43200,
        38200,
        33200,
        27200,
        21900,
        16900,
        11700,
        6700,
        1700,
        -3200,
        -9000,
        -14000,
        -19000,
        -24000,
        -29000,
        -34000,
        -40000,
    ]
    y = [
        -8500,
        -8500,
        -8500,
        -8500,
        -8300,
        -8500,
        -8500,
        -8500,
        -8700,
        -8300,
        -8800,
        -8500,
        -8500,
        -8500,
        -8500,
        -8700,
        -8800,
    ]

    names = ["bkg_vac"]
    x = [-10500]
    y = [-3000]

    for wa, de_y in zip(waxs_arc, del_y):
        yield from bps.mv(waxs, wa)
        for name, xs, ys in zip(names, x, y):
            yield from bps.mv(piezo.x, xs)
            yield from bps.mv(piezo.y, ys)

            det_exposure_time(t, t)
            name_fmt = "{sample}_10_16100eV_wa{wax}_bpm{xbpm}"

            bpm = xbpm2.sumX.value

            sample_name = name_fmt.format(sample=name, wax=wa, xbpm="%4.3f" % bpm)
            sample_id(user_name="GF", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)

    # yield from bps.mv(stage.y, 0)
    # yield from bps.mv(stage.th, 0)
    # names = ['C2C12C14_0per','C2C12C14_20per','C2C12C14_40per','C2C12C14_60per','C2C12C14_80per']
    # x = [44100, 4100, -100, -5100, -16100]
    # y = [-3000,-4000,-4000, -4000, -4000]

    # for wa, de_y in zip(waxs_arc, del_y):
    #     yield from bps.mv(waxs, wa)
    #     for name, xs, ys in zip(names, x, y):
    #         yield from bps.mv(piezo.x, xs)
    #         yield from bps.mv(piezo.y, ys+de_y)

    #         det_exposure_time(t,t)
    #         name_fmt = '{sample}_8_16100eV_wa{wax}_bpm{xbpm}'

    #         bpm = xbpm2.sumX.value

    #         sample_name = name_fmt.format(sample=name, wax = wa, xbpm = '%4.3f'%bpm)
    #         sample_id(user_name='GF', sample_name=sample_name)
    #         print(f'\n\t=== Sample: {sample_name} ===\n')
    #         yield from bp.count(dets, num=1)


def song_waxs_2020_3(t=1):
    dets = [pil300KW, pil1M]

    waxs_arc = np.linspace(19.5, 19.5, 1)
    del_y = [-500, 500, 3]

    yield from bps.mv(stage.th, 0)
    yield from bps.mv(stage.y, 0)
    names = [
        "A1",
        "A2",
        "A3",
        "A4",
        "A5",
        "B1",
        "B2",
        "B3",
        "B4",
        "B5",
        "C1",
        "C2",
        "C3",
        "C4",
        "C5",
        "D1",
        "D2",
        "D3",
        "D4",
        "D5",
        "E1",
        "E2",
        "E3",
        "E4",
        "E5",
        "F1",
        "F2",
        "F3",
        "F4",
        "F5",
        "G1",
        "G2",
        "G3",
    ]
    x = [
        43200,
        37500,
        32400,
        27000,
        21700,
        16700,
        11700,
        6700,
        1700,
        -3300,
        -8300,
        -13300,
        -18400,
        -23300,
        -28500,
        -34500,
        -40700,
        44000,
        39000,
        34000,
        28200,
        22700,
        17000,
        11000,
        5300,
        -500,
        -6400,
        -12100,
        -17900,
        -23300,
        -29000,
        -35200,
        -41200,
    ]
    y = [
        -7800,
        -7800,
        -7800,
        -7800,
        -7800,
        -7800,
        -7800,
        -7800,
        -7800,
        -7800,
        -7800,
        -7800,
        -7800,
        -7800,
        -7800,
        -7800,
        -7800,
        4500,
        4500,
        4300,
        4500,
        4500,
        4500,
        4500,
        4500,
        5400,
        4500,
        4500,
        5100,
        4500,
        4700,
        4700,
        4700,
    ]

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)
        for name, xs, ys in zip(names, x, y):
            yield from bps.mv(piezo.x, xs)
            yield from bps.mv(piezo.y, ys)

            det_exposure_time(t, t)
            name_fmt = "{sample}_10_16100eV_wa{wax}_bpm{xbpm}"

            bpm = xbpm2.sumX.value

            sample_name = name_fmt.format(
                sample=name, wax="%2.1f" % wa, xbpm="%4.3f" % bpm
            )
            sample_id(user_name="GF", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.rel_scan(dets, piezo.x, *del_y)

    # yield from bps.mv(stage.th, 1)
    # yield from bps.mv(stage.y, -7)
    # names = ['G4', 'H1', 'H2', 'H3', 'H4', 'H5']
    # x = [43200, 36800, 30000, 24200, 17500, 10600]
    # y = [-9000, -9000, -9000, -8900, -8900, -8500]

    # for wa in waxs_arc:
    #     yield from bps.mv(waxs, wa)
    #     for name, xs, ys in zip(names, x, y):
    #         yield from bps.mv(piezo.x, xs)
    #         yield from bps.mv(piezo.y, ys)

    #         det_exposure_time(t,t)
    #         name_fmt = '{sample}_16100eV_wa{wax}_bpm{xbpm}'

    #         bpm = xbpm2.sumX.value

    #         sample_name = name_fmt.format(sample=name, wax = '%2.1f'%wa, xbpm = '%4.3f'%bpm)
    #         sample_id(user_name='GF', sample_name=sample_name)
    #         print(f'\n\t=== Sample: {sample_name} ===\n')
    #         yield from bp.rel_scan(dets, piezo.x, *del_y)


def song_waxs_Sedge_2020_3(t=1):

    yield from bps.mv(GV7.close_cmd, 1)
    yield from bps.sleep(5)
    yield from bps.mv(GV7.close_cmd, 1)

    dets = [pil300KW]
    waxs_arc = np.linspace(0, 19.5, 4)
    energies = np.linspace(2460, 2490, 16)

    yield from bps.mv(stage.th, 0)
    yield from bps.mv(stage.y, 0)

    names = [
        "A1",
        "A2",
        "A3",
        "A4",
        "A5",
        "B1",
        "B2",
        "B3",
        "B4",
        "B5",
        "C1",
        "C2",
        "C3",
        "C4",
        "C5",
        "D1",
        "D2",
        "D3",
        "D4",
        "D5",
        "E1",
        "E2",
        "E3",
        "E4",
        "E5",
        "F1",
        "F2",
        "F3",
        "F4",
        "F5",
        "G1",
        "G2",
        "G3",
    ]
    x = [
        43300,
        37500,
        32150,
        26600,
        21600,
        16600,
        11600,
        6500,
        1500,
        -3500,
        -8300,
        -13300,
        -18650,
        -23800,
        -29000,
        -34500,
        -40950,
        44000,
        38750,
        33750,
        28450,
        22700,
        16500,
        11000,
        5050,
        -250,
        -6400,
        -12100,
        -17900,
        -23300,
        -29000,
        -35450,
        -41200,
    ]
    y = [
        -7300,
        -7300,
        -6800,
        -6800,
        -6800,
        -7000,
        -7000,
        -6500,
        -6500,
        -6700,
        -6700,
        -6700,
        -6700,
        -6500,
        -7000,
        -7000,
        -7000,
        5500,
        5500,
        5500,
        5500,
        5700,
        5900,
        5900,
        5900,
        6600,
        6100,
        5600,
        6400,
        5900,
        5900,
        6400,
        6400,
    ]

    for name, xs, ys in zip(names, x, y):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)

        yss = np.linspace(ys, ys + 500, 8)
        xss = np.linspace(xs, xs + 250, 2)

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

                bpm = xbpm2.sumX.value

                sample_name = name_fmt.format(
                    sample=name, energy="%6.2f" % e, wax=wa, xbpm="%4.3f" % bpm
                )
                sample_id(user_name="GF", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 2475)
            yield from bps.mv(energy, 2460)


def waxs_zhang(t=2):
    dets = [pil300KW]

    names = ["F1bd", "C1bd"]
    x = [-2000, -12000]
    y = [1500, 1500]

    # energies = np.linspace(2450, 2500, 26)
    waxs_arc = [0]

    for name, xs, ys in zip(names, x, y):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)

            det_exposure_time(t, t)
            name_fmt = "{sample}_16100.00eV_wa{wax}_bpm{xbpm}"

            bpm = xbpm2.sumX.value
            sample_name = name_fmt.format(sample=name, wax=wa, xbpm="%4.3f" % bpm)
            sample_id(user_name="SZ", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")

            yield from bp.count(dets, num=50)


def mapping_S_edge_zhang(t=2):
    dets = [pil300KW, pil1M]

    names = ["F3map", "C4map"]
    xx = [19200, 8800]
    yy = [600, 600]

    for x, y, name in zip(xx, yy, names):

        ys = np.linspace(y, y + 1800, 37)
        xs = np.linspace(x, x - 3000, 16)

        # energies = [2450, 2474, 2478, 2500]
        waxs_arc = [0]

        yss, xss = np.meshgrid(ys, xs)
        yss = yss.ravel()
        xss = xss.ravel()

        #  for e in energies:
        #      yield from bps.mv(energy, e)
        #      yield from bps.sleep(5)

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)

            for pos, (xsss, ysss) in enumerate(zip(xss, yss)):
                yield from bps.mv(piezo.x, xsss)
                yield from bps.mv(piezo.y, ysss)

                det_exposure_time(t, t)
                name_fmt = "{sample}_16100eV_wa{wax}_bpm{xbpm}_pos{posi}"
                bpm = xbpm2.sumX.value

                sample_name = name_fmt.format(
                    sample=name, wax=wa, xbpm="%4.3f" % bpm, posi="%3.3d" % pos
                )
                sample_id(user_name="SZ", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

    # yield from bps.mv(energy, 2470)
    # yield from bps.mv(energy, 2450)


def nightplan_S_edge_zhang(t=2):
    # yield from waxs_S_edge_zhang(t=2)
    # yield from bps.sleep(10)
    yield from mapping_S_edge_zhang(t=2)


def song_nexafs_S_2021_2(t=1):
    dets = [pil300KW]

    energies = (
        np.arange(2445, 2470, 5).tolist()
        + np.arange(2470, 2480, 0.25).tolist()
        + np.arange(2480, 2490, 1).tolist()
        + np.arange(2490, 2501, 5).tolist()
    )
    waxs_arc = np.linspace(52, 52, 1)

    # names = ['1A1', '1A2', '2E3', '1A4']
    # x = [42500, 36500, 30500, 25000]
    # y = [-4700, -4800, -5200, -5400]

    # names=['1A6','1A7','1A8', '1A9','1A10','1A11', '1A12',  '1B1',  '1B2',  '1B3',  '1B4',  '1B5',
    #      '1B6', '1B7', '1B8', '1B9','1B11','1B12',   'D1',   'D2',   'D3',   'D4',   'D5',   'D6',   'D7',   'D8',   'D9', 'D10']
    # x = [20100, 13200,  8900,  3100, -2900, -9200, -14700, -20700, -26700, -33700, -38700, -43000,
    #      45200, 39800, 33800, 28800, 22800, 17300, 10300,   4300,   -700,  -7500, -12500, -17700, -23700, -29400, -35300, -40800]
    # y = [-5000, -6100, -4700, -4700, -4700, -5100,  -4800,  -4800,  -4800,  -4800,  -4800,  -4500,
    #       7500,  7400,  7700,  7700,  7700,  8000,  7800,   7500,   7500,   7700,   7700,   7700,   7000,   7700,   7700,   7100]

    names = [
        "D11",
        "D12",
        "1E1",
        "1E2",
        "1E3",
        "1E4",
        "1E5",
        "1E6",
        "1E7",
        "1E8",
        "1E9",
        "1E10",
        "2E1",
        "2E2",
        "2E4",
        "2E6",
        "2F1",
        "2F2",
        "2F3",
    ]
    x = [
        44800,
        38800,
        33800,
        27800,
        22800,
        16800,
        11300,
        5500,
        0,
        -5300,
        -11000,
        -17000,
        -22000,
        -27200,
        -33700,
        -40500,
        43300,
        37300,
        31400,
    ]
    y = [
        -5700,
        -5700,
        -5700,
        -5500,
        -5500,
        -5600,
        -5600,
        -5600,
        -5600,
        -5600,
        -5600,
        -5600,
        -5600,
        -4500,
        -4700,
        -4400,
        6800,
        6800,
        6800,
    ]

    assert len(names) == len(
        x
    ), f"Number of X coordinates ({len(names)}) is different from number of samples ({len(x)})"
    assert len(y) == len(
        x
    ), f"Number of X coordinates ({len(y)}) is different from number of samples ({len(x)})"

    for name, xs, ys in zip(names, x, y):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)

            det_exposure_time(t, t)
            name_fmt = "{sample}_nexafs_{energy}eV_wa{wax}_bpm{xbpm}"
            for e in energies:
                yield from bps.mv(energy, e)
                yield from bps.sleep(1)

                bpm = xbpm2.sumX.value

                sample_name = name_fmt.format(
                    sample=name, energy="%6.2f" % e, wax=wa, xbpm="%4.3f" % bpm
                )
                sample_id(user_name="GF", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 2470)
            yield from bps.mv(energy, 2450)


def song_waxs_2021_2(t=1):
    dets = [pil300KW, pil1M]

    waxs_arc = np.linspace(0, 19.5, 4)

    # names=['1A1','1A2','2E3', '1A4', '1A6', '1A7', '1A8', '1A9','1A10','1A11', '1A12',  '1B1',  '1B2',  '1B3',  '1B4',  '1B5',
    #      '1B6', '1B7', '1B8', '1B9','1B11','1B12',  'D1',  'D2',  'D3',  'D4',   'D5',   'D6',   'D7',   'D8',   'D9', 'D10']
    # x = [42500, 36500, 30500, 25000, 20100, 13200,  8900,  3100, -2900, -9200, -14700, -20700, -26700, -33700, -38700, -43000,
    #      45200, 39800, 33800, 28800, 22800, 17300, 10300,  4300,  -700, -7500, -12500, -17700, -23700, -29400, -35300, -40800]
    # y = [-4700, -4800, -5000, -5200, -5000, -6100, -4700, -4700, -4700, -5100, -4800,  -4800,  -4800,  -4800,  -4800,  -4500,
    #       7500,  7400,  7700,  7700,  7700,  8000,  7800,  7500,  7500,  7700,   7700,   7700,   7000,   7700,   7700,   7100]

    names = ["1A4"]
    x = [25000]
    y = [-5200]

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)
        for name, xs, ys in zip(names, x, y):

            yield from bps.mv(piezo.x, xs)
            yield from bps.mv(piezo.y, ys)

            for pos, i in enumerate([0, 200, 400]):
                yield from bps.mv(piezo.x, xs + i)

                det_exposure_time(t, t)
                name_fmt = "{sample}_2_16100eV_sdd5m_wa{wax}_bpm{xbpm}_pos{pos}"

                bpm = xbpm2.sumX.value

                sample_name = name_fmt.format(
                    sample=name, wax="%2.1f" % wa, xbpm="%4.3f" % bpm, pos="%2.2d" % pos
                )
                sample_id(user_name="GF", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)


def song_waxs_Sedge_2021_1(t=1):
    # dets = [pil1M]
    dets = [pil300KW, pil1M]

    waxs_arc = np.linspace(0, 32.5, 6)

    # waxs_arc = np.linspace(0, 39, 7)
    energies = [2450, 2474, 2475, 2476, 2477, 2478]

    # names=['1A1','1A2','2E3', '1A4', '1A6', '1A7', '1A8', '1A9','1A10','1A11', '1A12',  '1B1',  '1B2',  '1B3',  '1B4',  '1B5',
    #      '1B6', '1B7', '1B8', '1B9','1B11','1B12',  'D1',  'D2',  'D3',  'D4',   'D5',   'D6',   'D7',   'D8',   'D9', 'D10']
    # x = [42500, 36700, 30000, 25300, 20100, 13600,  9000,  3100, -3100, -9400, -14700, -21200, -27000, -33700, -38700, -43000,
    #      45200, 39800, 33800, 28800, 22800, 17300, 10300,  4300,  -700, -7500, -12500, -17700, -23700, -29400, -35300, -40800]
    # y = [-4700, -4800, -5700, -5400, -5000, -6100, -4700, -4700, -2000, -5600, -4800,  -5100,  -5100,  -4800,  -4800,  -4500,
    #       7500,  7400,  7700,  7700,  7700,  8000,  7800,  7500,  7500,  7700,   7700,   7700,   7000,   7700,   7000,   7100]

    names = [
        "D11",
        "D12",
        "1E1",
        "1E2",
        "1E3",
        "1E4",
        "1E5",
        "1E6",
        "1E7",
        "1E8",
        "1E9",
        "1E10",
        "2E1",
        "2E2",
        "2E4",
        "2E6",
        "2F1",
        "2F2",
        "2F3",
    ]
    x = [
        44800,
        38800,
        33800,
        27800,
        22800,
        16800,
        11300,
        5500,
        0,
        -5300,
        -11000,
        -17000,
        -22000,
        -27200,
        -33700,
        -40500,
        43300,
        37300,
        31400,
    ]
    y = [
        -5700,
        -5700,
        -5700,
        -5500,
        -5500,
        -5600,
        -5600,
        -5600,
        -5600,
        -5600,
        -5600,
        -5600,
        -5600,
        -4500,
        -4700,
        -4400,
        6800,
        6800,
        6800,
    ]

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)

        for name, xs, ys in zip(names, x, y):
            yield from bps.mv(piezo.x, xs)
            yield from bps.mv(piezo.y, ys)
            xss = [0, -300]

            det_exposure_time(t, t)
            name_fmt = "{sample}_pos{pos}_sdd1.6m_{energy}eV_wa{wax}_bpm{xbpm}"
            for e in zip(energies):
                yield from bps.mv(energy, e)
                yield from bps.sleep(1)

                for k, xsss in enumerate(xss):
                    yield from bps.mv(piezo.x, xs + xsss)

                bpm = xbpm3.sumX.value

                sample_name = name_fmt.format(
                    sample=name, pos=k, energy="%6.2f" % e, wax=wa, xbpm="%4.3f" % bpm
                )
                sample_id(user_name="GF", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 2460)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 2450)
            yield from bps.sleep(2)


def song_waxs_2021_2(t=1):
    # dets = [pil1M]
    dets = [pil300KW, pil1M]

    waxs_arc = np.linspace(26, 26, 1)

    # names=['D11','D12', '1E1', '1E2', '1E3', '1E4', '1E5', '1E6', '1E7', '1E8',  '1E9', '1E10',  '2E1',  '2E2',  '2E4',  '2E6', '2F1', '2F2', '2F3']
    # x = [44800,  38800, 33800, 27800, 22500, 16800, 11300,  5500,     0, -5300, -11000, -17000, -22000, -27400, -33900, -40500, 43300, 37300, 31400]
    # y = [-5700,  -5700, -5700, -5500, -5350, -5800, -5800, -5800, -5800, -5500,  -5500,  -5500,  -5500,  -5100,  -5400,  -5400,  6800,  6800,  6500]

    names = [
        "1A1",
        "1A2",
        "2E3",
        "1A4",
        "1A6",
        "1A7",
        "1A8",
        "1A9",
        "1A10",
        "1A11",
        "1A12",
        "1B1",
        "1B2",
        "1B3",
        "1B4",
        "1B5",
        "1B6",
        "1B7",
        "1B8",
        "1B9",
        "1B11",
        "1B12",
        "D1",
        "D2",
        "D3",
        "D4",
        "D5",
        "D6",
        "D7",
        "D8",
        "D9",
        "D10",
    ]
    x = [
        42500,
        37200,
        30500,
        25300,
        20800,
        13800,
        9500,
        3100,
        -3100,
        -9200,
        -14700,
        -20700,
        -27000,
        -32600,
        -37300,
        -43000,
        45500,
        39800,
        34300,
        29800,
        22800,
        17900,
        10300,
        5000,
        -700,
        -6500,
        -12000,
        -17700,
        -23200,
        -29400,
        -34500,
        -40300,
    ]
    y = [
        -4700,
        -4900,
        -5700,
        -5400,
        -5200,
        -6400,
        -4900,
        -4800,
        -5500,
        -5600,
        -5600,
        -5600,
        -5600,
        -5600,
        -5600,
        -5600,
        7500,
        7400,
        7700,
        7700,
        7700,
        7900,
        6700,
        6700,
        6700,
        6700,
        6700,
        6700,
        7000,
        7000,
        6400,
        6400,
    ]

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


def song_waxs_S_edge_2022_2(t=1, strain=0):
    """
    Tender scans
    Args:
        t (float): detector exposure time,
        strain (float): strain value from Linkam MFS stage for filename metadata
    """

    names = ["P75_uncross_attempt2_1s"]
    x = [-0.3]
    y = [0.8]

    user_name = "SZ"
    energies = np.concatenate(
        (np.arange(2460, 2471, 5), np.arange(2475, 2480, 0.5), np.arange(2480, 2491, 5))
    )
    waxs_arc = [0, 20]
    names = [
        n.translate({ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ =,"}) for n in names
    ]

    for name, xs, ys in zip(names, x, y):
        yield from bps.mv(stage.x, xs)
        yield from bps.mv(stage.y, ys)

        yss = np.linspace(ys, ys + 0.4, len(energies))
        xss = np.linspace(xs, xs, 1)

        yss, xss = np.meshgrid(yss, xss)
        yss = yss.ravel()
        xss = xss.ravel()

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)
            dets = [pil900KW] if waxs.arc.position < 15 else [pil1M, pil900KW]
            det_exposure_time(t, t)
            name_fmt = (
                "{sample}_{energy}eV_strain{strain}_wa{wax}_sdd{sdd}m_id{scan_id}"
            )

            for e, xsss, ysss in zip(energies, xss, yss):
                yield from bps.mv(energy, e)
                yield from bps.sleep(2)

                yield from bps.mv(stage.y, ysss)
                yield from bps.mv(stage.x, xsss)

                # Metadata
                sdd = pil1m_pos.z.position / 1000
                scan_id = db[-1].start["scan_id"] + 1

                sample_name = name_fmt.format(
                    sample=name,
                    strain=strain,
                    energy="%6.2f" % e,
                    wax=wa,
                    sdd="%.1f" % sdd,
                    scan_id=scan_id,
                )
                sample_id(user_name=user_name, sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets)

            yield from bps.mv(energy, 2475)
            yield from bps.mv(energy, 2460)


def song_waxs_hard_2022_2(t=1, strain=0):
    """
    Hard X-ray script for MFS stage manual

    Args:
        t (float): detector exposure time,
        strain (float): strain value from Linkam MFS stage for filename metadata
    """

    names = ["p77_cross2_2s"]
    x = [-0.6]
    y = [-1.2]

    user_name = "SZ"

    waxs_arc = [0, 20]
    names = [
        n.translate({ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ =,"}) for n in names
    ]

    for name, xs, ys in zip(names, x, y):
        yield from bps.mv(stage.x, xs)
        yield from bps.mv(stage.y, ys)

        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)
            dets = [pil900KW] if waxs.arc.position < 15 else [pil1M, pil900KW]
            yield from bps.mv(stage.y, ys + i * 0.05)
            det_exposure_time(t, t)
            name_fmt = (
                "{sample}_{energy}keV_strain{strain}_wa{wax}_sdd{sdd}m_id{scan_id}"
            )

            # Metadata
            sdd = pil1m_pos.z.position / 1000
            e = energy.position.energy / 1000
            scan_id = db[-1].start["scan_id"] + 1

            sample_name = name_fmt.format(
                sample=name,
                strain=strain,
                energy="%2.1f" % e,
                wax=wa,
                sdd="%.1f" % sdd,
                scan_id=scan_id,
            )
            sample_id(user_name=user_name, sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets)
            sample_id(user_name="test", sample_name="test")



def waxs_S_edge_song_2022_3(t=1):
    dets = [pil900KW, pil1M]

    # names = [   'A1',      'A2',      'A3',  'A4_par',  'A4_per',  'A5_per',  'A5_par',      'B1',   'B3',
    #             'B4',  'B5_par',  'B5_per',      'C1',      'C2',      'C3',  'C4_par',  'C4_per']
    # x_piezo = [44000,     33500,     23000,     13000,      2000,     -8000,    -18500,    -28000, -39000,
    #            43000,     33000,     23000,     13000,      3000,     -7000,    -16000,    -27000]
    # y_piezo = [-8500,     -8500,     -9000,     -9000,     -9000,     -7500,     -8500,     -8500,  -8500, 
    #             4500,      4400,      3500,      3800,      3800,      4800,      4500,      4300]

    names = [   'A5_per_60deg']
    x_piezo = [-8000]
    y_piezo = [-7000]

    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"

    energies = np.arange(2450, 2470, 5).tolist()+ np.arange(2470, 2475, 1).tolist()+np.arange(2475, 2480, 0.5).tolist()+ np.arange(2480, 2490, 2).tolist()+ np.arange(2490, 2521, 5).tolist()

    waxs_arc = [0, 20, 40]

    for name, xs, ys in zip(names, x_piezo, y_piezo):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)

        yss = np.linspace(ys, ys + 1000, 31)
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

            name_fmt = "{sample}_sdd3.0m_{energy}eV_wa{wax}_bpm{xbpm}"
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

                sample_name = name_fmt.format(sample=name, energy="%6.2f" % e, wax=wa, xbpm="%4.3f" % bpm)
                sample_id(user_name="GF", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")

                yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 2490)
            yield from bps.sleep(3)
            yield from bps.mv(energy, 2470)
            yield from bps.sleep(3)
            yield from bps.mv(energy, 2450)
            yield from bps.sleep(3)



def hardxray_song_2022_3(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    names = [ 'AM_01', 'AM_02', 'AM_03', 'AM_04', 'AM_05',  'AM_06',  'AM_07',  'AM_08', 
              'YW_01', 'YW_02', 'YW_03', 'YW_04', 'YW_05',  'YW_06']
    x_piezo = [-50000,  -45000,  -29000,  -12000,    3000,    19000,    37000,    42000,
               -45000,  -29000,  -12000,    3000,   19000,    35000]
    x_hexap = [   -10,       0,       0,       0,       0,        0,        0,       10,
                    0,       0,       0,       0,       0,        0]
    y_piezo = [  4400,    4400,    4300,    4200,    4200,     4100,     4100,     4000,
                -4800,   -4800,   -4800,   -4800,   -4800,    -4800]

    #'LM_09'
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
def waxs_Se_edge_chris_n(t=1):

    dets = [pil300KW]

    names = ["J1_01", "J1_02", "J1_03", "J1_04"]
    x = [18200, 12400, 6400, 400]
    y = [-7300, -7400, -7500, -7500]

    energies = (
        np.arange(12620, 12640, 5).tolist()
        + np.arange(12640, 12660, 0.5).tolist()
        + np.arange(12660, 12670, 1).tolist()
        + np.arange(12670, 12701, 5).tolist()
    )
    waxs_arc = np.linspace(0, 26, 5)

    for name, xs, ys in zip(names, x, y):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)

        yss = np.linspace(ys, ys + 1000, 31)
        xss = np.array([xs, xs + 500])

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
                    sample=name, energy="%7.2f" % e, wax=wa, xbpm="%1.3f" % bpm
                )
                sample_id(user_name="CM", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 12670)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 12640)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 12620)
            yield from bps.sleep(2)


def NEXAFS_Br_edge(t=0.5, name="sample1"):
    dets = [pil300KW]
    # name = 'Kapton_NEXAFS_1_gvopen_wa70_'
    # x = [8800]

    energies = (
        np.arange(12620, 12640, 5).tolist()
        + np.arange(12640, 12660, 0.5).tolist()
        + np.arange(12660, 12670, 1).tolist()
        + np.arange(12670, 12716, 5).tolist()
    )
    energies = 815 + np.asarray(energies)

    det_exposure_time(t, t)
    name_fmt = "{sample}_{energy}eV_xbpm{xbpm}"
    for e in energies:
        yield from bps.mv(energy, e)
        sample_name = name_fmt.format(
            sample=name, energy="%7.2f" % e, xbpm="%3.1f" % xbpm3.sumY.value
        )
        sample_id(user_name="CM", sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")
        yield from bp.count(dets, num=1)

    yield from bps.mv(energy, 13500)


def waxs_Br_edge_chris(t=1):

    det_exposure_time(t, t)

    names = ["Br_01_02", "Br_01_03"]
    x = [46300, 41200]
    y = [-9200, -9200]

    dets = [pil300KW, pil1M]
    energies = (
        np.arange(12620, 12640, 5).tolist()
        + np.arange(12640, 12660, 0.5).tolist()
        + np.arange(12660, 12670, 1).tolist()
        + np.arange(12670, 12716, 5).tolist()
    )
    energies = 815 + np.asarray(energies)

    waxs_arc = np.linspace(0, 26, 5)

    for name, xs, ys in zip(names, x, y):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)

        yss = np.linspace(ys, ys + 500, 32)
        xss = np.array([xs, xs - 500])

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
                    sample=name, energy="%7.2f" % e, wax=wa, xbpm="%1.3f" % bpm
                )
                sample_id(user_name="CM", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 13495)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 13460)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 13435)
            yield from bps.sleep(2)


def giwaxs_Se_edge_chris(t=1):
    dets = [pil300KW]

    names = ["J2_01", "J2_02", "J2_03", "J2_04"]
    x = [46000, 28000, 10000, -11000]

    energies = (
        np.arange(12620, 12640, 5).tolist()
        + np.arange(12640, 12660, 0.5).tolist()
        + np.arange(12660, 12670, 1).tolist()
        + np.arange(12670, 12701, 5).tolist()
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

        yield from alignement_gisaxs(angle=0.2)

        yield from bps.mv(GV7.close_cmd, 1)
        yield from bps.sleep(1)
        yield from bps.mv(GV7.close_cmd, 1)
        yield from bps.sleep(1)

        ai0 = piezo.th.position
        yield from bps.mv(piezo.th, ai0 + 0.13)

        xss = np.linspace(xs, xs - 8000, 71)
        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)

            det_exposure_time(t, t)
            name_fmt = "{sample}_{energy}eV_ai0.13_wa{wax}_bpm{xbpm}"
            for e, xsss in zip(energies, xss):
                yield from bps.mv(energy, e)
                yield from bps.sleep(2)

                yield from bps.mv(piezo.x, xsss)
                bpm = xbpm2.sumX.value

                sample_name = name_fmt.format(
                    sample=name, energy="%7.2f" % e, wax=wa, xbpm="%1.3f" % bpm
                )
                sample_id(user_name="GF", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 12670)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 12640)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 12620)
            yield from bps.sleep(2)


def nexafs_90deg_McNeil(t=1):
    dets = [pil300KW]

    energies = (
        np.arange(2445, 2470, 5).tolist()
        + np.arange(2470, 2480, 0.25).tolist()
        + np.arange(2480, 2490, 1).tolist()
        + np.arange(2490, 2501, 5).tolist()
    )
    waxs_arc = [52.5]

    ai = [0.7, 20, 55]

    names = ["D1_06"]

    for name in names:
        det_exposure_time(t, t)
        name_fmt = "nexafs_vert_{sample}_{energy}eV_angle{ai}_bpm{xbpm}"

        ai0 = prs.position

        for ais in ai:
            yield from bps.mv(prs, ai0 - ais)
            yield from bps.mvr(piezo.y, 100)

            for e in energies:
                yield from bps.mv(energy, e)
                yield from bps.sleep(1)

                bpm = xbpm2.sumX.value

                sample_name = name_fmt.format(
                    sample=name,
                    energy="%6.2f" % e,
                    ai="%2.2d" % ais,
                    xbpm="%4.3f" % bpm,
                )
                sample_id(user_name="GF", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

        yield from bps.mv(energy, 2470)
        yield from bps.mv(energy, 2450)


def giwaxs_vert_S_edge_McNeil(t=1):
    dets = [pil300KW]

    names = ["3-2_ver_per_redo"]
    x = [-1333.6]
    ys = [-5000]
    # names = ['3-1_ver_par', '3-2_ver_per', '4-1_ver']

    energies = (
        np.arange(2445, 2470, 5).tolist()
        + np.arange(2470, 2480, 0.25).tolist()
        + np.arange(2480, 2490, 1).tolist()
        + np.arange(2490, 2501, 5).tolist()
    )

    waxs_arc = [4, 10.5, 17]
    dets = [pil300KW]

    for name, y in zip(names, ys):
        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(piezo.y, y)

            if i == 0:
                print("wa=4deg")
            else:
                yield from bps.mv(waxs, wa)

            name_fmt = (
                "GIWAXS_90deg_{sample}_{energy}eV_pos{pos}_ai1.5_wa{wax}_bpm{xbpm}"
            )
            for k, e in enumerate(energies):
                yield from bps.mv(energy, e)
                yield from bps.sleep(1)
                yield from bps.mvr(piezo.y, 3)

                bpm = xbpm2.sumX.value
                sample_name = name_fmt.format(
                    sample=name,
                    energy="%6.2f" % e,
                    pos="%2.2d" % k,
                    wax=wa,
                    xbpm="%4.3f" % bpm,
                )
                sample_id(user_name="GF", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)
            yield from bps.mv(energy, 2470)
            yield from bps.mv(energy, 2450)

    for name, y in zip(names, ys):
        yield from bps.mv(piezo.y, y)

        name_fmt = "GIWAXS_90deg_{sample}_{energy}eV__pos{pos}_ai1.5_wa{wax}_bpm{xbpm}"
        for k, e in enumerate(energies):
            yield from bps.mvr(piezo.y, 3)

            bpm = xbpm2.sumX.value
            sample_name = name_fmt.format(
                sample=name, energy=2450, pos="%2.2d" % k, wax=17, xbpm="%4.3f" % bpm
            )
            sample_id(user_name="GF", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)


def transition_S_Cl_edges():
    yield from bps.mv(energy, 2450)
    yield from bps.sleep(5)
    yield from bps.mv(energy, 2475)
    yield from bps.sleep(5)
    yield from bps.mv(energy, 2500)
    yield from bps.sleep(5)
    yield from bps.mv(energy, 2525)
    yield from bps.sleep(5)
    yield from bps.mv(energy, 2550)
    yield from bps.sleep(5)
    yield from bps.mv(energy, 2580)
    yield from bps.sleep(5)
    yield from bps.mv(energy, 2610)
    yield from bps.sleep(5)
    yield from bps.mv(energy, 2640)
    yield from bps.sleep(5)
    yield from bps.mv(energy, 2660)
    yield from bps.sleep(5)
    yield from bps.mv(energy, 2680)
    yield from bps.sleep(5)
    yield from bps.mv(energy, 2700)
    yield from bps.sleep(5)
    yield from bps.mv(energy, 2720)
    yield from bps.sleep(5)
    yield from bps.mv(energy, 2740)
    yield from bps.sleep(5)
    yield from bps.mv(energy, 2760)
    yield from bps.sleep(5)
    yield from bps.mv(energy, 2780)
    yield from bps.sleep(5)
    yield from bps.mv(energy, 2800)
    yield from bps.sleep(5)


def nexafs_oriented_S_edge_corr_only_allprs(t=1):
    dets = [pil300KW]

    # prs 0 deg
    yield from bps.mv(prs, 1)
    names = [
        "1-1_par_prs0deg",
        "1-2_per_prs0deg",
        "1-3_45de_prs0deg",
        "2-2_prs0deg",
        "5-1_par_prs0deg",
        "5-2_per_prs0deg",
        "5-3_45de_prs0deg",
        "6-1_prs0deg",
    ]
    x = [13300, 4600, -6600, -15000, 9000, 700, -7300, -15500]
    y = [-6000, -5800, -6200, -5500, 7000, 6700, 6700, 7500]

    energies = (
        np.arange(2445, 2470, 5).tolist()
        + np.arange(2470, 2480, 0.25).tolist()
        + np.arange(2480, 2490, 1).tolist()
        + np.arange(2490, 2501, 5).tolist()
    )
    waxs_arc = np.linspace(52, 52, 1)

    for name, xs, ys in zip(names, x, y):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)

        yss = np.linspace(ys, ys + 250, 58)
        xss = np.linspace(xs, xs, 1)

        yss, xss = np.meshgrid(yss, xss)
        yss = yss.ravel()
        xss = xss.ravel()

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)

            yield from bps.mv(energy, 2500)
            name_fmt = "nexafs_intcor_{sample}_{energy}eV_wa{wax}_bpm{xbpm}"
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

    # prs 30 deg
    yield from bps.mv(prs, -29)
    names = [
        "1-1_par_prs30deg",
        "1-2_per_prs30deg",
        "1-3_45de_prs30deg",
        "2-2_prs30deg",
        "5-1_par_prs30deg",
        "5-2_per_prs30deg",
        "5-3_45de_prs30deg",
        "6-1_prs30deg",
    ]
    x = [14000, 4900, -6000, -14200, 9700, 1000, -6000, -14400]
    y = [-6000, -6000, -6200, -5500, 7000, 7000, 7000, 7500]

    energies = (
        np.arange(2445, 2470, 5).tolist()
        + np.arange(2470, 2480, 0.25).tolist()
        + np.arange(2480, 2490, 1).tolist()
        + np.arange(2490, 2501, 5).tolist()
    )
    waxs_arc = np.linspace(52, 52, 1)

    for name, xs, ys in zip(names, x, y):
        xss = np.linspace(xs - 200, xs - 200, 1)
        yield from bps.mv(piezo.y, ys)

        yss = np.linspace(ys, ys + 250, 58)
        xss = np.linspace(xs, xs, 1)

        yss, xss = np.meshgrid(yss, xss)
        yss = yss.ravel()
        xss = xss.ravel()

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)

            yield from bps.mv(energy, 2500)
            name_fmt = "nexafs_intcor_{sample}_{energy}eV_wa{wax}_bpm{xbpm}"
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

    # prs 60 deg
    yield from bps.mv(prs, -59)
    names = [
        "1-1_par_prs60deg",
        "1-2_per_prs60deg",
        "1-3_45de_prs60deg",
        "2-2_prs60deg",
        "5-1_par_prs60deg",
        "5-2_per_prs60deg",
        "5-3_45de_prs60deg",
        "6-1_prs60deg",
    ]
    x = [15200, 6400, -3600, -11900, 11200, 3200, -3800, -12400]
    y = [-6000, -6000, -6200, -5500, 7000, 7000, 7000, 7500]

    energies = (
        np.arange(2445, 2470, 5).tolist()
        + np.arange(2470, 2480, 0.25).tolist()
        + np.arange(2480, 2490, 1).tolist()
        + np.arange(2490, 2501, 5).tolist()
    )
    waxs_arc = np.linspace(52, 52, 1)

    for name, xs, ys in zip(names, x, y):
        xss = np.linspace(xs - 200, xs - 200, 1)
        yield from bps.mv(piezo.y, ys)

        yss = np.linspace(ys, ys + 250, 58)
        xss = np.linspace(xs, xs, 1)

        yss, xss = np.meshgrid(yss, xss)
        yss = yss.ravel()
        xss = xss.ravel()

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)

            yield from bps.mv(energy, 2500)
            name_fmt = "nexafs_intcor_{sample}_{energy}eV_wa{wax}_bpm{xbpm}"
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

            yield from bps.mv(energy, 2470)
            yield from bps.mv(energy, 2450)

    yield from bps.mv(prs, 1)


def waxs_S_edge_chris_2021_3(t=1):
    dets = [pil900KW, pil1M]

    # names = ['A2_01', 'A2_02', 'A2_03', 'A2_04', 'A2_05', 'A2_06', 'A2_07', 'A2_08', 'A2_09', 'A2_10', 'A2_11', 'A2_12', 'A2_13', 'A2_14',
    # 'A2_15', 'B2_01', 'B2_02', 'B2_03', 'B2_04', 'B2_05', 'B2_06', 'B2_07', 'B2_08', 'B2_09', 'B2_10', 'B2_11', 'B2_12', 'C2_01', 'C2_02',
    # 'C2_03', 'C2_04', 'C2_05', 'C2_06', 'C2_07']
    # x = [      44000,   38500,   33000,   27500,   21500,   16200,   10700,    5000,    -500,   -6000,  -11500,  -16500,  -21700,  -27000,
    #  -32500,  -37500,  -43000,   45000,   39800,   34200,   29200,   24000,   18800,   13600,    8300,    2800,   -2400,   -7800,  -12900,
    #  -18000,  -23600,  -28600,  -33700,  -38800]
    # y = [      -7800,   -7700,   -7650,   -7700,   -7700,   -7700,   -7500,   -7200,   -7200,   -7200,   -7200,   -7400,   -7500,   -7300,
    #   -7200,   -7250,   -6900,    5400,    5400,    5500,    5400,    5300,    5300,    5200,    5350,    5500,    5500,    5600,    5700,
    #    5800,    5550,    5700,    5300,    5500]

    # names = ['C2_08', 'C2_09', 'C2_10', 'C2_11', 'D2_01', 'D2_02', 'D2_03', 'D2_04', 'D2_05', 'D2_06', 'D2_07', 'D2_08', 'D2_09']
    # x = [      35000,   29000,   24000,   18300,   13000,    7500,    2000,  -10500,  -15800,  -21800,  -27500,  -32700,  -38700]
    # y = [      -8200,   -8200,   -8200,   -8300,   -8200,   -8550,   -8500,   -8300,   -8300,   -8250,   -8000,   -7850,   -7700]

    names = ["D2_03", "D2_04", "D2_05", "D2_06", "D2_07", "D2_08", "D2_09"]
    x = [2000, -10500, -15800, -21800, -27500, -32700, -38700]
    y = [-8500, -8300, -8300, -8250, -8000, -7850, -7700]

    assert len(x) == len(
        y
    ), f"Number of X coordinates ({len(x)}) is different from number of samples ({len(y)})"
    assert len(x) == len(
        names
    ), f"Number of X coordinates ({len(x)}) is different from number of samples ({len(names)})"

    energies = (
        np.arange(2445, 2470, 5).tolist()
        + np.arange(2470, 2480, 0.25).tolist()
        + np.arange(2480, 2490, 1).tolist()
        + np.arange(2490, 2500, 5).tolist()
        + np.arange(2500, 2560, 10).tolist()
    )
    waxs_arc = [0, 20, 40]

    for name, xs, ys in zip(names, x, y):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)

        yss = np.linspace(ys, ys + 1400, 63)
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

            name_fmt = "{sample}_sdd7.0m_{energy}eV_wa{wax}_bpm{xbpm}"
            for e, xsss, ysss in zip(energies, xss, yss):
                yield from bps.mv(energy, e)
                if energy.energy.position - e > 5:
                    yield from bps.mv(energy, e - 5)
                    yield from bps.sleep(2)
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                elif energy.energy.position - e > 2:
                    yield from bps.sleep(5)
                else:
                    yield from bps.sleep(2)

                if xbpm2.sumX.get() < 120:
                    yield from bps.sleep(5)
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(3)

                yield from bps.mv(piezo.y, ysss)
                yield from bps.mv(piezo.x, xsss)

                bpm = xbpm2.sumX.value

                sample_name = name_fmt.format(
                    sample=name, energy="%6.2f" % e, wax=wa, xbpm="%4.3f" % bpm
                )
                sample_id(user_name="GF", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")

                yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 2500)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 2480)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 2445)


def waxs_Cl_edge_chris_2021_3(t=1):
    dets = [pil900KW, pil1M]

    names = [
        "B2_01",
        "B2_02",
        "B2_03",
        "B2_04",
        "B2_05",
        "B2_06",
        "B2_07",
        "B2_08",
        "B2_09",
        "B2_10",
        "B2_11",
        "B2_12",
    ]
    x = [
        -37000,
        -42500,
        45600,
        40400,
        34900,
        29800,
        24600,
        19600,
        14200,
        8900,
        3400,
        -1800,
    ]
    y = [-7250, -6900, 5400, 5400, 5500, 5400, 5300, 5250, 5200, 5300, 5400, 5500]

    assert len(x) == len(
        y
    ), f"Number of X coordinates ({len(x)}) is different from number of samples ({len(y)})"
    assert len(x) == len(
        names
    ), f"Number of X coordinates ({len(x)}) is different from number of samples ({len(names)})"

    energies = (
        np.arange(2810, 2820, 5).tolist()
        + np.arange(2820, 2825, 1).tolist()
        + np.arange(2825, 2835, 0.25).tolist()
        + np.arange(2835, 2840, 0.5).tolist()
        + np.arange(2840, 2850, 5).tolist()
        + np.arange(2850, 2910, 10).tolist()
    )

    waxs_arc = [0, 20, 40]

    for name, xs, ys in zip(names, x, y):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)

        yss = np.linspace(ys, ys + 1500, 65)
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

            name_fmt = "{sample}_sdd7.0m_{energy}eV_wa{wax}_bpm{xbpm}"
            for e, xsss, ysss in zip(energies, xss, yss):
                yield from bps.mv(energy, e)
                yield from bps.sleep(2)

                if xbpm2.sumX.get() < 120:
                    yield from bps.sleep(5)
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

            yield from bps.mv(energy, 2880)
            yield from bps.sleep(3)
            yield from bps.mv(energy, 2850)
            yield from bps.sleep(3)
            yield from bps.mv(energy, 2810)
            yield from bps.sleep(3)


def giwaxs_S_edge_2021_3(t=1):
    dets = [pil900KW]

    # names = ['A1_01', 'A1_02', 'A1_03', 'A1_04', 'A1_05', 'A1_06', 'A1_07', 'A1_08', 'A1_09']
    # x_piezo = [59000,   57000,   40000,   24000,    7000,  -10000,  -27000,  -44000,  -48000]
    # x_hexa = [    15,       0,       0,       0,       0,       0,       0,       0,     -13]
    # y_piezo = [ 5900,    5900,    5900,    5900,    5900,    5900,    5900,    5900,    5900]

    names = ["A1_10", "A1_11", "A1_12", "A1_13", "A1_14", "A1_15"]
    x_piezo = [59000, 57000, 42000, 25000, 8000, -10000]
    x_hexa = [16, 0, 0, 0, 0, 0]
    y_piezo = [5900, 5900, 5900, 5900, 5900, 5900]

    energies = (
        np.arange(2445, 2470, 5).tolist()
        + np.arange(2470, 2480, 0.25).tolist()
        + np.arange(2480, 2490, 1).tolist()
        + np.arange(2490, 2500, 5).tolist()
        + np.arange(2500, 2560, 10).tolist()
    )
    waxs_arc = [0, 20, 40]
    ai0 = 0

    assert len(x_piezo) == len(
        x_hexa
    ), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexa)})"
    assert len(x_piezo) == len(
        names
    ), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(
        y_piezo
    ), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"

    for name, xs_piezo, xs_hexa, ys_piezo in zip(names, x_piezo, x_hexa, y_piezo):
        yield from bps.mv(piezo.x, xs_piezo)
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.y, ys_piezo)

        yield from bps.mv(piezo.th, ai0)

        yield from bps.mv(GV7.open_cmd, 1)
        yield from bps.sleep(1)
        yield from bps.mv(GV7.open_cmd, 1)
        yield from bps.sleep(1)

        yield from alignement_gisaxs(angle=0.4)

        yield from bps.mv(GV7.close_cmd, 1)
        yield from bps.sleep(1)
        yield from bps.mv(GV7.close_cmd, 1)
        yield from bps.sleep(1)

        ai0 = piezo.th.position
        yield from bps.mv(piezo.th, ai0 + 0.7)
        xss = np.linspace(xs_piezo, xs_piezo - 8000, 63)

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)

            det_exposure_time(t, t)
            name_fmt = "{sample}_{energy}eV_ai0.7_wa{wax}_bpm{xbpm}"
            for k, (e, xsss) in enumerate(zip(energies, xss)):
                yield from bps.mv(energy, e)
                yield from bps.sleep(2)
                if xbpm2.sumX.get() < 120:
                    yield from bps.sleep(5)
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)

                yield from bps.mv(piezo.x, xsss)
                bpm = xbpm2.sumX.get()

                sample_name = name_fmt.format(
                    sample=name, energy="%6.2f" % e, wax=wa, xbpm="%4.3f" % bpm
                )
                sample_id(user_name="GF", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 2510)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 2490)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 2470)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 2450)
            yield from bps.sleep(2)


def giwaxs_S_edge_2021_3_doblestack(t=1):
    dets = [pil900KW]

    # names = ['A1_01', 'A1_02', 'A1_03', 'A1_04', 'A1_05', 'A1_06', 'A1_07', 'A1_08', 'A1_09']
    # x_piezo = [59000,   57000,   40000,   24000,    7000,  -10000,  -27000,  -44000,  -48000]
    # x_hexa = [    15,       0,       0,       0,       0,       0,       0,       0,     -13]
    # y_piezo = [ 5900,    5900,    5900,    5900,    5900,    5900,    5900,    5900,    5900]

    names = [
        "B1_11",
        "B1_12",
        "C1_01",
        "C1_02",
        "C1_03",
        "C1_04",
        "C1_05",
        "C1_06",
        "C1_07",
        "C1_08",
        "C1_09",
        "C1_10",
        "C1_11",
        "D1_01",
        "D1_02",
        "D1_03",
        "D1_04",
        "D1_05",
    ]
    x_piezo = [
        59000,
        54000,
        38000,
        20000,
        6000,
        -8000,
        -24000,
        -40000,
        -46000,
        59000,
        54000,
        38000,
        22000,
        6000,
        -8000,
        -25000,
        -41000,
        -46000,
    ]
    x_hexa = [9, 0, 0, 0, 0, 0, 0, 0, 0, 11, 0, 0, 0, 0, 0, 0, 0, -11]
    y_piezo = [
        5900,
        5900,
        5900,
        5900,
        5900,
        5900,
        5900,
        5900,
        5900,
        -2700,
        -2700,
        -2700,
        -2700,
        -2700,
        -2700,
        -2700,
        -2700,
        -2700,
    ]
    z_piezo = [
        -2500,
        -2500,
        -2500,
        -2500,
        -2500,
        -2500,
        -2500,
        -2500,
        -2500,
        5000,
        5000,
        5000,
        5000,
        5000,
        5000,
        5000,
        5000,
        5000,
    ]

    energies = (
        np.arange(2445, 2470, 5).tolist()
        + np.arange(2470, 2480, 0.25).tolist()
        + np.arange(2480, 2490, 1).tolist()
        + np.arange(2490, 2500, 5).tolist()
        + np.arange(2500, 2560, 10).tolist()
    )
    waxs_arc = [0, 20]
    ai0 = 0

    assert len(x_piezo) == len(
        x_hexa
    ), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexa)})"
    assert len(x_piezo) == len(
        names
    ), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(
        y_piezo
    ), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(
        z_piezo
    ), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(z_piezo)})"

    for name, xs_piezo, xs_hexa, ys_piezo, zs_piezo in zip(
        names, x_piezo, x_hexa, y_piezo, z_piezo
    ):
        yield from bps.mv(piezo.x, xs_piezo)
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.y, ys_piezo)
        yield from bps.mv(piezo.z, zs_piezo)

        yield from bps.mv(piezo.th, ai0)

        yield from bps.mv(GV7.open_cmd, 1)
        yield from bps.sleep(1)
        yield from bps.mv(GV7.open_cmd, 1)
        yield from bps.sleep(1)

        yield from alignement_gisaxs_test(angle=0.7)

        yield from bps.mv(GV7.close_cmd, 1)
        yield from bps.sleep(1)
        yield from bps.mv(GV7.close_cmd, 1)
        yield from bps.sleep(1)

        ai0 = piezo.th.position
        yield from bps.mv(piezo.th, ai0 + 0.7)
        xss = np.linspace(xs_piezo, xs_piezo - 8000, 63)

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)

            det_exposure_time(t, t)
            name_fmt = "{sample}_{energy}eV_ai0.7_wa{wax}_bpm{xbpm}"
            for k, (e, xsss) in enumerate(zip(energies, xss)):
                if energy.energy.position - e > 5:
                    yield from bps.mv(energy, e - 5)
                    yield from bps.sleep(2)
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                else:
                    yield from bps.sleep(2)

                if xbpm2.sumX.get() < 120:
                    yield from bps.sleep(5)
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)

                yield from bps.mv(piezo.x, xsss)
                bpm = xbpm2.sumX.get()

                sample_name = name_fmt.format(
                    sample=name, energy="%6.2f" % e, wax=wa, xbpm="%4.3f" % bpm
                )
                sample_id(user_name="GF", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 2510)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 2490)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 2470)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 2450)
            yield from bps.sleep(2)




def giwaxs_S_edge_2023_3_doblestack(t=1):
    dets = [pil900KW, pil1M]

    names =   ["A1_01","A1_02","A1_03","A1_04","A2_01_par","A2_02_par","A2_03_par"]
    x_piezo = [ -45000, -37000, -18000,   4000,      24000,      41000,      50000]
    x_hexa =  [    -13,      0,      0,      0,          0,          0,         12]
    y_piezo = [   4900,   4900,   4900,   4900,       4900,       4900,       4900]
    z_piezo = [   7000,   7000,   7000,   7000,       7000,       7000,       7000]

    names =   ["A1_02","A1_03","A1_04","A2_01_par","A2_02_par","A2_03_par"]
    x_piezo = [ -37000, -18000,   4000,      24000,      41000,      50000]
    x_hexa =  [      0,      0,      0,          0,          0,         12]
    y_piezo = [   4900,   4900,   4900,       4900,       4900,       4900]
    z_piezo = [   7000,   7000,   7000,       7000,       7000,       7000]


    energies = (
        np.arange(2445, 2470, 5).tolist()
        + np.arange(2470, 2480, 0.25).tolist()
        + np.arange(2480, 2490, 1).tolist()
        + np.arange(2490, 2500, 5).tolist()
        + np.arange(2500, 2560, 10).tolist()
    )
    waxs_arc = [0, 20]
    ai0 = 0

    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexa)})"
    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(z_piezo)})"

    for name, xs_piezo, xs_hexa, ys_piezo, zs_piezo in zip(names, x_piezo, x_hexa, y_piezo, z_piezo):
        yield from bps.mv(piezo.x, xs_piezo)
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.y, ys_piezo)
        yield from bps.mv(piezo.z, zs_piezo)

        yield from bps.mv(piezo.th, ai0)

        yield from alignement_gisaxs_doblestack(angle=0.7)

        ai0 = piezo.th.position
        yield from bps.mv(piezo.th, ai0 + 0.8)
        xss = np.linspace(xs_piezo, xs_piezo - 8000, 63)

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)

            det_exposure_time(t, t)
            name_fmt = "{sample}_{energy}eV_ai0.8_wa{wax}_bpm{xbpm}"
            for k, (e, xsss) in enumerate(zip(energies, xss)):
                yield from bps.mv(energy, e)
                yield from bps.sleep(2)
                if xbpm2.sumX.get() < 50:
                    yield from bps.sleep(2)
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)

                yield from bps.mv(piezo.x, xsss)
                bpm = xbpm2.sumX.get()

                sample_name = name_fmt.format(sample=name, energy="%6.2f" % e, wax=wa, xbpm="%4.3f" % bpm)
                sample_id(user_name="GF", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 2510)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 2490)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 2470)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 2450)
            yield from bps.sleep(2)
        yield from bps.mv(piezo.th, ai0)



def giwaxs_S_edge_2023_3_doblestack_Ruipeng(t=1):
    dets = [pil900KW, pil1M]

    names =   ["P13_P3HT","P16_DoppedP3HT"]
    x_piezo = [    -45000,         -42000]
    x_hexa =  [       -10,               0]
    y_piezo = [     -3600,           -3600]
    z_piezo = [      7000,            7000]

    energies = (
        np.arange(2445, 2470, 5).tolist()
        + np.arange(2470, 2480, 0.25).tolist()
        + np.arange(2480, 2490, 1).tolist()
        + np.arange(2490, 2500, 5).tolist()
        + np.arange(2500, 2560, 10).tolist()
    )
    waxs_arc = [0, 20]
    ai0 = 0

    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexa)})"
    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(z_piezo)})"

    for name, xs_piezo, xs_hexa, ys_piezo, zs_piezo in zip(names, x_piezo, x_hexa, y_piezo, z_piezo):
        yield from bps.mv(piezo.x, xs_piezo)
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.y, ys_piezo)
        yield from bps.mv(piezo.z, zs_piezo)

        yield from bps.mv(piezo.th, ai0)

        yield from alignement_gisaxs_doblestack(angle=0.7)

        ai0 = piezo.th.position
        yield from bps.mv(piezo.th, ai0 + 0.8)
        xss = np.linspace(xs_piezo, xs_piezo - 6000, 63)

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)

            det_exposure_time(t, t)
            name_fmt = "{sample}_{energy}eV_ai0.8_wa{wax}_bpm{xbpm}"
            for k, (e, xsss) in enumerate(zip(energies, xss)):
                yield from bps.mv(energy, e)
                yield from bps.sleep(2)
                if xbpm2.sumX.get() < 50:
                    yield from bps.sleep(2)
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)

                yield from bps.mv(piezo.x, xsss)
                bpm = xbpm2.sumX.get()

                sample_name = name_fmt.format(sample=name, energy="%6.2f" % e, wax=wa, xbpm="%4.3f" % bpm)
                sample_id(user_name="GF", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 2510)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 2490)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 2470)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 2450)
            yield from bps.sleep(2)
        yield from bps.mv(piezo.th, ai0)


def giwaxs_Cl_edge_2023_3_doblestack_Amalie(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    # bottom left first
    names = [     'AA_co_KClO4',    'AA_ht_KClO4',     'AA_mt_KClO4',   'AA_hTe_KClO4', 'AA_mTe_KClO4',   'AA_mB_KClO4',   'AA_hB_KClO4']
    x_piezo = [    -27000,     -14000,         2000,       18000,    31000,      46000,     51000]
    x_hexa = [          0,          0,            0,           0,        0,          0,        10]
    y_piezo = [     -3600,      -3600,        -3600,       -3600,    -3600,      -3600,     -3600]
    z_piezo = [      7000,       7000,         7000,        7000,     7000,       7000,      7000]
    
    x_piezo = 0 + np.asarray(x_piezo)
    
    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples1 ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples2 ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples3 ({len(z_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples4 ({len(x_hexa)})"

    energies1 =   np.asarray([2810.0, 2820.0, 2830.0, 2832.0, 2834.0, 2834.5, 2835.0, 2835.5, 2836.0, 2836.5, 2837.0, 2837.5, 2838.0, 2838.5, 2839.0,
    2839.5, 2840.0, 2840.5, 2841.0, 2841.5, 2845.0, 2850.0, 2855.0, 2860.0, 2865.0, 2870.0, 2875.0, 2880.0, 2890.0])
    
    waxs_arc = [0, 20]
    ai0_all = 0
    ai_list = [0.80]

    for name, xs, ys, zs, xs_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa):       
        ai_list = [0.80]
        energies = energies1

        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)

        yield from bps.mv(piezo.th, ai0_all)
        yield from alignement_gisaxs_doblestack(0.8)

        yield from bps.mv(att2_9.open_cmd, 1)
        yield from bps.sleep(1)
        yield from bps.mv(att2_9.open_cmd, 1)

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
                    yield from bps.mv(piezo.x, xs - counter * 30)
                    counter += 1

                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)

                name_fmt = "{sample}_pos2_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies[::-1]:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs - counter * 30)
                    counter += 1

                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)

            yield from bps.mv(piezo.th, ai0)




def night_Dec4(t=1):
    proposal_id("2023_3", "311000_Freychet_16")
    yield from giwaxs_S_edge_2023_3_doblestack(t=t)
    proposal_id("2023_3", "311000_Freychet_17")
    yield from giwaxs_S_edge_2023_3_doblestack_Ruipeng(t=t)
    
    yield from transition_S_Cl_edges()

    proposal_id("2023_3", "313690_Richter_09")
    yield from giwaxs_Cl_edge_2023_3_doblestack_Amalie(t=t)




def waxs_S_edge_chris_2024_1(t=1):
    dets = [pil900KW, pil1M]

    # names = ["A1_01G","A1_02G","A1_03G","A1_04G","A2_01G","A2_02G","A2_03G", "A1_01", "A1_02", "A1_03",  "A1_04",  "A1_05", "A1_06", "A1_07", "A1_08", 
    #           "A1_09", "A1_10", "A1_11", "D1_02", "D1_03", "D1_05", "D1_06", "D1_07", "D1_08", "Si3N4","PffBT4T"]
    # x = [       42300,   36900,   31700,   25800,   17900,   11900,    5900,   -2700,   -7800,  -13600,   -19000,   -25000,  -30700,  -36200, -471400,
    #             43700,   37800,   32500,   22700,   14700,    6700,     900,   -4500,  -10500,  -19500,   -24800]
    # y = [       -7500,   -7500,   -7400,   -7300,   -7400,   -7400,   -7500,   -7500,   -7500,   -7200,    -7200,    -7100,   -6800,   -6800,   -6900,
    #              5600,    5100,    4800,    5300,    5300,    5400,    5400,    5400,    5400,    5600,     5600] 

    # names = [ "A1_08", "A1_09", "A1_10", "A1_11", "D1_02", "D1_03", "D1_05", "D1_06", "D1_07", "D1_08", "Si3N4","PffBT4T"]
    # x = [      -41400,   43700,   37800,   32500,   22700,   14700,    6700,     900,   -4500,  -10500,  -19500,   -24800]
    # y = [       -6900,    5600,    5100,    4800,    5300,    5300,    5400,    5400,    5400,    5400,    5600,     5600] 

    # names = [ "Si3N4","PffBT4T"]
    # x = [      -19500,   -24800]
    # y = [        5600,     5600] 

    # names = [ "A2_01G_or1", "A2_02G_or1", "A2_03G_or1"]
    # x = [           -19500,   -24800]
    # y = [             5600,     5600] 

    names = [ "W2_01", "W2_02", "W2_03", "W2_04", "W2_05", "W2_06", "W2_07", "W2_08", "W2_09", "W2_10",  "W2_11",  "W2_12", "W2_13", "W2_14", "A1_12b","D1_01", "D1_04", 
              "D1_08", "D1_09", "D1_10", "D1_11", "D1_12"]
    x = [       42200,   37200,   32500,   26200,   21700,   16000,   10300,    4800,     400,   -5100,   -10530,   -15500,  -20500,  -26000,  -30800,  -35700,  -41400,
                42600,   37600,   32100,   27000,   21400]
    y = [       -7500,   -7400,   -7200,   -7200,   -7100,   -6800,   -6800,   -6900,   -6900,   -6900,    -6900,    -6900,   -6900,   -6800,   -6800,   -6800,   -6900,
                 5600,    5700,    5700,    5500,    5700] 

    names = [ "W2_03", "W2_04", "W2_05", "W2_06", "W2_07", "W2_08", "W2_09", "W2_10",  "W2_11",  "W2_12", "W2_13", "W2_14", "A1_12b","D1_01", "D1_04", 
              "D1_08", "D1_09", "D1_10", "D1_11", "D1_12"]
    x = [       32500,   26200,   21700,   16000,   10300,    4800,     400,   -5100,   -10530,   -15500,  -20500,  -26000,  -30800,  -35700,  -41400,
                42600,   37600,   32100,   27000,   21400]
    y = [       -7200,   -7200,   -7100,   -6800,   -6800,   -6900,   -6900,   -6900,    -6900,    -6900,   -6900,   -6800,   -6800,   -6800,   -6900,
                 5600,    5700,    5700,    5500,    5700] 


    names = [ "W2_10",  "W2_12", "W2_14"]
    x = [       -5100,   -15500,  -26000]
    y = [       -6900,    -6900,   -6800] 

    names = ["D1_01", "D1_04"]
    x = [     -35700,  -41400]
    y = [      -6800,   -6900] 

    names = ["D1_01", "D1_04"]
    x = [     -35700,  -41400]
    y = [      -6800,   -6900] 

    names = ["D1_02", "D1_06", "D1_07", "A1_04"]
    x = [      -3200,   -9600,  -15600,  -20800]
    y = [      -3700,   -3800,   -3700,   -3600] 

    assert len(x) == len(y), f"Number of X coordinates ({len(x)}) is different from number of samples ({len(y)})"
    assert len(x) == len(names), f"Number of X coordinates ({len(x)}) is different from number of samples ({len(names)})"

    energies = (np.arange(2445, 2470, 5).tolist()+ np.arange(2470, 2480, 0.25).tolist()+ np.arange(2480, 2490, 1).tolist()
                + np.arange(2490, 2500, 5).tolist()+ np.arange(2500, 2560, 10).tolist())
    
    waxs_arc = [0, 20, 40]
    waxs_arc = [0, 20]

    for name, xs, ys in zip(names, x, y):
        yield from bps.mv(piezo.x, xs,
                          piezo.y, ys)

        yss = np.linspace(ys, ys + 1500, 63)
        xss = np.array([xs-300])

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

            name_fmt = "{sample}_sdd1.8m_{energy}eV_wa{wax}_bpm{xbpm}"
            for e, xsss, ysss in zip(energies, xss, yss):
                yield from bps.mv(energy, e)
                yield from bps.sleep(2)
                if xbpm2.sumX.get() < 50:
                    yield from bps.sleep(2)
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)

                yield from bps.mv(piezo.y, ysss)
                yield from bps.mv(piezo.x, xsss)

                bpm = xbpm3.sumX.get()

                sample_name = name_fmt.format(sample=name, energy="%6.2f" % e, wax=wa, xbpm="%4.3f" % bpm)
                sample_id(user_name="CM", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")

                yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 2500)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 2480)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 2445)




def waxs_S_edge_chris_2024_2(t=1):
    dets = [pil900KW, pil1M]

    names = [ "A2_01G_or1", "A2_02G_or1", "A2_03G_or1"]
    x = [           -20900,       -29100,       -36600]
    y = [            -7400,        -7400,        -7300] 

    names = [ "A2_01G_or2", "A2_02G_or2", "A2_03G_or2"]
    x = [           -21400,       -29400,       -37000]
    y = [            -7100,        -6800,        -6900] 

    assert len(x) == len(y), f"Number of X coordinates ({len(x)}) is different from number of samples ({len(y)})"
    assert len(x) == len(names), f"Number of X coordinates ({len(x)}) is different from number of samples ({len(names)})"

    energies = (np.arange(2445, 2470, 5).tolist()+ np.arange(2470, 2480, 0.25).tolist()+ np.arange(2480, 2490, 1).tolist()
                + np.arange(2490, 2500, 5).tolist()+ np.arange(2500, 2560, 10).tolist())
    waxs_arc = [0, 20]

    for name, xs, ys in zip(names, x, y):
        yield from bps.mv(piezo.x, xs,
                          piezo.y, ys)

        yss = np.linspace(ys, ys + 1500, 63)
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

            name_fmt = "{sample}_sdd1.8m_{energy}eV_wa{wax}_bpm{xbpm}"
            for e, xsss, ysss in zip(energies, xss, yss):
                yield from bps.mv(energy, e)
                yield from bps.sleep(2)
                if xbpm2.sumX.get() < 50:
                    yield from bps.sleep(2)
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)

                yield from bps.mv(piezo.y, ysss)
                yield from bps.mv(piezo.x, xsss)

                bpm = xbpm3.sumX.get()

                sample_name = name_fmt.format(sample=name, energy="%6.2f" % e, wax=wa, xbpm="%4.3f" % bpm)
                sample_id(user_name="CM", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")

                yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 2500)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 2480)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 2445)



def saxs_S_edge_chris_2024_1(t=1):
    dets = [pil900KW, pil1M]

    names = [ "D1_06_10sexpo", "D1_07_10sexpo"]
    x = [         900,   -4500]
    y = [        5400,    5400] 

    assert len(x) == len(y), f"Number of X coordinates ({len(x)}) is different from number of samples ({len(y)})"
    assert len(x) == len(names), f"Number of X coordinates ({len(x)}) is different from number of samples ({len(names)})"

    energies = (np.arange(2445, 2470, 5).tolist()+ np.arange(2470, 2480, 0.25).tolist()+ np.arange(2480, 2490, 1).tolist()
                + np.arange(2490, 2500, 5).tolist()+ np.arange(2500, 2560, 10).tolist())
    waxs_arc = [20, 0]

    for name, xs, ys in zip(names, x, y):
        yield from bps.mv(piezo.x, xs,
                          piezo.y, ys)

        yss = np.linspace(ys, ys + 1500, 63)
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

            name_fmt = "{sample}_sdd1.8m_{energy}eV_wa{wax}_bpm{xbpm}"
            for e, xsss, ysss in zip(energies, xss, yss):
                yield from bps.mv(energy, e)
                yield from bps.sleep(2)
                if xbpm2.sumX.get() < 50:
                    yield from bps.sleep(2)
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)

                yield from bps.mv(piezo.y, ysss)
                yield from bps.mv(piezo.x, xsss)

                bpm = xbpm3.sumX.get()

                sample_name = name_fmt.format(sample=name, energy="%6.2f" % e, wax=wa, xbpm="%4.3f" % bpm)
                sample_id(user_name="CM", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")

                yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 2500)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 2480)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 2445)

def chris_2024_day(t=1):
    yield from waxs_S_edge_chris_2024_2(t=t)

    yield from saxs_S_edge_chris_2024_1(t=10)




def bpmvspindiode_Sedge_2024_1(t=1):
    dets = [pil1M]
    det_exposure_time(t, t)

    name = 'direct_beam_Sedge_scannormal'


    energies = (np.arange(2445, 2470, 5).tolist()+ np.arange(2470, 2480, 0.25).tolist()+ np.arange(2480, 2490, 1).tolist()
                + np.arange(2490, 2500, 5).tolist()+ np.arange(2500, 2560, 10).tolist())
    
    for e in energies:
        yield from bps.mv(energy, e)
        yield from bps.sleep(2)
        if xbpm2.sumX.get() < 50:
            yield from bps.sleep(2)
            yield from bps.mv(energy, e)
            yield from bps.sleep(2)

        fs.open()
        yield from bps.sleep(2)
        bpm2 = xbpm2.sumX.get()
        bpm3 = xbpm3.sumX.get()
        pdc = pdcurrent2.get()
        fs.close()

        name_fmt = "{sample}_{energy}eV_bpm2_{xbpm2}_bpm3_{xbpm3}_pd_{pd}"

        sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, xbpm2="%4.3f"%bpm2, xbpm3="%4.3f"%bpm3, pd="%4.3f"%pdc)
        sample_id(user_name="LR", sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")

        yield from bp.count([pil1M], num=1)

    yield from bps.mv(energy, 2500)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 2480)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 2445)



    
def waxs_S_edge_chris_amptek_2024_1(t=1):
    dets = [pil900KW, pil1M]

    names = ["A1_04_prs40deg"]
    x = [     -23500]
    y = [      -3600] 

    names = ["Si3N4_membrane"]
    x = [     3000]
    y = [    -3400] 

    assert len(x) == len(y), f"Number of X coordinates ({len(x)}) is different from number of samples ({len(y)})"
    assert len(x) == len(names), f"Number of X coordinates ({len(x)}) is different from number of samples ({len(names)})"

    energies = (np.arange(2445, 2470, 5).tolist()+ np.arange(2470, 2480, 0.25).tolist()+ np.arange(2480, 2490, 1).tolist()
                + np.arange(2490, 2500, 5).tolist()+ np.arange(2500, 2560, 10).tolist())
    
    waxs_arc = [20]

    for name, xs, ys in zip(names, x, y):
        yield from bps.mv(piezo.x, xs,
                          piezo.y, ys)

        yss = np.linspace(ys, ys + 0, 63)
        xss = np.array([xs])

        yss, xss = np.meshgrid(yss, xss)
        yss = yss.ravel()
        xss = xss.ravel()

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)
            dets = [pil900KW, amptek]

            det_exposure_time(t, t)

            name_fmt = "{sample}_{energy}eV_wa{wax}_bpm{xbpm}"
            for e, xsss, ysss in zip(energies, xss, yss):
                yield from bps.mv(energy, e)
                yield from bps.sleep(2)
                if xbpm2.sumX.get() < 50:
                    yield from bps.sleep(2)
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)

                yield from bps.mv(piezo.y, ysss)
                yield from bps.mv(piezo.x, xsss)

                bpm = xbpm3.sumX.get()

                sample_name = name_fmt.format(sample=name, energy="%6.2f" % e, wax=wa, xbpm="%4.3f" % bpm)
                sample_id(user_name="CM", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")

                yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 2500)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 2480)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 2445)








def giwaxs_S_edge_2024_3_McNeil(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    # bottom left first
    names = [     ]
    x_piezo = [    -27000,     -14000,         2000,       18000,    31000,      46000,     51000]
    x_hexa = [          0,          0,            0,           0,        0,          0,        10]
    y_piezo = [     -3600,      -3600,        -3600,       -3600,    -3600,      -3600,     -3600]
    z_piezo = [      7000,       7000,         7000,        7000,     7000,       7000,      7000]
    
    x_piezo = 0 + np.asarray(x_piezo)
    
    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples1 ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples2 ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples3 ({len(z_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples4 ({len(x_hexa)})"

    energies = (np.arange(2445, 2470, 5).tolist()+ np.arange(2470, 2480, 0.25).tolist()+ np.arange(2480, 2490, 1).tolist()
                + np.arange(2490, 2500, 5).tolist()+ np.arange(2500, 2560, 10).tolist())
    
    waxs_arc = [0, 20]
    ai_list = [0.80]

    for name, xs, ys, zs, xs_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa):       
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)

        yield from alignement_gisaxs(0.8)

        yield from bps.mv(att2_9.open_cmd, 1)
        yield from bps.sleep(1)
        yield from bps.mv(att2_9.open_cmd, 1)

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

                name_fmt = "{sample}_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs - counter * 30)
                    counter += 1

                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)
                
                yield from bps.mv(energy, 2500)
                yield from bps.sleep(2)
                yield from bps.mv(energy, 2480)
                yield from bps.sleep(2)
                yield from bps.mv(energy, 2445)

            yield from bps.mv(piezo.th, ai0)



def incident_scan_giwaxs_S_edge_2024_3(t=1):
    '''
    Study the beam damage on 1 film to define the opti;am experimental conitions.

    '''
    dets = [pil900KW]
    det_exposure_time(t, t)

    # bottom left first
    name = 'A1_01_test'
    
    energies = 2450
    yield from bps.mv(energy, energies)
    yield from bps.sleep(2)
    yield from bps.mv(energy, energies)
    yield from bps.sleep(2)

    waxs_arc = [0]
    ai_list = (np.arange(0.2, 0.46, 0.02).tolist()+ np.arange(0.46, 0.7, 0.003).tolist()+ np.arange(0.7, 1.0, 0.02).tolist()+ np.arange(1.0, 4.0, 0.1).tolist())    

    ai0 = piezo.th.position

    for i, wa in enumerate(waxs_arc):
        yield from bps.mv(waxs, wa)
        
        for k, ais in enumerate(ai_list):
            yield from bps.mv(piezo.th, ai0 + ais)
            name_fmt = "wideincidentanglescan_{sample}_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"

            bpm = xbpm2.sumX.get()
            sample_name = name_fmt.format(sample=name,energy="%6.2f"%energies, ai="%3.3f"%ais, wax=waxs_arc[0], xbpm="%4.3f"%bpm)
            sample_id(user_name="CM", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)

        yield from bps.mv(piezo.th, ai0)



def beamdamage_giwaxs_S_edge_2024_3(t=1, num=1):
    '''
    Study the beam damage on 1 film to define the opti;am experimental conitions.

    '''
    dets = [pil900KW]
    det_exposure_time(t, t)

    # bottom left first
    name = 'A1_05_bd'
    
    energies = 2477
    yield from bps.mv(energy, energies)
    yield from bps.sleep(2)
    yield from bps.mv(energy, energies)
    yield from bps.sleep(2)

    waxs_arc = [0]
    ai_list = [0.5]   
    ai0 = piezo.th.position

    for i, wa in enumerate(waxs_arc):
        yield from bps.mv(waxs, wa)
        
        for k, ais in enumerate(ai_list):
            yield from bps.mv(piezo.th, ai0 + ais)
            name_fmt = "beamdamage_freshspot_{sample}_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"

            bpm = xbpm2.sumX.get()
            sample_name = name_fmt.format(sample=name,energy="%6.2f"%energies, ai="%3.3f"%ais, wax=waxs_arc[0], xbpm="%4.3f"%bpm)
            sample_id(user_name="CM", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=num)

        yield from bps.mv(piezo.th, ai0)




def fluo_scan_giwaxs_S_edge_2024_3(t=1):
    '''
    Study the beam damage on 1 film to define the opti;am experimental conitions.

    '''
    dets = [pil900KW]
    det_exposure_time(t, t)

    # bottom left first
    name = 'A1_05_bd'    

    energies = (np.arange(2445, 2470, 5).tolist()+ np.arange(2470, 2480, 0.25).tolist()+ np.arange(2480, 2490, 1).tolist()
                + np.arange(2490, 2500, 5).tolist()+ np.arange(2500, 2560, 10).tolist())
    
    waxs_arc = [20]
    ai_list = [1.0]

    ai0 = piezo.th.position

    for i, wa in enumerate(waxs_arc):
        yield from bps.mv(waxs, wa)
        # Do not take SAXS when WAXS detector in the way

        for k, ais in enumerate(ai_list):
            yield from bps.mv(piezo.th, ai0 + ais)

            name_fmt = "fluoscan_{sample}_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
            
            for e in energies:
                yield from bps.mv(energy, e)
                yield from bps.sleep(2)
                if xbpm2.sumX.get() < 50:
                    yield from bps.sleep(2)
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)

                bpm = xbpm2.sumX.get()
                sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                sample_id(user_name="CM", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)
            
            yield from bps.mv(energy, 2500)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 2480)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 2445)

        yield from bps.mv(piezo.th, ai0)




def sevralai_giwaxs_S_edge_2024_3(t=1):
    '''
    Study the beam damage on 1 film to define the opti;am experimental conitions.

    '''
    dets = [pil900KW]

    # bottom left first
    name = 'A1_01_test'    

    energies = (np.arange(2445, 2470, 5).tolist()+ np.arange(2470, 2480, 0.25).tolist()+ np.arange(2480, 2490, 1).tolist()
                + np.arange(2490, 2500, 5).tolist()+ np.arange(2500, 2560, 10).tolist())
    
    waxs_arc = [0, 20]
    ai_list = [0.2, 0.4, 0.6, 0.8, 4, 8]

    ai0 = piezo.th.position
    xs = piezo.x.position

    for i, wa in enumerate(waxs_arc):
        yield from bps.mv(waxs, wa)
        # Do not take SAXS when WAXS detector in the way

        counter = 0
        for k, ais in enumerate(ai_list):
            if ais==0.6:
                det_exposure_time(0.5, 0.5)
            else:
                det_exposure_time(1, 1)

            yield from bps.mv(piezo.th, ai0 + ais)

            name_fmt = "{sample}_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
            
            for e in energies:
                yield from bps.mv(energy, e)
                yield from bps.sleep(2)
                if xbpm2.sumX.get() < 50:
                    yield from bps.sleep(2)
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                
                yield from bps.mv(piezo.x, xs + counter * 10)
                counter += 1
                bpm = xbpm2.sumX.get()
                sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                sample_id(user_name="CM", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)
            
            yield from bps.mv(energy, 2500)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 2480)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 2445)

        yield from bps.mv(piezo.th, ai0)




def aipeak_giwaxs_S_edge_2024_3(t=1):
    '''
    Study the beam damage on 1 film to define the opti;am experimental conitions.

    '''
    dets = [pil900KW]
    det_exposure_time(t, t)

    # bottom left first
    name = 'A1_05_test'    

    energies = (np.arange(2445, 2470, 5).tolist()+ np.arange(2470, 2480, 0.25).tolist()+ np.arange(2480, 2490, 1).tolist()
                + np.arange(2490, 2500, 5).tolist()+ np.arange(2500, 2560, 10).tolist())

    waxs_arc = [20]

    ai0 = piezo.th.position
    xs = piezo.x.position

    ai_lists = []

    # TEMP:
    # energies =  (np.arange(2481, 2490, 1).tolist() + np.arange(2490, 2500, 5).tolist()+ np.arange(2500, 2560, 10).tolist())
    
    ai_lists = ([0.543, 0.54, 0.54, 0.536, 0.533] + [0.529]*6 + [0.526]*8 + [0.522]*3 + [0.519]*3
                 + [0.55, 0.547, .547, .543, .54, .539, .54, .543, .547, .55, .55, .547 ,.54 ,.54, .54, .536, .536 ,.54, .536]
                 + [.533] * 4 + [0.536, 0.533] + [0.536]*2 + [0.529, 0.536, 0.533, 0.532, 0.536, 0.533, 0.532, 0.529, 0.529, 0.525, 0.522])

    yield from bps.mv(att2_9.open_cmd, 1)
    yield from bps.sleep(1)
    yield from bps.mv(att2_9.open_cmd, 1)
    yield from bps.sleep(1)

    for i, wa in enumerate(waxs_arc):
        yield from bps.mv(waxs, wa)
        # Do not take SAXS when WAXS detector in the way
        counter = 0
        yield from bps.mv(piezo.th, ai0)
 
        for k, e in enumerate(energies):
            yield from bps.mv(energy, e)
            yield from bps.sleep(2)
            if xbpm2.sumX.get() < 50:
                yield from bps.sleep(2)
                yield from bps.mv(energy, e)
                yield from bps.sleep(2)
            
            yield from bps.mv(piezo.x, xs + counter * 50)
            counter += 1

            # if i==0:
            #     incident_angle = yield from track_max()
            #     yield from bps.mv(piezo.th, ai0 + incident_angle)
            #     ai_lists += [incident_angle]
            # else:
            incident_angle = ai_lists[k]
            yield from bps.mv(piezo.th, ai0 + incident_angle)

            name_fmt = "aipeak_{sample}_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"

            bpm = xbpm2.sumX.get()
            sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.3f"%incident_angle, wax=wa, xbpm="%4.3f"%bpm)
            sample_id(user_name="CM", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)
            
            yield from bps.mv(piezo.th, ai0)
            
        yield from bps.mv(energy, 2500)
        yield from bps.sleep(2)
        yield from bps.mv(energy, 2480)
        yield from bps.sleep(2)
        yield from bps.mv(energy, 2445)

        yield from bps.mv(piezo.th, ai0)

def track_max():
    yield from bps.mv(waxs, 0)

    ai0=piezo.th.position

    yield from bps.mv(pil900KW.roi1.min_xyz.min_x, 240)
    yield from bps.mv(pil900KW.roi1.size.x, 130)
    yield from bps.mv(pil900KW.roi1.min_xyz.min_y, 707)
    yield from bps.mv(pil900KW.roi1.size.y, 53)

    sample_id(user_name="test", sample_name="test")
    yield from bp.scan([pil900KW], piezo.th, ai0+0.48, ai0+0.55, 21)
    maxi = bec.peaks.max['pil900KW_stats1_total'][0]
    yield from bps.mv(piezo.th, maxi)

    incident_angle = maxi-ai0
    return incident_angle


def incident_energy_scan_giwaxs_S_edge_2024_3(t=1, energies=2450, name="Test"):
    '''
    Study the beam damage on 1 film to define the opti;am experimental conitions.

    '''
    dets = [pil900KW]
    det_exposure_time(t, t)

    # bottom left first
    # name = 'A1_01_test'
    
    yield from bps.mv(energy, energies)
    yield from bps.sleep(2)
    yield from bps.mv(energy, energies)
    yield from bps.sleep(2)

    waxs_arc = [0]
    ai_list = (np.arange(0.2, 0.46, 0.02).tolist()+ np.arange(0.46, 0.7, 0.003).tolist()+ np.arange(0.7, 1.0, 0.02).tolist()+ np.arange(1.0, 4.0, 0.1).tolist())    

    ai0 = piezo.th.position

    for i, wa in enumerate(waxs_arc):
        yield from bps.mv(waxs, wa)
        
        for k, ais in enumerate(ai_list):
            yield from bps.mv(piezo.th, ai0 + ais)
            name_fmt = "wideincidentanglescan_{sample}_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"

            bpm = xbpm2.sumX.get()
            sample_name = name_fmt.format(sample=name,energy="%6.2f"%energies, ai="%3.3f"%ais, wax=waxs_arc[0], xbpm="%4.3f"%bpm)
            sample_id(user_name="CM", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)

        yield from bps.mv(piezo.th, ai0)


def sevralai_giwaxs_S_edge_2024_3_v2(t=1, name="Test", ai_list: list[int] = [], xstep=10, waxs_arc = [0, 20]):
    '''
    Study the beam damage on 1 film to define the opti;am experimental conitions.

    '''
    # dets = [pil900KW]


    # bottom left first
    # name = 'A1_01_test'    

    # 63 energies
    energies = (np.arange(2445, 2470, 5).tolist()+ np.arange(2470, 2480, 0.25).tolist()+ np.arange(2480, 2490, 1).tolist()
                + np.arange(2490, 2500, 5).tolist()+ np.arange(2500, 2560, 10).tolist())
    
    # ai_list = [0.2, 0.4, 0.6, 0.8, 4, 8]

    ai0 = piezo.th.position
    xs = piezo.x.position

    for i, wa in enumerate(waxs_arc):
        yield from bps.mv(waxs, wa)

        if wa ==0:
            dets = [pil900KW]
        else:
            dets = [pil900KW, pil1M]

        # Do not take SAXS when WAXS detector in the way

        counter = 0
        for k, ais in enumerate(ai_list):
            if ais==0.6:
                det_exposure_time(0.5, 0.5)
            else:
                det_exposure_time(1, 1)

            yield from bps.mv(piezo.th, ai0 + ais)

            name_fmt = "{sample}_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
            
            for e in energies:
                yield from bps.mv(energy, e)
                yield from bps.sleep(2)
                if xbpm2.sumX.get() < 50:
                    yield from bps.sleep(2)
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                
                yield from bps.mv(piezo.x, xs + counter * xstep)
                counter += 1
                bpm = xbpm2.sumX.get()
                sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                sample_id(user_name="CM", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)
            
            yield from bps.mv(energy, 2500)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 2480)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 2445)

        yield from bps.mv(piezo.th, ai0)

def sequence_scan_01_P3HT():
    """
    Scans samples of P3HT
    """

    # In McNeil_04
    # samples = ["A1_01_a", "A1_01_b", "A1_02_a", "A1_02_b", "A1_03_a", "A1_03_b", "A1_04_a"]
    # x_pos =     [-54000,-46000, -31000, -14000, -2000,  14000,  33000,  ]
    # x_offset =  [0,     0,      3000,   0,      0,      5000,   2000,   ]
    # x_pos_hex = [-10,   0,      0,      0,      0,      0,      0,      ]

    # In McNeil_05
    # samples = ["A1_01_a", "A1_04_b", "A1_05_a", "A1_05_b", "A1_06_a", "A1_06_b", "A2_06_a", "A2_06_b"]
    # x_pos =   [   -49000,    -44500,    -29200,    -14200,      2800,     17000,     34000,     47000]
    # x_offset = [       0,      3300,         0,         0,         0,         0,         0,         0]
    # x_pos_hex = [    -10,         0,         0,         0,         0,         0,         0,         4]
    
    # In McNeil_06
    samples = ["A2_01_a", "A1_01_b", "A2_01_b", "A1_02_b", "A1_03_a", "A1_03_b", "A1_04_a", "A2_02_a", "A2_02_b"]
    x_pos =   [   -54000,    -49000,    -34000,    -18000,      -500,     14000,     31000,     45500,     46000]
    x_offset = [       0,         0,         0,         0,         0,         0,         0,         0,         0]
    x_pos_hex = [    -10,         0,         0,         0,         0,         0,         0,         0,        15]
    
    # In McNeil_07




    for i, (sample, x) in enumerate(zip(samples, x_pos)):
        # Setup measurement for sample
        det_exposure_time(1, 1)
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(stage.x, x_pos_hex[i])

        # Sample alignment - align at 0.5 because....
        yield from alignement_gisaxs_doblestack(angle=0.3)

        yield from incident_energy_scan_giwaxs_S_edge_2024_3(t=1, energies=2450, name=sample)
        # beam is 200um.
        yield from bps.mv(piezo.x, x + 300)

        # Run sample scan
        if sample.endswith("_a"):
            yield from bps.mv(piezo.x, 0 if x_offset[i] != 0 else x + x_offset[i]) #um
            # 
            yield from sevralai_giwaxs_S_edge_2024_3_v2(
                t=1, name=sample, ai_list = [0.8], xstep=100) # steps 63 energies
        
        else:
            if x_offset[i] == 0:
                yield from sevralai_giwaxs_S_edge_2024_3_v2(
                    t=1, name=sample, ai_list = [0.4, 4, 8], xstep=50)
            else:
                yield from sevralai_giwaxs_S_edge_2024_3_v2(
                    t=1, name=sample, ai_list = [0.4], xstep=50)
                
                yield from bps.mv(piezo.x, x + x_offset[i]) #um

        
def sequence_scan_02(): #_P3HT
    """
    Running multiple samples with various scans
    """

    # In McNeil_07
    # samples = [  "A2_03", "A2_04_a", "A2_04_b", "A2_05_a", "A2_05_b",   "A3_01",   "A3_02",   "A3_03"]
    # x_pos =   [   -54000,    -47000,    -32000,    -16500,         0,     19000,     39000,     41000]
    # x_offset = [       0,         0,         0,         0,         0,         0,         0,         0]
    # x_pos_hex = [    -11,         0,         0,         0,         0,         0,         0,        17]
    # samples = [  "A2_03_redo",   "A3_02_redo",   "A3_03_redo"]
    # x_pos =   [   -50000,     43000,     47000]
    # x_offset = [       0,         0,         0]
    # x_pos_hex = [    -11,         0,        15]

    # In McNeil_10
    # samples = [  "A5_02", "A5_02_a", "A5_04", "A5_05", "A5_07", "A5_07_a", "A5_09", "A5_10", "A4_05"]
    # x_pos =   [   -54000,    -50000,  -36000,  -21000,   -6000,     11000,   26000,   43000,   44000]
    # x_offset = [       0,         0,       0,       0,       0,         0,       0,       0,       0]
    # x_pos_hex = [    -11,         0,       0,       0,       0,         0,       0,       0,      15]
    
    # In McNeil_14
    # Maximum x movement per sample is 300um + 63*50*3 = 9.75mm
    # samples = [  "A6_01",   "A6_02", "A6_03", "A6_04", "A6_05",   "A6_06", "A4_12", "A4_05"]
    # x_pos =   [   -54000,    -47000,  -31000,  -13000,    2000,     18500,   38000,   43000]
    # x_offset = [       0,         0,       0,       0,       0,         0,       0,       0]
    # x_pos_hex = [    -11,         0,       0,       0,       0,         0,       0,      12]
    
    # In McNeil_15
    # Maximum x movement per sample is 300um + 63*50*3 = 9.75mm
    # samples = [  "Y1_01",   "Y1_02", "Y1_03", "Y1_04", "Y1_05",   "Y1_06", "Y1_07", "Y1_08", "A1_09p", "A2_05",  "Si"]
    # x_pos =   [   -54000,    -51000,  -40000,  -29000,  -19000,     -7000,    3000,   15000,    26000,   38000, 50000]
    # x_step = [        30,        30,      30,      30,      30,        25,      20,      10,       35,      50,     0]
    # x_offset = [       0,         0,       0,       0,       0,         0,       0,       0,        0,       0,     0]
    # x_pos_hex = [    -15,         0,       0,       0,       0,         0,       0,       0,        0,       0,     9]

    # In McNeil_18
    # samples = [  "A1_04", "A2_03", "A4_02", "A4_03", "A4_04", "A4_06", "A4_07", "A4_08", "A5_06"]
    # x_pos =   [   -53000,  -52000,  -37000,  -22000,   -5000,   11000,   28000,   43000,   46000]
    # x_step = [        30,      30,      30,      30,      30,      30,      30,      30,      30]
    # x_offset = [       0,       0,       0,       0,       0,       0,       0,       0,       0]
    # x_pos_hex = [    -14,       0,       0,       0,       0,       0,       0,       0,      14]

    samples = [  "A2_03", "A4_02", "A4_03", "A4_04", "A4_06", "A4_07", "A4_08", "A5_06"]
    x_pos =   [   -52000,  -37000,  -22000,   -5000,   11000,   28000,   43000,   46000]
    x_step = [        30,      30,      30,      30,      30,      30,      30,      30]
    x_offset = [       0,       0,       0,       0,       0,       0,       0,       0]
    x_pos_hex = [      0,       0,       0,       0,       0,       0,       0,      14]



    for i, (sample, x, xstep, xhex) in enumerate(zip(samples, x_pos, x_step, x_pos_hex)):
        # Setup measurement for sample
        det_exposure_time(1, 1)
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(stage.x, xhex)

        # Sample alignment - align at 0.5 because....
        yield from alignement_gisaxs_doblestack(angle=0.3)

        yield from incident_energy_scan_giwaxs_S_edge_2024_3(t=1, energies=2450, name=sample)
        # beam is 200um.
        yield from bps.mv(piezo.x, x + 300)

        # Run sample scan
        # if sample.endswith("_a") or sample.endswith("_b"):
        #     if sample.endswith("_a"):
        #         yield from bps.mv(piezo.x, 0 if x_offset[i] != 0 else x + x_offset[i]) #um
        #         # 
        #         yield from sevralai_giwaxs_S_edge_2024_3_v2(
        #             t=1, name=sample, ai_list = [0.8], xstep=100) # steps 63 energies
            
        #     else:
        #         if x_offset[i] == 0:
        #             yield from sevralai_giwaxs_S_edge_2024_3_v2(
        #                 t=1, name=sample, ai_list = [0.4, 4, 8], xstep=50)
        #         else:
        #             yield from sevralai_giwaxs_S_edge_2024_3_v2(
        #                 t=1, name=sample, ai_list = [0.4], xstep=50)
                    
        #             yield from bps.mv(piezo.x, x + x_offset[i]) #um
        # else:
        yield from sevralai_giwaxs_S_edge_2024_3_v2(
                    t=1, name=sample, ai_list = [0.4, 0.8, 8], xstep=xstep) # steps 63 energies





def vert_giwaxs_S_edge_2024_3(t=1, name="Test", ai_list: list[int] = [], ystep=10, waxs_arc=[18]):
    '''
    Study the beam damage on 1 film to define the opti;am experimental conitions.

    '''
    dets = [pil900KW]


    # bottom left first
    # name = 'A1_01_test'    

    # 63 energies
    energies = (np.arange(2445, 2470, 5).tolist()+ np.arange(2470, 2480, 0.25).tolist()+ np.arange(2480, 2490, 1).tolist()
                + np.arange(2490, 2500, 5).tolist()+ np.arange(2500, 2560, 10).tolist())
    
    # waxs_arc = [18]

    ai0 = prs.position
    ys = piezo.y.position

    det_exposure_time(1, 1)

    for i, wa in enumerate(waxs_arc):
        yield from bps.mv(waxs, wa)

        counter = 0
        for k, ais in enumerate(ai_list):

            yield from bps.mv(prs, ai0 - ais)

            name_fmt = "{sample}_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
            
            for e in energies:
                yield from bps.mv(energy, e)
                yield from bps.sleep(2)
                if xbpm2.sumX.get() < 50:
                    yield from bps.sleep(2)
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                
                yield from bps.mv(piezo.y, ys - counter * ystep)
                counter += 1
                bpm = xbpm2.sumX.get()
                sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                sample_id(user_name="CM", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)
            
            yield from bps.mv(energy, 2500)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 2480)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 2445)

        yield from bps.mv(prs, ai0)



def vert_aiscan_giwaxs_S_edge_2024_3(t=1, energies=2450, name="Test", waxs_arc=[18]):
    '''
    Study the beam damage on 1 film to define the opti;am experimental conitions.

    '''
    dets = [pil900KW]
    det_exposure_time(t, t)
    
    yield from bps.mv(energy, energies)
    yield from bps.sleep(2)
    yield from bps.mv(energy, energies)
    yield from bps.sleep(2)

    # waxs_arc = [18]
    ai_list = (np.arange(0.2, 0.46, 0.02).tolist()+ np.arange(0.46, 0.7, 0.003).tolist()+ np.arange(0.7, 1.0, 0.02).tolist()+ np.arange(1.0, 4.0, 0.1).tolist())    

    ai0 = prs.position

    for i, wa in enumerate(waxs_arc):
        yield from bps.mv(waxs, wa)
        
        for k, ais in enumerate(ai_list):
            yield from bps.mv(prs, ai0 - ais)
            name_fmt = "wideincidentanglescan_{sample}_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"

            bpm = xbpm2.sumX.get()
            sample_name = name_fmt.format(sample=name,energy="%6.2f"%energies, ai="%3.3f"%ais, wax=waxs_arc[0], xbpm="%4.3f"%bpm)
            sample_id(user_name="CM", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)
            yield from bps.sleep(1)


        yield from bps.mv(prs, ai0)





def vert_sequence_scan_01():
    """
    Running multiple samples with various scans
    """

    # In McNeil_11
    # samples = ["A1_02p", "A1_03p", "A1_04p", "A1_05p", "A2_01p", "A2_02p", "A2_03p", "A2_04p", "A2_05p", "A2_06p", "A3_04p", "A3_06p"]
    # ys =   [      -4000,     5000,    -4000,     5000,    -4000,     5000,    -4000,     5000,    -4000,     5000,    -4000,     5000]
    # xs =   [     -48600,   -48600,   -34000,   -34000,   -10100,   -10100,    16400,    16400,    42000,    42000,    55000,    55000]
    # xshexa =   [    -10,      -10,        0,        0,        0,        0,        0,        0,        0,        0,       13,       13]
    # Crash during night, repeat after first 3.

    samples = ["A1_04p", "A2_01p", "A2_02p", "A2_03p", "A2_04p", "A2_05p", "A2_06p", "A3_04p", "A3_06p"]
    ys =   [      -4000,    -5000,     5000,    -5000,     5000,    -5000,     5000,    -5000,     5000]
    xs =   [     -34000,   -10100,   -10100,    16400,    16400,    42000,    42000,    55000,    55000]
    xshexa =   [      0,        0,        0,        0,        0,        0,        0,       13,       13]
    
    samples = ["A2_02p", "A2_03p", "A2_04p", "A2_05p", "A2_06p", "A3_04p", "A3_06p"]
    ys =   [       5000,    -5000,     5000,    -5000,     5000,    -5000,     5000]
    xs =   [     -10100,    16400,    16400,    42000,    42000,    55000,    55000]
    xshexa =   [      0,        0,        0,        0,        0,       13,       13]



    det_exposure_time(1, 1)


    for i, (sample, y, x, xhexa) in enumerate(zip(samples, ys, xs, xshexa)):
        # Setup measurement for sample
        yield from bps.mv(piezo.y, y)
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(stage.x, xhexa)

        if sample == "A1_04p" or 'A3' in sample:
            wa = [18]
        else:
            wa = [21]
        yield from bps.mv(GV7.open_cmd, 1)
        yield from bps.sleep(1)
        yield from bps.mv(GV7.open_cmd, 1)
        yield from bps.sleep(1)

        yield from alignement_xrr_xmotor(angle=0.1)

        yield from bps.mv(GV7.close_cmd, 1)
        yield from bps.sleep(1)
        yield from bps.mv(GV7.close_cmd, 1)
        yield from bps.sleep(1)



        yield from vert_aiscan_giwaxs_S_edge_2024_3(t=1, energies=2450, name=sample, waxs_arc=wa)
        # beam is 30um.
        yield from bps.mv(piezo.y, y - 30)

        # Run sample scan
        yield from vert_giwaxs_S_edge_2024_3(
            t=1, name=sample, ai_list = [0.4, 0.8, 8], ystep=20, waxs_arc=wa) # steps 63 energies
            




def bpmvspindiode_Chris_Sedge_2024_3(t=1):
    dets = [pil1M]
    det_exposure_time(t, t)

    # name = 'direct_beam_Sedge'
    name = 'direct_beam_Sedge_withatt1x9umAl'
    
    yield from bps.mv(att2_9.open_cmd, 1)
    yield from bps.sleep(1)
    yield from bps.mv(att2_9.open_cmd, 1)
    yield from bps.sleep(1)

    energies = (np.arange(2445, 2470, 5).tolist()+ np.arange(2470, 2480, 0.25).tolist()+ np.arange(2480, 2490, 1).tolist()
                + np.arange(2490, 2500, 5).tolist()+ np.arange(2500, 2560, 10).tolist())
    
    for e in energies:
        yield from bps.mv(energy, e)
        yield from bps.sleep(2)
        if xbpm2.sumX.get() < 50:
            yield from bps.sleep(2)
            yield from bps.mv(energy, e)
            yield from bps.sleep(2)

        fs.open()
        yield from bps.sleep(2)
        bpm2 = xbpm2.sumX.get()
        bpm3 = xbpm3.sumX.get()
        pdc = pdcurrent2.get()
        fs.close()

        name_fmt = "{sample}_{energy}eV_bpm2_{xbpm2}_bpm3_{xbpm3}_pd_{pd}"

        sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, xbpm2="%4.3f"%bpm2, xbpm3="%4.3f"%bpm3, pd="%4.3f"%pdc)
        sample_id(user_name="CM", sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")

        yield from bp.count([pil1M], num=1)

    yield from bps.mv(energy, 2500)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 2480)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 2445)





    
def waxs_S_edge_chris_2024_3(t=1):
    dets = [pil900KW, pil1M]

    names = ["Y2_01", "Y2_03", "Y2_05", "Y2_06", "Y2_07"]
    x = [      40000,   33500,   25500,   19500,   13900]
    y = [      -7700,   -7700,   -7700,   -7700,   -7900] 

    assert len(x) == len(y), f"Number of X coordinates ({len(x)}) is different from number of samples ({len(y)})"
    assert len(x) == len(names), f"Number of X coordinates ({len(x)}) is different from number of samples ({len(names)})"

    energies = (np.arange(2445, 2470, 5).tolist()+ np.arange(2470, 2480, 0.25).tolist()+ np.arange(2480, 2490, 1).tolist()
                + np.arange(2490, 2500, 5).tolist()+ np.arange(2500, 2560, 10).tolist())
    
    waxs_arc = [0, 20]

    for name, xs, ys in zip(names, x, y):
        yield from bps.mv(piezo.x, xs,
                          piezo.y, ys)

        yss = np.linspace(ys, ys + 1000, len(energies))
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

            name_fmt = "{sample}_{energy}eV_wa{wax}_bpm{xbpm}"
            for e, xsss, ysss in zip(energies, xss, yss):
                yield from bps.mv(energy, e)
                yield from bps.sleep(2)
                if xbpm2.sumX.get() < 50:
                    yield from bps.sleep(2)
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)

                yield from bps.mv(piezo.y, ysss)
                yield from bps.mv(piezo.x, xsss)

                bpm = xbpm3.sumX.get()

                sample_name = name_fmt.format(sample=name, energy="%6.2f" % e, wax=wa, xbpm="%4.3f" % bpm)
                sample_id(user_name="CM", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")

                yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 2500)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 2480)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 2445)





def giwaxs_hardxray_Chris_2024_3(t=1):

    # In McNeill_19
    # names = ['Q1_01', 'Q1_02', 'Q1_03', 'Q1_04', 'Q1_05', 'Q1_06', 'Q1_07', 'Q1_08', 'Q2_01', 'Q2_02', 'Q2_03',
    #          'Q2_04', 'Q2_05', 'Q2_06', 'Q2_07', 'Q2_08', 'Q3_01', 'Q3_02', 'Q3_03', 'Q3_04', 'Q3_05', 'Q3_06']
    # x_piezo = [52000,   52000,   38000,   27000,   14000,    5000,  -11000,  -25000,  -38000,  -50000,  -50000,  
    #            52000,   54000,   42000,   30000,   18000,    2000,   -8000,  -20000,  -33000,  -46000,  -50000]
    # x_hexa = [    14,       0,       0,       0,       0,       0,       0,       0,       0,       0,     -12,
    #               14,       0,       0,       0,       0,       0,       0,       0,       0,       0,     -10]
    # y_piezo = [ 7000,    7000,    7000,    7000,    7000,    7000,    7000,    7000,    7000,    7000,    7000,
    #            -1500,   -1500,   -1500,   -1500,   -1500,   -1500,   -1500,   -1500,   -1500,   -1500,   -1500]

    names = ['Q3_07', 'Q3_08', 'Q3_09']
    x_piezo = [46000,   32000,  -15000]
    x_hexa = [     0,       0,       0]
    y_piezo = [ 7000,    7000,    7000]


    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexa)})"

    waxs_arc = [7, 20]
    ai0 = 0
    ai_list = [0.06, 0.08, 0.09, 0.10, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.20]


    for name, xs, ys, xs_hexa in zip(names, x_piezo, y_piezo, x_hexa):
        yield from bps.mv(stage.x, xs_hexa,
                          piezo.x, xs,
                          piezo.y, ys)

        yield from bps.mv(piezo.th, ai0)
        yield from alignement_gisaxs_doblestack(angle=0.12)

        ai0 = piezo.th.position
        det_exposure_time(t, t)

        for k, ais in enumerate(ai_list):
            yield from bps.mv(piezo.th, ai0 + ais)

            for i, wa in enumerate(waxs_arc):
                yield from bps.mv(waxs, wa)
                # Do not take SAXS when WAXS detector in the way
                dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]

                name_fmt = "{sample}_{energy}eV_ai{ai}_wa{wax}_sdd1.8m"
                e=energy.energy.position
                sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa)
                sample_id(user_name="CM", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

        yield from bps.mv(piezo.th, ai0)



def vert_sequence_scan_01():
    """
    Running multiple samples with various scans
    """

    # In McNeil_11
    # samples = ["A1_02p", "A1_03p", "A1_04p", "A1_05p", "A2_01p", "A2_02p", "A2_03p", "A2_04p", "A2_05p", "A2_06p", "A3_04p", "A3_06p"]
    # ys =   [      -4000,     5000,    -4000,     5000,    -4000,     5000,    -4000,     5000,    -4000,     5000,    -4000,     5000]
    # xs =   [     -48600,   -48600,   -34000,   -34000,   -10100,   -10100,    16400,    16400,    42000,    42000,    55000,    55000]
    # xshexa =   [    -10,      -10,        0,        0,        0,        0,        0,        0,        0,        0,       13,       13]
    # Crash during night, repeat after first 3.

    samples = ["A1_04p", "A2_01p", "A2_02p", "A2_03p", "A2_04p", "A2_05p", "A2_06p", "A3_04p", "A3_06p"]
    ys =   [      -4000,    -5000,     5000,    -5000,     5000,    -5000,     5000,    -5000,     5000]
    xs =   [     -34000,   -10100,   -10100,    16400,    16400,    42000,    42000,    55000,    55000]
    xshexa =   [      0,        0,        0,        0,        0,        0,        0,       13,       13]
    
    samples = ["A2_02p", "A2_03p", "A2_04p", "A2_05p", "A2_06p", "A3_04p", "A3_06p"]
    ys =   [       5000,    -5000,     5000,    -5000,     5000,    -5000,     5000]
    xs =   [     -10100,    16400,    16400,    42000,    42000,    55000,    55000]
    xshexa =   [      0,        0,        0,        0,        0,       13,       13]

    det_exposure_time(1, 1)

    for i, (sample, y, x, xhexa) in enumerate(zip(samples, ys, xs, xshexa)):
        # Setup measurement for sample
        yield from bps.mv(piezo.y, y)
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(stage.x, xhexa)

        if sample == "A1_04p" or 'A3' in sample:
            wa = [18]
        else:
            wa = [21]
        yield from bps.mv(GV7.open_cmd, 1)
        yield from bps.sleep(1)
        yield from bps.mv(GV7.open_cmd, 1)
        yield from bps.sleep(1)

        yield from alignement_xrr_xmotor(angle=0.1)

        yield from bps.mv(GV7.close_cmd, 1)
        yield from bps.sleep(1)
        yield from bps.mv(GV7.close_cmd, 1)
        yield from bps.sleep(1)

        yield from calibrate_ai(t=1, energies=2450, name=sample)

        yield from vert_aiscan_giwaxs_S_edge_2024_3(t=1, energies=2450, name=sample, waxs_arc=wa)
        # beam is 30um.
        yield from bps.mv(piezo.y, y - 30)

        # Run sample scan
        yield from vert_giwaxs_S_edge_2024_3(
            t=1, name=sample, ai_list = [0.4, 0.8, 8], ystep=20, waxs_arc=wa) # steps 63 energies
            



def calibrate_ai_ver(t=1, energies=2450, name="Test"):
    '''
    Take a direct and reflected beam to ensure that the sample alignemenbt was correct, i.e. ai accurate

    '''
    dets = [pil900KW]
    det_exposure_time(t, t)
    
    yield from bps.mv(energy, energies)
    yield from bps.sleep(2)

    yield from bps.mv(att2_10.open_cmd, 1)
    yield from bps.sleep(1)
    yield from bps.mv(att2_10.open_cmd, 1)
    yield from bps.sleep(1)

    ai0 = prs.position
    yield from bps.mv(prs, ai0 - 1.5)

    yield from bps.mv(waxs, 0)
    yield from bps.mv(waxs.bs_x, -87.48)

    name_fmt = "calibrationai_{sample}_{energy}eV_ai{ai}_wa{wax}"
    sample_name = name_fmt.format(sample=name,energy="%6.2f"%energies, ai="%3.3f"%1.5, wax=0)
    sample_id(user_name="CM", sample_name=sample_name)
    print(f"\n\t=== Sample: {sample_name} ===\n")
    yield from bp.count(dets, num=1)

    yield from bps.mv(waxs, 0)

    yield from bps.mv(att2_10.close_cmd, 1)
    yield from bps.sleep(1)
    yield from bps.mv(att2_10.close_cmd, 1)
    yield from bps.sleep(1)

    yield from bps.mv(prs, ai0)




def calibrate_ai_hor(t=1, energies=2450, name="Test"):
    '''
    Take a direct and reflected beam to ensure that the sample alignemenbt was correct, i.e. ai accurate

    '''
    dets = [pil900KW]
    det_exposure_time(t, t)
    
    yield from bps.mv(energy, energies)
    yield from bps.sleep(2)

    yield from bps.mv(att2_10.open_cmd, 1)
    yield from bps.sleep(1)
    yield from bps.mv(att2_10.open_cmd, 1)
    yield from bps.sleep(1)

    ai0 = piezo.th.position
    yield from bps.mv(piezo.th, ai0 + 1.5)

    yield from bps.mv(waxs, 0)
    yield from bps.mv(waxs.bs_x, -87.48)

    name_fmt = "calibrationai_{sample}_{energy}eV_ai{ai}_wa{wax}"
    sample_name = name_fmt.format(sample=name,energy="%6.2f"%energies, ai="%3.3f"%1.5, wax=0)
    sample_id(user_name="CM", sample_name=sample_name)
    print(f"\n\t=== Sample: {sample_name} ===\n")
    yield from bp.count(dets, num=1)

    yield from bps.mv(waxs, 0)

    yield from bps.mv(att2_10.close_cmd, 1)
    yield from bps.sleep(1)
    yield from bps.mv(att2_10.close_cmd, 1)
    yield from bps.sleep(1)

    yield from bps.mv(piezo.th, ai0)




def fixedposition_energysweep_ver(t=1, name="Test", ai_list: list[int] = [], waxs_arc=[18]):
    '''
    Study the beam damage on 1 film to define the opti;am experimental conitions.

    '''
    dets = [pil900KW]

    energies = [2450, 2465, 2475, 2485, 2510, 2540, 2477.5]
    
    ai0 = prs.position
    ys = piezo.y.position

    det_exposure_time(1, 1)

    for i, wa in enumerate(waxs_arc):
        yield from bps.mv(waxs, wa)

        for k, ais in enumerate(ai_list):
            yield from bps.mv(piezo.y, ys - k * 20)

            yield from bps.mv(prs, ai0 - ais)
            name_fmt = "fixedpossweep_{sample}_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
            
            for e in energies:
                yield from bps.mv(energy, e)
                yield from bps.sleep(5)
                if xbpm2.sumX.get() < 50:
                    yield from bps.sleep(2)
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                
                bpm = xbpm2.sumX.get()
                sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                sample_id(user_name="CM", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)
            
            yield from bps.mv(energy, 2445)
            yield from bps.sleep(2)

        yield from bps.mv(prs, ai0)




def fixedposition_energysweep_hor(t=1, name="Test", ai_list: list[int] = [], waxs_arc=[18]):
    '''
    Study the beam damage on 1 film to define the opti;am experimental conitions.

    '''
    dets = [pil900KW]

    energies = [2450, 2465, 2475, 2485, 2510, 2540, 2477.5]
    
    ai0 = piezo.th.position
    xs = piezo.x.position

    det_exposure_time(1, 1)

    for i, wa in enumerate(waxs_arc):
        yield from bps.mv(waxs, wa)

        for k, ais in enumerate(ai_list):
            yield from bps.mv(piezo.x, xs + k * 100)

            yield from bps.mv(piezo.th, ai0 + ais)
            name_fmt = "fixedpossweep_{sample}_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
            
            for e in energies:
                yield from bps.mv(energy, e)
                yield from bps.sleep(5)
                if xbpm2.sumX.get() < 50:
                    yield from bps.sleep(2)
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                
                bpm = xbpm2.sumX.get()
                sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                sample_id(user_name="CM", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)
            
            yield from bps.mv(energy, 2445)
            yield from bps.sleep(2)

        yield from bps.mv(piezo.th, ai0)


def vert_sequence_scan_25_01_Si():
    """
    Measuring vertical Si wafer for reference, i.e. flux variation across the S-edge
    """

    # In McNeil_01
    samples = ["clean_Si_rerun"]
    ys =   [  -5000]
    xs =   [ -53026]
    xshexa =   [ -8]

    det_exposure_time(1, 1)

    for i, (sample, y, x, xhexa) in enumerate(zip(samples, ys, xs, xshexa)):
        wa = [18]
        # Setup measurement for sample
        yield from bps.mv(piezo.y, y)
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(stage.x, xhexa)

        yield from bps.mv(GV7.open_cmd, 1)
        yield from bps.sleep(1)
        yield from bps.mv(GV7.open_cmd, 1)
        yield from bps.sleep(1)

        yield from alignement_xrr_xmotor(angle=0.1)

        yield from bps.mv(GV7.close_cmd, 1)
        yield from bps.sleep(1)
        yield from bps.mv(GV7.close_cmd, 1)
        yield from bps.sleep(1)

        yield from calibrate_ai_ver(t=1, energies=2450, name=sample)

        # beam is 30um.
        yield from bps.mv(piezo.y, y - 30)

        # # Run sample scan
        # yield from vert_giwaxs_S_edge_2024_3(
        #     t=1, name=sample, ai_list = [0.4, 0.8, 4, 8], ystep=0, waxs_arc=wa) # steps 63 energies
            
         # Run sample scan
        yield from vert_giwaxs_S_edge_2024_3(
            t=1, name=sample, ai_list = [0.4], ystep=0, waxs_arc=wa) # steps 63 energies


def vert_sequence_scan_25_01():
    """
    Measuring samples mounted vertically:
    - Alignement in the vertical orientation
    - Take a direct and reflected beam at ai = 3 deg to verify the alignement precision
    - Take few energies without translation for an energy variation reference (no sample inhomogemetiy)
    - Scan the incident angle at 2450 eV
    - Fine energy scan at 0.4, 0.8, 4 and 8 deg incident angles
    """

    # In McNeil_03
    # samples = ["A1_01", "A1_02", "A1_03", "A1_04", "A1_05", "A1_06"]
    # ys =   [     -2500,   -2500,   -2500,   -2500,  -1000,    -4000]
    # xs =   [    -35300,  -11326,   15300,   40300,  52000,    52000]
    # xshexa =   [     0,       0,       0,       0,     14,       14]
    # yshexa =   [    -5,       0,       0,       0,      4,     -6.5]


    # In McNeil_04
    # samples = ["A2_01p", "A2_04p", "A2_06p", "A4_06p", "A4_13p", "A5_06p",
    #            "A2_02p", "A2_03p", "A2_05p", "A4_01p", "A4_08p", "A5_01p"]
    # ys =   [      -3000,    -3000,    -3000,    -3000,    -3000,    -3000,
    #               -2000,    -2000,    -2000,    -2000,    -2000,     5500]
    # xs =   [     -53000,   -35000,   -11326,    15300,    40300,    52000,
    #              -53000,   -35000,   -11326,    15300,    40300,    52000]
    # xshexa =   [     -8,        0,        0,        0,        0,       14,
    #                  -8,        0,        0,        0,        0,       14]
    # yshexa =   [     -3,     -5.5,       -4,       -6,       -4,        3,
    #                   4,        4,        4,        2,        4,        4]


    # # In McNeil_09
    # samples = ["S1_01p_b", "S1_02p_b", "A1_01p", "A1_06p", "A2_06p", "A4_05p",
    #            "S1_01p_a", "S1_02p_a", "S1_03p", "A1_02p", "A2_01p", "A4_04p"]
    # ys =   [      -3000,    -3000,    -3000,    -3000,    -3000,    -3000,
    #                   0,    -1000,    -1000,        0,     1000,     3000]
    # xs =   [     -53000,   -35000,   -11326,    15300,    40300,    52000,
    #              -53000,   -35000,   -11326,    15300,    40300,    52000]
    # xshexa =   [     -8,        0,        0,        0,        0,       14,
    #                  -8,        0,        0,        0,        0,       14]
    # yshexa =   [     -3,       -3,       -3,       -3,       -2,       -1,
    #                   4,        6,        6,        6,      6.5,        4]



    # In McNeil_11
    samples = ["Y1_01p", "Y1_01rp", "Y1_03p", "Y1_03rp", "Y1_02p", "Y1_02rp",
               "A4_04p", "A4_03p", "A3_12p", "Q1_01p", "Q1_02p", "Q1_03p"]
    ys =   [      -3000,    -3000,    -3000,    -3000,    -3000,    -4000,
                   2000,     2000,     2000,     2000,     2000,     3000]
    xs =   [     -53000,   -35000,   -11326,    15300,    40300,    52000,
                 -53000,   -35000,   -11326,    15300,    40300,    52000]
    xshexa =   [     -8,        0,        0,        0,        0,       14,
                     -8,        0,        0,        0,        0,       14]
    yshexa =   [     -1,       -1,       -3,       -3,       -3,       -4,
                      4,        5,        4,        4,        4,        4]


    assert len(samples) == len(ys), f"Number of X coordinates ({len(samples)}) is different from number of samples ({len(y)})"
    assert len(samples) == len(xs), f"Number of X coordinates ({len(samples)}) is different from number of samples ({len(names)})"
    assert len(samples) == len(xshexa), f"Number of X coordinates ({len(samples)}) is different from number of samples ({len(names)})"
    assert len(samples) == len(yshexa), f"Number of X coordinates ({len(samples)}) is different from number of samples ({len(names)})"


    det_exposure_time(1, 1)

    for i, (sample, y, x, xhexa, yhexa) in enumerate(zip(samples, ys, xs, xshexa, yshexa)):
        if 'A4' in sample or 'Q1' in sample:
            wa = [18]
        elif 'Y1' in sample or 'A3' in sample:
            wa = [20]

        if sample!='Y1_01p':
            # Setup measurement for sample
            yield from bps.mv(piezo.y, y)
            yield from bps.mv(piezo.x, x)
            yield from bps.mv(stage.x, xhexa)
            yield from bps.mv(stage.y, yhexa)

            yield from bps.mv(GV7.open_cmd, 1)
            yield from bps.sleep(1)
            yield from bps.mv(GV7.open_cmd, 1)
            yield from bps.sleep(1)

            yield from alignement_xrr_xmotor(angle=0.1)

            yield from bps.mv(GV7.close_cmd, 1)
            yield from bps.sleep(1)
            yield from bps.mv(GV7.close_cmd, 1)
            yield from bps.sleep(1)

            # beam is 30um.
            yield from calibrate_ai_ver(t=1, energies=2450, name=sample)

            # beam is 30um.
            yield from bps.mv(piezo.y, y - 30)

        # beam is 30um.
        yield from fixedposition_energysweep_ver(t=1, name=sample, ai_list=[0.4, 0.8, 4, 8], waxs_arc=wa)

        # beam is 30um.
        yield from bps.mv(piezo.y, y - 30)

        yield from vert_aiscan_giwaxs_S_edge_2024_3(t=1, energies=2450, name=sample, waxs_arc=wa)
        
        # beam is 30um.
        yield from bps.mv(piezo.y, y - 30)

        # Run sample scan
        yield from vert_giwaxs_S_edge_2024_3(
            t=1, name=sample, ai_list = [0.4, 0.8, 4, 8], ystep=20, waxs_arc=wa) # steps 63 energies
            





def hor_sequence_scan_25_01_Si():
    """
    Measuring vertical Si wafer for reference, i.e. flux variation across the S-edge
    """

    # In McNeil_01
    samples = ["Si_redo"]
    ys =      [0]
    xs =   [ -46000]
    xshexa =   [ -7]

    det_exposure_time(1, 1)

    for i, (sample, y, x, xhexa) in enumerate(zip(samples, ys, xs, xshexa)):
        # Setup measurement for sample
        yield from bps.mv(piezo.y, y)
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(stage.x, xhexa)

        yield from bps.mv(GV7.open_cmd, 1)
        yield from bps.sleep(1)
        yield from bps.mv(GV7.open_cmd, 1)
        yield from bps.sleep(1)

        yield from alignement_gisaxs(angle=0.1)

        yield from bps.mv(GV7.close_cmd, 1)
        yield from bps.sleep(1)
        yield from bps.mv(GV7.close_cmd, 1)
        yield from bps.sleep(1)

        yield from calibrate_ai_hor(t=1, energies=2450, name=sample)

        # beam is 30um.
        # yield from bps.mv(piezo.y, y)

        # # Run sample scan
        # yield from vert_giwaxs_S_edge_2024_3(
        #     t=1, name=sample, ai_list = [0.4, 0.8, 4, 8], ystep=0, waxs_arc=wa) # steps 63 energies
            
         # Run sample scan
        yield from sevralai_giwaxs_S_edge_2024_3_v2(
            t=1, name=sample, ai_list = [8.0], xstep=0, waxs_arc=[0]) # steps 63 energies


def hor_sequence_scan_25_01(): #_P3HT
    """
    Running multiple samples with various scans
    """


    # wa = [0, 20]
    # samples = [  "Y1_01", "Y1_01R", "Y1_02", "Y1_02R", "Y1_03", "Y1_03R"]
    # x_pos =   [   -35000,  -17000,     4000,    25000,   42000,    43000]
    # x_step = [        25,      25,       25,       25,      15,       25]
    # x_offset = [       0,       0,        0,        0,       0,        0]
    # x_pos_hex = [      0,       0,        0,        0,       0,       12]

    # samples = [  "Y1_03R"] #beam dump, didnt measure
    # x_pos =   [     44000]
    # x_step = [         25]
    # x_offset = [        0]
    # x_pos_hex = [      13]

    wa = [0, 20]
    # Q1_03 sample has spots, only x= 6000 realestate to move.
    #
    # samples = [  "S1_01a", "S1_01b", "S1_02a", "S1_02b", "Q1_01", "Q1_02",  "Q1_03"] 
    # x_pos =   [   -53880,  -44880,   -24720,    -4560,   16040,    24600,   46600.]
    # x_step = [        40,      40,       40,       40,      40,       30,   20]
    # x_offset = [       0,       0,        0,        0,       0,        0,   0]
    # x_pos_hex = [    -10,       0,        0,        0,       0,       13,   13]

    #McNeill_10
    samples = [  "Y1_03R"] 
    x_pos =   [      8000]
    x_step = [         35]
    x_pos_hex = [       0]

    for i, (sample, x, xstep, xhex) in enumerate(zip(samples, x_pos, x_step, x_pos_hex)):
        
        # Setup measurement for sample
        det_exposure_time(1, 1)
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(stage.x, xhex)

        # Sample alignment - align at 0.3 because....
        yield from alignement_gisaxs(angle=0.3)
    
        print('ai0 is ', piezo.th.position)

        yield from calibrate_ai_hor(t=1, energies=2450, name=sample)
    
        # beam is 200um.
        yield from fixedposition_energysweep_hor(t=1, name=sample, ai_list=[0.4, 0.8, 4, 8], waxs_arc=[0])

        yield from bps.mvr(piezo.x, 300)
        yield from incident_energy_scan_giwaxs_S_edge_2024_3(t=1, energies=2450, name=sample)
        # beam is 200um.
        yield from bps.mvr(piezo.x, 300)

        yield from sevralai_giwaxs_S_edge_2024_3_v2(t=1, 
                                                    name=sample, 
                                                    ai_list = [0.4, 0.8, 4.0, 8.0], 
                                                    xstep=xstep,
                                                    waxs_arc=wa) # steps 63 energies
        
def waxs_S_edge_chris_2025_1(t=1):
    dets = [pil900KW, pil1M]


    names = [ "Y2_01_a","Y2_01r_a", "Y2_01_b","Y2_01r_b", "Y2_01_c","Y2_01r_r","Q2_03","Y2_02_a","Y2_02r_a","Y2_02_b",
             "Y2_02r_b", "Y2_04_a","Y2_04r_a", "Y2_04_b","Y2_04r_b"]
    x = [        42000,    36100,    30300,    25000,    19300,    14000,   8500,    3000,    -2300,   -8300,
                -13600,   -21700,   -27300,   -33100,   -38300] 
    y = [        -4800,    -4800,    -4800,    -4800,    -4800,    -4900,  -4900,   -4700,    -4800,   -4800,
                 -4600,    -4600,    -4500,    -4700,    -4700]


    names = [ "Q2_03","Y2_02_a","Y2_02r_a","Y2_02_b",
             "Y2_02r_b", "Y2_04_a","Y2_04r_a", "Y2_04_b","Y2_04r_b"]
    x = [           8500,    3000,    -2300,   -8300,
                -13600,   -21700,   -27300,   -33100,   -38300] 
    y = [          -4900,   -4700,    -4800,   -4800,
                 -4600,    -4600,    -4500,    -4700,    -4700]


    assert len(x) == len(y), f"Number of X coordinates ({len(x)}) is different from number of samples ({len(y)})"
    assert len(x) == len(names), f"Number of X coordinates ({len(x)}) is different from number of samples ({len(names)})"

    energies = (np.arange(2445, 2470, 5).tolist()+ np.arange(2470, 2480, 0.25).tolist()+ np.arange(2480, 2490, 1).tolist()
                + np.arange(2490, 2500, 5).tolist()+ np.arange(2500, 2560, 10).tolist())
    
    waxs_arc = [0, 20]

    for name, xs, ys in zip(names, x, y):
        yield from bps.mv(piezo.x, xs,
                          piezo.y, ys)

        yss = np.linspace(ys, ys + 1500, len(energies))
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

            name_fmt = "{sample}_{energy}eV_wa{wax}_bpm{xbpm}"
            for e, xsss, ysss in zip(energies, xss, yss):
                yield from bps.mv(energy, e)
                yield from bps.sleep(2)
                if xbpm2.sumX.get() < 50:
                    yield from bps.sleep(2)
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)

                yield from bps.mv(piezo.y, ysss)
                yield from bps.mv(piezo.x, xsss)

                bpm = xbpm3.sumX.get()

                sample_name = name_fmt.format(sample=name, energy="%6.2f" % e, wax=wa, xbpm="%4.3f" % bpm)
                sample_id(user_name="CM", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")

                yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 2500)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 2480)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 2445)






def vert_sequence_scan_25_01_newsecurity():
    """
    Measuring samples mounted vertically:
    - Alignement in the vertical orientation
    - Take a direct and reflected beam at ai = 3 deg to verify the alignement precision
    - Take few energies without translation for an energy variation reference (no sample inhomogemetiy)
    - Scan the incident angle at 2450 eV
    - Fine energy scan at 0.4, 0.8, 4 and 8 deg incident angles
    """

    # In McNeil_11
    samples = ["A4_02p", "A1_02p", "Q1_01p", "Q1_02p", "Q1_03p", "A3_04p",
               "A3_05p", "A3_06p", "A3_12p"]
    ys =   [      -6000,    -6000,    -6000,    -5000,    -6000,    -4000,
                      0,        0,        0]
    xs =   [     -51000,   -35000,   -11326,    15300,    40300,    52000,
                 -51000,   -35000,   -11326]
    xshexa =   [     -8,        1,        1,        1,        1,       14,
                     -8,        0,        0]
    yshexa =   [     -8,       -10,       -10,       -8,       -10,       -5,
                      2,        2,        2]

    samples = [  "A3_06p", "A3_12p"]
    ys =   [         0,        0]
    xs =   [           -34000,   -10000]
    xshexa =   [            1,        1]
    yshexa =   [            3,        3]

    wa=[20]
    assert len(samples) == len(ys), f"Number of X coordinates ({len(samples)}) is different from number of samples ({len(y)})"
    assert len(samples) == len(xs), f"Number of X coordinates ({len(samples)}) is different from number of samples ({len(names)})"
    assert len(samples) == len(xshexa), f"Number of X coordinates ({len(samples)}) is different from number of samples ({len(names)})"
    assert len(samples) == len(yshexa), f"Number of X coordinates ({len(samples)}) is different from number of samples ({len(names)})"


    det_exposure_time(1, 1)

    for i, (sample, y, x, xhexa, yhexa) in enumerate(zip(samples, ys, xs, xshexa, yshexa)):
        if 'A4' in sample:
            wa = [18]
        elif 'Y1' in sample or 'A3' in sample or 'Q1' in sample:
            wa = [20]

        # Setup measurement for sample
        yield from bps.mv(piezo.y, y)
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(stage.x, xhexa)
        yield from bps.mv(stage.y, yhexa)

        yield from bps.mv(GV7.open_cmd, 1)
        yield from bps.sleep(1)
        yield from bps.mv(GV7.open_cmd, 1)
        yield from bps.sleep(1)

        yield from alignement_xrr_xmotor(angle=0.1)

        yield from bps.mv(GV7.close_cmd, 1)
        yield from bps.sleep(1)
        yield from bps.mv(GV7.close_cmd, 1)
        yield from bps.sleep(1)

        # beam is 30um.
        yield from calibrate_ai_ver(t=1, energies=2450, name=sample)

        # beam is 30um.
        yield from bps.mv(piezo.y, y - 30)

        # beam is 30um.
        yield from fixedposition_energysweep_ver_newsecurity(t=1, name=sample, ai_list=[0.4, 0.8, 4, 8], waxs_arc=wa)

        # beam is 30um.
        yield from bps.mv(piezo.y, y - 30)

        yield from vert_aiscan_giwaxs_S_edge_2024_3_newsecurity(t=1, energies=2450, name=sample, waxs_arc=wa)
        
        # beam is 30um.
        yield from bps.mv(piezo.y, y - 30)

        # Run sample scan
        yield from vert_giwaxs_S_edge_2024_3_newsecurity(
            t=1, name=sample, ai_list = [0.4, 0.8, 4, 8], ystep=20, waxs_arc=wa) # steps 63 energies



def fixedposition_energysweep_ver_newsecurity(t=1, name="Test", ai_list: list[int] = [], waxs_arc=[18]):
    '''
    Study the beam damage on 1 film to define the opti;am experimental conitions.

    '''
    dets = [pil900KW]

    energies = [2450, 2465, 2475, 2485, 2510, 2540, 2477.5]
    
    ai0 = prs.position
    ys = piezo.y.position

    det_exposure_time(1, 1)

    s = Signal(name='target_file_name', value='')
    @bpp.stage_decorator(dets)
    @bpp.run_decorator(md={'sample_name' :'{target_file_name}'})
    def inner():
        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)

            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.y, ys - k * 20)

                yield from bps.mv(prs, ai0 - ais)
                name_fmt = "fixedpossweep_{sample}_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                
                for e in energies:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(5)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    
                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    s.put(sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bps.trigger_and_read(dets + [energy, waxs, xbpm2, xbpm3] + [s])
                
                yield from bps.mv(energy, 2445)
                yield from bps.sleep(2)

            yield from bps.mv(prs, ai0)

    (yield from inner())



def vert_aiscan_giwaxs_S_edge_2024_3_newsecurity(t=1, energies=2450, name="Test", waxs_arc=[18]):
    '''
    Study the beam damage on 1 film to define the opti;am experimental conitions.

    '''
    dets = [pil900KW]
    det_exposure_time(t, t)
    
    yield from bps.mv(energy, energies)
    yield from bps.sleep(2)
    yield from bps.mv(energy, energies)
    yield from bps.sleep(2)

    # waxs_arc = [18]
    ai_list = (np.arange(0.2, 0.46, 0.02).tolist()+ np.arange(0.46, 0.7, 0.003).tolist()+ np.arange(0.7, 1.0, 0.02).tolist()+ np.arange(1.0, 4.0, 0.1).tolist())    

    ai0 = prs.position


    s = Signal(name='target_file_name', value='')
    @bpp.stage_decorator(dets)
    @bpp.run_decorator(md={'sample_name' :'{target_file_name}'})
    def inner():

        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)
            
            for k, ais in enumerate(ai_list):
                yield from bps.mv(prs, ai0 - ais)
                name_fmt = "wideincidentanglescan_{sample}_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"

                bpm = xbpm2.sumX.get()
                sample_name = name_fmt.format(sample=name,energy="%6.2f"%energies, ai="%3.3f"%ais, wax=waxs_arc[0], xbpm="%4.3f"%bpm)
                s.put(sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bps.trigger_and_read(dets + [energy, waxs, xbpm2, xbpm3] + [s])
                yield from bps.sleep(1)

            yield from bps.mv(prs, ai0)
    (yield from inner())



def vert_giwaxs_S_edge_2024_3_newsecurity(t=1, name="Test", ai_list: list[int] = [], ystep=10, waxs_arc=[18]):
    '''
    Study the beam damage on 1 film to define the opti;am experimental conitions.

    '''
    dets = [pil900KW]


    # bottom left first
    # name = 'A1_01_test'    

    # 63 energies
    energies = (np.arange(2445, 2470, 5).tolist()+ np.arange(2470, 2480, 0.25).tolist()+ np.arange(2480, 2490, 1).tolist()
                + np.arange(2490, 2500, 5).tolist()+ np.arange(2500, 2560, 10).tolist())
    
    # waxs_arc = [18]

    ai0 = prs.position
    ys = piezo.y.position

    det_exposure_time(1, 1)

    s = Signal(name='target_file_name', value='')
    @bpp.stage_decorator(dets)
    @bpp.run_decorator(md={'sample_name' :'{target_file_name}'})
    def inner():

        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)

            counter = 0
            for k, ais in enumerate(ai_list):

                yield from bps.mv(prs, ai0 - ais)

                name_fmt = "{sample}_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                
                for e in energies:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    
                    yield from bps.mv(piezo.y, ys - counter * ystep)
                    counter += 1
                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    s.put(sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bps.trigger_and_read(dets + [energy, waxs, xbpm2, xbpm3] + [s])
                
                yield from bps.mv(energy, 2500)
                yield from bps.sleep(2)
                yield from bps.mv(energy, 2480)
                yield from bps.sleep(2)
                yield from bps.mv(energy, 2445)

            yield from bps.mv(prs, ai0)

    (yield from inner())



def hor_sequence_scan_25_01_scan(): #_P3HT
    """
    Running multiple samples with various scans
    """
    wa = [0, 20]
    
    # Sample bar 2 left by Matt
    #
    samples = [  "A2_05", "A2_04", "A2_02", "A2_01", "A1_06", "A1_05",  "A1_02", "A1_01"] 
    x_pos =   [   -52000,  -48000,  -26000,  -10000,    6000,   27000,    43000,   47000]
    x_step = [        30,      30,      30,      30,      30,      30,       30,      30]
    x_pos_hex = [    -12,       0,       0,       0,       0,       0,        0,      12]
   
    samples = [   "A1_02", "A1_01"] 
    x_pos =   [  43000,   47000]
    x_step = [        30,      30]
    x_pos_hex = [   0,      12]
   

    for i, (sample, x, xstep, xhex) in enumerate(zip(samples, x_pos, x_step, x_pos_hex)):
        
        # Setup measurement for sample
        det_exposure_time(1, 1)
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(stage.x, xhex)

        # Sample alignment - align at 0.3 because....
        yield from alignement_gisaxs(angle=0.3)
    
        print('ai0 is ', piezo.th.position)

        yield from calibrate_ai_hor(t=1, energies=2450, name=sample)
    
        # beam is 200um.
        yield from fixedposition_energysweep_hor(t=1, name=sample, ai_list=[0.4, 0.8, 4, 8], waxs_arc=[0])

        yield from bps.mvr(piezo.x, 300)
        yield from incident_energy_scan_giwaxs_S_edge_2025_1_scan(t=1, energies=2450, name=sample)
        # beam is 200um.
        yield from bps.mvr(piezo.x, 300)

        yield from sevralai_giwaxs_S_edge_2025_1_scan(t=1, 
                                                    name=sample, 
                                                    ai_list = [0.4, 0.8, 4.0, 8.0], 
                                                    xstep=xstep,
                                                    waxs_arc=wa) # steps 63 energies
        


def sevralai_giwaxs_S_edge_2025_1_scan(t=1, name="Test", ai_list: list[int] = [], xstep=10, waxs_arc = [0, 20]):
    '''

    '''
    dets = [pil900KW, pil1M]
   
    # 63 energies
    energies = (np.arange(2445, 2470, 5).tolist()+ np.arange(2470, 2480, 0.25).tolist()+ np.arange(2480, 2490, 1).tolist()
                + np.arange(2490, 2500, 5).tolist()+ np.arange(2500, 2560, 10).tolist())
    
    ai0 = piezo.th.position
    xs = piezo.x.position

    s = Signal(name='target_file_name', value='')
    @bpp.stage_decorator(dets)
    @bpp.run_decorator(md={'sample_name' :'{target_file_name}'})
    def inner():
        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)

            counter = 0
            for k, ais in enumerate(ai_list):
                if ais==0.6:
                    det_exposure_time(0.5, 0.5)
                else:
                    det_exposure_time(1, 1)

                yield from bps.mv(piezo.th, ai0 + ais)

                name_fmt = "{sample}_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                
                for e in energies:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    
                    yield from bps.mv(piezo.x, xs + counter * xstep)
                    counter += 1
                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    s.put(sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bps.trigger_and_read(dets + [energy, waxs, xbpm2, xbpm3] + [s])
                
                yield from bps.mv(energy, 2500)
                yield from bps.sleep(2)
                yield from bps.mv(energy, 2480)
                yield from bps.sleep(2)
                yield from bps.mv(energy, 2445)

            yield from bps.mv(piezo.th, ai0)
    (yield from inner())


def incident_energy_scan_giwaxs_S_edge_2025_1_scan(t=1, energies=2450, name="Test"):
    '''
    Study the beam damage on 1 film to define the opti;am experimental conitions.

    '''
    dets = [pil900KW]
    det_exposure_time(t, t)

    # bottom left first
    # name = 'A1_01_test'
    
    yield from bps.mv(energy, energies)
    yield from bps.sleep(2)
    yield from bps.mv(energy, energies)
    yield from bps.sleep(2)

    waxs_arc = [0]
    ai_list = (np.arange(0.2, 0.46, 0.02).tolist()+ np.arange(0.46, 0.7, 0.003).tolist()+ np.arange(0.7, 1.0, 0.02).tolist()+ np.arange(1.0, 4.0, 0.1).tolist())    

    ai0 = piezo.th.position

    s = Signal(name='target_file_name', value='')
    @bpp.stage_decorator(dets)
    @bpp.run_decorator(md={'sample_name' :'{target_file_name}'})
    def inner():
        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)
            
            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)
                name_fmt = "wideincidentanglescan_{sample}_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"

                bpm = xbpm2.sumX.get()
                sample_name = name_fmt.format(sample=name,energy="%6.2f"%energies, ai="%3.3f"%ais, wax=waxs_arc[0], xbpm="%4.3f"%bpm)
                
                s.put(sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bps.trigger_and_read(dets + [energy, waxs, xbpm2, xbpm3] + [s])

            yield from bps.mv(piezo.th, ai0)
    (yield from inner())



def fixedposition_energysweep_hor_scan(t=1, name="Test", ai_list: list[int] = [], waxs_arc=[18]):
    '''
    Study the beam damage on 1 film to define the opti;am experimental conitions.

    '''
    dets = [pil900KW]

    energies = [2450, 2465, 2475, 2485, 2510, 2540, 2477.5]
    
    ai0 = piezo.th.position
    xs = piezo.x.position

    det_exposure_time(1, 1)

    s = Signal(name='target_file_name', value='')
    @bpp.stage_decorator(dets)
    @bpp.run_decorator(md={'sample_name' :'{target_file_name}'})
    def inner():

        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)

            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.x, xs + k * 100)

                yield from bps.mv(piezo.th, ai0 + ais)
                name_fmt = "fixedpossweep_{sample}_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                
                for e in energies:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(5)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    
                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    s.put(sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bps.trigger_and_read(dets + [energy, waxs, xbpm2, xbpm3] + [s])

                yield from bps.mv(energy, 2445)
                yield from bps.sleep(2)

            yield from bps.mv(piezo.th, ai0)

    (yield from inner())

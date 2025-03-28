def run_saxs_nexafs_greg(t=1):
    # yield from nexafs_prep_multisample_greg(t=0.5)
    # yield from bps.sleep(10)
    yield from saxs_prep_multisample(t=0.5)


def Su_nafion_nexafs_S_edge(t=1):
    dets = [pil900KW, pil1M]

    waxs_arc = [0, 20, 40]
    energies = 7 + np.asarray(
        np.arange(2445, 2470, 5).tolist()
        + np.arange(2470, 2480, 0.25).tolist()
        + np.arange(2480, 2490, 1).tolist()
        + np.arange(2490, 2501, 5).tolist()
    )

    yield from bps.mv(stage.y, 0)
    yield from bps.mv(stage.th, 0)

    names = ["NCo0", "NCo14", "NCo29", "NCo33", "DK_D139"]
    x = [43700, 21300, -1700, -24600, -55000]
    y = [-2400, -2400, -2000, -2000, -2400]
    z = [1186, 1186, 1186, 1186, 1186]

    for name, xs, ys, zs in zip(names, x, y, z):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)

        yss = np.linspace(ys, ys + 1000, 58)
        xss = np.linspace(xs, xs, 1)

        yss, xss = np.meshgrid(yss, xss)
        yss = yss.ravel()
        xss = xss.ravel()

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)

            det_exposure_time(t, t)
            name_fmt = "nexafs_{sample}_{energy}eV_sdd3m_wa{wax}_bpm{xbpm}"
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

    yield from bps.mv(stage.th, 5)
    yield from bps.mv(stage.y, -15)

    names = ["NCo70", "NCo114", "DK_N115", "DK_D114", "DK_D136"]
    x = [48300, 25800, 3300, -18800, -41800]
    y = [-9500, -9500, -9500, -9500, -9500]
    z = [14186, 14186, 14186, 14186, 14186]

    for name, xs, ys, zs in zip(names, x, y, z):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)

        yss = np.linspace(ys, ys + 1000, 58)
        xss = np.linspace(xs, xs, 1)

        yss, xss = np.meshgrid(yss, xss)
        yss = yss.ravel()
        xss = xss.ravel()

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)

            det_exposure_time(t, t)
            name_fmt = "nexafs_{sample}_{energy}eV_wa{wax}_bpm{xbpm}"
            for e, xsss, ysss in zip(energies, xss, yss):
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

            yield from bps.mv(energy, 2470)
            yield from bps.sleep(3)
            yield from bps.mv(energy, 2450)
            yield from bps.sleep(3)


def Su_nafion_swaxs_S_edge(t=1):
    dets = [pil900KW, pil300KW]

    waxs_arc = [0, 20]
    energies = 7 + np.asarray(
        np.arange(2445, 2470, 5).tolist()
        + np.arange(2470, 2480, 0.25).tolist()
        + np.arange(2480, 2490, 1).tolist()
        + np.arange(2490, 2501, 5).tolist()
    )
    # energies = np.asarray(np.arange(2810, 2820, 5).tolist() + np.arange(2820, 2825, 1).tolist() + np.arange(2825, 2835, 0.25).tolist() + np.arange(2835, 2840, 0.5).tolist() + np.arange(2840, 2850, 1).tolist())

    names = ["AK_PFSA_HPA", "AK_PFSA_ref", "MP_5", "MP_6", "MP_7"]
    x = [43000, 20000, -2500, -25000, -56500]
    y = [1000, 1000, 2500, -1000, 2400]
    z = [1186, 1186, 1186, 1186, 1186]

    # names = ['MP_6', 'MP_7']
    # x =     [-25000, -56500]
    # y =     [  1000,   2400]
    # z =     [  1186,   1186]

    # for name, xs, ys, zs in zip(names, x, y, z):
    #     yield from bps.mv(piezo.x, xs)
    #     yield from bps.mv(piezo.y, ys)
    #     yield from bps.mv(piezo.z, zs)

    #     yss = np.linspace(ys, ys + 1000, 58)
    #     xss = np.linspace(xs, xs, 1)

    #     yss, xss = np.meshgrid(yss, xss)
    #     yss = yss.ravel()
    #     xss = xss.ravel()

    #     for wa in waxs_arc:
    #         yield from bps.mv(waxs, wa)

    #         if wa ==0:
    #             dets = [pil900KW]
    #         else:
    #             dets = [pil900KW, pil1M]

    #         det_exposure_time(t,t)
    #         name_fmt = '{sample}_{energy}eV_sdd1.7m_wa{wax}_bpm{xbpm}'
    #         for e, xsss, ysss in zip(energies, xss, yss):
    #             yield from bps.mv(energy, e)
    #             yield from bps.sleep(3)

    #             yield from bps.mv(piezo.y, ysss)
    #             yield from bps.mv(piezo.x, xsss)

    #             bpm = xbpm2.sumX.value

    #             sample_name = name_fmt.format(sample=name, energy='%6.2f'%e, wax = wa, xbpm = '%4.3f'%bpm)
    #             sample_id(user_name='GF', sample_name=sample_name)
    #             print(f'\n\t=== Sample: {sample_name} ===\n')
    #             yield from bp.count(dets, num=1)

    #         yield from bps.mv(energy, 2470)
    #         yield from bps.sleep(3)
    #         yield from bps.mv(energy, 2450)
    #         yield from bps.sleep(3)

    waxs_arc = [0, 20]

    yield from bps.mv(stage.th, 0)
    yield from bps.mv(stage.y, -6)

    # names = ['MP_8', 'MP_1', 'MP_2', 'MP_3', 'MP_4']
    # x =     [ 46500,  21000,  -1500, -26500, -48000]
    # y =     [ -9500,  -9500,  -9500,  -9500,  -9500]
    # z =     [  1186,   1186,   1186,   1186,   1186]

    names = ["MP_4"]
    x = [-47000]
    y = [-8000]
    z = [1186]

    for name, xs, ys, zs in zip(names, x, y, z):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)

        yss = np.linspace(ys, ys + 1000, 67)
        xss = np.linspace(xs, xs, 1)

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
            name_fmt = "{sample}_{energy}eV_sdd1.7m_wa{wax}_bpm{xbpm}"
            for e, xsss, ysss in zip(energies, xss, yss):

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

            # yield from bps.mv(energy, 2470)
            yield from bps.mv(energy, 2830)
            yield from bps.sleep(3)
            yield from bps.mv(energy, 2810)
            # yield from bps.mv(energy, 2450)
            yield from bps.sleep(3)


def Su_nafion_waxs_S_edge(t=1):
    dets = [pil300KW, pil1M]

    yield from bps.mv(GV7.open_cmd, 1)
    yield from bps.sleep(5)
    yield from bps.mv(GV7.open_cmd, 1)

    energies = 7 + np.asarray(
        np.arange(2445, 2470, 5).tolist()
        + np.arange(2470, 2480, 0.25).tolist()
        + np.arange(2480, 2490, 1).tolist()
        + np.arange(2490, 2501, 5).tolist()
    )
    waxs_arc = np.linspace(0, 26, 5)

    yield from bps.mv(stage.y, 0)
    yield from bps.mv(stage.th, 0)

    names = ["SPES20", "SPES40", "SPES60", "70nPA"]
    x = [41500, 18500, -4500, -26500]
    y = [1500, 1000, 500, -500]

    for name, xs, ys in zip(names, x, y):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)

        yss = np.linspace(ys, ys + 1000, 15)
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

    yield from bps.mv(stage.th, 1)
    yield from bps.mv(stage.y, -8)

    names = ["50nPA", "30nPA", "10nPA"]
    x = [30500, 7500, -14200]
    y = [-9600, -9600, -9700]

    for name, xs, ys in zip(names, x, y):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)

        yss = np.linspace(ys, ys + 1000, 15)
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


def nexafs_Su(t=1):
    dets = [pil300KW]

    energies = np.asarray(
        np.arange(2445, 2470, 5).tolist()
        + np.arange(2470, 2480, 0.25).tolist()
        + np.arange(2480, 2490, 1).tolist()
        + np.arange(2490, 2501, 5).tolist()
    )
    # energies = np.linspace(2450, 2500, 51)
    waxs_arc = [52.5]

    names = ["sampleA_redo", "sampleB", "sampleC", "sampleD"]
    x = [-22200, -33200, -38700, -29600]
    y = [-5250, -5250, -5450, 7600]

    for name, xs, ys in zip(names, x, y):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)
            det_exposure_time(t, t)
            name_fmt = "nexafs_{sample}_{energy}eV_wa{wax}_bpm{xbpm}"
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


def waxs_S_edge_greg_2021_2(t=1):
    dets = [pil300KW, pil1M]
    yield from bps.mv(prs, 1)

    names = ["sampleA", "sampleB", "sampleC", "sampleD"]
    x = [-22200, -33200, -39200, -29600]
    y = [-5250, -5250, -5450, 7600]

    energies = (
        np.arange(2445, 2470, 5).tolist()
        + np.arange(2470, 2480, 0.5).tolist()
        + np.arange(2480, 2490, 2).tolist()
        + np.arange(2490, 2501, 5).tolist()
    )
    waxs_arc = np.linspace(13, 13, 1)

    for name, xs, ys in zip(names, x, y):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)

        yss = np.linspace(ys, ys + 200, 33)
        xss = np.array([xs])

        yss, xss = np.meshgrid(yss, xss)
        yss = yss.ravel()
        xss = xss.ravel()

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)

            det_exposure_time(t, t)

            name_fmt = "{sample}_1.6m_{energy}eV_wa{wax}_bpm{xbpm}"
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


def humidity_experiment(t=1):
    dets = [pil300KW, pil1M]

    # ai_aligned = [1.931, 1.788, 1.666, 1.817]
    # ys_aligned = [3.2, 3.189, 3.122, 3.053]
    # names = ['A30_T0', 'A50_T0', 'A70_T0', 'A90_T0']
    # x_hexa = [     23,        8,       -6,      -18]
    # y_hexa = [    3.2,      3.2,      3.2,      3.2]

    ai_aligned = [1.1248, 0.985, 0.995, 0.916]
    ys_aligned = [3.293, 3.247, 3.19, 3.123]

    # names = ['A30_T7', 'A50_T7', 'A70_T7', 'A90_T7']
    # x_hexa = [     22,       9,       -7,      -16.5]
    # y_hexa = [    3.2,      3.2,      3.2,      3.2]

    names = ["bkg"]
    x_hexa = [23.6]
    y_hexa = [0]

    setDryFlow(5)
    setWetFlow(0)

    humidity = "%3.2f" % readHumidity(verbosity=0)

    waxs_arc = np.linspace(0, 13, 3)

    ai_list = [0.10]

    for num, (name, xs_hexa, ys_hexa) in enumerate(zip(names, x_hexa, y_hexa)):
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(stage.y, ys_hexa)

        # yield from alignement_special_hex(angle = 0.15)

        # ai_aligned = ai_aligned + [ai0]
        # ys_aligned = ys_aligned + [stage.y.position]

        # yield from bps.mv(stage.y, ys_aligned[num])
        # yield from bps.mv(stage.th, ai_aligned[num])

        ai0 = stage.th.position

        # print(ai_aligned)
        # print(ys_aligned)

        det_exposure_time(t, t)

        for i, wa in enumerate(waxs_arc[::-1]):
            yield from bps.mv(waxs, wa)

            for k, ais in enumerate(ai_list):
                yield from bps.mv(stage.th, ai0 + ais)
                yield from bps.mv(stage.x, xs_hexa + k * 0.2)

                name_fmt = "{sample}_posthumi_16.1keV_3m_hum{hum}_wa{wax}"
                sample_name = name_fmt.format(sample=name, hum=humidity, wax=wa)
                sample_id(user_name="AB", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

        yield from bps.mv(stage.th, ai0)

    print(ai_aligned)
    print(ys_aligned)


def waxs_Se_edge_greg(t=1):

    det_exposure_time(t, t)

    names = ["PBTTTSe_neat", "P3RSe_dopped", "PBTTTS_dopped", "PBTTTSe_dopped"]
    x = [23700, 17600, 11300, 5400]
    y = [-8300, -8400, -8200, -8600]

    dets = [pil300KW, pil1M]
    energies = (
        np.arange(12620, 12640, 5).tolist()
        + np.arange(12640, 12660, 0.5).tolist()
        + np.arange(12660, 12670, 1).tolist()
        + np.arange(12670, 12716, 5).tolist()
    )
    waxs_arc = np.linspace(0, 26, 5)

    for name, xs, ys in zip(names, x, y):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)

        yss = np.linspace(ys, ys + 400, 32)
        xss = np.array([xs, xs - 400])

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

            yield from bps.mv(energy, 12680)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 12645)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 12620)
            yield from bps.sleep(2)


def Su_nafion_swaxs_K_edge(t=1):
    dets = [pil900KW, pil1M]

    waxs_arc = [0, 20, 40]
    energies = np.asarray(
        np.arange(3570, 3600, 5).tolist()
        + np.arange(3600, 3608, 2).tolist()
        + np.arange(3608, 3640, 1).tolist()
        + np.arange(3640, 3690, 5).tolist()
    )

    yield from bps.mv(stage.y, 5)
    yield from bps.mv(stage.th, 0)

    names = ["MP_1", "MP_3"]
    x = [-1000, -23000]
    y = [3000, 2000]
    z = [1186, 1186]

    for name, xs, ys, zs in zip(names, x, y, z):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)

        yss = np.linspace(ys, ys + 1000, 52)
        xss = np.linspace(xs, xs, 1)

        yss, xss = np.meshgrid(yss, xss)
        yss = yss.ravel()
        xss = xss.ravel()

        for wa in waxs_arc[::-1]:
            yield from bps.mv(waxs, wa)

            if wa == 0:
                dets = [pil900KW]
            else:
                dets = [pil900KW, pil1M]

            det_exposure_time(t, t)
            name_fmt = "{sample}_{energy}eV_sdd3m_wa{wax}_bpm{xbpm}"
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

            yield from bps.mv(energy, 3650)
            yield from bps.mv(energy, 3610)


def Su_nafion_nexafs_K_edge(t=1):
    dets = [pil900KW]

    waxs_arc = [40]
    energies = np.asarray(
        np.arange(3570, 3600, 5).tolist()
        + np.arange(3600, 3608, 2).tolist()
        + np.arange(3608, 3640, 1).tolist()
        + np.arange(3640, 3690, 5).tolist()
    )

    yield from bps.mv(stage.y, 5)
    yield from bps.mv(stage.th, 0)

    names = ["MP_1"]
    x = [-1000]
    y = [3000]
    z = [1186]

    for name, xs, ys, zs in zip(names, x, y, z):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)

        yss = np.linspace(ys, ys + 1000, 52)
        xss = np.linspace(xs, xs, 1)

        yss, xss = np.meshgrid(yss, xss)
        yss = yss.ravel()
        xss = xss.ravel()

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)

            det_exposure_time(t, t)
            name_fmt = "nexafs_{sample}_{energy}eV_sdd3m_wa{wax}_bpm{xbpm}"
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

            yield from bps.mv(energy, 3650)
            yield from bps.mv(energy, 3610)


def Su_nafion_swaxs_Co_edge(t=1):
    dets = [pil900KW, pil1M]

    waxs_arc = [0, 20, 40]
    energies = np.asarray(
        np.arange(7650, 7700, 5).tolist()
        + np.arange(7700, 7750, 1).tolist()
        + np.arange(7750, 8405, 5).tolist()
    )
    yield from bps.mv(stage.th, 0)

    names = ["NCo0", "NCo14", "NCo29", "NCo033", "NCo70", "NCo114"]
    x = [-56000, 46000, 22000, 0, -23000, -46000]
    y = [1000, -9500, -9500, -9500, -9500, -9500]
    z = [1186, 1186, 1186, 1186, 1186, 1186]
    y_hexa = [5, -6, -6, -6, -6, -6]

    for name, xs, ys, ys_hexa, zs in zip(names, x, y, y_hexa, z):
        if name == "NCo0":
            waxs_arc = [0, 20]
        else:
            waxs_arc = [0, 20, 40]

        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(stage.y, ys_hexa)

        yield from bps.mv(piezo.z, zs)

        yss = np.linspace(ys, ys + 1700, 170)
        xss = np.linspace(xs, xs, 1)

        yss, xss = np.meshgrid(yss, xss)
        yss = yss.ravel()
        xss = xss.ravel()

        for wa in waxs_arc[::-1]:
            yield from bps.mv(waxs, wa)

            if wa == 0:
                dets = [pil900KW]
            else:
                dets = [pil900KW, pil1M]

            det_exposure_time(t, t)
            name_fmt = "{sample}_{energy}eV_sdd3m_wa{wax}_bpm{xbpm}"
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

            for ene in np.linspace(8400, 7660, 38):
                yield from bps.mv(energy, ene)
                yield from bps.sleep(2)


def Su_nafion_swaxs_hard(t=1):
    dets = [pil900KW, pil1M]

    waxs_arc = [0, 20, 40]
    yield from bps.mv(stage.th, 0)

    # names = ['AK_PFSA_HPA','AK_PFSA_ref']
    # x =     [        43000,        20000]
    # y =     [         2000,         1500]
    # z =     [         1186,         1186]
    # y_hexa = [           5,            5]

    names = [
        "DK_N115",
        "DK_D114",
        "DK_D136",
        "DK_D139",
        "DK_D165",
        "MP_5",
        "MP_6",
        "MP_7",
        "MP_8",
    ]
    x = [42000, 17000, -5000, -30000, -56000, 45000, 5000, -18000, -41000]
    y = [3500, 3500, 3500, 3500, 2500, -8500, -8500, -8200, -8200]
    z = [1186, 1186, 1186, 1186, 1186, 1186, 1186, 1186, 1186]
    y_hexa = [5, 5, 5, 5, 5, -6, -6, -6, -6]

    x = [-41000]
    y = [-8200]
    z = [1186]
    y_hexa = [-6]

    for name, xs, ys, ys_hexa, zs in zip(names, x, y, y_hexa, z):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(stage.y, ys_hexa)
        yield from bps.mv(piezo.z, zs)

        for wa in waxs_arc[::-1]:
            yield from bps.mv(waxs, wa)

            if wa == 0:
                dets = [pil900KW]
            else:
                dets = [pil900KW, pil1M]

            det_exposure_time(t, t)
            name_fmt = "{sample}_16.1keV_sdd5m_wa{wax}"

            bpm = xbpm2.sumX.value

            sample_name = name_fmt.format(sample=name, wax=wa)
            sample_id(user_name="GF", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)


def Su_nafion_swaxs_S_edge_SVA_2021_3(t=1):
    dets = [pil900KW, pil1M]

    waxs_arc = [0, 20]
    energies = 7 + np.asarray(
        np.arange(2445, 2470, 5).tolist()
        + np.arange(2470, 2480, 0.25).tolist()
        + np.arange(2480, 2490, 1).tolist()
        + np.arange(2490, 2501, 5).tolist()
    )

    names = [
        "bkg",
        "NCo0",
        "NCo14",
        "NCo33",
        "NCo70",
        "NCo114",
        "MP_5",
        "MP_6",
        "MP_7",
        "MP_7",
    ]
    x = [30.5, 24.0, 18.0, 11.5, 5.0, -1.2, -7.6, -14.0, -20.2, -26.5]
    y = [-1.5, -1.5, -1.7, -1.7, -1.7, -1.7, -1.7, -1.7, -1.7, -1.7]

    for name, xs, ys in zip(names, x, y):
        yield from bps.mv(stage.x, xs)
        yield from bps.mv(stage.y, ys)

        yss = np.linspace(ys, ys + 0.4, 58)
        xss = np.linspace(xs, xs, 1)

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
            name_fmt = "{sample}_{energy}eV_sdd1.7m_wa{wax}_bpm{xbpm}_hum0per"
            for e, xsss, ysss in zip(energies, xss, yss):
                yield from bps.mv(energy, e)
                yield from bps.sleep(3)

                yield from bps.mv(stage.y, ysss)
                yield from bps.mv(stage.x, xsss)

                bpm = xbpm2.sumX.value

                sample_name = name_fmt.format(
                    sample=name, energy="%6.2f" % e, wax=wa, xbpm="%4.3f" % bpm
                )
                sample_id(user_name="GF", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 2470)
            yield from bps.sleep(3)
            yield from bps.mv(energy, 2450)
            yield from bps.sleep(3)

    # # Measure at flow 100 percent
    setDryFlow(0)
    setWetFlow(5)
    yield from bps.sleep(600)

    names = [
        "bkg",
        "NCo0",
        "NCo14",
        "NCo33",
        "NCo70",
        "NCo114",
        "MP_5",
        "MP_6",
        "MP_7",
        "MP_7",
    ]
    x = [30.5, 24.0, 17.5, 11.5, 5.0, -1.5, -8.0, -14.0, -20.5, -26.5]
    y = [-1.5, -1.5, -1.5, -1.5, -1.5, -1.5, -1.5, -1.5, -1.5, -1.5]

    for name, xs, ys in zip(names, x, y):
        yield from bps.mv(stage.x, xs)
        yield from bps.mv(stage.y, ys)

        yss = np.linspace(ys + 0.4, ys + 0.8, 58)
        xss = np.linspace(xs, xs, 1)

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
            name_fmt = "{sample}_{energy}eV_sdd1.7m_wa{wax}_bpm{xbpm}_hum100per"
            for e, xsss, ysss in zip(energies, xss, yss):
                yield from bps.mv(energy, e)
                yield from bps.sleep(3)

                yield from bps.mv(stage.y, ysss)
                yield from bps.mv(stage.x, xsss)

                bpm = xbpm2.sumX.value

                sample_name = name_fmt.format(
                    sample=name, energy="%6.2f" % e, wax=wa, xbpm="%4.3f" % bpm
                )
                sample_id(user_name="GF", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 2470)
            yield from bps.sleep(3)
            yield from bps.mv(energy, 2450)
            yield from bps.sleep(3)

    # # Measure at flow 100 percent
    setDryFlow(5)
    setWetFlow(0)
    yield from bps.sleep(600)

    names = [
        "bkg",
        "NCo0",
        "NCo14",
        "NCo33",
        "NCo70",
        "NCo114",
        "MP_5",
        "MP_6",
        "MP_7",
        "MP_7",
    ]
    x = [30.5, 24.0, 17.5, 11.5, 5.0, -1.5, -8.0, -14.0, -20.5, -26.5]
    y = [-1.5, -1.5, -1.5, -1.5, -1.5, -1.5, -1.5, -1.5, -1.5, -1.5]

    for name, xs, ys in zip(names, x, y):
        yield from bps.mv(stage.x, xs)
        yield from bps.mv(stage.y, ys)

        yss = np.linspace(ys + 0.8, ys + 1.2, 58)
        xss = np.linspace(xs, xs, 1)

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
            name_fmt = (
                "{sample}_{energy}eV_sdd1.7m_wa{wax}_bpm{xbpm}_hum0per_aftercycle"
            )
            for e, xsss, ysss in zip(energies, xss, yss):
                yield from bps.mv(energy, e)
                yield from bps.sleep(3)

                yield from bps.mv(stage.y, ysss)
                yield from bps.mv(stage.x, xsss)

                bpm = xbpm2.sumX.value

                sample_name = name_fmt.format(
                    sample=name, energy="%6.2f" % e, wax=wa, xbpm="%4.3f" % bpm
                )
                sample_id(user_name="GF", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 2470)
            yield from bps.sleep(3)
            yield from bps.mv(energy, 2450)
            yield from bps.sleep(3)

    setDryFlow(0)
    setWetFlow(0)


def waxs_S_edge_greg_2022_1(t=1):
    """
    307830_Su Feb 2, 2022
    """

    dets = [pil900KW, pil1M]

    # names = ['M725', 'M825', 'M1000', 'TF725T', 'TF825T', 'TF1000T', 'TF30T', 'TF50T', 'TF70T', 'TF90T', 'TF725', 'TF825', 'TF1000',
    #          'TF30', 'TF50',  'TF70',   'TF90',   'DT20',    'DT35',  'DT50', 'BLANK',   'M30',   'M50',   'M70',   'M90']

    # x =     [ 43000,  37000,   31000,    24500,    18500,     13000,    7500,    2000,   -3000,   -8500,  -14500,  -19500,  -25000,
    #           42000,  36500,   31000,    26000,    20500,     15000,    9500,    4200,   -3800,  -10000,  -18000,  -26000]

    # y =     [ -8500,  -8500,   -8500,    -8500,    -8700,     -8700,   -8700,   -8500,   -8500,   -8500,   -8500,   -8500,   -8500,
    #            4000,   4000,    4000,     4000,     4000,      4000,    4000,    4200,    4200,    4200,    4200,    4200]

    names = [
        "M725",
        "M825",
        "M1000",
        "TF50T",
        "TF70T",
        "TF90T",
        "TF725",
        "TF825",
        "TF1000",
        "TF30",
        "TF50",
        "TF70",
        "TF90",
        "DT20",
        "DT35",
        "DT50",
        "BLANK",
        "M30",
        "M50",
        "M70",
        "M90",
    ]

    x = [
        43000,
        37700,
        30000,
        2000,
        -3000,
        -8500,
        -14500,
        -19500,
        -25000,
        42000,
        36500,
        31000,
        26000,
        20500,
        15000,
        9500,
        4200,
        -3800,
        -10000,
        -18000,
        -26000,
    ]

    y = [
        -8500,
        -8700,
        -8700,
        -8500,
        -8500,
        -8500,
        -8500,
        -8500,
        -8500,
        4000,
        4000,
        4000,
        4000,
        4000,
        4000,
        4000,
        4200,
        4200,
        4200,
        4200,
        4200,
    ]

    # energies = np.arange(2445, 2470, 5).tolist() + np.arange(2470, 2480, 0.5).tolist() + np.arange(2480, 2490, 2).tolist()+ np.arange(2490, 2501, 5).tolist()
    energies = 7 + np.asarray(
        np.arange(2445, 2470, 5).tolist()
        + np.arange(2470, 2480, 0.25).tolist()
        + np.arange(2480, 2490, 1).tolist()
        + np.arange(2490, 2501, 5).tolist()
    )
    waxs_arc = [0, 20, 40, 60]

    for name, xs, ys in zip(names, x, y):
        # changing ys to allow for more room during dense energy scan
        ys = ys - 200
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)

        yss = np.linspace(ys, ys + 500, len(energies))
        xss = np.array([xs])

        yss, xss = np.meshgrid(yss, xss)
        yss = yss.ravel()
        xss = xss.ravel()

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)

            det_exposure_time(t, t)

            name_fmt = "{sample}_1.6m_{energy}eV_wa{wax}_bpm{xbpm}"
            for e, xsss, ysss in zip(energies, xss, yss):
                yield from bps.mv(energy, e)
                yield from bps.sleep(1)

                yield from bps.mv(piezo.y, ysss)
                yield from bps.mv(piezo.x, xsss)

                bpm = xbpm2.sumX.value

                sample_name = name_fmt.format(
                    sample=name, energy="%6.2f" % e, wax=wa, xbpm="%4.3f" % bpm
                )
                sample_id(user_name="AB", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")

                yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 2470)
            yield from bps.mv(energy, 2450)


def saxs_S_edge_greg_2022_1(t=1):
    """
    307830_Su Feb 2, 2022
    """
    proposal_id("2022_1", "307830_Su2")

    dets = [pil1M]

    # names = ['M725', 'M825', 'M1000', 'TF725T', 'TF825T', 'TF1000T', 'TF30T', 'TF50T', 'TF70T', 'TF90T', 'TF725', 'TF825', 'TF1000',
    #          'TF30', 'TF50',  'TF70',   'TF90',   'DT20',    'DT35',  'DT50', 'BLANK',   'M30',   'M50',   'M70',   'M90']

    # x =     [ 43000,  37000,   31000,    24500,    18500,     13000,    7500,    2000,   -3000,   -8500,  -14500,  -19500,  -25000,
    #           42000,  36500,   31000,    26000,    20500,     15000,    9500,    4200,   -3800,  -10000,  -18000,  -26000]

    # y =     [ -8500,  -8500,   -8500,    -8500,    -8700,     -8700,   -8700,   -8500,   -8500,   -8500,   -8500,   -8500,   -8500,
    #            4000,   4000,    4000,     4000,     4000,      4000,    4000,    4200,    4200,    4200,    4200,    4200]

    names = [
        "M725",
        "M825",
        "M1000",
        "TF50T",
        "TF70T",
        "TF90T",
        "TF725",
        "TF825",
        "TF1000",
        "TF30",
        "TF50",
        "TF70",
        "TF90",
        "DT20",
        "DT35",
        "DT50",
        "BLANK",
        "M30",
        "M50",
        "M70",
        "M90",
    ]

    x = [
        43000,
        37700,
        30000,
        2000,
        -3000,
        -8500,
        -14500,
        -19500,
        -25000,
        42000,
        36500,
        31000,
        26000,
        20500,
        15000,
        9500,
        4200,
        -3800,
        -10000,
        -18000,
        -26000,
    ]

    y = [
        -8500,
        -8700,
        -8700,
        -8500,
        -8500,
        -8500,
        -8500,
        -8500,
        -8500,
        4000,
        4000,
        4000,
        4000,
        4000,
        4000,
        4000,
        4200,
        4200,
        4200,
        4200,
        4200,
    ]

    # energies = np.arange(2445, 2470, 5).tolist() + np.arange(2470, 2480, 0.5).tolist() + np.arange(2480, 2490, 2).tolist()+ np.arange(2490, 2501, 5).tolist()
    energies = 7 + np.asarray(
        np.arange(2445, 2470, 5).tolist()
        + np.arange(2470, 2480, 0.25).tolist()
        + np.arange(2480, 2490, 1).tolist()
        + np.arange(2490, 2501, 5).tolist()
    )
    waxs_arc = [60]

    for name, xs, ys in zip(names, x, y):
        # changing ys to allow for more room during dense energy scan
        ys = ys - 200
        xs = xs - 400

        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)

        yss = np.linspace(ys, ys + 500, len(energies))
        xss = np.array([xs])

        yss, xss = np.meshgrid(yss, xss)
        yss = yss.ravel()
        xss = xss.ravel()

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)

            det_exposure_time(t, t)

            name_fmt = "{sample}_3.2m_{energy}eV_wa{wax}_bpm{xbpm}"
            for e, xsss, ysss in zip(energies, xss, yss):
                yield from bps.mv(energy, e)
                yield from bps.sleep(1)

                yield from bps.mv(piezo.y, ysss)
                yield from bps.mv(piezo.x, xsss)

                bpm = xbpm2.sumX.value

                sample_name = name_fmt.format(
                    sample=name, energy="%6.2f" % e, wax=wa, xbpm="%4.3f" % bpm
                )
                sample_id(user_name="AB", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")

                yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 2470)
            yield from bps.mv(energy, 2450)


def waxs_hard_Xray_Su3_2022_1(t=1):
    """
    307830_Su3 Feb 16, 2022
    """

    dets = [pil900KW, pil1M]

    # Included all the samples mounted on the sample bar
    names = [
        "M725",
        "M825",
        "M1000",
        "TF725T",
        "TF825T",
        "TF1000T",
        "TF30T",
        "TF50T",
        "TF70T",
        "TF90T",
        "TF725",
        "TF825",
        "TF1000",
        "TF30",
        "TF50",
        "TF70",
        "TF90",
        "DT20",
        "DT35",
        "DT50",
        "BLANK",
        "M30",
        "M50",
        "M70",
        "M90",
    ]

    x = [
        43500,
        37800,
        29000,
        24500,
        18500,
        13000,
        7700,
        2200,
        -2800,
        -8300,
        -14200,
        -19600,
        -24800,
        42000,
        36800,
        31500,
        26000,
        20500,
        15000,
        9700,
        4200,
        -3800,
        -10000,
        -18000,
        -26000,
    ]

    y = [
        -8500,
        -8500,
        -8500,
        -8500,
        -8500,
        -8500,
        -8500,
        -8300,
        -8500,
        -8500,
        -8300,
        -8300,
        -8500,
        4200,
        4200,
        4200,
        4200,
        4200,
        4200,
        4200,
        4000,
        4000,
        4000,
        4000,
        4000,
    ]

    waxs_arc = [0, 20, 40]

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)
        det_exposure_time(t, t)

        for name, xs, ys in zip(names, x, y):
            yield from bps.mv(piezo.x, xs)
            while abs(piezo.y.position - ys) > 100:
                yield from bps.mv(piezo.y, ys)
                yield from bps.sleep(10)

            name_fmt = "{sample}_{sdd}m_{energy}eV_wa{wax}_bpm{xbpm}"
            bpm = xbpm2.sumX.get()
            e = energy.energy.position
            sdd = pil1m_pos.z.position / 1000

            sample_name = name_fmt.format(
                sample=name,
                sdd="%.1f" % sdd,
                energy="%.0f" % e,
                wax=wa,
                xbpm="%4.3f" % bpm,
            )
            sample_id(user_name="AB", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")

            yield from bp.count(dets, num=1)



def waxs_S_edge_greg_2024_1(t=1):
    """
    307830_Su Feb 2, 2024
    """

    dets = [pil900KW, pil1M]

    names = ['N211_AR', 'NC700_AR', 'NC700_H', 'Pemion', 'Pemion_X1']
    x =     [    17500,       8500,      1500,    -6500,      -14500]
    y =     [    -7500,      -7500,     -7400,    -7400,       -7400]


    # energies = np.arange(2445, 2470, 5).tolist() + np.arange(2470, 2480, 0.5).tolist() + np.arange(2480, 2490, 2).tolist()+ np.arange(2490, 2501, 5).tolist()
    energies = 7 + np.asarray(np.arange(2445, 2470, 5).tolist() + np.arange(2470, 2480, 0.25).tolist() + np.arange(2480, 2490, 1).tolist()
                              + np.arange(2490, 2501, 5).tolist())
    
    waxs_arc = [0, 20]

    for name, xs, ys in zip(names, x, y):
        # changing ys to allow for more room during dense energy scan
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)

        yss = np.linspace(ys, ys + 1500, len(energies))
        xss = np.array([xs])

        yss, xss = np.meshgrid(yss, xss)
        yss = yss.ravel()
        xss = xss.ravel()

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)

            det_exposure_time(t, t)

            name_fmt = "{sample}_1.8m_{energy}eV_wa{wax}_bpm{xbpm}"
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

                sample_name = name_fmt.format(sample=name, energy="%6.2f" % e, wax=wa, xbpm="%4.3f"%bpm)
                sample_id(user_name="GS", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")

                yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 2470)
            yield from bps.mv(energy, 2450)




def swaxs_S_edge_greg_2024_2(t=1):
    """
    307830_Su Feb 2, 2024
    """

    dets = [pil900KW, pil1M]

    names = ['SO3_particle_1', 'SO3_particle_2', 'SO3_particle_3', 'SO3_particle_4']
    x =     [          -19200,           -25100,           -30500,           -36100]
    y =     [            6000,             6500,             6000,             6000]


    # energies = np.arange(2445, 2470, 5).tolist() + np.arange(2470, 2480, 0.5).tolist() + np.arange(2480, 2490, 2).tolist()+ np.arange(2490, 2501, 5).tolist()
    energies = 7+np.asarray(np.arange(2445, 2470, 5).tolist() + np.arange(2470, 2480, 0.25).tolist() + np.arange(2480, 2490, 1).tolist()
                              + np.arange(2490, 2501, 5).tolist())
    
    waxs_arc = [20]

    for name, xs, ys in zip(names, x, y):
        # changing ys to allow for more room during dense energy scan
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)

        yss = np.linspace(ys, ys + 0, len(energies))
        xss = np.array([xs])

        yss, xss = np.meshgrid(yss, xss)
        yss = yss.ravel()
        xss = xss.ravel()

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)

            det_exposure_time(t, t)

            name_fmt = "{sample}_3.0m_{energy}eV_wa{wax}_bpm{xbpm}"
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

                sample_name = name_fmt.format(sample=name, energy="%6.2f" % e, wax=wa, xbpm="%4.3f"%bpm)
                sample_id(user_name="GS", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")

                yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 2470)
            yield from bps.mv(energy, 2450)



def nexafs_Ce_edge_greg_2024_1(t=1):
    """
    307830_Su Feb 2, 2024
    """

    dets = [pil900KW, pil1M]

    names = ['test_nexafs']
    x =     [         8500]
    y =     [        -7500]

    dets = [pil900KW]
    det_exposure_time(t, t)

    energies = np.linspace(5710, 5760, 51)

    energies = np.asarray(np.arange(5700, 5720, 5).tolist() + np.arange(5720, 5727, 1).tolist() + np.arange(5727, 5737, 0.5).tolist() + np.arange(5737, 5747, 2).tolist()
                            + np.arange(5747, 5780, 5).tolist())
    
    waxs_arc = [40]

    for name, xs, ys in zip(names, x, y):
        # changing ys to allow for more room during dense energy scan
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)

        yss = np.linspace(ys, ys + 0, len(energies))
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
                yield from bps.sleep(2)
                if xbpm2.sumX.get() < 50:
                    yield from bps.sleep(2)
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)

                yield from bps.mv(piezo.y, ysss)
                yield from bps.mv(piezo.x, xsss)

                bpm = xbpm3.sumX.get()

                sample_name = name_fmt.format(sample=name, energy="%6.2f" % e, wax=wa, xbpm="%4.3f"%bpm)
                sample_id(user_name="GS", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")

                yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 5740)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 5710)
            yield from bps.sleep(2)



def swaxs_Ce_edge_greg_2024_1(t=1):
    """
    307830_Su Feb 2, 2024
    """

    dets = [pil900KW, pil1M]

    names = ['NC700_AR', 'NC700_H']
    x =     [      7500,       500]
    y =     [     -7500,     -7500]

    det_exposure_time(t, t)

    energies = np.asarray(np.arange(5700, 5720, 5).tolist() + np.arange(5720, 5727, 1).tolist() + np.arange(5727, 5737, 0.5).tolist() + np.arange(5737, 5747, 2).tolist()
                            + np.arange(5747, 5790, 5).tolist())
    
    waxs_arc = [40, 20, 0]

    for name, xs, ys in zip(names, x, y):
        # changing ys to allow for more room during dense energy scan
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)

        yss = np.linspace(ys, ys + 1000, len(energies))
        xss = np.array([xs])

        yss, xss = np.meshgrid(yss, xss)
        yss = yss.ravel()
        xss = xss.ravel()

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)

            det_exposure_time(t, t)

            name_fmt = "{sample}_sdd5100_{energy}eV_wa{wax}_bpm{xbpm}"
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

                sample_name = name_fmt.format(sample=name, energy="%6.2f" % e, wax=wa, xbpm="%4.3f"%bpm)
                sample_id(user_name="GS", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")

                yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 5750)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 5700)
            yield from bps.sleep(2)



def swaxs_S_edge_nafion_2024_2(t=1):
    """
    307830_Su June 23, 2024
    """

    dets = [pil900KW, pil1M]

    names = [ 'kapton', 'ppion_zrox01', 'ppion_zrox02', 'nafion212', 'P25-0p25',  'P25-0p5',    'P25-1',      'P25-2', 
              'P25-4',    'AHPP25-0p5',  'AHPP25-0p25',  'AHPP25-1', 'AHPP25-2', 'AHPP25-4',    'P5A-4',
               'P5A-2',        'P5A-1',      'P5A-0p5',  'P5A-0p25', 'AHPP5A-4',  'AHPP5-2', 'AHPP5A-1', 'AHPP5A-0p5', 
         'AHPP5A-0p25',        'LK-01',        'LK-02',     'LK-03',    'LK-04',    'LK-05']
    x =     [    42000,          33000,          26000,       18000,      12000,       5000,          0,        -5000,
                -10000,         -15000,         -19000,      -24000,     -29000,     -33000,     -38000,
                 45000,          40000,          35000,       30000,      26000,      21500,      16000,        11000,
                  6000,              0,          -5000,      -10000,     -18000,     -25000]
    y =     [    -8000,          -8000,          -8000,       -8000,      -8000,      -8000,      -8000,        -8000,
                 -8000,          -8000,          -8000,       -8000,      -8000,      -8000,      -8000,
                  4500,           4500,           4500,        4500,       4500,       4500,       4500,         4500,
                  4500,           4900,           4900,        4900,       4900,       4900]
    z =     [     2000,           2000,           2000,        1500,       1500,       1000,       1000,         1000,
                   500,            500,            500,           0,          0,          0,          0,
                  2000,           2000,           2000,        2000,       1500,       1500,       1000,         1000,
                  1000,            500,            500,           0,          0,          0]


    # energies = np.arange(2445, 2470, 5).tolist() + np.arange(2470, 2480, 0.5).tolist() + np.arange(2480, 2490, 2).tolist()+ np.arange(2490, 2501, 5).tolist()
    energies = 7 + np.asarray(np.arange(2445, 2470, 5).tolist() + np.arange(2470, 2480, 0.25).tolist() + np.arange(2480, 2490, 1).tolist()
                              + np.arange(2490, 2501, 5).tolist())
    
    waxs_arc = [0, 20]

    for name, xs, ys in zip(names, x, y):
        # changing ys to allow for more room during dense energy scan
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)

        yss = np.linspace(ys, ys + 1500, len(energies))
        xss = np.array([xs])

        yss, xss = np.meshgrid(yss, xss)
        yss = yss.ravel()
        xss = xss.ravel()

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)

            det_exposure_time(t, t)

            name_fmt = "{sample}_1.8m_{energy}eV_wa{wax}_bpm{xbpm}"
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

                sample_name = name_fmt.format(sample=name, energy="%6.2f" % e, wax=wa, xbpm="%4.3f"%bpm)
                sample_id(user_name="GS", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")

                yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 2470)
            yield from bps.mv(energy, 2450)



def bpmvspindiode_Sedge_2024_2(t=1):
    dets = [pil1M]
    det_exposure_time(t, t)

    name = 'Greg_Su_direct_beam_Sedge_scannormal'


    energies = 7 + np.asarray(np.arange(2445, 2470, 5).tolist() + np.arange(2470, 2480, 0.25).tolist() + np.arange(2480, 2490, 1).tolist()
                              + np.arange(2490, 2501, 5).tolist())
    
    # yield from bp.list_scan([energy, xbpm2, xbpm3, pdcurrent2], energy, list_ener)

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

        yield from bps.mv(energy, 2470)
        yield from bps.mv(energy, 2450)




def swaxs_hardxray_nafion_2024_2(t=1):
    """
    307830_Su June 23, 2024
    """

    dets = [pil900KW, pil1M]

    names = [ 'kapton', 'ppion_zrox01', 'ppion_zrox02', 'nafion212', 'P25-0p25',  'P25-0p5',    'P25-1',      'P25-2', 
              'P25-4',    'AHPP25-0p5',  'AHPP25-0p25',  'AHPP25-1', 'AHPP25-2', 'AHPP25-4',    'P5A-4',
               'P5A-2',        'P5A-1',      'P5A-0p5',  'P5A-0p25', 'AHPP5A-4',  'AHPP5-2', 'AHPP5A-1', 'AHPP5A-0p5', 
         'AHPP5A-0p25',        'LK-01',        'LK-02',     'LK-03',    'LK-04',    'LK-05']
    x =     [    42000,          33000,          26000,       18000,      12000,       5000,          0,        -5000,
                -10000,         -15000,         -19000,      -24000,     -29000,     -33000,     -38000,
                 45000,          40000,          35000,       30000,      26000,      21500,      16000,        11000,
                  6000,              0,          -5000,      -10000,     -18000,     -25000]
    y =     [    -8000,          -8000,          -8000,       -8000,      -8000,      -8000,      -8000,        -8000,
                 -8000,          -8000,          -8000,       -8000,      -8000,      -8000,      -8000,
                  4500,           4500,           4500,        4500,       4500,       4500,       4500,         4500,
                  4500,           4900,           4900,        4900,       4900,       4900]
    z =     [     2000,           2000,           2000,        1500,       1500,       1000,       1000,         1000,
                   500,            500,            500,           0,          0,          0,          0,
                  2000,           2000,           2000,        2000,       1500,       1500,       1000,         1000,
                  1000,            500,            500,           0,          0,          0]


    waxs_arc = [0, 20, 40]

    for name, xs, ys in zip(names, x, y):
        # changing ys to allow for more room during dense energy scan
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)

            det_exposure_time(t, t)

            name_fmt = "{sample}_1.8m_16100.0eV_wa{wax}"

            sample_name = name_fmt.format(sample=name, wax=wa)
            sample_id(user_name="GS", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")

            yield from bp.count(dets, num=1)







# 3 pm on Monday 24 June
# matt's bar w/ 9 samples for hard x-ray saxs/waxs (10 measurements since one sample has two positions)

def swaxs_hardxray_mrl_2024_2(t=1):
    """
    307830_Su June 23, 2024
    """

    dets = [pil900KW, pil1M]

    names = [             'xle-ctrl',               'xle-01',       'xle-02',           'xle-03',    'xle-04',    'xle-05',
              'alaska-filter1a-pos1', 'alaska-filter1a-pos2',  'kapton-ctrl',  'kapton-filter1b']
        
    x =     [                  43000,                  34000,          27000,              19000,       13000,      5000, 
                              -14300,                 -17300,         -26300,             -36300]
    y =     [                  -8500,                  -8500,          -8500,              -8500,       -8500,     -8500, 
                               -7900,                  -7900,          -7600,              -7600]
    z =     [                   2000,                   2000,           2000,               2000,        2000,      2000, 
                                2000,                   2000,           2000,               2000]


    waxs_arc = [0, 20, 40]

    for name, xs, ys in zip(names, x, y):
        # changing ys to allow for more room during dense energy scan
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)

            det_exposure_time(t, t)

            name_fmt = "{sample}_1.8m_16100.0eV_wa{wax}"

            sample_name = name_fmt.format(sample=name, wax=wa)
            sample_id(user_name="GS", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")

            yield from bp.count(dets, num=1)





def saxs_hardxray_capillaries_2024_2(t=0.1):
    """
    307830_Su June 24, 2024
    """

    dets = [pil1M]

    #names = [  'capillary-AgB', '144D7-20CuAc', '144D6-20CuAc', '144D5-20CuAc', '144Z-20CuAc', '144A-20CuAc',
     #          '93N-24', '109I-12CuAc', '109I-12CuAc-cloudy', '124Z6-20', '105D6-20CuAc', '105D5-20CuAc',
      #         '105Z-20CuAc', '107-Adam-SV', 'Adam-SAN15']
        
    #x =     [ -42000, -35500,  -29000, -22700, -16400, -10000, -3800, 2800, 9100, 15600 , 21700 , 28500, 34500 ,41100, 47600   ]
    #y =     [ -2500, -2500, -2500, -2500, -2500, -2500, -2500 , -2500 , -2500,  -2500 , -2500, -2500,  -2500 ,-2500 ,      -2500   ]
    #z =     [ 2000, 2000, 2000, 2000, 2000, 2000, 2000 , 2000, 2000,  2000 , 2000, 2000,  2000 ,2000,  2000 ]


    names = [  'capillary-AgB']
    
    x =     [ -42000  ]
    y =     [ -2500   ]
    z =     [ 2000    ]



    waxs_arc = [40]

    for name, xs, ys in zip(names, x, y):
        # changing ys to allow for more room during dense energy scan
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)

            det_exposure_time(t, t)

            name_fmt = "{sample}_1.8m_16100.0eV_wa{wax}"

            sample_name = name_fmt.format(sample=name, wax=wa)
            sample_id(user_name="GS", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")

            yield from bp.count(dets, num=1)




















def saxs_hardxray_mrl_capillaries_2024_2(t=1):
    """
    307830_Su June 24, 2024
    """

    dets = [pil1M]
    #names = [  'capillary-AgB']
    
   # x =     [ -42000  ]
    #y =     [ -8200   ]
    #z =     [ 2000    ]
    #sample names for bar 1, measured under vacuum, may have popped, may need to redo 
    names = [  '144D7-20CuAc', '144D6-20CuAc', '144D5-20CuAc', '144Z-20CuAc', '144A-20CuAc',
               '93N-24', '109I-12CuAc', '109I-12CuAc-cloudy', '124Z6-20', '105D6-20CuAc', '105D5-20CuAc',
               '105Z-20CuAc', '107-Adam-SV', 'Adam-SAN15']
        
    x =     [ -35500,  -29000, -22700, -16400, -10000, -3800, 2800, 9100, 15600 , 21700 , 28500, 34500 ,41100, 47600   ]
    y =     [ -2500, -2500, -2500, -2500, -2500, -2500 , -2500 , -2500,  -2500 , -2500, -2500,  -2500 ,-2500 ,      -2500   ]
    z =     [  2000, 2000, 2000, 2000, 2000, 2000 , 2000, 2000,  2000 , 2000, 2000,  2000 ,2000,  2000 ]




    #Sample names for bar 2
    names = ['Adam-SAN25', 'N-blend', '91N1', '91N1-MgAc02', '91N1-MgAc04',
            '91N1-MgAc1', '91N1-MgAc17','91N1-MgAc2', '91N1-CuAc03','91N1-CuAc05',
            '91N1-CuAc08', '91N1-CuAc11', '91N1-CuAc18']
    
    #positions
    x =     [ -42000, -35500, -29400, -22800, -16300,    -10000, -3500, 2600, 8900, 15400, 21900,  28200, 34400  ]
    y =     [ -2500, -2500, -2500, -2500, -2500, -2500 , -2500 , -2500,  -2500 , -2500, -2500,  -2500 ,-2500  ]
    z =     [  2000, 2000, 2000, 2000, 2000, 2000 , 2000, 2000,  2000 , 2000, 2000,  2000 ,2000 ]

   
    # sample names for bar 3
    names = ['tulasi-water', 'tulasi-01a', 'tulasi-01b', 'tulasi-02a', 'tulasi-02b', 'tulasi-03a', 'tulasi-03b']
    x = [             21200,        15800,         7800,         1300,        -6300,        -9900,      -17900 ]
    y = [             -1000,         -500,        -1000,        -1000,        -1000,        -1000,       -1000 ]
    z = [              2000,         2000,         2000,         2000,         2000,         2000,        2000 ]



    for name, xs, ys in zip(names, x, y):
        # changing ys to allow for more room during dense energy scan
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)

        det_exposure_time(t, t)

        name_fmt = "{sample}_1.8m_16100.0eV"

        sample_name = name_fmt.format(sample=name)
        sample_id(user_name="ML", sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")

        yield from bp.count([pil1M], num=1)



'''  notes from eliot for 2024-2 blade coating
thorlabs_su is the thorlabs motor, it's a normal motor record, so you can set .velocity

syringe_pu is the syringe pump, but I would suggest changing the component names to volume, rate and run rather than x1, x2, x3


matt notes:
- "value" parameters dont seem to work on syringe pump, but the start/stop commands do, so we'll use time and the syringe diameter (defined manually on the syringe pump) to control our rate and volume dispensing
- files are not saved properly, we'll deal with that later

'''



def alignment_blade_coating_2024_2(coating_start_pos, measurement_pos,th):

    yield from bps.mv(thorlabs_su, measurement_pos)
    yield from alignement_gisaxs_hex(angle=th)

    yield from bps.mvr(stage.th, th)
    yield from bps.mvr(stage.y, 0.05)

    yield from bps.mv(thorlabs_su, coating_start_pos)







def blade_coating_2024_2(sample_name='bladecoating', coating_start_pos=10, measurement_pos=87, th=0.16, dets = [pil1M, pil900KW]):
    # dets = ['pil900KW','pil1M']

    yield from shopen()
    yield from bps.sleep(1)
    yield from shopen()
    yield from bps.sleep(1)
    yield from shopen()
    yield from bps.sleep(2)
    
    yield from bps.mv(thorlabs_su, thorlabs_su.position)
    yield from alignment_blade_coating_2024_2(coating_start_pos, measurement_pos,th)

    #det_exposure_time(0.5,300)
    det_exposure_time(2, 600)
    sample_id(user_name='ML', sample_name=sample_name)
    yield from bps.mv(syringe_pu.x3, 1) 
    yield from bps.sleep(2.5)
    yield from bps.mv(syringe_pu.x4, 1)
    
    yield from bps.mv(thorlabs_su, measurement_pos)
    
    
    yield from bp.count(dets)

    yield from shclose()
    yield from bps.sleep(1)
    yield from shclose()
    yield from bps.sleep(1)
    yield from shclose()



def take_data():
    
    det_exposure_time(0.5,10)
    yield from bp.count([pil1M])



    
def syringe_pump_testing():
    yield from bps.mv(syringe_pu.go, 1) 
    yield from bps.sleep(2.5)
    yield from bps.mv(syringe_pu.stop_flow, 1)


def thorlabs_testing():
    yield from bps.mv(thorlabs_su, thorlabs_su.position)
    yield from bps.mv(thorlabs_su, 87)
    yield from bps.mv(thorlabs_su, 10)


def saxs_hardxray_inair_capillaries_2024_2(t=0.5):
    """
    307830_Su June 25, 2024
    MRL, in-air environemtn (same AgB as blade coating stage)
    moving the hexapod stage instead of SmarAct

    more capillaries and thin films on the morning (2am) of june 27, MRL
    """

    dets = [pil1M]

 
    # sample names
    names = ['tulasi03a-pos1', 'tulasi03a-pos2',  'tulasi02b-pos1', 'tulasi02b-pos2', 'tulasi02a-pos1', 'tulasi02a-pos2']
    x_hexa = [            1.0,              1.2,               7.5,              7.5,             13.7,             13.7]
    y_hexa = [            0.2,              1.5,                 0,              1.5,                0,              2.2]
    z_hexa = [            0.1,                0,                 0,                0,                0,                0]

    names = ['tulasi01b-pos1', 'tulasi01b-pos2',  'tulasi01a-pos1', 'tulasi01a-pos2', 'tulasi01a-pos3']
    x_hexa = [            1.2,              1.2,               7.0,              7.4,              7.7]
    y_hexa = [            0.2,              2.0,               1.4,             -7.5,             -8.8]
    z_hexa = [            0.1,                0,                 0,                0,                0]

    names     = [         'mostafa00',       'mostafa01', 'mostafa02', 'mostafa03', 'mostafa04', 'mostafa05', 'mostafa06', 'mostafa07', 
                 'tulasi-kapton-ctrl', 'tulasi-kapton-01a', 'tulasi-kapton-01b', 'tulasi-kapton-02a' ]
    x_smaract = [               19000,              8000,        1000,       -7000,      -14000,      -22000,      -27000,      -33000,
                               -37000,              -40000,              -46500,              -54500 ]
    y_smaract = [               -7000,             -7000,       -7000,       -7000,       -7000,       -7000,       -7000,       -7000,
                                -7000,               -7000,               -6500,               -5500 ]
   

    for name, xs_smaract, ys_smaract in zip(names, x_smaract, y_smaract):
        #yield from bps.mv(stage.x, xs_hexa)
        #yield from bps.mv(stage.y, ys_hexa)

        yield from bps.mv(piezo.x, xs_smaract)
        yield from bps.mv(piezo.y, ys_smaract)

        det_exposure_time(t, t)

        name_fmt = "{sample}_8.3m_16100.0eV"

        sample_name = name_fmt.format(sample=name)
        sample_id(user_name="ML", sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")

        yield from bp.count([pil1M], num=1)










def alignment_static_swaxs_2024_2(th=0.16):

    yield from bps.mv(thorlabs_su, thorlabs_su.position)
    yield from alignement_gisaxs_hex(angle=th)

    yield from bps.mvr(stage.th, th)
    yield from bps.mvr(stage.y, 0.05)















def waxs_hardxray_inair_2024_2(t=1):


    dets = [pil900KW]

 
    # sample names
    names     = ['tulasi-kapton-ctrl', 'tulasi-kapton-01a', 'tulasi-kapton-01b', 'tulasi-kapton-02a' ]
    x_smaract = [              -37000,              -40000,              -46500,              -54500 ]
    y_smaract = [               -7000,               -7000,               -6500,               -5500 ]
    
    
    names =     ['alaska-filter1a', 'alaska-filter1a-acid', 'alaska-filter1b', 'alaska-filter3a-pristine',       
                 'alaska-filter3b-fouled', 'alaska-filter3b-acid' ]
    x_smaract = [            17000,                    3000,             -5000,                     -18500,
                                   -27000,                 -33500 ]
    y_smaract = [            -1000,                   -1000,             -1000,                      -1000,
                                    -1000,                  -1000 ]


    names = ['AgB-thinfilm']
    x_smaract = [-40000]
    y_smaract = [-500]



    waxs_arc = [0, 20, 40]
    
    
    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)

        for name, xs_smaract, ys_smaract in zip(names, x_smaract, y_smaract):
            #yield from bps.mv(stage.x, xs_hexa)
            #yield from bps.mv(stage.y, ys_hexa)

            yield from bps.mv(piezo.x, xs_smaract)
            yield from bps.mv(piezo.y, ys_smaract)

            det_exposure_time(t, t)

            name_fmt = "{sample}_8.3m_16100.0eV_wa{wax}"

            sample_name = name_fmt.format(sample=name, wax=wa)
            sample_id(user_name="ML", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")

            yield from bp.count([pil900KW], num=1)



def saxs_hardxray_inair_june27_2024_2(t=1):


    dets = [pil1M]

 
    # sample names
    names =     ['kapton-psp4vp-ctrl', 'kapton-psp4vp-20wt', 'kapton-ctrl']
    x_smaract = [              -35000,                -5000,         20000]
    y_smaract = [               -1500,                -1500,         -1500]



    names     = ['105D6-20CuAc',  '105D5-20CuAc',      '105Z-20CuAc']
    x_smaract = [-46000, -22000, 7000 ]
    y_smaract = [-6500, -7500, -7000 ]


    waxs_arc = [40]
    
    
    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)

        for name, xs_smaract, ys_smaract in zip(names, x_smaract, y_smaract):
            #yield from bps.mv(stage.x, xs_hexa)
            #yield from bps.mv(stage.y, ys_hexa)

            yield from bps.mv(piezo.x, xs_smaract)
            yield from bps.mv(piezo.y, ys_smaract)

            det_exposure_time(t, t)

            name_fmt = "{sample}_8.3m_16100.0eV_wa{wax}"

            sample_name = name_fmt.format(sample=name, wax=wa)
            sample_id(user_name="ML", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")

            yield from bp.count([pil1M], num=1)





def acq_delay(dets,exp_time,delay,num):
    det_exposure_time(exp_time,exp_time)
    yield from bp.count(dets,num,delay)


def blade_coating_acqdelay_2024_2(sample_name='bladecoating', coating_start_pos=10, measurement_pos=87, th=0.16, dets = [pil1M, pil900KW]):
    # dets = ['pil900KW','pil1M']

    # yield from shopen()
    # yield from bps.sleep(1)
    # yield from shopen()
    # yield from bps.sleep(1)
    # yield from shopen()
    # yield from bps.sleep(2)
    
    yield from bps.mv(thorlabs_su, thorlabs_su.position)
    yield from alignment_blade_coating_2024_2(coating_start_pos, measurement_pos,th)

    #det_exposure_time(0.5,300)
    
    sample_id(user_name='ML', sample_name=sample_name)
    yield from bps.mv(syringe_pu.go, 1) # start pump 
    yield from bps.sleep(2.5)
    yield from bps.mv(syringe_pu.stop_flow, 1) # stop pump
    
    yield from bps.mv(thorlabs_su, measurement_pos)
    
    yield from acq_delay(dets=dets, exp_time=0.5, delay=5, num=300)

    # yield from shclose()
    # yield from bps.sleep(1)
    # yield from shclose()
    # yield from bps.sleep(1)
    # yield from shclose()











def swaxs_Br_edge_capillaries_2024_2(t=1):
    """
    315602 June 28, 2024
    MRL
    """

    dets = [pil900KW]

    names = [ 'carly01', 'carly02', 'carly03', 'carly04', 'carly05', 'carly06', 'carly07', 'carly08', 'carly09']
    x =     [    -43700,    -37400,    -31100,    -24800,    -18500,    -12000,     -5700,       700,     7050 ]
    y =     [     -6000,     -4620,     -4620,     -4620,     -4620,     -4620,     -4620,     -4620,    -4620 ]
    z =     [      2000,      2000,      2000,      2000,      2000,      2000,      2000,      2000,     2000 ]
 
    energies_swaxs = np.asarray(np.arange(13440, 13460, 5).tolist() +
                          np.arange(13460, 13480, 2).tolist() +
                          np.arange(13490, 13520, 10).tolist() )
    
    energies_swaxs_add = np.asarray([13420, 13480, 13485 ])
    
    energies_nexafs = np.asarray(np.arange(13440, 13520, 2))



    waxs_arc_swaxs = [0, 20, 40]
    waxs_arc_nexafs = [40]

    waxs_arc = waxs_arc_swaxs
    energies = energies_swaxs_add


    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)

        for name, xs, ys in zip(names, x, y):
            # changing ys to allow for more room during dense energy scan
            yield from bps.mv(piezo.x, xs)
            yield from bps.mv(piezo.y, ys)

            yss = np.linspace(ys, ys + 1500, len(energies))
            xss = np.array([xs])

            yss, xss = np.meshgrid(yss, xss)
            yss = yss.ravel()
            xss = xss.ravel()



            det_exposure_time(t, t)

            name_fmt = "{sample}_4.0m_{energy}eV_wa{wax}_bpm{xbpm}"
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

                sample_name = name_fmt.format(sample=name, energy="%6.2f" % e, wax=wa, xbpm="%4.3f"%bpm)
                sample_id(user_name="ML", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")

                yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 13480)
            yield from bps.mv(energy, 13440)





def swaxs_hardxray_kelvin_2024_3(t=1):
    """
    314483_Freychet_03 Sept 16, 2024
    """

    dets = [pil1M, pil900KW]

    names = [   'kl-blank',  'kl-nafion','kl-nf-p5-0.5', 'kl-nf-p5-2.0', 'kl-nf-p30-2.0', 'kl-nf-p30-0.5', 
             'kl-ahpp25-4','kl-ahpp25-2', 'kl-ahpp25-1','kl-ahpp25-0.5','kl-ahpp25-0.25',
             'kl-nf-p25-4','kl-nf-p25-2', 'kl-nf-p25-1','kl-nf-p25-0.5','kl-nf-p25-0.25', 
              'sj-ppion-k','sj-ppionzrox-k', 'sj-bkg-k']
        
    x =     [        44700,        36300,         28300,          19900,           12500,            4800, 
                     -3200,       -11000,        -19000,         -26600,          -34600, 
                     44500,        36500,         28500,          21000,           13100,
                      1100,       -15900,        -39900]
    y =     [        -6400,        -6800,         -6900,          -7100,           -7300,           -7300, 
                     -7300,        -7700,         -7700,          -8000,           -8000,
                      6500,         6000,          5700,           5700,            5700,
                      5700,         5700,          5700]
    z =     [         2800,         2800,          2800,           2800,            2800,            2800, 
                      2800,         2800,          2800,           2800,            2800,  
                      2800,         2800,          2800,           2800,            2800,
                      2800,         2800,          2800]

    assert len(names) == len(x), f"len of x ({len(x)}) is different from number of samples ({len(names)})"
    assert len(names) == len(y), f"len of y ({len(y)}) is different from number of samples ({len(names)})"
    assert len(names) == len(z), f"len of y ({len(z)}) is different from number of samples ({len(names)})"

    det_exposure_time(t, t)
    waxs_arc = [0, 20, 40]

    for name, xs, ys, zs in zip(names, x, y, z):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)

            for l, yy in enumerate([-100, 0, 100]):
                yield from bps.mv(piezo.y, ys+yy)
                yield from bps.sleep(1)

                name_fmt = "{sample}_3.0m_16100.0eV_pos{pos}_wa{wax}"

                sample_name = name_fmt.format(sample=name, pos=l, wax=wa)
                sample_id(user_name="GS", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")

                yield from bp.count(dets, num=1)


def swaxs_sedge_kelvin_2024_3(t=1):
    """
    314483_Freychet_03 Sept 16, 2024
    """

    dets = [pil1M, pil900KW]

    names = [   'kl-blank',  'kl-nafion','kl-nf-p5-0.5', 'kl-nf-p5-2.0', 'kl-nf-p30-2.0', 'kl-nf-p30-0.5', 
             'kl-ahpp25-4','kl-ahpp25-2', 'kl-ahpp25-1','kl-ahpp25-0.5','kl-ahpp25-0.25',
             'kl-nf-p25-4','kl-nf-p25-2', 'kl-nf-p25-1','kl-nf-p25-0.5','kl-nf-p25-0.25']
        
    x =     [        44700,        36100,         28300,          19900,           12500,            4800, 
                     -3200,       -11000,        -19000,         -26600,          -34600, 
                     44500,        36500,         28500,          21000,           13100]
    y =     [        -7200,        -7300,         -7500,          -7700,           -7600,           -7600, 
                     -7300,        -7700,         -7700,          -7800,           -7800,
                      5700,         5700,          5200,           5200,            5200]
    z =     [         2800,         2800,          2800,           2800,            2800,            2800, 
                      2800,         2800,          2800,           2800,            2800,  
                      2800,         2800,          2800,           2800,            2800]

    assert len(names) == len(x), f"len of x ({len(x)}) is different from number of samples ({len(names)})"
    assert len(names) == len(y), f"len of y ({len(y)}) is different from number of samples ({len(names)})"
    assert len(names) == len(z), f"len of y ({len(z)}) is different from number of samples ({len(names)})"

    det_exposure_time(t, t)

    energies = 7 + np.asarray(np.arange(2445, 2470, 5).tolist() + np.arange(2470, 2480, 0.25).tolist() + np.arange(2480, 2490, 1).tolist()
                              + np.arange(2490, 2500, 5).tolist()+ np.arange(2500, 2521, 10).tolist())
    
    waxs_arc = [0, 20]

    for name, xs, ys in zip(names, x, y):
        # changing ys to allow for more room during dense energy scan
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)

        yss = np.linspace(ys, ys + 1000, len(energies))
        xss = np.array([xs])

        yss, xss = np.meshgrid(yss, xss)
        yss = yss.ravel()
        xss = xss.ravel()

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)

            det_exposure_time(t, t)

            name_fmt = "{sample}_3.0m_{energy}eV_wa{wax}_bpm{xbpm}"
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

                sample_name = name_fmt.format(sample=name, energy="%6.2f" % e, wax=wa, xbpm="%4.3f"%bpm)
                sample_id(user_name="GS", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")

                yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 2470)
            yield from bps.mv(energy, 2450)


def nexafs_Zr_edge_greg_2024_1(t=1):
    """
    307830_Su Feb 2, 2024
    """

    dets = [pil900KW, pil1M]

    names = ['sj-ppionzrox-k', 'sj-ppion-k']
    x =     [          -15900,        -8900]
    y =     [            5700,         5700]

    names = ['sj-bkg-k']
    x =     [          -39900]
    y =     [            5700]


    det_exposure_time(t, t)

    energies = np.linspace(17970, 18070, 51)
    
    waxs_arc = [0, 20, 40]

    for name, xs, ys in zip(names, x, y):
        # changing ys to allow for more room during dense energy scan
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)

        yss = np.linspace(ys, ys + 0, len(energies))
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
                yield from bps.sleep(5)

                bpm = xbpm3.sumX.get()

                sample_name = name_fmt.format(sample=name, energy="%6.2f" % e, wax=wa, xbpm="%4.4f"%bpm)
                sample_id(user_name="GS", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")

                yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 18030)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 18000)
            yield from bps.sleep(2)




def Zr_edge_giswaxs_measurments_2024_3(t=1):
    dets = [pil900KW, pil1M]
    det_exposure_time(t, t)

    names = ['sj-ppionzrox-m-post', 'sj-ppionzrox-m-ox', 'sj-ppionzrox-m-pre', 'sj-ppion-m-ox', 
                 'sj-bkg-m-coated',     'sj-bkg-m-bare',    'sj-ppionzrox-si',   'sj-ppion-si', 'sj-bkg-si']
    x_piezo = [              55000,                55000,                48000,          37700,
                             26700,               17400,                 2500,          -13500,      -30500]
    x_hexa = [                  14,                 4.3,                    0,               0,
                                0,                    0,                    0,               0,           0]
    y_piezo = [               8400,                8200,                 8000,            7800,
                              7700,                7500,                 6500,            6300,        6000]
    z_piezo = [               2700,                2700,                 2700,            2700,
                              2700,                2700,                 2700,            2700,        2700]
       
    names = ['sj-ppionzrox-si',   'sj-ppion-si', 'sj-bkg-si']
    x_piezo = [           2500,          -13500,      -30500]
    x_hexa = [               0,               0,           0]
    y_piezo = [           6500,            6300,        6000]
    z_piezo = [           2700,            2700,        2700]
       

    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(z_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexa)})"

    energies = np.linspace(17970, 18070, 51)

    waxs_arc = [0, 20, 40]
    ai0_all = 0
    ai_list = [0.15]

    for name, xs, ys, zs, xs_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa):
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)

        yield from bps.mv(piezo.th, ai0_all)
        yield from alignement_gisaxs_rough(0.1)

        ai0 = piezo.th.position
        det_exposure_time(t, t)

        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)
            # Do not take SAXS when WAXS detector in the way

            yield from bps.mv(piezo.x, xs)

            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                name_fmt = "{sample}_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 5:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    
                    bpm = xbpm3.sumX.get()
                    sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)
                
                yield from bps.mv(energy, 18030)
                yield from bps.sleep(2)
                yield from bps.mv(energy, 18000)
                yield from bps.sleep(2)

            yield from bps.mv(piezo.th, ai0)




def giwaxs_S_edge_Su_2024_3(t=1):
 

    names = [  'GI_P25_4', 'GI_P25_2', 'GI_P25_1', 'GI_P25_0p5', 'GI_P25_0p25', 'GI_AHPP25_4', 'GI_AHPP25_2', 'GI_AHPP25_1', 'GI_AHPP25_0p5', 'GI_AHPP25_0p25',
               'GI_P5A_4', 'GI_P5A_2', 'GI_P5A_1', 'GI_P5A_0p5', 'GI_P5A_0p25', 'GI_AHPP5A_4', 'GI_AHPP5A_2', 'GI_AHPP5A_1', 'GI_AHPP5A_0p5', 'GI_AHPP5A_0p25']             
    x_piezo = [     54000,      54000,      40000,        25000,         15000,         -2000,        -15000,        -29000,          -42000,           -48000, 
                    55000,      52000,      40000,        25000,         15000,          4000,         -8000,        -24000,          -37000,           -48000]  
    x_hexa = [         15,          0,          0,            0,             0,             0,             0,             0,                0,              -8, 
                       15,          0,          0,            0,             0,             0,             0,             0,                0,              -8] 
    y_piezo = [      6800,       6800,       6800,         6800,          6800,          6800,          6800,          6800,             6800,            6800,
                    -2700,      -2700,      -2700,        -2700,         -2700,         -2700,         -2700,         -2700,            -2700,           -2700] 
    
    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexa)})"

    waxs_arc = [7, 20]
    ai0_all = 0
    ai_list = [1.0]

    energies = 7 + np.asarray(np.arange(2445, 2470, 5).tolist() + np.arange(2470, 2480, 0.5).tolist() + np.arange(2480, 2490, 2).tolist()
                            + np.arange(2490, 2500, 5).tolist()+ np.arange(2500, 2521, 10).tolist())

    xstep = 20

    for name, xs, ys, xs_hexa in zip(names, x_piezo, y_piezo, x_hexa):
        yield from bps.mv(stage.x, xs_hexa,
                          piezo.x, xs,
                          piezo.y, ys)

        yield from bps.mv(piezo.th, ai0_all)
        yield from alignement_gisaxs_doblestack(0.3)

        ai0 = piezo.th.position
        det_exposure_time(t, t)
        
        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)

            if wa ==0:
                dets = [pil900KW]
            else:
                dets = [pil900KW, pil1M]

            # Do not take SAXS when WAXS detector in the way

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
                    
                    yield from bps.mv(piezo.x, xs - counter * xstep)
                    counter += 1
                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="GS", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)
                
                yield from bps.mv(energy, 2500)
                yield from bps.sleep(2)
                yield from bps.mv(energy, 2480)
                yield from bps.sleep(2)
                yield from bps.mv(energy, 2445)

            yield from bps.mv(piezo.th, ai0)





def giwaxs_hardxray_Kelvin_2024_3(t=1):

    # In Freychet_11
    # names = [  'GI_P25_4', 'GI_P25_2', 'GI_P25_1', 'GI_P25_0p5', 'GI_P25_0p25', 'GI_AHPP25_4', 'GI_AHPP25_2', 'GI_AHPP25_1', 'GI_AHPP25_0p5', 'GI_AHPP25_0p25',
    #            'GI_P5A_4', 'GI_P5A_2', 'GI_P5A_1', 'GI_P5A_0p5', 'GI_P5A_0p25', 'GI_AHPP5A_4', 'GI_AHPP5A_2', 'GI_AHPP5A_1', 'GI_AHPP5A_0p5', 'GI_AHPP5A_0p25']             
    # x_piezo = [     54000,      54000,      40000,        25000,         15000,         -2000,        -15000,        -29000,          -42000,           -48000, 
    #                 55000,      52000,      40000,        25000,         15000,          4000,         -8000,        -24000,          -37000,           -48000]  
    # x_hexa = [         15,          0,          0,            0,             0,             0,             0,             0,               0,               -8, 
    #                    15,          0,          0,            0,             0,             0,             0,             0,               0,               -8] 
    # y_piezo = [      6800,       6800,       6800,         6800,          6800,          6800,          6800,          6800,            6800,             6800,
    #                 -1500,      -1500,      -1500,        -1500,         -1500,         -1500,         -1500,         -1500,           -1500,            -1500] 
    
    names = ['sj-ppionzrox-m-post', 'sj-ppionzrox-m-ox', 'sj-ppionzrox-m-pre', 'sj-ppion-m-ox', 
                 'sj-bkg-m-coated',     'sj-bkg-m-bare']
    x_piezo = [              53800,               53900,                48700,           37900,
                             26900,               16400]
    x_hexa = [                  14,                 4.3,                    0,               0,
                                0,                    0]
    y_piezo = [               7300,                7300,                 7300,            7300,
                              7300,                7200]

    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexa)})"

    waxs_arc = [7, 20]
    ai0_all = -1
    ai_list = [0.10, 0.12, 0.15, 0.20]
    xstep = 0


    for name, xs, ys, xs_hexa in zip(names, x_piezo, y_piezo, x_hexa):
        yield from bps.mv(stage.x, xs_hexa,
                          piezo.x, xs,
                          piezo.y, ys)

        yield from bps.mv(piezo.th, ai0_all)
        yield from alignement_gisaxs_doblestack(0.15)

        ai0 = piezo.th.position
        det_exposure_time(t, t)
        
        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)

            if wa ==0:
                dets = [pil900KW]
            else:
                dets = [pil900KW, pil1M]

            # Do not take SAXS when WAXS detector in the way

            counter = 0
            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                name_fmt = "{sample}_{energy}eV_ai{ai}_wa{wax}"
                
                yield from bps.mv(piezo.x, xs - counter * xstep)
                counter += 1
                e=energy.energy.position
                sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa)
                sample_id(user_name="GS", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

            yield from bps.mv(piezo.th, ai0)



def nexafs_As_edge_matt_2024_1(t=1):
    """
    307830_Su Feb 2, 2024
    """

    dets = [pil900KW]


    names = ['sludge_filter_pristine',        'sludge_filter_1C',       'sludge_filter_2C','jartest_filter_ctrl_0.2',
            'jartest_filter_expD_0.2','jartest_filter_expD_0.45','jartest_filter_expD_1.2',  'jartest_filter_expD_5',
               'housefilter_pristine',        'housefilter_H2F1',       'housefilter_H2F2',       'housefilter_H6F1',
                   'housefilter_H6F2',       'housefilter_H11F2']
    x =     [                   42000,                     36000,                    31000,                    25000, 
                                20000,                     15000,                     9500,                     4000,
                                -4000,                    -13000,                   -19000,                   -27000,
                               -35000,                    -39000]
    y =     [                   -2000,                     -2000,                    -2000,                    -2000,
                                -2000,                     -2000,                    -2000,                    -2000,
                                -2000,                     -2000,                    -2000,                    -2000,
                                -2000,                     -2000]

    det_exposure_time(t, t)

    # waxs_arc = [0, 20, 40]


    # for wa in waxs_arc:
    #     yield from bps.mv(waxs, wa)

    #     if wa==0:
    #         dets = [pil900KW]

    #     else:
    #         dets = [pil900KW, pil1M]

    #     det_exposure_time(t, t)
    
    #     for name, xs, ys in zip(names, x, y):
    #         yield from bps.mv(piezo.x, xs)
    #         yield from bps.mv(piezo.y, ys)

    #         name_fmt = "{sample}_{energy}eV_wa{wax}_bpm{xbpm}"
    #         bpm = xbpm3.sumX.get()

    #         e = energy.energy.position
    #         sample_name = name_fmt.format(sample=name, energy="%6.2f" % e, wax=wa, xbpm="%4.4f"%bpm)
    #         sample_id(user_name="GS", sample_name=sample_name)
    #         print(f"\n\t=== Sample: {sample_name} ===\n")

    #         yield from bp.count(dets, num=1)


    dets = [pil900KW]

    energies = np.asarray(np.arange(11850, 11865, 5).tolist() + np.arange(11865, 11873, 1).tolist() 
    + np.arange(11873, 11885, 0.5).tolist() + np.arange(11885, 11895, 1).tolist()+ np.arange(11895, 11930, 5).tolist())
    
    waxs_arc = [40]

    for name, xs, ys in zip(names[3:], x[3:], y[3:]):
        # changing ys to allow for more room during dense energy scan
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)

        yss = np.linspace(ys, ys + 0, len(energies))
        xss = np.array([xs])

        yss, xss = np.meshgrid(yss, xss)
        yss = yss.ravel()
        xss = xss.ravel()

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)

            det_exposure_time(t, t)

            name_fmt = "nexafs_{sample}_{energy}eV_wa{wax}_bpm{xbpm}"
            for e, xsss, ysss in zip(energies, xss, yss):

                energy.move(e)
                yield from bps.sleep(5)

                bpm = xbpm3.sumX.get()

                sample_name = name_fmt.format(sample=name, energy="%6.2f" % e, wax=wa, xbpm="%4.4f"%bpm)
                sample_id(user_name="GS", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")

                yield from bp.count(dets, num=1)
            
            energy.move(11870)
            yield from bps.sleep(5)
            energy.move(11850)
            yield from bps.sleep(5)



    for name, xs, ys in zip(names, x, y):
        # changing ys to allow for more room during dense energy scan
        yield from bps.mv(piezo.x, xs+100)
        yield from bps.mv(piezo.y, ys+200)

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)

            det_exposure_time(t, t)

            name_fmt = "nexafs_pos2_{sample}_{energy}eV_wa{wax}_bpm{xbpm}"
            for e, xsss, ysss in zip(energies, xss, yss):

                energy.move(e)
                yield from bps.sleep(5)

                bpm = xbpm3.sumX.get()

                sample_name = name_fmt.format(sample=name, energy="%6.2f" % e, wax=wa, xbpm="%4.4f"%bpm)
                sample_id(user_name="GS", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")

                yield from bp.count(dets, num=1)
            
            energy.move(11870)
            yield from bps.sleep(5)
            energy.move(11850)
            yield from bps.sleep(5)


    for name, xs, ys in zip(names, x, y):
        # changing ys to allow for more room during dense energy scan
        yield from bps.mv(piezo.x, xs-100)
        yield from bps.mv(piezo.y, ys-200)

        yss = np.linspace(ys, ys + 0, len(energies))
        xss = np.array([xs])

        yss, xss = np.meshgrid(yss, xss)
        yss = yss.ravel()
        xss = xss.ravel()

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)

            det_exposure_time(t, t)

            name_fmt = "nexafs_pos3_{sample}_{energy}eV_wa{wax}_bpm{xbpm}"
            for e, xsss, ysss in zip(energies, xss, yss):

                energy.move(e)
                yield from bps.sleep(5)

                bpm = xbpm3.sumX.get()

                sample_name = name_fmt.format(sample=name, energy="%6.2f" % e, wax=wa, xbpm="%4.4f"%bpm)
                sample_id(user_name="GS", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")

                yield from bp.count(dets, num=1)
            
            energy.move(11870)
            yield from bps.sleep(5)
            energy.move(11850)
            yield from bps.sleep(5)








# ----------------------------------------------------------------
# 2024-3


def alignment_blade_coating_2024_3(coating_start_pos, measurement_pos,th):

    yield from bps.mv(thorlabs_su, measurement_pos)
    yield from alignement_gisaxs_hex(angle=th)

    yield from bps.mvr(stage.th, th)
    yield from bps.mvr(stage.y, 0.05)

    yield from bps.mv(thorlabs_su, coating_start_pos)




def blade_coating_2024_3(sample_name='bladecoating', coating_start_pos=10, measurement_pos=87, th=0.12, dets = [pil1M, pil900KW]):
    # dets = ['pil900KW','pil1M']

    #yield from shopen()
    #yield from bps.sleep(1)
    #yield from shopen()
    #yield from bps.sleep(1)
    #yield from shopen()
    #yield from bps.sleep(2)
    
    yield from bps.mv(thorlabs_su, thorlabs_su.position)
    yield from alignment_blade_coating_2024_2(coating_start_pos, measurement_pos,th)

    det_exposure_time(0.5,300)
    #det_exposure_time(2, 600)
    sample_id(user_name='ML', sample_name=sample_name)
    yield from bps.mv(syringe_pu.go, 1) # start pump 
    yield from bps.sleep(2.5)
    yield from bps.mv(syringe_pu.stop_flow, 1) # stop pump
    
    yield from bps.mv(thorlabs_su, measurement_pos)
    
    
    yield from bp.count(dets)

    #yield from shclose()
    #yield from bps.sleep(1)
    #yield from shclose()
    yield from bps.sleep(2)
    yield from shclose()





def saxs_hardxray_capillaries_2024_3(t=0.1):
    """
    315602, Sept 29, 2024
    """

    dets = [pil1M]

    #names = [   '91N1MgAc1',  '91N1MgAc17','91N1MgAc2', '91N1CuAc01', '91N1CuAc02']
    #x =     [        -49150,        -42850,         -36550,          -30350,           -23750            ]
    #y =     [        9200,        9200,         9200,          9200,           9200           ]
    #z =     [        4800,        4800,         4800,          4800,           4800]
    #names = [   '91N1CuAc03',  '91N1CuAc04','91N1CuAc07', '27N15', '27N15CuAc']
    #x =     [        -49150,        -42850,         -36550,          -30350,           -23750            ]
    #y =     [        9200,        9200,         9200,          9200,           9200           ]
    #z =     [        4800,        4800,         4800,          4800,           4800] 
    #names = [   'Nblank',  '91N1MgAc02','91N1MgAc04','27N15CuAc3', '27N15CuAc1']
    #x =     [        -49150,        -42850,         -36550,          -30350,           -23750            ]
    #y =     [        9200,        9200,         9200,          9200,           9200           ]
    #z =     [        4800,        4800,         4800,          4800,           4800]
    #names = [   '27N15CuAc45',  '27N15CuAc6','27N1CuAc04','27N1CuAc07', '124D420']
    #x =     [        -49150,        -42850,         -36550,          -30350,           -23750            ]
    #y =     [        9200,        9200,         9200,          9200,           9200           ]
    #z =     [        4800,        4800,         4800,          4800,           4800]
    #names = [   '124D620','124D220','124D820', '124D429', '124D423']
    #x =     [        -49150,        -42850,         -36550,          -30350,           -23750            ]
    #y =     [        9200,        9200,         9200,          9200,           9200           ]
    #z =     [        4800,        4800,         4800,          4800,           4800]
    #names = [   '27N1CuA01','124D420','124D417', '124D520', '124D426']
    #x =     [        -49150,        -42850,         -36550,          -30350,           -23750            ]
    #y =     [        9200,        9200,         9200,          9200,           9200           ]
    #z =     [        4800,        4800,         4800,          4800,           4800]
    #names = [   '27N1CuA02','27N1CuAc03']
    #x =     [        -49150,        -42850]
    #y =     [        9200,        9200]
    #z =     [        4800,        4800]
    names = [   'AgB']
    x =     [        -49150]
    y =     [        9200]
    z =     [        4800]






    
    

    assert len(names) == len(x), f"len of x ({len(x)}) is different from number of samples ({len(names)})"
    assert len(names) == len(y), f"len of y ({len(y)}) is different from number of samples ({len(names)})"
    assert len(names) == len(z), f"len of y ({len(z)}) is different from number of samples ({len(names)})"

    det_exposure_time(t, t)

    for name, xs, ys, zs in zip(names, x, y, z):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)

        

        name_fmt = "{sample}_9.2m_16100.0eV_"

        sample_name = name_fmt.format(sample=name)
        sample_id(user_name="ML", sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")

        yield from bp.count(dets, num=1)











# switch from blade coating to ex situ samples





def swaxs_hardxray_mrl_2024_3(t=1):
    """
    315602_Su_8    Sept 30, 2024
    """

    dets = [pil1M, pil900KW]

    names = [   'capillary-jd11',  'capillary-jd10', 'capillary-jd9', 'capillary-jd8', 'capillary-jd7', 'capillary-jd6',
                'capillary-jd5',  'capillary-jd4', 'capillary-jd3', 'capillary-jd2', 'capillary-jd1', 'capillary-AgB']
        
    x =     [             -40149,       -34150,        -27650,         -21649,          -15149,          -9149,
                          -1950,         4050,          10050,         17250,            22649,           29250
                     ]
    y =     [              7200,         7200,         7200,            7100,             7200,           7200,
                           7200,         7200,         7200,            7200,             7200,           7700
                     ]
    z =     [              4801,         4801,          4801,           4801,            4801,            4801, 
                           4801,         4801,          4801,           4801,            4801,            4801
                     ]

    assert len(names) == len(x), f"len of x ({len(x)}) is different from number of samples ({len(names)})"
    assert len(names) == len(y), f"len of y ({len(y)}) is different from number of samples ({len(names)})"
    assert len(names) == len(z), f"len of y ({len(z)}) is different from number of samples ({len(names)})"

    det_exposure_time(t, t)
    waxs_arc = [0, 20, 40]

    for name, xs, ys, zs in zip(names, x, y, z):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)

            for l, yy in enumerate([-100, 0, 100]):
                yield from bps.mv(piezo.y, ys)
                yield from bps.sleep(1)

                name_fmt = "{sample}_6.0m_16100.0eV_pos{pos}_wa{wax}"

                sample_name = name_fmt.format(sample=name, pos=l, wax=wa)
                sample_id(user_name="ML", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")

                yield from bp.count(dets, num=1)



def swaxs_hardxray_mrl_v2_2024_3(t=1):
    """
    315602_Su_8    Sept 30, 2024
    switched for loops for sample position and waxs arc to make scans faster (go to one waxs position, run all samples, then move waxs arc)
    """

    dets = [pil1M, pil900KW]

    #names = [   'capillary-jd11',  'capillary-jd10', 'capillary-jd9', 'capillary-jd8', 'capillary-jd7', 'capillary-jd6',
    #            'capillary-jd5',  'capillary-jd4', 'capillary-jd3', 'capillary-jd2', 'capillary-jd1', 'capillary-AgB']
    #x =     [             -40149,       -34150,        -27650,         -21649,          -15149,          -9149,
    #                      -1950,         4050,          10050,         17250,            22649,           29250]
    #y =     [              7200,         7200,         7200,            7100,             7200,           7200,
    #                       7200,         7200,         7200,            7200,             7200,           7700]
    #z =     [              4801,         4801,          4801,           4801,            4801,            4801, 
    #                       4801,         4801,          4801,           4801,            4801,            4801]

    # mrl alaska bar 1 
    #names = ['sludge_filter_pristine',        'sludge_filter_1C',       'sludge_filter_2C','jartest_filter_ctrl_0.2',
    #        'jartest_filter_expD_0.2','jartest_filter_expD_0.45','jartest_filter_expD_1.2',  'jartest_filter_expD_5',
    #           'housefilter_pristine',        'housefilter_H2F1',       'housefilter_H2F2',       'housefilter_H6F1',
    #               'housefilter_H6F2',       'housefilter_H11F2']
    #x =     [                   33000,                     26000,                    21000,                    15000, 
    #                            10000,                     5000,                     -500,                     -6000,
    #                            -14000,                    -21000,                   -30000,                   -38000,
    #                           -45000,                    -49000]
    #y =     [                   -2500,                     -2500,                    -2500,                    -2500,
    #                            -2500,                     -2500,                    -2500,                    -2500,
    #                            -2500,                     -3000,                    -3000,                    -3000,
    #                            -3000,                     -3000]
    #z =     [                   4800,                     4800,                    4800,                    4800,
    #                            4800,                     4800,                    4800,                    4800,
    #                            4800,                     4800,                    4800,                    4800,
    #                            4800,                     4800]


    # mrl alaska bar 2 
    #names = [      'housefilter_H8F1',        'housefilter_H8F2',       'housefilter_H7F1',      'housefilter_H7F2',
     #              'housefilter_H5F1',        'housefilter_H5F2',       'housefilter_H4F1',       'housefilter_H4F2',
     #              'housefilter_H3F1',        'housefilter_H3F2',       'housefilter_H9F1',       'housefilter_H10F4',
     #              'housefilter_H10F1',  'jartest_filter_expG_02um', 'jartest_filter_expF_02um']
    #x =     [                   32000,                     24300,                    18700,                    12100, 
    #                            6700,                     1100,                     -3100,                     -8900,
    #                            -14200,                    -18700,                   -26200,                   -33900,
    #                           -39900,                    -45900,                      -52000    ]

   # y =     [                   500,                     500,                    500,                    500,
   #                             500,                     500,                    500,                    500,
   #                             500,                     500,                    500,                    500,
   #                             500,                     500,                    500       ]

  #  z =     [                   4800,                     4800,                    4800,                    4800,
  #                              4800,                     4800,                    4800,                    4800,
  #                              4800,                     4800,                    4800,                    4800,
  #                              4800,                     4800,                    4800       ]



    # supriya transmission bar
    names = [      'SG1',        'SG2',       'SG3',      'SG4',
                   'SG5',        'SG6',       'SG7',       'SG8',
                   'SG9',     ]
    

    x =     [      33600,       26400,        18600,       13200, 
                    5900,       -2100,        -10100,     -17900,
                   -26000    ]
    
    y =     [      -200,       -200,        700,       700, 
                    700,        700,        500,      1200,
                   1200    ]
    
    z =     [      4800,       4800,        4800,       4800, 
                   4800,       4800,        4800,       4800,
                   4800    ]









    assert len(names) == len(x), f"len of x ({len(x)}) is different from number of samples ({len(names)})"
    assert len(names) == len(y), f"len of y ({len(y)}) is different from number of samples ({len(names)})"
    assert len(names) == len(z), f"len of y ({len(z)}) is different from number of samples ({len(names)})"

    det_exposure_time(t, t)
    waxs_arc = [0, 20, 40]

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)
    
        for name, xs, ys, zs in zip(names, x, y, z):
            yield from bps.mv(piezo.x, xs)
            yield from bps.mv(piezo.y, ys)
            yield from bps.mv(piezo.z, zs)

            for l, yy in enumerate([-100, 0, 100]):
                yield from bps.mv(piezo.y, ys)
                yield from bps.sleep(1)

                name_fmt = "{sample}_6.0m_16100.0eV_pos{pos}_wa{wax}_1sec"

                sample_name = name_fmt.format(sample=name, pos=l, wax=wa)
                sample_id(user_name="ML", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")

                yield from bp.count(dets, num=1)





def nexafs_Ag_edge_Su_2024_3(t=0.2):
    """
    NEXAFS and SAXS at 40 deg across Ag L3 edge
    """

    user_name = "ML"

    # fourth bar: final bar, scattering and some additional scans for other edges
    # names = ["Ag_poly","AgNO3_ref"]
    # piezo_x = [-26000, -39000]
    # piezo_y = [  1000,    900]


    names = ["rough_nexafs_redo_AgNO3_ref"]
    piezo_x = [ -38200]
    piezo_y = [900]

    names = ["Ag_poly"]
    piezo_x = [-26000]
    piezo_y = [  1000]

    waxs_arc = [40]
    # to move piezo x slightly for different waxs angles
    waxs_piezo_x_offset = 200  # um
    det_exposure_time(t, t)

    assert len(piezo_x) == len(names), f"Number of piezo x coordinates ({len(piezo_x)}) is different from number of samples ({len(names)})"
    assert len(piezo_x) == len(piezo_y), f"Number of piezo x coordinates ({len(piezo_x)}) is different tan number of piezo y coordinates ({len(piezo_y)})"
    assert len(piezo_y) == len(names), f"Number of piezo y coordinates ({len(piezo_y)}) is different from number of samples ({len(names)})"

    # Check and correct sample names just in case
    names = [n.translate({ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ "}) for n in names]

    # Energies for silver L3 edge nexafs resolution
    energies = np.concatenate((np.arange(3300, 3340, 5), np.arange(3340, 3350, 2), np.arange(3350, 3390, 1), 
                               np.arange(3390, 3400, 2), np.arange(3400, 3450, 5)))


    # Go over WAXS arc positions as the sloest motor
    for i, wa in enumerate(waxs_arc):
        yield from bps.mv(waxs, wa)

        # Do not read SAXS if WAXS is in the way
        dets = [pil900KW]

        # Go over samples
        for name, xs, ys in zip(names, piezo_x, piezo_y):

            yield from bps.mv(piezo.x, xs)
            yield from bps.mv(piezo.y, ys)

            # Cover a range of 1.0 mm in y to avoid damage
            yss = np.linspace(ys, ys + 0, len(energies))

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

            yield from bps.mv(energy, 3400)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 3350)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 3300)
            yield from bps.sleep(2)





def nexafs_Fe_edge_mrl_2024_3(t=1):
    """
    315602_Su_10         Sept 30, 2024
    """

    dets = [pil900KW]


    #names = ['sludge_filter_pristine',        'sludge_filter_1C',       'sludge_filter_2C','jartest_filter_ctrl_0.2',
    #        'jartest_filter_expD_0.2','jartest_filter_expD_0.45','jartest_filter_expD_1.2',  'jartest_filter_expD_5',
    #           'housefilter_pristine',        'housefilter_H2F1',       'housefilter_H2F2',       'housefilter_H6F1',
    #               'housefilter_H6F2',       'housefilter_H11F2']
    #x =     [                   42000,                     36000,                    31000,                    25000, 
    #                            20000,                     15000,                     9500,                     4000,
    #                            -4000,                    -13000,                   -19000,                   -27000,
    #                           -35000,                    -39000]
    #y =     [                   -2000,                     -2000,                    -2000,                    -2000,
    #                            -2000,                     -2000,                    -2000,                    -2000,
    #                            -2000,                     -2000,                    -2000,                    -2000,
    #                            -2000,                     -2000]
    


    # mrl alaska bar 2 
    names = [      'housefilter_H8F1',        'housefilter_H8F2',       'housefilter_H7F1',      'housefilter_H7F2',
                   'housefilter_H5F1',        'housefilter_H5F2',       'housefilter_H4F1',       'housefilter_H4F2',
                  'housefilter_H3F1',        'housefilter_H3F2',       'housefilter_H9F1',       'housefilter_H10F4',
                   'housefilter_H10F1',  'jartest_filter_expG_02um', 'jartest_filter_expF_02um']
    x =     [                  41300 ,                     33300,                    28300,                    22300, 
                                16300,                     10700,                     6700,                     700,
                                -4800,                    -9400,                   -16700,                   -24700,
                               -30600,                    -36600,                      -41600    ]

    y =     [                   1000,                     1000,                    1000,                    1000,
                                1000,                     1000,                    1000,                    1000,
                                1000,                     1000,                    1000,                    1000,
                                1000,                     1000,                    1000       ]




    # mrl Fe K-edge 
    energies = np.concatenate((np.arange(7070, 7110, 5), 
                               np.arange(7110, 7150, 1),
                               np.arange(7150, 7160, 2), 
                               np.arange(7160, 7240, 5) ))



    waxs_arc = [40]

    for name, xs, ys in zip(names[:], x[:], y[:]):
        # changing ys to allow for more room during dense energy scan
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)

        yss = np.linspace(ys, ys + 0, len(energies))
        xss = np.array([xs])

        yss, xss = np.meshgrid(yss, xss)
        yss = yss.ravel()
        xss = xss.ravel()

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)

            det_exposure_time(t, t)

            name_fmt = "nexafs_{sample}_{energy}eV_wa{wax}_bpm{xbpm}"
            for e, xsss, ysss in zip(energies, xss, yss):

                energy.move(e)
                yield from bps.sleep(5)

                bpm = xbpm3.sumX.get()

                sample_name = name_fmt.format(sample=name, energy="%6.2f" % e, wax=wa, xbpm="%4.4f"%bpm)
                sample_id(user_name="GS", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")

                yield from bp.count(dets, num=1)
            
            energy.move(7240)
            yield from bps.sleep(5)
            energy.move(7070)
            yield from bps.sleep(5)







def nexafs_Mn_edge_mrl_2024_3(t=2):
    """
    315602_Su_11         Sept 30, 2024
    """

    dets = [pil900KW]


    #names = ['sludge_filter_pristine',        'sludge_filter_1C',       'sludge_filter_2C','jartest_filter_ctrl_0.2',
    #        'jartest_filter_expD_0.2','jartest_filter_expD_0.45','jartest_filter_expD_1.2',  'jartest_filter_expD_5',
    #           'housefilter_pristine',        'housefilter_H2F1',       'housefilter_H2F2',       'housefilter_H6F1',
    #               'housefilter_H6F2',       'housefilter_H11F2']
    #x =     [                   42000,                     36000,                    31000,                    25000, 
    #                            20000,                     15000,                     9500,                     4000,
    #                            -4000,                    -13000,                   -19000,                   -27000,
    #                           -35000,                    -39000]
    #y =     [                   -2000,                     -2000,                    -2000,                    -2000,
    #                            -2000,                     -2000,                    -2000,                    -2000,
    #                            -2000,                     -2000,                    -2000,                    -2000,
    #                            -2000,                     -2000]
    
#    names = ['sludge_filter_2C', 'jartest_filter_ctrl_0.2',
#            'jartest_filter_expD_0.2','jartest_filter_expD_0.45','jartest_filter_expD_1.2',  'jartest_filter_expD_5',
#               'housefilter_pristine',        'housefilter_H2F1',       'housefilter_H2F2',       'housefilter_H6F1',
#                   'housefilter_H6F2',       'housefilter_H11F2']
#    x =     [           31000,                    25000, 
#                        20000,                     15000,                     9500,                     4000,
#                        -4000,                    -13000,                   -19000,                   -27000,
#                        -35000,                    -39000]
#    y =     [          -2000,                    -2000,
#                        -2000,                     -2000,                    -2000,                    -2000,
#                        -2000,                     -2000,                    -2000,                    -2000,
#                        -2000,                     -2000]
    

    # mrl alaska bar 2 
    names = [      'KMnO4_ref', 'housefilter_H8F1',        'housefilter_H8F2',       'housefilter_H7F1',      'housefilter_H7F2',
                   'housefilter_H5F1',        'housefilter_H5F2',       'housefilter_H4F1',       'housefilter_H4F2',
                  'housefilter_H3F1',        'housefilter_H3F2',       'housefilter_H9F1',       'housefilter_H10F4',
                   'housefilter_H10F1' ]
    x =     [                  -37600, 41300 ,                     33300,                    28300,                    22300, 
                                16300,                     10700,                     6700,                     700,
                                -4800,                    -9400,                   -16700,                   -24700,
                               -30600    ]

    y =     [                   1000, 1000,                     1000,                    1000,                    1000,
                                1000,                     1000,                    1000,                    1000,
                                1000,                     1000,                    1000,                    1000,
                                1000  ]




    # mrl Mn K-edge 
    energies = np.concatenate((np.arange(6510, 6530, 5), 
                               np.arange(6530, 6535, 1),
                               np.arange(6535, 6555, 0.5),
                               np.arange(6555, 6570, 1),  
                               np.arange(6570, 6580, 2), 
                               np.arange(6580, 6640, 5) ))



    waxs_arc = [40]

    for name, xs, ys in zip(names[1:], x[1:], y[1:]):
        # changing ys to allow for more room during dense energy scan
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)

        yss = np.linspace(ys, ys + 0, len(energies))
        xss = np.array([xs])

        yss, xss = np.meshgrid(yss, xss)
        yss = yss.ravel()
        xss = xss.ravel()

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)

            det_exposure_time(t, t)

            name_fmt = "nexafs_{sample}_{energy}eV_wa{wax}_bpm{xbpm}"
            for e, xsss, ysss in zip(energies, xss, yss):

                energy.move(e)
                yield from bps.sleep(5)

                bpm = xbpm3.sumX.get()

                sample_name = name_fmt.format(sample=name, energy="%6.2f" % e, wax=wa, xbpm="%4.4f"%bpm)
                sample_id(user_name="ML", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")

                yield from bp.count(dets, num=1)
            
            energy.move(6640)
            yield from bps.sleep(5)
            energy.move(6510)
            yield from bps.sleep(5)






def swaxs_hardxray_jose_2025_1(t=1):
    """
    switched for loops for sample position and waxs arc to make scans faster (go to one waxs position, run all samples, then move waxs arc)
    """
    dets = [pil1M, pil900KW]


    #stage.y = 4 and stage.x = 0
    # names = ['CEM_1_K','CEM_2_K','CEM_3_K','CEM_4_K', 'AEM_1', 'AEM_2', 'AEM_3', 'AEM_4', 'AEM_2s', 'AEM_3s', 'AEM_4s']
    # x =     [    43000,    36000,    32000,    24000,   17000,   11500,    6000,     500,    -7000,   -12500,   -17500]
    # y =     [    -7000,    -7000,    -7000,    -7500,   -7000,   -7000,   -7000,   -7000,    -7000,    -7000,    -7000]
    # z =     [     3400,     3400,     3400,     3400,    3400,    3400,    3400,    3400,     3400,     3400,     3400]

    names = ['sj_ppion','sample_E','sample_EA','kapton']
    x =     [     13500,      7000,       2000,   -4000]
    y =     [      5000,      5000,       5000,    5000]
    z =     [      3400,      3400,       3400,    3400]

    assert len(names) == len(x), f"len of x ({len(x)}) is different from number of samples ({len(names)})"
    assert len(names) == len(y), f"len of y ({len(y)}) is different from number of samples ({len(names)})"
    assert len(names) == len(z), f"len of y ({len(z)}) is different from number of samples ({len(names)})"

    det_exposure_time(t, t)
    waxs_arc = [0, 20, 40]

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)
    
        for name, xs, ys, zs in zip(names, x, y, z):
            yield from bps.mv(piezo.x, xs)
            yield from bps.mv(piezo.y, ys)
            yield from bps.mv(piezo.z, zs)

            for l, xx in enumerate([-500, 0, 500]):
                yield from bps.mv(piezo.x, xs + xx)
                yield from bps.sleep(1)

                name_fmt = "{sample}_6.0m_16100.0eV_pos{pos}_wa{wax}_1sec"

                sample_name = name_fmt.format(sample=name, pos=l, wax=wa)
                sample_id(user_name="ML", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")

                yield from bp.count(dets, num=1)



def swaxs_Sedge_jose_2025_1(t=1):
    """
    switched for loops for sample position and waxs arc to make scans faster (go to one waxs position, run all samples, then move waxs arc)
    """
    dets = [pil1M, pil900KW]


    #stage.y = 4 and stage.x = 0
    names = ['CEM_1_K','CEM_2_K','CEM_3_K','CEM_4_K', 'CEM_4_K']
    x =     [    43000,    36000,    32000,    24000,    -44000]
    y =     [    -7500,    -7500,    -7500,    -7500,     -8000]
    z =     [     3400,     3400,     3400,     3400,      3400]

    assert len(names) == len(x), f"len of x ({len(x)}) is different from number of samples ({len(names)})"
    assert len(names) == len(y), f"len of y ({len(y)}) is different from number of samples ({len(names)})"
    assert len(names) == len(z), f"len of y ({len(z)}) is different from number of samples ({len(names)})"

    det_exposure_time(t, t)
    waxs_arc = [0, 20]

    energies = 7 + np.asarray(np.arange(2445, 2470, 5).tolist() + np.arange(2470, 2480, 0.5).tolist() + np.arange(2480, 2490, 2).tolist()
                            + np.arange(2490, 2500, 5).tolist()+ np.arange(2500, 2521, 10).tolist())

    yield from bps.mv(stage.y, -9)

    for name, xs, ys in zip(names, x, y):
        # changing ys to allow for more room during dense energy scan
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)

        yss = np.linspace(ys, ys + 500, len(energies))
        xss = np.array([xs])

        yss, xss = np.meshgrid(yss, xss)
        yss = yss.ravel()
        xss = xss.ravel()

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)

            det_exposure_time(t, t)

            name_fmt = "{sample}_2.0m_{energy}eV_wa{wax}_bpm{xbpm}"
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

                sample_name = name_fmt.format(sample=name, energy="%6.2f" % e, wax=wa, xbpm="%4.3f"%bpm)
                sample_id(user_name="GS", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")

                yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 2500)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 2470)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 2450)
            yield from bps.sleep(2)



def swaxs_Sedge_pierre_2025_1(t=1):
    """
    switched for loops for sample position and waxs arc to make scans faster (go to one waxs position, run all samples, then move waxs arc)
    """
    dets = [pil1M, pil900KW]


    #stage.y = 4 and stage.x = 0
    names = ['sample_E','sample_EA','kapton']
    x =     [      7000,       2000,   -4000]
    y =     [     -7500,      -7500,   -7500]
    z =     [      3400,       3400,    3400]


    assert len(names) == len(x), f"len of x ({len(x)}) is different from number of samples ({len(names)})"
    assert len(names) == len(y), f"len of y ({len(y)}) is different from number of samples ({len(names)})"
    assert len(names) == len(z), f"len of y ({len(z)}) is different from number of samples ({len(names)})"

    det_exposure_time(t, t)
    waxs_arc = [0, 20]

    energies = 7 + np.asarray(np.arange(2445, 2470, 5).tolist() + np.arange(2470, 2480, 0.5).tolist() + np.arange(2480, 2490, 2).tolist()
                            + np.arange(2490, 2500, 5).tolist()+ np.arange(2500, 2521, 10).tolist())


    yield from bps.mv(stage.y, 3)

    for name, xs, ys in zip(names, x, y):
        # changing ys to allow for more room during dense energy scan
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)

        yss = np.linspace(ys, ys + 500, len(energies))
        xss = np.array([xs])

        yss, xss = np.meshgrid(yss, xss)
        yss = yss.ravel()
        xss = xss.ravel()

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)

            det_exposure_time(t, t)

            name_fmt = "{sample}_2.0m_{energy}eV_wa{wax}_bpm{xbpm}"
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

                sample_name = name_fmt.format(sample=name, energy="%6.2f" % e, wax=wa, xbpm="%4.3f"%bpm)
                sample_id(user_name="GS", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")

                yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 2500)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 2470)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 2450)
            yield from bps.sleep(2)



def swaxs_Sedge_yunfei_2025_1(t=1):
    """
    switched for loops for sample position and waxs arc to make scans faster (go to one waxs position, run all samples, then move waxs arc)
    """
    dets = [pil1M, pil900KW]


    #stage.y = 4 and stage.x = 0
    names = [    'sa01',    'sa07',     'sa08',  'sa09']
    x =     [    -11000,    -20300,     -29400,  -38200]
    y =     [     -7200,     -6700,      -7300,   -6800]
    z =     [      3400,      3400,       3400,    3400]


    assert len(names) == len(x), f"len of x ({len(x)}) is different from number of samples ({len(names)})"
    assert len(names) == len(y), f"len of y ({len(y)}) is different from number of samples ({len(names)})"
    assert len(names) == len(z), f"len of y ({len(z)}) is different from number of samples ({len(names)})"

    det_exposure_time(t, t)
    waxs_arc = [0, 2, 20, 22]

    energies = [2460, 2470, 2472, 2474, 2475, 2476, 2477, 2478, 2480, 2490]

    yield from bps.mv(stage.y, 3)

    for name, xs, ys in zip(names, x, y):
        # changing ys to allow for more room during dense energy scan
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)

        yss = np.linspace(ys, ys, len(energies))
        xss = np.array([xs])

        yss, xss = np.meshgrid(yss, xss)
        yss = yss.ravel()
        xss = xss.ravel()

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)

            det_exposure_time(t, t)

            name_fmt = "{sample}_2.0m_{energy}eV_wa{wax}_bpm{xbpm}"
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

                sample_name = name_fmt.format(sample=name, energy="%6.2f" % e, wax=wa, xbpm="%4.3f"%bpm)
                sample_id(user_name="GS", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")

                yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 2470)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 2450)
            yield from bps.sleep(2)



def swaxs_Cledge_jose_2025_1(t=1):
    """
    switched for loops for sample position and waxs arc to make scans faster (go to one waxs position, run all samples, then move waxs arc)
    """
    dets = [pil1M, pil900KW]

    energies = np.asarray(np.arange(2800, 2820, 5).tolist() + np.arange(2820, 2823, 1.0).tolist() 
                          + np.arange(2823, 2835, 0.5).tolist() + np.arange(2835, 2845, 2).tolist()
                          + np.arange(2845, 2860, 5).tolist() + np.arange(2860, 2900, 10).tolist())



    #stage.y = 4 and stage.x = 0
    names = [ 'AEM_1', 'AEM_2', 'AEM_3', 'AEM_4', 'AEM_2s', 'AEM_3s', 'AEM_4s']
    x =     [   17000,   11500,    6000,     500,    -7000,   -12500,   -17500]
    y =     [   -7500,   -7500,   -7500,   -7500,    -8000,    -8000,    -8000]
    z =     [    3400,    3400,    3400,    3400,     3400,     3400,     3400]


    assert len(names) == len(x), f"len of x ({len(x)}) is different from number of samples ({len(names)})"
    assert len(names) == len(y), f"len of y ({len(y)}) is different from number of samples ({len(names)})"
    assert len(names) == len(z), f"len of y ({len(z)}) is different from number of samples ({len(names)})"

    det_exposure_time(t, t)
    waxs_arc = [0, 20]

    yield from bps.mv(stage.y, -9)

    for name, xs, ys in zip(names, x, y):
        # changing ys to allow for more room during dense energy scan
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)

        yss = np.linspace(ys, ys + 500, len(energies))
        xss = np.array([xs])

        yss, xss = np.meshgrid(yss, xss)
        yss = yss.ravel()
        xss = xss.ravel()

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)

            det_exposure_time(t, t)

            name_fmt = "{sample}_2.0m_{energy}eV_wa{wax}_bpm{xbpm}"
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

                sample_name = name_fmt.format(sample=name, energy="%6.2f" % e, wax=wa, xbpm="%4.3f"%bpm)
                sample_id(user_name="GS", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")

                yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 2870)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 2840)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 2800)
            yield from bps.sleep(2)


def night(t=1):
    
    # proposal_id("2025_1", "314483_Freychet_11")
    # yield from swaxs_Sedge_pierre_2025_1(t=1)
    # yield from bps.sleep(5)

    # proposal_id("2025_1", "314483_Freychet_12")
    # yield from swaxs_Sedge_yunfei_2025_1(t=1)
    # yield from bps.sleep(5)

    # proposal_id("2025_1", "314483_Freychet_13")
    # yield from swaxs_Sedge_jose_2025_1(t=1)

    # yield from bps.sleep(5)

    yield from transition_S_Cl_edges()
    yield from bps.sleep(5)

    proposal_id("2025_1", "314483_Freychet_14")
    yield from swaxs_Cledge_jose_2025_1(t=1)


def nexafs_cl():
    dets = [pil900KW]
    # energies1 =   np.asarray([2810.0, 2820.0, 2830.0, 2832.0, 2834.0, 2834.5, 2835.0, 2835.5, 2836.0, 2836.5, 2837.0, 2837.5, 2838.0, 2838.5, 2839.0,
    # 2839.5, 2840.0, 2840.5, 2841.0, 2841.5, 2845.0, 2850.0, 2855.0, 2860.0, 2865.0, 2870.0, 2875.0, 2880.0, 2890.0])
    name='testnexafs'
    energies = np.linspace(2810, 2830, 21)    
    y = piezo.y.position
    for i, e in enumerate(energies):
        yield from bps.mv(energy, e)
        yield from bps.sleep(2)

        if xbpm2.sumX.get() < 120:
            yield from bps.sleep(5)
            yield from bps.mv(energy, e)
            yield from bps.sleep(2)

        yield from bps.mv(piezo.y, y + i * 20)
        bpm = xbpm3.sumX.value
        
        name_fmt = "{sample}_{energy}eV_wa{wax}_bpm{xbpm}"

        sample_name = name_fmt.format(sample=name, energy="%6.2f" % e, wax=20, xbpm="%4.3f" % bpm)
        sample_id(user_name="GF", sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")

        yield from bp.count(dets, num=1)

    yield from bps.mv(energy, 2850)
    yield from bps.sleep(3)
    yield from bps.mv(energy, 2810)
    yield from bps.sleep(3)






def alignment_blade_coating_2025_1(coating_start_pos, measurement_pos,th):

    yield from bps.mv(thorlabs_su, measurement_pos)
    yield from alignement_gisaxs_hex(angle=th)

    yield from bps.mvr(stage.th, th)
    yield from bps.mvr(stage.y, 0.05)

    yield from bps.mv(thorlabs_su, coating_start_pos)




def blade_coating_2025_1(sample_name='bladecoating', coating_start_pos=10, measurement_pos=87, th=0.12, dets = [pil1M, pil900KW]):
    #yield from shopen()
    #yield from bps.sleep(1)
    #yield from shopen()
    #yield from bps.sleep(1)
    #yield from shopen()
    #yield from bps.sleep(2)
    
    # yield from bps.mv(thorlabs_su, thorlabs_su.position)
    yield from alignment_blade_coating_2025_1(coating_start_pos, measurement_pos,th)

    det_exposure_time(1, 200)
    # det_exposure_time(0.5,300)
    #det_exposure_time(2, 600)
    sample_id(user_name='ML', sample_name=sample_name)
    yield from bps.mv(syringe_pu.go, 1) # start pump 
    yield from bps.sleep(2.5)
    yield from bps.mv(syringe_pu.stop_flow, 1) # stop pump
    
    yield from bps.mv(thorlabs_su, measurement_pos)
    yield from bp.count(dets)

    # yield from shclose()





def blade_coating_2025_1_slowexp_withoutmotion(sample_name='bladecoating', coating_start_pos=10, measurement_pos=87, th=0.12, dets = [pil1M, pil900KW]):   
    
    yield from alignment_blade_coating_2025_1(coating_start_pos, measurement_pos,th)

    det_exposure_time(0.5, 0.5)
    # det_exposure_time(0.5,300)
    #det_exposure_time(2, 600)
    sample_id(user_name='ML', sample_name=sample_name)
    yield from bps.mv(syringe_pu.go, 1) # start pump 
    yield from bps.sleep(2.5)
    yield from bps.mv(syringe_pu.stop_flow, 1) # stop pump
    
    yield from bps.mv(thorlabs_su, measurement_pos)


    yield from bp.count(dets, num=240, delay=2.5)


def blade_coating_2025_1_slowexp_withmotion(sample_name='bladecoating', coating_start_pos=10, measurement_pos=87, th=0.12, dets = [pil1M, pil900KW]):
    
    yield from alignment_blade_coating_2025_1(coating_start_pos, measurement_pos,th)

    det_exposure_time(0.5, 0.5)
    # det_exposure_time(0.5,300)
    #det_exposure_time(2, 600)
    sample_id(user_name='ML', sample_name=sample_name)
    yield from bps.mv(syringe_pu.go, 1) # start pump 
    yield from bps.sleep(2.5)
    yield from bps.mv(syringe_pu.stop_flow, 1) # stop pump
    
    yield from bps.mv(thorlabs_su, measurement_pos)
    yield from bp.scan([pil1M, pil900KW], thorlabs_su, measurement_pos, measurement_pos-15, num=360, per_step=one_1d_step_withwait)




def exsitu_2025_01(sample_name='bladecoating', th=0.12, dets = [pil1M, pil900KW]):
    
    #yield from alignement_gisaxs_hex(0.1)

    det_exposure_time(0.5,0.5)
    sample_id(user_name='ML', sample_name=sample_name)
    
    yield from bps.mvr(stage.th, th)
    yield from bp.count([pil1M, pil900KW])
    yield from bps.mvr(stage.th, -th)



def one_1d_step_withwait(detectors, motor, step, take_reading=None):
    """
    Inner loop of a 1D step scan

    This is the default function for ``per_step`` param in 1D plans.

    Parameters
    ----------
    detectors : iterable
        devices to read
    motor : Settable
        The motor to move
    step : Any
        Where to move the motor to
    take_reading : plan, optional
        function to do the actual acquisition ::

           def take_reading(dets, name='primary'):
                yield from ...

        Callable[List[OphydObj], Optional[str]] -> Generator[Msg], optional

        Defaults to `trigger_and_read`
    """
    take_reading = bps.trigger_and_read if take_reading is None else take_reading

    def move():
        grp = bps._short_uid("set")
        yield bps.Msg("checkpoint")
        yield bps.Msg("set", motor, step, group=grp)
        yield bps.Msg("wait", None, group=grp)

    yield from move()
    yield from bps.sleep(1)
    return (yield from take_reading(list(detectors) + [motor]))



import bluesky.preprocessors as bpp
import bluesky.plans as bp
import bluesky.plan_stubs as bps
from ophyd import Signal


def single_scan_giwaxs(t=1, name="Test", ai_list: list[int]|None = None, xstep=10, waxs_arc = (0, 20)):
    '''
    GISWAXS data collected in vacuum


    '''
    
#     names = ['54I_1', '80_AgTF2N_pebax','70_AgTF2N_pebax','60_AgFSI_pegda','60_AgFSI_pegda_2',       'pegda','10_AgTF2n_pegda','20_AgTF2n_pegda','33_AgTF2n_pegda','50_AgTF2n_pegda','55_AgTF2n_pegda','60_AgTF2n_pegda',
#    '65_AgTF2n_pegda', '70_AgTF2n_pegda',    '3_T4_AgTF2N',   '6_T4_AgTF2N',     '9_T4_AgTF2N','12_T4_AgTF2N',         'C8_new',           'C8_W',          'C10_W',          'C12_W',          'C14_W',           'C8_S',
#              'C10_S',          'C12_S',          'C14_S']
#     x_piezo = [50000,             50000,            50000,           50000,              47000,        41000,            34000,            29000,             24000,            20000,            14000,            10000,
#                 5000,              2000,            -4000,          -11000,             -18000,       -24000,           -31000,           -35000,            -40000,           -44000,           -48000,           -52000, 
#               -54000,            -54000,           -54000]
#     x_hexa = [    17,                12,                7,               2,                  0,            0,                0,                0,                 0,                0,                0,                0,
#                    0,                 0,                0,               0,                  0,            0,                0,                0,                 0,                0,                0,                0,
#                   -3,                -7,              -12]
#     y_piezo = [-1000,             -2000,            -2000,           -2000,              -2000,        -2000,            -2000,            -2000,             -2000,            -2000,            -2000,            -2000,
#                -2000,             -2000,            -2000,           -2000,              -2000,        -2000,            -2000,            -2000,             -2000,            -2000,            -2000,            -2000,
#                -2000,             -2000,            -2000]

    # names = ['C8_S',
    #           'C10_S',           'C12_S',          'C14_S']
    # x_piezo = [-52000, 
    #            -54000,            -54000,           -54000]
    # x_hexa = [      0,
    #                -3,                -7,              -12]
    # y_piezo = [ -1000,
    #             -1000,             -1000,            -1000]


    # names = [  'C14',  'C12',  'C10',  'C08','SG_NCs_1','SG_NCs_2', 'HOPI_70water_1', 'HOPI_70water_2']
    # x_piezo = [ 2000,  -5000, -14000, -22000,    -33000,    -44000,           -55000,           -55000]
    # x_hexa = [      0,     0,      0,      0,         0,         0,               -1,              -11]
    # y_piezo = [ -4000,  -4000, -4000,  -4000,     -4000,     -4000,            -4000,            -4000]


    # names = [  'SG_NCs_1','SG_NCs_2', 'HOPI_70water_1', 'HOPI_70water_2']
    # x_piezo = [-33000,    -44000,           -55000,           -55000]
    # x_hexa = [      0,         0,               -1,              -11]
    # y_piezo = [ -4000,     -4000,            -4000,            -4000]

    names = [  'HOPI_70water_1', 'HOPI_70water_2']
    x_piezo = [          -55000,           -55000]
    x_hexa = [               -1,              -11]
    y_piezo = [           -4000,            -4000]

    names = [   'C12',  'C10',  'C08','HOPI_70water_1', 'HOPI_70water_2']
    x_piezo = [ -5000, -14000, -22000,          -55000,           -55000]
    x_hexa = [      0,      0,      0,              -1,              -11]
    y_piezo = [ -4000, -4000,  -4000,           -4000,            -4000]

    names = [  'C14']
    x_piezo = [ 2000]
    x_hexa = [      0]
    y_piezo = [ -4000]

    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexa)})"

    waxs_arc = [20, 0]

    ai0_all = -1
    ai_list = [0.12]
    xstep = 0

    dets = [pil1M, pil900KW]


    for name, xs, ys, xs_hexa in zip(names, x_piezo, y_piezo, x_hexa):
        yield from bps.mv(stage.x, xs_hexa,
                          piezo.x, xs,
                          piezo.y, ys)

        yield from bps.mv(piezo.th, ai0_all)
        yield from alignement_gisaxs_doblestack(0.15)

        ai0 = piezo.th.position
        det_exposure_time(t, t)

        s = Signal(name='target_file_name', value='')

        @bpp.stage_decorator(dets)
        @bpp.run_decorator(md={'sample_name' :'{target_file_name}'})
        def inner():
            for i, wa in enumerate(waxs_arc):
                yield from bps.mv(waxs, wa)

                counter = 0
                for k, ais in enumerate(ai_list):
                    yield from bps.mv(piezo.th, ai0 + ais)

                    name_fmt = "{sample}_{energy}eV_ai{ai}_wa{wax}"
                    
                    # yield from bps.mv(piezo.x, xs - counter * xstep)
                    counter += 1
                    e=energy.energy.position
                    sdd=pil1m_pos.z.position
                    sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, sdd="%1f"%sdd)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    s.put(sample_name)
                    yield from bps.trigger_and_read(dets + [energy, waxs, xbpm2, xbpm3, piezo.th, piezo.x] + [s])
            yield from bps.mv(piezo.th, ai0)

        (yield from inner())






def single_scan_waxs(t=1, name="Test", ai_list: list[int]|None = None, xstep=10, waxs_arc = (0, 20)):
    '''
    GISWAXS data collected in vacuum


    '''
    
    # names = ['80_AgTF2N_pebax','70_AgTF2N_pebax','60_AgFSI_pegda','60_AgFSI_pegda_2',       'pegda','10_AgTF2n_pegda','20_AgTF2n_pegda','33_AgTF2n_pegda','50_AgTF2n_pegda','55_AgTF2n_pegda','60_AgTF2n_pegda',
    #          '65_AgTF2n_pegda', '70_AgTF2n_pegda']
    # x_piezo = [         -43000,            -40000,           -35000,          -29000,        -22000,           -18000,           -12000,           -41000,           -35000,           -31000,           -27000,
    #                     -21000,             -16000]
    # x_hexa = [               0,                 0,                0,               0,              0,               0,                0,                0,                0,                0,                0,
    #                          0,                 0]
    # y_hexa = [              -4,                -4,               -4,              -4,             -4,              -4,               -4,                7,                7,                7,                7,
    #                          7,                 7]
    # y_piezo = [          -5000,             -4180,            -3180,           -3180,          -3180,           -3180,            -3180,             1000,             1000,             1000,             1000,
    #                       1000,              1000]

    # names = [           'AgBeh',            'C14',           'C12',             'C10',         'C08']
    # x_piezo = [          45900,             39300,           32900,             26500,         20200]
    # x_hexa = [               0,                 0,               0,                 0,             0]
    # y_hexa = [               7,                 7,               7,                 7,             7]
    # y_piezo = [           1000,              1000,            1000,              1000,          1000]


    names = [           'EtOH',     '0p02piperon',    '0p2piperon',      '1p0piperon']
    x_piezo = [          13700,              7400,            1300,             -4900]
    x_hexa = [               0,                 0,               0,                 0]
    y_hexa = [               7,                 7,               7,                 7]
    y_piezo = [           1000,              1000,            1000,              1000]



    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexa)})"
    assert len(x_piezo) == len(y_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexa)})"


    waxs_arc = [0, 20]
    xstep = 0

    dets = [pil1M, pil900KW]


    for name, xs, ys, xs_hexa, ys_hexa in zip(names, x_piezo, y_piezo, x_hexa, y_hexa):
        yield from bps.mv(stage.x, xs_hexa,
                          stage.y, ys_hexa,
                          piezo.x, xs,
                          piezo.y, ys)


        if waxs.arc.position<10:
            waxs_arc = [0, 20]
        else:
            waxs_arc = [20, 0]


        det_exposure_time(t, t)
        s = Signal(name='target_file_name', value='')

        @bpp.stage_decorator(dets)
        @bpp.run_decorator(md={'sample_name' :'{target_file_name}'})
        def inner():
            for i, wa in enumerate(waxs_arc):
                yield from bps.mv(waxs, wa)

                name_fmt = "{sample}_{energy}eV_wa{wax}"
                
                # yield from bps.mv(piezo.x, xs - counter * xstep)
                e=energy.energy.position
                sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, wax=wa)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                s.put(sample_name)
                yield from bps.trigger_and_read(dets + [energy, waxs, xbpm2, xbpm3, piezo.x] + [s])

        (yield from inner())







def scan_nexafs_Ti():
    dets = [pil900KW]
    # energies1 =   np.asarray([2810.0, 2820.0, 2830.0, 2832.0, 2834.0, 2834.5, 2835.0, 2835.5, 2836.0, 2836.5, 2837.0, 2837.5, 2838.0, 2838.5, 2839.0,
    # 2839.5, 2840.0, 2840.5, 2841.0, 2841.5, 2845.0, 2850.0, 2855.0, 2860.0, 2865.0, 2870.0, 2875.0, 2880.0, 2890.0])
    
    name='testnexafsTi'
    energies = np.linspace(4990, 5040, 51)    
    y = piezo.y.position
    waxs_arc = [20]

    s = Signal(name='target_file_name', value='')

    @bpp.stage_decorator(dets)
    @bpp.run_decorator(md={'sample_name' :'{target_file_name}'})
    def inner():
        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)

            for i, e in enumerate(energies):
                yield from bps.mv(energy, e)
                yield from bps.sleep(2)

                if xbpm2.sumX.get() < 50:
                    yield from bps.mv(energy, e)
                
                
                yield from bps.mv(piezo.y, y - i * 20)

                # Metadata
                #e = energy.position.energy / 1000
                wa = str(np.round(float(wa), 1)).zfill(4)
                sdd = pil1m_pos.z.position / 1000

                # Sample name
                name_fmt = ("{sample}_{energy}eV_wa{wax}_sdd{sdd}m_up")
                sample_name = name_fmt.format(sample = name,energy = "%.2f" % e , wax = wa, sdd = "%.1f" % sdd)
                sample_name = sample_name.translate({ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ =, "})
                print(f"\n\n\n\t=== Sample: {sample_name} ===")
                s.put(sample_name)
                
                yield from bps.trigger_and_read(dets + [energy, waxs, xbpm2, xbpm3] + [s])

            yield from bps.mv(energy, 5000)
            yield from bps.sleep(2)
    (yield from inner())




def energy_Tiedge_scan(t=1, name="Test", ai_list: list[int]|None = None, xstep=10, waxs_arc = (0, 20)):
    '''
    SWAXS at the Ti edge
    '''

    names =   ['kl_nf_ahp_0p5', 'kl_nf_ahp_1',  'kl_nf_ahp_2',  'kl_nf_nil_nil']       
    piezo_x = [         -39300,        -33500,         -27700,           -22000]   
    piezo_y = [          -2000,         -2000,         -2200,             -1700]

    names =   [         'sa05',         'sa06',      'sa07',        'sa08',  'sa09']       
    piezo_x = [         43300,        38200,         32000,           26700, 20300]   
    piezo_y = [          -920,         -1020,         -1020,             -1020, -1220]


    assert len(names)   == len(piezo_x), f"Wrong list lenghts"
    assert len(piezo_x) == len(piezo_y), f"Wrong list lenghts"

    waxs_arc = [0, 20]
    
    # 41 energies
    energies = np.asarray(np.arange(4960, 4980, 5).tolist() + np.arange(4980, 4990, 2).tolist() 
                          + np.arange(4990, 5000, 0.5).tolist() + np.arange(5000, 5020, 2).tolist()
                          + np.arange(5020, 5035, 5).tolist())


    dets = [pil900KW, pil1M]
    det_exposure_time(t, t)

    for name, x, y in zip(names, piezo_x, piezo_y):
        yield from bps.mv(piezo.x, x, piezo.y, y)

        s = Signal(name='target_file_name', value='')

        @bpp.stage_decorator(dets)
        @bpp.run_decorator(md={'sample_name' :'{target_file_name}'})
        def inner():
            for wa in waxs_arc:
                yield from bps.mv(waxs, wa)

                for i, e in enumerate(energies):
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)

                    if xbpm2.sumX.get() < 50:
                        yield from bps.mv(energy, e)

                    yield from bps.mv(piezo.y, y - i * 20)
                
                    # Metadata
                    wa = str(np.round(float(wa), 1)).zfill(4)
                    sdd = pil1m_pos.z.position / 1000
                    bpm3 = xbpm3.sumX.get()

                    # Sample name
                    name_fmt = ("{sample}_{energy}eV_wa{wax}_sdd{sdd}m_bpm{bpm}")
                    sample_name = name_fmt.format(sample = name,energy = "%.2f" % e , wax = wa, sdd = "%.1f" % sdd, bpm = "%.2f" % bpm3)
                    sample_name = sample_name.translate({ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ =, "})
                    print(f"\n\n\n\t=== Sample: {sample_name} ===")
                    s.put(sample_name)
                    
                    yield from bps.trigger_and_read(dets + [energy, waxs, xbpm2, xbpm3, ] + [s])

                yield from bps.mv(energy, 5000)
                yield from bps.sleep(2)
                yield from bps.mv(energy, 4960)
                yield from bps.sleep(2)

        (yield from inner())





def temp_series(name='temp',temps = np.linspace(25,40,16),exp_time=1, hold_delay=120, dets=[pil1M]):   # function loop to bring linkam to temp, hold and measure
# Function will begin at start_temp and take a SAXS measurement at every temperature given 
    
    temps = [240, 230, 220, 210, 200, 175, 150, 125, 100, 75, 50, 30]

    dets = [pil1M]
    LThermal.setTemperature(temps[0])
    # LThermal.setTemperatureRate(ramp)
    LThermal.on() # turn on 
    det_exposure_time(exp_time,exp_time)

    s = Signal(name='target_file_name', value='')
    RE.md["sample_name"] = '{target_file_name}'
    for i, temp in enumerate(temps):
        LThermal.setTemperature(temp)

        while abs(LThermal.temperature()-temp)>1:
            yield from bps.sleep(10)
            print('waiting for 10s')

        print('Reached tem', temp)
        print('Waiting during equilibration')
        yield from bps.sleep(hold_delay)
        

        # Metadata
        sdd = pil1m_pos.z.position / 1000

        # Sample name
        name_fmt = ("{sample}_{energy}eV_sdd{sdd}m_temp{temp}")
        sample_name = name_fmt.format(sample = name,energy = "%.2f" % energy.energy.position , sdd = "%.1f" % sdd, temp = "%.1f" %temp)
        sample_name = sample_name.translate({ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ =, "})

        print(f"\n\n\n\t=== Sample: {sample_name} ===")
        s.put(sample_name)
        
        yield from bp.count(dets + [s])

    LThermal.off()





def xpcs_2025_1(sample_name='bladecoating', coating_start_pos=10, measurement_pos=87, th=0.12, dets = [pil1M, pil900KW]):

    det_exposure_time(0.5, 500)
    sample_id(user_name='ML', sample_name=sample_name)
    yield from bp.count(dets)
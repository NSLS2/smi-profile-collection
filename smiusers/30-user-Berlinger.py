def Nafion_waxs_S_edge(t=1):
    dets = [pil1M]

    energies = 7 + np.asarray(
        np.arange(2445, 2470, 5).tolist()
        + np.arange(2470, 2480, 0.25).tolist()
        + np.arange(2480, 2490, 1).tolist()
        + np.arange(2490, 2501, 5).tolist()
    )
    waxs_arc = np.linspace(52, 52, 1)

    names = ["70nPA", "50nPA", "30nPA", "10nPA"]
    x = [-23500, -1200, 23000, 44500]
    y = [-9700, -9600, -9500, -9000]

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
                try:
                    yield from bps.mv(energy, e)
                except:
                    print("energy failed to move, sleep for 30 s")
                    yield from bps.sleep(30)
                    print("Slept for 30 s, try move energy again")
                    yield from bps.mv(energy, e)
                yield from bps.sleep(1)

                yield from bps.mv(piezo.y, ysss)
                yield from bps.mv(piezo.x, xsss)

                bpm = xbpm2.sumX.value

                sample_name = name_fmt.format(
                    sample=name, energy="%6.2f" % e, wax=wa, xbpm="%4.3f" % bpm
                )
                sample_id(user_name="GF_sdd2m", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 2470)
            yield from bps.mv(energy, 2450)

    # yield from bps.mv(stage.y, 0)
    # yield from bps.mv(stage.th, 0)

    # names = ['Nafion_xl']
    # x = [-42800]
    # y = [-2500]

    # for name, xs, ys in zip(names, x, y):
    #     yield from bps.mv(piezo.x, xs)
    #     yield from bps.mv(piezo.y, ys)

    #     yss = np.linspace(ys, ys + 1000, 15)
    #     xss = np.linspace(xs, xs + 1000, 4)

    #     yss, xss = np.meshgrid(yss, xss)
    #     yss = yss.ravel()
    #     xss = xss.ravel()

    #     for wa in waxs_arc:
    #         yield from bps.mv(waxs, wa)

    #         det_exposure_time(t,t)
    #         name_fmt = '{sample}_{energy}eV_wa{wax}_bpm{xbpm}'
    #         for e, xsss, ysss in zip(energies, xss, yss):
    #             yield from bps.mv(energy, e)
    #             yield from bps.sleep(1)

    #             yield from bps.mv(piezo.y, ysss)
    #             yield from bps.mv(piezo.x, xsss)

    #             bpm = xbpm2.sumX.value

    #             sample_name = name_fmt.format(sample=name, energy='%6.2f'%e, wax = wa, xbpm = '%4.3f'%bpm)
    #             sample_id(user_name='GF', sample_name=sample_name)
    #             print(f'\n\t=== Sample: {sample_name} ===\n')
    #             yield from bp.count(dets, num=1)

    #         yield from bps.mv(energy, 2470)
    #         yield from bps.mv(energy, 2450)


def Su_nafion_waxs_hard(t=1):
    dets = [pil300KW, pil1M]

    waxs_arc = np.linspace(0, 32.5, 6)

    yield from bps.mv(stage.y, 0)
    yield from bps.mv(stage.th, 0)

    names = ["30nPA", "50nPA"]
    x = [12500, -15500]
    y = [-300, -300]

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)

        for name, xs, ys in zip(names, x, y):
            yield from bps.mv(piezo.x, xs)
            yield from bps.mv(piezo.y, ys)

            det_exposure_time(t, t)
            name_fmt = "{sample}_16100eV_sdd8.3_wa{wax}"
            sample_name = name_fmt.format(sample=name, wax=wa)
            sample_id(user_name="GF", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)

    yield from bps.mv(stage.th, 1.5)
    yield from bps.mv(stage.y, -8)

    names = ["70nPA", "Nafion_xl"]
    x = [32000, 1000]
    y = [-9000, -9000]

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)

        for name, xs, ys in zip(names, x, y):
            yield from bps.mv(piezo.x, xs)
            yield from bps.mv(piezo.y, ys)

            det_exposure_time(t, t)
            name_fmt = "{sample}_16100eV_sdd8.3_wa{wax}"
            sample_name = name_fmt.format(sample=name, wax=wa)
            sample_id(user_name="GF", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)


def sara_nafion_waxs_hard(t=1):
    dets = [pil300KW, pil1M]

    waxs_arc = np.linspace(0, 32.5, 6)

    # names = ['10nPA_sol', '30nPA_sol', '50nPA_sol', '60nPA_sol']
    # x = [-37200, -31200, -25100, -12200]
    # y = [1000,     1000,   1000,   1000]

    names = ["SPES_20", "SPES_40", "SPES_60"]
    x = [26000, 4000, -20000]
    y = [0, 0, 0]

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)

        for name, xs, ys in zip(names, x, y):
            yield from bps.mv(piezo.x, xs)
            yield from bps.mv(piezo.y, ys)

            det_exposure_time(t, t)
            name_fmt = "{sample}_16100eV_sdd8.3_wa{wax}"
            sample_name = name_fmt.format(sample=name, wax=wa)
            sample_id(user_name="GF", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)

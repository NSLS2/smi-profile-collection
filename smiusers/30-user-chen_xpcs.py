def grid_scan_xpcs():

    folder = "301000_Chen34"
    xs = np.linspace(-9350, -9150, 2)
    ys = np.linspace(1220, 1420, 2)
    names = ["PSBMA5_200um_grid"]

    energies = [2450, 2472, 2476, 2490]

    x_off = [0, 60, 0, 60]
    y_off = [0, 0, 60, 60]

    xxs, yys = np.meshgrid(xs, ys)

    dets = [pil1M]
    for name in names:
        for ener, xof, yof in zip(energies, x_off, y_off):
            yield from bps.mv(energy, ener)
            yield from bps.sleep(10)
            for i, (x, y) in enumerate(zip(xxs.ravel(), yys.ravel())):

                pil1M.cam.file_path.put(
                    f"/ramdisk/images/users/2019_3/%s/1M/%s_pos%s" % (folder, name, i)
                )

                yield from bps.mv(piezo.x, x + xof)
                yield from bps.mv(piezo.y, y + yof)

                name_fmt = "{sample}_{energy}eV_pos{pos}"
                sample_name = name_fmt.format(sample=name, energy=ener, pos="%2.2d" % i)
                sample_id(user_name="Chen", sample_name=sample_name)
                yield from bps.sleep(5)

                det_exposure_time(0.03, 30)

                print(f"\n\t=== Sample: {sample_name} ===\n")

                pil1M.cam.acquire.put(1)
                yield from bps.sleep(5)
                pv = EpicsSignal("XF:12IDC-ES:2{Det:1M}cam1:Acquire", name="pv")

                while pv.get() == 1:
                    yield from bps.sleep(5)

        yield from bps.mv(energy, 2475)
        yield from bps.mv(energy, 2450)


def NEXAFS_SAXS_S_edge(t=1):
    dets = [pil300KW]
    name = "sample_thick_waxs"

    energies = [2450, 2480, 2483, 2484, 2485, 2486, 2500]

    det_exposure_time(t, t)
    name_fmt = "{sample}_{energy}eV_wa{wa}"

    waxs_an = np.linspace(0, 26, 5)

    yss = np.linspace(1075, 1575, 5)

    for wax in waxs_an:
        yield from bps.mv(waxs, wax)
        for e, ys in zip(energies, yss):
            yield from bps.mv(energy, e)
            yield from bps.mv(piezo.y, ys)
            sample_name = name_fmt.format(sample=name, energy=e, wa="%3.1f" % wax)
            sample_id(user_name="Chen", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)

        yield from bps.mv(energy, 2475)
        yield from bps.mv(energy, 2450)


def grid_scan_static():

    names = ["PSBMA30_10um_static"]

    x_off = -36860 + np.asarray([-200, 200])
    y_off = 1220 + np.asarray([-100, 0, 100])

    energies = np.linspace(2500, 2450, 51)
    xxs, yys = np.meshgrid(x_off, y_off)

    dets = [pil300KW, pil1M]
    for name in names:
        for i, (x, y) in enumerate(zip(xxs.ravel(), yys.ravel())):
            yield from bps.mv(piezo.x, x)
            yield from bps.mv(piezo.y, y)
            energies = energies[::-1]
            yield from bps.sleep(2)

            for ener in energies:
                yield from bps.mv(energy, ener)

                yield from bps.sleep(0.1)

                name_fmt = "{sample}_{energy}eV_pos{pos}_xbpm{xbpm}"
                sample_name = name_fmt.format(
                    sample=name,
                    energy=ener,
                    pos="%2.2d" % i,
                    xbpm="%3.1f" % xbpm3.sumY.value,
                )
                sample_id(user_name="Chen", sample_name=sample_name)

                det_exposure_time(0.1, 0.1)
                yield from bp.count(dets, num=1)


def nexafs_S_edge_chen(t=1):
    dets = [pil300KW]
    det_exposure_time(t, t)

    waxs_arc = [45.0]

    name_fmt = "nexafs_sampletest1_4_{energy}eV_wa{wax}_bpm{xbpm}"

    for wa in waxs_arc:
        for e in energies:
            yield from bps.mv(energy, e)
            yield from bps.sleep(1)

            bpm = xbpm2.sumX.value

            sample_name = name_fmt.format(
                energy="%6.2f" % e, wax=wa, xbpm="%4.3f" % bpm
            )
            sample_id(user_name="WC", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)

    yield from bps.mv(energy, 2490)
    yield from bps.mv(energy, 2470)
    yield from bps.mv(energy, 2450)


def waxs_S_edge_chen_2020_3(t=1):
    dets = [pil300KW, pil1M]

    names = [
        "sampleA1",
        "sampleB1",
        "sampleB2",
        "sampleB3",
        "sampleC4",
        "sampleC5",
        "sampleE8",
        "sampleD1",
        "sampleD2",
        "sampleD3",
        "sampleD4",
        "sampleD5",
        "sampleC8",
        "sampleF1",
        "sampleF2",
        "sampleE1",
        "sampleE3",
        "sampleE4",
        "sampleE5",
        "sampleD8",
        "sampleF8",
    ]
    x = [
        43800,
        28250,
        20750,
        13350,
        5150,
        -5660,
        -10900,
        -18400,
        -26600,
        -34800,
        -42800,
        42300,
        34400,
        26700,
        18800,
        11200,
        2900,
        -5000,
        -12000,
        -20300,
        -27800,
    ]
    y = [
        -4900,
        -5440,
        -5960,
        -5660,
        -5660,
        -5660,
        -5880,
        -4750,
        -5450,
        -5000,
        -4450,
        6950,
        6950,
        6950,
        7450,
        7200,
        7400,
        8250,
        8250,
        8250,
        7750,
    ]

    energies = [
        2450.0,
        2474.0,
        2475.0,
        2476.0,
        2477.0,
        2478.0,
        2479.0,
        2482.0,
        2483.0,
        2484.0,
        2485.0,
        2486.0,
        2487.0,
        2490.0,
        2500.0,
    ]

    waxs_arc = np.linspace(0, 13, 3)

    for name, xs, ys in zip(names, x, y):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys + 30)

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)

            det_exposure_time(t, t)
            name_fmt = "{sample}_rev_{energy}eV_wa{wax}_bpm{xbpm}"
            for e in energies[::-1]:
                yield from bps.mv(energy, e)
                yield from bps.sleep(1)

                bpm = xbpm2.sumX.value

                sample_name = name_fmt.format(
                    sample=name, energy="%6.2f" % e, wax=wa, xbpm="%4.3f" % bpm
                )
                sample_id(user_name="GF", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 2480)
            yield from bps.mv(energy, 2460)

def saxs_waxs_Shejla(t=1):
    dets = [pil300KW, pil1M]

    waxs_arc = np.linspace(0, 26, 5)

    yield from bps.mv(stage.y, 0)
    yield from bps.mv(stage.th, 0)
    # names = ['DHH1_2', 'DHH2_2', 'DHH3_2', 'HHH1_2', 'HHH2_2']
    # x = [-34500, -15000,  4000, 24000, 43500]
    # y = [ -2000,  -2500, -2500, -1500, -2000]
    # z = [  2700,   2700,  2700,  2700,  2700]

    names = ["DHH2_rehyd", "HHH2_rehyd"]
    x = [-33000, 25500]
    y = [0, -1000]
    z = [2700, 2700]

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)

        for name, xs, ys, zs in zip(names, x, y, z):
            yield from bps.mv(piezo.x, xs)
            yield from bps.mv(piezo.y, ys)
            yield from bps.mv(piezo.z, zs)

            xss = np.linspace(xs - 500, xs + 500, 3)
            yss = np.linspace(ys - 300, ys + 300, 3)
            yss, xss = np.meshgrid(yss, xss)
            yss = yss.ravel()
            xss = xss.ravel()

            det_exposure_time(t, t)
            name_fmt = "{sample}_16100eV_sdd8.3_wa{wax}"
            sample_name = name_fmt.format(sample=name, wax=wa)
            sample_id(user_name="GF", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.list_scan(dets, piezo.x, xss.tolist(), piezo.y, yss.tolist())

    # yield from bps.mv(stage.th, 1.5)
    # yield from bps.mv(stage.y, -10)
    # names = ['HHH3_2', 'Blank_water_2', 'Bkg_dry_2', 'DHH-Wet_2', 'HHH-Wet_2']
    # x = [45500, 26000,  6000, -13500, -32500]
    # y = [-9000, -9000, -9000,  -9000,  -9000]
    # z = [15800, 15800, 15800,  15800,  15800]

    # for wa in waxs_arc:
    #     yield from bps.mv(waxs, wa)

    #     for name, xs, ys, zs in zip(names, x, y, z):
    #         yield from bps.mv(piezo.x, xs)
    #         yield from bps.mv(piezo.y, ys)
    #         yield from bps.mv(piezo.z, zs)

    #         xss = np.linspace(xs - 500, xs + 500, 3)
    #         yss = np.linspace(ys - 300, ys + 300, 3)
    #         yss, xss = np.meshgrid(yss, xss)
    #         yss = yss.ravel()
    #         xss = xss.ravel()

    #         det_exposure_time(t,t)
    #         name_fmt = '{sample}_16100eV_sdd8.3_wa{wax}'
    #         sample_name = name_fmt.format(sample=name, wax = wa)
    #         sample_id(user_name='GF', sample_name=sample_name)
    #         print(f'\n\t=== Sample: {sample_name} ===\n')
    #         yield from bp.list_scan(dets, piezo.x, xss.tolist() , piezo.y, yss.tolist())

def Ru_edge_zhengxing_2024_2(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)
    '''
    names = [   'P2_80C',    'P4_80C']
    x_piezo = [    39200,       26500]
    x_hexa =  [        0,           0]
    y_piezo = [    -3900,       -3600]
    z_piezo = [     6600,        6600]
    '''

    names = ['P1_120C_1', 'P1_120C_2','P1_120C_3','P1_120C_4', 'P1_120C_5','P1_120C_6','P1_120C_7']
    x = [           -2.6,        -2.5,       -2.4,       -2.3,        -2.2,       -2.1,      -2.4]
    y = [           -3.2,        -3.2,       -3.2,       -3.2,        -3.2,       -3.2,      -3.2]

    assert len(x) == len(names), f"Number of X coordinates ({len(x)}) is different from number of samples ({len(names)})"
    assert len(x) == len(y), f"Number of X coordinates ({len(x)}) is different from number of samples ({len(y)})"

    energies = np.arange(2800, 2825, 5).tolist() + np.arange(2825, 2830, 0.5).tolist() + np.arange(2830, 2848, 2).tolist()+ np.arange(2838, 2850, 0.5).tolist()+ np.arange(2850, 2881, 5).tolist()

    waxs_arc = [20, 0]

    for name, xs, ys in zip(names, x, y):
        yield from bps.mv(stage.x, xs)
        yield from bps.mv(stage.y, ys)

        det_exposure_time(t, t)

        yss = np.linspace(ys, ys + 0.5, 55)
        xss = np.array([xs])

        yss, xss = np.meshgrid(yss, xss)
        yss = yss.ravel()
        xss = xss.ravel()

        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)
            # Do not take SAXS when WAXS detector in the way
            dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]

            name_fmt = "{sample}_pos1_{energy}eV_wa{wax}_bpm{xbpm}_sdd3m"

            for e, xsss, ysss in zip(energies, xss, yss):
                yield from bps.mv(energy, e)
                yield from bps.sleep(2)
                if xbpm2.sumX.get() < 50:
                    yield from bps.sleep(2)
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                yield from bps.mv(stage.y, ysss)
                yield from bps.mv(stage.x, xsss)
                
                bpm = xbpm2.sumX.get()
                sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, wax=wa, xbpm="%4.3f"%bpm)
                sample_id(user_name="ZP", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 2860)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 2840)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 2820)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 2800)
            yield from bps.sleep(2)

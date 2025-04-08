def temp_snapshop(name_base="temp",num=1,delay=0, exp_time=1,en=2472,dets=[pil900KW]):
    det_exposure_time(exp_time,exp_time)
    energy.move(en)
    for i in range(num):
        sample_id(user_name='Gorecka', sample_name=f'{name_base}_{LThermal.temperature()}degC_{en}eV')
        RE.md['temp'] = LThermal.temperature()
        yield from bp.count(dets)
        yield from bps.sleep(delay)



def saxs_S_edge_linkam_2024_1(t=1,temps=[30]):
    dets = [pil900KW, pil1M]

    name = "D1_06_10sexpo"

    energies = (2472,2475,247)
    waxs_arc = [20, 0]

    
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
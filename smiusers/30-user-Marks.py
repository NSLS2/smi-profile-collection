    # vol = Cpt(EpicsSignal, "Val:Vol-SP",) 
    # rate = Cpt(EpicsSignal, "Val:Rate-SP", )
    # go = Cpt(EpicsSignal, "Cmd:Run-Cmd",)
    # stop_flow = Cpt(EpicsSignal, "Cmd:Stop-Cmd",)
    # dia = Cpt(EpicsSignal, "Val:Dia-RB")
    # dir = Cpt(EpicsSignal, "Val:Dir-Sel",) 

def waxs_S_edge_marks_2025_1_coarse(name, x=[0], y=[-3190], t=1):
    dets = [pil900KW, pil1M]

    # names = ["PM7_TO1"]
    # x = [          2000] 7500  9500
    # y = [         -6458] -3639 -3588

    assert len(x) == len(y), f"Number of X coordinates ({len(x)}) is different from number of samples ({len(y)})"
    # assert len(x) == len(names), f"Number of X coordinates ({len(x)}) is different from number of samples ({len(names)})"
    
    # less energies for long exposure
    # energies = (np.arange(2450, 2470, 10).tolist()+ np.arange(2470, 2480, 1).tolist()
    #         + np.arange(2480, 2520, 20).tolist())
    


    energies = (np.arange(2445, 2470, 5).tolist()+ np.arange(2470, 2480, 0.25).tolist()+ np.arange(2480, 2490, 1).tolist()
                + np.arange(2490, 2500, 5).tolist()+ np.arange(2500, 2560, 10).tolist())

    xsss = np.linspace(x[0], x[0]+2000, len(energies))
    ysss = np.linspace(y[0], y[0], len(energies))


    waxs_arc = [0, 20]

    # yield from bps.mv(syringe_pu.go, 1) # start pump


    yield from bps.mv(syringe_pu.go, 1) # start pump

    for xs, ys in zip(x, y):
        yield from bps.mv(piezo.x, xs,
                          piezo.y, ys)

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)
            if wa == 0:
                dets = [pil900KW]
            else:
                dets = [pil900KW, pil1M]

            det_exposure_time(t, t)

            name_fmt = "{sample}_sdd3.0m_{energy}eV_wa{wax}_bpm{xbpm}"
            for e, xss, yss in zip(energies, xsss, ysss):
                # print(e, xss)
                yield from bps.mv(piezo.x, xss)
                yield from bps.mv(piezo.y, yss)
                yield from bps.mv(energy, e)

                yield from bps.sleep(2)
                if xbpm2.sumX.get() < 50:
                    yield from bps.sleep(2)
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)

                bpm = xbpm3.sumX.get()

                sample_name = name_fmt.format(sample=name, energy="%6.2f" % e, wax=wa, xbpm="%4.3f" % bpm)
                sample_id(user_name="TC", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")

                yield from bp.count(dets, num=1)

                # yield from bps.mv(syringe_pu.stop_flow, 1) # stop pump

            yield from bps.mv(energy, 2500)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 2480)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 2445)
    
    yield from bps.mv(syringe_pu.stop_flow, 1) # stop pump
    sample_id(user_name="test", sample_name="test")
    det_exposure_time(1, 1)





def nexafs_S_edge_marks_2025_1_coarse(name, x=[0], y=[-3190], t=1):
    dets = [pil900KW, pil1M]


    assert len(x) == len(y), f"Number of X coordinates ({len(x)}) is different from number of samples ({len(y)})"
    
    #y -3613 x = 0
    #y -3600 x = 2000

    # Coarse first to look at the edge
    energies = (np.arange(2445, 2470, 5).tolist()+ np.arange(2470, 2490, 1).tolist()
                + np.arange(2490, 2500, 5).tolist()+ np.arange(2500, 2560, 10).tolist())


    xsss = np.linspace(x[0], x[0]+2000, len(energies))
    ysss = np.linspace(y[0], y[0], len(energies))

    waxs_arc = [20]

    for xs, ys in zip(x, y):
        yield from bps.mv(piezo.x, xs,
                          piezo.y, ys)

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)
            dets = [pil900KW]
            det_exposure_time(t, t)

            name_fmt = "nexafs_{sample}_{energy}eV_wa{wax}_bpm{xbpm}"
            for e, xss, yss in zip(energies, xsss, ysss):
                # print(e, xss)
                yield from bps.mv(piezo.x, xss)
                yield from bps.mv(piezo.y, yss)

                yield from bps.mv(energy, e)
                yield from bps.sleep(2)
                if xbpm2.sumX.get() < 50:
                    yield from bps.sleep(2)
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)

                bpm = xbpm3.sumX.get()

                sample_name = name_fmt.format(sample=name, energy="%6.2f" % e, wax=wa, xbpm="%4.3f" % bpm)
                sample_id(user_name="SM", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 2500)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 2480)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 2445)

    sample_id(user_name="test", sample_name="test")



def nexafs_Br_edge_2023_3(t=1):
    dets = [pil900KW]
    det_exposure_time(t, t)

    yield from engage_detectors()

    names = [ 'LiBr-sol-nosolv-a-nexafs' ]
    x_piezo = [-20200]
    x_hexa = [      0]
    y_piezo = [ -5000]
    z_piezo = [  -200]

    msg = "Wrong number of coordinates, check names, piezos, and hexas"
    assert len(x_piezo) == len(names), msg
    assert len(x_piezo) == len(y_piezo), msg
    assert len(x_piezo) == len(z_piezo), msg
    assert len(x_piezo) == len(x_hexa), msg

    det_exposure_time(t, t)
    energies = np.linspace(13450, 13500, 51)
    waxs_arc = [20]

    for name, xs, ys, zs, xs_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa):
        yield from bps.mv(
            stage.x, xs_hexa,
            piezo.x, xs,
            piezo.y, ys,
            piezo.z, zs,
        )

        yss = np.linspace(ys, ys + 350, 52)
        xss = np.array([xs])

        yss, xss = np.meshgrid(yss, xss)
        yss = yss.ravel()
        xss = xss.ravel()

        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)
            # Do not take SAXS when WAXS detector in the way
            dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]

            name_fmt = "{sample}_pos1_{energy}eV_wa{wax}_bpm{xbpm}"

            for e, xsss, ysss in zip(energies, xss, yss):
                yield from bps.mv(energy, e)
                yield from bps.sleep(2)
                if xbpm2.sumX.get() < 50:
                    yield from bps.sleep(2)
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                yield from bps.mv(piezo.y, ysss,
                                  piezo.x, xsss)
                
                bpm = xbpm2.sumX.get()
                bpm = str(np.round(float(bpm), 3)).zfill(5)
                pos = 1
                #sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, wax=wa, xbpm="%4.3f"%bpm)
                sample_name = f'{name}_pos{pos}{get_scan_md(tender=True)}_bpm{bpm}'
                sample_id(user_name="IB", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets)

            yield from bps.sleep(2)
            yield from bps.mv(energy, 13470)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 13450)
            yield from bps.sleep(2)

def nexafs_Rb_edge_2023_3(t=1):
    dets = [pil900KW]
    det_exposure_time(t, t)

    yield from engage_detectors()

    names = [ 'DIPA_RbBr-org-a-nexafs' ]
    x_piezo = [  -500]
    x_hexa = [      0]
    y_piezo = [ -4306]
    z_piezo = [ -1300]

    msg = "Wrong number of coordinates, check names, piezos, and hexas"
    assert len(x_piezo) == len(names), msg
    assert len(x_piezo) == len(y_piezo), msg
    assert len(x_piezo) == len(z_piezo), msg
    assert len(x_piezo) == len(x_hexa), msg

    det_exposure_time(t, t)
    energies = np.linspace(15180, 15230, 51)
    waxs_arc = [40]

    for name, xs, ys, zs, xs_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa):
        yield from bps.mv(
            stage.x, xs_hexa,
            piezo.x, xs,
            piezo.y, ys,
            piezo.z, zs,
        )

        yss = np.linspace(ys, ys + 0, 52)
        xss = np.array([xs])

        yss, xss = np.meshgrid(yss, xss)
        yss = yss.ravel()
        xss = xss.ravel()

        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)
            # Do not take SAXS when WAXS detector in the way
            dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]

            name_fmt = "{sample}_pos1_{energy}eV_wa{wax}_bpm{xbpm}"

            for e, xsss, ysss in zip(energies, xss, yss):
                yield from bps.mv(energy, e)
                yield from bps.sleep(2)
                if xbpm2.sumX.get() < 50:
                    yield from bps.sleep(2)
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                yield from bps.mv(piezo.y, ysss,
                                  piezo.x, xsss)
                
                bpm = xbpm2.sumX.get()
                bpm = str(np.round(float(bpm), 3)).zfill(5)
                pos = 1
                #sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, wax=wa, xbpm="%4.3f"%bpm)
                sample_name = f'{name}_pos{pos}{get_scan_md(tender=True)}_bpm{bpm}'
                sample_id(user_name="IB", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets)

            yield from bps.sleep(2)
            yield from bps.mv(energy, 15200)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 15180)
            yield from bps.sleep(2)



def swaxs_Br_edge_2023_3(t=1):
    dets = [pil1M, pil900KW]
    # dets = [pil1M]

    det_exposure_time(t, t)

    # names = ['kaptom',   'LiBr_sol_no_solv-b',  'NaBr_sol_no_solv-b',     'KBr_sol_no_solv-b',  'RbBr_sol_no_solv-b']
    # x_piezo = [-26400, -20200, -14000, -7600, -1400]
    # x_hexa =  [     0,      0,      0,     0,     0]
    # y_piezo = [ -4656,  -4656,  -4656, -4656, -4656]
    # z_piezo = [  -200,   -200,   -200,  -200,  -200] #used in initial measurements, 11/30/2023, about 11 am

    # names = ['water-a',   'DIPA_LiBr_org_phase-a',  
    #          'DIPA_RbBr_org_phase-a',     'DIPA_NaBr_aq_phase-a',  
    #          'DIPA_KBr_aq_phase-a', 'DIPA_RbBr_aq_phase-a']
    # x_piezo = [-13700,  -7550,  -1400,  5100, 11300, 17650]
    # x_hexa =  [     0,      0,      0,     0,     0,     0]
    # y_piezo = [ -4306,  -4306,  -4306, -4306, -4306, -4306]
    # z_piezo = [  -200,   -200,   -200,  -200,  -200,   200] # used for second batch of samples, exposure time 1s, 11/30/2023 starting 2:19 pm

    # names = ['KBr_sol_no_solv-c',   'LiBr_sol_no_solv-c', 'water-c',
    #          'DIPA_LiBr_org_phase-c', 'DIPA_RbBr_org_phase-c',
    #          'DIPA_NaBr_aq_phase-c', 'DIPA_KBr_aq_phase-c',
    #          'DIPA_RbBr_aq_phase-c', 'kapton-c',
    #          'RbBr_sol_no_solv-c', 'NaBr_sol_no_solv-c'
    #          ] # used for longer exposure on the night between 11/30 and 12/1. Used longer exposure time.

    # x_piezo = [-26100, -19600, -12900,
    #            -6700, -450,
    #            6200, 12400,
    #            18750, 25100,
    #            31400, 38050]
    # x_hexa =  [0,0,0,0,0,0,0,0,0,0,0]
    # y_piezo = [ -4306,  -4306,  -4306, -4306, -4306, -4306, -4306,  -4306,  -4306, -4306, -4306]
    # z_piezo = [  -200,   -200,   -200,  -200,  -200,   -200,  -200,   -200,   -200,  -200,  -200]

    names = ['DIPA', 'DIPA_H2O', 'DIPA_NaBr_org_phase', 'DIPA_KBr_org_phase', 'TOA', 'TOA_LiBr_org_phase_1',
             'TOA_LiBr_org_phase_2', 'TOA_NaBr_org_phase', 'TOA_KBr_org_phase', 'TOA_RbBr_org_phase'] # second set of samples
    x_piezo = [-33150, -27450, -20500,-14550, -8150, -1850, 
               4850, 11250, 17800, 23950]
    x_hexa = [0,0,0,0,0,0,
              0,0,0,0]
    y_piezo=[-4306,-4306,-4306,-4306,-4306,-4306,
              -4306,-4306,-4306,-4306]
    z_piezo = [-200,-200,-200,-200,-200,-200,
              -200,-200,-200,-200]

    names = ['DIPA_H2O', 'DIPA_NaBr_org_phase', 'DIPA_KBr_org_phase', 'TOA', 'TOA_LiBr_org_phase_1',
             'TOA_LiBr_org_phase_2', 'TOA_NaBr_org_phase', 'TOA_KBr_org_phase', 'TOA_RbBr_org_phase'] # second set of samples
    x_piezo = [-27450, -20500,-14550, -8150, -1850, 
               4850, 11250, 17800, 23950]
    x_hexa = [0,0,0,0,0,
              0,0,0,0]
    y_piezo=[-4306,-4306,-4306,-4306,-4306,
              -4306,-4306,-4306,-4306]
    z_piezo = [-200,-200,-200,-200,-200,
              -200,-200,-200,-200]

    msg = "Wrong number of coordinates, check names, piezos, and hexas"
    assert len(x_piezo) == len(names), msg
    assert len(x_piezo) == len(y_piezo), msg
    assert len(x_piezo) == len(z_piezo), msg
    assert len(x_piezo) == len(x_hexa), msg

    energies = np.concatenate((
        np.arange(13450, 13460, 5),
        np.arange(13460, 13465, 1),
        np.arange(13465, 13475, 0.5),
        np.arange(13475, 13485, 2),
        np.arange(13485, 13531, 5),
    ))

    waxs_arc = [0, 20, 40]
    # waxs_arc = [40]

    det_exposure_time(t, t)

    for name, xs, ys, zs, xs_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa):
        yield from bps.mv(
            stage.x, xs_hexa,
            piezo.x, xs,
            piezo.y, ys,
            piezo.z, zs,
        )

        yss = np.linspace(ys, ys + 0, len(energies))
        xss = np.array([xs])

        yss, xss = np.meshgrid(yss, xss)
        yss = yss.ravel()
        xss = xss.ravel()

        if waxs.arc.position>20:
            waxs_arc = [40, 20, 0]
        else:
            waxs_arc = [0, 20, 40]


        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)
            # Do not take SAXS when WAXS detector in the way
            dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]

            name_fmt = "{sample}_pos1_{energy}eV_wa{wax}_bpm{xbpm}"

            for e, xsss, ysss in zip(energies, xss, yss):
                yield from bps.mv(energy, e)
                yield from bps.sleep(1)
                if xbpm2.sumX.get() < 3:
                    yield from bps.sleep(2)
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                yield from bps.mv(piezo.y, ysss)
                yield from bps.mv(piezo.x, xsss)
                
                bpm = xbpm2.sumX.get()
                bpm = str(np.round(float(bpm), 3)).zfill(5)
                pos = 1
                #sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, wax=wa, xbpm="%4.3f"%bpm)
                sample_name = f'{name}_pos{pos}{get_scan_md(tender=True)}_bpm{bpm}'
                sample_id(user_name="IB", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 13530)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 13470)
            yield from bps.sleep(2)



def swaxs_Rb_edge_2023_3(t=1):
    dets = [pil1M, pil900KW]
    # dets = [pil1M]

    det_exposure_time(t, t)

    # names = ['kaptom',   'LiBr_sol_no_solv-b',  'NaBr_sol_no_solv-b',     'KBr_sol_no_solv-b',  'RbBr_sol_no_solv-b']
    # x_piezo = [-26400, -20200, -14000, -7600, -1400]
    # x_hexa =  [     0,      0,      0,     0,     0]
    # y_piezo = [ -4656,  -4656,  -4656, -4656, -4656]
    # z_piezo = [  -200,   -200,   -200,  -200,  -200]

    # names = ['DIPA_RbBr_org_phase_Rb_kedge', 'DIPA_RbBr_aq_phase_Rb_kedge', 
    #          'RbBr_sol_no_solv_Rb_kedge','kapton_Rb_kedge', 'water_Rb_kedge'] #used in the Rb K-edge measurements
    # x_piezo = [-450,  18750,  31400,  25100, -12900]
    # x_hexa =  [     0,      0,      0,     0,     0]
    # y_piezo = [ -4306,  -4306,  -4306, -4306, -4306]
    # z_piezo = [  -200,   -200,   -200,  -200,  -200]
    

    # names = ['kapton_Rb_kedge', 'water_Rb_kedge'] #used in the Rb K-edge measurements, exposure time 10s, waxs detector at 40 deg
    # x_piezo = [ 25100, -12900]
    # x_hexa =  [        0,     0]
    # y_piezo = [  -4306, -4306]
    # z_piezo = [    -200,  -200]

    # TOA Rb samples
    names = [
        'TOA_Rb_kedge', 'TOA_RbBr_org_phase_Rb_kedge' 
    ]
    x_piezo = [-8150, 23950]
    x_hexa =  [0, 0]
    y_piezo = [-4306, -4306]
    z_piezo = [-200, -200]

    msg = "Wrong number of coordinates, check names, piezos, and hexas"
    assert len(x_piezo) == len(names), msg
    assert len(x_piezo) == len(y_piezo), msg
    assert len(x_piezo) == len(z_piezo), msg
    assert len(x_piezo) == len(x_hexa), msg

    energies = np.concatenate((
        np.arange(15175, 15185, 5),
        np.arange(15185, 15190, 1),
        np.arange(15190, 15200, 0.5),
        np.arange(15200, 15210, 2),
        np.arange(15210, 15260, 5),
    ))

    waxs_arc = [0, 20, 40]
    # waxs_arc = [40]

    det_exposure_time(t, t)

    for name, xs, ys, zs, xs_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa):
        yield from bps.mv(
            stage.x, xs_hexa,
            piezo.x, xs,
            piezo.y, ys,
            piezo.z, zs,
        )

        yss = np.linspace(ys, ys + 0, len(energies))
        xss = np.array([xs])

        yss, xss = np.meshgrid(yss, xss)
        yss = yss.ravel()
        xss = xss.ravel()

        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)
            # Do not take SAXS when WAXS detector in the way
            # dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]

            name_fmt = "{sample}_pos1_{energy}eV_wa{wax}_bpm{xbpm}"

            for e, xsss, ysss in zip(energies, xss, yss):
                yield from bps.mv(energy, e)
                yield from bps.sleep(2)
                if xbpm2.sumX.get() < 50:
                    yield from bps.sleep(2)
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                yield from bps.mv(piezo.y, ysss)
                yield from bps.mv(piezo.x, xsss)
                
                bpm = xbpm2.sumX.get()
                bpm = str(np.round(float(bpm), 3)).zfill(5)
                pos = 1
                #sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, wax=wa, xbpm="%4.3f"%bpm)
                sample_name = f'{name}_pos{pos}{get_scan_md(tender=True)}_bpm{bpm}'
                sample_id(user_name="IB", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 15230)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 15200)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 15175)
            yield from bps.sleep(2)

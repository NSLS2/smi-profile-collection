def alignement_katz_2021_1():
    global names, x_piezo, y_piezo, z_piezo, incident_angles, y_piezo_aligned
    
    names =   ['sample1', 'sample2', 'sample3', 'sample4', 'sample5', 'sample6', 'sample7']
    x_piezo = [   55000,     42000,     19000,      2000,    -16000,    -31000,    -49000]
    y_piezo = [    4800,      2900,      2900,      2900,      2900,      2900,      3300]
    x_hexa =  [       7,         0,         0,         0,         0,         0,         0]

    incident_angles = [       0,      0,        0,        0,        0,        0,       0]
    y_piezo_aligned = [4757.703, 3054.9, 3133.065, 3031.989, 3414.158, 3546.666, 3715.74]

    #sample2: y = 5332.784, th = 0.973826
    #sample 4:: th [2, 0.9738, 2, 0.97, 0.582, 0.297, 0.0655], y: [7100, 5332.784, 5142.4, 4975.875, 5447.996, 5487.398, 5792.193]

    # incident_angles = [2, 0.9738, 2, 0.97, 0.582, 0.297, 0.0655]
    # y_piezo_aligned = [7100, 5332.784, 5142.4, 4975.875, 5447.996, 5487.398, 5792.193]

    smi = SMI_Beamline()
    yield from smi.modeAlignment(technique='gisaxs')


    for name, xs_piezo, ys_piezo, xs_hexa in zip(names, x_piezo, y_piezo, x_hexa):
        yield from bps.mv(stage.x, xs_hexa)

        yield from bps.mv(piezo.x, xs_piezo)
        yield from bps.mv(piezo.y, ys_piezo)
        # yield from alignement_gisaxs(0.3)

        yield from alignement_gisaxs_multisample_special(angle = 0.25)

        y_piezo_aligned = y_piezo_aligned + [piezo.y.position]

    yield from smi.modeMeasurement()

    print(incident_angles)



def nexafs_Sedge_Katz(t=1):
    dets = [pil300KW, pil900KW]


    names =   ['sample1', 'sample2', 'sample3', 'sample4', 'sample5', 'sample6', 'sample7']
    x_piezo = [   55000,     42000,     19000,      2000,    -16000,    -31000,    -49000]
    y_piezo = [    4800,      2900,      2900,      2900,      2900,      2900,      3300]
    x_hexa =  [       7,         0,         0,         0,         0,         0,         0]

    incident_angles = [       0,      0,        0,        0,        0,        0,       0]
    y_piezo_aligned = [4757.703, 3054.9, 3133.065, 3031.989, 3414.158, 3546.666, 3715.74]


    energies = 7 + np.asarray(np.arange(2445, 2470, 5).tolist() + np.arange(2470, 2480, 0.25).tolist() + np.arange(2480, 2490, 1).tolist()+ np.arange(2490, 2501, 5).tolist())
    waxs_arc = [52.5]

    for name, xs, ys, zs, aiss, ys in zip(names, x_piezo, y_piezo, z_piezo, incident_angles, y_piezo_aligned):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)
        yield from bps.mv(piezo.th, aiss + 0.7)

        ai0 = piezo.th.position

        yield from bps.mv(waxs, waxs_arc[0])    
        det_exposure_time(t,t) 
        name_fmt = 'nexafs_{sample}_{energy}eV_wa60.0_bpm{xbpm}'
        for e in energies: 
            yield from bps.mv(energy, e)
            yield from bps.sleep(1)

            bpm = xbpm2.sumX.value

            sample_name = name_fmt.format(sample=name, energy='%6.2f'%e, xbpm = '%4.3f'%bpm)
            sample_id(user_name='GF', sample_name=sample_name)
            print(f'\n\t=== Sample: {sample_name} ===\n')
            yield from bp.count(dets, num=1)

        yield from bps.mv(energy, 2490)
        yield from bps.mv(energy, 2470)
        yield from bps.mv(energy, 2450)




def nexafs_Caedge_Katz(t=1):
    dets = [pil300KW]

    names =   ['sample7_1']

    energies = np.linspace(4030, 4110, 81)
    waxs_arc = [52.5]

    for name in names:

        ai0 = piezo.th.position

        yield from bps.mv(waxs, waxs_arc[0])    
        det_exposure_time(t,t) 
        name_fmt = 'nexafs_{sample}_{energy}eV_wa52.5_ai0.7deg_bpm{xbpm}'
        for e in energies: 
            yield from bps.mv(energy, e)
            yield from bps.sleep(1)

            bpm = xbpm2.sumX.value

            sample_name = name_fmt.format(sample=name, energy='%6.2f'%e, xbpm = '%4.3f'%bpm)
            sample_id(user_name='GF', sample_name=sample_name)
            print(f'\n\t=== Sample: {sample_name} ===\n')
            yield from bp.count(dets, num=1)

        yield from bps.mv(energy, 4100)
        yield from bps.mv(energy, 4080)
        yield from bps.mv(energy, 4050)





def saxs_14keV_Matt_2021_2(t=1): 

    
    xlocs = [44000, 35000, 21500, 11000, -1000, -12000, -23000, -36000, 44000, 32500, 21000, 10000, -2000, -13500]
    ylocs = [-5000, -4500, -5000, -5000, -5000,  -5000,  -5000,  -5000,  8000,  8000,  8000,  8000,  8000,   8000]
    zlocs = [ 2700,  2700,  2700,  2700,  2700,   2700,   2700,   2700,  2700,  2700,  2700,  2700,  2700,   2700]
    names = ['MWET_01', 'MWET_02', 'MWET_03', 'MWET_04', 'MWET_05', 'MWET_06', 'MWET_07a', 'MWET_07b', 'MWET_08', 'MWET_09', 'MWET_10', 'MWET_11',
    'MWET_12', 'MWET_13']


    user = 'ML'    
    det_exposure_time(t,t)     
    
    assert len(xlocs) == len(names), f'Number of X coordinates ({len(xlocs)}) is different from number of samples ({len(names)})'
    
    # Detectors, motors:
    dets = [pil300KW, pil900KW, pil1M]
    waxs_range = [0, 2, 19.5, 21.5, 39, 41]

    ypos = [-500, 500, 3]

    for wa in waxs_range[::-1]:
        yield from bps.mv(waxs, wa)
        for sam, x, y, z in zip(names, xlocs, ylocs, zlocs):
            yield from bps.mv(piezo.x, x)            
            yield from bps.mv(piezo.y, y)
            yield from bps.mv(piezo.z, z)

            name_fmt = '{sam}_stats1_14.0keV_sdd8.3m_wa{waxs}'
            sample_name = name_fmt.format(sam=sam,  waxs='%2.1f'%wa)
            sample_id(user_name=user, sample_name=sample_name) 
            print(f'\n\t=== Sample: {sample_name} ===\n')
            yield from bp.rel_scan(dets, piezo.y, *ypos)
            yield from bps.sleep(2)

    sample_id(user_name='test', sample_name='test')
    det_exposure_time(0.3, 0.3) 



def saxs_2p4keV_Matt_2021_2(t=1): 

    
    xlocs = [44000, 35000, 21500, 11000, -1000, -12000, -23000, -36000, 44000, 32500, 21000, 10000, -2000, -13500]
    ylocs = [-5000, -4500, -5000, -5000, -5000,  -5000,  -5000,  -5000,  8000,  8000,  8000,  8000,  8000,   8000]
    zlocs = [ 2700,  2700,  2700,  2700,  2700,   2700,   2700,   2700,  2700,  2700,  2700,  2700,  2700,   2700]
    names = ['MWET_01', 'MWET_02', 'MWET_03', 'MWET_04', 'MWET_05', 'MWET_06', 'MWET_07a', 'MWET_07b', 'MWET_08', 'MWET_09', 'MWET_10', 'MWET_11',
    'MWET_12', 'MWET_13']


    user = 'ML'    
    det_exposure_time(t,t)     
    
    assert len(xlocs) == len(names), f'Number of X coordinates ({len(xlocs)}) is different from number of samples ({len(names)})'
    
    # Detectors, motors:
    dets = [pil300KW, pil900KW, pil1M]
    waxs_range = [0, 2, 19.5, 21.5, 39, 41]

    ypos = [-500, 500, 3]

    for wa in waxs_range[::-1]:
        yield from bps.mv(waxs, wa)
        for sam, x, y, z in zip(names, xlocs, ylocs, zlocs):
            yield from bps.mv(piezo.x, x)            
            yield from bps.mv(piezo.y, y)
            yield from bps.mv(piezo.z, z)

            name_fmt = '{sam}_stats1_2.45keV_sdd3.0m_wa{waxs}'
            sample_name = name_fmt.format(sam=sam,  waxs='%2.1f'%wa)
            sample_id(user_name=user, sample_name=sample_name) 
            print(f'\n\t=== Sample: {sample_name} ===\n')
            yield from bp.rel_scan(dets, piezo.y, *ypos)
            yield from bps.sleep(2)

    sample_id(user_name='test', sample_name='test')
    det_exposure_time(0.3, 0.3) 



def nexafs_Sedge_Katz_2021_2(t=1):
    dets = [pil300KW, pil900KW]


    x_piezo = [ 32500]
    y_piezo = [ 8000]
    z_piezo = [  2700]
    names = ['MWET_09']


    energies = np.linspace(2450, 2530, 81)
    waxs_arc = [59]

    for name, xs, ys, zs in zip(names, x_piezo, y_piezo, z_piezo):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)

        yield from bps.mv(waxs, waxs_arc[0])    
        det_exposure_time(t,t) 
        name_fmt = 'nexafs_{sample}_{energy}eV_wa59_bpm{xbpm}'
        for e in energies: 
            yield from bps.mv(energy, e)
            yield from bps.sleep(2)

            bpm = xbpm2.sumX.value

            sample_name = name_fmt.format(sample=name, energy='%6.2f'%e, xbpm = '%4.3f'%bpm)
            sample_id(user_name='GF', sample_name=sample_name)
            print(f'\n\t=== Sample: {sample_name} ===\n')
            yield from bp.count(dets, num=1)

        yield from bps.mv(energy, 2500)
        yield from bps.mv(energy, 2480)
        yield from bps.mv(energy, 2450)






def nexafs_Sedge_Katz_2021_2(t=1):
    dets = [pil900KW]

    # names =   ['sample1', 'sample2', 'sample3', 'sample4', 'sample5']
    # x_piezo = [    54000,     38000,     18000,      3000,    -17000]
    # inc_angl = [ -0.6074,   -0.4144,     0.185,   -0.1982,   -2.4638]
    # y_piezo = [  4647.88,   5180.45,   4970.04,    4909.86,  5090.90]

    names =   [ 'sample4_redo']
    x_piezo = [    3200]
    inc_angl = [   -0.1982]
    y_piezo = [  4890.86]

    energies = 7 + np.asarray(np.arange(2445, 2470, 5).tolist() + np.arange(2470, 2480, 0.25).tolist() + np.arange(2480, 2490, 1).tolist()+ np.arange(2490, 2501, 5).tolist())
    waxs_arc = 60

    angle_mes = [0.1]

    for name, xs, ys, aiss in zip(names, x_piezo, y_piezo, inc_angl):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.th, aiss)

        yield from bps.mv(waxs, 59)    
        det_exposure_time(t,t) 
        
        for angle_me in angle_mes:
            yield from bps.mv(piezo.th, aiss + angle_me)

            name_fmt = 'nexafs_{sample}_{energy}eV_wa60_bpm{xbpm}_ai{ai}'
            for e in energies: 
                yield from bps.mv(energy, e)
                yield from bps.sleep(2)

                bpm = xbpm2.sumX.value

                sample_name = name_fmt.format(sample=name, energy='%6.2f'%e, xbpm = '%4.3f'%bpm, ai='%1.2f'%angle_me)
                sample_id(user_name='GF', sample_name=sample_name)
                print(f'\n\t=== Sample: {sample_name} ===\n')
                yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 2490)
            yield from bps.mv(energy, 2470)
            yield from bps.mv(energy, 2450)




def nexafs_Caedge_David(t=1):
    dets = [pil900KW]

    # names =   ['sample1', 'sample2', 'sample3', 'sample4', 'sample5']
    # x_piezo = [    54000,     38000,     18000,      3000,    -17000]
    # inc_angl = [ -0.6074,   -0.4144,     0.185,   -0.1982,   -2.4638]
    # y_piezo = 40 + np.asarray([  4647.88,   5180.45,   4970.04,    4909.86,  5090.90])
    names =   ['sample3', 'sample4', 'sample5']
    x_piezo = [      18000,      3000,    -17000]
    inc_angl = [      0.185,   -0.1982,   -2.4638]
    y_piezo = 40 + np.asarray([  4970.04,    4909.86,  5090.90])

    # names =   [ 'sample2', 'sample3', 'sample4', 'sample5']
    # x_piezo = [         38000,     18000,      3000,    -17000]
    # inc_angl = [    -0.4144,     0.185,   -0.1982,   -2.4638]
    # y_piezo = 40 + np.asarray([     5180.45,   4970.04,    4909.86,  5090.90])


    # energies = np.linspace(4030, 4110, 81)
    energies = np.asarray(np.arange(4020, 4035, 5).tolist() + np.arange(4035, 4042, 2).tolist() + np.arange(4042, 4070, 0.5).tolist() + np.arange(4070, 4080, 2).tolist() + np.arange(4080, 4130, 5).tolist())

    for name, xs, ys, aiss in zip(names, x_piezo, y_piezo, inc_angl):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.th, aiss)

        yield from bps.mv(waxs, 59)    
        det_exposure_time(t,t) 
        
        angle_mes = [0.1]

        for angle_me in angle_mes:
            yield from bps.mv(piezo.th, aiss + angle_me)

            name_fmt = 'nexafs_{sample}_{energy}eV_wa60_ai{ai}_bpm{xbpm}'
            for e in energies: 
                yield from bps.mv(energy, e)
                yield from bps.sleep(2)

                bpm = xbpm2.sumX.value

                sample_name = name_fmt.format(sample=name, energy='%6.2f'%e, ai='%1.2f'%angle_me , xbpm = '%4.3f'%bpm)
                sample_id(user_name='GF', sample_name=sample_name)
                print(f'\n\t=== Sample: {sample_name} ===\n')
                yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 4100)
            yield from bps.mv(energy, 4080)
            yield from bps.mv(energy, 4050)




def nexafs_Caedge_Matt(t=0.5, name='test'):
    yield from bps.mv(waxs, 59)
    dets = [pil900KW]

    energies = np.asarray(np.arange(4020, 4035, 5).tolist() + np.arange(4035, 4042, 2).tolist() + np.arange(4042, 4070, 0.5).tolist() + np.arange(4070, 4080, 2).tolist() + np.arange(4080, 4140, 5).tolist())

    samples = ['mwet_01', 'mwet_02', 'mwet_03', 'mwet_04', 'mwet_05', 'mwet_06', 'mwet_07', 'mwet_08', 'mwet_09', 'mwet_10', 'mwet_11']
    x_list  = [    46000,     35000,     22500,     11000,         0,    -12000,    -24000,    -35000,     24000,     12000,         0]
    y_list =  [    -8500,     -8500,     -8500,     -8500,     -8500,     -8500,     -8500,     -8500,      4500,      4500,      4500]
    

    for name, x, y in zip(samples, x_list, y_list):
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(piezo.y, y)

        det_exposure_time(t,t) 
        name_fmt = 'nexafs_{sample}_{energy}eV_wa60_bpm{xbpm}'
        for e in energies:                              
            yield from bps.mv(energy, e)
            yield from bps.sleep(2)

            bpm = xbpm2.sumX.value
            sample_name = name_fmt.format(sample=name, energy='%6.2f'%e, xbpm = '%4.3f'%bpm)
            sample_id(user_name='GS', sample_name=sample_name)
            print(f'\n\t=== Sample: {sample_name} ===\n')
            yield from bp.count(dets, num=1)

        yield from bps.mv(energy, 4110)
        yield from bps.sleep(2)
        yield from bps.mv(energy, 4070) 
        yield from bps.sleep(2)       
        yield from bps.mv(energy, 4030)
        yield from bps.sleep(2)


        sample_id(user_name='test', sample_name='test')


def saxs_prep_multisample(t=1):
    dets = [pil900KW, pil1M]

    energies = [4030, 4040, 4050, 4055, 4075]
    det_exposure_time(t,t)     
    waxs_range = [0, 2, 19.5, 21.5, 39, 41]

    det_exposure_time(t,t)

    xpos = [-500, 500, 3]

    for wa in waxs_range[::-1]:
        yield from bps.mv(waxs, wa)

        samples = ['mwet_01', 'mwet_02', 'mwet_03', 'mwet_04', 'mwet_05', 'mwet_06', 'mwet_07', 'mwet_08', 'mwet_09', 'mwet_10', 'mwet_11']
        x_list  = [    46000,     35000,     22500,     11000,         0,    -12000,    -24000,    -35000,     24000,     12000,         0]
        y_list =  100+ np.asarray([    -8500,     -8500,     -8500,     -8500,     -8500,     -8500,     -8500,     -8500,      4500,      4500,      4500])

        for name, x, y in zip(samples, x_list, y_list):
            yield from bps.mv(piezo.x, x)
            yield from bps.mv(piezo.y, y)

            for k, e in enumerate(energies):                              
                yield from bps.mv(energy, e)
                yield from bps.sleep(2)

                yield from bps.mv(piezo.y, y + k * 100)

                name_fmt = '{sample}_{energy}eV_xbpm{xbpm}_wa{wa}'
                bpm = xbpm2.sumX.value

                sample_name = name_fmt.format(sample=name,energy='%6.2f'%e, xbpm = '%3.1f'%bpm, wa='%2.1f'%wa)
                sample_id(user_name='OS', sample_name=sample_name)
                print(f'\n\t=== Sample: {sample_name} ===\n')
                yield from bp.rel_scan(dets, piezo.x, *xpos)
                        
            yield from bps.mv(energy, 4050)
            yield from bps.mv(energy, 4030)




def K_edge_xscan_2024_2(t=1):
    dets = [pil900KW, amptek]
    det_exposure_time(t, t)

    #names = ['PTTEG-3_S2_KClO4_exp']
    #x_min = [20.0]
    #x_max = [10.0]
    
    names = ['Edepo_pedot_KClO4_exp']
    x_min = [-13.0]
    x_max = [-19.0]


    step= 0.2
    assert len(x_min) == len(names), f"Number of X coordinates ({len(x_hexa)}) is different from number of samples ({len(names)})"
    assert len(x_max) == len(names), f"Number of X coordinates ({len(x_hexa)}) is different from number of samples ({len(y_hexa)})"

    energies = energy.energy.position

    waxs_arc = [20]
    ais = 0.80
    ai0 = stage.th.position

    for name, xmin, xmax in zip(names, x_min, x_max):
        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)
            # Do not take SAXS when WAXS detector in the way
            yield from bps.mv(stage.th, ai0 + ais)


            name_fmt = "{sample}_xscan_{energy}eV_x{x}_ai{ai}_wa{wax}_bpm{xbpm}"
            yield from bps.mv(energy, energies)
            yield from bps.sleep(2)
            yield from bps.sleep(2)

            # for ais in np.linspace(0.1, 0.8, 15):
            for xss in np.linspace(xmin, xmax, int(1+(xmin-xmax)/step)):
                # yield from bps.mv(stage.th, ai0+ais)                

                yield from bps.mv(stage.x, xss)                
                bpm = xbpm2.sumX.get()
                sample_name = name_fmt.format(sample=name, energy="%6.2f"%energies, x="%1.2f"%stage.x.position, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                sample_id(user_name="LR", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

            yield from bps.mv(stage.th, ai0)



def K_edge_timescan_2023_3(t=1):
    dets = [pil900KW, amptek]
    det_exposure_time(t, t)
    energies=energy.energy.position
    ais=0.8
    wa=0
    name = 'pgBTTT_KCl_sample3_Vds500mV_Vgs200mV_reversed_x14.5_timescan_try5'
    # name = 'test_timescan_try5'

    t0 = time.time()
    for i in range(100):
        t1 = time.time()
        name_fmt = "{sample}_{energy}eV_time{times}_ai{ai}_wa{wax}_bpm{xbpm}"
        bpm = xbpm2.sumX.get()
        sample_name = name_fmt.format(sample=name, energy="%6.2f"%energies, times="%1.2f"%(t1-t0), ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
        sample_id(user_name="LR", sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")
        yield from bp.count(dets, num=1)






def S_edge_measurments_2024_2_Jul3_night(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    # bottom left first
    names = [  'Edepo_pedot_100mM_5C',  'Edepo_pedot_100mM_10C', 'Edepo_pedot_100mM_30C','Edepo_pedot_100mM_50C', 
             'Edepo_pedot_100mM_100C', 'Edepo_pedot_100mM_200C',
                'Edepo_pedot_20mM_5C',   'Edepo_pedot_20mM_10C',  'Edepo_pedot_20mM_30C', 'Edepo_pedot_20mM_50C',
              'Edepo_pedot_20mM_100C',  'Edepo_pedot_20mM_200C']
             
    x_piezo = [                 57000,                    57000,                   48000,                  38000,
                                27000,                   16000,
                                3000,                    -9000,                   -20000,                   -31000]
    x_hexa = [                     15,                        3,                       0,                      0,
                                    0,                        0,
                                    0,                        0,                       0,                      0]
    y_piezo = [                  6500,                     6500,                    6500,                   6500,
                                 6500,                     6500,
                                 6500,                     6500,                    6500,                   6500]
    z_piezo = [                  3000,                     3000,                    3000,                   3000, 
                                 3000,                     3000,
                                 3000,                     3000,                    3000,                   3000]
    
    x_piezo = np.asarray(x_piezo)

    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(z_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexa)})"

    energies = [2450.0,2455.0,2460.0,2465.0,2470.0,2473.0,2475.0,2475.5,2476.0,2476.5,2477.0,2477.5,2478.0,2478.5,2479.0,2479.5,
    2480.0,2480.5,2481.0,2482.0,2483.0,2484.0,2485.0,2486.0, 2487.0,2488.0,2489.0,2490.0,2492.5,2495.0,2500.0,2510.0,2515.0]

    waxs_arc = [7, 20]
    ai0_all = 1
    ai_list = [2.2]

    for name, xs, ys, zs, xs_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa):
            yield from bps.mv(stage.x, xs_hexa)
            yield from bps.mv(piezo.x, xs)
            yield from bps.mv(piezo.y, ys)
            yield from bps.mv(piezo.z, zs)

            yield from bps.mv(piezo.th, ai0_all)
            yield from alignement_gisaxs_doblestack(0.8)

            #yield from bps.mv(att2_9.open_cmd, 1)
            #yield from bps.sleep(1)
            ##yield from bps.mv(att2_9.open_cmd, 1)
            #yield from bps.sleep(1)

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
                        yield from bps.mv(piezo.x, xs - counter * 20)
                        counter += 1
                        
                        bpm = xbpm2.sumX.get()
                        sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
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
                        yield from bps.mv(piezo.x, xs - counter * 20)
                        counter += 1

                        bpm = xbpm2.sumX.get()
                        sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                        sample_id(user_name="LR", sample_name=sample_name)
                        print(f"\n\t=== Sample: {sample_name} ===\n")
                        yield from bp.count(dets, num=1)

                yield from bps.mv(piezo.th, ai0)





def Cl_edge_measurments_2024_2_Jul3_night(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    # bottom left first
    names = [  'pg2T_as',  'pg2T_middoped', 'pg2T_doped','pg2T_dedoped', 
             'pg2T_exp', 'pgBT_as',
                'pgBT_middoped',   'pgBT_doped',  'pgBT_dedoped', 'pgBT_exp'
            ]
             
    x_piezo = [                 57000,                    57000,                   48000,                  38000,
                                27000,                   16000,
                                3000,                    -9000,                   -20000,                   -31000]
    x_hexa = [                     15,                        3,                       0,                      0,
                                    0,                        0,
                                    0,                        0,                       0,                      0]
    y_piezo = [                  6000,                     6000,                    6000,                   6000,
                                 6000,                     6000,
                                 6000,                     6000,                    6000,                   6000]
    z_piezo = [                  3000,                     3000,                    3000,                   3000, 
                                 3000,                     3000,
                                 3000,                     3000,                    3000,                   3000]
    
    names = [  
                'pgBT_middoped',   'pgBT_doped',  'pgBT_dedoped', 'pgBT_exp'
            ]
             
    x_piezo = [                 
                                3000,                    -9000,                   -20000,                   -31000]
    x_hexa = [                     
                                    0,                        0,                       0,                      0]
    y_piezo = [                  6400,                     6400,                    6400,                   6400,
                                 ]
    z_piezo = [                  3000,                     3000,                    3000,                   3000, 
                                 ]
    
    x_piezo = np.asarray(x_piezo)

    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(z_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexa)})"

    energies = np.asarray([2810.0, 2820.0, 2828.0, 2829.0, 2830.0, 2831.0, 2832.0, 2833.0, 2834.0, 2834.5, 2835.0, 2835.5, 2836.0, 2836.5, 2837.0, 2837.5, 2838.0, 2838.5, 2839.0,
    2839.5, 2840.0, 2840.5, 2841.0, 2841.5, 2845.0, 2850.0, 2855.0, 2860.0, 2865.0, 2870.0, 2875.0, 2880.0, 2890.0])


    waxs_arc = [7, 20]
    ai0_all = 1.5
    ai_list = [1.6, 3.2]

    for name, xs, ys, zs, xs_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa):
            yield from bps.mv(stage.x, xs_hexa)
            yield from bps.mv(piezo.x, xs)
            yield from bps.mv(piezo.y, ys)
            yield from bps.mv(piezo.z, zs)

            yield from bps.mv(piezo.th, ai0_all)
            yield from alignement_gisaxs_doblestack(0.8)

            yield from bps.mv(att2_9.open_cmd, 1)
            yield from bps.sleep(1)
            yield from bps.mv(att2_9.open_cmd, 1)
            yield from bps.sleep(1)

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
                        yield from bps.mv(piezo.x, xs - counter * 20)
                        counter += 1
                        
                        bpm = xbpm2.sumX.get()
                        sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
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
                        yield from bps.mv(piezo.x, xs - counter * 20)
                        counter += 1

                        bpm = xbpm2.sumX.get()
                        sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                        sample_id(user_name="LR", sample_name=sample_name)
                        print(f"\n\t=== Sample: {sample_name} ===\n")
                        yield from bp.count(dets, num=1)

                yield from bps.mv(piezo.th, ai0)





def KClO4_edge_measurments_2023_2_sva(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    # names = ['MM460_KClO4_partialdoped0V']
    # x_hexa = [-18.6]
    
    #MM460_dry_nistfrit 10 to 18 chi 0 th 3.457 y 0
    # names = ['PG2T-TT_nistfrit_KCl_redoped_0p6V']
    names = ['PTTEG-3_KClO4_redoped_600mV']

    x_hexa = [18]

    assert len(x_hexa) == len(names), f"Number of X coordinates ({len(x_hexa)}) is different from number of samples ({len(names)})"

    energies = np.asarray([2810.0, 2820.0, 2830.0, 2832.0, 2834.0, 2834.5, 2835.0, 2835.5, 2836.0, 2836.5, 2837.0, 2837.5, 2838.0, 2838.5, 2839.0,
    2839.5, 2840.0, 2840.5, 2841.0, 2841.5, 2845.0, 2850.0, 2855.0, 2860.0, 2865.0, 2870.0, 2875.0, 2880.0, 2890.0])
    
    waxs_arc = [7]
    ai_list = [1.6]

    for name, xs_hexa in zip(names, x_hexa):
        yield from bps.mv(stage.x, xs_hexa)

        # No alignement 
        # yield from bps.mv(stage.th, ai0)
        # yield from alignement_gisaxs_hex(0.8)

        ##yield from bps.mv(att2_9.open_cmd, 1)
        #yield from bps.sleep(1)
        #yield from bps.mv(att2_9.open_cmd, 1)
        #yield from bps.sleep(1)

        ai0 = stage.th.position
        det_exposure_time(t, t)

        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)
            # Do not take SAXS when WAXS detector in the way
            dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]

            counter = 0

            for k, ais in enumerate(ai_list):
                yield from bps.mv(stage.th, ai0 + ais)

                name_fmt = "{sample}_pos1_{energy}eV_x{x}_ai{ai}_wa{wax}_bpm{xbpm}"
                x="%1.2f"%stage.x.position
                for e in energies:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(stage.x, xs_hexa - counter * 0.030)
                    counter += 1
                    
                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, x=x, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)

                x="%1.2f"%stage.x.position
                name_fmt = "{sample}_pos2_{energy}eV_x{x}_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies[::-1]:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(stage.x, xs_hexa - counter * 0.030)
                    counter += 1

                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, x=x, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)
            yield from bps.mv(stage.th, ai0)

def Fluo_standards_2024_2_Jul5_night(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    # bottom left first
    #4 samples on bottom row, rest is on top row
    names = [  'NaPSS_KCl_4_1',  'NaPSS_KCl_8_1', 'NaPSS_KCl_16_1','NaPSS_KCl_32_1', 
               'NaPSS_5k',       'NaPSS_3k',
               'NaPSS_NaCl_1_1', 'NaPSS_NaCl_2_1',  'NaPSS_NaCl_4_1', 'NaPSS_NaCl_8_1',
               'NaPSS_NaCl_16_1','NaPSS_NaCl_32_1',
               'NaPSS_KCl_1_1',  'NaPSS_KCl_2_1'
            ]
    #need to set right y_piezo and z_piezo still         
    x_piezo = [                 57000,                   57000,                    33000,                   14000,
                                57000,                   57000,
                                57000,                   46000,                    31000,                   17000,
                                 2000,                  -13000,
                               -26000,                  -32000]
    x_hexa = [                     18,                        0,                       0,                      0,
                                   27,                       15,
                                    0,                        0,                       0,                      0,
                                    0,                        0,
                                    0,                       -5]
    y_piezo = [                  5400,                    5600,                    5800,                   5000,
                                 -4000,                     -3300,
                                 -3100,                    -2900,                   -2700,                   -2500,
                                 6000,                     6000,
                                 -2300,                     -2100]
    z_piezo = [                  3000,                     3000,                    3000,                   3000, 
                                 3000,                     3000,
                                 3000,                     3000,                    3000,                   3000,
                                 3000,                     3000,
                                 3000,                     3000]
    names = [  
               'NaPSS_NaCl_16_1','NaPSS_NaCl_32_1',
               'NaPSS_KCl_1_1',  'NaPSS_KCl_2_1'
            ]
    x_piezo = [                 
                                 2000,                  -13000,
                               -26000,                  -32000]
    x_hexa = [                     
                                    0,                        0,
                                    0,                       -5]
    y_piezo = [                  
                                 -2200,                     -1900,
                                 -1300,                     -1100]
    z_piezo = [                 
                                 3000,                     3000,
                                 3000,                     3000]

    waxs_arc = [0]
    ai0_all = 0
    ai_list = [1.6, 3.2]

    for name, xs, ys, zs, xs_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa):
            yield from bps.mv(stage.x, xs_hexa)
            yield from bps.mv(piezo.x, xs)
            yield from bps.mv(piezo.y, ys)
            yield from bps.mv(piezo.z, zs)

            yield from bps.mv(piezo.th, ai0_all)
            yield from alignement_gisaxs_doblestack(0.8)
            yield from bps.mv(att2_10.open_cmd, 1)
            yield from bps.sleep(1)
            yield from bps.mv(att2_10.open_cmd, 1)
            yield from bps.sleep(1)
            
            ai0 = piezo.th.position
            det_exposure_time(t, t)

            for i, wa in enumerate(waxs_arc):
                yield from bps.mv(waxs, wa)
                # Do not take SAXS when WAXS detector in the way
                dets = [pil900KW, amptek]

                yield from bps.mv(piezo.x, xs)
                counter = 0

                for k, ais in enumerate(ai_list):
                    yield from bps.mv(piezo.th, ai0 + ais)
                    yield from bps.mv(stage.x, xs_hexa - counter * 0.20)

                    name_fmt = "{sample}_pos1_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                    
                    e=4000
                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)
                    counter += 1


                    yield from bps.mv(stage.x, xs_hexa - counter * 0.20)
                    name_fmt = "{sample}_pos2_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                    
                    e=4000
                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)
                    counter += 1



                yield from bps.mv(piezo.th, ai0)





def Cl_edge_measurments_2024_3(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    # bottom left first
    names = [   'Si', 'pgBTTT_as', 'pgBTTT_exp', 'pgBTTT_middoped', 'pgBTTT_dedoped', 'pgBTpgBTTT_overdoped']
    x_piezo = [50000,       36000,        11500,             -1700,           -14000,                 -28000]
    x_hexa = [     0,           0,            0,                 0,                0,                      0]
    y_piezo = [ 6900,        6900,         6900,              6900,             6900,                   6900]
    z_piezo = [ 3800,        3800,         3800,              3800,             3800,                   3800]
    
    x_piezo = np.asarray(x_piezo)

    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(z_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexa)})"

    energies = np.asarray([2810.0, 2820.0, 2828.0, 2829.0, 2830.0, 2831.0, 2832.0, 2833.0, 2834.0, 2834.5, 2835.0, 2835.5, 2836.0, 2836.5, 2837.0, 2837.5, 2838.0, 2838.5, 2839.0,
    2839.5, 2840.0, 2840.5, 2841.0, 2841.5, 2845.0, 2850.0, 2855.0, 2860.0, 2865.0, 2870.0, 2875.0, 2880.0, 2890.0])

    waxs_arc = [7, 20]
    ai0_all = 0
    ai_list = [1.6]

    for name, xs, ys, zs, xs_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa):
            yield from bps.mv(stage.x, xs_hexa)
            yield from bps.mv(piezo.x, xs)
            yield from bps.mv(piezo.y, ys)
            yield from bps.mv(piezo.z, zs)

            yield from bps.mv(piezo.th, ai0_all)
            yield from alignement_gisaxs_doblestack(0.3)

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
                        yield from bps.mv(piezo.x, xs - counter * 50)
                        counter += 1
                        
                        bpm = xbpm2.sumX.get()
                        sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
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
                        yield from bps.mv(piezo.x, xs - counter * 50)
                        counter += 1

                        bpm = xbpm2.sumX.get()
                        sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                        sample_id(user_name="LR", sample_name=sample_name)
                        print(f"\n\t=== Sample: {sample_name} ===\n")
                        yield from bp.count(dets, num=1)

                yield from bps.mv(piezo.th, ai0)


    waxs_arc = [7, 20]
    ai_list = [3.2]

    for name, xs, ys, zs, xs_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa):
            yield from bps.mv(stage.x, xs_hexa)
            yield from bps.mv(piezo.x, xs)
            yield from bps.mv(piezo.y, ys)
            yield from bps.mv(piezo.z, zs)

            yield from bps.mv(piezo.th, ai0_all)
            yield from alignement_gisaxs_doblestack(0.8)

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
                        yield from bps.mv(piezo.x, xs - counter * 50)
                        counter += 1
                        
                        bpm = xbpm2.sumX.get()
                        sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
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
                        yield from bps.mv(piezo.x, xs - counter * 50)
                        counter += 1

                        bpm = xbpm2.sumX.get()
                        sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                        sample_id(user_name="LR", sample_name=sample_name)
                        print(f"\n\t=== Sample: {sample_name} ===\n")
                        yield from bp.count(dets, num=1)

                yield from bps.mv(piezo.th, ai0)



def bpmvspindiode_Cledge_2024_3(t=1):
    dets = [pil1M]
    det_exposure_time(t, t)

    names = ['direct_beam_Cledge', 'direct_beam_Cledge_withatt1x9umAl']

    energies = np.asarray([2810.0, 2820.0, 2828.0, 2829.0, 2830.0, 2831.0, 2832.0, 2833.0, 2834.0, 2834.5, 2835.0, 2835.5, 2836.0, 2836.5, 2837.0, 2837.5, 2838.0, 2838.5, 2839.0,
    2839.5, 2840.0, 2840.5, 2841.0, 2841.5, 2845.0, 2850.0, 2855.0, 2860.0, 2865.0, 2870.0, 2875.0, 2880.0, 2890.0])


    for name in names:
        if 'withatt1x9umAl' in name:
            yield from bps.mv(att2_9.open_cmd, 1)
            yield from bps.sleep(1)
            yield from bps.mv(att2_9.open_cmd, 1)
            yield from bps.sleep(1)

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
            sample_id(user_name="DM", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")

            yield from bp.count([pil1M], num=1)

    yield from bps.mv(energy, 2850)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 2830)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 2810)
    yield from bps.sleep(2)




def Cl_edge_nexafs_2024_1_surfactant(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    # bottom left first
    names = ['nexafs_test']             
    x_piezo = [      13000]
    x_hexa = [           0]
    y_piezo = [       7000]
    z_piezo = [      -3000]
    
    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(z_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexa)})"



    energies = -10 + np.asarray([2810.0, 2820.0, 2828.0, 2829.0, 2830.0, 2831.0, 2832.0, 2833.0, 2834.0, 2834.5, 2835.0, 2835.5, 2836.0, 2836.5, 2837.0, 2837.5, 2838.0, 2838.5, 2839.0,
    2839.5, 2840.0, 2840.5, 2841.0, 2841.5, 2845.0, 2850.0, 2855.0, 2860.0, 2865.0, 2870.0, 2875.0, 2880.0, 2890.0])

    # energies = np.linspace(2820, 2860, 41)

    waxs_arc = [0]
    ai0_all = 0
    ai_list = [1.6]

    for name, xs, ys, zs, xs_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa):
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)

        yield from bps.mv(piezo.th, ai0_all)
        yield from alignement_gisaxs_doblestack(0.7)

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
                    yield from bps.mv(piezo.x, xs - counter * 30)
                    counter += 1
                    

                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="NS", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)

                dets = [pil900KW, amptek]
                det_exposure_time(3, 3)
                yield from bps.sleep(5)

                name_fmt = "{sample}_amptek_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                sample_id(user_name="NS", sample_name=sample_name)

                yield from bp.count(dets, num=1)
                yield from bps.sleep(5)

                det_exposure_time(t, t)
                dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]

                name_fmt = "{sample}_pos2_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies[::-1]:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs - counter * 30)
                    counter += 1

                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="NS", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)


            yield from bps.mv(piezo.th, ai0)




def Cl_edge_measurments_2024_1_surfactant(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    # names = ['Cl_12_PS', 'Cl_14_PS', 'Cl_16_PS']             
    # x_piezo = [   13000,        570,      -7430]
    # x_hexa = [        0,          0,          0]
    # y_piezo = [    7000,       7000,       7000]
    # z_piezo = [   -3000,      -3000,      -3000]

    # names = [      'PS', 'FS1_PBTTT_C14', 'FS3_PBTTT_C16', 'FS52_PBTTTC14_C', 'FS11_Cl12_PS','FS12_Cl14_PS', 'FS13_Cl16_PS', 'FS61_PBTTTC14_Cl12','FS54_PBTTTC14_Cl14','FS62_PBTTTC14_Cl16','FS63_PBTTTC16_Cl14','FS64_PBTTTC16_Cl16']             
    # x_piezo = [   55000,           55000,             44000,           33000,          22000,         12500,            500,               -10500,              -22200,              -33200,              -45200,              -45000]
    # x_hexa = [       11,               0,                 0,               0,              0,             0,              0,                    0,                   0,                   0,                   0,                 -12]
    # y_piezo = [    7000,            7000,              7000,            7000,           7000,          7000,           7000,                 7000,                7000,                7000,                7000,                7000]
    # z_piezo = [   -3000,           -3000,             -3000,           -3000,          -3000,         -3000,          -3000,                -3000,               -3000,               -3000,               -3000,               -3000]
    
    names = [' P3HT1500',        'PVC1000',      'IL5_C12mimCl',  'IL7_PBTTTC14',      'IL8_PBTTTC16', 'IL21_PBTTTC14_C12mimCl_3_1']             
    x_piezo = [    55000,            54000,               43000,           33000,               18000,                       -49000]
    x_hexa = [        13,                0,                   0,               0,                   0,                           -1]
    y_piezo = [     6600,             6600,                6700,            6800,                6800,                         7500]
    z_piezo = [    -3000,            -3000,               -3000,           -3000,               -3000,                        -3000]
       

    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(z_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexa)})"

    energies = -10 + np.asarray([2810.0, 2820.0, 2828.0, 2829.0, 2830.0, 2831.0, 2832.0, 2833.0, 2834.0, 2834.5, 2835.0, 2835.5, 2836.0, 2836.5, 2837.0, 2837.5, 2838.0, 2838.5, 2839.0,
    2839.5, 2840.0, 2840.5, 2841.0, 2841.5, 2845.0, 2850.0, 2855.0, 2860.0, 2865.0, 2870.0, 2875.0, 2880.0, 2890.0])

    waxs_arc = [0, 20]
    ai0_all = 0
    ai_list = [1.6]

    for name, xs, ys, zs, xs_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa):
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, -2000+xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)

        yield from bps.mv(piezo.th, ai0_all)
        yield from alignement_gisaxs_doblestack(0.7)

        # yield from bps.mv(att2_9.open_cmd, 1)
        # yield from bps.sleep(1)
        # yield from bps.mv(att2_9.open_cmd, 1)
        # yield from bps.sleep(1)

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
                    yield from bps.mv(piezo.x, xs - counter * 30)
                    counter += 1
                    
                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="NS", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)

                dets = [pil900KW, amptek]
                det_exposure_time(3, 3)
                yield from bps.sleep(5)

                name_fmt = "{sample}_amptek_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                sample_id(user_name="NS", sample_name=sample_name)

                yield from bp.count(dets, num=1)
                yield from bps.sleep(5)

                det_exposure_time(t, t)
                dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]

                name_fmt = "{sample}_pos2_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies[::-1]:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs - counter * 30)
                    counter += 1

                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="NS", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)


            yield from bps.mv(piezo.th, ai0)




def S_edge_measurments_2024_1_surfactant(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    names = [      'PS', 'FS1_PBTTT_C14', 'FS3_PBTTT_C16', 'FS52_PBTTTC14_C',  'FS61_PBTTTC14_Cl12','FS54_PBTTTC14_Cl14','FS62_PBTTTC14_Cl16','FS63_PBTTTC16_Cl14','FS64_PBTTTC16_Cl16']             
    x_piezo = [   55000,           55000,             44000,           33000,                -10500,              -22200,              -33200,              -45200,              -45000]
    x_hexa = [       11,               0,                 0,               0,                     0,                   0,                   0,                   0,                 -12]
    y_piezo = [    7000,            7000,              7000,            7000,                  7000,                7000,                7000,                7000,                7000]
    z_piezo = [   -3000,           -3000,             -3000,           -3000,                 -3000,               -3000,               -3000,               -3000,               -3000]

    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(z_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexa)})"

    energies = [2450.0,2455.0,2460.0,2465.0,2470.0,2473.0,2475.0,2475.5,2476.0,2476.5,2477.0,2477.5,2478.0,2478.5,2479.0,2479.5,
    2480.0,2480.5,2481.0,2482.0,2483.0,2484.0,2485.0,2486.0, 2487.0,2488.0,2489.0,2490.0,2492.5,2495.0,2500.0,2510.0,2515.0]


    waxs_arc = [0, 20]
    ai0_all = 0
    ai_list = [1.6]

    for name, xs, ys, zs, xs_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa):
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)

        yield from bps.mv(piezo.th, ai0_all)
        yield from alignement_gisaxs_doblestack(0.7)

        # yield from bps.mv(att2_9.open_cmd, 1)
        # yield from bps.sleep(1)
        # yield from bps.mv(att2_9.open_cmd, 1)
        # yield from bps.sleep(1)

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
                    yield from bps.mv(piezo.x, xs - counter * 30)
                    counter += 1
                    
                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="NS", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)

                dets = [pil900KW, amptek]
                det_exposure_time(3, 3)
                yield from bps.sleep(5)

                name_fmt = "{sample}_amptek_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                sample_id(user_name="NS", sample_name=sample_name)

                yield from bp.count(dets, num=1)
                yield from bps.sleep(5)

                det_exposure_time(t, t)
                dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]

                name_fmt = "{sample}_pos2_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies[::-1]:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs - counter * 30)
                    counter += 1

                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="NS", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)


            yield from bps.mv(piezo.th, ai0)


def S_edge_measurments_2024_1_ILs(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    # names = [' P3HT1500',        'PVC1000',      'IL5_C12mimCl',  'IL7_PBTTTC14',      'IL8_PBTTTC16', 'IL16_PBTTTC14_C14mim_1_1','IL17_PBTTTC14_C14mim_1_3','IL18_PBTTTC14_C16mim_3_1','IL19_PBTTTC14_C16mim_1_1', 'IL20_PBTTTC14_C16mim_1_3','IL21_PBTTTC14_C12mimCl_3_1', 'IL22_PBTTTC14_C12mimOTrf_1_1']             
    # x_piezo = [    55000,            54000,               43000,           33000,               18000,                       9000,                         0,                    -9000,                    -26000,                     -38000,                     -49000,                    -49000]
    # x_hexa = [        13,                0,                   0,               0,                   0,                          0,                         0,                        0,                         0,                          0,                         -1,                       -14]
    # y_piezo = [     6600,             6600,                6700,            6800,                6800,                       6900,                      6800,                     7000,                      7300,                       7300,                       7500,                      7700]
    # z_piezo = [    -3000,            -3000,               -3000,           -3000,               -3000,                      -3000,                     -3000,                    -3000,                     -3000,                      -3000,                      -3000,                     -3000]
       
    # names = ['IL1_C8mim_NEXAFS'] 
    # x_piezo = [    55000] 
    # x_hexa = [        12] 
    # y_piezo = [     6040] 
    # z_piezo = [    -3000]

    # names = [      'IL5_C12mimCl_rerun',  'IL17_PBTTTC14_C14mim_1_3_rerun']             
    # x_piezo = [                   41000,                             -1750]
    # x_hexa = [                        0,                                 0]
    # y_piezo = [                    6700,                              7100]
    # z_piezo = [                   -3000,                             -3000]
       
    names = ['IL24_PBTTTC16_C16mim_1_1', 'IL23_PBTTTC16_C12mim_1_1', 'FS64_PBTTTC16_Cl16']             
    x_piezo = [                   54000,                      41000,                29000]
    x_hexa = [                        0,                          0,                    0]
    y_piezo = [                    6600,                       6700,                 6700]
    z_piezo = [                   -3000,                      -3000,                -3000]

    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(z_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexa)})"

    energies = [2450.0,2455.0,2460.0,2465.0,2470.0,2473.0,2475.0,2475.5,2476.0,2476.5,2477.0,2477.5,2478.0,2478.5,2479.0,2479.5,
    2480.0,2480.5,2481.0,2481.5,2482.0,2482.5,2483.0,2483.5,2484.0,2484.5,2485.0,2485.5,2486.0,2487.0,2488.0,2489.0,2490.0,2491.0,2492.5,2495.0,2500.0,2510.0,2515.0]

    # energies = np.linspace(2470,2510,41)

    waxs_arc = [0, 20]
    ai0_all = 0
    ai_list = [1.6]

    for name, xs, ys, zs, xs_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa):
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)

        yield from bps.mv(piezo.th, ai0_all)
        yield from alignement_gisaxs_doblestack(0.7)

        # yield from bps.mv(att2_9.open_cmd, 1)
        # yield from bps.sleep(1)
        # yield from bps.mv(att2_9.open_cmd, 1)
        # yield from bps.sleep(1)

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
                    yield from bps.mv(piezo.x, xs - counter * 30)
                    counter += 1
                    
                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="NS", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)

                dets = [pil900KW, amptek]
                det_exposure_time(3, 3)
                yield from bps.sleep(5)

                name_fmt = "{sample}_amptek_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                sample_id(user_name="NS", sample_name=sample_name)

                yield from bp.count(dets, num=1)
                yield from bps.sleep(5)

                det_exposure_time(t, t)
                dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]

                name_fmt = "{sample}_pos2_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies[::-1]:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs - counter * 30)
                    counter += 1

                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="NS", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)


            yield from bps.mv(piezo.th, ai0)            




def nexafs_S_edge_measurments_2024_1_ILs(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    names = ['nexafs_IL22_PBTTTC14_C12mimOTrf_1_1']             
    x_piezo = [       -49000]
    x_hexa = [            -14]
    y_piezo = [        7700]
    z_piezo = [       -3000]
       
    # names = ['IL1_C8mim_NEXAFS'] 
    # x_piezo = [    55000] 
    # x_hexa = [        12] 
    # y_piezo = [     6040] 
    # z_piezo = [    -3000]


    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(z_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexa)})"

    # energies = [2450.0,2455.0,2460.0,2465.0,2470.0,2473.0,2475.0,2475.5,2476.0,2476.5,2477.0,2477.5,2478.0,2478.5,2479.0,2479.5,
    # 2480.0,2480.5,2481.0,2481.5,2482.0,2482.5,2483.0,2483.5,2484.0,2484.5,2485.0,2485.5,2486.0,2487.0,2488.0,2489.0,2490.0,2491.0,2492.5,2495.0,2500.0,2510.0,2515.0]

    energies = np.linspace(2470,2510,41)

    waxs_arc = [0]
    ai0_all = 0
    ai_list = [1.6]

    for name, xs, ys, zs, xs_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa):
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)

        yield from bps.mv(piezo.th, ai0_all)
        yield from alignement_gisaxs_doblestack(0.7)

        # yield from bps.mv(att2_9.open_cmd, 1)
        # yield from bps.sleep(1)
        # yield from bps.mv(att2_9.open_cmd, 1)
        # yield from bps.sleep(1)

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
                    yield from bps.mv(piezo.x, xs - counter * 30)
                    counter += 1
                    
                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="NS", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)

                dets = [pil900KW, amptek]
                det_exposure_time(3, 3)
                yield from bps.sleep(5)

                name_fmt = "{sample}_amptek_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                sample_id(user_name="NS", sample_name=sample_name)

                yield from bp.count(dets, num=1)
                yield from bps.sleep(5)

                det_exposure_time(t, t)
                dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]

                name_fmt = "{sample}_pos2_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies[::-1]:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs - counter * 30)
                    counter += 1

                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="NS", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)


            yield from bps.mv(piezo.th, ai0)            





def Cl_edge_measurments_2024_1_ILs(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    # names = [' P3HT1500',        'PVC1000',      'IL5_C12mimCl',  'IL7_PBTTTC14',      'IL8_PBTTTC16', 'IL21_PBTTTC14_C12mimCl_3_1']             
    # x_piezo = [    55000,            54000,               43000,           33000,               18000,                       -49000]
    # x_hexa = [        13,                0,                   0,               0,                   0,                           -1]
    # y_piezo = [     6600,             6600,                6700,            6800,                6800,                         7500]
    # z_piezo = [    -3000,            -3000,               -3000,           -3000,               -3000,                        -3000]

    names = [ 'FS64_PBTTTC16_Cl16']             
    x_piezo = [              29000]
    x_hexa = [                   0]
    y_piezo = [               6700]
    z_piezo = [              -3000]


    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(z_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexa)})"

    energies = -10 + np.asarray([2810.0, 2820.0, 2828.0, 2829.0, 2830.0, 2831.0, 2832.0, 2833.0, 2834.0, 2834.5, 2835.0, 2835.5, 2836.0, 2836.5, 2837.0, 2837.5, 2838.0, 2838.5, 2839.0,
    2839.5, 2840.0, 2840.5, 2841.0, 2841.5, 2845.0, 2850.0, 2855.0, 2860.0, 2865.0, 2870.0, 2875.0, 2880.0, 2890.0])

    waxs_arc = [0, 20]
    ai0_all = 0
    ai_list = [1.6]

    for name, xs, ys, zs, xs_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa):
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)

        yield from bps.mv(piezo.th, ai0_all)
        yield from alignement_gisaxs_doblestack(0.7)

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
                    yield from bps.mv(piezo.x, xs - counter * 30)
                    counter += 1
                    
                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="NS", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)

                dets = [pil900KW, amptek]
                det_exposure_time(3, 3)
                yield from bps.sleep(5)

                name_fmt = "{sample}_amptek_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                sample_id(user_name="NS", sample_name=sample_name)

                yield from bp.count(dets, num=1)
                yield from bps.sleep(5)

                det_exposure_time(t, t)
                dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]

                name_fmt = "{sample}_pos2_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies[::-1]:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs - counter * 30)
                    counter += 1

                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="NS", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)


            yield from bps.mv(piezo.th, ai0)




def Cl_edge_measurments_2024_1_Amalie(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    # bottom left first
    # names = [  'Co_25mmol_FeCl3', 'hT_25mmol_FeCl3', 'mT_25mmol_FeCl3', 'hTe_25mmol_FeCl3', 'mTe_25mmol_FeCl3', 'mB_25mmol_FeCl3', 'hB_25mmol_FeCl3']             
    # x_piezo = [            18000,              5000,             -9000,             -22000,             -34000,            -40000,            -45000]
    # x_hexa = [                 0,                 0,                 0,                  0,                  0,                -9,               -16]
    # y_piezo = [             7000,              7000,              7000,               7200,               7200,              7200,              7200]
    # z_piezo = [            -3000,             -3000,             -3000,              -3000,              -3000,             -3000,             -3000]
    
    names = [       'Co_dedoped', 'hT_400mmol_FeCl3', 'mT_400mmol_FeCl3', 'hTe_1.5mmol_FeCl3',  'mTe_6mmol_FeCl3']             
    x_piezo = [            49000,              35000,              20000,                6000,             -10000]
    x_hexa = [                 0,                  0,                  0,                   0,                  0]
    y_piezo = [            -2000,              -1900,              -1800,               -1800,              -1600]
    z_piezo = [            -3000,              -3000,              -3000,               -3000,              -3000]

    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(z_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexa)})"

    energies = -10 + np.asarray([2810.0, 2820.0, 2828.0, 2829.0, 2830.0, 2831.0, 2832.0, 2833.0, 2834.0, 2834.5, 2835.0, 2835.5, 2836.0, 2836.5, 2837.0, 2837.5, 2838.0, 2838.5, 2839.0,
    2839.5, 2840.0, 2840.5, 2841.0, 2841.5, 2845.0, 2850.0, 2855.0, 2860.0, 2865.0, 2870.0, 2875.0, 2880.0, 2890.0])

    waxs_arc = [0, 20]
    ai0_all = 0
    ai_list = [1.6, 3.2]

    for name, xs, ys, zs, xs_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa):
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)

        yield from bps.mv(piezo.th, ai0_all)
        yield from alignement_gisaxs_doblestack(0.7)

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
                    yield from bps.mv(piezo.x, xs - counter * 30)
                    counter += 1
                    
                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)

                dets = [pil900KW, amptek]
                det_exposure_time(3, 3)
                yield from bps.sleep(5)

                name_fmt = "{sample}_amptek_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                sample_id(user_name="LR", sample_name=sample_name)

                yield from bp.count(dets, num=1)
                yield from bps.sleep(5)

                det_exposure_time(t, t)
                dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]

                name_fmt = "{sample}_pos2_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies[::-1]:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs - counter * 30)
                    counter += 1

                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)


            yield from bps.mv(piezo.th, ai0)




def stingelin_2024_11_day(t=1):
    yield from Cl_edge_measurments_2024_1_ILs(t=t)

    proposal_id("2024_1", "313968_Stingelin_06")
    yield from Cl_edge_measurments_2024_1_Amalie(t=t)



def Cl_edge_measurments_2024_1_Ginger1(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    # names = [  ' P3HT1500', 'PVC1000','Pg32T-TT_FeCl3_sa1','Pg32T-TT_FeCl3_sa2','Pg32T-TT_FeCl3_sa3','Pg32T-TT_FeCl3_sa4','Pg32T-TT_FeCl3_sa5','Pg32T-TT_FeCl3_sa6','Pg32T-TT_FeCl3_sa7']             
    # x_piezo = [      55000,     51000,               38000,               23000,                7000,              -10000,              -24000,              -41000,              -46000]
    # x_hexa = [          10,         0,                   0,                   0,                   0,                   0,                   0,                   0,                 -10]
    # y_piezo = [       6700,      6700,                6800,                6800,                6900,                6900,                7000,                7000,                7100] 
    # z_piezo = [      -3000,     -3000,               -3000,               -3000,               -3000,               -3000,               -3000,               -3000,               -3000]
     

    names = [ ' P3MEEMT_FeCl3_sa12','P3MEEMT_FeCl3_sa13','P3MEEMT_FeCl3_sa14','P3MEEMT_FeCl3_sa15','Pg32T-TT_KCl04_sa1','Pg32T-TT_KCl04_sa2','Pg32T-TT_KCl04_sa3','Pg32T-TT_KCl04_sa4','Pg32T-TT_KCl04_sa5',
               'Pg32T-TT_FeCl3_sa8','Pg32T-TT_KCl04_sa6','Pg32T-TT_KCl04_sa7','Pg32T-TT_KCl04_sa8','Pg32T-TT_KCl04_sa9', 'P3MEEMT_FeCl3_sa9','P3MEEMT_FeCl3_sa10','P3MEEMT_FeCl3_sa11']             
    x_piezo = [               55000,               53000,               36000,               21000,                6000,               -9000,              -24000,              -41000,              -46000,
                              55000,               50000 ,              34000,               17000,                   0,              -24000,              -41000,              -46000]
    x_hexa = [                   11,                   0,                   0,                   0,                   0,                   0,                   0,                   0,                 -10,
                                 10,                   0,                   0,                   0,                   0,                   0,                   0,                 -10]
    y_piezo = [                6700,                6700,                6800,                6800,                6900,                6900,                7000,                7000,                7100,
                              -2100,               -2000,               -1900,               -1700,               -1700,               -1600,               -1400,               -1400] 
    z_piezo = [               -3000,               -3000,               -3000,               -3000,               -3000,               -3000,               -3000,               -3000,               -3000,
                              -3000,               -3000,               -3000,               -3000,               -3000,               -3000,               -3000,               -3000]
     

    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(z_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexa)})"

    #FeCl3
    energies = -10 + np.asarray([2810.0, 2820.0, 2828.0, 2829.0, 2830.0, 2831.0, 2832.0, 2833.0, 2834.0, 2834.5, 2835.0, 2835.5, 2836.0, 2836.5, 2837.0, 2837.5, 2838.0, 2838.5, 2839.0,
    2839.5, 2840.0, 2840.5, 2841.0, 2841.5, 2845.0, 2850.0, 2855.0, 2860.0, 2865.0, 2870.0, 2875.0, 2880.0, 2890.0])

    waxs_arc = [0, 20]
    ai0_all = 0
    ai_list = [1.6]

    for name, xs, ys, zs, xs_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa):
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)

        yield from bps.mv(piezo.th, ai0_all)
        yield from alignement_gisaxs_doblestack(0.7)

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
                    yield from bps.mv(piezo.x, xs - counter * 30)
                    counter += 1
                    
                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)

                dets = [pil900KW, amptek]
                det_exposure_time(3, 3)
                yield from bps.sleep(5)

                name_fmt = "{sample}_amptek_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                sample_id(user_name="LR", sample_name=sample_name)

                yield from bp.count(dets, num=1)
                yield from bps.sleep(5)

                det_exposure_time(t, t)
                dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]

                name_fmt = "{sample}_pos2_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies[::-1]:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs - counter * 30)
                    counter += 1

                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)


                name_fmt = "{sample}_pos3_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs - counter * 30)
                    counter += 1
                    
                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)


                name_fmt = "{sample}_pos4_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies[::-1]:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs - counter * 30)
                    counter += 1

                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)

            yield from bps.mv(piezo.th, ai0)




def Cl_edge_measurments_2024_1_Ginger2(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)


    # names = [ ' P3MEEMT_FeCl3_sa12','P3MEEMT_FeCl3_sa13','P3MEEMT_FeCl3_sa14','P3MEEMT_FeCl3_sa15','Pg32T-TT_KCl04_sa1','Pg32T-TT_KCl04_sa2','Pg32T-TT_KCl04_sa3','Pg32T-TT_KCl04_sa4','Pg32T-TT_KCl04_sa5',
    #            'Pg32T-TT_FeCl3_sa8','Pg32T-TT_KCl04_sa6','Pg32T-TT_KCl04_sa7','Pg32T-TT_KCl04_sa8','Pg32T-TT_KCl04_sa9', 'P3MEEMT_FeCl3_sa9','P3MEEMT_FeCl3_sa10','P3MEEMT_FeCl3_sa11']             
    # x_piezo = [               55000,               53000,               36000,               21000,                6000,               -9000,              -24000,              -41000,              -46000,
    #                           55000,               50000 ,              34000,               17000,                   0,              -24000,              -41000,              -46000]
    # x_hexa = [                   11,                   0,                   0,                   0,                   0,                   0,                   0,                   0,                 -10,
    #                              10,                   0,                   0,                   0,                   0,                   0,                   0,                 -10]
    # y_piezo = [                6700,                6700,                6800,                6800,                6900,                6900,                7000,                7000,                7100,
    #                           -2100,               -2000,               -1900,               -1700,               -1700,               -1600,               -1400,               -1400] 
    # z_piezo = [               -3000,               -3000,               -3000,               -3000,               -3000,               -3000,               -3000,               -3000,               -3000,
    #                           -3000,               -3000,               -3000,               -3000,               -3000,               -3000,               -3000,               -3000]
     
    names = [  'P3MEEMT_FeCl3_sa16','P3MEEMT_FeCl3_sa13_redo']             
    x_piezo = [               46000,                    29000]
    x_hexa = [                    0,                        0]
    y_piezo = [                6700,                     6700] 
    z_piezo = [               -3000,                    -3000]
     

    names = [  'P3MEEMT_FeCl3_sa16_redo']             
    x_piezo = [               41800]
    x_hexa = [                    0]
    y_piezo = [                6700] 
    z_piezo = [               -3000]

    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(z_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexa)})"

    #FeCl3
    energies1 = -10 + np.asarray([2810.0, 2820.0, 2828.0, 2829.0, 2830.0, 2831.0, 2832.0, 2833.0, 2834.0, 2834.5, 2835.0, 2835.5, 2836.0, 2836.5, 2837.0, 2837.5, 2838.0, 2838.5, 2839.0,
    2839.5, 2840.0, 2840.5, 2841.0, 2841.5, 2845.0, 2850.0, 2855.0, 2860.0, 2865.0, 2870.0, 2875.0, 2880.0, 2890.0])

    #KCLO4
    energies2 = np.asarray([2810.0, 2820.0, 2828.0, 2829.0, 2830.0, 2831.0, 2832.0, 2833.0, 2834.0, 2834.5, 2835.0, 2835.5, 2836.0, 2836.5, 2837.0, 2837.5, 2838.0, 2838.5, 2839.0,
    2839.5, 2840.0, 2840.5, 2841.0, 2841.5, 2845.0, 2850.0, 2855.0, 2860.0, 2865.0, 2870.0, 2875.0, 2880.0, 2890.0])

    waxs_arc = [0, 20]
    ai0_all = 0
    ai_list = [1.6]

    for name, xs, ys, zs, xs_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa):
        if 'KCl04' in name:
            energies = energies2
        else:
            energies = energies1

        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)

        yield from bps.mv(piezo.th, ai0_all)
        yield from alignement_gisaxs_doblestack(0.7)

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
                    yield from bps.mv(piezo.x, xs - counter * 30)
                    counter += 1
                    
                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)

                dets = [pil900KW, amptek]
                det_exposure_time(3, 3)
                yield from bps.sleep(5)

                name_fmt = "{sample}_amptek_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                sample_id(user_name="LR", sample_name=sample_name)

                yield from bp.count(dets, num=1)
                yield from bps.sleep(5)

                det_exposure_time(t, t)
                dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]

                name_fmt = "{sample}_pos2_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies[::-1]:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs - counter * 30)
                    counter += 1

                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)


                name_fmt = "{sample}_pos3_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs - counter * 30)
                    counter += 1
                    
                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)


                name_fmt = "{sample}_pos4_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies[::-1]:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs - counter * 30)
                    counter += 1

                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)

            yield from bps.mv(piezo.th, ai0)

def stingelin_2024_11_afternoon(t=1):
    proposal_id("2024_1", "313968_Stingelin_08")
    yield from Cl_edge_measurments_2024_1_Amalie(t=t)

    proposal_id("2024_1", "313968_Stingelin_09")
    yield from Cl_edge_measurments_2024_1_Ginger1(t=t)





def Cl_edge_transmission_measurments_2024_1_Amalie(t=1):
    dets = [pil900KW, pil1M]

    # Att2_9 for this serie of sample
    names = [  'Co_25mmol_FeCl3', 'hT_25mmol_FeCl3', 'mT_25mmol_FeCl3', 'hTe_25mmol_FeCl3', 'mTe_25mmol_FeCl3', 'mB_25mmol_FeCl3']             
    x_piezo = [            44000,             37800,             31500,              25600,              19800,             12700]
    y_piezo = [            -6900,             -6900,             -6900,              -6700,              -6400,             -6900]

    # Remove att2_9 for this serie of sample
    names = [  'hB_25mmol_FeCl3', 'Co_dedoped', 'hT_400mmol_FeCl3', 'mT_400mmol_FeCl3', 'hTe_1.5mmol_FeCl3',  'mTe_6mmol_FeCl3']             
    x_piezo = [             6500,         -100,              -6500,             -12600,              -19000,             -25300]
    y_piezo = [            -6400,        -6200,              -6500,              -6800,               -6400,              -6700]


    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x)}) is different from number of samples ({len(y)})"
    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x)}) is different from number of samples ({len(names)})"

    energies = -10 + np.asarray([2810.0, 2820.0, 2828.0, 2829.0, 2830.0, 2831.0, 2832.0, 2833.0, 2834.0, 2834.5, 2835.0, 2835.5, 2836.0, 2836.5, 2837.0, 2837.5, 2838.0, 2838.5, 2839.0,
    2839.5, 2840.0, 2840.5, 2841.0, 2841.5, 2845.0, 2850.0, 2855.0, 2860.0, 2865.0, 2870.0, 2875.0, 2880.0, 2890.0])

    waxs_arc = [0, 20]

    for name, xs, ys in zip(names, x_piezo, y_piezo):
        yield from bps.mv(piezo.x, xs,
                          piezo.y, ys)

        yss = np.linspace(ys, ys + 500, 33)
        xss = np.array([xs])

        yss, xss = np.meshgrid(yss, xss)
        yss = yss.ravel()
        xss = xss.ravel()

        yss1 = np.linspace(ys, ys + 500, 33)
        xss1 = np.array([xs-400])

        yss1, xss1 = np.meshgrid(yss1, xss1)
        yss1 = yss1.ravel()
        xss1 = xss1.ravel()

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)
            if wa == 0:
                dets = [pil900KW]
            else:
                dets = [pil900KW, pil1M]

            det_exposure_time(t, t)

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
                name_fmt = "{sample}_pos1_sdd1.8m_{energy}eV_wa{wax}_bpm{xbpm}"
                sample_name = name_fmt.format(sample=name, energy="%6.2f" % e, wax=wa, xbpm="%4.3f" % bpm)
                sample_id(user_name="CM", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")

                yield from bp.count(dets, num=1)

            for e, xsss, ysss in zip(energies[::-1], xss1, yss1):
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)

                    yield from bps.mv(piezo.y, ysss)
                    yield from bps.mv(piezo.x, xsss)

                    bpm = xbpm3.sumX.get()

                    name_fmt = "{sample}_pos2_sdd1.8m_{energy}eV_wa{wax}_bpm{xbpm}"
                    sample_name = name_fmt.format(sample=name, energy="%6.2f" % e, wax=wa, xbpm="%4.3f" % bpm)
                    sample_id(user_name="CM", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")

                    yield from bp.count(dets, num=1)




def bpmvspindiode_Cledge_2024_1(t=1):
    dets = [pil1M]
    det_exposure_time(t, t)

    name = 'direct_beam_Cledge_no att'

    energies = -10 + np.asarray([2810.0, 2820.0, 2830.0, 2832.0, 2834.0, 2834.5, 2835.0, 2835.5, 2836.0, 2836.5, 2837.0, 2837.5, 2838.0, 2838.5, 2839.0,
    2839.5, 2840.0, 2840.5, 2841.0, 2841.5, 2845.0, 2850.0, 2855.0, 2860.0, 2865.0, 2870.0, 2875.0, 2880.0, 2890.0])

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

        name_fmt = "{sample}_pos1_{energy}eV_bpm2_{xbpm2}_bpm3_{xbpm3}_pd_{pd}"

        sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, xbpm2="%4.3f"%bpm2, xbpm3="%4.3f"%bpm3, pd="%4.3f"%pdc)
        sample_id(user_name="LR", sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")

        yield from bp.count([pil1M], num=1)


    for e in energies[::-1]:
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

        name_fmt = "{sample}_pos2_{energy}eV_bpm2_{xbpm2}_bpm3_{xbpm3}_pd_{pd}"

        sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, xbpm2="%4.3f"%bpm2, xbpm3="%4.3f"%bpm3, pd="%4.3f"%pdc)
        sample_id(user_name="LR", sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")

        yield from bp.count([pil1M], num=1)







def S_edge_measurments_2024_2_ILs_Linkam(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)
    

    
    names = ['IL11_PBTTTC14:C8mim TFSI_1_3']             
    x_piezo = [                   9350]
    y_piezo = [                    1746]
    z_piezo = [                   -3000]

    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(z_piezo)})"

    energies = [2450.0,2455.0,2460.0,2465.0,2470.0,2473.0,2475.0,2475.5,2476.0,2476.5,2477.0,2477.5,2478.0,2478.5,2479.0,2479.5,
    2480.0,2480.5,2481.0,2481.5,2482.0,2482.5,2483.0,2483.5,2484.0,2484.5,2485.0,2485.5,2486.0,2487.0,2488.0,2489.0,2490.0,2491.0,2492.5,2495.0,2500.0,2510.0,2515.0]

    waxs_arc = [0, 20]
    ai0_all = 0
    ai_list = [3.2, 5.0]
 
    temp = LThermal.temperature()

    for name, xs, ys, zs in zip(names, x_piezo, y_piezo, z_piezo):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)

        yield from bps.mv(piezo.th, ai0_all)
        yield from alignement_gisaxs(0.7)

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

                name_fmt = "{sample}_pos1_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}_temp{temp}"

                #LThermal.temperature()
                for e in energies:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs - counter * 30)
                    counter += 1
                    
                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm, temp="%3.1f"%temp)
                    sample_id(user_name="NS", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)


                # dets = [pil900KW, amptek]
                # det_exposure_time(3, 3)
                # yield from bps.sleep(5)

                # name_fmt = "{sample}_amptek_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                # sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                # sample_id(user_name="NS", sample_name=sample_name)

                # yield from bp.count(dets, num=1)
                # yield from bps.sleep(5)

                det_exposure_time(t, t)
                dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]

                name_fmt = "{sample}_pos2_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies[::-1]:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs - counter * 30)
                    counter += 1

                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="NS", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)


            yield from bps.mv(piezo.th, ai0)            





def S_edge_measurments_2024_2_ILs(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)
#names = ['PBTTTC16_Doped-05V-C12mimTFSI', 'PBTTTC16-Doped-06V-C12mimTFSI', 'PBTTTC16-Doped-10V-C12mimTFSI', 'IL1_NeatC8mimTFSI', 'IL2_NeatC12mimTFSI', 'IL3_NeatC14mimTFSI', 'IL20_PBTTTC14_C14mimTFSI 2_1', 'IL21_PBTTTC14_C14mimTFSI 1_1', 'IL22_PBTTTC14_C14mimTFSI 1_2', 'IL30_NeatPBTTTC16-ILConditions', 'IL31_PBTTTC16_C12mimTFSI 1_1', 'IL32_PBTTTC16_C12mimTFSI 2_1', 'IL33_PBTTTC16_C12mimTFSI 3_1', 'IL34_PBTTTC16_C14mimTFSI 1_1', 'IL35_PBTTTC16_C14mimTFSI 2_1', 'IL36_PBTTTC16_C14mimTFSI 3_1', 'IL37_PBTTTC16_C16mimTFSI 1_1', 'IL38_PBTTTC16_C16mimTFSI 2_1', 'IL39_PBTTTC16_C16mimTFSI 3_1', 'IL7_PBTTTC14_C8mimTFSI 3_1', 'IL8_PBTTTC14_C8mimTFSI 2_1']
#12 samples on bottom 9 on top, Names go Left to Right beginning on Bottom gold substrates for the first 3 -Focus on bleached circular area in center of films for the 1st 2
    names = ['PBTTTC16_Doped-03V-C12mimTFSI',  'PBTTTC16_Doped-04V-C12mimTFSI',             'PBTTTC16-Undoped', 
                        'IL4_NeatC16mimTFSI', 'IL5_Neat-PBTTTC14-ILConditions',   'IL6_PBTTTC14_C8mimTFSI 5_1', 
                'IL7_PBTTTC14_C8mimTFSI 3_1',     'IL8_PBTTTC14_C8mimTFSI 2_1',   'IL9_PBTTTC14_C8mimTFSI 1_1', 
               'IL10_PBTTTC14_C8mimTFSI 1_2',    'IL11_PBTTTC14_C8mimTFSI 1_3', 'IL12_PBTTTC14_C12mimTFSI 5_1', 
              'IL13_PBTTTC14_C12mimTFSI 3_1',   'IL14_PBTTTC14_C12mimTFSI 2_1', 'IL15_PBTTTC14_C12mimTFSI 1_1', 
              'IL16_PBTTTC14_C12mimTFSI 1_2',   'IL17_PBTTTC14_C12mimTFSI 1_3', 'IL18_PBTTTC14_C14mimTFSI 5_1', 
              'IL19_PBTTTC14_C14mimTFSI 3_1',   'IL29_PBTTTC14_C16mimTFSI 1_3', 'IL28_PBTTTC14_C16mimTFSI 1_2', 
              'IL27_PBTTTC14_C16mimTFSI 1_1',   'IL26_PBTTTC14_C16mimTFSI 2_1', 'IL25_PBTTTC14_C16mimTFSI 3_1', 
              'IL24_PBTTTC14_C16mimTFSI 5_1',   'IL23_PBTTTC14_C14mimTFSI 1_3']             
    x_piezo = [                        -51000,                           -47000,                        -34000,
                                       -23000,                           -12000,                         0,
                                       9000,                            20000,                         30000,
                                       42000,                            51000,                         53000,
                                       56000,                           -51000,                        -52000,
                                       -41000,                           -28000,                        -16000,
                                       -6500,                            4000,                         16000,
                                       27000,                            39000,                         49000,
                                       54000,                            56000]
    #hexapod -12 and 12
    x_hexa = [                             -10,                                0,                            0,
                                           0,                                0,                            0,
                                           0,                                0,                            0,
                                           0,                                0,                            7,
                                           14,                                -10,                            0,
                                           0,                                0,                            0,
                                           0,                                0,                            0,
                                           0,                                0,                            0,
                                           7,                                14]
    y_piezo = [                         2000,                             2000,                         2000,
                                        2000,                             2000,                         2000,
                                        2000,                             2000,                         2000,
                                        2000,                             2000,                         2000,
                                        2000,                             -7000,                         -7000,
                                        -7000,                             -7000,                         -7000,
                                       -7000,                            -7000,                       -7000,
                                       -7000,                            -7000,                        -7000,
                                       -7000,                            -7000]
    z_piezo = [                        -3000,                            -3000,                        -3000,
                                       -3000,                            -3000,                        -3000,
                                       -3000,                            -3000,                        -3000,
                                       -3000,                            -3000,                        -3000,
                                       -3000,                            -3000,                        -3000,
                                       -3000,                            -3000,                        -3000,
                                       -3000,                            -3000,                        -3000,
                                       -3000,                            -3000,                        -3000,
                                       -3000,                            -3000]


    #names = ['IL9_PBTTTC14_C8mimTFSI 1_1', 'IL10_PBTTTC14_C8mimTFSI 1_2', 'IL11_PBTTTC14_C8mimTFSI 1_3', 'IL12_PBTTTC14_C12mimTFSI 5_1', 'IL13_PBTTTC14_C12mimTFSI 3_1', 'IL19_PBTTTC14_C14mimTFSI 3_1', 'IL35_PBTTTC16_C16mimTFSI 2_1', 'IL36_PBTTTC16_C16mimTFSI 3_1', 'IL37_PBTTTC16_C16mimTFSI 1_1', 'IL26_PBTTTC14_C16mimTFSI 2_1', 'IL27_PBTTTC14_C16mimTFSI 1_1', 'IL28_PBTTTC14_C16mimTFSI 1_2', 'IL29_PBTTTC14_C16mimTFSI 1_3' ]
    #Samples from left to right, all on bottom row, beginning on sample closest to the chamber's door
    names = ['IL9_PBTTTC14_C8mimTFSI 1_1', 'IL10_PBTTTC14_C8mimTFSI 1_2', 'PBTTTC16-Doped-10V-C12mimTFSI', 
                          'IL1_NeatC8mimTFSI',           'IL2_NeatC12mimTFSI',            'IL3_NeatC14mimTFSI', 
               'IL20_PBTTTC14_C14mimTFSI 2_1', 'IL21_PBTTTC14_C14mimTFSI 1_1',  'IL22_PBTTTC14_C14mimTFSI 1_2', 
             'IL30_NeatPBTTTC16-ILConditions', 'IL31_PBTTTC16_C12mimTFSI 1_1',  'IL32_PBTTTC16_C12mimTFSI 2_1', 
               'IL33_PBTTTC16_C12mimTFSI 3_1', 'IL34_PBTTTC16_C14mimTFSI 1_1',  'IL35_PBTTTC16_C14mimTFSI 2_1', 
               'IL36_PBTTTC16_C14mimTFSI 3_1', 'IL37_PBTTTC16_C16mimTFSI 1_1',  'IL38_PBTTTC16_C16mimTFSI 2_1', 
               'IL39_PBTTTC16_C16mimTFSI 3_1',   'IL7_PBTTTC14_C8mimTFSI 3_1',     'IL8_PBTTTC14_C8mimTFSI 2_1']            
    x_piezo = [                        -47000,                         -45000,                          -30000,
                                       -18000,                          -5000,                            8000,
                                        19000,                          31000,                           44000,
                                        55000,                          56000,
                                       -47000,                         -39000,                          -30000,
                                       -18000,                          -2000,                           14000,
                                        30000,                          48000,                           55000,
                                        56000]
    #hexapod -12 and 12
    x_hexa = [                           -10,                                0,                            0,
                                           0,                                0,                            0,
                                           0,                                0,                            0,
                                           2,                               12,
                                          -5,                                0,                            0,
                                           0,                                0,                            0,
                                           0,                                0,                            2,
                                          12]
    y_piezo = [                         2000,                             2000,                         2000,
                                        2000,                             2000,                         2000,
                                        2000,                             2000,                         2000,
                                        2000,                             2000,
                                       -7000,                            -7000,                        -7000,
                                       -7000,                            -7000,                        -7000,
                                       -7000,                            -7000,                        -7000,
                                       -7000]
    z_piezo = [                        -3000,                            -3000,                        -3000,
                                       -3000,                            -3000,                        -3000,
                                       -3000,                            -3000,                        -3000,
                                       -3000,                            -3000,
                                       -3000,                            -3000,                        -3000,
                                       -3000,                            -3000,                        -3000,
                                       -3000,                            -3000,                        -3000,
                                       -3000]



    #names = 
    #Samples from left to right, all on bottom row, beginning on sample closest to the chamber's door
    names = [  'IL9_PBTTTC14_C8mimTFSI 1_1',  'IL10_PBTTTC14_C8mimTFSI 1_2',  'IL11_PBTTTC14_C8mimTFSI 1_3', 
             'IL12_PBTTTC14_C12mimTFSI 5_1', 'IL13_PBTTTC14_C12mimTFSI 3_1', 'IL19_PBTTTC14_C14mimTFSI 3_1', 
             'IL35_PBTTTC16_C16mimTFSI 2_1', 'IL36_PBTTTC16_C16mimTFSI 3_1', 'IL37_PBTTTC16_C16mimTFSI 1_1', 
             'IL26_PBTTTC14_C16mimTFSI 2_1', 'IL27_PBTTTC14_C16mimTFSI 1_1', 'IL28_PBTTTC14_C16mimTFSI 1_2', 
             'IL29_PBTTTC14_C16mimTFSI 1_3' ]            
    x_piezo = [                        -50000,                         -40000,                          -27000,
                                       -10000,                              0,                            7000,
                                        14000,                          22000,                           31000,
                                        42000,                          51000,                           55000,
                                        57000]
    #hexapod -12 and 12
    x_hexa = [                            -4,                                0,                            0,
                                           0,                                0,                            0,
                                           0,                                0,                            0,
                                           0,                                0,                            7,
                                          13]
    y_piezo = [                         2000,                             2000,                         2000,
                                        2000,                             2000,                         2000,
                                        2000,                             2000,                         2000,
                                        2000,                             2000,                         2000,
                                        2000]
    z_piezo = [                        -3000,                            -3000,                        -3000,
                                       -3000,                            -3000,                        -3000,
                                       -3000,                            -3000,                        -3000,
                                       -3000,                            -3000,                        -3000,
                                       -3000]

    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(z_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexa)})"

    energies = [2450.0,2455.0,2460.0,2465.0,2470.0,2473.0,2475.0,2475.5,2476.0,2476.5,2477.0,2477.5,2478.0,2478.5,2479.0,2479.5,
    2480.0,2480.5,2481.0,2481.5,2482.0,2482.5,2483.0,2483.5,2484.0,2484.5,2485.0,2485.5,2486.0,2487.0,2488.0,2489.0,2490.0,2491.0,2492.5,2495.0,2500.0,2510.0,2515.0]


    #waxs_arc = [0, 20]
    waxs_arc = [0]
    ai0_all = 0
    ai_list = [3.2, 5.0]

    for name, xs, ys, zs, xs_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa):
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)

        yield from bps.mv(piezo.th, ai0_all)
        yield from alignement_gisaxs_doblestack(0.7)

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
                    yield from bps.mv(piezo.x, xs - counter * 30)
                    counter += 1
                    
                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="NS", sample_name=sample_name)
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
                    yield from bps.mv(piezo.x, xs - counter * 30)
                    counter += 1

                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="NS", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)


            yield from bps.mv(piezo.th, ai0)            


def bpmvspindiode_Sedge_2024_2_Stingelin(t=1):
    dets = [pil1M]
    det_exposure_time(t, t)

    name = 'Stingelin_direct_beam_Sedge_scannormal'


    energies = [2450.0,2455.0,2460.0,2465.0,2470.0,2473.0,2475.0,2475.5,2476.0,2476.5,2477.0,2477.5,2478.0,2478.5,2479.0,2479.5,
    2480.0,2480.5,2481.0,2481.5,2482.0,2482.5,2483.0,2483.5,2484.0,2484.5,2485.0,2485.5,2486.0,2487.0,2488.0,2489.0,2490.0,2491.0,2492.5,2495.0,2500.0,2510.0,2515.0]


    
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

        name_fmt = "{sample}_pos1_{energy}eV_bpm2_{xbpm2}_bpm3_{xbpm3}_pd_{pd}"

        sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, xbpm2="%4.3f"%bpm2, xbpm3="%4.3f"%bpm3, pd="%4.3f"%pdc)
        sample_id(user_name="LR", sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")

        yield from bp.count([pil1M], num=1)


    for e in energies[::-1]:
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

        name_fmt = "{sample}_pos2_{energy}eV_bpm2_{xbpm2}_bpm3_{xbpm3}_pd_{pd}"

        sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, xbpm2="%4.3f"%bpm2, xbpm3="%4.3f"%bpm3, pd="%4.3f"%pdc)
        sample_id(user_name="LR", sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")

        yield from bp.count([pil1M], num=1)



##2024-3

# def GIWAXS_2024_2(t=1):
#     dets = [pil1M, pil900KW]
#     det_exposure_time(t, t)


#     # top of bar approx y=-3500, ai0=-.7, z=5200
#     # bottom of bar approx y=5300, ai0=.3, z=1600
#     names = [   'PS2',  'PS2',  'PS3', 'PS3',  'PS4', 'PS4',    'PS5',  'PS5',      'PS6',      'PS6',      'PS7',      'PS7',
#                 'PS8',  'PS8',  'PS9', 'PS9',  'PS10','PS10',   'PS11',  'PS11',   'PS12',      'PS12',     'PS13',     'PS13',
#                 'PS14',     'PS14',     'PS16',     'PS16',     'PS17',     'PS17',     'PS18',     'PS18',     'PS19',     'PS19',
#                 'PS20',     'PS20',     'PS21',     'PS21',     'PS22',     'PS22',     'PS23',     'PS23',     'PS24',     'PS24',
#                 'PS25',     'PS25',     'PS26',     'PS26',     'PS1',      'PS1',      'PS15',     'PS15']             
#     poss =   [      1,      2,      1,     2,      1,    2,         1,      2,      1,          2,          1,          2,
#                     1,      2,      1,     2,       1,      2,      1,      2,          1,           2,         1,          2,
#                     1,          2,          1,          2,          1,          2,          1,          2,          1,          2,
#                     1,           2,         1,           2,         1,          2,          1,          2,          1,          2,
#                     1,          2,          1,          2,          1,          2,          1,          2]
#     x_piezo = [-57000, -56000,  -48000,-49000,-39000, -38000,   -28000, -27000,     -18000,     -17000,     -8000,      -7000,
#                 3000,    4000,  12000, 13000,   20000,  21000,  29000,  30000,       37000,     38000,      45000,      46000, 
#                 49000,      49000,     -57000,      -56000,     -48000,     -47000,     -36000,       -35000,    -26000,     -25000,
#                -17000,      -16000,     -8000,      -7000,          0,        1000,      9000,      10000,       16000,     17000, 
#                 25000,      26000,      34000,      35000,       44000,     45000,     49000,       49000     ]
#     x_hexa = [     -1,     -1,      -1,    -1,     -1,   -1,        -1,     -1,        -1,      -1,            -1,      -1,
#                    -1,     -1,      -1,    -1,      -1,  -1,        -1,     -1,         -1,     -1,            -1,         -1, 
#                    3,           4,          0,          0,          0,          0,          0,             0,       0,          0,
#                    0,           0,          0,           0,         0,          0,          0,            0,        0,          0,
#                    0,           0,          0,          0,          0,          0,          6,      7]
#     y_piezo = [  5300,    5300,   5300,  5300, 5300,  5300,       5300, 5300,       5300,       5300,         5300,     5300,
#                  5300,    5300,   5300,  5300, 5300,  5300,       5300,    5300,     5300,        5300,       5300,     5300,
#                  5300,      5300,       -3500,        -3500,       -3500,     -3500,     -3500,       -3500,      -3500,    -3500,
#                  -3500,     -3500,      -3500,        -3500,        -3500,    -3500,      -3500,      -3500,      -3500,     -3500,
#                  -3500,     -3500,      -3500,        -3500,        -3500,    -3500,        -3500,      -3500]
#     z_piezo = [  1600,    1600,   1600,  1600,  1600, 1600,     900,      900,      900,        900,            900,      900,
#                  900,      900,    900,   900,  900,   900,        900,     900,      900,        900,          900,      900,
#                  900,          900,      5200,        5200,         5200,     5200,      5200,          5200,   5200,       5200,
#                  5200,      5200,        5200,        5200,         5200,     5200,     5200,           5200,   5200,       5200,
#                  5200,      5200,        5200,        5200,         5200,     5200,       5200,         5200]

#     assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
#     assert len(x_piezo) == len(poss), f"Number of X coordinates ({len(x_piezo)}) is different from number of positions ({len(poss)})"
#     assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of y positions ({len(y_piezo)})"
#     assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of z positions ({len(z_piezo)})"
#     assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of x heaxpos positions ({len(x_hexa)})"

#     waxs_arc = [20, 0]
#     ai0_list = []
#     ai_list = [0.08, 0.1, 0.12, 0.15, 0.2]


#     yield from bps.mv(waxs, 20)

#     for name, xs, ys, zs, xs_hexa, pos in zip(names, x_piezo, y_piezo, z_piezo, x_hexa, poss):
#         yield from bps.mv(stage.x, xs_hexa)
#         yield from bps.mv(piezo.x, xs)
#         yield from bps.mv(piezo.y, ys)
#         yield from bps.mv(piezo.z, zs)


#         if ys <0 : 
#             ai0_all = -0.7
#         if ys > 0:
#             ai0_all = 0.3
#         yield from bps.mv(piezo.th, ai0_all)
#         yield from alignement_gisaxs_doblestack(0.15)
        
        

#         ai0 = piezo.th.position
#         ai0_list.append(ai0)

#         dets = [pil1M, pil900KW]

#         det_exposure_time(t, t)

#         for k, ais in enumerate(ai_list):
#             yield from bps.mv(piezo.th, ai0 + ais)

#             name_fmt = "{sample}_pos{pos}_ai{ai}_wa{wax}_bpm{xbpm}"
        
#             bpm = xbpm2.sumX.get()
#             sample_name = name_fmt.format(sample=name, ai="%3.2f"%ais, wax=20, xbpm="%4.3f"%bpm, pos="%d"%pos)
#             sample_id(user_name="NS", sample_name=sample_name)
#             print(f"\n\t=== Sample: {sample_name} ===\n")
#             yield from bp.count(dets, num=1)



#     print(f'list of angles: {ai0_list}')
#     dets = [pil900KW]
#     yield from bps.mv(waxs, 0)
#     for name, xs, ys, zs, xs_hexa, pos, ai0 in zip(names, x_piezo, y_piezo, z_piezo, x_hexa, poss, ai0_list):
#         yield from bps.mv(stage.x, xs_hexa)
#         yield from bps.mv(piezo.x, xs)
#         yield from bps.mv(piezo.y, ys)
#         yield from bps.mv(piezo.z, zs)
#         det_exposure_time(t, t)

#         for k, ais in enumerate(ai_list):
#             yield from bps.mv(piezo.th, ai0 + ais)

#             name_fmt = "{sample}_pos{pos}_ai{ai}_wa{wax}_bpm{xbpm}"
        
#             bpm = xbpm2.sumX.get()
#             sample_name = name_fmt.format(sample=name, ai="%3.2f"%ais, wax=0, xbpm="%4.3f"%bpm, pos="%d"%pos)
#             sample_id(user_name="NS", sample_name=sample_name)
#             print(f"\n\t=== Sample: {sample_name} ===\n")
#             yield from bp.count(dets, num=1)


def GIWAXS_2024_2(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)


    # top of bar approx y=-3500, ai0=-.7, z=5200
    # bottom of bar approx y=5300, ai0=.3, z=1600
    names = [  'PS7',      'PS7',
                'PS8',  'PS8',  'PS9', 'PS9',  'PS10','PS10',   'PS11',  'PS11',   'PS12',      'PS12',     'PS13',     'PS13',
                'PS14',     'PS14',     'PS16',     'PS16',     'PS17',     'PS17',     'PS18',     'PS18',     'PS19',     'PS19',
                'PS20',     'PS20',     'PS21',     'PS21',     'PS22',     'PS22',     'PS23',     'PS23',     'PS24',     'PS24',
                'PS25',     'PS25',     'PS26',     'PS26',     'PS1',      'PS1',      'PS15',     'PS15']             
    poss =   [        1,          2,
                    1,      2,      1,     2,       1,      2,      1,      2,          1,           2,         1,          2,
                    1,          2,          1,          2,          1,          2,          1,          2,          1,          2,
                    1,           2,         1,           2,         1,          2,          1,          2,          1,          2,
                    1,          2,          1,          2,          1,          2,          1,          2]
    x_piezo = [    -8000,      -7000,
                3000,    4000,  12000, 13000,   20000,  21000,  29000,  30000,       37000,     38000,      45000,      46000, 
                49000,      49000,     -57000,      -56000,     -48000,     -47000,     -36000,       -35000,    -26000,     -25000,
               -17000,      -16000,     -8000,      -7000,          0,        1000,      9000,      10000,       16000,     17000, 
                25000,      26000,      34000,      35000,       44000,     45000,     49000,       49000     ]
    x_hexa = [  -1,      -1,
                   -1,     -1,      -1,    -1,      -1,  -1,        -1,     -1,         -1,     -1,            -1,         -1, 
                   3,           4,          0,          0,          0,          0,          0,             0,       0,          0,
                   0,           0,          0,           0,         0,          0,          0,            0,        0,          0,
                   0,           0,          0,          0,          0,          0,          6,      7]
    y_piezo = [    5300,     5300,
                 5300,    5300,   5300,  5300, 5300,  5300,       5300,    5300,     5300,        5300,       5300,     5300,
                 5300,      5300,       -3500,        -3500,       -3500,     -3500,     -3500,       -3500,      -3500,    -3500,
                 -3500,     -3500,      -3500,        -3500,        -3500,    -3500,      -3500,      -3500,      -3500,     -3500,
                 -3500,     -3500,      -3500,        -3500,        -3500,    -3500,        -3500,      -3500]
    z_piezo = [    900,      900,
                 900,      900,    900,   900,  900,   900,        900,     900,      900,        900,          900,      900,
                 900,          900,      5200,        5200,         5200,     5200,      5200,          5200,   5200,       5200,
                 5200,      5200,        5200,        5200,         5200,     5200,     5200,           5200,   5200,       5200,
                 5200,      5200,        5200,        5200,         5200,     5200,       5200,         5200]

    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(poss), f"Number of X coordinates ({len(x_piezo)}) is different from number of positions ({len(poss)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of y positions ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of z positions ({len(z_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of x heaxpos positions ({len(x_hexa)})"

    waxs_arc = [20, 0]
    ai0_list = []
    y0_list = []
    ai_list = [0.08, 0.1, 0.12, 0.15, 0.2]


    yield from bps.mv(waxs, 20)

    for name, xs, ys, zs, xs_hexa, pos in zip(names, x_piezo, y_piezo, z_piezo, x_hexa, poss):
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)


        if ys <0 : 
            ai0_all = -0.7
        if ys > 0:
            ai0_all = 0.3
        yield from bps.mv(piezo.th, ai0_all)
        yield from alignement_gisaxs_doblestack(0.15)
        
        

        ai0 = piezo.th.position
        ypos = piezo.y.position
        ai0_list.append(ai0)
        y0_list.append(ypos)
        print(f'{sample_name} position is th={ai0},y={ypos}')
        dets = [pil1M, pil900KW]

        det_exposure_time(t, t)

        for k, ais in enumerate(ai_list):
            yield from bps.mv(piezo.th, ai0 + ais)

            name_fmt = "{sample}_pos{pos}_ai{ai}_wa{wax}_bpm{xbpm}"
        
            bpm = xbpm2.sumX.get()
            sample_name = name_fmt.format(sample=name, ai="%3.2f"%ais, wax=20, xbpm="%4.3f"%bpm, pos="%d"%pos)
            sample_id(user_name="NS", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)



    print(f'list of angles: {ai0_list}')
    dets = [pil900KW]
    yield from bps.mv(waxs, 0)
    for name, xs, ys, zs, xs_hexa, pos, ai0 in zip(names, x_piezo, y0_list, z_piezo, x_hexa, poss, ai0_list):
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)
        det_exposure_time(t, t)

        for k, ais in enumerate(ai_list):
            yield from bps.mv(piezo.th, ai0 + ais)

            name_fmt = "{sample}_pos{pos}_ai{ai}_wa{wax}_bpm{xbpm}"
        
            bpm = xbpm2.sumX.get()
            sample_name = name_fmt.format(sample=name, ai="%3.2f"%ais, wax=0, xbpm="%4.3f"%bpm, pos="%d"%pos)
            sample_id(user_name="NS", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)


def GIWAXS_2024_3(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)


    # top of bar approx y=-3500, ai0=-.7, z=5200
    # bottom of bar approx y=5300, ai0=.3, z=1600
    names = [    'PS7',        'PS8',      'PS9',     'PS10',     'PS11',     'PS12',     'PS13',     'PS14',     'PS16',     'PS17',    
                'PS18',       'PS19',     'PS20',     'PS21',     'PS22',     'PS23',     'PS24',     'PS25',     'PS26',      'PS1',
                'PS15']             
    x_piezo =[    -8000,      3000,       12000,      20000,      29000,      37000,      45000,      49000,     -57000,     -48000,     
                 -36000,    -26000,      -17000,       -8000,          0,       9000,      16000,      25000,      34000,      44000,      
                 49000 ]
    x_hexa = [      -1,           -1,         -1,        -1,          -1,         -1,         -1,         3 ,         0 ,         0,
                    0,           0,         0,        0,           0,          0,          0,          0,          0,             0,
                     0]
    y_piezo = [   5300,         5300,       5300,       5300,      5300,        5300,       5300,       5300,       -3500,      -3500, 
                 -3500,         -3500,     -3500,      -3500,     -3500,       -3500,      -3500,      -3500,        -3500,     -3500,
                 -3500]
    z_piezo = [    900,          900,        900,        900,       900,         900,        900,        900,        5200,       5200,
                 5200,          5200,       5200,       5200,      5200,        5200,       5200,       5200,        5200,       5200,
                 5200]

    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of y positions ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of z positions ({len(z_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of x heaxpos positions ({len(x_hexa)})"

    waxs_arc = [20, 0]
    ai0_list = []
    y0_list = []
    ai_list = [0.08, 0.1, 0.12, 0.15, 0.2]


    yield from bps.mv(waxs, 20)

    for name, xs, ys, zs, xs_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa):
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)


        if ys <0 : 
            ai0_all = -0.7
        if ys > 0:
            ai0_all = 0.3
        yield from bps.mv(piezo.th, ai0_all)
        yield from alignement_gisaxs_doblestack(0.15)
        
        

        ai0 = piezo.th.position
        ypos = piezo.y.position
        ai0_list.append(ai0)
        y0_list.append(ypos)
        print(f'{name} position is th={ai0},y={ypos}')

        dets = [pil1M, pil900KW]

        det_exposure_time(t, t)
        poss = [1,2]
        for pos in poss:
            if pos == 2:
                yield from bps.mvr(stage.x, 1)
               
            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                name_fmt = "{sample}_pos{pos}_ai{ai}_wa{wax}_bpm{xbpm}"
            
                bpm = xbpm2.sumX.get()
                sample_name = name_fmt.format(sample=name, ai="%3.2f"%ais, wax=20, xbpm="%4.3f"%bpm, pos="%d"%pos)
                sample_id(user_name="NS", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

def GIWAXS_2024_4(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)


    # top of bar approx y=-3500, ai0=-.7, z=5200
    # bottom of bar approx y=5300, ai0=.3, z=1600
    names = [       'PS22',     'PS23',     'PS24',     'PS25',     'PS26',      'PS1',
                'PS15']             
    x_piezo =[                0,       9000,      16000,      25000,      34000,      44000,      
                 49000 ]
    x_hexa = [                0,          0,          0,          0,          0,             0,
                     0]
    y_piezo = [          -3500,       -3500,      -3500,      -3500,        -3500,     -3500,
                 -3500]
    z_piezo = [           5200,        5200,       5200,       5200,        5200,       5200,
                 5200]

    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of y positions ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of z positions ({len(z_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of x heaxpos positions ({len(x_hexa)})"

    waxs_arc = [20, 0]
    ai0_list = []
    y0_list = []
    ai_list = [0.08, 0.1, 0.12, 0.15, 0.2]


    yield from bps.mv(waxs, 20)

    for name, xs, ys, zs, xs_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa):
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)


        if ys <0 : 
            ai0_all = -0.7
        if ys > 0:
            ai0_all = 0.3
        yield from bps.mv(piezo.th, ai0_all)
        yield from alignement_gisaxs_doblestack(0.15)
        
        

        ai0 = piezo.th.position
        ypos = piezo.y.position
        ai0_list.append(ai0)
        y0_list.append(ypos)
        print(f'{name} position is th={ai0},y={ypos}')

        dets = [pil1M, pil900KW]

        det_exposure_time(t, t)
        poss = [1,2]
        for pos in poss:
            if pos == 2:
                yield from bps.mvr(stage.x, 1)
               
            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                name_fmt = "{sample}_pos{pos}_ai{ai}_wa{wax}_bpm{xbpm}"
            
                bpm = xbpm2.sumX.get()
                sample_name = name_fmt.format(sample=name, ai="%3.2f"%ais, wax=20, xbpm="%4.3f"%bpm, pos="%d"%pos)
                sample_id(user_name="NS", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)



    print(f'list of angles: {ai0_list}')
    dets = [pil900KW]
    yield from bps.mv(waxs, 0)
    for name, xs, ys, zs, xs_hexa, ai0 in zip(names, x_piezo, y0_list, z_piezo, x_hexa, ai0_list):
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)
        det_exposure_time(t, t)

        for pos in poss:
            if pos == 2:
                yield from bps.mvr(stage.x, 1)
            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                name_fmt = "{sample}_pos{pos}_ai{ai}_wa{wax}_bpm{xbpm}"
            
                bpm = xbpm2.sumX.get()
                sample_name = name_fmt.format(sample=name, ai="%3.2f"%ais, wax=0, xbpm="%4.3f"%bpm, pos="%d"%pos)
                sample_id(user_name="NS", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

def GISWAXS_2024_5(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)


    # top of bar approx y=-3500, ai0=-.7, z=5200
    # bottom of bar approx y=5300, ai0=.3, z=1600
    names = [   'PS15','PS6', 'PS21']             
    x_piezo =[  49000,-18000,  -8000]
    x_hexa = [     6, -1,      0  ]
    y_piezo = [   -4000,  4300,   -4000]
    z_piezo = [  5200, 900,    5200]

    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of y positions ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of z positions ({len(z_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of x heaxpos positions ({len(x_hexa)})"

    waxs_arc = [20, 0]
    ai0_list = []
    y0_list = []
    ai_list = [0.08, 0.1, 0.12, 0.15, 0.2]


    yield from bps.mv(waxs, 20)

    for name, xs, ys, zs, xs_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa):
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)


        if ys <0 : 
            ai0_all = -0.7
        if ys > 0:
            ai0_all = 0.3
        yield from bps.mv(piezo.th, ai0_all)
        yield from alignement_gisaxs_doblestack(0.15)
        
        

        ai0 = piezo.th.position
        ypos = piezo.y.position
        ai0_list.append(ai0)
        y0_list.append(ypos)
        print(f'{name} position is th={ai0},y={ypos}')
        print(f'current aoi list is {ai0_list}')
        print(f'current y0 list is {y0_list}')

        dets = [pil1M, pil900KW]

        det_exposure_time(t, t)
        poss = [1,2]
        for pos in poss:
            if pos == 2:
                yield from bps.mvr(stage.x, 1)
               
            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                name_fmt = "{sample}_pos{pos}_ai{ai}_wa{wax}_bpm{xbpm}"
            
                bpm = xbpm2.sumX.get()
                sample_name = name_fmt.format(sample=name, ai="%3.2f"%ais, wax=20, xbpm="%4.3f"%bpm, pos="%d"%pos)
                sample_id(user_name="NS", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

    print(f'list of angles: {ai0_list}')
    dets = [pil900KW]
    yield from bps.mv(waxs, 0)
    for name, xs, ys, zs, xs_hexa, ai0 in zip(names, x_piezo, y0_list, z_piezo, x_hexa, ai0_list):
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)
        det_exposure_time(t, t)

        for pos in poss:
            if pos == 2:
                yield from bps.mvr(stage.x, 1)
            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                name_fmt = "{sample}_pos{pos}_ai{ai}_wa{wax}_bpm{xbpm}"
            
                bpm = xbpm2.sumX.get()
                sample_name = name_fmt.format(sample=name, ai="%3.2f"%ais, wax=0, xbpm="%4.3f"%bpm, pos="%d"%pos)
                sample_id(user_name="NS", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

def GISWAXS_2024_6(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)


    # top of bar approx y=-3500, ai0=-.7, z=5200
    # bottom of bar approx y=5300, ai0=.3, z=1600
    names = [   'PS21']             
    x_piezo =[   -8000]
    x_hexa = [     0  ]
    y_piezo = [     -4000]
    z_piezo = [     5200]

    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of y positions ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of z positions ({len(z_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of x heaxpos positions ({len(x_hexa)})"

    waxs_arc = [20, 0]
    ai0_list = []
    y0_list = []
    ai_list = [0.08, 0.1, 0.12, 0.15, 0.2]


    yield from bps.mv(waxs, 20)

    for name, xs, ys, zs, xs_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa):
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)


        if ys <0 : 
            ai0_all = -0.7
        if ys > 0:
            ai0_all = 0.3
        yield from bps.mv(piezo.th, ai0_all)
        yield from alignement_gisaxs_doblestack(0.15)
        
        

        ai0 = piezo.th.position
        ypos = piezo.y.position
        ai0_list.append(ai0)
        y0_list.append(ypos)
        print(f'{name} position is th={ai0},y={ypos}')
        print(f'current aoi list is {ai0_list}')
        print(f'current y0 list is {y0_list}')

        dets = [pil1M, pil900KW]

        det_exposure_time(t, t)
        poss = [1,2]
        for pos in poss:
            if pos == 2:
                yield from bps.mvr(stage.x, 1)
               
            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                name_fmt = "{sample}_pos{pos}_ai{ai}_wa{wax}_bpm{xbpm}"
            
                bpm = xbpm2.sumX.get()
                sample_name = name_fmt.format(sample=name, ai="%3.2f"%ais, wax=20, xbpm="%4.3f"%bpm, pos="%d"%pos)
                sample_id(user_name="NS", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

    print(f'list of angles: {ai0_list}')
    dets = [pil900KW]
    yield from bps.mv(waxs, 10)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 5)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 2)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 0)

    """
    while waxs.arc.position > 0:
        yield from bps.mvr(waxs, -1)
        yield from bps.sleep(1)
    yield from bps.mv(waxs, 0)
    """


    for name, xs, ys, zs, xs_hexa, ai0 in zip(names, x_piezo, y0_list, z_piezo, x_hexa, ai0_list):
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)
        det_exposure_time(t, t)
        poss = [1,2]
        for pos in poss:
            if pos == 2:
                yield from bps.mvr(stage.x, 1)
            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                name_fmt = "{sample}_pos{pos}_ai{ai}_wa{wax}_bpm{xbpm}"
            
                bpm = xbpm2.sumX.get()
                sample_name = name_fmt.format(sample=name, ai="%3.2f"%ais, wax=0, xbpm="%4.3f"%bpm, pos="%d"%pos)
                sample_id(user_name="NS", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)                

def take_manual_waxs(name='test', ai_list = [0.08, 0.1, 0.12, 0.15, 0.2],t=1):
    """
    In case waxs arc breaks while moving, take data after sample was aligned
    """
    yield from bps.mv(waxs, 0)
    
    dets = [pil900KW]
    ai0 = piezo.th.position
    det_exposure_time(t, t)
    poss = [1,2]
    for pos in poss:
        if pos == 2:
            yield from bps.mvr(stage.x, 1)
        for k, ais in enumerate(ai_list):
            yield from bps.mv(piezo.th, ai0 + ais)

            name_fmt = "{sample}_pos{pos}_ai{ai}_wa{wax}_bpm{xbpm}"
        
            bpm = xbpm2.sumX.get()
            sample_name = name_fmt.format(sample=name, ai="%3.2f"%ais, wax=0, xbpm="%4.3f"%bpm, pos="%d"%pos)
            sample_id(user_name="NS", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)
    bps.mvr(stage.x, -1)


def take_manual_saxs(name='test', ai_list = [0.08, 0.1, 0.12, 0.15, 0.2],t=1):
    """
    take SAXS data after sample was aligned
    """
    yield from bps.mv(waxs, 20)
    ai0 = piezo.th.position
    print(f"alignment angle was {ai0}")
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)
    poss = [1,2]
    for pos in poss:
        if pos == 2:
            yield from bps.mvr(stage.x, 1)
            
        for k, ais in enumerate(ai_list):
            yield from bps.mv(piezo.th, ai0 + ais)

            name_fmt = "{sample}_pos{pos}_ai{ai}_wa{wax}_bpm{xbpm}"
        
            bpm = xbpm2.sumX.get()
            sample_name = name_fmt.format(sample=name, ai="%3.2f"%ais, wax=20, xbpm="%4.3f"%bpm, pos="%d"%pos)
            sample_id(user_name="NS", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)
        ### move back to pos 1
        yield from bps.mvr(stage.x, -1)

def GIWAXS_2024_all(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)


    # top of bar approx y=-3500, ai0=-.7, z=5200
    # bottom of bar approx y=5300, ai0=.3, z=1600
    names = [    'PS2',        'PS3',      'PS4',     'PS5',
                'PS7',        'PS8',      'PS9',     'PS10',     'PS11',     'PS12',     'PS13',     'PS14',     'PS16',     'PS17',    
                'PS18',       'PS19',     'PS20',                'PS22',     'PS23',     'PS24',     'PS25',     'PS26',      'PS1',
                'PS15']             
    x_piezo =[    -57000,       -48000,     -39000,   -28000, 
                  -8000,      3000,       12000,      20000,      29000,      37000,      45000,      49000,     -57000,     -48000,     
                 -36000,    -26000,      -17000,                      0,       9000,      16000,      25000,      34000,      44000,      
                 49000 ]
    x_hexa = [      -1,           -1,         -1,        -1,     
                    -1,           -1,         -1,        -1,          -1,         -1,         -1,         3 ,         0 ,         0,
                    0,           0,         0,                        0,          0,          0,          0,          0,             0,
                     0]
    y_piezo = [   5300,         5300,       5300,       5300,   
                  5300,         5300,       5300,       5300,      5300,        5300,       5300,       5300,       -3500,      -3500, 
                 -3500,         -3500,     -3500,                  -3500,       -3500,      -3500,      -3500,        -3500,     -3500,
                 -3500]
    z_piezo = [   1600,         1600,      1600,        900,     
                  900,          900,        900,        900,       900,         900,        900,        900,        5200,       5200,
                 5200,          5200,       5200,                 5200,        5200,       5200,       5200,        5200,       5200,
                 5200]

    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of y positions ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of z positions ({len(z_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of x heaxpos positions ({len(x_hexa)})"

    waxs_arc = [20, 0]
    ai0_list = [-0.1027,0.2656,0.8518,-0.99,.2652,2.062,1.457,-0.723,0.956,-0.335,0.0172,0.5438,-1.086,-0.808,-1.508,-0.795,-2.1257,-1.0755,-0.974,
                -0.1227,-0.5788,-0.6207,0.498,0.1339]
    y0_list = [5229.6,5188.5,5249.24,3510.2,5165.8,5100.5,5087.3,5183.5,5162.4,5172.1,5187.7,4969,-3694.1,-3691.7,-3807.8,-3745.1,-3923.3,-3796.7,-3791.6,
               -3649.3,-3753.1,-3751.3,-3742.9,-3854.98]
    ai_list = [0.08, 0.1, 0.12, 0.15, 0.2]


    # yield from bps.mv(waxs, 20)

    # for name, xs, ys, zs, xs_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa):
    #     yield from bps.mv(stage.x, xs_hexa)
    #     yield from bps.mv(piezo.x, xs)
    #     yield from bps.mv(piezo.y, ys)
    #     yield from bps.mv(piezo.z, zs)


    #     if ys <0 : 
    #         ai0_all = -0.7
    #     if ys > 0:
    #         ai0_all = 0.3
    #     yield from bps.mv(piezo.th, ai0_all)
    #     yield from alignement_gisaxs_doblestack(0.15)
        
        

    #     ai0 = piezo.th.position
    #     ypos = piezo.y.position
    #     ai0_list.append(ai0)
    #     y0_list.append(ypos)
    #     print(f'{name} position is th={ai0},y={ypos}')

    #     dets = [pil1M, pil900KW]

    #     det_exposure_time(t, t)
    #     poss = [1,2]
    #     for pos in poss:
    #         if pos == 2:
    #             yield from bps.mvr(stage.x, 1)
               
    #         for k, ais in enumerate(ai_list):
    #             yield from bps.mv(piezo.th, ai0 + ais)

    #             name_fmt = "{sample}_pos{pos}_ai{ai}_wa{wax}_bpm{xbpm}"
            
    #             bpm = xbpm2.sumX.get()
    #             sample_name = name_fmt.format(sample=name, ai="%3.2f"%ais, wax=20, xbpm="%4.3f"%bpm, pos="%d"%pos)
    #             sample_id(user_name="NS", sample_name=sample_name)
    #             print(f"\n\t=== Sample: {sample_name} ===\n")
    #             yield from bp.count(dets, num=1)

    # print(f'list of angles: {ai0_list}')

    # to pause for 1 second:
    # yield from bps.sleep(1)
    dets = [pil900KW]
    yield from bps.mv(waxs, 0)
    for name, xs, ys, zs, xs_hexa, ai0 in zip(names, x_piezo, y0_list, z_piezo, x_hexa, ai0_list):
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)
        det_exposure_time(t, t)
        poss = [1,2]
        for pos in poss:
            if pos == 2:
                yield from bps.mvr(stage.x, 1)
            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                name_fmt = "{sample}_pos{pos}_ai{ai}_wa{wax}_bpm{xbpm}"
            
                bpm = xbpm2.sumX.get()
                sample_name = name_fmt.format(sample=name, ai="%3.2f"%ais, wax=0, xbpm="%4.3f"%bpm, pos="%d"%pos)
                sample_id(user_name="NS", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

def GIWAXS_2024_vacuum(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    # top of bar approx y=-3500, ai0=-.7, z=5200
    # bottom of bar approx y=5300, ai0=.3, z=1600
    names = [   'PS5',      'PS6',
                'PS7',        'PS8',       'PS9',     'PS10',     'PS11',     'PS12',     'PS13',     'PS14',     'PS16',     'PS17',    
                'PS18',       'PS19',     'PS20',     'PS21',     'PS22',     'PS23',     'PS24',     'PS25',     'PS26',      'PS1',
                'PS15']             
    x_piezo =[   -27000,      -19000,
                  -8000,      3000,       12000,      20000,      29000,      37000,      46000,      49000,     -57000,     -48000,     
                 -36000,    -26000,      -17000,       -8000,          0,       9000,      17000,      26000,      34000,      45000,      
                 49000 ]
    x_hexa = [       -1,           -1,
                   -1,           -1,         -1,        -1,          -1,         -1,         -1,         4 ,         0 ,         0,
                    0,           0,         0,        0,           0,          0,          0,          0,          0,             0,
                    6]
    y_piezo = [   5300,       5300,
                  5300,         5300,       5300,       5300,      5300,        5300,       5300,       5300,       -3500,      -3500, 
                 -3500,         -3500,     -3500,      -3500,     -3500,       -3500,      -3500,      -3500,        -3500,     -3500,
                 -3500]
    z_piezo = [   900,       900,
                  900,          900,        900,        900,       900,         900,        900,        900,        5600,       5600,
                 5600,          5600,       5600,       5600,      5600,        5600,       5400,       5200,        5200,       5200,
                 5200]

    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of y positions ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of z positions ({len(z_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of x heaxpos positions ({len(x_hexa)})"

    waxs_arc = [20, 0] ### not needed anymore I think
    ai0_list = []
    y0_list = []
    ai_list = [0.08, 0.1, 0.12, 0.15, 0.2]


    

    for name, xs, ys, zs, xs_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa):
        yield from bps.mv(waxs, 20)
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)


        if ys <0 : 
            ai0_all = -0.7
        if ys > 0:
            ai0_all = 0.3
        yield from bps.mv(piezo.th, ai0_all)
        yield from alignement_gisaxs_doblestack(0.15)
        
        ai0 = piezo.th.position
        ypos = piezo.y.position
        ai0_list.append(ai0)
        y0_list.append(ypos)
        print(f'{name} position is th={ai0},y={ypos}')

        dets = [pil1M, pil900KW]

        det_exposure_time(t, t)
        poss = [1,2]
        for pos in poss:
            if pos == 2:
                yield from bps.mvr(stage.x, 1)
               
            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                name_fmt = "{sample}_pos{pos}_ai{ai}_wa{wax}_bpm{xbpm}"
            
                bpm = xbpm2.sumX.get()
                sample_name = name_fmt.format(sample=name, ai="%3.2f"%ais, wax=20, xbpm="%4.3f"%bpm, pos="%d"%pos)
                sample_id(user_name="NS", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)
        ### move back to pos 1
        yield from bps.mvr(stage.x, -1)
        # move the waxs detector back in slowly
        yield from bps.mv(waxs, 10)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 6)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 5)
        yield from bps.sleep(1)

        # while waxs.arc.position > 0:
        yield from bps.mv(waxs, 4)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 3)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 2)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 1)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 0)
        dets = [pil900KW]
        det_exposure_time(t, t)
        for pos in poss:
            if pos == 2:
                yield from bps.mvr(stage.x, 1)
            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                name_fmt = "{sample}_pos{pos}_ai{ai}_wa{wax}_bpm{xbpm}"
            
                bpm = xbpm2.sumX.get()
                sample_name = name_fmt.format(sample=name, ai="%3.2f"%ais, wax=0, xbpm="%4.3f"%bpm, pos="%d"%pos)
                sample_id(user_name="NS", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

def move_waxs_man():
    yield from bps.mv(waxs, 7)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 6)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 5)
    yield from bps.sleep(2)
    yield from bps.mv(waxs, 4)
    yield from bps.sleep(2)
    yield from bps.mv(waxs, 3)
    yield from bps.sleep(2)
    yield from bps.mv(waxs, 2)
    yield from bps.sleep(2)
    yield from bps.mv(waxs, 1)
    yield from bps.sleep(2)
    yield from bps.mv(waxs, 0)


def GIWAXS_2024_vacuum_22_end(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    # top of bar approx y=-3500, ai0=-.7, z=5200
    # bottom of bar approx y=5300, ai0=.3, z=1600
    names = [      'PS22',     'PS23',     'PS24',     'PS25',     'PS26',      'PS1',
                'PS15', 'PS21']             
    x_piezo =[           0,       9000,      17000,      26000,      34000,      45000,      
                 49000, -8000 ]
    x_hexa = [             0,          0,          0,          0,          0,             0,
                    6,  0]
    y_piezo = [       -3500,       -3500,      -3500,      -3500,        -3500,     -3500,
                 -3500, -3500]
    z_piezo = [         5600,        5600,       5400,       5200,        5200,       5200,
                 5200,  5600]

    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of y positions ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of z positions ({len(z_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of x heaxpos positions ({len(x_hexa)})"

    waxs_arc = [20, 0] ### not needed anymore I think
    ai0_list = []
    y0_list = []
    ai_list = [0.08, 0.1, 0.12, 0.15, 0.2]


    

    for name, xs, ys, zs, xs_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa):
        yield from bps.mv(waxs, 20)
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)


        if ys <0 : 
            ai0_all = -0.7
        if ys > 0:
            ai0_all = 0.3
        yield from bps.mv(piezo.th, ai0_all)
        yield from alignement_gisaxs_doblestack(0.15)
        
        ai0 = piezo.th.position
        ypos = piezo.y.position
        ai0_list.append(ai0)
        y0_list.append(ypos)
        print(f'{name} position is th={ai0},y={ypos}')

        dets = [pil1M, pil900KW]

        det_exposure_time(t, t)
        poss = [1,2]
        for pos in poss:
            if pos == 2:
                yield from bps.mvr(stage.x, 1)
               
            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                name_fmt = "{sample}_pos{pos}_ai{ai}_wa{wax}_bpm{xbpm}"
            
                bpm = xbpm2.sumX.get()
                sample_name = name_fmt.format(sample=name, ai="%3.2f"%ais, wax=20, xbpm="%4.3f"%bpm, pos="%d"%pos)
                sample_id(user_name="NS", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)
        ### move back to pos 1
        yield from bps.mvr(stage.x, -1)
        # move the waxs detector back in slowly
        yield from bps.mv(waxs, 10)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 6)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 5)
        yield from bps.sleep(1)

        # while waxs.arc.position > 0:
        yield from bps.mv(waxs, 4)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 3)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 2)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 1)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 0)
        dets = [pil900KW]
        det_exposure_time(t, t)
        for pos in poss:
            if pos == 2:
                yield from bps.mvr(stage.x, 1)
            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                name_fmt = "{sample}_pos{pos}_ai{ai}_wa{wax}_bpm{xbpm}"
            
                bpm = xbpm2.sumX.get()
                sample_name = name_fmt.format(sample=name, ai="%3.2f"%ais, wax=0, xbpm="%4.3f"%bpm, pos="%d"%pos)
                sample_id(user_name="NS", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

# def move_waxs_man():
#     yield from bps.mv(waxs, 7)
#     yield from bps.sleep(1)
#     yield from bps.mv(waxs, 6)
#     yield from bps.sleep(1)
#     yield from bps.mv(waxs, 5)
#     yield from bps.sleep(2)
#     yield from bps.mv(waxs, 4)
#     yield from bps.sleep(2)
#     yield from bps.mv(waxs, 3)
#     yield from bps.sleep(2)
#     yield from bps.mv(waxs, 2)
#     yield from bps.sleep(2)
#     yield from bps.mv(waxs, 1)
#     yield from bps.sleep(2)
#     yield from bps.mv(waxs, 0)
    
    
def GIWAXS_2024_vacuum_15_end(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    # top of bar approx y=-3500, ai0=-.7, z=5200
    # bottom of bar approx y=5300, ai0=.3, z=1600
    names = [     'PS15', 'PS21']             
    x_piezo =[           49000, -8000 ]
    x_hexa = [        6,  0]
    y_piezo = [     -3500, -3500]
    z_piezo = [     5200,  5600]

    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of y positions ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of z positions ({len(z_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of x heaxpos positions ({len(x_hexa)})"

    waxs_arc = [20, 0] ### not needed anymore I think
    ai0_list = []
    y0_list = []
    ai_list = [0.08, 0.1, 0.12, 0.15, 0.2]


    

    for name, xs, ys, zs, xs_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa):
        yield from bps.mv(waxs, 20)
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)


        if ys <0 : 
            ai0_all = -0.7
        if ys > 0:
            ai0_all = 0.8
        yield from bps.mv(piezo.th, ai0_all)
        yield from alignement_gisaxs_doblestack(0.15)
        
        ai0 = piezo.th.position
        ypos = piezo.y.position
        ai0_list.append(ai0)
        y0_list.append(ypos)
        print(f'{name} position is th={ai0},y={ypos}')

        dets = [pil1M, pil900KW]

        det_exposure_time(t, t)
        poss = [1,2]
        for pos in poss:
            if pos == 2:
                yield from bps.mvr(stage.x, 1)
               
            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                name_fmt = "{sample}_pos{pos}_ai{ai}_wa{wax}_bpm{xbpm}"
            
                bpm = xbpm2.sumX.get()
                sample_name = name_fmt.format(sample=name, ai="%3.2f"%ais, wax=20, xbpm="%4.3f"%bpm, pos="%d"%pos)
                sample_id(user_name="NS", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)
        ### move back to pos 1
        yield from bps.mvr(stage.x, -1)
        # move the waxs detector back in slowly
        yield from bps.mv(waxs, 10)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 6)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 5)
        yield from bps.sleep(1)

        # while waxs.arc.position > 0:
        yield from bps.mv(waxs, 4)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 3)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 2)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 1)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 0)
        dets = [pil900KW]
        det_exposure_time(t, t)
        for pos in poss:
            if pos == 2:
                yield from bps.mvr(stage.x, 1)
            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                name_fmt = "{sample}_pos{pos}_ai{ai}_wa{wax}_bpm{xbpm}"
            
                bpm = xbpm2.sumX.get()
                sample_name = name_fmt.format(sample=name, ai="%3.2f"%ais, wax=0, xbpm="%4.3f"%bpm, pos="%d"%pos)
                sample_id(user_name="NS", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)
        

def GIWAXS_2024_vacuum_IL(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    # top of bar approx y=-3500, ai0=-.7, z=5200
    # bottom of bar approx y=5300, ai0=.3, z=1600
    names = [   'IL1',      'IL2',
                'IL3',        'IL4',       'IL5',     'IL6',     'IL7',     'IL8',     'IL9',     'IL10',     'IL11',     'IL12',    
                'IL13',       'IL14',     'IL15',     'IL16',     'IL17',     'IL18',     'IL19',     'IL20',     'IL21',      
                'IL22']             
    x_piezo =[   -49000,      -40000,
                  -26000,      -16000,       -7000,      1000,      11000,      23000,      34000,      44000,     49000,     49000,     
                 42000,          33000,       24000,     15000,       4000,      -9000,      -17000,      -26000,      -37000,      
                 -49000 ]
    x_hexa = [       -1,           -1,
                   -1,           -1,         -1,        -1,          -1,         -1,         -1,         -1,         3,         3,
                    0,            0,        0,           0,          0,          0,          0,          0,             0,
                    0]
    y_piezo = [   5300,       5300,
                  5300,          5300,       5300,       5300,      5300,        5300,       5300,       5300,       5300,      -3500, 
                 -3500,         -3500,      -3500,     -3500,       -3500,      -3500,      -3500,        -3500,     -3500,
                 -3500]
    z_piezo = [   400,         400,
                  400,          400,        400,        400,       400,         400,        400,        400,          400,       4600,
                 4600,           5300,       5600,      5600,        5600,       5600,       5600,        5600,       5600,
                 5600]

    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of y positions ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of z positions ({len(z_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of x heaxpos positions ({len(x_hexa)})"

    waxs_arc = [20, 0] ### not needed anymore I think
    ai0_list = []
    y0_list = []
    ai_list = [0.08, 0.1, 0.12, 0.15, 0.2]


    

    for name, xs, ys, zs, xs_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa):
        yield from bps.mv(waxs, 20)
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)


        if ys <0 : 
            ai0_all = -0.7
        if ys > 0:
            ai0_all = 0.3
        yield from bps.mv(piezo.th, ai0_all)
        yield from alignement_gisaxs_doblestack(0.15)
        
        ai0 = piezo.th.position
        ypos = piezo.y.position
        ai0_list.append(ai0)
        y0_list.append(ypos)
        print(f'{name} position is th={ai0},y={ypos}')

        dets = [pil1M, pil900KW]

        det_exposure_time(t, t)
        poss = [1,2]
        for pos in poss:
            if pos == 2:
                yield from bps.mvr(stage.x, 1)
               
            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                name_fmt = "{sample}_pos{pos}_ai{ai}_wa{wax}_bpm{xbpm}"
            
                bpm = xbpm2.sumX.get()
                sample_name = name_fmt.format(sample=name, ai="%3.2f"%ais, wax=20, xbpm="%4.3f"%bpm, pos="%d"%pos)
                sample_id(user_name="NS", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)
        ### move back to pos 1
        yield from bps.mvr(stage.x, -1)
        # move the waxs detector back in slowly
        yield from bps.mv(waxs, 10)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 6)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 5)
        yield from bps.sleep(1)

        # while waxs.arc.position > 0:
        yield from bps.mv(waxs, 4)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 3)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 2)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 1)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 0)
        dets = [pil900KW]
        det_exposure_time(t, t)
        for pos in poss:
            if pos == 2:
                yield from bps.mvr(stage.x, 1)
            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                name_fmt = "{sample}_pos{pos}_ai{ai}_wa{wax}_bpm{xbpm}"
            
                bpm = xbpm2.sumX.get()
                sample_name = name_fmt.format(sample=name, ai="%3.2f"%ais, wax=0, xbpm="%4.3f"%bpm, pos="%d"%pos)
                sample_id(user_name="NS", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

def GIWAXS_2024_vacuum_PN(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    # top of bar approx y=-3500, ai0=-.7, z=5200
    # bottom of bar approx y=5300, ai0=.3, z=1600
    names = [   'PN2',
                'PN3',         'PN4',      'PN5',      'PN6',      'PN7',      'PN8',      'PN9',     'PN10',     'PN11',     'PN12',    
                'PN13',       'PN14',     'PN15',     'PN16',     'PN17',     'PN18',     'PN19',     'PN20',     'PN21',     'PN22', 
                'PN23',     'PN24',     'PN25',     'PN26',     'Si_blank']             
    x_piezo =[   -50000,      
                 -44000,      -35000,      -26000,     -18000,      -8000,      1000,        9000,      18500,      27000,     37000,  
                  47000,       49000,        49000,      44000,       36000,      27000,      15000,      7000,      -4000,      -12000,
                  -2000,      -29000,      -36000,     -45000,      -50000]
    x_hexa = [     -1,           
                   -1,            -1,           -1,       -1,          -1,          -1,         -1,         -1,         -1,         -1,
                   -1,             5,            5,           0,          0,          0,          0,          0,             0,        0,
                    0,            0,        0,         0,           -1]
    y_piezo = [   4900,          
                  4900,         4900,          4900,       4900,       4900,      4900,        4900,       4900,       4900,       4900,
                  4900,         4900,         -4100,     -4100,       -4100,      -4100,      -4100,      -4100,     -4100,      -4100,
                 -4100,         -4100,       -4100,     -4100,       -4100]
    z_piezo = [   400,          
                  400,            400,            400,        400,        400,       400,         400,        400,        400,      400,
                  400,            400,           4000,      4000,        4000,       4000,       4700,        4700,       4700,     4700,
                 4700,           5400,       5400,       5400,       5400]

    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of y positions ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of z positions ({len(z_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of x heaxpos positions ({len(x_hexa)})"

    waxs_arc = [20, 0] ### not needed anymore I think
    ai0_list = []
    y0_list = []
    ai_list = [0.08, 0.1, 0.12, 0.15, 0.2]


    

    for name, xs, ys, zs, xs_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa):
        yield from bps.mv(waxs, 20)
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)


        if ys <0 : 
            ai0_all = -0.7
        if ys > 0:
            ai0_all = 0.3
        yield from bps.mv(piezo.th, ai0_all)
        yield from alignement_gisaxs_doblestack(0.15)
        
        ai0 = piezo.th.position
        ypos = piezo.y.position
        ai0_list.append(ai0)
        y0_list.append(ypos)
        print(f'{name} position is th={ai0},y={ypos}')

        dets = [pil1M, pil900KW]

        det_exposure_time(t, t)
        poss = [1,2]
        for pos in poss:
            if pos == 2:
                yield from bps.mvr(stage.x, 1)
               
            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                name_fmt = "{sample}_pos{pos}_ai{ai}_wa{wax}_bpm{xbpm}"
            
                bpm = xbpm2.sumX.get()
                sample_name = name_fmt.format(sample=name, ai="%3.2f"%ais, wax=20, xbpm="%4.3f"%bpm, pos="%d"%pos)
                sample_id(user_name="NS", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)
        ### move back to pos 1
        yield from bps.mvr(stage.x, -1)
        # move the waxs detector back in slowly
        yield from bps.mv(waxs, 10)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 6)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 5)
        yield from bps.sleep(1)

        # while waxs.arc.position > 0:
        yield from bps.mv(waxs, 4)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 3)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 2)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 1)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 0)
        dets = [pil900KW]
        det_exposure_time(t, t)
        for pos in poss:
            if pos == 2:
                yield from bps.mvr(stage.x, 1)
            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                name_fmt = "{sample}_pos{pos}_ai{ai}_wa{wax}_bpm{xbpm}"
            
                bpm = xbpm2.sumX.get()
                sample_name = name_fmt.format(sample=name, ai="%3.2f"%ais, wax=0, xbpm="%4.3f"%bpm, pos="%d"%pos)
                sample_id(user_name="NS", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

def GIWAXS_2024_vacuum_PT(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    # top of bar approx y=-3500, ai0=-.7, z=5200
    # bottom of bar approx y=5300, ai0=.3, z=1600
    names = [    'PT1',         'PT2',      'PT3',      'PT4',      'PT5',      'PT6',      'PT7',     'PT8',     'PT9',     'PT10',    
                'PT11',        'PT12',      'PT13',     'PN1',     'PT14',     'PT15',     'PT16',     'PT17',    'PT18',    'PT19',     'PT20', 
                'PT21',        'PT22',     'PT23',     'PT24',     'PT25',     'PT26',     'PT27']             
    x_piezo =[  -49000,        -40000,      -33000,      -24000,     -17000,      -7000,       1000,       9000,     19000,      28000,     
                37000,          44000,       49000,       49000,      49000,      42000,      35000,      28000,      21000,    14000,        6000,         
                    0,          -8000,     -15000,      -23000,      -32000,     -40000,      -49000]
    x_hexa = [      -1,             -1,        -1,          -1,         -1,         -1,         -1,      -1,         -1,         -1,       
                  -1,               -1,         3,           9,          2,          0,          0,          0,      0,          0,          0, 
                   0,                0,          0,           0,          0,         0,          0]
    y_piezo = [    5300,         5300,        5300,        5300,      5300,       5300,       5300,       5300,       5300,       5300,       
                 5300,          5300,          5300,       -3500,    -3500,     -3500,       -3500,     -3500,      -3500,      -3500,      -3500,     
                   -3500,      -3500,         -3500,       -3500,     -3500,       -3500,   -3500]
    z_piezo = [    400,          400,           400,         400,       400,         400,       400,         400,        400,        400,    
                   400,          400,            400,        5900,      5900,       5900,        5900,      5900,       5900,       5400,    5400,
                  5400,          5400,           5400,       5400,       5400,       5400,    5400]

    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of y positions ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of z positions ({len(z_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of x heaxpos positions ({len(x_hexa)})"

    waxs_arc = [20, 0] ### not needed anymore I think
    ai0_list = []
    y0_list = []
    ai_list = [0.08, 0.1, 0.12, 0.15, 0.2]


    

    for name, xs, ys, zs, xs_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa):
        yield from bps.mv(waxs, 20)
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)


        if ys <0 : 
            ai0_all = -0.7
        if ys > 0:
            ai0_all = 0.3
        yield from bps.mv(piezo.th, ai0_all)
        yield from alignement_gisaxs_doblestack(0.15)
        
        ai0 = piezo.th.position
        ypos = piezo.y.position
        ai0_list.append(ai0)
        y0_list.append(ypos)
        print(f'{name} position is th={ai0},y={ypos}')

        dets = [pil1M, pil900KW]

        det_exposure_time(t, t)
        poss = [1,2]
        for pos in poss:
            if pos == 2:
                yield from bps.mvr(stage.x, 1)
               
            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                name_fmt = "{sample}_pos{pos}_ai{ai}_wa{wax}_bpm{xbpm}"
            
                bpm = xbpm2.sumX.get()
                sample_name = name_fmt.format(sample=name, ai="%3.2f"%ais, wax=20, xbpm="%4.3f"%bpm, pos="%d"%pos)
                sample_id(user_name="NS", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)
        ### move back to pos 1
        yield from bps.mvr(stage.x, -1)
        # move the waxs detector back in slowly
        yield from bps.mv(waxs, 10)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 6)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 5)
        yield from bps.sleep(1)

        # while waxs.arc.position > 0:
        yield from bps.mv(waxs, 4)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 3)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 2)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 1)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 0)
        dets = [pil900KW]
        det_exposure_time(t, t)
        for pos in poss:
            if pos == 2:
                yield from bps.mvr(stage.x, 1)
            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                name_fmt = "{sample}_pos{pos}_ai{ai}_wa{wax}_bpm{xbpm}"
            
                bpm = xbpm2.sumX.get()
                sample_name = name_fmt.format(sample=name, ai="%3.2f"%ais, wax=0, xbpm="%4.3f"%bpm, pos="%d"%pos)
                sample_id(user_name="NS", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)


def GIWAXS_2024_vacuum_PT_11toend(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    # top of bar approx y=-3500, ai0=-.7, z=5200
    # bottom of bar approx y=5300, ai0=.3, z=1600
    names = [        
                'PT11',        'PT12',      'PT13',     'PN1',     'PT14',     'PT15',     'PT16',     'PT17',    'PT18',    'PT19',     'PT20', 
                'PT21',        'PT22',     'PT23',     'PT24',     'PT25',     'PT26',     'PT27']             
    x_piezo =[       
                37000,          44000,       49000,       49000,      49000,      42000,      35000,      28000,      21000,    14000,        6000,         
                    0,          -8000,     -15000,      -23000,      -32000,     -40000,      -49000]
    x_hexa = [       
                  -1,               -1,         3,           9,          2,          0,          0,          0,      0,          0,          0, 
                   0,                0,          0,           0,          0,         0,          0]
    y_piezo = [        
                 5300,          5300,          5300,       -3500,    -3500,     -3500,       -3500,     -3500,      -3500,      -3500,      -3500,     
                   -3500,      -3500,         -3500,       -3500,     -3500,       -3500,   -3500]
    z_piezo = [       
                   400,          400,            400,        5900,      5900,       5900,        5900,      5900,       5900,       5400,    5400,
                  5400,          5400,           5400,       5400,       5400,       5400,    5400]

    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of y positions ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of z positions ({len(z_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of x heaxpos positions ({len(x_hexa)})"

    waxs_arc = [20, 0] ### not needed anymore I think
    ai0_list = []
    y0_list = []
    ai_list = [0.08, 0.1, 0.12, 0.15, 0.2]


    

    for name, xs, ys, zs, xs_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa):
        yield from bps.mv(waxs, 20)
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)


        if ys <0 : 
            ai0_all = -0.7
        if ys > 0:
            ai0_all = 0.3
        yield from bps.mv(piezo.th, ai0_all)
        yield from alignement_gisaxs_doblestack(0.15)
        
        ai0 = piezo.th.position
        ypos = piezo.y.position
        ai0_list.append(ai0)
        y0_list.append(ypos)
        print(f'{name} position is th={ai0},y={ypos}')

        dets = [pil1M, pil900KW]

        det_exposure_time(t, t)
        poss = [1,2]
        for pos in poss:
            if pos == 2:
                yield from bps.mvr(stage.x, 1)
               
            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                name_fmt = "{sample}_pos{pos}_ai{ai}_wa{wax}_bpm{xbpm}"
            
                bpm = xbpm2.sumX.get()
                sample_name = name_fmt.format(sample=name, ai="%3.2f"%ais, wax=20, xbpm="%4.3f"%bpm, pos="%d"%pos)
                sample_id(user_name="NS", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)
        ### move back to pos 1
        yield from bps.mvr(stage.x, -1)
        # move the waxs detector back in slowly
        yield from bps.mv(waxs, 10)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 6)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 5)
        yield from bps.sleep(1)

        # while waxs.arc.position > 0:
        yield from bps.mv(waxs, 4)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 3)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 2)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 1)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 0)
        dets = [pil900KW]
        det_exposure_time(t, t)
        for pos in poss:
            if pos == 2:
                yield from bps.mvr(stage.x, 1)
            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                name_fmt = "{sample}_pos{pos}_ai{ai}_wa{wax}_bpm{xbpm}"
            
                bpm = xbpm2.sumX.get()
                sample_name = name_fmt.format(sample=name, ai="%3.2f"%ais, wax=0, xbpm="%4.3f"%bpm, pos="%d"%pos)
                sample_id(user_name="NS", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

def GIWAXS_2024_vacuum_PF1(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    # top of bar approx y=-3500, ai0=-.7, z=5200
    # bottom of bar approx y=5300, ai0=.3, z=1600
    names = [    'PF1',         'PF2',      'PF3',      'PF4',      'PF5',      'PF6',      'PF7',     'PF8',     'PF9',     'PF10',    'PT11',    
                'PF11',        'PF12',     'PF13',     'PF14',     'PF15',     'PF16',     'PF17',     'PF18',    'PF19',    'PF20']             
    x_piezo =[  -49500,        -45500,      -33000,      -20000,     -9000,      4000,       16000,      25000,    36000,      47000,    49000,
                49000,          42000,       31000,       18000,      8000,      -1000,     -16000,      -23000,  -36000,    -47000]
    x_hexa = [      -1,            -1,          -1,          -1,         -1,        -1,         -1,       -1,         -1,       -1,         7,
                    2,            0,           0,           0,          0,          0,          0,        0,          0,        0]
    y_piezo = [    5300,         5300,        5300,        5300,      5300,       5300,        5300,      5300,       5300,       5300,     5300,  
                  -3500,        -3500,       -3500,       -3500,     -3500,      -3500,       -3500,     -3500,      -3500,      -3500]
    z_piezo = [    400,          400,           300,         400,       400,         400,       400,       400,       400,        400,       100,
                  4300,         4700,          4700,        4800,      4800,        4900,      4900,      4900,      4900,       4900]

    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of y positions ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of z positions ({len(z_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of x heaxpos positions ({len(x_hexa)})"

    waxs_arc = [20, 0] ### not needed anymore I think
    ai0_list = []
    y0_list = []
    ai_list = [0.08, 0.1, 0.12, 0.15, 0.2]


    

    for name, xs, ys, zs, xs_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa):
        yield from bps.mv(waxs, 20)
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)


        if ys <0 : 
            ai0_all = -0.7
        if ys > 0:
            ai0_all = 0.3
        yield from bps.mv(piezo.th, ai0_all)
        yield from alignement_gisaxs_doblestack(0.15)
        
        ai0 = piezo.th.position
        ypos = piezo.y.position
        ai0_list.append(ai0)
        y0_list.append(ypos)
        print(f'{name} position is th={ai0},y={ypos}')

        dets = [pil1M, pil900KW]

        det_exposure_time(t, t)
        poss = [1,2]
        for pos in poss:
            if pos == 2:
                yield from bps.mvr(stage.x, 1)
               
            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                name_fmt = "{sample}_pos{pos}_ai{ai}_wa{wax}_bpm{xbpm}"
            
                bpm = xbpm2.sumX.get()
                sample_name = name_fmt.format(sample=name, ai="%3.2f"%ais, wax=20, xbpm="%4.3f"%bpm, pos="%d"%pos)
                sample_id(user_name="NS", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)
        ### move back to pos 1
        yield from bps.mvr(stage.x, -1)
        # move the waxs detector back in slowly
        yield from bps.mv(waxs, 10)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 6)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 5)
        yield from bps.sleep(1)

        # while waxs.arc.position > 0:
        yield from bps.mv(waxs, 4)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 3)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 2)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 1)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 0)
        dets = [pil900KW]
        det_exposure_time(t, t)
        for pos in poss:
            if pos == 2:
                yield from bps.mvr(stage.x, 1)
            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                name_fmt = "{sample}_pos{pos}_ai{ai}_wa{wax}_bpm{xbpm}"
            
                bpm = xbpm2.sumX.get()
                sample_name = name_fmt.format(sample=name, ai="%3.2f"%ais, wax=0, xbpm="%4.3f"%bpm, pos="%d"%pos)
                sample_id(user_name="NS", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

def GIWAXS_2024_vacuum_PF2(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    # top of bar approx y=-3500, ai0=-.7, z=5200
    # bottom of bar approx y=5300, ai0=.3, z=1600
    names = [   'PF22',        'PF23',      'PF24',      'PF25',     'PF26',     'PF27',     'PF28',     'PF29',     'PF30',    'PT31',    
                'PF32',        'PF33',      'PF34',      'PF35',     'PF36',     'PF37',     'PF38',     'PF39',    'PF40',    'PF41',
                'PF42'        ]             
    x_piezo =[  -49500,        -42000,      -32000,      -20000,     -6000,      5000,       17000,      32000,    42000,      49000,    
                49000,          45000,       36000,       28000,      19000,      10000,     1000,      -10000,  -22000,    -33000,
               -44000                               ]
    x_hexa = [      -1,            -1,          -1,          -1,         -1,         -1,         -1,       -1,         -1,       1,        
                    4,              0,           0,           0,          0,          0,          0,        0,          0,        0,
                    0]
    y_piezo = [    5300,         5300,        5300,        5300,      5300,       5300,        5300,      5300,       5300,       5300,      
                  -3500,        -3500,       -3500,       -3500,     -3500,      -3500,       -3500,     -3500,      -3500,      -3500,
                  -3500]
    z_piezo = [    400,          400,           400,         400,       400,         400,       400,       400,       400,        400,  
                  5200,         5200,          5200,        5200,      5200,        5200,      5200,      5200,      5200,       5200,
                  5200]

    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of y positions ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of z positions ({len(z_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of x heaxpos positions ({len(x_hexa)})"

    waxs_arc = [20, 0] ### not needed anymore I think
    ai0_list = []
    y0_list = []
    ai_list = [0.08, 0.1, 0.12, 0.15, 0.2]


    

    for name, xs, ys, zs, xs_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa):
        yield from bps.mv(waxs, 20)
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)


        if ys <0 : 
            ai0_all = -0.7
        if ys > 0:
            ai0_all = 0.3
        yield from bps.mv(piezo.th, ai0_all)
        yield from alignement_gisaxs_doblestack(0.15)
        
        ai0 = piezo.th.position
        ypos = piezo.y.position
        ai0_list.append(ai0)
        y0_list.append(ypos)
        print(f'{name} position is th={ai0},y={ypos}')

        dets = [pil1M, pil900KW]

        det_exposure_time(t, t)
        poss = [1,2]
        for pos in poss:
            if pos == 2:
                yield from bps.mvr(stage.x, 1)
               
            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                name_fmt = "{sample}_pos{pos}_ai{ai}_wa{wax}_bpm{xbpm}"
            
                bpm = xbpm2.sumX.get()
                sample_name = name_fmt.format(sample=name, ai="%3.2f"%ais, wax=20, xbpm="%4.3f"%bpm, pos="%d"%pos)
                sample_id(user_name="NS", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)
        ### move back to pos 1
        yield from bps.mvr(stage.x, -1)
        # move the waxs detector back in slowly
        yield from bps.mv(waxs, 10)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 6)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 5)
        yield from bps.sleep(1)

        # while waxs.arc.position > 0:
        yield from bps.mv(waxs, 4)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 3)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 2)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 1)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 0)
        dets = [pil900KW]
        det_exposure_time(t, t)
        for pos in poss:
            if pos == 2:
                yield from bps.mvr(stage.x, 1)
            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                name_fmt = "{sample}_pos{pos}_ai{ai}_wa{wax}_bpm{xbpm}"
            
                bpm = xbpm2.sumX.get()
                sample_name = name_fmt.format(sample=name, ai="%3.2f"%ais, wax=0, xbpm="%4.3f"%bpm, pos="%d"%pos)
                sample_id(user_name="NS", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)


def GIWAXS_2024_vacuum_PF2_36_end(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    # top of bar approx y=-3500, ai0=-.7, z=5200
    # bottom of bar approx y=5300, ai0=.3, z=1600
    names = [        'PF36',     'PF37',     'PF38',     'PF39',    'PF40',    'PF41',
                'PF42'        ]             
    x_piezo =[        19000,      10000,     1000,      -10000,  -22000,    -33000,
               -44000]
    x_hexa = [             0,          0,          0,        0,          0,        0,
                    0]
    y_piezo = [       -3500,      -3500,       -3500,     -3500,      -3500,      -3500,
                  -3500]
    z_piezo = [          5200,        5200,      5200,      5200,      5200,       5200,
                  5200]

    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of y positions ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of z positions ({len(z_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of x heaxpos positions ({len(x_hexa)})"

    waxs_arc = [20, 0] ### not needed anymore I think
    ai0_list = []
    y0_list = []
    ai_list = [0.08, 0.1, 0.12, 0.15, 0.2]


    

    for name, xs, ys, zs, xs_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa):
        yield from bps.mv(waxs, 20)
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)


        if ys <0 : 
            ai0_all = -0.7
        if ys > 0:
            ai0_all = 0.3
        yield from bps.mv(piezo.th, ai0_all)
        yield from alignement_gisaxs_doblestack(0.15)
        
        ai0 = piezo.th.position
        ypos = piezo.y.position
        ai0_list.append(ai0)
        y0_list.append(ypos)
        print(f'{name} position is th={ai0},y={ypos}')

        dets = [pil1M, pil900KW]

        det_exposure_time(t, t)
        poss = [1,2]
        for pos in poss:
            if pos == 2:
                yield from bps.mvr(stage.x, 1)
               
            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                name_fmt = "{sample}_pos{pos}_ai{ai}_wa{wax}_bpm{xbpm}"
            
                bpm = xbpm2.sumX.get()
                sample_name = name_fmt.format(sample=name, ai="%3.2f"%ais, wax=20, xbpm="%4.3f"%bpm, pos="%d"%pos)
                sample_id(user_name="NS", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)
        ### move back to pos 1
        yield from bps.mvr(stage.x, -1)
        # move the waxs detector back in slowly
        yield from bps.mv(waxs, 10)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 6)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 5)
        yield from bps.sleep(1)

        # while waxs.arc.position > 0:
        yield from bps.mv(waxs, 4)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 3)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 2)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 1)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 0)
        dets = [pil900KW]
        det_exposure_time(t, t)
        for pos in poss:
            if pos == 2:
                yield from bps.mvr(stage.x, 1)
            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                name_fmt = "{sample}_pos{pos}_ai{ai}_wa{wax}_bpm{xbpm}"
            
                bpm = xbpm2.sumX.get()
                sample_name = name_fmt.format(sample=name, ai="%3.2f"%ais, wax=0, xbpm="%4.3f"%bpm, pos="%d"%pos)
                sample_id(user_name="NS", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)



def GIWAXS_2024_vacuum_NCSU1(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    # top of bar approx y=-3500, ai0=-.7, z=5200
    # bottom of bar approx y=5300, ai0=.3, z=1600
    names = [   'DL1',        'DL2',      'DL3',      'DL4',        'DL5',     'DL6',     'DL7',     'DL8',     'DL9',    'DL10',    
                'DL11',        'VM1',      'VM2',      'VM3',        'VM4',     'VM5',     'VM6',     'VM7',     'PF21']             
    x_piezo =[  -45000,      -35000,      -25000,      -15000,     -4000,      7000,      17000,      27000,     36000,      47000,    
                48000,        37000,       25000,       12000,         0,    -13000,     -27000,     -39000,    -49000]
    x_hexa = [      0,          0,           0,           0,          0,          0,          0,        0,          0,         0,        
                    0,          0,           0,           0,          0,          0,          0,        0,          0]
    y_piezo = [    5300,       5300,        5300,        5300,      5300,       5300,      5300,      5300,      5300,      5300,      
                  -3500,      -3500,       -3500,       -3500,     -3500,      -3500,     -3500,     -3500,     -3500]
    z_piezo = [    400,       400,         400,          400,         400,      400,       400,       400,       400,        200,  
                  5200,       5200,       5200,        5200,         5200,      5200,      5200,      5200,      5200]

    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of y positions ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of z positions ({len(z_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of x heaxpos positions ({len(x_hexa)})"

    waxs_arc = [20, 0] ### not needed anymore I think
    ai0_list = []
    y0_list = []
    ai_list = [0.08, 0.1, 0.12, 0.15, 0.2]


    

    for name, xs, ys, zs, xs_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa):
        yield from bps.mv(waxs, 20)
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)


        if ys <0 : 
            ai0_all = -0.7
        if ys > 0:
            ai0_all = 0.3
        yield from bps.mv(piezo.th, ai0_all)
        yield from alignement_gisaxs_doblestack(0.15)
        
        ai0 = piezo.th.position
        ypos = piezo.y.position
        ai0_list.append(ai0)
        y0_list.append(ypos)
        print(f'{name} position is th={ai0},y={ypos}')

        dets = [pil1M, pil900KW]

        det_exposure_time(t, t)
        poss = [1,2]
        for pos in poss:
            if pos == 2:
                yield from bps.mvr(stage.x, 1)
               
            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                name_fmt = "{sample}_pos{pos}_ai{ai}_wa{wax}_bpm{xbpm}"
            
                bpm = xbpm2.sumX.get()
                sample_name = name_fmt.format(sample=name, ai="%3.2f"%ais, wax=20, xbpm="%4.3f"%bpm, pos="%d"%pos)
                sample_id(user_name="NS", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)
        ### move back to pos 1
        yield from bps.mvr(stage.x, -1)
        # move the waxs detector back in slowly
        yield from bps.mv(waxs, 10)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 6)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 5)
        yield from bps.sleep(1)

        # while waxs.arc.position > 0:
        yield from bps.mv(waxs, 4)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 3)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 2)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 1)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 0)
        dets = [pil900KW]
        det_exposure_time(t, t)
        for pos in poss:
            if pos == 2:
                yield from bps.mvr(stage.x, 1)
            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                name_fmt = "{sample}_pos{pos}_ai{ai}_wa{wax}_bpm{xbpm}"
            
                bpm = xbpm2.sumX.get()
                sample_name = name_fmt.format(sample=name, ai="%3.2f"%ais, wax=0, xbpm="%4.3f"%bpm, pos="%d"%pos)
                sample_id(user_name="NS", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)



def GIWAXS_2024_vacuum_NCSU2_plus_reruns(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    # top of bar approx y=-3500, ai0=-.7, z=5200
    # bottom of bar approx y=5300, ai0=.3, z=1600
    names = [   'PC_VTA_a',  'PC_VTA_b',  'PC_As_a',   'PC_As_b',  'PQ_VTA_a', 'PQ_VTA_b',  'PQ_As_a',  'PQ_As_b',  'F_VTA_a', 'F_VTA_b',    
                'F_As_a',    'F_As_b',    'PC_VTA',     'PS8',     'PS9',      'PS10',      'PS15',     'PS17',     'PS18',    'PS19',
                'PS20',      'PS21',      'PS22']             
    x_piezo =[  -49000,      -37000,      -26000,      -15000,     -5000,        6000,      17000,       28000,     40000,      48000,    
                48000,        37000,       27000,       18000,     11000,        2000,      -5000,      -13000,    -22000,     -28000, 
               -35000,       -44000,      -49000]
    x_hexa = [      0,          0,           0,           0,          0,          0,          0,         0,          0,         4,        
                    0,          0,           0,           0,          0,          0,          0,         0,          0,         0,
                    0,         0,           -1]
    y_piezo = [    5300,       5300,        5300,        5300,      5300,       5300,      5300,        5300,      5300,      5300,      
                  -3500,      -3500,       -3500,       -3500,     -3500,      -3500,     -3500,       -3500,     -3500,     -3500,
                  -3500,      -3500,       -3500]
    z_piezo = [    400,       400,         400,          400,         400,      400,       400,         400,       400,        200,  
                  5200,       5200,       5200,        5200,         5200,      5200,      5200,        5200,      5100,      5200,
                  5200,       5200,       5200]

    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of y positions ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of z positions ({len(z_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of x heaxpos positions ({len(x_hexa)})"

    waxs_arc = [20, 0] ### not needed anymore I think
    ai0_list = []
    y0_list = []
    ai_list = [0.08, 0.1, 0.12, 0.15, 0.2]


    

    for name, xs, ys, zs, xs_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa):
        yield from bps.mv(waxs, 20)
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)


        if ys <0 : 
            ai0_all = -0.7
        if ys > 0:
            ai0_all = 0.3
        yield from bps.mv(piezo.th, ai0_all)
        yield from alignement_gisaxs_doblestack(0.15)
        
        ai0 = piezo.th.position
        ypos = piezo.y.position
        ai0_list.append(ai0)
        y0_list.append(ypos)
        print(f'{name} position is th={ai0},y={ypos}')

        dets = [pil1M, pil900KW]

        det_exposure_time(t, t)
        poss = [1,2]
        for pos in poss:
            if pos == 2:
                yield from bps.mvr(stage.x, 1)
               
            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                name_fmt = "{sample}_pos{pos}_ai{ai}_wa{wax}_bpm{xbpm}"
            
                bpm = xbpm2.sumX.get()
                sample_name = name_fmt.format(sample=name, ai="%3.2f"%ais, wax=20, xbpm="%4.3f"%bpm, pos="%d"%pos)
                sample_id(user_name="NS", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)
        ### move back to pos 1
        yield from bps.mvr(stage.x, -1)
        # move the waxs detector back in slowly
        yield from bps.mv(waxs, 10)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 6)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 5)
        yield from bps.sleep(1)

        # while waxs.arc.position > 0:
        yield from bps.mv(waxs, 4)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 3)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 2)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 1)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 0)
        dets = [pil900KW]
        det_exposure_time(t, t)
        for pos in poss:
            if pos == 2:
                yield from bps.mvr(stage.x, 1)
            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                name_fmt = "{sample}_pos{pos}_ai{ai}_wa{wax}_bpm{xbpm}"
            
                bpm = xbpm2.sumX.get()
                sample_name = name_fmt.format(sample=name, ai="%3.2f"%ais, wax=0, xbpm="%4.3f"%bpm, pos="%d"%pos)
                sample_id(user_name="NS", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)




def GIWAXS_2024_vacuum_NCSU2_plus_reruns2(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    # top of bar approx y=-3500, ai0=-.7, z=5200
    # bottom of bar approx y=5300, ai0=.3, z=1600
    names = [   'PS15',     'PS17',     'PS18',    'PS19',   'PS20',      'PS21',      'PS22']             
    x_piezo =[    -5000,      -13000,    -22000,   -28000,   -35000,       -44000,      -49000]
    x_hexa = [         0,         0,          0,      0,          0,         0,           -1]
    y_piezo = [     -3500,       -3500,     -3500,   -3500,   -3500,      -3500,       -3500]
    z_piezo = [      5200,        5200,      5100,   5200,      5200,       5200,       5200]

    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of y positions ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of z positions ({len(z_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of x heaxpos positions ({len(x_hexa)})"

    waxs_arc = [20, 0] ### not needed anymore I think
    ai0_list = []
    y0_list = []
    ai_list = [0.08, 0.1, 0.12, 0.15, 0.2]


    

    for name, xs, ys, zs, xs_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa):
        yield from bps.mv(waxs, 20)
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)


        if ys <0 : 
            ai0_all = -0.7
        if ys > 0:
            ai0_all = 0.3
        yield from bps.mv(piezo.th, ai0_all)
        yield from alignement_gisaxs_doblestack(0.15)
        
        ai0 = piezo.th.position
        ypos = piezo.y.position
        ai0_list.append(ai0)
        y0_list.append(ypos)
        print(f'{name} position is th={ai0},y={ypos}')

        dets = [pil1M, pil900KW]

        det_exposure_time(t, t)
        poss = [1,2]
        for pos in poss:
            if pos == 2:
                yield from bps.mvr(stage.x, 1)
               
            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                name_fmt = "{sample}_pos{pos}_ai{ai}_wa{wax}_bpm{xbpm}"
            
                bpm = xbpm2.sumX.get()
                sample_name = name_fmt.format(sample=name, ai="%3.2f"%ais, wax=20, xbpm="%4.3f"%bpm, pos="%d"%pos)
                sample_id(user_name="NS", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)
        ### move back to pos 1
        yield from bps.mvr(stage.x, -1)
        # move the waxs detector back in slowly
        yield from bps.mv(waxs, 10)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 6)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 5)
        yield from bps.sleep(1)

        # while waxs.arc.position > 0:
        yield from bps.mv(waxs, 4)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 3)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 2)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 1)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 0)
        dets = [pil900KW]
        det_exposure_time(t, t)
        for pos in poss:
            if pos == 2:
                yield from bps.mvr(stage.x, 1)
            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                name_fmt = "{sample}_pos{pos}_ai{ai}_wa{wax}_bpm{xbpm}"
            
                bpm = xbpm2.sumX.get()
                sample_name = name_fmt.format(sample=name, ai="%3.2f"%ais, wax=0, xbpm="%4.3f"%bpm, pos="%d"%pos)
                sample_id(user_name="NS", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

def GIWAXS_2024_vacuum_NCSU2_plus_reruns3(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    # top of bar approx y=-3500, ai0=-.7, z=5200
    # bottom of bar approx y=5300, ai0=.3, z=1600
    names = [  'PS22']             
    x_piezo =[     -49000]
    x_hexa = [       -1]
    y_piezo = [      -3500]
    z_piezo = [         5200]

    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of y positions ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of z positions ({len(z_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of x heaxpos positions ({len(x_hexa)})"

    waxs_arc = [20, 0] ### not needed anymore I think
    ai0_list = []
    y0_list = []
    ai_list = [0.08, 0.1, 0.12, 0.15, 0.2]


    

    for name, xs, ys, zs, xs_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa):
        yield from bps.mv(waxs, 20)
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)


        if ys <0 : 
            ai0_all = -0.7
        if ys > 0:
            ai0_all = 0.3
        yield from bps.mv(piezo.th, ai0_all)
        yield from alignement_gisaxs_doblestack(0.15)
        
        ai0 = piezo.th.position
        ypos = piezo.y.position
        ai0_list.append(ai0)
        y0_list.append(ypos)
        print(f'{name} position is th={ai0},y={ypos}')

        dets = [pil1M, pil900KW]

        det_exposure_time(t, t)
        poss = [1,2]
        for pos in poss:
            if pos == 2:
                yield from bps.mvr(stage.x, 1)
               
            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                name_fmt = "{sample}_pos{pos}_ai{ai}_wa{wax}_bpm{xbpm}"
            
                bpm = xbpm2.sumX.get()
                sample_name = name_fmt.format(sample=name, ai="%3.2f"%ais, wax=20, xbpm="%4.3f"%bpm, pos="%d"%pos)
                sample_id(user_name="NS", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)
        ### move back to pos 1
        yield from bps.mvr(stage.x, -1)
        # move the waxs detector back in slowly
        yield from bps.mv(waxs, 10)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 6)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 5)
        yield from bps.sleep(1)

        # while waxs.arc.position > 0:
        yield from bps.mv(waxs, 4)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 3)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 2)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 1)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 0)
        dets = [pil900KW]
        det_exposure_time(t, t)
        for pos in poss:
            if pos == 2:
                yield from bps.mvr(stage.x, 1)
            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                name_fmt = "{sample}_pos{pos}_ai{ai}_wa{wax}_bpm{xbpm}"
            
                bpm = xbpm2.sumX.get()
                sample_name = name_fmt.format(sample=name, ai="%3.2f"%ais, wax=0, xbpm="%4.3f"%bpm, pos="%d"%pos)
                sample_id(user_name="NS", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)




    # LThermal

    # #examples

    # right before a measurement, you can add the current temperature to the file name like this:
    # sample_id(user_name='NS', sample_name=f'{name_base}_{LThermal.temperature()}degC')
    # and add the temperature to the metadata as well like this    
    # RE.md['temp'] = LThermal.temperature()


    # LThermal.on() # turn on the heating

    # LThermal.off(self): # turn off the heating

    # LThermal.setTemperature(temperature): # sets the setpoint

    # LThermal.setTemperatureRate(temperature_rate): # sets the rate

    # LThermal.temperature() #reads back the current temperature

    # LThermal.temperatureRate() # reads back the current temperature

    
    """to set a temperature and wait until you get there you can do something like this:
    
    yield from bps.mv(LThermal.lnp_mode_set,'Auto') # set the Auto pump setting
    
    LThermal.setTemperatureRate(20) # set the ramp rate (20C/min)

    LThermal.setTemperature(100) # set the temperature to whatever (100C)

    LThermal.on() # turn the heater on (start the ramp)

    # sleep for the ramp time that the linkam thinks it will take
    yield from bps.sleep(60*LThermal.ramptime.get()) 

    # check if you are there and wait a little longer if not and maybe error out after some long time
    wait_counter=0
    while(abs(LThermal.temperature()-temperature)>1):
        yield from bps.sleep(60)
        wait_counter+=1
        if wait_counter>5
            raise TimeoutError("Linkam is not getting to temperature!")

    # read the temperature and put it in the filename and metadata (assuming you've already defined name_base)
    sample_id(user_name='NS', sample_name=f'{name_base}_{LThermal.temperature()}degC')
    
    # put the actual temperature in the metadata (not filename)
    RE.md['temp'] = LThermal.temperature()

    # take your measurements
    yield from bps.count([dets]) ...
    """


    # instead of other alignment use: 
    # alignement_gisaxs_hex()

def GIWAXS_TD_run():
    T_start = 20
    T_array = [-70,-50,25]
    names = ['PS3',       'PS7',     'PS11']
    
    x_hexa = [2.5 ,     -4,           -11]
    y_piezo = [0.2,       0.2,    0.2] ### piezo here is just the name, it is actually moving hexa. don't mess with the piezo
    z_piezo =  [3,3,3]

    assert len(x_hexa) == len(y_piezo), f"Number of X coordinates ({len(x_hexa)}) is different from number of y positions ({len(y_piezo)})"
    assert len(x_hexa) == len(z_piezo), f"Number of X coordinates ({len(x_hexa)}) is different from number of z positions ({len(z_piezo)})"
    assert len(x_hexa) == len(names), f"Number of X coordinates ({len(x_hexa)}) is different from number of z positions ({len(names)})"

    ai0_list = []
    y0_list = []
    ai0_list_cold = []
    y0_list_cold = []
    ai_list = [0.08, 0.1, 0.12, 0.15, 0.2]
    dets = [pil900KW]
    yield from bps.mv(LThermal.lnp_mode_set,'Auto')
    LThermal.setTemperatureRate(20)

    # Move to first temperature
    LThermal.setTemperature(T_start)
    LThermal.on()
    yield from bps.sleep(60*LThermal.ramptime.get()) 
    wait_counter=0
    while(abs(LThermal.temperature()-T_start)>1):
        yield from bps.sleep(10)
        wait_counter+=1
        if wait_counter>5*6:
            raise TimeoutError("Linkam is not getting to temperature!")
        ## 


    ### align the samples first before cooling
    for name, ys, zs, xs_hexa in zip(names, y_piezo, z_piezo, x_hexa):
        yield from bps.mv(waxs, 15)
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(stage.y, ys)
        yield from bps.mv(stage.z, zs)

        yield from alignement_gisaxs_hex(0.15)
        ai0 = stage.th.position
        ypos = stage.y.position
        ai0_list.append(ai0)
        y0_list.append(ypos)
        print(f'{name} position is th={ai0},y={ypos}')
        print(f'ai0 list is {ai0_list} and y list is {y0_list}')
    
    ### move waxs arc back in for waxs
    yield from bps.mv(waxs, 10)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 6)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 5)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 4)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 3)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 2)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 1)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 0)

    # measure the first temperature waxs
    for name, ys, zs, xs_hexa, ai0 in zip(names, y0_list, z_piezo, x_hexa, ai0_list):
        yield from bps.mv(waxs, 0)
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(stage.y, ys)
        yield from bps.mv(stage.z, zs)
            
        for k, ais in enumerate(ai_list):
            yield from bps.mv(stage.th, ai0 + ais)

            name_fmt = "{sample}_{temp}C_ai{ai}_wa{wax}_bpm{xbpm}"
        
            bpm = xbpm2.sumX.get()
            sample_name = name_fmt.format(sample=name, ai="%3.2f"%ais, wax=0, xbpm="%4.3f"%bpm,temp = "%3.2f"%T_start)
            sample_id(user_name="NS", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)    

    # Move to first cold temperature
    # ai0 list is [0.454, 0.428, 0.38] and y list is [0.243, 0.271, 0.31]
    LThermal.setTemperature(T_array[0])
    LThermal.on()
    yield from bps.sleep(60*LThermal.ramptime.get()) 
    wait_counter=0
    while(abs(LThermal.temperature()-T_array[0])>1):
        yield from bps.sleep(10)
        wait_counter+=1
        if wait_counter>5*6:
            raise TimeoutError("Linkam is not getting to temperature!")
        ## 

    # check alignment again at first temperature
    for name, ys, zs, xs_hexa in zip(names, y0_list, z_piezo, x_hexa):
        yield from bps.mv(waxs, 15)
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(stage.y, ys)
        yield from bps.mv(stage.z, zs)

        yield from alignement_gisaxs_hex(0.15)
        ai0_cold = stage.th.position
        ypos_cold = stage.y.position
        ai0_list_cold.append(ai0_cold)
        y0_list_cold.append(ypos_cold)
        print(f'{name} position is th={ai0_cold},y={ypos_cold}')
        print(f'ai0 list is {ai0_list_cold} and y list is {y0_list_cold}')
    for i, cold_align in enumerate(ai0_list_cold):
        if abs(ai0_list_cold[i] - ai0_list[i]) > 0.015:
            raise ValueError(f'ai0 alignment at cold T ({ai0_list_cold}) was way far off initial alignment ({ai0_list})')
        if abs(y0_list_cold[i] - y0_list[i]) > 0.03:
            raise ValueError(f'y alignment at cold T ({y0_list_cold}) was way far off initial alignment ({y0_list})')

    ### move waxs arc back in for waxs
    yield from bps.mv(waxs, 10)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 6)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 5)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 4)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 3)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 2)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 1)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 0)
    
    for T in T_array:

        LThermal.setTemperature(T)
        LThermal.on()
        yield from bps.sleep(60*LThermal.ramptime.get()) 
        wait_counter=0
        while(abs(LThermal.temperature()-temperature)>1):
            yield from bps.sleep(10)
            wait_counter+=1
            if wait_counter>5*6:
                raise TimeoutError("Linkam is not getting to temperature!")
            
        ### at a temp, do a quick T hold
        yield from bps.sleep(150)

        ## measure the waxs for each sample 
        for name, ys, zs, xs_hexa, ai0 in zip(names, y0_list, z_piezo, x_hexa, ai0_list):
            yield from bps.mv(waxs, 0)
            yield from bps.mv(stage.x, xs_hexa)
            yield from bps.mv(stage.y, ys)
            yield from bps.mv(stage.z, zs)

                
            for k, ais in enumerate(ai_list):
                yield from bps.mv(stage.th, ai0 + ais)

                name_fmt = "{sample}_{temp}C_ai{ai}_wa{wax}_bpm{xbpm}"
            
                bpm = xbpm2.sumX.get()
                sample_name = name_fmt.format(sample=name, ai="%3.2f"%ais, wax=0, xbpm="%4.3f"%bpm, temp = "%3.2f"%T)
                sample_id(user_name="NS", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)    

def take_manual_waxs_TD(name='test', ai_list = [0.08, 0.1, 0.12, 0.15, 0.2],t=1):
    """
    In case waxs arc breaks while moving, take data after sample was aligned
    """
    yield from bps.mv(waxs, 2.5)
    
    dets = [pil900KW]
    ai0 = stage.th.position # needs to be stage right?
    det_exposure_time(t, t)
    for k, ais in enumerate(ai_list):
        yield from bps.mv(stage.th, ai0 + ais)

        name_fmt = "{sample}_ai{ai}_wa{wax}"
    
        bpm = xbpm2.sumX.get()
        sample_name = name_fmt.format(sample=name, ai="%3.2f"%ais, wax=0)
        sample_id(user_name="NS", sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")
        yield from bp.count(dets, num=1)

def GIWAXS_TD_run2():
    T_start = 20
    T_array = [-70,-50,25]
    names = ['PS3',       'PS7',     'PS11']
    
    x_hexa = [2.5 ,     -4,           -11]
    y_piezo = [0.2,       0.2,    0.2] ### piezo here is just the name, it is actually moving hexa. don't mess with the piezo
    z_piezo =  [3,3,3]

    assert len(x_hexa) == len(y_piezo), f"Number of X coordinates ({len(x_hexa)}) is different from number of y positions ({len(y_piezo)})"
    assert len(x_hexa) == len(z_piezo), f"Number of X coordinates ({len(x_hexa)}) is different from number of z positions ({len(z_piezo)})"
    assert len(x_hexa) == len(names), f"Number of X coordinates ({len(x_hexa)}) is different from number of z positions ({len(names)})"

    ai0_list = [0.453, 0.437, 0.361]
    y0_list =  [0.25, 0.292, 0.335]
    ai0_list_cold = []
    y0_list_cold = []
    ai_list = [0.05,0.08, 0.1, 0.12, 0.15, 0.2,0.25,0.3]
    dets = [pil900KW]
    yield from bps.mv(LThermal.lnp_mode_set,'Auto')
    LThermal.setTemperatureRate(20)

    # # Move to first temperature
    # LThermal.setTemperature(T_start)
    # LThermal.on()
    # yield from bps.sleep(60*LThermal.ramptime.get()) 
    # wait_counter=0
    # while(abs(LThermal.temperature()-T_start)>1):
    #     yield from bps.sleep(10)
    #     wait_counter+=1
    #     if wait_counter>5*6:
    #         raise TimeoutError("Linkam is not getting to temperature!")
    #     ## 


    # ### align the samples first before cooling
    # for name, ys, zs, xs_hexa in zip(names, y_piezo, z_piezo, x_hexa):
    #     yield from bps.mv(waxs, 15)
    #     yield from bps.mv(stage.x, xs_hexa)
    #     yield from bps.mv(stage.y, ys)
    #     yield from bps.mv(stage.z, zs)

    #     yield from alignement_gisaxs_hex(0.15)
    #     ai0 = stage.th.position
    #     ypos = stage.y.position
    #     ai0_list.append(ai0)
    #     y0_list.append(ypos)
    #     print(f'{name} position is th={ai0},y={ypos}')
    #     print(f'ai0 list is {ai0_list} and y list is {y0_list}')
    
    # ### move waxs arc back in for waxs
    # yield from bps.mv(waxs, 10)
    # yield from bps.sleep(1)
    # yield from bps.mv(waxs, 6)
    # yield from bps.sleep(1)
    # yield from bps.mv(waxs, 5)
    # yield from bps.sleep(1)
    # yield from bps.mv(waxs, 4)
    # yield from bps.sleep(1)
    # yield from bps.mv(waxs, 3)
    # yield from bps.sleep(1)
    # yield from bps.mv(waxs, 2)
    # yield from bps.sleep(1)
    # yield from bps.mv(waxs, 1)
    # yield from bps.sleep(1)
    # yield from bps.mv(waxs, 0)

    # # measure the first temperature waxs
    # for name, ys, zs, xs_hexa, ai0 in zip(names, y0_list, z_piezo, x_hexa, ai0_list):
    #     yield from bps.mv(waxs, 0)
    #     yield from bps.mv(stage.x, xs_hexa)
    #     yield from bps.mv(stage.y, ys)
    #     yield from bps.mv(stage.z, zs)
            
    #     for k, ais in enumerate(ai_list):
    #         yield from bps.mv(stage.th, ai0 + ais)

    #         name_fmt = "{sample}_{temp}C_ai{ai}_wa{wax}_bpm{xbpm}"
        
    #         bpm = xbpm2.sumX.get()
    #         sample_name = name_fmt.format(sample=name, ai="%3.2f"%ais, wax=0, xbpm="%4.3f"%bpm,temp = "%3.2f"%T_start)
    #         sample_id(user_name="NS", sample_name=sample_name)
    #         print(f"\n\t=== Sample: {sample_name} ===\n")
    #         yield from bp.count(dets, num=1)    

    # Move to first cold temperature
    # ai0 list is [0.454, 0.428, 0.38] and y list is [0.243, 0.271, 0.31]
    # LThermal.setTemperature(T_array[0])
    # LThermal.on()
    # yield from bps.sleep(60*LThermal.ramptime.get()) 
    # wait_counter=0
    # while(abs(LThermal.temperature()-T_array[0])>1):
    #     yield from bps.sleep(10)
    #     wait_counter+=1
    #     if wait_counter>5*6:
    #         raise TimeoutError("Linkam is not getting to temperature!")
    #     ## 

    # # check alignment again at first temperature
    # for name, ys, zs, xs_hexa in zip(names, y0_list, z_piezo, x_hexa):
    #     yield from bps.mv(waxs, 15)
    #     yield from bps.mv(stage.x, xs_hexa)
    #     yield from bps.mv(stage.y, ys)
    #     yield from bps.mv(stage.z, zs)

    #     yield from alignement_gisaxs_hex(0.15)
    #     ai0_cold = stage.th.position
    #     ypos_cold = stage.y.position
    #     ai0_list_cold.append(ai0_cold)
    #     y0_list_cold.append(ypos_cold)
    #     print(f'{name} position is th={ai0_cold},y={ypos_cold}')
    #     print(f'ai0 list is {ai0_list_cold} and y list is {y0_list_cold}')
    # for i, cold_align in enumerate(ai0_list_cold):
    #     if abs(ai0_list_cold[i] - ai0_list[i]) > 0.015:
    #         raise ValueError(f'ai0 alignment at cold T ({ai0_list_cold}) was way far off initial alignment ({ai0_list})')
    #     if abs(y0_list_cold[i] - y0_list[i]) > 0.03:
    #         raise ValueError(f'y alignment at cold T ({y0_list_cold}) was way far off initial alignment ({y0_list})')

    ### move waxs arc back in for waxs
    # yield from bps.mv(waxs, 10)
    # yield from bps.sleep(1)
    # yield from bps.mv(waxs, 6)
    # yield from bps.sleep(1)
    # yield from bps.mv(waxs, 5)
    # yield from bps.sleep(1)
    # yield from bps.mv(waxs, 4)
    # yield from bps.sleep(1)
    # yield from bps.mv(waxs, 3)
    # yield from bps.sleep(1)
    # yield from bps.mv(waxs, 2)
    # yield from bps.sleep(1)
    # yield from bps.mv(waxs, 1)
    # yield from bps.sleep(1)
    # yield from bps.mv(waxs, 0)

# add metadata for all scans from no onward
    # RE.md['sample notes'] = {'sample info 1": 2 ,"sample_info_3":[1,2,3,4,5]}
# remove metadata
    # del RE.md['sample_notes']

    for T in T_array:

        LThermal.setTemperature(T)
        LThermal.on()
        yield from bps.sleep(60*LThermal.ramptime.get()) 
        wait_counter=0
        while(abs(LThermal.temperature()-T)>1):
            yield from bps.sleep(10)
            wait_counter+=1
            if wait_counter>5*6:
                raise TimeoutError("Linkam is not getting to temperature!")
            
        ### at a temp, do a quick T hold
        yield from bps.sleep(150)

        ## measure the waxs for each sample 
        for name, ys, zs, xs_hexa, ai0 in zip(names, y0_list, z_piezo, x_hexa, ai0_list):
            yield from bps.mv(waxs, 2.5)
            yield from bps.mv(stage.x, xs_hexa)
            yield from bps.mv(stage.y, ys)
            yield from bps.mv(stage.z, zs)

            RE.md['alignment results']={'ai0':ai0,'y0':ys}
            for k, ais in enumerate(ai_list):
                yield from bps.mv(stage.th, ai0 + ais)

                name_fmt = "{sample}_{temp}C_ai{ai}_wa{wax}_bpm{xbpm}"
            
                bpm = xbpm2.sumX.get()
                sample_name = name_fmt.format(sample=name, ai="%3.2f"%ais, wax=0, xbpm="%4.3f"%bpm, temp = "%3.2f"%T)
                sample_id(user_name="NS", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)  

def GIWAXS_TD_run3():
    T_start = 20
    T_array = [-70,-50,25]
    names = ['PS12',       'PS2',     'PS13',       'PS14']
    
    x_hexa = [3 ,     -1.5,           -6.5, -11]
    y_piezo = [0.3,       0.3,    0.3, 0.3] ### piezo here is just the name, it is actually moving hexa. don't mess with the piezo
    z_piezo =  [3,3,3,3]

    assert len(x_hexa) == len(y_piezo), f"Number of X coordinates ({len(x_hexa)}) is different from number of y positions ({len(y_piezo)})"
    assert len(x_hexa) == len(z_piezo), f"Number of X coordinates ({len(x_hexa)}) is different from number of z positions ({len(z_piezo)})"
    assert len(x_hexa) == len(names), f"Number of X coordinates ({len(x_hexa)}) is different from number of z positions ({len(names)})"

    ai0_list = []
    y0_list = []
    ai0_list_cold = []
    y0_list_cold = []
    ai_list = [0.05,0.08, 0.1, 0.12, 0.15, 0.2,0.25,0.3]
    dets = [pil900KW]
    yield from bps.mv(LThermal.lnp_mode_set,'Auto')
    LThermal.setTemperatureRate(20)

    # Move to first temperature
    LThermal.setTemperature(T_start)
    LThermal.on()
    yield from bps.sleep(60*LThermal.ramptime.get()) 
    wait_counter=0
    while(abs(LThermal.temperature()-T_start)>1):
        yield from bps.sleep(10)
        wait_counter+=1
        if wait_counter>5*6:
            raise TimeoutError("Linkam is not getting to temperature!")
        ## 


    ### align the samples first before cooling
    for name, ys, zs, xs_hexa in zip(names, y_piezo, z_piezo, x_hexa):
        yield from bps.mv(waxs, 15)
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(stage.y, ys)
        yield from bps.mv(stage.z, zs)

        yield from alignement_gisaxs_hex(0.15)
        ai0 = stage.th.position
        ypos = stage.y.position
        ai0_list.append(ai0)
        y0_list.append(ypos)
        print(f'{name} position is th={ai0},y={ypos}')
        print(f'ai0 list is {ai0_list} and y list is {y0_list}')
    
    ### move waxs arc back in for waxs
    yield from bps.mv(waxs, 10)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 6)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 5)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 4)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 3)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 2.5)


    # measure the first temperature waxs
    for name, ys, zs, xs_hexa, ai0 in zip(names, y0_list, z_piezo, x_hexa, ai0_list):
        yield from bps.mv(waxs, 2.5)
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(stage.y, ys)
        yield from bps.mv(stage.z, zs)
            
        for k, ais in enumerate(ai_list):
            yield from bps.mv(stage.th, ai0 + ais)

            name_fmt = "{sample}_{temp}C_ai{ai}_wa{wax}_bpm{xbpm}"
        
            bpm = xbpm2.sumX.get()
            sample_name = name_fmt.format(sample=name, ai="%3.2f"%ais, wax=0, xbpm="%4.3f"%bpm,temp = "%3.2f"%T_start)
            sample_id(user_name="NS", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)    

    # Move to first cold temperature
    LThermal.setTemperature(T_array[0])
    LThermal.on()
    yield from bps.sleep(60*LThermal.ramptime.get()) 
    wait_counter=0
    while(abs(LThermal.temperature()-T_array[0])>1):
        yield from bps.sleep(10)
        wait_counter+=1
        if wait_counter>5*6:
            raise TimeoutError("Linkam is not getting to temperature!")
        ## 

    # check alignment again at first temperature
    for name, ys, zs, xs_hexa in zip(names, y0_list, z_piezo, x_hexa):
        yield from bps.mv(waxs, 15)
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(stage.y, ys)
        yield from bps.mv(stage.z, zs)

        yield from alignement_gisaxs_hex(0.15)
        ai0_cold = stage.th.position
        ypos_cold = stage.y.position
        ai0_list_cold.append(ai0_cold)
        y0_list_cold.append(ypos_cold)
        print(f'{name} position is th={ai0_cold},y={ypos_cold}')
        print(f'ai0 list is {ai0_list_cold} and y list is {y0_list_cold}')
    for i, cold_align in enumerate(ai0_list_cold):
        if abs(ai0_list_cold[i] - ai0_list[i]) > 0.03:
            raise ValueError(f'ai0 alignment at cold T ({ai0_list_cold}) was way far off initial alignment ({ai0_list})')
        if abs(y0_list_cold[i] - y0_list[i]) > 0.035:
            raise ValueError(f'y alignment at cold T ({y0_list_cold}) was way far off initial alignment ({y0_list})')

    ### move waxs arc back in for waxs
    yield from bps.mv(waxs, 10)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 6)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 5)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 4)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 3)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 2.5)
    
    for T in T_array:

        LThermal.setTemperature(T)
        LThermal.on()
        yield from bps.sleep(60*LThermal.ramptime.get()) 
        wait_counter=0
        while(abs(LThermal.temperature()-T)>1):
            yield from bps.sleep(10)
            wait_counter+=1
            if wait_counter>5*6:
                raise TimeoutError("Linkam is not getting to temperature!")
            
        ### at a temp, do a quick T hold
        yield from bps.sleep(150)

        ## measure the waxs for each sample 
        for name, ys, zs, xs_hexa, ai0 in zip(names, y0_list, z_piezo, x_hexa, ai0_list):
            yield from bps.mv(waxs, 2.5)
            yield from bps.mv(stage.x, xs_hexa)
            yield from bps.mv(stage.y, ys)
            yield from bps.mv(stage.z, zs)

                
            for k, ais in enumerate(ai_list):
                yield from bps.mv(stage.th, ai0 + ais)

                name_fmt = "{sample}_{temp}C_ai{ai}_wa{wax}_bpm{xbpm}"
            
                bpm = xbpm2.sumX.get()
                sample_name = name_fmt.format(sample=name, ai="%3.2f"%ais, wax=0, xbpm="%4.3f"%bpm, temp = "%3.2f"%T)
                sample_id(user_name="NS", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)   

def GIWAXS_TD_run4():
    T_start = 20
    T_array = [-70,-50,25]
    names = ['PS12',       'PS2',     'PS13',       'PS14']
    
    x_hexa = [3 ,     -1.5,           -6.5, -11]
    y_piezo = [0.3,       0.3,    0.3, 0.3] ### piezo here is just the name, it is actually moving hexa. don't mess with the piezo
    z_piezo =  [3,3,3,3]

    assert len(x_hexa) == len(y_piezo), f"Number of X coordinates ({len(x_hexa)}) is different from number of y positions ({len(y_piezo)})"
    assert len(x_hexa) == len(z_piezo), f"Number of X coordinates ({len(x_hexa)}) is different from number of z positions ({len(z_piezo)})"
    assert len(x_hexa) == len(names), f"Number of X coordinates ({len(x_hexa)}) is different from number of z positions ({len(names)})"

    ai0_list = [0.278, -0.078, 0.34600000000000003, 0.358]
    y0_list = [0.278, -0.078, 0.34600000000000003, 0.358]
    ai0_list_cold = []
    y0_list_cold = []
    ai_list = [0.05,0.08, 0.1, 0.12, 0.15, 0.2,0.25,0.3]
    dets = [pil900KW]
    yield from bps.mv(LThermal.lnp_mode_set,'Auto')
    LThermal.setTemperatureRate(20)

    # # Move to first temperature
    # LThermal.setTemperature(T_start)
    # LThermal.on()
    # yield from bps.sleep(60*LThermal.ramptime.get()) 
    # wait_counter=0
    # while(abs(LThermal.temperature()-T_start)>1):
    #     yield from bps.sleep(10)
    #     wait_counter+=1
    #     if wait_counter>5*6:
    #         raise TimeoutError("Linkam is not getting to temperature!")
    #     ## 


    # ### align the samples first before cooling
    # for name, ys, zs, xs_hexa in zip(names, y_piezo, z_piezo, x_hexa):
    #     yield from bps.mv(waxs, 15)
    #     yield from bps.mv(stage.x, xs_hexa)
    #     yield from bps.mv(stage.y, ys)
    #     yield from bps.mv(stage.z, zs)

    #     yield from alignement_gisaxs_hex(0.15)
    #     ai0 = stage.th.position
    #     ypos = stage.y.position
    #     ai0_list.append(ai0)
    #     y0_list.append(ypos)
    #     print(f'{name} position is th={ai0},y={ypos}')
    #     print(f'ai0 list is {ai0_list} and y list is {y0_list}')
    
    # ### move waxs arc back in for waxs
    # yield from bps.mv(waxs, 10)
    # yield from bps.sleep(1)
    # yield from bps.mv(waxs, 6)
    # yield from bps.sleep(1)
    # yield from bps.mv(waxs, 5)
    # yield from bps.sleep(1)
    # yield from bps.mv(waxs, 4)
    # yield from bps.sleep(1)
    # yield from bps.mv(waxs, 3)
    # yield from bps.sleep(1)
    # yield from bps.mv(waxs, 2.5)


    # # measure the first temperature waxs
    # for name, ys, zs, xs_hexa, ai0 in zip(names, y0_list, z_piezo, x_hexa, ai0_list):
    #     yield from bps.mv(waxs, 2.5)
    #     yield from bps.mv(stage.x, xs_hexa)
    #     yield from bps.mv(stage.y, ys)
    #     yield from bps.mv(stage.z, zs)
            
    #     for k, ais in enumerate(ai_list):
    #         yield from bps.mv(stage.th, ai0 + ais)

    #         name_fmt = "{sample}_{temp}C_ai{ai}_wa{wax}_bpm{xbpm}"
        
    #         bpm = xbpm2.sumX.get()
    #         sample_name = name_fmt.format(sample=name, ai="%3.2f"%ais, wax=0, xbpm="%4.3f"%bpm,temp = "%3.2f"%T_start)
    #         sample_id(user_name="NS", sample_name=sample_name)
    #         print(f"\n\t=== Sample: {sample_name} ===\n")
    #         yield from bp.count(dets, num=1)    

    # # Move to first cold temperature
    # LThermal.setTemperature(T_array[0])
    # LThermal.on()
    # yield from bps.sleep(60*LThermal.ramptime.get()) 
    # wait_counter=0
    # while(abs(LThermal.temperature()-T_array[0])>1):
    #     yield from bps.sleep(10)
    #     wait_counter+=1
    #     if wait_counter>5*6:
    #         raise TimeoutError("Linkam is not getting to temperature!")
    #     ## 

    # # check alignment again at first temperature
    # for name, ys, zs, xs_hexa in zip(names, y0_list, z_piezo, x_hexa):
    #     yield from bps.mv(waxs, 15)
    #     yield from bps.mv(stage.x, xs_hexa)
    #     yield from bps.mv(stage.y, ys)
    #     yield from bps.mv(stage.z, zs)

    #     yield from alignement_gisaxs_hex(0.15)
    #     ai0_cold = stage.th.position
    #     ypos_cold = stage.y.position
    #     ai0_list_cold.append(ai0_cold)
    #     y0_list_cold.append(ypos_cold)
    #     print(f'{name} position is th={ai0_cold},y={ypos_cold}')
    #     print(f'ai0 list is {ai0_list_cold} and y list is {y0_list_cold}')
    # for i, cold_align in enumerate(ai0_list_cold):
    #     if abs(ai0_list_cold[i] - ai0_list[i]) > 0.03:
    #         raise ValueError(f'ai0 alignment at cold T ({ai0_list_cold}) was way far off initial alignment ({ai0_list})')
    #     if abs(y0_list_cold[i] - y0_list[i]) > 0.035:
    #         raise ValueError(f'y alignment at cold T ({y0_list_cold}) was way far off initial alignment ({y0_list})')

    # ### move waxs arc back in for waxs
    # yield from bps.mv(waxs, 10)
    # yield from bps.sleep(1)
    # yield from bps.mv(waxs, 6)
    # yield from bps.sleep(1)
    # yield from bps.mv(waxs, 5)
    # yield from bps.sleep(1)
    # yield from bps.mv(waxs, 4)
    # yield from bps.sleep(1)
    # yield from bps.mv(waxs, 3)
    # yield from bps.sleep(1)
    # yield from bps.mv(waxs, 2.5)
    
    for T in T_array:

        LThermal.setTemperature(T)
        LThermal.on()
        yield from bps.sleep(60*LThermal.ramptime.get()) 
        wait_counter=0
        while(abs(LThermal.temperature()-T)>1):
            yield from bps.sleep(10)
            wait_counter+=1
            if wait_counter>5*6:
                raise TimeoutError("Linkam is not getting to temperature!")
            
        ### at a temp, do a quick T hold
        yield from bps.sleep(150)

        ## measure the waxs for each sample 
        for name, ys, zs, xs_hexa, ai0 in zip(names, y0_list, z_piezo, x_hexa, ai0_list):
            yield from bps.mv(waxs, 2.5)
            yield from bps.mv(stage.x, xs_hexa)
            yield from bps.mv(stage.y, ys)
            yield from bps.mv(stage.z, zs)

            RE.md['alignment results']={'ai0':ai0,'y0':ys}
            for k, ais in enumerate(ai_list):
                yield from bps.mv(stage.th, ai0 + ais)
                
                name_fmt = "{sample}_{temp}C_ai{ai}_wa{wax}_bpm{xbpm}"
            
                bpm = xbpm2.sumX.get()
                sample_name = name_fmt.format(sample=name, ai="%3.2f"%ais, wax=0, xbpm="%4.3f"%bpm, temp = "%3.2f"%T)
                sample_id(user_name="NS", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)   


def GIWAXS_TD_run5():
    T_start = 20
    T_array = [-70,-50,25]
    names = ['PS16',       'PS23',     'PS24',       'PS25']
    
    x_hexa = [3 ,     -1.5,           -6.5, -10.5]
    y_piezo = [0.3,       0.3,    0.3, 0.3] ### piezo here is just the name, it is actually moving hexa. don't mess with the piezo
    z_piezo =  [3,3,3,3]

    assert len(x_hexa) == len(y_piezo), f"Number of X coordinates ({len(x_hexa)}) is different from number of y positions ({len(y_piezo)})"
    assert len(x_hexa) == len(z_piezo), f"Number of X coordinates ({len(x_hexa)}) is different from number of z positions ({len(z_piezo)})"
    assert len(x_hexa) == len(names), f"Number of X coordinates ({len(x_hexa)}) is different from number of z positions ({len(names)})"

    ai0_list = []
    y0_list = []
    ai0_list_cold = []
    y0_list_cold = []
    ai_list = [0.05,0.08, 0.1, 0.12, 0.15, 0.2,0.25,0.3]
    dets = [pil900KW]
    yield from bps.mv(LThermal.lnp_mode_set,'Auto')
    LThermal.setTemperatureRate(20)

    # Move to first temperature
    LThermal.setTemperature(T_start)
    LThermal.on()
    yield from bps.sleep(60*LThermal.ramptime.get()) 
    wait_counter=0
    while(abs(LThermal.temperature()-T_start)>1):
        yield from bps.sleep(10)
        wait_counter+=1
        if wait_counter>5*6:
            raise TimeoutError("Linkam is not getting to temperature!")
        ## 


    ### align the samples first before cooling
    for name, ys, zs, xs_hexa in zip(names, y_piezo, z_piezo, x_hexa):
        yield from bps.mv(waxs, 15)
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(stage.y, ys)
        yield from bps.mv(stage.z, zs)

        yield from alignement_gisaxs_hex(0.15)
        ai0 = stage.th.position
        ypos = stage.y.position
        ai0_list.append(ai0)
        y0_list.append(ypos)
        print(f'{name} position is th={ai0},y={ypos}')
        print(f'ai0 list is {ai0_list} and y list is {y0_list}')
    
    ### move waxs arc back in for waxs
    yield from bps.mv(waxs, 10)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 6)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 5)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 4)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 3)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 2.5)


    # measure the first temperature waxs
    for name, ys, zs, xs_hexa, ai0 in zip(names, y0_list, z_piezo, x_hexa, ai0_list):
        yield from bps.mv(waxs, 2.5)
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(stage.y, ys)
        yield from bps.mv(stage.z, zs)
            
        for k, ais in enumerate(ai_list):
            yield from bps.mv(stage.th, ai0 + ais)

            name_fmt = "{sample}_{temp}C_ai{ai}_wa{wax}_bpm{xbpm}"
        
            bpm = xbpm2.sumX.get()
            sample_name = name_fmt.format(sample=name, ai="%3.2f"%ais, wax=0, xbpm="%4.3f"%bpm,temp = "%3.2f"%T_start)
            sample_id(user_name="NS", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)    

    # Move to first cold temperature
    LThermal.setTemperature(T_array[0])
    LThermal.on()
    yield from bps.sleep(60*LThermal.ramptime.get()) 
    wait_counter=0
    while(abs(LThermal.temperature()-T_array[0])>1):
        yield from bps.sleep(10)
        wait_counter+=1
        if wait_counter>5*6:
            raise TimeoutError("Linkam is not getting to temperature!")
        ## 

    # check alignment again at first temperature
    for name, ys, zs, xs_hexa in zip(names, y0_list, z_piezo, x_hexa):
        yield from bps.mv(waxs, 15)
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(stage.y, ys)
        yield from bps.mv(stage.z, zs)

        yield from alignement_gisaxs_hex(0.15)
        ai0_cold = stage.th.position
        ypos_cold = stage.y.position
        ai0_list_cold.append(ai0_cold)
        y0_list_cold.append(ypos_cold)
        print(f'{name} position is th={ai0_cold},y={ypos_cold}')
        print(f'ai0 cold list is {ai0_list_cold} and y cold list is {y0_list_cold}')
    print(f'ai0 list is {ai0_list} and y cold is {y0_list}')
    for i, cold_align in enumerate(ai0_list_cold):
        if abs(ai0_list_cold[i] - ai0_list[i]) > 0.03:
            raise ValueError(f'ai0 alignment at cold T ({ai0_list_cold}) was way far off initial alignment ({ai0_list})')
        if abs(y0_list_cold[i] - y0_list[i]) > 0.035:
            raise ValueError(f'y alignment at cold T ({y0_list_cold}) was way far off initial alignment ({y0_list})')

    ### move waxs arc back in for waxs
    yield from bps.mv(waxs, 10)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 6)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 5)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 4)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 3)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 2.5)
    
    for T in T_array:

        LThermal.setTemperature(T)
        LThermal.on()
        yield from bps.sleep(60*LThermal.ramptime.get()) 
        wait_counter=0
        while(abs(LThermal.temperature()-T)>1):
            yield from bps.sleep(10)
            wait_counter+=1
            if wait_counter>5*6:
                raise TimeoutError("Linkam is not getting to temperature!")
            
        ### at a temp, do a quick T hold
        yield from bps.sleep(150)

        ## measure the waxs for each sample 
        for name, ys, zs, xs_hexa, ai0 in zip(names, y0_list, z_piezo, x_hexa, ai0_list):
            yield from bps.mv(waxs, 2.5)
            yield from bps.mv(stage.x, xs_hexa)
            yield from bps.mv(stage.y, ys)
            yield from bps.mv(stage.z, zs)

                
            for k, ais in enumerate(ai_list):
                yield from bps.mv(stage.th, ai0 + ais)

                name_fmt = "{sample}_{temp}C_ai{ai}_wa{wax}_bpm{xbpm}"
            
                bpm = xbpm2.sumX.get()
                sample_name = name_fmt.format(sample=name, ai="%3.2f"%ais, wax=0, xbpm="%4.3f"%bpm, temp = "%3.2f"%T)
                sample_id(user_name="NS", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)  
    #ai0 cold list is [0.387, 0.304, 0.253, 0.022] and y cold list is [0.254, 0.292, 0.318, 0.317]
    #ai0 list is [0.402, 0.307, 0.246, 0.005] and y cold is [0.244, 0.272, 0.302, 0.308]

def GIWAXS_TD_run6():
    T_start = 25
    T_array = [-50,0,35,80,35,0,-50,25]
    names = ['IL2',       'IL4',     'IL11',       'IL12']
    
    x_hexa = [-9 ,     -6.5,           -3.5, 0]
    y_piezo = [0.3,       0.3,    0.3, 0.3] ### piezo here is just the name, it is actually moving hexa. don't mess with the piezo
    z_piezo =  [3,3,3,3]

    assert len(x_hexa) == len(y_piezo), f"Number of X coordinates ({len(x_hexa)}) is different from number of y positions ({len(y_piezo)})"
    assert len(x_hexa) == len(z_piezo), f"Number of X coordinates ({len(x_hexa)}) is different from number of z positions ({len(z_piezo)})"
    assert len(x_hexa) == len(names), f"Number of X coordinates ({len(x_hexa)}) is different from number of z positions ({len(names)})"

    ai0_list = []
    y0_list = []
    ai0_list_cold = []
    y0_list_cold = []
    ai_list = [0.05,0.08, 0.1, 0.12, 0.15, 0.2,0.25,0.3]
    dets = [pil900KW]
    yield from bps.mv(LThermal.lnp_mode_set,'Auto')
    LThermal.setTemperatureRate(20)

    # Move to first temperature
    LThermal.setTemperature(T_start)
    LThermal.on()
    yield from bps.sleep(60*LThermal.ramptime.get()) 
    wait_counter=0
    while(abs(LThermal.temperature()-T_start)>1):
        yield from bps.sleep(10)
        wait_counter+=1
        if wait_counter>5*6:
            raise TimeoutError("Linkam is not getting to temperature!")
        ## 


    ### align the samples first before cooling
    for name, ys, zs, xs_hexa in zip(names, y_piezo, z_piezo, x_hexa):
        yield from bps.mv(waxs, 15)
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(stage.y, ys)
        yield from bps.mv(stage.z, zs)

        yield from alignement_gisaxs_hex(0.15)
        ai0 = stage.th.position
        ypos = stage.y.position
        ai0_list.append(ai0)
        y0_list.append(ypos)
        print(f'{name} position is th={ai0},y={ypos}')
        print(f'ai0 list is {ai0_list} and y list is {y0_list}')
    
    ### move waxs arc back in for waxs
    yield from bps.mv(waxs, 10)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 6)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 5)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 4)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 3)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 2.5)


    # measure the first temperature waxs
    for name, ys, zs, xs_hexa, ai0 in zip(names, y0_list, z_piezo, x_hexa, ai0_list):
        yield from bps.mv(waxs, 2.5)
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(stage.y, ys)
        yield from bps.mv(stage.z, zs)
            
        for k, ais in enumerate(ai_list):
            yield from bps.mv(stage.th, ai0 + ais)

            name_fmt = "{sample}_{temp}C_ai{ai}_wa{wax}_bpm{xbpm}"
        
            bpm = xbpm2.sumX.get()
            sample_name = name_fmt.format(sample=name, ai="%3.2f"%ais, wax=0, xbpm="%4.3f"%bpm,temp = "%3.2f"%T_start)
            sample_id(user_name="NS", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)    

    # Move to first cold temperature
    LThermal.setTemperature(T_array[0])
    LThermal.on()
    yield from bps.sleep(60*LThermal.ramptime.get()) 
    wait_counter=0
    while(abs(LThermal.temperature()-T_array[0])>1):
        yield from bps.sleep(10)
        wait_counter+=1
        if wait_counter>5*6:
            raise TimeoutError("Linkam is not getting to temperature!")
        ## 

    # check alignment again at first temperature
    for name, ys, zs, xs_hexa in zip(names, y0_list, z_piezo, x_hexa):
        yield from bps.mv(waxs, 15)
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(stage.y, ys)
        yield from bps.mv(stage.z, zs)

        yield from alignement_gisaxs_hex(0.15)
        ai0_cold = stage.th.position
        ypos_cold = stage.y.position
        ai0_list_cold.append(ai0_cold)
        y0_list_cold.append(ypos_cold)
        print(f'{name} position is th={ai0_cold},y={ypos_cold}')
        print(f'ai0 cold list is {ai0_list_cold} and y cold list is {y0_list_cold}')
    print(f'ai0 list is {ai0_list} and y cold is {y0_list}')
    for i, cold_align in enumerate(ai0_list_cold):
        if abs(ai0_list_cold[i] - ai0_list[i]) > 0.03:
            raise ValueError(f'ai0 alignment at cold T ({ai0_list_cold}) was way far off initial alignment ({ai0_list})')
        if abs(y0_list_cold[i] - y0_list[i]) > 0.035:
            raise ValueError(f'y alignment at cold T ({y0_list_cold}) was way far off initial alignment ({y0_list})')

    ### move waxs arc back in for waxs
    yield from bps.mv(waxs, 10)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 6)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 5)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 4)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 3)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 2.5)
    
    for T in T_array:

        LThermal.setTemperature(T)
        LThermal.on()
        yield from bps.sleep(60*LThermal.ramptime.get()) 
        wait_counter=0
        while(abs(LThermal.temperature()-T)>1):
            yield from bps.sleep(10)
            wait_counter+=1
            if wait_counter>5*6:
                raise TimeoutError("Linkam is not getting to temperature!")
            
        ### at a temp, do a quick T hold
        yield from bps.sleep(150)

        ## measure the waxs for each sample 
        for name, ys, zs, xs_hexa, ai0 in zip(names, y0_list, z_piezo, x_hexa, ai0_list):
            yield from bps.mv(waxs, 2.5)
            yield from bps.mv(stage.x, xs_hexa)
            yield from bps.mv(stage.y, ys)
            yield from bps.mv(stage.z, zs)

                
            for k, ais in enumerate(ai_list):
                yield from bps.mv(stage.th, ai0 + ais)

                name_fmt = "{sample}_{temp}C_ai{ai}_wa{wax}_bpm{xbpm}"
            
                bpm = xbpm2.sumX.get()
                sample_name = name_fmt.format(sample=name, ai="%3.2f"%ais, wax=0, xbpm="%4.3f"%bpm, temp = "%3.2f"%T)
                sample_id(user_name="NS", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)  

def GIWAXS_TD_run7():
    T_start = 25
    T_array = [-70,-50,35,80,35,-50,-70,25]
    names = ['IL13',       'IL1',     'IL6']
    
    x_hexa = [3,     -3,           -9]
    y_piezo = [0.3,       0.3,    0.3] ### piezo here is just the name, it is actually moving hexa. don't mess with the piezo
    z_piezo =  [3,3,3]

    assert len(x_hexa) == len(y_piezo), f"Number of X coordinates ({len(x_hexa)}) is different from number of y positions ({len(y_piezo)})"
    assert len(x_hexa) == len(z_piezo), f"Number of X coordinates ({len(x_hexa)}) is different from number of z positions ({len(z_piezo)})"
    assert len(x_hexa) == len(names), f"Number of X coordinates ({len(x_hexa)}) is different from number of z positions ({len(names)})"

    ai0_list = []
    y0_list = []
    ai0_list_cold = []
    y0_list_cold = []
    ai_list = [0.05,0.08, 0.1, 0.12, 0.15, 0.2,0.25,0.3]
    dets = [pil900KW]
    yield from bps.mv(LThermal.lnp_mode_set,'Auto')
    LThermal.setTemperatureRate(20)

    # Move to first temperature
    LThermal.setTemperature(T_start)
    LThermal.on()
    yield from bps.sleep(60*LThermal.ramptime.get()) 
    wait_counter=0
    while(abs(LThermal.temperature()-T_start)>1):
        yield from bps.sleep(10)
        wait_counter+=1
        if wait_counter>5*6:
            raise TimeoutError("Linkam is not getting to temperature!")
        ## 


    ### align the samples first before cooling
    for name, ys, zs, xs_hexa in zip(names, y_piezo, z_piezo, x_hexa):
        yield from bps.mv(waxs, 15)
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(stage.y, ys)
        yield from bps.mv(stage.z, zs)

        yield from alignement_gisaxs_hex(0.15)
        ai0 = stage.th.position
        ypos = stage.y.position
        ai0_list.append(ai0)
        y0_list.append(ypos)
        print(f'{name} position is th={ai0},y={ypos}')
        print(f'ai0 list is {ai0_list} and y list is {y0_list}')
    
    ### move waxs arc back in for waxs
    yield from bps.mv(waxs, 10)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 6)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 5)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 4)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 3)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 2.5)


    # measure the first temperature waxs
    for name, ys, zs, xs_hexa, ai0 in zip(names, y0_list, z_piezo, x_hexa, ai0_list):
        yield from bps.mv(waxs, 2.5)
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(stage.y, ys)
        yield from bps.mv(stage.z, zs)
            
        for k, ais in enumerate(ai_list):
            yield from bps.mv(stage.th, ai0 + ais)

            name_fmt = "{sample}_{temp}C_ai{ai}_wa{wax}_bpm{xbpm}"
        
            bpm = xbpm2.sumX.get()
            sample_name = name_fmt.format(sample=name, ai="%3.2f"%ais, wax=0, xbpm="%4.3f"%bpm,temp = "%3.2f"%T_start)
            sample_id(user_name="NS", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)    

    # Move to first cold temperature
    LThermal.setTemperature(T_array[0])
    LThermal.on()
    yield from bps.sleep(60*LThermal.ramptime.get()) 
    wait_counter=0
    while(abs(LThermal.temperature()-T_array[0])>1):
        yield from bps.sleep(10)
        wait_counter+=1
        if wait_counter>5*6:
            raise TimeoutError("Linkam is not getting to temperature!")
        ## 

    # check alignment again at first temperature
    for name, ys, zs, xs_hexa in zip(names, y0_list, z_piezo, x_hexa):
        yield from bps.mv(waxs, 15)
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(stage.y, ys)
        yield from bps.mv(stage.z, zs)

        yield from alignement_gisaxs_hex(0.15)
        ai0_cold = stage.th.position
        ypos_cold = stage.y.position
        ai0_list_cold.append(ai0_cold)
        y0_list_cold.append(ypos_cold)
        print(f'{name} position is th={ai0_cold},y={ypos_cold}')
        print(f'ai0 cold list is {ai0_list_cold} and y cold list is {y0_list_cold}')
    print(f'ai0 list is {ai0_list} and y cold is {y0_list}')
    for i, cold_align in enumerate(ai0_list_cold):
        if abs(ai0_list_cold[i] - ai0_list[i]) > 0.03:
            raise ValueError(f'ai0 alignment at cold T ({ai0_list_cold}) was way far off initial alignment ({ai0_list})')
        if abs(y0_list_cold[i] - y0_list[i]) > 0.035:
            raise ValueError(f'y alignment at cold T ({y0_list_cold}) was way far off initial alignment ({y0_list})')

    ### move waxs arc back in for waxs
    yield from bps.mv(waxs, 10)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 6)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 5)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 4)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 3)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 2.5)
    
    for T in T_array:

        LThermal.setTemperature(T)
        LThermal.on()
        yield from bps.sleep(60*LThermal.ramptime.get()) 
        wait_counter=0
        while(abs(LThermal.temperature()-T)>1):
            yield from bps.sleep(10)
            wait_counter+=1
            if wait_counter>5*6:
                raise TimeoutError("Linkam is not getting to temperature!")
            
        ### at a temp, do a quick T hold
        yield from bps.sleep(150)

        ## measure the waxs for each sample 
        for name, ys, zs, xs_hexa, ai0 in zip(names, y0_list, z_piezo, x_hexa, ai0_list):
            yield from bps.mv(waxs, 2.5)
            yield from bps.mv(stage.x, xs_hexa)
            yield from bps.mv(stage.y, ys)
            yield from bps.mv(stage.z, zs)

                
            for k, ais in enumerate(ai_list):
                yield from bps.mv(stage.th, ai0 + ais)

                name_fmt = "{sample}_{temp}C_ai{ai}_wa{wax}_bpm{xbpm}"
            
                bpm = xbpm2.sumX.get()
                sample_name = name_fmt.format(sample=name, ai="%3.2f"%ais, wax=0, xbpm="%4.3f"%bpm, temp = "%3.2f"%T)
                sample_id(user_name="NS", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)  

def GIWAXS_TD_run8():
    T_start = 25
    T_array = [-70,25,35,80,35,-70,25]
    names = ['IL8',       'IL10',     'PS26']
    
    x_hexa = [1,     -5,           -9.5]
    y_piezo = [0.3,       0.3,    0.3] ### piezo here is just the name, it is actually moving hexa. don't mess with the piezo
    z_piezo =  [3,3,3]

    assert len(x_hexa) == len(y_piezo), f"Number of X coordinates ({len(x_hexa)}) is different from number of y positions ({len(y_piezo)})"
    assert len(x_hexa) == len(z_piezo), f"Number of X coordinates ({len(x_hexa)}) is different from number of z positions ({len(z_piezo)})"
    assert len(x_hexa) == len(names), f"Number of X coordinates ({len(x_hexa)}) is different from number of z positions ({len(names)})"

    ai0_list = []
    y0_list = []
    ai0_list_cold = []
    y0_list_cold = []
    ai_list = [0.05,0.08, 0.1, 0.12, 0.15, 0.2,0.25,0.3]
    dets = [pil900KW]
    yield from bps.mv(LThermal.lnp_mode_set,'Auto')
    LThermal.setTemperatureRate(20)

    # Move to first temperature
    LThermal.setTemperature(T_start)
    LThermal.on()
    yield from bps.sleep(60*LThermal.ramptime.get()) 
    wait_counter=0
    while(abs(LThermal.temperature()-T_start)>1):
        yield from bps.sleep(10)
        wait_counter+=1
        if wait_counter>5*6:
            raise TimeoutError("Linkam is not getting to temperature!")
        ## 


    ### align the samples first before cooling
    for name, ys, zs, xs_hexa in zip(names, y_piezo, z_piezo, x_hexa):
        yield from bps.mv(waxs, 15)
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(stage.y, ys)
        yield from bps.mv(stage.z, zs)

        yield from alignement_gisaxs_hex(0.15)
        ai0 = stage.th.position
        ypos = stage.y.position
        ai0_list.append(ai0)
        y0_list.append(ypos)
        print(f'{name} position is th={ai0},y={ypos}')
        print(f'ai0 list is {ai0_list} and y list is {y0_list}')
    
    ### move waxs arc back in for waxs
    yield from bps.mv(waxs, 10)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 6)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 5)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 4)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 3)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 2.5)


    # measure the first temperature waxs
    for name, ys, zs, xs_hexa, ai0 in zip(names, y0_list, z_piezo, x_hexa, ai0_list):
        yield from bps.mv(waxs, 2.5)
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(stage.y, ys)
        yield from bps.mv(stage.z, zs)
            
        for k, ais in enumerate(ai_list):
            yield from bps.mv(stage.th, ai0 + ais)

            name_fmt = "{sample}_{temp}C_ai{ai}_wa{wax}_bpm{xbpm}"
        
            bpm = xbpm2.sumX.get()
            sample_name = name_fmt.format(sample=name, ai="%3.2f"%ais, wax=0, xbpm="%4.3f"%bpm,temp = "%3.2f"%T_start)
            sample_id(user_name="NS", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)    

    # Move to first cold temperature
    LThermal.setTemperature(T_array[0])
    LThermal.on()
    yield from bps.sleep(60*LThermal.ramptime.get()) 
    wait_counter=0
    while(abs(LThermal.temperature()-T_array[0])>1):
        yield from bps.sleep(10)
        wait_counter+=1
        if wait_counter>5*6:
            raise TimeoutError("Linkam is not getting to temperature!")
        ## 

    # check alignment again at first temperature
    for name, ys, zs, xs_hexa in zip(names, y0_list, z_piezo, x_hexa):
        yield from bps.mv(waxs, 15)
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(stage.y, ys)
        yield from bps.mv(stage.z, zs)

        yield from alignement_gisaxs_hex(0.15)
        ai0_cold = stage.th.position
        ypos_cold = stage.y.position
        ai0_list_cold.append(ai0_cold)
        y0_list_cold.append(ypos_cold)
        print(f'{name} position is th={ai0_cold},y={ypos_cold}')
        print(f'ai0 cold list is {ai0_list_cold} and y cold list is {y0_list_cold}')
    print(f'ai0 list is {ai0_list} and y cold is {y0_list}')
    for i, cold_align in enumerate(ai0_list_cold):
        if abs(ai0_list_cold[i] - ai0_list[i]) > 0.03:
            raise ValueError(f'ai0 alignment at cold T ({ai0_list_cold}) was way far off initial alignment ({ai0_list})')
        if abs(y0_list_cold[i] - y0_list[i]) > 0.035:
            raise ValueError(f'y alignment at cold T ({y0_list_cold}) was way far off initial alignment ({y0_list})')

    ### move waxs arc back in for waxs
    yield from bps.mv(waxs, 10)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 6)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 5)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 4)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 3)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 2.5)
    
    for T in T_array:

        LThermal.setTemperature(T)
        LThermal.on()
        yield from bps.sleep(60*LThermal.ramptime.get()) 
        wait_counter=0
        while(abs(LThermal.temperature()-T)>1):
            yield from bps.sleep(10)
            wait_counter+=1
            if wait_counter>5*6:
                raise TimeoutError("Linkam is not getting to temperature!")
            
        ### at a temp, do a quick T hold
        yield from bps.sleep(150)

        ## measure the waxs for each sample 
        for name, ys, zs, xs_hexa, ai0 in zip(names, y0_list, z_piezo, x_hexa, ai0_list):
            yield from bps.mv(waxs, 2.5)
            yield from bps.mv(stage.x, xs_hexa)
            yield from bps.mv(stage.y, ys)
            yield from bps.mv(stage.z, zs)

                
            for k, ais in enumerate(ai_list):
                yield from bps.mv(stage.th, ai0 + ais)

                name_fmt = "{sample}_{temp}C_ai{ai}_wa{wax}_bpm{xbpm}"
            
                bpm = xbpm2.sumX.get()
                sample_name = name_fmt.format(sample=name, ai="%3.2f"%ais, wax=0, xbpm="%4.3f"%bpm, temp = "%3.2f"%T)
                sample_id(user_name="NS", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)  



def GIWAXS_TD_run9():
    T_start = 25
    T_array = [-70,25,35,80,35,-70,25]
    names = ['IL8',          'PS26']
    
    x_hexa = [1,            -9.5]
    y_piezo = [0.3,          0.3] ### piezo here is just the name, it is actually moving hexa. don't mess with the piezo
    z_piezo =  [3,3]

    assert len(x_hexa) == len(y_piezo), f"Number of X coordinates ({len(x_hexa)}) is different from number of y positions ({len(y_piezo)})"
    assert len(x_hexa) == len(z_piezo), f"Number of X coordinates ({len(x_hexa)}) is different from number of z positions ({len(z_piezo)})"
    assert len(x_hexa) == len(names), f"Number of X coordinates ({len(x_hexa)}) is different from number of z positions ({len(names)})"

    ai0_list = []
    y0_list = []
    ai0_list_cold = []
    y0_list_cold = []
    ai_list = [0.05,0.08, 0.1, 0.12, 0.15, 0.2,0.25,0.3]
    dets = [pil900KW]
    yield from bps.mv(LThermal.lnp_mode_set,'Auto')
    LThermal.setTemperatureRate(20)

    # Move to first temperature
    #LThermal.setTemperature(T_start)
    #LThermal.on()
    #yield from bps.sleep(60*LThermal.ramptime.get()) 
    #wait_counter=0
    #while(abs(LThermal.temperature()-T_start)>1):
        #yield from bps.sleep(10)
        #wait_counter+=1
        #if wait_counter>5*6:
          #  raise TimeoutError("Linkam is not getting to temperature!")
        ## 


    ### move waxs arc back in for waxs
    yield from bps.mv(waxs, 10)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 6)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 5)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 4)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 3)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 2.5)
    
    for T in T_array:

        LThermal.setTemperature(T)
        LThermal.on()
        yield from bps.sleep(60*LThermal.ramptime.get()) 
        wait_counter=0
        while(abs(LThermal.temperature()-T)>1):
            yield from bps.sleep(10)
            wait_counter+=1
            if wait_counter>5*6:
                raise TimeoutError("Linkam is not getting to temperature!")
            
        ### at a temp, do a quick T hold
        yield from bps.sleep(150)

        ## measure the waxs for each sample 
        for name, ys, zs, xs_hexa, ai0 in zip(names, y0_list, z_piezo, x_hexa, ai0_list):
            yield from bps.mv(waxs, 2.5)
            yield from bps.mv(stage.x, xs_hexa)
            yield from bps.mv(stage.y, ys)
            yield from bps.mv(stage.z, zs)

                
            for k, ais in enumerate(ai_list):
                yield from bps.mv(stage.th, ai0 + ais)

                name_fmt = "{sample}_{temp}C_ai{ai}_wa{wax}_bpm{xbpm}"
            
                bpm = xbpm2.sumX.get()
                sample_name = name_fmt.format(sample=name, ai="%3.2f"%ais, wax=0, xbpm="%4.3f"%bpm, temp = "%3.2f"%T)
                sample_id(user_name="NS", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)  




def GIWAXS_TD_run10():
    T_start = 25
    T_array = [-70,25,35,80,35,-70,25]
    names = ['IL8',            'PS26']
    
    x_hexa = [1,             -9.5]
    y_piezo = [0.3,         0.3] ### piezo here is just the name, it is actually moving hexa. don't mess with the piezo
    z_piezo =  [3,3]

    assert len(x_hexa) == len(y_piezo), f"Number of X coordinates ({len(x_hexa)}) is different from number of y positions ({len(y_piezo)})"
    assert len(x_hexa) == len(z_piezo), f"Number of X coordinates ({len(x_hexa)}) is different from number of z positions ({len(z_piezo)})"
    assert len(x_hexa) == len(names), f"Number of X coordinates ({len(x_hexa)}) is different from number of z positions ({len(names)})"

    ai0_list = []
    y0_list = []
    ai0_list_cold = []
    y0_list_cold = []
    ai_list = [0.05,0.08, 0.1, 0.12, 0.15, 0.2,0.25,0.3]
    dets = [pil900KW]
    yield from bps.mv(LThermal.lnp_mode_set,'Auto')
    LThermal.setTemperatureRate(20)

    # Move to first temperature
    LThermal.setTemperature(T_start)
    LThermal.on()
    yield from bps.sleep(60*LThermal.ramptime.get()) 
    wait_counter=0
    while(abs(LThermal.temperature()-T_start)>1):
        yield from bps.sleep(10)
        wait_counter+=1
        if wait_counter>5*6:
            raise TimeoutError("Linkam is not getting to temperature!")
        ## 


    ### align the samples first before cooling
    for name, ys, zs, xs_hexa in zip(names, y_piezo, z_piezo, x_hexa):
        yield from bps.mv(waxs, 15)
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(stage.y, ys)
        yield from bps.mv(stage.z, zs)

        yield from alignement_gisaxs_hex(0.15)
        ai0 = stage.th.position
        ypos = stage.y.position
        ai0_list.append(ai0)
        y0_list.append(ypos)
        print(f'{name} position is th={ai0},y={ypos}')
        print(f'ai0 list is {ai0_list} and y list is {y0_list}')
    
    ### move waxs arc back in for waxs
    yield from bps.mv(waxs, 10)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 6)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 5)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 4)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 3)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 2.5)


    # measure the first temperature waxs
    for name, ys, zs, xs_hexa, ai0 in zip(names, y0_list, z_piezo, x_hexa, ai0_list):
        yield from bps.mv(waxs, 2.5)
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(stage.y, ys)
        yield from bps.mv(stage.z, zs)
            
        for k, ais in enumerate(ai_list):
            yield from bps.mv(stage.th, ai0 + ais)

            name_fmt = "{sample}_{temp}C_ai{ai}_wa{wax}_bpm{xbpm}"
        
            bpm = xbpm2.sumX.get()
            sample_name = name_fmt.format(sample=name, ai="%3.2f"%ais, wax=0, xbpm="%4.3f"%bpm,temp = "%3.2f"%T_start)
            sample_id(user_name="NS", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)    

    # Move to first cold temperature
    LThermal.setTemperature(T_array[0])
    LThermal.on()
    yield from bps.sleep(60*LThermal.ramptime.get()) 
    wait_counter=0
    while(abs(LThermal.temperature()-T_array[0])>1):
        yield from bps.sleep(10)
        wait_counter+=1
        if wait_counter>5*6:
            raise TimeoutError("Linkam is not getting to temperature!")
        ## 

    # check alignment again at first temperature
    for name, ys, zs, xs_hexa in zip(names, y0_list, z_piezo, x_hexa):
        yield from bps.mv(waxs, 15)
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(stage.y, ys)
        yield from bps.mv(stage.z, zs)

        yield from alignement_gisaxs_hex(0.15)
        ai0_cold = stage.th.position
        ypos_cold = stage.y.position
        ai0_list_cold.append(ai0_cold)
        y0_list_cold.append(ypos_cold)
        print(f'{name} position is th={ai0_cold},y={ypos_cold}')
        print(f'ai0 cold list is {ai0_list_cold} and y cold list is {y0_list_cold}')
    print(f'ai0 list is {ai0_list} and y cold is {y0_list}')
    for i, cold_align in enumerate(ai0_list_cold):
        if abs(ai0_list_cold[i] - ai0_list[i]) > 0.03:
            raise ValueError(f'ai0 alignment at cold T ({ai0_list_cold}) was way far off initial alignment ({ai0_list})')
        if abs(y0_list_cold[i] - y0_list[i]) > 0.035:
            raise ValueError(f'y alignment at cold T ({y0_list_cold}) was way far off initial alignment ({y0_list})')

    ### move waxs arc back in for waxs
    yield from bps.mv(waxs, 10)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 6)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 5)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 4)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 3)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 2.5)
    
    for T in T_array:

        LThermal.setTemperature(T)
        LThermal.on()
        yield from bps.sleep(60*LThermal.ramptime.get()) 
        wait_counter=0
        while(abs(LThermal.temperature()-T)>1):
            yield from bps.sleep(10)
            wait_counter+=1
            if wait_counter>5*6:
                raise TimeoutError("Linkam is not getting to temperature!")
            
        ### at a temp, do a quick T hold
        yield from bps.sleep(150)

        ## measure the waxs for each sample 
        for name, ys, zs, xs_hexa, ai0 in zip(names, y0_list, z_piezo, x_hexa, ai0_list):
            yield from bps.mv(waxs, 2.5)
            yield from bps.mv(stage.x, xs_hexa)
            yield from bps.mv(stage.y, ys)
            yield from bps.mv(stage.z, zs)

                
            for k, ais in enumerate(ai_list):
                yield from bps.mv(stage.th, ai0 + ais)

                name_fmt = "{sample}_{temp}C_ai{ai}_wa{wax}_bpm{xbpm}"
            
                bpm = xbpm2.sumX.get()
                sample_name = name_fmt.format(sample=name, ai="%3.2f"%ais, wax=0, xbpm="%4.3f"%bpm, temp = "%3.2f"%T)
                sample_id(user_name="NS", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)  


def GIWAXS_TD_run11():
    T_start = 25
    T_array = [-70,25,35,80,35,-70,25]
    names = [      'IL10'    ]
    
    x_hexa = [     1.5]
    y_piezo = [    0.3] ### piezo here is just the name, it is actually moving hexa. don't mess with the piezo
    z_piezo =  [5]

    assert len(x_hexa) == len(y_piezo), f"Number of X coordinates ({len(x_hexa)}) is different from number of y positions ({len(y_piezo)})"
    assert len(x_hexa) == len(z_piezo), f"Number of X coordinates ({len(x_hexa)}) is different from number of z positions ({len(z_piezo)})"
    assert len(x_hexa) == len(names), f"Number of X coordinates ({len(x_hexa)}) is different from number of z positions ({len(names)})"

    ai0_list = []
    y0_list = []
    ai0_list_cold = []
    y0_list_cold = []
    ai_list = [0.05,0.08, 0.1, 0.12, 0.15, 0.2,0.25,0.3]
    dets = [pil900KW]
    yield from bps.mv(LThermal.lnp_mode_set,'Auto')
    LThermal.setTemperatureRate(20)

    # Move to first temperature
    LThermal.setTemperature(T_start)
    LThermal.on()
    yield from bps.sleep(60*LThermal.ramptime.get()) 
    wait_counter=0
    while(abs(LThermal.temperature()-T_start)>1):
        yield from bps.sleep(10)
        wait_counter+=1
        if wait_counter>5*6:
            raise TimeoutError("Linkam is not getting to temperature!")
        ## 


    ### align the samples first before cooling
    for name, ys, zs, xs_hexa in zip(names, y_piezo, z_piezo, x_hexa):
        yield from bps.mv(waxs, 15)
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(stage.y, ys)
        yield from bps.mv(stage.z, zs)

        yield from alignement_gisaxs_hex(0.15)
        ai0 = stage.th.position
        ypos = stage.y.position
        ai0_list.append(ai0)
        y0_list.append(ypos)
        print(f'{name} position is th={ai0},y={ypos}')
        print(f'ai0 list is {ai0_list} and y list is {y0_list}')
    
    ### move waxs arc back in for waxs
    yield from bps.mv(waxs, 10)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 6)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 5)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 4)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 3)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 2.5)


    # measure the first temperature waxs
    for name, ys, zs, xs_hexa, ai0 in zip(names, y0_list, z_piezo, x_hexa, ai0_list):
        yield from bps.mv(waxs, 2.5)
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(stage.y, ys)
        yield from bps.mv(stage.z, zs)
            
        for k, ais in enumerate(ai_list):
            yield from bps.mv(stage.th, ai0 + ais)

            name_fmt = "{sample}_{temp}C_ai{ai}_wa{wax}_bpm{xbpm}"
        
            bpm = xbpm2.sumX.get()
            sample_name = name_fmt.format(sample=name, ai="%3.2f"%ais, wax=0, xbpm="%4.3f"%bpm,temp = "%3.2f"%T_start)
            sample_id(user_name="NS", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)    

    # Move to first cold temperature
    LThermal.setTemperature(T_array[0])
    LThermal.on()
    yield from bps.sleep(60*LThermal.ramptime.get()) 
    wait_counter=0
    while(abs(LThermal.temperature()-T_array[0])>1):
        yield from bps.sleep(10)
        wait_counter+=1
        if wait_counter>5*6:
            raise TimeoutError("Linkam is not getting to temperature!")
        ## 

    # check alignment again at first temperature
    for name, ys, zs, xs_hexa in zip(names, y0_list, z_piezo, x_hexa):
        yield from bps.mv(waxs, 15)
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(stage.y, ys)
        yield from bps.mv(stage.z, zs)

        yield from alignement_gisaxs_hex(0.15)
        ai0_cold = stage.th.position
        ypos_cold = stage.y.position
        ai0_list_cold.append(ai0_cold)
        y0_list_cold.append(ypos_cold)
        print(f'{name} position is th={ai0_cold},y={ypos_cold}')
        print(f'ai0 cold list is {ai0_list_cold} and y cold list is {y0_list_cold}')
    print(f'ai0 list is {ai0_list} and y list is {y0_list}')
    for i, cold_align in enumerate(ai0_list_cold):
        if abs(ai0_list_cold[i] - ai0_list[i]) > 0.03:
            raise ValueError(f'ai0 alignment at cold T ({ai0_list_cold}) was way far off initial alignment ({ai0_list})')
        if abs(y0_list_cold[i] - y0_list[i]) > 0.035:
            raise ValueError(f'y alignment at cold T ({y0_list_cold}) was way far off initial alignment ({y0_list})')

    ### move waxs arc back in for waxs
    yield from bps.mv(waxs, 10)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 6)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 5)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 4)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 3)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 2.5)
    
    for T in T_array:

        LThermal.setTemperature(T)
        LThermal.on()
        yield from bps.sleep(60*LThermal.ramptime.get()) 
        wait_counter=0
        while(abs(LThermal.temperature()-T)>1):
            yield from bps.sleep(10)
            wait_counter+=1
            if wait_counter>5*6:
                raise TimeoutError("Linkam is not getting to temperature!")
            
        ### at a temp, do a quick T hold
        yield from bps.sleep(150)

        ## measure the waxs for each sample 
        for name, ys, zs, xs_hexa, ai0 in zip(names, y0_list, z_piezo, x_hexa, ai0_list):
            yield from bps.mv(waxs, 2.5)
            yield from bps.mv(stage.x, xs_hexa)
            yield from bps.mv(stage.y, ys)
            yield from bps.mv(stage.z, zs)

                
            for k, ais in enumerate(ai_list):
                yield from bps.mv(stage.th, ai0 + ais)

                name_fmt = "{sample}_{temp}C_ai{ai}_wa{wax}_bpm{xbpm}"
            
                bpm = xbpm2.sumX.get()
                sample_name = name_fmt.format(sample=name, ai="%3.2f"%ais, wax=0, xbpm="%4.3f"%bpm, temp = "%3.2f"%T)
                sample_id(user_name="NS", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1) 



def GIWAXS_2024_vacuum_last4(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    # top of bar approx y=-3500, ai0=-.7, z=5200
    # bottom of bar approx y=5300, ai0=.3, z=1600
    names = ['PS8',   'PS9',   'PS10',     'PS19']
    
    x_hexa = [2.5,     -1.5,    -5.5,     -9]
    y_piezo = [0.3,     0.3] ### piezo here is just the name, it is actually moving hexa. don't mess with the piezo
    z_piezo =  [3,3]

    assert len(x_hexa) == len(y_piezo), f"Number of X coordinates ({len(x_hexa)}) is different from number of y positions ({len(y_piezo)})"
    assert len(x_hexa) == len(z_piezo), f"Number of X coordinates ({len(x_hexa)}) is different from number of z positions ({len(z_piezo)})"
    assert len(x_hexa) == len(names), f"Number of X coordinates ({len(x_hexa)}) is different from number of z positions ({len(names)})"

    waxs_arc = [15, 2.5] ### not needed anymore I think
    ai0_list = []
    y0_list = []
    ai_list = [0.08, 0.1, 0.12, 0.15, 0.2]


    

    for name, xs, ys, zs, xs_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa):
        yield from bps.mv(waxs, 20)
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)


        if ys <0 : 
            ai0_all = -0.7
        if ys > 0:
            ai0_all = 0.3
        yield from bps.mv(piezo.th, ai0_all)
        yield from alignement_gisaxs_doblestack(0.15)
        
        ai0 = piezo.th.position
        ypos = piezo.y.position
        ai0_list.append(ai0)
        y0_list.append(ypos)
        print(f'{name} position is th={ai0},y={ypos}')

        dets = [pil1M, pil900KW]

        det_exposure_time(t, t)
        poss = [1,2]
        for pos in poss:
            if pos == 2:
                yield from bps.mvr(stage.x, 1)
               
            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                name_fmt = "{sample}_pos{pos}_ai{ai}_wa{wax}_bpm{xbpm}"
            
                bpm = xbpm2.sumX.get()
                sample_name = name_fmt.format(sample=name, ai="%3.2f"%ais, wax=20, xbpm="%4.3f"%bpm, pos="%d"%pos)
                sample_id(user_name="NS", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)
        ### move back to pos 1
        yield from bps.mvr(stage.x, -1)
        # move the waxs detector back in slowly
        yield from bps.mv(waxs, 10)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 6)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 5)
        yield from bps.sleep(1)

        # while waxs.arc.position > 0:
        yield from bps.mv(waxs, 4)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 3)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 2)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 1)
        yield from bps.sleep(1)
        yield from bps.mv(waxs, 0)
        dets = [pil900KW]
        det_exposure_time(t, t)
        for pos in poss:
            if pos == 2:
                yield from bps.mvr(stage.x, 1)
            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                name_fmt = "{sample}_pos{pos}_ai{ai}_wa{wax}_bpm{xbpm}"
            
                bpm = xbpm2.sumX.get()
                sample_name = name_fmt.format(sample=name, ai="%3.2f"%ais, wax=0, xbpm="%4.3f"%bpm, pos="%d"%pos)
                sample_id(user_name="NS", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)


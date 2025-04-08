def run_capillaries_Alexandra_2023_3(ts=0.5, tl=5, waxs_only=False):
    """
    Standard SAXS, measure transmission only during the first run

    Use two exposures:
        ts (float): shorter exposure time for first measurement,
        tl (float): longer exposure time for second measurement.
    
    sample_id(user_name='test', sample_name='test')
    RE(count([pil900KW]))
    
    """
    # yield from bps.sleep(1500)
    names = ['NAP7_100mM_correct_more']
    # names = ['EC_H_DCM_10mgml_waxs']
    # piezo_x = [-25300]
    piezo_x = [-12500]
    #names = ['nap7_100mM_redone2_more']
    #piezo_x = [300]
    #names =   [  'EC_A_THF_10mgml_waxs','EC_B_THF_10mgml_waxs','EC_C_THF_10mgml_waxs','EC_D_THF_10mgml_waxs','EC_E_THF_10mgml_waxs','EC_F_THF_10mgml_waxs','EC_G_THF_10mgml_waxs','EC_H_THF_10mgml_waxs','EC_I_THF_10mgml_waxs','EC_A_DCM_10mgml_waxs','EC_B_DCM_10mgml_waxs','EC_C_DCM_10mgml_waxs','EC_D_DCM_10mgml_waxs','EC_E_DCM_10mgml_waxs','EC_F_DCM_10mgml_waxs']
    #names =   [ 'sample51_redone_more','sample52_redone_more','sample53_redone_more','sample54_redone_more','sample55_redone_more','sample56_redone_more','sample57_redone_more','sample58_redone_more','sample59_redone_more','sample60_redone_more','sample61_redone_more','sample62_redone_more','sample63_redone_more','sample64_redone_more','sample65_redone_more']
    #piezo_x = [-45100, -38700,-32300,-25800,-19600,-13000,-6000,-400,5700,12500,18600,24900, 31200,37200, 44000 ]   
    piezo_y = [      -3100 for n in names ]
    piezo_z = [ 5151 for n in names]

    assert len(names)   == len(piezo_x), f"Wrong list lenghts"
    assert len(piezo_x) == len(piezo_y), f"Wrong list lenghts"
    assert len(piezo_x) == len(piezo_z), f"Wrong list lenghts"

    waxs_arc = [20]
    
    y_off = [0, 100]
    user_name = 'AG'
    
    exposures = [ts, tl]
    
    dets = [pil900KW]  if waxs_only else [pil1M]
    waxs_arc = [0, 20] if waxs_only else [20]

    for name, x, y, z in zip(names, piezo_x, piezo_y, piezo_z):
        yield from bps.mv(piezo.x, x,
                          piezo.y, y,
                          piezo.z, z,
                          )

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)

            #dets = [pil900KW] if waxs.arc.position < 15 else [pil1M, pil900KW]

            # Read pin diode current
            if waxs.arc.position > 15:
                fs.open()
                yield from bps.sleep(0.3)
                pd_curr = pdcurrent1.value
                fs.close()
                pd = str(int(np.round(pd_curr, 0))).zfill(7)
            else:
                pd = 0
            
            for yy, y_of in enumerate(y_off):
                yield from bps.mv(piezo.y, y + y_of)

                for exp in exposures:
                    det_exposure_time(exp, exp)
                    yield from bps.sleep(2)

                    exp_save = str(int(np.round(exp, 0))).zfill(2)

                    sample_name = f'{name}_exp{exp_save}_loc{yy}_pd{pd}{get_scan_md()}'
                    sample_id(user_name=user_name, sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets)


    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)


def run_temp_capillaries_Alexandra_2023_3(ts=0.5, tl=1, waxs_only=False):
    """
    Standard SAXS with resistive heating stage,
    measure transmission only during the first run

    Use two exposures:
        ts (float): shorter exposure time for first measurement,
        tl (float): longer exposure time for second measurement.
    
    To engage WAXS if needed, in BlueSky
    sample_id(user_name='test', sample_name='test')
    RE(count([pil900KW]))
    
    """
    # yield from bps.sleep(1500)
    names = ['sample41_43C','sample42_43C','sample43_43C','sample44_43C','sample45_43C','sample46_43C']
    piezo_x = [6600, 12800,19400, 25600, 32000,38400]
    # names = ['sampleHY1_redone','sampleHY2_redone']
    #piezo_x = [-13100, -6800]
    #names =   [  'EC_A_THF_10mgml_waxs','EC_B_THF_10mgml_waxs','EC_C_THF_10mgml_waxs','EC_D_THF_10mgml_waxs','EC_E_THF_10mgml_waxs','EC_F_THF_10mgml_waxs','EC_G_THF_10mgml_waxs','EC_H_THF_10mgml_waxs','EC_I_THF_10mgml_waxs','EC_A_DCM_10mgml_waxs','EC_B_DCM_10mgml_waxs','EC_C_DCM_10mgml_waxs','EC_D_DCM_10mgml_waxs','EC_E_DCM_10mgml_waxs','EC_F_DCM_10mgml_waxs']
    #names =   [ 'sample51_redone_more','sample52_redone_more','sample53_redone_more','sample54_redone_more','sample55_redone_more','sample56_redone_more','sample57_redone_more','sample58_redone_more','sample59_redone_more','sample60_redone_more','sample61_redone_more','sample62_redone_more','sample63_redone_more','sample64_redone_more','sample65_redone_more']
    #piezo_x = [-45100, -38700,-32300,-25800,-19600,-13000,-6000,-400,5700,12500,18600,24900, 31200,37200, 44000 ]   
    piezo_y = [      -3000 for n in names ]
    piezo_z = [ 5151 for n in names]

    assert len(names)   == len(piezo_x), f"Wrong list lenghts"
    assert len(piezo_x) == len(piezo_y), f"Wrong list lenghts"
    assert len(piezo_x) == len(piezo_z), f"Wrong list lenghts"

    waxs_arc = [20]
    temperatures = [ 43 ]
    
    y_off = [0, 100]
    user_name = 'AG'
    
    exposures = [ts, tl]
    
    dets = [pil900KW]  if waxs_only else [pil1M]
    waxs_arc = [0, 20] if waxs_only else [20]

    for temperature in temperatures:
        t_kelvin = temperature + 273.15
        yield from ls.output1.mv_temp(t_kelvin)

        # Activate heating range in Lakeshore
        if temperature < 70:
            yield from bps.mv(ls.output1.status, 1)
        else:
            yield from bps.mv(ls.output1.status, 3)

        # Equalise temperature
        print(f"Equalising temperature to {temperature:.0f} deg C")
        start = time.time()
        temp = ls.input_A.get()
        while abs(temp - t_kelvin) > 5:
            print("Difference: {:.1f} K".format(abs(temp - t_kelvin)))
            yield from bps.sleep(10)
            temp = ls.input_A.get()
            
            # Escape the loop if too much time passes
            if time.time() - start > 15 * 60:
                temp = t_kelvin
        print(
            "Time needed to equilibrate: {:.1f} min".format((time.time() - start) / 60)
        )

        # Wait extra time depending on temperature
        if (56 < temperature) and (temperature < 160):
            yield from bps.sleep(300)
        elif 160 <= temperature:
            yield from bps.sleep(600)

        # Read T and convert to deg C
        temp_degC = ls.input_A.get() - 273.15
        temp = str(np.round(float(temp_degC), 1)).zfill(5)

        for name, x, y, z in zip(names, piezo_x, piezo_y, piezo_z):
            yield from bps.mv(piezo.x, x,
                              piezo.y, y,
                              piezo.z, z,
                             )

            for wa in waxs_arc:
                yield from bps.mv(waxs, wa)

                #dets = [pil900KW] if waxs.arc.position < 15 else [pil1M, pil900KW]

                # Read pin diode current
                if waxs.arc.position > 15:
                    fs.open()
                    yield from bps.sleep(0.3)
                    pd_curr = pdcurrent1.value
                    fs.close()
                    pd = str(int(np.round(pd_curr, 0))).zfill(7)
                else:
                    pd = 0
                
                for yy, y_of in enumerate(y_off):
                    yield from bps.mv(piezo.y, y + y_of)

                    for exp in exposures:
                        det_exposure_time(exp, exp)
                        yield from bps.sleep(2)

                        exp_save = str(int(np.round(exp, 0))).zfill(2)

                        sample_name = f'{name}_temp{temp}exp{exp_save}_loc{yy}_pd{pd}{get_scan_md()}'
                        sample_id(user_name=user_name, sample_name=sample_name)
                        print(f"\n\t=== Sample: {sample_name} ===\n")
                        yield from bp.count(dets)


    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)


def run_capillaries_Chen_2024_1_saxsonly(ts1=10,ts2=20,tl=30):
    """
    Standard SAXS, measure transmission only during the first run

    Use two exposures:
        ts (float): shorter exposure time for first measurement,
        tl (float): longer exposure time for second measurement.
    
    sample_id(user_name='test', sample_name='test')
    RE(count([pil900KW]))
    


    """
    # yield from bps.sleep(1500)
    
    #names =   ['PN13-3','PN14-3','PN15-3','PN16-3','PN17-3','PN18-3','PN19-3','PN20-3','PN21-3','PN22-3','PN23-3','PN24-3','PN25-3','PN-empty-3']
    #piezo_x = [ -35400, -28900,   -22700, -16400,   -10000,  -3600,    2800,    9300,    15600,    21900,   28200,   34600,  40900, 47300 ]
    #piezo_y = [ -950 for n in names]
    #piezo_z = [ -5000 for n in names]

    #names =   ['PN1-3','PN2-3','PN3-3','PN4-3','PN5-3','PN6-3','PN7-3','PN8-3','PN9-3','PN10-3','PN11-3','PN12-3']
    #piezo_x = [ -34500, -27900,-21500, -15100, -8900,  -2500,  3800,    10200,  16400,   23000,   29300,   35400]
    #piezo_y = [ 50 for n in names]
    #piezo_z = [ -5000 for n in names]

    #names =   ['PN13-trial-6']
    #piezo_x = [ -34500]
    #piezo_y = [ 2450 for n in names]
    #piezo_z = [ -4600 for n in names]

    names =   ['H3_4longer']
    piezo_x = [-27600]
    piezo_y = [ -7550]
    piezo_z = [ -5500]  


    assert len(names)   == len(piezo_x), f"Wrong list lenghts"
    assert len(piezo_x) == len(piezo_y), f"Wrong list lenghts"
    assert len(piezo_x) == len(piezo_z), f"Wrong list lenghts"

    
    y_off = [0]
    user_name = 'TC'
    
    exposures = [ts1, ts2,tl]
    
    dets = [pil1M]

    for name, x, y, z in zip(names, piezo_x, piezo_y, piezo_z):
        yield from bps.mv(piezo.x, x,
                          piezo.y, y,
                          piezo.z, z,
                          )



        # Read pin diode current
        if waxs.arc.position > 15:
            fs.open()
            yield from bps.sleep(0.3)
            pd_curr = pdcurrent1.value
            fs.close()
            pd = str(int(np.round(pd_curr, 0))).zfill(7)
        else:
            pd = 0
        
        for yy, y_of in enumerate(y_off):
            yield from bps.mv(piezo.y, y + y_of)

            for exp in exposures:
                det_exposure_time(exp, exp)
                yield from bps.sleep(2)

                exp_save = str(int(np.round(exp, 0))).zfill(2)

                sample_name = f'{name}_exp{exp_save}_loc{yy}_pd{pd}{get_scan_md()}'
                sample_id(user_name=user_name, sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets)


    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)



def run_capillaries_Chen_2024_1_waxs(ts1=0.5, ts2=1):
    """
    Standard SAXS, measure transmission only during the first run

    Use two exposures:
        ts (float): shorter exposure time for first measurement,
        tl (float): longer exposure time for second measurement.
    
    sample_id(user_name='test', sample_name='test')
    RE(count([pil900KW]))
    
    """
    # yield from bps.sleep(1500)
    #names =   [ 'AgB-2m']
    #piezo_x = [  -38900 ]
    #piezo_y = [  4000 ]
    #piezo_z = [ -8224 for n in names]

    names =   ['Dry-D-SXQ-A1-17-076-02-2','Dry-D-SXQ-A1-09-04-2','Dry-SXQ-A1-17-076-02-2','Dry-SXQ-A1-09-04-2']
    piezo_x = [-30200,                      -25600,                   -17200,                -10600   ]
    piezo_y = [3100 for n in names]
    piezo_z = [-5500 for n in names]

    assert len(names)   == len(piezo_x), f"Wrong list lenghts"
    assert len(piezo_x) == len(piezo_y), f"Wrong list lenghts"
    assert len(piezo_x) == len(piezo_z), f"Wrong list lenghts"

    waxs_arc = [0,20]
    
    y_off = [0]
    user_name = 'TC'
    
    exposures = [ts1, ts2]
    
    #waxs_arc = [0, 20] if waxs_only else [20]

    for name, x, y, z in zip(names, piezo_x, piezo_y, piezo_z):
        yield from bps.mv(piezo.x, x,
                          piezo.y, y,
                          piezo.z, z,
                          )

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)

            dets = [pil900KW] if waxs.arc.position < 15 else [pil1M, pil900KW]

            # Read pin diode current
            if waxs.arc.position > 15:
                fs.open()
                yield from bps.sleep(0.3)
                pd_curr = pdcurrent1.value
                fs.close()
                pd = str(int(np.round(pd_curr, 0))).zfill(7)
            else:
                pd = 0
            
            for yy, y_of in enumerate(y_off):
                yield from bps.mv(piezo.y, y + y_of)

                for exp in exposures:
                    det_exposure_time(exp, exp)
                    yield from bps.sleep(2)

                    exp_save = str(int(np.round(exp, 0))).zfill(2)

                    sample_name = f'{name}_exp{exp_save}_loc{yy}_pd{pd}{get_scan_md()}'
                    sample_id(user_name=user_name, sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets)


    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)




def run_capillaries_Chen_2024_1_saxs_time(exp_time=0.5, delay_sec=300,num=7):
    """
    Standard SAXS, measure transmission only during the first run

    Use two exposures:
        ts (float): shorter exposure time for first measurement,
        tl (float): longer exposure time for second measurement.
    
    sample_id(user_name='test', sample_name='test')
    RE(count([pil900KW]))
    
    """
    # yield from bps.sleep(1500)
    names =   [ 'TC5-thf-timestudy']
    piezo_x = [ -28400]
    piezo_y = [ 2550 for n in names]
    piezo_z = [ -4200 for n in names]

    assert len(names)   == len(piezo_x), f"Wrong list lenghts"
    assert len(piezo_x) == len(piezo_y), f"Wrong list lenghts"
    assert len(piezo_x) == len(piezo_z), f"Wrong list lenghts"

    
    dets = [pil1M]
    y_off = [0]
    user_name = 'TC'
    
    exposures = [exp_time]
    

    for name, x, y, z in zip(names, piezo_x, piezo_y, piezo_z):
        yield from bps.mv(piezo.x, x,
                          piezo.y, y,
                          piezo.z, z,
                          )



        # Read pin diode current
        if waxs.arc.position > 15:
            fs.open()
            yield from bps.sleep(0.3)
            pd_curr = pdcurrent1.value
            fs.close()
            pd = str(int(np.round(pd_curr, 0))).zfill(7)
        else:
            pd = 0
        
        for yy, y_of in enumerate(y_off):
            yield from bps.mv(piezo.y, y + y_of)

            for exp in exposures:
                det_exposure_time(exp, exp)
                yield from bps.sleep(2)

                exp_save = str(int(np.round(exp, 0))).zfill(2)

                sample_name = f'{name}_exp{exp_save}_loc{yy}_pd{pd}{get_scan_md()}'
                sample_id(user_name=user_name, sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets,num,delay_sec)


    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)

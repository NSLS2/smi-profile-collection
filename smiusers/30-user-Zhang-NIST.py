def run_continous_Zhang(name='test', t=1, td=10):
    """
    Continous SWAXS measurement

    Args:
        name (str): sample name, please make it unique for each,
        t (float): detector exposure time is seconds,
        td (flaot): time interval between measurements.
    """

    user = "FZ"
    wa = 17

    det_exposure_time(t, t)

    t_initial = time.time()

    yield from bps.mv(waxs, wa)
    dets = [pil900KW] if waxs.arc.position < 14.9 else [pil1M, pil900KW]

    
    for i in range(99999):

        t_measurement = time.time()
        
        # Generate sample name
        step = str(i).zfill(4)
        time_sname = str(np.round(t_measurement - t_initial, 0)).zfill(7)
        sample_name = f'{name}_step{step}_time{time_sname}s{get_scan_md()}'
        sample_id(user_name=user, sample_name=sample_name)
        
        print(f"\n\n\n\t=== Sample: {sample_name} ===")
        yield from bp.count(dets)
    
        # Wait until the total time difference passes
        while (time.time() - t_measurement) < td:
            yield from bps.sleep(0.1)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)



def run_continous_pindiode_Zhang(name='test', t=1, td=10):
    """
    Continous SWAXS measurement

    Args:
        name (str): sample name, please make it unique for each,
        t (float): detector exposure time is seconds,
        td (flaot): time interval between measurements.
    """

    user = "FZ"
    wa = 15

    det_exposure_time(t, t)

    t_initial = time.time()

    yield from bps.mv(waxs, wa)
    dets = [pil900KW] if waxs.arc.position < 14.9 else [pil1M, pil900KW]
    dets.append(pdcurrent1)

    
    for i in range(99999):

        # Read pin diode current when the shutter is open
        fs.open()
        yield from bps.sleep(0.3)
        pd_curr = pdcurrent1.value
        fs.close()
        pd = str(int(np.round(pd_curr, 0))).zfill(4)

        t_measurement = time.time()
        
        # Generate sample name
        step = str(i).zfill(4)
        time_sname = str(np.round(t_measurement - t_initial, 0)).zfill(7)
        sample_name = f'{name}_step{step}_time{time_sname}s_pd{pd}{get_scan_md()}'
        sample_id(user_name=user, sample_name=sample_name)
        
        print(f"\n\n\n\t=== Sample: {sample_name} ===")
        yield from bp.count(dets)
    
        # Wait until the total time difference passes
        while (time.time() - t_measurement) < td:
            yield from bps.sleep(0.1)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)


def run_standard_swaxs_Zhang_2023_3(t=2):
    """
    Standard SWAXS scan
    """
    
    names =   [     'KaptonBlank',  'Air Blank', ]
    piezo_x = [     24000,    -3800 ] 
    piezo_y = [  1200 for n in names ]
    piezo_z = [ 10400 for n in names ]

    assert len(names)   == len(piezo_x), f"Wrong list lenghts"
    assert len(piezo_x) == len(piezo_y), f"Wrong list lenghts"
    assert len(piezo_x) == len(piezo_z), f"Wrong list lenghts"

    user = 'FZ'
    waxs_arc = [ 20, 0 ]
    x_off = [-500, 0, 500 ]
    det_exposure_time(t, t)

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)

        condition = waxs.arc.position < 15

        dets = [pil900KW] if condition else [pil1M, pil900KW]
            
        for name, x, y, z in zip(names, piezo_x, piezo_y, piezo_z):
            yield from bps.mv(piezo.x, x,
                              piezo.y, y,
                              piezo.z, z,
            )
        
            for xx, x_of in enumerate(x_off):
                yield from bps.mv(piezo.x, x + x_of)

                if not condition:
                    fs.open()
                    yield from bps.sleep(0.3)
                    pd_curr = pdcurrent1.value
                    fs.close()
                else:
                    pd_curr = 0

                pd = str(int(np.round(pd_curr, 0))).zfill(4)
                
                sample_name = f'{name}_loc{xx}_pd{pd}{get_scan_md()}'
                sample_id(user_name=user, sample_name=sample_name)
                print(f"\n\n\n\t=== Sample: {sample_name} ===")
                yield from bp.count(dets)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)
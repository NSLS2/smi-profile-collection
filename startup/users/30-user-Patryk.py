def patryk_saxs_overnight(t=1):
    """
    SAXS mapping
    """

    names =     ['ORF7A-C-60um', 'ORF7A-C-60um-bkg', 'ORF7A-D-50um-wet', 'ORF7A-D-50um-wet-bkg', 
             'ORF7A-D-50um-dry', 'ORF7A-D-50um-dry-bkg', ]

    piezo_x =   [         14000,              19000,             -11000,               -8000, 
                         -18700,                 -16100, ]
    
    piezo_y =   [             0,                  0,               2200,                2200, 
                          -2100,                  -3100, ]
    
    piezo_z =   [          7700,               7700,               7900,                7900, 
                           7900,                   7900, ]

    names = [n + '-grid01' for n in names]

    assert len(names)   == len(piezo_x), f"Wrong list lenghts"
    assert len(piezo_x) == len(piezo_y), f"Wrong list lenghts"
    assert len(piezo_y) == len(piezo_z), f"Wrong list lenghts"

    # Move WAXS out of the way
    if waxs.arc.position < 19.5:
        yield from bps.mv(waxs, 20)
    dets = [pil1M]
    det_exposure_time(t, t)

    for name, x, y, z, in zip(names, piezo_x, piezo_y, piezo_z):
        yield from bps.mv(piezo.x, x,
                          piezo.y, y,
                          piezo.z, z)

        sample_name = f'{name}{get_scan_md()}'
        sample_id(user_name='PW', sample_name=sample_name)
        print(f"\n\n\n\t=== Sample: {sample_name} ===")

        # Take on axis camera
        yield from bp.count([OAV_writing])

        scan_id = db[-1].start['scan_id'] + 1
        msg = f'sample: {sample_name}\nscan_id: {scan_id}'
        olog(msg, logbooks='Experiments')

        y_range = [-3000, 3000, 31] if 'ORF7A-D-50um' not in name else [-2000, 2000, 81]
        x_range = [-3000, 3000, 31] if 'ORF7A-D-50um' not in name else [-2000, 2000, 21]

        if 'bkg' not in name:
            yield from rel_grid_scan([pil1M], piezo.y, *y_range, piezo.x, *x_range)

        else:
            yield from rel_grid_scan([pil1M], piezo.y, -500, 500, 5, piezo.x, -500, 500, 5)


def run_swaxs_Dominik_2023_1(t=0.1):
    """
    Take WAXS and SAXS at a few sample positions for averaging

    Specify central positions on the samples with xlocs and ylocs,
    then offsets from central positions with x_off and y_off. Run
    WAXS arc as the slowest motor.
    """

    names_1   = [   'D123', 'FeEDTA', 'Ni5Z30', '10RhZ23', 'D133', '1.0Pdfresh',   '1.0Pdcalc',]
    piezo_x_1 = [  -28600,    -20600,   -14000,     -2600,  13400,        27000,         39000,]
    piezo_y_1 = [   -2000,     -1500,    -1500,     -2000,  -2000,        -2000,         -2000,]
    stage_y_1 = [ 0 for n in names_1 ]

    names_2   = [ ] 
    piezo_x_2 = [ ]
    piezo_y_2 = [ ]
    stage_y_2 = [ ]

    # Combine rows
    names   = names_1   + names_2
    piezo_x = piezo_x_1 + piezo_x_2
    piezo_y = piezo_y_1 + piezo_y_2
    stage_y  = stage_y_1  + stage_y_2

    # Offsets for taking a few points per sample
    x_off = [0, 500]
    y_off = [0, 200]

    waxs_arc = [20, 0]
    user_name = "DW"

    assert len(names)    == len(piezo_x), f"Wrong list lenghts"
    assert len(piezo_x)  == len(piezo_y), f"Wrong list lenghts"
    assert len(piezo_y)  == len(stage_y), f"Wrong list lenghts"

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)
        
        dets = [pil900KW] if waxs.arc.position < 15 else [pil900KW, pil1M]
        det_exposure_time(t, t)

        for name, x, y, hex_y in zip(names, piezo_x, piezo_y, stage_y):

            yield from bps.mv(piezo.x, x,
                              piezo.y, y,
                              stage.y, hex_y)

            for yy, y_of in enumerate(y_off):
                yield from bps.mv(piezo.y, y + y_of)

                for xx, x_of in enumerate(x_off):
                    yield from bps.mv(piezo.x, x + x_of)

                    loc = f'{yy}{xx}'
                    sample_name = f'{name}{get_scan_md()}_loc{loc}'
                    sample_id(user_name=user_name, sample_name=sample_name)
                    print(f"\n\n\n\t=== Sample: {sample_name} ===")

                    yield from bp.count(dets)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.1, 0.1)


# RE.md['SAF_number'] = 311069

def run_swaxs_fibres_2023_1(t=1):
    """
    Take WAXS and SAXS at a few sample positions for averaging

    Specify central positions on the samples with xlocs and ylocs,
    then offsets from central positions with x_off and y_off. Run
    WAXS arc as the slowest motor.
    """

    names_1   = [ '4-pgsk-fib-1', '4-pgsk-fib-2', '4-pgsk-fib-3', '3-sk-fib-1', '3-sk-fib-2', '3-sk-fib-3', 'bkg_vcm', ]
    piezo_x_1 = [            700,           1850,           4010,        15810,        17310,        19500,     20500, ]
    piezo_y_1 = [          -1850,          -1850,          -2400,        -2400,        -2400,        -1000,     -1000, ]
    stage_y_1 = [ 0 for n in names_1 ]

    names_2   = [ '2-pgsk-flm-1', '2-pgsk-flm-2', '2-pgsk-flm-3', '1-sk-flm-1', '1-sk-flm-2', '1-sk-flm-3', ] 
    piezo_x_2 = [          29500,          30000,          28500,        43500,        44000,        45000, ]
    piezo_y_2 = [          -1000,          -2000,            500,        -2000,            0,         1000, ]
    stage_y_2 = [ 0 for n in names_2 ]

    # Combine rows
    names   = names_1   + names_2
    piezo_x = piezo_x_1 + piezo_x_2
    piezo_y = piezo_y_1 + piezo_y_2
    stage_y  = stage_y_1  + stage_y_2

    # offsets inside the main loop

    waxs_arc = [20]
    user_name = "PW"

    assert len(names)    == len(piezo_x), f"Wrong list lenghts"
    assert len(piezo_x)  == len(piezo_y), f"Wrong list lenghts"
    assert len(piezo_y)  == len(stage_y), f"Wrong list lenghts"

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)
        
        #dets = [pil900KW] if waxs.arc.position < 15 else [pil900KW, pil1M]
        dets = [pil1M]
        det_exposure_time(t, t)

        for name, x, y, hex_y in zip(names, piezo_x, piezo_y, stage_y):

            yield from bps.mv(piezo.x, x,
                              piezo.y, y,
                              stage.y, hex_y)
            
            if 'fib' in name:
                x_off = [0, ]
                y_off = [0, 30, 60, 90, 120]
            else:
                x_off = [0, 250, 500, 750, ]
                y_off = [0, 250, 500, 750, ]

            for yy, y_of in enumerate(y_off):
                yield from bps.mv(piezo.y, y + y_of)

                for xx, x_of in enumerate(x_off):
                    yield from bps.mv(piezo.x, x + x_of)

                    loc = f'{yy}{xx}'
                    sample_name = f'{name}{get_scan_md()}_loc{loc}'
                    sample_id(user_name=user_name, sample_name=sample_name)
                    print(f"\n\n\n\t=== Sample: {sample_name} ===")

                    yield from bp.count(dets)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)


def run_swaxs_textile_2023_2(t=0.5):
    """
    Take WAXS and SAXS at a few sample positions for averaging
    """

    names   = [  's01']#, 's02', 's03', 's04', 's05',  'bkg', ]
    piezo_x = [  -37900]#, 33000, 18000,  4500, -8000, -18000, ]
    piezo_y = [  3200 for n in names ]
    stage_y = [ 0 for n in names ]
    names = [ n + '-try4' for n in names]

    # offsets inside the main loop

    waxs_arc = [ 20 ]
    x_off = [ 500, 0, 500 ]
    y_off = [ 0, ]
    user_name = "PW"

    assert len(names)    == len(piezo_x), f"Wrong list lenghts"
    assert len(piezo_x)  == len(piezo_y), f"Wrong list lenghts"
    assert len(piezo_y)  == len(stage_y), f"Wrong list lenghts"


    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)

        #dets = [pil900KW] if waxs.arc.position < 15 else [pil900KW, pil1M]
        dets = [pil1M]
        det_exposure_time(t, t)

        for name, x, y, hex_y in zip(names, piezo_x, piezo_y, stage_y):

            yield from bps.mv(piezo.x, x,
                              piezo.y, y,
                              stage.y, hex_y)

            for yy, y_of in enumerate(y_off):
                yield from bps.mv(piezo.y, y + y_of)

                for xx, x_of in enumerate(x_off):
                    yield from bps.mv(piezo.x, x + x_of)

                    #if (
                    #     #(name == names[0])
                    #     (wa == waxs_arc[0])
                    #     and (yy == 0)
                    #     and (xx == 0)
                    #    ):
                    #
                    #    sample_id(user_name="test", sample_name="test")
                    #    yield from bp.count(dets)

                    loc = f'{yy}{xx}'
                    sample_name = f'{name}{get_scan_md()}_loc{loc}'
                    print(f"\n\n\n\t=== Sample: {sample_name} ===")
                    sample_id(user_name=user_name, sample_name=sample_name)
                    yield from bp.count(dets)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)


def run_swaxs_workaround_2023_2(t=0.5):
    """
    Take WAXS and SAXS at a few sample positions for averaging
    """

    names   = [  's01', 's02', 's03', 's04', 's05',  'bkg', ]
    piezo_x = [  44000, 33000, 18000,  4500, -8000, -18000, ]
    piezo_y = [  2000 for n in names ]
    stage_y = [ 0 for n in names ]
    names = [ n + '-attn-nobs' for n in names]

    # offsets inside the main loop

    waxs_arc = [ 20 ]
    x_off = [ -500, 0, 500 ]
    y_off = [ 0, ]
    user_name = "PW"

    assert len(names)    == len(piezo_x), f"Wrong list lenghts"
    assert len(piezo_x)  == len(piezo_y), f"Wrong list lenghts"
    assert len(piezo_y)  == len(stage_y), f"Wrong list lenghts"


    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)

        #dets = [pil900KW] if waxs.arc.position < 15 else [pil900KW, pil1M]
        dets = [pil1M]
        det_exposure_time(t, t)

        for name, x, y, hex_y in zip(names, piezo_x, piezo_y, stage_y):

            yield from bps.mv(piezo.x, x,
                              piezo.y, y,
                              stage.y, hex_y)

            for yy, y_of in enumerate(y_off):
                yield from bps.mv(piezo.y, y + y_of)

                for xx, x_of in enumerate(x_off):
                    yield from bps.mv(piezo.x, x + x_of)

                    loc = f'{yy}{xx}'

                    if loc != '01':
                        sample_name = 'test'
                        sample_id(user_name="test", sample_name=sample_name)

                    else:
                        sample_name = f'{name}{get_scan_md()}_loc{loc}'
                        sample_id(user_name=user_name, sample_name=sample_name)
                    print(f"\n\n\n\t=== Sample: {sample_name} ===")
                    yield from bp.count(dets)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)

def move_energy_slowly(target_e, e_step=100):
    """
    Move energy gently using feedback
    """

    current_e = energy.position.energy
    

    if (current_e > 10000) and (target_e > 10000):

        energies = np.arange(current_e, target_e + 1, e_step)

        for e in energies:

            feedback('off')
            yield from bps.mv(energy, e)
            yield from bps.sleep(2)
            feedback('on')
            yield from bps.sleep(5)
    else:
        print('Energy change not allowed, do proper alignment')



def test_DI(t=1):
    """
    Test duplicated images
    """

    user_name = "test"

    names = ["test2", "test3"]

    det_exposure_time(t, t)

    # Energies for calcium K edge, coarse resolution
    energies_coarse = np.concatenate(
        (
            np.linspace(4030, 4045, 3),
        )
    )

    # Do not read SAXS if WAXS is in the way
    wa = waxs.arc.position
    dets = [pil900KW]

    # Change energies
    energies = energies_coarse

    # Go over samples

    for name in names:

        # Scan over energies
        for e in energies:
            yield from bps.sleep(2)

            # Metadata
            bpm = xbpm3.sumX.get()
            sdd = pil1m_pos.z.position / 1000
            wa = str(np.round(float(wa), 1)).zfill(4)

            # Detector file name
            name_fmt = "{sample}_{energy}eV_wa{wax}_sdd{sdd}m_bpm{xbpm}"
            sample_name = name_fmt.format(
                sample=name,
                energy="%6.2f" % e,
                wax=wa,
                sdd="%.1f" % sdd,
                xbpm="%4.3f" % bpm,
            )
            sample_id(user_name=user_name, sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")

            yield from bp.count(dets, num=1)

def test_example_SWAXS_2023_3(t=0.5):
    """
    Standard SWAXS scan
    """
    
    names =   [ 'AgBH-1', 'AgBH-2', 'empty', ]
    piezo_x = [   -45400,   -44400,  -19000, ] 
    piezo_y = [     3800,     4200,    4200, ]
    piezo_z = [ 14400 for n in names ]

    assert len(names)   == len(piezo_x), f"Wrong list lenghts"
    assert len(piezo_x) == len(piezo_y), f"Wrong list lenghts"
    assert len(piezo_x) == len(piezo_z), f"Wrong list lenghts"

    user = 'test'
    waxs_arc = [40, 20, 0]
    det_exposure_time(t, t)

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)
        dets = [pil900KW] if waxs.arc.position < 15 else [pil1M, pil900KW]
            
        for name, x, y, z in zip(names, piezo_x, piezo_y, piezo_z):
            yield from bps.mv(piezo.x, x,
                              piezo.y, y,
                              piezo.z, z,
            )
        
            sample_name = f'{name}{get_scan_md()}'
            sample_id(user_name=user, sample_name=sample_name)
            print(f"\n\n\n\t=== Sample: {sample_name} ===")
            yield from bp.count(dets)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)

# DT-313930

def get_more_md(temp=25, tender=True, bpm=True):
    """
    Add temperature and XBPM3 readings into the scan metadata
    """

    more_md = f'{get_scan_md(tender=tender)}'

    if temp:
        temp = str(np.round(float(temp), 1)).zfill(5)
        more_md = f'_{temp}degC{more_md}'
    if bpm:
        xbpm = xbpm3.sumX.get()
        xbpm = str(np.round(float(xbpm), 3)).zfill(5)
        more_md = f'{more_md}_xbpm{xbpm}'

    return more_md


def take_single_temp_frame(name='test', temp=25):
    """
    After reaching T, take data
    """

    dets = [pil900KW]


    sample_name = f'{name}{get_more_md(temp)}'
    sample_id(user_name='PW', sample_name=sample_name)
    print(f"\n\n\n\t=== Sample: {sample_name} ===")
    yield from bp.count(dets)

def take_energy_temp_scan(name='test', temp=25):
    """
    After reaching T, take data
    """

    e = np.around(energy.position.energy)
    energies = np.concatenate((
        np.arange(e - 5, e - 2, 1),
        np.arange(e - 2, e + 2 + 0.5, 0.5),
        np.arange(e + 2 + 1 , e + 2 + 2 + 1, 1),
    ))

    dets = [pil900KW] if waxs.arc.position < 15 else [pil900KW, pil1M]

    for nrg in energies:
        yield from bps.mv(energy, nrg)
        yield from bps.sleep(2)
        if xbpm2.sumX.get() < 50:
            yield from bps.sleep(2)
            yield from bps.mv(energy, nrg)
            yield from bps.sleep(2)

        sample_name = f'{name}-escan{get_more_md(temp=temp)}'
        sample_id(user_name='PW', sample_name=sample_name)
        print(f"\n\n\n\t=== Sample: {sample_name} ===")
        yield from bp.count(dets)

    yield from bps.mv(energy, e)
    sample_id(user_name='test', sample_name=f'test_{get_more_md()}')

def create_timestamp():
    """
    store in RE.md and print
    """
    RE.md['tstamp'] = time.time()
    print('\nTime stamp created in RE.md')
    tstamp = RE.md['tstamp']
    print(f'tstamp: {tstamp}')



def run_Linkam_temp_run(name, t=0.5, td= 4 * 60, frames=600):
    """
    Set temperature ramp in Linkam, create timestamp,
    run continous measurement, explore WAXS and SAXS

    Args:
        name (str): sample name,
        t (float): exposure time for one frame in s,
        td (float): time difference between point measurements,
        frames (int): number of franes.
    """

    try:
        tstamp = RE.md['tstamp']
    except:
        tstamp = time.time()
        RE.md['tstamp'] = tstamp
        print(f'\nTime stamp created in RE.md: {tstamp}')

    waxs_arc = [0, 20]
    det_exposure_time(t, t)
    user = 'PW'

    for spoint in range(frames):
        print(f'Frame {spoint + 1} / {frames}')
        t_frame = time.time()

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)
            dets = [pil900KW] if waxs.arc.position < 14.9 else [pil1M, pil900KW]

            t_measurement = time.time()
            time_sname = str(np.round(t_measurement - tstamp, 0)).zfill(7)
            md = f'{get_more_md(temp=False)}'

            sample_name = f'{name}-tscan_time{time_sname}s{md}'
            sample_id(user_name=user, sample_name=sample_name)
            print(f"\n\n\n\t=== Sample: {sample_name} ===")
            yield from bp.count(dets)

        yield from bps.mv(waxs, waxs_arc[0])
        print(f'Waiting for {td}s to pass between frames')
        while (time.time() - t_frame) < td:
            yield from bps.sleep(1)

    sample_id(user_name='test', sample_name=f'test')


def run_swaxs_2024_1_slk(t=1):
    """
    Take WAXS and SAXS at several sample positions

    Specify central positions on the samples with xlocs and ylocs,
    then offsets from central positions with x_off and y_off.
    """

    names_1 = ['flm-100-0-MeOH', 'flm-90-10-MeOH', 'flm-80-20-MeOH', 'flm-70-30-MeOH', 'flm-50-50-MeOH',]           
    piezo_x_1 = [        -43200,           -37000,           -32000,           -24500,           -17500,]         
    piezo_y_1 = [          1000,              600,             1000,             1200,             1200,]

    names_2 = ['flm-30-70-MeOH', 'fbr-30-70-untr-1draw', 'fbr-30-70-untr-2draw', 'fbr-30-70-MeOH-2draw',]
    piezo_x_2 = [        -10000,                  -2860,                   2290,                   6790,] 
    piezo_y_2 = [          1200,                    600,                   1700,                   1200,]

    names   = names_1   + names_2
    piezo_x = piezo_x_1 + piezo_x_2
    piezo_y = piezo_y_1 + piezo_y_2      

    #x_off = [ 0 ]
    #y_off = [ 0 ]    
    waxs_arc = [0, 20]

    user = "PW"
    det_exposure_time(t, t)

    msg = "Wrong number of coordinates"
    assert len(piezo_x) == len(names), msg
    assert len(piezo_x) == len(piezo_y), msg

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)
        dets = [pil900KW] if waxs.arc.position < 15 else [pil900KW, pil1M]
        dets.append(OAV_writing)

        for name, x, y in zip(names, piezo_x, piezo_y):
            yield from bps.mv(piezo.y, y,
                              piezo.x, x,
                              )
            
            if 'fbr' in name:
                x_off = [ 0 ]
                y_off = [ -200, -150, -100, -50, 0, 50, 100, 150, 200 ]
            else:
                x_off = [ -300, 0, 300 ]
                y_off = [ -300, 0, 300 ] 

            for yy, y_of in enumerate(y_off):
                yield from bps.mv(piezo.y, y + y_of)

                for xx, x_of in enumerate(x_off):
                    yield from bps.mv(piezo.x, x + x_of)
                    
                    loc = f'{yy}{xx}'
                    sample_name = f'{name}{get_scan_md()}_loc{loc}'
                    sample_id(user_name=user, sample_name=sample_name)
                    print(f"\n\n\n\t=== Sample: {sample_name} ===")
                    yield from bp.count(dets)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)

def run_swaxs_2024_1_par(t=1):
    """
    Take WAXS and SAXS at several sample positions

    Specify central positions on the samples with xlocs and ylocs,
    then offsets from central positions with x_off and y_off.
    """

    names =   [  'AgBH', 'PSTFSI-Li-10to1',]           
    piezo_x = [  -44000,            -11200, ]         
    piezo_y = [   -4000,              6400, ]
    piezo_z = [    8200,             12600, ]
    # hexa(x, y, z) =  (0, 7, 4)

    x_off = [ -600, -300, 0, 300, 600 ]
    y_off = [ -150,       0,      150 ]
    waxs_arc = [0, 20]

    user = "PW"
    det_exposure_time(t, t)

    msg = "Wrong number of coordinates"
    assert len(piezo_x) == len(names), msg
    assert len(piezo_x) == len(piezo_y), msg
    assert len(piezo_x) == len(piezo_z), msg

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)
        dets = [pil900KW] if waxs.arc.position < 15 else [pil900KW, pil1M]
        dets.append(OAV_writing)

        for name, x, y, z in zip(names, piezo_x, piezo_y, piezo_z):
            yield from bps.mv(piezo.y, y,
                              piezo.x, x,
                              piezo.z, z,
                              )

            for yy, y_of in enumerate(y_off):
                yield from bps.mv(piezo.y, y + y_of)

                for xx, x_of in enumerate(x_off):
                    yield from bps.mv(piezo.x, x + x_of)
                    
                    loc = f'{xx}{yy}'
                    sample_name = f'{name}{get_scan_md()}_loc{loc}'
                    sample_id(user_name=user, sample_name=sample_name)
                    print(f"\n\n\n\t=== Sample: {sample_name} ===")
                    yield from bp.count(dets)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)



def get_more_md(tender=True, bpm=True):
    """
    Add temperature and XBPM2 readings into the scan metadata
    """

    more_md = f'{get_scan_md(tender=tender)}'

    if bpm:
        xbpm = xbpm2.sumX.get()
        xbpm = str(np.round(float(xbpm), 3)).zfill(5)
        more_md = f'{more_md}_xbpm{xbpm}'

    return more_md

def take_energy_scan_2024_1(t=1):
    """
    Energy scan
    """
    names =   [ 'SLi10-nexafs-3', ]           
    piezo_x = [           -31650, ]         
    piezo_y = [            -7800, ]
    piezo_z = [             7000, ]

    msg = "Wrong number of coordinates"
    assert len(piezo_x) == len(names), msg
    assert len(piezo_x) == len(piezo_y), msg
    assert len(piezo_x) == len(piezo_z), msg

    waxs_arc = [ 60 ]

    user = "PW"
    det_exposure_time(t, t)

    energies = np.concatenate((
        np.arange(2445, 2470, 5),
        np.arange(2470, 2480, 0.5),
        np.arange(2480, 2490, 0.5),
        np.arange(2490, 2501, 5),
    ))
    
    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)
        dets = [pil900KW] # if waxs.arc.position < 15 else [pil900KW, pil1M]

        for name, x, y, z in zip(names, piezo_x, piezo_y, piezo_z):
            yield from bps.mv(piezo.y, y,
                              piezo.x, x,
                              piezo.z, z,
                              )

            for nrg in energies:
                yield from bps.mv(energy, nrg)
                yield from bps.sleep(2)
                if xbpm2.sumX.get() < 50:
                    yield from bps.sleep(2)
                    yield from bps.mv(energy, nrg)
                    yield from bps.sleep(2)

                sample_name = f'{name}-escan{get_more_md()}_loc00'
                sample_id(user_name='PW', sample_name=sample_name)
                print(f"\n\n\n\t=== Sample: {sample_name} ===")
                yield from bp.count(dets)

    sample_id(user_name='test', sample_name=f'test_{get_more_md()}')


def run_swaxs_2024_1_par2(t=2):
    """
    Take WAXS and SAXS at several sample positions

    Specify central positions on the samples with xlocs and ylocs,
    then offsets from central positions with x_off and y_off.
    """

    names =   [  'mpt1.5', 'mpt1.0',  'SLi10',  'SNa10',  'MLi10',  'MNa10', 'SNa0', 'SLi0', 'MLi0',  'MNa0', 'SLi5', 'MNa5', 'SNa5', ]           
    piezo_x = [   -44100,    -37500,   -31650,   -24600,   -18000,   -12600,  -5250,    600,   6900,   13500,  20200,  25400,  32100, ]         
    piezo_y = [     6000,      6000,    -7800,    -8600,    -8400,    -8600,  -7400,   1750,  -6500,   -8900,  -7200,  -8500,   1550, ]
    piezo_z = [     9400,      6600,     7000,     5200,     5200,     5200,   5200,   7000,   5600,    5600,   5600,   5600,   5600, ]


    x_off = [ 0 ]
    y_off = [ -100, -50, 0, 50, 100, 150, 200, 250, 300]
    waxs_arc = [0, 20]

    user = "BP"
    det_exposure_time(t, t)

    msg = "Wrong number of coordinates"
    assert len(piezo_x) == len(names), msg
    assert len(piezo_x) == len(piezo_y), msg
    assert len(piezo_x) == len(piezo_z), msg

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)
        dets = [pil900KW] if waxs.arc.position < 15 else [pil900KW, pil1M]
        #dets.append(OAV_writing)

        for name, x, y, z, in zip(names, piezo_x, piezo_y, piezo_z):
            yield from bps.mv(piezo.y, y,
                              piezo.x, x,
                              piezo.z, z,
                              )

            for yy, y_of in enumerate(y_off):
                yield from bps.mv(piezo.y, y + y_of)

                for xx, x_of in enumerate(x_off):
                    yield from bps.mv(piezo.x, x + x_of)
                    
                    loc = f'{xx}{yy}'
                    sample_name = f'{name}{get_scan_md()}_loc{loc}'
                    sample_id(user_name=user, sample_name=sample_name)
                    print(f"\n\n\n\t=== Sample: {sample_name} ===")
                    yield from bp.count(dets)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)

def run_swaxs_2024_1_par2tender(t=5):
    """
    Take WAXS and SAXS at several sample positions

    Specify central positions on the samples with xlocs and ylocs,
    then offsets from central positions with x_off and y_off.
    """

    names =   [  'mpt1.5', 'mpt1.0',  'SLi10',  'SNa10',  'MLi10',  'MNa10', 'SNa0', 'SLi0', 'MLi0',  'MNa0', 'SLi5', 'MNa5', 'SNa5', ]           
    piezo_x = [   -44200,    -37600,   -31650,   -24600,   -18000,   -12600,  -5250,    750,   7000,   13500,  20200,  25700,  32100, ]         
    piezo_y = [     6000,      6000,    -6000,    -8100,    -8300,    -8300,  -7300,   1550,  -6500,   -8900,  -7400,  -8500,   1350, ]
    piezo_z = [     9400,      6600,     7000,     5800,     5400,     5400,   5200,   5400,   5600,    5600,   5600,   5600,   5600, ]


    x_off = [ 0 ]
    y_off = [ -100, -50, 0, 50, 100, 150, 200, 250, 300]
    waxs_arc = [0, 20]

    user = "BP"
    det_exposure_time(t, t)

    msg = "Wrong number of coordinates"
    assert len(piezo_x) == len(names), msg
    assert len(piezo_x) == len(piezo_y), msg
    assert len(piezo_x) == len(piezo_z), msg

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)
        dets = [pil900KW] if waxs.arc.position < 15 else [pil900KW, pil1M]
        #dets.append(OAV_writing)

        for name, x, y, z, in zip(names, piezo_x, piezo_y, piezo_z):
            yield from bps.mv(piezo.y, y,
                              piezo.x, x,
                              piezo.z, z,
                              )

            for yy, y_of in enumerate(y_off):
                yield from bps.mv(piezo.y, y + y_of)

                for xx, x_of in enumerate(x_off):
                    yield from bps.mv(piezo.x, x + x_of)
                    
                    loc = f'{xx}{yy}'
                    sample_name = f'{name}{get_more_md()}_loc{loc}'
                    sample_id(user_name=user, sample_name=sample_name)
                    print(f"\n\n\n\t=== Sample: {sample_name} ===")
                    yield from bp.count(dets)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def run_swaxs_2024_1_par2tender_energy(t=2):
    """
    Take WAXS and SAXS at several sample positions

    Specify central positions on the samples with xlocs and ylocs,
    then offsets from central positions with x_off and y_off.
    """

    names =   [  'mpt1.5', 'mpt1.0',  'SLi10',  'SNa10',  'MLi10',  'MNa10', 'SNa0', 'SLi0', 'MLi0',  'MNa0', 'SLi5', 'MNa5', 'SNa5', ]           
    piezo_x = [   -44200,    -37600,   -31650,   -24600,   -18000,   -12600,  -5250,    750,   7000,   13500,  20200,  25700,  32100, ]         
    piezo_y = [     6000,      6000,    -6000,    -8100,    -8300,    -8300,  -7300,   1550,  -6500,   -8900,  -7400,  -8500,   1350, ]
    piezo_z = [     9400,      6600,     7000,     5800,     5400,     5400,   5200,   5400,   5600,    5600,   5600,   5600,   5600, ]


    waxs_arc = [0, 20]

    energies = np.concatenate((
        np.arange(2445, 2470, 5),
        np.arange(2470, 2480, 0.25),
        np.arange(2480, 2490, 1),
        np.arange(2490, 2501, 5),
    ))

    user = "BP"
    det_exposure_time(t, t)

    msg = "Wrong number of coordinates"
    assert len(piezo_x) == len(names), msg
    assert len(piezo_x) == len(piezo_y), msg
    assert len(piezo_x) == len(piezo_z), msg

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)
        dets = [pil900KW] if waxs.arc.position < 15 else [pil900KW, pil1M]
        #dets.append(OAV_writing)

        for name, x, y, z, in zip(names, piezo_x, piezo_y, piezo_z):
            yield from bps.mv(piezo.y, y,
                              piezo.x, x,
                              piezo.z, z,
                              )

            for nrg in energies:
                yield from bps.mv(energy, nrg)
                yield from bps.sleep(2)
                if xbpm2.sumX.get() < 50:
                    yield from bps.sleep(2)
                    yield from bps.mv(energy, nrg)
                    yield from bps.sleep(2)

                loc = '00'
                sample_name = f'{name}-escan{get_more_md()}_loc{loc}'
                sample_id(user_name='PW', sample_name=sample_name)
                print(f"\n\n\n\t=== Sample: {sample_name} ===")
                yield from bp.count(dets)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def run_swaxs_2024_1_par3(t=2):
    """
    Take WAXS and SAXS at several sample positions

    Specify central positions on the samples with xlocs and ylocs,
    then offsets from central positions with x_off and y_off.
    """

    names =   [  'mpt1.5', 'mpt1.0',  'SLi10',  'SNa10',  'MLi10',  'MNa10', 'SNa0', 'SLi0', 'MLi0',  'MNa0', 'SLi5', 'MNa5', 'SNa5', ]           
    piezo_x = [   -44100,    -37500,   -31650,   -24600,   -18100,   -12700,  -5650,    600,   6900,   13300,  20200,  25800,  32900, ]         
    piezo_y = [     6000,      6000,    -8100,    -8900,    -8400,    -8800,  -7400,   1650,   7700,    3500,  -7200,  -7200,   1350, ]
    piezo_z = [     6600,      6600,     7000,     6000,     6000,     6000,   6200,   7000,   5600,    5600,   5600,   5600,   5600, ]


    x_off = [ 0 ]
    y_off = [ -100, 0, 100, 200, ]
    waxs_arc = [ 20, 0 ]

    user = "BP"
    det_exposure_time(t, t)

    msg = "Wrong number of coordinates"
    assert len(piezo_x) == len(names), msg
    assert len(piezo_x) == len(piezo_y), msg
    assert len(piezo_x) == len(piezo_z), msg

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)
        dets = [pil900KW] if waxs.arc.position < 15 else [pil900KW, pil1M]
        #dets.append(OAV_writing)

        for name, x, y, z, in zip(names, piezo_x, piezo_y, piezo_z):
            yield from bps.mv(piezo.y, y,
                              piezo.x, x,
                              piezo.z, z,
                              )

            for yy, y_of in enumerate(y_off):
                yield from bps.mv(piezo.y, y + y_of)

                for xx, x_of in enumerate(x_off):
                    yield from bps.mv(piezo.x, x + x_of)
                    
                    loc = f'{xx}{yy}'
                    sample_name = f'{name}{get_scan_md()}_loc{loc}'
                    sample_id(user_name=user, sample_name=sample_name)
                    print(f"\n\n\n\t=== Sample: {sample_name} ===")
                    yield from bp.count(dets)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def grazing_brsc_zinc_2024_2(t=3):
    """
    standard GI-S/WAXS across energies
    """
    
    names   = [    'S01',    'S02',   'S03',   'S04',   'S05',   'S06',  'S07', 'A02', 'A08', 'A11', 'A13', 'A0B', 'A21', 'A81', ]
    piezo_x = [   -55300,   -47000,  -36000,  -38000,  -28000,  -17000,  -6500,  5000, 15000, 26000, 36000, 46000, 45000, 55000, ]
    piezo_y = [     7700,     7700,    7700,    7500,    7500,    7500,   7500,  7100,  7100,  7100,  7100,  7100,  7100,  7100, ]          
    piezo_z = [     2500,     2500,    2500,    2500,    2500,    2500,   2500,  2500,  2500,  2500,  2500,  2500,  2500,  2500, ]
    hexa_x =  [    -11.4,    -11.4,   -11.4,       0,       0,       0,      0,     0,     0,     0,     0,     0,    13,    13, ]
    
    n = 7
    m = 1
    names   = names[m:n]
    piezo_x = piezo_x[m:n]
    piezo_y = piezo_y[m:n]
    piezo_z = piezo_z[m:n]
    hexa_x  = hexa_x[m:n]

    # Energies across Zn K-edge
    energies = [ 9600, 9610, 9620, 9630, 9640, 9650, 9660, 9670, 9680, 9690, 9700]


    msg = "Wrong number of coordinates"
    assert len(piezo_x) == len(names), msg
    assert len(piezo_x) == len(piezo_y), msg
    assert len(piezo_x) == len(piezo_z), msg
    assert len(piezo_x) == len(hexa_x), msg

    waxs_arc = [ 0, 20 ]
    x_off = [0]
    #incident_angles = [ 0.1, 0.2 ]
    #incident_angles = [ 0.05, 0.15, 0.25, 0.5 ]
    incident_angles = [ 0.5 ]
    user_name = 'PW'

    for name, x, y, z, hx in zip(names, piezo_x, piezo_y, piezo_z, hexa_x):

        yield from bps.mv(piezo.x, x,
                          piezo.y, y,
                          piezo.z, z,
                          stage.x, hx)

        # Align the sample
        try:
            yield from alignement_gisaxs(0.1) #0.1 to 0.15
        except:
            #yield from alignement_gisaxs(0.01)
            print('\n\n\n\n\n\n\n\n\n\nCould not align, remeasure!!!\n\n\n\n\n\n\n\n\n\n')

        # Sample flat at ai0
        ai0 = piezo.th.position
        det_exposure_time(t, t)

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)
            dets = [pil900KW] if waxs.arc.position < 15 else [pil900KW, pil1M]

            # problems with the beamstop
            yield from bps.mv(waxs.bs_y, -3)

            for xx, x_of in enumerate(x_off):
                yield from bps.mv(piezo.x, x + x_of)
                for en in energies:
                    
                    yield from bps.mv(energy, en)
                    yield from bps.sleep(3)
                    for ai in incident_angles:
                        yield from bps.mv(piezo.th, ai0 + ai)

                        sample_name = f'{name}{get_scan_md()}_loc{xx}_ai{ai}'

                        sample_id(user_name=user_name, sample_name=sample_name)
                        print(f"\n\n\n\t=== Sample: {sample_name} ===")
                        yield from bp.count(dets)
                yield from bps.mv(energy, energies[0])
                yield from bps.sleep(2)
        yield from bps.mv(piezo.th, ai0)

    sample_id(user_name='test', sample_name='test')
    det_exposure_time(0.5, 0.5)


def grazing_brsc_2024_2(t=1):
    """
    standard GI-S/WAXS
    """
    
    names   = [  'S01',  'S02',  'S03',  'S04',  'S05',  'S06', 'S07','A02', 'A08', 'A11', 'A13', 'A0B', 'A21', 'A81', ]
    piezo_x = [ -55000, -46500, -35500, -37500, -27500, -16500, -6000, 5500, 15500, 26500, 36500, 46500, 45500, 55200, ]
    piezo_y = [   7700,   7700,   7700,   7500,   7500,   7500,  7500, 7100,  7100,  7100,  7100,  7100,  7100,  7100, ]          
    piezo_z = [   2500,   2500,   2500,   2500,   2500,   2500,  2500, 2500,  2500,  2500,  2500,  2500,  2500,  2500, ]
    hexa_x =  [  -11.4,  -11.4,  -11.4,      0,      0,      0,     0,    0,     0,     0,     0,     0,    13,    13, ]
    
    msg = "Wrong number of coordinates"
    assert len(piezo_x) == len(names), msg
    assert len(piezo_x) == len(piezo_y), msg
    assert len(piezo_x) == len(piezo_z), msg
    assert len(piezo_x) == len(hexa_x), msg

    waxs_arc = [ 0, 20 ]
    x_off = [0]
    incident_angles = [ 0.1, 0.2, 0.5 ]
    user_name = 'PW'

    for name, x, y, z, hx in zip(names, piezo_x, piezo_y, piezo_z, hexa_x):

        yield from bps.mv(piezo.x, x,
                          piezo.y, y,
                          piezo.z, z,
                          stage.x, hx)

        # Align the sample
        try:
            yield from alignement_gisaxs(0.1) #0.1 to 0.15
        except:
            yield from alignement_gisaxs(0.01)
            print('\n\n\n\n\n\n\n\n\n\nCould not align, remeasure!!!\n\n\n\n\n\n\n\n\n\n')

        # Sample flat at ai0
        ai0 = piezo.th.position
        det_exposure_time(t, t)

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)
            dets = [pil900KW] if waxs.arc.position < 15 else [pil900KW, pil1M]

            # problems with the beamstop
            yield from bps.mv(waxs.bs_y, -3)

            for xx, x_of in enumerate(x_off):
                yield from bps.mv(piezo.x, x + x_of)
                for ai in incident_angles:
                    yield from bps.mv(piezo.th, ai0 + ai)

                    sample_name = f'{name}{get_scan_md()}_loc{xx}_ai{ai}'

                    sample_id(user_name=user_name, sample_name=sample_name)
                    print(f"\n\n\n\t=== Sample: {sample_name} ===")
                    yield from bp.count(dets)

        yield from bps.mv(piezo.th, ai0)

    sample_id(user_name='test', sample_name='test')
    det_exposure_time(0.5, 0.5)
    proposal_id('2024_2', '000000_tests')


def run_swaxs_2024_2_Paren_tender(t=2):
    """
    Take WAXS and SAXS at several sample positions

    Specify central positions on the samples with xlocs and ylocs,
    then offsets from central positions with x_off and y_off.
    """

    names =   [ 'SLi0-edge', 'SLi10', 'SLi10-edge', 'MNa10', 'MNa10-edge', 'MLi0-edge', 'MLi10-edge', 'MNa0-edge', 'SNa10', 'SNa10-edge', 'SNa0-edge',  'blank', 'darks', ]           
    piezo_x = [       42150,   35600,        36000,   28400,        29900,       22500,        16400,       11200,    5200,         4900,       -3250,    -9300,  -21300, ]         
    piezo_y = [       -5900,   -5900,        -5900,   -5900,        -4900,       -5200,        -5200,       -4700,   -5900,        -5900,       -4750,    -6100,   -6100, ]
    piezo_z = [        2600,    2600,         2600,    2600,         2600,        2600,         2600,        2600,    2600,         2600,        2600,     2600,    2600, ]

    names = names[1:]
    piezo_x = piezo_x[1:]
    piezo_y = piezo_y[1:]
    piezo_z = piezo_z[1:]
    waxs_arc = [0]

    energies = np.concatenate((
        np.arange(2445, 2470, 5),
        np.arange(2470, 2480, 0.25),
        np.arange(2480, 2490, 1),
        np.arange(2490, 2501, 5),
    ))

    user = "BP"
    det_exposure_time(t, t)

    step = 1000 / len(energies)

    msg = "Wrong number of coordinates"
    assert len(piezo_x) == len(names), msg
    assert len(piezo_x) == len(piezo_y), msg
    assert len(piezo_x) == len(piezo_z), msg

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)
        dets = [pil900KW] if waxs.arc.position < 15 else [pil900KW, pil1M]
        #dets.append(OAV_writing)

        for name, x, y, z, in zip(names, piezo_x, piezo_y, piezo_z):
            yield from bps.mv(piezo.y, y,
                              piezo.x, x,
                              piezo.z, z,
                              )

            for i, nrg in enumerate(energies):
                yield from bps.mv(energy, nrg)
                yield from bps.sleep(2)
                if xbpm2.sumX.get() < 50:
                    yield from bps.sleep(2)
                    yield from bps.mv(energy, nrg)
                    yield from bps.sleep(2)
                
                if 'edge' not in name:
                    yield from bps.mv(piezo.y, y + i * step)
                    loc = str(i).zfill(2)
                else:
                    loc = '00'

                sample_name = f'{name}{get_more_md()}_loc{loc}'
                sample_id(user_name=user, sample_name=sample_name)
                print(f"\n\n\n\t=== Sample: {sample_name} ===")
                yield from bp.count(dets)

                if (wa == waxs_arc[0]) and (i == 0):
                    yield from bp.count([OAV_writing])

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def run_swaxs_2024_2_Paren_tender_long_exposure(t=7):
    """
    Take WAXS and SAXS at several sample positions

    Specify central positions on the samples with xlocs and ylocs,
    then offsets from central positions with x_off and y_off.
    """

    names_1   = [ 'SLi0-a', 'SLi0-b', 'SLi0-c',  'SLi10-a', 'SLi10-b', 'SLi10-c',  'MNa10-a', 'MNa10-b', 'MNa10-c', ]
    piezo_x_1 = [    42150,    42150,    43350,      36000,     35900,     35900,      29900,     28400,     29000, ]
    piezo_y_1 = [    -5900,    -4500,    -4500,      -5900,     -5400,     -4600,      -4900,     -5900,     -5000, ]

    names_2   = [ 'MLi0-a', 'MLi0-b', 'MLi0-c',  'MLi10-a', 'MLi10-b', 'MLi10-c',   'MNa0-a',  'MNa0-b',  'MNa0-c', ]
    piezo_x_2 = [    22500,    22500,    23700,      16400,     16400,     17700,      11200,      9900,     11500, ]
    piezo_y_2 = [    -5200,    -4600,    -5400,      -5200,     -4700,     -4700,      -4700,     -4800,     -6200, ]
    
    names_3   = ['SNa10-a','SNa10-b','SNa10-c',   'SNa0-a',  'SNa0-b',  'SNa0-c',    'blank',   'darks', ]
    piezo_x_3 = [     4900,     5200,     5200,      -3250,     -1400,     -1400,      -9300,    -21300, ]
    piezo_y_3 = [    -5900,    -5900,    -5100,      -4750,     -4650,     -4550,      -6100,     -8500, ]
    

    names   =   names_1 +   names_2 +   names_3
    piezo_x = piezo_x_1 + piezo_x_2 + piezo_x_3
    piezo_y = piezo_y_1 + piezo_y_2 + piezo_y_3
    piezo_z = [2600 for n in names]

    waxs_arc = [0, 20]

    energies = [ 2445, 2474, 2476, 2478.25, 2500 ]

    user = "BP"
    det_exposure_time(t, t)


    msg = "Wrong number of coordinates"
    assert len(piezo_x) == len(names), msg
    assert len(piezo_x) == len(piezo_y), msg
    assert len(piezo_x) == len(piezo_z), msg

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)
        dets = [pil900KW] if waxs.arc.position < 15 else [pil900KW, pil1M]
        #dets.append(OAV_writing)

        for name, x, y, z, in zip(names, piezo_x, piezo_y, piezo_z):
            yield from bps.mv(piezo.y, y,
                              piezo.x, x,
                              piezo.z, z,
                              )

            for i, nrg in enumerate(energies):
                yield from bps.mv(energy, nrg)
                yield from bps.sleep(2)
                if xbpm2.sumX.get() < 50:
                    yield from bps.sleep(2)
                    yield from bps.mv(energy, nrg)
                    yield from bps.sleep(2)

                loc = '00'

                sample_name = f'{name}{get_more_md()}_loc{loc}'
                sample_id(user_name=user, sample_name=sample_name)
                print(f"\n\n\n\t=== Sample: {sample_name} ===")
                yield from bp.count(dets)

                if (wa == waxs_arc[0]) and (i == 0):
                    yield from bp.count([OAV_writing])

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def run_swaxs_2024_2_Paren_tender_nexafs(t=2):
    """
    Take WAXS and SAXS at several sample positions

    Specify central positions on the samples with xlocs and ylocs,
    then offsets from central positions with x_off and y_off.
    """

    names_1   = [ 'SLi0-a', 'SLi0-b', 'SLi0-c',  'SLi10-a', 'SLi10-b', 'SLi10-c',  'MNa10-a', 'MNa10-b', 'MNa10-c', ]
    piezo_x_1 = [    42150,    42150,    43350,      36000,     35900,     35900,      29900,     28400,     29000, ]
    piezo_y_1 = [    -5900,    -4500,    -4500,      -5900,     -5400,     -4600,      -4900,     -5900,     -5000, ]

    names_2   = [ 'MLi0-a', 'MLi0-b', 'MLi0-c',  'MLi10-a', 'MLi10-b', 'MLi10-c',   'MNa0-a',  'MNa0-b',  'MNa0-c', ]
    piezo_x_2 = [    22500,    22500,    23700,      16400,     16400,     17700,      11200,      9900,     11500, ]
    piezo_y_2 = [    -5200,    -4600,    -5400,      -5200,     -4700,     -4700,      -4700,     -4800,     -6200, ]
    
    names_3   = ['SNa10-a','SNa10-b','SNa10-c',   'SNa0-a',  'SNa0-b',  'SNa0-c',    'blank',   'darks', ]
    piezo_x_3 = [     4900,     5200,     5200,      -3250,     -1400,     -1400,      -9300,    -21300, ]
    piezo_y_3 = [    -5900,    -5900,    -5100,      -4750,     -4650,     -4550,      -6100,     -6100, ]
    

    names   =   names_1 +   names_2 +   names_3
    piezo_x = piezo_x_1 + piezo_x_2 + piezo_x_3
    piezo_y = piezo_y_1 + piezo_y_2 + piezo_y_3
    piezo_z = [2600 for n in names]

    names = [ n + f'-nexafs' for n in names]

    waxs_arc = [ 60, 0, 20, 40]

    energies = np.concatenate((
        np.arange(2445, 2470, 5),
        np.arange(2470, 2480, 0.25),
        np.arange(2480, 2490, 1),
        np.arange(2490, 2501, 5),
    ))

    user = "BP"
    det_exposure_time(t, t)


    msg = "Wrong number of coordinates"
    assert len(piezo_x) == len(names), msg
    assert len(piezo_x) == len(piezo_y), msg
    assert len(piezo_x) == len(piezo_z), msg

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)
        dets = [pil900KW] if waxs.arc.position < 15 else [pil900KW, pil1M]

        for name, x, y, z, in zip(names, piezo_x, piezo_y, piezo_z):
            
            if ('0-c' not in name) and (wa != waxs_arc[0]):
                print(f'No measurement for {name} at lower angles')
                continue

            else:
            
                yield from bps.mv(
                    piezo.y, y,
                    piezo.x, x,
                    piezo.z, z,
                )

                for i, nrg in enumerate(energies):
                    yield from bps.mv(energy, nrg)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, nrg)
                        yield from bps.sleep(2)

                    loc = '00'

                    sample_name = f'{name}{get_more_md()}_loc{loc}'
                    sample_id(user_name=user, sample_name=sample_name)
                    print(f"\n\n\n\t=== Sample: {sample_name} ===")
                    yield from bp.count(dets)

                    if (wa == waxs_arc[0]) and (i == 0):
                        yield from bp.count([OAV_writing])

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)

def run_tender_overnight_Paren_2024_2():
    '''
    Run overnight all samples across 5 energies,
    then nexafs for all, and 0, 20, 40, for -c samples
    '''
    yield from run_swaxs_2024_2_Paren_tender_long_exposure(t=7)
    yield from run_swaxs_2024_2_Paren_tender_nexafs(t=2)
    print('All done!!!')


def run_swaxs_2024_2_Paren_hard(t=2):
    """
    Take WAXS and SAXS at several sample positions

    Specify central positions on the samples with xlocs and ylocs,
    then offsets from central positions with x_off and y_off.
    """

    names_1   = [ 'SLi0-a', 'SLi0-b', 'SLi0-c',  'SLi10-a', 'SLi10-b', 'SLi10-c',  'MNa10-a', 'MNa10-b', 'MNa10-c', ]
    piezo_x_1 = [    42150,    42150,    43350,      36000,     35900,     35900,      29900,     28400,     29000, ]
    piezo_y_1 = [    -5900,    -4500,    -4500,      -5900,     -5400,     -4600,      -4900,     -5900,     -5000, ]

    names_2   = [ 'MLi0-a', 'MLi0-b', 'MLi0-c',  'MLi10-a', 'MLi10-b', 'MLi10-c',   'MNa0-a',  'MNa0-b',  'MNa0-c', ]
    piezo_x_2 = [    22500,    22500,    23700,      16400,     16400,     17700,      11200,      9900,     11500, ]
    piezo_y_2 = [    -5200,    -4600,    -5400,      -5200,     -4700,     -4700,      -4700,     -4800,     -6200, ]
    
    names_3   = ['SNa10-a','SNa10-b','SNa10-c',   'SNa0-a',  'SNa0-b',  'SNa0-c',    'blank',   'darks', ]
    piezo_x_3 = [     4900,     5200,     5200,      -3250,     -1400,     -1400,      -9300,    -21300, ]
    piezo_y_3 = [    -5900,    -5900,    -5100,      -4750,     -4650,     -4550,      -6100,     -9000, ]
    

    names   =   names_1 +   names_2 +   names_3
    piezo_x = piezo_x_1 + piezo_x_2 + piezo_x_3
    piezo_y = piezo_y_1 + piezo_y_2 + piezo_y_3
    piezo_z = [2600 for n in names]

    user = "BP"
    waxs_arc = [ 0, 20, 40 ]
    det_exposure_time(t, t)


    msg = "Wrong number of coordinates"
    assert len(piezo_x) == len(names), msg
    assert len(piezo_x) == len(piezo_y), msg
    assert len(piezo_x) == len(piezo_z), msg

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)
        dets = [pil900KW] if waxs.arc.position < 15 else [pil900KW, pil1M]

        for name, x, y, z, in zip(names, piezo_x, piezo_y, piezo_z):
            
            
            yield from bps.mv(
                piezo.y, y,
                piezo.x, x,
                piezo.z, z,
            )

            loc = '00'

            sample_name = f'{name}{get_scan_md()}_loc{loc}'
            sample_id(user_name=user, sample_name=sample_name)
            print(f"\n\n\n\t=== Sample: {sample_name} ===")
            yield from bp.count(dets)

            if (wa == waxs_arc[0]) and (i == 0):
                yield from bp.count([OAV_writing])

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def run_swaxs_2024_2_Paren_tender_long_exposure2(t=10):
    """
    Take WAXS and SAXS at several sample positions

    Specify central positions on the samples with xlocs and ylocs,
    then offsets from central positions with x_off and y_off.
    """

    names_1   = [ 'SLi0-a', 'SLi0-b', 'SLi0-c',  'SLi10-a', 'SLi10-b', 'SLi10-c',  'MNa10-a', 'MNa10-b', 'MNa10-c', ]
    piezo_x_1 = [    42150,    42150,    43350,      36000,     35900,     35900,      29900,     28400,     29000, ]
    piezo_y_1 = [    -5900,    -4500,    -4500,      -5900,     -5400,     -4600,      -4900,     -5900,     -5000, ]

    names_2   = [ 'MLi0-a', 'MLi0-b', 'MLi0-c',  'MLi10-a', 'MLi10-b', 'MLi10-c',   'MNa0-a',  'MNa0-b',  'MNa0-c', ]
    piezo_x_2 = [    22500,    22500,    23700,      16400,     16400,     17700,      11200,      9900,     11500, ]
    piezo_y_2 = [    -5200,    -4600,    -5400,      -5200,     -4700,     -4700,      -4700,     -4800,     -6200, ]
    
    names_3   = ['SNa10-a','SNa10-b','SNa10-c',   'SNa0-a',  'SNa0-b',  'SNa0-c',    'blank',   'darks', ]
    piezo_x_3 = [     4900,     5200,     5200,      -3250,     -1400,     -1400,      -9300,    -21300, ]
    piezo_y_3 = [    -5900,    -5900,    -5100,      -4750,     -4650,     -4550,      -6100,     -8500, ]
    

    names   =   names_1 +   names_2 +   names_3
    piezo_x = piezo_x_1 + piezo_x_2 + piezo_x_3
    piezo_y = piezo_y_1 + piezo_y_2 + piezo_y_3
    piezo_z = [2600 for n in names]

    waxs_arc = [0, 20]

    energies = [ 2445, 2474, 2476, 2478.25, 2500 ]

    user = "BP"
    det_exposure_time(t, t)


    msg = "Wrong number of coordinates"
    assert len(piezo_x) == len(names), msg
    assert len(piezo_x) == len(piezo_y), msg
    assert len(piezo_x) == len(piezo_z), msg

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)
        dets = [pil900KW] if waxs.arc.position < 15 else [pil900KW, pil1M]
        #dets.append(OAV_writing)

        for name, x, y, z, in zip(names, piezo_x, piezo_y, piezo_z):

            if '0-a' not in name:
                print(f'No measurement for {name}')
                continue

            yield from bps.mv(piezo.y, y,
                              piezo.x, x,
                              piezo.z, z,
                              )

            for i, nrg in enumerate(energies):
                yield from bps.mv(energy, nrg)
                yield from bps.sleep(2)
                if xbpm2.sumX.get() < 50:
                    yield from bps.sleep(2)
                    yield from bps.mv(energy, nrg)
                    yield from bps.sleep(2)

                loc = '00'

                sample_name = f'{name}{get_more_md()}_loc{loc}'
                sample_id(user_name=user, sample_name=sample_name)
                print(f"\n\n\n\t=== Sample: {sample_name} ===")
                yield from bp.count(dets)

                if (wa == waxs_arc[0]) and (i == 0):
                    yield from bp.count([OAV_writing])

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)

def run_Paren_tender_initial_nexafs(t=2):
    """
    """

    names   = [ 'SNa0-b2', ]# 'SNa0-a1', ]
    piezo_x = [     36300, ]#    36300, ]
    piezo_y = [      5500, ]#     5100,]

    piezo_z = [1000 for n in names]

    #names = [ n + f'-nexafs' for n in names]

    waxs_arc = [ 60 ]

    energies = np.concatenate((
        np.arange(2445, 2470, 5),
        np.arange(2470, 2480, 0.25),
        np.arange(2480, 2490, 1),
        np.arange(2490, 2501, 5),
    ))

    energies = np.concatenate((
        np.arange(2460, 2470, 5),
        np.arange(2470, 2490, 0.25),
        np.arange(2490, 2501, 1),
        #np.arange(2490, 2501, 5),
        ))

    user = "BP"
    det_exposure_time(t, t)


    msg = "Wrong number of coordinates"
    assert len(piezo_x) == len(names), msg
    assert len(piezo_x) == len(piezo_y), msg
    assert len(piezo_x) == len(piezo_z), msg

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)
        dets = [pil900KW] if waxs.arc.position < 15 else [pil900KW, pil1M]

        for name, x, y, z, in zip(names, piezo_x, piezo_y, piezo_z):

            yield from bps.mv(
                piezo.y, y,
                piezo.x, x,
                piezo.z, z,
            )

            for i, nrg in enumerate(energies):
                yield from bps.mv(energy, nrg)
                yield from bps.sleep(2)
                if xbpm2.sumX.get() < 50:
                    yield from bps.sleep(2)
                    yield from bps.mv(energy, nrg)
                    yield from bps.sleep(2)

                loc = '00'

                sample_name = f'{name}{get_more_md()}_loc{loc}'
                sample_id(user_name=user, sample_name=sample_name)
                print(f"\n\n\n\t=== Sample: {sample_name} ===")
                yield from bp.count(dets)

                if (wa == waxs_arc[0]) and (i == 0):
                    yield from bp.count([OAV_writing])

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def run_Paren_tender_2024_3(t=1):
    """
    """

    names_1   = [ 'SLi0-a',  'SNa0-c', 'MLi0-a',  'MNa0-a',  'SLi10-a',  'SNa10-a',    'MLi10-a',  'MNa10-a', ]
    piezo_x_1 = [    41900,     36300,    29400,     23000,      15800,       4200,         7000,       -200, ]
    piezo_y_1 = [     4400,      5800,     4600,      5200,       5500,      -7000,         5500,       5500, ]

    names_2   = [ 'SLi5-a',  'SNa5-a', 'MLi5-a',  'MNa5-a',   'MNa5-b',  'SLi20-a', 'blankSiN-a', 'blankvac', ]
    piezo_x_2 = [    -6200,    -12200,   -18800,    -23400,     -23400,     -30600,       -36600,     -42600, ]
    piezo_y_2 = [     5500,      5200,     5400,      5400,       6400,       5000,         5000,       5200, ]
    
    names   =   names_1 +   names_2
    piezo_x = piezo_x_1 + piezo_x_2
    piezo_y = piezo_y_1 + piezo_y_2
    piezo_z = [1000 for n in names]
    
    waxs_arc = [ 0, 20, 40 ]
    energies = np.concatenate((
        np.arange(2460, 2470, 5),
        np.arange(2470, 2490, 0.5),
        np.arange(2490, 2501, 1),
    ))

    user = "BP"
    det_exposure_time(t, t)

    msg = "Wrong number of coordinates"
    assert len(piezo_x) == len(names), msg
    assert len(piezo_x) == len(piezo_y), msg
    assert len(piezo_x) == len(piezo_z), msg

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)
        dets = [pil900KW] if waxs.arc.position < 15 else [pil900KW, pil1M]

        for name, x, y, z, in zip(names, piezo_x, piezo_y, piezo_z):

            yield from bps.mv(
                piezo.y, y,
                piezo.x, x,
                piezo.z, z,
            )

            for i, nrg in enumerate(energies):
                yield from bps.mv(energy, nrg)
                yield from bps.sleep(2)
                if xbpm2.sumX.get() < 50:
                    yield from bps.sleep(2)
                    yield from bps.mv(energy, nrg)
                    yield from bps.sleep(2)

                loc = '00'

                sample_name = f'{name}{get_more_md()}_loc{loc}'
                sample_id(user_name=user, sample_name=sample_name)
                print(f"\n\n\n\t=== Sample: {sample_name} ===")
                yield from bp.count(dets)

                if (wa == waxs_arc[0]) and (i == 0):
                    yield from bp.count([OAV_writing])

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def run_Paren_tender_darks_2024_3(t=1):
    """
    """

    yield from shclose()
    print('Photo Shutter Closed!')
    yield from bps.sleep(2)

    names   = [ 'darks' ]
    waxs_arc = [ 0, 20, 40 ]
    energies = np.concatenate((
        np.arange(2460, 2470, 5),
        np.arange(2470, 2490, 0.5),
        np.arange(2490, 2501, 1),
    ))

    user = "BP"
    det_exposure_time(t, t)

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)
        dets = [pil900KW] if waxs.arc.position < 15 else [pil900KW, pil1M]

        for name in names:
            for i, nrg in enumerate(energies):
                yield from bps.mv(energy, nrg)
                yield from bps.sleep(2)
                if xbpm2.sumX.get() < 50:
                    yield from bps.sleep(2)
                    yield from bps.mv(energy, nrg)
                    yield from bps.sleep(2)

                loc = '00'
                sample_name = f'{name}{get_more_md()}_loc{loc}'
                sample_id(user_name=user, sample_name=sample_name)
                print(f"\n\n\n\t=== Sample: {sample_name} ===")
                yield from bp.count(dets)

                if (wa == waxs_arc[0]) and (i == 0):
                    yield from bp.count([OAV_writing])

    yield from shopen()
    yield from bps.sleep(2)
    print('Photo Shutter Open!')
    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def run_Paren_tender_overnight_2024_3(t=3):
    """
    """

    names_1   = [ 'SLi0-b',  'SNa0-d', 'MLi0-b',  'MNa0-b',  'SLi10-b',  'SNa10-b',    'MLi10-b',  'MNa10-b', ]
    piezo_x_1 = [    41900,     36300,    29400,     23000,      15800,       4200,         7000,       -200, ]
    piezo_y_1 = [     4900,      6000,     4400,      5400,       5800,      -7200,         5800,       5800, ]

    names_2   = [ 'SLi5-b',  'SNa5-b', 'MLi5-b',  'MNa5-c',     'SLi20-b',  'blankSiN-b', 'blankvac-b', ]
    piezo_x_2 = [    -6200,    -12600,   -18800,    -23400,       -30600,         -36600,       -42600, ]
    piezo_y_2 = [     5800,      5700,     5700,      5700,         5200,           5200,         5200, ]
    

    names   =   names_1 +   names_2
    piezo_x = piezo_x_1 + piezo_x_2
    piezo_y = piezo_y_1 + piezo_y_2
    piezo_z = [1000 for n in names]
    
    waxs_arc = [ 0, 20, 40, 60 ]
    energies = np.concatenate((
        np.arange(2460, 2470, 5),
        np.arange(2470, 2490, 0.5),
        np.arange(2490, 2501, 1),
    ))

    user = "BP"
    det_exposure_time(t, t)

    msg = "Wrong number of coordinates"
    assert len(piezo_x) == len(names), msg
    assert len(piezo_x) == len(piezo_y), msg
    assert len(piezo_x) == len(piezo_z), msg

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)
        dets = [pil900KW] if waxs.arc.position < 15 else [pil900KW, pil1M]

        for name, x, y, z, in zip(names, piezo_x, piezo_y, piezo_z):

            yield from bps.mv(
                piezo.y, y,
                piezo.x, x,
                piezo.z, z,
            )

            for i, nrg in enumerate(energies):
                yield from bps.mv(energy, nrg)
                yield from bps.sleep(2)
                if xbpm2.sumX.get() < 50:
                    yield from bps.sleep(2)
                    yield from bps.mv(energy, nrg)
                    yield from bps.sleep(2)

                loc = '00'

                sample_name = f'{name}{get_more_md()}_loc{loc}'
                sample_id(user_name=user, sample_name=sample_name)
                print(f"\n\n\n\t=== Sample: {sample_name} ===")
                yield from bp.count(dets)

                if (wa == waxs_arc[0]) and (i == 0):
                    yield from bp.count([OAV_writing])

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)

def Paren_overnight_2024_3():
    yield from run_Paren_tender_overnight_2024_3(t=3)
    yield from run_Paren_tender_darks_2024_3(t=3)

def run_Paren_flatfield(t=30):
    """
    """

    name =   'flatfield-MLi10-c-30s'
    x =      7400
    y =      4200
    z =      1000

    wa = 50

    dets = [pil900KW]

    energies = np.concatenate((
        np.arange(2460, 2470, 5),
        np.arange(2470, 2490, 0.5),
        np.arange(2490, 2501, 1),
    ))

    user = "BP"
    det_exposure_time(t, t)

    y_step = 30 #(5800 - 4200) / len(energies)

    yield from bps.mv(
        piezo.y, y,
        piezo.x, x,
        piezo.z, z,
        waxs, wa,
    )

    for i, nrg in enumerate(energies[1:]):
        yield from bps.mv(energy, nrg,
                            piezo.y, y + (i + 1) * y_step)
        yield from bps.sleep(2)
        if xbpm2.sumX.get() < 50:
            yield from bps.sleep(2)
            yield from bps.mv(energy, nrg)
            yield from bps.sleep(2)

        loc = '00'
        sample_name = f'{name}{get_more_md()}_loc{loc}'
        sample_id(user_name=user, sample_name=sample_name)
        print(f"\n\n\n\t=== Sample: {sample_name} ===")
        yield from bp.count(dets)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def run_Paren_hard_2024_3(t=2):
    """
    """

    #names_1   = [ 'C8Br-b1', 'C8Pf6-b1', 'C8OTf-b1', 'C8NTf2-b1',  'BaeS4-b1',  'BaeS3-b1',  'BaeS2-b1', 'BaeS1-b1',  ]
    #piezo_x_1 = [    -4400,      800,       7800,      14600,      24400,      29400,      33400,     37800,  ]
    #piezo_y_1 = [     5600,     5600,       5600,       5600,       5600,       5600,       5000,      5800,  ]

    names_1   = [ 'EmptyCap-c',  'BaeS4RH-c', 'BaeS3RH-c',  'BaeS2RH-c',  'BaeS1RH-c', ]
    piezo_x_1 = [       -12000,        -5600,        1000,         7200,        13400, ]
    piezo_y_1 = [         4000,         4800,        4800,          400,         5000, ]
    
    names_2   = [ ]
    piezo_x_2 = [ ]
    piezo_y_2 = [ ]
    

    names   =   names_1 +   names_2
    piezo_x = piezo_x_1 + piezo_x_2
    piezo_y = piezo_y_1 + piezo_y_2
    piezo_z = [ -500 for n in names ]
    
    waxs_arc = [ 0, 2, 7, 15, 20, ][::-1]
    saxs_only = False

    #y_off = [ 0, ] # 250, 600 ]

    user = "BP"
    det_exposure_time(t, t)

    msg = "Wrong number of coordinates"
    assert len(piezo_x) == len(names), msg
    assert len(piezo_x) == len(piezo_y), msg
    assert len(piezo_x) == len(piezo_z), msg

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)
        dets = [pil900KW] if waxs.arc.position < 14.9 else [pil900KW, pil1M]

        if saxs_only and waxs.arc.position > 14.9:
            dets = [pil1M]

        for name, x, y, z, in zip(names, piezo_x, piezo_y, piezo_z):

            yield from bps.mv(
                piezo.y, y + 100,
                piezo.x, x,
                piezo.z, z,
            )

            #for yy, y_of in enumerate(y_off):
            #    yield from bps.mv(piezo.y, y + y_of)

            loc = f'00'
            sample_name = f'{name}{get_more_md()}_loc{loc}'
            sample_id(user_name=user, sample_name=sample_name)
            print(f"\n\n\n\t=== Sample: {sample_name} ===")
            yield from bp.count(dets)

            if (wa == waxs_arc[0]):# and (i == 0):
                yield from bp.count([OAV_writing])

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)

def grazing(t=0.5):
    """
    standard GI-S/WAXS on double stack holder
    """
    """
    # Top sample bar O1, to be measured, position needs to be checked
    names_1   = ['H400nmTcom16-minus42C-b801-85C', 'H400nmTcom16-minus42C-b849-110C', 'H400nmTcom16-minus42C-b897-160C', 'H400nmTcom16-minus42C-b996-60C', 'H400nmTcom16-minus42C-b948-40C', 'H400nmTcom16-minus42C-b995-60C', 'H400nmTcom16-minus42C-B270-110C', 'H400nmTcom16-minus42C-b1062-RT','H400nmTcom15-minus9C-b848-110C', 'H400nmTcom15-minus9C-b993-60C', 'H400nmTcom15-minus9C-b994-60C', 'H400nmTcom15-minus9C-b1061-RT', 'OG-600nm-b1077-RT-20240725',] 
    piezo_x_1 = [                          -54000,                            -43000,                            -32000,                           -21000,                           -10000,                             2000,                             13000,                            24000,                           35000,                           46000,                           36000,                           48000,                        52000,]
    piezo_y_1 = [ -3500 for n1 in names_1]          
    piezo_z_1 = [  7000 for n1 in names_1]
    hexa_x_1 =  [                             -12,                               -12,                               -12,                              -12,                              -12,                              -12,                               -12,                              -12,                             -12,                             -12,                              10,                              10,                           14,]

    # Bottom sample bar O1, to be measured, position needs to be checked
    names_2   = ['Tcom16-minus42C-b1135-85C', 'Tcom16-minus42C-b1098-110C', 'Tcom16-minus42C-b1105-160C','Tcom16-minus42C-b1029-60C', 'Tcom16-minus42C-b1128-60C', 'Tcom16-minus42C-b1145-RT', 'Tcom16-minus42C-B311-110C', 'Tcom16-minus42C-b1118-40C', 'Tcom15-minus9C-b1097-110C','Tcom15-minus9C-b1028-60C', 'Tcom15-minus9C-b1144-RT', 'Tcom15-minus9C-b1117-40C',]
    piezo_x_2 = [                     -50000,                       -38000,                       -26000,                     -15000,                       -4000,                       7000,                       18000,                       29000,                       41000,                     31000,                     45000,                      56000,]
    piezo_y_2 = [  5000 for n2 in names_2]          
    piezo_z_2 = [   500 for n2 in names_2]
    hexa_x_2 =  [                        -12,                          -12,                          -12,                        -12,                         -12,                        -12,                         -12,                         -12,                         -12,                        10,                        10,                         10,]
    
    names   = names_1   + names_2
    piezo_x = piezo_x_1 + piezo_x_2
    piezo_y = piezo_y_1 + piezo_y_2
    piezo_z = piezo_z_1 + piezo_z_2
    hexa_x  = hexa_x_1  + hexa_x_2

    names = [ '20240620-245nm-O1-' + n for n in names]
    """
    # Top sample bar P, to be measured, position needs to be checked
    names_1   = ['Tcom15-minus9C-b794-85C', 'Tcom15-minus9C-b890-160C', 'Tcom15-minus9C-b938-40C', 'Tcom15-minus9C-B263-110C', 'Tcom14-27C-b889-160C', 'Tcom14-27C-b793-85C', 'Tcom14-27C-B262-110C', 'Tcom14-27C-b937-40C','Tcom14-27C-b1036-RT', 'Tcom14-27C-b841-110C', 'Tcom14-27C-b985-60C', 'Tcom14-27C-b1037-RT', 'minus9C-180nm-B307-110C-20240606',] 
    piezo_x_1 = [                   -54000,                     -43000,                    -32000,                     -21000,                 -10000,                  2000,                  13000,                 24000,                35000,                  46000,                 36000,                 48000,                              55000,]
    piezo_y_1 = [ -3500 for n1 in names_1]          
    piezo_z_1 = [  6000 for n1 in names_1]
    hexa_x_1 =  [                      -12,                        -12,                       -12,                        -12,                    -12,                   -12,                    -12,                   -12,                  -12,                    -12,                    10,                    10,                                 10,]

    # Bottom sample bar P, to be measured, position needs to be checked
    names_2   = ['Tcom16-minus42C-b795-85C', 'Tcom16-minus42C-b843-110C', 'Tcom16-minus42C-b891-160C','Tcom16-minus42C-b1041-RT', 'Tcom16-minus42C-b939-40C', 'Tcom16-minus42C-b1140-RT', 'Tcom16-minus42C-B264-110C', 'Tcom16-minus42C-b987-60C', 'Tcom15-minus9C-b842-110C','OG-Tcom15-minus9C-b1038-RT', 'Tcom15-minus9C-b1039-RT', 'Tcom15-minus9C-b986-60C',]
    piezo_x_2 = [                    -50000,                      -38000,                      -26000,                    -15000,                      -4000,                       7000,                       18000,                      29000,                      41000,                       31000,                     45000,                     56000,]
    piezo_y_2 = [  5000 for n2 in names_2]          
    piezo_z_2 = [   500 for n2 in names_2]
    hexa_x_2 =  [                       -12,                         -12,                         -12,                       -12,                        -12,                        -12,                         -12,                        -12,                        -12,                          10,                        10,                        10,]
    
    names   = names_1   + names_2
    piezo_x = piezo_x_1 + piezo_x_2
    piezo_y = piezo_y_1 + piezo_y_2
    piezo_z = piezo_z_1 + piezo_z_2
    hexa_x  = hexa_x_1  + hexa_x_2

    names = [ '20240605-50nm-P-' + n for n in names]
    

    # Starting from ith sample
    i = 0
    names   = names[i:]
    piezo_x = piezo_x[i:]
    piezo_y = piezo_y[i:]
    piezo_z = piezo_z[i:]
    hexa_x =  hexa_x[i:]

    msg = "Wrong number of coordinates"
    assert len(piezo_x) == len(names), msg
    assert len(piezo_x) == len(piezo_y), msg
    assert len(piezo_x) == len(piezo_z), msg
    assert len(piezo_x) == len(hexa_x), msg

    waxs_arc = [ 0, 2, 7 ]
    x_off = [0]
    incident_angles = [ 0.10, 0.25 ]
    user_name = 'TT'

    det_exposure_time(t, t)

    bp_pos_x = 1.95


    try:
        misaligned_samples = RE.md['misaligned_samples']
    except:
        misaligned_samples = []
        RE.md['misaligned_samples'] = misaligned_samples


    for name, x, y, z, hx in zip(names, piezo_x, piezo_y, piezo_z, hexa_x):

        yield from bps.mv(piezo.x, x,
                          piezo.y, y,
                          piezo.z, z,
                          stage.x, hx)

        # Align the sample
        try:
            yield from alignement_gisaxs_doblestack(0.1)
        except:
            misaligned_samples.append(name)
            RE.md['misaligned_samples'] = misaligned_samples

        # Sample flat at ai0
        ai0 = piezo.th.position
        yield from bps.mv(pil1m_bs_rod.x, bp_pos_x)

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)
            dets = [pil900KW] if waxs.arc.position < 15 else [pil900KW, pil1M]

            # problems with the beamstop
            yield from bps.mv(waxs.bs_y, -3)

            for ai in incident_angles:
                yield from bps.mv(piezo.th, ai0 + ai)

                sample_name = f'{name}{get_scan_md()}_ai{ai}'

                sample_id(user_name=user_name, sample_name=sample_name)
                print(f"\n\n\n\t=== Sample: {sample_name} ===")
                yield from bp.count(dets)

        yield from bps.mv(piezo.th, ai0)

    sample_id(user_name='test', sample_name='test')
    det_exposure_time(0.5, 0.5)

def get_scan_time(scan_id=-1):
    """
    from databroker import Broker
    db = Broker.named('smi')
    """

    h = db[scan_id]

    tpp = (h.stop['time'] - h.start['time']) / h.start['num_points']

    return tpp

def overnight_mapping(t=0.5):
    """
    two samples 700 x 700
    """

    names =   [   'N4',    'N2'    ]
    piezo_x = [ -29910,   -16560,  ]
    piezo_y = [   1340,      920,  ]
    piezo_z = [    700,      700,  ]

    msg = "Wrong number of coordinates"
    assert len(piezo_x) == len(names), msg
    assert len(piezo_x) == len(piezo_y), msg
    assert len(piezo_x) == len(piezo_z), msg

    waxs_arc = [ 20, 0 ]
    det_exposure_time(t, t)

    for name, x, y, z in zip(names, piezo_x, piezo_y, piezo_z):

        yield from bps.mv(
            piezo.x, x,
            piezo.y, y,
            piezo.z, z,
        )

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)
            dets = [pil900KW] if waxs.arc.position < 14.9 else [pil900KW, pil1M]
            dets.append(OAV_writing)
            sample_name = f'{name}{get_scan_md()}'
            sample_id(user_name='PW', sample_name=sample_name)
            print(f"\n\n\n\t=== Sample: {sample_name} ===")
            
            yield from bp.rel_grid_scan(dets, piezo.y, -350, 350, 291,  piezo.x, -350, 350, 29, 0)

    sample_id(user_name='test', sample_name='test')
    det_exposure_time(0.5, 0.5)
    
def overday_mapping(t=2):
    """
    two samples 400 x 400
    """

    names =   [   'N4',    'N2',   'bkg-N4',   'bkg-2', ]
    piezo_x = [ -29780,   -16240,    -28380,    -14440, ]
    piezo_y = [  -3900,    -4340,     -3800,     -4380, ]
    piezo_z = [   1420,     1400,      1420,      1400, ]

    msg = "Wrong number of coordinates"
    assert len(piezo_x) == len(names), msg
    assert len(piezo_x) == len(piezo_y), msg
    assert len(piezo_x) == len(piezo_z), msg

    waxs_arc = [ 0 , 20]
    det_exposure_time(t, t)

    for name, x, y, z in zip(names, piezo_x, piezo_y, piezo_z):

        yield from bps.mv(
            piezo.x, x,
            piezo.y, y,
            piezo.z, z,
        )

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)
            dets = [pil900KW] if waxs.arc.position < 14.9 else [pil900KW, pil1M]
            
            sample_name = f'{name}_{get_scan_md()}'
            sample_id(user_name='PW', sample_name=sample_name)
            print(f"\n\n\n\t=== Sample: {sample_name} ===")
            
            if 'bkg' not in name:
                yield from bp.rel_grid_scan(dets, piezo.y, -200, 200, 161,  piezo.x, -200, 200, 17, 0)
            else:
                yield from bp.rel_grid_scan(dets, piezo.y, -100, 100, 11,  piezo.x, -100, 100, 11, 0)

    sample_id(user_name='test', sample_name='test')
    det_exposure_time(0.5, 0.5)

def overnight_mapping(t=1):
    """
    two samples 400 x 400
    """

    names =   [   'N4',    'bkg-N4',   ]
    piezo_x = [ -29780,     -28380,    ]
    piezo_y = [  -3900,       -3800,   ]
    piezo_z = [   1420,       1420,    ]

    msg = "Wrong number of coordinates"
    assert len(piezo_x) == len(names), msg
    assert len(piezo_x) == len(piezo_y), msg
    assert len(piezo_x) == len(piezo_z), msg

    waxs_arc = [ 0 , 20]
    det_exposure_time(t, t)

    for name, x, y, z in zip(names, piezo_x, piezo_y, piezo_z):

        yield from bps.mv(
            piezo.x, x,
            piezo.y, y,
            piezo.z, z,
        )

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)
            dets = [pil900KW] if waxs.arc.position < 14.9 else [pil900KW, pil1M]
            
            sample_name = f'{name}_{get_scan_md()}'
            sample_id(user_name='PW', sample_name=sample_name)
            print(f"\n\n\n\t=== Sample: {sample_name} ===")
            
            if 'bkg' not in name:
                yield from bp.rel_grid_scan(dets, piezo.y, -350, 350, 281,  piezo.x, -350, 350, 29, 0)
            else:
                yield from bp.rel_grid_scan(dets, piezo.y, -100, 100, 11,  piezo.x, -100, 100, 11, 0)

    sample_id(user_name='test', sample_name='test')
    det_exposure_time(0.5, 0.5)
    
    
def take_bkg(name='bkg4-N2', t=2):
    waxs_arc = [ 0 ]#, 20]
    det_exposure_time(t, t)

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)
        dets = [pil900KW] if waxs.arc.position < 14.9 else [pil900KW, pil1M]
        
        sample_name = f'{name}_{get_scan_md()}'
        sample_id(user_name='PW', sample_name=sample_name)
        print(f"\n\n\n\t=== Sample: {sample_name} ===")

        yield from bp.rel_grid_scan(dets, piezo.y, -100, 100, 11,  piezo.x, -100, 100, 11, 0)

    sample_id(user_name='test', sample_name='test')
    det_exposure_time(0.5, 0.5)

def rh(prefix='_RH'):
    rh  = str(np.round(readHumidity(verbosity=0), 2)).zfill(4)
    return f'{prefix}{rh}'


def run_Ray_swaxs_2024_3(t=1):
    """
    SWAXS on humidity cell point
    Make sample names unique for each scan point
    """

    names =   ['CEC-Anneal','CEC-WT','CEC-L44A',]
    #stage_x = [ -7.4 , -1.0, 5.3,]
    #stage_x = [-13.7 , -7.4 , -1.0, 5.3, 11.6, 17.9, 24.3, 30.548]
    # stage-x limits = [-10, 25] 
    #stage_x = [ -0.9, 5.6, 11.8, 18.1]
    stage_x = [ -0.9, 5.6, 11.8]

    #stage_y = [   2.2,     2.2, ]
    stage_y = [ 2.2 for n in names]
    

    msg = "Wrong number of coordinates"
    assert len(stage_x) == len(names), msg
    assert len(stage_x) == len(stage_y), msg

    #waxs_arc = [ 0 , 20]
    waxs_arc = [ 0 ]
    #use just [0] if we just want to run quick WAXS with no SAXS

    det_exposure_time(t, t)

    for name, x, y in zip(names, stage_x, stage_y):
        
        rh_val = rh()
        yield from bps.mv(
            stage.x, x,
            stage.y, y,
        )

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)
            dets = [pil900KW] if waxs.arc.position < 14.9 else [pil900KW, pil1M]

            sample_name = f'{name}{rh_val}{get_scan_md()}'
            sample_id(user_name='RT', sample_name=sample_name)
            print(f"\n\n\n\t=== Sample: {sample_name} ===")
            yield from bp.count(dets)

    sample_id(user_name='test', sample_name='test')
    det_exposure_time(0.5, 0.5)


def run_Ray_swaxs_2024_3_single(t=1):
    """
    SWAXS on humidity cell point
    Make sample names unique for each scan point
    """

    # names =   ['LP-Can-XT-UnT-a', 'LP-Can-XT-MeOH-a', 'LP-Can-T-UnT-a','LP-Can-T-MeOH-a','LP-Can-M-UnT-a','LP-Can-M-MeOH-a','LP-Can-S-UnT-a','LP-Can-S-MeOH-a', ]
    # stage_x = [-13.7 , -7.4 , -1.0, 5.3, 11.6, 17.9, 24.3, 30.548]
    names =   ['LP-Can-S-MeOH-a' ]
    stage_x = [30.548]
    #stage_y = [   2.2,     2.2, ]
    stage_y = [ 2.2 for n in names]
    

    msg = "Wrong number of coordinates"
    assert len(stage_x) == len(names), msg
    assert len(stage_x) == len(stage_y), msg

    waxs_arc = [ 0 , 20]
    #waxs_arc = [ 0 ]
    #use this if we just want to run quick WAXS with no SAXS

    det_exposure_time(t, t)

    for name, x, y in zip(names, stage_x, stage_y):
        
        rh_val = rh()
        # yield from bps.mv(
        #     # stage.x, x,
        #     stage.y, y,
        # )

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)
            dets = [pil900KW] if waxs.arc.position < 14.9 else [pil900KW, pil1M]

            sample_name = f'{name}{rh_val}{get_scan_md()}'
            sample_id(user_name='RT', sample_name=sample_name)
            print(f"\n\n\n\t=== Sample: {sample_name} ===")
            yield from bp.count(dets)

    sample_id(user_name='test', sample_name='test')
    det_exposure_time(0.5, 0.5)


def andrew_mapping_2025_1(t=3):
    """
    Grid mapping on samples
    """
    names =   [         'Claw',        'bkg-Claw',          'Club1',      'bkg-Club1',         'Chitin',         'Club2',       'bkg-Club2', ]
    piezo_x = [          23500,             24250,            -2230,            -2980,            42450,           13790,             14540, ]
    piezo_y = [           -570,              -570,              110,              110,             -650,            -260,              -260, ]
    piezo_z = [           9800,              9800,             9800,             9800,             9400,            9800,              9800, ]

    y_range = [[-375, 375, 301], [-125, 125,  11], [-175, 175, 141], [-125, 125,  11], [-125, 125,  21], [-175, 175, 141], [-125, 125,  11], ]
    x_range = [[-250, 250,  21], [-125, 125,  11], [-175, 175,  15], [-125, 125,  11], [-125, 125,  11], [-150, 150,  13], [-125, 125,  11], ]
    

    msg = "Wrong number of coordinates"
    assert len(piezo_x) == len(names), msg
    assert len(piezo_x) == len(piezo_y), msg
    assert len(piezo_x) == len(piezo_z), msg
    assert len(piezo_x) == len(y_range), msg
    assert len(piezo_x) == len(x_range), msg

    waxs_arc = [ 0 ]
    det_exposure_time(t, t)

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)
        dets = [pil900KW] if waxs.arc.position < 14.9 else [pil900KW, pil1M]

        for name, x, y, z, y_r, x_r in zip(names, piezo_x, piezo_y, piezo_z, y_range, x_range):

            yield from bps.mv(
                piezo.x, x,
                piezo.y, y,
                piezo.z, z,
            )

            sample_name = f'{name}_{get_scan_md()}'
            sample_id(user_name='AN', sample_name=sample_name)
            print(f"\n\n\n\t=== Sample: {sample_name} ===")

            yield from bp.rel_grid_scan(dets, piezo.y, *y_r, piezo.x, *x_r, 0)
            
            sample_id(user_name='test', sample_name='test')
    det_exposure_time(0.5, 0.5)


def run_Paren_tender_overnight_2025_1(t=2):
    """
    """

    names_1   = [ 'MNa20', 'MLi20', 'SNa20', 'SLi20', 'MNa10r', 'MLi10r', 'SLi5', 'vacuum', ]
    piezo_x_1 = [  -13700,   -9600,   -3600,    1600,     6800,    12000,  21800,    35800, ]
    piezo_y_1 = [   -5700,   -5800,   -5600,   -6600,    -7150,    -6500,  -6900,    -6650, ]

    names_2   = [  'SiN', 'SNa10-0.5k', 'SNa10-2.0k', 'MNa10', 'MLi10', 'SNa10', 'SLi10', 'MNa5', 'MLi5', 'SNa5', 'MNa0', 'MLi0', 'SNa0', ] 
    piezo_x_2 = [ -34200,       -26500,       -19000,  -14800,   -8700,   -4100,    1300,   6900,  11900,  16900,  27100,  31800,  36800, ]
    piezo_y_2 = [   5950,         6150,         6100,    5850,    5800,    6000,    5750,   5750,   5800,   5650,   5900,   6100,   6100, ]
    

    names   =   names_1 +   names_2
    piezo_x = piezo_x_1 + piezo_x_2
    piezo_y = piezo_y_1 + piezo_y_2
    piezo_z = [ 3600 for n in names ]
    
    waxs_arc = [ 0, 20, 40 ]
    energies = np.concatenate((
        np.arange(2460, 2470, 5),
        np.arange(2470, 2490, 0.5),
        np.arange(2490, 2511, 1),
    ))

    step_y = 15
    user = "BP"
    det_exposure_time(t, t)

    msg = "Wrong number of coordinates"
    assert len(piezo_x) == len(names), msg
    assert len(piezo_x) == len(piezo_y), msg
    assert len(piezo_x) == len(piezo_z), msg

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)
        dets = [pil900KW] if waxs.arc.position < 15 else [pil900KW, pil1M]

        for name, x, y, z, in zip(names, piezo_x, piezo_y, piezo_z):

            yield from bps.mv(
                piezo.y, y,
                piezo.x, x,
                piezo.z, z,
            )

            for i, nrg in enumerate(energies):
                yield from bps.mv(energy, nrg)
                yield from bps.mv(piezo.y, y + i * step_y)
                yield from bps.sleep(2)
                if xbpm2.sumX.get() < 50:
                    yield from bps.sleep(2)
                    yield from bps.mv(energy, nrg)
                    yield from bps.sleep(2)

                loc = '00'

                sample_name = f'{name}{get_more_md()}_loc{loc}'
                sample_id(user_name=user, sample_name=sample_name)
                print(f"\n\n\n\t=== Sample: {sample_name} ===")
                yield from bp.count(dets)

                #if (wa == waxs_arc[0]) and (i == 0):
                #    yield from bp.count([OAV_writing])

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)

def run_Paren_flatfield_2025_1(t=10):
    """
    """

    name =   'flatfield-MNa20-30s'
    x =      -14900
    y =      -5600
    z =       3600

    wa = 50

    dets = [pil900KW]

    energies = np.concatenate((
        np.arange(2460, 2470, 5),
        np.arange(2470, 2490, 0.5),
        np.arange(2490, 2511, 1),
    ))

    user = "BP"
    det_exposure_time(t, t)

    y_step = 15 #(5800 - 4200) / len(energies)

    yield from bps.mv(
        piezo.y, y,
        piezo.x, x,
        piezo.z, z,
        waxs, wa,
    )

    for i, nrg in enumerate(energies):
        yield from bps.mv(
            energy, nrg,
            piezo.y, y + i  * y_step,
            )
        yield from bps.sleep(2)
        if xbpm2.sumX.get() < 50:
            yield from bps.sleep(2)
            yield from bps.mv(energy, nrg)
            yield from bps.sleep(2)

        loc = '00'
        sample_name = f'{name}{get_more_md()}_loc{loc}'
        sample_id(user_name=user, sample_name=sample_name)
        print(f"\n\n\n\t=== Sample: {sample_name} ===")
        yield from bp.count(dets)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)
    yield from bps.mv(waxs, 0)

def run_scans_Paren_2025_1():
    yield from run_Paren_tender_overnight_2025_1(t=2)
    yield from run_Paren_flatfield_2025_1(t=30)

def run_Paren_hard_2025_1(t=5):
    """
    """

    names_1   = [ 'MNa20-b', 'MLi20-b', 'SNa20-b', 'SLi20-b', 'MNa10r-b', 'MLi10r-b', 'SLi5-b', 'vacuum', ]
    piezo_x_1 = [   -14600,      -9200,     -3200,      2000,       7300,      12400,    22200,    35800, ]
    piezo_y_1 = [    -5550,      -5800,     -5800,     -5800,      -6400,      -6400,    -6400,    -6650, ]

    names_2   = [ 'MNa20-c', 'MLi20-c', 'SNa20-c', 'SLi20-c', 'MNa10r-c', 'MLi10r-c', 'SLi5-c', 'vacuum', ]
    piezo_x_2 = [  -14600,       -9200,     -3200,      2000,       7300,      12400,    22200,    35800, ]
    piezo_y_2 = [   -5500,       -5750,     -5750,     -5750,      -6350,      -6350,    -6350,    -6650, ]

    names_3   = [  'SiN-b', 'SNa10-0.5k-b', 'SNa10-2.0k-b', 'MNa10-b', 'MLi10-b', 'SNa10-b', 'SLi10-b', 'MNa5-b', 'MLi5-b', 'SNa5-b', 'MNa0-b', 'MLi0-b', 'SNa0-b', 'SLi0-b', ] 
    piezo_x_3 = [   -33800,         -26100,         -19500,    -14000,     -9700,     -3600,    1900,       7500,    12400,    17400,  27800,      33000,    38000,    43400, ]
    piezo_y_3 = [     6100,           6100,           6100,      6100,      6100,      6100,    6100,       6100,     6100,     6100,   6100,       7100,     7100,     5900, ]
    
    names_4   = [  'SiN-c', 'SNa10-0.5k-c', 'SNa10-2.0k-c', 'MNa10-c', 'MLi10-c', 'SNa10-c', 'SLi10-c', 'MNa5-c', 'MLi5-c', 'SNa5-c', 'MNa0-c', 'MLi0-c', 'SNa0-c', 'SLi0-c', ] 
    piezo_x_4 = [   -34200,         -26100,         -19500,    -14000,     -9700,     -3600,    1900,       7500,    12400,    17400,  27800,      33300,    38000,    42700, ]
    piezo_y_4 = [     6150,           6150,           6150,      6150,      6150,      6150,    6150,       6150,     6150,     6150,   7500,       7150,     7150,     5850, ]
    

    names   =   names_1 +   names_2 +   names_3 +   names_4
    piezo_x = piezo_x_1 + piezo_x_2 + piezo_x_3 + piezo_x_4
    piezo_y = piezo_y_1 + piezo_y_2 + piezo_y_3 + piezo_y_4
    piezo_z = [ 3600 for n in names ]
    
    waxs_arc = [ 0, 20, 40 ]

    user = "BP"
    det_exposure_time(t, t)

    msg = "Wrong number of coordinates"
    assert len(piezo_x) == len(names), msg
    assert len(piezo_x) == len(piezo_y), msg
    assert len(piezo_x) == len(piezo_z), msg

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)
        dets = [pil900KW] if waxs.arc.position < 14.9 else [pil900KW, pil1M]

        for name, x, y, z, in zip(names, piezo_x, piezo_y, piezo_z):

            yield from bps.mv(
                piezo.y, y,
                piezo.x, x,
                piezo.z, z,
            )
            loc = f'00'

            sample_name = f'{name}{get_scan_md()}_loc{loc}'
            sample_id(user_name=user, sample_name=sample_name)
            print(f"\n\n\n\t=== Sample: {sample_name} ===")
            yield from bp.count(dets)


    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)

def run_Paren_flatfield_hard_2025_1(t=30):
    """
    """

    name =   'flatfield-SNa0-30s'
    x =      37400
    y =       6700
    z =       3600

    wa = 50

    dets = [pil900KW, pil1M]

    user = "BP"
    det_exposure_time(t, t)


    yield from bps.mv(
        piezo.y, y,
        piezo.x, x,
        piezo.z, z,
        waxs, wa,
    )

    loc = '00'
    sample_name = f'{name}{get_scan_md()}_loc{loc}'
    sample_id(user_name=user, sample_name=sample_name)
    print(f"\n\n\n\t=== Sample: {sample_name} ===")
    yield from bp.count(dets)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)
    yield from bps.mv(waxs, 0)

def run_scans_hard_Paren_2025_1():
    yield from run_Paren_hard_2025_1(t=5)
    yield from run_Paren_flatfield_hard_2025_1()


def overnight_mapping_Das_2025_1(t=2):
    """
    SAXS is the priority, 300x300, 61(y) x 13(x)

    """

    names =   [   'S1',   'S2',   'S3',   'S4',  'S5',  'S6',  'S7',  'bkg', ]
    piezo_x = [ -39000, -28000,  14000,   2000, 15000, 28000, 41000,  45000, ]
    piezo_y = [    500,    500,    500,    500,   500,   600,   900,    900, ]
    piezo_z = [   3700,   3700,   3700,   3700,  3700,  3700,  3700,   3700, ]

    msg = "Wrong number of coordinates"
    assert len(piezo_x) == len(names), msg
    assert len(piezo_x) == len(piezo_y), msg
    assert len(piezo_x) == len(piezo_z), msg

    waxs_arc = [ 20 , 0]
    det_exposure_time(t, t)

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)
        dets = [pil900KW] if waxs.arc.position < 14.9 else [pil900KW, pil1M]
        
        # Get xbpm3
        dets.append(xbpm3.sumX)

        for name, x, y, z in zip(names, piezo_x, piezo_y, piezo_z):

            yield from bps.mv(
                piezo.x, x,
                piezo.y, y,
                piezo.z, z,
            )

            sample_name = f'{name}_{get_scan_md()}'
            sample_id(user_name='SD', sample_name=sample_name)
            print(f"\n\n\n\t=== Sample: {sample_name} ===")
            
            if 'bkg' not in name:
                yield from bp.rel_grid_scan(dets, piezo.y, -150, 150, 61,  piezo.x, -150, 150, 13, 0)
            else:
                yield from bp.rel_grid_scan(dets, piezo.y, -100, 100, 11,  piezo.x, -100, 100, 11, 0)

    sample_id(user_name='test', sample_name='test')
    det_exposure_time(0.5, 0.5)


def insitu_mapping_Das_2025_1(t=1, waxs_only=False):
    """
    WAXS or SAXS/WAXS at once, 300x300, 61(y) x 13(x)

    """
    # Sample name and coordinates
    
    name = 'BKG-Air'
    x =    -6300
    y =     2200
    z =     -800

    x_offset = 300
    extra_exposure = 5

    if waxs_only:
        waxs_arc = [ 0 ]
    else:
        waxs_arc = [ 15 ]
    
    det_exposure_time(t, t)

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)
        dets = [pil900KW] if waxs.arc.position < 14.9 else [pil900KW, pil1M]
        
        # Get xbpm3
        dets.append(xbpm3.sumX)

        yield from bps.mv(
            piezo.x, x,
            piezo.y, y,
            piezo.z, z,
            )

        sample_name = f'{name}_{get_scan_md()}'
        sample_id(user_name='SD', sample_name=sample_name)
        print(f"\n\n\n\t=== Sample: {sample_name} ===")
            
        if 'fgk' not in name:
            yield from bp.rel_grid_scan(dets, piezo.y, -2, 2, 3,  piezo.x, -2, 2, 3, 0)
        else:
            yield from bp.rel_grid_scan(dets, piezo.y, -100, 100, 11,  piezo.x, -100, 100, 11, 0)

        
        # # Do a single WAXS + SAXS scan at the end
        waxs_arc_single = [20, 0]
        for wa in waxs_arc_single:
            det_exposure_time(extra_exposure, extra_exposure)

            yield from bps.mv(waxs, wa)
            yield from bps.mv(piezo.x, x + x_offset)

            dets = [pil900KW] if waxs.arc.position < 14.9 else [pil900KW, pil1M]
            dets.append(xbpm3.sumX)

            sample_name = f'{name}-single{get_scan_md()}'
            sample_id(user_name='SD', sample_name=sample_name)
            print(f"\n\n\n\t=== Sample: {sample_name} ===")
            yield from bp.count(dets)
        
        # move back to sample
        yield from bps.mv(
            piezo.x, x,
            piezo.y, y,
            piezo.z, z,
            waxs, waxs_arc[0],
        )


    sample_id(user_name='test', sample_name='test')
    det_exposure_time(0.5, 0.5)


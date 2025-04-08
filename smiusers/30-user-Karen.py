def get_positions():
    """
    Create a string with scan metadata
    """
    
    # Metadata
    x = piezo.x.position
    y = piezo.y.position
    z = piezo.z.position
    th = piezo.th.position
    temp = ls.input_A.get() - 273.15

    
    x = str(np.round(float(x), 0)).zfill(5)
    y = str(np.round(float(y), 0)).zfill(5)
    z = str(np.round(float(z), 0)).zfill(5)
    th = str(np.round(float(th), 4)).zfill(0)
    temp = str(np.round(float(temp), 1)).zfill(5)
   
    return f'x={x}_y={y}_z={z}_th={th}_temp{temp}degC'


def name_sample(name, tstamp):
    """
    Create sample name with metadata

    Args:
        name (str): sample name
        tstamp (time): referenced start time created separately as
            tstamp = time.time()
    """

    eplased = time.time() - tstamp
    sample_name = f'{name}{get_scan_md()}_t{eplased:.1f}_{get_positions()}'
    sample_id(user_name='YCK', sample_name=sample_name)
    print(sample_name)

def take_data_manually(name, t=2):
    """
    """
    try:
        tstamp = RE.md['tstamp']
    except:
        tstamp = time.time()
        RE.md['tstamp'] = tstamp
    name_sample(name, tstamp)

    det_exposure_time(t, t)
    yield from bp.count([pil900KW])


def create_timestamp():
    """
    store in RE.md and print
    """
    RE.md['tstamp'] = time.time()
    print('\nTime stamp created in RE.md')
    tstamp = RE.md['tstamp']
    print(f'tstamp: {tstamp}')


def continous_run(sname='test', t=2, wait=8, frames=2160):
    """
    Take data continously
    
    Create timestamp in BlueSky before running this function as
    create_timestamp()

    Args:
        sname (str): basic sample name,
        t (float): camera exposure time is seconds,
        wait (float): delay between frames,
        frames(int): number of frames to take
    """
    try:
        tstamp = RE.md['tstamp']
    except:
        tstamp = time.time()
        RE.md['tstamp'] = tstamp
    
    det_exposure_time(t, t)

    for i in range(frames):

        print(f'Taking {i + 1} / {frames} frames')

        # update sample name
        name_sample(sname, tstamp)

        # take one fram
        yield from bp.count([pil900KW])

        # wait
        print(f'\nWaiting {wait} s')
        yield from bps.sleep(wait)

def manual_th_scan(name, t=2, angles=[0.05, 0.10, 0.15, 0.20, 0.25, 0.30], loc=None):
    """
    Take data manually over a few theta angles
    and come back to 0.1 deg incident angle
    
    """
    det_exposure_time(t, t)
    
    try:
        tstamp = RE.md['tstamp']
    except:
        tstamp = time.time()
        RE.md['tstamp'] = tstamp

    try:
        th0 = RE.md['th0']
    except:
        th0 = -1.30-0.1 # as measured
        RE.md['th0'] = th0

    for ai in angles:
        yield from bps.mv(piezo.th, th0 + ai)

        name_sample(name, tstamp)
        sname = RE.md['sample_name']
        RE.md['sample_name'] += f'ai={ai}'
        if loc is not None:
            RE.md['sample_name'] += f'_loc{loc}'
        yield from bp.count([pil900KW])
        RE.md['sample_name'] = sname

    yield from bps.mv(piezo.th, th0 + 0.1)


def run_x_th_scan(name, t):
    """
    """

    x = piezo.x.position

    x_table = [-100, -50, 0, 50, 100]

    for x_step in x_table:
        yield from bps.mv(piezo.x, x + x_step)

        yield from manual_th_scan(name, t)
    
    yield from bps.mv(piezo.x, x)


def run_swaxs_KCW_2023_3(t=2):
    """
    Hard X-ray WAXS and SAXS
    """

    names =   [ 'calib-kapton', 'calib-celgart-rot0', 'calib-glass-fibre', 'calib-cu-foil', 'calib-celgard-rot90'] 
    piezo_x = [   -15000, -6700, 2300, 12300, 22300 ]   
    piezo_y = [    -4000, -4000, -4000, -4000, -5700 ]          
    piezo_z = [ 3000 for n in names ]
    hexa_x =  [ 0 for n in names]

    msg = "Wrong number of coordinates"
    assert len(piezo_x) == len(names), msg
    assert len(piezo_x) == len(piezo_y), msg
    assert len(piezo_x) == len(piezo_z), msg
    assert len(piezo_x) == len(hexa_x), msg

    user_name = "KCW"
    waxs_arc = [0, 20]

    det_exposure_time(t, t)

    # Make sure cam server engages with the detector
    yield from engage_detectors()

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)

        dets = [pil900KW] if waxs.arc.position < 15 else [pil1M, pil900KW]

        for name, x, y, z, hx in zip(names, piezo_x, piezo_y, piezo_z, hexa_x):
            yield from bps.mv(piezo.x, x,
                              piezo.y, y,
                              piezo.z, z,
                              stage.x, hx)

            # Take normal scans
            sample_name = f'{name}{get_scan_md()}'
            sample_id(user_name=user_name, sample_name=sample_name)
            print(f"\n\n\n\t=== Sample: {sample_name} ===")
            yield from bp.count(dets)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)


def loop_scans_across_y(sname=f'20231106_opexp_NaCu_a', t=2, wait=1, frames=1):
    """
    Sample alignment
    """

    piezo_x = np.round(piezo.x.position, 2)
    piezo_y = np.round(piezo.y.position, 2)

    x_off = [-100, 0, 100, 250]
    y_off = np.linspace(-20, 20, 41)

    for x in x_off:
        yield from bps.mv(piezo.x, piezo_x + x)

        for y in y_off:
            yield from bps.mv(piezo.y, piezo_y + y)

            yield from continous_run(sname=sname, t=t, wait=wait, frames=frames)

    yield from bps.mv(piezo.x, piezo_x,
                      piezo.y, piezo_y,)

def loop_overnight_scans_(sname=f'20231106_opexp_NaCu_a', t=2, wait=1, frames=1):
    """
    Overnight x vs y vs theta
    move to nominal pozition manually after the scan
    """

    piezo_x = [  12450,  12550,  12650, ]
    piezo_y = [ -1225, -1225, -1225, ]

    y_off = [-2, 0, 2]

    for frame in range(frames):
        print(f'Taking {frame + 1} / {frames} frames')

        for i, (x, y) in enumerate(zip(piezo_x, piezo_y)):
            yield from bps.mv(piezo.x, x,
                              piezo.y, y)

            for j, y_of in enumerate(y_off):
                yield from bps.mv(piezo.y, y + y_of)

                loc = f'{i}{j}'
                yield from manual_th_scan(sname, t=2, angles=[0.05, 0.10, 0.15], loc=loc)

def grazing_Chen_Wiegart_2023_3(t=0.5):
    """
    standard GI-S/WAXS
    """
    #[ 'G1-01-x2.083']
    #[ -52417 ] 
    #[   6775 ]  
    #[   9800 ] 
    #[    -13 ] 
    # names   =  [  'G1-01-x7.083',  'G1-01-x8.750',  'G1-01-x9.167', 'G1-01-x10.000', 'G1-01-x25.000', 'G3-01-x25.000', 'G3-01-x10.000', 'G3-01-x7.083', 'G3-01-x2.083', 'G4-01-x2.083', 'G4-01-x7.083', 'G4-01-x25.000']
    # piezo_x =  [    -47417,          -45750,          -45333,         -44500,          -29500,          7300,             22292,          25211,          30215,           17985,          22989,          40900]
    # piezo_y =  [    6775,              6775,           6775,           6775,           6775,            6775,             5815,           5815,           5815,            5615,           5615,           5415]          
    # piezo_z =  [    9800,              9800,           9800,           9800,           9200,            6600,             5600,           5600,           5600,            5400,           5400,           4200]
    # hexa_x =   [     -13,               -13,            -13,            -13,            -13,            -13,              -13,            -13,            -13,             12,             12,             12]
    # names   =  [  'b44-01_VTiCu_Pristine',  'b44-02_VTiCu_750C30M',  'b45-01_NbAlCu_Pristine', 'b45-02_NbAlCu_500C30M', 'b46-01_MoTiCu_Pristine', 'b46-02_MoTiCu_750C30M', 'b47-01_NbAlSc_Pristine', 'b47-02_NbAlSc_900C30M']
    # piezo_x =  [  -53100,                   -41100,                  -29100,                   -17100,                  -3100,                    8900,                    20900,                    34900                  ]
    # piezo_y =  [    6984,                     6984,                    6784,                     6684,                   6584,                    6484,                     6484,                    6284                   ]          
    # piezo_z =  [    8800,                     7800,                    7300,                     6800,                   6800,                    6300,                     6300,                    4800                   ]
    # hexa_x =   [     -13,                      -13,                     -13,                      -13,                    -13,                     -13,                      -13,                    -13                    ]
    names   =  [  'Cufoil_reflection']
    piezo_x =  [  1900]
    piezo_y =  [  7856]          
    piezo_z =  [  6800]
    hexa_x =   [   -13]


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

    waxs_arc = [ 0, 20, ]  # degrees
    x_off = [ 0 ]
    incident_angles = [ 0.10, 0.15, 0.20, 0.25, 0.30, 0.50]
    user_name = 'YCW'

    det_exposure_time(t, t)

    # Make sure cam server engages with the detector
    #yield from engage_detectors()
 
    for name, x, y, z, hx in zip(names, piezo_x, piezo_y, piezo_z, hexa_x):

        #yield from bps.mv(piezo.x, x,
        #                  piezo.y, y,
        #                  piezo.z, z,
        #                  stage.x, hx)

        # Align the sample
        #yield from alignement_gisaxs(0.1) #0.1 to 0.15


        # Sample flat at ai0
        ai0 = piezo.th.position

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)
            dets = [pil900KW] if waxs.arc.position < 15 else [pil900KW, pil1M]

            # problems with the beamstop
            yield from bps.mv(waxs.bs_y, -3)

            for xx, x_of in enumerate(x_off):
                yield from bps.mv(piezo.x, x + x_of)
            
                for ai in incident_angles:
                    yield from bps.mv(piezo.th, ai0 + ai)

                    sample_name = f'{name}{get_scan_md()}_ai{ai}'

                    sample_id(user_name=user_name, sample_name=sample_name)
                    print(f"\n\n\n\t=== Sample: {sample_name} ===")
                    yield from bp.count(dets)

        yield from bps.mv(piezo.th, ai0)

    sample_id(user_name='test', sample_name='test')
    det_exposure_time(0.5, 0.5)

def alignment_on():
    """
    Alignment mode on
    """
    smi = SMI_Beamline()
    yield from smi.modeAlignment(technique="gisaxs")
    yield from smi.setDirectBeamROI(size=[48, 20])
    sample_id(user_name='test', sample_name='test')
    det_exposure_time(0.5, 0.5)
    print('\t\tALIGNMENT MODE ON')

def alignment_off():
    """
    Alignment mode off
    """
    print('\t\tALIGNMENT MODE OFF and WAXS arc to 0 deg')
    smi = SMI_Beamline()
    yield from smi.modeMeasurement()
    yield from bps.mv(waxs, 0)

def continous_run_change_xpos(sname='20250205_op_b_echem', t=2, wait=100, frames=5000,
        x_off=[-150, -100, -50, 0, 50, 100,150]):

    """
    Take data continously
    
    Create timestamp in BlueSky before running this function as
    create_timestamp()

    Args:
        sname (str): basic sample name,
        t (float): camera exposure time is seconds,
        wait (float): delay between frames,
        frames(int): number of frames to take,
        x_off (list of floats): relative x positions to take data at.
    """
    try:
        tstamp = RE.md['tstamp']
    except:
        tstamp = time.time()
        RE.md['tstamp'] = tstamp
    
    det_exposure_time(t, t)

    for i in range(frames):

        print(f'Taking {i + 1} / {frames} frames for {len(x_off)} x positions')

        x_0 = piezo.x.position
        # this could change because of drift.

        for x_step in x_off:
            yield from bps.mv(piezo.x, x_0 + x_step)
            # update sample name
            name_sample(sname, tstamp)

            # take one frame
            yield from bp.count([pil900KW])
        
        yield from bps.mv(piezo.x, x_0)

        # don't wait
        print(f'\nWaiting {wait} s')
        yield from bps.sleep(wait)

def take_data_across_x(sname='20241030_op_Na_Cu_bar_b', t=2, x_off=[-500, -400, -300, -250, -200,-150, -100, -50, 0, 50, 
                                                                  100,150, 200, 250, 300, 400, 500]):

    try:
        tstamp = RE.md['tstamp']
    except:
        tstamp = time.time()
        RE.md['tstamp'] = tstamp

    x_0 = piezo.x.position

    for x_step in x_off:
        yield from bps.mv(piezo.x, x_0 + x_step)
        # update sample name
        name_sample(sname, tstamp)

        # take one frame
        yield from bp.count([pil900KW])
    
    yield from bps.mv(piezo.x, x_0)


def align_across_x():
    """
    Create alignment look up table for different positions

    Need to go manually
    """

    try:
        sample_pos = RE.md['sample_pos0']
        x0 = sample_pos['x0']
    except:
        x0 = piezo.x.position
        y0 = piezo.y.position
        z0 = piezo.z.position
        th0 = piezo.th.position
        ch0 = piezo.ch.position
        RE.md['sample_pos0'] = dict(x0=x0, y0=y0, z0=z0, th0=th0, ch0=ch0)

    piezo_x = np.linspace(-500, 500, 11, dtype=int) + x0

    yield from bps.mv(
        piezo.x, sample_pos['x0'],
        piezo.y, sample_pos['y0'],
        piezo.th, sample_pos['th0'],
    )

    yield from alignment_on()

    RE.md['alignment_LUT'] = dict()

    for i, x in enumerate(piezo_x):
        yield from bps.mv(piezo.x, x)



        # Align step by step
        alignment_LUP = dict()

        yield from rel_scan([pil1M], piezo.y, -100, 100, 26)
        ps(der=True)
        yield from bps.mv(piezo.y, ps.cen)

        yield from rel_scan([pil1M], piezo.th, -1.5, 1.5, 26)
        ps(der=False)
        yield from bps.mv(piezo.th, ps.peak)

        plt.close('all')

        yield from bps.sleep(1)

        dict1 = dict(
            x = piezo.x.position,
            y = piezo.y.position,
            th = piezo.th.position,
        )

        RE.md['alignment_LUT'][i] = dict1

    yield from alignment_off()


def save_alignment_to_md(point='0'):
    """
    Save alignment positon for single point
    """

    dict1 = dict(
        x = np.round(piezo.x.position, 2),
        y = np.round(piezo.y.position, 2),
        z = np.round(piezo.z.position, 2),
        th = np.round(piezo.th.position, 3),
    )

    try:
        RE.md['alignment_LUT'][str(point)] = dict1
    except:
        RE.md['alignment_LUT'] = dict()
        RE.md['alignment_LUT'][str(point)] = dict1

def move_to_sample_pos0(key='sample_pos0'):
    """
    Move to starting position based on RE.md
    """

    try:
        sample_pos = RE.md[key]
    except:
        print(f'There is no starting position {key} saved in RE.md')

    print(f'Moving to sample position\n{sample_pos}')

    yield from bps.mv(
        piezo.x, sample_pos['x0'],
        piezo.y, sample_pos['y0'],
        piezo.z, sample_pos['z0'],
        piezo.th, sample_pos['th0'],
        piezo.ch, sample_pos['ch0']
    )

def save_sample_pos0():
    """
    Save sample start position into metadata after alignment
    """

    x0 = np.round(piezo.x.position, 2)
    y0 = np.round(piezo.y.position, 2)
    z0 = np.round(piezo.z.position, 2)
    th0 = np.round(piezo.th.position, 3)
    ch0 = np.round(piezo.ch.position, 3)

    RE.md['sample_pos0'] = dict(x0=x0, y0=y0, z0=z0, th0=th0, ch0=ch0)


def clear_md():
    """
    Remove time stamp, sample zero, and alignment after changing the cell
    """

    keys = [ 'tstamp', 'alignment_LUT', 'sample_pos0']
    
    for k in keys:
        try:
            RE.md.pop(k)
        except:
            print(f'No {k} key')


def continous_run_prealigned_positions_2024_1(sname='20240408_op_Na_Cu_bar_a', t=2, wait=8, frames=1):
    """
    WAXS at each prealigned point

    Args:
        sname (str): sample name,
        t (float): exposure time,
        wait (float): wait time after one series of points is done.
    """

    try:
        alignment = RE.md['alignment_LUT']
    except:
        alignment =  {
                      '0': {'x': 814.46, 'y': 5918.27, 'z': 3400, 'th': 0.185},
                        '-500': {'x': 314.373, 'y': 5899.3, 'z': 3400, 'th': 0.185},
                        '-1000': {'x': -185.627, 'y': 5894.043, 'z': 3400, 'th': 0.185},
                        '500': {'x': 1314.373, 'y': 5926.778, 'z': 3400, 'th': 0.185},
                        '1000': {'x': 1814.373, 'y': 5938.7, 'z': 3400, 'th': 0.185}
        }
        RE.md['alignment_LUT'] = alignment

    alignment = {int(k) : v for k, v in alignment.items()}

    try:
        tstamp = RE.md['tstamp']
    except:
        tstamp = time.time()
        RE.md['tstamp'] = tstamp

    for i in range(frames):

        print(f'Taking {i + 1} / {frames} frames for {len(alignment)} x positions')

        for key, value in sorted(alignment.items()):

            yield from bps.mv(
                piezo.x, value['x'],
                piezo.y, value['y'],
                #piezo.z, value['z'],
                #piezo.th, value['th'] + 0.1, # angle set already
                piezo.th, value['th'],
            )

            name_sample(sname, tstamp)
            yield from bp.count([pil900KW])
        
        # wait
        print(f'\nWaiting {wait} s')
        yield from bps.sleep(wait)

def continous_run_change_xpos_thpos(
        sname='20240524_operando_exp_b_echem',
        t=2, wait=93, frames=5000,
        x_off=[-600, -300, -250, 0, 250, 300, 600],
        ai_off=[0.05, 0.10, 0.15, 0.20, 0.30],
    ):
    """
    Take data continously
    
    Create timestamp in BlueSky before running this function as
    create_timestamp()

    Args:
        sname (str): basic sample name,
        t (float): camera exposure time is seconds,
        wait (float): delay between frames,
        frames(int): number of frames to take,
        x_off (list of floats): relative x positions to take data at.
    """
    try:
        tstamp = RE.md['tstamp']
    except:
        tstamp = time.time()
        RE.md['tstamp'] = tstamp
        print(f'Setting timestampt to {tstamp}')

    try:
        th0 = RE.md['th0']
    except:
        th0 = piezo.th.position
        RE.md['th0'] = th0
        print(f'Setting th0 to current position of {th0} deg')

    det_exposure_time(t, t)
    x_0 = piezo.x.position

    for i in range(frames):

        print(f'Taking {i + 1} / {frames} frames for {len(x_off)} x positions')
    
        for x_step in x_off:
            yield from bps.mv(piezo.x, x_0 + x_step)

            for ai in ai_off:
                yield from bps.mv(piezo.th, th0 + ai)
                # update sample name
                name_sample(sname, tstamp)

                # take one frame
                yield from bp.count([pil900KW])
        
        yield from bps.mv(piezo.x, x_0,
                          piezo.th, th0)

        # don't wait
        print(f'\nWaiting {wait} s')
        yield from bps.sleep(wait)


# Backup
''' {'0': {'x': 3648.04, 'y': -1263.1, 'z': 799.8, 'th': 2.19},
 '-100': {'x': 3547.69, 'y': -1249.21, 'z': 799.82, 'th': 2.19},
 '-200': {'x': 3447.79, 'y': -1249.52, 'z': 799.82, 'th': 2.19},
 '-300': {'x': 3347.77, 'y': -1249.37, 'z': 799.82, 'th': 1.875},
 '-400': {'x': 3247.8, 'y': -1244.76, 'z': 799.81, 'th': 1.875},
 '-500': {'x': 3147.79, 'y': -1244.88, 'z': 799.81, 'th': 1.875},
 '-1000': {'x': 2647.77, 'y': -1239.85, 'z': 799.81, 'th': 1.875},
 '-900': {'x': 2748.02, 'y': -1239.9, 'z': 799.81, 'th': 1.875},
 '-1100': {'x': 2547.76, 'y': -1239.96, 'z': 799.81, 'th': 1.875},
 '-1500': {'x': 2147.76, 'y': -1230.9, 'z': 799.8, 'th': 1.675},
 '-1400': {'x': 2248.09, 'y': -1229.97, 'z': 799.79, 'th': 1.686},
 '-1600': {'x': 2047.73, 'y': -1225.97, 'z': 799.79, 'th': 1.686},
 '100': {'x': 3748.02, 'y': -1255.0, 'z': 799.77, 'th': 2.04},
 '200': {'x': 3848.0, 'y': -1255.05, 'z': 799.77, 'th': 2.04},
 '300': {'x': 3947.96, 'y': -1250.96, 'z': 799.77, 'th': 2.04},
 '400': {'x': 4047.98, 'y': -1251.02, 'z': 799.76, 'th': 2.04},
 '500': {'x': 4148.0, 'y': -1251.18, 'z': 799.74, 'th': 2.04},
 '1000': {'x': 4648.05, 'y': -1256.98, 'z': 799.74, 'th': 2.18},
 '900': {'x': 4547.77, 'y': -1255.99, 'z': 799.74, 'th': 2.18},
 '1100': {'x': 4748.04, 'y': -1257.98, 'z': 799.74, 'th': 2.33},
 '1500': {'x': 5148.08, 'y': -1259.73, 'z': 799.74, 'th': 2.18},
 '1400': {'x': 5047.73, 'y': -1257.99, 'z': 799.74, 'th': 2.32},
 '1600': {'x': 5248.13, 'y': -1259.23, 'z': 799.73, 'th': 2.02}}

 
 {'0': {'x': 3999.71, 'y': -1442.75, 'z': 799.8, 'th': 1.00},
 '-250': {'x': 3749.71, 'y': -1437.84, 'z': 799.82, 'th': 1.00},
 '-500': {'x': 3499.71, 'y': -1437.94, 'z': 799.82, 'th': 1.00},
 '250': {'x': 4249.71, 'y': -1438.07, 'z': 799.82, 'th': 1.00},
 '500': {'x': 4499.71, 'y': -1438.41, 'z': 799.81, 'th': 1.00}


    0': {'x': 3999.71, 'y': -1442.75, 'z': 799.8, 'th': 1.00},
 '-250': {'x': 3749.71, 'y': -1437.84, 'z': 799.82, 'th': 1.00},
 '-500': {'x': 3499.71, 'y': -1437.94, 'z': 799.82, 'th': 1.00},
 '250': {'x': 4249.71, 'y': -1438.07, 'z': 799.82, 'th': 1.00},
 '500': {'x': 4499.71, 'y': -1438.41, 'z': 799.81, 'th': 1.00}

 0': {'x': 3999.71, 'y': -1250.94, 'z': 799.8, 'th': 2.05},
 '-250': {'x': 3749.71, 'y': -1247.7, 'z': 799.82, 'th': 2.05},
 '-500': {'x': 3499.71, 'y': -1243.4, 'z': 799.82, 'th': 2.05},
 '250': {'x': 4249.71, 'y': -1249.9, 'z': 799.82, 'th': 2.05},
 '500': {'x': 4499.71, 'y': -1454.7, 'z': 799.81, 'th': 2.05}
 ,


'''
# Read T and convert to deg C
#temp = ls.input_A.get() - 273.15
#temp = str(np.round(float(temp), 1)).zfill(5)
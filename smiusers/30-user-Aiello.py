def atten_move_in():
    """
    Move 4x + 2x Sn 60 um attenuators in
    """
    print('Moving attenuators in')

    while att1_7.status.get() != 'Open':
        yield from bps.mv(att1_7.open_cmd, 1)
        yield from bps.sleep(1)
    while att1_6.status.get() != 'Open':
        yield from bps.mv(att1_6.open_cmd, 1)
        yield from bps.sleep(1)

def atten_move_out():
    """
    Move 4x + 2x Sn 60 um attenuators out
    """
    print('Moving attenuators out')
    while att1_7.status.get() != 'Not Open':
        yield from bps.mv(att1_7.close_cmd, 1)
        yield from bps.sleep(1)
    while att1_6.status.get() != 'Not Open':
        yield from bps.mv(att1_6.close_cmd, 1)
        yield from bps.sleep(1)

def take_test_det(t=0.5):
    """
    Take some data just in case WAXS complains
    """
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)
    sample_id(user_name="test", sample_name="test")
    yield from bp.count(dets)

def run_nist_linescans(t=0.5):
    """
    Microfocusing line scans along y axis, set y_range for each sample
    """
    
    # names =   ['PET1000_b','PET1000_c','PET1500_a','PET1500_b',    'PET1500_c','PET2000_a',   'PET2000_b',   'PET2000_c', 'PET3000_a',  'PET3000_b',   'PET3000c',    'PET4000a',    'PET4000b', 'PET4000c',  'PET0redo_a',  'PET0redo_b', 'PET0redo_c','PET4000S_a', 'PET4000S_b', 'PET4000S_c','PET3000S_a',   'PET3000S_b', 'PET3000S_c', 'PET2000S_a',  'PET2000S_b',  'PET2000S_c', 'PET1500S_a',  'PET1500S_b', 'PET1500S_c',  'PET1000S_a','PET1000S_b', 'PET1000S_c',  'PET500S_a', 'PET500S_b', 'PET500S_c',    'PET250S_a',   'PET250S_b', 'PET250S_c']
    # piezo_x = [   26600,    26000,          18000,       15500,         14000,       5750 ,          3250,         1750,        -2650,        -5650,        -8150,       -14650,         -17150,     -18650,        -23850,        -27350,       -30350,      -17350,       -15350,       -13350,       -7850,          -5350,        -2850,        1650,           4150,          7650,        12650,          15150,       17650,         22150,       25150,        28150,        34150,       36150,        38150,         44150,         46150,        48150]
    # piezo_y = [   -7490,    -7470,          -7400,       -7400,         -7400,      -7170,          -7080,        -7010,        -6900,        -6820,        -6760,        -6930,          -6730,      -6640,         -6810,         -6660,        -6570,        6060,         6040,         5940,        5720,           5660,         5660,        5820,           5820,          5680,         5660,          5670,         5650,         5410,         5410,         5380,         5320,        5290,        5240,           5360,          5320,        5320]

    # Bar 4: 1-15
    #                    1                2                3              4               5             6             7                 8               9             10              11            12          13           14         15
    # names =   ['180_100_100_N1_c','210_100_100_N1','240_100_100_N1','180_10_N1','210_30prob10_N1','240_10_N1','180_100_100_N2','210_100_100_N2','240_100_100_N2','180_10_N2','210_30prob10_N2','240_10_N2','180_30_PP','210_30_PP','240_30_PP']
    # piezo_x = [     48150,              42650,          37550,        32450,        26450,          20950,          15450,          9750,           4050,           -1750,          -7850,      -13450,     -18950,     -24450,       -29950]
    # piezo_y = [     -850,               -780,           -655,         -655,         -740,           -445,           -115,          -175,            -165,           -380,           -300,       -160,       260,        330,            520]

    # Bar 3: 13-18       
    #                   13                 14               15             16          17          18
    # names =   ['180_100_100_PP_c','210_100_100_PP','240_100_100_PP','180_10_PP','210_10_PP','240_10_PP']
    # piezo_x = [     -10650,            -15650,          -20650,        -25650,     -31050,     -36450]
    # piezo_y = [       340,               680,             110,           120,        170,        465]
    
    #names =   ['180_100_100_PP_c','210_100_100_PP','240_100_100_PP','180_10_PP','210_10_PP','240_10_PP']
    #piezo_x = [-10650,-15650,-20650,-25650,-31050,-36450]
    #piezo_y = [340,680,110,120,170,465]

    names =   ['AAA0_a',   'AAA0_b',      'AAA250',    'AAA500',    'AAA1000',     'AAA1500',  'AAA2000_a', 'AAA2000_b',  'AAA3000_a',  'AAA3000_b',   'AAA4000_a', 'AAA4000_b',      'PP75C',        'PP0',  'AAA4000s_a', 'AAA4000s_b', 'AAA3000s_a', 'AAA3000s_b',   'AAA2000s',   'AAA1500s',   'AAA1000s',    'AAA500s',    'AAA250s']
    piezo_x = [   47245,      45245,          35245,      24745,        13745,          1945,        -7055,       -9555,           -25555,   -27555,        -35555,      -37555,       -36055,       -26055,        -17055,       -15055,        -6055,        -2055,         6945,        16945,        26945,        36945,        46945]
    piezo_y = [   -7500,      -7500,          -7500,      -7460,        -6840,          -7150,       -6920,       -6860,            -6320,     -6360,        -6320,       -6300,         6400,        6040,           5680,        5680,          5860,         5840,         5940,        5720,          5220,         5260,         5020]
    
    y_ranges = [
        [0, 500, 101], [0, 500, 101],[0, 500, 101],[0, 500, 101],[0, 500, 101],[0, 500, 101],[0, 500, 101],[0, 500, 101],[0, 500, 101],[0, 500, 101],[0, 500, 101],[0, 500, 101],[0, 500, 101],[0, 500, 101],[0, 500, 101],[0, 500, 101], [0, 500, 101],[0, 500, 101],[0, 500, 101],[0, 500, 101],[0, 500, 101],[0, 500, 101],[0, 500, 101],
    ]
        
    msg = "Wrong number of coordinates in lists, check names, piezos, etc"
    assert len(piezo_x) == len(names), msg
    assert len(piezo_x) == len(piezo_y), msg
    assert len(piezo_x) == len(y_ranges), msg

    user_name = "AA"
    waxs_arc = [0, 20]

    # Direct beam coordinates
    dbeam_x = 18000
    dbeam_y = -900
    stats1_direct = 1



    # beamstop x position on SAXS
    bs_pos = 2.2
    yield from atten_move_out()
    yield from bps.mv(pil1m_bs_rod.x, bs_pos)

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)
        dets = [pil900KW] if waxs.arc.position < 15 else [pil1M, pil900KW]
        det_exposure_time(t, t)

        condition = ( 19 < waxs.arc.position ) and ( waxs.arc.position < 21 )

        # Take direct beam readout for transmission caluclation
        if condition:
            yield from atten_move_in()
            yield from bps.mv(piezo.x, dbeam_x,
                              piezo.y, dbeam_y,
                              pil1m_bs_rod.x, bs_pos + 5)
            
            sample_name = f'empty-attn-direct'
            sample_id(user_name='test', sample_name=sample_name)
            print(f"\n\n\n\t=== Sample: {sample_name} ===")
            yield from bp.count([pil1M])
            stats1_direct = db[-1].table(stream_name='primary')['pil1M_stats1_total'].values[0]

            yield from bps.mv(pil1m_bs_rod.x, bs_pos)
            yield from atten_move_out()
        
        # Measure samples
        for name, x, y, y_r in zip(names, piezo_x, piezo_y, y_ranges):
            yield from bps.mv(piezo.y, y,
                              piezo.x, x,)

            # Take transmission data
            if condition:
                yield from atten_move_in()
                yield from bps.mv(piezo.y, y + y_r[1] / 2,
                                  pil1m_bs_rod.x, bs_pos + 5,)

                sample_name = f'{name}-attn-sample'
                sample_id(user_name='test', sample_name=sample_name)
                print(f"\n\n\t=== Sample: {sample_name} ===")
                yield from bp.count([pil1M])
                stats1_sample = db[-1].table(stream_name='primary')['pil1M_stats1_total'].values[0]
                
                # Transmission
                trans = np.round( stats1_sample / stats1_direct, 5)

                # Revert configuraton
                yield from bps.mv(pil1m_bs_rod.x, bs_pos,
                                  piezo.y, y,)
                yield from atten_move_out()
            else:
                trans = 0
            
            # Take sample y scan
            sample_name = f'{name}{get_scan_md()}_trs{trans}'
            sample_id(user_name=user_name, sample_name=sample_name)
            print(f"\n\n\n\t=== Sample: {sample_name} ===")
            yield from bp.rel_scan(dets, piezo.y, *y_r)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)


def run_nist_spirals(t=0.5):
    """
    Microfocusing spiral scans
    """

    names =   ['180_100_50_PP_CS_L2_c',],#'180_100_50_PP_CS_L1']
    piezo_x = [             40835,]#                  45585]
    piezo_y = [             -1320,]#                  -1120]
    
    # x range, y range, delta r, theta for spiral
    ranges = [
        [500, 500, 50, 12],
        #[250, 150, 50, 12],
    ]
        
    msg = "Wrong number of coordinates in lists, check names, piezos, etc"
    assert len(piezo_x) == len(names), msg
    assert len(piezo_x) == len(piezo_y), msg
    assert len(piezo_x) == len(ranges), msg

    user_name = "JS"
    waxs_arc = [0]

    # Take test images just in case
    yield from take_test_det(t)

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)
        dets = [pil900KW] if waxs.arc.position < 15 else [pil1M, pil900KW]
        dets.append(OAV_writing)
        det_exposure_time(t, t)
        
        # Measure samples
        for name, x, y, r in zip(names, piezo_x, piezo_y, ranges):
            yield from bps.mv(piezo.y, y,
                              piezo.x, x,)

            sample_name = f'{name}{get_scan_md()}'
            sample_id(user_name=user_name, sample_name=sample_name)
            print(f"\n\n\n\t=== Sample: {sample_name} ===")
            yield from bp.rel_spiral(dets, piezo.x, piezo.y, *r)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)

def run_nist_grids(t=0.3):
    """
    Microfocusing grid scans
    """
    # Bar 2: 2,4,6,8,10,12,13-18
    #           2                   4                   6                      8                    10                  12                13                14                15                16                17                18
    # ['240_100_PP_CS_L2','240_100_100_PP_CS_L2','240_100_N1_CS_L2','240_100_100_N1_CS_L2','240_100_N2_CS_L2','240_100_100_CS_L2','180_10_PP_CS_LS','180_10_N1_CS_LS','180_10_N2_CS_LS','210_10_PP_CS_LS','210_10_N1_CS_LS','210_10_N2_CS_LS']
    
    # Bar 1:
    # names =   ['180_100_100_N1_CS_L2_b','180_100_50_N2_CS_L2','210_100_PP_CS_L2','210_100_100_PP_CS_L2','210_100_100_N1_CS_L2','210_100_N2_CS_L2','210_100_100_N2_CS_L2']
    # piezo_x = [                 32675,                23285,             12860,                 3020,                  -7120,            -17180,                -26875]
    # piezo_y = [                 -1180,                -1020,              -520,                 -430,                   -550,              -120,                   -10]
    
    # Bar 3: 1-2
    #                   1                 2           
    # names =   ['240_10_PP_CS_L2_b','240_10_N1_CS_L2']
    # piezo_x = [       49330,            44230,      ]
    # piezo_y = [       -585,             -515,       ]
    #ranges_x = [ [-250, 250, 11],[-250, 250, 11]]
    #ranges_y = [ [-150, 150, 21],[-150, 150, 21],]

    # Bar 3: 3-12 Stopped after sample 3!
    #                   3                 4                 5                 6                 7                 8                 9                10                11                12 
    #names =   ['240_10_N2_CS_L2','180_30_PP_CS_L2','180_30_N1_CS_L2','180_30_N2_CS_L2','210_30_PP_CS_L2','210_30_N1_CS_L2','210_30_N2_CS_L2','210_30_PP_CS_L2','210_30_N1_CS_L2','210_30_N2_CS_L2']
    #piezo_x = [      38280,            33540,            28650,            23880,            18960,             14710,            9230,             4040,            -1140,            -5940]
    #piezo_y = [      -495,             -575,             -325,             -245,             -355,              -725,             -295,             -380,             -250,             -220]

    # start, stop, number of points
    #ranges_x = [
    #            [-250, 250, 11],[-250, 250, 11],[-250, 250, 11],[-250, 250, 11],[-250, 250, 11],[-250, 250, 11],[-250, 250, 11],[-250, 250, 11],[-250, 250, 11],[-250, 250, 11]
    #]
    #ranges_y = [
    #            [-150, 150, 16],[-150, 150, 16],[-150, 150, 16],[-150, 150, 16],[-150, 150, 16],[-150, 150, 16],[-150, 150, 16],[-150, 150, 16],[-150, 150, 21],[-150, 150, 16]
    #]

# Bar 2: 2,4,6,8,10,12,13-18
    #                    2                   4                   6                      8                    10                  12                13               14                15                16                17                18
    names =   ['240_100_PP_CS_L2','240_100_100_PP_CS_L2','240_100_N1_CS_L2','240_100_100_N1_CS_L2','240_100_N2_CS_L2','240_100_100_CS_L2','180_10_PP_CS_LS','180_10_N1_CS_LS','180_10_N2_CS_LS','210_10_PP_CS_LS','210_10_N1_CS_LS','210_10_N2_CS_LS']
    piezo_x = [        43230,              33395,               24865,                15055,                   5305,          -4465,            -9434,            -14775,               -19755,            -23895,         -29604,         -33925]
    piezo_y = [       -1035,               -740,                -750,                  -900,                   -640,           -630,            -170,               -230,               -510,               70,              -180,         10]

    # start, stop, number of points
    ranges_x = [
                [-250, 250, 11],[-250, 250, 11],[-250, 250, 11],[-250, 250, 11],[-250, 250, 11],[-250, 250, 11],[-250, 250, 11],[-250, 250, 11],[-250, 250, 11],[-250, 250, 11],[-250, 250, 11],[-250, 250, 11]
    ]
    ranges_y = [
                [-150, 150, 16],[-150, 150, 16],[-150, 150, 16],[-150, 150, 16],[-150, 150, 16],[-150, 150, 16],[-150, 150, 16],[-150, 150, 16],[-150, 150, 16],[-150, 150, 16],[-150, 150, 21],[-150, 150, 16]
    ]
    

    msg = "Wrong number of coordinates in lists, check names, piezos, etc"
    assert len(piezo_x) == len(names), msg
    assert len(piezo_x) == len(piezo_y), msg
    assert len(piezo_x) == len(ranges_x), msg
    assert len(ranges_x) == len(ranges_y), msg

    user_name = "JS"
    waxs_arc = [0]

    print('Take test data just in case dets are not ready')
    yield from take_test_det(t)

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)
        dets = [pil900KW] if waxs.arc.position < 15 else [pil1M, pil900KW]
        dets.append(OAV_writing)
        det_exposure_time(t, t)
        
        # Measure samples
        for name, x, y, rx, ry, in zip(names, piezo_x, piezo_y, ranges_x, ranges_y):
            yield from bps.mv(piezo.y, y,
                              piezo.x, x,)

            sample_name = f'{name}{get_scan_md()}'
            sample_id(user_name=user_name, sample_name=sample_name)
            print(f"\n\n\n\t=== Sample: {sample_name} ===")
            yield from bp.rel_grid_scan(dets, piezo.x, *rx, piezo.y, *ry)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)


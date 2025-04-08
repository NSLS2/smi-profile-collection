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


def run_swaxs_Liu_2023_2(t=2):
    """
    Take WAXS and SAXS as linescans across capillaries
    Take transmission using attenuators

    """

    names =   [ 'n-1',' n-6',   'B-A',  'B-B',   'B-C',  'B-D',  'B-E',  'B-F',  'B-L',  'z-42-2',]
    piezo_x = [  48950, 42850,  36300,  30150,   23800,  17350,  11200,   4450,  -1700,  -8000,]
    piezo_y = [  -3600, -3600,  -3600,  -3600,   -3600,  -3600,  -3600,  -3600,  -3600,  -3600, ]
    #hexa_y =  [      0,     0,      0,      0,      0,      0,      0,      0,      0,      0, ]  #in mm
    #points =  [      3,     3,      3,      3,      3,      3,      3,      3,      3,      3,       3,      3,      3,     3,     3,]
    hexa_y =  [ 0 for n in names]
    points =  [ 3 for n in names]

    dy = 100
    waxs_arc = [20, 0]

    beamstop = pil1m_bs_pd
    bs_pos_x = -202.5
    transmission_exposure = 1.0
    dx = 1500
    user = "TB"

    dbeam_x = 46000
    dbeam_y = -4000
    stats1_direct = 1


    # Check if the length of xlocs, ylocs and names are the same
    msg = "Wrong number of coordinates, check names, piezos, and hexas"
    assert len(piezo_x) == len(names), msg
    assert len(piezo_x) == len(piezo_y), msg
    assert len(piezo_x) == len(hexa_y), msg

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)
        dets = [pil900KW] if waxs.arc.position < 15 else [pil900KW, pil1M]

        condition = ( 19 < waxs.arc.position ) and ( waxs.arc.position < 21 )

        if condition:
            yield from atten_move_in()
            yield from bps.mv(beamstop.x, bs_pos_x + 5,
                              piezo.x, dbeam_x,
                              piezo.y, dbeam_y)

            sample_name = f'empty_-attn-direct'
            sample_id(user_name='test', sample_name=sample_name)
            print(f"\n\n\n\t=== Sample: {sample_name} ===")
            yield from bp.count([pil1M])
            stats1_direct = db[-1].table(stream_name='primary')['pil1M_stats1_total'].values[0]
            yield from bps.mv(beamstop.x, bs_pos_x)
            yield from atten_move_out()

        for name, x, y, hy, pts in zip(names, piezo_x, piezo_y, hexa_y, points):
            yield from bps.mv(piezo.y, y,
                              piezo.x, x,
                              stage.y, hy)
            
            # Take sample camera image
            if wa == waxs_arc[0]:
                sample_name = f'{name}{get_scan_md()}_loc0'
                yield from bp.count([OAV_writing])
            
            for i, pt in enumerate(range(pts)):

                yield from bps.mv(piezo.y, y + i * dy)

                if ( condition and i == 0 ):

                    # Take transmission
                    det_exposure_time(transmission_exposure, transmission_exposure)
                    yield from atten_move_in()

                    # Sample
                    yield from bps.mv(beamstop.x, bs_pos_x + 5)
                    sample_name = f'{name}-attn-sample'
                    sample_id(user_name='test', sample_name=sample_name)
                    yield from bp.count([pil1M])
                    stats1_sample = db[-1].table(stream_name='primary')['pil1M_stats1_total'].values[0]

                    # Transmission
                    trans = np.round( stats1_sample / stats1_direct, 5)

                    # Revert configuraton
                    det_exposure_time(t, t)
                    yield from bps.mv(beamstop.x, bs_pos_x)
                    yield from atten_move_out()
                else:
                    trans = 0

                # Take normal scans
                yield from bps.mv(piezo.x, x)
                sample_name = f'{name}{get_scan_md()}_loc{pt}_trs{trans}'
                sample_id(user_name=user, sample_name=sample_name)
                print(f"\n\n\n\t=== Sample: {sample_name} ===")
                yield from bp.count(dets)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def run_swaxs_Liu_2023_3(t=2):
    """
    Take WAXS and SAXS as linescans across capillaries
    Take transmission using attenuators

    """

    names =   [  'Z48',  'Z49',  'Z50',  ]
    piezo_x = [ -43150, -36600, -30100,  ] 
    
    piezo_y = [ 0 for n in names]
    hexa_y =  [ 0 for n in names]
    points =  [ 3 for n in names]

    dy = 100
    waxs_arc = [20, 0]

    beamstop = pil1m_bs_pd
    bs_pos_x = -201.5
    user = 'PW'

    dbeam_x = -41400
    dbeam_y = 400
    stats1_direct = 1

    det_exposure_time(t, t)


    # Check if the length of xlocs, ylocs and names are the same
    msg = "Wrong number of coordinates, check names, piezos, and hexas"
    assert len(piezo_x) == len(names), msg
    assert len(piezo_x) == len(piezo_y), msg
    assert len(piezo_x) == len(hexa_y), msg

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)
        dets = [pil900KW] if waxs.arc.position < 15 else [pil900KW, pil1M]

        condition = ( 19 < waxs.arc.position ) and ( waxs.arc.position < 21 )

        if condition:
            yield from atten_move_in()
            yield from bps.mv(beamstop.x, bs_pos_x + 5,
                              piezo.x, dbeam_x,
                              piezo.y, dbeam_y)

            sample_name = f'empty_-attn-direct'
            sample_id(user_name='test', sample_name=sample_name)
            print(f"\n\n\n\t=== Sample: {sample_name} ===")
            yield from bp.count([pil1M])
            stats1_direct = db[-1].table(stream_name='primary')['pil1M_stats1_total'].values[0]
            yield from bps.mv(beamstop.x, bs_pos_x)
            yield from atten_move_out()


        for name, x, y, hy, pts in zip(names, piezo_x, piezo_y, hexa_y, points):
            yield from bps.mv(piezo.y, y,
                              piezo.x, x,
                              stage.y, hy)
            
            # Take sample camera image
            if wa == waxs_arc[0]:
                sample_name = f'{name}{get_scan_md()}_loc0'
                sample_id(user_name=user, sample_name=sample_name)
                yield from bp.count([OAV_writing])
            
            for i in range(pts):

                yield from bps.mv(piezo.y, y + i * dy)

                if ( condition and i == 0 ):

                    # Take transmission
                    yield from atten_move_in()

                    # Sample
                    yield from bps.mv(beamstop.x, bs_pos_x + 5)
                    sample_name = f'{name}-attn-sample'
                    sample_id(user_name='test', sample_name=sample_name)
                    yield from bp.count([pil1M])
                    stats1_sample = db[-1].table(stream_name='primary')['pil1M_stats1_total'].values[0]

                    # Transmission
                    trans = np.round( stats1_sample / stats1_direct, 5)

                    # Revert configuraton
                    yield from bps.mv(beamstop.x, bs_pos_x)
                    yield from atten_move_out()
                
                if not condition:
                    trans = 0

                # Take normal scans
                yield from bps.mv(piezo.x, x)
                sample_name = f'{name}{get_scan_md()}_loc{i}_trs{trans}'
                sample_id(user_name=user, sample_name=sample_name)
                print(f"\n\n\n\t=== Sample: {sample_name} ===")
                yield from bp.count(dets)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def run_swaxs_Liu_2024_1(t=2):
    """
    Take WAXS and SAXS as linescans across capillaries
    Take transmission using attenuators

    """

    names =   [  'M03',  'J35',  'J34',  'J33',  'J30',  'J31',  'J29',  'J28',  'J27', ]#  'J09',  'J10',  'J11',  'M01',  'JM02', ]
    piezo_x = [ -44700, -38500, -32100, -25800, -19700, -12900,  -6300,   -500,   6100, ]# 12500,  19000,  25100,  31300,  37900, ] 
    
    piezo_y = [ 2500 for n in names]
    hexa_y =  [ 0 for n in names]
    points =  [ 3 for n in names]

    dy = 100
    waxs_arc = [20, 0]

    beamstop = pil1m_bs_pd
    bs_pos_x = -201.5
    user = 'PW'

    dbeam_x = -41400
    dbeam_y = 2500
    stats1_direct = 1

    det_exposure_time(t, t)


    # Check if the length of xlocs, ylocs and names are the same
    msg = "Wrong number of coordinates, check names, piezos, and hexas"
    assert len(piezo_x) == len(names), msg
    assert len(piezo_x) == len(piezo_y), msg
    assert len(piezo_x) == len(hexa_y), msg

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)
        dets = [pil900KW] if waxs.arc.position < 15 else [pil900KW, pil1M]

        condition = ( 19 < waxs.arc.position ) and ( waxs.arc.position < 21 )

        if condition:
            yield from atten_move_in()
            yield from bps.mv(beamstop.x, bs_pos_x + 5,
                              piezo.x, dbeam_x,
                              piezo.y, dbeam_y)

            sample_name = f'empty-attn-direct'
            sample_id(user_name='test', sample_name=sample_name)
            print(f"\n\n\n\t=== Sample: {sample_name} ===")
            yield from bp.count([pil1M])
            stats1_direct = db[-1].table(stream_name='primary')['pil1M_stats1_total'].values[0]
            yield from bps.mv(beamstop.x, bs_pos_x)
            yield from atten_move_out()


        for name, x, y, hy, pts in zip(names, piezo_x, piezo_y, hexa_y, points):
            yield from bps.mv(piezo.y, y,
                              piezo.x, x,
                              stage.y, hy)
            
            # Take sample camera image
            if wa == waxs_arc[0]:
                sample_name = f'{name}{get_scan_md()}_loc0'
                sample_id(user_name=user, sample_name=sample_name)
                yield from bp.count([OAV_writing])
            
            for i in range(pts):

                yield from bps.mv(piezo.y, y + i * dy)

                if ( condition and i == 0 ):

                    # Take transmission
                    yield from atten_move_in()

                    # Sample
                    yield from bps.mv(beamstop.x, bs_pos_x + 5)
                    sample_name = f'{name}-attn-sample'
                    sample_id(user_name='test', sample_name=sample_name)
                    yield from bp.count([pil1M])
                    stats1_sample = db[-1].table(stream_name='primary')['pil1M_stats1_total'].values[0]

                    # Transmission
                    trans = np.round( stats1_sample / stats1_direct, 5)

                    # Revert configuraton
                    yield from bps.mv(beamstop.x, bs_pos_x)
                    yield from atten_move_out()
                
                if not condition:
                    trans = 0

                # Take normal scans
                yield from bps.mv(piezo.x, x)
                sample_name = f'{name}{get_scan_md()}_loc{i}_trs{trans}'
                sample_id(user_name=user, sample_name=sample_name)
                print(f"\n\n\n\t=== Sample: {sample_name} ===")
                yield from bp.count(dets)

    yield from bps.mv(waxs, waxs_arc[0],
                      piezo.y, piezo_y[0],
                      piezo.x, piezo_x[0],
                      )
    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def run_swaxs_Liu_2024_2(t=2):
    """
    Take WAXS and SAXS as linescans across capillaries
    Take transmission using attenuators

    """

    #names =   [  'J15',  'J14',  'J13',  'J12',  'J11',  'J10',  'J09',  'J08A',  'J07',  'J06',  'J05',  'J04',  'J03',  'J02',  'J01', ]
    #piezo_x = [ -43400, -37000, -30400, -24400, -17800, -11800,  -5100,   1100,   7500,  13800,  20000,  26500,  32700,  39000,  45500, ] 

    names =   [  'AgBh', 'vac-bkg',]
    piezo_x = [  -43600,    -19600,]

    piezo_y = [ 5500 for n in names]
    hexa_y =  [ 0 for n in names]
    points =  [ 3 for n in names]

    dy = 100
    waxs_arc = [20, 0]

    beamstop = pil1m_bs_pd
    bs_pos_x = -200.8
    user = 'PW'

    dbeam_x = -19000
    dbeam_y = 5500
    stats1_direct = 1

    det_exposure_time(t, t)


    msg = "Wrong number of coordinates, check names, piezos, and hexas"
    assert len(piezo_x) == len(names), msg
    assert len(piezo_x) == len(piezo_y), msg
    assert len(piezo_x) == len(hexa_y), msg

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)
        dets = [pil900KW] if waxs.arc.position < 15 else [pil900KW, pil1M]

        condition = ( 19 < waxs.arc.position ) and ( waxs.arc.position < 21 )

        if condition:
            yield from atten_move_in()
            yield from bps.mv(beamstop.x, bs_pos_x + 5,
                              piezo.x, dbeam_x,
                              piezo.y, dbeam_y)

            sample_name = f'empty-attn-direct'
            sample_id(user_name='test', sample_name=sample_name)
            print(f"\n\n\n\t=== Sample: {sample_name} ===")
            yield from bp.count([pil1M])
            stats1_direct = db[-1].table(stream_name='primary')['pil1M_stats1_total'].values[0]
            yield from bps.mv(beamstop.x, bs_pos_x)
            yield from atten_move_out()


        for name, x, y, hy, pts in zip(names, piezo_x, piezo_y, hexa_y, points):
            yield from bps.mv(piezo.y, y,
                              piezo.x, x,
                              stage.y, hy)
            
            # Take sample camera image
            if wa == waxs_arc[0]:
                sample_name = f'{name}{get_scan_md()}_loc0'
                sample_id(user_name=user, sample_name=sample_name)
                yield from bp.count([OAV_writing])
            
            for i in range(pts):

                yield from bps.mv(piezo.y, y + i * dy)

                if ( condition and i == 0 ):

                    # Take transmission
                    yield from atten_move_in()

                    # Sample
                    yield from bps.mv(beamstop.x, bs_pos_x + 5)
                    sample_name = f'{name}-attn-sample'
                    sample_id(user_name='test', sample_name=sample_name)
                    yield from bp.count([pil1M])
                    stats1_sample = db[-1].table(stream_name='primary')['pil1M_stats1_total'].values[0]

                    # Transmission
                    trans = np.round( stats1_sample / stats1_direct, 5)

                    # Revert configuraton
                    yield from bps.mv(beamstop.x, bs_pos_x)
                    yield from atten_move_out()
                
                if not condition:
                    trans = 0

                # Take normal scans
                yield from bps.mv(piezo.x, x)
                sample_name = f'{name}{get_scan_md()}_loc{i}_trs{trans}'
                sample_id(user_name=user, sample_name=sample_name)
                print(f"\n\n\n\t=== Sample: {sample_name} ===")
                yield from bp.count(dets)

    yield from bps.mv(waxs, waxs_arc[0],
                      piezo.y, piezo_y[0],
                      piezo.x, piezo_x[0],
                      )
    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)
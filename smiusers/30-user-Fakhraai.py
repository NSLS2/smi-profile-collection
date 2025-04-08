def run_giwaxs_Fak(t=1):
    dets = [pil300KW, pil1M]
    xlocs1 = [-22000, 3000, 21500]
    names1 = ["TPD_52nm", "TPD_42nm", "TPD_32nm"]

    # what we run now
    curr_tray = xlocs1
    curr_names = names1
    assert len(curr_tray) == len(
        curr_names
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    waxs_range = [0, 13, 3]
    for x, name in zip(curr_tray, curr_names):
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(piezo.th, 0.1)
        yield from alignement_gisaxs(0.1)
        plt.close("all")
        angle_offset = [0.1]
        a_off = piezo.th.position
        det_exposure_time(t, t)
        name_fmt = "{sample}_{angle}deg"
        for j, ang in enumerate(a_off + np.array(angle_offset)):
            yield from bps.mv(piezo.x, (x + j * 500))
            real_ang = angle_offset[j]
            yield from bps.mv(piezo.th, ang)
            sample_name = name_fmt.format(sample=name, angle=float("%.3f" % real_ang))
            sample_id(user_name="YJ", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.scan(dets, waxs, *waxs_range)

        sample_id(user_name="test", sample_name="test")
        det_exposure_time(0.5, 0.5)


def gFak1(meas_t=1):
    username = "AZ"
    names1 = "aaA_20190926_OG_hot"

    dets = [pil1M, pil300KW, rayonix]
    angle_offset = [0.1]
    length = 17000
    x_edge = 31000  # make sure to define the edge as a top border of the sample on the camera using SmarAct X
    x_step = 4000
    nb_pt = (length - 500) // x_step
    xlocs1 = []
    for step in range(0, nb_pt + 1, 1):
        xlocs1 += [np.round(x_edge - step * x_step)]

    # what we run now
    curr_tray = xlocs1
    waxs_range = [0, 13, 3]

    yield from bps.mv(piezo.x, x_edge)
    yield from bps.mv(piezo.th, 0.1)
    yield from alignement_gisaxs(0.1)
    a_off = piezo.th.position
    plt.close("all")
    for i, x in enumerate(curr_tray):
        yield from bps.mv(piezo.x, x)
        if i != 0:
            yield from bps.mv(piezo.th, a_off + angle_offset[0])
            yield from quickalign_gisaxs(0.1)
            plt.close("all")
            a_off = piezo.th.position
        for ii, an in enumerate(angle_offset):
            yield from bps.mv(piezo.th, a_off + an)
            det_exposure_time(meas_t, meas_t)
            # temper = ls.ch1_read.value
            name_fmt = "{sample}_x{xlocation}_{angl}deg"
            sample_name = name_fmt.format(sample=names1, xlocation=x, angl=an)
            sample_id(user_name=username, sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.scan(dets, waxs, *waxs_range)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def gFak2(meas_t=1):
    username = "YJ"
    names1 = "aaA_20190926_OG_middle"

    dets = [pil1M, pil300KW, rayonix]
    angle_offset = [0.1]
    length = 21000
    x_edge = 11000  # make sure to define the edge as a top border of the sample on the camera using SmarAct X
    x_step = 4000
    nb_pt = (length - 500) // x_step
    xlocs1 = []
    for step in range(0, nb_pt + 1, 1):
        xlocs1 += [np.round(x_edge - step * x_step)]

    # what we run now
    curr_tray = xlocs1
    waxs_range = [0, 13, 3]

    yield from bps.mv(piezo.x, x_edge)
    yield from bps.mv(piezo.th, 0.1)
    yield from alignement_gisaxs(0.1)
    a_off = piezo.th.position
    plt.close("all")
    for i, x in enumerate(curr_tray):
        yield from bps.mv(piezo.x, x)
        if i != 0:
            yield from bps.mv(piezo.th, a_off + angle_offset[0])
            yield from quickalign_gisaxs(0.1)
            plt.close("all")
            a_off = piezo.th.position
        for ii, an in enumerate(angle_offset):
            yield from bps.mv(piezo.th, a_off + an)
            det_exposure_time(meas_t, meas_t)
            # temper = ls.ch1_read.value
            name_fmt = "{sample}_x{xlocation}_{angl}deg"
            sample_name = name_fmt.format(sample=names1, xlocation=x, angl=an)
            sample_id(user_name=username, sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.scan(dets, waxs, *waxs_range)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def gFak3(meas_t=1):
    username = "AZ"
    names1 = "aaA_20190926_OG_cold"

    dets = [pil1M, pil300KW, rayonix]
    angle_offset = [0.1]
    length = 17000
    x_edge = (
        -14000
    )  # make sure to define the edge as a top border of the sample on the camera using SmarAct X
    x_step = 4000
    nb_pt = (length - 500) // x_step
    xlocs1 = []
    for step in range(0, nb_pt + 1, 1):
        xlocs1 += [np.round(x_edge - step * x_step)]

    # what we run now
    curr_tray = xlocs1
    waxs_range = [0, 13, 3]

    yield from bps.mv(piezo.x, x_edge)
    yield from bps.mv(piezo.th, 0.1)
    yield from alignement_gisaxs(0.1)
    a_off = piezo.th.position
    plt.close("all")
    for i, x in enumerate(curr_tray):
        yield from bps.mv(piezo.x, x)
        if i != 0:
            yield from bps.mv(piezo.th, a_off + angle_offset[0])
            yield from quickalign_gisaxs(0.1)
            plt.close("all")
            a_off = piezo.th.position
        for ii, an in enumerate(angle_offset):
            yield from bps.mv(piezo.th, a_off + an)
            det_exposure_time(meas_t, meas_t)
            # temper = ls.ch1_read.value
            name_fmt = "{sample}_x{xlocation}_{angl}deg"
            sample_name = name_fmt.format(sample=names1, xlocation=x, angl=an)
            sample_id(user_name=username, sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.scan(dets, waxs, *waxs_range)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def run_all_gFak():
    yield from gFak1()
    yield from gFak2()
    yield from gFak3()


###################
### 2022_02 Luo ###
###################


def grazing_Luo_2022_2(t=0.5, incident_angle=0.1):
    """
    Scan substrates on the bar

    309557 Luo
    Overlaping essential to cover the detector gaps

    SmarAct nanopositioner units: micrometers
    Hexapod stage units: milimeters
    Incident angle (piezo.th): degrees

    Params:
        t (float): exposure time,
        incident_angle (float): self explained
    """
    user_name = "PL"

    # Samples

    skip = 0

    names = ["81nm_aaA27C_0p2As_2022-05-17"]
    piezo_xs = [50600]
    hexa_xs = [0]
    angles = [0, 2, 18, 20]  # degrees
    step_across_sample = 200  # microns

    assert len(names) == len(
        piezo_xs
    ), f"Number of X coordinates ({len(piezo_xs)}) is different from number of samples ({len(names)})"
    assert len(hexa_xs) == len(
        names
    ), f"Number of X hexapod coordinates ({len(hexa_xs)}) is different from number of samples ({len(names)})"

    for name, piezo_x, hexa_x in zip(names[skip:], piezo_xs[skip:], hexa_xs[skip:]):

        # Move motors to locate the sample
        yield from bps.mv(piezo.x, piezo_x, stage.x, hexa_x)
        # Align the sample
        try:
            yield from alignement_gisaxs()
        except:
            yield from alignement_gisaxs(0.4)

        # Go to incident
        yield from bps.mvr(piezo.th, incident_angle)

        det_exposure_time(t, t)

        # Scan sample across angles
        for i, wa in enumerate(angles):
            yield from bps.mv(waxs, wa)
            dets = [pil900KW] if wa < 15 else [pil900KW, pil1M]
            yield from bps.mvr(piezo.x, (i + 1) * step_across_sample)

            # Metadata
            name_fmt = "{sample}_{energy}keV_{sdd}m_wa{wax}_ai{ai}_bpm{xbpm}"
            bpm = xbpm2.sumX.get()
            e = energy.energy.position / 1000
            sdd = pil1m_pos.z.position / 1000

            sample_name = name_fmt.format(
                sample=name,
                energy="%.1f" % e,
                sdd="%.0f" % sdd,
                wax=wa,
                ai="%.1f" % incident_angle,
                xbpm="%4.3f" % bpm,
            )
            sample_id(user_name=user_name, sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            # Take data
            yield from bp.count(dets, num=1)

            sample_id(user_name="test", sample_name="test")


def grazing_gradient_Luo_2022_2(t=0.5, incident_angle=0.1):
    """
    Scan gradient sample

    309557 Luo
    Overlaping WAXS essential to cover the detector gaps, no offset in x.

    SmarAct nanopositioner units: micrometers
    Hexapod stage units: milimeters
    Incident angle (piezo.th): degrees

    Params:
        t (float): exposure time,
        incident_angle (float): self explained
    """
    user_name = "PL"
    angles = [0, 2, 18, 20]  # degrees
    step_across_gradient = 2  # mm

    # Sample parameters
    names = ["60nm_TPD_0p2As_-63Cto67C_2022-05-05"]
    sample_edges = [[34700, -32200]]
    sample_margins = [[0, 0]]

    assert len(names) == len(
        sample_edges
    ), f"Number of samples ({len(names)}) is different from number of edges ({len(sample_edges)})"
    assert len(names) == len(
        sample_margins
    ), f"Number of samples ({len(names)}) is different from number of margins ({len(sample_margins)})"

    # Make sure beam is on
    # yield from bps.mv(GV7.open_cmd, 1)
    yield from shopen()
    yield from bps.sleep(3)

    yield from bps.mv(piezo.z, 300)

    for name, edges, margins in zip(names, sample_edges, sample_margins):

        # Check sample name just in case
        name = name.translate({ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+"})

        start_piezo_x = edges[0] - margins[0]
        end_piezo_x = edges[1] + margins[1]
        length = start_piezo_x - end_piezo_x

        positions = [
            1 + i * step_across_gradient for i in range(100) if i * 2 < length / 1000
        ]

        for i, position in enumerate(positions):
            # print('Position {} / {}'.format(i + 1), len(positions))

            new_piezo_x = start_piezo_x - 1000 * position
            yield from bps.mv(piezo.x, new_piezo_x + 200)

            # Full alignment / quick wasn't working well
            try:
                yield from alignement_gisaxs()
            except:
                yield from alignement_gisaxs(0.4)
            yield from bps.mvr(piezo.th, incident_angle)

            yield from bps.mv(piezo.x, new_piezo_x)

            for wa in angles:
                yield from bps.mv(waxs, wa)
                dets = [pil900KW] if wa < 15 else [pil900KW, pil1M]

                # Metadata
                name_fmt = (
                    "{sample}_{energy}keV_{sdd}m_wa{wax}_ai{ai}_pos_{pos}mm_bpm{xbpm}"
                )
                bpm = xbpm2.sumX.get()
                e = energy.energy.position / 1000
                sdd = pil1m_pos.z.position / 1000

                sample_name = name_fmt.format(
                    sample=name,
                    energy="%.1f" % e,
                    sdd="%.0f" % sdd,
                    wax=wa,
                    ai="%.1f" % incident_angle,
                    pos="%.1f" % position,
                    xbpm="%4.3f" % bpm,
                )
                sample_id(user_name=user_name, sample_name=sample_name)

                # Take data
                yield from bp.count(dets, num=1)
                sample_id(user_name="test", sample_name="test")

def atten_move_in(x4=True, x2=True):
    """
    Move 4x + 2x Sn 60 um attenuators in
    """
    print('Moving attenuators in')

    if x4:
        while att1_7.status.get() != 'Open':
            yield from bps.mv(att1_7.open_cmd, 1)
            yield from bps.sleep(1)
    if x2:
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

def engage_detectors():
    """
    Making sure camserver responds and data is taken
    """

    yield from atten_move_in()
    sample_id(user_name='test', sample_name='test')
    print(f"\n\n\n\t=== Making sure detectores are engaged and ready ===")
    yield from bp.count([pil900KW, pil1M])
    yield from atten_move_out()


def grazing_Kritika_2023_3(t=0.5):
    """
    standard GI-S/WAXS
    """
    #names   = [   's01',  's02',  's03',  's04',  's05',  's06',  's07',  's08',  's09',  's10',  's11',  's12',  's13',  's14',  's15', ]
    #piezo_x = [ -56000,  -46500, -39000, -40500, -30000, -19500,  -9500,  -1000,  14000,  22000,  32000,  42000,  51500,  51000,  55500, ]
    #piezo_y = [   4800,    4800,   4800,   4600,   4500,   4500,   4300,   4300,   4200,   4200,   4200,   4100,   3900,   3800,   3800  ]          
    #piezo_z = [   5000,    5000,   5000,   5000,   5000,   5000,   4000,   4000,   4000,   4000,   4000,   3500,   3500,   3500,   3500, ]
    #hexa_x =  [    -14,     -14,    -14,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,   10,       13, ]

    names   = [   's03',  's04',  's09',  's10', ]
    piezo_x = [ -33000,  -23000,  39000,  51000, ]
    piezo_y = [   4600,    4400,   4000,   4000, ]          
    piezo_z = [   5000,    5000,   3500,   3500, ]
    hexa_x =  [      0,       0,      0,      0, ]
    
    
    names = [ n + '-rot90'+ '-inair' + '-2023Oct30' for n in names ]
    #piezo_x = np.asarray(piezo_x) + 1000


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

    waxs_arc = [ 0, 2, 20, 22 ]  # degrees
    x_off = [-500, 0, 500 ]
    incident_angles = [ 0.1 ]
    user_name = 'KJ'

    det_exposure_time(t, t)

    # Make sure cam server engages with the detector
    #yield from engage_detectors()
 
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

                    sample_name = f'{name}{get_scan_md()}_loc{xx}_ai{ai}'

                    sample_id(user_name=user_name, sample_name=sample_name)
                    print(f"\n\n\n\t=== Sample: {sample_name} ===")
                    yield from bp.count(dets)

        yield from bps.mv(piezo.th, ai0)

    sample_id(user_name='test', sample_name='test')
    det_exposure_time(0.5, 0.5)


def grazing_Kritika_2024_1(t=0.5):
    """
    standard GI-S/WAXS
    """
    
    names   = [   's03a', 's03b', 's05a', 's05b',  's10a',  's10b',  's14a',   's14b', ]
    piezo_x = [  -27000,  -26000, -14000, -13000,   -1000,       0,   14000,    15000, ]
    piezo_y = [    2100,    2100,   2200,   2250,    2400,    2400,    2400,     2400, ]          
    piezo_z = [    4000,    4000,   4000,   4000,    4600,    4600,    4600,     4600, ]
    hexa_x =  [ 0 for n in names ]
    
    
    names = [ n + '-rot90alonglonger' for n in names]
    #piezo_x = np.asarray(piezo_x) + 1000


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

    waxs_arc = [ 0, 2, 20, 22 ]  # degrees
    x_off = [0]
    incident_angles = [ 0.1 ]
    user_name = 'KJ'

    det_exposure_time(t, t)

    # Make sure cam server engages with the detector
    #yield from engage_detectors()
 
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

                    sample_name = f'{name}{get_scan_md()}_loc{xx}_ai{ai}'

                    sample_id(user_name=user_name, sample_name=sample_name)
                    print(f"\n\n\n\t=== Sample: {sample_name} ===")
                    yield from bp.count(dets)

        yield from bps.mv(piezo.th, ai0)

    sample_id(user_name='test', sample_name='test')
    det_exposure_time(0.5, 0.5)


### 2024-2 ###
# yield from alignement_gisaxs_doblestack(0.8)

def grazing_Peng_2024_2(t=0.5):
    """
    standard GI-S/WAXS on double stack holder

    bsui - turn on bluesky if crashed
    fg - if by accident ctrl+z in bs window
    """
    """
    # Top sample bar A
    names_1   = [ 'Tcom15-minus9C-b791-85C', 'Tcom15-minus9C-b887-160C', 'Tcom15-minus9C-b935-40C', 'Tcom15-minus9C-B260-110C', 'Tcom14-27C-b886-160C', 'Tcom14-27C-b790-85C', 'Tcom14-27C-B259-110C', 'Tcom14-27C-b934-40C', 'Tcom14-27C-b1030-RT', 'Tcom14-27C-b838-110C', 'Tcom14-27C-b982-60C', 'Tcom14-27C-b1031-RT',] 
    piezo_x_1 = [                    -53000,                     -41000,                    -30000,                     -19000,                  -7000,                  5000,                  18000,                 29000,                 41000,                  52000,                 42000,                 54000,]
    piezo_y_1 = [                     -1500,                      -1500,                     -1500,                      -1500,                  -1500,                 -1500,                  -1500,                 -1500,                 -1500,                  -1500,                 -1500,                 -1500,]          
    piezo_z_1 = [                      6300,                       6300,                      6300,                       6300,                   6300,                  6300,                   6300,                  6300,                  6300,                   6300,                  6300,                  6300,]
    hexa_x_1 =  [                       -12,                        -12,                       -12,                        -12,                    -12,                   -12,                    -12,                   -12,                   -12,                    -12,                    10,                    10,]

    # Bottom sample bar A
    names_2   = ['Tcom14-minus42C-b792-85C', 'Tcom14-minus42C-b840-110C', 'Tcom14-minus42C-b888-160C', 'Tcom14-minus42C-b1035-RT', 'Tcom14-minus42C-b936-40C', 'Tcom14-minus42C-b1034-RT', 'Tcom14-minus42C-B261-110C', 'Tcom14-minus42C-b984-60C', 'Tcom15-minus9C-b839-110C', 'Tcom15-minus9C-b1032-RT', 'Tcom15-minus9C-b1033-RT', 'Tcom15-minus9C-b983-60C',]
    piezo_x_2 = [                    -50000,                      -40000,                      -28000,                     -17000,                      -5000,                       6000,                       17000,                      29000,                      38000,                     29000,                     41000,                     53000,]
    piezo_y_2 = [                      7000,                        7000,                        7000,                       7000,                       7000,                       7000,                        7000,                       7000,                       7000,                      7000,                      7000,                      7000,]          
    piezo_z_2 = [                     -1700,                       -1700,                       -1700,                      -1700,                      -1700,                      -1700,                       -1700,                      -1700,                      -1700,                     -1700,                     -1700,                     -1700,]
    hexa_x_2 =  [                       -12,                         -12,                         -12,                        -12,                        -12,                        -12,                         -12,                        -12,                        -12,                        10,                        10,                        10,]
    
    names = [ '20240604-180nm-A-' + n for n in names]
    """

    """
    # Top sample bar B
    names_1   = [ 'Tcom15-minus9C-b1064-RT', 'Tcom15-minus9C-b899-160C', 'Tcom15-minus9C-b950-40C', 'Tcom15-minus9C-B272-110C', 'Tcom14-27C-b898-160C', 'Tcom14-27C-b1063-RT', 'Tcom14-27C-B271-110C', 'Tcom14-27C-b949-40C', 'Tcom14-27C-b802-85C', 'Tcom14-27C-b850-110C', 'Tcom14-27C-b997-60C', 'Tcom14-27C-b803-85C',] 
    piezo_x_1 = [                    -51000,                     -39000,                    -28000,                     -16000,                  -4000,                  8000,                  18000,                 29000,                 40000,                  51000,                 41000,                 51000,]
    piezo_y_1 = [                     -1500,                      -1500,                     -1500,                      -1500,                  -1500,                 -1500,                  -1500,                 -1500,                 -1500,                  -1500,                 -1500,                 -1500,]          
    piezo_z_1 = [                      6300,                       6300,                      6300,                       6300,                   6300,                  6300,                   6300,                  6300,                  6300,                   6300,                  6300,                  6300,]
    hexa_x_1 =  [                       -12,                        -12,                       -12,                        -12,                    -12,                   -12,                    -12,                   -12,                   -12,                    -12,                    10,                    10,]

    # Bottom sample bar B
    names_2   = ['Tcom16-minus42C-b1065-RT', 'Tcom16-minus42C-b852-110C', 'Tcom16-minus42C-b900-160C', 'Tcom16-minus42C-b807-85C', 'Tcom16-minus42C-b951-40C', 'Tcom16-minus42C-b806-85C', 'Tcom16-minus42C-B273-110C', 'Tcom16-minus42C-b999-60C', 'Tcom15-minus9C-b851-110C', 'Tcom15-minus9C-b804-85C', 'Tcom15-minus9C-b805-85C', 'Tcom15-minus9C-b998-60C',]
    piezo_x_2 = [                    -50000,                      -38000,                      -27000,                     -15000,                      -3000,                       8000,                       19000,                      30000,                      41000,                     30000,                     41000,                     52000,]
    piezo_y_2 = [                      7000,                        7000,                        7000,                       7000,                       7000,                       7000,                        7000,                       7000,                       7000,                      7000,                      7000,                      7000,]          
    piezo_z_2 = [                     -1700,                       -1700,                       -1700,                      -1700,                      -1700,                      -1700,                       -1700,                      -1700,                      -1700,                     -1700,                     -1700,                     -1700,]
    hexa_x_2 =  [                       -12,                         -12,                         -12,                        -12,                        -12,                        -12,                         -12,                        -12,                        -12,                        10,                        10,                        10,]


    names   = names_1   + names_2
    piezo_x = piezo_x_1 + piezo_x_2
    piezo_y = piezo_y_1 + piezo_y_2
    piezo_z = piezo_z_1 + piezo_z_2
    hexa_x  = hexa_x_1  + hexa_x_2

    names = [ '20240610-370nm-B-' + n for n in names]

    Really is 330nm
    """    
    """
    # Top sample bar C
    names_1   = [ 'Tcom15-minus9C-b809-85C', 'Tcom15-minus9C-b902-160C', 'Tcom15-minus9C-b953-40C', 'Tcom15-minus9C-B275-110C', 'Tcom14-27C-b901-160C', 'Tcom14-27C-b808-85C', 'Tcom14-27C-B274-110C', 'Tcom14-27C-b952-40C', 'Tcom14-27C-b853-110C', 'Tcom14-27C-b1066-RT', 'Tcom14-27C-b1000-60C', 'Tcom14-27C-b854-110C',] 
    piezo_x_1 = [                    -52000,                     -39000,                    -28000,                     -18000,                  -7000,                  4000,                  16000,                 27000,                 37000,                  49000,                 38000,                 50000,]
    piezo_y_1 = [                     -1500,                      -1500,                     -1500,                      -1500,                  -1500,                 -1500,                  -1500,                 -1500,                 -1500,                  -1500,                 -1500,                 -1500,]          
    piezo_z_1 = [                      6300,                       6300,                      6300,                       6300,                   6300,                  6300,                   6300,                  6300,                  6300,                   6300,                  6300,                  6300,]
    hexa_x_1 =  [                       -12,                        -12,                       -12,                        -12,                    -12,                   -12,                    -12,                   -12,                   -12,                    -12,                    10,                    10,]

    # Bottom sample bar C
    names_2   = ['Tcom16-minus42C-b810-85C', 'Tcom16-minus42C-b1068-RT', 'Tcom16-minus42C-b903-160C', 'Tcom16-minus42C-b858-110C', 'Tcom16-minus42C-b954-40C', 'Tcom16-minus42C-b857-110C', 'Tcom16-minus42C-B276-110C', 'Tcom16-minus42C-b1002-60C', 'Tcom15-minus9C-b1067-RT', 'Tcom15-minus9C-b855-110C', 'Tcom15-minus9C-b856-110C', 'Tcom15-minus9C-b1001-60C',]
    piezo_x_2 = [                    -51000,                      -40000,                      -28000,                     -17000,                      -6000,                       5000,                       16000,                      26000,                      37000,                     28000,                     38000,                     50000,]
    piezo_y_2 = [                      7000,                        7000,                        7000,                       7000,                       7000,                       7000,                        7000,                       7000,                       7000,                      7000,                      7000,                      7000,]          
    piezo_z_2 = [                     -1700,                       -1700,                       -1700,                      -1700,                      -1700,                      -1700,                       -1700,                      -1700,                      -1700,                     -1700,                     -1700,                     -1700,]
    hexa_x_2 =  [                       -12,                         -12,                         -12,                        -12,                        -12,                        -12,                         -12,                        -12,                        -12,                        10,                        10,                        10,]


    names   = names_1   + names_2
    piezo_x = piezo_x_1 + piezo_x_2
    piezo_y = piezo_y_1 + piezo_y_2
    piezo_z = piezo_z_1 + piezo_z_2
    hexa_x  = hexa_x_1  + hexa_x_2

    names = [ '20240611-270nm-C-' + n for n in names]
    """
    """
    # Top sample bar D
    names_1   = [ 'Tcom15-minus9C-b818-85C', 'Tcom15-minus9C-b914-160C', 'Tcom15-minus9C-b962-40C', 'Tcom15-minus9C-B284-110C', 'Tcom14-27C-b913-160C', 'Tcom14-27C-b817-85C', 'Tcom14-27C-B283-110C', 'Tcom14-27C-b961-40C', 'Tcom14-27C-Si', 'Tcom14-27C-b865-110C', 'Tcom14-27C-b1009-60C', 'Tcom14-27C-b1078-RT',] 
    piezo_x_1 = [                    -52000,                     -41000,                    -30000,                     -19000,                  -8000,                  3000,                  14000,                 26000,           37000,                  48000,                 36000,                  48000,]
    piezo_y_1 = [                     -1500,                      -1500,                     -1500,                      -1500,                  -1500,                 -1500,                  -1500,                 -1500,           -1500,                  -1500,                 -1500,                  -1500,]          
    piezo_z_1 = [                      6300,                       6300,                      6300,                       6300,                   6300,                  6300,                   6300,                  6300,            6300,                   6300,                  6300,                   6300,]
    hexa_x_1 =  [                       -12,                        -12,                       -12,                        -12,                    -12,                   -12,                    -12,                   -12,             -12,                    -12,                    10,                     10,]

    # Bottom sample bar D
    names_2   = ['Tcom16-minus42C-b819-85C', 'Tcom16-minus42C-b867-110C', 'Tcom16-minus42C-b915-160C',   'Tcom16-minus42C-Si', 'Tcom16-minus42C-b963-40C', 'Tcom16-minus42C-b1080-RT', 'Tcom16-minus42C-B285-110C', 'Tcom16-minus42C-b1011-60C', 'Tcom15-minus9C-b866-110C', 'Tcom15-minus9C-Si', 'Tcom15-minus9C-b1079-RT', 'Tcom15-minus9C-b1010-60C',]
    piezo_x_2 = [                    -50000,                      -39000,                      -26000,                 -15000,                      -3000,                       8000,                       20000,                      31000,                      43000,                31000,                     43000,                      52000,]
    piezo_y_2 = [                      7000,                        7000,                        7000,                   7000,                       7000,                       7000,                        7000,                       7000,                       7000,                 7000,                      7000,                       7000,]          
    piezo_z_2 = [                     -1700,                       -1700,                       -1700,                  -1700,                      -1700,                      -1700,                       -1700,                      -1700,                      -1700,                -1700,                     -1700,                      -1700,]
    hexa_x_2 =  [                       -12,                         -12,                         -12,                    -12,                        -12,                        -12,                         -12,                        -12,                        -12,                   10,                        10,                         10,]


    names   = names_1   + names_2
    piezo_x = piezo_x_1 + piezo_x_2
    piezo_y = piezo_y_1 + piezo_y_2
    piezo_z = piezo_z_1 + piezo_z_2
    hexa_x  = hexa_x_1  + hexa_x_2

    names = [ '20240614-1320nm-D-' + n for n in names]
    """
    """
    # Top sample bar E
    names_1   = [ 'Tcom15-minus9C-b812-85C', 'Tcom15-minus9C-b1070-RT', 'Tcom15-minus9C-b956-40C', 'Tcom15-minus9C-B278-110C', 'Tcom14-27C-b1069-RT', 'Tcom14-27C-b811-85C', 'Tcom14-27C-B277-110C', 'Tcom14-27C-b955-40C', 'Tcom14-27C-b904-160C', 'Tcom14-27C-b859-110C', 'Tcom14-27C-b1003-60C', 'Tcom14-27C-b905-160C',] 
    piezo_x_1 = [                    -51000,                     -40000,                   -28000,                     -17000,                 -6000,                  5000,                  16000,                 28000,                  39000,                  50000,                  38000,                  49000,]
    piezo_y_1 = [                     -1500,                      -1500,                    -1500,                      -1500,                 -1500,                 -1500,                  -1500,                 -1500,                  -1500,                  -1500,                  -1500,                  -1500,]          
    piezo_z_1 = [                      6300,                       6300,                     6300,                       6300,                  6300,                  6300,                   6300,                  6300,                   6300,                   6300,                   6300,                   6300,]
    hexa_x_1 =  [                       -12,                        -12,                      -12,                        -12,                   -12,                   -12,                    -12,                   -12,                    -12,                    -12,                     10,                     10,]

    # Bottom sample bar E
    names_2   = ['Tcom16-minus42C-b813-85C', 'Tcom16-minus42C-b861-110C', 'Tcom16-minus42C-b1071-RT', 'Tcom16-minus42C-b909-160C', 'Tcom16-minus42C-b957-40C', 'Tcom16-minus42C-b908-160C', 'Tcom16-minus42C-B279-110C', 'Tcom16-minus42C-b1005-60C', 'Tcom15-minus9C-b860-110C', 'Tcom15-minus9C-b906-160C', 'Tcom15-minus9C-b907-160C', 'Tcom15-minus9C-b1004-60C',]
    piezo_x_2 = [                    -49000,                      -37000,                     -25000,                      -13000,                      -1000,                        11000,                       23000,                       33000,                      43000,                      33000,                      44000,                      55000,]
    piezo_y_2 = [                      7000,                        7000,                       7000,                        7000,                       7000,                        7000,                        7000,                        7000,                       7000,                       7000,                       7000,                       7000,]          
    piezo_z_2 = [                     -1700,                       -1700,                      -1700,                       -1700,                      -1700,                       -1700,                       -1700,                       -1700,                      -1700,                      -1700,                      -1700,                      -1700,]
    hexa_x_2 =  [                       -12,                         -12,                        -12,                         -12,                        -12,                         -12,                         -12,                         -12,                        -12,                         10,                         10,                         10,]


    names   = names_1   + names_2
    piezo_x = piezo_x_1 + piezo_x_2
    piezo_y = piezo_y_1 + piezo_y_2
    piezo_z = piezo_z_1 + piezo_z_2
    hexa_x  = hexa_x_1  + hexa_x_2

    names = [ '20240612-220nm-E-' + n for n in names]
    """


    """
    # Top sample bar F
    names_1   = [ 'Tcom15-minus9C-b815-85C', 'Tcom15-minus9C-b911-160C', 'Tcom15-minus9C-b959-40C', 'Tcom15-minus9C-B281-110C', 'Tcom14-27C-b910-160C', 'Tcom14-27C-b814-85C', 'Tcom14-27C-B280-110C', 'Tcom14-27C-b958-40C', 'Tcom14-27C-b1072-RT', 'Tcom14-27C-b862-110C', 'Tcom14-27C-b1006-60C', 'Tcom14-27C-b1073-RT',] 
    piezo_x_1 = [                    -52000,                     -40000,                    -28000,                     -17000,                  -6000,                  6000,                  18000,                 29000,                 41000,                  52000,                  41000,                 53000,]
    piezo_y_1 = [                     -1500,                      -1500,                     -1500,                      -1500,                  -1500,                 -1500,                  -1500,                 -1500,                 -1500,                  -1500,                  -1500,                 -1500,]          
    piezo_z_1 = [                      6300,                       6300,                      6300,                       6300,                   6300,                  6300,                   6300,                  6300,                  6300,                   6300,                   6300,                  6300,]
    hexa_x_1 =  [                       -12,                        -12,                       -12,                        -12,                    -12,                   -12,                    -12,                   -12,                   -12,                    -12,                     10,                    10,]

    # Bottom sample bar F
    names_2   = ['Tcom16-minus42C-b816-85C', 'Tcom16-minus42C-b864-110C', 'Tcom16-minus42C-b912-160C', 'Tcom16-minus42C-b1077-RT', 'Tcom16-minus42C-b960-40C', 'Tcom16-minus42C-b1076-RT', 'Tcom16-minus42C-B282-110C', 'Tcom16-minus42C-b1008-60C', 'Tcom15-minus9C-b863-110C', 'Tcom15-minus9C-b1074-RT', 'Tcom15-minus9C-b1075-RT', 'Tcom15-minus9C-b1007-60C',]
    piezo_x_2 = [                    -49000,                      -37000,                      -26000,                     -15000,                      -4000,                      8000,                       19000,                       30000,                      41000,                     31000,                     42000,                      54000,]
    piezo_y_2 = [                      7000,                        7000,                        7000,                       7000,                       7000,                       7000,                        7000,                        7000,                       7000,                      7000,                      7000,                       7000,]          
    piezo_z_2 = [                     -1700,                       -1700,                       -1700,                      -1700,                      -1700,                      -1700,                       -1700,                       -1700,                      -1700,                     -1700,                     -1700,                      -1700,]
    hexa_x_2 =  [                       -12,                         -12,                         -12,                        -12,                        -12,                        -12,                         -12,                         -12,                        -12,                        10,                        10,                         10,]


    names   = names_1   + names_2
    piezo_x = piezo_x_1 + piezo_x_2
    piezo_y = piezo_y_1 + piezo_y_2
    piezo_z = piezo_z_1 + piezo_z_2
    hexa_x  = hexa_x_1  + hexa_x_2

    names = [ '20240613-6000nm-F-' + n for n in names]
    """
    """
        # Top sample bar G
    names_1   = [ 'Tcom15-minus9C-b797-85C', 'Tcom15-minus9C-b893-160C', 'Tcom15-minus9C-b943-40C', 'Tcom15-minus9C-B266-110C', 'Tcom14-27C-b892-160C', 'Tcom14-27C-b796-85C', 'Tcom14-27C-B265-110C', 'Tcom14-27C-b941-40C', 'Tcom14-27C-b940-40C-repeat', 'Tcom14-27C-b844-110C', 'Tcom14-27C-b988-60C', 'Tcom14-27C-b1057-RT',] 
    piezo_x_1 = [                    -52000,                     -40000,                    -28000,                     -18000,                  -7000,                  5000,                  17000,                 28000,                40500,                  51000,                  41000,                 52000,]
    piezo_y_1 = [                     -1500,                      -1500,                     -1500,                      -1500,                  -1500,                 -1500,                  -1500,                 -1500,                -1500,                  -1500,                  -1500,                 -1500,]          
    piezo_z_1 = [                      6300,                       6300,                      6300,                       6300,                   6300,                  6300,                   6300,                  6300,                 6300,                   6300,                   6300,                  6300,]
    hexa_x_1 =  [                       -12,                        -12,                       -12,                        -12,                    -12,                   -12,                    -12,                   -12,                  -12,                    -12,                     10,                    10,]

    # Bottom sample bar G
    names_2   = ['Tcom16-minus42C-b798-85C', 'Tcom16-minus42C-b846-110C', 'Tcom16-minus42C-b894-160C', 'Tcom16-minus42C-b945-40C', 'Tcom16-minus42C-b944-40C', 'Tcom16-minus42C-b1059-RT', 'Tcom16-minus42C-B267-110C', 'Tcom16-minus42C-b990-60C', 'Tcom15-minus9C-b845-110C', 'Tcom15-minus9C-b942-40C', 'Tcom15-minus9C-b1058-RT', 'Tcom15-minus9C-b989-60C',]
    piezo_x_2 = [                    -50000,                      -40000,                      -29000,                     -18000,                      -7000,                       4000,                       16000,                      27000,                      39000,                     28000,                     39000,                     51000,]
    piezo_y_2 = [                      7000,                        7000,                        7000,                       7000,                       7000,                       7000,                        7000,                       7000,                       7000,                      7000,                      7000,                      7000,]          
    piezo_z_2 = [                     -1700,                       -1700,                       -1700,                      -1700,                      -1700,                      -1700,                       -1700,                      -1700,                      -1700,                     -1700,                     -1700,                     -1700,]
    hexa_x_2 =  [                       -12,                         -12,                         -12,                        -12,                        -12,                        -12,                         -12,                        -12,                        -12,                        10,                        10,                        10,]


    names   = names_1   + names_2
    piezo_x = piezo_x_1 + piezo_x_2
    piezo_y = piezo_y_1 + piezo_y_2
    piezo_z = piezo_z_1 + piezo_z_2
    hexa_x  = hexa_x_1  + hexa_x_2

    names = [ '20240607-490nm-G-' + n for n in names]
    """    
    """
        # Top sample bar H
    names_1   = [ 'Tcom15-minus9C-b800-85C', 'Tcom15-minus9C-b896-160C', 'Tcom15-minus9C-b947-40C', 'Tcom15-minus9C-B269-110C', 'Tcom14-27C-b895-160C', 'Tcom14-27C-b799-85C', 'Tcom14-27C-B268-110C', 'Tcom14-27C-b946-40C', 'Tcom14-27C-b991-60C', 'Tcom14-27C-b847-110C', 'Tcom14-27C-b1060-RT', 'Tcom14-27C-b992-60C',] 
    piezo_x_1 = [                    -52000,                     -40000,                    -29000,                     -18000,                  -6000,                  6000,                  18000,                 29000,                41000,                  52000,                   41000,                53000,]
    piezo_y_1 = [                     -1500,                      -1500,                     -1500,                      -1500,                  -1500,                 -1500,                  -1500,                 -1500,                -1500,                  -1500,                   -1500,                -1500,]          
    piezo_z_1 = [                      6300,                       6300,                      6300,                       6300,                   6300,                  6300,                   6300,                  6300,                 6300,                   6300,                    6300,                 6300,]
    hexa_x_1 =  [                       -12,                        -12,                       -12,                        -12,                    -12,                   -12,                    -12,                   -12,                  -12,                    -12,                      10,                   10,]

    # Bottom sample bar H
    names_2   = ['Tcom16-minus42C-b801-85C', 'Tcom16-minus42C-b849-110C', 'Tcom16-minus42C-b897-160C', 'Tcom16-minus42C-b996-60C', 'Tcom16-minus42C-b948-40C', 'Tcom16-minus42C-b995-60C', 'Tcom16-minus42C-B270-110C', 'Tcom16-minus42C-b 1062-RT', 'Tcom15-minus9C-b848-110C', 'Tcom15-minus9C-b993-60C', 'Tcom15-minus9C-b994-60C', 'Tcom15-minus9C-b1061-RT',]
    piezo_x_2 = [                    -50000,                      -39000,                      -28000,                     -15000,                      -4000,                       8000,                       19000,                       30000,                      41000,                     30000,                     41000,                     52000,]
    piezo_y_2 = [                      7000,                        7000,                        7000,                       7000,                       7000,                       7000,                        7000,                        7000,                       7000,                      7000,                      7000,                      7000,]          
    piezo_z_2 = [                     -1700,                       -1700,                       -1700,                      -1700,                      -1700,                      -1700,                       -1700,                       -1700,                      -1700,                     -1700,                     -1700,                     -1700,]
    hexa_x_2 =  [                       -12,                         -12,                         -12,                        -12,                        -12,                        -12,                         -12,                         -12,                        -12,                        10,                        10,                        10,]
    

    names   = names_1   + names_2
    piezo_x = piezo_x_1 + piezo_x_2
    piezo_y = piezo_y_1 + piezo_y_2
    piezo_z = piezo_z_1 + piezo_z_2
    hexa_x  = hexa_x_1  + hexa_x_2

    names = [ '20240609-400nm-H-' + n for n in names]
    """
    
    """
        # Top sample bar G - REPEAT
    names_1   = ['Tcom14-27C-b940-40C-repeat',] 
    piezo_x_1 = [40500,]
    piezo_y_1 = [-1500,]          
    piezo_z_1 = [6300,]
    hexa_x_1 =  [-12,]

    names   = names_1 
    piezo_x = piezo_x_1 
    piezo_y = piezo_y_1 
    piezo_z = piezo_z_1 
    hexa_x  = hexa_x_1  

    names = [ '20240607-490nm-G-' + n for n in names]
    """
    
    """
        # Top sample bar I
    names_1   = [ 'Tcom15-minus9C-b821-85C', 'Tcom15-minus9C-b917-160C', 'Tcom15-minus9C-b965-40C', 'Tcom15-minus9C-B287-110C', 'Tcom14-27C-b916-160C', 'Tcom14-27C-b820-85C', 'Tcom14-27C-B286-110C', 'Tcom14-27C-b964-40C', 'Tcom14-27C-Si', 'Tcom14-27C-b868-110C', 'Tcom14-27C-b1012-60C', 'Tcom14-27C-b1081-RT', 'OG-180nm-b1034-RT',] 
    piezo_x_1 = [                    -54000,                     -43000,                    -32000,                     -21000,                 -10000,                  1000,                  12000,                 24000,           35000,                  47000,                  37000,                 48000,               55000,]
    piezo_y_1 = [                     -1500,                      -1500,                     -1500,                      -1500,                  -1500,                 -1500,                  -1500,                 -1500,           -1500,                  -1500,                  -1500,                 -1500,               -1500,]          
    piezo_z_1 = [                      6300,                       6300,                      6300,                       6300,                   6300,                  6300,                   6300,                  6300,            6300,                   6300,                   6300,                  6300,                6300,]
    hexa_x_1 =  [                       -12,                        -12,                       -12,                        -12,                    -12,                   -12,                    -12,                   -12,             -12,                    -12,                     10,                    10,                  15,]

    # Bottom sample bar I
    names_2   = ['Tcom16-minus42C-b822-85C', 'Tcom16-minus42C-b870-110C', 'Tcom16-minus42C-b918-160C', 'Tcom16-minus42C-Si', 'Tcom16-minus42C-b966-40C', 'Tcom16-minus42C-b1083-RT', 'Tcom16-minus42C-B288-110C', 'Tcom16-minus42C-b1014-60C', 'Tcom15-minus9C-b869-110C', 'Tcom15-minus9C-Si', 'Tcom15-minus9C-b1082-RT', 'Tcom15-minus9C-b1013-60C',]
    piezo_x_2 = [                    -50000,                      -39000,                      -28000,               -18000,                      -5000,                       5000,                       19000,                       30000,                      42000,               30000,                     43000,                      55000,]
    piezo_y_2 = [                      7000,                        7000,                        7000,                 7000,                       7000,                       7000,                        7000,                        7000,                       7000,                7000,                      7000,                       7000,]          
    piezo_z_2 = [                     -1700,                       -1700,                       -1700,                -1700,                      -1700,                      -1700,                       -1700,                       -1700,                      -1700,               -1700,                     -1700,                      -1700,]
    hexa_x_2 =  [                       -12,                         -12,                         -12,                  -12,                        -12,                        -12,                         -12,                         -12,                        -12,                  10,                        10,                         10,]
    

    names   = names_1   + names_2
    piezo_x = piezo_x_1 + piezo_x_2
    piezo_y = piezo_y_1 + piezo_y_2
    piezo_z = piezo_z_1 + piezo_z_2
    hexa_x  = hexa_x_1  + hexa_x_2

    names = [ '20240615-730nm-I-' + n for n in names]
    """

    """
        # Top sample bar I
    names_1   = [ 'Tcom15-minus9C-b821-85C_repeat', 'Tcom15-minus9C-b917-160C_repeat',] 
    piezo_x_1 = [                           -55000,                            -44000,]
    piezo_y_1 = [                            -1500,                             -1500,]          
    piezo_z_1 = [                             6300,                              6300,]
    hexa_x_1 =  [                              -12,                               -12,]

    # Bottom sample bar I
    names_2   = ['Tcom16-minus42C-Si',]
    piezo_x_2 = [              -18000,]
    piezo_y_2 = [                7000,]          
    piezo_z_2 = [               -1700,]
    hexa_x_2 =  [                 -12,]
    

    names   = names_1   + names_2
    piezo_x = piezo_x_1 + piezo_x_2
    piezo_y = piezo_y_1 + piezo_y_2
    piezo_z = piezo_z_1 + piezo_z_2
    hexa_x  = hexa_x_1  + hexa_x_2

    names = [ '20240615-730nm-I-' + n for n in names]
    """

    """
    # Top sample bar J
    names_1   = [ 'Tcom15-minus9C-b824-85C-1', 'Tcom15-minus9C-b920-160C-1', 'Tcom15-minus9C-b968-40C-1', 'Tcom15-minus9C-B290-110C-1', 'Tcom14-27C-b919-160C-1', 'Tcom14-27C-b823-85C-1', 'Tcom14-27C-B289-110C-1', 'Tcom14-27C-b967-40C-1', 'Tcom14-27C-b1084RT', 'Tcom14-27C-b871-110C', 'Tcom14-27C-b1015-60C', 'Tcom14-27C-b1085-RT', 'OG-1320nm-Si',] 
    piezo_x_1 = [                    -52500,                     -41500,                    -30500,                     -18500,                  -7500,                  4500,                  16500,                 27500,                38000,                  49000,                  40000,                 51000,          55000,]
    piezo_y_1 = [                     -1500,                      -1500,                     -1500,                      -1500,                  -1500,                 -1500,                  -1500,                 -1500,                -1500,                  -1500,                  -1500,                 -1500,          -1500,]          
    piezo_z_1 = [                      6300,                       6300,                      6300,                       6300,                   6300,                  6300,                   6300,                  6300,                 6300,                   6300,                   6300,                  6300,           6300,]
    hexa_x_1 =  [                       -12,                        -12,                       -12,                        -12,                    -12,                   -12,                    -12,                   -12,                  -12,                    -12,                     10,                    10,             16,]

    # Bottom sample bar J
    names_2   = ['Tcom16-minus42C-b825-85C', 'Tcom16-minus42C-b873-110C', 'Tcom16-minus42C-b921-160C', 'Tcom16-minus42C-b1089-RT', 'Tcom16-minus42C-b969-40C', 'Tcom16-minus42C-b1088-RT', 'Tcom16-minus42C-B291-110C', 'Tcom16-minus42C-b1017-60C', 'Tcom15-minus9C-b872-110C', 'Tcom15-minus9C-b1086-RT', 'Tcom15-minus9C-b1087-RT', 'Tcom15-minus9C-b1016-60C',]
    piezo_x_2 = [                    -49000,                      -38000,                      -27000,                     -16000,                      -5000,                       7000,                       19000,                       30000,                      42000,                     30000,                     42000,                      54000,]
    piezo_y_2 = [                      7000,                        7000,                        7000,                       7000,                       7000,                       7000,                        7000,                        7000,                       7000,                      7000,                      7000,                       7000,]          
    piezo_z_2 = [                     -1700,                       -1700,                       -1700,                      -1700,                      -1700,                      -1700,                       -1700,                       -1700,                      -1700,                     -1700,                     -1700,                      -1700,]
    hexa_x_2 =  [                       -12,                         -12,                         -12,                        -12,                        -12,                        -12,                         -12,                         -12,                        -12,                        10,                        10,                         10,]
    

    names   = names_1   + names_2
    piezo_x = piezo_x_1 + piezo_x_2
    piezo_y = piezo_y_1 + piezo_y_2
    piezo_z = piezo_z_1 + piezo_z_2
    hexa_x  = hexa_x_1  + hexa_x_2

    names = [ '20240616-940nm-J-' + n for n in names]
    """
    """
        # Top sample bar J
    names_1   = [ 'Tcom15-minus9C-b824-85C-repeat', 'Tcom15-minus9C-b920-160C-repeat', 'Tcom15-minus9C-b968-40C-repeat', 'Tcom15-minus9C-B290-110C-repeat', 'Tcom14-27C-b919-160C-repeat', 'Tcom14-27C-b823-85C-repeat', 'Tcom14-27C-B289-110C-1', 'Tcom14-27C-b967-40C-repeat', ] 
    piezo_x_1 = [                           -52500,                            -41500,                    -30500,                                   -18500,                         -7500,                         4500,                    16500,                        27500, ]
    piezo_y_1 = [                            -1500,                             -1500,                     -1500,                                    -1500,                         -1500,                        -1500,                    -1500,                        -1500, ]          
    piezo_z_1 = [                             6300,                              6300,                      6300,                                     6300,                          6300,                         6300,                     6300,                         6300, ]
    hexa_x_1 =  [                              -12,                               -12,                       -12,                                      -12,                           -12,                          -12,                      -12,                          -12, ]

    # Bottom sample bar J
    names_2   = []
    piezo_x_2 = []
    piezo_y_2 = []          
    piezo_z_2 = []
    hexa_x_2 =  []
    
    
    names   = names_1   + names_2
    piezo_x = piezo_x_1 + piezo_x_2
    piezo_y = piezo_y_1 + piezo_y_2
    piezo_z = piezo_z_1 + piezo_z_2
    hexa_x  = hexa_x_1  + hexa_x_2

    names = [ '20240616-940nm-J-' + n for n in names]
    """
 
    """
    # Top sample bar K
    names_1   = [ 'Tcom15-minus9C-b827-85C', 'Tcom15-minus9C-b923-160C', 'Tcom15-minus9C-b971-40C', 'Tcom15-minus9C-B293-110C', 'Tcom14-27C-b922-160C', 'Tcom14-27C-b826-85C', 'Tcom14-27C-B292-110C', 'Tcom14-27C-b970-40C',      'Tcom14-27C-Si', 'Tcom14-27C-b874-110C', 'Tcom14-27C-b1018-60C', 'Tcom14-27C-b1090-RT', 'OG-180nm-Si',] 
    piezo_x_1 = [                    -54000,                     -43000,                    -31000,                     -20000,                  -9000,                  2000,                  14000,                 25000,                35000,                  46000,                  35000,                 47000,         54000,]
    piezo_y_1 = [                     -1500,                      -1500,                     -1500,                      -1500,                  -1500,                 -1500,                  -1500,                 -1500,                -1500,                  -1500,                  -1500,                 -1500,         -1500,]          
    piezo_z_1 = [                      6300,                       6300,                      6300,                       6300,                   6300,                  6300,                   6300,                  6300,                 6300,                   6300,                   6300,                  6300,          6300,]
    hexa_x_1 =  [                       -12,                        -12,                       -12,                        -12,                    -12,                   -12,                    -12,                   -12,                  -12,                    -12,                     10,                    10,            15,]

    # Bottom sample bar K
    names_2   = ['Tcom16-minus42C-b828-85C', 'Tcom16-minus42C-b876-110C', 'Tcom16-minus42C-b924-160C',       'Tcom16-minus42C-Si', 'Tcom16-minus42C-b972-40C', 'Tcom16-minus42C-b1092-RT', 'Tcom16-minus42C-B294-110C', 'Tcom16-minus42C-b1020-60C', 'Tcom15-minus9C-b875-110C',       'Tcom15-minus9C-Si', 'Tcom15-minus9C-b1091-RT', 'Tcom15-minus9C-b1019-60C',]
    piezo_x_2 = [                    -49000,                      -38000,                      -26000,                     -15000,                      -5000,                       7000,                       18000,                       30000,                      41000,                     30000,                     41000,                      53000,]
    piezo_y_2 = [                      7000,                        7000,                        7000,                       7000,                       7000,                       7000,                        7000,                        7000,                       7000,                      7000,                      7000,                       7000,]          
    piezo_z_2 = [                     -1700,                       -1700,                       -1700,                      -1700,                      -1700,                      -1700,                       -1700,                       -1700,                      -1700,                     -1700,                     -1700,                      -1700,]
    hexa_x_2 =  [                       -12,                         -12,                         -12,                        -12,                        -12,                        -12,                         -12,                         -12,                        -12,                        10,                        10,                         10,]
    

    names   = names_1   + names_2
    piezo_x = piezo_x_1 + piezo_x_2
    piezo_y = piezo_y_1 + piezo_y_2
    piezo_z = piezo_z_1 + piezo_z_2
    hexa_x  = hexa_x_1  + hexa_x_2

    names = [ '20240617-130nm-K-' + n for n in names]
    """

    """
     # Top sample bar K
    names_1   = [] 
    piezo_x_1 = []
    piezo_y_1 = []          
    piezo_z_1 = []
    hexa_x_1 =  []

    # Bottom sample bar K
    names_2   = ['Tcom15-minus9C-Si',]
    piezo_x_2 = [              29000,]
    piezo_y_2 = [               7000,]          
    piezo_z_2 = [              -1700,]
    hexa_x_2 =  [                 10,]
    

    names   = names_1   + names_2
    piezo_x = piezo_x_1 + piezo_x_2
    piezo_y = piezo_y_1 + piezo_y_2
    piezo_z = piezo_z_1 + piezo_z_2
    hexa_x  = hexa_x_1  + hexa_x_2

    names = [ '20240617-130nm-K-' + n for n in names]
    """
    """
        # Top sample bar L
    names_1   = [ 'Tcom15-minus9C-b830-85C', 'Tcom15-minus9C-b926-160C', 'Tcom15-minus9C-b974-40C', 'Tcom15-minus9C-B296-110C', 'Tcom14-27C-b925-160C', 'Tcom14-27C-b829-85C', 'Tcom14-27C-B295-110C', 'Tcom14-27C-b973-40C',      'Tcom14-27C-Si', 'Tcom14-27C-b877-110C', 'Tcom14-27C-b1021-60C', 'Tcom14-27C-b1107-RT', 'OG-270nm-b857-110C',] 
    piezo_x_1 = [                    -53000,                     -42000,                    -28000,                     -18000,                  -7000,                  4000,                  16000,                 28000,                39000,                  50000,                  39000,                 51000,                54000,]
    piezo_y_1 = [                     -1500,                      -1500,                     -1500,                      -1500,                  -1500,                 -1500,                  -1500,                 -1500,                -1500,                  -1500,                  -1500,                 -1500,                -1500,]          
    piezo_z_1 = [                      6300,                       6300,                      6300,                       6300,                   6300,                  6300,                   6300,                  6300,                 6300,                   6300,                   6300,                  6300,                 6300,]
    hexa_x_1 =  [                       -12,                        -12,                       -12,                        -12,                    -12,                   -12,                    -12,                   -12,                  -12,                    -12,                     10,                    10,                   21,]

    # Bottom sample bar L
    names_2   = ['Tcom16-minus42C-b831-85C', 'Tcom16-minus42C-b879-110C', 'Tcom16-minus42C-b927-160C',       'Tcom16-minus42C-Si', 'Tcom16-minus42C-b975-40C', 'Tcom16-minus42C-b1109-RT', 'Tcom16-minus42C-B297-110C', 'Tcom16-minus42C-b1023-60C', 'Tcom15-minus9C-b878-110C',       'Tcom15-minus9C-Si', 'Tcom15-minus9C-b1108-RT', 'Tcom15-minus9C-b1022-60C',]
    piezo_x_2 = [                    -50000,                      -39000,                      -29000,                     -16000,                      -6000,                       9000,                       19000,                       31000,                      43000,                     32000,                     43000,                      54000,]
    piezo_y_2 = [                      7000,                        7000,                        7000,                       7000,                       7000,                       7000,                        7000,                        7000,                       7000,                      7000,                      7000,                       7000,]          
    piezo_z_2 = [                     -1700,                       -1700,                       -1700,                      -1700,                      -1700,                      -1700,                       -1700,                       -1700,                      -1700,                     -1700,                     -1700,                      -1700,]
    hexa_x_2 =  [                       -12,                         -12,                         -12,                        -12,                        -12,                        -12,                         -12,                         -12,                        -12,                        10,                        10,                         10,]
    

    names   = names_1   + names_2
    piezo_x = piezo_x_1 + piezo_x_2
    piezo_y = piezo_y_1 + piezo_y_2
    piezo_z = piezo_z_1 + piezo_z_2
    hexa_x  = hexa_x_1  + hexa_x_2

    names = [ '20240618-2000nm-L-' + n for n in names]
    """

    """
       # Top sample bar L
    names_1   = ['OG-270nm-b857-110C-repeat',] 
    piezo_x_1 = [                      54000,]
    piezo_y_1 = [                      -1500,]          
    piezo_z_1 = [                       6300,]
    hexa_x_1 =  [                         19,]

    # Bottom sample bar L
    names_2   = ['Tcom16-minus42C-Si-repeat',]
    piezo_x_2 = [              -17000,]
    piezo_y_2 = [                7000,]          
    piezo_z_2 = [               -1700,]
    hexa_x_2 =  [                 -12,]
    

    names   = names_1   + names_2
    piezo_x = piezo_x_1 + piezo_x_2
    piezo_y = piezo_y_1 + piezo_y_2
    piezo_z = piezo_z_1 + piezo_z_2
    hexa_x  = hexa_x_1  + hexa_x_2

    names = [ '20240618-2000nm-L-' + n for n in names]
    """
    """
        # Top sample bar M
    names_1   = ['Tcom15-minus9C-b1131-85C', 'Tcom15-minus9C-b1101-160C', 'Tcom15-minus9C-b1111-40C',        'Tcom15-minus9C-Si', 'Tcom14-27C-b1100-160C', 'Tcom14-27C-b1130-85C',        'Tcom14-27C-Si', 'Tcom14-27C-b1110-40C', 'Tcom14-27C-b976-40C', 'Tcom14-27C-b1093-110C', 'Tcom14-27C-b1123-60C', 'Tcom14-27C-b1137-RT', 'minus9C-180nm-B308-110C',] 
    piezo_x_1 = [                    -53000,                      -42000,                     -31000,                     -20000,                   -8000,                   3000,                  14000,                  26000,                 39000,                   50000,                  38000,                 49000,                     54000,]
    piezo_y_1 = [                     -1500,                       -1500,                      -1500,                      -1500,                   -1500,                  -1500,                  -1500,                  -1500,                 -1500,                   -1500,                  -1500,                 -1500,                     -1500,]          
    piezo_z_1 = [                      6300,                        6300,                       6300,                       6300,                    6300,                   6300,                   6300,                   6300,                  6300,                    6300,                   6300,                  6300,                      6300,]
    hexa_x_1 =  [                       -12,                         -12,                        -12,                        -12,                     -12,                    -12,                    -12,                    -12,                   -12,                     -12,                     10,                    10,                        16,]

    # Bottom sample bar M
    names_2   = ['Tcom16-minus42C-b1132-85C', 'Tcom16-minus42C-b1095-110C', 'Tcom16-minus42C-b1102-160C', 'Tcom16-minus42C-b978-40C', 'Tcom16-minus42C-b1112-40C', 'Tcom16-minus42C-b1139-RT', 'Tcom16-minus42C-Si', 'Tcom16-minus42C-b1125-60C', 'Tcom15-minus9C-b1094-110C', 'Tcom15-minus9C-b977-40C', 'Tcom15-minus9C-b1138-RT', 'Tcom15-minus9C-b1124-60C',]
    piezo_x_2 = [                     -50000,                       -38000,                       -27000,                     -15000,                       -3000,                       9000,                20000,                       31000,                       42000,                     31000,                     42000,                      53000,]
    piezo_y_2 = [                       7000,                         7000,                         7000,                       7000,                        7000,                       7000,                 7000,                        7000,                        7000,                      7000,                      7000,                       7000,]          
    piezo_z_2 = [                      -1700,                        -1700,                        -1700,                      -1700,                       -1700,                      -1700,                -1700,                       -1700,                       -1700,                     -1700,                     -1700,                      -1700,]
    hexa_x_2 =  [                        -12,                          -12,                          -12,                        -12,                         -12,                        -12,                  -12,                         -12,                         -12,                        10,                        10,                         10,]
    

    names   = names_1   + names_2
    piezo_x = piezo_x_1 + piezo_x_2
    piezo_y = piezo_y_1 + piezo_y_2
    piezo_z = piezo_z_1 + piezo_z_2
    hexa_x  = hexa_x_1  + hexa_x_2

    names = [ '20240619-180nm-M-' + n for n in names]
    """
    """
        # Top sample bar M
    names_1   = [] 
    piezo_x_1 = []
    piezo_y_1 = []          
    piezo_z_1 = []
    hexa_x_1 =  []

    # Bottom sample bar M
    names_2   = ['Tcom16-minus42C-Si-repeat-again',]
    piezo_x_2 = [                      19000,]
    piezo_y_2 = [                       7000,]          
    piezo_z_2 = [                      -1700,]
    hexa_x_2 =  [                        -12,]
    

    names   = names_1   + names_2
    piezo_x = piezo_x_1 + piezo_x_2
    piezo_y = piezo_y_1 + piezo_y_2
    piezo_z = piezo_z_1 + piezo_z_2
    hexa_x  = hexa_x_1  + hexa_x_2

    names = [ '20240619-180nm-M-' + n for n in names]
    """ 
    """ 
        # Top sample bar N
    names_1   = [ 'Tcom15-minus9C-b833-85C',  'Tcom15-minus9C-b929-160C',  'Tcom15-minus9C-b980-40C', 'Tcom15-minus9C-B299-110C',  'Tcom14-27C-b928-160C',  'Tcom14-27C-b832-85C', 'Tcom14-27C-B298-110C',  'Tcom14-27C-b979-40C','Tcom14-27C-b1113-40C',  'Tcom14-27C-b880-110C', 'Tcom14-27C-b1024-60C', 'Tcom14-27C-b1140-RT', 'minus9C-180nm-Si-20240606',] 
    piezo_x_1 = [                    -54000,                      -42000,                     -30000,                     -17000,                   -5000,                   6000,                  18000,                  30000,                 42000,                   52000,                  41000,                 52000,                       55000,]
    piezo_y_1 = [                     -1500,                       -1500,                      -1500,                      -1500,                   -1500,                  -1500,                  -1500,                  -1500,                 -1500,                   -1500,                  -1500,                 -1500,                       -1500,]          
    piezo_z_1 = [                      6300,                        6300,                       6300,                       6300,                    6300,                   6300,                   6300,                   6300,                  6300,                    6300,                   6300,                  6300,                        6300,]
    hexa_x_1 =  [                       -12,                         -12,                        -12,                        -12,                     -12,                    -12,                    -12,                    -12,                   -12,                     -12,                     10,                    10,                          17,]

    # Bottom sample bar N
    names_2   = [ 'Tcom16-minus42C-b834-85C',  'Tcom16-minus42C-b882-110C',  'Tcom16-minus42C-b930-160C','Tcom16-minus42C-b1115-40C',  'Tcom16-minus42C-b981-40C', 'Tcom16-minus42C-b1142-RT', 'Tcom16-minus42C-B300-110C', 'Tcom16-minus42C-b1026-60C',  'Tcom15-minus9C-b881-110C','Tcom15-minus9C-b1114-40C', 'Tcom15-minus9C-b1141-RT', 'Tcom15-minus9C-b1025-60C',]
    piezo_x_2 = [                     -50000,                       -39000,                       -29000,                     -17000,                       -6000,                       9000,                       20000,                       33000,                       43000,                     33000,                     45000,                      56000,]
    piezo_y_2 = [                       7000,                         7000,                         7000,                       7000,                        7000,                       7000,                        7000,                        7000,                        7000,                      7000,                      7000,                       7000,]          
    piezo_z_2 = [                      -1700,                        -1700,                        -1700,                      -1700,                       -1700,                      -1700,                       -1700,                       -1700,                       -1700,                     -1700,                     -1700,                      -1700,]
    hexa_x_2 =  [                        -12,                          -12,                          -12,                        -12,                         -12,                        -12,                         -12,                         -12,                         -12,                        10,                        10,                         10,]
    

    names   = names_1   + names_2
    piezo_x = piezo_x_1 + piezo_x_2
    piezo_y = piezo_y_1 + piezo_y_2
    piezo_z = piezo_z_1 + piezo_z_2
    hexa_x  = hexa_x_1  + hexa_x_2

    names = [ '20240620-630nm-N-' + n for n in names]
    """ 
    """
# Top sample bar N
    names_1   = [] 
    piezo_x_1 = []
    piezo_y_1 = []          
    piezo_z_1 = []
    hexa_x_1 =  []

    # Bottom sample bar N
    names_2   = ['Tcom15-minus9C-b1025-60C-repeat-again',]
    piezo_x_2 = [55000,]
    piezo_y_2 = [7000,]          
    piezo_z_2 = [700,]
    hexa_x_2 =  [10,]
    

    names   = names_1   + names_2
    piezo_x = piezo_x_1 + piezo_x_2
    piezo_y = piezo_y_1 + piezo_y_2
    piezo_z = piezo_z_1 + piezo_z_2
    hexa_x  = hexa_x_1  + hexa_x_2

    names = [ '20240620-630nm-N-' + n for n in names]
    """
 
    # Top sample bar O
    names_1   = ['Tcom15-minus9C-b1134-85C', 'Tcom15-minus9C-b1104-160C', 'Tcom15-minus9C-b1127-60C', 'Tcom15-minus9C-B310-110C', 'Tcom14-27C-b1103-160C', 'Tcom14-27C-b1133-85C', 'Tcom14-27C-B309-110C', 'Tcom14-27C-b1126-60C','Tcom14-27C-b1027-60C', 'Tcom14-27C-b1096-110C', 'Tcom14-27C-b1116-40C', 'Tcom14-27C-b1143-RT', 'minus42C-180nm-Si-20240619',] 
    piezo_x_1 = [                    -54000,                      -43000,                     -32000,                     -21000,                  -10000,                   2000,                  13000,                  24000,                 35000,                   46000,                  36000,                 48000,                        52000,]
    piezo_y_1 = [                     -1500,                       -1500,                      -1500,                      -1500,                   -1500,                  -1500,                  -1500,                  -1500,                 -1500,                   -1500,                  -1500,                 -1500,                        -1500,]          
    piezo_z_1 = [                      6300,                        6300,                       6300,                       6300,                    6300,                   6300,                   6300,                   6300,                  6300,                    6300,                   6300,                  6300,                         6300,]
    hexa_x_1 =  [                       -12,                         -12,                        -12,                        -12,                     -12,                    -12,                    -12,                    -12,                   -12,                     -12,                     10,                    10,                           17,]

    # Bottom sample bar O
    names_2   = ['Tcom16-minus42C-b1135-85C', 'Tcom16-minus42C-b1098-110C', 'Tcom16-minus42C-b1105-160C','Tcom16-minus42C-b1029-60C', 'Tcom16-minus42C-b1128-60C', 'Tcom16-minus42C-b1145-RT', 'Tcom16-minus42C-B311-110C', 'Tcom16-minus42C-b1118-40C', 'Tcom15-minus9C-b1097-110C','Tcom15-minus9C-b1028-60C', 'Tcom15-minus9C-b1144-RT', 'Tcom15-minus9C-b1117-40C',]
    piezo_x_2 = [                     -50000,                       -38000,                       -26000,                     -15000,                       -4000,                       7000,                       18000,                       29000,                       41000,                     31000,                     45000,                      56000,]
    piezo_y_2 = [                       7000,                         7000,                         7000,                       7000,                        7000,                       7000,                        7000,                        7000,                        7000,                      7000,                      7000,                       7000,]          
    piezo_z_2 = [                        700,                          700,                          700,                        700,                         700,                        700,                         700,                         700,                         700,                       700,                       700,                        700,]
    hexa_x_2 =  [                        -12,                          -12,                          -12,                        -12,                         -12,                        -12,                         -12,                         -12,                         -12,                        10,                        10,                         10,]
    

    names   = names_1   + names_2
    piezo_x = piezo_x_1 + piezo_x_2
    piezo_y = piezo_y_1 + piezo_y_2
    piezo_z = piezo_z_1 + piezo_z_2
    hexa_x  = hexa_x_1  + hexa_x_2

    names = [ '20240620-245nm-O-' + n for n in names]
  

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

    waxs_arc = [ 0, 2, 7 ]# , 20, 22 ]  # degrees
    x_off = [0]
    incident_angles = [ 0.10, 0.25 ]
    user_name = 'PL'

    det_exposure_time(t, t)


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
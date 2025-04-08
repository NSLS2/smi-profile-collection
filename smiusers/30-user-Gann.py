def get_scan_md_tender():
    """
    Create a string with scan metadata
    """
    # Metadata
    e = energy.position.energy / 1000
    #temp = str(np.round(float(temp_degC), 1)).zfill(5)
    wa = waxs.arc.position + 0.001
    wa = str(np.round(float(wa), 1)).zfill(4)
    sdd = pil1m_pos.z.position / 1000

    md_fmt = ("_{energy}keV_wa{wa}_sdd{sdd}m")

    scan_md = md_fmt.format(
        energy = "%.5f" % e ,
        wa = wa,
        sdd = "%.1f" % sdd,
    )
    return scan_md

'''
def test_gi_tender(t=0.5):
    """
    Grazing incidence tender
    """

    proposal_id('2023_2', '000001_Gann', analysis=True)

def giwaxs_guillaume_2023_1(t=0.5):
    """
    GISAXS macro for 14 keV for Amalie sample
    """
    user_name = "GF"

    names = [ 'giwaxssa01','giwaxssa02','giwaxssa03','giwaxssa04','giwaxssa05']
    x_piezo = [      55000,       42000,       25000,        7000,      -10000]
    y_piezo = [       5000,        5000,        5000,        5000,        5000]
    z_piezo = [       7000,        7000,        7000,        7000,        7000]
    x_hexa =  [         10,          10,          10,          10,          10]


    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(z_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexa)})"

    waxs_angles = [0, 2, 20, 22]
    inc_angles = [0.15, 0.20, 0.3]

    for name, xs, zs, ys, xs_hexa in zip(names, x_piezo, z_piezo, y_piezo, x_hexa):
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)
        yield from bps.mv(piezo.th, -1)

        yield from alignement_gisaxs(angle=0.15)
        ai0 = piezo.th.position

        det_exposure_time(t, t)
        for wa in waxs_angles:
            yield from bps.mv(waxs, wa)

            dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]

            for i, ai in enumerate(inc_angles):
                yield from bps.mv(piezo.x, xs-500*i)
                yield from bps.mv(piezo.th, ai0 + ai)
                yield from bps.sleep(20)

                bpm = xbpm3.sumX.get()
                e = energy.energy.position / 1000
                sdd = pil1m_pos.z.position / 1000

                name_fmt = "{sample}_ai{ai}_{energy}eV_wa{wax}_sdd{sdd}m"
                sample_name = name_fmt.format(sample=name, ai="%.2f"%ai, energy="%.1f"%e, sdd="%.1f"%sdd, wax="%.1f"%wa)
                sample_id(user_name=user_name, sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)
                yield from bps.sleep(2)

            yield from bps.mv(piezo.th, ai0)

    piezo_z = [ 6600 for n in names ]

    energies = np.concatenate((np.arange(2445, 2470, 5),
                               np.arange(2470, 2480, 0.25),
                               np.arange(2480, 2490, 1),
                               np.arange(2490, 2501, 5),
                               ))

    incident_angles = [0.1, 0.2, 0.3, 0.4]
    waxs_arc = [0, 20, 40, 60]

    user_name = "EG"
    det_exposure_time(t, t)

    msg = "Wrong number of coordinates, check names, piezos, and hexas"
    assert len(piezo_x) == len(names), msg
    assert len(piezo_x) == len(piezo_y), msg
    assert len(piezo_y) == len(piezo_z), msg
    yield from bps.mv(waxs, waxs_arc[0])

    for name, x, y, z in zip(names, piezo_x, piezo_y, piezo_z):

        yield from bps.mv(piezo.x, x,
                          piezo.y, y,
                          piezo.z, z,)

        # Align the sample
        try:
            yield from alignement_gisaxs()
        except:
            yield from alignement_gisaxs(0.01)

        # Sample flat at ai0
        ai0 = piezo.th.position
        # construct the det list here
        # add run decorator and stage decorators here ()
        def inner():
            for wa in waxs_arc:
                yield from bps.mv(waxs, wa)
                dets = [pil900KW] if waxs.arc.position < 15 else [pil900KW, pil1M] # making one run this will not be possible
                # potentially we don't link those useless files
                # or make the detecor know when it's useless and produce none and have tiled assume nans
                # or have different trigger and reads e.g.(name="saxs") (different streams) for each detector
                yield from bps.declare_stream(...)
                for ai in incident_angles:

                    yield from bps.mv(piezo.th, ai0 + ai)
                    for e in energies:
                        
                        yield from bps.mv(energy, e)# ADD SETTLE TIME TO ENERGY?
                        yield from bps.sleep(2)

                        sample_name = f'{name}{get_scan_md_tender()}_ai{ai}'
                        sample_id(user_name=user_name, sample_name=sample_name)
                        print(f"\n\n\n\t=== Sample: {sample_name} ===")
                        yield from bp.count(dets) # potentially add all motors to  and motor indexes(soft signals to match up saxs and nosaxs streams) 
                        
                        def inner_copunt(...):
                        #Toms replacement for bp.count
                        yield from bps.checkpoint()
                        yield from bps.trigger(pil900KW, group='dets')
                        arc = yield from  bps.rd(waxs.arc)
                        if arc is not None and arc > 15:
                            yield from bps.trigger(pil1M, group='dets')
                        yield from bps.wait(group='dets')
                        yield from bps.create(name='SAXS')
                        yield from bps.read(...)
                        yield from bps.save()
                        if COND:
                            yield from bps.create(name='WAXS')

                            yield from bps.read(pil1M)
                            for m in motors:
                                yield from bps.read(m)
                            yield from bps.save()
                        # (do hinting to adjust what adds to the livetable etc)
                        # change count to trigger_and_read(), add around the outer for loop stage list of detector, run decorator 
                        # add all motors we care about in the dets scan_nd([dets])
                        # add signal for index position in scan -  motor positions
                        # to trigger once..
                    yield from bps.mv(energy, energies[int(len(energies) / 2)])
                    yield from bps.sleep(2)
                    yield from bps.mv(energy, energies[0])
                
                yield from bps.mv(piezo.th, ai0)
            waxs_arc = waxs_arc[::-1]
        yield from inner()
    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)
'''
'''
Sample    piezo_x: min     max    cen   piezo_y    piezo_z   th_0    stage_x
-----------------------------------------------------------------------
Fl screen       -51000                   6000
6.0             -46000  -38000 -42000    6646.7       800      2.920      o
5.0             -34000  -26000 -30000    6616.7       800      2.927      0
4.0             -22000  -16000 -19000    6628.1       800      2.930      0
0                -9000   -1000  -5000    6544.6       800      2.943      0
0                 3000   13000   8000    6574.1       800      2.930      0
3.0              18000   25000  21500    6571.1       800      2.930      0
2.5              29000   37000  33000    6536.7       800      2.452      0
2.25             42000   50000  45000    6554.9       800      2.939      0
Si               53000   57000  54000    6713.0       200      2.943      0

Si
----------
angle   roi_min_Y      attenuators
0           1253         att2_6, att2_5 
0.1         1247
0.2         1241
0.3         1236
0.4         1230
0.5         1225
0.75        1211         att2_6, att2_12
1           1197            
1.25                 att2_6
1.5         1167         att2_5, att2_12
1.75                
2           1139         att2_5
2.25                 att2_12
2.5         1112         att2_12
3           1082         att2_12
3.5         1053         att2_12
4           1026         att2_12

'''

def att6(angle):
    if angle < 1.3:
        return 1
    else:
        return 0
def att5(angle):
    if angle < 0.5:
        return 1
    elif angle < 1.3:
        return 0
    elif angle <2.2:
        return 1
    else:
        return 0
    
def att12(angle):
    if angle < 0.5:
        return 0
    elif angle < 0.9 :
        return 1
    elif angle < 1.3:
        return 0
    elif angle < 1.9:
        return 1
    elif angle < 2.2:
        return 0
    else:
        return 1


def roiy(angle):
    return int(1252.855 -1620.548*np.tan(np.deg2rad(angle)*2)) 

def goto_angle(angle,th0_si):
    yield from bps.mv(
        att2_6.open_cmd, att6(angle),
        att2_6.close_cmd, 1-att6(angle),
        att2_5.open_cmd, att5(angle),
        att2_5.close_cmd, 1-att5(angle),
        att2_12.open_cmd, att12(angle),
        att2_12.close_cmd, 1-att12(angle),
        pil900KW.roi4.min_xyz.min_y,roiy(angle),
        piezo.th,th0_si+angle
    )




def reflectivity_multisample():
    sample_names = ['IBMSi1',    'IBM6p0',  'IBM5p0',  'IBM4p0',  'IBM0p01',    'IBM0p02', 'IBM3p0',  'IBM2p5',     'IBM2p25', 'IBMSi2']
    x_piezos =     [55000,      -43000,    -31000,     -20000,     -6000,      -9000,      22000,      33000,      47000,     55000]
    y_piezos =     [6713.0,     6646.7,    6616.7,     6628.1,     6544.6,     6574.1,     6571.1,     6536.7,     6554.9,    6713.0]
    th0s     =     [2.943,      2.920,     2.927,      2.930,      2.943,      2.930,      2.930,      2.452 ,     2.939,     2.943]



    angles = np.linspace(0,4,800)
    
    attenuator6o = [att6(angle) for angle in angles]
    attenuator6c = [1-att6(angle)for angle in angles]
    attenuator5o = [att5(angle) for angle in angles]
    attenuator5c = [1-att5(angle) for angle in angles]
    attenuator12o = [att12(angle) for angle in angles]
    attenuator12c = [1-att12(angle) for angle in angles]

    roi_centers = [roiy(angle) for angle in angles]


    pil900KW.stats4.centroid.x.kind = 'hinted'
    pil900KW.stats4.centroid.y.kind = 'hinted'
    pil900KW.stats4.centroid_total.kind = 'hinted'
    pil900KW.stats4.total.kind = 'hinted'
    pil900KW.stats4.kind = 'hinted'
    
    for sample, xp, yp, th0 in zip(sample_names, x_piezos, y_piezos, th0s):
        angles0 = [th0 + angle for angle in angles]


        yield from bps.mv(  piezo.x, xp,
                            piezo.y, yp)
        sample_id(user_name="Eliot", sample_name=sample)

        yield from bp.list_scan([pil900KW,pil900KW.stats4.centroid_total,pil900KW.stats4.total],
                                piezo.th,angles0,
                                pil900KW.roi4.min_xyz.min_y,roi_centers,
                                att2_6,attenuator6o,
                                att2_5,attenuator5o,
                                att2_12,attenuator12o,
                                )





### In case useful ###

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

### In case useful ###
def reflectivity_multisample_segment():
    sample_names = ['IBMSi',    'IBM6p0',  'IBM5p0',  'IBM4p0',  'IBM0p01',    'IBM0p02', 'IBM3p0',  'IBM2p5',     'IBM2p25', 'IBMSi']
    x_piezos =     [55000,      -43000,    -31000,     -20000,     -6000,      -9000,      22000,      33000,      47000,     55000]
    y_piezos =     [6713.0,     6646.7,    6616.7,     6628.1,     6544.6,     6574.1,     6571.1,     6536.7,     6554.9,    6713.0]
    th0s     =     [2.943,      2.920,     2.927,      2.930,      2.943,      2.930,      2.930,      2.452 ,     2.939,     2.943]

    angles_1 = np.linspace(0.0,  0.7,  71)[:-1]
    angles_2 = np.linspace(0.7,  0.9,  21)[:-1]
    angles_3 = np.linspace(0.9,  1.3,  41)[:-1]
    angles_4 = np.linspace(1.3,  1.9,  61)[:-1]
    angles_5 = np.linspace(1.9,  2.2,  31)[:-1]
    angles_6 = np.linspace(2.2,  4.0,  181)[:-1]

    angles = np.linspace(0,4,20)
    
    attenuator6o = [att6(angle) for angle in angles]
    attenuator6c = [1-att6(angle)for angle in angles]
    attenuator5o = [att5(angle) for angle in angles]
    attenuator5c = [1-att5(angle) for angle in angles]
    attenuator12o = [att12(angle) for angle in angles]
    attenuator12c = [1-att12(angle) for angle in angles]

    roi_centers = [roiy(angle) for angle in angles]


    pil900KW.stats4.centroid.x.kind = 'hinted'
    pil900KW.stats4.centroid.y.kind = 'hinted'
    pil900KW.stats4.centroid_total.kind = 'hinted'
    pil900KW.stats4.total.kind = 'hinted'
    
    for sample, xp, yp, th0 in zip(sample_names, x_piezos, y_piezos, th0s):
        angles0 = [th0 + angle for angle in angles]


        yield from bps.mv(  piezo.x, xp,
                            piezo.y, yp)
        sample_id(user_name="Eliot", sample_name=sample)

        yield from bp.list_scan([pil900KW,pil900KW.stats4.centroid_total,pil900KW.stats4.total],
                                piezo.th,angles0,
                                pil900KW.roi4.min_xyz.min_y,roi_centers,
                                att2_6.open_cmd,attenuator6o,
                                att2_6.close_cmd,attenuator6c,
                                att2_5.open_cmd,attenuator5o,
                                att2_5.close_cmd,attenuator5c,
                                att2_12.open_cmd,attenuator12o,
                                att2_12.close_cmd,attenuator12c,
                                )


def giwaxs_eliot_2024_3(t=0.5):
    """
    GISAXS macro for 16 keV
    """
    user_name = "EG"

    names =   [ 'linear3',    'Linear2side1', 'Linear2side2',  'Linear1side1','Linear1side2',]
    x_piezo = [      -37650,       -10600,       -13000,        30300,          37300,]
    y_piezo = [       2000,        -800,         -800,          800,            800,]
    z_piezo = [       7600,        7600,         7600,          7600,           7600,]


    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(z_piezo)})"
    
    waxs_angles = [0, 20,]
    inc_angles = [0.05, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2, 0.25, 0.3]

    for name, xs, zs, ys in zip(names, x_piezo, z_piezo, y_piezo):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)
        yield from bps.mv(piezo.th, 0)

        yield from alignement_gisaxs(angle=0.15)
        ai0 = piezo.th.position

        det_exposure_time(t, t)
        for wa in waxs_angles:
            yield from bps.mv(waxs, wa)

            dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]

            for i, ai in enumerate(inc_angles):
                yield from bps.mv(piezo.th, ai0 + ai)

                bpm = xbpm3.sumX.get()
                e = energy.energy.position / 1000
                sdd = pil1m_pos.z.position / 1000

                name_fmt = "{sample}_ai{ai}_{energy}eV_wa{wax}_sdd{sdd}m"
                sample_name = name_fmt.format(sample=name, ai="%.2f"%ai, energy="%.1f"%e, sdd="%.1f"%sdd, wax="%.1f"%wa)
                sample_id(user_name=user_name, sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)
                yield from bps.sleep(2)

            yield from bps.mv(piezo.th, ai0)


def giwaxs_et_2024_3(ts=[0.5, 5, 15]):
    """
    GISAXS macro for 16 keV
    """
    user_name = "DG"

    names =   [ 'T1',    'U1', ]
    x_piezo = [      -5700,       5300,   ]
    y_piezo = [       3773,        3773,    ]
    z_piezo = [       7600,        7600,  ]


    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(z_piezo)})"
    
    waxs_angles = [20,]
    # inc_angles = [0.05, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2, 0.25, 0.3]
    # inc_angles = np.arange(0.05, 0.152, 0.002) #51
    inc_angles = np.arange(0.09, 0.106, 0.002) 

    for name, xs, zs, ys in zip(names, x_piezo, z_piezo, y_piezo):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)
        #yield from bps.mv(piezo.th, 0)

        yield from alignement_gisaxs(angle=0.15)
        ai0 = piezo.th.position

        for t in  ts:
            det_exposure_time(t, t)
            for wa in waxs_angles:
                yield from bps.mv(waxs, wa)

                #dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]
                dets = [pil1M]

                for i, ai in enumerate(inc_angles):
                    yield from bps.mv(piezo.th, ai0 + ai)

                    bpm = xbpm3.sumX.get()
                    e = energy.energy.position / 1000
                    sdd = pil1m_pos.z.position / 1000

                    name_fmt = "{sample}_ai{ai}_{t}s_{energy}eV_wa{wax}_sdd{sdd}m"
                    sample_name = name_fmt.format(sample=name, ai="%.3f"%ai, energy="%.1f"%e, sdd="%.1f"%sdd, t="%.1f"%t, wax="%.1f"%wa)
                    sample_id(user_name=user_name, sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)
                    yield from bps.sleep(2)

                yield from bps.mv(piezo.th, ai0)


def nikhil_S_edge_spectroscopy(t=1,ai=0.5):


    names = ["ZnS_pristinehr", "ZnS_annealedhr",
             "CdS_pristinehr", "CdS_annealedhr",
             "BiS_pristinehr", "BiS_annealedhr"]
    x = [-40000, -28000, -18000,  -4000,  12000,  25000]
    y = [  6700,   6700,   6700,   6700,   6700,   6700]

    
    yield from bps.mv(waxs, 52)
    dets = [pil1M, pil900KW]


    energies = (np.arange(2445, 2470, 5).tolist()+ np.arange(2470, 2480, 0.25).tolist()+ np.arange(2480, 2490, 1).tolist()
                + np.arange(2490, 2500, 5).tolist()+ np.arange(2500, 2560, 10).tolist())
    
    yield from bps.mv(energy,energies[0])

    det_exposure_time(t, t)
    name_fmt = "{sample}_{energy}eV_xbpm{xbpm}"

    for name, xs, ys in zip(names, x, y):
        yield from bps.mv(piezo.x, xs,
                          piezo.y, ys,
                          piezo.th,0)
        
        yield from alignement_gisaxs(0.5)

        yield from bps.mvr(piezo.th,ai)
        
        for e in energies:
            try:
                yield from bps.mv(energy, e)
            except:
                print("energy failed to move, sleep for 30 s")
                yield from bps.sleep(30)
                print("Slept for 30 s, try move energy again")
                yield from bps.mv(energy, e)
            yield from bps.sleep(1)
            yield from bps.mvr(piezo.x,20)
            sample_name = name_fmt.format(
                sample=name, energy="%6.2f" % e, xbpm="%3.1f" % xbpm3.sumY.get()
            )
            sample_id(user_name="NT", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)

        yield from bps.mv(energy, 2470)
        yield from bps.mv(energy, 2450)




def nikhil_Zn_edge_spectroscopy(t=1,ai=0.2):


    names = [
             "ZnS_pristinehr", "ZnS_annealedhr",
             #"CdS_pristinehr", "CdS_annealedhr",
             #"BiS_pristinehr", "BiS_annealedhr"
             ]
    x = [
         -38000, -25000,
         #-18000,  -4000,
         #12000,  25000
         ]
    y = [
          6900,   6900,
         # 6700,   6700,
         # 6700,   6700
          ]

    
    yield from bps.mv(waxs, 52)
    dets = [pil1M, pil900KW]


    #energies = (np.arange(2445, 2470, 5).tolist()+ np.arange(2470, 2480, 0.25).tolist()+ np.arange(2480, 2490, 1).tolist()
    #            + np.arange(2490, 2500, 5).tolist()+ np.arange(2500, 2560, 10).tolist())
    
    energies = (np.arange(9600, 9650, 5).tolist()+ 
                np.arange(9650, 9700, 1).tolist()+
                np.arange(9700, 2750, 5).tolist())

    yield from bps.mv(energy,energies[0])

    det_exposure_time(t, t)
    name_fmt = "{sample}_{energy}eV_xbpm{xbpm}"

    for name, xs, ys in zip(names, x, y):
        yield from bps.mv(piezo.x, xs,
                          piezo.y, ys,
                          piezo.th,0)
        
        yield from alignement_gisaxs(0.2)

        yield from bps.mvr(piezo.th,ai)
        
        for e in energies:
            try:
                yield from bps.mv(energy, e)
            except:
                print("energy failed to move, sleep for 30 s")
                yield from bps.sleep(30)
                print("Slept for 30 s, try move energy again")
                yield from bps.mv(energy, e)
            yield from bps.sleep(1)
            yield from bps.mvr(piezo.x,20)
            sample_name = name_fmt.format(
                sample=name, energy="%6.2f" % e, xbpm="%3.1f" % xbpm3.sumY.get()
            )
            sample_id(user_name="NT", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)



def nikhil_Bi_edge_spectroscopy(t=1,ai=0.2):


    names = [
             #"ZnS_pristinehr", "ZnS_annealedhr",
             #"CdS_pristinehr", "CdS_annealedhr",
             "BiS_pristinehr", "BiS_annealedhr"
             ]
    x = [
         #-40000, -28000,
         #-18000,  -4000,
         14000,  30000
         ]
    y = [
         # 6700,   6700,
         # 6700,   6700,
          6900,   6900
          ]

    
    yield from bps.mv(waxs, 52)
    dets = [pil1M, pil900KW]


    #energies = (np.arange(2445, 2470, 5).tolist()+ np.arange(2470, 2480, 0.25).tolist()+ np.arange(2480, 2490, 1).tolist()
    #            + np.arange(2490, 2500, 5).tolist()+ np.arange(2500, 2560, 10).tolist())
    
    energies = (np.arange(13300, 9650, 10).tolist()+ 
                np.arange(13400, 13500, 2).tolist()+
                np.arange(13500, 13600, 10).tolist())

    det_exposure_time(t, t)
    name_fmt = "{sample}_{energy.name}eV_xbpm{xbpm}"

    for name, xs, ys in zip(names, x, y):
        yield from bps.mv(piezo.x, xs,
                          piezo.y, ys,
                          piezo.th,0)
        
        yield from alignement_gisaxs(0.2)

        yield from bps.mvr(piezo.th,ai)
        
        for e in energies:
            try:
                yield from bps.mv(energy, e)
            except:
                print("energy failed to move, sleep for 30 s")
                yield from bps.sleep(30)
                print("Slept for 30 s, try move energy again")
                yield from bps.mv(energy, e)
            yield from bps.sleep(1)
            yield from bps.mvr(piezo.x,20)
            sample_name = name_fmt.format(
                sample=name, energy="%6.2f" % e, xbpm="%3.1f" % xbpm3.sumY.get()
            )
            sample_id(user_name="NT", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)


def Nikhil_hard_NEXAFS():
    yield from nikhil_Zn_edge_spectroscopy()
    yield from nikhil_Bi_edge_spectroscopy()



def nikhil_S_edge_spectroscopy_2(t=1,ai=0.5):


    names = ["BiS_exphr"]
    x = [-10000]
    y = [  6700]

    
    yield from bps.mv(waxs, 52)
    dets = [pil1M, pil900KW]


    energies = (np.arange(2445, 2470, 5).tolist()+ np.arange(2470, 2480, 0.25).tolist()+ np.arange(2480, 2490, 1).tolist()
                + np.arange(2490, 2500, 5).tolist()+ np.arange(2500, 2560, 10).tolist())
    
    yield from bps.mv(energy,energies[0])

    det_exposure_time(t, t)
    name_fmt = "{sample}_{energy}eV_xbpm{xbpm}"

    for name, xs, ys in zip(names, x, y):
        yield from bps.mv(piezo.x, xs,
                          piezo.y, ys,
                          piezo.th,0)
        
        yield from alignement_gisaxs(ai)

        yield from bps.mvr(piezo.th,ai)
        
        for e in energies:
            try:
                yield from bps.mv(energy, e)
            except:
                print("energy failed to move, sleep for 30 s")
                yield from bps.sleep(30)
                print("Slept for 30 s, try move energy again")
                yield from bps.mv(energy, e)
            yield from bps.sleep(1)
            yield from bps.mvr(piezo.x,20)
            sample_name = name_fmt.format(
                sample=name, energy="%6.2f" % e, xbpm="%3.1f" % xbpm3.sumY.get()
            )
            sample_id(user_name="NT", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)

        yield from bps.mv(energy, 2470)
        yield from bps.mv(energy, 2450)


def nikhil_Zn_edge_spectroscopy2(t=1,ai=0.2):


    names = [   "ZnO_pristinehr",   "ZnO_annealedhr",   ]
    x =     [   21000,             3000,             ]
    y =     [   6900,               6900,               ]

    
    yield from bps.mv(waxs, 52)
    dets = [pil1M, pil900KW]


    #energies = (np.arange(2445, 2470, 5).tolist()+ np.arange(2470, 2480, 0.25).tolist()+ np.arange(2480, 2490, 1).tolist()
    #            + np.arange(2490, 2500, 5).tolist()+ np.arange(2500, 2560, 10).tolist())
    
    energies = (np.arange(9600, 9650, 5).tolist()+ 
                np.arange(9650, 9700, 1).tolist()+
                np.arange(9700, 2750, 5).tolist())

    yield from bps.mv(energy,energies[0])

    det_exposure_time(t, t)
    name_fmt = "{sample}_{energy}eV_xbpm{xbpm}"

    for name, xs, ys in zip(names, x, y):
        yield from bps.mv(piezo.x, xs,
                          piezo.y, ys,
                          piezo.th,0)
        
        yield from alignement_gisaxs(ai)

        yield from bps.mvr(piezo.th,ai)
        
        for e in energies:
            try:
                yield from bps.mv(energy, e)
            except:
                print("energy failed to move, sleep for 30 s")
                yield from bps.sleep(30)
                print("Slept for 30 s, try move energy again")
                yield from bps.mv(energy, e)
            yield from bps.sleep(1)
            yield from bps.mvr(piezo.x,20)
            sample_name = name_fmt.format(
                sample=name, energy="%6.2f" % e, xbpm="%3.1f" % xbpm3.sumY.get()
            )
            sample_id(user_name="NT", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)






# IBM reflectivity Oct 27 2024
def reflectivity_multisample_2024():
    sample_names = ['IBMSi1',    'IBM6p0',  'IBM5p0',  'IBM4p0',  'IBM0p01',    'IBM0p02', 'IBM3p0',  'IBM2p5',     'IBM2p25', 'IBMSi2']
    x_piezos =     [55000,      -43000,    -31000,     -20000,     -6000,      7000,      22000,      33000,      47000,     55000]
    y_piezos =     [4500,     4500.7,    4500.7,     4500.1,     4500.6,     4500.1,     4500.1,     4500.7,     4500.9,    4500.0]
    th0s     =     [-1,      -1,     0,      -1,      -1,      -1,      -1,      -1 ,     -1,     -1]



    angles = np.linspace(0,6,600)
    energies = [2450,2470,2475,2480]

    attenuator9o = [att9(angle) for angle in angles]
    attenuator10o = [att10(angle) for angle in angles]
    attenuator11o = [att11(angle) for angle in angles]

    #roi_centers = [roiy(angle) for angle in angles]


    pil900KW.stats4.centroid.x.kind = 'hinted'
    pil900KW.stats4.centroid.y.kind = 'hinted'
    pil900KW.stats4.centroid_total.kind = 'hinted'
    pil900KW.stats4.total.kind = 'hinted'
    pil900KW.stats4.kind = 'hinted'
    
    for sample, xp, yp, thp in zip(sample_names, x_piezos, y_piezos, th0s):
       


        yield from bps.mv(  piezo.x, xp,
                            piezo.y, yp,
                            piezo.th, thp)
        
        yield from alignement_gisaxs(.2)
        yield from bps.mv(waxs,6)
        th0 = piezo.th.user_readback.get()

        angles0 = [th0 + angle for angle in angles]
        for en in energies:
            sample_id(user_name="EG", sample_name=f'{sample}_{en}eV')


            yield from bp.list_scan([pil900KW,pil900KW.stats4.centroid_total,pil900KW.stats4.total],
                                    piezo.th,angles0,
                                    att2_11,attenuator11o,
                                    att2_10,attenuator10o,
                                    att2_9,attenuator9o,
                                    )


# attenuators for Oct27 2024


# def att11(angle):
#     if angle < 0.6:
#         return 1
#     else:
#         return 0
# def att10(angle):
#     if angle < 0.6:
#         return 0
#     elif angle < 2:
#         return 1 
#     else:
#         return 0
    
# def att9(angle):
#     if angle < 0.6:
#         return 0
#     elif angle < 1.2 :
#         return 1
#     elif angle < 2:
#         return 0
#     elif angle < 4:
#         return 1
#     else:
#         return 0
    

# def att11(angle):
#     if angle < 0.5:
#         return 1
#     else:
#         return 0
# def att10(angle):
#     if angle < 0.5:
#         return 0
#     elif angle < 1.5:
#         return 1 
#     else:
#         return 0
    
# def att9(angle):
#     if angle < 0.5:
#         return 0
#     elif angle < 1 :
#         return 1
#     elif angle < 1.5:
#         return 0
#     elif angle < 4:
#         return 1
#     else:
#         return 0
def att11(angle):
    if angle < 0.5:

        return 1
    else:
        return 0
def att10(angle):

    if angle < 0.5:
        return 0
    elif angle < 1.5:

        return 1 
    else:
        return 0
    
def att9(angle):

    if angle < 0.5:
        return 0
    elif angle < 1 :
        return 1
    elif angle < 1.5:

        return 0
    elif angle < 4:
        return 1
    else:
        return 0


def xrr_sedge_2025_1():
    #List of incident angles clustured in subsection for attenuators
    # sample_names = ['IBM2p25_2', 'IBM2p5', 'IBM3p0', 'IBM4p0', 'IBM5p0', 'IBM6p0', ]
    # x_piezos =     [      30000,     17000,    1000,    -15000,    -32000,    -50000,    ]
    # y_piezos =     [       -200,      0,        0,       232,       432,       452,     ]
    # th0s     =     [         -2,        -2,        -2,        -2,        -2,        -2,    ]


    # sample_names = [ 'IBM0p0_2', 'IBM2p25_2', 'IBM2p5', 'IBM3p0', 'IBM4p0', 'IBM5p0', 'IBM6p0', ]
    # x_piezos =     [      43000,       29000,    16000,     1000,    -15000,    -33000,    -50000,    ]
    # y_piezos =     [       -400,        -200,     -200,        0,       232,       432,       452,     ]
    # th0s     =     [         -2,          -2,       -2,       -2,        -2,        -2,    -2]

    sample_names = [ 'IBM0p0_0_1', 'IBM0p0_0_2',]
    x_piezos =     [      23000,      -30000,   ]
    y_piezos =     [      -1000,        -1000,  ]
    th0s     =     [         -2,          -2,   ]


    
    angles = np.linspace(0.03, 1.03, 76).tolist()
    angles +=            np.linspace(1.05,  2.01, 41).tolist()
    angles +=            np.linspace(2.01,  2.51, 35).tolist()
    angles +=            np.linspace(2.55, 4, 50).tolist()
    angles +=            np.linspace(4, 6, 41).tolist()
    angles +=            np.linspace(6, 8, 41).tolist()
    
    # energies = [2450,2460,2500,2475,2477,2478,2479,2480,2481,2482,2483,2485,2487,2520]

    energies = [2450,2477,2480,2482,2520]

    attenuator9o = [att9(angle) for angle in angles]
    attenuator10o = [att10(angle) for angle in angles]
    attenuator11o = [att11(angle) for angle in angles]

    #roi_centers = [roiy(angle) for angle in angles]


    pil900KW.stats1.centroid.x.kind = 'hinted'
    pil900KW.stats1.centroid.y.kind = 'hinted'
    pil900KW.stats1.centroid_total.kind = 'hinted'
    pil900KW.stats1.total.kind = 'hinted'
    pil900KW.stats1.kind = 'hinted'

    set_energy_cam(pil900KW.cam,energies[0])
    set_energy_cam(pil1M.cam,energies[0])
    # yield from bps.mv(energy,energies[0])
    yield from bps.sleep(5)

    
    for sample, xp, yp, thp in zip(sample_names, x_piezos, y_piezos, th0s):
        # if sample == 'IBM6p0':
        #     energies = [2481,2483,2487,2520]
        # else:
        #     energies = [2450,2475,2477.5,2481,2483,2487,2520]


        yield from bps.mv(  piezo.x, xp,
                            piezo.y, yp,
                            piezo.th, thp)
        

        yield from bps.mv(energy,energies[0])
        yield from bps.sleep(5)

        yield from alignement_gisaxs(.5)
        
        yield from bps.mv(waxs.arc,7)
        th0 = piezo.th.user_readback.get()

        angles0 = [th0 + angle for angle in angles]
        for en in energies:
            print('The sample measured is ', sample)
            print('The energy is ', en)


            yield from bps.mv(energy,en)
            yield from bps.mvr(piezo.x, 500)
            yield from bps.sleep(5)
            sample_id(user_name="EG", sample_name=f'{sample}_{en}eV')

            yield from bp.list_scan([pil900KW,pil900KW.stats1.centroid_total,pil900KW.stats1.total],
                                    piezo.th,angles0,
                                    att2_11,attenuator11o,
                                    att2_10,attenuator10o,
                                    att2_9,attenuator9o,
                                    )
        yield from bps.mv(energy,2475)
        yield from bps.sleep(5)

    

    
def att11(angle):
    if angle < 0.5:
        return 1
    else:
        return 0
def att10(angle):
    if angle < 0.5:
        return 0
    elif angle < 1.5:
        return 1 
    else:
        return 0
    
def att9(angle):
    if angle < 0.5:
        return 0
    elif angle < 1 :
        return 1
    elif angle < 1.5:
        return 0
    elif angle < 4:
        return 1
    else:
        return 0



def nexafs_sedge_2025_1():
    dets = [pil900KW]
    # energies1 =   np.asarray([2810.0, 2820.0, 2830.0, 2832.0, 2834.0, 2834.5, 2835.0, 2835.5, 2836.0, 2836.5, 2837.0, 2837.5, 2838.0, 2838.5, 2839.0,
    # 2839.5, 2840.0, 2840.5, 2841.0, 2841.5, 2845.0, 2850.0, 2855.0, 2860.0, 2865.0, 2870.0, 2875.0, 2880.0, 2890.0])
    name='IBM6p0NEXAFS'
    energies = np.asarray(np.arange(2445, 2475, 5).tolist() + np.arange(2475, 2490, 0.25).tolist()
                            + np.arange(2490, 2500, 5).tolist()+ np.arange(2500, 2521, 10).tolist())
    for i, e in enumerate(energies):
        yield from bps.mv(energy, e)
        yield from bps.sleep(2)

        if xbpm2.sumX.get() < 120:
            yield from bps.sleep(5)
            yield from bps.mv(energy, e)
            yield from bps.sleep(2)

        bpm = xbpm3.sumX.value
        
        name_fmt = "{sample}_{energy}eV_wa{wax}_bpm{xbpm}"

        sample_name = name_fmt.format(sample=name, energy="%6.2f" % e, wax=20, xbpm="%4.3f" % bpm)
        sample_id(user_name="JJS", sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")

        yield from bp.count(dets, num=1)

    yield from bps.mv(energy, 2475)
    yield from bps.sleep(3)
    yield from bps.mv(energy, 2450)
    yield from bps.sleep(3)

import bluesky.preprocessors as bpp
import bluesky.plans as bp
import bluesky.plan_stubs as bps
from ophyd import Signal

def single_scan(t=1, name="Test", ai_list: list[int]|None = None, xstep=10, waxs_arc = (0, 20)):
    '''
    Study the beam damage on 1 film to define the opti;am experimental conitions.

    '''
    # dets = [pil900KW]
    if ai_list is None:
        ai_list = []

    # bottom left first
    # name = 'A1_01_test'    

    # 63 energies
    energies = (np.arange(2445, 2470, 5).tolist()+ np.arange(2470, 2480, 0.25).tolist()+ np.arange(2480, 2490, 1).tolist()
                + np.arange(2490, 2500, 5).tolist()+ np.arange(2500, 2560, 10).tolist())
    
    # ai_list = [0.2, 0.4, 0.6, 0.8, 4, 8]

    ai0 = piezo.th.position
    xs = piezo.x.position
    dets = [pil900KW, pil1M]

    s = Signal(name='target_file_name', value='')

    @bpp.stage_decorator(dets)
    @bpp.run_decorator(md={})
    def inner():
        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)

            counter = 0
            for k, ais in enumerate(ai_list):
                if ais==0.6:
                    det_exposure_time(0.5, 0.5)
                else:
                    det_exposure_time(1, 1)

                yield from bps.mv(piezo.th, ai0 + ais)

                name_fmt = "{sample}_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                
                for e in energies:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    
                    yield from bps.mv(piezo.x, xs + counter * xstep)
                    counter += 1
                    bpm = yield from bps.rd(xbpm2.sumX)
                    sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    # sample_id(user_name="CM", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    s.put(sample_name)
                    yield from bps.trigger_and_read(dets + [energy, waxs, xbpm2, piezo.th, piezo.x] + [s])
                
                yield from bps.mv(energy, 2500)
                yield from bps.sleep(2)
                yield from bps.mv(energy, 2480)
                yield from bps.sleep(2)
                yield from bps.mv(energy, 2445)

            yield from bps.mv(piezo.th, ai0)
    return (yield from inner())



# multirun code prototype from Tom

import numpy as np

from bluesky import RunEngine

import bluesky.plan_stubs as bps
import bluesky.preprocessors as bpp

from bluesky.callbacks.best_effort import BestEffortCallback

from ophyd.sim import motor1, motor2, det1

from event_model import RunRouter

def multi_scan(start, stop, steps, mds):
    n = len(mds)
    for j, md in enumerate(mds):
        # open each run
        yield from bpp.set_run_key_wrapper(
            bps.open_run({"run_num": j, "total": n, **md}), f"run {j}"
        )
        # declare we will have a primary stream
        yield from bpp.set_run_key_wrapper(
            bps.declare_stream(motor1, motor2, det1, name="primary"), f"run {j}"
        )

    for k in np.linspace(start, stop, steps):
        # do the outer "slow" motor
        yield from bps.mv(motor1, k)
        for j in range(n):
            # do the inner "fast" motor
            yield from bps.mv(motor2, j)
            yield from bpp.set_run_key_wrapper(
                bps.trigger_and_read([motor1, motor2, det1]), f"run {j}"
            )
            
    # TODO wrap this up with finalize_wrapper
    for j in range(n):
        # close each of the runs
        yield from bpp.set_run_key_wrapper(bps.close_run(), f"run {j}")

def factory(name, doc):
    # BestEffortCallback assumes only one run open at a time so make a a new
    # one for each run
    bec = BestEffortCallback()
    # turn off tables as interleaved tables are useless!
    bec.disable_table()
    return [bec], []

rr = RunRouter([factory])

RE = RunEngine()
RE.subscribe(rr)







# multirun code prototype from Tom

import numpy as np

from bluesky import RunEngine

import bluesky.plan_stubs as bps
import bluesky.preprocessors as bpp

from bluesky.callbacks.best_effort import BestEffortCallback

from ophyd.sim import motor1, motor2, det1

from event_model import RunRouter

def multi_scan_2025_1_su(start, stop, steps, mds):
    n = len(mds)
    for j, md in enumerate(mds):
        # open each run
        yield from bpp.set_run_key_wrapper(
            bps.open_run({"run_num": j, "total": n, **md}), f"run {j}"
        )
        # declare we will have a primary stream
        yield from bpp.set_run_key_wrapper(
            bps.declare_stream(motor1, motor2, det1, name="primary"), f"run {j}"
        )

    for i, wa in enumerate(waxs_arc):
        yield from bps.mv(waxs, wa)
        # do the outer "slow" motor
        for j in range(n):
            # do the inner "fast" motor
            yield from bps.mv(motor2, j)
            yield from bpp.set_run_key_wrapper(
                bps.trigger_and_read([motor1, motor2, det1]), f"run {j}"
            )
            
    # TODO wrap this up with finalize_wrapper
    for j in range(n):
        # close each of the runs
        yield from bpp.set_run_key_wrapper(bps.close_run(), f"run {j}")



def giwaxs_hardxray_Kelvin_2024_3(t=1):

    # In Freychet_11
    # names = [  'GI_P25_4', 'GI_P25_2', 'GI_P25_1', 'GI_P25_0p5', 'GI_P25_0p25', 'GI_AHPP25_4', 'GI_AHPP25_2', 'GI_AHPP25_1', 'GI_AHPP25_0p5', 'GI_AHPP25_0p25',
    #            'GI_P5A_4', 'GI_P5A_2', 'GI_P5A_1', 'GI_P5A_0p5', 'GI_P5A_0p25', 'GI_AHPP5A_4', 'GI_AHPP5A_2', 'GI_AHPP5A_1', 'GI_AHPP5A_0p5', 'GI_AHPP5A_0p25']             
    # x_piezo = [     54000,      54000,      40000,        25000,         15000,         -2000,        -15000,        -29000,          -42000,           -48000, 
    #                 55000,      52000,      40000,        25000,         15000,          4000,         -8000,        -24000,          -37000,           -48000]  
    # x_hexa = [         15,          0,          0,            0,             0,             0,             0,             0,               0,               -8, 
    #                    15,          0,          0,            0,             0,             0,             0,             0,               0,               -8] 
    # y_piezo = [      6800,       6800,       6800,         6800,          6800,          6800,          6800,          6800,            6800,             6800,
    #                 -1500,      -1500,      -1500,        -1500,         -1500,         -1500,         -1500,         -1500,           -1500,            -1500] 
    
    names = ['sj-ppionzrox-m-post', 'sj-ppionzrox-m-ox', 'sj-ppionzrox-m-pre', 'sj-ppion-m-ox', 
                 'sj-bkg-m-coated',     'sj-bkg-m-bare']
    x_piezo = [              53800,               53900,                48700,           37900,
                             26900,               16400]
    x_hexa = [                  14,                 4.3,                    0,               0,
                                0,                    0]
    y_piezo = [               7300,                7300,                 7300,            7300,
                              7300,                7200]

    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexa)})"

    waxs_arc = [7, 20]
    ai0_all = -1
    ai_list = [0.10, 0.12, 0.15, 0.20]
    xstep = 0


    for name, xs, ys, xs_hexa in zip(names, x_piezo, y_piezo, x_hexa):
        yield from bps.mv(stage.x, xs_hexa,
                          piezo.x, xs,
                          piezo.y, ys)

        yield from bps.mv(piezo.th, ai0_all)
        yield from alignement_gisaxs_doblestack(0.15)

        ai0 = piezo.th.position
        det_exposure_time(t, t)
        
        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)

            if wa ==0:
                dets = [pil900KW]
            else:
                dets = [pil900KW, pil1M]

            # Do not take SAXS when WAXS detector in the way

            counter = 0
            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                name_fmt = "{sample}_{energy}eV_ai{ai}_wa{wax}"
                
                yield from bps.mv(piezo.x, xs - counter * xstep)
                counter += 1
                e=energy.energy.position
                sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa)
                sample_id(user_name="GS", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

            yield from bps.mv(piezo.th, ai0)




import bluesky.preprocessors as bpp
import bluesky.plans as bp
import bluesky.plan_stubs as bps
from ophyd import Signal

def single_scan_giwaxs(t=1, name="Test", ai_list: list[int]|None = None, xstep=10, waxs_arc = (0, 20)):
    '''
    Study the beam damage on 1 film to define the opti;am experimental conitions.

    '''
    names = ['sj-ppionzrox-m-post', 'sj-ppionzrox-m-ox', 'sj-ppionzrox-m-pre', 'sj-ppion-m-ox', 
                 'sj-bkg-m-coated',     'sj-bkg-m-bare']
    x_piezo = [              53800,               53900,                48700,           37900,
                             26900,               16400]
    x_hexa = [                  14,                 4.3,                    0,               0,
                                0,                    0]
    y_piezo = [               7300,                7300,                 7300,            7300,
                              7300,                7200]

    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexa)})"

    waxs_arc = [7, 20]
    ai0_all = -1
    ai_list = [0.10, 0.12, 0.15, 0.20]
    xstep = 0


    for name, xs, ys, xs_hexa in zip(names, x_piezo, y_piezo, x_hexa):
        yield from bps.mv(stage.x, xs_hexa,
                          piezo.x, xs,
                          piezo.y, ys)

        yield from bps.mv(piezo.th, ai0_all)
        yield from alignement_gisaxs_doblestack(0.15)

        ai0 = piezo.th.position
        det_exposure_time(t, t)

        s = Signal(name='target_file_name', value='')

        @bpp.stage_decorator(dets)
        @bpp.run_decorator(md={})
        def inner():
            for i, wa in enumerate(waxs_arc):
                yield from bps.mv(waxs, wa)

                counter = 0
                for k, ais in enumerate(ai_list):
                    yield from bps.mv(piezo.th, ai0 + ais)

                    name_fmt = "{sample}_{energy}eV_ai{ai}_wa{wax}"
                    
                    yield from bps.mv(piezo.x, xs - counter * xstep)
                    counter += 1
                    e=energy.energy.position
                    sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    s.put(sample_name)
                    yield from bps.trigger_and_read(dets + [energy, waxs, xbpm2, xbpm3, piezo.th, piezo.x] + [s])
            yield from bps.mv(piezo.th, ai0)

        return (yield from inner())
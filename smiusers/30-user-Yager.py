def measure(det=[pil1M], sample='test',  t=1):
    det_exposure_time(t, t)
    sample_name = "{sample}".format(sample=sample)
    sample_id(user_name="JK", sample_name=sample_name)
    print(f"\n\t=== Sample: {sample_name} ===\n")
    yield from bp.count(det, num=1)


def cd_saxs(th_ini, th_fin, th_st, exp_t=1, sample='test', nume=1, det=[pil1M]):
    det_exposure_time(exp_t, exp_t*nume)

    for num, theta in enumerate(np.linspace(th_ini, th_fin, th_st)):
        yield from bps.mv(prs, theta)
        name_fmt = "{sample}_5.2m_16.1keV_num{num}_{th}deg_bpm{bpm}"
        sample_name = name_fmt.format(sample=sample, num="%2.2d"%num, th="%2.2d"%theta, bpm="%1.3f"%xbpm3.sumX.get())
        # sample_id(user_name="JK", sample_name=sample_name)
        sample_id(sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")
        yield from bp.count(det, num=1)





def cdsaxs_2024_1(t=1):
    det = [pil1M]
    det_exposure_time(t, t)

    phi_offest = -2

    # names = [ 'C5b-L60p120']
    # x =     [   20800]
    # x_hexa =[     0.3]
    # y=      [    -3400]
    # z=      [    -1200]
    # chi=    [    0.6]
    # th =    [  5.75]

    # names = [ 'H5b-L52p104', 'E4b-L52p104', 'C5-L50p100', 'C5-L52p104', 'C5-L55p110', 'C5-L60p120']
    # x =     [   8550, -24350,       24400, 23500, 22600, 21700]
    # x_hexa =[     0.3, 0.3,         0.3, 0.3, 0.3, 0.3]
    # y=      [    -3250, -4100,      -3400, -3400, -3400, -3400]
    # z=      [    -550, 550,         -1200, -1200, -1200, -1200]
    # chi=    [    -0.5, 0.1,         0.6, 0.6, 0.6, 0.6]
    # th =    [  5.35, 5.85,          5.75, 5.75, 5.75, 5.75]

    names = [ 'B305-L50p100', 'B305-L52p104', 'B305-L55p110', 'B305-L57p115', 'B305-L60p120']
    x =     [   -350, 550, 1450, 2350, 3250]
    x_hexa =[     0.3,  0.3,    0.3, 0.3,  0.3]
    y=      [    3450, 3450, 3450, 3450, 3450]
    z=      [    -4600, -4600, -4600, -4600, -4600]
    chi=    [    -1.6, -1.6, -1.6, -1.6, -1.6]
    th =    [  3.5, 3.5, 3.5, 3.5, 3.5]

    # names = [ 'F11-L60P120V', 'F11-L80P160V']
    # x =     [   15200, 16100]
    # x_hexa =[     0.3 , 0.3]
    # y=      [    650, 650]
    # z=      [    -4800, -4800]
    # chi=    [    -0.1, -0.1]
    # th =    [  5.5, 5.5]


    assert len(names) == len(x), f"len of x ({len(x)}) is different from number of samples ({len(names)})"
    assert len(names) == len(y), f"len of y ({len(y)}) is different from number of samples ({len(names)})"
    assert len(names) == len(x_hexa), f"len of x_hexa ({len(x_hexa)}) is different from number of samples ({len(names)})"
    assert len(names) == len(z), f"len of z ({len(z)}) is different from number of samples ({len(names)})"
    assert len(names) == len(chi), f"len of y ({len(chi)}) is different from number of samples ({len(names)})"
    assert len(names) == len(th), f"len of z ({len(th)}) is different from number of samples ({len(names)})"

    for i in range(1):
        for name, xs, xs_hexa, ys, zs, chis, ths in zip(names, x, x_hexa, y, z, chi, th):
            yield from bps.mv(stage.x, xs_hexa)
            # yield from bps.mv(stage.y, ys_hexa)

            yield from bps.mv(piezo.z, zs)
            yield from bps.mv(piezo.ch, chis)
            yield from bps.mv(piezo.th, ths)
            yield from bps.mv(piezo.x, xs)
            yield from bps.mv(piezo.y, ys)
            # yield from bp
            yield from cd_saxs(phi_offest, phi_offest, 1, exp_t=t, sample=name+'measure_ref-A%s'%(i+1), nume=1)
            yield from cd_saxs(-60+phi_offest, 60+phi_offest, 121, exp_t=t, sample=name+'measure%s'%(i+1), nume=1)
            yield from cd_saxs(phi_offest, phi_offest, 1, exp_t=t, sample=name+'measure_ref-B%s'%(i+1), nume=1)




def cdsaxs_2025_1(t=0.2):
    det = [pil1M]
    phi_offest = 0

    # names = [ 'B305-L50p100', 'B305-L52p104', 'B305-L55p110', 'B305-L57p115', 'B305-L60p120']
    # x =     [   -350, 550, 1450, 2350, 3250]
    # # x_hexa =[     0.3,  0.3,    0.3, 0.3,  0.3]
    # y=      [    3450, 3450, 3450, 3450, 3450]
    # z=      [    -4600, -4600, -4600, -4600, -4600]
    # chi=    [    -1.6, -1.6, -1.6, -1.6, -1.6]
    # th =    [  3.5, 3.5, 3.5, 3.5, 3.5]

    names = [    'intel4',       'W204_F2',    'W204_I9',        'W204_I10',       'W204_H8',     'W204_H11', 'W204_L11', 'W204_M9',  ]
    x =     [     4350,        -22170,      -16860,           -10890,          -5950,         -100,        4600,      10300,   ]
    y=      [    -2100,          8500,        8900,             8650,           8950,         8900,        9000,       9100,   ]
    z=      [     9850,          9060,        9160,             9280,           9420,         9460,        9470,       9600,   ]
    chi=    [      1.3,          -0.9,        -0.2,             -1.0,            1.1,         -0.4,         1.0,          0,   ]
    th =    [    - 0.1,           0.1,         0.1,              0.1,             .1,         0.05,         0.1,          0,   ]

    assert len(names) == len(x), f"len of x ({len(x)}) is different from number of samples ({len(names)})"
    assert len(names) == len(y), f"len of y ({len(y)}) is different from number of samples ({len(names)})"
    # assert len(names) == len(x_hexa), f"len of x_hexa ({len(x_hexa)}) is different from number of samples ({len(names)})"
    assert len(names) == len(z), f"len of z ({len(z)}) is different from number of samples ({len(names)})"
    assert len(names) == len(chi), f"len of y ({len(chi)}) is different from number of samples ({len(names)})"
    assert len(names) == len(th), f"len of z ({len(th)}) is different from number of samples ({len(names)})"

    for i in range(1):
        for nn, (name, xs, ys, zs, chis, ths) in enumerate(zip(names, x, y, z, chi, th)):
            # yield from bps.mv(stage.x, xs_hexa)
            # yield from bps.mv(stage.y, ys_hexa)
            if nn>=4:

                yield from bps.mv(piezo.z, zs)
                yield from bps.mv(piezo.ch, chis)
                yield from bps.mv(piezo.th, ths)
                yield from bps.mv(piezo.x, xs)
                yield from bps.mv(piezo.y, ys)

                if 'intel' in name:
                    number = 2
                else:
                    number = 10              
        

                # yield from bp
                yield from cd_saxs(phi_offest, phi_offest, 1, exp_t=t, sample=name+'measure_ref-A%s'%(i+1), nume=1)
                yield from cd_saxs(-60+phi_offest, 60+phi_offest, 121, exp_t=t, sample=name+'measure%s'%(i+1), nume=number)
                yield from cd_saxs(phi_offest, phi_offest, 1, exp_t=t, sample=name+'measure_ref-B%s'%(i+1), nume=1)

def cdsaxs_2025_1_Karen(t=10):
    det = [pil1M]
    phi_offest = 0

    # names = [ 'B305-L50p100', 'B305-L52p104', 'B305-L55p110', 'B305-L57p115', 'B305-L60p120']
    # x =     [   -350, 550, 1450, 2350, 3250]
    # # x_hexa =[     0.3,  0.3,    0.3, 0.3,  0.3]
    # y=      [    3450, 3450, 3450, 3450, 3450]
    # z=      [    -4600, -4600, -4600, -4600, -4600]
    # chi=    [    -1.6, -1.6, -1.6, -1.6, -1.6]
    # th =    [  3.5, 3.5, 3.5, 3.5, 3.5]

    names = [    '45s_30nm_200nm_pitch',       '45s_30nm_300nm_pitch',    '45s_50nm_200nm_pitch',        '45s_50nm_300nm_pitch',       '45s_100nm_300nm_pitch',     '75s_30nm_200nm_pitch', '75s_30nm_300nm_pitch', '75s_50nm_200nm_pitch',  ]
    x =     [          -23040,                         -23038,                   -23020,                         -23020,                         -23020,                         27080,                   27120,               27120,       ]
    y=      [           -3262,                           -750,                     1750,                           4250,                           6750,                           -1450,                   1050,                3560,       ]
    z=      [            6100,                           6110,                     6080,                           6060,                           6040,                           7770,                    7760,                 7680,         ]
    chi=    [               0,                              0,                        0,                                   0,                               0,                            0,                 0,                     0,            ]
    th =    [               0,                              0,                        0,                                 0,                               0,                            0,                     0,                 0,                   ]

    assert len(names) == len(x), f"len of x ({len(x)}) is different from number of samples ({len(names)})"
    assert len(names) == len(y), f"len of y ({len(y)}) is different from number of samples ({len(names)})"
    # assert len(names) == len(x_hexa), f"len of x_hexa ({len(x_hexa)}) is different from number of samples ({len(names)})"
    assert len(names) == len(z), f"len of z ({len(z)}) is different from number of samples ({len(names)})"
    assert len(names) == len(chi), f"len of y ({len(chi)}) is different from number of samples ({len(names)})"
    assert len(names) == len(th), f"len of z ({len(th)}) is different from number of samples ({len(names)})"

    for i in range(1):
        for nn, (name, xs, ys, zs, chis, ths) in enumerate(zip(names, x, y, z, chi, th)):
            # yield from bps.mv(stage.x, xs_hexa)
            # yield from bps.mv(stage.y, ys_hexa)
            
            if nn>=7:
                yield from bps.mv(piezo.z, zs)
                yield from bps.mv(piezo.ch, chis)
                yield from bps.mv(piezo.th, ths)
                yield from bps.mv(piezo.x, xs)
                yield from bps.mv(piezo.y, ys)
                
                while abs(piezo.y.position - ys) >= 1:
                    print('y motor error')
                    yield from bps.mv(piezo.y, ys)
                    yield from bps.sleep(5)
                
                number = 1              
        

                # yield from bp
                yield from cd_saxs(phi_offest, phi_offest, 1, exp_t=t, sample=name+'measure_ref-A%s'%(i+1), nume=1)
                yield from cd_saxs(-60+phi_offest, 60+phi_offest, 121, exp_t=t, sample=name+'measure%s'%(i+1), nume=number)
                yield from cd_saxs(phi_offest, phi_offest, 1, exp_t=t, sample=name+'measure_ref-B%s'%(i+1), nume=1)
            
def cdsaxs_2025_1_Matt(t=5):
    det = [pil1M]
    phi_offest = 0

    # names = [ 'B305-L50p100', 'B305-L52p104', 'B305-L55p110', 'B305-L57p115', 'B305-L60p120']
    # x =     [   -350, 550, 1450, 2350, 3250]
    # # x_hexa =[     0.3,  0.3,    0.3, 0.3,  0.3]
    # y=      [    3450, 3450, 3450, 3450, 3450]
    # z=      [    -4600, -4600, -4600, -4600, -4600]
    # chi=    [    -1.6, -1.6, -1.6, -1.6, -1.6]
    # th =    [  3.5, 3.5, 3.5, 3.5, 3.5]

    names = [    'W4_D25',       'W2_D25',    'W2_D22',     'W2_D18',       'W1_D9',      'W1_12',     'W_15',   'W3_14',  'W3_20',  'W3_23',]
    x =     [          40620,        -15680,    -29300,      -35500,         -44500,       -32200,     -20100,     28500,    39200,    44500,]
    y=      [           7500,         7500,       7500,        7500,          -7000,        -7000,      -6000,     -6000,    -8000,    -8000,]
    z=      [            2040,         1040,       640,        740,            940,          1140,       1140,      2240,     2440,     2540,]
    chi=    [               0,          0,          0,            0,              0,          3.9,          6,        -4,      1.5,        0,]
    th =    [               0,          0,          0,            0,              0,            0,          0,         0,        0,        0,]

    assert len(names) == len(x), f"len of x ({len(x)}) is different from number of samples ({len(names)})"
    assert len(names) == len(y), f"len of y ({len(y)}) is different from number of samples ({len(names)})"
    # assert len(names) == len(x_hexa), f"len of x_hexa ({len(x_hexa)}) is different from number of samples ({len(names)})"
    assert len(names) == len(z), f"len of z ({len(z)}) is different from number of samples ({len(names)})"
    assert len(names) == len(chi), f"len of y ({len(chi)}) is different from number of samples ({len(names)})"
    assert len(names) == len(th), f"len of z ({len(th)}) is different from number of samples ({len(names)})"

    for i in range(1):
        for nn, (name, xs, ys, zs, chis, ths) in enumerate(zip(names, x, y, z, chi, th)):
            # yield from bps.mv(stage.x, xs_hexa)
            # yield from bps.mv(stage.y, ys_hexa)
            
            if nn>=0:
                yield from bps.mv(piezo.z, zs)
                yield from bps.mv(piezo.ch, chis)
                yield from bps.mv(piezo.th, ths)
                yield from bps.mv(piezo.x, xs)
                yield from bps.mv(piezo.y, ys)
                
                # force piezo.y to move to the correct position
                while abs(piezo.y.position - ys) >= 1:
                    print('y motor error')
                    yield from bps.mv(piezo.y, ys)
                    yield from bps.sleep(4)
                
                number = 1              
        

                # yield from bp
                yield from cd_saxs(phi_offest, phi_offest, 1, exp_t=t, sample=name+'measure_ref-A%s'%(i+1), nume=1)
                yield from cd_saxs(-46+phi_offest, 44+phi_offest, 46, exp_t=t, sample=name+'measure1%s'%(i+1), nume=number)
                yield from cd_saxs(phi_offest, phi_offest, 1, exp_t=t, sample=name+'measure_ref-B%s'%(i+1), nume=1)
                yield from cd_saxs(-45+phi_offest, 45+phi_offest, 46, exp_t=t, sample=name+'measure2%s'%(i+1), nume=number)
                yield from cd_saxs(phi_offest, phi_offest, 1, exp_t=t, sample=name+'measure_ref-C%s'%(i+1), nume=1)
                yield from cd_saxs(-46+phi_offest, 44+phi_offest, 46, exp_t=t, sample=name+'measure3%s'%(i+1), nume=number)
                yield from cd_saxs(phi_offest, phi_offest, 1, exp_t=t, sample=name+'measure_ref-D%s'%(i+1), nume=1)
                yield from cd_saxs(-45+phi_offest, 45+phi_offest, 46, exp_t=t, sample=name+'measure4%s'%(i+1), nume=number)
                yield from cd_saxs(phi_offest, phi_offest, 1, exp_t=t, sample=name+'measure_ref-E%s'%(i+1), nume=1)
            


def cdsaxs_2025_1_scan(t=0.2, scan= [1, 1, 1, 1, 1]):
    det = [pil1M]
    phi_offest = 0

    # names = [ 'B305-L50p100', 'B305-L52p104', 'B305-L55p110', 'B305-L57p115', 'B305-L60p120']
    # x =     [   -350, 550, 1450, 2350, 3250]
    # # x_hexa =[     0.3,  0.3,    0.3, 0.3,  0.3]
    # y=      [    3450, 3450, 3450, 3450, 3450]
    # z=      [    -4600, -4600, -4600, -4600, -4600]
    # chi=    [    -1.6, -1.6, -1.6, -1.6, -1.6]
    # th =    [  3.5, 3.5, 3.5, 3.5, 3.5]

    names = [     'W204_F2',    'W204_I9',        'W204_I10',       'W204_H8',     'W204_H11', 'W204_L11', 'W204_M9',  ]
    x =     [      -22170,      -16860,           -10890,          -5950,         -100,        4600,      10300,   ]
    y=      [           8500,        8900,             8650,           8950,         8900,        9000,       9100,   ]
    z=      [          9060,        9160,             9280,           9420,         9460,        9470,       9600,   ]
    chi=    [                -0.9,        -0.2,             -1.0,            1.1,         -0.4,         1.0,          0,   ]
    th =    [              0.1,         0.1,              0.1,             .1,         0.05,         0.1,          0,   ]


    # names = [    'test',  ]
    # x =     [      -22170]
    # y=      [           8500]
    # z=      [          9060 ]
    # chi=    [                -0.9  ]
    # th =    [              0.1 ]


    assert len(names) == len(x), f"len of x ({len(x)}) is different from number of samples ({len(names)})"
    assert len(names) == len(y), f"len of y ({len(y)}) is different from number of samples ({len(names)})"
    # assert len(names) == len(x_hexa), f"len of x_hexa ({len(x_hexa)}) is different from number of samples ({len(names)})"
    assert len(names) == len(z), f"len of z ({len(z)}) is different from number of samples ({len(names)})"
    assert len(names) == len(chi), f"len of y ({len(chi)}) is different from number of samples ({len(names)})"
    assert len(names) == len(th), f"len of z ({len(th)}) is different from number of samples ({len(names)})"

    for i in range(1):
        for name, xs, ys, zs, chis, ths in zip(names, x, y, z, chi, th):
            yield from bps.mv(piezo.z, zs)
            yield from bps.mv(piezo.ch, chis)
            yield from bps.mv(piezo.th, ths)
            yield from bps.mv(piezo.x, xs)
            yield from bps.mv(piezo.y, ys)

            number = 10           
    
            ############# scan phi (PRS)
            if scan[0]:
                print("==== scan PRS")
                # yield from bp
                # yield from cd_saxs(phi_offest, phi_offest, 1, exp_t=t, sample=name+'measure_ref-A%s'%(i+1), nume=1)
                yield from cd_saxs(-1+phi_offest, 1+phi_offest, 41, exp_t=t, sample=name+'phi-scan%s'%(i+1), nume=number)
                # yield from cd_saxs(phi_offest, phi_offest, 1, exp_t=t, sample=name+'measure_ref-B%s'%(i+1), nume=1)

            ############# scan y
            if scan[1]:
                print("==== scan y")
                phi = phi_offest
                yield from bps.mv(prs, phi_offest)
                yield from bps.mv(piezo.z, zs)
                yield from bps.mv(piezo.ch, chis)
                yield from bps.mv(piezo.th, ths)
                yield from bps.mv(piezo.x, xs)
                yield from bps.mv(piezo.y, ys)

                det_exposure_time(t, t*number)

                for ii, yys in enumerate(np.arange(-0.3, 0.3+0.01, 0.05)):
                    ypos = ys + yys
                    yield from bps.mv(piezo.y, ypos)

                    sample=name+'y-scan%s'%(ii+1)
                    name_fmt = "{sample}_5.2m_16.1keV_num{num}_{phi}deg_y{y}_yr{yr}_z{z}_bpm{bpm}"
                    sample_name = name_fmt.format(sample=sample, num="%2.2d"%ii, phi="%2.2d"%phi, y="%5.2d"%ypos, yr="%5.2d"%yys, z="%2.2d"%zs, bpm="%1.3f"%xbpm3.sumX.get())
                    # sample_id(user_name="JK", sample_name=sample_name)
                    sample_id(sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(det, num=1)
                    
                yield from bps.mv(piezo.y, ys)

            ############# scan z
            if scan[2]:
                print("==== scan z")
                number = 1
                det_exposure_time(t, t*number)

                phi = phi_offest
                yield from bps.mv(prs, phi_offest)
                yield from bps.mv(piezo.z, zs)
                yield from bps.mv(piezo.ch, chis)
                yield from bps.mv(piezo.th, ths)
                yield from bps.mv(piezo.x, xs)
                yield from bps.mv(piezo.y, ys)

                z_list = [-20000, -10000,  -9000,  -8000,  -7000,  -6000,  -5000,  -4000,  -3000,
            -2000,  -1000,   -500, -400, -300, -200, -100,    0,  100,  200,  300,  400,  500,
                1000,   2000,   3000,   4000,   5000,
            6000,   7000,   8000,   9000, 10000, 20000]
                for ii, zzs in enumerate(z_list):
                    zpos = zs + zzs
                    yield from bps.mv(piezo.z, zpos)

                    sample=name+'z-scan%s'%(ii+1)
                    name_fmt = "{sample}_5.2m_16.1keV_num{num}_{phi}deg_y{y}_z{z}_zr{zr}_bpm{bpm}"
                    sample_name = name_fmt.format(sample=sample, num="%2.2d"%ii, phi="%2.2f"%phi, y="%5.2d"%ys, z="%2.2d"%zpos, zr="%2.2d"%zzs, bpm="%1.3f"%xbpm3.sumX.get())
                    # sample_id(user_name="JK", sample_name=sample_name)
                    sample_id(sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(det, num=1)
                    
                yield from bps.mv(piezo.y, ys)
                yield from bps.mv(piezo.z, zs)
                        
            ############# scan theta
            if scan[3]:
                print("==== scan theta")
                phi = phi_offest
                yield from bps.mv(prs, phi_offest)
                yield from bps.mv(piezo.z, zs)
                yield from bps.mv(piezo.ch, chis)
                yield from bps.mv(piezo.th, ths)
                yield from bps.mv(piezo.x, xs)
                yield from bps.mv(piezo.y, ys)

                det_exposure_time(t, t*number)

                for ii, thr in enumerate(np.arange(-1, 1.01, 0.1)):
                    thpos = ths + thr
                    yield from bps.mv(piezo.th, thpos)

                    sample=name+'th-scan%s'%(ii+1)
                    name_fmt = "{sample}_5.2m_16.1keV_num{num}_{phi}deg_th{th}_thr{thr}_z{z}_bpm{bpm}"
                    sample_name = name_fmt.format(sample=sample, num="%2.2d"%ii, phi="%2.2f"%phi, th="%5.2f"%thpos, thr="%5.2f"%thr, z="%2.2d"%zs, bpm="%1.3f"%xbpm3.sumX.get())
                    # sample_id(user_name="JK", sample_name=sample_name)
                    sample_id(sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(det, num=1)
                    

            ############# scan chi
            if scan[4]:

                print("==== scan chi")
                phi = phi_offest
                yield from bps.mv(prs, phi_offest)
                yield from bps.mv(piezo.z, zs)
                yield from bps.mv(piezo.ch, chis)
                yield from bps.mv(piezo.th, ths)
                yield from bps.mv(piezo.x, xs)
                yield from bps.mv(piezo.y, ys)

                det_exposure_time(t, t*number)

                for ii, chr in enumerate(np.arange(-1, 1.01, 0.1)):
                    chpos = chis + chr
                    yield from bps.mv(piezo.ch, chpos)

                    sample=name+'ch-scan%s'%(ii+1)
                    name_fmt = "{sample}_5.2m_16.1keV_num{num}_{phi}deg_ch{ch}_chr{chr}_z{z}_bpm{bpm}"
                    sample_name = name_fmt.format(sample=sample, num="%2.2d"%ii, phi="%2.2f"%phi, ch="%5.2f"%chpos, chr="%5.2f"%chr, z="%2.2d"%zs, bpm="%1.3f"%xbpm3.sumX.get())
                    # sample_id(user_name="JK", sample_name=sample_name)
                    sample_id(sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(det, num=1)
                            





def cd_gisaxs(t=1):
    prs_offset = -1.854

    det = [pil1M]
    det_exposure_time(t, t)

    names = ['sam2_g1',  'sam2_g2',  'sam2_g3',  'sam2_g4', 'sam2_g5', 'sam2_g6']
    x =     [   -29300,     -35300,     -21300,     -17300,     -13300,    -9300]
    x_hexa =[     0.20,       0.20,       0.20,       0.20,       0.20,     0.20]
    y=      [     6900,       6900,       6900,       6900,       6900,     6900]
    y_hexa =[      0.0,        0.0,        0.0,        0.0,        0.0,      0.0]
    z=      [      200,        200,        200,        200,        200,      200]
    chi=    [   -1.055,     -1.055,     -1.055,     -1.055,     -1.055,   -1.055]
    th =    [  -0.7229,    -0.7229,    -0.7229,    -0.7229,    -0.7229,  -0.7229]

    names = ['sam2_g2',  'sam2_g3',  'sam2_g4', 'sam2_g5', 'sam2_g6']
    x =     [   -25300,     -21300,     -17300,     -13300,    -9300]
    x_hexa =[     0.20,       0.20,       0.20,       0.20,     0.20]
    y=      [     6900,       6900,       6900,       6900,     6900]
    y_hexa =[      0.0,        0.0,        0.0,        0.0,      0.0]
    z=      [      200,        200,        200,        200,      200]
    chi=    [   -1.055,     -1.055,     -1.055,     -1.055,   -1.055]
    th =    [  -0.7229,    -0.7229,    -0.7229,    -0.7229,  -0.7229]

    assert len(names) == len(x), f"len of x ({len(x)}) is different from number of samples ({len(names)})"
    assert len(names) == len(y), f"len of y ({len(y)}) is different from number of samples ({len(names)})"
    assert len(names) == len(x_hexa), f"len of x_hexa ({len(x_hexa)}) is different from number of samples ({len(names)})"
    assert len(names) == len(z), f"len of z ({len(z)}) is different from number of samples ({len(names)})"
    assert len(names) == len(chi), f"len of y ({len(chi)}) is different from number of samples ({len(names)})"
    assert len(names) == len(th), f"len of z ({len(th)}) is different from number of samples ({len(names)})"

    for name, xs, xs_hexa, ys, ys_hexa, zs, chis, ths in zip(names, x, x_hexa, y, y_hexa, z, chi, th):
        yield from bps.mv(prs, prs_offset)
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(stage.y, ys_hexa)
        yield from bps.mv(piezo.z, zs)
        yield from bps.mv(piezo.ch, chis)
        yield from bps.mv(piezo.th, ths)
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)

        yield from alignement_gisaxs_hex(0.1)
        
        ai0=stage.th.position

        for num, ai in enumerate([0.15, 0.20, 0.30, 0.50]):
            if ai == 0.15:
                    yield from bps.mv(att1_5.open_cmd, 1)
                    yield from bps.mv(att1_6.open_cmd, 1)
                    yield from bps.sleep(2)
                    yield from bps.mv(att1_5.open_cmd, 1)
                    yield from bps.mv(att1_6.open_cmd, 1)
            else:
                    yield from bps.mv(att1_5.close_cmd, 1)
                    yield from bps.mv(att1_6.open_cmd, 1)
                    yield from bps.sleep(2)
                    yield from bps.mv(att1_5.close_cmd, 1)
                    yield from bps.mv(att1_6.open_cmd, 1)       

            yield from bps.mv(stage.th, ai0+ai)
            
            for num1, phi in enumerate(np.concatenate([np.linspace(-5, -1.02, 200), np.linspace(-1, 1, 401), np.linspace(1.02, 5, 200)])):
                yield from bps.mv(prs, prs_offset+phi)

                name_fmt = "{sample}_9.2m_16.1keV_phi{phii}deg_ai{aii}deg"
                sample_name = name_fmt.format(sample=name, num="%2.2d"%num1, phii="%1.3f"%phi, aii="%1.2f"%ai)
                sample_id(user_name="KY_GI", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(det, num=1)



    prs_offset = -3.337
    names = ['sam1_g1',  'sam1_g2',  'sam1_g3',  'sam1_g4', 'sam1_g5', 'sam1_g6']
    x =     [    42700,      38700,      34700,      30700,      26700,    22700]
    x_hexa =[     0.20,       0.20,       0.20,       0.20,       0.20,     0.20]
    y=      [     6900,       6900,       6900,       6900,       6900,     6900]
    y_hexa =[      0.0,        0.0,        0.0,        0.0,        0.0,      0.0]
    z=      [      200,        200,        200,        200,        200,      200]
    chi=    [   -1.055,     -1.055,     -1.055,     -1.055,     -1.055,   -1.055]
    th =    [  -0.7229,    -0.7229,    -0.7229,    -0.7229,    -0.7229,  -0.7229]

    assert len(names) == len(x), f"len of x ({len(x)}) is different from number of samples ({len(names)})"
    assert len(names) == len(y), f"len of y ({len(y)}) is different from number of samples ({len(names)})"
    assert len(names) == len(x_hexa), f"len of x_hexa ({len(x_hexa)}) is different from number of samples ({len(names)})"
    assert len(names) == len(z), f"len of z ({len(z)}) is different from number of samples ({len(names)})"
    assert len(names) == len(chi), f"len of y ({len(chi)}) is different from number of samples ({len(names)})"
    assert len(names) == len(th), f"len of z ({len(th)}) is different from number of samples ({len(names)})"

    for name, xs, xs_hexa, ys, ys_hexa, zs, chis, ths in zip(names, x, x_hexa, y, y_hexa, z, chi, th):
        yield from bps.mv(prs, prs_offset)

        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(stage.y, ys_hexa)
        yield from bps.mv(piezo.z, zs)
        yield from bps.mv(piezo.ch, chis)
        yield from bps.mv(piezo.th, ths)
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)

        yield from alignement_gisaxs_hex(0.1)
        ai0=stage.th.position

        for num, ai in enumerate([0.15, 0.20, 0.30, 0.50]):
            if ai == 0.15:
                    yield from bps.mv(att1_5.open_cmd, 1)
                    yield from bps.mv(att1_6.open_cmd, 1)
                    yield from bps.sleep(2)
                    yield from bps.mv(att1_5.open_cmd, 1)
                    yield from bps.mv(att1_6.open_cmd, 1)
            else:
                    yield from bps.mv(att1_5.close_cmd, 1)
                    yield from bps.mv(att1_6.open_cmd, 1)
                    yield from bps.sleep(2)
                    yield from bps.mv(att1_5.close_cmd, 1)
                    yield from bps.mv(att1_6.open_cmd, 1)       

            yield from bps.mv(stage.th, ai0+ai)
            
            for num1, phi in enumerate(np.concatenate([np.linspace(-5, -1.02, 200), np.linspace(-1, 1, 401), np.linspace(1.02, 5, 200)])):
                yield from bps.mv(prs, prs_offset+phi)

                name_fmt = "{sample}_9.2m_16.1keV_phi{phii}deg_ai{aii}deg"
                sample_name = name_fmt.format(sample=name, num="%2.2d"%num1, phii="%1.3f"%phi, aii="%1.2f"%ai)
                sample_id(user_name="KY_GI", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(det, num=1)
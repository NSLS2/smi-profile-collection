# 2023-June-2 Fri
#
# 16.1 keV, 200*30um beam, air
# proposal_id("2023_2", "312283_Jones", analysis=True)
# RE.md['SAF_number'] = 311104
# RE.md['SAXS_setup'] = {'sdd': 9200, 'beam_centre': [450, 554], 'bs': 'rod', 'energy': 16100}
# 
# RE(rel_scan([pil1M], stage.y, -2, 2, 15)); ps()
# ---------------------------------------------------------------
# ---------------------------------------------------------------
# 1. [Search hutch and close]
# 2. RE(shopen())
# 3. [Enter sample name and x-position in this 30-user-Jones.py]
# [Ctrl+s to save this file]
# %run -i /home/xf12id/.ipython/profile_collection/startup/users/30-user-Jones.py
#
# (Just in case)
# Ctrl+c once/twice; RE.abort()
# bsui
# %run -i /home/xf12id/.ipython/profile_collection/startup/users/30-user-Jones.py
#
# 4. RE(shclose())
# 5. [To take out sample]
# ---------------------------------------------------------------
# Note: 
# beamstop_save()

def run_giswaxs_2025C1(t=2, flag_align=1, flag_reflect = 1, waxs_angles = [15, 0], piezo_y_init=6700):
    
    ###### Bar 1
    if 0:
        x_offset = -49000-3000
        temp = [9000, 15000, 20000, 25000, 
                31000, 37000, 43000, 48000, 55000, 
                60000, 66000, 72000, 77000, 84000, 
                90000, 95000, 101000]
        # temp = [3000]
        x_array = x_offset + np.array(temp)
        x_list = list(x_array)

        sample_list = [
            'sam2_a85_S2VPL52_SR1.5_85C', 'sam3_a90_S2VPL52_SR1.5_90C', 'sam4_a100_S2VPL52_SR1.5_100C', 'sam5_a110_S2VPL52_SR1.5_110C', 
            'sam6_a120_S2VPL52_SR1.5_120C', 'sam7_a130_S2VPL52_SR1.5_130C', 'sam8_b_S2VPL52(80)_PS6k(20)_SR1.5', 'sam9_b85_S2VPL52(80)_PS6k(20)_SR1.5_85C', 'sam10_b90_S2VPL52(80)_PS6k(20)_SR1.5_90C', 
            'sam11_b100_S2VPL52(80)_PS6k(20)_SR1.5_100C', 'sam12_b110_S2VPL52(80)_PS6k(20)_SR1.5_110C', 'sam13_b120_S2VPL52(80)_PS6k(20)_SR1.5_120C', 'sam14_b130_S2VPL52(80)_PS6k(20)_SR1.5_130C', 'sam15_c_S2VPL52(80)_PS3k(20)_SR1.5', 
            'sam16_c85_S2VPL52(80)_PS3k(20)_SR1.5_85C', 'sam17_c90_S2VPL52(80)_PS3k(20)_SR1.5_90C', 'sam18_c100_S2VPL52(80)_PS3k(20)_SR1.5_100C']

        # sample_list = [
        #     'sam1_a_S2VPL52_SR1.5']

    ###### Bar 2
    x_offset = -49000-3000
    temp = [3000, 9000, 15000, 22000, 28000, 34000, 40000, 45000, 52000, 58000, 63000, 70000, 75000]
    x_array = x_offset + np.array(temp)
    x_list = list(x_array)
    sample_list = ['b2sam1_c110_S2VPL52(80)_PS3k(20)_SR1.5_110C', 'b2sam2_c120_S2VPL52(80)_PS3k(20)_SR1.5_120C', 
                   'b2sam3_c130_S2VPL52(80)_PS3k(20)_SR1.5_130C', 'b2sam4_d_S2VPL52(80)_PS6k(10)_P2VP6k(10)_SR1.5', 
                   'b2sam5_d85_S2VPL52(80)_PS6k(10)_P2VP6k(10)_SR1.5_85C', 'b2sam6_d90_S2VPL52(80)_PS6k(10)_P2VP6k(10)_SR1.5_90C', 
                   'b2sam7_d100_S2VPL52(80)_PS6k(10)_P2VP6k(10)_SR1.5_100C', 'b2sam8_d110_S2VPL52(80)_PS6k(10)_P2VP6k(10)_SR1.5_110C',
                'b2sam9_d120_S2VPL52(80)_PS6k(10)_P2VP6k(10)_SR1.5_120C', 'b2sam10_d130_S2VPL52(80)_PS6k(10)_P2VP6k(10)_SR1.5_130C', ''
                'b2sam11_e_S2VPL52(80)_P2VP6k(20)_SR1.5', 'b2sam12_e100_S2VPL52(80)_P2VP6k(20)_SR1.5_100C', 'b2sam13_e120_S2VPL52(80)_P2VP6k(20)_SR1.5_120C']



    t0 = time.time()
    assert len(x_list) == len(sample_list), f"Sample name/position list is incorrect"

    # data_dir = '/nsls2/data/smi/legacy/results/data/2024_1/312437_Jones/'
    data_dir = '/nsls2/data/smi/legacy/results/data/2025_1/317473_ETsai/'

    x_shift_array = np.asarray([0]) 
    for x, sample in zip(x_list, sample_list):  # loop over samples on bar

        yield from bps.mv(piezo.x, x)  # move to next sample
        if flag_align:
            yield from bps.mv(piezo.th, 0) 
            yield from bps.mv(piezo.y, piezo_y_init) 
            yield from alignement_gisaxs(0.1, flag_reflect=flag_reflect)  # run alignment routine
        else:
            yield from SMI_Beamline().modeMeasurement()

        print('##### {}, x = {}, aligned at y = {}, theta = {}'.format(sample, piezo.x.position, piezo.y.position, piezo.th.position))
        if flag_align:
            #aligned_positions.append([sample, piezo.x.position, piezo.y.position, piezo.th.position])
            with open(data_dir+'Align/aligned_positions.txt', 'a') as f:
                note = '{}: x{}, y{}, th{},'.format(sample, piezo.x.position, piezo.y.position, piezo.th.position)
                f.write(note)
                f.write('\n')

        det_exposure_time(t, t)
        x_pos_array = x  + x_shift_array

        # for waxs_angle in waxs_angles:  # loop through waxs angles
        #     yield from bps.mv(waxs, waxs_angle)
        if 1:

            # if waxs_angle >= 15:
            #     dets = [pil900KW, pil1M] 
            #     angle_arc = np.array([0.08, 0.12, 0.16, 0.2])  # incident angles
            # else:
            #     dets = [pil900KW] 
            #     angle_arc = np.array([0.08, 0.12, 0.16, 0.2])  # incident angles

            dets = [pil1M] 
            # angle_arc = np.array([0.12])  # incident angles
            angle_arc = np.array([0.05, 0.08, 0.1, 0.12])  # incident angles
            th_meas = (
                angle_arc + piezo.th.position
            ) 

            for x_pos in x_pos_array:
                yield from bps.mv(piezo.x, x_pos)  

                for i, th in enumerate(th_meas):  # loop over incident angles
                    yield from bps.mv(piezo.th, th)

                    sample_name = "{sample}_{th:5.4f}deg_x{x}_{t}s".format( #_waxs{waxs_angle:05.2f}
                        sample=sample,
                        th=angle_arc[i],
                        #waxs_angle=waxs_angle,
                        x=x_pos,
                        t=t,
                        #scan_id=RE.md["scan_id"],
                    )
                    # name_fmt = '{sample}_16.1keV_8.3m_waxs{waxs_angle:05.2f}_x{x:04.2f}_{t:05.2f}s_{scan_id}'
                    # sample_name = name_fmt.format(sample=sample, waxs_angle=waxs_angle, x=x, t=t, scan_id=RE.md['scan_id'])
                    sample_id(user_name="KM", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")

                    # yield from bp.scan(dets, energy, e, e, 1)
                    # yield from bp.scan(dets, waxs, *waxs_arc)
                    yield from bp.count(dets, num=1)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)
    print('Total time = {}min.'.format((time.time()-t0)/60))





#sample_id(user_name='test', sample_name=f'test{get_scan_md()}')
def measure_saxs(t=1, user_name="NEA", sample='D2O_s1', xr_list = [0, 100], yr_list = [0, 500]):
    x0 = piezo.x.position
    y0 = -8000 #piezo.y.position
    dets = [pil1M]
    det_exposure_time(t, t)

    for xr in xr_list:
        for yr in yr_list:
            x = x0+xr
            y = x0+yr
            yield from bps.mv(piezo.x, x0+xr)
            yield from bps.mv(piezo.y, y0+yr)

            sample_name = "{sample}_x{x:06.0f}_y{y:06.0f}_{md}".format(
                sample=sample,
                x=x,
                y=y0,
                md=get_scan_md(),
            )
            sample_id(user_name=user_name, sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")

            yield from bp.count(dets, num=1)


def measure_saxs_array(t=1, user_name="SF", sample='Ba4_d', xr_list = [-200, 0]):
    #x0 = piezo.x.position
    x0_list = np.arange(-43550, 40451-12000, 6000)
    # x0_list = [-19400, -13500]

    for idx, x0 in enumerate(x0_list):
        y0 = piezo.y.position
        dets = [pil1M]
        det_exposure_time(t, t)

        for xr in xr_list:
            x = x0+xr
            yield from bps.mv(piezo.x, x0+xr)

            sample_name = "{sample}{ii}_sdd2200_x{x:06.0f}_y{y:06.0f}_{t}s".format(
                sample=sample,
                ii = idx+1,
                x=x,
                y=y0,
                t=t,
            )
            sample_id(user_name=user_name, sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")

            yield from bp.count(dets, num=1)


## RE(measure_waxs(t=1, waxs_angle=0, user_name="SM", sample='test', yr_list = np.arange(-200, 210, 20))
def measure_waxs(t=1, waxs_angle=0, user_name="CK", sample='test', yr_list = [-50, 0, 50]):
    
    #yield from bps.mv(waxs, waxs_angle)
    #yield from bps.mv(piezo.y, 3880)

    x0_list = [piezo.x.position] #pos5, -17500
    #x0_list = np.arange(-43550, 40451, 6000)
    # x0_list = [-42700] #, -36100, -29900, -23900, -17300, -10800, -4300, 8500, 15000, 21300, ]
    x0_list = [-42750,     -33550, -24550, -16050,-7550, 1750,    10450, 19450, 28850 ] #37650, 46500 ]
    #y0_list = [-10500, 2400, ] #19
    # sam_list = ['s11',     's10', 's9', 's8','s7', 's6',     's5','s4','s3','s2',  's1']
    sam_list = ['s12',     's13', 's14_sam1', 's15_sam2','s16_sam3', 's17_sam4',     's18_sam5','s19_sam6','s20_sam7',]
  
    for x0, sample in zip(x0_list, sam_list):
        yield from bps.mv(piezo.x, x0)

        y0 = piezo.y.position
        dets = [pil900KW]
        det_exposure_time(t, t)

        for yr in yr_list:
            y = y0+yr
            yield from bps.mv(piezo.y, y0+yr)

            sample_name = "{sample}_x{x:06.0f}_y{y:06.0f}_waxs{waxs_angle:05.2f}_{t}s".format(
                sample=sample,
                x=x0,
                y=y,
                waxs_angle = waxs_angle,
                t=t,
            )
            sample_id(user_name=user_name, sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")

            yield from bp.count(dets, num=1)


def test_measure(t=1, waxs_angle=0, user_name="test", sample_name='EmptyKapton', dets = [pil1M, pil900KW]):
    yield from bps.mv(waxs, waxs_angle)
    sample_id(user_name=user_name, sample_name=sample_name)
    det_exposure_time(t, t)
    yield from bp.count(dets, num=1)

def move_waxs(waxs_angle=20):
    yield from bps.mv(waxs, waxs_angle)


def alignement_gisaxs(angle=0.15, flag_reflect = 1):
    """
    Regular alignement routine for gisaxs and giwaxs. First, scan of the sample height and incident angle on the direct beam.
    Then scan of teh incident angle, height and incident angle again on the reflected beam.

    param angle: np.float. Angle at which the alignement on the reflected beam will be done

    """

    # Activate the automated derivative calculation
    bec._calc_derivative_and_stats = True

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)

    smi = SMI_Beamline()
    yield from smi.modeAlignment(technique="gisaxs")

    # Set direct beam ROI
    yield from smi.setDirectBeamROI(size=[48, 36])

    # Scan theta and height
    yield from align_gisaxs_height(800, 21, der=True)
    yield from align_gisaxs_th(1.5, 31)

    if flag_reflect:
        print('## Align with reflected beam.....')
        # move to theta 0 + value
        yield from bps.mv(piezo.th, ps.peak + angle)

        # Set reflected ROI
        yield from smi.setReflectedBeamROI(total_angle=angle, technique="gisaxs", size=[48, 16])

        # Scan theta and height
        yield from align_gisaxs_th(0.2, 21)
        yield from align_gisaxs_height_rb(150, 16)
        yield from align_gisaxs_th(0.025, 21)  # was .025, 21 changed to .1 31
    else:
        print('## Align with direct beam.....')
        # Scan theta and height
        yield from align_gisaxs_height(200, 16, der=True)
        yield from align_gisaxs_th(0.3, 21)

    # Close all the matplotlib windows
    #plt.close("all")

    # Return angle
    if flag_reflect:
        yield from bps.mv(piezo.th, ps.cen - angle)
    else:
        yield from bps.mv(piezo.th, ps.peak)

    yield from smi.modeMeasurement()

    # Deactivate the automated derivative calculation
    bec._calc_derivative_and_stats = False

    
# 2023-Jun-2 Static, pil1M Y-44.4
# RE(run_giswaxs(t=5, , flag_align=1))
# RE(run_giswaxs(t=5, flag_align=1, flag_reflect=0, piezo_y_init=7700))
def run_giswaxs(t=2, flag_align=1, flag_reflect = 0, waxs_angles = [15, 0], piezo_y_init=7500):
    x_list = [-33700, -25700, -17700, -9700, 
              -2700, 4300, 12300, 18300, 24300, 
              33300, 39300]
    sample_list = ["ZC_Bar1s3", "ZC_Bar1s4", "ZC_Bar1s5", "ZC_Bar1s6",
                "ZC_Bar1s7", "ZC_Bar1s8", "ZC_Bar1s9", "ZC_Bar1s10", "ZC_Bar1s11", 
                "ZC_Bar1s12", "ZC_Bar1s13"]

    t0 = time.time()
    assert len(x_list) == len(sample_list), f"Sample name/position list is incorrect"

    data_dir = '/nsls2/data/smi/legacy/results/data/2024_1/312437_Jones/'

    x_shift_array = np.asarray([0, -100]) 
    for x, sample in zip(x_list, sample_list):  # loop over samples on bar
        # if 's1' in sample or 's4' in sample or 's5' in sample:
        #     x_shift_array = np.asarray([0, -100]) 
        # else:
        #     x_shift_array = np.asarray([0]) 

        yield from bps.mv(piezo.x, x)  # move to next sample
        if flag_align:
            yield from bps.mv(piezo.th, 0) 
            yield from bps.mv(piezo.y, piezo_y_init) 
            yield from alignement_gisaxs(0.1, flag_reflect=flag_reflect)  # run alignment routine
        else:
            yield from SMI_Beamline().modeMeasurement()

        print('##### {}, x = {}, aligned at y = {}, theta = {}'.format(sample, piezo.x.position, piezo.y.position, piezo.th.position))
        #aligned_positions.append([sample, piezo.x.position, piezo.y.position, piezo.th.position])
        with open(data_dir+'Align/aligned_positions.txt', 'a') as f:
            note = '{}: x{}, y{}, th{},'.format(sample, piezo.x.position, piezo.y.position, piezo.th.position)
            f.write(note)
            f.write('\n')

        det_exposure_time(t, t)
        x_pos_array = x  + x_shift_array

        for waxs_angle in waxs_angles:  # loop through waxs angles
            yield from bps.mv(waxs, waxs_angle)

            if waxs_angle >= 15:
                dets = [pil900KW, pil1M] 
                angle_arc = np.array([0.08, 0.12, 0.16, 0.2])  # incident angles
            else:
                dets = [pil900KW] 
                angle_arc = np.array([0.08, 0.12, 0.16, 0.2])  # incident angles

            th_meas = (
                angle_arc + piezo.th.position
            ) 

            for x_pos in x_pos_array:
                yield from bps.mv(piezo.x, x_pos)  

                for i, th in enumerate(th_meas):  # loop over incident angles
                    yield from bps.mv(piezo.th, th)

                    sample_name = "{sample}_{th:5.4f}deg_waxs{waxs_angle:05.2f}_x{x}_{t}s".format(
                        sample=sample,
                        th=angle_arc[i],
                        waxs_angle=waxs_angle,
                        x=x_pos,
                        t=t,
                        #scan_id=RE.md["scan_id"],
                    )
                    # name_fmt = '{sample}_16.1keV_8.3m_waxs{waxs_angle:05.2f}_x{x:04.2f}_{t:05.2f}s_{scan_id}'
                    # sample_name = name_fmt.format(sample=sample, waxs_angle=waxs_angle, x=x, t=t, scan_id=RE.md['scan_id'])
                    sample_id(user_name="GI", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")

                    # yield from bp.scan(dets, energy, e, e, 1)
                    # yield from bp.scan(dets, waxs, *waxs_arc)
                    yield from bp.count(dets, num=1)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)
    print('Total time = {}min.'.format((time.time()-t0)/60))

# =============== Humidity Chamber ===============
# readHumidity()
# moxa_in.ch1_sp.get()
# moxa_in.ch1_sp.put(0)
#RE(set_humidity_90())
def set_humidity_80(): # Set up but didn't use for 2023-June
    setWetFlow(3.5)
    setDryFlow(1.5)

# RE(alignement_gisaxs_hex(angle=0.1, rough_y=0.5, flag_reflection = 1))
def alignement_gisaxs_hex(angle=0.1, rough_y=0.5, flag_reflection = 1):
    """
    Regular alignement routine for gisaxs and giwaxs using the hexapod. First,
    scan of the sample height and incident angle on the direct beam. Then scan
    of teh incident angle, height and incident angle again on the reflected beam.
    param angle: np.float. Angle at which the alignement on the reflected beam will be done

    """

    # Activate the automated derivative calculation
    bec._calc_derivative_and_stats = True

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)

    smi = SMI_Beamline()
    yield from smi.modeAlignment()

    # Set direct beam ROI
    yield from smi.setDirectBeamROI(size=[48, 36])

    # Scan theta and height
    yield from align_gisaxs_height_hex(rough_y, 21, der=True)
    yield from align_gisaxs_th_hex(0.6, 16)
   
    if flag_reflection:
        # move to theta 0 + value
        yield from bps.mv(stage.th, ps.cen + angle)

        # Set reflected ROI
        yield from smi.setReflectedBeamROI(total_angle=angle, technique='gisaxs', size=[48, 16])

        # Scan theta and height
        yield from align_gisaxs_th_hex(0.8, 21)
        yield from align_gisaxs_height_hex(0.1, 15)
        yield from align_gisaxs_th_hex(0.1, 16)
    else:
        # Scan theta and height
        yield from align_gisaxs_height_hex(0.5, 13, der=True)
        yield from align_gisaxs_th_hex(0.5, 16)
        yield from align_gisaxs_height_hex(0.2, 13, der=True)
        yield from align_gisaxs_th_hex(0.2, 16)

    if flag_reflection:
        # Return angle
        yield from bps.mv(stage.th, ps.cen - angle)

    # Close all the matplotlib windows
    #plt.close("all")
    print('### Aligned x{}, y{}, z{}'.format(stage.x, stage.y, stage.th))

    # Return angle
    #      yield from bps.mvr(stage.th, -angle)
    yield from smi.modeMeasurement()

    # Deactivate the automated derivative calculation
    bec._calc_derivative_and_stats = False


# RE(run_gi_humid(t=5, flag_align = 0, Nmax=1000, time_hr = [0.05, 0.1] , time_sleep_sec= [20, 10, 8]))
#2023-June. Hexa with z~3, theta=1.5, x -14/-12 to 18/20, y -20 to 8 still ok
#Maybe better to do each alignment manually with: 
# RE(alignement_gisaxs_hex(angle=0.1, rough_y=0.5, flag_reflection = 1))
# RE(rel_scan([pil1M], stage.y, -0.2, 0.2, 16))
# RE(rel_scan([pil1M], stage.th, -0.5, 0.5, 11))
# RE(rel_scan([pil1M, pil900KW], stage.y, -0.3, 0.3, 13))
# RE(rel_scan([pil1M, pil900KW], stage.th, -0.5, 0.5, 11))
# 
# RE(run_gi_humid(t=1, flag_align = 0, n0=42, t0 = None, Nmax=15, time_hr = [0.05, 0.1] , time_sleep_sec= [10, 5, 4]))
# RE(run_gi_humid(t=1, flag_align = 0, n0=0, t0 = t0, Nmax=9999, time_hr = [4, 6] , time_sleep_sec= [3600, 1200, 600]))
# RE(run_gi_humid(t=1, flag_align = 0, n0=0, t0 = t0, Nmax=9999, time_hr = [3, 6] , time_sleep_sec= [3600, 600, 900]))
def run_gi_humid(t=5, flag_align = 0, n0=0, t0 = 0, Nmax=9999, time_hr = [4, 8] , time_sleep_sec= [1200, 600, 30]):

    sample_list = [
        "ZC_dynamic16",
        "ZC_dynamic17",
        "ZC_dynamic18",
        "ZC_dynamic19",
        "ZC_dynamic20",
    ]

    waxs_angles = np.array(
        [15]
    )

    if flag_align == 0:
        x_hexa_list = [12.8, 7.5, 2.0, -3.3, -9.0]  
        y_hexa_aligned = [3.401, 3.398, 3.41, 3.4, 3.379]     
        th_hexa_aligned = [2.467, 2.434, 2.456, 2.54, 2.437]
        # x_hexa_list = [-9.0, -3.5 ]  
        # y_hexa_aligned = [-6.54]     
        # th_hexa_aligned = [2.62]    
    else:
        # Intial positions
        x_hexa_list = [2]  
        y_hexa_list = [3.4]     
        th_hexa_list = [0.6]

        ## Align all samples & save positions
        th_hexa_aligned = []
        y_hexa_aligned = []        

        for sample, x_hexa, y_hexa, th_hex in zip(sample_list, x_hexa_list, y_hexa_list, th_hexa_list):  # loop over samples on bar
            yield from bps.mv(stage.th, th_hex)        
            yield from bps.mv(stage.x, x_hexa)
            yield from bps.mv(stage.y, y_hexa)
            yield from alignement_gisaxs_hex(angle=0.1, rough_y=0.5, flag_reflection = 1)

            th_hexa_aligned = th_hexa_aligned + [stage.th.position]
            y_hexa_aligned = y_hexa_aligned + [stage.y.position]  

    print(y_hexa_aligned)
    print(th_hexa_aligned)

    ## Measure
    det_exposure_time(t, t)
    if t0 is None:
        t0 = time.time()
    for nn in range(Nmax):
        for sample, x_hexa, th_hexa, y_hexa in zip(sample_list, x_hexa_list, th_hexa_aligned, y_hexa_aligned):
            xr_list = [0]
            if np.mod(nn, 5)==0:
                xr_list = [0, 0.4]
            if np.mod(nn, 10)==0:
                xr_list = [-0.4, 0, 0.4]

            for xr in xr_list:
                yield from bps.mv(stage.x, x_hexa+xr)
                yield from bps.mv(stage.y, y_hexa)

                incident_angles = [0.08, 0.12, 0.16, 0.2, 0.3, 0.5]
                #incident_angles = [0.5]
                th_real = np.array(incident_angles)  # incident angles
                th_meas = (  ## Stage positions
                    th_real + th_hexa
                )  
                
                for waxs_angle in waxs_angles:  # loop through waxs angles
                    yield from bps.mv(waxs, waxs_angle)
                    if waxs_angle >= 15:
                        dets = [pil900KW, pil1M] 
                    else:
                        dets = [pil900KW] 

                    for i, th in enumerate(th_meas):  # loop over incident angles
                        yield from bps.mv(stage.th, th)

                        humidity = "%3.2f" % readHumidity(verbosity=0)
                        sample_name = "{sample}_n{nn}_t{time:05.0f}s_{th:5.4f}deg_waxs{waxs_angle:05.2f}_x{x:05.1f}_{t}s".format(
                            sample=sample,
                            nn=nn+n0,
                            time = time.time()-t0,
                            th=th_real[i],
                            waxs_angle=waxs_angle,
                            x=x_hexa+xr,
                            t=t,
                        )
                        sample_id(user_name='Insitu', sample_name=sample_name)
                        print(f"\n\t=== Sample: {sample_name} ===\n")
                        yield from bp.count(dets, num=1)

        if (time.time()-t0) < time_hr[0]*3600:
            print("\nnn={}, time {:.0f}min; Time range 1: sleeping for {}s".format(nn+n0, (time.time()-t0)/60, time_sleep_sec[0]))
            time.sleep(time_sleep_sec[0])

        elif (time.time()-t0) < time_hr[1]*3600:
            print("\nnn={}, time {:.0f}min; Time range 2: sleeping for {}s".format(nn+n0, (time.time()-t0)/60, time_sleep_sec[1]))
            time.sleep(time_sleep_sec[1])

        else:
            print("\nnn={}, time {:.0f}min; Time range 3: sleeping for {}s".format(nn+n0, (time.time()-t0)/60, time_sleep_sec[2]))
            time.sleep(time_sleep_sec[2])


    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)

####
# Put in new bar
# t0 = time.time()
# REhopen())
#
# Move HEX x to new sample alignment spot (substrate only)
# RE(alignRE(alignement_gisaxs_hex(angle=0.1, rough_y=0.5, flag_reflection RE(alignement_gisaxs_hex(angle=0.1, rough_y=0.5, flag_reflection = 1))= 1))ement_gisaxs_hex(angle=0.1, rough_y=0.5, flag_reflection RE(alignement_gisaxs_hex(angle=0.1, rough_y=0.5, flagRE(alignRE(alignement_gisaxs_hex(angle=0.1, rough_y=0.5, flag_reflection RE(alignement_gisaxs_hex(angle=0.1, rough_y=0.5, flag_reflection = 1))= 1))ement_gisaxs_hex(angle=0.1, rough_y=0.5, flag_reflection RE(alignement_gisaxs_hex(angle=0.1, rough_y=0.5, flag_reflection = 1))= 1))_reflection = 1))= 1))
# Note down all the y, th positions
# Note down x (measurement positions), choose option 1 or not
#
# %run -i /home/xf12id/.ipython/profile_collection/startup/users/30-user-Joneun -i /home/xf12id/.ipythons.py
#
# RE(run_gi_humid_new(t=1, t0=t0, n0=0, time_hr = [3, 5], time_sleep_sec = [600, 20, RE(run_gi_humid_new(t=1, t0=t0, n0=0, time_hr = [3, 5], time_sleep_sec = [600, 20, 1200], Nmax=999))1200], Nmax=999))
# RE(shclose())
#
# ctrl+C, RE.abort()
# (normally not needed) bsuicR
#
# (test only) RE(run_gi_humid_new(t=1, n0=0, time_hr = [0.1, 0.2], time_sleep_sec = [3, 5, 6], Nmax=999))
def run_gi_humid_new(t=0.5, t0=0, user_name='Insitu', time_hr = [2], time_sleep_sec = [3600, 600], xr_list=[0.3], n0=0, Nmax=999):
    if t0==None:
        t0 = time.time()
   
    sample_list = [
        "ZC_dynamic11",
        "ZC_dynamic12",
        "ZC_dynamic13",
        "ZC_dynamic14",
        "ZC_dynamic15"
    ]
    if 1:     
        x_hexa_list = [-21.3, -14.5, -5.8, 2.7, 9.2] 
        y_hexa_aligned = [-6.545, -6.568, -6.578, -6.625, -6.605]       
        th_hexa_aligned = [1.846, 1.855, 1.851, 1.871, 1.858]  

    #th_real = np.array([0.12, 0.16, 0.2])  # incident angles
    th_real = np.array([0.16])  # incident angles
     
    print(x_hexa_list)
    print(y_hexa_aligned)
    print(th_hexa_aligned)

    waxs_angles = np.array([15])

    ## Measure
    det_exposure_time(t, t)
    for nn in range(Nmax):
        for sample, x_hexa, th_hexa, y_hexa in zip(sample_list, x_hexa_list, th_hexa_aligned, y_hexa_aligned):
           
            flag_option1 = True #False, CHANGE THIS

            # ### OPTION 1
            # if flag_option1:  
            #     xr_list = [-0.75 + np.mod(nn, 6)*0.3]
            #     ypos_list = [y_hexa]
            #     if np.mod(nn, 6)==0:
            #         xr_list.append(0)
            #         ypos_list.append(y_hexa-0.2)
                        
            # ### OPTION 2 
            # else:
                # xr_list = [-0.3 + np.mod(nn, 3)*0.3]
                # ypos_list = [y_hexa - 0.2*np.mod(np.floor(nn/3), 2)]
            #xr_list = [0]
            ypos_list = [y_hexa]  


            th_meas = (  ## Stage positions
                th_real + th_hexa
            )   
                        
            for xr, ypos in zip(xr_list, ypos_list): 
                yield from bps.mv(stage.x, x_hexa+xr)                
                yield from bps.mv(stage.y, ypos) 
                    
                for waxs_angle in waxs_angles:  # loop through waxs angles
                    #yield from bps.mv(waxs, waxs_angle)

                    if waxs_angle >= 15:
                        dets = [pil900KW, pil1M] 
                    else:
                        dets = [pil900KW] 

                    for i, th in enumerate(th_meas):  # loop over incident angles
                        yield from bps.mv(stage.th, th)

                        sample_name = "{sample}_n{nn}_t{time:05.0f}s_{th:5.4f}deg_waxs{waxs_angle:05.2f}_x{x:06.2f}_y{y:06.2f}_{t}s".format(
                            sample=sample,
                            nn=nn+n0,
                            time = time.time()-t0,
                            th=th_real[i],
                            waxs_angle=waxs_angle,
                            x=x_hexa+xr,
                            y=ypos,
                            t=t,
                        )
                        sample_id(user_name=user_name, sample_name=sample_name)
                        print(f"\n\t=== Sample: {sample_name} ===\n")
                        yield from bp.count(dets, num=1)

        if (time.time()-t0) < time_hr[0]*3600:
            print("\nnn={}, time {:.0f}min; Time range 1: sleeping for {}s".format(nn+n0, (time.time()-t0)/60, time_sleep_sec[0]))
            #time.sleep(time_sleep_sec[0])
            yield from bps.sleep(time_sleep_sec[0])

        elif (time.time()-t0) < time_hr[1]*3600:
            print("\nnn={}, time {:.0f}min; Time range 2: sleeping for {}s".format(nn+n0, (time.time()-t0)/60, time_sleep_sec[1]))
            yield from bps.sleep(time_sleep_sec[1])

        else:
            print("\nnn={}, time {:.0f}min; Time range 3: sleeping for {}s".format(nn+n0, (time.time()-t0)/60, time_sleep_sec[2]))
            yield from bps.sleep(time_sleep_sec[2])

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)


# RE(run_gi_humid_testexp(t_list = [0.5, 1, 2, 3, 5], xr_list=[-0.4], n0=41, Nmax=1, incident_angles = [0.08, 0.5]))
def run_gi_humid_testexp(t_list = [0.5, 1, 2, 3, 5], xr_list=[-0.4], n0=41, Nmax=1, incident_angles = [0.08, 0.5]):

    sample_list = [
        "ZC_dynamic2",
    ]

    waxs_angles = np.array(
        [15]
    )

    if 1:
        x_hexa_list = [8.8]  
        y_hexa_aligned = [3.43]     
        th_hexa_aligned = [2.493]

    print(y_hexa_aligned)
    print(th_hexa_aligned)

    ## Measure
    for t in t_list:
        det_exposure_time(t, t)
        for sample, x_hexa, th_hexa, y_hexa in zip(sample_list, x_hexa_list, th_hexa_aligned, y_hexa_aligned):
            yield from bps.mv(stage.y, y_hexa)

            for xr in xr_list:
                yield from bps.mv(stage.x, x_hexa+xr)

                th_real = np.array(incident_angles)  # incident angles
                th_meas = (  ## Stage positions
                    th_real + th_hexa
                )  
                
                for waxs_angle in waxs_angles:  # loop through waxs angles

                    yield from bps.mv(waxs, waxs_angle)
                    if waxs_angle >= 15:
                        dets = [pil900KW, pil1M] 
                    else:
                        dets = [pil900KW] 

                    for i, th in enumerate(th_meas):  # loop over incident angles
                        yield from bps.mv(stage.th, th)

                        humidity = "%3.2f" % readHumidity(verbosity=0)
                        sample_name = "{sample}_n{nn}_{th:5.4f}deg_waxs{waxs_angle:05.2f}_x{x:05.1f}_{t}s".format(
                            sample=sample,
                            nn=n0,
                            #time = time.time()-t0,
                            th=th_real[i],
                            waxs_angle=waxs_angle,
                            x=x_hexa+xr,
                            t=t,
                        )
                        sample_id(user_name='Insitu', sample_name=sample_name)
                        print(f"\n\t=== Sample: {sample_name} ===\n")
                        for nn in range(Nmax):
                            yield from bp.count(dets, num=1)


    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)





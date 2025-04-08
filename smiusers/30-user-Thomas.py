# 2023-May-22 Mon
# 16.1 keV, 25um*5um beam, Transmission Linkam with LN2, vac
# proposal_id("2023_2", "312283_Subramanian", analysis=True)
# RE.md['SAF_number'] = 311336
# RE.md['SAXS_setup'] = {'sdd': 9200, 'beam_centre': [395, 558], 'bs': 'rod', 'energy': 16100}
# 
# RE(rel_scan([pil1M], stage.y, -2, 2, 15)); ps()
# ---------------------------------------------------------------
# ---------------------------------------------------------------
# *Auto Evac (click), wait until in vac, yellow turns green, open valves before and after WAXS chamber, 
# Search hutch and close
# RE(shopen())
# Start det3: ctrl+x twice
# type: setthreshold energy 16100 autog 11000
#
# # Ctrl+s to save this file
# %run -i /home/xf12id/.ipython/profile_collection/startup/users/30-user-Thomas.py
#
# Ctrl+c once/twice; RE.abort()
# bsui
# %run -i /home/xf12id/.ipython/profile_collection/startup/users/30-user-Thomas.py
#
# RE(shclose())
# To take out sample: wait for sample to go back to RT
# *Auto Bleed to air (click), open WAXS soft vent, 6.5e2
# ---------------------------------------------------------------
# Note: Linkam Transmission, HEXAPOD around x=-9.3, y=1, z=-7.257
# beamstop_save()

def move_waxs(waxs_angle=20):
    yield from bps.mv(waxs, waxs_angle)

    
# 2023-May
# Measures at 0, 15 waxs detector angles; Take both SAXS and WAXS
# RE(run_measure1(t=0.5, user_name='VS', sam_name='PS-PDMS_5033_run1'))
def run_measure1(t=0.5, user_name='VS', sam_name='PS-PDMS_5033'):
    det_exposure_time(t, t)
    t0 = time.time()
    waxs_angles = np.array([0, 15]) ## Takes about 30sec to move

    for waxs_angle in waxs_angles:  # loop through waxs angles
        yield from bps.mv(waxs, waxs_angle)
        if waxs_angle >= 15: # WAXS, SAXS
            dets = [pil900KW, pil1M]
        else:                # WAXS
            dets = [pil900KW]

        x = stage.x.position
        y = stage.y.position
        temp = ls.input_A_celsius.get()  # ls.ch1_read.value

        name_fmt = "{sample}_16.1keV_9.2m_{temperature}C_waxs{waxs_angle:05.2f}_x{x:05.3f}_y{y:05.3f}_{t:05.2f}s"
        sample_name = name_fmt.format(
            sample=sam_name,
            temperature="%1.1f" % temp,
            waxs_angle=waxs_angle,
            x=x,
            y=y,
            t=t,
        )
        print(f"\n\t=== Sample: {sample_name} ===\n")
        sample_id(user_name=user_name, sample_name=sample_name)
        yield from bp.count(dets, num=1)

    print('Took {}s'.format(time.time()-t0))

# For Isothermal
# RE(run_isothermal(t=0.5, Nmax=1000, user_name='VS', sam_name='PS-PDMS_5033_run1', time_sleep_sec=5, y_step=0.002))
def run_isothermal(t=0.5, Nmax=1000, user_name='VS', sam_name='test', time_sleep_sec=10, y_step=0.002):
    det_exposure_time(t, t)
    waxs_angle = 15
    yield from bps.mv(waxs, waxs_angle)
    dets = [pil900KW, pil1M]

    for nn in range(Nmax):
        yield from bps.mvr(stage.y, y_step)
        x = stage.x.position
        y = stage.y.position
        temp = ls.input_A_celsius.get()  # ls.ch1_read.value

        name_fmt = "{sample}_16.1keV_9.2m_{temperature}C_waxs{waxs_angle:05.2f}_x{x:05.3f}_y{y:05.3f}_{t:05.2f}s"
        sample_name = name_fmt.format(
            sample=sam_name,
            temperature="%1.1f" % temp,
            waxs_angle=waxs_angle,
            x=x,
            y=y,
            t=t,
        )
        print(f"\n\t=== Sample: {sample_name} ===\n")
        sample_id(user_name=user_name, sample_name=sample_name)
        yield from bp.count(dets, num=1)

        print("\nnn={}; Sleeping for {}s".format(nn, time_sleep_sec))
        time.sleep(time_sleep_sec)


# Need to select det & specify WAXs angle
# SAXS: RE(run_test(t=0.5, dets = [pil1M], waxs_angle=15, user_name='test', sam_name='test'))
# WAXS: RE(run_test(t=0.5, dets = [pil900KW], waxs_angle=0, user_name='test', sam_name='test'))
def run_test(t=0.5, dets = [pil1M], waxs_angle=15, user_name='VS', sam_name='test'):
    det_exposure_time(t, t)
    yield from bps.mv(waxs, waxs_angle)
    x = stage.x.position
    y = stage.y.position
    temp = ls.input_A_celsius.get()  # ls.ch1_read.value

    name_fmt = "{sample}_16.1keV_9.2m_{temperature}C_waxs{waxs_angle:05.2f}_x{x:05.3f}_y{y:05.3f}_{t:05.2f}s"
    sample_name = name_fmt.format(
        sample=sam_name,
        temperature="%1.1f" % temp,
        waxs_angle=waxs_angle,
        x=x,
        y=y,
        t=t,
    )
    print(f"\n\t=== Sample: {sample_name} ===\n")
    sample_id(user_name=user_name, sample_name=sample_name)
    yield from bp.count(dets, num=1)





"""
8.3m
  smi_config_update = smi_config.append(current_config_DF, ignore_index=True)
1.248555 1.248555 -13.000182 0.0 8.649654
"""

# 2021-Jul-11
# RE(run_Thomas_temp2(t=0.5, name='VS', samples=['test'], Nmax=1, time_sleep_sec=0))
# RE(run_Thomas_temp2(t=0.5, name='VS', samples=['PS-PDMS_5033'], Nmax=1, time_sleep_sec=0, time_interval_sec=0))

def run_Thomas_temp2(
    t=0.5,
    name="VS",
    samples=["thermal_test"],
    Nmax=1,
    time_sleep_sec=120,
    time_interval_sec=10,
):
    # Slowest cycle:
    #x_list = [-2.6]  # [-3.4] #[-3.5] #HEXAPOD
    #y_list = [2.3]  # [2.3] #[2.25]
    # samples = ['thermal1']

    # 2023-May
    x_list = [-8.6]  
    y_list = [0.81]  #z=-7.257

    # Detectors, motors:
    dets = [pil900KW, pil1M]

    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    det_exposure_time(t, t)

    t0 = time.time()

    waxs_angles = np.array([0, 15])

    # time.sleep(time_sleep_sec)
    yield from bps.sleep(time_sleep_sec)

    for waxs_angle in waxs_angles:  # loop through waxs angles
        yield from bps.mv(waxs, waxs_angle)
        if waxs_angle >= 15:
            dets = [pil900KW, pil1M, pil300KW]
        else:
            dets = [pil900KW, pil300KW]
        print("Meausre saxs and/or waxs here for w-angle=%s" % waxs_angle)

        for i in range(Nmax):
            t1 = time.time()
            temp = ls.input_A_celsius.get()  # ls.ch1_read.value
            for x, y, names in zip(x_list, y_list, samples):
                yield from bps.mv(stage.x, x)  # HEXAPOD
                yield from bps.mv(stage.y, y)

                #name_fmt = "{sample}_16.1keV_8.3m_{time}s_{temperature}C_waxs{waxs_angle:05.2f}_x{x:04.2f}_y{y:04.2f}_{scan_id}"
                name_fmt = "{sample}_16.1keV_9.2m_{time}s_{temperature}C_waxs{waxs_angle:05.2f}_x{x:04.2f}_y{y:04.2f}_{scan_id}"
                sample_name = name_fmt.format(
                    sample=names,
                    time="%1.1f" % (t1 - t0),
                    temperature="%1.1f" % temp,
                    waxs_angle=waxs_angle,
                    x=x,
                    y=y,
                    scan_id=RE.md["scan_id"],
                )

                # xss = np.linspace(x - 500, x + 500, 3)
                # yss = np.linspace(y - 300, y + 300, 3)
                # yss, xss = np.meshgrid(yss, xss)
                # yss = yss.ravel()
                # xss = xss.ravel()

                print(f"\n\t=== Sample: {sample_name} ===\n")
                sample_id(user_name=name, sample_name=sample_name)
                yield from bp.count(dets, num=1)

            yield from bps.sleep(time_interval_sec)

            # time.sleep(time_sleep_sec)

    sample_id(user_name="test", sample_name="test")


# 2023-May-22 Static transmission
# RE(run_tswaxs_single(t=10, user_name='StaticT', sam_name='VS_sam1', waxs_angles = [0]))
def run_tswaxs_single(t=10, user_name='StaticT', sam_name='PS-PDMS', waxs_angles = [0], grid=0, Nmax=1):
    # 59000 (sample1),-44000 (AgBH)

    det_exposure_time(t, t)

    t0 = time.time()
    #waxs_angles = np.array([15, 0])

    for waxs_angle in waxs_angles:  # loop through waxs angles
        yield from bps.mv(waxs, waxs_angle)
        if waxs_angle >= 15:
            dets = [pil900KW, pil1M] #, pil300KW]
        else:
            dets = [pil900KW] #, pil300KW]
        print("Meausre saxs and/or waxs here for w-angle=%s" % waxs_angle)

        for i in range(Nmax):
            x = piezo.x.position
            y = piezo.y.position

            name_fmt = "{sample}_16.1keV_9.2m_waxs{waxs_angle:05.2f}_x{x:04.2f}_y{y:04.2f}_{t:05.2f}s"
            sample_name = name_fmt.format(
                sample=sam_name,
                waxs_angle=waxs_angle,
                x=x,
                y=y,
                t=t,
                #scan_id=RE.md["scan_id"],
            )

            print(f"\n\t=== Sample: {sample_name} ===\n")
            sample_id(user_name=user_name, sample_name=sample_name)

            if grid == 0:
                yield from bp.count(dets, num=1)
            else:
                xss = np.linspace(x - 300, x + 300, 3)
                yss = np.linspace(y - 300, y + 300, 3)
                yss, xss = np.meshgrid(yss, xss)
                yss = yss.ravel()
                xss = xss.ravel()
                yield from bp.list_scan(
                    dets, piezo.x, xss.tolist(), piezo.y, yss.tolist()
                )

    sample_id(user_name="test", sample_name="test")



# RE(run_tswaxs(t=2, name = 'T', waxs_angles = [15]))
def run_tswaxs(t=10, name="T", grid=0, Nmax=1):
    # 59000 (sample1),-44000 (AgBH)
    
    # x_list = [-31430, -18430, 1570, 9570, 23570, 33570, 37370, 43170]
    # y_list = [-2900, -2900, -2900, -2900, -2900, -2900, -2900, -2800]  
    # samples = ["KL13", "KL12", "KL1", "KL2", "KL3","KL4", "KL5", "Kapton2"]
    x_list = [42120]
    y_list = [-8000]
    samples = ['Kapton3']
    # # HEX: -3.41, y 1.67, z-1.4
    # sam6: x-7830, y -10950, z7500
    # x_list = [-3000, 4000, 10000, 17000, 23000, 32100, 39100]
    # y_list = [-5000, -4500, -5000, -5500, -5500, -5500, -5500]  #-5800
    # samples = ["HE_s1_S2VP_Bulk_Pristine_Trans", "HE_s2_S2VP_Bulk_LiTFSI_Trans", 
    #            "HE_s3_S2VP_Bulk_EIMTFSI_Trans","HE_s4_SnBA_Bulk_66",
    #            "HE_s5_SnBA_Bulk_16", "HE_s6_SnBA_Sphere_66",
    #            "HE_s7_SnBA_Sphere_16"]
    # x_list = [-43000, -43000, -37250, -31260, -24270, -18330]
    # y_list = [-2500, -3300, -2750, -2900, -2900, -2900]  #-5800
    # samples = ["KL7a", "KL7b", "KL8", "KL9", "KL10", "KL11"]  


    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    det_exposure_time(t, t)

    t0 = time.time()
    waxs_angles = np.array([0])

    for waxs_angle in waxs_angles:  # loop through waxs angles
        yield from bps.mv(waxs, waxs_angle)
        if waxs_angle >= 15:
            dets = [pil900KW, pil1M] #, pil300KW]
        else:
            dets = [pil900KW] #, pil300KW]
        print("Meausre saxs and/or waxs here for w-angle=%s" % waxs_angle)

        for i in range(Nmax):
            t1 = time.time()
            # temp = ls.input_A_celsius.get() #ls.ch1_read.value
            for x, y, names in zip(x_list, y_list, samples):
                yield from bps.mv(piezo.x, x)
                yield from bps.mv(piezo.y, y)

                name_fmt = "{sample}_16.1keV_8.3m_waxs{waxs_angle:05.2f}_x{x:04.2f}_y{y:04.2f}_{t:05.2f}s"
                sample_name = name_fmt.format(
                    sample=names,
                    waxs_angle=waxs_angle,
                    x=x,
                    y=y,
                    t=t,
                    #scan_id=RE.md["scan_id"],
                )

                print(f"\n\t=== Sample: {sample_name} ===\n")
                sample_id(user_name=name, sample_name=sample_name)

                if grid == 0:
                    yield from bp.count(dets, num=1)
                else:
                    xss = np.linspace(x - 300, x + 300, 3)
                    yss = np.linspace(y - 300, y + 300, 3)
                    yss, xss = np.meshgrid(yss, xss)
                    yss = yss.ravel()
                    xss = xss.ravel()
                    yield from bp.list_scan(
                        dets, piezo.x, xss.tolist(), piezo.y, yss.tolist()
                    )

    sample_id(user_name="test", sample_name="test")




# RE(run_giswaxs(t=0.5))
def run_giswaxs(t=0.5, flag_align=1, flag_reflect=1, piezo_y_init=7200):

    # x_list = [50000, 40000, 28000, 14000, -4000,    -24000]
    # sample_list = ['WS1', 'WS2', 'WS3', 'WS4','WS5',    'sam17']
    #yield from bps.mv(piezo.y, 1800)

    ### 2023-May-22, 
    # HEXAPOD x=-9, y=0, z=4; bsx 3.65-3.45; (was 2.65)
    #   smi_config_update = smi_config.append(current_config_DF, ignore_index=True)
    # 3.649785 3.649785 13.000338 0.000234 9.799842
    #x_list =  [59000] #, 47000, 39000, 28000, 15000, 3000, -15000]
    #sample_list = ["HE_sam1-1"] #,"HE_sam1-2","HE_sam1-3","HE_sam2-1","HE_sam2-2","HE_sam2-3", "KS_sam1"]
    #x_list = [-48000, -36000, -14000, 7000, 22000, 35000]
    #sample_list = ["HE_s1_Bulk_S2VP_Pristine","HE_s2_Bulk_S2VP_LiTFSI","HE_s3_Bulk_S2VP_EIMTFSI","HE_s4_Film_S2VP_Pristine","HE_s5_Film_S2VP_LiTFSI","HE_s6_Film_S2VP_EIMTFSI"] 
    x_list = [-14000+400]
    sample_list = ["HE_s3_Bulk_S2VP_EIMTFSI"] 
 
    ##### HE_sam1-1, x = 58999.955, aligned at y = 4687.467, theta = 0.126291

    assert len(x_list) == len(sample_list), f"Sample name/position list is borked"

    # angle_arc = np.array([0.1, 0.15, 0.19]) # incident angles
    angle_arc = np.array([0.12, 0.16, 0.2])  # incident angles
    # waxs_angle_array = np.linspace(0, 84, 15)

    waxs_angles = np.array(
        [20]
    )  # q=4*3.14/0.77*np.sin((max angle+3.5)/2*3.14159/180)
    
    data_dir = '/nsls2/data/smi/legacy/results/data/2024_1/312283_Subramanian/'

    # x_shift_array = np.linspace(-500, 500, 3) # measure at a few x positions
    aligned_positions = []
    for x, sample in zip(x_list, sample_list):  # loop over samples on bar

        yield from bps.mv(piezo.x, x)  # move to next sample
        if flag_align:
            yield from bps.mv(piezo.y, piezo_y_init) 
            yield from alignement_gisaxs(0.1, flag_reflect=flag_reflect)  # run alignment routine

        print('##### {}, x = {}, aligned at y = {}, theta = {}'.format(sample, piezo.x.position, piezo.y.position, piezo.th.position))
        aligned_positions.append([sample, piezo.x.position, piezo.y.position, piezo.th.position])
        with open(data_dir+'Align/aligned_positions.txt', 'a') as f:
            note = '{}: x{}, y{}, th{},'.format(sample, piezo.x.position, piezo.y.position, piezo.th.position)
            f.write(note)
            f.write('\n')

        th_meas = (
            angle_arc + piezo.th.position
        )  # np.array([0.10 + piezo.th.position, 0.20 + piezo.th.position])
        th_real = angle_arc

        det_exposure_time(t, t)
        x_pos_array = x  # + x_shift_array

        for waxs_angle in waxs_angles:  # loop through waxs angles

            yield from bps.mv(waxs, waxs_angle)
            if waxs_angle >= 15:
                dets = [pil900KW, pil1M] #, pil300KW]
            else:
                dets = [pil900KW] #, pil300KW]

            for i, th in enumerate(th_meas):  # loop over incident angles
                yield from bps.mv(piezo.th, th)

                sample_name = "{sample}_{th:5.4f}deg_waxs{waxs_angle:05.2f}_ssd9200_x{x}_{t}s".format(
                    sample=sample,
                    th=th_real[i],
                    waxs_angle=waxs_angle,
                    x=x,
                    t=t,
                    #scan_id=RE.md["scan_id"],
                )
                # name_fmt = '{sample}_16.1keV_8.3m_waxs{waxs_angle:05.2f}_x{x:04.2f}_{t:05.2f}s_{scan_id}'
                # sample_name = name_fmt.format(sample=sample, waxs_angle=waxs_angle, x=x, t=t, scan_id=RE.md['scan_id'])
                sample_id(user_name="Static", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")

                # yield from bp.scan(dets, energy, e, e, 1)
                # yield from bp.scan(dets, waxs, *waxs_arc)
                yield from bp.count(dets, num=1)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5)


########################################
# 2021
def run_Thomas_temp(t=1, name="HarvPoly"):
    # Slowest cycle:
    x_list = [13300, -12100]
    y_list = [-3400, -3400]
    samples = ["thermal1", "thermal2"]

    # Detectors, motors:
    dets = [pil1M]

    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    det_exposure_time(t, t)

    t0 = time.time()
    for i in range(2000):
        t1 = time.time()
        temp = ls.ch1_read.value
        for x, y, names in zip(x_list, y_list, samples):
            yield from bps.mv(piezo.x, x)
            yield from bps.mv(piezo.y, y)

            name_fmt = "{sample}_11.15keV_7.5m_{time}s_{temperature}C_{i}"
            sample_name = name_fmt.format(
                sample=names,
                time="%1.1f" % (t1 - t0),
                temperature="%1.1f" % temp,
                i="%3.3d" % i,
            )

            xss = np.linspace(x - 500, x + 500, 3)
            yss = np.linspace(y - 300, y + 300, 3)
            yss, xss = np.meshgrid(yss, xss)
            yss = yss.ravel()
            xss = xss.ravel()

            print(f"\n\t=== Sample: {sample_name} ===\n")
            sample_id(user_name=name, sample_name=sample_name)
            yield from bp.list_scan(dets, piezo.x, xss.tolist(), piezo.y, yss.tolist())

        time.sleep(1800)

    sample_id(user_name="test", sample_name="test")


def saxs_cryo(t=0.5, tem=25, num_max=100):
    global num
    # Slowest cycle:
    name = "ET"
    # Detectors, motors:
    dets = [pil300KW, pil1M]
    # sample = 'PDMS_sdd8.3m'
    sample = "bkg_sdd8.3m"

    waxs_range = np.linspace(0, 13, 3)

    det_exposure_time(t, t)

    while num < num_max:
        yield from bps.mvr(stage.y, 0.02)
        num += 1
        if waxs.arc.position > 7:
            waxs_ran = waxs_range[::-1]
        else:
            waxs_ran = waxs_range

        for wa in waxs_ran:
            yield from bps.mv(waxs, wa)
            name_fmt = "num{nu}_{temperature}C_wa{wa}"
            sample_name = name_fmt.format(nu=num, temperature="%4.2f" % tem, wa=wa)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            sample_id(user_name=sample, sample_name=sample_name)

            yield from bp.count(dets, num=1)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def gisaxs_Thomas(t=1):
    samples = ["T1_A", "T1_B", "T2_A", "T2_B"]
    x_list = [58500, 49000, 39000, 28000]

    waxs_arc = np.linspace(0, 13, 3)
    angle = [0.12, 0.16, 0.2]

    # Detectors, motors:
    dets = [pil1M, pil300KW]
    det_exposure_time(t, t)

    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"

    for x, sample in zip(x_list, samples):
        yield from bps.mv(piezo.x, x)

        sample_id(user_name="NT", sample_name=sample)

        yield from alignement_gisaxs(0.08)

        ai0 = piezo.th.position
        det_exposure_time(t, t)
        name_fmt = "{sample}_ai{angle}deg_wa{waxs}_pos{pos}"
        for j, wa in enumerate(waxs_arc[::-1]):
            yield from bps.mv(waxs, wa)

            for nu, num in enumerate([0, 1, 2, 3, 4]):
                yield from bps.mv(piezo.x, x - nu * 300)

                for an in angle:
                    yield from bps.mv(piezo.th, ai0 + an)
                    sample_name = name_fmt.format(
                        sample=sample, angle="%3.2f" % an, waxs="%2.1f" % wa, pos=nu
                    )
                    sample_id(user_name="PT", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")

                    yield from bp.count(dets, num=1)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.1, 0.1)


def waxs_Thomas(t=1, x_off=0, user="NT"):
    samples = [
        "sample01",
        "sample02",
        "sample03",
        "sample04",
        "sample05",
        "sample06",
        "sample07",
        "sample08",
        "sample09",
        "sample10",
        "sample11",
        "sample12",
        "sample13",
        "sample14",
        "sample15",
        "sample16",
        "sample17",
        "sample18",
        "sample19",
        "sample20",
        "sample21",
        "sample22",
        "sample23",
        "sample24",
        "sample25",
        "sample26",
        "sample27",
        "sample28",
        "sample29",
        "sample30",
        "sample31",
        "sample32",
        "sample33",
        "sample34",
        "sample35",
        "sample36",
        "sample37",
        "sample38",
        "sample39",
        "sample40",
        "sample41",
    ]
    x_list = [
        44700,
        41700,
        37700,
        32000,
        28000,
        21000,
        15000,
        10000,
        5800,
        2500,
        -1500,
        -4500,
        -6900,
        -11900,
        -16500,
        -19800,
        -23800,
        -27800,
        -33800,
        -37800,
        -41800,
        45000,
        41000,
        38000,
        33000,
        31000,
        27000,
        22500,
        20000,
        17500,
        15000,
        11000,
        8000,
        4500,
        1500,
        -1500,
        -4500,
        -9500,
        -13500,
        -17500,
        -21500,
    ]
    y_list = [
        -7800,
        -7800,
        -7800,
        -7800,
        -7800,
        -7700,
        -7700,
        -7600,
        -7400,
        -7400,
        -7400,
        -7400,
        -7400,
        -7400,
        -7400,
        -7400,
        -7400,
        -7400,
        -7400,
        -7400,
        -7400,
        3000,
        3000,
        3000,
        3000,
        3000,
        3000,
        3000,
        3200,
        3200,
        3200,
        3200,
        3200,
        3200,
        3200,
        3700,
        3400,
        3400,
        3400,
        3400,
        3500,
    ]
    z_list = [
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
    ]

    assert len(samples) == len(
        x_list
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    assert len(samples) == len(
        y_list
    ), f"Number of X coordinates ({len(y_list)}) is different from number of samples ({len(samples)})"
    assert len(samples) == len(
        z_list
    ), f"Number of X coordinates ({len(z_list)}) is different from number of samples ({len(samples)})"

    waxs_arc = np.linspace(0, 13, 3)

    # Detectors, motors:
    dets = [pil1M, pil300KW]
    det_exposure_time(t, t)

    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"

    for j, wa in enumerate(waxs_arc[::-1]):
        yield from bps.mv(waxs, wa)

        for x, y, z, sample in zip(x_list, y_list, z_list, samples):
            yield from bps.mv(piezo.x, x + x_off)
            yield from bps.mv(piezo.y, y)
            yield from bps.mv(piezo.z, z)

            det_exposure_time(t, t)
            name_fmt = "{sample}_wa{waxs}_pos{pos}"

            for nu, num in enumerate([0, 1, 2, 3, 4]):
                yield from bps.mv(piezo.y, y + nu * 50)

                sample_name = name_fmt.format(sample=sample, waxs="%2.1f" % wa, pos=nu)
                sample_id(user_name=user, sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")

                yield from bp.count(dets, num=1)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.1, 0.1)


def run_Thomas(t=1, x_off=0):
    yield from waxs_Thomas(t=0.5, x_off=-500, user="NT_pos2_0.5s")
    yield from waxs_Thomas(t=0.5, x_off=-250, user="NT_pos3_0.5s")
    yield from waxs_Thomas(t=0.5, x_off=250, user="NT_pos4_0.5s")


def saxs_cryo_2021_1(t=0.5, tem=25, num_max=100):
    global num
    # Slowest cycle:
    name = "ET"

    # Detectors, motors:
    dets = [pil300KW, pil1M]
    sample = "kapton"

    waxs_range = np.linspace(0, 13, 3)
    det_exposure_time(t, t)

    # while num < num_max:
    # yield from bps.mvr(stage.y, 0.02)
    num += 1
    if waxs.arc.position > 7:
        waxs_ran = waxs_range[::-1]
    else:
        waxs_ran = waxs_range

    for wa in waxs_ran:
        yield from bps.mv(waxs, wa)
        name_fmt = "num{nu}_{temperature}C_wa{wa}"
        sample_name = name_fmt.format(nu=num, temperature="%4.2f" % tem, wa=wa)
        print(f"\n\t=== Sample: {sample_name} ===\n")
        sample_id(user_name=sample, sample_name=sample_name)

        yield from bp.count(dets, num=1)

    yield from bps.mvr(stage.y, 0.02)
    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def saxs_2021_1(t=0.5, tem=25, num_max=100):
    global num
    # Slowest cycle:
    name = "ET"

    # Detectors, motors:
    dets = [pil1M]
    sample = "PS_PDMS_50.33dg_sdd8.3m_loop2"

    waxs_range = np.linspace(0, 13, 3)
    det_exposure_time(t, t)

    yield from bps.mv(waxs, 13.0)

    t0 = time.time()

    while num < 500:
        t1 = time.time()

        name_fmt = "num{nu}_{temperature}C_{time}s"
        sample_name = name_fmt.format(
            nu=num, temperature="%4.2f" % tem, time=np.round(t1 - t0)
        )
        print(f"\n\t=== Sample: {sample_name} ===\n")
        sample_id(user_name=sample, sample_name=sample_name)

        yield from bp.count(dets, num=1)
        yield from bps.sleep(30)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def waxs_2021_1(t=0.5, tem=25, num_max=1000):
    global num
    # Slowest cycle:
    name = "ET"

    # Detectors, motors:
    dets = [pil1M, pil300KW]
    sample = "PS_PDMS_50.33dg_sdd8.3m_isotherm"

    waxs_range = np.linspace(0, 13, 3)
    det_exposure_time(t, t)

    yield from bps.mv(waxs, 6.5)

    t0 = time.time()

    while num < num_max:
        t1 = time.time()

        name_fmt = "num{nu}_{temperature}C_{time}s"
        sample_name = name_fmt.format(
            nu=num, temperature="%4.2f" % tem, time=np.round(t1 - t0)
        )
        print(f"\n\t=== Sample: {sample_name} ===\n")
        sample_id(user_name=sample, sample_name=sample_name)

        yield from bp.count(dets, num=1)
        yield from bps.sleep(5)
        yield from bps.mvr(stage.y, 0.02)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def saxs_Thomas(t=1, x_off=0, user="NT"):
    samples = [
        "sample01",
        "sample02",
        "sample03",
        "sample04",
        "sample05",
        "sample06",
        "sample07",
        "sample08",
        "sample09",
        "sample10",
        "sample11",
        "sample12",
        "sample13",
        "sample14",
        "sample16",
        "sample17",
        "sample18",
        "sample19",
        "sample20",
        "sample21",
        "sample22",
        "sample23",
        "sample24",
        "sample25",
        "sample26",
        "sample27",
        "sample28",
        "sample29",
        "sample30",
        "sample31",
        "kapton_bkg",
    ]
    x_list = [
        46000,
        42000,
        38500,
        35000,
        31500,
        27500,
        23500,
        21000,
        16000,
        11000,
        5000,
        -500,
        -5000,
        -13000,
        45700,
        43700,
        41000,
        34000,
        29800,
        25800,
        22800,
        19800,
        17200,
        15200,
        12200,
        9000,
        2000,
        -4000,
        -7000,
        -10300,
        -13300,
    ]
    y_list = [
        -7600,
        -7600,
        -7600,
        -7600,
        -7600,
        -7600,
        -7600,
        -7600,
        -7600,
        -7600,
        -7600,
        -7600,
        -7600,
        -7600,
        5000,
        4500,
        5000,
        5000,
        5000,
        5000,
        5000,
        5000,
        5300,
        5300,
        5300,
        5300,
        4300,
        5400,
        5400,
        3800,
        3800,
    ]
    z_list = [
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
    ]

    assert len(samples) == len(
        x_list
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    assert len(samples) == len(
        y_list
    ), f"Number of X coordinates ({len(y_list)}) is different from number of samples ({len(samples)})"
    assert len(samples) == len(
        z_list
    ), f"Number of X coordinates ({len(z_list)}) is different from number of samples ({len(samples)})"

    xpos = [-500, 500, 5]

    # Detectors, motors:
    dets = [pil1M]
    det_exposure_time(t, t)

    for x, y, z, sample in zip(x_list, y_list, z_list, samples):
        yield from bps.mv(piezo.x, x + x_off)
        yield from bps.mv(piezo.y, y)
        yield from bps.mv(piezo.z, z)

        det_exposure_time(t, t)
        name_fmt = "{sample}_8.3m_16.1keV"

        sample_name = name_fmt.format(sample=sample)
        sample_id(user_name=user, sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")

        yield from bp.rel_scan(dets, piezo.x, *xpos)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.1, 0.1)


def rotscan_Thomas(t=1):
    samples = ["sample15_grid"]
    x_list = [-30600]
    y_list = [-9400]
    z_list = [1600]

    assert len(samples) == len(
        x_list
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    assert len(samples) == len(
        y_list
    ), f"Number of X coordinates ({len(y_list)}) is different from number of samples ({len(samples)})"
    assert len(samples) == len(
        z_list
    ), f"Number of X coordinates ({len(z_list)}) is different from number of samples ({len(samples)})"

    # Detectors, motors:
    dets = [pil1M]
    det_exposure_time(t, t)

    for x, y, z, sample in zip(x_list, y_list, z_list, samples):
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(piezo.y, y)
        yield from bps.mv(piezo.z, z)

        for i, prs_pos in enumerate(np.linspace(-65, 65, 131)):
            yield from bps.mv(prs, prs_pos)
            yield from bps.sleep(2)

            name_fmt = "{sample}_8.3m_16.1keV_num{num}_{prs}deg"

            sample_name = name_fmt.format(
                sample=sample, num="%3.3d" % prs_pos, prs="%3.1f" % prs_pos
            )
            sample_id(user_name="NT", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")

            y_r = [-200, 200, 3]
            x_r = [-500, 500, 3]
            yield from bp.rel_grid_scan(dets, piezo.y, *y_r, piezo.x, *x_r, 0)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.1, 0.1)

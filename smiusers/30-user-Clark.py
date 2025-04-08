import numpy as np
from cycler import cycler


def crazy_mapping(x_top, x_range, x_step, y_top, y_range, y_step, angle):
    x_all, y_all = [], []

    for num, y_coord in enumerate(np.linspace(y_top, y_top + y_range, y_step)):
        x_coord = x_top + (y_coord - y_top) * np.tan(np.deg2rad(angle))
        xs = np.linspace(x_coord, x_coord + x_range, x_step)
        ys = np.repeat(y_coord, len(xs))

        x_all = x_all + xs.tolist()
        y_all = y_all + ys.tolist()

    xall = [int(i) for i in x_all]
    yall = [int(i) for i in y_all]

    return xall, yall


def mapping2_waxs_ucol(t=1):
    waxs_range = [13, 6.5, 0]
    name = "NC"
    dets = [pil1M, pil300KW]
    det_exposure_time(t, t)

    # samples = ['GTAC_smcap']
    # x_list = [-30501]
    # y_list = [-2000]
    # x_range=[ [0, 0, 1]]
    # y_range=[ [0, 5000, 251]]

    samples = [
        "GTAC_SMcap_real",
        "cap_bag5",
        "cap_bag4",
        "Bag2_S2.4",
        "bag3_4d",
        "bag3_2d_part1",
        "bag3_2d_part2",
        "bag3_1d",
    ]
    x_list = [-23701, -18501, -10801, -45101, 11300, 30398, 36098, 48800]
    y_list = [-1000, -5700, -6900, -4700, -1900, -3100, -2800, -6900]
    x_range = [
        [0, 0, 1],
        [0, 0, 1],
        [0, 0, 1],
        [0, 4400, 45],
        [0, 2300, 24],
        [0, 2000, 21],
        [0, 2000, 21],
        [0, 5000, 51],
    ]
    y_range = [
        [0, 5000, 251],
        [0, 6000, 201],
        [0, 6000, 201],
        [0, 4000, 41],
        [0, 2800, 29],
        [0, 3300, 34],
        [0, 2600, 27],
        [0, 4500, 46],
    ]

    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    for x, y, sample, x_r, y_r in zip(x_list, y_list, samples, x_range, y_range):
        pil1M.cam.file_path.put(
            f"/nsls2/xf12id2/data/images/users/2020_2/305363_Clark2/1M/%s" % sample
        )
        pil300KW.cam.file_path.put(
            f"/nsls2/xf12id2/data/images/users/2020_2/305363_Clark2/300KW/%s" % sample
        )

        yield from bps.mv(piezo.x, x)
        yield from bps.mv(piezo.y, y)
        for wa in waxs_range:
            yield from bps.mv(waxs, wa)
            name_fmt = "{sam}_wa{waxs}"
            sample_name = name_fmt.format(sam=sample, waxs="%2.1f" % wa)
            sample_id(user_name=name, sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.rel_grid_scan(dets, piezo.y, *y_r, piezo.x, *x_r, 0)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def mapping1_waxs_ucol(t=1):
    waxs_range = [13, 6.5, 0]
    name = "NC"
    dets = [pil1M, pil300KW]
    det_exposure_time(t, t)
    """
    sample = 'Bag1_S2_inner'
    
    pil1M.cam.file_path.put(f"/ramdisk/images/users/2020_2/305363_Clark1/1M/%s"%sample)
    pil300KW.cam.file_path.put(f"/nsls2/xf12id2/data/images/users/2020_2/305363_Clark1/300KW/%s"%sample)

    samples = ['Bag1S2_in_midleft','Bag1S2_in_botleft', 'Bag1S2_in_bot', 'Bag1S2_in_midright',
    'Bag1S2_in_topright', 'Bag1S2_in_top']

    x_list = [10600, 9100, 9100, 10815, 17715, 17915, 14915]
    y_list = [-3300, -1300, 3700, 5300, 3000, 0, -3000]
    x_range= [1000, 1000, 1000, 5600, 1000, 1000, 1000]
    y_range= [2000, 5000, 1600, 1000, 2300, 3000, 3000]
    angles = [-45, 0, 47, 0, -47, 0, 45]

    assert len(x_list) == len(samples), f'Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})'
    for x, y, sample, x_r, y_r, angle in zip(x_list, y_list, samples, x_range, y_range, angles):       
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(piezo.y, y)

        x_all, y_all = crazy_mapping(x_top=x, x_range=x_r, x_step=20, y_top=y, y_range=y_r, y_step=20, angle=angle)

        for wa in waxs_range:
            yield from bps.mv(waxs, wa)
            name_fmt = '{sam}_wa{waxs}'
            sample_name = name_fmt.format(sam=sample, waxs='%2.1f'%wa)
            sample_id(user_name=name, sample_name=sample_name) 
            print(f'\n\t=== Sample: {sample_name} ===\n')
            traj1 = cycler(piezo.y, y_all)
            traj2 = cycler(piezo.x, x_all)
            traj = traj1+traj2
            yield from bp.scan_nd(dets, traj)

    """
    sample = "Bag1_S3"

    pil1M.cam.file_path.put(
        f"/ramdisk/images/users/2020_2/305363_Clark1/1M/%s" % sample
    )
    pil300KW.cam.file_path.put(
        f"/nsls2/xf12id2/data/images/users/2020_2/305363_Clark1/300KW/%s" % sample
    )

    samples = [
        "Bag1_S3_in_topleft",
        "Bag1_S3_in_midleft",
        "Bag1_S3_in_botleft",
        "Bag1_S3_in_bot",
        "Bag1_S3_in_botright",
        "Bag1_S3_in_midright",
        "Bag1_S3_in_topright",
    ]

    x_list = [10600, 9100, 9100, 10815, 17715, 17915, 14915]
    y_list = [-3300, -1300, 3700, 5300, 3000, 0, -3000]
    x_range = [1000, 1000, 1000, 5600, 1000, 1000, 1000]
    y_range = [2000, 5000, 1600, 1000, 2300, 3000, 3000]
    angles = [-45, 0, 47, 0, -47, 0, 45]

    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    for x, y, sample, x_r, y_r, angle in zip(
        x_list, y_list, samples, x_range, y_range, angles
    ):
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(piezo.y, y)

        x_all, y_all = crazy_mapping(
            x_top=x,
            x_range=x_r,
            x_step=15,
            y_top=y,
            y_range=y_r,
            y_step=15,
            angle=angle,
        )

        for wa in waxs_range:
            yield from bps.mv(waxs, wa)
            name_fmt = "{sam}_wa{waxs}"
            sample_name = name_fmt.format(sam=sample, waxs="%2.1f" % wa)
            sample_id(user_name=name, sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            traj1 = cycler(piezo.y, y_all)
            traj2 = cycler(piezo.x, x_all)
            traj = traj1 + traj2
            yield from bp.scan_nd(dets, traj)

    samples = ["Bag2_S2.1", "Bag2_S2.3", "Bag1_S2_inner"]
    x_list = [
        38798,
        -15000,
        -42000,
    ]
    y_list = [-2099, 100, -2200]
    x_range = [[0, 3500, 36], [0, 3600, 37], [0, 3500, 15]]
    y_range = [[0, 3800, 39], [0, 3100, 32], [0, 5000, 21]]

    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    for x, y, sample, x_r, y_r in zip(x_list, y_list, samples, x_range, y_range):
        pil1M.cam.file_path.put(
            f"/ramdisk/images/users/2020_2/305363_Clark1/1M/%s" % sample
        )
        pil300KW.cam.file_path.put(
            f"/nsls2/xf12id2/data/images/users/2020_2/305363_Clark1/300KW/%s" % sample
        )

        yield from bps.mv(piezo.x, x)
        yield from bps.mv(piezo.y, y)
        for wa in waxs_range:
            yield from bps.mv(waxs, wa)
            name_fmt = "{sam}_wa{waxs}"
            sample_name = name_fmt.format(sam=sample, waxs="%2.1f" % wa)
            sample_id(user_name=name, sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.rel_grid_scan(dets, piezo.y, *y_r, piezo.x, *x_r, 0)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def mapping_waxs_ucol(t=1):
    # samples = ['Bag1_S2_rim', 'Bag1_S2_inner','Bag2_S2.2','Bag1_S3','Bag1_S1']
    # x_list = [  -43900,         -42000,         -16200,     9400,      36800]
    # y_list = [   -3300,          -2200,            0,      -2800,      -2800]
    samples = ["Bag2_S2.2", "Bag1_S1"]
    x_list = [-16200, 36800]
    y_list = [0, -2800]
    name = "NC"

    # x_range=[[0, 7500, 126], [0, 3500, 15], [0, 3800, 39], [0, 9300, 32], [0, 9000, 31]]
    # y_range=[[0, 9000, 151], [0, 5000, 21], [0, 3800, 77], [0, 8400, 29], [0, 9000, 31]]
    x_range = [[0, 3800, 39], [0, 9000, 31]]
    y_range = [[0, 3800, 77], [0, 9000, 31]]

    waxs_range = [13, 6.5, 0]
    # Detectors, motors:
    dets = [pil1M, pil300KW]  # dets = [pil1M,pil300KW]
    det_exposure_time(t, t)

    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    for x, y, sample, x_r, y_r in zip(x_list, y_list, samples, x_range, y_range):
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(piezo.y, y)
        for wa in waxs_range:
            yield from bps.mv(waxs, wa)
            name_fmt = "{sam}_wa{waxs}"
            sample_name = name_fmt.format(sam=sample, waxs="%2.1f" % wa)
            sample_id(user_name=name, sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.rel_grid_scan(dets, piezo.y, *y_r, piezo.x, *x_r, 0)

        #     for yrs in np.linspace(y_r[0], y_r[1], y_r[2]):
        #         yield from bps.mv(piezo.y, y+yrs)
        #         for xrs in np.linspace(x_r[0], x_r[1], x_r[2]):
        #             yield from bps.mv(piezo.x, x+xrs)
        #             name_fmt = '{sam}_x{x}_y{y}'
        #             sample_name = name_fmt.format(sam=sample, x='%6.6d'%(x+xrs), y='%6.6d'%(y+yrs))
        #             sample_id(user_name=name, sample_name=sample_name)
        #             #print(f'\n\t=== Sample: {sample_name} ===\n')
        #             yield from bp.count(dets, num=1)

        # #yield from bp.rel_grid_scan(dets, piezo.x, *x_r, piezo.y, *y_r, 0) #1 = snake, 0 = not-snake

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def run_waxs_UCol(t=1):
    xlocs = [5500]
    names = ["salmonDNA2_air"]
    user = "GS"
    det_exposure_time(t, t)
    y0 = -1350
    assert len(xlocs) == len(
        names
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    y_range = np.linspace(
        -40, 200, 49
    )  # if you start from the bottom, reverse signs: 40, -200, 49
    # Detectors, motors:
    dets = [pil300KW]
    waxs_range = [0, 13, 3]
    for sam, x in zip(names, xlocs):
        yield from bps.mv(piezo.x, x)
        for y in y_range:
            yield from bps.mv(piezo.y, y0 + y)
            name_fmt = "{sam}_y{y_pos}um"
            sample_name = name_fmt.format(sam=sam, y_pos="%2.1f" % y)
            sample_id(user_name=user, sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.scan(dets, waxs, *waxs_range)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def run_waxs_emptyUCol(t=1):
    xlocs = [-34500, -25000, -17050, -3825, 3750, 14050]
    ylocs = [0, 0, 0, 0, 0, 0]
    names = [
        "sDDnem_vac1_bkg",
        "sDDcol_vac_bkg",
        "DDshort_vac1_bkg",
        "DDlong_vac_bkg",
        "GTACshort_vac_bkg",
        "GTAClong_vac_bkg",
    ]
    user = "GS"
    det_exposure_time(t, t)

    assert len(xlocs) == len(
        names
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"

    # Detectors, motors:
    dets = [pil300KW]
    waxs_range = [0, 13, 3]
    for sam, x in zip(names, xlocs):
        yield from bps.mv(piezo.x, x)
        name_fmt = "{sam}"
        sample_name = name_fmt.format(sam=sam)
        sample_id(user_name=user, sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")
        yield from bp.scan(dets, waxs, *waxs_range)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def saxs_waxs_temps_Ucol(t=0.5):
    # Slowest cycle:
    name = "VM"

    # Detectors, motors:
    dets = [pil1M, pil300KW, rayonix, ls.ch1_read]
    y_range = [5.6, 5.6, 1]
    sample = "W1013ITO"
    waxs_range = [0, 13, 3]

    name_fmt = "{sam}_{temperature}C_{tim}s"

    det_exposure_time(t, t)
    temp = ls.ch1_read.value
    t1 = time.time()
    time_elapsed = int(t1 - t0)
    sample_name = name_fmt.format(temperature=temp, sam=sample, tim=time_elapsed)
    print(f"\n\t=== Sample: {sample_name} ===\n")
    sample_id(user_name=sample, sample_name=sample_name)
    # yield from bp.count(dets)
    yield from bp.scan(dets, waxs, *waxs_range)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def run_contRPI(t=1, numb=100, sleep=5):
    det_exposure_time(t, t)
    dets = [pil1M, pil300KW]
    # dets = [pil300Kw]
    for i in range(numb):
        yield from bp.count(dets, num=1)
        yield from bps.sleep(sleep)


def instec_insitu_hard_xray(t=0.4):
    dets = [pil300KW, pil1M]
    det_exposure_time(t, t)

    name = "DIO_loop3"
    temperatures = np.arange(90, 39, -1).tolist()

    waxs_arc = np.linspace(0, 19.5, 4)

    yss = np.linspace(-1.05, -0.85, 21)
    xss = np.linspace(-1.3, -1.5, 21)

    yss, xss = np.meshgrid(yss, xss)

    yss = yss.ravel()
    xss = xss.ravel()

    num = 0
    cur_temp = 400

    t0 = time.time()

    while num < 200 and cur_temp > 313:
        yield from bps.mv(stage.y, yss[num])
        yield from bps.mv(stage.x, xss[num])

        num = num + 1

        t_kelvin = t + 273.15
        cur_temp = ls.input_A.value

        while cur_temp < 100:
            yield from bps.sleep(10)
            cur_temp = ls.input_A.value

        # yield from bps.sleep(60)

        if waxs.arc.position > 10:
            wa_arc = waxs_arc[::-1]
        else:
            wa_arc = waxs_arc

        t1 = time.time()

        for j, wa in enumerate(wa_arc):
            yield from bps.mv(waxs, wa)
            name_fmt = "{sample}_{temperature}C_t{time}_wa{waxs}_sdd1.6m"
            sample_name = name_fmt.format(
                sample=name,
                temperature="%3.1f" % (cur_temp - 273.15),
                time="%3.1f" % (t1 - t0),
                waxs="%2.1f" % wa,
            )
            print(f"\n\t=== Sample: {sample_name} ===\n")
            sample_id(user_name="NC", sample_name=sample_name)
            yield from bp.count(dets, num=1)


def instec_insitu_t_step_hard_xray(t=0.4):
    dets = [pil300KW, pil1M]
    det_exposure_time(t, t)

    name = "RM734_loop1"
    temperatures = np.arange(86, 80, -2).tolist()

    waxs_arc = np.linspace(0, 19.5, 4)

    yss = np.linspace(-1.0, -0.9, 11)
    xss = np.linspace(1.2, 1.1, 11)

    yss, xss = np.meshgrid(yss, xss)

    yss = yss.ravel()
    xss = xss.ravel()

    for num, temper in enumerate(temperatures):
        yield from bps.mv(stage.y, yss[num])
        yield from bps.mv(stage.x, xss[num])

        t_kelvin = temper + 273.15
        yield from ls.output3.mv_temp(t_kelvin - 10)

        cur_temp = ls.input_A.value

        while abs(cur_temp - t_kelvin) > 1.5:
            yield from bps.sleep(10)
            cur_temp = ls.input_A.value

        yield from bps.sleep(60)

        if waxs.arc.position > 10:
            wa_arc = waxs_arc[::-1]
        else:
            wa_arc = waxs_arc

        for j, wa in enumerate(wa_arc):
            yield from bps.mv(waxs, wa)
            name_fmt = "{sample}_{temperature}C_wa{waxs}_sdd1.6m"
            sample_name = name_fmt.format(
                sample=name, temperature="%3.1f" % temper, waxs="%2.1f" % wa
            )
            print(f"\n\t=== Sample: {sample_name} ===\n")
            sample_id(user_name="NC", sample_name=sample_name)
            yield from bp.count(dets, num=1)


def instec_insitu_hard_xray_fixT(t=0.4):

    dets = [pil300KW, pil1M]
    det_exposure_time(t, t)

    name = "RM734__edgeglass"

    temp_C = 110
    # temperatures = [120]
    waxs_arc = np.linspace(0, 19.5, 4)

    if waxs.arc.position > 10:
        wa_arc = waxs_arc[::-1]
    else:
        wa_arc = waxs_arc

    for j, wa in enumerate(wa_arc):
        yield from bps.mv(waxs, wa)
        name_fmt = "{sample}_{temperature}C_wa{waxs}_sdd1.6m_11.15keV"
        sample_name = name_fmt.format(
            sample=name, temperature="%3.1f" % temp_C, waxs="%2.1f" % wa
        )
        print(f"\n\t=== Sample: {sample_name} ===\n")
        sample_id(user_name="NC", sample_name=sample_name)
        yield from bp.count(dets, num=1)


def hard_xray_greg(t=0.5):

    dets = [pil300KW, pil1M]
    det_exposure_time(t, t)

    name = "glass"

    # temperatures = [120]
    waxs_arc = np.linspace(0, 13.0, 3)

    if waxs.arc.position > 10:
        wa_arc = waxs_arc[::-1]
    else:
        wa_arc = waxs_arc

    ypos = [-300, 300, 3]
    for j, wa in enumerate(wa_arc):
        yield from bps.mv(waxs, wa)
        name_fmt = "{sample}_wa{waxs}_sdd1.6m"
        sample_name = name_fmt.format(sample=name, waxs="%2.1f" % wa)
        print(f"\n\t=== Sample: {sample_name} ===\n")
        sample_id(user_name="GS", sample_name=sample_name)
        # yield from bp.rel_scan(dets, piezo.y, *ypos)
        yield from bp.count(dets)


def instec_insitu_hard_xray_2021_3(t=0.4):
    dets = [pil900KW, pil1M]
    det_exposure_time(t, t)

    name = "7-N_"
    waxs_arc = [0, 20]

    yss = np.linspace(-1.55, -1.4, 26)
    xss = np.linspace(-3.0, -2.8, 15)

    yss, xss = np.meshgrid(yss, xss)

    yss = yss.ravel()
    xss = xss.ravel()

    num = 0
    cur_temp = 400

    t0 = time.time()

    while num < 200 and cur_temp > 300:
        yield from bps.mv(stage.y, yss[num])
        yield from bps.mv(stage.x, xss[num])

        num = num + 1

        t_kelvin = t + 273.15
        cur_temp = ls.input_A.value

        while cur_temp < 100:
            yield from bps.sleep(2)
            cur_temp = ls.input_A.value

        # yield from bps.sleep(60)

        if waxs.arc.position > 10:
            wa_arc = waxs_arc[::-1]
        else:
            wa_arc = waxs_arc
        yield from bps.sleep(2)

        t1 = time.time()

        for j, wa in enumerate(wa_arc):
            yield from bps.mv(waxs, wa)
            name_fmt = "{sample}_{temperature}C_t{time}_wa{waxs}_sdd2.0m_16.1keV"
            sample_name = name_fmt.format(
                sample=name,
                temperature="%3.1f" % (cur_temp - 273.15),
                time="%4.1f" % (3940 + t1 - t0),
                waxs="%2.1f" % wa,
            )
            print(f"\n\t=== Sample: {sample_name} ===\n")
            sample_id(user_name="NC", sample_name=sample_name)
            yield from bp.count(dets, num=1)


def instec_oneshot_hard_xray_2021_3(t=0.4):
    dets = [pil900KW, pil1M]
    det_exposure_time(t, t)

    name = "7-N_RT_120deg"
    waxs_arc = [0, 20]

    if waxs.arc.position > 10:
        wa_arc = waxs_arc[::-1]
    else:
        wa_arc = waxs_arc

    for j, wa in enumerate(wa_arc):
        yield from bps.mv(waxs, wa)
        name_fmt = "{sample}_wa{waxs}_sdd2.0m_16.1keV"
        sample_name = name_fmt.format(sample=name, waxs="%2.1f" % wa)
        print(f"\n\t=== Sample: {sample_name} ===\n")
        sample_id(user_name="NC", sample_name=sample_name)
        yield from bp.count(dets, num=1)

####line scan

# sample_id(user_name='ST',sample_name='Nitra-glass_RT_y-4300')


def run_tsaxs_ST(t=0.1):

    # define names of samples on sample bar
    # sample_list = ['sb-b_1_1'] #
    sample_list = ["sam1"]
    # x_list = [42000]
    x_list = [-5800]

    assert len(x_list) == len(sample_list), f"Sample name/position list is borked"

    # angle_arc = np.array([0.08, 0.1, 0.15, 0.2]) # incident angles
    waxs_angle_array = np.linspace(
        0, 18, 4
    )  # q=4*3.14/0.77*np.sin((max angle+3.5)/2*3.14159/180)
    # if 12, 3: up to q=2.199
    # if 18, 4: up to q=3.04
    dets = [
        pil300KW,
        ls.ch1_read,
        rayonix,
        pil1M,
    ]  # waxs, maxs, saxs = [pil300KW, rayonix, pil1M]

    for x, sample in zip(x_list, sample_list):  # loop over samples on bar

        yield from bps.mv(piezo.x, x)  # move to next sample
        # yield from alignement_gisaxs(0.1) #run alignment routine

        # th_meas = angle_arc + piezo.th.position #np.array([0.10 + piezo.th.position, 0.20 + piezo.th.position])
        # th_real = angle_arc
        y_array = np.array([-4500, -4000])

        det_exposure_time(t, t)
        x_meas = x

        for waxs_angle in waxs_angle_array:  # loop through waxs angles
            yield from bps.mv(waxs, waxs_angle)

            for i, th in enumerate(th_meas):  # loop over incident angles
                # yield from bps.mv(piezo.th, th)

                # x_meas = x_meas - 200   # shift a bit in x
                # yield from bps.mv(piezo.x, x_meas)
                temp = ls.ch1_read.value
                sample_name = (
                    "{sample}_{temp}deg_waxs{waxs_angle:05.2f}_x{x}_{t}s".format(
                        sample=sample, temp=temp, waxs_angle=waxs_angle, x=x_meas, t=t
                    )
                )
                sample_id(user_name="ST", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")

                # yield from bp.scan(dets, energy, e, e, 1)
                # yield from bp.scan(dets, waxs, *waxs_arc)
                yield from bp.count(dets, num=1)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5)


def run_harv_temp(tim=1, name="HarvTempRe"):
    # Slowest cycle:
    temperatures = [25, 150]
    # x_list  = [-42000, -20400, 200, 20400, 44300]
    x_list = [50000, 40500, 29000, 19000, 7300, -3400, -18000, -26000, -33000, -39000]
    # y_list =  [  5600,   5800, 5920, 5822,  5972]
    y_list = [8950, 8850, 8750, 8850, 8700, 8650, 8800, 7970, 7970, 7670]
    samples = ["S1", "S2", "S3", "S4", "S5", "S6", "S7", "SH2", "SH3", "SH4"]
    # samples = ['S29']
    # Detectors, motors:
    # dets = [pil1M, rayonix, pil300KW,ls.ch1_read, xbpm3.sumY] #ALL detectors
    dets = [pil300KW, ls.ch1_read, xbpm3.sumY]  # WAXS detector ALONE
    x_offset = [0, 200, 400, 600, 800]
    waxs_arc = [0, 30, 6]
    name_fmt = "{sample}_{offset}um_{temperature}C"
    #    param   = '16.1keV'
    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    det_exposure_time(tim, tim)
    for i_t, t in enumerate(temperatures):
        yield from bps.mv(ls.ch1_sp, t)
        if i_t > 0:
            yield from bps.sleep(600)
        for x, y, s in zip(x_list, y_list, samples):
            temp = ls.ch1_read.value
            yield from bps.mv(piezo.x, x)
            yield from bps.mv(piezo.y, y)
            yield from bps.mv(piezo.z, 200)
            for i_o, o in enumerate(x_offset):
                sample_name = name_fmt.format(sample=s, offset=o, temperature=temp)
                yield from bps.mv(piezo.x, x + x_offset[i_o])
                print(f"\n\t=== Sample: {sample_name} ===\n")
                sample_id(user_name=name, sample_name=sample_name)
                yield from bp.scan(dets, waxs, *waxs_arc)
    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)
    yield from bps.mv(ls.ch1_sp, 28)


def run_harv_poly(tim=1, name="HarvPoly"):
    # Slowest cycle:
    temperatures = [85]
    x_list = [-1000]
    y_list = [-4740]
    samples = ["S29"]
    # Detectors, motors:
    dets = [pil300KW, ls.ch1_read, xbpm3.sumY]
    name_fmt = "{sample}_{temperature}C"
    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    det_exposure_time(tim, tim)
    for i_t, t in enumerate(temperatures):
        yield from bps.mv(ls.ch1_sp, t)
        # yield from bps.sleep(30)
        yield from bps.mv(ls.ch1_sp, 28)
        for x, y, s in zip(x_list, y_list, samples):
            yield from bps.mv(piezo.x, x)
            yield from bps.mv(piezo.y, y)
            yield from bps.mv(piezo.z, 200)
            for i in range(600):
                temp = ls.ch1_read.value
                sample_name = name_fmt.format(sample=s, temperature=temp)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                sample_id(user_name=name, sample_name=sample_name)
                yield from bp.count(dets, num=1)
                yield from bps.sleep(30)
    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)
    yield from bps.mv(ls.ch1_sp, 28)


def run_harv_micro(tim=3, name="HarvMicro_2_25C"):
    # Slowest cycle:
    temperatures = [150]
    # x_list  = [-42000, -20400, 200, 20400, 44300]
    x_list = [
        40016,
    ]
    # y_list =  [  5600,   5800, 5920, 5822,  5972]
    y_list = [
        -3880,
    ]
    samples = ["SC10", "SC11", "SC12", "SC13", "SC14", "SC15", "SC16", "SC17"]
    # samples = ['S29']
    # Detectors, motors:
    # dets = [pil1M, rayonix, pil300KW,ls.ch1_read, xbpm3.sumY] #ALL detectors
    dets = [pil300KW, ls.ch1_read, xbpm3.sumY]  # WAXS detector ALONE
    x_offset = [-704, -352, 0, 352, 704]
    y_range = [20, -20, 3]
    waxs_arc = [0, 30, 6]
    name_fmt = "{sample}_{xoffset}um_{temperature}C"
    #    param   = '16.1keV'
    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    det_exposure_time(tim, tim)
    for i_t, t in enumerate(temperatures):
        yield from bps.mv(ls.ch1_sp, t)
        if i_t > 0:
            yield from bps.sleep(600)
        for x, y, s in zip(x_list, y_list, samples):
            temp = ls.ch1_read.value
            yield from bps.mv(piezo.x, x)
            yield from bps.mv(piezo.y, y)
            yield from bps.mv(piezo.z, 2800)
            for i_x, xo in enumerate(x_offset):
                sample_name = name_fmt.format(sample=s, xoffset=xo, temperature=temp)
                yield from bps.mv(piezo.x, x + x_offset[i_x])
                print(f"\n\t=== Sample: {sample_name} ===\n")
                sample_id(user_name=name, sample_name=sample_name)
                yield from bp.rel_scan(dets, piezo.y, *y_range)
    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)
    yield from bps.mv(ls.ch1_sp, 28)

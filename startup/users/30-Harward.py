####line scan


def run_harv_temp(tim=0.5):
    # Slowest cycle:
    temperatures = [25]
    name = "ML"
    x_list = [-7000, 6000]
    y_list = [4900, 5100]
    samples = ["set7_sample1_3rdcycle", "set7_sample2_3rdcycle"]
    assert len(x_list) == len(
        y_list
    ), f"Number of X coordinates ({len(x_list)}) is different from number of Y coordinates ({len(y_list)})"
    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"

    # Detectors, motors:
    dets = [pil1M, pil300KW]  # ALL detectors
    # dets = [pil300KW,ls.ch1_read, xbpm3.sumY] # WAXS detector ALONE

    x_offset = [0, 0, 400, 400]
    y_offset = [0, 50, 0, 50]
    zoff = -9000
    waxs_arc = np.linspace(0, 32.5, 6)
    name_fmt = "{sample}_pos{offset}_{temperature}C_wa{waxs}"
    yield from bps.mv(piezo.z, zoff)

    det_exposure_time(tim, tim)
    for i_t, t in enumerate(temperatures):
        yield from bps.mv(ls.ch1_sp, t)
        if i_t != 0:
            yield from bps.sleep(600)
        temp = ls.ch1_read.value
        for j, wa in enumerate(waxs_arc):  #
            yield from bps.mv(waxs, wa)
            for x, y, s in zip(x_list, y_list, samples):
                yield from bps.mv(piezo.x, x)
                yield from bps.mv(piezo.y, y)
                for i_0, (x_0, y_0) in enumerate(zip(x_offset, y_offset)):
                    sample_name = name_fmt.format(
                        sample=s,
                        offset=i_0 + 1,
                        temperature="%3.1f" % temp,
                        waxs="%2.1f" % wa,
                    )
                    yield from bps.mv(piezo.x, x + x_0)
                    yield from bps.mv(piezo.y, y + y_0)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    sample_id(user_name=name, sample_name=sample_name)
                    yield from bp.count(dets, num=1)
    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)
    yield from bps.mv(ls.ch1_sp, 28)


def run_harv_temp_all_2022_1(tim=0.5):
    # Slowest cycle:
    temperatures = [30, 100, 180]
    # temperatures = [30, 100, 150]

    name = "ML"

    # x_list  = [-45880, -38480, -29480, -23480, -16700, -4700, 3300, 10300, 18300, 26300, 32700, 37600, 45800]
    # y_list =  [  6700,   6700,   6700,   6520,   6480,  6440, 6400,  6340,  6340,  6220,  6180,  6180,  6380]
    # samples = ['set1_MML_071', 'set1_MML_076', 'set1_MML_077', 'set1_MML_081', 'set1_MML_082-1', 'set1_MML_082-2', 'set1_MML_083-1',
    # 'set1_MML_083-2', 'set2_ST03457', 'set2_ST03866', 'set2_ST05874', 'set2_ST02670', 'set2_ST04180']

    # x_list  = [-42000, -34500, -27000, -21000, -14000, -8300, -2300, 5300, 13000, 19500, 26500, 32500, 40500, 49500]
    # y_list =  [  6630,   6630,   6530,   6330,   6530,  6330,  6130, 6230,  6330,  6030,  6130,  6130,  6330,  6230]
    # samples = ['set3_RM257_2.5', 'set3_RM257_5.0', 'set3_RM257_10.0', 'set3_RM257_15.0', 'set4_RM82_2.5', 'set4_RM82_5.0', 'set4_RM82_10.0',
    # 'set5_sample1', 'set7_700G', 'set7_790G', 'set7_600G', 'set7_250G', 'set10_sample1', 'set10_sample2d']

    # x_list  = [-48000, -40000, -32000, -25000, -20500, -16500, -11700, -6700, 3300, 15300, 26200, 32800, 41900, 49500]
    # y_list =  [  6580,   6580,   6880,   6730,   6830,   6830,   6330,  6430, 5030,  5030,  6730,  6670,  6630,  6690]
    # samples = ['set4_RM82_2.5-2', 'set4_RM82_15.0', 'set8_azo_2.5', 'set8_azo_5.0', 'set8_azo_5.0-2', 'set8_azo_10.0', 'set8_azo_15.0',
    # 'stex_MML-076', 'set11_symx_1', 'set11_symz_2', 'set6_SP1', 'set6_SP2', 'set6_SP3', 'set6_SP4']

    x_list = [-41000, -30500, -22500, -14000, -3000]
    y_list = [6620, 6500, 6580, 6400, 6220]
    samples = [
        "set9_ST04180",
        "set9_ST03866",
        "set9_ST03866_2",
        "set9_ST02670",
        "set9_ST05874",
    ]

    assert len(x_list) == len(
        y_list
    ), f"Number of X coordinates ({len(x_list)}) is different from number of Y coordinates ({len(y_list)})"
    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"

    # Detectors, motors:
    dets = [pil1M, pil300KW]  # ALL detectors
    # dets = [pil300KW,ls.ch1_read, xbpm3.sumY] # WAXS detector ALONE

    x_offset = [0, 0, 400, 400]
    y_offset = [0, 50, 0, 50]
    zoff = -10000
    waxs_arc = np.linspace(0, 32.5, 6)
    name_fmt = "{sample}_2_pos{offset}_{temperature}C_wa{waxs}"
    yield from bps.mv(piezo.z, zoff)

    det_exposure_time(tim, tim)
    for i_t, t in enumerate(temperatures):
        yield from bps.mv(ls.ch1_sp, t)
        if i_t != 0:
            yield from bps.sleep(600)

        temp = ls.ch1_read.value
        for j, wa in enumerate(waxs_arc):  #
            yield from bps.mv(waxs, wa)
            for x, y, s in zip(x_list, y_list, samples):
                yield from bps.mv(piezo.x, x)
                yield from bps.mv(piezo.y, y)
                if s == "set11_symx_1" or s == "set11_symz_2":
                    sample_name = name_fmt.format(
                        sample=s,
                        offset=0,
                        temperature="%3.1f" % temp,
                        waxs="%2.1f" % wa,
                    )
                    yield from bps.mv(piezo.x, x)
                    yield from bps.mv(piezo.y, y)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    sample_id(user_name=name, sample_name=sample_name)
                    yield from bp.scan(dets, piezo.y, y, y + 1110, 38)

                else:
                    for i_0, (x_0, y_0) in enumerate(zip(x_offset, y_offset)):
                        sample_name = name_fmt.format(
                            sample=s,
                            offset=i_0 + 1,
                            temperature="%3.1f" % temp,
                            waxs="%2.1f" % wa,
                        )
                        yield from bps.mv(piezo.x, x + x_0)
                        yield from bps.mv(piezo.y, y + y_0)
                        print(f"\n\t=== Sample: {sample_name} ===\n")
                        sample_id(user_name=name, sample_name=sample_name)
                        yield from bp.count(dets, num=1)
    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)
    yield from bps.mv(ls.ch1_sp, 28)


def temp_2021_3(tim=0.5):
    # Slowest cycle:
    # temperatures = [27, 45, 70, 100, 120, 150, 170, 30]
    temperatures = [30]

    name = "MW"

    # samples = ['set1_sam1', 'set1_sam2', 'set1_sam3', 'set1_sam4', 'set1_sam5', 'set1_sam6', 'set1_sam7', 'set1_sam8', 'set1_sam9', 'set1_sam10',
    #  'set1_sam11', 'set1_sam12','set1_sam13', 'set1_sam14', 'set1_sam15', 'set1_sam16']
    # x_list  = [49600, 45600, 41000, 35800, 29000, 23800, 17800, 7600,  800, -5000, -12500, -18900, -24500, -31300,-37900, -44300]
    # y_list =  [-8700, -8700, -9000, -8700,-8700, -8700, -8700, -8700, -8600, -8500, -8700, -8700,  -8600, -8700, -8450, -8450]

    samples = [
        "Sideon_7.5HDDA_zalignedrod",
        "Endon_2.5HDDA_zalignedrod_thick",
        "Endon_2.5HDDA_zalignedrod_thin_5CBswollen",
        "Endon_2.5HDDA_splayalignedrod_5CBswollen",
    ]
    x_list = [-40400, -35200, -26000, -18600, -11200, -3800, 2800]
    y_list = [400, 475, 450, 400, 250, 100, 225]

    # -24000 -50000
    assert len(x_list) == len(
        y_list
    ), f"Number of X coordinates ({len(x_list)}) is different from number of Y coordinates ({len(y_list)})"
    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"

    # Detectors, motors:
    dets = [pil1M, pil900KW]  # ALL detectors

    x_offset = [0, 0, 400, 400, 800, 800, 1200, 1200]
    y_offset = [0, 50, 0, 50, 0, 50, 0, 50]
    waxs_arc = [0, 20]
    name_fmt = "{sample}_afterheating_18.25keV_1.6m_pos{offset}_{temperature}C_wa{waxs}"

    det_exposure_time(tim, tim)
    for i_t, t in enumerate(temperatures):
        t_kelvin = t + 273.15
        yield from ls.output1.mv_temp(t_kelvin)
        temp = ls.input_A.get()

        while abs(temp - t_kelvin) > 2:
            print(abs(temp - t_kelvin))
            yield from bps.sleep(10)
            temp = ls.input_A.get()

        if i_t != 0:
            yield from bps.sleep(450)

        # temp = ls.input_A.get()
        t_celsius = temp - 273.15

        for j, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)
            for x, y, s in zip(x_list, y_list, samples):
                yield from bps.mv(piezo.x, x)
                yield from bps.mv(piezo.y, y)

                # if s != 'set3_sam1':
                #     x_offset = [0, 0, 400, 400]
                #     y_offset = [0, 50, 0, 50]

                # else:
                #     x_offset = np.linspace(0, -26000, 27)
                #     y_offset = np.linspace(0, 0, 27)

                for i_0, (x_0, y_0) in enumerate(zip(x_offset, y_offset)):
                    sample_name = name_fmt.format(
                        sample=s,
                        offset=i_0 + 1,
                        temperature="%3.1f" % t_celsius,
                        waxs="%2.1f" % wa,
                    )
                    yield from bps.mv(piezo.x, x + x_0)
                    yield from bps.mv(piezo.y, y + y_0)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    sample_id(user_name=name, sample_name=sample_name)
                    yield from bp.count(dets, num=1)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)

    t_kelvin = 25 + 273.15
    yield from ls.output1.mv_temp(t_kelvin)


def temp_xscan_2022_1(tim=0.5):
    # Slowest cycle:
    # temperatures = [27, 45, 70, 100, 120, 150, 170, 30]
    temperatures = [30, 100, 180]

    name = "PQ"

    # samples = ['set1_sam1', 'set1_sam2', 'set1_sam3', 'set1_sam4', 'set1_sam5', 'set1_sam6', 'set1_sam7', 'set1_sam8', 'set1_sam9', 'set1_sam10',
    #  'set1_sam11', 'set1_sam12','set1_sam13', 'set1_sam14', 'set1_sam15', 'set1_sam16']
    # x_list  = [49600, 45600, 41000, 35800, 29000, 23800, 17800, 7600,  800, -5000, -12500, -18900, -24500, -31300,-37900, -44300]
    # y_list =  [-8700, -8700, -9000, -8700,-8700, -8700, -8700, -8700, -8600, -8500, -8700, -8700,  -8600, -8700, -8450, -8450]

    samples = ["A-0", "A-4", "A-5", "A-6", "A-7", "A-8"]
    x_list = [-15800, -34000, -19000, -8000, 6000, 19000]
    y_list = [-2200, 3630, 3540, 3510, 3900, 3870]
    y_range = [
        [0, 6000, 61],
        [0, 8000, 81],
        [0, 7000, 71],
        [0, 8000, 81],
        [0, 7500, 76],
        [0, 3500, 36],
    ]

    # -24000 -50000
    assert len(x_list) == len(
        y_list
    ), f"Number of X coordinates ({len(x_list)}) is different from number of Y coordinates ({len(y_list)})"
    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"

    # Detectors, motors:
    dets = [pil1M, pil900KW]  # ALL detectors
    det_exposure_time(tim, tim)
    waxs_arc = [0, 20]
    name_fmt = "{sample}_16.1keV_1.6m_pos{offset}_{temperature}C_wa{waxs}"

    det_exposure_time(tim, tim)
    for i_t, t in enumerate(temperatures):
        t_kelvin = t + 273.15
        yield from ls.output1.mv_temp(t_kelvin)
        temp = ls.input_A.get()

        while abs(temp - t_kelvin) > 2:
            print(abs(temp - t_kelvin))
            yield from bps.sleep(10)
            temp = ls.input_A.get()

        if i_t != 0:
            yield from bps.sleep(450)

        # temp = ls.input_A.get()
        t_celsius = temp - 273.15

        for j, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)
            for x, y, s, x_r in zip(x_list, y_list, samples, x_range):
                yield from bps.mv(piezo.x, x)
                yield from bps.mv(piezo.y, y)

                for i_0, xrs in enumerate(np.linspace(x_r[0], x_r[1], x_r[2])):
                    sample_name = name_fmt.format(
                        sample=s,
                        offset=i_0 + 1,
                        temperature="%3.1f" % t_celsius,
                        waxs="%2.1f" % wa,
                    )
                    yield from bps.mv(piezo.x, x + xrs)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    sample_id(user_name=name, sample_name=sample_name)
                    yield from bp.count(dets, num=1)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)

    t_kelvin = 25 + 273.15
    yield from ls.output1.mv_temp(t_kelvi % rn)


def temp_yscan_2022_1(tim=1):
    # Slowest cycle:
    # temperatures = [27, 45, 70, 100, 120, 150, 170, 30]
    temperatures = [30, 100, 180]

    name = "PQ"

    # samples = ['set1_sam1', 'set1_sam2', 'set1_sam3', 'set1_sam4', 'set1_sam5', 'set1_sam6', 'set1_sam7', 'set1_sam8', 'set1_sam9', 'set1_sam10',
    #  'set1_sam11', 'set1_sam12','set1_sam13', 'set1_sam14', 'set1_sam15', 'set1_sam16']
    # x_list  = [49600, 45600, 41000, 35800, 29000, 23800, 17800, 7600,  800, -5000, -12500, -18900, -24500, -31300,-37900, -44300]
    # y_list =  [-8700, -8700, -9000, -8700,-8700, -8700, -8700, -8700, -8600, -8500, -8700, -8700,  -8600, -8700, -8450, -8450]

    samples = ["A-0", "A-1", "A-2", "C-1-1", "C-1-2"]
    x_list = [-15800, -4800, 10200, 26030, 36190]
    y_list = [-2200, -2200, -2200, -400, 700]
    chi_list = [0, 0, 0, 4, 4.2]
    y_range = [
        [0, 2000, 11],
        [0, 2000, 11],
        [0, 2000, 11],
        [0, 1800, 91],
        [0, 1800, 91],
    ]

    # -24000 -50000
    assert len(x_list) == len(
        y_list
    ), f"Number of X coordinates ({len(x_list)}) is different from number of Y coordinates ({len(y_list)})"
    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"

    # Detectors, motors:
    dets = [pil1M, pil900KW]  # ALL detectors

    waxs_arc = [0, 20]
    name_fmt = "{sample}_16.1keV_1.6m_pos{offset}_{temperature}C_wa{waxs}"

    det_exposure_time(tim, tim)
    for i_t, t in enumerate(temperatures):
        t_kelvin = t + 273.15
        yield from ls.output1.mv_temp(t_kelvin)
        temp = ls.input_A.get()

        while abs(temp - t_kelvin) > 2:
            print(abs(temp - t_kelvin))
            yield from bps.sleep(10)
            temp = ls.input_A.get()

        if i_t != 0:
            yield from bps.sleep(450)

        # temp = ls.input_A.get()
        t_celsius = temp - 273.15

        for j, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)
            for x, y, chi, s, y_r in zip(x_list, y_list, chi_list, samples, y_range):
                yield from bps.mv(piezo.x, x)
                yield from bps.mv(piezo.y, y)
                yield from bps.mv(piezo.ch, chi)

                for i_0, yrs in enumerate(np.linspace(y_r[0], y_r[1], y_r[2])):
                    sample_name = name_fmt.format(
                        sample=s,
                        offset=i_0 + 1,
                        temperature="%3.1f" % t_celsius,
                        waxs="%2.1f" % wa,
                    )
                    yield from bps.mv(piezo.y, y + yrs)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    sample_id(user_name=name, sample_name=sample_name)
                    yield from bp.count(dets, num=1)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)

    t_kelvin = 25 + 273.15
    yield from ls.output1.mv_temp(t_kelvin)


def hydrogel_2021_1(tim=0.5):

    x_list = [43900, 35000, 23500, 13500, 6000, -10700, -18500, -32400, -33800, -36400]
    y_list = [8700, -5300, -5300, -5300, 8700, 8700, -5300, 8700, 8700, 8700]
    samples = [
        "hyd_gel_Spindmso",
        "hyd_gel_sample2",
        "hyd_gel_sample3",
        "hyd_gel_sample9",
        "hyd_gel_sample10",
        "hyd_gel_sample5",
        "hyd_gel_sample11",
        "hyd_gel_sample6",
        "hyd_gel_sample7",
        "hyd_gel_sample8",
    ]

    assert len(x_list) == len(
        y_list
    ), f"Number of X coordinates ({len(x_list)}) is different from number of Y coordinates ({len(y_list)})"
    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"

    # Detectors, motors:
    dets = [pil1M, pil300KW]  # ALL detectors

    x_offset = [0, 0, 0]
    y_offset = [-200, 0, 200]
    waxs_arc = np.linspace(0, 32.5, 6)
    name_fmt = "{sample}_18.25keV_1.6m_pos{offset}_wa{waxs}"

    det_exposure_time(tim, tim)

    for j, wa in enumerate(waxs_arc):
        yield from bps.mv(waxs, wa)
        for x, y, s in zip(x_list, y_list, samples):
            yield from bps.mv(piezo.x, x)
            yield from bps.mv(piezo.y, y)

            for i_0, (x_0, y_0) in enumerate(zip(x_offset, y_offset)):
                sample_name = name_fmt.format(
                    sample=s, offset=i_0 + 1, waxs="%2.1f" % wa
                )
                yield from bps.mv(piezo.x, x + x_0)
                yield from bps.mv(piezo.y, y + y_0)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                sample_id(user_name="ML", sample_name=sample_name)
                yield from bp.count(dets, num=1)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)

    t_kelvin = 25 + 273.15
    yield from ls.output1.mv_temp(t_kelvin)


def run_harv_temp_all(tim=0.5):
    # Slowest cycle:
    temperatures = [100, 150]
    name = "ML"
    # x_list  = [-46300, -37300, -29800, -20300, -13800, -6200, 1300, 9000, 16700, 26300, 33300, 39300, 46300, 53000]
    # y_list =  [-8800, -8800, -8800, -8750, -8750, -8750, -9200, -9200, -9300, -9100, -9200, -9300, -8970, -9000]
    # samples = [ 'set1_sample1', 'set1_sample2','set1_sample3','set1_sample4','set1_sample5', 'set1_sample6', 'set3_sample1', 'set3_sample2','set3_sample3','set3_sample4','set3_sample5', 'set3_sample6','set2_sample3', 'set2_sample4']

    x_list = [42000, 28000, 13300, -7700, -14100]
    y_list = [-6800, -7800, -8800, -8800, -7800]
    samples = [
        "set6_headon_sample1",
        "set6_headon_sample2",
        "set6_headon_sample3",
        "set6_headon_sample4",
        "set6_headon_sample5",
    ]

    assert len(x_list) == len(
        y_list
    ), f"Number of X coordinates ({len(x_list)}) is different from number of Y coordinates ({len(y_list)})"
    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"

    # Detectors, motors:
    dets = [pil1M, pil300KW]  # ALL detectors
    # dets = [pil300KW,ls.ch1_read, xbpm3.sumY] # WAXS detector ALONE

    x_offset = [0, 0, 400, 400]
    y_offset = [0, 50, 0, 50]
    zoff = -2000
    waxs_arc = np.linspace(0, 32.5, 6)
    name_fmt = "{sample}_pos{offset}_{temperature}C_wa{waxs}"
    yield from bps.mv(piezo.z, zoff)

    det_exposure_time(tim, tim)
    for i_t, t in enumerate(temperatures):
        yield from bps.mv(ls.ch1_sp, t)
        if i_t != 0:
            yield from bps.sleep(600)
        temp = ls.ch1_read.value
        for j, wa in enumerate(waxs_arc):  #
            yield from bps.mv(waxs, wa)
            for x, y, s in zip(x_list, y_list, samples):
                yield from bps.mv(piezo.x, x)
                yield from bps.mv(piezo.y, y)
                for i_0, (x_0, y_0) in enumerate(zip(x_offset, y_offset)):
                    sample_name = name_fmt.format(
                        sample=s,
                        offset=i_0 + 1,
                        temperature="%3.1f" % temp,
                        waxs="%2.1f" % wa,
                    )
                    yield from bps.mv(piezo.x, x + x_0)
                    yield from bps.mv(piezo.y, y + y_0)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    sample_id(user_name=name, sample_name=sample_name)
                    yield from bp.count(dets, num=1)
    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)
    yield from bps.mv(ls.ch1_sp, 28)


def run_linkam_cooling(t=0.15, tim=0.15):
    name = "PQ"
    sample = "insitu_b-7"
    offset = 300  # microns
    # Detectors, motors:
    # dets = [pil900KW, pil1M]
    waxs_arc = [0, 20]
    name_fmt = "{sample}_wa{waxs}_time{ctime}s"
    now = time.time()
    det_exposure_time(t, tim)
    for i in range(100):
        yield from bps.mvr(piezo.x, offset)
        for j, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)
            dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]
            ctime = time.time() - now
            sample_name = name_fmt.format(
                sample=sample, waxs="%2.1f" % wa, ctime="%.0f" % ctime
            )
            print(f"\n\t=== Sample: {sample_name} ===\n")
            sample_id(user_name=name, sample_name=sample_name)
            yield from bp.count(dets, num=1)
            yield from bps.sleep(120)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)


def run_harv_linkam_waxs(t=0.2, tim=20):
    name = "MW"
    sample = "InSitu_AzoSideon_spot2"
    offset = 600  # microns
    # Detectors, motors:
    dets = [pil900KW]
    waxs_arc = [7]
    name_fmt = "{sample}_{temperature}C_wa{waxs}"

    det_exposure_time(t, tim)

    temp = ls.input_A_celsius.get()
    yield from bps.mvr(piezo.x, offset)
    for j, wa in enumerate(waxs_arc):
        yield from bps.mv(waxs, wa)
        sample_name = name_fmt.format(
            sample=sample, temperature="%2.2f" % temp, waxs="%2.1f" % wa
        )
        print(f"\n\t=== Sample: {sample_name} ===\n")
        sample_id(user_name=name, sample_name=sample_name)
        # yield from bp.count(dets, num=1)
        pil900KW.cam.acquire.put(1)
        yield from bps.sleep(tim + 1)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)


def run_harv_linkam_saxs(t=0.2, tim=20):
    name = "MW"
    sample = "InSitu_AzoSideonspot2"

    # Detectors, motors:
    dets = [pil1M]
    wa = 20
    name_fmt = "{sample}_{temperature}C"

    det_exposure_time(t, tim)

    temp = ls.input_A_celsius.get()
    yield from bps.mv(waxs, wa)
    sample_name = name_fmt.format(sample=sample, temperature="%2.2f" % temp)
    print(f"\n\t=== Sample: {sample_name} ===\n")
    sample_id(user_name=name, sample_name=sample_name)
    # yield from bp.count(dets, num=1)
    pil1M.cam.acquire.put(1)
    yield from bps.sleep(tim + 1)


def run_harv_linkam(t=0.2, tim=20):
    yield from run_harv_linkam_saxs(t=t, tim=tim)
    yield from run_harv_linkam_waxs(t=t, tim=tim)


def run_harv_linkam_both(t=0.3, tim=0.3):
    name = "MW"
    names = [
        "endon_2.5HDDA_zalignedrod_pos1_lower",
        "endon_2.5HDDA_zalignedrod_pos2_lower",
        "endon_2.5HDDA_zalignedrod_pos3_lower",
        "endon_2.5HDDA_zalignedrod_pos4_lower",
        "endon_2.5HDDA_zalignedrod_pos5_lower",
        "endon_2.5HDDA_zalignedrod_pos6_lower",
        "endon_2.5HDDA_zalignedrod_pos7_lower",
    ]
    piezo_x = [-1651, -451, 749, 1949, 3149, 4349, 5549]
    piezo_y = [-3349, -3349, -3349, -3349, -3349, -3349, -3349]
    # sample = 'InSitu_AzoSideon_spot2'
    # Detectors, motors:
    dets = [pil1M]
    wa = 20
    name_fmt = "{sample}_{temperature}C"

    det_exposure_time(t, tim)

    temp = ls.input_A_celsius.get()
    yield from bps.mv(waxs, wa)

    for sample, x, y in zip(names, piezo_x, piezo_y):
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(piezo.y, y)
        sample_name = name_fmt.format(sample=sample, temperature="%2.2f" % temp)
        print(f"\n\t=== Sample: {sample_name} ===\n")
        sample_id(user_name=name, sample_name=sample_name)
        yield from bp.count(dets, num=1)  # for singleshot
        # pil1M.cam.acquire.put(1) #next 2 lines for burst shots
        # yield from bps.sleep(tim+1)

    offset = 600  # microns
    # Detectors, motors:
    dets = [pil900KW]
    waxs_arc = [7]
    name_fmt = "{sample}_{temperature}C_wa{waxs}"

    yield from bps.mvr(piezo.x, offset)
    for j, wa in enumerate(waxs_arc):
        yield from bps.mv(waxs, wa)
        for sample, x in zip(names, piezo_x):
            yield from bps.mv(piezo.x, x + offset)
            sample_name = name_fmt.format(
                sample=sample, temperature="%2.2f" % temp, waxs="%2.1f" % wa
            )
            print(f"\n\t=== Sample: {sample_name} ===\n")
            sample_id(user_name=name, sample_name=sample_name)
            yield from bp.count(dets, num=1)  # for single shot
            # pil900KW.cam.acquire.put(1) #next 2 lines for burst shots
            # yield from bps.sleep(tim+1)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)


def run_harv_temp_time(tim=0.2):
    name = "SL"
    sample = "InSitu_EndOn_NoCross_PhaseDia_40C_v3_UVlvl_0.5V"
    timegaps = [10] * 4 + [30] * 2 + [60] * 3
    # Detectors, motors:
    dets = [pil1M]
    waxs_arc = [19.5]
    name_fmt = "{sample}_{temperature}C_wa{waxs}"

    # Openinig the gate valve
    yield from bps.mv(GV7.open_cmd, 1)
    yield from bps.sleep(5)
    yield from bps.mv(GV7.open_cmd, 1)
    yield from bps.sleep(5)

    det_exposure_time(tim, tim)

    temp = ls.ch1_read.value
    for i, gap in enumerate(timegaps):
        sample = sample + "_timestep" + str(i)
        for j, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)
            sample_name = name_fmt.format(
                sample=sample, temperature="%2.2f" % temp, waxs="%2.1f" % wa
            )
            print(f"\n\t=== Sample: {sample_name} ===\n")
            sample_id(user_name=name, sample_name=sample_name)
            yield from bp.count(dets, num=1)
        yield from bps.sleep(gap)
    for j, wa in enumerate(waxs_arc):
        yield from bps.mv(waxs, wa)
        sample_name = name_fmt.format(
            sample=sample, temperature="%2.2f" % temp, waxs="%2.1f" % wa
        )
        print(f"\n\t=== Sample: {sample_name} ===\n")
        sample_id(user_name=name, sample_name=sample_name)
        yield from bp.count(dets, num=1)
    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)

    # Closing the gate valve
    yield from bps.mv(GV7.close_cmd, 1)
    yield from bps.sleep(5)
    yield from bps.mv(GV7.close_cmd, 1)
    yield from bps.sleep(5)


def harvphi(meas_t=0.5):
    waxs_arc = np.linspace(0, 32.5, 6)  # (2th_min 2th_max steps)
    dets = [pil300KW, pil1M]
    names = ["DDDA5_vert_100C"]
    # phis = np.linspace(-90, 90, 13)
    phis = np.linspace(-75, 75, 11)

    for name in names:
        det_exposure_time(meas_t, meas_t)

        name_fmt = "{sample}_phi{phi}deg_wa{waxs}"
        # waxs is the slowest cycle:
        for j, wa in enumerate(waxs_arc):  #
            yield from bps.mv(waxs, wa)
            # phi is scanned for a single waxs
            for i, phi in enumerate(phis):
                yield from bps.mv(prs, phi)
                sample_name = name_fmt.format(
                    sample=name, phi="%2.1f" % phi, waxs="%2.1f" % wa
                )
                sample_id(user_name="SL", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

        yield from bps.mv(prs, 0)
    sample_id(user_name="test", sample_name="test")


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
        # yield from bps.sleep(def run_harv_pos_scan(tim=3,name = 'Harv_SideOn_2.5_PA'):
    # x_list  = [-42000, -20400, 200, 20400, 44300]
    x_list = np.linspace(-5800, -13800, 17)
    # y_list =  [  5600,   5800, 5920, 5822,  5972]
    y_list = [-4400]

    # Detectors, motors:
    # dets = [pil1M, rayonix, pil300KW,ls.ch1_read, xbpm3.sumY] #ALL detectors
    dets = [pil300KW, ls.ch1_read, xbpm3.sumY]  # WAXS detector ALONE
    waxs_arc = [0, 30, 6]
    name_fmt = "{sample}_{xoffset}um_{temperature}C"
    #    param   = '16.1keV'
    det_exposure_time(tim, tim)
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


def run_harv_pos(tim=5):
    # Slowest cycle:
    name = "SL"
    x_list = [np.linspace(27700, 28200, 26)]
    y_list = [-4400]
    samples = ["EndOn_1.5_HDDA_MicroStruct_Cap_Step20um_Area2"]

    assert len(x_list) == len(
        y_list
    ), f"Number of X coordinates ({len(x_list)}) is different from number of Y coordinates ({len(y_list)})"
    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"

    # Detectors, motors:
    dets = [pil1M, pil300KW]  # ALL detectors

    waxs_arc = [13]
    name_fmt = "{sample}_pos{offset}_wa{waxs}"

    det_exposure_time(tim, tim)
    for j, wa in enumerate(waxs_arc):  #
        yield from bps.mv(waxs, wa)

        for x, y, s in zip(x_list, y_list, samples):
            yield from bps.mv(piezo.y, y)

            for i_0, x_0 in enumerate(x):
                yield from bps.mv(piezo.x, x_0)
                sample_name = name_fmt.format(
                    sample=s, offset=i_0 + 1, waxs="%2.1f" % wa
                )
                print(f"\n\t=== Sample: {sample_name} ===\n")
                sample_id(user_name=name, sample_name=sample_name)
                yield from bp.count(dets, num=1)
    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)
    yield from bps.mv(ls.ch1_sp, 28)


def mesh_milan_2022_2(t=0.5):
    waxs_range = [0, 20]

    dets = [pil900KW, pil1M]
    det_exposure_time(t, t)

    # these samples are very large areas and 3rd priority (lowest) except for the 1st teeth12.
    samples = [
        "20220801MW_C_1",
        "20220801MW_C_2",
        "20220801MW_C_3",
        "20220801MW_C_4",
        "20220801MW_C_5",
        "20220801MW_C_6",
        "20220801MW_C_7",
    ]
    x_list = [46200, 34900, 18050, 5950, -24710, -45660, -58760]
    y_list = [2940, 3310, 3840, 3980, 4170, 4320, 4370]
    z_list = [-2600, -2600, -2600, -2800, -2600, -2400, -2400]
    hexa_x = [16, 0, 0, 0, 0, 0, 0]
    th_list = [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7]
    x_range = [
        [0, 12000, 241],
        [0, 18000, 361],
        [0, 9000, 181],
        [0, 4000, 81],
        [0, 10000, 201],
        [0, 10000, 201],
        [0, 9000, 181],
    ]
    y_range = [
        [0, 700, 3],
        [0, 700, 3],
        [0, 100, 3],
        [0, 150, 3],
        [0, 200, 3],
        [0, 200, 3],
        [0, 200, 3],
    ]

    # first load room T
    # samples = ['20220801MW_C_1', '20220801MW_C_2','20220801MW_C_3', '20220801MW_C_4', '20220801MW_C_5', '20220801MW_C_6', '20220801MW_C_7']
    # x_list = [ 46100,              34800,                18050,            5950,            -24710,              -45660,            -58760]
    # y_list = [ 2940,               3310,                 3840,              3980,             4170,                4320 ,              4370]
    # z_list = [  -2600,           -2600,                 -2600,            -2800,             -2600,              -2400,              -2400]
    # hexa_x = [   16,               0,                   0,                 0,               0,                   0 ,                 0]
    # th_list = [0.7,               0.7,                 0.7,               0.7,              0.7,                 0.7,                0.7]
    # x_range=[ [0,12000,241],   [0,18000,361],       [0,9000,181],       [0,4000,81],     [0,10000,201],    [0,10000,201],      [0,9000,181]]
    # y_range=[ [0,700,3],        [0,700,3],          [0,100,3],          [0,150,3],       [0,200,3],         [0,200,3],           [0,200,3]]

    assert len(x_list) == len(
        y_list
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(y_list)})"
    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    assert len(x_list) == len(
        x_range
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(x_range)})"
    assert len(x_list) == len(
        y_range
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(y_range)})"

    for x, y, z, th, hx, name, x_r, y_r in zip(
        x_list, y_list, z_list, th_list, hexa_x, samples, x_range, y_range
    ):
        # proposal_id('2021_3', 'Wang%s'%num)
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(piezo.y, y)
        yield from bps.mv(piezo.z, z)
        yield from bps.mv(piezo.th, th)
        yield from bps.mv(stage.x, hx)

        for wa in waxs_range:
            yield from bps.mv(waxs, wa)
            dets = [pil900KW] if waxs.arc.position < 15 else [pil900KW, pil1M]

            e = energy.position.energy / 1000  # energy keV
            sdd = pil1m_pos.z.position / 1000  # SAXS detector distance
            scan_id = db[-1].start["scan_id"] + 1  # transient scan ID
            proposal_id("2022_2", "310149_Wilborn/%s" % name)

            name_fmt = "{sample}_{energy}keV_sdd{sdd}m_wa{wax}_id{scan_id}_dx50um"
            sample_name = name_fmt.format(
                sample=name,
                energy="%.1f" % e,
                sdd="%.1f" % sdd,
                wax="%2.1f" % wa,
                scan_id=scan_id,
            )
            sample_name = sample_name.translate(
                {ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ =,"}
            )
            sample_id(user_name="MW", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")

            yield from bp.rel_grid_scan(dets, piezo.y, *y_r, piezo.x, *x_r, 0)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def mesh_milan_temp_2022_2(t=0.5):
    waxs_range = [0, 20]
    temperatures = [100, 150]
    dets = [pil900KW, pil1M]
    det_exposure_time(t, t)

    # second load, heated stage
    samples = [
        "20220801MW_C_8",
        "20220801MW_C_10",
        "20220801MW_C_11",
        "20220801MW_C_12",
        "20220801MW_C_13",
        "20220801MW_C_14",
        "20220801MW_C_15",
    ]
    x_list = [37128, 27598, 9798, -8602, -23352, -28352, -49752]
    y_list = [3369, 3329, 3469, 3509, 3729, 4129, 3939]
    z_list = [-11300, -11300, -11300, -11300, -11300, -11300, -7300]
    hexa_x = [0, 0, 0, 0, 0, 0, 0]
    th_list = [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7]
    x_range = [
        [0, 18000, 361],
        [0, 5000, 101],
        [0, 8000, 161],
        [0, 9000, 181],
        [0, 8500, 171],
        [0, 7500, 151],
        [0, 8000, 161],
    ]
    y_range = [
        [0, 200, 3],
        [0, 100, 3],
        [0, 200, 3],
        [0, 200, 3],
        [0, 250, 3],
        [0, 150, 3],
        [0, 300, 3],
    ]

    # first load, heated stage
    # samples = ['20220801MW_C_1', '20220801MW_C_3', '20220801MW_C_4', '20220801MW_C_5', '20220801MW_C_6', '20220801MW_C_7']
    # x_list = [ 39500,                -1000,            -13500,          -27400,           -40800,            -52400]
    # y_list = [ 2970,                  3690,              3780,            3960,             4110 ,              4070]
    # z_list = [ -12100,               -12100,            -12100,          -12100,           -11300,              -11300]
    # hexa_x = [   0,                   0,                 0,                0,                0 ,                 0]
    # th_list = [0.7,                  0.7,               0.7,              0.7,              0.7,                0.7]
    # x_range=[ [0,12000,241],       [0,9000,181],       [0,8000,81],     [0,9000,181],    [0,10000,201],      [0,8000,11]]
    # y_range=[ [0,500,3],           [0,100,3],          [0,100,3],       [0,100,3],         [0,100,3],           [0,200,3]]

    # first load room T
    # samples = ['20220801MW_C_1', '20220801MW_C_2','20220801MW_C_3', '20220801MW_C_4', '20220801MW_C_5', '20220801MW_C_6', '20220801MW_C_7']
    # x_list = [ 46100,              34800,                18050,            5950,            -24710,              -45660,            -58760]
    # y_list = [ 2940,               3310,                 3840,              3980,             4170,                4320 ,              4370]
    # z_list = [  -2600,           -2600,                 -2600,            -2800,             -2600,              -2400,              -2400]
    # hexa_x = [   16,               0,                   0,                 0,               0,                   0 ,                 0]
    # th_list = [0.7,               0.7,                 0.7,               0.7,              0.7,                 0.7,                0.7]
    # x_range=[ [0,12000,241],   [0,18000,361],       [0,9000,181],       [0,4000,81],     [0,10000,201],    [0,10000,201],      [0,9000,181]]
    # y_range=[ [0,700,3],        [0,700,3],          [0,100,3],          [0,150,3],       [0,200,3],         [0,200,3],           [0,200,3]]

    assert len(x_list) == len(
        y_list
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(y_list)})"
    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    assert len(x_list) == len(
        x_range
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(x_range)})"
    assert len(x_list) == len(
        y_range
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(y_range)})"

    for temperature in temperatures:
        t_kelvin = temperature + 273.15
        yield from ls.output1.mv_temp(t_kelvin)

        # Activate heating range in Lakeshore
        # if temperature < 80:
        #    yield from bps.mv(ls.output1.status, 1)
        # else:
        yield from bps.mv(ls.output1.status, 3)

        # Equalise temperature
        print(f"Equalising temperature to {temperature} deg C")
        start = time.time()
        temp = ls.input_A.get()
        while abs(temp - t_kelvin) > 1:
            print("Difference: {:.1f} K".format(abs(temp - t_kelvin)))
            yield from bps.sleep(10)
            temp = ls.input_A.get()

            # Escape the loop if too much time passes
            if time.time() - start > 1800:
                temp = t_kelvin
        print(
            "Time needed to equilibrate: {:.1f} min".format((time.time() - start) / 60)
        )
        # Wait extra time depending on temperature
        if (35 < temperature) and (temperature < 181):
            yield from bps.sleep(300)

        # Read T and convert to deg C
        temp_degC = ls.input_A.get() - 273.15

        for x, y, z, th, hx, name, x_r, y_r in zip(
            x_list, y_list, z_list, th_list, hexa_x, samples, x_range, y_range
        ):
            # proposal_id('2021_3', 'Wang%s'%num)
            yield from bps.mv(piezo.x, x)
            yield from bps.mv(piezo.y, y)
            yield from bps.mv(piezo.z, z)
            yield from bps.mv(piezo.th, th)
            yield from bps.mv(stage.x, hx)

            for wa in waxs_range:
                yield from bps.mv(waxs, wa)
                dets = [pil900KW] if wa < 15 else [pil900KW, pil1M]

                e = energy.position.energy / 1000  # energy keV
                sdd = pil1m_pos.z.position / 1000  # SAXS detector distance
                scan_id = db[-1].start["scan_id"] + 1  # transient scan ID
                temp = str(np.round(float(temp_degC), 1)).zfill(5)
                proposal_id("2022_2", "310149_Wilborn1/%s" % name)

                name_fmt = "{sample}_{temp}degC_{energy}keV_sdd{sdd}m_wa{wax}_id{scan_id}_dx50um"
                sample_name = name_fmt.format(
                    sample=name,
                    temp=temp,
                    energy="%.1f" % e,
                    sdd="%.1f" % sdd,
                    wax="%2.1f" % wa,
                    scan_id=scan_id,
                )
                sample_name = sample_name.translate(
                    {ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ =,"}
                )
                sample_id(user_name="MW", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")

                yield from bp.rel_grid_scan(dets, piezo.y, *y_r, piezo.x, *x_r, 0)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)
    # Turn off the heating and set temperature to 23 deg C
    t_kelvin = 23 + 273.15
    yield from ls.output1.mv_temp(t_kelvin)
    yield from ls.output1.turn_off()


def linescan_milan_temp_2022_3(t=0.5):
    """
    Fine line scan on Linkam GI thermal stage
    """

    names =   ['MWA01','MWA02', 'MWA03','MWB01','MWB02','MWB03','MWB04','MWD01','FSB21','FSB23']

    piezo_x = [ 61200,  50700,     45850,  42750,   31000,  19300,       7650,      -4450, -32950, -42750]
    piezo_y = [  170,    380,     400,      610,   870,   1090,        1240,    1670,      2110,    2110]
    piezo_z = [   -3270,  -3270,    -3270,        -3270, -3270,    -3270,    -3270,    -3270, -3270, -3270]
    #piezo_z = [8400 for n in names]
    y_range = [[0, -9500, 96],[0,-4200,43], [0,-2100,22], [0, -10500, 106],[0, -10800, 109], [0,-11000,111], [0, -8800, 89], [0, -14500, 146], [0, -4000, 41], [0, -800, 9]]

    assert len(names) == len(piezo_x),  f"Wrong list lenghts"
    assert len(piezo_y) == len(piezo_x),  f"Wrong list lenghts"
    assert len(piezo_y) == len(piezo_z), f"Wrong list lenghts"
    assert len(piezo_z) == len(y_range), f"Wrong list lenghts"

    waxs_arc = [0, 20]
    temperatures = [38, 95, 150]


    for temperature in temperatures:
        t_kelvin = temperature + 273.15
        yield from ls.output1.mv_temp(t_kelvin)
        yield from bps.mv(ls.output1.status, 3)

        # Equalise temperature
        print(f"Equalising temperature to {temperature} deg C")
        start = time.time()
        temp = ls.input_A.get()
        while abs(temp - t_kelvin) > 3:
            print("Difference: {:.1f} K".format(abs(temp - t_kelvin)))
            yield from bps.sleep(10)
            temp = ls.input_A.get()

            # Escape the loop if too much time passes
            if time.time() - start > 1800:
                temp = t_kelvin
        print(
            "Time needed to equilibrate: {:.1f} min".format((time.time() - start) / 60)
        )
        # Wait extra time depending on temperature
        if (35 < temperature) and (temperature < 181):
            yield from bps.sleep(300)

        # Read T and convert to deg C
        temp_degC = ls.input_A.get() - 273.15

        for name, x, y, z, scan_pts in zip(names, piezo_x, piezo_y, piezo_z, y_range):
            yield from bps.mv(piezo.x, x,
                              piezo.y, y,
                              piezo.z, z)

            for wa in waxs_arc:
                yield from bps.mv(waxs, wa)
                dets = [pil900KW] if waxs.arc.position < 15 else [pil1M, pil900KW]
                det_exposure_time(t, t)

                e = energy.position.energy / 1000  # energy keV
                sdd = pil1m_pos.z.position / 1000  # SAXS detector distance
                temp = str(np.round(float(temp_degC), 1)).zfill(5)
                wa = waxs.arc.position + 0.001
                wa = str(np.round(float(wa), 1)).zfill(4)
                #proposal_id("2022_2", "310149_Wilborn1/%s" % name)
                name_fmt = "{sample}_{temp}degC_{energy}keV_wa{wax}_sdd{sdd}m"
                sample_name = name_fmt.format(
                    sample=name,
                    temp=temp,
                    energy="%.2f" % e,
                    wax=wa,
                    sdd="%.1f" % sdd,   
                )
                sample_name = sample_name.translate(
                    {ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ =,"}
                )
                sample_id(user_name="MW", sample_name=sample_name)
                print(f"\n\n\n\t=== Sample: {sample_name} ===")

                yield from bp.rel_scan(dets, piezo.x, *scan_pts)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)
    # Turn off the heating and set temperature to 23 deg C
    t_kelvin = 23 + 273.15
    yield from ls.output1.mv_temp(t_kelvin)
    yield from ls.output1.turn_off()


def milan_temp_2023_1(tim=0.2):
    """
    Temperature scan using Linkam thermal GI stage for transmission with the hexa tilt.
    RT, 100C, 150C, 4 points per sample. For hockey pucks.

    REMEMBER: add temperature to file name or retrive later with databroker...
    """

    names =   ['JMA08', 'JMB08','JMA02','JMA04','JMA06','JMA07','JMA09','JMB04','JMB06','JMA05','JMA03','JMA10','FTB64','FTA64','FTB53','FTA67','FTD54','FTA54','FTB54', 'FTB75']
    piezo_x = [  57900,    53100,  47300, 42500,     37500,   30500,     23500,     18300,    12900,   8100,      2900,     -2100,    -6900,   -11300,   -17300,   -22900,   -28100,   -34300,   -41500,   -47900]
    piezo_y = [    300,      300,    550,   600,        750,     750,      1000,     1000,     1000,     1350,        1350,      1350,     1850,   1950, 2150, 2400, 2400, 2250, 2800,2449]
    piezo_z = [       -3370,         -3370,        -3370,      -3370,            -3370,        -3370,         -3370,      -3370,     -3370,     -3370,        -3370,       -3370,      -3370,    -1470, -2470, -1220, -2270, -2970, -1870, -4620]
    #piezo_z = [8400 for n in names]


    assert len(names) == len(
        piezo_x), f"Number of X coordinates ({len(names)}) is different from number of samples ({len(piezo_x)})"
    assert len(piezo_y) == len(
        piezo_x), f"Number of Y coordinates ({len(piezo_y)}) is different from number of samples ({len(piezo_x)})"


    #temperatures = [28]
    user_name = 'MW'

    x_offset = [0,  200]
    y_offset = [0, 0]
    waxs_arc = [0, 20]

    #for i_t, t in enumerate(temperatures):
    #print(f'Going to {t:.0f} deg C')
    #t_kelvin = t + 273.15
    #yield from ls.output1.mv_temp(t_kelvin)
    #yield from bps.mv(ls.output1.status, 3)
    #temp = ls.input_A.get()

    #while abs(temp - t_kelvin) > 3:
    #    print(f'Current temp: {temp - 273.15:.1f} degC,\t difference: {(temp - t_kelvin):.1f} deg C')
    #    yield from bps.sleep(10)
    #    temp = ls.input_A.get()

    #if i_t != 0:
    #    yield from bps.sleep(450)

    #temp = ls.input_A.get()
    #t_celsius = temp - 273.15

    for wa in waxs_arc:

        yield from bps.mv(waxs, wa)
        
        dets = [pil900KW] if waxs.arc.position < 15 else [pil1M, pil900KW]
        det_exposure_time(tim, tim)

        for name, x, y, z in zip(names, piezo_x, piezo_y, piezo_z):
            yield from bps.mv(piezo.x, x,
                                piezo.y, y,
                                piezo.z, z)

            for i, (x_off, y_off) in enumerate(zip(x_offset, y_offset)):
                
                yield from bps.mv(piezo.x, x + x_off,
                                    piezo.y, y + y_off)

                # Metadata
                e = energy.position.energy / 1000
                wa = waxs.arc.position + 0.001
                wa = str(np.round(float(wa), 1)).zfill(4)
                sdd = pil1m_pos.z.position / 1000
                #t_celsius = str(np.round(float(t_celsius), 1)).zfill(5)


                # Sample name
                #name_fmt = '{sample}_{t_c}degC_{energy}keV_wa{wax}_sdd{sdd}m_pos{pos}'
                name_fmt = '{sample}_{energy}keV_wa{wax}_sdd{sdd}m_pos{pos}'
                sample_name = name_fmt.format(
                    sample=name,
                    #t_c = t_celsius,
                    energy="%.2f" % e,
                    wax=wa,
                    sdd="%.1f" % sdd,
                    pos=i,
                )
                
                print(f"\n\n\n\t=== Sample: {sample_name} ===")
                sample_id(user_name=user_name, sample_name=sample_name)
                yield from bp.count(dets)

    sample_id(user_name='test', sample_name='test')
    det_exposure_time(0.2, 0.2)

    #t_kelvin = 25 + 273.15
    #yield from ls.output1.mv_temp(t_kelvin)
    #yield from ls.output1.turn_off()


def grid_milan_temp_2023_1(t=0.2):
    """
    Fine grid scan on Linkam GI thermal stage
    """
    names =   [ 'JMB9','JMC8','JMD8','FTB47','FTB49','FTD67','FTA75','FTA70','FTA68', 'FT',  'KLA12',      'KLA11',        'KLA10',      'KLA09',        'KLA08',   'KLA07',      'KLA06',     'KLA05',    'KLA04',    'KLA03',    'KLA02',    'KLA01']

    piezo_x = [-46900, -39300, -35200, -23800, -13600, -9200, -1600, 2000, 6000, 12800, 20600, 24600, 28600,30600,35100, 36600,40600,43600, 44600, 46600,50600, 56600]
    piezo_y = [ 3000, 3149, 2949, 2099, 2049, 1899, 1749, 1749, 1649, 1449, 1250, 1150,  1050,1050,950, 950,550, 950,450,450,650, 650]
    piezo_z = [-1570, 180, 180, 630, -2020, -1970,-1970,-1970,-1970,-1970, -3670,-3670,-3670,-3670,-3670,-3670,-3670,-3670,-3670,-3670,-3670, -3670]
    #piezo_z = [8400 for n in names]
    y_range = [[0, 100, 2],[0, 100, 2],[0, 100, 2],[0, 100, 2],[0, 100, 2],[0, 100, 2],[0, 100, 2],[0, 100, 2],[0, 100, 2],[0, 100, 2],[0, 100, 11],[0, 100, 11],[0, 100, 11],[0, 100, 11],[0, 100, 11],[0, 100, 11],[0, 200, 21],[0, 200, 21],[0, 400, 41],[0, 200, 21],[0, 200, 21],[0, 200, 21]]
    x_range = [[0, 300, 2], [0, 300, 2],[0, 300, 2],[0, 300, 2],[0, 300, 2],[0, 300, 2],[0, 300, 2],[0, 300, 2],[0, 300, 2],[0, 300, 2],[0, 300, 2],[0, 300, 2],[0, 300, 2],[0, 300, 2],[0, 300, 2],[0, 300, 2],[0, 300, 2],[0, 300, 2],[0, 300, 2],[0, 300, 2],[0, 300, 2],[0, 300, 2]]


    assert len(names) == len(piezo_x),   f"Wrong list lenghts"
    assert len(piezo_y) == len(piezo_x), f"Wrong list lenghts"
    assert len(piezo_y) == len(piezo_z), f"Wrong list lenghts"
    assert len(piezo_z) == len(y_range), f"Wrong list lenghts"
    assert len(y_range) == len(x_range), f"Wrong list lenghts"

    waxs_arc = [0, 20]
    temperatures = [28, 80, 100, 150] 

    for temperature in temperatures:
        t_kelvin = temperature + 273.15
        yield from ls.output1.mv_temp(t_kelvin)
        yield from bps.mv(ls.output1.status, 3)

        # Equalise temperature
        print(f"Equalising temperature to {temperature} deg C")
        start = time.time()
        temp = ls.input_A.get()
        while abs(temp - t_kelvin) > 5:
            print("Difference: {:.1f} K".format(abs(temp - t_kelvin)))
            yield from bps.sleep(10)
            temp = ls.input_A.get()

            # Escape the loop if too much time passes
            if time.time() - start > 1800:
                temp = t_kelvin
        print(
            "Time needed to equilibrate: {:.1f} min".format((time.time() - start) / 60)
        )
        # Wait extra time depending on temperature
        if (40 < temperature) and (temperature < 181):
            yield from bps.sleep(300)

        # Read T and convert to deg C
        temp_degC = ls.input_A.get() - 273.15

        for name, x, y, z, scan_pts_y, scan_pts_x in zip(names, piezo_x, piezo_y, piezo_z, y_range, x_range):
            yield from bps.mv(piezo.x, x,
                              piezo.y, y,
                              piezo.z, z)

            for wa in waxs_arc:
                yield from bps.mv(waxs, wa)
                dets = [pil900KW] if waxs.arc.position < 15 else [pil1M, pil900KW]
                det_exposure_time(t, t)

                e = energy.position.energy / 1000
                sdd = pil1m_pos.z.position / 1000
                temp = str(np.round(float(temp_degC), 1)).zfill(5)
                wa = waxs.arc.position + 0.001
                wa = str(np.round(float(wa), 1)).zfill(4)
                #proposal_id("2022_2", "310149_Wilborn1/%s" % name)
                name_fmt = "{sample}_{temp}degC_{energy}keV_wa{wax}_sdd{sdd}m"
                sample_name = name_fmt.format(
                    sample=name,
                    temp=temp,
                    energy="%.2f" % e,
                    wax=wa,
                    sdd="%.1f" % sdd,   
                )
                sample_name = sample_name.translate(
                    {ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ =,"}
                )
                sample_id(user_name="MW", sample_name=sample_name)
                print(f"\n\n\n\t=== Sample: {sample_name} ===")

                yield from bp.rel_grid_scan(dets, piezo.x, *scan_pts_x, piezo.y, *scan_pts_y)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)
    # Turn off the heating and set temperature to 23 deg C
    t_kelvin = 23 + 273.15
    yield from ls.output1.mv_temp(t_kelvin)
    yield from ls.output1.turn_off()

def run_harv_linkam_swaxs_2023_2(t=0.2, t_tot=20, temp=25):
    """
    WAXS and SAXS continous measurement on Linkam GI stage
    Args:
        t (float): detector exposure time single frame,
        t_tot (float): total exposure time,
        temp (float): temperature from Linkam to record in sample.
    """

    # Samples and coordinats
    names   = ['FSB41' ]
    piezo_x = [  7500 ]
    piezo_y = [ -2170 ]
    piezo_z = [ 7200 ]

    # Check if the length of xlocs, ylocs and names are the same
    msg = "Wrong number of coordinates, check names and piezos"
    assert len(piezo_x) == len(names), msg
    assert len(piezo_x) == len(piezo_y), msg
    assert len(piezo_x) == len(piezo_z), msg

    waxs_arc = [20, 7]
    det_exposure_time(t, t)
    user = "FS"
    waxs_rounds = int(np.ceil( t_tot / t / 2))

    yield from bps.mv(waxs, waxs_arc[0])

    for name, x, y, z in zip(names, piezo_x, piezo_y, piezo_z):

        yield from bps.mv(piezo.x, x,
                          piezo.y, y,
                          piezo.z, z,
                          waxs, waxs_arc[0])
        
        t0 = time.time() - 1400


        for i in range(waxs_rounds):
            for wa in waxs_arc:
                yield from bps.mv(waxs, wa)
                dets = [pil900KW] if waxs.arc.position < 14 else [pil900KW, pil1M]

                # Metadata
                step = str(i).zfill(3)
                td = str(np.round(time.time() - t0, 1)).zfill(6)
                temp = str(np.round(float(temp), 1)).zfill(5)

                sample_name = f'{name}_{temp}degC_step{step}_time{td}s{get_scan_md()}'
                sample_name = sample_name.translate(
                    {ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ =,"})
                sample_id(user_name=user, sample_name=sample_name)
                print(f"\n\n\n\t=== Sample: {sample_name} ===")
                yield from bp.count(dets)

    # End of the scan
    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)


def grid_milan_temp_2023_2(t=0.5):
    """
    Fine grid scan on GI thermal stage but
    """
    names =   [ 'JMA01','JMA02','JMB02','JMC02','JMA03','JMB03','JMC03','JMA04','JMB04','JMC04','JMA05','JMB05','JMC05','JMA06','JMB06','JMC06','FSB34','FSB33','FSA25','FSB23','FSB24']

    piezo_x = [-44100,  -40100, -36100, -31100, -23600, -19600, -14600, -8600, -3600,  -100,  2900,   8400,   12900,  18400,  23400,  28800,  34200,  41200,  45800,  53800,    57800 ]
    piezo_y = [ -2100,  -2000,  -2000,  -2900,  -1600,  -1700,  -1600,  -1500,  -2400,  -1400,  -1300,  -2800,  -2100,  -900,  -1300,  -1100,  -2300,   -2100,   -1700,   -800, -700 ]
    piezo_z = [-4400,   -4400,  -4400,  -4400,  -1400,  -4400,  -4400,  -5800,  -5400,  -4600,  -4600,  -4600,  -3800,  -2000,  -3800,  -3600,  -5200,  -5000,  -3000,  -4400,  -4400]
    #piezo_z = [8400 for n in names]
    y_range = [[0, 300, 3],[0, 200, 2],[0, 200, 2],[0, 1200, 12],[0, 300, 3],[0, 400, 4],[0, 300, 3],[0, 300, 3],[0, 1300, 13],[0, 300, 3],[0, 200, 2],[0, 1600, 16],[0, 1100, 11],[0, 2, 1],[0, 400, 4],[0, 400, 4],[0, 900, 9],[0, 1400, 14],[0, 1100, 11],[0, 200, 2],[0, 200, 2]]
    x_range = [[0, 300, 2],[0, 300, 2],[0, 300, 2],[0, 300, 2],[0, 300, 2],[0, 300, 2],[0, 300, 2],[0, 300, 2],[0, 300, 2],[0, 300, 2],[0, 300, 2],[0, 300, 2],[0, 300, 2],[0, 300, 2],[0, 300, 2],[0, 300, 2],[0, 300, 2],[0, 300, 2],[0, 300, 2],[0, 300, 2],[0, 300, 2] ]

    msg = "Wrong number of coordinates, check names and piezos"
    assert len(names) == len(piezo_x),   msg
    assert len(piezo_y) == len(piezo_x), msg
    assert len(piezo_y) == len(piezo_z), msg
    assert len(piezo_z) == len(y_range), msg
    assert len(y_range) == len(x_range), msg

    waxs_arc = [0, 20]
    # #temperatures = [27,80,150]
    det_exposure_time(t, t)

    # for temperature in temperatures:
    #     t_kelvin = temperature + 273.15
    #     yield from ls.output1.mv_temp(t_kelvin)
    #     yield from bps.mv(ls.output1.status, 3)

    #     # Equalise temperature
    #     print(f"Equalising temperature to {temperature} deg C")
    #     start = time.time()
    #     temp = ls.input_A.get()
    #     while abs(temp - t_kelvin) > 5:
    #         print("Difference: {:.1f} K".format(abs(temp - t_kelvin)))
    #         yield from bps.sleep(10)
    #         temp = ls.input_A.get()

    #         # Escape the loop if too much time passes
    #         if time.time() - start > 1800:
    #             temp = t_kelvin
    #     print(
    #         "Time needed to equilibrate: {:.1f} min".format((time.time() - start) / 60)
    #     )
    #     # Wait extra time depending on temperature
    #     if (40 < temperature) and (temperature < 181) and (temperature != temperatures[0]):
    #         yield from bps.sleep(600)

    #     for name, x, y, z, scan_pts_y, scan_pts_x in zip(names, piezo_x, piezo_y, piezo_z, y_range, x_range):
    #         yield from bps.mv(piezo.x, x,
    #                           piezo.y, y,
    #                           piezo.z, z)

    #         # Read T and convert to deg C
    #         temp_degC = ls.input_A.get() - 273.15
    #         temp = str(np.round(float(temp_degC), 1)).zfill(5)

    #         for wa in waxs_arc:
    #             yield from bps.mv(waxs, wa)
    #             dets = [pil900KW] if waxs.arc.position < 15 else [pil1M, pil900KW]
    
    #             sample_name = f'{name}_{temp}degC{get_scan_md()}'
    #             sample_name = sample_name.translate(
    #                 {ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ =,"}
    #             )
    #             sample_id(user_name="MW", sample_name=sample_name)
    #             print(f"\n\n\n\t=== Sample: {sample_name} ===")

    #             yield from bp.rel_grid_scan(dets + [ls.input_A], piezo.x, *scan_pts_x, piezo.y, *scan_pts_y)
    #             plt.close('all')

    #         waxs_arc = waxs_arc[::-1]

    for name, x, y, z, scan_pts_y, scan_pts_x in zip(names, piezo_x, piezo_y, piezo_z, y_range, x_range):
        yield from bps.mv(piezo.x, x,
                      piezo.y, y,
                      piezo.z, z)

        for wa in waxs_arc:
                yield from bps.mv(waxs, wa)
                dets = [pil900KW] if waxs.arc.position < 15 else [pil1M, pil900KW]
                
                sample_name = f'{name}_150degC{get_scan_md()}'
                sample_name = sample_name.translate(
                    {ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ =,"}
                )
                sample_id(user_name="MW", sample_name=sample_name)
                print(f"\n\n\n\t=== Sample: {sample_name} ===")

                yield from bp.rel_grid_scan(dets + [ls.input_A], piezo.x, *scan_pts_x, piezo.y, *scan_pts_y)
                plt.close('all')

        waxs_arc = waxs_arc[::-1]
    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)

    # Turn off the heating and set temperature to 23 deg C
    # t_kelvin = 23 + 273.15
    # yield from ls.output1.mv_temp(t_kelvin)
    # yield from ls.output1.turn_off()

def linescan_milan_temp_2023_2(t=0.5):
    """
    Fine line scan on Linkam GI thermal stage
    """

    names =   ['JMA04','JMC07','JMAB07','JMC04','JMA07','JMC03','JMC02','JMA02','JMA03','MWB01','MWA01' ]
    piezo_x = [ -38400,-30400,-19900,-10900,-2900,5100,14100,23100,30100,45100,50000  ]
    piezo_y = [  -2300,-2000,-2000,-2000,-1700,-1700,-1700,-1700,-1700,-900,-650  ]
    piezo_z = [ -5000,-5000,-5000,-5000,-5600,-4200,-4200,-4200,-600,-4000,-4000 ]
    #piezo_z = [8400 for n in names]
    x_range = [[0, 2000, 40],[0, 2000, 40],[0, 1500, 30],[0, 2000, 40],[0, 1000, 20],[0, 2000, 40],[0, 1000, 20],[0, 1000, 20],[0, 2000, 40],[0, 1500, 30],[0, 11400, 228]]

    msg = "Wrong number of coordinates, check names and piezos"
    assert len(names) == len(piezo_x),   msg
    assert len(piezo_y) == len(piezo_x), msg
    assert len(piezo_y) == len(piezo_z), msg
    assert len(piezo_z) == len(x_range), msg
    assert len(x_range) == len(x_range), msg

    waxs_arc = [0, 20]
    # temperatures = [27, 100, 150]
    det_exposure_time(t, t)

    # for temperature in temperatures:
    #     t_kelvin = temperature + 273.15
    #     yield from ls.output1.mv_temp(t_kelvin)
    #     yield from bps.mv(ls.output1.status, 3)

    #     # Equalise temperature
    #     print(f"Equalising temperature to {temperature} deg C")
    #     start = time.time()
    #     temp = ls.input_A.get()
    #     while abs(temp - t_kelvin) > 5:
    #         print("Difference: {:.1f} K".format(abs(temp - t_kelvin)))
    #         yield from bps.sleep(10)
    #         temp = ls.input_A.get()

    #         # Escape the loop if too much time passes
    #         if time.time() - start > 1800:
    #             temp = t_kelvin
    #     print(
    #         "Time needed to equilibrate: {:.1f} min".format((time.time() - start) / 60)
    #     )
    #     # Wait extra time depending on temperature
    #     if (40 < temperature) and (temperature < 181):
    #         yield from bps.sleep(1800)

    #     for name, x, y, z, scan_pts_x in zip(names, piezo_x, piezo_y, piezo_z, x_range):
    #         yield from bps.mv(piezo.x, x,
    #                           piezo.y, y,
    #                           piezo.z, z)
            
    #         # Read T and convert to deg C
    #         temp_degC = ls.input_A.get() - 273.15
    #         temp = str(np.round(float(temp_degC), 1)).zfill(5)
            
    #         for wa in waxs_arc:
    #             yield from bps.mv(waxs, wa)
    #             dets = [pil900KW] if waxs.arc.position < 15 else [pil1M, pil900KW]

    #             sample_name = f'{name}_{temp}degC{get_scan_md()}'
    #             sample_name = sample_name.translate(
    #                 {ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ =,"}
    #             )
    #             sample_id(user_name="MW", sample_name=sample_name)
    #             print(f"\n\n\n\t=== Sample: {sample_name} ===")

    #             yield from bp.rel_scan(dets + [ls.input_A], piezo.x, *scan_pts_x)
    #             plt.close('all')
    #         waxs_arc = waxs_arc[::-1]
    for name, x, y, z, scan_pts_x in zip(names, piezo_x, piezo_y, piezo_z, x_range):
            yield from bps.mv(piezo.x, x,
                              piezo.y, y,
                              piezo.z, z)

            for wa in waxs_arc:
                yield from bps.mv(waxs, wa)
                dets = [pil900KW] if waxs.arc.position < 15 else [pil1M, pil900KW]

                sample_name = f'{name}_150degC{get_scan_md()}'
                sample_name = sample_name.translate(
                    {ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ =,"}
                )
                sample_id(user_name="MW", sample_name=sample_name)
                print(f"\n\n\n\t=== Sample: {sample_name} ===")

                yield from bp.rel_scan(dets, piezo.x, *scan_pts_x)
                plt.close('all')
            waxs_arc = waxs_arc[::-1]
    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)

    # # Turn off the heating and set temperature to 23 deg C
    # t_kelvin = 23 + 273.15
    # yield from ls.output1.mv_temp(t_kelvin)
    # yield from ls.output1.turn_off()


def linescan_milan_notemp_2023_3(t=0.5):
    """
    Fine line scan on magnetic sample bar
    """

    names =   ['FS_B_44','FT_A_98','FT_B_98','FT_C_98','FT_D_98','FT_E_98','FT_F_98','FT_G_98','FT_H_98','FT_I_98','FT_J_98','FT_A_99','FT_B_45','FT_A_46','FT_A_67','FT_B_49','FT_A_50','FT_C_45','FT_A_47','FT_B_47']
    piezo_x = [ -15450,-1450,1800,4050,7550,9550,12550,16050,19550,23050,26050,28800,31800,35300,38300,41300,44800,47800,51800,55300]
    piezo_y = [  7123,6123,6123,5923,6123,6123,6123,6123,6023,6023,6123,6023,5923,5823,5923,5723,5723,5823,5723,5723]
    piezo_z = [ -4600,-5600,-5600,-5400,-5400,-5400,-5400,-5400,-5400,-5400,-5400,-5400,-5400,-7400,-7400,-7400,-7400,-7400,-7400,-7400 ]
    #piezo_z = [8400 for n in names]
    x_range = [[0, 10500, 105],[0, 200, 2],[0, 200, 2],[0, 200, 2],[0, 200, 2],[0, 200, 2],[0, 200, 2],[0, 200, 2],[0, 200, 2],[0, 200, 2],[0, 200, 2],[0, 200, 2],[0, 200, 2],[0, 200, 2],[0, 200, 2],[0, 200, 2],[0, 200, 2],[0, 200, 2],[0, 200, 2],[0, 200, 2]]

    msg = "Wrong number of coordinates, check names and piezos"
    assert len(names) == len(piezo_x),   msg
    assert len(piezo_y) == len(piezo_x), msg
    assert len(piezo_y) == len(piezo_z), msg
    assert len(piezo_z) == len(x_range), msg
    assert len(x_range) == len(x_range), msg

    waxs_arc = [0, 20]

    det_exposure_time(t, t)

    temp_degC = 25
    temp = str(np.round(float(temp_degC), 1)).zfill(5)

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)
        dets = [pil900KW] if waxs.arc.position < 15 else [pil1M, pil900KW]

        for name, x, y, z, scan_pts_x in zip(names, piezo_x, piezo_y, piezo_z, x_range):

            yield from bps.mv(piezo.x, x,
                              piezo.y, y,
                              piezo.z, z)

            sample_name = f'{name}_temp{temp}degC{get_scan_md()}'
            sample_id(user_name="MW", sample_name=sample_name)
            print(f"\n\n\n\t=== Sample: {sample_name} ===")

            yield from bp.rel_scan(dets, piezo.x, *scan_pts_x)
            plt.close('all')

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def run_linkam_temp_run_linescan_2023_3(t=0.5, temp=80, delay=60):
    """
    Fine y line scan Linkam temp control
    Put temperature as the function argument temp = XX
    """

    names =   ['FS_B_18', 'FS_B_28', 'FS_B_41', 'FS_B_26', 'FS_B_13', ]
    piezo_x = [    -5700,     -2300,      1100,      5600,      8600, ]
    piezo_y = [    -1750,     -1900,     -1950,     -2350,     -1750, ]
    piezo_z = [     6400,      6400,      6400,      6400,      5600, ]
    #piezo_z = [8400 for n in names]
    y_range = [[0, 300, 31],[0, 350, 36],[0, 450, 46], [0, 900, 91], [0, 500, 51]]

    msg = "Wrong number of coordinates, check names and piezos"
    assert len(names) == len(piezo_x),   msg
    assert len(piezo_y) == len(piezo_x), msg
    assert len(piezo_y) == len(piezo_z), msg
    assert len(piezo_z) == len(y_range), msg

    waxs_arc = [0, 20]
    det_exposure_time(t, t)
    temp = str(np.round(float(temp), 1)).zfill(5)

    for name, x, y, z, scan_pts_y in zip(names, piezo_x, piezo_y, piezo_z, y_range):
        yield from bps.mv(piezo.x, x,
                          piezo.y, y,
                          piezo.z, z)
        
        time0 = time.time()
        print(f'Moving WAXS to {waxs_arc[0]} deg')
        yield from bps.mv(waxs, waxs_arc[0])

        # Wait for the delay time to pass after the detector moved
        while (time.time() - time0) < delay:
            print(f'Waiting: {(time.time() - time0):.1f} s')
            yield from bps.sleep(1)
        
        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)
            dets = [pil900KW] if waxs.arc.position < 15 else [pil1M, pil900KW]

            sample_name = f'{name}_temp{temp}degC{get_scan_md()}'
            sample_id(user_name="MW", sample_name=sample_name)
            print(f"\n\n\n\t=== Sample: {sample_name} ===")

            yield from bp.rel_scan(dets, piezo.y, *scan_pts_y)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)
    print(f'Moving WAXS to {waxs_arc[0]} deg')
    yield from bps.mv(waxs, waxs_arc[0])


def milan_temp_2023_3(tim=0.2):
    """
    Temperature scan using resistive thermal GI stage for transmission with the hexa tilt.
    4 points per sample. For hockey pucks.

    """

    names =   ['FS_B_1','FS_B_2','FS_B_3','FS_B_4','FS_B_5','FS_B_6','FS_B_7','FS_B_8','FS_B_9','FS_B_10','FS_B_15','FS_B_16','FS_B_17','FS_B_19','FS_B_20','FS_B_21','FS_B_22','FS_B_23','FS_B_29','FS_B_30','FT_A_118','FT_B_118','FT_C_118']
    piezo_x = [  -52000,  -47700,  -44100,  -40900,   -36900,  -32900, -28700, -24900,   -21350,  -18850,    -15050,   -6550,   -3550,    -450,     3550,      9950,    15300,    19800,    24000,     28000,    33000,    37500,     43000 ]
    piezo_y = [    -3700,  -3525,  -3425,    -3575,    -3675,   -3975,  -3685,   -3655,  -3635,    -3675,       -3705,   -3675,   -3855,    -3975,    -3855,    -3855,   -4305,    -4095,   -4245,     -4275,    -4305,     -4305,     -4335 ]
    piezo_z = [   -7500,    -6500,  1500,    -4500,   -4500,    -4500,   -2000,   -4500,  -3000,    -2500,        -2500, -1000,   -1000,       -1000, -1000,   -500,    -2500,     -2500,     -2500,     -3400,     -1400,     -1400,     -1400 ]
    #piezo_z = [8400 for n in names]

    msg = "Wrong number of coordinates, check names and piezos"
    assert len(names) == len(piezo_x),   msg
    assert len(piezo_y) == len(piezo_x), msg
    assert len(piezo_y) == len(piezo_z), msg


    temperatures = [24.5]
    user_name = 'MW'
    det_exposure_time(tim, tim)

    x_offsets = [0, 50]
    y_offsets = [0, 50]
    waxs_arc = [0, 20]

    yield from engage_detectors()

    for temperature in temperatures:
        t_kelvin = temperature + 273.15
        yield from ls.output1.mv_temp(t_kelvin)

        # Activate heating range in Lakeshore
        yield from bps.mv(ls.output1.status, 3)

        # Equalise temperature
        print(f"Equalising temperature to {temperature:.0f} deg C")
        start = time.time()
        temp = ls.input_A.get()
        while abs(temp - t_kelvin) > 5:
            print("Difference: {:.1f} K".format(abs(temp - t_kelvin)))
            yield from bps.sleep(5)
            temp = ls.input_A.get()
            
            # Escape the loop if too much time passes
            if time.time() - start > 30 * 60:
                temp = t_kelvin
        
        print("Time needed to equilibrate: {:.1f} min".format((time.time() - start) / 60))

        # Wait extra time depending on temperature
        if temperature != temperatures[0]:
            wait_time = 300
            print(f'Sleeping for {wait_time} seconds')
            yield from bps.sleep(wait_time)

        for name, x, y, z in zip(names, piezo_x, piezo_y, piezo_z):
            yield from bps.mv(piezo.x, x,
                              piezo.y, y,
                              piezo.z, z)

            # Read T and convert to deg C
            temp_degC = ls.input_A.get() - 273.15
            temp = str(np.round(float(temp_degC), 1)).zfill(5)

            for wa in waxs_arc:
                yield from bps.mv(waxs, wa)
                dets = [pil900KW] if waxs.arc.position < 15 else [pil1M, pil900KW]

                for yy, y_of in enumerate(y_offsets):
                    yield from bps.mv(piezo.y, y + y_of)

                    for xx, x_of in enumerate(x_offsets):
                        yield from bps.mv(piezo.x, x + x_of)

                        loc = f'{yy}{xx}'

                        sample_name = f'{name}_temp{temp}degC{get_scan_md()}_loc{loc}'
                        sample_id(user_name=user_name, sample_name=sample_name)
                        print(f"\n\n\n\t=== Sample: {sample_name} ===")
                        yield from bp.count(dets)

        sample_id(user_name='test', sample_name='test')
        det_exposure_time(0.2, 0.2)

        t_kelvin = 25 + 273.15
        yield from ls.output1.mv_temp(t_kelvin)
        yield from ls.output1.turn_off()


def grid_milan_temp_2023_2(t=0.5):
    """
    Fine grid scan on Linkam GI thermal stage
    """
    names =   [ 'FS_C_16','FS_C_17','FS_C_19','FS_C_3','FS_C_4','FS_C_5','FT_A_104','FT_Y_104','FT_A_105', 'FT_A_113',  'FT_Y_95',      'FT_Y_96',        'FT_B_105',      'FT_B_67',        'FS_B_11',   'FS_B_12',      'FS_B_13',     'FS_B_24',    'FS_B_25',    'FS_B_31',    'FS_B_27',    'FS_B_32',    'FS_B_33',    'FS_B_35',    'FS_B_36',    'FS_B_38',    'FS_B_42',    'FS_B_39',    'FS_B_40',    'FS_B_43',    'FS_C_18',    'FS_C_28',    'FS_C_41',    'FS_C_26',    'FS_C_13']

    piezo_x = [-52950,     -48950,    -45950,   -41950,   -39950, -34950,  -30950,   -27950,    -23950,      -19950,     -16950,          -13950,          -10950,          -8450,             -4450,         -1450,         1550,          5550,        7550,         11100,       15100,        18100,           20100,        22100,       25100,        28100,      30600,        32200,         33700,       35200,         38700,      42200,45700,50200,52700]
    piezo_y = [ -3355,     -3655,    -3855,      -3555, -3810,     -4110,  -4010,   -4410,       -3910,      -3910,      -4210,            -4110,             -4110,          -4410,           -3910,        -4010,        -3810,          -3910,       -3810,         -4110,       -4010,        -4110,          -4110,       -4110,        -4210,        -4110,     -4410,         -4510,        -4510,        -4510,            -4310,-4410,-4410,-4610,-4410]
    piezo_z = [-3200,    -3200,       -3200,    -3200,    -3200,  -3200,    -3200,   -3200,     -3200,       -3200,       -3200,          -3200,           -3200,             -3200,            -3800,        -3800,          -3800,       -3800,       -3800,         -3800,       -3800,         -3800,         -3800,       -3800,        -3800,         -3800,    -1400,        -1400,           -1400,      -1400,           -800,-800,-800,-800,-800]
    #piezo_z = [8400 for n in names]
    y_range = [[0, 400, 8],[0, 300, 6],[0, 500, 10],[0, 400, 8],[0, 400, 8],[0, 400, 8],[0, 700, 14],[0, 1100, 22],[0, 500, 10],[0, 500, 10],[0, 800, 16],[0, 600, 12],[0, 500, 10],[0, 800, 16],[0, 300, 6],[0, 600, 12],[0, 200, 4],[0, 300, 6],[0, 200, 4],[0, 400, 8],[0, 300, 6],[0, 300, 6],[0, 300, 6],[0, 400, 8],[0, 400, 8],[0, 400, 8],[0, 500, 10],[0, 500, 10],[0, 500, 10],[0, 500, 10],[0, 300, 6],[0, 400, 8],[0, 400, 8],[0, 500, 10],[0, 600, 12]]
    x_range = [[0, 300, 2], [0, 300, 2],[0, 300, 2],[0, 300, 2],[0, 300, 2],[0, 300, 2],[0, 300, 2],[0, 300, 2],[0, 300, 2],[0, 300, 2],[0, 300, 2],[0, 300, 2],[0, 300, 2],[0, 300, 2],[0, 300, 2],[0, 300, 2],[0, 300, 2],[0, 300, 2],[0, 300, 2],[0, 300, 2],[0, 300, 2],[0, 300, 2],[0, 300, 2],[0, 300, 2],[0, 300, 2],[0, 300, 2],[0, 300, 2],[0, 300, 2],[0, 300, 2],[0, 300, 2],[0, 300, 2],[0, 300, 2],[0, 300, 2],[0, 300, 2],[0, 300, 2]]


    assert len(names) == len(piezo_x),   f"Wrong list lenghts 1"
    assert len(piezo_y) == len(piezo_x), f"Wrong list lenghts 2"
    assert len(piezo_y) == len(piezo_z), f"Wrong list lenghts 3"
    assert len(piezo_z) == len(y_range), f"Wrong list lenghts 4"
    assert len(y_range) == len(x_range), f"Wrong list lenghts 5"

    waxs_arc = [0, 20]
    temperatures = [28, 80, 100, 150] 
    yield from engage_detectors()

    for temperature in temperatures:
        t_kelvin = temperature + 273.15
        yield from ls.output1.mv_temp(t_kelvin)
        yield from bps.mv(ls.output1.status, 3)

        # Equalise temperature
        print(f"Equalising temperature to {temperature} deg C")
        start = time.time()
        temp = ls.input_A.get()
        while abs(temp - t_kelvin) > 5:
            print("Difference: {:.1f} K".format(abs(temp - t_kelvin)))
            yield from bps.sleep(10)
            temp = ls.input_A.get()

            # Escape the loop if too much time passes
            if time.time() - start > 30 * 60:
                temp = t_kelvin
        print(
            "Time needed to equilibrate: {:.1f} min".format((time.time() - start) / 60)
        )
        # Wait extra time depending on temperature
        if temperature != temperatures[0]:
            wait_time = 300
            print(f'Sleeping for {wait_time} seconds')
            yield from bps.sleep(wait_time)

        # Read T and convert to deg C
        temp_degC = ls.input_A.get() - 273.15

        for name, x, y, z, scan_pts_y, scan_pts_x in zip(names, piezo_x, piezo_y, piezo_z, y_range, x_range):
            yield from bps.mv(piezo.x, x,
                              piezo.y, y,
                              piezo.z, z)

            for wa in waxs_arc:
                yield from bps.mv(waxs, wa)
                dets = [pil900KW] if waxs.arc.position < 15 else [pil1M, pil900KW]
                det_exposure_time(t, t)

                e = energy.position.energy / 1000
                sdd = pil1m_pos.z.position / 1000
                temp = str(np.round(float(temp_degC), 1)).zfill(5)
                wa = waxs.arc.position + 0.001
                wa = str(np.round(float(wa), 1)).zfill(4)
                #proposal_id("2022_2", "310149_Wilborn1/%s" % name)
                name_fmt = "{sample}_{temp}degC_{energy}keV_wa{wax}_sdd{sdd}m"
                sample_name = name_fmt.format(
                    sample=name,
                    temp=temp,
                    energy="%.2f" % e,
                    wax=wa,
                    sdd="%.1f" % sdd,   
                )
                sample_name = sample_name.translate(
                    {ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ =,"}
                )
                sample_id(user_name="MW", sample_name=sample_name)
                print(f"\n\n\n\t=== Sample: {sample_name} ===")

                yield from bp.rel_grid_scan(dets, piezo.x, *scan_pts_x, piezo.y, *scan_pts_y)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)
    # Turn off the heating and set temperature to 23 deg C
    t_kelvin = 23 + 273.15
    yield from ls.output1.mv_temp(t_kelvin)
    yield from ls.output1.turn_off()


def run_linkam_temp_run_linescan_2024_1(t=0.5, temp=40, run=0, points=50):
    """
    Single point line scan on Linkam temp control
    Curation by beam controlled by exposure points

    Args:
        temp (float): Put temperature from Linkam as the function argument temp = XX,
        run (int): number ot temperature run to offset the sample position,
        points (int): number of exposures of the same point on the sample.
    """

    names =   ['MW_D_01', 'MW_D_02', 'MW_D_03', 'MW_D_04', 'MW_D_05','MW_D_06' ]
    piezo_x = [    -5800,     -900,      3100,      7500,      11500,14000, ]
    piezo_y = [    -4380,     -4500,     -4680,     -4700,     -4780, -4900, ]
    piezo_z = [     -11600,      -10400,      -11600, -11600,    -11400, -11400, ]
    #piezo_z = [8400 for n in names]
    #x_range = [[0, 0, 1],[0, 0, 1],[0, 0, 1], [0, 0, 1], [0, 0, 1]]
    x_range = [ [0, 0, points] for n in names]

    msg = "Wrong number of coordinates, check names and piezos"
    assert len(names) == len(piezo_x),   msg
    assert len(piezo_y) == len(piezo_x), msg
    assert len(piezo_y) == len(piezo_z), msg
    assert len(piezo_z) == len(x_range), msg

    offset_x = 50
    waxs_arc = [0, 20]
    det_exposure_time(t, t)
    temp = str(np.round(float(temp), 1)).zfill(5)

    for name, x, y, z, scan_pts_x in zip(names, piezo_x, piezo_y, piezo_z, x_range):
        yield from bps.mv(piezo.x, x + run * offset_x,
                          piezo.y, y,
                          piezo.z, z)

        print(f'Moving WAXS to {waxs_arc[0]} deg')
        yield from bps.mv(waxs, waxs_arc[0])
        
        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)
            dets = [pil900KW] if waxs.arc.position < 15 else [pil1M, pil900KW]

            sample_name = f'{name}_temp{temp}degC{get_scan_md()}'
            sample_id(user_name='MW', sample_name=sample_name)
            print(f"\n\n\n\t=== Sample: {sample_name} ===")

            yield from bp.rel_scan(dets, piezo.x, *scan_pts_x)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)
    print(f'Moving WAXS to {waxs_arc[0]} deg')
    yield from bps.mv(waxs, waxs_arc[0])


def milan_temp_2024_1(tim=0.5):
    """
    Temperature scan using resistive thermal GI stage for transmission with the hexa tilt.
    4 points per sample. For hockey pucks.

    """

    names =   ['KD_A_10','KD_B_10','KD_C_10','KD_E_10','FS_M_23']
    piezo_x = [  -5500,  -550,  3450,  7650,   12050,   ]
    piezo_y = [    6384,  5785,  5785,    5835,    6185 ]
    piezo_z = [   -22200,    -22200,  -22200,    -22200,   -22200  ]
    #piezo_z = [8400 for n in names]

    msg = "Wrong number of coordinates, check names and piezos"
    assert len(names) == len(piezo_x),   msg
    assert len(piezo_y) == len(piezo_x), msg
    assert len(piezo_y) == len(piezo_z), msg


    temperatures = [26]
    user_name = 'MW'
    det_exposure_time(tim, tim)

    x_offsets = [0, 50]
    y_offsets = [0, 50]
    waxs_arc = [0, 20]


    for temperature in temperatures:
        t_kelvin = temperature + 273.15
        yield from ls.output1.mv_temp(t_kelvin)

        # Activate heating range in Lakeshore
        yield from bps.mv(ls.output1.status, 3)

        # Equalise temperature
        print(f"Equalising temperature to {temperature:.0f} deg C")
        start = time.time()
        temp = ls.input_A.get()
        while abs(temp - t_kelvin) > 5:
            print("Difference: {:.1f} K".format(abs(temp - t_kelvin)))
            yield from bps.sleep(5)
            temp = ls.input_A.get()
            
            # Escape the loop if too much time passes
            if time.time() - start > 30 * 60:
                temp = t_kelvin
        
        print("Time needed to equilibrate: {:.1f} min".format((time.time() - start) / 60))

        # Wait extra time depending on temperature
        if temperature != temperatures[0]:
            wait_time = 300
            print(f'Sleeping for {wait_time} seconds')
            yield from bps.sleep(wait_time)

        for name, x, y, z in zip(names, piezo_x, piezo_y, piezo_z):
            yield from bps.mv(piezo.x, x,
                              piezo.y, y,
                              piezo.z, z)

            # Read T and convert to deg C
            temp_degC = ls.input_A.get() - 273.15
            temp = str(np.round(float(temp_degC), 1)).zfill(5)

            for wa in waxs_arc:
                yield from bps.mv(waxs, wa)
                dets = [pil900KW] if waxs.arc.position < 15 else [pil1M, pil900KW]

                for yy, y_of in enumerate(y_offsets):
                    yield from bps.mv(piezo.y, y + y_of)

                    for xx, x_of in enumerate(x_offsets):
                        yield from bps.mv(piezo.x, x + x_of)

                        loc = f'{yy}{xx}'

                        sample_name = f'{name}_temp{temp}degC{get_scan_md()}_loc{loc}'
                        sample_id(user_name=user_name, sample_name=sample_name)
                        print(f"\n\n\n\t=== Sample: {sample_name} ===")
                        yield from bp.count(dets)

        sample_id(user_name='test', sample_name='test')
        det_exposure_time(0.5, 0.5)

        t_kelvin = 25 + 273.15
        yield from ls.output1.mv_temp(t_kelvin)
        yield from ls.output1.turn_off()


def milan_temp_2024_1_1(tim=0.2):
    """
    Temperature scan using resistive thermal GI stage for transmission with the hexa tilt.
    4 points per sample. For hockey pucks.

    """

    names =   ['E7', 'E8', 'D25', 'E9', 'E10', 'D18', 'D26', 'E11', 'E12', 'F1', 'E13', 'F2', 'D11','E14', 'E15', 'MWC3','MWC2', 'MWC1', 'MWB6', 'MWB5', 'MWB4', 'MWB3', 'MWB2','MWB1', 'MWA7', 'MWA6' ,'MWA5', 'MWA4', 'MWA3', 'MWA2', 'MWA1']
    piezo_x = [-39340, -35540, -33040, -30940, -26740, -21440, -17940, -16140, -14740, -10840,-6140,  -2140 ,   860 ,  3860,   7060,  12560,  14760,  18160,  22160,  25960,28720,  31220,  34220,  36600 , 38800,  41500,  43490,  45900,  48600 , 51300,53800]
    piezo_y = [6854, 6755, 7055, 6754, 6455, 6605, 6505, 6655, 6505, 5754, 6405 ,5755 ,6255 ,6005,5905 ,6205 ,6055 ,5905 ,5805 ,5705 ,5905 ,5655, 5605, 5755, 5405, 5455 ,5705 ,5505, 5505, 5305, 5445]
    piezo_z = [-23400, -23400, -23400, -23400, -23400 ,-23400, -23400, -23400, -23400, -23400,-23400, -23400 ,-23400 ,-23400 ,-23400 ,-22600 ,-22600 ,-22600 ,-22600 ,-22600,-24200, -23600, -23600 ,-23600, -23600, -23600, -23600, -23600 ,-22600, -23400,-23400]
    #piezo_z = [8400 for n in names]

    msg = "Wrong number of coordinates, check names and piezos"
    assert len(names) == len(piezo_x),   msg
    assert len(piezo_y) == len(piezo_x), msg
    assert len(piezo_y) == len(piezo_z), msg


    temperatures = [130,160]
    user_name = 'MW'
    det_exposure_time(tim, tim)

    x_offsets = [0, 50]
    y_offsets = [0, 50]
    waxs_arc = [0, 20]

  

    for temperature in temperatures:
        t_kelvin = temperature + 273.15
        yield from ls.output1.mv_temp(t_kelvin)

        # Activate heating range in Lakeshore
        yield from bps.mv(ls.output1.status, 3)

        # Equalise temperature
        print(f"Equalising temperature to {temperature:.0f} deg C")
        start = time.time()
        temp = ls.input_A.get()
        while abs(temp - t_kelvin) > 5:
            print("Difference: {:.1f} K".format(abs(temp - t_kelvin)))
            yield from bps.sleep(5)
            temp = ls.input_A.get()
            
            # Escape the loop if too much time passes
            if time.time() - start > 30 * 60:
                temp = t_kelvin
        
        print("Time needed to equilibrate: {:.1f} min".format((time.time() - start) / 60))

        # Wait extra time depending on temperature
        if temperature != temperatures[0]:
            wait_time = 300
            print(f'Sleeping for {wait_time} seconds')
            yield from bps.sleep(wait_time)

        for name, x, y, z in zip(names, piezo_x, piezo_y, piezo_z):
            yield from bps.mv(piezo.x, x,
                              piezo.y, y,
                              piezo.z, z)

            # Read T and convert to deg C
            temp_degC = ls.input_A.get() - 273.15
            temp = str(np.round(float(temp_degC), 1)).zfill(5)

            for wa in waxs_arc:
                yield from bps.mv(waxs, wa)
                dets = [pil900KW] if waxs.arc.position < 15 else [pil1M, pil900KW]
                                                                                                                                                                                                           
                for yy, y_of in enumerate(y_offsets):
                    yield from bps.mv(piezo.y, y + y_of)

                    for xx, x_of in enumerate(x_offsets):
                        yield from bps.mv(piezo.x, x + x_of)

                        loc = f'{yy}{xx}'

                        sample_name = f'{name}_temp{temp}degC{get_scan_md()}_loc{loc}'
                        sample_id(user_name=user_name, sample_name=sample_name)
                        print(f"\n\n\n\t=== Sample: {sample_name} ===")
                        yield from bp.count(dets)

        sample_id(user_name='test', sample_name='test')
        det_exposure_time(0.2, 0.2)

        t_kelvin = 25 + 273.15
        yield from ls.output1.mv_temp(t_kelvin)
        yield from ls.output1.turn_off()


def milan_temp_grid_2024_1(tim=0.5):
    """
    Temperature scan using resistive thermal GI stage for transmission with the hexa tilt.
    4 points per sample. For hockey pucks.

    """

    proposal_id('2024_1', '312571_Wilborn_03', analysis=True)

    names =   ['RF_X_04','RF_X_03','RF_X_02','RF_X_01','RP_F_04','RP_F_03','RP_F_02','RP_F_11','RP_F_01','RP_Z_01','RP_A_02','RP_A_03','JL_A_02','JC_A_02','JR_A_02','JL_A_03','JC_A_03','JR_A_03','JL_A_04','JC_A_04','JR_A_04','JL_B_02','JC_B_02','JR_B_02','JL_B_03','JC_B_03','JR_B_03','JL_A_06','JC_A_06','JR_A_06','JL_C_02','JR_C_02']
    piezo_x = [  -49850,  -48650,  -47950,  -46650,   -43950,  -42450, -40850, -39950, -39550,  -36350,  -30350,    -22850,   21900,   23000,    24250,     28800,      30050,    31150,    33800,    35000,     36100,    39090,    40230,     41230, 44280, 45320, 46400, 50500, 51560, 52600, 56070, 57060 ]
    piezo_y = [    6930,  6930,  6390,    7130,    7230,   7280,  7305,   7180,  7280,    7235,       7185,   6860,   4035,    3985,    3985,    4035,   4035,    4035,   4035,     4035,    4035,     3735,     3735, 3735, 3635, 3635, 3635, 3685, 3685, 3685, 3455, 3455 ]
    piezo_z = [   -22600,  -22600,  -22600,    -22600,    -21400,    -21400,   -21400,   -22600,  -22600,    -20600,        -20600, -20600,   -20600,       -20600, -20600,   -20600,    -20600,     -20600,     -20600,     -20600,     -20600,     -20600,     -20600, -20600, -22200,-22200,-22200, -22200,-22200,-22200,-22200,-22200 ]
    #piezo_z = [8400 for n in names]
    y_range = [[0, 200, 4],[0, 400, 8],[0, 750, 15],[0, 50, 1],[0, 50, 1],[0, 100, 2],[0, 50, 1],[0, 100, 2],[0, 50, 1],[0, 100, 2],[0, 150, 3],[0, 50, 1],[0, 1850, 37],[0, 1900, 38],[0, 1900, 38],[0, 1750, 35],[0, 1750, 35],[0, 1750, 35],[0, 1800, 36],[0, 1800, 36],[0, 1800, 36],[0, 1900, 38],[0, 1900, 38],[0, 1900, 38],[0, 1800, 36],[0, 1800, 36],[0, 1800, 36],[0, 1650, 33],[0, 1650, 33],[0, 1650, 33],[0, 1850, 37],[0, 1850, 37]]
    x_range = [[0, 300, 6], [0, 100, 2],[0, 200, 4],[0, 50, 1],[0, 500, 10],[0, 700, 14],[0, 200, 4],[0, 500, 10],[0, 1600, 32],[0, 6000, 120],[0, 4500, 90],[0, 11000, 110],[0, 250, 5],[0, 250, 5],[0, 300, 6],[0, 350, 7],[0, 300, 6],[0, 300, 6],[0, 350, 7],[0, 300, 6],[0, 300, 6],[0, 250, 5],[0, 300, 6],[0, 300, 6],[0, 250, 5],[0, 300, 6],[0, 300, 6],[0, 200, 4],[0, 250, 5],[0, 350, 7],[0, 200, 4],[0, 300, 6]]


    msg = "Wrong number of coordinates, check names and piezos"
    assert len(names) == len(piezo_x),   msg
    assert len(piezo_y) == len(piezo_x), msg
    assert len(piezo_y) == len(piezo_z), msg
    assert len(y_range) == len(piezo_z), msg
    assert len(piezo_y) == len(x_range), msg


    temperatures = [25]
    user_name = 'MW'
    det_exposure_time(tim, tim)
    waxs_arc = [0, 20]

    for temperature in temperatures:
        t_kelvin = temperature + 273.15
        yield from ls.output1.mv_temp(t_kelvin)

        # Activate heating range in Lakeshore
        yield from bps.mv(ls.output1.status, 3)

        # Equalise temperature
        print(f"Equalising temperature to {temperature:.0f} deg C")
        start = time.time()
        temp = ls.input_A.get()
        while abs(temp - t_kelvin) > 10:
            print("Difference: {:.1f} K".format(abs(temp - t_kelvin)))
            yield from bps.sleep(5)
            temp = ls.input_A.get()
            
            # Escape the loop if too much time passes
            if time.time() - start > 30 * 60:
                temp = t_kelvin
        
        print("Time needed to equilibrate: {:.1f} min".format((time.time() - start) / 60))

        # Wait extra time depending on temperature
        if temperature != temperatures[0]:
            wait_time = 10
            print(f'Sleeping for {wait_time} seconds')
            yield from bps.sleep(wait_time)

        for name, x, y, z, scan_pts_y, scan_pts_x in zip(names, piezo_x, piezo_y, piezo_z, y_range, x_range):
            yield from bps.mv(piezo.x, x,
                              piezo.y, y,
                              piezo.z, z)

            # Read T and convert to deg C
            temp_degC = ls.input_A.get() - 273.15
            temp = str(np.round(float(temp_degC), 1)).zfill(5)

            for wa in waxs_arc:
                yield from bps.mv(waxs, wa)
                dets = [pil900KW] if waxs.arc.position < 15 else [pil1M, pil900KW]

                sample_name = f'{name}_temp{temp}degC{get_scan_md()}'
                sample_id(user_name=user_name, sample_name=sample_name)
                print(f"\n\n\n\t=== Sample: {sample_name} ===")
                yield from bp.rel_grid_scan(dets, piezo.x, *scan_pts_x, piezo.y, *scan_pts_y)

        sample_id(user_name='test', sample_name='test')
        det_exposure_time(0.2, 0.2)

        t_kelvin = 25 + 273.15
        yield from ls.output1.mv_temp(t_kelvin)
        yield from ls.output1.turn_off()



def milan_temp_grid_2024_1_1(tim=0.5):
    """
    Temperature scan using resistive thermal GI stage for transmission with the hexa tilt.
    4 points per sample. For hockey pucks.

    """

    proposal_id('2024_1', '312571_Wilborn_03', analysis=True)

    names =   ['JL_A_02','JC_A_02','JR_A_02','JL_A_03','JC_A_03','JR_A_03','JL_A_04','JC_A_04','JR_A_04','JL_B_02','JC_B_02','JR_B_02','JL_B_03','JC_B_03','JR_B_03','JL_A_06','JC_A_06','JR_A_06','JL_C_02','JR_C_02']
    piezo_x = [ 21900,   23000,    24250,     28800,      30050,    31150,    33800,    35000,     36100,    39090,    40230,     41230, 44280, 45320, 46400, 50500, 51560, 52600, 56070, 57060 ]
    piezo_y = [ 4960,    4935,    4935,    4910,   4910,    4910,   4935,     4935,    4935,     4685,     4685, 4685, 4535, 4535, 4535, 4500, 4500, 4500, 4380, 4380 ]
    piezo_z = [ -20600,       -20600, -20600,   -20600,    -20600,     -20600,     -20600,     -20600,     -20600,     -20600,     -20600, -20600, -22200,-22200,-22200, -22200,-22200,-22200,-22200,-22200 ]
    #piezo_z = [8400 for n in names]
    #y_range = [[0, 200, 4],[0, 400, 8],[0, 750, 15],[0, 50, 1],[0, 50, 1],[0, 100, 2],[0, 50, 1],[0, 100, 2],[0, 50, 1],[0, 100, 2],[0, 150, 3],[0, 50, 1],[0, 1850, 37],[0, 1900, 38],[0, 1900, 38],[0, 1750, 35],[0, 1750, 35],[0, 1750, 35],[0, 1800, 36],[0, 1800, 36],[0, 1800, 36],[0, 1900, 38],[0, 1900, 38],[0, 1900, 38],[0, 1800, 36],[0, 1800, 36],[0, 1800, 36],[0, 1650, 33],[0, 1650, 33],[0, 1650, 33],[0, 1850, 37],[0, 1850, 37]]
    x_range = [[0, 250, 5],[0, 250, 5],[0, 300, 6],[0, 350, 7],[0, 300, 6],[0, 300, 6],[0, 350, 7],[0, 300, 6],[0, 300, 6],[0, 250, 5],[0, 300, 6],[0, 300, 6],[0, 250, 5],[0, 300, 6],[0, 300, 6],[0, 200, 4],[0, 250, 5],[0, 350, 7],[0, 200, 4],[0, 300, 6]]


    msg = "Wrong number of coordinates, check names and piezos"
    assert len(names) == len(piezo_x),   msg
    assert len(piezo_y) == len(piezo_x), msg
    assert len(piezo_y) == len(piezo_z), msg
   # assert len(y_range) == len(piezo_z), msg
    assert len(piezo_y) == len(x_range), msg


    temperatures = [25]
    user_name = 'MW'
    det_exposure_time(tim, tim)
    waxs_arc = [0, 20]

    for temperature in temperatures:
        t_kelvin = temperature + 273.15
        yield from ls.output1.mv_temp(t_kelvin)

        # Activate heating range in Lakeshore
        yield from bps.mv(ls.output1.status, 3)

        # Equalise temperature
        print(f"Equalising temperature to {temperature:.0f} deg C")
        start = time.time()
        temp = ls.input_A.get()
        while abs(temp - t_kelvin) > 10:
            print("Difference: {:.1f} K".format(abs(temp - t_kelvin)))
            yield from bps.sleep(5)
            temp = ls.input_A.get()
            
            # Escape the loop if too much time passes
            if time.time() - start > 30 * 60:
                temp = t_kelvin
        
        print("Time needed to equilibrate: {:.1f} min".format((time.time() - start) / 60))

        # Wait extra time depending on temperature
        if temperature != temperatures[0]:
            wait_time = 10
            print(f'Sleeping for {wait_time} seconds')
            yield from bps.sleep(wait_time)

        for name, x, y, z, scan_pts_x in zip(names, piezo_x, piezo_y, piezo_z, x_range):
            yield from bps.mv(piezo.x, x,
                              piezo.y, y,
                              piezo.z, z)

            # Read T and convert to deg C
            temp_degC = ls.input_A.get() - 273.15
            temp = str(np.round(float(temp_degC), 1)).zfill(5)

            for wa in waxs_arc:
                yield from bps.mv(waxs, wa)
                dets = [pil900KW] if waxs.arc.position < 15 else [pil1M, pil900KW]

                sample_name = f'{name}_temp{temp}degC{get_scan_md()}'
                sample_id(user_name=user_name, sample_name=sample_name)
                print(f"\n\n\n\t=== Sample: {sample_name} ===")
                yield from bp.rel_grid_scan(dets, piezo.x, *scan_pts_x)

        sample_id(user_name='test', sample_name='test')
        det_exposure_time(0.2, 0.2)

        t_kelvin = 25 + 273.15
        yield from ls.output1.mv_temp(t_kelvin)
        yield from ls.output1.turn_off()

        ######################################################################

def milan_Jacopo(tim=0.5):
    """
    Linescan in 'y' bc Jacopo is stupid.

    """

    proposal_id('2024_1', '312571_Wilborn_03', analysis=True)

    names =   ['IC_B_03','IR_B_03','IL_A_06','IC_A_06','IR_A_06','IL_C_02','IR_C_02']
    piezo_x = [  45600, 46700, 50700, 51810, 52950, 56250, 57360 ]
    piezo_y = [  3635, 3635, 3685, 3685, 3685, 3455, 3455 ]
    piezo_z = [-22200,-22200, -22200,-22200,-22200,-22200,-22200]
    #piezo_z = [8400 for n in names]
    y_range = [[0, 1800, 36],[0, 1800, 36],[0, 1650, 33],[0, 1650, 33],[0, 1650, 33],[0, 1850, 37],[0, 1850, 37]]
    #x_range = [[0, 300, 6], [0, 100, 2],[0, 200, 4],[0, 50, 1],[0, 500, 10],[0, 700, 14],[0, 200, 4],[0, 500, 10],[0, 1600, 32],[0, 6000, 120],[0, 4500, 90],[0, 11000, 110],[0, 250, 5],[0, 250, 5],[0, 300, 6],[0, 350, 7],[0, 300, 6],[0, 300, 6],[0, 350, 7],[0, 300, 6],[0, 300, 6],[0, 250, 5],[0, 300, 6],[0, 300, 6],[0, 250, 5],[0, 300, 6],[0, 300, 6],[0, 200, 4],[0, 250, 5],[0, 350, 7],[0, 200, 4],[0, 300, 6]]


    msg = "Wrong number of coordinates, check names and piezos"
    assert len(names) == len(piezo_x),   msg
    assert len(piezo_y) == len(piezo_x), msg
    assert len(piezo_y) == len(piezo_z), msg
    assert len(y_range) == len(piezo_z), msg
    #assert len(piezo_y) == len(x_range), msg


    temperatures = [25]
    user_name = 'MW'
    det_exposure_time(tim, tim)
    waxs_arc = [0, 20]

    for temperature in temperatures:
        t_kelvin = temperature + 273.15
        yield from ls.output1.mv_temp(t_kelvin)

        # Activate heating range in Lakeshore
        yield from bps.mv(ls.output1.status, 3)

        # Equalise temperature
        print(f"Equalising temperature to {temperature:.0f} deg C")
        start = time.time()
        temp = ls.input_A.get()
        while abs(temp - t_kelvin) > 10:
            print("Difference: {:.1f} K".format(abs(temp - t_kelvin)))
            yield from bps.sleep(5)
            temp = ls.input_A.get()
            
            # Escape the loop if too much time passes
            if time.time() - start > 30 * 60:
                temp = t_kelvin
        
        print("Time needed to equilibrate: {:.1f} min".format((time.time() - start) / 60))

        # Wait extra time depending on temperature
        if temperature != temperatures[0]:
            wait_time = 10
            print(f'Sleeping for {wait_time} seconds')
            yield from bps.sleep(wait_time)

        for name, x, y, z, scan_pts_y, in zip(names, piezo_x, piezo_y, piezo_z, y_range):
            yield from bps.mv(piezo.x, x,
                              piezo.y, y,
                              piezo.z, z)

            # Read T and convert to deg C
            temp_degC = ls.input_A.get() - 273.15
            temp = str(np.round(float(temp_degC), 1)).zfill(5)

            for wa in waxs_arc:
                yield from bps.mv(waxs, wa)
                dets = [pil900KW] if waxs.arc.position < 15 else [pil1M, pil900KW]

                sample_name = f'{name}_temp{temp}degC{get_scan_md()}'
                sample_id(user_name=user_name, sample_name=sample_name)
                print(f"\n\n\n\t=== Sample: {sample_name} ===")
                yield from bp.rel_grid_scan(dets, piezo.y, *scan_pts_y)

        sample_id(user_name='test', sample_name='test')
        det_exposure_time(0.2, 0.2)

        t_kelvin = 25 + 273.15
        yield from ls.output1.mv_temp(t_kelvin)
        yield from ls.output1.turn_off()

def milan_temp_2024_1_fix(tim=0.2):
    """
    Temperature scan using resistive thermal GI stage for transmission with the hexa tilt.
    4 points per sample. For hockey pucks.

    """

    names =   ['CB_5_01','CB_8_01','FT_A_27' ]
    piezo_x = [-6350,650,8650]
    piezo_y = [-6375,-6775,-7175 ]
    piezo_z = [-14800,-19600,-21800]
    #piezo_z = [8400 for n in names]

    msg = "Wrong number of coordinates, check names and piezos"
    assert len(names) == len(piezo_x),   msg
    assert len(piezo_y) == len(piezo_x), msg
    assert len(piezo_y) == len(piezo_z), msg


    temperatures = [30,40,60]
    user_name = 'MW'
    det_exposure_time(tim, tim)

    x_offsets = [0, 50]
    y_offsets = [0, 50]
    waxs_arc = [0, 20]

  

    for temperature in temperatures:
        t_kelvin = temperature + 273.15
        yield from ls.output1.mv_temp(t_kelvin)

        # Activate heating range in Lakeshore
        yield from bps.mv(ls.output1.status, 3)

        # Equalise temperature
        print(f"Equalising temperature to {temperature:.0f} deg C")
        start = time.time()
        temp = ls.input_A.get()
        while abs(temp - t_kelvin) > 5:
            print("Difference: {:.1f} K".format(abs(temp - t_kelvin)))
            yield from bps.sleep(5)
            temp = ls.input_A.get()
            
            # Escape the loop if too much time passes
            if time.time() - start > 30 * 60:
                temp = t_kelvin
        
        print("Time needed to equilibrate: {:.1f} min".format((time.time() - start) / 60))

        # Wait extra time depending on temperature
        if temperature != temperatures[0]:
            wait_time = 60
            print(f'Sleeping for {wait_time} seconds')
            yield from bps.sleep(wait_time)

        for name, x, y, z in zip(names, piezo_x, piezo_y, piezo_z):
            yield from bps.mv(piezo.x, x,
                              piezo.y, y,
                              piezo.z, z)

            # Read T and convert to deg C
            temp_degC = ls.input_A.get() - 273.15
            temp = str(np.round(float(temp_degC), 1)).zfill(5)

            for wa in waxs_arc:
                yield from bps.mv(waxs, wa)
                dets = [pil900KW] if waxs.arc.position < 15 else [pil1M, pil900KW]
                                                                                                                                                                                                           
                for yy, y_of in enumerate(y_offsets):
                    yield from bps.mv(piezo.y, y + y_of)

                    for xx, x_of in enumerate(x_offsets):
                        yield from bps.mv(piezo.x, x + x_of)

                        loc = f'{yy}{xx}'

                        sample_name = f'{name}_temp{temp}degC{get_scan_md()}_loc{loc}'
                        sample_id(user_name=user_name, sample_name=sample_name)
                        print(f"\n\n\n\t=== Sample: {sample_name} ===")
                        yield from bp.count(dets)

        sample_id(user_name='test', sample_name='test')
        det_exposure_time(0.2, 0.2)

        t_kelvin = 25 + 273.15
        yield from ls.output1.mv_temp(t_kelvin)
        yield from ls.output1.turn_off()


def milan_single_measurement_2024_2(name='FT_I_01_90C_1', t_frame=0.2, t_tot=0.2):

    """
    As the name says, set coordinates via CSS, then take data
    WAXS only
    """

    det_exposure_time_old(t_frame, t_tot)
    waxs_arc = [0] # Set 20 for SAXS

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)
        dets = [pil900KW] if waxs.arc.position < 15 else [pil1M, pil900KW]

        sample_name = f'{name}_{get_scan_md()}_loc00'
        sample_id(user_name='MW', sample_name=sample_name)
        print(f"\n\n\n\t=== Sample: {sample_name} ===")
        yield from bp.count(dets)

    sample_id(user_name='test', sample_name='test')
    det_exposure_time(0.2, 0.2)

def milan_temp_2024_3_fix(tim=0.2):
    """
    Temperature scan using resistive thermal GI stage for transmission with the hexa tilt.
    4 points per sample. For hockey pucks.

    """

    names =   ['RP_G_04','RP_G_03','RP_G_02','RP_G_01','FS_F_19','FS_F_20','FS_F_17','FS_F_18','FS_F_22','FS_F_23','FS_F_24','FS_F_25','FS_F_26','FS_F_27','FS_F_28','FS_F_29','FS_F_30','FS_F_31','FS_F_32','FS_F_33','FS_F_34' ]
    piezo_x = [-50220,-44220,-40220,-36720,-31220,-26720,-23220,-18720,-13720,-8720,-4220,780,6280,13280,15780,21780,24880,29880,36380,46880,51880]
    piezo_y = [-9090,-9140,-9140,-9190,-9415,-9465,-9390,-9390,-9365,-9365,-9465,-9340,-9340,-9515,-9440,-9390,-9265,-9140,-8990,-9090,-9090 ]
    piezo_z = [-8900,-8900,-8900,-8900,-9300,-9300,-9300,-9300,-9300,-9300,-9300,-9300,-9300,-9300,-8100,-7700,-7700,-7700,-7700,-7700,-7700]
    #piezo_z = [8400 for n in names]

    msg = "Wrong number of coordinates, check names and piezos"
    assert len(names) == len(piezo_x),   msg
    assert len(piezo_y) == len(piezo_x), msg
    assert len(piezo_y) == len(piezo_z), msg


    temperatures = [80,140]
    user_name = 'MW'
    det_exposure_time(tim, tim)

    x_offsets = [0, 50]
    y_offsets = [0, 50]
    waxs_arc = [0, 20]

  

    for temperature in temperatures:
        t_kelvin = temperature + 273.15
        yield from ls.output1.mv_temp(t_kelvin)

        # Activate heating range in Lakeshore
        yield from bps.mv(ls.output1.status, 3)

        # Equalise temperature
        print(f"Equalising temperature to {temperature:.0f} deg C")
        start = time.time()
        temp = ls.input_A.get()
        while abs(temp - t_kelvin) > 5:
            print("Difference: {:.1f} K".format(abs(temp - t_kelvin)))
            yield from bps.sleep(5)
            temp = ls.input_A.get()
            
            # Escape the loop if too much time passes
            if time.time() - start > 30 * 60:
                temp = t_kelvin
        
        print("Time needed to equilibrate: {:.1f} min".format((time.time() - start) / 60))

        # Wait extra time depending on temperature
        if temperature != temperatures[0]:
            wait_time = 60
            print(f'Sleeping for {wait_time} seconds')
            yield from bps.sleep(wait_time)

        for name, x, y, z in zip(names, piezo_x, piezo_y, piezo_z):
            yield from bps.mv(piezo.x, x,
                              piezo.y, y,
                              piezo.z, z)

            # Read T and convert to deg C
            temp_degC = ls.input_A.get() - 273.15
            temp = str(np.round(float(temp_degC), 1)).zfill(5)

            for wa in waxs_arc:
                yield from bps.mv(waxs, wa)
                dets = [pil900KW] if waxs.arc.position < 15 else [pil1M, pil900KW]
                                                                                                                                                                                                           
                for yy, y_of in enumerate(y_offsets):
                    yield from bps.mv(piezo.y, y + y_of)

                    for xx, x_of in enumerate(x_offsets):
                        yield from bps.mv(piezo.x, x + x_of)

                        loc = f'{yy}{xx}'

                        sample_name = f'{name}_temp{temp}degC{get_scan_md()}_loc{loc}'
                        sample_id(user_name=user_name, sample_name=sample_name)
                        print(f"\n\n\n\t=== Sample: {sample_name} ===")
                        yield from bp.count(dets)

        sample_id(user_name='test', sample_name='test')
        det_exposure_time(0.2, 0.2)

        t_kelvin = 25 + 273.15
        yield from ls.output1.mv_temp(t_kelvin)
        yield from ls.output1.turn_off()
def milan_temp_2024_3_fixed(tim=0.2):
    """
    Temperature scan using resistive thermal GI stage for transmission with the hexa tilt.
    4 points per sample. For hockey pucks.

    """

    names =   ['FS_G_28']
    piezo_x = [15780]
    piezo_y = [-9440]
    piezo_z = [-8100]
    #piezo_z = [8400 for n in names]

    msg = "Wrong number of coordinates, check names and piezos"
    assert len(names) == len(piezo_x),   msg
    assert len(piezo_y) == len(piezo_x), msg
    assert len(piezo_y) == len(piezo_z), msg


    temperatures = [30]
    user_name = 'MW'
    det_exposure_time(tim, tim)

    x_offsets = [0, 50]
    y_offsets = [0, 50]
    waxs_arc = [0, 20]

  

    for temperature in temperatures:
        t_kelvin = temperature + 273.15
        yield from ls.output1.mv_temp(t_kelvin)

        # Activate heating range in Lakeshore
        yield from bps.mv(ls.output1.status, 3)

        # Equalise temperature
        print(f"Equalising temperature to {temperature:.0f} deg C")
        start = time.time()
        temp = ls.input_A.get()
        while abs(temp - t_kelvin) > 5:
            print("Difference: {:.1f} K".format(abs(temp - t_kelvin)))
            yield from bps.sleep(5)
            temp = ls.input_A.get()
            
            # Escape the loop if too much time passes
            if time.time() - start > 30 * 60:
                temp = t_kelvin
        
        print("Time needed to equilibrate: {:.1f} min".format((time.time() - start) / 60))

        # Wait extra time depending on temperature
        if temperature != temperatures[0]:
            wait_time = 60
            print(f'Sleeping for {wait_time} seconds')
            yield from bps.sleep(wait_time)

        for name, x, y, z in zip(names, piezo_x, piezo_y, piezo_z):
            yield from bps.mv(piezo.x, x,
                              piezo.y, y,
                              piezo.z, z)

            # Read T and convert to deg C
            temp_degC = ls.input_A.get() - 273.15
            temp = str(np.round(float(temp_degC), 1)).zfill(5)

            for wa in waxs_arc:
                yield from bps.mv(waxs, wa)
                dets = [pil900KW] if waxs.arc.position < 15 else [pil1M, pil900KW]
                                                                                                                                                                                                           
                for yy, y_of in enumerate(y_offsets):
                    yield from bps.mv(piezo.y, y + y_of)

                    for xx, x_of in enumerate(x_offsets):
                        yield from bps.mv(piezo.x, x + x_of)

                        loc = f'{yy}{xx}'

                        sample_name = f'{name}_temp{temp}degC{get_scan_md()}_loc{loc}'
                        sample_id(user_name=user_name, sample_name=sample_name)
                        print(f"\n\n\n\t=== Sample: {sample_name} ===")
                        yield from bp.count(dets)

        sample_id(user_name='test', sample_name='test')
        det_exposure_time(0.2, 0.2)

        t_kelvin = 25 + 273.15
        yield from ls.output1.mv_temp(t_kelvin)
        yield from ls.output1.turn_off()        


def milan_temp_2024_3_highrestemp(tim=0.2):
    """
    Temperature scan using resistive thermal GI stage for transmission with the hexa tilt.
    4 points per sample. For hockey pucks.

    """
    names =   ['FS_Y_23','FS_Y_17','FS_Y_08','FS_Y_29','FS_Y_91','FS_Y_01','FS_Y_02','FS_Y_03','MW_Q_01']
    piezo_x = [-29945,-26945,-23945,-18945,-13945,-4945,-2445,655,10655]
    piezo_y = [-8325,-8400,-8400,-8425,-8325,-8575,-8575,-8700,-8625]
    piezo_z = [-12300,-12300,-12300,-12300,-12300,-12300,-12300,-12300,-10050]
    #piezo_z = [8400 for n in names]
    
    """names =   ['FT_A_04','FT_A_05','FT_A_06','FT_A_07','FT_A_08','FT_A_09','FT_A_10','FT_A_11','FT_A_12','FT_A_13','FT_A_14',]
    piezo_x = [4780,8780,13280,17780,23280,27280,31280,35280,38780,43780,51280]
    piezo_y = [-9590,-9590,-9590,-9640,-9465,-9465,-9465,-9465,-9390,-8515,-9290]
    piezo_z = [-9400,-8400,-8400,-8400,-7600,-7600,-7600,-7600,-6800,-700,-6700]
    #piezo_z = [8400 for n in names]"""

    msg = "Wrong number of coordinates, check names and piezos"
    assert len(names) == len(piezo_x),   msg
    assert len(piezo_y) == len(piezo_x), msg
    assert len(piezo_y) == len(piezo_z), msg


    temperatures = [30,40,50,60,70,80,90,110,120,130,140,160,180]
    user_name = 'MW'
    det_exposure_time(tim, tim)

    x_offsets = [0, 75]
    y_offsets = [0, 75]
    waxs_arc = [0, 20]

  

    for temperature in temperatures:
        t_kelvin = temperature + 273.15
        yield from ls.output1.mv_temp(t_kelvin)

        # Activate heating range in Lakeshore
        yield from bps.mv(ls.output1.status, 3)

        # Equalise temperature
        print(f"Equalising temperature to {temperature:.0f} deg C")
        start = time.time()
        temp = ls.input_A.get()
        while abs(temp - t_kelvin) > 3:
            print("Difference: {:.1f} K".format(abs(temp - t_kelvin)))
            yield from bps.sleep(5)
            temp = ls.input_A.get()
            
            # Escape the loop if too much time passes
            if time.time() - start > 30 * 60:
                temp = t_kelvin
        
        print("Time needed to equilibrate: {:.1f} min".format((time.time() - start) / 60))

        # Wait extra time depending on temperature
        if temperature != temperatures[0]:
            wait_time = 60
            print(f'Sleeping for {wait_time} seconds')
            yield from bps.sleep(wait_time)

        for name, x, y, z in zip(names, piezo_x, piezo_y, piezo_z):
            yield from bps.mv(piezo.x, x,
                              piezo.y, y,
                              piezo.z, z)

            # Read T and convert to deg C
            temp_degC = ls.input_A.get() - 273.15
            temp = str(np.round(float(temp_degC), 1)).zfill(5)

            for wa in waxs_arc:
                yield from bps.mv(waxs, wa)
                dets = [pil900KW] if waxs.arc.position < 15 else [pil1M, pil900KW]
                                                                                                                                                                                                           
                for yy, y_of in enumerate(y_offsets):
                    yield from bps.mv(piezo.y, y + y_of)

                    for xx, x_of in enumerate(x_offsets):
                        yield from bps.mv(piezo.x, x + x_of)

                        loc = f'{yy}{xx}'

                        sample_name = f'{name}_temp{temp}degC{get_scan_md()}_loc{loc}'
                        sample_id(user_name=user_name, sample_name=sample_name)
                        print(f"\n\n\n\t=== Sample: {sample_name} ===")
                        yield from bp.count(dets)

        sample_id(user_name='test', sample_name='test')
        det_exposure_time(0.2, 0.2)

        t_kelvin = 25 + 273.15
        yield from ls.output1.mv_temp(t_kelvin)
        yield from ls.output1.turn_off()


def milan_temp_grid_2024_1_1(tim=0.2):
    """
        Xscan

    """

    names =   ['FS_G_90','FS_G_91','FS_G_92','MW_G_01','MW_G_02','FS_G_04','FS_G_05','FS_G_32','FS_G_34']
    piezo_x = [-52120,-41220,-31920,-19320,-5820,7780,20480,31780,45780]
    piezo_y = [-9040,-9140,-9140,-9040,-8990,-8990,-8865,-8940,-9065 ]
    piezo_z = [ -11800, -11800, -11800,  -10100, -10100,-7900,-6200,-6200,-6200]
    
    #piezo_z = [8400 for n in names]
    #y_range = [[0, 200, 4],[0, 400, 8],[0, 750, 15],[0, 50, 1],[0, 50, 1],[0, 100, 2],[0, 50, 1],[0, 100, 2],[0, 50, 1],[0, 100, 2],[0, 150, 3],[0, 50, 1],[0, 1850, 37],[0, 1900, 38],[0, 1900, 38],[0, 1750, 35],[0, 1750, 35],[0, 1750, 35],[0, 1800, 36],[0, 1800, 36],[0, 1800, 36],[0, 1900, 38],[0, 1900, 38],[0, 1900, 38],[0, 1800, 36],[0, 1800, 36],[0, 1800, 36],[0, 1650, 33],[0, 1650, 33],[0, 1650, 33],[0, 1850, 37],[0, 1850, 37]]
    x_range = [[0, 9600, 193],[0, 7500, 151],[0, 9600, 193],[0, 10400, 209],[0, 11299, 227],[0, 11000, 221],[0, 8200,165],[0, 12000, 241],[0, 10000, 201]]


    msg = "Wrong number of coordinates, check names and piezos"
    assert len(names) == len(piezo_x),   msg
    assert len(piezo_y) == len(piezo_x), msg
    assert len(piezo_y) == len(piezo_z), msg
   # assert len(y_range) == len(piezo_z), msg
    assert len(piezo_y) == len(x_range), msg


    temperatures = [25]
    user_name = 'MW'
    det_exposure_time(tim, tim)
    waxs_arc = [0, 20]

    for temperature in temperatures:
        t_kelvin = temperature + 273.15
        yield from ls.output1.mv_temp(t_kelvin)

        # Activate heating range in Lakeshore
        yield from bps.mv(ls.output1.status, 3)

        # Equalise temperature
        print(f"Equalising temperature to {temperature:.0f} deg C")
        start = time.time()
        temp = ls.input_A.get()
        while abs(temp - t_kelvin) > 10:
            print("Difference: {:.1f} K".format(abs(temp - t_kelvin)))
            yield from bps.sleep(5)
            temp = ls.input_A.get()
            
            # Escape the loop if too much time passes
            if time.time() - start > 30 * 60:
                temp = t_kelvin
        
        print("Time needed to equilibrate: {:.1f} min".format((time.time() - start) / 60))

        # Wait extra time depending on temperature
        if temperature != temperatures[0]:
            wait_time = 10
            print(f'Sleeping for {wait_time} seconds')
            yield from bps.sleep(wait_time)

        for name, x, y, z, scan_pts_x in zip(names, piezo_x, piezo_y, piezo_z, x_range):
            yield from bps.mv(piezo.x, x,
                              piezo.y, y,
                              piezo.z, z)

            # Read T and convert to deg C
            temp_degC = ls.input_A.get() - 273.15
            temp = str(np.round(float(temp_degC), 1)).zfill(5)

            for wa in waxs_arc:
                yield from bps.mv(waxs, wa)
                dets = [pil900KW] if waxs.arc.position < 15 else [pil1M, pil900KW]

                sample_name = f'{name}_temp{temp}degC{get_scan_md()}'
                sample_id(user_name=user_name, sample_name=sample_name)
                print(f"\n\n\n\t=== Sample: {sample_name} ===")
                yield from bp.rel_grid_scan(dets, piezo.x, *scan_pts_x)

        sample_id(user_name='test', sample_name='test')
        #det_exposure_time(0.2, 0.2)

        t_kelvin = 25 + 273.15
        yield from ls.output1.mv_temp(t_kelvin)
        yield from ls.output1.turn_off()

        ######################################################################
def milan_single_measurement_2024_3(name='', t_frame=0.1, t_tot=10):

    """
    As the name says, set coordinates via CSS, then take data
    WAXS only
    """
    det_exposure_time(t_frame, t_tot, period_delay=0.005)
    # det_exposure_time_old(t_frame, t_tot)
    yield from bps.sleep(1)
    waxs_arc = [0] # Set 20 for SAXS

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)
        dets = [pil900KW] if waxs.arc.position < 15 else [pil1M, pil900KW]

        sample_name = f'{name}_{get_scan_md()}_loc00'
        sample_id(user_name='MW', sample_name=sample_name)
        print(f"\n\n\n\t=== Sample: {sample_name} ===")
        yield from bp.count(dets)

    sample_id(user_name='test', sample_name='test')
    #det_exposure_time(0.2, 0.2)

def milan_single_measurement_2024_3(name='FT_I_01-90C', t_frame=0.2, t_tot=0.2):

    """
    As the name says, set coordinates via CSS, then take data
    WAXS only

    This one is working, above does not at the moment
    """
    det_exposure_time(t_frame, t_tot, period_delay=0.005)
    # det_exposure_time_old(t_frame, t_tot)
    yield from bps.sleep(1)

    dets = [pil900KW] if waxs.arc.position < 15 else [pil1M, pil900KW]

    sample_name = f'{name}_{get_scan_md()}_loc00'
    sample_id(user_name='MW', sample_name=sample_name)
    print(f"\n\n\n\t=== Sample: {sample_name} ===")
    yield from bp.count(dets)

    sample_id(user_name='test', sample_name='test')
    det_exposure_time(0.2, 0.2)


def milan_temp_2024_3_highrestemp(tim=0.2):
    """
    Temperature scan using resistive thermal GI stage for transmission with the hexa tilt.
    4 points per sample. For hockey pucks.


    names =   ['FS_R_01','FS_R_02','FS_R_03','FS_R_04','FS_R_05','FS_R_06','FS_R_07','FS_R_08','FS_R_09','FS_R_10','FS_R_11','FS_R_12','FS_R_13','FS_R_14','FS_R_15','FS_R_16','FS_R_17','FS_R_18','FS_R_19','FS_R_20','FS_R_21','FS_R_22','FS_R_23','FS_R_24','FS_R_25']
    piezo_x = [-51950,-48050,-44850,-37850, -32350, -27150, -22950, -14950, -12450, -8950, -5150, -2650, -650, 3350, 8350, 11800, 16350, 19350, 25850, 31950, 34200, 38200, 43200, 48200, 52950]
    piezo_y = [-10450,-10450,-10350,-10200, -9923, -9923, -9898, -9898, -9773, -9573, -9573, -9273, -9500, -9500, -9500, -9500, -9223, -9400, -9400, -9075, -9075, -9000, -9225, -8800, -8373]
    piezo_z = [-13500, -13500, -13500, -11300, -10100, -12100, -11100, -10500, -9700, -10300, -10300, -8700, -8700, -8700, -8700, -8700, -8700, -8700, -8700, -7100, -7100, -7100, -6100, -6100, -4900]
    #piezo_z = [8400 for n in names]
     """
     
    names =   ['FT_B_02','FT_A_47','FT_B_45','FT_C_45','FT_A_03','FT_A_06','FT_B_07','FT_B_03','FT_C_03','FT_B_06','FT_A_05', 'FT_A_08', 'FT_B_53','FT_B_08', 'FT_A_07', 'FT_A_04', 'FT_D_04','FT_A_01', 'FT_A_02', 'FT_C_04', 'FT_B_04']
    piezo_x = [52350, 48525, 44325, 39325, 34325, 30125, 25325, 20725, 15925, 9925, 6125, -875, -4475, -9475, -14475, -20275, -26075, -29475, -34375, -40925, -44925]
    piezo_y = [-8623, -8823, -8773, -8698, -8673, -8848, -8923, -8973, -9048, -9298, -9473, -9473, -9673, -9723, -9948, -9948, -10098, -10023, -10373, -10423, -10323]
    piezo_z = [-7000, -7000, -8400, -7800, -8200, -8200, -7200, -7200, -7200, -7200, -8400, -8400, -8800, -9400, -9800, -10000, -10200, -10800, -10800, -11600, -11600]
    #piezo_z = [8400 for n in names]"""

    msg = "Wrong number of coordinates, check names and piezos"
    assert len(names) == len(piezo_x),   msg
    assert len(piezo_y) == len(piezo_x), msg
    assert len(piezo_y) == len(piezo_z), msg


    # temperatures = [30,40,50,60,70,80,90,100,110,130,140,160,180,200]
    temperatures = [100,250]
    user_name = 'MW'
    det_exposure_time(tim, tim)

    x_offsets = [0, 75]
    y_offsets = [0, 75]
    waxs_arc = [0, 20]

  

    for temperature in temperatures:
        t_kelvin = temperature + 273.15
        yield from ls.output1.mv_temp(t_kelvin)

        # Activate heating range in Lakeshore
        yield from bps.mv(ls.output1.status, 3)

        # Equalise temperature
        print(f"Equalising temperature to {temperature:.0f} deg C")
        start = time.time()
        temp = ls.input_A.get()
        while abs(temp - t_kelvin) > 3:
            print("Difference: {:.1f} K".format(abs(temp - t_kelvin)))
            yield from bps.sleep(5)
            temp = ls.input_A.get()
            
            # Escape the loop if too much time passes
            if time.time() - start > 30 * 60:
                temp = t_kelvin
        
        print("Time needed to equilibrate: {:.1f} min".format((time.time() - start) / 60))

        # Wait extra time depending on temperature
        if temperature != temperatures[0]:
            wait_time = 60
            print(f'Sleeping for {wait_time} seconds')
            yield from bps.sleep(wait_time)

        for name, x, y, z in zip(names, piezo_x, piezo_y, piezo_z):
            yield from bps.mv(piezo.x, x,
                              piezo.y, y,
                              piezo.z, z)

            # Read T and convert to deg C
            temp_degC = ls.input_A.get() - 273.15
            temp = str(np.round(float(temp_degC), 1)).zfill(5)

            for wa in waxs_arc:
                yield from bps.mv(waxs, wa)
                dets = [pil900KW] if waxs.arc.position < 15 else [pil1M, pil900KW]
                                                                                                                                                                                                           
                for yy, y_of in enumerate(y_offsets):
                    yield from bps.mv(piezo.y, y + y_of)

                    for xx, x_of in enumerate(x_offsets):
                        yield from bps.mv(piezo.x, x + x_of)

                        loc = f'{yy}{xx}'

                        sample_name = f'{name}_temp{temp}degC{get_scan_md()}_loc{loc}'
                        sample_id(user_name=user_name, sample_name=sample_name)
                        print(f"\n\n\n\t=== Sample: {sample_name} ===")
                        yield from bp.count(dets)

        sample_id(user_name='test', sample_name='test')
        det_exposure_time(0.2, 0.2)

        t_kelvin = 25 + 273.15
        yield from ls.output1.mv_temp(t_kelvin)
        yield from ls.output1.turn_off()

def linescan_milan_temp_2023_2(t=0.5):
    """
    Fine line scan on Linkam GI thermal stage
    """

    names =   ['JMA04','JMC07','JMAB07','JMC04','JMA07','JMC03','JMC02','JMA02','JMA03','MWB01','MWA01' ]
    piezo_x = [ -38400,-30400,-19900,-10900,-2900,5100,14100,23100,30100,45100,50000  ]
    piezo_y = [  -2300,-2000,-2000,-2000,-1700,-1700,-1700,-1700,-1700,-900,-650  ]
    piezo_z = [ -5000,-5000,-5000,-5000,-5600,-4200,-4200,-4200,-600,-4000,-4000 ]
    #piezo_z = [8400 for n in names]
    x_range = [[0, 2000, 40],[0, 2000, 40],[0, 1500, 30],[0, 2000, 40],[0, 1000, 20],[0, 2000, 40],[0, 1000, 20],[0, 1000, 20],[0, 2000, 40],[0, 1500, 30],[0, 11400, 228]]

    msg = "Wrong number of coordinates, check names and piezos"
    assert len(names) == len(piezo_x),   msg
    assert len(piezo_y) == len(piezo_x), msg
    assert len(piezo_y) == len(piezo_z), msg
    assert len(piezo_z) == len(x_range), msg
    assert len(x_range) == len(x_range), msg

    waxs_arc = [0, 20]
    # temperatures = [27, 100, 150]
    det_exposure_time(t, t)

    # for temperature in temperatures:
    #     t_kelvin = temperature + 273.15
    #     yield from ls.output1.mv_temp(t_kelvin)
    #     yield from bps.mv(ls.output1.status, 3)

    #     # Equalise temperature
    #     print(f"Equalising temperature to {temperature} deg C")
    #     start = time.time()
    #     temp = ls.input_A.get()
    #     while abs(temp - t_kelvin) > 5:
    #         print("Difference: {:.1f} K".format(abs(temp - t_kelvin)))
    #         yield from bps.sleep(10)
    #         temp = ls.input_A.get()

    #         # Escape the loop if too much time passes
    #         if time.time() - start > 1800:
    #             temp = t_kelvin
    #     print(
    #         "Time needed to equilibrate: {:.1f} min".format((time.time() - start) / 60)
    #     )
    #     # Wait extra time depending on temperature
    #     if (40 < temperature) and (temperature < 181):
    #         yield from bps.sleep(1800)

    #     for name, x, y, z, scan_pts_x in zip(names, piezo_x, piezo_y, piezo_z, x_range):
    #         yield from bps.mv(piezo.x, x,
    #                           piezo.y, y,
    #                           piezo.z, z)
            
    #         # Read T and convert to deg C
    #         temp_degC = ls.input_A.get() - 273.15
    #         temp = str(np.round(float(temp_degC), 1)).zfill(5)
            
    #         for wa in waxs_arc:
    #             yield from bps.mv(waxs, wa)
    #             dets = [pil900KW] if waxs.arc.position < 15 else [pil1M, pil900KW]

    #             sample_name = f'{name}_{temp}degC{get_scan_md()}'
    #             sample_name = sample_name.translate(
    #                 {ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ =,"}
    #             )
    #             sample_id(user_name="MW", sample_name=sample_name)
    #             print(f"\n\n\n\t=== Sample: {sample_name} ===")

    #             yield from bp.rel_scan(dets + [ls.input_A], piezo.x, *scan_pts_x)
    #             plt.close('all')
    #         waxs_arc = waxs_arc[::-1]
    for name, x, y, z, scan_pts_x in zip(names, piezo_x, piezo_y, piezo_z, x_range):
            yield from bps.mv(piezo.x, x,
                              piezo.y, y,
                              piezo.z, z)

            for wa in waxs_arc:
                yield from bps.mv(waxs, wa)
                dets = [pil900KW] if waxs.arc.position < 15 else [pil1M, pil900KW]

                sample_name = f'{name}_150degC{get_scan_md()}'
                sample_name = sample_name.translate(
                    {ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ =,"}
                )
                sample_id(user_name="MW", sample_name=sample_name)
                print(f"\n\n\n\t=== Sample: {sample_name} ===")

                yield from bp.rel_scan(dets, piezo.x, *scan_pts_x)
                plt.close('all')
            waxs_arc = waxs_arc[::-1]
    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)

    # # Turn off the heating and set temperature to 23 deg C
    # t_kelvin = 23 + 273.15
    # yield from ls.output1.mv_temp(t_kelvin)
    # yield from ls.output1.turn_off()


def linescan_milan_temp_2024_3(t=0.2):
    """
    Fine line scan on Linkam GI thermal stage
    """

    names =   ['JM_A_03', 'JM_A_02', 'JM_A_01', 'JM_B_03', 'JM_B_02', 'JM_B_01']
    piezo_x = [-2950, 2050, 5550, 16000, 21500, 28500]
    piezo_y = [-8925, -8925, -8925, -9600, -9400, -9400]
    piezo_z = [-7400, -9400, -9400, -9400, -9400, -9400]
    #piezo_z = [8400 for n in names]
    x_range = [[0, 2000, 3],[0, 1000, 3],[0, 3500, 3],[0, 2000, 3],[0, 3000, 3],[0, 2450, 3]]

    msg = "Wrong number of coordinates, check names and piezos"
    assert len(names) == len(piezo_x),   msg
    assert len(piezo_y) == len(piezo_x), msg
    assert len(piezo_y) == len(piezo_z), msg
    assert len(piezo_z) == len(x_range), msg
    assert len(x_range) == len(x_range), msg

    waxs_arc = [0, 20]
    temperatures = [100, 250]
    det_exposure_time(t, t)

    for temperature in temperatures:
        t_kelvin = temperature + 273.15
        yield from ls.output1.mv_temp(t_kelvin)
        yield from bps.mv(ls.output1.status, 3)

        # Equalise temperature
        print(f"Equalising temperature to {temperature} deg C")
        start = time.time()
        temp = ls.input_A.get()
        while abs(temp - t_kelvin) > 5:
            print("Difference: {:.1f} K".format(abs(temp - t_kelvin)))
            yield from bps.sleep(10)
            temp = ls.input_A.get()

            # Escape the loop if too much time passes
            if time.time() - start > 1800:
                temp = t_kelvin
        print(
            "Time needed to equilibrate: {:.1f} min".format((time.time() - start) / 60)
        )
        # Wait extra time depending on temperature
        if (40 < temperature) and (temperature < 181):
            yield from bps.sleep(120)

        for name, x, y, z, scan_pts_x in zip(names, piezo_x, piezo_y, piezo_z, x_range):
            yield from bps.mv(piezo.x, x,
                              piezo.y, y,
                              piezo.z, z)
            
            # Read T and convert to deg C
            temp_degC = ls.input_A.get() - 273.15
            temp = str(np.round(float(temp_degC), 1)).zfill(5)
            
            for wa in waxs_arc:
                yield from bps.mv(waxs, wa)
                dets = [pil900KW] if waxs.arc.position < 15 else [pil1M, pil900KW]

                sample_name = f'{name}_{temp}degC{get_scan_md()}'
                sample_name = sample_name.translate(
                    {ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ =,"}
                )
                sample_id(user_name="MW", sample_name=sample_name)
                print(f"\n\n\n\t=== Sample: {sample_name} ===")

                yield from bp.rel_scan(dets + [ls.input_A], piezo.x, *scan_pts_x)
                plt.close('all')
            waxs_arc = waxs_arc[::-1]
    # for name, x, y, z, scan_pts_x in zip(names, piezo_x, piezo_y, piezo_z, x_range):
    #         yield from bps.mv(piezo.x, x,
    #                           piezo.y, y,
    #                           piezo.z, z)

    #         for wa in waxs_arc:
    #             yield from bps.mv(waxs, wa)
    #             dets = [pil900KW] if waxs.arc.position < 15 else [pil1M, pil900KW]

    #             sample_name = f'{name}_150degC{get_scan_md()}'
    #             sample_name = sample_name.translate(
    #                 {ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ =,"}
    #             )
    #             sample_id(user_name="MW", sample_name=sample_name)
    #             print(f"\n\n\n\t=== Sample: {sample_name} ===")

    #             yield from bp.rel_scan(dets, piezo.x, *scan_pts_x)
    #             plt.close('all')
    #         waxs_arc = waxs_arc[::-1]
    # sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.2, 0.2)

    # Turn off the heating and set temperature to 23 deg C
    t_kelvin = 23 + 273.15
    yield from ls.output1.mv_temp(t_kelvin)
    yield from ls.output1.turn_off()

def milan_single_measurement_2025_1(name='FS_A_02_40-2', t_frame=0.05, t_tot=3):

    """
    As the name says, set coordinates via CSS, then take data
    WAXS only

    This one is working, above does not at the moment
    """
    yield from bps.mv(waxs, 0)
    det_exposure_time(t_frame, t_tot, period_delay=0.005)
    # det_exposure_time_old(t_frame, t_tot)
    yield from bps.sleep(1)

    dets = [pil900KW] if waxs.arc.position < 15 else [pil1M, pil900KW]
    sample_name = f'{name}_{get_scan_md()}_loc00'
    sample_id(user_name='MW', sample_name=sample_name)
    print(f"\n\n\n\t=== Sample: {sample_name} ===")
    yield from bp.count(dets)

    sample_id(user_name='test', sample_name='test')
    det_exposure_time(0.2, 0.2)

def milan_temp_2025_1_highrestemp(tim=0.2):
    """
    Temperature scan using resistive thermal GI stage for transmission with the hexa tilt.
    4 points per sample. For hockey pucks.


    names =   ['FS_R_01','FS_R_02','FS_R_03','FS_R_04','FS_R_05','FS_R_06','FS_R_07','FS_R_08','FS_R_09','FS_R_10','FS_R_11','FS_R_12','FS_R_13','FS_R_14','FS_R_15','FS_R_16','FS_R_17','FS_R_18','FS_R_19','FS_R_20','FS_R_21','FS_R_22','FS_R_23','FS_R_24','FS_R_25']
    piezo_x = [-51950,-48050,-44850,-37850, -32350, -27150, -22950, -14950, -12450, -8950, -5150, -2650, -650, 3350, 8350, 11800, 16350, 19350, 25850, 31950, 34200, 38200, 43200, 48200, 52950]
    piezo_y = [-10450,-10450,-10350,-10200, -9923, -9923, -9898, -9898, -9773, -9573, -9573, -9273, -9500, -9500, -9500, -9500, -9223, -9400, -9400, -9075, -9075, -9000, -9225, -8800, -8373]
    piezo_z = [-13500, -13500, -13500, -11300, -10100, -12100, -11100, -10500, -9700, -10300, -10300, -8700, -8700, -8700, -8700, -8700, -8700, -8700, -8700, -7100, -7100, -7100, -6100, -6100, -4900]
    #piezo_z = [8400 for n in names]
     """
     
    names =   ['FT_A_02','FT_B_01','FT_D_01','FT_D_03','FT_F_01','FT_F_02','FT_F_03','FT_F_04','FT_E_03r','FT_C_03','FT_G_02', 'FT_D_04', 'FT_E_05','FT_E_02', 'JM_A_01', 'JM_A_02', 'JM_A_03','JM_B_01', 'JM_B_02', 'JM_B_03', 'JM_C_01', 'JM_C_02', 'JM_D_01', 'JM_D_02', 'JM_E_02', 'JM_E_03']
    piezo_x = [56900, 53000, 48900, 43400, 40200, 36900, 33800, 28400, 24400, 20900, 15900, 9900, 7350, 3650, -3250, -7450, -11950, -15450, -18950, -22950, -27850, -31850, -34350, -38850, -43050, -46950]
    piezo_y = [-3350, -3550, -3350, -3050, -2950, -2750, -2600, -2550, -2750, -2750, -2400, -2650, -2700, -2450, -2175, -2225, -2075, -2025, -2025, -2025, -1815, -1665, -1690, -1565, -1615, -1590]
    piezo_z = [-7350, -7550, -6950, -6950, -7350, -6950, -6950, -6150, -6150, -6150, -5250, -4850, -4750, -4350, -5150, -4850, -4450, -4450, -4250, -4050, -3850, -2850, -2850, -2850, -2850, -2950]
    #piezo_z = [8400 for n in names]"""

    sample_index = 8

    names = names[sample_index:]
    piezo_x = piezo_x[sample_index:]
    piezo_y = piezo_y[sample_index:]
    piezo_z = piezo_z[sample_index:]

    msg = "Wrong number of coordinates, check names and piezos"
    assert len(names) == len(piezo_x),   msg
    assert len(piezo_y) == len(piezo_x), msg
    assert len(piezo_y) == len(piezo_z), msg


    # temperatures = [30,40,50,60,70,80,90,100,110,130,140,160,180,200]
    temperatures = [260]
    user_name = 'MW'
    det_exposure_time(tim, tim)

    x_offsets = [0, 75]
    y_offsets = [0, 75]
    waxs_arc = [0, 20]
    waxs_arc = [0]


  

    for temperature in temperatures:
        t_kelvin = temperature + 273.15
        yield from ls.output1.mv_temp(t_kelvin)

        # Activate heating range in Lakeshore
        yield from bps.mv(ls.output1.status, 3)

        # Equalise temperature
        print(f"Equalising temperature to {temperature:.0f} deg C")
        start = time.time()
        temp = ls.input_A.get()
        while abs(temp - t_kelvin) > 3:
            print("Difference: {:.1f} K".format(abs(temp - t_kelvin)))
            yield from bps.sleep(5)
            temp = ls.input_A.get()
            
            # Escape the loop if too much time passes
            if time.time() - start > 30 * 60:
                temp = t_kelvin
        
        print("Time needed to equilibrate: {:.1f} min".format((time.time() - start) / 60))

        # Wait extra time depending on temperature
        if temperature != temperatures[0]:
            wait_time = 60
            print(f'Sleeping for {wait_time} seconds')
            yield from bps.sleep(wait_time)

        for name, x, y, z in zip(names, piezo_x, piezo_y, piezo_z):
            yield from bps.mv(piezo.x, x,
                              piezo.y, y,
                              piezo.z, z)

            # Read T and convert to deg C
            temp_degC = ls.input_A.get() - 273.15
            temp = str(np.round(float(temp_degC), 1)).zfill(5)

            print(f'Temperature {temp} degC for sample {name}')

            for wa in waxs_arc:
                print(f'Moving WAXS arc to {wa} deg')


                # Problems with WAXS arc
                msg = 'Problems with moving WAXS arc, will retry 10 times before failing'
                fail_count = 0
                try:
                    yield from bps.mv(waxs, wa)
                except:
                    fail_count =+ 1
                    print(msg, fail_count)
                    pass
                try:
                    yield from bps.mv(waxs, wa)
                except:
                    fail_count =+ 1
                    print(msg, fail_count)
                    pass
                try:
                    yield from bps.mv(waxs, wa)
                except:
                    fail_count =+ 1
                    print(msg, fail_count)
                    pass
                try:
                    yield from bps.mv(waxs, wa)
                except:
                    fail_count =+ 1
                    print(msg, fail_count)
                    pass
                try:
                    yield from bps.mv(waxs, wa)
                except:
                    fail_count =+ 1
                    print(msg, fail_count)
                    pass

                dets = [pil900KW] if waxs.arc.position < 15 else [pil1M, pil900KW]
                                                                                                                                                                                                           
                for yy, y_of in enumerate(y_offsets):
                    yield from bps.mv(piezo.y, y + y_of)

                    for xx, x_of in enumerate(x_offsets):
                        yield from bps.mv(piezo.x, x + x_of)

                        loc = f'{yy}{xx}'

                        print(f'Location on sample: {loc}')

                        sample_name = f'{name}_temp{temp}degC{get_scan_md()}_loc{loc}'
                        sample_id(user_name=user_name, sample_name=sample_name)
                        print(f"\n\n\n\t=== Sample: {sample_name} ===")
                        yield from bp.count(dets)

        sample_id(user_name='test', sample_name='test')
        det_exposure_time(0.2, 0.2)

        t_kelvin = 25 + 273.15
        yield from ls.output1.mv_temp(t_kelvin)
        yield from ls.output1.turn_off()

def linescan_milan_temp_2025_1(t=0.5):
    """
    Fine line scan on Linkam GI thermal stage
    WAXS arc as the slowest motor, outside sample loop
    """

    # names =   ['RP_M_62','RP_M_61','RP_M_52','RP_M_51','RP_M_42','RP_M_41','RP_M_32','RP_M_31','RP_M_21','RP_M_13','RP_M_12','RP_M_11','RP_Q_06','RP_Q_05','RP_Q_04','RP_Q_03','RP_Q_20','RP_Q_21','RP_Q_22','RP_Q_23','RP_Q_10','RP_Q_11','RP_Q_12']
    # piezo_x = [-44330,-42130,-39130,-37530,-34730,-32130,-28130,-26530,-22130,-18330,-15130,-12730,-8330,-4730,-1780,170,4170,9970,14770,20370,31370,39970,47370]
    # piezo_y = [-8085,-7885,-7885,-7735,-7585,-7565,-7410,-7360,-7135,-7010,-6935,-6910,-6760,-6660,-6460,-6410,-6285,-6110,-5960,-5760,-5260,-5080,-4960]
    # piezo_z = [6500,6500,6500,6500,5300,5300,5300,5300,5300,5300,5300,5300,5900,5300,5300,6300,3500,3500,3500,3500,3500,3500,3500]
    # #piezo_z = [8400 for n in names]
    # x_range = [[0, 1000, 4],[0, 1000, 4],[0, 600, 4],[0, 1400, 4],[0, 1600, 4],[0, 1200, 4],[0, 1000, 4],[0, 800, 4],[0, 1600, 4],[0, 1600, 4],[0, 1400, 4],[0, 1000, 4],[0, 1000, 4],[0, 600, 4],[0, 350, 4],[0, 1400, 4],[0, 5800, 117],[0, 4800, 97],[0, 5600, 113],[0, 8400, 169],[0, 8600, 173],[0, 7400, 149],[0, 4800, 97]]

    names =   ['RP_P_13','RP_P_12','RP_P_11','RP_R_06','RP_R_05','RP_R_04','RP_R_03','RP_R_02','RP_R_10','RP_R_11','RP_R_12','RP_R_13','RP_R_14','RP_Q_10','RP_Q_11','RP_Q_12','RP_Q_13','RP_Q_20','RP_Q_21','RP_Q_22','RP_Q_23']
    piezo_x = [-42370,-39170,-36970,-31820,-30020,-27820,-25620,-23220,-20620,-14420,-11020,-5820,-620,4980,10380,16380,21980,27980,33380,38180,44780]
    piezo_y = [-7960,-7960,-7910,-7610,-7585,-7510,-7460,-7360,-6960,-6810,-6710,-6510,-6385,-6135,-5835,-5660,-5460,-5285,-5035,-4860,-4735]
    piezo_z = [5100,5100,5100,5100,5100,5100,5100,5100,5100,5100,5100,5100,5100,5100,5100,5100,5100,5100,5100,5100,5100]
    #piezo_z = [8400 for n in names]
    x_range = [[0, 1400, 4],[0, 1400, 4],[0, 2000, 4],[0, 600, 4],[0, 800, 4],[0, 1000, 4],[0, 800, 4],[0, 1000, 4],[0, 6200, 125],[0, 3400, 69],[0, 5200, 105],[0, 5200, 105],[0, 3160, 64],[0, 5400, 109],[0, 6000, 121],[0, 5600, 113],[0, 3600, 73],[0, 5400, 109],[0, 4800, 97],[0, 6600, 133],[0, 7400, 149]]



    msg = "Wrong number of coordinates, check names and piezos"
    assert len(names) == len(piezo_x),   msg
    assert len(piezo_y) == len(piezo_x), msg
    assert len(piezo_y) == len(piezo_z), msg
    assert len(piezo_z) == len(x_range), msg
    assert len(x_range) == len(x_range), msg

    waxs_arc = [0]
    temperatures = [25]
    det_exposure_time(t, t)

    for temperature in temperatures:
        t_kelvin = temperature + 273.15
        yield from ls.output1.mv_temp(t_kelvin)
        yield from bps.mv(ls.output1.status, 3)

        # Equalise temperature
        print(f"Equalising temperature to {temperature} deg C")
        start = time.time()
        temp = ls.input_A.get()
        while abs(temp - t_kelvin) > 100:
            print("Difference: {:.1f} K".format(abs(temp - t_kelvin)))
            yield from bps.sleep(10)
            temp = ls.input_A.get()

            # Escape the loop if too much time passes
            if time.time() - start > 5:
                temp = t_kelvin
        print(
            "Time needed to equilibrate: {:.1f} min".format((time.time() - start) / 60)
        )
        # Wait extra time depending on temperature
        #if (40 < temperature) and (temperature < 181):
        #    yield from bps.sleep(120)
        #for wa in waxs_arc:
        #    yield from bps.mv(waxs, wa)
        dets = [pil900KW] if waxs.arc.position < 15 else [pil1M, pil900KW]
        # dets = [pil1M]
        for name, x, y, z, scan_pts_x in zip(names, piezo_x, piezo_y, piezo_z, x_range):
            yield from bps.mv(piezo.x, x,
                            piezo.y, y,
                            piezo.z, z)
            
            # Read T and convert to deg C
            temp_degC = ls.input_A.get() - 273.15
            temp = str(np.round(float(temp_degC), 1)).zfill(5)
            
            sample_name = f'{name}_{temp}degC{get_scan_md()}'
            sample_id(user_name="MW", sample_name=sample_name)
            print(f"\n\n\n\t=== Sample: {sample_name} ===")

            yield from bp.rel_scan(dets + [ls.input_A], piezo.x, *scan_pts_x)
            plt.close('all')

    det_exposure_time(0.2, 0.2)

    # Turn off the heating and set temperature to 23 deg C
    t_kelvin = 23 + 273.15
    yield from ls.output1.mv_temp(t_kelvin)
    yield from ls.output1.turn_off()


def linescan_milan_tempy_2025_1(t=0.5):
    """
    Fine line scan on Linkam GI thermal stage
    WAXS arc as the slowest motor, outside sample loop

    Y range 
    """

    names =   ['test']
    piezo_x = [7700]
    piezo_y = [-0.158]
    piezo_z = [87.575]
    #piezo_z = [8400 for n in names]
    y_range = [[0, 5, 1]]

    msg = "Wrong number of coordinates, check names and piezos"
    assert len(names) == len(piezo_x),   msg
    assert len(piezo_y) == len(piezo_x), msg
    assert len(piezo_y) == len(piezo_z), msg
    assert len(piezo_z) == len(y_range), msg
    assert len(y_range) == len(y_range), msg

    waxs_arc = [0]
    temperatures = [25]
    det_exposure_time(t, t)

    for temperature in temperatures:
        t_kelvin = temperature + 273.15
        yield from ls.output1.mv_temp(t_kelvin)
        yield from bps.mv(ls.output1.status, 3)

        # Equalise temperature
        print(f"Equalising temperature to {temperature} deg C")
        start = time.time()
        temp = ls.input_A.get()
        while abs(temp - t_kelvin) > 25:
            print("Difference: {:.1f} K".format(abs(temp - t_kelvin)))
            yield from bps.sleep(10)
            temp = ls.input_A.get()

            # Escape the loop if too much time passes
            if time.time() - start > 1800:
                temp = t_kelvin
        print(
            "Time needed to equilibrate: {:.1f} min".format((time.time() - start) / 60)
        )
        # Wait extra time depending on temperature
        #if (40 < temperature) and (temperature < 181):
        #    yield from bps.sleep(120)
        #for wa in waxs_arc:
        #    yield from bps.mv(waxs, wa)
        dets = [pil900KW] if waxs.arc.position < 15 else [pil1M, pil900KW]
        for name, x, y, z, scan_pts_y in zip(names, piezo_x, piezo_y, piezo_z, y_range):
            yield from bps.mv(piezo.x, x,
                            piezo.y, y,
                            piezo.z, z)
            
            # Read T and convert to deg C
            temp_degC = ls.input_A.get() - 273.15
            temp = str(np.round(float(temp_degC), 1)).zfill(5)
            
            sample_name = f'{name}_{temp}degC{get_scan_md()}'
            sample_id(user_name="MW", sample_name=sample_name)
            print(f"\n\n\n\t=== Sample: {sample_name} ===")

            yield from bp.rel_scan(dets + [ls.input_A], piezo.y, *scan_pts_y)
            plt.close('all')

    det_exposure_time(0.2, 0.2)

    # Turn off the heating and set temperature to 23 deg C
    t_kelvin = 23 + 273.15
    yield from ls.output1.mv_temp(t_kelvin)
    yield from ls.output1.turn_off()

def milan_single_measurement_2025_1(name='FT_A_03', t_frame=0.5, t_tot=0.5):

    """
    As the name says, set coordinates via CSS, then take data
    WAXS only

    This one is working, above does not at the moment
    """
    yield from bps.mv(waxs, 0)
    det_exposure_time(t_frame, t_tot, period_delay=0.005)
    # det_exposure_time(t_frame, t_tot)
    yield from bps.sleep(1)

    dets = [pil900KW] if waxs.arc.position < 15 else [pil1M, pil900KW]
    sample_name = f'{name}_{get_scan_md()}_loc00'
    sample_id(user_name='MW', sample_name=sample_name)
    print(f"\n\n\n\t=== Sample: {sample_name} ===")
    yield from bp.count(dets)

    sample_id(user_name='test', sample_name='test')
    det_exposure_time(0.2, 0.2)

def test_shot(name='test'):#, t_frame=0.5, t_tot=0.5):
    """
    As the name says, set coordinates via CSS, then take data
    WAXS only

    This one is working, above does not at the moment
    """

    dets = [pil900KW] if waxs.arc.position < 15 else [pil1M, pil900KW]
    sample_name = f'{name}_{get_scan_md()}_loc00'
    sample_id(user_name='MW', sample_name=sample_name)
    print(f"\n\n\n\t=== Sample: {sample_name} ===")
    yield from bp.count(dets)

    sample_id(user_name='test', sample_name='test')
    # det_exposure_time(0.2, 0.2)



def milan_puck4pt_2025_1(tim=0.5,temp=200):
    '''
    Temperature scan using resistive thermal GI stage for transmission with the hexa tilt.
    4 points per sample. For hockey pucks. Input temp manually into script, running on linkam


    names =   ['FS_R_01','FS_R_02','FS_R_03','FS_R_04','FS_R_05','FS_R_06','FS_R_07','FS_R_08','FS_R_09','FS_R_10','FS_R_11','FS_R_12','FS_R_13','FS_R_14','FS_R_15','FS_R_16','FS_R_17','FS_R_18','FS_R_19','FS_R_20','FS_R_21','FS_R_22','FS_R_23','FS_R_24','FS_R_25']
    piezo_x = [-51950,-48050,-44850,-37850, -32350, -27150, -22950, -14950, -12450, -8950, -5150, -2650, -650, 3350, 8350, 11800, 16350, 19350, 25850, 31950, 34200, 38200, 43200, 48200, 52950]
    piezo_y = [-10450,-10450,-10350,-10200, -9923, -9923, -9898, -9898, -9773, -9573, -9573, -9273, -9500, -9500, -9500, -9500, -9223, -9400, -9400, -9075, -9075, -9000, -9225, -8800, -8373]
    piezo_z = [-13500, -13500, -13500, -11300, -10100, -12100, -11100, -10500, -9700, -10300, -10300, -8700, -8700, -8700, -8700, -8700, -8700, -8700, -8700, -7100, -7100, -7100, -6100, -6100, -4900]
    #piezo_z = [8400 for n in names]
    
    '''
    names =   ['JM_F_02','JM_F_03','JM_G_01','JM_G_02','JM_G_03','JM_G_04','FT_A_03']
    piezo_x = [12730, 9130, 3730, 830, -2370, -3490, -6090]
    piezo_y = [-8940, -8800, -8620, -8540, -8400, -8490, -8650]
    piezo_z = [-5000, -5000,-4200,-4200,-4200,-2900, -2900]
    #piezo_z = [8400 for n in names]"""

    msg = "Wrong number of coordinates, check names and piezos"
    assert len(names) == len(piezo_x),   msg
    assert len(piezo_y) == len(piezo_x), msg
    assert len(piezo_y) == len(piezo_z), msg


    # temperatures = [30,40,50,60,70,80,90,100,110,130,140,160,180,200]
    #temperatures = [40]
    user_name = 'MW'
    det_exposure_time(tim, tim)

    x_offsets = [0, 75]
    y_offsets = [0, 75]
    waxs_arc = [0]

  

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)
        dets = [pil900KW] if waxs.arc.position < 15 else [pil1M, pil900KW]
        
        for name, x, y, z in zip(names, piezo_x, piezo_y, piezo_z):
            yield from bps.mv(piezo.x, x,
                                piezo.y, y,
                                piezo.z, z)
                                                                                                                                                                   
            for yy, y_of in enumerate(y_offsets):
                yield from bps.mv(piezo.y, y + y_of)

                for xx, x_of in enumerate(x_offsets):
                    yield from bps.mv(piezo.x, x + x_of)

                    loc = f'{yy}{xx}'

                    sample_name = f'{name}_temp{temp}degC{get_scan_md()}_loc{loc}'
                    sample_id(user_name=user_name, sample_name=sample_name)
                    print(f"\n\n\n\t=== Sample: {sample_name} ===")
                    yield from bp.count(dets)

    sample_id(user_name='test', sample_name='test')
    det_exposure_time(0.2, 0.2)

    t_kelvin = 25 + 273.15
    yield from ls.output1.mv_temp(t_kelvin)
    yield from ls.output1.turn_off()


def milan_single_measurement_2025_1(name='RP_E_01_35C', t_frame=0.5, t_tot=0.5):

    """
    As the name says, set coordinates via CSS, then take data
    WAXS only

    This one is working, above does not at the moment
    """
    # yield from bps.mv(waxs, 0)
    # det_exposure_time(t_frame, t_tot, period_delay=0.005)
    # # det_exposure_time_old(t_frame, t_tot)
    # yield from bps.sleep(1)

    dets = [pil900KW] if waxs.arc.position < 15 else [pil1M, pil900KW]
    sample_name = f'{name}_{get_scan_md()}_loc00'
    sample_id(user_name='MW', sample_name=sample_name)
    print(f"\n\n\n\t=== Sample: {sample_name} ===")
    yield from bp.count(dets)

    sample_id(user_name='test', sample_name='test')
    det_exposure_time(0.2, 0.2)


def milan_puck4pt2_2025_1(tim=0.2,temp=300):
    '''
    Temperature scan using resistive thermal GI stage for transmission with the hexa tilt.
    4 points per sample. For hockey pucks. Input temp manually into script, running on linkam


    names =   ['FS_R_01','FS_R_02','FS_R_03','FS_R_04','FS_R_05','FS_R_06','FS_R_07','FS_R_08','FS_R_09','FS_R_10','FS_R_11','FS_R_12','FS_R_13','FS_R_14','FS_R_15','FS_R_16','FS_R_17','FS_R_18','FS_R_19','FS_R_20','FS_R_21','FS_R_22','FS_R_23','FS_R_24','FS_R_25']
    piezo_x = [-51950,-48050,-44850,-37850, -32350, -27150, -22950, -14950, -12450, -8950, -5150, -2650, -650, 3350, 8350, 11800, 16350, 19350, 25850, 31950, 34200, 38200, 43200, 48200, 52950]
    piezo_y = [-10450,-10450,-10350,-10200, -9923, -9923, -9898, -9898, -9773, -9573, -9573, -9273, -9500, -9500, -9500, -9500, -9223, -9400, -9400, -9075, -9075, -9000, -9225, -8800, -8373]
    piezo_z = [-13500, -13500, -13500, -11300, -10100, -12100, -11100, -10500, -9700, -10300, -10300, -8700, -8700, -8700, -8700, -8700, -8700, -8700, -8700, -7100, -7100, -7100, -6100, -6100, -4900]
    #piezo_z = [8400 for n in names]
    
    '''
    names =   ['FS_A_01','FS_A_02','FS_A_03','FS_A_04']
    piezo_x = [14135, 11635, 9135, 6635]
    piezo_y = [-9357, -9297, -9217, -9137]
    piezo_z = [7400, 7400, 7400, 7400]
    #piezo_z = [8400 for n in names]"""


    # names =   ['FS_A_01','FS_A_02','FS_A_03','FS_A_04','JL_A_01','JL_A_02','JL_A_03', 'JL_A_04','JL_A_05']
    # piezo_x = [14135, 11635, 9135, 6635, 5360, 3060, 1660, -340, -2140]
    # piezo_y = [-9357, -9297, -9217, -9137, -9372, -9372, -9312, -9312, -9352]
    # piezo_z = [7400, 7400, 7400, 7400, 4500, 4500, 5600, 5600, 5600]
    #piezo_z = [8400 for n in names]"""

    # names =   ['JL_A_01','JL_A_02','JL_A_03', 'JL_A_04','JL_A_05']
    # piezo_x = [5360, 3060, 1660, -340, -2140]
    # piezo_y = [-9372, -9372, -9312, -9312, -9352]
    # piezo_z = [4500, 4500, 5600, 5600, 5600]
    #piezo_z = [8400 for n in names]"""


    msg = "Wrong number of coordinates, check names and piezos"
    assert len(names) == len(piezo_x),   msg
    assert len(piezo_y) == len(piezo_x), msg
    assert len(piezo_y) == len(piezo_z), msg


    # temperatures = [30,40,50,60,70,80,90,100,110,130,140,160,180,200]
    #temperatures = [40]
    user_name = 'MW'
    det_exposure_time(tim, tim)

    x_offsets = [0, 75]
    y_offsets = [0, 75]
    waxs_arc = [0]

  

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)
        dets = [pil900KW] if waxs.arc.position < 15 else [pil1M, pil900KW]
        
        for name, x, y, z in zip(names, piezo_x, piezo_y, piezo_z):
            yield from bps.mv(piezo.x, x,
                                piezo.y, y,
                                piezo.z, z)
                                                                                                                                                                   
            for yy, y_of in enumerate(y_offsets):
                yield from bps.mv(piezo.y, y + y_of)

                for xx, x_of in enumerate(x_offsets):
                    yield from bps.mv(piezo.x, x + x_of)

                    loc = f'{yy}{xx}'

                    sample_name = f'{name}_temp{temp}degC{get_scan_md()}_loc{loc}'
                    sample_id(user_name=user_name, sample_name=sample_name)
                    print(f"\n\n\n\t=== Sample: {sample_name} ===")
                    yield from bp.count(dets)

    sample_id(user_name='test', sample_name='test')
    det_exposure_time(0.2, 0.2)

    t_kelvin = 25 + 273.15
    yield from ls.output1.mv_temp(t_kelvin)
    yield from ls.output1.turn_off()

def milan_single_measurement2_2025_1(name='MW_X_01', t_frame=1, t_tot=100):

    """
    As the name says, set coordinates via CSS, then take data
    WAXS only

    This one is working, above does not at the moment
    """
    yield from bps.mv(waxs, 0)
    det_exposure_time(t_frame, t_tot, period_delay=0.005)
    # det_exposure_time_old(t_frame, t_tot)
    yield from bps.sleep(1)

    dets = [pil900KW] if waxs.arc.position < 15 else [pil1M, pil900KW]
    sample_name = f'{name}_{get_scan_md()}_loc00'
    sample_id(user_name='MW', sample_name=sample_name)
    print(f"\n\n\n\t=== Sample: {sample_name} ===")
    yield from bp.count(dets)

    sample_id(user_name='test', sample_name='test')
    det_exposure_time(0.2, 0.2)

####line scan


def aaron_rot(t=8):
    sample_id(user_name="AM", sample_name="tetrahedral")
    det_exposure_time(t)
    yield from bp.inner_product_scan(
        [pil1M], 24, prs, 45, 22, stage.x, 0.23, 0.15, piezo.y, -1792.6, -1792.6
    )
    yield from bp.inner_product_scan(
        [pil1M], 22, prs, 21, 0, stage.x, 0.15, 0.11, piezo.y, -1792.6, -1792.6
    )
    yield from bp.inner_product_scan(
        [pil1M], 11, prs, -1, -11, stage.x, 0.11, 0.1, piezo.y, -1792.6, -1792.1
    )
    yield from bp.inner_product_scan(
        [pil1M], 11, prs, -12, -22, stage.x, 0.1, 0.1, piezo.y, -1792.1, -1791.6
    )
    yield from bp.inner_product_scan(
        [pil1M], 11, prs, -23, -33, stage.x, 0.1, 0.114, piezo.y, -1791.6, -1790.9
    )
    yield from bp.inner_product_scan(
        [pil1M], 12, prs, -34, -45, stage.x, 0.114, 0.134, piezo.y, -1790.9, -1790.9
    )


def brian_caps(t=1):
    x_list = [
        -36500,
        -30150,
        -23800,
        -17450,
        -11100,
        -4750,
        1600,
        7950,
        14400,
        20700,
        27050,
        33400,
        39850,
    ]  #
    y_list = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    samples = [
        "test",
        "LC-O36-6",
        "LC-O36-7",
        "LC-O36-8",
        "LC-O36-9",
        "LC-O37-6",
        "LC-O37-7",
        "LC-O37-8",
        "LC-O37-9",
    ]
    # Detectors, motors:
    dets = [pil1M]
    y_range = [0, 0, 1]
    #    param   = '16.1keV'
    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    det_exposure_time(t, t)
    for x, y, sample in zip(x_list, y_list, samples):
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(piezo.y, y)
        sample_id(user_name="BM", sample_name=sample)
        # yield from bp.scan(dets, piezo.y, *y_range)
        yield from bp.count(dets, num=1)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def brian_caps_2020_3(t=1):
    # samples = ['buffer1', 'GB01', 'GB02', 'GB03', 'GB04', 'GB05', 'GB06', 'GB08', 'GB09', 'GB10', 'GB11', 'GB12']
    # samples = ['Y01', 'Y02', 'Y03', 'Y04', 'Y05', 'Y06']

    # x_list = [-22300, -18600, -11000, -4500, 2300, 8500, 14500, 21000, 27500, 33800, 40300, 46700]
    # y_list = [2500,     2500,   2500,  2500, 2500, 2500,  2500,  2500,  2500,  2500,  2500,  2500]
    # z_list = [4000,     2500,   2500,  2500, 2500, 2500,  2500,  2500,  2500,  2500,  2500,  2500]

    samples = [
        "S1_43",
        "S1_44",
        "S1_45",
        "S1_46",
        "S1_47",
        "S1_48",
        "S1_49",
        "S1_50",
        "S1_51",
        "S1_52",
        "S1_53",
        "S1_54",
        "S1_55",
        "S1_56",
        "S1_57",
        "S1_58",
        "S1_59",
        "S1_60",
        "S1_61",
        "S1_62",
        "S2_63",
        "S2_67",
        "S2_68",
        "S2_69",
        "S2_70",
        "S2_71",
    ]

    x_list = [
        -39100,
        -32820,
        -26400,
        -20240,
        -13880,
        -7020,
        -720,
        5390,
        11680,
        18180,
        24560,
        31040,
        37360,
        43820,
        -37780,
        -31530,
        -24530,
        -17840,
        -12100,
        -5800,
        790,
        7170,
        13000,
        19420,
        25840,
        32260,
    ]
    y_list = [
        200,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
    ]
    z_list = [
        12500,
        12500,
        12500,
        12500,
        12500,
        12500,
        12500,
        12500,
        12500,
        12500,
        12500,
        12500,
        12500,
        12500,
        2000,
        2000,
        2000,
        2000,
        2000,
        2000,
        2000,
        2000,
        2000,
        2000,
        2000,
        2000,
    ]

    # Detectors, motors:
    dets = [pil1M]
    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    assert len(x_list) == len(
        y_list
    ), f"Number of X coordinates ({len(x_list)}) is different from number of Y coord ({len(y_list)})"
    assert len(x_list) == len(
        z_list
    ), f"Number of X coordinates ({len(x_list)}) is different from number of Z coord ({len(z_list)})"
    ypos = [0, 50, 2]

    det_exposure_time(t, t)
    for x, y, z, sample in zip(x_list, y_list, z_list, samples):
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(piezo.y, y)
        yield from bps.mv(piezo.z, z)
        sample_id(user_name="BM", sample_name=sample + "_test_18.25keV")
        # yield from bp.rel_scan(dets, piezo.y, *ypos)
        yield from bp.count(dets, num=240)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def brian_caps_damage_2021_1(t=1):

    samples = [
        "V1_01",
        "V1_02",
        "V1_03",
        "V1_04",
        "V1_05",
        "V1_06",
        "V1_07",
        "V1_08",
        "V1_09",
        "V1_10",
        "V1_11",
        "V1_12",
        "V1_13",
        "V1_14",
        "V1_15",
        "V1_16",
        "V1_17",
        "V1_18",
        "V1_19",
        "V1_20",
        "V1_21",
        "V1_22",
        "V1_23",
        "V1_24",
        "V1_25",
        "V1_26",
        "V1_27",
        "V1_28",
        "V1_29",
        "V1_30",
        "V1_31",
        "V1_32",
        "V1_33",
        "V1_35",
        "V1_36",
    ]

    x_list = [
        41600,
        35500,
        28950,
        22600,
        16600,
        10050,
        3600,
        -2750,
        -9050,
        -15350,
        -21650,
        -28100,
        -34450,
        40500,
        34500,
        27600,
        21000,
        15150,
        8650,
        2700,
        -4000,
        -10250,
        -16600,
        -22850,
        -28950,
        -35500,
        38900,
        32950,
        26900,
        19900,
        13350,
        7100,
        1000,
        -5500,
        -11700,
    ]
    y_list = [
        3000,
        3000,
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
    z_list = [
        -9000,
        -9000,
        -9000,
        -9000,
        -9000,
        -9000,
        -9000,
        -9000,
        -9000,
        -9000,
        -9000,
        -9000,
        -9000,
        900,
        900,
        900,
        900,
        900,
        900,
        900,
        900,
        900,
        900,
        900,
        900,
        900,
        10900,
        10900,
        10900,
        10900,
        10900,
        10900,
        10900,
        10900,
        10900,
    ]

    # Detectors, motors:
    dets = [pil1M]
    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    assert len(x_list) == len(
        y_list
    ), f"Number of X coordinates ({len(x_list)}) is different from number of Y coord ({len(y_list)})"
    assert len(x_list) == len(
        z_list
    ), f"Number of X coordinates ({len(x_list)}) is different from number of Z coord ({len(z_list)})"
    ypos = [0, 50, 2]

    det_exposure_time(1, 180)
    for x, y, z, sample in zip(x_list, y_list, z_list, samples):
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(piezo.y, y)
        yield from bps.mv(piezo.z, z)
        sample_id(user_name="BM", sample_name=sample + "_11.85keV_8.3m_1s")
        yield from bp.count(dets, num=1)
        yield from bps.sleep(200)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def brian_caps_2021_2(t=1):
    # samples = ['NT1_01', 'NT1_02', 'NT1_03', 'NT1_04', 'NT1_05', 'NT1_06', 'NT1_08', 'NT1_09', 'NT1_10', 'NT1_11', 'NT1_12', 'NT1_13', 'NT1_14', 'NT1_15',
    #            'NT1_17', 'NT1_18', 'NT1_19', 'NT1_20', 'NT1_21', 'NT1_22', 'NT1_23', 'NT2_59', 'NT2_60', 'NT2_61', 'NT2_62', 'NT2_63', 'NT2_64',
    #            'NT2_73', 'NT2_74', 'NT2_75', 'NT2_76', 'NT2_77', 'NT2_78', 'NT2_79', 'NT2_80', 'NT2_81', 'NT2_82', 'NT2_83', 'NT2_84', 'NT2_85']

    # samples = ['NT2_86', 'NT2_87', 'NT2_88', 'NT2_89', 'NT2_90',  'B1_01',  'B1_02',  'B1_03',  'B1_04',  'B1_05',  'B1_06',  'B1_07',  'B1_08',  'B1_09',
    #             'B1_10',  'B1_11',  'B1_12',  'B1_13',  'B1_14',  'B1_15',  'B1_16',  'B1_17',  'B1_18',  'B1_19',  'B1_20',  'B1_21',  'B1_22',
    #             'B2_23',  'B2_24',  'B2_25',  'B2_26',  'B2_27',  'B2_28',  'B2_29',  'B2_30',  'B2_31',  'B2_32',  'B2_33',  'B2_34',  'B2_35']

    # samples = [ 'B2_36',  'B2_37',  'B2_38',  'B2_39',  'B2_40',  'B2_41',  'B2_42',  'B2_43',  'B2_44',  'B2_45',  'B2_46',  'B2_47',  'B2_48',  'B2_49',
    #             'B2_50',  'B2_51',  'B2_52',  'B2_53',  'B2_54',  'B2_55',  'B2_56',  'B2_57',  'B2_59',  'B2_60',  'B2_61',  'B2_62',  'B2_63',
    #             'B2_64',  'B2_65',  'B2_66',  'B2_67',  'B@_68',  'B2_69',  'B2_70',  'B2_71',  'G1_01',  'G1_02',  'G1_03',  'G1_04',  'G1_05']

    samples = [
        "G1_09",
        "G1_10",
        "G1_08",
        "G1_07",
        "G1_12",
        "G1_11",
        "G1_06",
        "TD_01",
        "TD_02",
    ]

    x_list = [46350, 40400, 33450, 27700, 21350, 14700, 8650, 2350, -3950]
    y_list = [2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000]
    z_list = [-9600, -9600, -9600, -9600, -9600, -9600, -9600, -9600, -9600]

    # x_list = [    46350,    39500,    33400,    27400,    21300,    14900,     8700,     2300,    -3850,   -9850,   -16800,   -23050,   -29550,   -35600,
    #               41800,    35400,    29300,    22900,    16650,    10200,     4000,    -2100,    -8700,   -14800,   -20900,   -27500,   -33500,
    #               43900,    37700,    31100,    25100,    18550,    12600,     6000,        0,    -6100,   -12800,   -18800,   -25000,   -31900]
    # y_list = [     2000,     2000,     2000,     2000,     2000,     2000,     2000,     2000,     2000,     2000,     2000,     2000,     2000,     2000,
    #                2000,     2000,     2000,     2000,     2000,     2000,     2000,     2000,     2000,     2000,     2000,     2000,     2000,
    #                2000,     2000,     2000,     2000,     2000,     2000,     2000,     2000,     2000,     2000,     2000,     2000,     2000]
    # z_list = [    -9600,    -9600,    -9600,    -9600,    -9600,    -9600,    -9600,    -9600,    -9600,    -9600,    -9600,    -9600,    -9600,    -9600,
    #                -600,     -600,     -600,     -600,     -600,     -600,     -600,     -600,     -600,     -600,     -600,     -600,     -600,
    #               10300,    10300,    10300,    10300,    10300,    10300,    10300,    10300,    10300,    10300,    10300,    10300,    10300]

    # Detectors, motors:
    dets = [pil1M]
    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    assert len(x_list) == len(
        y_list
    ), f"Number of X coordinates ({len(x_list)}) is different from number of Y coord ({len(y_list)})"
    assert len(x_list) == len(
        z_list
    ), f"Number of X coordinates ({len(x_list)}) is different from number of Z coord ({len(z_list)})"
    ypos = [0, 50, 2]

    det_exposure_time(t, t)
    for x, y, z, sample in zip(x_list, y_list, z_list, samples):
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(piezo.y, y)
        yield from bps.mv(piezo.z, z)

        det_exposure_time(1, 1)

        sample_id(user_name="BM", sample_name=sample + "_16.1keV_8.3m_1s")
        yield from bp.rel_scan(dets, piezo.y, *ypos)
        yield from bps.sleep(2)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def run_mesh_aaron_2021(t=1):
    name = "AM"
    dets = [pil1M]
    det_exposure_time(t, t)

    samples = ["sample_fe1"]
    x_list = [-25100]
    y_list = [3600]
    x_range = [[-25100, -24900, 9]]
    y_range = [[3600, 3800, 81]]

    i = 0
    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"

    yield from bps.mv(pil1m_pos.y, -60.0)
    for x, y, sample, x_r, y_r in zip(x_list, y_list, samples, x_range, y_range):
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(piezo.y, y)

        for xs in np.linspace(x_r[0], x_r[1], x_r[2]):
            for ys in np.linspace(y_r[0], y_r[1], y_r[2]):
                yield from bps.mv(piezo.x, xs)
                yield from bps.mv(piezo.y, ys)

                name_fmt = "{sam}_8.3m_16.1keV_pos{pos}_up"
                sample_name = name_fmt.format(sam=sample, pos="%4.4d" % i)

                sample_id(user_name=name, sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")

                yield from bp.count(dets, num=1)
                yield from bps.sleep(1)

                i += 1

    yield from bps.mv(pil1m_pos.y, -55.7)
    for x, y, sample, x_r, y_r in zip(x_list, y_list, samples, x_range, y_range):
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(piezo.y, y)

        for xs in np.linspace(x_r[0], x_r[1], x_r[2]):
            for ys in np.linspace(y_r[0], y_r[1], y_r[2]):
                yield from bps.mv(piezo.x, xs)
                yield from bps.mv(piezo.y, ys)

                name_fmt = "{sam}_8.3m_16.1keV_pos{pos}_dn"
                sample_name = name_fmt.format(sam=sample, pos="%4.4d" % i)

                sample_id(user_name=name, sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")

                yield from bp.count(dets, num=1)
                yield from bps.sleep(2)

                i += 1

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def brian_caps(t=1):
    samples = [
        "sample44_1",
        "sample44_2",
        "sample45_1",
        "sample45_2",
        "sampleB_1",
        "sampleB_2",
        "sampleB_3",
        "sampleP_1",
        "sampleP_2",
    ]

    x_list = [-41000, -34350, -28400, -22000, -15700, -9350, -2700, 3400, 19200]

    y_list = [7600, 7600, 7700, 8000, 7800, 7500, 7500, 7500, 7500]

    z_list = [9600, 9600, 9600, 9600, 9600, 9600, 9600, 9600, 2600]

    # Detectors, motors:
    dets = [pil1M]
    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    assert len(x_list) == len(
        y_list
    ), f"Number of X coordinates ({len(x_list)}) is different from number of Y coord ({len(y_list)})"
    assert len(x_list) == len(
        z_list
    ), f"Number of X coordinates ({len(x_list)}) is different from number of Z coord ({len(z_list)})"
    ypos = [0, 50, 2]

    det_exposure_time(t, t)
    for x, y, z, sample in zip(x_list, y_list, z_list, samples):
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(piezo.y, y)
        yield from bps.mv(piezo.z, z)
        sample_id(user_name="BM", sample_name=sample)
        # yield from bp.rel_scan(dets, piezo.y, *ypos)
        yield from bp.count(dets, num=1)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def run_mesh_aaron(t=1):
    name = "AM"
    dets = [pil1M]
    det_exposure_time(t, t)

    # samples = ['sample_b1_area1', 'sample_b1_area2']
    # x_list = [45365, 46145]
    # y_list = [-1865, -1895]
    # x_range=[[0,150,7], [0,200,9]]
    # y_range=[[0,150,76],[0,150,76]]

    samples = [
        "sample_b1_area1_1",
        "sample_b1_area2_1",
        "sample_b2_area1",
        "sample_b2_area2",
        "sample_c1_area1",
        "sample_c1_area2",
        "sample_c2_area1",
        "sample_t1_area1",
        "sample_t1_area2",
    ]
    x_list = [45423, 46344, 22765, 22415, 2040, 540, -19755, -43785, -42785]
    y_list = [-2035, -2135, -1165, -1765, -590, -1770, -1095, 480, -120]
    x_range = [
        [0, 150, 7],
        [0, 150, 7],
        [0, 250, 13],
        [0, 200, 9],
        [0, 300, 13],
        [0, 300, 13],
        [0, 300, 13],
        [0, 500, 21],
        [0, 300, 13],
        [0, 150, 7],
    ]
    y_range = [
        [0, 200, 101],
        [0, 150, 76],
        [0, 150, 76],
        [0, 150, 76],
        [0, 300, 151],
        [0, 200, 101],
        [0, 200, 101],
        [0, 300, 151],
        [0, 200, 101],
        [0, 150, 76],
    ]

    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    for x, y, sample, x_r, y_r in zip(x_list, y_list, samples, x_range, y_range):
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(piezo.y, y)
        name_fmt = "{sam}"
        sample_name = name_fmt.format(sam=sample)
        sample_id(user_name=name, sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")
        yield from bp.rel_grid_scan(dets, piezo.y, *y_r, piezo.x, *x_r, 0)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)

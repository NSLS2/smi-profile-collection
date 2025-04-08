def ex_situ_hardxray(t=1):
    # samples = ['PLA2','PLA1','CON6','CON5', 'CON4','CON3','CON2','CON1',
    # '05_Ca_1', '05_Ca_2', '05_UT_1', '05_UT_2', 'PLA6','PLA4','PLA3',
    # ]

    # samples = ['B5_1','B5_2','B5_3', 'B6_1','B6_2','B6_3','B7_1','B7_2','B7_3','B12_1','B12_2','B12_3']
    # x_list  = [45550, 41200, 35600, 25600, 20900, 15400, -1900, -7900, -14000, -24100, -28200, -32700, ]
    # y_list =  [-9300, -9300, -9300, -9300, -9300, -9300, -9300, -9300, -9300, -9300, -9300, -9300]

    # samples = ['A1_1','A1_2','A1_3', 'A1_4','A2_5','A2_6','A2_7','A2_8','A3_9','A3_10','A3_11','A3_12','A3_13','A3_14','A4_15', 'A4_16', 'A4_17', 'A4_19']
    # x_list  = [45950, 43250, 37250, 31650, 24400, 18850, 12500, 8000, -3400, -7300, -11300, -16800, -20900, -26400, -33000,  -37400, -41900, -45200]
    # y_list =  [3500,  3500,  3500,  3500,  3500,  3500,  3500,  3500,  3500,  3500,  3500,  3500,   3500,   3500,    3500, 3500, 3500, 3500]

    # samples = ['C8_32', 'C8_33', 'C8_34', 'C8_35', 'C9_36', 'C9_37', 'C9_38', 'C9_39', 'C10_40', 'C10_41', 'C10_42', 'C10_43',
    # 'C10_44', 'C10_45', 'C11_46', 'C11_47', 'C11_48', 'C11_49', 'C11_50']
    # x_list  = [43700, 38300, 34000, 27800, 20900, 16200, 12100, 7100, -2700, -6700, -10500, -15700, -20000,
    # -24200, -29300, -32700, -36700, -41000, -45000]
    # y_list =  [3700,  3700,  3700,  3700,  3700,  3700,  3700,  3700, 3700,  3700,  3700,   3700,   3700,
    # 3700,   3700,    3700,   3700,  3700,  3700]

    samples = [
        "D13_51",
        "D13_52",
        "D13_53",
        "D14_54",
        "D14_55",
        "D14_56",
        "D15_57",
        "D15_58",
        "D15_59",
        "D16_60",
        "D16_61",
        "D16_62",
        "D16_63",
        "D16_64",
        "D17_65",
        "D17_66",
        "D17_67",
    ]
    x_list = [
        43700,
        38400,
        34000,
        25200,
        20000,
        15400,
        6700,
        2500,
        -2300,
        -6800,
        -14000,
        -19000,
        -23300,
        -28500,
        -34700,
        -39300,
        -43600,
    ]
    y_list = [
        -9880,
        -9880,
        -9880,
        -9880,
        -9880,
        -9880,
        -9880,
        -9880,
        -9880,
        -9880,
        -9880,
        -9880,
        -9880,
        -9880,
        -9880,
        -9880,
        -9880,
    ]

    # Detectors, motors:
    dets = [pil1M, pil300KW]
    waxs_range = np.linspace(13, 0, 3)

    ypos = [0, 400, 3]
    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    assert len(x_list) == len(
        y_list
    ), f"Number of X coordinates ({len(x_list)}) is different from number of Y coord ({len(y_list)})"

    det_exposure_time(t, t)

    for wa in waxs_range:
        yield from bps.mv(waxs, wa)
        for sam, x, y in zip(samples, x_list, y_list):
            yield from bps.mv(piezo.x, x)
            yield from bps.mv(piezo.y, y)

            name_fmt = "{sam}_wa{waxs}"
            sample_name = name_fmt.format(sam=sam, waxs="%2.1f" % wa)
            sample_id(user_name="OS", sample_name=sample_name)
            yield from bp.rel_scan(dets, piezo.y, *ypos)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def ex_situ_hardxray_2020_3(t=1):
    yield from bps.mv(stage.y, 0)
    yield from bps.mv(stage.th, 0)
    samples = [
        "F22_83",
        "F22_84",
        "F22_85",
        "F23_86",
        "F23_87",
        "F23_88",
        "F24_89",
        "F24_90",
        "F24_91",
        "F24_92",
        "F24_93",
        "F24_94",
        "F25_95",
        "F25_96",
        "F25_97",
        "F25_98",
    ]
    x_list = [
        45100,
        38750,
        33500,
        26450,
        21600,
        17300,
        7800,
        3600,
        -2300,
        -7800,
        -13400,
        -18500,
        -28800,
        -32400,
        -36700,
        -42500,
    ]
    y_list = [
        -1500,
        -1500,
        -1500,
        -1500,
        -1500,
        -1500,
        -1500,
        -1500,
        -1500,
        -1500,
        -1500,
        -1500,
        -1500,
        -1500,
        -1500,
        -1500,
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
    ]

    # Detectors, motors:
    dets = [pil1M, pil300KW]
    waxs_range = np.linspace(0, 32.5, 6)

    ypos = [0, 400, 3]
    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    assert len(x_list) == len(
        y_list
    ), f"Number of X coordinates ({len(x_list)}) is different from number of Y coord ({len(y_list)})"

    det_exposure_time(t, t)

    for wa in waxs_range:
        yield from bps.mv(waxs, wa)
        for sam, x, y, z in zip(samples, x_list, y_list, z_list):
            yield from bps.mv(piezo.x, x)
            yield from bps.mv(piezo.y, y)
            yield from bps.mv(piezo.z, z)

            name_fmt = "{sam}_wa{waxs}"
            sample_name = name_fmt.format(sam=sam, waxs="%2.1f" % wa)
            sample_id(user_name="OS", sample_name=sample_name)
            yield from bp.rel_scan(dets, piezo.y, *ypos)

    sample_id(user_name="test", sample_name="test")
    # det_exposure_time(0.3,0.3)

    yield from bps.mv(stage.th, 1.5)
    yield from bps.mv(stage.y, -11)
    samples = [
        "E18_67",
        "E18_68",
        "E18_69",
        "E19_70",
        "E19_71",
        "E19_72",
        "E19_73",
        "E19_74",
        "E19_75",
        "E20_76",
        "E20_77",
        "E20_78",
        "E21_79",
        "E21_80",
        "E21_81",
        "E22_82",
    ]
    x_list = [
        43500,
        37500,
        32100,
        23600,
        18350,
        13000,
        7200,
        3300,
        -450,
        -9400,
        -14300,
        -19400,
        -25900,
        -31300,
        -36200,
        -43200,
    ]
    y_list = [
        -9700,
        -9700,
        -9700,
        -9700,
        -9700,
        -9700,
        -9700,
        -9700,
        -9700,
        -9700,
        -9700,
        -9700,
        -9700,
        -9700,
        -9700,
        -9700,
    ]
    z_list = [
        4200,
        4200,
        4200,
        4200,
        4200,
        4200,
        4200,
        4200,
        4200,
        4200,
        4200,
        4200,
        4200,
        4200,
        4200,
        4200,
    ]

    # Detectors, motors:
    dets = [pil1M, pil300KW]
    waxs_range = np.linspace(0, 32.5, 6)

    ypos = [0, 400, 3]
    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    assert len(x_list) == len(
        y_list
    ), f"Number of X coordinates ({len(x_list)}) is different from number of Y coord ({len(y_list)})"

    det_exposure_time(t, t)

    for wa in waxs_range:
        yield from bps.mv(waxs, wa)
        for sam, x, y, z in zip(samples, x_list, y_list, z_list):
            yield from bps.mv(piezo.x, x)
            yield from bps.mv(piezo.y, y)
            yield from bps.mv(piezo.z, z)

            name_fmt = "{sam}_16.1keV_wa{waxs}"
            sample_name = name_fmt.format(sam=sam, waxs="%2.1f" % wa)
            sample_id(user_name="OS", sample_name=sample_name)
            yield from bp.rel_scan(dets, piezo.y, *ypos)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)

    # def ex_situ_hardxray_2021_1(t=1):
    #     yield from bps.mv(stage.y, 0)
    #     yield from bps.mv(stage.th, 0)
    #     samples = ['F22_83','F22_84','F22_85','F23_86','F23_87','F23_88','F24_89','F24_90','F24_91','F24_92','F24_93','F24_94','F25_95','F25_96','F25_97','F25_98']
    #     x_list  = [45100, 38750, 33500, 26450, 21600, 17300,  7800,  3600, -2300, -7800, -13400, -18500, -28800, -32400, -36700, -42500]
    #     y_list =  [-1500, -1500, -1500, -1500, -1500, -1500, -1500, -1500, -1500, -1500,  -1500,  -1500,  -1500,  -1500,  -1500,  -1500]
    #     z_list =  [ 2700,  2700,  2700,  2700,  2700,  2700,  2700,  2700,  2700,  2700,   2700,   2700,   2700,   2700,   2700,   2700]

    #     # Detectors, motors:
    #     dets = [pil1M, pil300KW]
    #     waxs_range = np.linspace(0, 32.5, 6)

    #     ypos = [0, 400, 3]
    #     assert len(x_list) == len(samples), f'Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})'
    #     assert len(x_list) == len(y_list), f'Number of X coordinates ({len(x_list)}) is different from number of Y coord ({len(y_list)})'

    #     det_exposure_time(t,t)

    #     for wa in waxs_range:
    #         yield from bps.mv(waxs, wa)
    #         for sam, x, y, z in zip(samples, x_list, y_list, z_list):
    #             yield from bps.mv(piezo.x, x)
    #             yield from bps.mv(piezo.y, y)
    #             yield from bps.mv(piezo.z, z)

    #             name_fmt = '{sam}_wa{waxs}'
    #             sample_name = name_fmt.format(sam=sam, waxs='%2.1f'%wa)
    #             sample_id(user_name='OS', sample_name=sample_name)
    #             yield from bp.rel_scan(dets, piezo.y, *ypos)

    #     sample_id(user_name='test', sample_name='test')
    #     # det_exposure_time(0.3,0.3)

    #     yield from bps.mv(stage.th, 1.5)
    #     yield from bps.mv(stage.y, -11)
    #     samples = ['E18_67','E18_68','E18_69','E19_70','E19_71','E19_72','E19_73','E19_74','E19_75','E20_76','E20_77','E20_78','E21_79','E21_80','E21_81','E22_82']
    #     x_list  = [43500, 37500, 32100, 23600, 18350, 13000,  7200,  3300,  -450, -9400, -14300, -19400, -25900, -31300, -36200, -43200]
    #     y_list =  [-9700, -9700, -9700, -9700, -9700, -9700, -9700, -9700, -9700, -9700,  -9700,  -9700,  -9700,  -9700,  -9700,  -9700]
    #     z_list =  [ 4200,  4200,  4200,  4200,  4200,  4200,  4200,  4200,  4200,  4200,   4200,   4200,   4200,   4200,   4200,   4200]

    #     # Detectors, motors:
    #     dets = [pil1M, pil300KW]
    #     waxs_range = np.linspace(0, 32.5, 6)

    #     ypos = [0, 400, 3]
    #     assert len(x_list) == len(samples), f'Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})'
    #     assert len(x_list) == len(y_list), f'Number of X coordinates ({len(x_list)}) is different from number of Y coord ({len(y_list)})'

    #     det_exposure_time(t,t)

    #     for wa in waxs_range:
    #         yield from bps.mv(waxs, wa)
    #         for sam, x, y, z in zip(samples, x_list, y_list, z_list):
    #             yield from bps.mv(piezo.x, x)
    #             yield from bps.mv(piezo.y, y)
    #             yield from bps.mv(piezo.z, z)

    #             name_fmt = '{sam}_16.1keV_wa{waxs}'
    #             sample_name = name_fmt.format(sam=sam, waxs='%2.1f'%wa)
    #             sample_id(user_name='OS', sample_name=sample_name)
    #             yield from bp.rel_scan(dets, piezo.y, *ypos)

    #     sample_id(user_name='test', sample_name='test')
    det_exposure_time(0.3, 0.3)


def ex_situ_hardxray_2021_1(t=1):

    yield from bps.mv(stage.th, 0)
    yield from bps.mv(stage.y, 0)
    # samples = ['P1_1', 'P1_2', 'P1_3', 'P2_1', 'P2_2', 'P2_3', 'P3_1', 'P3_2', 'P3_3', 'P4_1', 'P4_2', 'P4_3', 'P5_1', 'P5_2', 'P5_3',
    # 'P6_1', 'P6_2', 'P6_3', 'P7_1', 'P7_2', 'P7_3', 'P8_1', 'P8_2', 'P8_3']
    # x_list  = [ 45400, 41100, 37500, 32400, 29400, 25900, 20200, 16700, 13100, 6800, 3700, 200, -4600, -8400, -12000, -17200, -20600,
    # -24000, -29400, -33100, -36200, -40000, -42500, -45500]
    # y_list =  [ -3000,  -3000,  -3000,  -3000,  -3000,  -3000,  -3000,  -3000,  -3000, -3000, -3000, -3000,  -3000,  -3000,   -3000,   -3000,   -3000,
    #     -3000,   -3000,   -3000,   -3000,   -3000,   -3000,   -3000]
    # z_list =  [  4000,  4000,  4100,  4100,  4200,  4200,  4200,  4200,  4300, 4300, 4400, 4400,  4500,  4500,   4600,   4600,   4700,
    #     4700,   4800,   4800,   4900,   4900,   5000,   5000]

    samples = [
        "N1_1",
        "N1_2",
        "N1_3",
        "N1_4",
        "N2_1",
        "N2_2",
        "N2_3",
        "N2_4",
        "N3_1",
        "N3_2",
        "N3_3",
        "N4_1",
        "N4_2",
        "N4_3",
        "N5_1",
        "N5_2",
        "N5_3",
    ]
    x_list = [
        45300,
        41400,
        38200,
        34700,
        29600,
        26300,
        22900,
        18400,
        7700,
        3100,
        -1300,
        -9300,
        -14200,
        -19600,
        -28600,
        -35100,
        -41200,
    ]
    y_list = [
        -2500,
        -2500,
        -2500,
        -2500,
        -2500,
        -2500,
        -2500,
        -2500,
        -2500,
        -2500,
        -2500,
        -2500,
        -2500,
        -2500,
        -2500,
        -2500,
        -2500,
    ]
    z_list = [
        4500,
        4500,
        4500,
        4500,
        4500,
        4500,
        4500,
        4500,
        4500,
        4500,
        4500,
        4500,
        4500,
        4500,
        4500,
        4500,
        4500,
    ]

    # Detectors, motors:
    dets = [pil1M, pil300KW]
    waxs_range = np.linspace(0, 32.5, 6)

    ypos = [0, 400, 3]
    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    assert len(x_list) == len(
        y_list
    ), f"Number of X coordinates ({len(x_list)}) is different from number of Y coord ({len(y_list)})"

    det_exposure_time(t, t)

    for wa in waxs_range:
        yield from bps.mv(waxs, wa)
        for sam, x, y, z in zip(samples, x_list, y_list, z_list):
            yield from bps.mv(piezo.x, x)
            yield from bps.mv(piezo.y, y)
            yield from bps.mv(piezo.z, z)

            name_fmt = "{sam}_wa{waxs}_sdd8.3m_16.1keV"
            sample_name = name_fmt.format(sam=sam, waxs="%2.1f" % wa)
            sample_id(user_name="OS", sample_name=sample_name)
            yield from bp.rel_scan(dets, piezo.y, *ypos)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)

    # yield from bps.mv(stage.th, 2.5)
    # yield from bps.mv(stage.y, -13)
    # samples = ['R1_1', 'R1_2', 'R1_3', 'R2_1', 'R2_2', 'R2_3', 'R3_1', 'R3_2', 'R3_3', 'R4_1', 'R4_2', 'R4_3', 'R5_1', 'R5_2', 'R5_3']
    # x_list  = [ 44800,  40300,  34800,  24800,  18800,  12300,   4000,  -1700,  -7800, -13700, -20700, -27700, -33200, -38200, -43400]
    # y_list =  [ -9500,  -9500,  -9500,  -9500,  -9500,  -9500,  -9500,  -9500,  -9500,  -9500,  -9500,  -9500,  -9500,  -9500,  -9500]
    # z_list =  [  3000,   3000,   3000,   3000,   3000,   3000,   3000,   3000,   3000,   3000,   3000,   3000,   3000,   3000,   3000]

    # for wa in waxs_range:
    #     yield from bps.mv(waxs, wa)
    #     for sam, x, y, z in zip(samples, x_list, y_list, z_list):
    #         yield from bps.mv(piezo.x, x)
    #         yield from bps.mv(piezo.y, y)
    #         yield from bps.mv(piezo.z, z)

    #         name_fmt = '{sam}_wa{waxs}_sdd8.3m_16.1keV'
    #         sample_name = name_fmt.format(sam=sam, waxs='%2.1f'%wa)
    #         sample_id(user_name='OS', sample_name=sample_name)
    #         yield from bp.rel_scan(dets, piezo.y, *ypos)

    # sample_id(user_name='test', sample_name='test')
    # det_exposure_time(0.3,0.3)


def run_saxs_nexafs(t=1):
    yield from waxs_prep_multisample_nov(t=0.5)
    # yield from bps.sleep(10)
    # yield from nexafs_prep_multisample_nov(t=1)


def saxs_prep_multisample_nov(t=1):
    dets = [pil1M]
    energies = [4030, 4040, 4050, 4055, 4065, 4075, 4105]
    det_exposure_time(t, t)
    name_fmt = "{sample}_{energy}eV_pos{posi}_wa{wa}_xbpm{xbpm}"
    waxs_range = [32.5]

    ypos = [0, 400, 3]
    for wa in waxs_range:
        yield from bps.mv(waxs, wa)
        yield from bps.mv(stage.th, 3.5)
        yield from bps.mv(stage.y, -13)

        # samples = ['K5-6', 'K5-5', 'K5-4', 'K5-3', 'K5-2', 'K5-1', 'K4-3', 'K4-2', 'K4-1', 'K3-3', 'K3-2', 'K3-1', 'K2-3', 'K2-2', 'K2-1', 'K1-3', 'K1-2', 'K1-1']
        # x_list  = [41400, 37700,34300,26750,23800,20600,1700,-2100,-5300,-10200,-14150,-19200,-27500,-32000,-37500,-41100,-45800,-49400]
        # y_list =  [-9500, -9500,-9500,-9500,-9500,-9500,-9500,-9500,-9500,-9500, -9500, -9500, -9500, -9500, -9500, -9500, -9700, -9500]
        # z_list =  [ 5500,  5500, 5400, 5300, 5200, 5100, 5000, 4900, 4800, 4700,  4600,  4500,  4400,  4300,  4200,  4100,  4000,  3900]

        # samples = ['M14-1', 'M14-2', 'M14-3', 'M15-1', 'M15-2', 'M15-3', 'M16-1', 'M16-2', 'M16-3', 'M17-1', 'M17-2', 'M17-3', 'M18-1', 'M18-2', 'M18-3', 'M18-4', 'M18-5']
        # x_list  = [  46900,   44500,   41500,   31900,   27300,   22750,   12750,   10500,    7800,   -2800,   -4900,   -9100,  -17400,  -20800,  -23800,  -26550,  -29950]
        # y_list =  [  -8500,   -8500,   -8500,   -8500,   -8500,   -8500,   -8500,   -8500,   -8500,   -8100,   -8500,   -8500,   -8500,   -8500,   -8500,   -8500,   -8500]
        # z_list =  [   4800,    4800,    4700,    4600,    4500,    4500,    4400,    4300,    4200,    4100,    4100,    4000,    3900,    3800,    3800,    3700,    3600]

        samples = [
            "M16-2",
            "M16-3",
            "M17-1",
            "M17-2",
            "M17-3",
            "M18-1",
            "M18-2",
            "M18-3",
            "M18-4",
            "M18-5",
        ]
        x_list = [
            10500,
            7800,
            -2800,
            -4900,
            -9100,
            -17400,
            -20800,
            -23800,
            -26550,
            -29950,
        ]
        y_list = [-8500, -8500, -8100, -8500, -8500, -8500, -8500, -8500, -8500, -8500]
        z_list = [4300, 4200, 4100, 4100, 4000, 3900, 3800, 3800, 3700, 3600]

        for x, y, z, name in zip(x_list, y_list, z_list, samples):
            yield from bps.mv(piezo.x, x)
            yield from bps.mv(piezo.y, y)
            yield from bps.mv(piezo.z, z)

            for k, e in enumerate(energies):
                yield from bps.mv(energy, e)
                yield from bps.sleep(3)
                name_fmt = "{sample}_{energy}eV_5m_xbpm{xbpm}_wa{wa}"

                sample_name = name_fmt.format(
                    sample=name,
                    energy=e,
                    xbpm="%3.1f" % xbpm3.sumY.value,
                    wa="%2.1f" % wa,
                )
                sample_id(user_name="OS", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.rel_scan(dets, piezo.y, *ypos)

            yield from bps.mv(energy, 4080)
            yield from bps.mv(energy, 4055)
            yield from bps.mv(energy, 4030)

    # for wa in waxs_range:
    #     yield from bps.mv(waxs, wa)
    #     yield from bps.mv(stage.y, 0)
    #     yield from bps.mv(stage.th, 0)

    #     samples = ['L13-3', 'L13-2', 'L13-1', 'L12-3', 'L12-2', 'L12-1', 'L11-3', 'L11-2', 'L11-1', 'L10-3', 'L10-2', 'L10-1', 'L9-3', 'L9-2', 'L9-1', 'L8-3', 'L8-2',
    #     'L8-1', 'L7-3', 'L7-2', 'L7-1', 'L6-3', 'L6-2', 'L6-1']
    #     x_list  = [40600, 37500, 34500, 29400, 25600, 22300, 17100, 14250, 10800,  5900,  3450,  550, -5050, -7250, -9100, -13900,-16200,-18500,-22300,-24700,-27050,
    #     -34800, -38450, -42250]
    #     y_list =  [-1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000,
    #     -1000,  -1000,  -1000]
    #     z_list =  [ 5400, 5400,   5300,  5200,  5100,  5000,  4900,  4800,  4700,  4600,  4500,  4400,  4300,  4200,  4100,  4000,  3900,  3800,  3700,   3600, 3500,
    #     3300,   3400,   3300]

    #     assert len(x_list) == len(samples), f'Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})'
    #     assert len(x_list) == len(y_list), f'Number of X coordinates ({len(x_list)}) is different from number of Y coord ({len(y_list)})'
    #     assert len(x_list) == len(z_list), f'Number of X coordinates ({len(x_list)}) is different from number of z coord ({len(z_list)})'

    #     for x, y, z, name in zip(x_list, y_list, z_list, samples):
    #         yield from bps.mv(piezo.x, x)
    #         yield from bps.mv(piezo.y, y)
    #         yield from bps.mv(piezo.z, z)

    #         for k, e in enumerate(energies):
    #             yield from bps.mv(energy, e)
    #             yield from bps.sleep(3)

    #             name_fmt = '{sample}_{energy}eV_xbpm{xbpm}_wa{wa}'

    #             sample_name = name_fmt.format(sample=name, energy=e, xbpm = '%3.1f'%xbpm3.sumY.value, wa='%2.1f'%wa)
    #             sample_id(user_name='OS', sample_name=sample_name)
    #             print(f'\n\t=== Sample: {sample_name} ===\n')
    #             yield from bp.rel_scan(dets, piezo.y, *ypos)

    #         yield from bps.mv(energy, 4080)
    #         yield from bps.mv(energy, 4055)
    #         yield from bps.mv(energy, 4030)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def waxs_prep_multisample_nov(t=1):
    dets = [pil300KW]
    energies = [4030, 4040, 4050, 4055, 4065, 4075, 4105]
    det_exposure_time(t, t)
    name_fmt = "{sample}_{energy}eV_pos{posi}_wa{wa}_xbpm{xbpm}"
    waxs_range = [0, 6.5, 13.0, 19.5, 26, 32.5, 39.0, 45.5]

    ypos = [0, 400, 3]
    # for wa in waxs_range:
    #     yield from bps.mv(waxs, wa)
    #     yield from bps.mv(stage.th, 3.5)
    #     yield from bps.mv(stage.y, -13)

    #     # samples = ['K5-6', 'K5-5', 'K5-4', 'K5-3', 'K5-2', 'K5-1', 'K4-3', 'K4-2', 'K4-1', 'K3-3', 'K3-2', 'K3-1', 'K2-3', 'K2-2', 'K2-1', 'K1-3', 'K1-2', 'K1-1']
    #     # x_list  = [41400, 37700,34300,26750,23800,20600,1700,-2100,-5300,-10200,-14150,-19200,-27500,-32000,-37500,-41100,-45800,-49400]
    #     # y_list =  [-9500, -9500,-9500,-9500,-9500,-9500,-9500,-9500,-9500,-9500, -9500, -9500, -9500, -9500, -9500, -9500, -9700, -9500]
    #     # z_list =  [ 5500,  5500, 5400, 5300, 5200, 5100, 5000, 4900, 4800, 4700,  4600,  4500,  4400,  4300,  4200,  4100,  4000,  3900]

    #     samples = ['M14-1', 'M14-2', 'M14-3', 'M15-1', 'M15-2', 'M15-3', 'M16-1', 'M16-2', 'M16-3', 'M17-1', 'M17-2', 'M17-3', 'M18-1', 'M18-2', 'M18-3', 'M18-4', 'M18-5']
    #     x_list  = [  46900,   44500,   41500,   31900,   27300,   22750,   12750,   10500,    7800,   -2800,   -4900,   -9100,  -17400,  -20800,  -23800,  -26550,  -29950]
    #     y_list =  [  -8500,   -8500,   -8500,   -8500,   -8500,   -8500,   -8500,   -8500,   -8500,   -8100,   -8500,   -8500,   -8500,   -8500,   -8500,   -8500,   -8500]
    #     z_list =  [   4800,    4800,    4700,    4600,    4500,    4500,    4400,    4300,    4200,    4100,    4100,    4000,    3900,    3800,    3800,    3700,    3600]

    #     for x, y, z, name in zip(x_list, y_list, z_list, samples):
    #         yield from bps.mv(piezo.x, x)
    #         yield from bps.mv(piezo.y, y)
    #         yield from bps.mv(piezo.z, z)

    #         for k, e in enumerate(energies):
    #             yield from bps.mv(energy, e)
    #             yield from bps.sleep(3)
    #             name_fmt = '{sample}_{energy}eV_xbpm{xbpm}_wa{wa}'

    #             sample_name = name_fmt.format(sample=name, energy=e, xbpm = '%3.1f'%xbpm3.sumY.value, wa='%2.1f'%wa)
    #             sample_id(user_name='OS', sample_name=sample_name)
    #             print(f'\n\t=== Sample: {sample_name} ===\n')
    #             yield from bp.rel_scan(dets, piezo.y, *ypos)

    #         yield from bps.mv(energy, 4080)
    #         yield from bps.mv(energy, 4055)
    #         yield from bps.mv(energy, 4030)

    # energies = [4030, 4040, 4050, 4055, 4065, 4075, 4105]
    # waxs_range = [0, 6.5, 13.0, 19.5, 26, 32.5, 39.0, 45.5]
    # for wa in waxs_range:
    #     yield from bps.mv(waxs, wa)
    #     yield from bps.mv(stage.y, 0)
    #     yield from bps.mv(stage.th, 0)

    #     # samples = ['L13-3', 'L13-2', 'L13-1', 'L12-3', 'L12-2', 'L12-1', 'L11-3', 'L11-2', 'L11-1', 'L10-3', 'L10-2', 'L10-1', 'L9-3', 'L9-2', 'L9-1', 'L8-3', 'L8-2',
    #     # 'L8-1', 'L7-3', 'L7-2', 'L7-1', 'L6-3', 'L6-2', 'L6-1']
    #     # x_list  = [40600, 37500, 34500, 29400, 25600, 22300, 17100, 14250, 10800,  5900,  3450,  550, -5050, -7250, -9100, -13900,-16200,-18500,-22300,-24700,-27050,
    #     # -34800, -38450, -42250]
    #     # y_list =  [-1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000,
    #     # -1000,  -1000,  -1000]
    #     # z_list =  [ 5400, 5400,   5300,  5200,  5100,  5000,  4900,  4800,  4700,  4600,  4500,  4400,  4300,  4200,  4100,  4000,  3900,  3800,  3700,   3600, 3500,
    #     # 3300,   3400,   3300]

    #     samples = [ 'P1', 'P2', 'E1',  'E2',  'PG1',  'PG2']
    #     x_list  = [11400, 6200,  200, -5200, -13200, -26200]
    #     y_list =  [-1000, -900, -900,  -700,  -1300,  -1300]
    #     z_list =  [ 4500, 4300, 4200,  4100,   4000,   4000]

    # assert len(x_list) == len(samples), f'Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})'
    # assert len(x_list) == len(y_list), f'Number of X coordinates ({len(x_list)}) is different from number of Y coord ({len(y_list)})'
    # assert len(x_list) == len(z_list), f'Number of X coordinates ({len(x_list)}) is different from number of z coord ({len(z_list)})'

    # for x, y, z, name in zip(x_list, y_list, z_list, samples):
    #     yield from bps.mv(piezo.x, x)
    #     yield from bps.mv(piezo.y, y)
    #     yield from bps.mv(piezo.z, z)

    #     for k, e in enumerate(energies):
    #         yield from bps.mv(energy, e)
    #         yield from bps.sleep(3)

    #         name_fmt = '{sample}_{energy}eV_xbpm{xbpm}_wa{wa}'

    #         sample_name = name_fmt.format(sample=name, energy=e, xbpm = '%3.1f'%xbpm3.sumY.value, wa='%2.1f'%wa)
    #         sample_id(user_name='OS', sample_name=sample_name)
    #         print(f'\n\t=== Sample: {sample_name} ===\n')
    #         yield from bp.rel_scan(dets, piezo.y, *ypos)

    #     yield from bps.mv(energy, 4080)
    #     yield from bps.mv(energy, 4055)
    #     yield from bps.mv(energy, 4030)

    energies = (
        np.arange(4030, 4040, 5).tolist()
        + np.arange(4040, 4060, 0.5).tolist()
        + np.arange(4060, 4080, 2).tolist()
        + np.arange(4080, 4150, 5).tolist()
    )
    # waxs_range = [0, 6.5, 13.0, 19.5, 26, 32.5, 39.0, 45.5]
    waxs_range = [6.5]

    for wa in waxs_range:
        yield from bps.mv(waxs, wa)
        yield from bps.mv(stage.y, 0)
        yield from bps.mv(stage.th, 0)

        # samples = [ 'U1',  'U2',  'Ca1',  'Ca2']
        # x_list  = [43000, 31000, -36500, -44000]
        # y_list =  [ -700,  -700,   -900,   -900]
        # z_list =  [ 4600,  4600,   3600,   3600]

        samples = ["Ca2"]
        x_list = [-44000]
        y_list = [-900]
        z_list = [3600]

        assert len(x_list) == len(
            samples
        ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
        assert len(x_list) == len(
            y_list
        ), f"Number of X coordinates ({len(x_list)}) is different from number of Y coord ({len(y_list)})"
        assert len(x_list) == len(
            z_list
        ), f"Number of X coordinates ({len(x_list)}) is different from number of z coord ({len(z_list)})"

        for x, y, z, name in zip(x_list, y_list, z_list, samples):
            yield from bps.mv(piezo.x, x)
            yield from bps.mv(piezo.y, y)
            yield from bps.mv(piezo.z, z)

            for k, e in enumerate(energies):
                yield from bps.mv(energy, e)
                yield from bps.sleep(3)

                name_fmt = "{sample}_{energy}eV_xbpm{xbpm}_wa{wa}"

                sample_name = name_fmt.format(
                    sample=name,
                    energy=e,
                    xbpm="%3.1f" % xbpm3.sumY.value,
                    wa="%2.1f" % wa,
                )
                sample_id(user_name="OS", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.rel_scan(dets, piezo.y, *ypos)

            yield from bps.mv(energy, 4120)
            yield from bps.mv(energy, 4090)
            yield from bps.mv(energy, 4060)
            yield from bps.mv(energy, 4030)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def nexafs_prep_multisample_nov(t=1):

    # samples = ['K5-6', 'K5-5', 'K5-4', 'K5-3', 'K5-2', 'K5-1', 'K4-3', 'K4-2', 'K4-1', 'K3-3', 'K3-2', 'K3-1', 'K2-3', 'K2-2', 'K2-1', 'K1-3', 'K1-2', 'K1-1']
    # x_list  = [41400,   37700,  34300,  26750,  23800,  20600,   1700,  -2100,  -5300, -10200,-14150,-19200,-27500,-32000,-37500,-41100,-45800,-49400]
    # y_list =  [-9500,   -9500,  -9500,  -9500,  -9500,  -9500,  -9500,-  9500,  -9500,-9500, -9500, -9500, -9500, -9500, -9500, -9500, -9700, -9500]
    # z_list =  [ 5500,    5500,   5400,   5300,   5200,   5100,   5000,   4900,   4800, 4700,  4600,  4500,  4400,  4300,  4200,  4100,  4000,  3900]

    yield from bps.mv(stage.th, 3.5)
    yield from bps.mv(stage.y, -13)
    samples = [
        "M14-1",
        "M14-2",
        "M14-3",
        "M15-1",
        "M15-2",
        "M15-3",
        "M16-1",
        "M16-2",
        "M16-3",
        "M17-1",
        "M17-2",
        "M17-3",
        "M18-1",
        "M18-2",
        "M18-3",
        "M18-4",
        "M18-5",
    ]
    x_list = [
        46900,
        44500,
        41500,
        31900,
        27300,
        22750,
        12750,
        10500,
        7800,
        -2800,
        -4900,
        -9100,
        -17400,
        -20800,
        -23800,
        -26550,
        -29950,
    ]
    y_list = [
        -8500,
        -8500,
        -8500,
        -8500,
        -8500,
        -8500,
        -8500,
        -8500,
        -8500,
        -8100,
        -8500,
        -8500,
        -8500,
        -8500,
        -8500,
        -8500,
        -8500,
    ]
    z_list = [
        4800,
        4800,
        4700,
        4600,
        4500,
        4500,
        4400,
        4300,
        4200,
        4100,
        4100,
        4000,
        3900,
        3800,
        3800,
        3700,
        3600,
    ]

    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    assert len(x_list) == len(
        y_list
    ), f"Number of X coordinates ({len(x_list)}) is different from number of Y coord ({len(y_list)})"
    assert len(x_list) == len(
        z_list
    ), f"Number of X coordinates ({len(x_list)}) is different from number of Y coord ({len(z_list)})"

    for x, y, z, name in zip(x_list, y_list, z_list, samples):
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(piezo.y, y)
        yield from bps.mv(piezo.z, z)

        yield from NEXAFS_Ca_edge_multi(t=t, name=name)

    yield from bps.mv(stage.y, 0)
    yield from bps.mv(stage.th, 0)

    # samples = ['L13-3', 'L13-2', 'L13-1', 'L12-3', 'L12-2', 'L12-1', 'L11-3', 'L11-2', 'L11-1', 'L10-3', 'L10-2', 'L10-1', 'L9-3', 'L9-2', 'L9-1', 'L8-3', 'L8-2',
    #  'L8-1', 'L7-3', 'L7-2', 'L7-1', 'L6-3', 'L6-2', 'L6-1']
    # x_list  = [40600, 37500, 34500, 29400, 25600, 22300, 17100, 14250, 10800,  5900,  3450,  550, -5050, -7250, -9100, -13900,-16200,-18500,-22300,-24700,-27050,
    # -34800, -38450, -42250]
    # y_list =  [-1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000,
    #  -1000,  -1000,  -1000]
    # z_list =  [ 5400, 5400,   5300,  5200,  5100,  5000,  4900,  4800,  4700,  4600,  4500,  4400,  4300,  4200,  4100,  4000,  3900,  3800,  3700,   3600, 3500,
    #   3300,   3400,   3300]

    samples = ["C1", "C2", "P1", "P2", "E1", "E2", "PG1", "PG2"]
    x_list = [21800, 16500, 11400, 6200, 200, -5200, -13200, -26200]
    y_list = [-900, -700, -800, -700, -700, -500, -1100, -1100]
    z_list = [4600, 4600, 4500, 4300, 4200, 4100, 4000, 4000]

    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    assert len(x_list) == len(
        y_list
    ), f"Number of X coordinates ({len(x_list)}) is different from number of Y coord ({len(y_list)})"
    assert len(x_list) == len(
        z_list
    ), f"Number of X coordinates ({len(x_list)}) is different from number of z coord ({len(z_list)})"

    for x, y, z, name in zip(x_list, y_list, z_list, samples):
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(piezo.y, y)
        yield from bps.mv(piezo.z, z)

        yield from NEXAFS_Ca_edge_multi(t=t, name=name)

    # sample_id(user_name='test', sample_name='test')
    # yield from bps.mv(att2_11, 'Insert')
    # yield from bps.mv(GV7.open_cmd, 1 )
    # yield from bps.sleep(2)
    # yield from bps.mv(att2_11, 'Insert')
    # yield from bps.mv(GV7.open_cmd, 1 )


def NEXAFS_Ca_edge_multi(t=0.5, name="test"):
    yield from bps.mv(waxs, 52)

    dets = [pil300KW]

    energies = np.linspace(4030, 4150, 121)

    det_exposure_time(t, t)
    name_fmt = "nexafs_{sample}_{energy}eV_xbpm{xbpm}"
    for e in energies:
        yield from bps.mv(energy, e)
        yield from bps.sleep(3)
        sample_name = name_fmt.format(
            sample=name, energy=e, xbpm="%3.1f" % xbpm3.sumY.value
        )
        RE.md["filename_amptek"] = sample_name
        sample_id(user_name="OS", sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")
        yield from bp.count(dets, num=1)

    yield from bps.mv(energy, 4125)
    yield from bps.mv(energy, 4100)
    yield from bps.mv(energy, 4075)
    yield from bps.mv(energy, 4050)
    yield from bps.mv(energy, 4030)

    sample_id(user_name="test", sample_name="test")

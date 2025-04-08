# command for running the code
# %run -i /home/xf12id/.ipython/profile_collection/startup/users/30-user-Cai.py



def mapping_saxs_Cai(t=1):
    samples = [
        "3Dprinted_filament_sr3",
        "3Dprinted_filament_sr30",
        "3Dprinted_filament_sr300",
        "3Dprinted_filament_sr3000",
        "Interface_3Dpr_sp0.5",
        "Interface_3Dpr_sp0.7",
        "Interface_3Dpr_sp0.9",
        "Interface_3Dpr_sp1.1",
    ]

    x_list = [38000, 26000, 13200, 2600, -10600, -22600, -32600, -43600]
    y_list = [100, -450, 600, -100, -300, -2300, -2000, -2100]

    name = "PT"

    x_range = [
        [0, 5000, 11],
        [0, 5000, 11],
        [0, 5000, 11],
        [0, 5000, 11],
        [0, 5000, 11],
        [0, 5000, 11],
        [0, 5000, 11],
        [0, 5000, 11],
    ]
    y_range = [
        [0, 800, 41],
        [0, 1000, 51],
        [0, 1100, 56],
        [0, 1000, 51],
        [0, 3400, 171],
        [0, 4500, 226],
        [0, 5200, 261],
        [0, 6300, 316],
    ]

    # Detectors, motors:
    dets = [pil1M]  # dets = [pil1M,pil300KW]
    det_exposure_time(t, t)

    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    for x, y, sample, x_r, y_r in zip(x_list, y_list, samples, x_range, y_range):
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(piezo.y, y)
        sample_id(user_name=name, sample_name=sample)
        yield from bp.rel_grid_scan(dets, piezo.x, *x_r, piezo.y, *y_r, 0)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def saxs_cap_cai(t=1):
    # xlocs = [-38000, -25000,-12500, -6800, -200, 6600, 12900, 19200, 25900, 32300, 44800]
    xlocs = [-44300]
    # ylocs = [-6800, -1700,-9600, 9000, 300, -2200, 9000, 9000, 9000, 6600, 5000, 7000]
    ylocs = [-9300]
    # names = ['BnMA0.0','BnMA0.3','BnMA0.6','BnMA0.80','BnMA0.85','BnMA1.1','BnMA2.0','BnMA3.0','BnMA5.5','BnMA0.54','BnMA1.1_new'][::-1]
    names = [
        "Cap_bkg",
    ]

    user = "LC"
    det_exposure_time(t, t)

    assert len(xlocs) == len(
        names
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"

    # Detectors, motors:
    dets = [pil1M, pil300KW]
    waxs_range = np.linspace(13, 0, 3)

    # x_off = [-1000, 0, 1000]

    for wa in waxs_range:
        yield from bps.mv(waxs, wa)
        for sam, x, y in zip(names, xlocs, ylocs):
            yield from bps.mv(piezo.x, x)
            yield from bps.mv(piezo.y, y)

            # for xx, x_of in enumerate(x_off):
            #     yield from bps.mv(piezo.x, x+x_of)
            #     xxa = xx+1

            name_fmt = "{sam}_cap_wa{waxs}"
            sample_name = name_fmt.format(sam=sam, waxs="%2.1f" % wa)
            sample_id(user_name=user, sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def saxs_cai_2020_3(t=1):
    # xlocs = [-43000, -31000, -20000, -7500, 7000,  19200, 30500, 42500,
    #         -44000,  -36000, -26500, -16000, -5500, 4000, 14000, 25000, 35500, 46000]
    # ylocs = [-9000,   -9000,  -9000,  -9000, -9000, -9500, -8400, -9000,
    #           8700,    8900,   8900,   8900,  8900,  9100, 9100,  9100,  9100, 8700]
    # zlocs = [2900,    2900,    2900,   2900,  2900,  2900,  2900,  2900,
    #         -1100,   -1100,   -1100,  -1100, -1100, -1100, -1100, -1100, -1100,  -1100]
    # names = ['BMMB_1.74', 'BMMB_1.14', 'BMMB_0.84', 'BMMB_0.434', 'BMMB_0.35', 'M17n_0.04', 'M17n_0.05', 'M17n_0.06',
    #          'M17n_0.08', 'M17n_0.12', 'M17n_0.17', 'M17n_0.21', 'M17n_0.24', 'M17n_0.28', 'M17n_0.30', 'M17n_0.34', 'M17n_0.35', 'M17n_0.40' ]

    # xlocs = [-43000, -30500, -17500, -3420,  6880, 12140, 27340, 38240]
    # ylocs = [  8700,   8700,   8700,  8900, -9000, -7600,  7315,  9515]
    # zlocs = [-1100,   -1100,  -1100, -1100, -1100, -1100, -1100, -1100]
    # names = ['M17n_0.44', 'LhBBL_0.64', 'bbPDMS_1', 'hDPDMS_0.64', 'hDPDMS_0.84', 'hDPDMS_0.94', 'hDPDMS_1.08', 'bbPDMS_5']

    xlocs = [
        -11820,
    ]
    ylocs = [-8400]
    zlocs = [3700]
    names = ["BM_0.875"]

    # xlocs = [-43740, -37440, -31100, -24640, -18460, -5680,  600, 6940, 13200, 19660, 26160, 32780, 38940, 45020]
    # ylocs = [   200,    200,    200,    200,    200,   200,  200,  200,   600,   200,   200,   200,   200,   200]
    # zlocs = [  3700,   3700,   3700,   3700,   3700,  3700, 3700, 3700,  3700,  3700,  3700,  3700,  3700,  3700]
    # names = ['BM_2.15', 'BM_1.475', 'BM_1.42', 'BM_1.26', 'BM_1.00', 'BM_0.825', 'BM_0.6', 'BM_0.31', 'PDMS', 'MM_1.74', 'MM_1.14', 'MM_0.84',
    # 'MM_0.434', 'MM_0.35']
    user = "LC"
    det_exposure_time(t, t)

    assert len(xlocs) == len(
        names
    ), f"Number of X coordinates ({len(xlocs)}) is different from number of samples ({len(names)})"

    # Detectors, motors:
    dets = [pil1M, pil300KW]
    waxs_range = np.linspace(0, 32.5, 6)
    # waxs_range = np.linspace(32.5, 32.5, 1)

    ypos = [-200, 200, 3]

    for wa in waxs_range:
        yield from bps.mv(waxs, wa)
        for sam, x, y, z in zip(names, xlocs, ylocs, zlocs):
            yield from bps.mv(piezo.x, x)
            yield from bps.mv(piezo.y, y)
            yield from bps.mv(piezo.z, z)

            name_fmt = "{sam}_16.1keV_sdd8.3m_wa{waxs}"
            sample_name = name_fmt.format(sam=sam, waxs="%2.1f" % wa)
            sample_id(user_name=user, sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.rel_scan(dets, piezo.y, *ypos)
            yield from bps.sleep(2)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def saxs_cai_2021_1(t=1):
    # names = ['glass_bkg', 'M11_LBBL_0.26', 'M11_LBBL_0.30', 'M11_LBBL_0.34', 'M11_LBBL_0.38', 'M11_LBBL_0.44', 'M17_LBBL_200k','M17_LBBL_500k',
    # 'M17_LBBL_1000k', 'HA_251_f_10', 'HA_251_f_25', 'HA_988_f_11', 'HA_909_AAPA_89_f_12', 'HA_239_AAPA_23_f_12', 'HA_239_AAPA_23_f_26']
    # xlocs = [39000, 44000, 31000, 16000,  3000, -10000, -23000, -37000, 42000, 26000, 14000,    0, -13000, -27000, -41000]
    # ylocs = [-7000, -7000, -7000, -7000, -6000,  -6000,  -6000,  -6000,  6000,  6000,  6000, 6000,   6000,   6000,   6000]
    # zlocs = [ 2700,  2700,  2700,  2700,  2700,   2700,   2700,   2700,  2700,  2700,  2700, 2700,   2700,   2700,   2700]

    # names = ['HA_180_AAPA_60_f_11', 'HA_188_AAPA_62_f_32', 'BMB_6per', 'BMB_17per', 'BMB_1.1', 'Si']
    # xlocs = [38000, 24000, 10000, -2000, -14000, -25000]
    # ylocs = [    0,     0,     0,     0,      0,      0]
    # zlocs = [ 2700,  2700,  2700,  2700,   2700,   2700]

    # names = ['HA_251', 'HA_988', 'HA_239_AAPA_23', 'HA_180_AAPA_60', 'HA_188_AAPA_62', 'HA_909_AAPA_89']
    # xlocs = [-39000, -23600, -14600,  9000, 26500, 38000]
    # ylocs = [ -9500,   2800,   2800,  2800,  2800,  2000]
    # zlocs = [  2700,  -6100,  -5900, -5900, -5900,  -200]

    names = [
        "Cap_blank",
        "HA_988_2",
        "HA_239_AAPA_23_2",
        "HA_180_AAPA_60_2",
        "HA_188_AAPA_62_2",
    ]
    xlocs = [-38900, -24000, -13800, 8100, 25900]
    ylocs = [-2500, -2500, -6000, -8300, -9500]
    zlocs = [500, -6100, -5900, -5900, -5900]

    user = "LC"
    det_exposure_time(t, t)

    assert len(xlocs) == len(
        names
    ), f"Number of X coordinates ({len(xlocs)}) is different from number of samples ({len(names)})"

    # Detectors, motors:
    dets = [pil1M, pil300KW]
    waxs_range = np.linspace(0, 32.5, 6)

    ypos = [-200, 200, 3]

    for wa in waxs_range:
        yield from bps.mv(waxs, wa)
        for sam, x, y, z in zip(names, xlocs, ylocs, zlocs):
            yield from bps.mv(piezo.x, x)
            yield from bps.mv(piezo.y, y)
            yield from bps.mv(piezo.z, z)

            name_fmt = "{sam}_16.1keV_sdd8.3m_wa{waxs}"
            sample_name = name_fmt.format(sam=sam, waxs="%2.1f" % wa)
            sample_id(user_name=user, sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.rel_scan(dets, piezo.y, *ypos)
            yield from bps.sleep(2)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def saxs_cai(t=1):
    # xlocs = [-40000,-29000,-18500, -5500,8500,16500,32500,42500, -37000,-24500,-14000, -6000,-2500,9000, 19000, 34000, 44000]
    # y_top = -5900
    # y_bot = 6500

    # ylocs = [y_top,y_top,y_top,y_top,y_top,y_top,y_top,y_top,   y_bot,y_bot,y_bot,y_bot,y_bot,y_bot,y_bot, y_bot, y_bot ]

    # names = ['HA_123_AAPA_133', 'HA_64_AAPA_191', 'AAPA_247', 'AAPA_280', 'LhBBL_tBuMA_x_0.6', 'LhBBL_tBuMA_x_1', 'LhBBL_tBuMA_x_1.44', 'LhBBL_tBuMA_x_2.3',
    # 'LBBL_378', 'LhBBL_306_BnMA_x_0.83', 'LhBBL_402_BnMA_x_0.84', 'LhBBL_508_BnMA_x_0.83', 'M17_LBBL_0.45','glass_bkg', 'M17_LBBL_0.49', 'M17_LBBL_0.54', 'HA_188_AAPA_62_f_27']

    xlocs = [1000, -8000, -21000, -31500, -41500]
    ylocs = [6500, 5900, 5900, 5900, 5000]

    names = [
        "LhBBL_207_BnMA_x_2.39",
        "LhBBL_200_BnMA_x_3.46",
        "hPDMS_207_BnMA_x_2.39",
        "hPDMS_200_BnMA_x_3.46",
        "hPDMS_198_BnMA_x_6.2",
    ]

    user = "LC"
    det_exposure_time(t, t)

    assert len(xlocs) == len(
        names
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"

    # Detectors, motors:
    dets = [pil1M, pil300KW]
    waxs_range = np.linspace(32.5, 0, 6)

    x_off = [-500, 0, 500]

    for wa in waxs_range:
        yield from bps.mv(waxs, wa)
        for sam, x, y in zip(names, xlocs, ylocs):
            yield from bps.mv(piezo.x, x)
            yield from bps.mv(piezo.y, y)

            for xx, x_of in enumerate(x_off):
                yield from bps.mv(piezo.x, x + x_of)
                xxa = xx + 1

                name_fmt = "{sam}_pos{pos}_wa{waxs}_16.1keV_sdd8.3m"
                sample_name = name_fmt.format(
                    sam=sam, pos="%1.1d" % xxa, waxs="%2.1f" % wa
                )
                sample_id(user_name=user, sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def gisaxs_cai(t=1):
    # samples = ['LhBBL_0_80','LhBBL_0.3_80','LhBBL_0.6_80','LhBBL_0.8_80','LhBBL_0.85_80', 'LhBBL_1.1_80','LhBBL_2_80','LhBBL_3_80','LhBBL_5.5_80','LhBBL_0.54_80', 'LhBBL_1.1new_80']
    samples = [
        "LhBBL_0_40",
        "LhBBL_0.3_40",
        "LhBBL_0.6_40",
        "LhBBL_0.8_40",
        "LhBBL_0.85_40",
        "LhBBL_1.1_40",
        "LhBBL_2_40",
        "LhBBL_3_40",
        "LhBBL_5.5_40",
        "LhBBL_0.54_40",
        "LhBBL_1.1new_40",
    ]
    x_list = [
        -49000,
        -39000,
        -30000,
        -18000,
        -7000,
        3000,
        12000,
        22000,
        32000,
        42000,
        52000,
    ]
    waxs_arc = [13, 6.5, 0]
    angle = [0.08, 0.125, 0.2]

    # Detectors, motors:
    dets = [pil1M, pil300KW]

    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"

    for x, sample in zip(x_list, samples):
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(pil1m_pos.x, -2.3)
        yield from alignement_gisaxs(0.08)
        yield from bps.mv(pil1m_pos.x, 0.8)

        det_exposure_time(t, t)
        name_fmt = "{sample}_ai{angle}deg_wa{wax}"
        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)
            for an in angle:
                yield from bps.mvr(piezo.th, an)
                sample_name = name_fmt.format(
                    sample=sample, angle="%3.3f" % an, wax="%2.2d" % wa
                )
                sample_id(user_name="ZG", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)
                yield from bps.mvr(piezo.th, -an)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def run_giwaxs_cai(t=1):
    # run with WAXS
    dets = [pil300KW, pil1M]
    waxs_arc = [13, 0, 3]

    # run with SAXS only
    # dets = [pil1M]
    # redo this but subtract another 800 um from X
    xlocs1 = [-51000, -40200, -24800, -14200, -3600, 6600, 16400, 24000, 35600, 50000]
    names1 = [
        "3_100_80mgmL",
        "3_104_80mgmL",
        "3_106_80mgmL",
        "3_107_80mgmL",
        "3_108_80mgmL",
        "3_100_40mgmL",
        "3_104_40mgmL",
        "3_106_40mgmL",
        "3_107_40mgmL",
        "3_108_40mgmL",
    ]

    xlocs2 = [-15000, -3500, 7500, 19500]
    xlocs3 = [-46000, -40000, -28000, -18000, -7000, 3000, 14000, 24000, 35000, 45000]
    xlocs4 = [-50000, -40000, -29000, -18000, -7000, 4000, 14000, 25500, 36000, 47000]
    xlocs5 = [-50000, -38000, -25500, -17000, -5000, 8000, 16000, 27000, 37000, 48000]
    xlocs6 = [-50000, -39000, -29000, -15000, -6000, 5000, 15000, 26000, 37000, 48000]
    xlocs7 = [-49000, -37000, -24000, -11000, 6500, 16500, 29000, 4100]
    xlocs8 = [29500, 41000]
    xlocs9 = [-44300, -34300, -25800, -15800, -800, 7000, 17000, 28200, 38200, 48200]

    names2 = [
        "BzMA_5.5_M11_80mgmL",
        "BzMA_M11_BzMA_40mgmL",
        "BzMA_BzMA_0.3_M11_BzMA_40mgmL",
        "BzMA_BzMA_0.6_M11_BzMA_40mgmL",
        "BzMA_BzMA_0.8_M11_BzMA_40mgmL",
        "BzMA_BzMA_1.1_M11_BzMA_40mgmL",
        "BzMA_BzMA_2.0_M11_BzMA_40mgmL",
        "BzMA_BzMA_3.0_M11_BzMA_40mgmL",
        "BzMA_BzMA_5.5_M11_BzMA_40mgmL",
        "BzMA_BzMA_3.2_M11_BzMA_40mgmL",
    ]
    names3 = [
        "BB5k_900k_PS_2x14k_80mgmL",
        "BB5k_900k_PS_2x14k_40mgmL",
        "BB5k_900k_PS_2x14k_20mgmL",
        "BB5k_900k_PS_2x14k_10mgmL",
        "NBPS160k_NBPDMS_4dot5M_NBPS_160k_80mgmL",
        "NBPS160k_NBPDMS_4dot5M_NBPS_160k_40mgmL",
        "NBPS160k_NBPDMS_4dot5M_NBPS_160k_20mgmL",
        "NBPS160k_NBPDMS_4dot5M_NBPS_160k_10mgmL",
        "NBPS300k_NBPDMS_8M_NBPS_300k_80mgmL",
        "NBPS300k_NBPDMS_8M_NBPS_300k_40mgmL",
    ]
    names4 = [
        "BB5k_50k_BzMA_2x45_80mgmL",
        "BB5k_50k_BzMA_2x115_80mgmL",
        "BB5k_50k_BzMA_2x382_80mgmL",
        "BB5k_50k_BzMA_2x580_80mgmL",
        "BB5k_42k_BzMA_2x168_80mgmL",
        "BB5k_50k_BzMA_2x45_40mgmL",
        "BB5k_50k_BzMA_2x115_40mgmL",
        "BB5k_50k_BzMA_2x382_40mgmL",
        "BB5k_50k_BzMA_2x580_40mgmL",
        "BB5k_42k_BzMA_2x168_20mgmL",
    ]
    names5 = [
        "BzMA_BzMA_0.8_M11_BzMA_80mgmL_2nd",
        "BzMA_3.0_M11_80mgmL_2nd",
        "BzMA_5.5_M11_80mgmL_2nd",
        "BzMA_BzMA_0.8_M11_BzMA_40mgmL_2nd",
    ]
    names6 = [
        "PHA10NH_37k_PS_2x3536_80mgmL",
        "PHA10NH_37k_PS_2x3536_40mgmL",
        "PHA10NH_37k_PS_2x3536_20mgmL",
        "PHA10NH_37k_PS_2x3536_10mgmL",
        "PHA10NH_43k_PS_2x6552_80mgmL",
        "PHA10NH_43k_PS_2x6552_40mgmL",
        "PHA10NH_43k_PS_2x6552_20mgmL",
        "PHA10NH_43k_PS_2x6552_10mgmL",
        "PHA25NH_38dot5k_PS_2x5928_80mgmL",
        "PHA25NH_38dot5k_PS_2x5928_40mgmL",
    ]
    names7 = [
        "PHA25NH_38dot5k_PS_2x5928_20mgmL",
        "PHA25NH_38dot5k_PS_2x5928_10mgmL",
        "PHA100NH_65k_80mgmL",
        "PHA100NH_65k_40mgmL",
        "PHA100NH_65k_20mgmL",
        "PHA100NH_65k_10mgmL",
        "Shifeng_1",
        "Shifeng_2",
    ]
    names8 = [
        "NBPS300k_NBPDMS_8M_NBPS_300k_20mgmL",
        "NBPS300k_NBPDMS_8M_NBPS_300k_10mgmL",
    ]

    # what we run now
    curr_tray = xlocs2
    curr_names = names5
    assert len(curr_tray) == len(
        curr_names
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    for x, name in zip(curr_tray, curr_names):
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(piezo.th, 0.5)
        yield from bps.mv(pil1m_pos.x, -2.3)
        # yield from bps.sleep(2)
        yield from alignement_gisaxs(0.1)
        yield from bps.mv(pil1m_pos.x, 0.7)
        # yield from bps.sleep(2)
        plt.close("all")
        angle_offset = [0.125, 0.2]
        a_off = piezo.th.position
        det_exposure_time(t, t)
        name_fmt = "{sample}_{angle}deg"
        for j, ang in enumerate(a_off + np.array(angle_offset)):
            yield from bps.mv(piezo.x, (x + j * 400))
            real_ang = angle_offset[j]
            yield from bps.mv(piezo.th, ang)
            sample_name = name_fmt.format(sample=name, angle=float("%.3f" % real_ang))
            sample_id(user_name="LC", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            # yield from bp.count(dets, num=1)
            yield from bp.scan(dets, waxs, *waxs_arc)

        sample_id(user_name="test", sample_name="test")
        det_exposure_time(0.3, 0.3)


def run_trans_cai(t=1):
    # run with WAXS
    dets = [pil300KW, pil1M]
    waxs_arc = [0, 6.5, 13]

    # run with SAXS only
    # dets = [pil1M]

    x_list = [
        34000,
        24200,
        13200,
        1200,
        -9800,
        -20800,
        -42800,
        -31800,
        -20800,
        -9800,
        1200,
        13200,
        24200,
        34000,
    ]
    y_list = [
        -10000,
        -10000,
        -10000,
        -10000,
        -10000,
        -10000,
        6000,
        6000,
        6000,
        6000,
        6000,
        6000,
        6000,
        6000,
    ]
    samples = [
        "BzMA_3.0_M11_Trans_2nd",
        "BB5k_50k_BzMA_2x45_Trans_2nd",
        "BB5k_50k_BzMA_2x115_Trans_2nd",
        "BB5k_42k_BzMA_2x168_Trans_2nd",
        "BB5k_50k_BzMA_2x382_Trans_2nd",
        "BB5k_50k_BzMA_2x580_Trans_2nd",
        "BzMA_BzMA_5.5_M11_BzMA_Trans_2nd",
        "BzMA_BzMA_3.0_M11_BzMA_Trans_2nd",
        "BzMA_BzMA_2_M11_BzMA_Trans_2nd",
        "BzMA_BzMA_1.1_M11_BzMA_Trans_2nd",
        "BzMA_BzMA_0.8_M11_BzMA_Trans_2nd",
        "BzMA_BzMA_0.6_M11_BzMA_Trans_2nd",
        "BzMA_BzMA_0.3_M11_BzMA_Trans_2nd",
        "BzMA_M11_BzMA_Trans_2nd",
    ]

    assert len(x_list) == len(
        y_list
    ), f"Number of X coordinates ({len(x_list)}) is different from number of Y coordinates ({len(y_list)})"
    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"

    # what we run now

    for wa in waxs_arc[::-1]:
        yield from bps.mv(waxs, wa)

        for x, y, s in zip(x_list, y_list, samples):
            yield from bps.mv(piezo.x, x)
            yield from bps.mv(piezo.y, y)
            yield from bps.sleep(2)

            det_exposure_time(t, t)
            name_fmt = "{sample}_wa{wax}"
            sample_name = name_fmt.format(sample=s, wax="%2.2d" % wa)
            sample_id(user_name="LC", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)
            sample_id(user_name="test", sample_name="test")
            det_exposure_time(0.3, 0.3)


def run_saxs_cai_2021_2(t=1):
    # run with WAXS
    dets = [pil300KW, pil900KW, pil1M]
    waxs_arc = [0, 2, 19.5, 21.5, 39, 41]

    # x_list  = [    46000,   45700,   40800,   33800,   26900,   21500,   14800,    8000,    2100,   -4500]
    # y_list =  [    -7500,    2000,    2000,    2000,    1900,    1900,    1900,    2300,    1600,    1600]
    # z_list =  [    -5500,   -5200,   -5000,   -4800,   -4600,   -4500,   -4300,   -4000,   -3800,   -3500]
    # samples = ['cap_bkg', 'old_1', 'old_2', 'old_3', 'old_4', 'new_1', 'new_2', 'new_3', 'new_4', 'new_5']

    x_list = [2100]
    y_list = [-9800]
    z_list = [-3500]
    samples = ["cap_bkg2"]

    assert len(x_list) == len(
        y_list
    ), f"Number of X coordinates ({len(x_list)}) is different from number of Y coordinates ({len(y_list)})"
    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"

    for wa in waxs_arc[::-1]:
        yield from bps.mv(waxs, wa)

        for x, y, z, s in zip(x_list, y_list, z_list, samples):
            yield from bps.mv(piezo.x, x)
            yield from bps.mv(piezo.y, y)
            yield from bps.mv(piezo.z, z)

            yield from bps.sleep(2)

            det_exposure_time(t, t)
            name_fmt = "{sample}_8.3m_14keV_wa{wax}"
            sample_name = name_fmt.format(sample=s, wax="%2.2d" % wa)
            sample_id(user_name="LC", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)
            sample_id(user_name="test", sample_name="test")
            det_exposure_time(0.3, 0.3)


def run_giwaxs_cai_temp(t=1):
    dets = [pil300KW, pil1M]
    xlocs1 = [2800, -8600]

    names1 = ["BzMA_3.0_M11_80mgmL", "BzMA_5.5_M11_80mgmL"]

    # what we run now
    curr_tray = xlocs1
    curr_names = names1
    assert len(curr_tray) == len(
        curr_names
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    waxs_arc = [0, 6.5, 13.0, 19.5]
    for x, name in zip(curr_tray, curr_names):
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(piezo.th, 0)
        yield from bps.mv(pil1m_pos.x, -2.3)
        # yield from bps.sleep(2)
        yield from alignement_gisaxs_shorter(0.1)
        yield from bps.mv(pil1m_pos.x, 0.7)
        # yield from bps.sleep(2)
        plt.close("all")
        angle_offset = [0.125, 0.2]
        a_off = piezo.th.position
        det_exposure_time(t, t)
        temper = ls.ch1_read.value
        for wa in waxs_arc:
            name_fmt = "{sample}_{temp}_{angle}deg_wa{wax}"
            # name_fmt = '{sample}_{angle}deg_wa{wax}'

            for j, ang in enumerate(a_off + np.array(angle_offset)):
                yield from bps.mv(piezo.x, (x + j * 200))
                real_ang = angle_offset[j]
                yield from bps.mv(piezo.th, ang)
                sample_name = name_fmt.format(
                    sample=name,
                    temp="%5.2f" % temper,
                    angle=float("%.3f" % real_ang),
                    wax="%2.2d" % wa,
                )
                # sample_name = name_fmt.format(sample=name, angle=float('%.3f'%real_ang), wax = '%2.2d'%wa)

                sample_id(user_name="LC", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

        sample_id(user_name="test", sample_name="test")
        det_exposure_time(0.3, 0.3)


def gisaxsCaiTempOLD(meas_t=1):
    temperatures = [190]
    waxs_arc = [8, 8, 1]
    dets = [pil1M, pil300KW, xbpm3.sumY]
    # glob_xoff = 1000
    xlocs1 = [-39000, -28000, -18000, -7000, 2000, 13000, 24000, 35000, 46000]
    xlocs2 = [-44000, -33000, -22000, -11000, 0, 11000, 22000, 33000, 44000]
    xlocs3 = [-44500, -33000, -22000, -11000, 0, 11000, 22000, 33000, 43800]
    xlocs4 = [-44000, -33000, -23000, -10000, 0, 11000, 22000, 33000, 44000]
    xlocs5 = [-44000, -33000, -24000, -11000, 0, 11000, 22000, 32000, 43000]
    xlocs6 = [-43000, -34000, -22000, -10000, 1000, 10500, 22000]

    xlocsT = [50500, 40500, 28500, 18500, 7500, -2500, -17500, -27500, -37500, -47500]

    names1 = [
        "M11_500kDa_100mgmL",
        "M11_500kDa_50mgmL",
        "M11_500kDa_25mgmL",
        "M11_500kDa_12mgmL",
        "M11_500kDa_6mgmL",
        "M11_500kDa_3mgmL",
        "M11_500kDa_1.6mgmL",
        "M11_1MDa_80mgmL",
        "M11_1MDa_40mgmL",
    ]
    names2 = [
        "M11_1MDa_20mgmL",
        "M11_1MDa_10mgmL",
        "M11_1MDa_5mgmL",
        "M11_1MDa_2.5mgmL",
        "M11_1MDa_1.25mgmL",
        "M11_1MDa_0.6mgmL",
        "M17_500kDa_100mgmL",
        "M17_500kDa_50mgmL",
        "M17_500kDa_25mgmL",
    ]
    names3 = [
        "M17_500kDa_12.5mgmL",
        "M17_500kDa_6.25mgmL",
        "M17_500kDa_3.1mgmL",
        "M17_500kDa_1.6mgmL",
        "M22_500kDa_40mgmL",
        "M22_500kDa_20mgmL",
        "M22_500kDa_10mgmL",
        "M22_1MDa_5mgmL",
        "M22_1MDa_2.5mgmL",
    ]
    names4 = [
        "M22_500kDa_1.25mgmL_new",
        "M22_500kDa_0.6mgmL",
        "M07_1MDa_80mgmL",
        "M07_1MDa_40mgmL",
        "M07_1MDa_20mgmL",
        "M07_1MDa_10mgmL",
        "M07_1MDa_5mgmL",
        "M07_1MDa_2.5mgmL",
        "M07_1MDa_1.25mgmL",
    ]
    names5 = [
        "M07_1MDa_0.6mgmL",
        "M11_500kDa_NoA_100mgmL",
        "M11_500kDa_NoA_50mgmL",
        "M11_500kDa_NoA_25mgmL",
        "M11_500kDa_NoA_12.5mgmL",
        "M11_500kDa_NoA_6.25mgmL",
        "M11_500kDa_NoA_3.1mgmL",
        "M11_500kDa_NoA_1.6mgmL",
        "M11_1MDa_NoA_80mgmL",
    ]
    names6 = [
        "M11_1MDa_NoA_40mgmL",
        "M11_1MDa_NoA_20mgmL",
        "M11_1MDa_NoA_10mgmL",
        "M11_1MDa_NoA_5mgmL",
        "M11_1MDa_NoA_2.5mgmL",
        "M11_1MDa_NoA_1.25mgmL",
        "M11_1MDa_NoA_0.6mgmL",
    ]

    namesT = [
        "M11_500kDa_1.6mgmL_8",
        "M11_1MDa_1.25mgmL_8",
        "M11_1MDa_0.6mgmL_8",
        "M17_500kDa_1.6mgmL_8",
        "M22_500kDa_1.25mgmL_8",
        "M22_500kDa_0.6mgmL_8",
        "M07_1MDa_1.25mgmL_8",
        "M07_1MDa_0.6mgmL_8",
        "M11_500kDa_NoA_1.6mgmL_8",
        "M11_1MDa_NoA_0.6mgmL_8",
    ]

    # what we run now
    curr_tray = xlocsT
    curr_names = namesT
    for i_t, t in enumerate(temperatures):
        yield from bps.mv(ls.ch1_sp, t)
        if i_t > 0:
            yield from bps.sleep(600)
        for x, name in zip(curr_tray, curr_names):
            yield from bps.mv(piezo.x, x)
            yield from bps.mv(piezo.th, 0.05 - 1)
            yield from alignCai()
            plt.close("all")
            angle_offset = [0.0, 0.025]
            a_off = piezo.th.position
            det_exposure_time(meas_t)
            name_fmt = "{sample}_{temperature}C_{angle}deg"
            temp = ls.ch1_read.value
            for j, ang in enumerate(a_off + np.array(angle_offset)):
                yield from bps.mv(piezo.x, (x + j * 200))
                real_ang = 0.1 + angle_offset[j]
                yield from bps.mv(piezo.th, ang)
                sample_name = name_fmt.format(
                    sample=name, temperature=temp, angle=real_ang
                )
                sample_id(user_name="LC", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.scan(dets, waxs, *waxs_arc)

    yield from bps.mv(ls.ch1_sp, 20)
    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5)


def saxs_cai_2021_2(t=1):

    # xlocs = [45800, 42800, 35500, 29000, 17500, 12900,  1400, -7300, -13400, -17700, -24200, -30500, -35500, -40500]
    # ylocs = [ 3000,  1500, -1800, -1200,  3600,  5500,  5700,  4900,   5800,   5800,   2600,  -8400,  -2400,   3000]
    # zlocs = [ 2000,  -700,  -700,  -700,  -700,  -700, -3500,  5000,   5000,   5000,   -700,   -700,   -700,   -700]
    # ystage = [-2.99,-2.99, -2.99, -2.99, -2.99, -2.99, -2.99, -2.99,  -2.99,  -2.99,  -2.99,   -6.0,   -2.99, -2.99]
    # names = ['HA_251', 'HA_229_AAPA_21', 'HA_189_AAPA_64', 'HA_1009', 'HA_927_AAPA_93', 'HA_725_AAPA_255', 'hPDMS_tBuMA_x_0.6', 'hPDMS_tBuMA_x_1',
    # 'hPDMS_tBuMA_x_1.44', 'hPDMS_tBuMA_x_2.3', 'PDMS_378', 'hPDMS_306_BnMA_x_0.83', 'hPDMS_402_BnMA_x_0.84', 'hPDMS_508_BnMA_x_0.83']

    names = [
        "LhBBL _207_BnMA_x_2.39",
        "LhBBL _200_BnMA_x_3.46",
        "hPDMS_207_BnMA_x_2.39",
        "hPDMS_200_BnMA_x_3.46",
        "hPDMS_198_BnMA_x_6.2",
    ]

    user = "LC"
    det_exposure_time(t, t)

    assert len(xlocs) == len(
        names
    ), f"Number of X coordinates ({len(xlocs)}) is different from number of samples ({len(names)})"
    assert len(xlocs) == len(
        ylocs
    ), f"Number of X coordinates ({len(xlocs)}) is different from number of samples ({len(ylocs)})"
    assert len(xlocs) == len(
        zlocs
    ), f"Number of X coordinates ({len(xlocs)}) is different from number of samples ({len(zlocs)})"
    assert len(xlocs) == len(
        ystage
    ), f"Number of X coordinates ({len(xlocs)}) is different from number of samples ({len(ystage)})"
    assert len(xlocs) == len(
        names
    ), f"Number of X coordinates ({len(xlocs)}) is different from number of samples ({len(names)})"

    # Detectors, motors:
    dets = [pil1M, pil300KW]
    waxs_range = np.linspace(32.5, 0, 6)
    # waxs_range = np.linspace(32.5, 32.5, 1)

    ypos = [-200, 200, 3]

    for wa in waxs_range:
        yield from bps.mv(waxs, wa)
        for sam, x, y, z, y_sta in zip(names, xlocs, ylocs, zlocs, ystage):
            yield from bps.mv(piezo.x, x)
            yield from bps.mv(piezo.y, y)
            yield from bps.mv(piezo.z, z)
            yield from bps.mv(stage.y, y_sta)

            name_fmt = "{sam}_16.1keV_sdd8.3m_wa{waxs}"
            sample_name = name_fmt.format(sam=sam, waxs="%2.1f" % wa)
            sample_id(user_name=user, sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.rel_scan(dets, piezo.y, *ypos)
            yield from bps.sleep(2)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def saxs_cai_2021_3(t=1):

    xlocs = [
        42000,
        25000,
        10000,
        -5000,
        -17000,
        -34000,
        44000,
        29500,
        13500,
        -3500,
        -21500,
    ]
    ylocs = [-9000, -9000, -9000, -9000, -9000, -9000, 2000, 2000, 2000, 2000, 2000]
    zlocs = [2700, 2700, 2700, 2700, 2700, 2700, 2700, 2700, 2700, 2700, 2700]
    ystage = [-2.0, -2.0, -2.0, -2.0, -2.0, -2.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    names = [
        "TR1",
        "TR2",
        "TR3",
        "TV1",
        "TV2",
        "TV3",
        "sample1",
        "sample2",
        "sample3",
        "sample4",
        "sample5",
    ]

    user = "LC"
    det_exposure_time(t, t)

    assert len(xlocs) == len(
        names
    ), f"Number of X coordinates ({len(xlocs)}) is different from number of samples ({len(names)})"
    assert len(xlocs) == len(
        ylocs
    ), f"Number of X coordinates ({len(xlocs)}) is different from number of samples ({len(ylocs)})"
    assert len(xlocs) == len(
        zlocs
    ), f"Number of X coordinates ({len(xlocs)}) is different from number of samples ({len(zlocs)})"
    assert len(xlocs) == len(
        ystage
    ), f"Number of X coordinates ({len(xlocs)}) is different from number of samples ({len(ystage)})"
    assert len(xlocs) == len(
        names
    ), f"Number of X coordinates ({len(xlocs)}) is different from number of samples ({len(names)})"

    # Detectors, motors:
    dets = [pil1M, pil900KW]
    waxs_range = [40, 20, 0]

    ypos = [-200, 200, 3]

    for wa in waxs_range:
        yield from bps.mv(waxs, wa)
        for sam, x, y, z, y_sta in zip(names, xlocs, ylocs, zlocs, ystage):
            yield from bps.mv(piezo.x, x)
            yield from bps.mv(piezo.y, y)
            yield from bps.mv(piezo.z, z)
            yield from bps.mv(stage.y, y_sta)

            name_fmt = "{sam}_14.0keV_sdd8.3m_wa{waxs}"
            sample_name = name_fmt.format(sam=sam, waxs="%2.1f" % wa)
            sample_id(user_name=user, sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.rel_scan(dets, piezo.y, *ypos)
            yield from bps.sleep(2)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def Cai_saxs_tensile_hard(t=0.2):
    dets = [pil1M]
    names = "sample142_3"

    t0 = time.time()
    for i in range(5000):
        det_exposure_time(t, t)
        name_fmt = "{sample}_14keV_sdd8p3_waxs30.0_{time}s_{i}"
        t1 = time.time()
        sample_name = name_fmt.format(
            sample=names, time="%1.1f" % (t1 - t0), i="%3.3d" % i
        )
        sample_id(user_name="SN", sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")
        yield from bp.count(dets, num=1)

        yield from bps.sleep(20)


def cai_tensile_continous_hard_2022_2(t=0.2):
    """
    WAXS and SAXS continous measurement on Linkam MFS stage

    setthreshold energy 16100 autog 11000

    Args:
        t (float): detector exposure time,
    """

    name = "MMA0.80-6"

    # Sampe starting hexapod positions in mm
    stage_x = -0.8
    stage_y = 0.6

    # Calculate position pairs for sample offset
    # np.linspace(start, stop, number of points)
    yss = np.linspace(stage_y, stage_y + 0.4, 20)
    xss = np.linspace(stage_x, stage_x + 0.4, 5)
    yss, xss = np.meshgrid(yss, xss)
    yss = yss.ravel()
    xss = xss.ravel()

    # Delay between taking detector images in seconds
    delay = 0

    waxs_arc = [15, 7]
    det_exposure_time(t, t)
    user_name = "BQ"

    t0 = time.time()

    yield from bps.mv(stage.y, stage_y, stage.x, stage_x, waxs, waxs_arc[0])

    for i in range(5000):

        yield from bps.mv(stage.y, yss[i % len(yss)], stage.x, xss[i % len(xss)])

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)

            # Do not read SAXS if WAXS is in the way
            dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]
            t1 = time.time()

            # Metadata
            step = str(i).zfill(3)
            td = str(np.round(t1 - t0, 1)).zfill(6)
            e = energy.position.energy / 1000
            sdd = pil1m_pos.z.position / 1000
            scan_id = db[-1].start["scan_id"] + 1

            # Sample name
            name_fmt = (
                "{sample}_step{step}_time{td}s_{energy}eV_wa{wax}_sdd{sdd}m_id{scan_id}"
            )
            sample_name = name_fmt.format(
                sample=name,
                step=step,
                td=td,
                energy="%.1f" % e,
                wax=wa,
                sdd="%.1f" % sdd,
                scan_id=scan_id,
            )
            sample_name = sample_name.translate(
                {ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ =,"}
            )
            sample_id(user_name=user_name, sample_name=sample_name)

            print(f"\n\t=== Step {i + 1} Sample: {sample_name} ===\n")
            yield from bp.count(dets)
        print(f"Sleep for {delay} seconds")
        yield from bps.sleep(delay)

    # End of the scan
    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)


def cai_transmission_hard__2022_2(t=1, xoff=0, yoff=0):
    """ """

    # x and y are positions on the sample, a and b are different rows
    names_a = [
        "MYO-sample_04-2",
        "MYO-sample_04-1",
        "MYO-sample_03",
        "MYO-sample_02",
        "MYO-sample_01",
        "MYO-background",
    ]
    x_a = [21500, 15000, 9000, 2000, -4000, -10000]
    y_a = [100, 100, 100, 100, 100, 100]

    # RA-proposal 2022_3: x and y are positions on the sample, a and b are different rows
    names_a = [
        "RED_05", "RED_06", "RED_07", "RED_08", "RED_09", "RED_10", "RED_11", "Empty_spot", "Capillary_quartz", "Capillary_glass",]
    
    x_a = [
           39800,    33440,    27220,    20800,    14500,     8200,     1540,        -4500,             -11100,            -17200,]
    y_a = [
           -8000,    -8000,    -8000,    -8000,    -8000,    -5100,    -8000,        -8000,              -8000,             -8000,]

    x_a = (np.array(x_a) + xoff).tolist()
    y_a = (np.array(y_a) + xoff).tolist()
    names_a = [n + '_xoff_%s__yoff_%s'%(xoff, yoff) for n in names_a]




    names_b = []
    x_b = []
    y_b = []

    # Combine sample lists
    names = names_a + names_b
    piezo_x = x_a + x_b
    piezo_y = y_a + y_b

    waxs_arc = [40, 20, 0]
    det_exposure_time(t, t)
    user_name = "BQ"

    assert len(piezo_x) == len(
        names
    ), f"Number of x coordinates ({len(piezo_x)}) is different from number of samples ({len(names)})"
    assert len(piezo_x) == len(
        piezo_y
    ), f"Number of x coordinates ({len(piezo_x)}) is different number of y coordinates ({len(piezo_y)})"
    assert len(piezo_y) == len(
        names
    ), f"Number of y coordinates ({len(piezo_y)}) is different from number of samples ({len(names)})"

    # Detectors, motors:
    waxs_range = [40, 20, 0]

    for i, wa in enumerate(waxs_range):
        yield from bps.mv(waxs, wa, piezo.x, piezo_x[0], piezo.y, piezo_y[0])
        # Do not read SAXS if WAXS is in the way
        dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]
        det_exposure_time(t, t)

        for name, xs, ys in zip(names, piezo_x, piezo_y):
            yield from bps.mv(piezo.x, xs, piezo.y, ys + i * 50)

            # Metadata
            e = energy.position.energy / 1000
            sdd = pil1m_pos.z.position / 1000
            scan_id = db[-1].start["scan_id"] + 1

            # Sample name
            name_fmt = "{sample}_{energy}keV_wa{wax}_sdd{sdd}m_id{scan_id}"
            sample_name = name_fmt.format(
                sample=name,
                energy="%.1f" % e,
                wax=wa,
                sdd="%.1f" % sdd,
                scan_id=scan_id,
            )
            sample_name = sample_name.translate(
                {ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ =,"}
            )
            sample_id(user_name=user_name, sample_name=sample_name)
            print(f"\n\n\n\t=== Sample: {sample_name} ===")
            # yield from bp.count(dets + [energy], md={'smi_md':{'energy': e, 'wax': wa, 'sdd': sdd}})
            yield from bp.count(dets)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def cai_giswaxs_temperature_scan_2022_2(t=0.5):
    """
    Grazing incidence measurement using Lakeshore controlled heating bar
    """

    names = ["BQ-sample-06", "BQ-sample-05"]
    piezo_x = [7500, -5800]
    piezo_z = 2200

    temperatures = [50, 55, 60, 80, 100, 105, 110, 115, 120, 210, 215, 220, 225, 350]

    incident_angles = [0.125, 0.2]
    waxs_range = [0, 20, 40]
    step_across_sample = 200
    user_name = "BQ"

    assert len(names) == len(
        piezo_x
    ), f"Number of X coordinates ({len(piezo_x)}) is different from number of samples ({len(names)})"

    yield from bps.mv(piezo.z, piezo_z)

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
        elif 160 <= temperature:
            yield from bps.sleep(600)

        # Read T and convert to deg C
        temp_degC = ls.input_A.get() - 273.15

        for (
            name,
            xs,
        ) in zip(names, piezo_x):

            # Move motors to locate the sample
            yield from bps.mv(piezo.x, xs)

            # Align the sample
            yield from bps.mv(pil1m_pos.x, -2.3)
            try:
                yield from alignement_gisaxs()
            except:
                yield from alignement_gisaxs(0.4)
            yield from bps.mv(pil1m_pos.x, 0.7)

            # Sample flat at ai0
            ai0 = piezo.th.position

            for i, wa in enumerate(waxs_range):
                yield from bps.mv(waxs, wa)
                dets = [pil900KW] if wa < 15 else [pil900KW, pil1M]
                det_exposure_time(t, t)

                yield from bps.mvr(piezo.x, (i + 1) * step_across_sample)

                for ai in incident_angles:
                    yield from bps.mv(piezo.th, ai0 + ai)

                    # Metadata
                    e = energy.position.energy / 1000
                    sdd = pil1m_pos.z.position / 1000
                    scan_id = db[-1].start["scan_id"] + 1
                    temp = str(np.round(float(temp_degC), 1)).zfill(5)

                    # Sample name
                    name_fmt = "{sample}_{temp}degC_{energy}keV_wa{wax}_sdd{sdd}m_id{scan_id}_ai{ai}"
                    sample_name = name_fmt.format(
                        sample=name,
                        temp=temp,
                        energy="%.1f" % e,
                        wax=wa,
                        sdd="%.1f" % sdd,
                        scan_id=scan_id,
                        ai=ai,
                    )
                    sample_name = sample_name.translate(
                        {ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ =,"}
                    )
                    sample_id(user_name=user_name, sample_name=sample_name)
                    print(f"\n\n\n\t=== Sample: {sample_name} ===")
                    yield from bp.count(dets)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)

    # Turn off the heating and set temperature to 23 deg C
    t_kelvin = 23 + 273.15
    yield from ls.output1.mv_temp(t_kelvin)
    yield from ls.output1.turn_off()


def run_swaxs_Cai_2022_3(t=1):
    """
    Take WAXS and SAXS at six sample positions for averaging

    Specify central positions on the samples with xlocs and ylocs,
    then offsets from central positions with x_off and y_off. Run
    WAXS arc as the slowest motor.
    Hexapod may need adjustment for the lower samples.
    """

    # Top sample row
    names_a   = ['sample-23', 'sample-24','sample-25', 'sample-26', 'sample-27',]
    piezo_x_a = [     42000,      27000,      11000,       -2000,       -16000,]
    piezo_y_a = [      -8500,       -8500,      -8500,      -8500,        -8000,]
    hexa_y_a  = [0 for n in names_a]  #in mm

    # Bottom sample row
    names_b   = ['Background', ]
    piezo_x_b = [       44000,]
    piezo_y_b = [        4000,]
    hexa_y_b  = [0 for n in names_b]  #in mm

    # Combine rows
    names   = names_a + names_b
    piezo_x = piezo_x_a + piezo_x_b
    piezo_y = piezo_y_a + piezo_y_b
    hexa_y  = hexa_y_a + hexa_y_b

    # Offsets for taking a few points per sample
    x_off = [0, -1000]
    y_off = [0, 500, 1000]
    y_off_waxs = 100

    waxs_arc = [40, 20, 0]
    user = "LC"
    

    # Check and correct sample names just in case
    names = [n.translate({ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ "}) for n in names]

    # Check if the length of xlocs, ylocs and names are the same
    assert len(piezo_x) == len(names), f"Number of X coordinates ({len(piezo_x)}) is different from number of samples ({len(names)})"
    assert len(piezo_x) == len(piezo_y), f"Number of X coordinates ({len(piezo_x)}) is different from number of samples ({len(piezo_y)})"
    assert len(piezo_x) == len(hexa_y), f"Number of X coordinates ({len(piezo_x)}) is different from hexapod y positions ({len(hexa_y)})"

    for i, wa in enumerate(waxs_arc):
        yield from bps.mv(waxs, wa)
        # Detectors, disable SAXS when WAXS in the way
        dets = [pil900KW] if waxs.arc.position < 15 else [pil900KW, pil1M]
        det_exposure_time(t, t)

        for name, x, y, hy in zip(names, piezo_x, piezo_y, hexa_y):
            yield from bps.mv(stage.y, hy)

            for yy, y_of in enumerate(y_off):
                yield from bps.mv(piezo.y, y + y_of + i * y_off_waxs)

                for xx, x_of in enumerate(x_off):
                    yield from bps.mv(piezo.x, x + x_of)

                    loc = xx + 2 * yy + 1

                    # Metadata
                    e = energy.position.energy / 1000
                    wa = waxs.arc.position + 0.001
                    wa = str(np.round(float(wa), 1)).zfill(4)
                    sdd = pil1m_pos.z.position / 1000

                    # Sample name
                    name_fmt = ( "{sample}_{energy}keV_wa{wax}_sdd{sdd}m_loc{loc}")
                    sample_name = name_fmt.format(
                        sample=name,
                        energy="%.2f" % e,
                        wax=wa,
                        sdd="%.1f" % sdd,
                        loc=int(loc),
                    )
                    sample_id(user_name=user, sample_name=sample_name)
                    print(f"\n\n\n\t=== Sample: {sample_name} ===")
                    yield from bp.count(dets)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def run_swaxs_capillaries_Cai_2022_3(t=1):
    """
    Take WAXS and SAXS at six sample positions for averaging

    Specify central positions on the samples with xlocs and ylocs,
    then offsets from central positions with x_off and y_off. Run
    WAXS arc as the slowest motor.
    Hexapod may need adjustment for the lower samples.
    """

    #names   = [ 'red-07', 'red-08', 'red-09', 'red-10', 'red-11', 'pink-04' ]
    #piezo_x = [    39100,    32800,    26000,    20400,    13400,      6400, ]
    #piezo_y = [    -1900,    -1600,    -1600,    -1600,    -1600,     -4000, ]
    #hexa_y  = [0 for n in names]  #in mm
    # hexa_y  = [0, 0, -5, -5, 0, ....]

    #Liquid Samples- 2nd set
    #names   = [ 'red-07', 'red-08', 'red-09', 'red-10', 'red-11', 'pink-04' ]
    #piezo_x = [    39100,    32800,    26000,    20400,    13400,      7600, ]
    #piezo_y = [    -1900,    -1600,    -1600,    -1600,    -1600,     -9600, ]
    #hexa_y  = [0, 0, 0, 0, 0, -10.31]

    #Redo of Pink-04 only
    names   = ['pink-04_Run2' ]
    piezo_x = [ 7600, ]
    piezo_y = [ -10400, ]
    hexa_y  = [ -10.31]

    # Offsets for taking a few points per sample
    x_off = [0, 200]
    y_off = [0, 500, 1000]
    y_off_waxs = 100

    waxs_arc = [40, 20, 0]
    user = "LC"
    

    # Check and correct sample names just in case
    names = [n.translate({ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ "}) for n in names]

    # Check if the length of xlocs, ylocs and names are the same
    assert len(piezo_x) == len(names), f"Number of X coordinates ({len(piezo_x)}) is different from number of samples ({len(names)})"
    assert len(piezo_x) == len(piezo_y), f"Number of X coordinates ({len(piezo_x)}) is different from number of samples ({len(piezo_y)})"
    assert len(piezo_x) == len(hexa_y), f"Number of X coordinates ({len(piezo_x)}) is different from hexapod y positions ({len(hexa_y)})"

    for i, wa in enumerate(waxs_arc):
        yield from bps.mv(waxs, wa)
        # Detectors, disable SAXS when WAXS in the way
        dets = [pil900KW] if waxs.arc.position < 15 else [pil900KW, pil1M]
        det_exposure_time(t, t)

        for name, x, y, hy in zip(names, piezo_x, piezo_y, hexa_y):
            yield from bps.mv(stage.y, hy)

            for yy, y_of in enumerate(y_off):
                yield from bps.mv(piezo.y, y + y_of + i * y_off_waxs)

                for xx, x_of in enumerate(x_off):
                    yield from bps.mv(piezo.x, x + x_of)

                    loc = xx + 2 * yy + 1

                    # Metadata
                    e = energy.position.energy / 1000
                    wa = waxs.arc.position + 0.001
                    wa = str(np.round(float(wa), 1)).zfill(4)
                    sdd = pil1m_pos.z.position / 1000

                    # Sample name
                    name_fmt = ( "{sample}_{energy}keV_wa{wax}_sdd{sdd}m_loc{loc}")
                    sample_name = name_fmt.format(
                        sample=name,
                        energy="%.2f" % e,
                        wax=wa,
                        sdd="%.1f" % sdd,
                        loc=int(loc),
                    )
                    sample_id(user_name=user, sample_name=sample_name)
                    print(f"\n\n\n\t=== Sample: {sample_name} ===")
                    yield from bp.count(dets)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)

def cai_printing(xpos, ypos, sample_name='test'):
    """
    xpos=[start, stop, npoints]
    ypos=[step,npoints]%
    """
    
    sname = f'{sample_name}{get_scan_md()}'
    sname = sname.translate({ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ =,"})
    sample_id(user_name='LC', sample_name=sname)

    dets = [pil900KW, OAV_writing]
    if waxs.arc.position > 15:
        dets.append(pil1M)

    for yy,y in enumerate(range(ypos[1])):
        if np.mod(yy,2) == 0:
            xs=xpos[0];xe=xpos[1]
        else:
            xs=xpos[1];xe=xpos[0]
        yield from bp.scan(dets, stage.x, xs, xe, xpos[2])
        yield from bps.mvr(stage.y,ypos[0])

def cai_printing_vertical(ypos,reps=1,sleep_time=0,x_step=-.1):
    """
    ypos=[start, stop, npoints]
    """
    for r in range(reps):
        yield from bp.scan([pil1M,pil900KW,OAV_writing],stage.y,ypos[0],ypos[1],ypos[2])
        yield from bps.mvr(stage.x,x_step)
    yield from bps.mvr(stage.x,-(r+1)*x_step)



def cai_printing_horizontal(speed=.25,time_step=.5,total_time=20):
    """
    ypos=[start, stop, npoints]
    """
    
    pil1M.cam.acquire_period.set(pil1M.cam.acquire_time.get())
    OAV.cam.acquire_period.set(OAV.cam.acquire_time.get())
    pil900KW.cam.acquire_period.set(pil900KW.cam.acquire_time.get())
    pil1M.cam.num_images.set(1);OAV.cam.num_images.set(1);pil900KW.cam.num_images.set(1)
    
    step_size=speed*time_step
    nsteps = int((total_time/time_step)+1)
    cur_x=stage.x.user_readback.get()
    RE.md['x_start']=cur_x
    yield from bp.scan([pil1M,pil900KW,OAV_writing],stage.x,cur_x,cur_x-nsteps*step_size,nsteps)
    
def cai_printing_time_evolution_horizontal(total_points=15,sleep_time=12,xstep=.05):
    # take 2 images / point and use acquire period to make up sleep time
    st=np.max([sleep_time-pil1M.cam.acquire_time.get(),0])
    pil1M.cam.acquire_period.set(st);OAV.cam.acquire_period.set(st);pil900KW.cam.acquire_period.set(st)
    pil1M.cam.num_images.set(2);OAV.cam.num_images.set(2);pil900KW.cam.num_images.set(2)
    cur_x=stage.x.user_readback.get()
    yield from bp.scan([pil1M,pil900KW,OAV_writing],stage.x,cur_x,cur_x-total_points*xstep,total_points)
    # set acquire time back to exposure time:
    pil1M.cam.acquire_period.set(pil1M.cam.acquire_time.get())
    OAV.cam.acquire_period.set(OAV.cam.acquire_time.get())
    pil900KW.cam.acquire_period.set(pil900KW.cam.acquire_time.get())
    pil1M.cam.num_images.set(1);OAV.cam.num_images.set(1);pil900KW.cam.num_images.set(1)


def cai_tensile_continous_hard_2022_3(t=0.2):
    """
    WAXS and SAXS continous measurement on Linkam MFS stage

    setthreshold energy 14000 autog 11500

    Args:
        t (float): detector exposure time,
    """

    name = "BzMA-0.84-3"

    # Sampe starting hexapod positions in mm
    stage_x = -0.3
    stage_y = 0.7

    # Calculate position pairs for sample offset
    # np.linspace(start, stop, number of points)
    yss = np.linspace(stage_y, stage_y + 0.1, 9)
    xss = np.linspace(stage_x, stage_x + 0.4, 2)
    yss, xss = np.meshgrid(yss, xss)
    yss = yss.ravel()
    xss = xss.ravel()

    # Delay between taking detector images in seconds
    delay = 0

    waxs_arc = [15, 7]
    det_exposure_time(t, t)
    user_name = "BQ"

    t0 = time.time()

    yield from bps.mv(stage.y, stage_y, stage.x, stage_x, waxs, waxs_arc[0])

    for i in range(5000):

        yield from bps.mv(stage.y, yss[i % len(yss)], stage.x, xss[i % len(xss)])

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)

            # Do not read SAXS if WAXS is in the way
            dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]
            t1 = time.time()

            # Metadata
            step = str(i).zfill(3)
            td = str(np.round(t1 - t0, 1)).zfill(6)
            e = energy.position.energy / 1000
            sdd = pil1m_pos.z.position / 1000

            # Sample name
            name_fmt = (
                "{sample}_step{step}_time{td}s_{energy}eV_wa{wax}_sdd{sdd}m"
            )
            sample_name = name_fmt.format(
                sample=name,
                step=step,
                td=td,
                energy="%.1f" % e,
                wax=wa,
                sdd="%.1f" % sdd,
            )
            sample_name = sample_name.translate(
                {ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ =,"}
            )
            sample_id(user_name=user_name, sample_name=sample_name)

            print(f"\n\t=== Step {i + 1} Sample: {sample_name} ===\n")
            yield from bp.count(dets)
        print(f"Sleep for {delay} seconds")
        yield from bps.sleep(delay)

    # End of the scan
    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)


def give_sample_name(sample='test', user_name='DR'):
    """
    Wrapper for sample naming and includes metadata
    """

    RE.md['sample'] = sample

    e = energy.position.energy / 1000
    sdd = pil1m_pos.z.position / 1000
    wa = waxs.arc.position + 0.001
    wa = str(np.round(float(wa), 1)).zfill(4)

    # Sample name
    name_fmt = ("{sample}_{energy}keV_wa{wax}_sdd{sdd}m")
    sample_name = name_fmt.format(
        sample=sample,
        energy="%.2f" % e,
        wax=wa,
        sdd="%.1f" % sdd,
    )
    sample_id(user_name=user_name, sample_name=sample_name)
    print(f"\n\n\n\t=== Sample: {sample_name} ===")


def run_swaxs_capillary_overnight_Cai_2022_3(t=1):
    """
    Take WAXS and SAXS at 2 sample positions,
    heating done by Linkam

    """

    name   = 'AAPA-80_run2'
    hexa_y  =  -0.4
    hexa_x  =  -7.7
    hexa_z  =  -5.5

    # Offsets for taking a few points per sample
    y_off = [0, 0.5]
    y_off_step = 0.025

    waxs_arc = [20, 0]
    user = "LC"

    temperatures =   [50, 100, 150, 200, 250]
    temp_ramp_time = [x * 60 for x in [0, 5, 5, 5, 5]]
    times = [x * 60 for x in [5, 10, 30, 60]]

    t0_total = time.time()
    
    yield from bps.mv(
        stage.y, hexa_y,
        stage.x, hexa_x,
        stage.z, hexa_z,
        waxs, waxs_arc[0],
    )

    counter = 0

    for temp, ramp in zip(temperatures, temp_ramp_time):
        print(f'Waiting for ramp {ramp} s')
        print(temp)
        yield from bps.sleep(ramp) 

        t_at_temp = time.time()

        for ti in times:
            t_difference = time.time() - t_at_temp + 30

            while abs(t_difference) < ti:
                yield from bps.sleep(10)
                t_difference = time.time() - t_at_temp + 30
                print(f'Wating for {ti - t_difference:.0f} s')
            
            for i, wa in enumerate(waxs_arc):
                yield from bps.mv(waxs, wa)
                # Detectors, disable SAXS when WAXS in the way
                dets = [pil900KW] if waxs.arc.position < 15 else [pil900KW, pil1M]
                det_exposure_time(t, t)

                for yy, y_of in enumerate(y_off):
                    yield from bps.mv(stage.y, hexa_y + y_of + counter * y_off_step)

                    # Metadata
                    e = energy.position.energy / 1000
                    wa = waxs.arc.position + 0.001
                    wa = str(np.round(float(wa), 1)).zfill(4)
                    sdd = pil1m_pos.z.position / 1000
                    temp = str(temp).zfill(3)
                    tm = str(np.round(float(ti), 0)).zfill(5)

                    t1 = time.time()
                    td = str(np.round(t1 - t0_total, 1)).zfill(6)

                    # Sample name
                    name_fmt = ( "{sample}_{temp}C_{tm}s_{energy}keV_wa{wax}_sdd{sdd}m_loc{loc}_time{td}s")
                    sample_name = name_fmt.format(
                        sample=name,
                        temp=temp,
                        tm=tm,
                        energy="%.2f" % e,
                        wax=wa,
                        sdd="%.1f" % sdd,
                        td=td,
                        loc=int(yy),
                    )
                    sample_id(user_name=user, sample_name=sample_name)
                    print(f"\n\n\n\t=== Sample: {sample_name} ===")
                    yield from bp.count(dets)
                    counter += 1
        if temp == 25:
            break
        
def cai_tensile_continous_hard_2023_2(t=0.2):
    """
    WAXS and SAXS continous measurement on Linkam MFS stage

    setthreshold energy 14000 autog 11500

    Args:
        t (float): detector exposure time,
    """

    name = "LfBBL-MMA3.62-4th"

    # Sampe starting hexapod positions in mm
    stage_x = 1.2
    stage_y = 0.7

    # Calculate position pairs for sample offset
    # np.linspace(start, stop, number of points)
    yss = np.linspace(stage_y, stage_y + 0.1, 9)
    xss = np.linspace(stage_x, stage_x + 0.4, 2)
    yss, xss = np.meshgrid(yss, xss)
    yss = yss.ravel()
    xss = xss.ravel()

    # Delay between taking detector images in seconds
    delay = 0

    waxs_arc = [15, 7]
    det_exposure_time(t, t)
    user_name = "BQ"

    t0 = time.time()

    yield from bps.mv(stage.y, stage_y, stage.x, stage_x, waxs, waxs_arc[0])

    for i in range(5000):

        yield from bps.mv(stage.y, yss[i % len(yss)], stage.x, xss[i % len(xss)])

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)

            # Do not read SAXS if WAXS is in the way
            dets = [pil900KW] if waxs.arc.position < 10 else [pil1M, pil900KW]

            if waxs.arc.position > 10:
                dets.append(pdcurrent)
                dets.append(pdcurrent1)
                dets.append(pdcurrent2)


            t1 = time.time()

            # Metadata
            step = str(i).zfill(3)
            td = str(np.round(t1 - t0, 1)).zfill(6)
            
            sample_name = f'{name}_step{step}_time{td}s{get_scan_md()}'

            # Sample name
            #name_fmt = (
            #    "{sample}_step{step}_time{td}s_{energy}eV_wa{wax}_sdd{sdd}m"
            #)
            #sample_name = name_fmt.format(
            #    sample=name,
            #    step=step,
            #    td=td,
            #    energy="%.1f" % e,
            #    wax=wa,
            #    sdd="%.1f" % sdd,
            #)
            sample_name = sample_name.translate(
                {ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ =,"}
            )
            sample_id(user_name=user_name, sample_name=sample_name)

            print(f"\n\t=== Step {i + 1} Sample: {sample_name} ===\n")
            yield from bp.count(dets)
        print(f"Sleep for {delay} seconds")
        yield from bps.sleep(delay)

    # End of the scan
    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)


def run_swaxs_Cai_2023_2(t=1):
    """
    Take WAXS and SAXS at six sample positions for averaging

    Specify central positions on the samples with xlocs and ylocs,
    then offsets from central positions with x_off and y_off. Run
    WAXS arc as the slowest motor.
    Hexapod may need adjustment for the lower samples.
    """

    # Top sample row
    names_a   = [ 'Myoeum-LQ-Empty', 'Myoeum-LQ-4', 'Myoeum-LQ-3_2', 'Myoeum-LQ-3', 'Myoeum-LQ-2_2', 'Myoeum-LQ-2', 'Myoeum-LQ-1', 'BQ-LQ-3','BQ-LQ-2','BQ-LQ-1','BQ-LQ-10-1mg','BQ-LQ-4-1mg','BQ-LQ-empty-H2O',]
    piezo_x_a = [   -31400,           -25200,        -18600,           -12600,        -6400,           0,            6600,           13000,    19400,    26000,    32200,         38600,        45000,]
    piezo_y_a = [ -1300 for n in names_a ]
    hexa_x_a  = [ 0 for n in names_a ]  #in mm
    hexa_y_a  = [ 0 for n in names_a ]  #in mm

    # Bottom sample row
    names_b   = [ ]
    piezo_x_b = [ ]
    piezo_y_b = [ ]
    hexa_x_b  = [ ]#0 for n in names_b]  #in mm
    hexa_y_b  = [ ]#0 for n in names_b]  #in mm

    # Combine rows
    names   = names_a + names_b
    piezo_x = piezo_x_a + piezo_x_b
    piezo_y = piezo_y_a + piezo_y_b
    hexa_x  = hexa_x_a + hexa_x_b
    hexa_y  = hexa_y_a + hexa_y_b

    # Offsets for taking a few points per sample
    #x_off = [0, -1000]
    #y_off = [0, 350, 700]

    x_off = [0]
    y_off = [-250, 0, 250]
    y_off_waxs = 0

    waxs_arc = [40, 20, 0]
    user = "LC"
    
    # Check and correct sample names just in case
    names = [n.translate({ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ "}) for n in names]


    # Check if the length of xlocs, ylocs and names are the same
    msg = "Wrong number of coordinates, check names, piezos, and hexas"
    assert len(piezo_x) == len(names), msg
    assert len(piezo_x) == len(piezo_y), msg
    assert len(piezo_x) == len(hexa_y), msg
    assert len(hexa_x) == len(hexa_y), msg

    for i, wa in enumerate(waxs_arc):
        yield from bps.mv(waxs, wa)
        # Detectors, disable SAXS when WAXS in the way
        dets = [pil900KW] if waxs.arc.position < 15 else [pil900KW, pil1M]
        det_exposure_time(t, t)
        

        for name, x, y, hx, hy in zip(names, piezo_x, piezo_y, hexa_x, hexa_y):


            yield from bps.mv(stage.x, hx,
                              stage.y, hy,
                              )
            loc = 0
            for yy, y_of in enumerate(y_off):
                yield from bps.mv(piezo.y, y + y_of + i * y_off_waxs)

                for xx, x_of in enumerate(x_off):
                    yield from bps.mv(piezo.x, x + x_of)

                    #loc = xx + 2 * yy + 1

                    sample_name = f'{name}{get_scan_md()}_loc{loc}'
                    sample_id(user_name=user, sample_name=sample_name)
                    print(f"\n\n\n\t=== Sample: {sample_name} ===")
                    yield from bp.count(dets)
                    loc += 1

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def cai_giswaxs_temperature_scan_2023_2(t=0.5):
    """
    Grazing incidence measurement using Lakeshore controlled heating bar
    """

    proposal_id('2023_2', '310896_Cai_03', analysis=True)

    names   = ['sample-NIPAm10-1','sample-NIPAm10-2','sample-NIPAm6-1','sample-NIPAm6-2','sample-NIPAm0-1','sample-NIPAm0-2', ]
    piezo_x = [  40000,             28000,             12000,            0,                -12000,            -24000, ]
    piezo_y = [ -200 for n in names ]
    piezo_z = [ -800 for n in names ]

    temperatures = [26, 30, 35, 36, 37, 38, 39, 40, 43, 46, 50, 60, 70]

    incident_angles = [0.125, 0.2]
    waxs_range = [0, 20, 40]
    step_across_sample = 200
    user_name = "BQ"
    det_exposure_time(t, t)

    msg = "Wrong number of coordinates, check names, piezos, and hexas"
    assert len(piezo_x) == len(names), msg
    assert len(piezo_x) == len(piezo_y), msg
    assert len(piezo_y) == len(piezo_z), msg


    for temperature in temperatures:
        t_kelvin = temperature + 273.15
        yield from ls.output1.mv_temp(t_kelvin)

        # Activate heating range in Lakeshore
        #if temperature < 80:
        #   yield from bps.mv(ls.output1.status, 1)
        #else:
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
        print("Time needed to equilibrate: {:.1f} min".format((time.time() - start) / 60))

        # Wait extra time depending on temperature

        if (30 < temperature) and (temperature < 181):
            extra_time = 1200
        elif 160 <= temperature:
            extra_time = 1200
        else:
            extra_time = 0
        
        print(f'Equilibrating temperature for extra {extra_time} s\n')
        t_start = time.time()
        while (time.time() - t_start) < extra_time:
            print(f'Pumping time: {(time.time() - t_start):.1f} s')
            yield from bps.sleep(30)

        # Read T and convert to deg C
        temp_degC = ls.input_A.get() - 273.15

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

            for i, wa in enumerate(waxs_range):
                yield from bps.mv(waxs, wa)
                dets = [pil900KW] if waxs.arc.position < 15 else [pil900KW, pil1M]
                
                yield from bps.mvr(piezo.x, (i + 1) * step_across_sample)

                for ai in incident_angles:
                    yield from bps.mv(piezo.th, ai0 + ai)

                    temp = str(np.round(float(temp_degC), 1)).zfill(5)
                    sample_name = f'{name}_{temp}degC{get_scan_md()}_ai{ai}'
                    sample_name = sample_name.translate(
                        {ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ =,"}
                    )
                    sample_id(user_name=user_name, sample_name=sample_name)
                    print(f"\n\n\n\t=== Sample: {sample_name} ===")
                    yield from bp.count(dets)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)

    # Turn off the heating and set temperature to 23 deg C
    t_kelvin = 23 + 273.15
    yield from ls.output1.mv_temp(t_kelvin)
    yield from ls.output1.turn_off()


def cai_temperature_scan_2023_2(t=0.5):
    """
    Transmission using Lakeshore controlled heating bar
    """

    proposal_id('2023_2', '310896_Cai_05', analysis=True)

    names   = ['NIPAm0-glass', 'NIPAm0-SI-1', 'NIPAm0-SI-2', 'NIPAm6-SI-1', 'NIPAm6-SI-2', 'NIPAm6-glass', 'NIPAm10-SI', 'NIPAm10-glass']  
    piezo_x = [         51500,         40000,         28000,         11000,         -1000,         -13000,       -27000,          -38000]
    piezo_y = [     -9785.137,     -9075.141,     -8818.138,     -8423.131,     -8223.627,      -8350.874,    -7615.144,       -7806.003]
    piezo_th = [     -1.68278,     -1.587648,     -1.269735,     -2.120736,     -1.726573,      -1.626816,    -0.750505,       -1.759373]

    temperatures = [27, 30, 35, 37, 39, 41, 43, 45, 50, 55, 60, 65, 70]
    temperatures = [30, 35, 37, 39, 41, 43, 45, 50, 55, 60, 65, 70]
    temperatures = [60, 65, 70]

    waxs_range = [0]
    user_name = "BQ"
    det_exposure_time(t, t)

    msg = "Wrong number of coordinates, check names, piezos, and hexas"
    assert len(piezo_x) == len(names), msg
    assert len(piezo_x) == len(piezo_y), msg

    for temperature in temperatures:
        t_kelvin = temperature + 273.15
        yield from ls.output1.mv_temp(t_kelvin)
        yield from bps.mv(ls.output1.status, 2)

        # Equalise temperature
        print(f"Equalising temperature to {temperature} deg C")
        start = time.time()
        temp = ls.input_A.get()
        if temperature!=30:
            while abs(temp - t_kelvin) > 1:
                print("Difference: {:.1f} K".format(abs(temp - t_kelvin)))
                yield from bps.sleep(10)
                temp = ls.input_A.get()

                # Escape the loop if too much time passes
                if time.time() - start > 1800:
                    temp = t_kelvin
        print("Time needed to equilibrate: {:.1f} min".format((time.time() - start) / 60))


        # Wait extra time depending on temperature
        if temperature!=30:
            yield from bps.sleep(600)

        # Read T and convert to deg C
        temp_degC = ls.input_A.get() - 273.15

        for name, x, y, th in zip(names, piezo_x, piezo_y, piezo_th):

            yield from bps.mv(piezo.x, x,
                              piezo.y, y,
                              piezo.th, th+0.2)

            for i, wa in enumerate(waxs_range):
                yield from bps.mv(waxs, wa)
                dets = [pil900KW] if waxs.arc.position < 15 else [pil900KW, pil1M]
                
                temp = str(np.round(float(temp_degC), 1)).zfill(5)
                sample_name = f'{name}_ai0.2_{temp}degC{get_scan_md()}'
                sample_name = sample_name.translate(
                    {ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ =,"}
                )
                sample_id(user_name=user_name, sample_name=sample_name)
                print(f"\n\n\n\t=== Sample: {sample_name} ===")
                yield from bps.sleep(10)
                yield from bp.count(dets)


    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)

    # Turn off the heating and set temperature to 23 deg C
    t_kelvin = 23 + 273.15
    yield from ls.output1.mv_temp(t_kelvin)
    yield from ls.output1.turn_off()



def cai_temperature_trans_scan_2023_2(t=0.5):
    """
    Transmission using Lakeshore controlled heating bar
    """

    proposal_id('2023_2', '310896_Cai_06', analysis=True)

    names   = ['NIPAm10-0.2mg/ml', 'NIPAm6-0.2mg/ml', 'NIPAm0-0.2mg/ml']  
    piezo_x = [         -4800,          8000,         20600]
    piezo_y = [         -8106,         -8106,         -8106]

    temperatures = [27, 30, 35, 37, 39, 41, 43, 45, 50, 55, 60, 65, 70]

    waxs_range = [0, 20]
    user_name = "BQ"
    det_exposure_time(t, t)

    msg = "Wrong number of coordinates, check names, piezos, and hexas"
    assert len(piezo_x) == len(names), msg
    assert len(piezo_x) == len(piezo_y), msg

    for temperature in temperatures:
        t_kelvin = temperature + 273.15
        yield from ls.output1.mv_temp(t_kelvin)
        yield from bps.mv(ls.output1.status, 3)

        # Equalise temperature
        print(f"Equalising temperature to {temperature} deg C")
        start = time.time()
        temp = ls.input_A.get()
        if temperature!=27:
            while abs(temp - t_kelvin) > 1:
                print("Difference: {:.1f} K".format(abs(temp - t_kelvin)))
                yield from bps.sleep(10)
                temp = ls.input_A.get()

                # Escape the loop if too much time passes
                if time.time() - start > 600:
                    temp = t_kelvin
        print("Time needed to equilibrate: {:.1f} min".format((time.time() - start) / 60))


        # Wait extra time depending on temperature
        if temperature!=27:
            yield from bps.sleep(600)

        # Read T and convert to deg C
        temp_degC = ls.input_A.get() - 273.15

        for name, x, y in zip(names, piezo_x, piezo_y):

            yield from bps.mv(piezo.x, x,
                              piezo.y, y)


            if waxs.arc.position>15:
                waxs_range = [20, 0]
            else:
                waxs_range = [0, 20]

            for i, wa in enumerate(waxs_range):
                yield from bps.mv(waxs, wa)
                dets = [pil900KW] if waxs.arc.position < 15 else [pil900KW, pil1M]
                
                temp = str(np.round(float(temp_degC), 1)).zfill(5)
                sample_name = f'{name}_{temp}degC{get_scan_md()}'
                sample_name = sample_name.translate(
                    {ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ =,"}
                )
                sample_id(user_name=user_name, sample_name=sample_name)
                print(f"\n\n\n\t=== Sample: {sample_name} ===")
                yield from bps.sleep(10)
                # yield from bp.count(dets)
                yield from bp.scan(dets, piezo.y, y-200, y+200, 3)



    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)

    # Turn off the heating and set temperature to 23 deg C
    t_kelvin = 23 + 273.15
    yield from ls.output1.mv_temp(t_kelvin)
    yield from ls.output1.turn_off()

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

def run_swaxs_Cai_2023_3(t=0.5):
    """
    Hard X-ray WAXS and SAXS
    Measure transmission only during the first run
    """
    #Capillaries, run 1
    #names =   [  'control0', '1.1', '1.2', '1.3', '1.4', '1.5', '5.M1', '5.M2', 'control1'] 
    #piezo_x = [ -13000, -6800, -800, 5800, 12200, 18600, 25000, 31400, 37400]   
    #piezo_y = [   2700, 2700, 2700, 2700, 2700, 2700, 2700, 2700, 2700]          
    #p0iezo_z = [ 14600 for n in names ]

    #Test 3, run 1
    #names =   [  'control_JustBeam', '4.1', '4.2', '4.3', '4.4', '4.6'] 
    #piezo_x = [ -41500, -20000, 2000, 28500, -33500, -1500, 32500]   
    #piezo_y = [  -4800, -4800, -4800, -6000, 7200, 7200, 7200]     
    #piezo_z = [ 9000 for n in names ]
    #piezo_z = [  14600, ]

    #Test 4, run 1
    #names =   [  'control_JustBeam', '4.1', '4.2', '4.3', '4.4', '4.5', '4.6'] 
    #piezo_x = [ -40000, -36000, -20000, -8000, 8500, 21500, 27500]   
    #piezo_y = [  1700, 1700, 1700, 1700, 1700, 1300, 1300]     
    #piezo_z = [ 9000 for n in names ]
    #piezo_z = [  14600, ]

    #Test 5, run 1
    names =   ['control_JustBeam', '6.1', '6.2', '6.3', '6.4', '6.5','6.6'] 
    piezo_x = [-42000, -36000, -20000, -12000, -2000, 6000, 14000]   
    piezo_y = [1700, 1700, 1700, 1700, 1700, 1700, 1700]     
    piezo_z = [ 9000 for n in names ]
    #piezo_z = [  14600, ]
    
    hexa_x =  [ 0 for n in names]

    msg = "Wrong number of coordinates"
    assert len(piezo_x) == len(names), msg
    assert len(piezo_x) == len(piezo_y), msg
    assert len(piezo_x) == len(piezo_z), msg
    assert len(piezo_x) == len(hexa_x), msg

    user_name = "DR"
    waxs_arc = [20, 0]

    points = 3
    dy = 150
    dbeam_x = -44000
    dbeam_y = 2400

    bs_pos = 2.90

    det_exposure_time(t, t)

    # Make sure cam server engages with the detector
    yield from engage_detectors()


    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)

        dets = [pil900KW] if waxs.arc.position < 15 else [pil1M, pil900KW]
        

        condition = (
            ( 19 < waxs.arc.position )
            and ( waxs.arc.position < 21 )
        )

        if condition:
            yield from atten_move_in()
            yield from bps.mv(pil1m_bs_rod.x, bs_pos + 5)
            yield from bps.mv(piezo.x, dbeam_x,
                              piezo.y, dbeam_y)

            sample_id(user_name='test', sample_name='test')
            yield from bp.count([pil1M])
            stats1_direct = db[-1].table(stream_name='primary')['pil1M_stats1_total'].values[0]
            yield from bps.mv(pil1m_bs_rod.x, bs_pos)
            yield from atten_move_out()

        for name, x, y, z, hx in zip(names, piezo_x, piezo_y, piezo_z, hexa_x):
            yield from bps.mv(piezo.x, x,
                              piezo.y, y,
                              piezo.z, z,
                              stage.x, hx)

            # Scan along the capillary
            for i in range(points):

                new_y = y + i * dy

                yield from bps.mv(piezo.y, new_y)

                if (condition and i == 0):

                    # Take transmission
                    yield from atten_move_in()

                    # Sample
                    yield from bps.mv(pil1m_bs_rod.x, bs_pos + 5)
                    sample_id(user_name='test', sample_name='test')
                    yield from bp.count([pil1M])
                    stats1_sample = db[-1].table(stream_name='primary')['pil1M_stats1_total'].values[0]

                    # Transmission
                    trans = np.round( stats1_sample / stats1_direct, 5)

                    # Revert configuraton
                    yield from bps.mv(pil1m_bs_rod.x, bs_pos)
                    yield from atten_move_out()
                
                if not condition:
                    trans = 0

                # Take normal scans
                sample_name = f'{name}{get_scan_md()}_loc{i}_trs{trans}'
                sample_id(user_name=user_name, sample_name=sample_name)
                print(f"\n\n\n\t=== Sample: {sample_name} ===")
                yield from bp.count(dets)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)


def cai_tensile_continous_hard_2023_3(t=0.2):
    """
    WAXS and SAXS continous measurement on Linkam MFS stage

    setthreshold energy 14000 autog 11500

    Args:
        t (float): detector exposure time,
    """

    name = "400-1-2000_PEG-PEGDA-NIPAM_Cast_Damp"

    # Sampe starting hexapod positions in mm
    stage_x = -0.2
    stage_y = 0.5

    # Calculate position pairs for sample offset
    # np.linspace(start, stop, number of points)
    yss = np.linspace(stage_y, stage_y + 0.1, 4)
    xss = np.linspace(stage_x, stage_x + 0.1, 3)
    yss, xss = np.meshgrid(yss, xss)
    yss = yss.ravel()
    xss = xss.ravel()

    # Delay between taking detector images in seconds
    delay = 0

    waxs_arc = [15, 7]
    det_exposure_time(t, t)
    user_name = "DR"

    #yield from engage_detectors()

    t0 = time.time()

    yield from bps.mv(stage.y, stage_y, stage.x, stage_x, waxs, waxs_arc[0])

    for i in range(5000):

        yield from bps.mv(stage.y, yss[i % len(yss)], stage.x, xss[i % len(xss)])

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)

            # Do not read SAXS if WAXS is in the way
            dets = [pil900KW] if waxs.arc.position < 10 else [pil1M, pil900KW]

            t1 = time.time()

            # Metadata
            step = str(i).zfill(3)
            td = str(np.round(t1 - t0, 1)).zfill(6)
            
            sample_name = f'{name}_step{step}_time{td}s{get_scan_md()}'
            sample_id(user_name=user_name, sample_name=sample_name)

            print(f"\n\t=== Step {i + 1} Sample: {sample_name} ===\n")
            yield from bp.count(dets)
        print(f"Sleep for {delay} seconds")
        yield from bps.sleep(delay)

    # End of the scan
    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)


def cai_giswaxs_temp_scan_2023_3(t=0.5):
    """
    Grazing incidence measurement using Lakeshore controlled heating bar
    """

    names   = [  'LBBL_35per', 'LfBBL_s2.70', 'MSolid1', 'MSolid2', 'MSolid3' ]
    piezo_x = [ -35500,               -16000,      8000,     26000,    44000]
    piezo_y = [ 600,  400,  -500, -900, -900]
    piezo_z = [ 5000 for n in names ]

    i = 1
    names   = names[i:]
    piezo_x = piezo_x[i:]
    piezo_y = piezo_y[i:]
    piezo_z = piezo_z[i:]


    temperatures = [26.7, 50, 75, 100, 125, 150, 175, 200, 225, 200, 175, 150, 125, 100, 75, 50, 25] 

    incident_angles = [0.125, 0.2]
    waxs_arc = [0, 20, 40]
    user_name = "DR"
    det_exposure_time(t, t)

    msg = "Wrong number of coordinates, check names, piezos, and hexas"
    assert len(piezo_x) == len(names), msg
    assert len(piezo_x) == len(piezo_y), msg
    assert len(piezo_y) == len(piezo_z), msg


    for ts, temperature in enumerate(temperatures):
        t_kelvin = temperature + 273.15
        yield from ls.output1.mv_temp(t_kelvin)

        # Activate heating range in Lakeshore
        #if temperature < 80:
        #   yield from bps.mv(ls.output1.status, 1)
        #else:
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
        print("Time needed to equilibrate: {:.1f} min".format((time.time() - start) / 60))

        # Wait extra time depending on temperature

        if (30 < temperature) and (temperature < 181):
            extra_time = 1200
        elif 160 <= temperature:
            extra_time = 1200
        else:
            extra_time = 0
        
        print(f'Equilibrating temperature for extra {extra_time} s\n')
        t_start = time.time()
        while (time.time() - t_start) < extra_time:
            print(f'Pumping time: {(time.time() - t_start):.1f} s')
            yield from bps.sleep(30)

        # Read T and convert to deg C
        temp_degC = ls.input_A.get() - 273.15

        for name, x, y, z in zip(names, piezo_x, piezo_y, piezo_z):

            yield from bps.mv(piezo.x, x,
                              piezo.y, y,
                              piezo.z, z,)

            # Align the sample
            try:
                yield from alignement_gisaxs_cai()
            except:
                yield from alignement_gisaxs(0.01)

            # Sample flat at ai0
            ai0 = piezo.th.position

            for wa in waxs_arc:
                yield from bps.mv(waxs, wa)
                dets = [pil900KW] if waxs.arc.position < 15 else [pil900KW, pil1M]
 
                for ai in incident_angles:
                    yield from bps.mv(piezo.th, ai0 + ai)

                    temp = str(np.round(float(temp_degC), 1)).zfill(5)
                    sample_name = f'{name}_ts{ts}_temp{temp}_ai{ai}{get_scan_md()}'
                    sample_id(user_name=user_name, sample_name=sample_name)
                    print(f"\n\n\n\t=== Sample: {sample_name} ===")
                    yield from bp.count(dets)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)

    # Turn off the heating and set temperature to 23 deg C
    t_kelvin = 23 + 273.15
    yield from ls.output1.mv_temp(t_kelvin)
    yield from ls.output1.turn_off()


def alignement_gisaxs_cai(angle=0.15):
    """
    Regular alignement routine for gisaxs and giwaxs.
    First, scan of the sample height and incident angle on the direct beam.
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
    yield from smi.setDirectBeamROI()

    # Scan theta and height
    yield from align_gisaxs_height(1000, 51, der=True)
    yield from align_gisaxs_th(5, 51)

    # move to theta 0 + value
    yield from bps.mv(piezo.th, ps.peak + angle)

    # Set reflected ROI
    yield from smi.setReflectedBeamROI(total_angle=angle, technique="gisaxs")

    # Scan theta and height
    #yield from align_gisaxs_th(0.2, 21)
    yield from align_gisaxs_th(0.5, 51)
    yield from align_gisaxs_height_rb(300, 31)
    yield from align_gisaxs_th(0.1, 31)  # was .025, 21 changed to .1 31

    # Close all the matplotlib windows
    plt.close("all")

    # Return angle
    yield from bps.mv(piezo.th, ps.cen - angle)
    yield from smi.modeMeasurement()

    # Deactivate the automated derivative calculation
    bec._calc_derivative_and_stats = False

def cai_printing_2023_3(xpos, ypos, sample_name='test'):
    """
    xpos=[startX, stop, npoints]
    ypos=[startY,step,npoints]%
    RE(mv(waxs, 0)) in BlueSky to move waxs
    """
    #RAU added move to starting y
    #bps.mvr(stage.y,ypos[0])
    yield from bps.mv(stage.y,ypos[0])
        
    sname = f'{sample_name}{get_scan_md()}'
    sample_id(user_name='DR', sample_name=sname)

    dets = [pil900KW, OAV_writing]
    if waxs.arc.position > 14:
        dets.append(pil1M)

    for yy,y in enumerate(range(ypos[2])):
        if np.mod(yy, 2) == 0:
            xs=xpos[0]; xe=xpos[1]
        else:
            xs=xpos[1]; xe=xpos[0]
        yield from bp.scan(dets, stage.x, xs, xe, xpos[2])
        yield from bps.mvr(stage.y,ypos[1])


def run_swaxs_Cai_2024_1(t=0.5):
    """
    Hard X-ray WAXS and SAXS
    Measure transmission only during the first run
    """
    
    #Test 5, run 1
    names =   [ 'MMA1.5',  'MMA1.7',  'MK2',  'MMA2.77',  'MM2.15',  'BnMA1.85',  'MK2-film',  'vacuum', ] 
    piezo_x = [   -46300,    -39800, -33500,      -3500,      8500,       17500,       29500,     41500, ]   
    piezo_y = [    -3000,     -3000,  -3000,      -3000,     -3000,       -3000,       -3000,     -3000, ]     
    piezo_z = [    10800,     10800,  10800,       4000,      4000,        4000,        4000,      4000, ]

    
    hexa_x =  [ 0 for n in names]

    msg = "Wrong number of coordinates"
    assert len(piezo_x) == len(names), msg
    assert len(piezo_x) == len(piezo_y), msg
    assert len(piezo_x) == len(piezo_z), msg
    assert len(piezo_x) == len(hexa_x), msg

    user_name = "PW"
    waxs_arc = [20, 0]

    points = 5
    dy = 150
    dbeam_x = -25900
    dbeam_y = -3000

    bs_pos = -199.0

    det_exposure_time(t, t)

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)

        dets = [pil900KW] if waxs.arc.position < 15 else [pil1M, pil900KW]
        
        condition = (
            ( 19 < waxs.arc.position )
            and ( waxs.arc.position < 21 )
        )

        if condition:
            yield from atten_move_in()
            yield from bps.mv(pil1m_bs_pd.x, bs_pos + 10)
            yield from bps.mv(piezo.x, dbeam_x,
                              piezo.y, dbeam_y)

            sample_id(user_name='test', sample_name='test')
            yield from bp.count([pil1M])
            stats1_direct = db[-1].table(stream_name='primary')['pil1M_stats1_total'].values[0]
            yield from bps.mv(pil1m_bs_pd.x, bs_pos)
            yield from atten_move_out()

        for name, x, y, z, hx in zip(names, piezo_x, piezo_y, piezo_z, hexa_x):
            yield from bps.mv(piezo.x, x,
                              piezo.y, y,
                              piezo.z, z,
                              stage.x, hx)

            # Scan along the capillary
            for i in range(points):

                new_y = y + i * dy

                yield from bps.mv(piezo.y, new_y)

                if (condition and i == 0):

                    # Take transmission
                    yield from atten_move_in()

                    # Sample
                    yield from bps.mv(pil1m_bs_pd.x, bs_pos + 5)
                    sample_id(user_name='test', sample_name='test')
                    yield from bp.count([pil1M])
                    stats1_sample = db[-1].table(stream_name='primary')['pil1M_stats1_total'].values[0]

                    # Transmission
                    trans = np.round( stats1_sample / stats1_direct, 5)

                    # Revert configuraton
                    yield from bps.mv(pil1m_bs_pd.x, bs_pos)
                    yield from atten_move_out()
                
                if not condition:
                    trans = 0

                # Take normal scans
                sample_name = f'{name}{get_scan_md()}_loc{i}_trs{trans}'
                sample_id(user_name=user_name, sample_name=sample_name)
                print(f"\n\n\n\t=== Sample: {sample_name} ===")
                yield from bp.count(dets)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)
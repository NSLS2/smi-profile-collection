def run_caps_fastRPI(t=1):
    x_list = [6908, 13476, 19764, 26055]  #
    # Detectors, motors:
    dets = [pil1M, pil300KW]
    waxs_range = np.linspace(0, 45.5, 8)
    samples = [
        "LC-O38-6-100Cto40C",
        "LC-O37-7-100Cto40C",
        "LC-O36-9-100Cto40C",
        "LC-O35-8-100Cto40C",
    ]
    #    param   = '16.1keV'
    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    det_exposure_time(t, t)
    for wa in waxs_range:
        yield from bps.mv(waxs, wa)
        for sam, x in zip(samples, x_list):
            yield from bps.mv(piezo.x, x)
            name_fmt = "{sam}_wa{waxs}"
            sample_name = name_fmt.format(sam=sam, waxs="%2.1f" % wa)
            sample_id(user_name=user, sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5)


def run_saxs_capsRPI(t=1):


    x_list = [6908, 13476, 19764, 26055]  #
    # Detectors, motors:
    dets = [pil1M]
    y_range = [2000, -8000, 11]  # [2.64, 8.64, 2]
    samples = [
        "LC-O38-6-100Cto40C",
        "LC-O37-7-100Cto40C",
        "LC-O36-9-100Cto40C",
        "LC-O35-8-100Cto40C",
    ]
    #    param   = '16.1keV'
    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    det_exposure_time(t)
    for x, sample in zip(x_list, samples):
        yield from bps.mv(piezo.x, x)
        sample_id(user_name=sample, sample_name="")
        yield from bp.scan(dets, piezo.y, *y_range)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5)


# ,'SL-PS3','SL-PS3_98_8_PS33','SL-PS3_97_0_PS33','SL-PS3_94_9_PS33','SL-PS3_93_0_PS33','SL-PS3_89_9_PS33','SL-PS3_79_8_PS33','SL-PS3_70_1_PS33','SL-PS3_60_0_PS33','SL-PS3_49_9_PS33','SL-PS3_40_0_PS33','SL-PS3_29_8_PS33','SL-PS3_20_1_PS33','SL-PS3_10_0_PS33','SL-PS3_7_0_PS33','SL-PS3_4_9_PS33','SL-PS3_3_0_PS33','SL-PS33','SL-PS148


# xlocs = [42000,33000,24000,15000,5000,-4000,-13000,-22000,-32000,-41000,42000,33000,24000,15000,5000,-4000,-13000,-22000,-32000,-41000]
# ylocs = [8800,8800,8800,8800,8800,8800,8800,8800,8800,8800,-7200,-7200,-7200,-7200,-7200,-7200,-7200,-7200,-7200,-7200]

# xlocs = [42000,33000,24000,15000,5000,-4000,-13000,-22000,-30000,42000,32000,24000,15000,4000,-4000,-12000]
# ylocs = [8500,8500,8500,8500,8500,8500,8500,8500,8500,-6800,-6800,-6800,-6800,-6800,-6800,-6800]
#  names = ['EPTD-y0.9-2s','EPTD-y1.0-2s','EPG-X0.8-2s','EPG-X0.9-2s','ETP-x0-2s','ETP-x0.1-2s','ETP-x0.2-2s','ETP-x0.3-2s','ETP-x0.4-2s','ETP-x0.6-2s','ETP-x0.7-2s','ETP-x0.8-2s','ETP-x0.9-2s','ETP-x1.0-2s','ETP-x0.5-2s','vacuum-2s']

#  xlocs = [-37550,-37550,-37550,-38950,-38950,-38950,-41850,-41850,-41850,-42850,-42850,-42850,-16100,-16100,-16100,-18600,-18600,-18600,-20400,-20400,-20400,-22500,-22500,-22500,-24100,-24100,-24100, -26100,-26100,-26100,-28300,-28300,-28300,-29300,-29300,-29300,-32900,-32900,-32900,-34900,-34900,-34900]
#   ylocs = [8000, 8500,9000, 8000, 8500,9000, 8000, 8500,9000, 8000, 8500,9000,-7000, -7500, -8000,-7000, -7500, -8000,-7000, -7500, -8000,-7000, -7500, -8000,-7000, -7500, -8000,-7000, -7500, -8000,-7000, -7500, -8000,-7000, -7500, -8000,-7000, -7500, -8000,-7000, -7500, -8000]
#   names = ['PACM-1','PACM-2','PACM-3','EPON828-1','EPON828-2','EPON828-3','DDS-1','DDS-2','DDS-3','B8O1-3-1','B8O1-3-2','B8O1-3-3','D2000-1','D2000-2','D2000-3','T3000-1','T3000-2','T3000-3','PPG-1','PPG-2','PPG-3','D230-1','D230-2','D230-3','blank-1mm-1','blank-1mm-2','blank-1mm-3','B8O1-1-1','B8O1-1-2','B8O1-1-3','B8O1-2-1','B8O1-2-2','B8O1-2-3','B9O1-1-1','B9O1-1-2','B9O1-1-3','B10O1-1-1','B10O1-1-2','B10O1-1-3','vacuum-1s-1','vacuum-1s-2','vacuum-1s-3']


def run_saxs_capsRPI_2021_1(t=1):

    # samples = ['J1_S01_14wt_q55_01', 'J1_S02_14wt_q45_01', 'J1_S03_14wt_q35_01', 'J1_S04_14wt_q25_01', 'J1_S05_14wt_q25_h45_01', 'J1_S06_15wt_q60_01',
    # 'J1_S07_15wt_q55_01', 'J1_S08_15wt_q50_01', 'J1_S09_15wt_q40_01', 'J1_S10_15wt_q25_01', 'J1_S11_15wt_q25_h55_01', 'J1_S12_16wt_q65_01',
    # 'J1_S13_16wt_q60_01', 'J1_S14_16wt_q55_01', 'J1_S15_16wt_q50_01']
    # xlocs = [ 44000, 38000, 31600, 25200, 19100, 12900, 6500, 200, -6350, -12700, -19050, -25350, -31200, -37800, -44250]
    # y_range = [-4100, 1030, 20]

    # samples = ['J2_S01_16wt_q45_01', 'J2_S02_16wt_q40_01', 'J2_S03_16wt_q25_01', 'J2_S04_16wt_q25_h60_01', 'J2_S05_16wt_q25_h55_01',
    # 'J2_S06_16wt_q25_h50_01', 'J2_S07_17wt_q65_01', 'J2_S08_17wt_q50_01', 'J2_S09_17wt_q40_01', 'J2_S10_17wt_q25_01', 'J2_S11_17wt_q25_h65_01',
    # 'J2_S12_17wt_q25_h50_01', 'J2_S13_18wt_q77_01', 'J2_S14_18wt_q70_01', 'J2_S15_18wt_q65_01']
    # xlocs = [ 44200, 37950, 31700, 25450, 19250, 12750, 6100, 0, -6100, -12450, -18800, -25150, -31300, -37900, -43850]
    # y_range = [-4100, 1030, 20]

    # samples = ['J3_S01-18wt_q60_01', 'J3_S02_18wt_q40_01', 'J3_S03_18wt_q25_01', 'J3_S04_18wt_q25_h70_01', 'J3_S05_18wt_q25_h50_01', 'J3_S06_19wt_q65_01',
    # 'J3_S07_19wt_q55_01', 'J3_S08_19wt_q40_01', 'J3_S09_19wt_q25_01', 'J3_S10_19wt_q25_h77_01', 'J3_S11_19wt_q25_h70_01', 'J3_S12_20wt_q82_01',
    # 'J3_S13_20wt_q79_01', 'J3_S14_20wt_q75_01', 'J3_S15_20wt_q60_01']
    # xlocs = [ 44000, 38100, 31750, 25100, 18750, 12400, 6550, -100, -6000, -12400, -19000, -25100, -31300, -37650, -44150]
    # y_range = [-4100, 1030, 20]

    # samples = ['J4_S01_20wt_q40_01', 'J4_S02_20wt_q25_01', 'J4_S03_20wt_q25_h79_01', 'J4_S04_20wt_q25_h70_01', 'J4_S05_21wt_q84_01', 'J4_S06_21wt_q81_01',
    # 'J4_S07_21wt_q75_01', 'J4_S08_21wt_q70_01', 'J4_S09_21wt_q50_01', 'J4_S10_21wt_q25_01', 'J4_S11_21wt_q25_h81_01', 'J4_S12_21wt_q25_h70_01',
    # 'J4_S13_22wt_q86_01', 'J4_S14_22wt_q83_01', 'J4_S15_22wt_q80_01']
    # xlocs = [ 44000, 37450, 31200, 24900, 18850, 12700, 6400, -50, -6400, -12650, -18950, -25300, -31700, -38050, -44550]
    # y_range = [-4100, 1030, 20]

    # samples = ['J5_S01_22wt_q75_01', 'J5_S02_22wt_q60_01', 'J5_S03_22wt_q40_01', 'J5_S04_22wt_q25_01', 'J5_S05_22wt_q25_h83_01', 'J5_S06_22wt_q25_h75_01',
    # 'J5_S07_23wt_q88_01', 'J5_S08_23wt_q84_01', 'J5_S09_23wt_q80_01', 'J5_S10_23wt_q75_01', 'J5_S11_23wt_q60_01', 'J5_S12_23wt_q40_01',
    # 'J5_S13_23wt_q25_01', 'J5_S14_23wt_q25_h84_01', 'J5_S15_23wt_q25_h75_01']
    # xlocs = [ 44050, 37950, 31600, 25450, 19150, 12900, 6350, 0, -6300, -12500, -18800, -25150, -31200, -37800, -43900]
    # y_range = [-4100, 1030, 20]

    # samples = ['J6_S01_24wt_q93_01', 'J6_S02_24wt_q90_01', 'J6_S03_24wt_q80_01', 'J6_S04_24wt_q75_01', 'J6_S05_24wt_q60_01', 'J6_S06_24wt_q40_01',
    # 'J6_S07_24wt_q25_01', 'J6_S08_24wt_q25_h90_01', 'J6_S09_24wt_q25_h75_01', 'J6_S10_12wt_q40_01', 'J6_S11_12wt_q35_01', 'J6_S12_12wt_q25_01',
    # 'J6_S13_12wt_q25_h40_01', 'J6_S14_127wt_q45_01', 'J6_S15_127wt_q40_01']
    # xlocs = [ 44300, 38050, 31700, 25350, 19050, 12700, 6550, 0, -5900, -12550, -18650, -24950, -31100, -37450, -43800]
    # y_range = [-4100, 1030, 20]

    # samples = ['J7_S01_127wt_q35_01', 'J7_S02_127wt_q25_01', 'J7_S03_127wt_q25_h40_01', 'J7_S04_137wt_q55_01', 'J7_S05_137wt_q45_01',
    # 'J7_S06_137wt_q35_01', 'J7_S07_137wt_q25_01', 'J7_S08_137wt_q25_h45_01', 'J7_S09_S_water_01', 'J7_S10_blank_cap_01']
    # xlocs = [ 44100, 37450, 31200, 25200, 18750, 12600, 6100, 0, -6550, -12800]
    # y_range = [-4100, 1030, 20]

    samples = [
        "CT1_1_Blank_S_11",
        "CT1_2_QAT2C_S_11",
        "CT1_3_QAT3C_S_11",
        "CT1_4_QAT5C_S_11",
        "CT1_5_QAT6C_S_11",
        "CT1_6_QAT7C_S_11",
        "CT1_12_QAS7C_S_11",
        "CT1_13_QAS9C_S_11",
        "CT1_14_QAS10C_S_11",
        "CT1_15_QAS11C_S_11",
    ]
    xlocs = [44400, 38100, 31600, 25200, 19200, 12700, -24900, -31300, -37800, -44000]
    y_range = [-3000, 0, 4]

    # samples = ['CT2_1_QAT2CP_S_11', 'CT2_2_QAT3CP_S_11', 'CT2_3_QAT5CP_S_11', 'CT2_4_QAT6CP_S_11', 'CT2_5_QAT7CP_S_11',
    # 'CT2_9_QAS7CP_S_11', 'CT2_11_QAS9CP_S_11', 'CT2_12_QAS10CP_S_11', 'CT2_14_QAS11CP_S_11']
    # xlocs = [ 44100, 37450, 31200, 25200, 18750, 12600, 6100, 0, -6550, -12800]
    # y_range = [-4100, 1030, 20]

    assert len(xlocs) == len(
        samples
    ), f"Number of X coordinates ({len(xlocs)}) is different from number of samples ({len(samples)})"

    dets = [pil1M]
    det_exposure_time(t)

    for x, sample in zip(xlocs, samples):
        yield from bps.mv(piezo.x, x)
        sample_id(user_name=sample, sample_name="")
        yield from bp.scan(dets, piezo.y, *y_range)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5)


def run_waxs_fastRPI_2021_(t=1):
    # samples = ['CT1_1_Blank_S_11', 'CT1_2_QAT2C_S_11', 'CT1_3_QAT3C_S_11', 'CT1_4_QAT5C_S_11', 'CT1_5_QAT6C_S_11', 'CT1_6_QAT7C_S_11',
    # 'CT1_12_QAS7C_S_11', 'CT1_13_QAS9C_S_11', 'CT1_14_QAS10C_S_11', 'CT1_15_QAS11C_S_11']
    # xlocs = [44400, 38100, 31600, 25200, 19200, 12700, -24900, -31300, -37800, -44000]
    # y_range = [-3000, 0, 4]

    samples = [
        "CT2_1_QAT2CP_S_11",
        "CT2_2_QAT3CP_S_11",
        "CT2_3_QAT5CP_S_11",
        "CT2_4_QAT6CP_S_11",
        "CT2_5_QAT7CP_S_11",
        "CT2_9_QAS7CP_S_11",
        "CT2_11_QAS9CP_S_11",
        "CT2_12_QAS10CP_S_11",
        "CT2_14_QAS11CP_S_11",
    ]
    xlocs = [44500, 38400, 32000, 25600, 19400, -5600, -18600, -24700, -37400]
    y_range = [-3000, 0, 4]

    user = "SL"

    # Check if the length of xlocs, ylocs and names are the same
    assert len(xlocs) == len(
        samples
    ), f"Number of X coordinates ({len(xlocs)}) is different from number of samples ({len(samples)})"

    # Detectors, motors:
    dets = [pil1M, pil300KW]
    waxs_range = np.linspace(0, 45.5, 8)

    for wa in waxs_range:
        yield from bps.mv(waxs, wa)
        for sam, x in zip(samples, xlocs):
            yield from bps.mv(piezo.x, x)

            name_fmt = "{sam}_wa{waxs}"
            sample_name = name_fmt.format(sam=sam, waxs="%2.1f" % wa)
            sample_id(user_name=user, sample_name=sample_name)

            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.scan(dets, piezo.y, *y_range)


def run_waxs_fastRPI_2021_2(t=1):

    y_top = -8000
    y_bot = 8000
    #         1      2       3       4       5      6      7       8       9
    xlocs = [
        42000,
        33000,
        20000,
        12000,
        5000,
        -6500,
        -16000,
        -26000,
        -36000,
        42000,
        34000,
        23000,
        12000,
    ]
    ylocs = [
        y_top,
        y_top,
        y_top,
        y_top,
        y_top,
        y_top,
        y_top,
        y_top,
        y_top,
        y_bot,
        y_bot,
        y_bot,
        y_bot,
    ]

    # xlocs = [ 42000, 33000,  22000,  12000,  5000, -6500, -16000, -25000, -34000,
    #           42000, 33000,  22000,  12000,  5000, -6500, -17500, -25000, -34000]
    # ylocs = [ y_top, y_top,  y_top,  y_top,  y_top, y_top, y_top,  y_top,  y_top,
    #           y_bot, y_bot,  y_bot,  y_bot,  y_bot, y_bot, y_bot,  y_bot,  y_bot]

    # Capillary
    # x_off = [0]
    # y_off = [-1000, -500, 0, 500, 1000]

    # Plaques
    x_off = [-500, 0, 500]
    y_off = [-500, 500]

    # # Rack N1 - Plaques
    #         1                      2                    3                     4                     5                     6                     7                     8                      9
    # names =['N1_S01_ETTD_m04_n00','N1_S02_ETTD_m04_n01','N1_S03_ETTD_m04_n02','N1_S04_ETTD_m04_n03','N1_S05_ETTD_m04_n04','N1_S06_ETTD_m04_n05','N1_S07_ETTD_m04_n06','N1_S08_ETTD_m04_n07','N1_S09_ETTD_m04_n08',
    #        'N1_S10_ETTD_m04_n09','N1_S11_ETTD_m04_n10','N1_S12_ETTD_m05_n00','N1_S13_ETTD_m05_n01','N1_S14_ETTD_m05_n02','N1_S15_ETTD_m05_n03','N1_S16_ETTD_m05_n04','N1_S17_ETTD_m05_n05','N1_S18_ETTD_m05_n06']

    # # Rack N1 - Capillaries
    #         1       2
    # xlocs = [ -40300, -43300]
    # ylocs = [ 8500, 8500]
    # names =['E80_T20_S_25C','E50_D50_S_25C']

    # # Rack N2 - Plaques
    #        1                      2                    3                     4                     5                     6                     7                     8                      9
    # names =['N2_S01_ETTD_m05_n07','N2_S02_ETTD_m05_n08','N2_S03_ETTD_m05_n09','N2_S04_ETTD_m05_n10','N2_S05_ETTD_m06_n00','N2_S06_ETTD_m06_n01','N2_S07_ETTD_m06_n02','N2_S08_ETTD_m06_n03','N2_S09_ETTD_m06_n04',
    #        'N2_S10_ETTD_m06_n05','N2_S11_ETTD_m06_n06','N2_S12_ETTD_m06_n07','N2_S13_ETTD_m06_n08','N2_S14_ETTD_m06_n09','N2_S15_ETTD_m06_n10','N2_S16_ETTD_m07_n00','N2_S17_ETTD_m07_n01','N2_S18_ETTD_m07_n02']

    # # Rack N3 - Plaques
    #         1                     2                     3                     4                     5                     6                     7                     8                     9
    # names =['N3_S01_ETTD_m07_n03','N3_S02_ETTD_m07_n04','N3_S03_ETTD_m07_n05','N3_S04_ETTD_m07_n06','N3_S05_ETTD_m07_n07','N3_S06_ETTD_m07_n08','N3_S07_ETTD_m07_n09','N3_S08_ETTD_m07_n10','N3_S09_ETTD_m08_n00',
    #         'N3_S10_ETTD_m08_n01','N3_S11_ETTD_m08_n02','N3_S12_ETTD_m08_n03','N3_S13_ETTD_m08_n04','N3_S14_ETTD_m08_n05','N3_S15_ETTD_m08_n06','N3_S16_ETTD_m08_n07','N3_S17_ETTD_m08_n08','N3_S18_ETTD_m08_n09']

    # # Rack N4 - Plaques
    #         1                     2                     3                     4                     5                     6                     7                     8                      9
    # names =['N4_S01_ETTD_m08_n10','N4_S02_ETTD_m09_n00','N4_S03_ETTD_m09_n01','N4_S04_ETTD_m09_n02','N4_S05_ETTD_m09_n03','N4_S06_ETTD_m09_n04','N4_S07_ETTD_m09_n05','N4_S08_ETTD_m09_n06','N4_S09_ETTD_m09_n07',
    #         'N4_S10_ETTD_m09_n08','N4_S11_ETTD_m09_n09','N4_S12_ETTD_m09_n10','N4_S13_DETT_e00',    'N4_S14_DETT_e01',    'N4_S15_DETT_e02',    'N4_S16_DETT_e03',    'N4_S17_DETT_e04',    'N4_S18_DETT_e05']

    # # Rack N5 - Plaques
    #         1                 2                 3                 4                 5                 6                 7                 8                 9
    # names =['N5_S01_DETT_e06','N5_S02_DETT_e07','N5_S03_DETT_e08','N5_S04_DETT_e09','N5_S05_DETT_e10','N5_S06_ETRD_R00','N5_S07_ETRD_R01','N5_S08_ETRD_R02','N5_S09_ETRD_R03',
    #         'N5_S10_ETRD_R04','N5_S11_ETRD_R05','N5_S12_ETRD_R06','N5_S13_ETRD_R07','N5_S14_ETRD_R08','N5_S15_ETRD_R09','N5_S16_ETRD_R10','N5_S17_EDPT_R00','N5_S18_EDPT_R01']

    # # Rack N6 - Plaques
    #         1                 2                 3                 4                 5                 6                 7                 8                 9
    names = [
        "N6_S01_EDPT_R02",
        "N6_S02_EDPT_R03",
        "N6_S03_EDPT_R04",
        "N6_S04_EDPT_R05",
        "N6_S05_EDPT_R06",
        "N6_S06_EDPT_R07",
        "N6_S07_EDPT_R08",
        "N6_S08_EDPT_R09",
        "N6_S09_EDPT_R10",
        "N6_S10_ED",
        "N6_S11_EP",
        "N6_S12_D7TE",
        "N6_S13_D7T3",
    ]

    user = "SL"
    det_exposure_time(t, t)

    # Check if the length of xlocs, ylocs and names are the same
    assert len(xlocs) == len(
        names
    ), f"Number of X coordinates ({len(xlocs)}) is different from number of samples ({len(names)})"
    assert len(xlocs) == len(
        ylocs
    ), f"Number of X coordinates ({len(xlocs)}) is different from number of samples ({len(ylocs)})"

    # Detectors, motors:
    dets = [pil1M, pil300KW]
    waxs_range = np.linspace(45.5, 0, 8)

    for wa in waxs_range:
        yield from bps.mv(waxs, wa)
        for sam, x, y in zip(names, xlocs, ylocs):
            yield from bps.mv(piezo.x, x)
            yield from bps.mv(piezo.y, y)
            for yy, y_of in enumerate(y_off):
                yield from bps.mv(piezo.y, y + y_of)
                for xx, x_of in enumerate(x_off):
                    yield from bps.mv(piezo.x, x + x_of)
                    xxa = xx + 1
                    yya = yy + 1
                    name_fmt = "{sam}_wa{waxs}_loc{xx}{yy}"
                    sample_name = name_fmt.format(
                        sam=sam, xx="%1.1d" % xxa, yy="%1.1d" % yya, waxs="%2.1f" % wa
                    )
                    sample_id(user_name=user, sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def run_waxs_fastRPI(t=1):

    names = ["TR_ETTD_m03_n05_S_40min_80C_0.5sx8"]
    user = "SL"
    det_exposure_time(t, t)

    # Detectors, motors:
    dets = [pil1M, pil300KW]
    waxs_range = np.linspace(45.5, 0, 8)

    for wa in waxs_range:
        yield from bps.mv(waxs, wa)
        name_fmt = "{sam}_wa{waxs}"
        sample_name = name_fmt.format(sam=names[0], waxs="%2.1f" % wa)
        sample_id(user_name=user, sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")
        yield from bp.count(dets, num=1)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def run_saxs_linkamRPI(t=1):

    names = ["B5O3-18wt-30T-5-211-25C-89C77m"]
    user = "SL"
    det_exposure_time(t, t)

    # y_range = [1.85, 1.85, 1]
    y_range = [2.75, 1.8, 6]
    # y_range = [2.75, 2.75, 1]

    # Detectors, motors:
    dets = [pil1M]
    # waxs_range = np.linspace(45.5, 0, 8)

    name_fmt = "{sam}"
    sample_name = name_fmt.format(sam=names[0])
    sample_id(user_name=user, sample_name=sample_name)
    print(f"\n\t=== Sample: {sample_name} ===\n")
    yield from bp.scan(dets, stage.y, *y_range)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def run_waxs_fastRPIy(t=1):

    xlocs = [39000, 19000, 3000]
    ylocs = [-6000, -6000, -6000]
    names = ["CW-mTPNI-3", "CW-mTPNI-4", "CW-mTPNI-5"]

    y_off = [8000, 7000, 6000, 5000, 4000, 3000, 2000]
    user = "SL"
    det_exposure_time(t, t)

    assert len(xlocs) == len(
        names
    ), f"Number of X coordinates ({len(x_locs)}) is different from number of samples ({len(samples)})"

    # Detectors, motors:
    dets = [pil1M, pil300KW]
    waxs_range = np.linspace(13, 13, 1)

    # yield from bps.mv(GV7.open_cmd, 1 )
    # yield from bps.sleep(10)
    # yield from bps.mv(GV7.open_cmd, 1 )
    # yield from bps.sleep(10)
    # yield from bps.mv(GV7.open_cmd, 1 )
    # yield from bps.sleep(10)

    for wa in waxs_range:
        yield from bps.mv(waxs, wa)
        for sam, x, y in zip(names, xlocs, ylocs):
            yield from bps.mv(piezo.x, x)
            yield from bps.mv(piezo.y, y)
            for yy, y_of in enumerate(y_off):
                yield from bps.mv(piezo.y, y + y_of)

                name_fmt = "{sam}_wa{waxs}_yloc{yy}"
                sample_name = name_fmt.format(
                    sam=sam, yy="%2.2d" % yy, waxs="%2.1f" % wa
                )
                sample_id(user_name=user, sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)

    # yield from bps.mv(GV7.close_cmd, 1 )
    # yield from bps.sleep(10)
    # yield from bps.mv(GV7.close_cmd, 1 )
    # yield from bps.sleep(10)
    # yield from bps.mv(GV7.close_cmd, 1 )
    # yield from bps.sleep(10)


def run_waxs_cap_temp(t=1):
    ylocs = [3.9]  # Between 3.1 and 4.1
    name = "nPEO_isothermal40"
    user = "DW"

    det_exposure_time(t, t)
    dets = [pil1M, pil300KW]
    waxs_range = np.linspace(0, 13, 3)

    for wa in waxs_range:
        if wa == 0:
            temp = ls.ch1_read.value
        yield from bps.mv(waxs, wa)
        for y in ylocs:
            yield from bps.mv(stage.y, y)
            # temp = ls.ch1_read.value
            name_fmt = "{sam}_wa{waxs}_temp{tem}"
            sample_name = name_fmt.format(sam=name, tem=temp, waxs="%2.1f" % wa)
            sample_id(user_name=user, sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)

    yield from bps.mv(waxs, 0)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def run_saxs_fastRPI(t=1):

    xlocs = [
        42500,
        38300,
        29300,
        22900,
        16400,
        9000,
        2500,
        -3800,
        -7800,
        -11800,
        -15400,
        -19400,
        -23200,
        -27700,
        -31600,
        -34900,
        -38600,
    ]
    ylocs = [
        5500,
        5500,
        5500,
        5500,
        5500,
        5500,
        5500,
        5500,
        5500,
        5500,
        5500,
        5500,
        5500,
        5500,
        5500,
        5500,
        5500,
    ]
    names = [
        "BPSAW",
        "FLSAW",
        "DW-01",
        "DW-02",
        "DW-03",
        "DW-04",
        "blank-capillary",
        "mTPSAW",
        "BPSArSA-DMACw",
        "BPSArSA-DMSOW",
        "BPSOArSAW",
        "pTPSAW",
        "XW-1-35-1wd",
        "XW-1-35-2w",
        "XW-1-35-3w",
        "XW-1-35-4w",
        "blankW",
    ]

    user = "LC_SAXS_ONLY"
    det_exposure_time(t, t)

    assert len(xlocs) == len(
        names
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"

    # Detectors, motors:
    dets = [pil1M]
    for sam, x, y in zip(names, xlocs, ylocs):
        yield from bps.mv(piezo.y, y)
        yield from bps.mv(piezo.x, x)
        name_fmt = "{sam}"
        sample_name = name_fmt.format(sam=sam)
        sample_id(user_name=user, sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")
        yield from bp.count(dets, num=1)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def run_contRPI(t=1, numb=100, sleep=5):

    det_exposure_time(t, t)
    dets = [pil1M, pil300KW]
    # dets = [pil300Kw]
    for i in range(numb):
        yield from bp.count(dets, num=1)
        yield from bps.sleep(sleep)


def acq_tem(t=0.2):
    sam = "0122A-11-lk5.5m-1s"

    dets = [pil1M]
    det_exposure_time(t, t)
    temp = ls.ch1_read.value
    name_fmt = "{sam}_{temp}C"
    sample_name = name_fmt.format(sam=sam, temp="%4.1f" % temp)
    sample_id(user_name="LC", sample_name=sample_name)
    yield from bp.scan(dets, stage.y, 5.3, 5.9, 4)


def acq_bd(t=0.2):
    sam = "0122A-10-lk5.5m-0.2s-4"

    dets = [pil1M]
    det_exposure_time(t, t)
    temp = ls.ch1_read.value
    name_fmt = "{sam}_{temp}C"
    sample_name = name_fmt.format(sam=sam, temp="%4.1f" % temp)
    sample_id(user_name="LC", sample_name=sample_name)
    yield from bp.scan(dets, piezo.th, 0, 0, 1)


# Sample set 1
# xlocs = [60000,38700,31700,25700,20700,11900,2899,-13100,-28100,-37100,-42099,-35100,-28100,-23000,-16000,-8200,-2200,3800,12800,19800,25800,33800,41800]
# ylocs = [7300,7300,7300,7300,7300,7300,7300,7300,7300,7300,7300,-8700,-8700,-8700,-8700,-8700,-8700,-8700,-8700,-8700,-8700,-8700,-8700]
# names = ['blank','XW-01-033','NF150-1A','NF150-2A','NF150-1B','NF150-2B','DW-13','DW-14','DW-15','DW-nPEO','Blank Kapton','XW-01-40','XW-1-35-4d','XW-1-35-3d','XW-1-35-2d','XW-1-35-1d','Fenton-BPSOArSA','Fenton-BPSArSA','Fenton-mTPSA','Fenton-BPSA','BPSArSA-DMSOd','pTPSAd','FLSAd']


# ylocs = [5000,5000,5000,5000,5000]
#   xlocs = [29500,23000,16500,9000,2600]
#  names = ['DW-1','DW-2','DW-3','DW-4','blankcap-1.5-vacuum']

# Sample set 3
# xlocs = [43800,33100,24100,14800,4400,-6900,-16600,-18200,-27400,-28400,-36400,-40400,44800,39800,34800,31800,25800,21800,16800,13000,6800,4000,-2200,-5200,-11200,-14400,-21200,-23400,-31200,-33400,-40000,-43000]
#  ylocs = [8400,8400,8400,8400,8400,8400,8400,8400,8400,8000,8400,8400,-6000,-6000,-6000,-6000,-6000,-6000,-6000,-6000,-6000,-6000,-6000,-6000,-6000,-6000,-6000,-6000,-6000,-6000,-6000,-6000]
# names = ['m-TPN1-11-1','m-TPN1-11-2','m-TPN1-CNC-13','m-TPN1-CNC-14','m-TPN1-CNC-15-5','m-TPN1-CNC-15-m','SP59-1','SP59-2','P59-1','P59-2','828-T3000-PAM-X0.0-1','828-T3000-PAM-X0.0-2','828-T3000-PAM-X0.1-1','828-T3000-PAM-X0.1-2','828-T3000-PAM-X0.3-1','828-T3000-PAM-X0.3-2','828-T3000-PAM-X0.4-1','828-T3000-PAM-X0.4-2','828-T3000-PAM-X0.5-1','828-T3000-PAM-X0.5-2','828-T3000-PAM-X0.6-1','828-T3000-PAM-X0.6-2','828-T3000-PAM-X0.7-1','828-T3000-PAM-X0.7-2','828-T3000-PAM-X0.8-1','828-T3000-PAM-X0.8-2','828-T3000-PAM-X0.9-1','828-T3000-PAM-X0.9-2','828-T3000-PAM-X1.0-1','828-T3000-PAM-X1.0-2']


# Sample set 4
# names = ['828-T3000-D230-PACM-X0.7-Y0.0-1','828-T3000-D230-PACM-X0.7-Y0.0-2','828-T3000-D230-PACM-X0.7-Y0.1-1','828-T3000-D230-PACM-X0.7-Y0.1-2','828-T3000-D230-PACM-X0.7-Y0.2-1','828-T3000-D230-PACM-X0.7-Y0.2-2','828-T3000-D230-PACM-X0.7-Y0.3-1','828-T3000-D230-PACM-X0.7-Y0.3-2','828-T3000-D230-PACM-X0.7-Y0.4-1','828-T3000-D230-PACM-X0.7-Y0.4-2','828-T3000-D230-PACM-X0.7-Y0.5-1','828-T3000-D230-PACM-X0.7-Y0.5-2','828-T3000-D230-PACM-X0.7-Y0.6-1','828-T3000-D230-PACM-X0.7-Y0.6-2','828-T3000-D230-PACM-X0.7-Y0.7-1','828-T3000-D230-PACM-X0.7-Y0.7-2','828-T3000-D230-PACM-X0.7-Y0.8-1','828-T3000-D230-PACM-X0.7-Y0.8-2','828-T3000-D230-PACM-X0.7-Y0.9-1','828-T3000-D230-PACM-X0.7-Y0.9-2','828-T3000-D230-PACM-X0.7-Y1.0-1','828-T3000-D230-PACM-X0.7-Y1.0-2','828-EK3140-PACM-X0.0-1','828-EK3140-PACM-X0.0-2','828-EK3140-PACM-X0.1-1','828-EK3140-PACM-X0.1-2','828-EK3140-PACM-X0.2-1','828-EK3140-PACM-X0.2-2','828-EK3140-PACM-X0.3-1','828-EK3140-PACM-X0.3-2','828-EK3140-PACM-X0.4-1','828-EK3140-PACM-X0.4-2','828-EK3140-PACM-X0.5-1','828-EK3140-PACM-X0.5-2','828-EK3140-PACM-X0.6-1','828-EK3140-PACM-X0.6-2','828-EK3140-PACM-X0.7-1','828-EK3140-PACM-X0.7-2','828-EK3140-PACM-X0.8-1','828-EK3140-PACM-X0.8-2']

# ylocs =        [8400,8400,8400,8400,8400,8400,8400,8400,8400,8400,8400,8400,8400,8400,8400,8400,8400,8400,8400,8400,-7000,-7000,-7000,-7000,-7000,-7000,-7000,-7000,-7000,-7000,-7000,-7000,-7000,-7000,-7000,-7000,-7000,-7000,-7000,-7000]
# xlocs = [44000,39800,34800,31500,25800,21800,16800,13000,6800,4000,-2200,-5200,-12200,-14400,-21200,-23400,-31200,-33400,-40000,-43000,44000,39800,34800,31500,25800,21800,16600,13000,6800,4000,-2200,-5200,-12200,-14400,-21200,-23400,-32000,-33400,-40000,-42500]


# Sample set 5
# ylocs =        [8000,8000,8000,8200,8000,8400,8400,8400,8600,8600,8600,8600,8600,8200,8200,8200,8200,8200,8200,8200,-6600,-6600,-6600,-6600,-6600,-6600,-6600,-6600,-6600,-6600,-7000,-7000,-7000,-7000,-7000,-7000,-7000,-7000,-7000,-7000]

#  xlocs = [43000,41400,34500,32800,26500,22500,17500,14500,7500,3500,-500,-5500,-10500,-14500,-20500,-23500,-29500,-33500,-39500,-42500,44000,41000,36000,33000,27000,23000,18000,14000,8000,4000,0,-6000,-10000,-13500,-20500,-23500,-30500,-32500,-39500,-42500]

# names = ['828-EK3140-PACM-X0.9-1','828-EK3140-PACM-X0.9-2','828-EK3140-PACM-X1.0-1','828-EK3140-PACM-X1.0-2','828-D2000-PACM-X0.6-1','828-D2000-PACM-X0.6-2','828-D2000-PACM-X0.7-1','828-D2000-PACM-X0.7-2','828-D2000-PACM-X0.8-1','828-D2000-PACM-X0.8-2','828-D2000-PACM-X0.9-1','828-D2000-PACM-X0.9-2','828-D2000-PACM-X1.0-1','828-D2000-PACM-X1.0-2','TGPPM-2E1-0.00MDA-1','TGPPM-2E1-0.00MDA-2','TGPPM-2E1-0.25MDA-1','TGPPM-2E1-0.25MDA-2','TGPPM-2E1-0.50MDA-1','TGPPM-2E1-0.50MDA-2','TGPPM-2E1-0.75MDA-1','TGPPM-2E1-0.75MDA-2','TGPPM-2E1-1.00MDA-1','TGPPM-2E1-1.00MDA-2','TCDDA-XDT-1-1','TCDDA-XDT-1-2','TCDDA-XDT-2-1','TCDDA-XDT-2-2','TCDDA-XDT-3-1','TCDDA-XDT-3-2','TCDDA-XDT-4-1','TCDDA-XDT-4-2','TCDDA-XDT-5-1','TCDDA-XDT-5-2','TCDDA-XDT-6-1','TCDDA-XDT-6-2','TCDDA-XDT-7-1','TCDDA-XDT-7-2','TCDDA-XDT-8-1','TCDDA-XDT-8-2']


# Sample set 6-1
# names = [TCDDA-XDT-10-1,TCDDA-XDT-10-2,TCDDA-XDT-11-1,TCDDA-XDT-11-2,TCDDA-XDT-12-1,TCDDA-XDT-12-2,TCDDA-XDT-13-1,TCDDA-XDT-13-2,TCDDA-XDT-14-1,TCDDA-XDT-14-2,TCDDA-XDT-15-1,TCDDA-XDT-15-2,TCDDA-XDT-16-1,TCDDA-XDT-16-2,TCDDA-XDT-17-1,TCDDA-XDT-17-2,TCDDA-XDT-18-1,TCDDA-XDT-18-2,SP-2d-1,SP-2d-2,TCDDA-XDT-9-1,TCDDA-XDT-9-2,SP-1b-1,SP-1b-2,SP-1d-1,SP-1d-2,SP-2b-1,SP-2b-2,SP-3b-1,SP-3b-2,SP-3d-1,SP-3d-2,SP-5b-1,SP-5b-2,SP-6b-1,SP-6b-2,SP-4b-1,SP-4b-2,vacuum-10s]
# ylocs =        [8000,8000,8000,8000,8000,8000,8000,8000,8000,8000,8000,8600,8600,8000,8000,8600,8800,8000,8000,8000,-7000,-6500,-7200,-7200,-7000,-7000,-7000,-7000,-7000,-7000,-7000,-7000,-7000,-7000,-7000,-6500,-7200,-7200,-6500]

#  xlocs = [44000,42000,36000,33000,26000,23000,17000,14000,8000,4000,-1000,-7000,-10000,-15000,-22000,-25000,-30000,-33000,-42000,-43500,45000,42000,36000,34500,29000,27000,22000,20000,12000,10000,4500,3000,-4000,-5500,-13500,-15000,-20000,-21500,-35500]


# Sample set 6-2
# ylocs=[-6500,-6500,-6500,-6500,-6500,-6500]
# xlocs=[-29500,-33200,-37200,-40200,-41600,-43600]
# names = ['MP-FLSAW','MP-BPSAW','DW-1','DW-2','DW-3','DW-4']


# ylocs =        [8400,8400,8400,8400,8400,8400,8400,8400,8400,8400,8400,8400,8400,8400,8400,8400,8400,8400]
# xlocs = [44000,39800,34800,31500,25800,21800,16800,13000,6800,4000,-2200,-5200,-12200,-14400,-21200,-23400,-31200,-33400]


def gisaxs_rpi_2021_3(t=1):

    samples = [
        "PR_Silica",
        "PR_Silica_Br",
        "PR_C2_2",
        "PR_C2_15",
        "PR_C18_2",
        "PR_C18_8",
    ]
    x_list = [39000, 30000, 14000, 3000, -13000, -26000]
    x_hexa = [0, 0, 0, 0, 0, 0]

    waxs_arc = [20, 0]
    angle = [0.10, 0.12, 0.15]

    # Detectors, motors:
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    assert len(x_list) == len(
        x_hexa
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(x_hexa)})"

    for x, sample, x_hex in zip(x_list, samples, x_hexa):
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(stage.x, x_hex)

        sample_id(user_name="SL", sample_name=sample)

        yield from alignement_gisaxs(0.08)
        yield from bps.mv(att1_5.open_cmd, 1)

        ai0 = piezo.th.position

        det_exposure_time(t, t)
        name_fmt = "{sample}_8.3m_14.0keV_ai{angle}deg_wa{waxs}_25C"
        for j, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)

            for i, an in enumerate(angle):
                yield from bps.mv(piezo.x, x - i * 500)
                yield from bps.mv(piezo.th, ai0 + an)
                yield from bps.sleep(1)
                sample_name = name_fmt.format(
                    sample=sample, angle="%3.2f" % an, waxs="%2.1f" % wa
                )
                sample_id(user_name="SL", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")

                yield from bp.count(dets, num=1)

        yield from bps.mv(piezo.th, ai0)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.1, 0.1)


def run_waxs_fastRPI_2021_3(t=1):

    xlocs = [39000, 19000, 3000]
    ylocs = [-6000, -6000, -6000]
    names = ["CW-mTPNI-3", "CW-mTPNI-4", "CW-mTPNI-5"]

    x_off = [-1000, 0, 1000]
    y_off = [-500, 500]

    user = "SL"
    det_exposure_time(t, t)

    # Check if the length of xlocs, ylocs and names are the same
    assert len(xlocs) == len(
        names
    ), f"Number of X coordinates ({len(xlocs)}) is different from number of samples ({len(names)})"
    assert len(xlocs) == len(
        ylocs
    ), f"Number of X coordinates ({len(xlocs)}) is different from number of samples ({len(ylocs)})"

    # Detectors, motors:
    dets = [pil1M, pil900KW]
    waxs_range = [40, 20, 0]

    for wa in waxs_range:
        yield from bps.mv(waxs, wa)
        for sam, x, y in zip(names, xlocs, ylocs):
            yield from bps.mv(piezo.x, x)
            yield from bps.mv(piezo.y, y)
            for yy, y_of in enumerate(y_off):
                yield from bps.mv(piezo.y, y + y_of)
                for xx, x_of in enumerate(x_off):
                    yield from bps.mv(piezo.x, x + x_of)
                    xxa = xx + 1
                    yya = yy + 1
                    name_fmt = "{sam}_wa{waxs}_loc{xx}{yy}"
                    sample_name = name_fmt.format(
                        sam=sam, xx="%1.1d" % xxa, yy="%1.1d" % yya, waxs="%2.1f" % wa
                    )
                    sample_id(user_name=user, sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def run_waxs_capRPI_2021_3(t=1):

    names = ["JA_S62_SP_PI_1k_2-04_-40C"]
    user = "SL"
    det_exposure_time(t, t)

    # Detectors, motors:
    dets = [pil1M, pil900KW]
    waxs_range = [40, 20, 0]

    for wa in waxs_range:
        yield from bps.mv(waxs, wa)
        name_fmt = "{sam}_wa{waxs}"
        sample_name = name_fmt.format(sam=names[0], waxs="%2.1f" % wa)
        sample_id(user_name=user, sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")
        yield from bp.count(dets, num=1)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)
    yield from bps.mv(waxs, 40)


def run_waxs_linkamRPI_2021_3(t=1):

    names = ["Air"]
    user = "JA"
    det_exposure_time(t, t)

    # Detectors, motors:
    dets = [pil1M]

    name_fmt = "{sam}"
    sample_name = name_fmt.format(sam=names[0])
    sample_id(user_name=user, sample_name=sample_name)
    print(f"\n\t=== Sample: {sample_name} ===\n")

    yield from bp.scan(dets, stage.y, 3.2, 1.9, 6)
    # yield from bp.scan(dets, stage.y, 3.27,1.97,6)

    # yield from bp.scan(dets, stage.y, 3.2,3.2,1)
    # yield from bp.scan(dets, stage.y, 2.94,2.94,1)
    # yield from bp.scan(dets, stage.y, 2.68,2.68,1)
    # yield from bp.scan(dets, stage.y, 2.42,2.42,1)
    # yield from bp.scan(dets, stage.y, 2.16,2.16,1)
    # yield from bp.scan(dets, stage.y, 1.9,1.9,1)

    # sample_id(user_name='test', sample_name='test')
    # det_exposure_time(0.3, 0.3)


def run_waxs_linkamRPI_2022_1(t=1):
    names = ["testtest"]
    time_rec = [0.1, 0.5, 1, 60]
    waxs_range = [20, 0]

    user = "SL"
    det_exposure_time(t, t)

    # Detectors, motors:
    dets = [pil1M, pil900KW]

    t0 = time.time()

    for t in time_rec:
        while (time.time() - t0) < (t * 60):
            yield from bps.sleep(10)

        for wa in waxs_range:
            yield from bps.mv(waxs, wa)
            name_fmt = "{sample}_{time}s"
            sample_name = name_fmt.format(
                sample=names[0], time="%.1f" % (time.time() - t0)
            )
            sample_id(user_name=user, sample_name=sample_name)

            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)

    sample_id(user_name=user, sample_name=sample_name)
    print(f"\n\t=== Sample: {sample_name} ===\n")

    det_exposure_time(0.3, 0.3)


def run_swaxs_fastRPI_2022_2(t=1):
    """
    Take WAXS and SAXS at six sample positions for averaging

    Specify central positions on the samples with xlocs and ylocs,
    then offsets from central positions with x_off and y_off. Run
    WAXS arc as the slowest motor.
    Hexapod y needs adjustment for the lower samples.
    """

    names = [
        "Dehyd_C1",
        "Dehyd_LMLC",
        "Dehyd_HMLC",
        "Dehyd_LMHC",
        "Dehyd_HMHC",
        "DoubleTape",
    ]
    xlocs = [-12400, -18400, -24400, -31400, -38400, -43400]
    ylocs = [-8000, -8000, -9500, -8000, -8000, -8000]
    hexa_y = [0, 0, 0, 0, 0, 0]  # either -5 (top row) or 0 (bottom row), in mm

    x_off = [-500, 500]
    y_off = [0, -500, -1000]

    waxs_arc = [40, 20, 0]

    user = "SL"
    det_exposure_time(t, t)

    # Check and correct sample names just in case
    names = [n.translate({ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ "}) for n in names]

    # Check if the length of xlocs, ylocs and names are the same
    assert len(xlocs) == len(
        names
    ), f"Number of X coordinates ({len(xlocs)}) is different from number of samples ({len(names)})"
    assert len(xlocs) == len(
        ylocs
    ), f"Number of X coordinates ({len(xlocs)}) is different from number of samples ({len(ylocs)})"
    assert len(xlocs) == len(
        hexa_y
    ), f"Number of X coordinates ({len(xlocs)}) is different from hexapod y positions ({len(hexa_y)})"

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)
        # Detectors, disable SAXS when WAXS in the way
        dets = [pil900KW] if wa < 15 else [pil900KW, pil1M]

        for name, x, y, hy in zip(names, xlocs, ylocs, hexa_y):
            yield from bps.mv(piezo.y, y)
            yield from bps.mv(piezo.x, x)
            yield from bps.mv(stage.y, hy)

            for yy, y_of in enumerate(y_off):
                yield from bps.mv(piezo.y, y + y_of)

                for xx, x_of in enumerate(x_off):
                    yield from bps.mv(piezo.x, x + x_of)

                    # xxa and yya go into the file name as sampel position
                    xxa = xx + 1
                    yya = yy + 1

                    # Metadata
                    e = energy.position.energy / 1000
                    wa = waxs.arc.position
                    wa = str(np.round(float(wa), 1)).zfill(4)
                    sdd = pil1m_pos.z.position / 1000
                    scan_id = db[-1].start["scan_id"] + 1

                    # Sample name
                    name_fmt = (
                        "{sample}_{energy}keV_wa{wax}_sdd{sdd}m_id{scan_id}_loc{xx}{yy}"
                    )
                    sample_name = name_fmt.format(
                        sample=name,
                        energy="%.2f" % e,
                        wax=wa,
                        sdd="%.1f" % sdd,
                        scan_id=scan_id,
                        xx="%1.1d" % xxa,
                        yy="%1.1d" % yya,
                    )
                    # Reference for data analysis
                    # name_fmt = '{sam}_wa{waxs}_loc{xx}{yy}'
                    # sample_name = name_fmt.format(sam=name, xx='%1.1d'%xxa, yy='%1.1d'%yya, waxs='%2.1f'%wa)

                    sample_id(user_name=user, sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def run_saxs_linkam_temp_2022_2(t=0.5, temp=25):
    """
    Single SAXS measurement

    Linkam capillary stage driven from a laptop and temperature specified manually.
    Remember to change sample name, coordinates, and scan range after changing sample.

    Params:
        t (float): detector exposure time,
        temp (flaot): temperature of the stage to pass to filename metadata.

    Inside the function:
        y_coord (float): starting position of the hexapod stage in y, units are mm,
        y_range (list of floats): disance to scan in y in mm,
        n_points (int): number of scan points along the range, include start, middle, and stop.
    """

    y_coord = 1.8
    y_range = [0, 0.5]
    n_points = 2

    name = "test"
    user = "test"

    det_exposure_time(t, t)
    dets = [pil1M]

    # Metadata
    e = energy.position.energy / 1000
    wa = waxs.arc.position + 0.001
    wa = str(np.round(float(wa), 1)).zfill(4)
    # temp = ls.input_A.get() - 273.15
    temp = str(np.round(float(temp), 1)).zfill(5)
    sdd = pil1m_pos.z.position / 1000
    scan_id = db[-1].start["scan_id"] + 1
    # bpm = xbpm3.sumX.get()

    # Sample name
    name_fmt = "{sample}_{energy}keV_{temp}degC_wa{wax}_sdd{sdd}m_id{scan_id}"
    sample_name = name_fmt.format(
        sample=name,
        energy="%.2f" % e,
        temp=temp,
        wax=wa,
        sdd="%.1f" % sdd,
        scan_id=scan_id,
    )
    print(f"\n\t=== Sample: {sample_name} ===\n")
    sample_id(user_name=user, sample_name=sample_name)

    yield from bp.rel_scan(dets, stage.y, *y_range, n_points)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def run_saxs_linkamRPI_2022_2_ps(t=1):
    """
    New script for polystryne in 2022_2 cycle in vacuum setup.

    Scan first SAXS then WAXS, just one position on the sample.
    """

    names = ["Vac_PS_3"]
    user = "SL"

    waxs_arc = [20, 0]

    det_exposure_time(t, t)

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)
        # Detectors, disable SAXS when WAXS in the way
        dets = [pil900KW] if waxs.arc.position < 15 else [pil900KW, pil1M]

        wa = str(np.round(float(wa), 1)).zfill(4)
        name_fmt = "{sam}_wa{wa}"
        sample_name = name_fmt.format(sam=names[0], wa=wa)
        sample_id(user_name=user, sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")
        yield from bp.count(dets)

        sample_id(user_name="test", sample_name="test")
        det_exposure_time(0.3, 0.3)


def run_swaxs_fastRPI_2022_3(t=1):
    """
    Take WAXS and SAXS at six sample positions for averaging

    Specify central positions on the samples with xlocs and ylocs,
    then offsets from central positions with x_off and y_off. Run
    WAXS arc as the slowest motor.
    Hexapod may need adjustment for the lower samples.
    """

    names = [ "S06_5PVPCe-6", "S05_10PVCe-5", "S04_P250-RT-4", "S03_P1000-80-3", "S02_P650-RT-2", "S01_P1000-RT-1","S00_Vacuum25C"]
    names = [ f'Oct2022_{n}' for n in names]
    xlocs = [-29000, -18000, -7000, 5000, 21000, 35000,45000]
    ylocs = [0, 0, 0, 1500, 1500, 1500,1500]
    hexa_y = [7 for n in names]  #in mm

    x_off = [-500, 500]
    y_off = [0, -500, -1000]

    waxs_arc = [40, 20, 0]

    user = "JA"
    det_exposure_time(t, t)

    # Check and correct sample names just in case
    names = [n.translate({ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ "}) for n in names]

    # Check if the length of xlocs, ylocs and names are the same
    assert len(xlocs) == len(names), f"Number of X coordinates ({len(xlocs)}) is different from number of samples ({len(names)})"
    assert len(xlocs) == len(ylocs), f"Number of X coordinates ({len(xlocs)}) is different from number of samples ({len(ylocs)})"
    assert len(xlocs) == len(hexa_y), f"Number of X coordinates ({len(xlocs)}) is different from hexapod y positions ({len(hexa_y)})"

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)
        # Detectors, disable SAXS when WAXS in the way
        dets = [pil900KW] if waxs.arc.position < 15 else [pil900KW, pil1M]

        for name, x, y, hy in zip(names, xlocs, ylocs, hexa_y):
            yield from bps.mv(piezo.y, y,
                              piezo.x, x,
                              stage.y, hy)

            for yy, y_of in enumerate(y_off):
                yield from bps.mv(piezo.y, y + y_of)

                for xx, x_of in enumerate(x_off):
                    yield from bps.mv(piezo.x, x + x_of)

                    # xxa and yya go into the file name as sample position
                    #xxa = xx + 1
                    #yya = yy + 1
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
                    # Reference for data analysis
                    # name_fmt = '{sam}_wa{waxs}_loc{xx}{yy}'
                    # sample_name = name_fmt.format(sam=name, xx='%1.1d'%xxa, yy='%1.1d'%yya, waxs='%2.1f'%wa)

                    sample_id(user_name=user, sample_name=sample_name)
                    print(f"\n\n\n\t=== Sample: {sample_name} ===")
                    yield from bp.count(dets)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def run_saxs_linkamRPI_2022_3_ps(t=1):
    """
    New script for polystryne in 2022_2 cycle in vacuum setup.

    Scan first SAXS then WAXS, just one position on the sample.
    """
    name = "Oct2022_S158_B5O3-235wt-3_100C5m-25C"
    #name = "Oct2022_S010_Air"
    user = "JA"

    # Hexapod stage, in mm
    stage_x =-6.5
    stage_y = 0

    stage_x_off = [0]
    #stage_y_off = [0]
    stage_y_off = [-0.6, -0.4, -0.2, 0, 0.2, 0.4, 0.6]

    #Only SAXS
    waxs_arc = [20]

    det_exposure_time(t, t)

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa,
                          stage.y, stage_y,
                          stage.x, stage_x
        )

        #dets = [pil900KW] if waxs.arc.position < 15 else [pil900KW, pil1M]
        dets = [pil1M]

        for yy, y_of in enumerate(stage_y_off):
            yield from bps.mv(stage.y, stage_y + y_of)

            for xx, x_of in enumerate(stage_x_off):
                yield from bps.mv(stage.x, stage_x + x_of)

                loc = xx + yy + 1

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
                    loc=int(loc)
                )
                sample_id(user_name=user, sample_name=sample_name)
                print(f"\n\n\n\n\n\t=== Sample: {sample_name} ===")
                yield from bp.count(dets)

        sample_id(user_name="test", sample_name="test")
        det_exposure_time(0.3, 0.3)
        yield from bps.mv(stage.y, stage_y,
                          stage.x, stage_x,
                          waxs, waxs_arc[0])


def run_cap_swaxs_fastRPI_2023_1(t=1):
    """
    Take WAXS and SAXS at several sample positions for averaging

    Specify central positions on the samples with xlocs and ylocs,
    then offsets from central positions with x_off and y_off. Run
    WAXS arc as the slowest motor.
    Hexapod may need adjustment for the lower samples.
    Capillary samples. SAXS at 8.3 m
    """

    names = [ 'S020_H14','S067_PS-D120','S068_PS-D168']
    names = [ f'Feb2023_{n}' for n in names]
    piezo_x = [-33000,-9600,5200]
    piezo_y = [-2300,-2400,-2600]
    hexa_y =  [0 for n in names]  #in mm

    x_off = [0]
    y_off = [-900, -600, -300, 0, 300, 600, 900]

    waxs_arc = [40, 20, 0]

    user = "JA"
    det_exposure_time(t, t)

    # Check and correct sample names just in case
    names = [n.translate({ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ "}) for n in names]

    # Check if the length of xlocs, ylocs and names are the same
    msg = "Wrong number of coordinates"
    assert len(piezo_x) == len(names), msg
    assert len(piezo_x) == len(piezo_y), msg
    assert len(piezo_x) == len(hexa_y), msg

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)
        # Detectors, disable SAXS when WAXS in the way
        dets = [pil900KW] if waxs.arc.position < 15 else [pil900KW, pil1M]

        for name, x, y, hy in zip(names, piezo_x, piezo_y, hexa_y):
            yield from bps.mv(piezo.y, y,
                              piezo.x, x,
                              stage.y, hy)

            for yy, y_of in enumerate(y_off):
                yield from bps.mv(piezo.y, y + y_of)

                for xx, x_of in enumerate(x_off):
                    yield from bps.mv(piezo.x, x + x_of)
                    
                    loc = yy + 1

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


def run_plaq_swaxs_fastRPI_2023_1(t=1):
    """
    Take WAXS and SAXS at several sample positions for averaging

    Specify central positions on the samples with xlocs and ylocs,
    then offsets from central positions with x_off and y_off.
    Hexapod may need adjustment for the upper row samples.
    """
    #names_top =   ['S074_FA6-8','S073_FA6-10','S072_FA4-4','S071_FA4-6','S070_FA4-8','S069_FA4-10']
    #piezo_x_top = [-36500,-18500,-6000,12500,26500,42000  ]
    #piezo_y_top = [-7000, -7000,-7000,-7000,-7000,-7000]
    #hexa_y_top =  [-3 for n in names_top]  #in mm
    names_top =   []
    piezo_x_top = []
    piezo_y_top = []
    hexa_y_top =  []  #in mm

    names_bot =   ['S60_S30-30','S059_S30-3','S058_S20-30','S057_S10-30','S056_S10-3','S055_S5-30','S054_HDPEN']
    piezo_x_bot = [-32000,-19500,-5500,6000,17000,29000,42000 ]
    piezo_y_bot = [7000,7000,7000,7000,7000,7000,7000]
    hexa_y_bot =  [ 0 for n in names_bot]  #in mm

    names   = names_top   + names_bot
    piezo_x = piezo_x_top + piezo_x_bot
    piezo_y = piezo_y_top + piezo_y_bot
    hexa_y  = hexa_y_top  + hexa_y_bot

    names = [ f'Feb2023_{n}' for n in names]

    x_off = [-500, 0, 500]
    y_off = [ 0, 250]

    waxs_arc = [40, 20, 0]

    user = "JA"
    det_exposure_time(t, t)

    # Check and correct sample names just in case
    names = [n.translate({ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ "}) for n in names]

    # Check if the length of xlocs, ylocs and names are the same
    msg = "Wrong number of coordinates"
    assert len(piezo_x) == len(names), msg
    assert len(piezo_x) == len(piezo_y), msg
    assert len(piezo_x) == len(hexa_y), msg

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)
        # Detectors, disable SAXS when WAXS in the way
        dets = [pil900KW] if waxs.arc.position < 15 else [pil900KW, pil1M]

        for name, x, y, hy in zip(names, piezo_x, piezo_y, hexa_y):
            yield from bps.mv(piezo.y, y,
                              piezo.x, x,
                              stage.y, hy)

            for yy, y_of in enumerate(y_off):
                yield from bps.mv(piezo.y, y + y_of)

                for xx, x_of in enumerate(x_off):
                    yield from bps.mv(piezo.x, x + x_of)
                    
                    loc = yy + 2*xx + 1

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


def run_saxs_linkamRPI_2023_1(t=1):
    """
    Scan SAXS, just one position on the sample.
    """
    name = "S120_LinkamAir"
    user = "JA"

    name = f'Feb2023_{name}'

    # Hexapod stage, in mm
    stage_x = -6.0
    stage_y = -1.1
    # x -27500 y 3000
    stage_x_off = [0]
    #stage_y_off = [1]
    stage_y_off = [0,0.2,0.4,0.6,0.8,1.0]
    #stage_y_off = [0.4]
    #Only SAXS
    waxs_arc = [20]

    det_exposure_time(t, t)

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa,
                          stage.y, stage_y,
                          stage.x, stage_x
        )

        #dets = [pil900KW] if waxs.arc.position < 15 else [pil900KW, pil1M]
        dets = [pil1M]

        for yy, y_of in enumerate(stage_y_off):
            yield from bps.mv(stage.y, stage_y + y_of)

            for xx, x_of in enumerate(stage_x_off):
                yield from bps.mv(stage.x, stage_x + x_of)

                loc = xx + yy + 1

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
                    loc=int(loc)
                )
                sample_id(user_name=user, sample_name=sample_name)
                print(f"\n\n\n\n\n\t=== Sample: {sample_name} ===")
                yield from bp.count(dets)

        sample_id(user_name="test", sample_name="test")
        det_exposure_time(0.3, 0.3)
        yield from bps.mv(stage.y, stage_y,
                          stage.x, stage_x,
                          waxs, waxs_arc[0])



def run_plaq_swaxs_fastRPI_2023_2(t=1):
    """
    Take WAXS and SAXS at several sample positions for averaging

    Specify central positions on the samples with xlocs and ylocs,
    then offsets from central positions with x_off and y_off.
    Hexapod may need adjustment for the upper row samples.
    """

    names_1 =   [ 'S041_BlankFoil','S042_B5O3-Film','S043_B5O4-Film','S044_Mix050-Film','S045_Mix100-Film','S046_Mix300-Film',
                  'S047_Mix500-Film','S048_B5O3-Melt-Kapton','S049_B5O4-Melt-Kapton','S050_Mix050-Melt-Kapton',
                  'S051_Mix100-Melt-Kapton','S052_Mix300-Melt-Kapton','S053_Mix500-Melt-Kapton'
                 ]
                  
    piezo_x_1 = [ -32350, -21350, -12350, -3350,12150, 25650, 42150,
                   -21500, -8500 ,2500,14500,25500, 36500 
                   ]
    piezo_y_1 = [  -8000, -8000, -8000, -8000, -8000, -8000, -8000,  
                    8500, 7500, 7700, 7500, 7500,7500
                    ]
    hexa_y_1 =  [ -11 for n in names_1]  #in mm

    names_2 =   []
    piezo_x_2 = []
    piezo_y_2 = []
    hexa_y_2 =  [ -11 for n in names_2]  #in mm

    names   = names_1   + names_2
    piezo_x = piezo_x_1 + piezo_x_2
    piezo_y = piezo_y_1 + piezo_y_2
    hexa_y  = hexa_y_1  + hexa_y_2

    names = [ f'May2023_{n}' for n in names]

    x_off = [-500, 0, 500]
    y_off = [ 0, 250, 500]

    waxs_arc = [40, 20, 0]

    user = "JA"
    det_exposure_time(t, t)

    # Check if the length of xlocs, ylocs and names are the same
    msg = "Wrong number of coordinates"
    assert len(piezo_x) == len(names), msg
    assert len(piezo_x) == len(piezo_y), msg
    assert len(piezo_x) == len(hexa_y), msg

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)
        dets = [pil900KW] if waxs.arc.position < 15 else [pil900KW, pil1M]

        for name, x, y, hy in zip(names, piezo_x, piezo_y, hexa_y):
            yield from bps.mv(piezo.y, y,
                              piezo.x, x,
                              stage.y, hy)
            
            for yy, y_of in enumerate(y_off):
                yield from bps.mv(piezo.y, y + y_of)

                for xx, x_of in enumerate(x_off):
                    yield from bps.mv(piezo.x, x + x_of)
                    
                    loc = yy + 2*xx + 1
                    sample_name = f'{name}{get_scan_md()}_loc{loc}'
                    sample_id(user_name=user, sample_name=sample_name)
                    print(f"\n\n\n\t=== Sample: {sample_name} ===")
                    yield from bp.count(dets)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def run_saxs_linkamRPI_2023_2(t=1):
    """
    Scan SAXS, just one position on the sample.
    """
    name = "S275_B5O3-23wt_96C3m-82C-87C-3timeRipening-82C3m-25C"
    user = "JA"

    name = f'May2023_{name}'

    # Hexapod stage, in mm
    stage_x = -5.75
    stage_y = 0.35
    # x -27500 y 3000
    stage_x_off = [0.15] # =-0.25
    
    stage_y_off = [0.05,0.25,0.45,0.65,0.85,1.05]
    #stage_y_off = [1.05]


    waxs_arc = [20]

    dets = [pil1M]
    det_exposure_time(t, t)

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa,
                          stage.y, stage_y,
                          stage.x, stage_x
        )
        

        for yy, y_of in enumerate(stage_y_off):
            yield from bps.mv(stage.y, stage_y + y_of)

            for xx, x_of in enumerate(stage_x_off):
                yield from bps.mv(stage.x, stage_x + x_of)

                loc = xx + yy + 1

                sample_name = f'{name}{get_scan_md()}_loc{loc}'
                sample_id(user_name=user, sample_name=sample_name)
                print(f"\n\n\n\t=== Sample: {sample_name} ===")
                yield from bp.count(dets)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)
    yield from bps.mv(stage.y, stage_y,
                      stage.x, stage_x,
                      waxs, waxs_arc[0])

def run_plaq_swaxs_fastRPI_2023_3(t=1):
    """
    Take WAXS and SAXS at several sample positions for averaging

    Specify central positions on the samples with xlocs and ylocs,
    then offsets from central positions with x_off and y_off.
    Hexapod may need adjustment for the upper row samples.
    """

    names_1 =   ['S016_1A', 'S017_1C', 'S018_1D', 'S019_2A', 'S020_2B', 'S021_2C', 'S022_3A', 'S023_3B', 'S024_3C', 'S025_3D', 'S026_4A',
                 'S027_4B', 'S028_4C', 'S029_5A', 'S030_5C', 'S031_5D', 'S032_5E', 'S033_6A', 'S034_6C', 'S035_6D', 'S036_6E']
                       
    piezo_x_1 = [-38550, -36150, -34150, -26550, -24350, -21350, -11550, -9450, -7450, -4950, 2550, 4650, 7150, 19450, 21350, 23350, 26250, 37950, 40950, 43550, 46150]         
    piezo_y_1 = [  7400,   7400,   7400,   7400,   7400,   7400,   7400,  7400,  7400,  7400, 7400, 7400, 7400,  7100,  6900,  6900,  6900,  6500,  6500,  6500,  6500]
    #hexa_y_1 =  [ -5 for n in names_1]  #in mm
    hexa_y_1 =  [ 5 for n in names_1]
    names_2 =   []
    piezo_x_2 = []
    piezo_y_2 = []
    hexa_y_2 =  [ -11 for n in names_2]  #in mm

    names   = names_1   + names_2
    piezo_x = piezo_x_1 + piezo_x_2
    piezo_y = piezo_y_1 + piezo_y_2
    hexa_y  = hexa_y_1  + hexa_y_2

    names = [ f'Sep2023_{n}' for n in names]

    x_off = [0]
    y_off = [ 0, -1000, -2000, -3000]
        
    waxs_arc = [20, 40, 0]
    
    user = "JA"
    det_exposure_time(t, t)

    # Check if the length of xlocs, ylocs and names are the same
    msg = "Wrong number of coordinates"
    assert len(piezo_x) == len(names), msg
    assert len(piezo_x) == len(piezo_y), msg
    assert len(piezo_x) == len(hexa_y), msg

    # Make sure cam server engages with the detector
    sample_id(user_name='test', sample_name='test')
    yield from bp.count([pil900KW])

    y_add = 0
    
    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)
        dets = [pil900KW] if waxs.arc.position < 15 else [pil900KW, pil1M]
        
        y_add=300*wa/20
        
        for name, x, y, hy in zip(names, piezo_x, piezo_y, hexa_y):
            yield from bps.mv(piezo.y, y,
                              piezo.x, x,
                              stage.y, hy)
            
            for yy, y_of in enumerate(y_off):
                yield from bps.mv(piezo.y, y + y_of+y_add)

                for xx, x_of in enumerate(x_off):
                    yield from bps.mv(piezo.x, x + x_of)
                    
                    loc = yy + 2*xx + 1
                    sample_name = f'{name}{get_scan_md()}_loc{loc}'
                    sample_id(user_name=user, sample_name=sample_name)
                    print(f"\n\n\n\t=== Sample: {sample_name} ===")
                    yield from bp.count(dets)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)

def run_saxs_linkamRPI_2023_3(t=1):
    """
    Scan SAXS, just one position on the sample.
    """
    name = "S251_B5O4nB5O3-r1wt-15.5wt-2_77C-25C"
    #name = "S037_4"
    user = "JA"

    name = f'Sep2023_{name}'

    # Hexapod stage, in mm
    stage_x = -6
    stage_y = -0.6
    # x -27500 y 3000
    stage_x_off = [0] # =-0.25
    
    
    stage_y_off = [0,0.270,0.54,0.81,1.08,1.35]
    #stage_y_off = [0.81]


    waxs_arc = [20]

    dets = [pil1M]
    det_exposure_time(t, t)

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa,
                          stage.y, stage_y,
                          stage.x, stage_x
        )
        

        for yy, y_of in enumerate(stage_y_off):
            yield from bps.mv(stage.y, stage_y + y_of)

            for xx, x_of in enumerate(stage_x_off):
                yield from bps.mv(stage.x, stage_x + x_of)

                loc = xx + yy + 1

                sample_name = f'{name}{get_scan_md()}_loc{loc}'
                sample_id(user_name=user, sample_name=sample_name)
                print(f"\n\n\n\t=== Sample: {sample_name} ===")
                yield from bp.count(dets)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)
    yield from bps.mv(stage.y, stage_y,
                      stage.x, stage_x,
                      waxs, waxs_arc[0])


def run_plaq_swaxs_fastRPI_2024_1(t=1):
    """
    Take WAXS and SAXS at sev0eral sample positions for averaging

    Specify central positions on the samples with xlocs and ylocs,
    then offsets from central positions with x_off and y_off.
    Hexapod may need adjustment for the upper row samples.
    """

    names_1 = ['S046_EPON828_RE','S047_EPON862_RE','S048_D230_RE']
   
    
   
                   
    piezo_x_1 = [25200,27000,28800]         
    piezo_y_1 = [3500,3500,3500]
    #hexa_y_1 =  [ -5 for n in names_1]  #in mm
    hexa_y_1 =  [ 3 for n in names_1]
    names_2 =   []
    piezo_x_2 = []
    piezo_y_2 = []
    hexa_y_2 =  []  #in mm

    names   = names_1   + names_2
    piezo_x = piezo_x_1 + piezo_x_2
    piezo_y = piezo_y_1 + piezo_y_2
    hexa_y  = hexa_y_1  + hexa_y_2

    names = [ f'Jan2024_{n}' for n in names]

    x_off = [ 0]
    y_off = [ -750,-450,-150,150,450,750]  
        
    waxs_arc = [20, 40, 0]
    


    user = "JA"
    det_exposure_time(t, t)

    # Check if the length of xlocs, ylocs and names are the same
    msg = "Wrong number of coordinates"
    assert len(piezo_x) == len(names), msg
    assert len(piezo_x) == len(piezo_y), msg
    assert len(piezo_x) == len(hexa_y), msg

    # Make sure cam server engages with the detector
    sample_id(user_name='test', sample_name='test')
    yield from bp.count([pil900KW])

    y_add = 0
    
    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)
        dets = [pil900KW] if waxs.arc.position < 15 else [pil900KW, pil1M]
        
        y_add=300*wa/20
        
        for name, x, y, hy in zip(names, piezo_x, piezo_y, hexa_y):
            yield from bps.mv(piezo.y, y,
                              piezo.x, x,
                              stage.y, hy)
            
            for yy, y_of in enumerate(y_off):
                yield from bps.mv(piezo.y, y + y_of+y_add)

                for xx, x_of in enumerate(x_off):
                    yield from bps.mv(piezo.x, x + x_of)
                    
                    loc = f'{yy}{xx}'
                    sample_name = f'{name}{get_scan_md()}_loc{loc}'
                    sample_id(user_name=user, sample_name=sample_name)
                    print(f"\n\n\n\t=== Sample: {sample_name} ===")
                    yield from bp.count(dets)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)

def run_saxs_linkamRPI_2024_1(t=1):
    """
    Scan SAXS, just one position on the sample.
    """
    name = "S203_B5OM63-molr1-12wt-2_Full-35C"
    #name = "S066_Air-WaterBlank_25C"    
    #name = "TEST-air_25C"
    user = "JA"
    name = f'Jan2024_{name}'
  
    # Hexapod stage, in mm
    stage_x = -7.8 # -7.6
    stage_y = -3.1
    
    # x -27500 y 3000


    stage_x_off = [0,0.2] # =+0.20
    stage_y_off = [0,0.27,0.54,0.81,1.08]
    
    #stage_x_off = [0.2]
    #stage_y_off = [0.81]


    waxs_arc = [20]

    dets = [pil1M]
    det_exposure_time(t, t)

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa,
                          stage.y, stage_y,
                          stage.x, stage_x
        )
        

        for yy, y_of in enumerate(stage_y_off):
            yield from bps.mv(stage.y, stage_y + y_of)

            for xx, x_of in enumerate(stage_x_off):
                yield from bps.mv(stage.x, stage_x + x_of)

                loc = f'{yy}{xx}'

                sample_name = f'{name}{get_scan_md()}_loc{loc}'
                sample_id(user_name=user, sample_name=sample_name)
                print(f"\n\n\n\t=== Sample: {sample_name} ===")
                yield from bp.count(dets)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)
    yield from bps.mv(stage.y, stage_y,
                      stage.x, stage_x,
                      waxs, waxs_arc[0])


def run_plaq_swaxs_fastRPI_2024_2(t=1):
    """
    Take WAXS and SAXS at sev0eral sample positions for averaging

    Specify central positions on the samples with xlocs and ylocs,
    then offsets from central positions with x_off and y_off.
    Hexapod may need adjustment for the upper row samples.
    """

    names_1 = ['S018_BlankCap_25C-Vac','S019_FormFactor-B5O3-1wt_25C-Vac','S020_FormFactor-B2O1-Alkyl-1wt-RE_25C-Vac']
   
    piezo_x_1 = [-41900,-35500,-29350]         
    piezo_y_1 = [-7000,-7000,-7000]
    #hexa_y_1 =  [ -5 for n in names_1]  #in mm
    hexa_y_1 =  [ 0 for n in names_1]
    names_2 =   []
    piezo_x_2 = []
    piezo_y_2 = []
    hexa_y_2 =  []  #in mm

    names   = names_1   + names_2
    piezo_x = piezo_x_1 + piezo_x_2
    piezo_y = piezo_y_1 + piezo_y_2
    hexa_y  = hexa_y_1  + hexa_y_2

    names = [ f'May2024_{n}' for n in names]

    x_off = [ 0]
    y_off = [0, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500,
             5000, 5500, 6000, 6500, 7000, 7500, 8000, 8500, 9000, 9500]  
        
    waxs_arc = [20, 40, 0]
    


    user = "JA"
    det_exposure_time(t, t)

    # Check if the length of xlocs, ylocs and names are the same
    msg = "Wrong number of coordinates"
    assert len(piezo_x) == len(names), msg
    assert len(piezo_x) == len(piezo_y), msg
    assert len(piezo_x) == len(hexa_y), msg

    y_add = 0
    
    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)
        dets = [pil900KW] if waxs.arc.position < 15 else [pil900KW, pil1M]
        
        y_add = 300 * wa / 20
        
        for name, x, y, hy in zip(names, piezo_x, piezo_y, hexa_y):
            yield from bps.mv(piezo.y, y,
                              piezo.x, x,
                              stage.y, hy)
            
            for yy, y_of in enumerate(y_off):
                yield from bps.mv(piezo.y, y + y_of + y_add)

                for xx, x_of in enumerate(x_off):
                    yield from bps.mv(piezo.x, x + x_of)
                    
                    loc = f'{yy}{xx}'
                    sample_name = f'{name}{get_scan_md()}_loc{loc}'
                    sample_id(user_name=user, sample_name=sample_name)
                    print(f"\n\n\n\t=== Sample: {sample_name} ===")
                    yield from bp.count(dets)
        y_off = y_off[::-1]
            
    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def run_saxs_linkamRPI_2024_2(t=1, waxs_data=False):
    """
    Scan SAXS, just one position on the sample.
    """
    name = "S310_XO59k-NC6-14wt-1_72C-25C"
    # name = "S065_XO11k-NC6-Melt_120C"
    # name = "S021_B5O3-Melt_25C-Air"

    user = "JA"
    name = f'May2024_{name}'
  
    # Hexapod stage, in mm
    stage_x = -3.1 # -7.6
    stage_y = -2.25

    #stage_y = -0.5
    stage_x_off = [0, 0.2] # =+0.20
    stage_y_off = [0, 0.27, 0.54, 0.81, 1.08]
    #stage_x_off = [0.1]
    #stage_y_off = [0]

    waxs_arc = [20] if not waxs_data else [20, 40, 0]
  

    det_exposure_time(t, t)

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa,
                          stage.y, stage_y,
                          stage.x, stage_x
        )
        
        if waxs_data:
            dets = [pil900KW] if waxs.arc.position < 15 else [pil900KW, pil1M]
        else:
            dets = [pil1M]

        for yy, y_of in enumerate(stage_y_off):
            yield from bps.mv(stage.y, stage_y + y_of)

            for xx, x_of in enumerate(stage_x_off):
                yield from bps.mv(stage.x, stage_x + x_of)

                loc = f'{yy}{xx}'

                sample_name = f'{name}{get_scan_md()}_loc{loc}'
                sample_id(user_name=user, sample_name=sample_name)
                print(f"\n\n\n\t=== Sample: {sample_name} ===")
                yield from bp.count(dets)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)
    yield from bps.mv(stage.y, stage_y,
                      stage.x, stage_x,
                      waxs, waxs_arc[0])


### 2024-3 ###
# 'SAXS_setup': {'sdd': 8300, 'beam_centre': [457.5, 576], 'bs': 'rod', 'energy': 14000}
# SAXS 3mm rod bs x : 1.65

# 'SAXS_setup': {'sdd': 8300, 'beam_centre': [457.5, 576], 'bs': 'rod', 'energy': 14000}
# SAXS 3mm rod bs x : 1.95

# Beam centre in the module
# RE.md['SAXS_setup'] =  {'sdd': 3000, 'beam_centre': [490, 579], 'bs': 'rod', 'energy': 14000}

def run_saxs_linkamRPI_2024_3(t=1, waxs_data=False):
    """
    Scan SAXS, just one position on the sample.
    """
    name = "S072_Cap-B5O3-Processed-120C-made-in-May2024_80C10min-from25C-from50C"
    # name = "S065_XO11k-NC6-Melt_120C"
    # name = "S021_B5O3-Melt_25C-Air"

    user = "JA"
    name = f'Sep2024_{name}'
  
    # Hexapod stage, in mm
    stage_x = -3.0 # -7.6
    stage_y = -2.0

    #stage_y = -0.5
    #stage_x_off = [0, 0.2] # =+0.20
    #stage_y_off = [0, 0.27, 0.54, 0.81, 1.08]
    stage_x_off = [0]
    stage_y_off = [0.27]

    waxs_arc = [20] if not waxs_data else [20, 40, 0]
  

    det_exposure_time(t, t)

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa,
                          stage.y, stage_y,
                          stage.x, stage_x
        )
        
        if waxs_data:
            dets = [pil900KW] if waxs.arc.position < 15 else [pil900KW, pil1M]
        else:
            dets = [pil1M]

        for yy, y_of in enumerate(stage_y_off):
            yield from bps.mv(stage.y, stage_y + y_of)

            for xx, x_of in enumerate(stage_x_off):
                yield from bps.mv(stage.x, stage_x + x_of)

                loc = f'{yy}{xx}'

                sample_name = f'{name}{get_scan_md()}_loc{loc}'
                sample_id(user_name=user, sample_name=sample_name)
                print(f"\n\n\n\t=== Sample: {sample_name} ===")
                yield from bp.count(dets)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)
    yield from bps.mv(stage.y, stage_y,
                      stage.x, stage_x,
                      waxs, waxs_arc[0])


def run_plaq_swaxs_fastRPI_2024_3(t=1):
    """
    Take WAXS and SAXS at sev0eral sample positions for averaging

    Specify central positions on the samples with xlocs and ylocs,
    then offsets from central positions with x_off and y_off.
    Hexapod may need adjustment for the upper row samples.
    """

    names_1 = ['S090_m1n8-TPO-0.2PC-0.8TC_Vac-25C','S089_m1n8-TPO-0.15PC-0.85TC_Vac-25C','S088_m1n8-TPO-0.1PC-0.9TC_Vac-25C',
               'S087_m1n0-TPO-0.2PC-0.8TC_Vac-25C','S086_m1n0-TPO-0.15PC-0.85TC_Vac-25C','S085_m1n0-TPO-0.1PC-0.9TC_Vac-25C',
               'S084_m2n8-TPO-0.2PC-0.8TC_Vac-25C','S083_m2n8-TPO-0.15PC-0.85TC_Vac-25C','S082_m2n8-TPO-0.1PC-0.9TC_Vac-25C',
               'S081_m2n4-TPO-0.2PC-0.8TC_Vac-25C','S080_m2n4-TPO-0.15PC-0.85TC_Vac-25C','S079_m2n4-TPO-0.1PC-0.9TC_Vac-25C',
               'S078_m2n2-TPO-0.2PC-0.8TC_Vac-25C','S077_m2n2-TPO-0.15PC-0.85TC_Vac-25C','S076_m2n2-TPO-0.1PC-0.9TC_Vac-25C',
               'S075_m1n0-TPO-0.2PC-0.8TC_Vac-25C','S074_m1n0-TPO-0.15PC-0.85TC_Vac-25C','S073_m1n0-TPO-0.1PC-0.9TC_Vac-25C',
               'S091_S95TMPTA-5GMA-DMPA_Vac-25C',  'S092_S95TMPTA-5GMA-TPO_Vac-25C',     'S093_m2n0-DMPA-0.1PC-0.9TC_Vac-25C',
               'S094_m2n0-DMPA-0.15PC-0.85TC_Vac-25C','S095_m2n8-DMPA-0.1PC-0.9TC_Vac-25C','S096_m2n8-DMPA-0.15PC-0.85TC_Vac-25C',
               'S097_E828-D230-TPO-0.1PC-0.9TC_Vac-25C','S098_E828-D230-TPO-0.15PC-0.85TC_Vac-25C','S099_E828-D230-TPO-0.2PC-0.8TC_Vac-25C',
               'S100_E828-D230-TPO-0.3PC-0.7TC_Vac-25C','S101_E828-D230-TPO-0.4PC-0.6TC_Vac-25C','S102_E828-DMPA-0.2PC-0.8TC_Vac-25C',
               'S103_DMPA_Vac-25C','S104_GMA_Vac-25C','S105_TMPTA_Vac-25C','S106_TPO_Vac-25C','S107_Cap_Vac-25C','S108_Empty_Vac-25C']
   
    piezo_x_1 = [-16000,-11500, -7500, -3500,   500,  4200,  8500, 12500, 16500, 20500, 24500, 28500, 31900, 36700, 40700, 44700, 48700, 52500,
                  47500, 44100, 40100, 36500, 32200, 28200, 24200, 20200, 16500, 12500,  8500,  4500,-22600,-25700,-31500,-35500,-37100,-33300]         
    piezo_y_1 = [-10500,-10500,-10500,-10500,-10500,-10500,-10500,-10500,-10500,-10500,-10500,-10500,-10500,-10500,-10500,-10500,-10500,-10500,
                   6500,  6500,  6500,  6500,  6500,  6500,  6500,  6500,  6800,  6800,  6800,  6800,  6800,  6800,  6800,  6800,  6800,  6800]
    #hexa_y_1 =  [ -5 for n in names_1]  #in mm
    hexa_y_1 =  [ -10 for n in names_1]
    names_2 =   []
    piezo_x_2 = []
    piezo_y_2 = []
    hexa_y_2 =  []  #in mm

    names   = names_1   + names_2
    piezo_x = piezo_x_1 + piezo_x_2
    piezo_y = piezo_y_1 + piezo_y_2
    hexa_y  = hexa_y_1  + hexa_y_2

    names = [ f'Sep2024_{n}' for n in names]

    x_off = [0]
    y_off = [0, 500, 1000, 1500, 2000, 2500, 3000]  
        
    waxs_arc = [20, 40, 0]
    


    user = "JA"
    det_exposure_time(t, t)

    # Check if the length of xlocs, ylocs and names are the same
    msg = "Wrong number of coordinates"
    assert len(piezo_x) == len(names), msg
    assert len(piezo_x) == len(piezo_y), msg
    assert len(piezo_x) == len(hexa_y), msg

    y_add = 0
    
    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)
        dets = [pil900KW] if waxs.arc.position < 15 else [pil900KW, pil1M]
        
        y_add = 300 * wa / 20
        
        for name, x, y, hy in zip(names, piezo_x, piezo_y, hexa_y):
            yield from bps.mv(piezo.y, y,
                              piezo.x, x,
                              stage.y, hy)
            
            for yy, y_of in enumerate(y_off):
                yield from bps.mv(piezo.y, y + y_of + y_add)

                for xx, x_of in enumerate(x_off):
                    yield from bps.mv(piezo.x, x + x_of)
                    
                    loc = f'{yy}{xx}'
                    sample_name = f'{name}{get_scan_md()}_loc{loc}'
                    sample_id(user_name=user, sample_name=sample_name)
                    print(f"\n\n\n\t=== Sample: {sample_name} ===")
                    yield from bp.count(dets)
        y_off = y_off[::-1]
            
    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def run_saxs_linkamRPI_2024_3_Vac(t=1, waxs_data=False):
    """
    Scan SAXS, just one position on the sample.
    """
    name = "S125_FormFactor-B5O3-59k-2-1wt_5C-Vac"
    #name = "S123_Empty-No-Capillary_5C-Vac"
    # name = "S021_B5O3-Melt_25C-Air"

    user = "JA"
    name = f'Sep2024_{name}'
  
    # Hexapod stage, in mm
    stage_x = -3.4 # -7.6
    stage_y = -2.1

    #stage_y = -0.5
    #stage_x_off = [0, 0.2] # =+0.20
    stage_y_off = [0, 0.27, 0.54, 0.81, 1.08]
    stage_x_off = [0]
    #stage_y_off = [1.08]

    waxs_arc = [30] if not waxs_data else [30, 40, 0]
  

    det_exposure_time(t, t)

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa,
                          stage.y, stage_y,
                          stage.x, stage_x
        )
        
        if waxs_data:
            dets = [pil900KW] if waxs.arc.position < 15 else [pil900KW, pil1M]
        else:
            dets = [pil1M]

        for yy, y_of in enumerate(stage_y_off):
            yield from bps.mv(stage.y, stage_y + y_of)

            for xx, x_of in enumerate(stage_x_off):
                yield from bps.mv(stage.x, stage_x + x_of)

                loc = f'{yy}{xx}'

                sample_name = f'{name}{get_scan_md()}_loc{loc}'
                sample_id(user_name=user, sample_name=sample_name)
                print(f"\n\n\n\t=== Sample: {sample_name} ===")
                yield from bp.count(dets)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)
    yield from bps.mv(stage.y, stage_y,
                      stage.x, stage_x,
                      waxs, waxs_arc[0])
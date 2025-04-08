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


def NEXAFS_Fe_edge(t=0.5, name="sample1"):
    dets = [pil300KW]
    # name = 'Kapton_NEXAFS_1_gvopen_wa70_'
    # x = [8800]

    energies = np.linspace(7100, 7150, 51)

    # for name, x in zip(names, x):
    # bps.mv(piezo.x, x)
    det_exposure_time(t, t)
    name_fmt = "{sample}_{energy}eV_xbpm{xbpm}"
    for e in energies:
        yield from bps.mv(energy, e)
        sample_name = name_fmt.format(
            sample=name, energy=e, xbpm="%3.1f" % xbpm3.sumY.value
        )
        sample_id(user_name="SR", sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")
        yield from bp.count(dets, num=1)

    yield from bps.mv(energy, 7100)
    # name_fmt = '{sample}_2430eV_postmeas_xbpm{xbpm}'
    # sample_name = name_fmt.format(sample=name, xbpm = '%3.1f'%xbpm3.sumY.value)
    # sample_id(user_name='GF', sample_name=sample_name)
    # print(f'\n\t=== Sample: {sample_name} ===\n')
    # yield from bp.count(dets, num=1)


def SAXS_Fe_edge(t=0.5):
    dets = [pil1M]
    names = [
        "Ca10_2_SAXS_sdd5_1s_redo_",
        "Ca2_2_SAXS_sdd5_1s_redo_",
        "Ca2_4_SAXS_sdd5_1s_redo_",
        "PBS_2_SAXS_sdd5_1s_redo_",
    ]
    names1 = [
        "Ca10_2_NEXAFS_wa0_redo_",
        "Ca2_2_NEXAFS_wa0_redo_",
        "Ca2_4_NEXAFS_wa0_redo_",
        "PBS_2_NEXAFS_wa0_redo_",
    ]

    xs = [-36600, -10600, 15400, 41100]
    ys = [-1050, -1050, -1050, -1050]
    energies = [7100, 7110, 7114, 7115, 7118, 7120, 7125, 7140]

    for i, (name, name1, x, y) in enumerate(zip(names, names1, xs, ys)):
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(piezo.y, y)

        yield from NEXAFS_Fe_edge(t=1, name=name1)
        dets = [pil1M]

        det_exposure_time(t, t)
        xsss = [x + 400, x + 900, x + 1200]
        for j, xss in enumerate(xsss):
            yield from bps.mv(piezo.x, xss)
            for e in energies:
                name_fmt = "{sample}_pos{pos}_{energy}eV_xbpm{xbpm}"

                yield from bps.mv(energy, e)
                sample_name = name_fmt.format(
                    sample=name,
                    pos="%2.2d" % j,
                    energy=e,
                    xbpm="%3.1f" % xbpm3.sumY.value,
                )
                sample_id(user_name="SR", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 7100)
            name_fmt = "{sample}_pos{pos}_7100eV_postmeas_xbpm{xbpm}"
            sample_name = name_fmt.format(
                sample=name, pos="%2.2d" % j, xbpm="%3.1f" % xbpm3.sumY.value
            )
            sample_id(user_name="GF", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)


def NEXAFS_Ag_edge(t=0.5):
    dets = [pil300KW]
    name = "N2_redo_GINEXAFS_wa75_"
    # x = [8800]

    energies = np.linspace(3340, 3390, 51)

    # for name, x in zip(names, x):
    # bps.mv(piezo.x, x)
    det_exposure_time(t, t)
    name_fmt = "{sample}_{energy}eV_xbpm{xbpm}"
    for e in energies:
        yield from bps.mv(energy, e)
        sample_name = name_fmt.format(
            sample=name, energy=e, xbpm="%3.1f" % xbpm3.sumY.value
        )
        sample_id(user_name="SR", sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")
        yield from bp.count(dets, num=1)
        yield from bps.sleep(2)

    yield from bps.mv(energy, 3340)
    yield from bps.sleep(10)


def GISAXS_Ca_edge(t=0.5):
    dets = [pil300KW]
    names = [
        "O_9_gisaxs",
        "O_8_gisaxs",
        "O_7_gisaxs",
        "O_6_gisaxs",
        "O_5_gisaxs",
        "O_4_gisaxs",
        "O_3_gisaxs",
        "O_2_gisaxs",
        "O_1_gisaxs",
        "Si_last_gisaxs",
    ]
    xs = [-50000, -38500, -22500, -11500, 500, 15000, 27000, 41000, 50000, 31400]
    zs = [700, 0, -800, 400, 1900, -2000, -1000, 300, -600, -800]

    energies = [4030, 4050, 4055, 4075]
    det_exposure_time(t, t)

    name_fmt = "{sample}_{energy}eV_ai{ai}_xbpm{xbpm}_wa{wa}"
    angles = [0.38, 0.4]
    wax = [0, 6.5, 13]

    th_0 = piezo.th.position
    for x, z, name in zip(xs, zs, names):
        yield from bps.mv(piezo.th, th_0)

        yield from bps.mv(piezo.x, x)
        yield from bps.mv(piezo.z, z)

        yield from bps.mv(GV7.open_cmd, 1)
        yield from bps.sleep(5)

        yield from bps.mv(GV7.open_cmd, 1)
        yield from alignement_gisaxs(0.3)
        yield from bps.mv(att2_11, "Insert")

        yield from bps.mv(GV7.close_cmd, 1)
        yield from bps.sleep(5)
        yield from bps.mv(att2_11, "Insert")

        yield from bps.mv(GV7.close_cmd, 1)

        th_0 = piezo.th.position
        for wa in wax:
            yield from bps.mv(waxs, wa)
            for k, e in enumerate(energies):
                yield from bps.mv(energy, e)
                for alpha_i in angles:
                    yield from bps.mv(piezo.th, th_0 + alpha_i)
                    sample_name = name_fmt.format(
                        sample=name,
                        energy=e,
                        ai="%3.2f" % alpha_i,
                        xbpm="%3.1f" % xbpm3.sumY.value,
                        wa="%2.1f" % wa,
                    )
                    sample_id(user_name="SR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 4050)
            yield from bps.mv(energy, 4030)


def SAXS_Ca_edge_hyd(t=0.5):
    dets = [pil1M]
    name = "hyd_cell_blank"

    energies = [4030, 4050, 4055, 4075]
    det_exposure_time(t, t)
    name_fmt = "{sample}_{energy}eV_xbpm{xbpm}_sp{sp}"
    x_pos = piezo.x.position
    y_pos = piezo.y.position

    for k, e in enumerate(energies):
        yield from bps.mv(energy, e)
        yield from bps.mv(piezo.x, x_pos + k * 500)

        for i in range(0, 5, 1):
            yield from bps.mv(piezo.y, y_pos + i * 200)

            sample_name = name_fmt.format(
                sample=name, energy=e, sp="%2.2d" % i, xbpm="%3.1f" % xbpm3.sumY.value
            )
            sample_id(user_name="JDM", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)

        yield from bps.mv(piezo.y, y_pos)

    yield from bps.mv(energy, 4050)
    yield from bps.mv(energy, 4030)


def SAXS_Ca_edge_hyd_onespot(t=0.5):
    dets = [pil1M]
    name = "hyd_cell_blank_onespot2"

    energies = [4030, 4040, 4050, 4055, 4075]
    det_exposure_time(t, t)
    name_fmt = "{sample}_{energy}eV_xbpm{xbpm}_sp{sp}"
    y_pos = piezo.y.position

    for k, e in enumerate(energies):
        yield from bps.mv(energy, e)

        for i in range(0, 5, 1):
            yield from bps.mv(piezo.y, y_pos + i * 200)

            sample_name = name_fmt.format(
                sample=name, energy=e, sp="%2.2d" % i, xbpm="%3.1f" % xbpm3.sumY.value
            )
            sample_id(user_name="JDM", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)

        yield from bps.mv(piezo.y, y_pos)

    yield from bps.mv(energy, 4050)
    yield from bps.mv(energy, 4030)


def SAXS_Ca_edge_dry1(t=1):
    dets = [pil300KW, pil1M]
    name = "hyd_cell_blank2"

    energies = [4030, 4040, 4050, 4055, 4075]
    det_exposure_time(t, t)
    name_fmt = "{sample}_{energy}eV_xbpm{xbpm}_wa{wa}"
    wa = [0.0, 6.5, 13.0]

    yield from bps.mv(GV7.close_cmd, 1)
    yield from bps.sleep(1)
    yield from bps.mv(GV7.close_cmd, 1)

    for wax in wa:
        yield from bps.mv(waxs, wax)
        for k, e in enumerate(energies):
            yield from bps.mv(energy, e)
            sample_name = name_fmt.format(
                sample=name, energy=e, xbpm="%3.1f" % xbpm3.sumY.value, wa="%2.1f" % wax
            )
            sample_id(user_name="JDM", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)

        yield from bps.mv(energy, 4050)
        yield from bps.mv(energy, 4030)

    for wax in wa[::-1]:
        yield from bps.mv(waxs, wax)

        name_fmt = "{sample}_4030eV_postmeas_xbpm{xbpm}_wa{wa}"
        sample_name = name_fmt.format(
            sample=name, xbpm="%3.1f" % xbpm3.sumY.value, wa="%2.1f" % wax
        )
        sample_id(user_name="OS", sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")
        yield from bp.count(dets, num=1)

    sample_id(user_name="test", sample_name="test")


def SAXS_Ca_edge_dry_special1(t=1):
    dets = [pil300KW]
    names = ["O5_chl_4"]
    x_s = [-44500]
    y_s = [-1200]

    energies = [4030, 4040, 4050, 4055, 4075]
    det_exposure_time(t, t)
    name_fmt = "{sample}_{energy}eV_pos{posi}_wa{wa}_xbpm{xbpm}"
    wa = [0.0, 6.5, 13.0]

    yield from bps.mv(GV7.close_cmd, 1)
    yield from bps.sleep(1)
    yield from bps.mv(GV7.close_cmd, 1)

    for x, y, name in zip(x_s, y_s, names):
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(piezo.y, y)
        ys = np.linspace(y, y + 250, 5)
        xs = np.linspace(x, x - 400, 3)

        yss, xss = np.meshgrid(ys, xs)
        yss = yss.ravel()
        xss = xss.ravel()

        for pos, (xsss, ysss) in enumerate(zip(xss, yss)):
            yield from bps.mv(piezo.x, xsss)
            yield from bps.mv(piezo.y, ysss)
            name_new = name + "pos%2.2d" % pos
            yield from NEXAFS_Ca_edge_special(t=0.5, name=name_new)

        for wax in wa:
            yield from bps.mv(waxs, wax)

            for k, e in enumerate(energies):
                yield from bps.mv(energy, e)

                for pos, (xsss, ysss) in enumerate(zip(xss, yss)):
                    yield from bps.mv(piezo.x, xsss)
                    yield from bps.mv(piezo.y, ysss)

                    sample_name = name_fmt.format(
                        sample=name,
                        energy=e,
                        posi="%2.2d" % pos,
                        wa="%2.1f" % wax,
                        xbpm="%3.1f" % xbpm3.sumY.value,
                    )
                    sample_id(user_name="JDM", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)

                yield from bps.mv(energy, 4050)
                yield from bps.mv(energy, 4030)

        for wax in wa[::-1]:
            yield from bps.mv(waxs, wax)

            for pos, (xsss, ysss) in enumerate(zip(xss, yss)):
                yield from bps.mv(piezo.x, xsss)
                yield from bps.mv(piezo.y, ysss)

                name_fmt = "{sample}_postmeas_4030eV_pos{posi}_wa{wa}_xbpm{xbpm}"
                sample_name = name_fmt.format(
                    sample=name,
                    posi="%2.2d" % pos,
                    wa="%2.1f" % wax,
                    xbpm="%3.1f" % xbpm3.sumY.value,
                )
                sample_id(user_name="JDM", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

    sample_id(user_name="test", sample_name="test")


def SAXS_Ca_edge_dry_special2(t=1):
    dets = [pil300KW, pil1M]
    names = [
        "O5_ut_2",
        "O5_ut_3",
        "O5_ut_4",
        "O5_ca_1",
        "O5_ca_2",
        "O5_ca_3",
        "O5_chl_1",
        "O5_chl_2",
        "O5_chl_3",
    ]
    x_s = [31500, 25000, 18000, 5400, 100, -5400, -22600, -30600, -38600]
    y_s = [-2200, -1400, -2000, -2000, -2000, -2000, -800, -2000, -2000]

    energies = [4030, 4040, 4050, 4055, 4075]
    det_exposure_time(t, t)
    name_fmt = "{sample}_{energy}eV_pos{posi}_wa{wa}_xbpm{xbpm}"
    wa = [0.0, 6.5, 13.0]

    yield from bps.mv(GV7.open_cmd, 1)
    yield from bps.sleep(1)
    yield from bps.mv(GV7.open_cmd, 1)

    for x, y, name in zip(x_s, y_s, names):
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(piezo.y, y)

        ys = np.linspace(y, y + 500, 2)
        xs = np.linspace(x, x - 500, 2)

        yss, xss = np.meshgrid(ys, xs)
        yss = yss.ravel()
        xss = xss.ravel()
        yield from NEXAFS_Ca_edge_special(t=0.5, name=name)

        for wax in wa:

            yield from bps.mv(waxs, wax)

            for k, e in enumerate(energies):
                yield from bps.mv(energy, e)

                for pos, (xsss, ysss) in enumerate(zip(xss, yss)):
                    yield from bps.mv(piezo.x, xsss)
                    yield from bps.mv(piezo.y, ysss)

                    sample_name = name_fmt.format(
                        sample=name,
                        energy=e,
                        posi="%1.1d" % pos,
                        wa="%2.1f" % wax,
                        xbpm="%3.1f" % xbpm3.sumY.value,
                    )
                    sample_id(user_name="JDM", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)

                yield from bps.mv(energy, 4050)
                yield from bps.mv(energy, 4030)

        wa = [0.0, 6.5, 13.0]
        for wax in wa[::-1]:
            yield from bps.mv(waxs, wax)

            for pos, (xsss, ysss) in enumerate(zip(xss, yss)):
                yield from bps.mv(piezo.x, xsss)
                yield from bps.mv(piezo.y, ysss)

                name_fmt = "{sample}_postmeas_4030eV_pos{posi}_wa{wa}_xbpm{xbpm}"
                sample_name = name_fmt.format(
                    sample=name,
                    posi="%2.2d" % pos,
                    wa="%2.1f" % wax,
                    xbpm="%3.1f" % xbpm3.sumY.value,
                )
                sample_id(user_name="JDM", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

    sample_id(user_name="test", sample_name="test")


def NEXAFS_Ca_edge_special(t=0.5, name="test"):
    yield from bps.mv(waxs, 60)
    dets = [pil300KW]

    energies = np.linspace(4030, 4100, 71)

    det_exposure_time(t, t)
    name_fmt = "nexafs_{sample}_{energy}eV_xbpm{xbpm}"
    for e in energies:
        yield from bps.mv(energy, e)
        sample_name = name_fmt.format(
            sample=name, energy=e, xbpm="%3.1f" % xbpm3.sumY.value
        )
        sample_id(user_name="JDM", sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")
        yield from bp.count(dets, num=1)

    yield from bps.mv(energy, 4075)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 4050)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 4030)

    sample_id(user_name="test", sample_name="test")


def night_shift_run(t=1):
    yield from SAXS_Ca_edge_dry_special1(t=0.5)
    yield from bps.sleep(10)
    yield from SAXS_Ca_edge_dry_special2(t=0.5)


def run_saxs_nexafs(t=1):
    yield from nexafs_prep_multisample(t=0.5)
    yield from bps.sleep(10)
    yield from saxs_prep_multisample(t=0.5)


def nexafs_prep_multisample(t=1):
    names = [
        "NEXAFS_WT_CH24_1_spot3",
        "NEXAFS_WT_CH24_2_spot3",
        "NEXAFS_WT_CH24_3_spot3",
        "NEXAFS_xxt1xxt2_CH24_Ca_1_spot1",
    ]
    x_s = [27400, 20800, 14700, -13250]
    y_s = [300, 300, 200, -1300]

    for x, y, name in zip(x_s, y_s, names):
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(piezo.y, y)

        yield from NEXAFS_Ca_edge_multi(t=0.5, name=name)

    sample_id(user_name="test", sample_name="test")


def saxs_prep_multisample(t=1):
    dets = [pil300KW, pil1M]
    names = [
        "xxt1xxt2_CH24_Ca_1_spot1",
        "xxt1xxt2_CH24_Ca_1_spot2",
        "xxt1xxt2_CH24_Ca_1_spot3",
        "xxt1xxt2_CH24_Ca_3_spot3",
        "xxt1xxt2_CH24_Ca_3_spot2",
        "xxt1xxt2_CH24_Ca_3_spot1",
    ]
    x_s = [-13250, -13250, -13250, -27550, -27250, -27490]
    y_s = [-1400, -800, 100, 300, -800, -1600]

    energies = [4030, 4040, 4050, 4055, 4075]
    det_exposure_time(t, t)
    name_fmt = "{sample}_{energy}eV_pos{posi}_wa{wa}_xbpm{xbpm}"
    wa = [0, 6.5, 13.0]  # 19.5

    for x, y, name in zip(x_s, y_s, names):
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(piezo.y, y)

        for wax in wa:
            yield from bps.mv(waxs, wax)
            for k, e in enumerate(energies):
                yield from bps.mv(energy, e)
                name_fmt = "{sample}_{energy}eV_xbpm{xbpm}_wa{wa}"

                sample_name = name_fmt.format(
                    sample=name,
                    energy=e,
                    xbpm="%3.1f" % xbpm3.sumY.value,
                    wa="%2.1f" % wax,
                )
                sample_id(user_name="OS", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 4050)
            yield from bps.mv(energy, 4030)

        for wax in wa[::-1]:
            yield from bps.mv(waxs, wax)

            name_fmt = "{sample}_4030eV_postmeas_xbpm{xbpm}_wa{wa}"
            sample_name = name_fmt.format(
                sample=name, xbpm="%3.1f" % xbpm3.sumY.value, wa="%2.1f" % wax
            )
            sample_id(user_name="OS", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)

        sample_id(user_name="test", sample_name="test")


def NEXAFS_Ca_edge_multi(t=0.5, name="test"):
    yield from bps.mv(waxs, 60)
    dets = [pil300KW]

    energies = np.linspace(4030, 4150, 121)

    det_exposure_time(t, t)
    name_fmt = "{sample}_{energy}eV_xbpm{xbpm}"
    for e in energies:
        yield from bps.mv(energy, e)
        sample_name = name_fmt.format(
            sample=name, energy=e, xbpm="%3.1f" % xbpm3.sumY.value
        )
        sample_id(user_name="OS", sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")
        yield from bp.count(dets, num=1)

    yield from bps.mv(energy, 4125)
    yield from bps.mv(energy, 4100)
    yield from bps.mv(energy, 4075)
    yield from bps.mv(energy, 4050)
    yield from bps.mv(energy, 4030)

    sample_id(user_name="test", sample_name="test")


def NEXAFS_Ca_edge(
    t=0.5,
):
    yield from bps.mv(waxs, 60)
    dets = [pil300KW]
    name = "hyd_cell_blank_sp2"
    # x = [8800]

    energies = np.linspace(4030, 4150, 121)

    # for name, x in zip(names, x):
    # bps.mv(piezo.x, x)
    det_exposure_time(t, t)
    name_fmt = "{sample}_{energy}eV_xbpm{xbpm}"
    for e in energies:
        yield from bps.mv(energy, e)
        sample_name = name_fmt.format(
            sample=name, energy=e, xbpm="%3.1f" % xbpm3.sumY.value
        )
        sample_id(user_name="JDM", sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")
        yield from bp.count(dets, num=1)

    yield from bps.mv(energy, 4125)
    yield from bps.mv(energy, 4100)
    yield from bps.mv(energy, 4075)
    yield from bps.mv(energy, 4050)
    yield from bps.mv(energy, 4030)
    name_fmt = "{sample}_4030.0eV_postmeas"
    sample_name = name_fmt.format(sample=name)
    sample_id(user_name="OS", sample_name=sample_name)
    print(f"\n\t=== Sample: {sample_name} ===\n")
    yield from bp.count(dets, num=1)

    sample_id(user_name="test", sample_name="test")


def NEXAFS_P_edge(t=0.5):
    yield from bps.mv(waxs, 30)
    dets = [pil300KW]
    name = "NEXAFS_PBS1_Pedge_nspot1"

    energies = np.linspace(2140, 2180, 41)
    energies_back = np.linspace(2180, 2140, 41)

    det_exposure_time(t, t)
    name_fmt = "{sample}_{energy}eV_xbpm{xbpm}"
    for e in energies:
        yield from bps.mv(energy, e)
        sample_name = name_fmt.format(
            sample=name, energy=e, xbpm="%3.1f" % xbpm3.sumY.value
        )
        sample_id(user_name="SR", sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")
        yield from bp.count(dets, num=1)

    for e in energies_back:
        yield from bps.mv(energy, e)
        yield from bps.sleep(2)


def NEXAFS_S_edge(t=0.5):
    yield from bps.mv(waxs, 30)
    dets = [pil300KW]
    name = "NEXAFS_A12_Sedge"

    energies = np.linspace(2430, 2500, 71)
    energies_back = np.linspace(2500, 2430, 36)

    det_exposure_time(t, t)
    name_fmt = "{sample}_{energy}eV_xbpm{xbpm}"
    for e in energies:
        yield from bps.mv(energy, e)
        sample_name = name_fmt.format(
            sample=name, energy=e, xbpm="%3.1f" % xbpm3.sumY.value
        )
        sample_id(user_name="SR", sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")
        yield from bp.count(dets, num=1)

    for e in energies_back:
        yield from bps.mv(energy, e)


def waxs_S_edge(t=1):
    dets = [pil300KW]

    names = ["A41"]
    x = [-28200]
    y = [1600]

    names1 = ["P3HT"]
    x1 = [-38700]
    y1 = [900]

    energies = np.linspace(2456, 2500, 23)
    Ys = np.linspace(900, 2200, 23)
    waxs_arc = [0, 19.5, 4]

    for name, xs, ys in zip(names, x, y):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        det_exposure_time(t, t)
        name_fmt = "{sample}_{energy}eV"
        for e in energies:
            yield from bps.mv(energy, e)
            sample_name = name_fmt.format(sample=name, energy=e)
            sample_id(user_name="SR", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.scan(dets, waxs, *waxs_arc)

        yield from bps.mv(energy, 2490)
        yield from bps.mv(energy, 2480)
        yield from bps.mv(energy, 2470)
        yield from bps.mv(energy, 2460)
        yield from bps.mv(energy, 2456)

        name_fmt = "{sample}_2456eV_postmeas"
        sample_name = name_fmt.format(sample=name)
        sample_id(user_name="SR", sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")
        yield from bp.scan(dets, waxs, *waxs_arc)


def waxs_S_edge(t=1):
    dets = [pil300KW]

    names1 = ["P3HT"]
    x1 = [-38700]
    y1 = [900]

    energies = [2460, 2465, 2470, 2474, 2475, 2476, 2478, 2480]
    Ys = np.linspace(900, 2200, 8)

    waxs_arc = [0, 39, 7]
    for name, xs, ys in zip(names1, x1, y1):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        det_exposure_time(t, t)
        name_fmt = "{sample}_{energy}eV"
        for e, ys in zip(energies, Ys):
            yield from bps.mv(energy, e)
            yield from bps.mv(piezo.y, ys)
            sample_name = name_fmt.format(sample=name, energy=e)
            sample_id(user_name="GF", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.scan(dets, waxs, *waxs_arc)

        yield from bps.mv(energy, 2470)
        yield from bps.mv(energy, 2460)

        name_fmt = "{sample}_2460eV_postmeas"
        sample_name = name_fmt.format(sample=name)
        sample_id(user_name="SR", sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")
        yield from bp.scan(dets, waxs, *waxs_arc)


def gomez_S_edge_new(t=1):
    dets = [pil300KW]

    energies = (
        np.arange(2445, 2470, 5).tolist()
        + np.arange(2470, 2480, 0.25).tolist()
        + np.arange(2480, 2490, 1).tolist()
        + np.arange(2490, 2501, 5).tolist()
    )
    waxs_arc = np.linspace(0, 19.5, 4)

    yield from bps.mv(stage.th, 0)
    yield from bps.mv(stage.y, 0)

    names = [
        "P-1",
        "P-2",
        "Y-1",
        "Y-2",
        "Y-3",
        "A5-1",
        "A05-2",
        "A0-1",
        "A0-2",
        "A2-1",
        "A2-2",
        "A05-1",
        "A5-2",
        "5",
        "2-1",
        "2-2",
        "05",
    ]
    x = [
        43400,
        38100,
        32300,
        26850,
        21700,
        16200,
        11000,
        5600,
        400,
        -4900,
        -10300,
        -15600,
        -21100,
        -26300,
        -31400,
        -36500,
        -42100,
    ]
    y = [
        -3850,
        -3950,
        -3800,
        -400,
        -4100,
        -4150,
        -4150,
        -4150,
        -4100,
        -4100,
        -4050,
        -4200,
        -3750,
        -3800,
        -3700,
        -3650,
        -3800,
    ]

    for name, xs, ys in zip(names, x, y):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)

        yss = np.linspace(ys, ys + 700, 29)
        xss = np.array([xs, xs + 300])

        yss, xss = np.meshgrid(yss, xss)
        yss = yss.ravel()
        xss = xss.ravel()

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)

            det_exposure_time(t, t)
            name_fmt = "{sample}_{energy}eV_wa{wax}_bpm{xbpm}"
            for e, xsss, ysss in zip(energies, xss, yss):
                yield from bps.mv(energy, e)
                yield from bps.sleep(1)

                yield from bps.mv(piezo.y, ysss)
                yield from bps.mv(piezo.x, xsss)

                bpm = xbpm2.sumX.value

                sample_name = name_fmt.format(
                    sample=name, energy="%6.2f" % e, wax=wa, xbpm="%4.3f" % bpm
                )
                sample_id(user_name="GF", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 2470)
            yield from bps.mv(energy, 2450)

    yield from bps.mv(stage.th, 1)
    yield from bps.mv(stage.y, -8)
    names = ["10", "CN", "CN-2", "CB", "CB-2", "DIO", "AA-1", "AA-2", "AA-3"]
    x = [44300, 39200, 33800, 28500, 23200, 18100, 11700, 6300, 900]
    y = [-8700, -8700, -8550, -8400, -8400, -7800, -8600, -8500, -8400]

    for name, xs, ys in zip(names, x, y):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)

        yss = np.linspace(ys, ys + 700, 29)
        xss = np.array([xs, xs + 300])

        yss, xss = np.meshgrid(yss, xss)
        yss = yss.ravel()
        xss = xss.ravel()

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)

            det_exposure_time(t, t)
            name_fmt = "{sample}_{energy}eV_wa{wax}_bpm{xbpm}"
            for e, xsss, ysss in zip(energies, xss, yss):
                yield from bps.mv(energy, e)
                yield from bps.sleep(1)

                yield from bps.mv(piezo.y, ysss)
                yield from bps.mv(piezo.x, xsss)

                bpm = xbpm2.sumX.value

                sample_name = name_fmt.format(
                    sample=name, energy="%6.2f" % e, wax=wa, xbpm="%4.3f" % bpm
                )
                sample_id(user_name="GF", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 2470)
            yield from bps.mv(energy, 2450)


def nexafs_gomez_S_edge_new(t=1):
    dets = [pil300KW]

    energies = (
        np.arange(2445, 2470, 5).tolist()
        + np.arange(2470, 2480, 0.25).tolist()
        + np.arange(2480, 2490, 1).tolist()
        + np.arange(2490, 2501, 5).tolist()
    )
    waxs_arc = [52.5]

    yield from bps.mv(stage.th, 0)
    yield from bps.mv(stage.y, 0)

    names = ["A05-1", "A5-2", "5", "2-1", "2-2", "05"]
    x = [-15600, -21100, -26300, -31400, -36500, -42100]
    y = [-4200, -3750, -3800, -3700, -3650, -3800]

    for name, xs, ys in zip(names, x, y):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)
            det_exposure_time(t, t)
            name_fmt = "nexafs_{sample}_{energy}eV_wa{wax}_bpm{xbpm}"
            for e in energies:
                yield from bps.mv(energy, e)
                yield from bps.sleep(1)

                bpm = xbpm2.sumX.value

                sample_name = name_fmt.format(
                    sample=name, energy="%6.2f" % e, wax=wa, xbpm="%4.3f" % bpm
                )
                sample_id(user_name="GF", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 2470)
            yield from bps.mv(energy, 2450)

    yield from bps.mv(stage.th, 1)
    yield from bps.mv(stage.y, -8)
    names = ["10", "CN", "CN-2", "CB", "CB-2", "DIO", "AA-1", "AA-2", "AA-3"]
    x = [44300, 39200, 33800, 28500, 23200, 18100, 11700, 6300, 900]
    y = [-8700, -8700, -8550, -8400, -8400, -7800, -8600, -8500, -8400]

    for name, xs, ys in zip(names, x, y):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)

            det_exposure_time(t, t)
            name_fmt = "nexafs_{sample}_{energy}eV_wa{wax}_bpm{xbpm}"
            for e in energies:
                yield from bps.mv(energy, e)
                yield from bps.sleep(1)

                bpm = xbpm2.sumX.value

                sample_name = name_fmt.format(
                    sample=name, energy="%6.2f" % e, wax=wa, xbpm="%4.3f" % bpm
                )
                sample_id(user_name="GF", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 2470)
            yield from bps.mv(energy, 2450)


def trans_sulf(en1, en2, step):
    eners = np.linspace(en1, en2, step)
    for e in eners:
        yield from bps.mv(energy, e)
        yield from bps.sleep(10)

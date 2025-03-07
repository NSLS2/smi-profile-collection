def P_edge_measurments(t=1):
    dets = [pil1M, pil300KW]
    det_exposure_time(t, t)

    names = [
        "s05_P3MEEMT_115C_KPF6",
        "s34_MM460_170_KPF6",
        "s30_MMM389_170_KPF6",
        "s38_MM461_170_KPF6",
        "s8_P3HT_ac_KPF6",
        "s42_MM389_170_KPF6",
        "s46_MM460_170_KPF6",
        "s50_MM461_170_KPF6",
    ]
    x_piezo = [42000, 31000, 19000, 6000, -6000, -16000, -33000, -44000]

    energies = [
        2140.0,
        2145.0,
        2150.0,
        2155.0,
        2157.0,
        2157.5,
        2158.0,
        2158.5,
        2159.0,
        2159.5,
        2160.0,
        2160.5,
        2161.0,
        2161.5,
        2162.0,
        2162.5,
        2163.0,
        2163.5,
        2164.0,
        2164.5,
        2165.0,
        2165.5,
        2166.0,
        2170.0,
        2175.0,
        2180.0,
        2185.0,
        2190.0,
        2195.0,
        2200.0,
    ]
    xbpm3_y = [
        1.416,
        1.414,
        1.412,
        1.41,
        1.4092,
        1.409,
        1.4088,
        1.4086,
        1.4084,
        1.4082,
        1.408,
        1.4078,
        1.4076,
        1.4074,
        1.4072,
        1.407,
        1.4068,
        1.4066,
        1.4064,
        1.4062,
        1.406,
        1.4058,
        1.4056,
        1.404,
        1.402,
        1.4,
        1.398,
        1.396,
        1.394,
        1.392,
    ]

    waxs_arc = [0, 17]
    ai0 = 0
    ai_list = [0.52, 0.80]

    offset = 0  # offset to not measure again teh same position as sulfur

    for name, xs in zip(names, x_piezo):
        yield from bps.mv(piezo.x, xs)

        yield from alignement_special(angle=0.75)

        ai0 = piezo.th.position
        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)

            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)
                yield from bps.mv(piezo.x, xs + offset + k * 400)

                name_fmt = "{sample}_{energy}eV_ai{ai}_pos1_wa{wax}_bpm{xbpm}"

                for e, xbpm3_ys in zip(energies, xbpm3_y):
                    yield from bps.mv(energy, e)
                    yield from bps.mv(xbpm3_pos.y, xbpm3_ys)
                    yield from bps.sleep(1)
                    bpm = xbpm2.sumX.value
                    sample_name = name_fmt.format(
                        sample=name,
                        energy="%6.2f" % e,
                        ai="%3.2f" % ais,
                        wax=wa,
                        xbpm="%4.3f" % bpm,
                    )
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)

                yield from bps.mvr(piezo.x, 200)
                name_fmt = "{sample}_{energy}eV_ai{ai}_pos2_wa{wax}_bpm{xbpm}"
                for e, xbpm3_ys in zip(energies[::-1], xbpm3_y[::-1]):
                    yield from bps.mv(energy, e)
                    yield from bps.mv(xbpm3_pos.y, xbpm3_ys)
                    yield from bps.sleep(1)
                    bpm = xbpm2.sumX.value
                    sample_name = name_fmt.format(
                        sample=name,
                        energy="%6.2f" % e,
                        ai="%3.2f" % ais,
                        wax=wa,
                        xbpm="%4.3f" % bpm,
                    )
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)


def transition_Cl_S_edges():
    yield from bps.mv(energy, 2800)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 2780)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 2760)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 2740)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 2720)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 2700)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 2680)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 2660)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 2640)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 2610)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 2580)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 2550)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 2525)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 2500)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 2475)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 2450)
    yield from bps.sleep(2)


def transition_S_Cl_edges():
    yield from bps.mv(energy, 2450)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 2475)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 2500)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 2525)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 2550)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 2580)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 2610)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 2640)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 2660)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 2680)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 2700)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 2720)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 2740)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 2760)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 2780)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 2800)
    yield from bps.sleep(2)


def Cl_edge_vertical(t=1):
    dets = [pil300KW]
    det_exposure_time(t, t)

    # name = 's01_P3HT015_un', 's04_P3MEEMT_115_un', 's33_MM460_170_ClO4'
    name = "s33_MM460_170_ClO4"

    energies = [
        2820.0,
        2830.0,
        2832.0,
        2834.0,
        2834.5,
        2835.0,
        2835.5,
        2836.0,
        2836.5,
        2837.0,
        2837.5,
        2838.0,
        2838.5,
        2839.0,
        2839.5,
        2840.0,
        2840.5,
        2841.0,
        2841.5,
        2845.0,
        2850.0,
        2855.0,
        2860.0,
        2865.0,
        2870.0,
    ]

    waxs_arc = [4, 10.5, 17, 45]

    ai0 = piezo.th.position
    for i, wa in enumerate(waxs_arc):
        if i == 0:
            print("wa=4deg")
        else:
            yield from bps.mv(waxs, wa)

        name_fmt = "{sample}_vertical_{energy}eV_ai0.8deg_pos1_wa{wax}_bpm{xbpm}"
        for e in energies:
            yield from bps.mv(energy, e)
            yield from bps.sleep(1)
            bpm = xbpm2.sumX.value
            sample_name = name_fmt.format(
                sample=name, energy="%6.2f" % e, wax=wa, xbpm="%4.3f" % bpm
            )
            sample_id(user_name="LR", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)

        yield from bps.mv(energy, 2850)
        yield from bps.sleep(2)
        yield from bps.mv(energy, 2830)
        yield from bps.sleep(2)
        yield from bps.mv(energy, 2810)
        yield from bps.sleep(2)


def NEXAFS_P_edge(t=0.5):
    yield from bps.mv(waxs, 45)
    dets = [pil300KW]
    name = "NEXAFS_s3_test_Pedge_nspot1"

    energies = np.linspace(2130, 2180, 51)
    xbpm3_y = np.linspace(1.42, 1.40, 51)

    det_exposure_time(t, t)
    name_fmt = "{sample}_{energy}eV_xbpm{xbpm}"

    for e, xbpm3_ys in zip(energies, xbpm3_y):
        yield from bps.mv(energy, e)
        yield from bps.mv(xbpm3_pos.y, xbpm3_ys)

        yield from bps.sleep(1)

        sample_name = name_fmt.format(
            sample=name, energy=e, xbpm="%3.1f" % xbpm2.sumX.value
        )
        sample_id(user_name="LR", sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")
        yield from bp.count(dets, num=1)


def S_edge_vertical(t=1):
    dets = [pil300KW]
    det_exposure_time(t, t)

    # name = 's01_P3HT015_un', 's04_P3MEEMT_115_un', 's33_MM460_170_ClO4'
    name = "MM460_170"

    energies = [
        2450.0,
        2455.0,
        2460.0,
        2465.0,
        2470.0,
        2473.0,
        2475.0,
        2475.5,
        2476.0,
        2476.5,
        2477.0,
        2477.5,
        2478.0,
        2478.5,
        2479.0,
        2479.5,
        2480.0,
        2480.5,
        2483.0,
        2485.0,
        2487.5,
        2490.0,
        2492.5,
        2495.0,
        2500.0,
        2510.0,
        2515.0,
    ]

    # waxs_arc = [4, 10.5, 17]
    waxs_arc = [10.5, 17]

    ai0 = piezo.th.position
    for i, wa in enumerate(waxs_arc):
        if wa == 4:
            print("wa=4deg")
        else:
            yield from bps.mv(waxs, wa)

        name_fmt = "{sample}_vertical_{energy}eV_ai7.7deg_pos1_wa{wax}_bpm{xbpm}"
        for e in energies:
            yield from bps.mv(energy, e)
            yield from bps.sleep(1)
            bpm = xbpm2.sumX.value
            sample_name = name_fmt.format(
                sample=name, energy="%6.2f" % e, wax=wa, xbpm="%4.3f" % bpm
            )
            sample_id(user_name="LR", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)

        yield from bps.mv(energy, 2490)
        yield from bps.sleep(1)
        yield from bps.mv(energy, 2470)
        yield from bps.sleep(1)
        yield from bps.mv(energy, 2450)
        yield from bps.sleep(1)


def giwaxs_Cl_edge_Lee_aois_2121_1(t=1):
    dets = [pil1M, pil300KW]

    # names =   ['P3HT_600_KCl04_par', 'P3HT_500_KCl04', 'P3HT_neat', 'P3HT_600_KCl']
    # x_piezo = [              -31000,           -41000,      -53000,         -56000]
    # x_hexa =  [                   0,                0,           0,             -8]
    # z_piezo = [                   0,                0,           0,              0]

    names = ["P3HT_KCl04_bilayer"]
    x_piezo = [50000]
    x_hexa = [0]
    z_piezo = [0]

    dets = [pil1M, pil300KW]
    waxs_arc = [0, 15]

    for numero, (name, xs_piezo, xs_hexa, zs_piezo) in enumerate(
        zip(names, x_piezo, x_hexa, z_piezo)
    ):
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, xs_piezo)
        yield from bps.mv(piezo.z, zs_piezo)

        ai0 = 0
        yield from bps.mv(piezo.th, ai0)
        yield from alignement_gisaxs(angle=0.4)
        ai0 = piezo.th.position

        yield from bps.mv(att2_9.open_cmd, 1)
        yield from bps.sleep(1)
        yield from bps.mv(att2_9.open_cmd, 1)

        ai_list = np.arange(0.3, 0.8, 0.01).tolist()
        ai_list = [round(1000 * x, 4) for x in ai_list]
        ai_list = np.asarray(ai_list) / 1000
        energies = [2820.0, 2838.5, 2870.0]

        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)

            for k, e in enumerate(energies):
                yield from bps.mv(energy, e)
                yield from bps.sleep(2)

                yield from bps.mv(piezo.x, xs_piezo + k * 600 + i * 200)

                for l, ais in enumerate(ai_list):
                    yield from bps.mv(piezo.th, ai0 + ais)

                    det_exposure_time(t, t)
                    name_fmt = (
                        "{sample}_pos1_aiscan_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                    )

                    bpm = xbpm2.sumX.value
                    sample_name = name_fmt.format(
                        sample=name,
                        energy="%6.2f" % e,
                        ai="%1.4f" % ais,
                        wax=wa,
                        xbpm="%4.3f" % bpm,
                    )
                    sample_id(user_name="GF", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)

            for k, e in enumerate(energies[::-1]):
                yield from bps.mv(energy, e)
                yield from bps.sleep(2)

                yield from bps.mv(piezo.x, xs_piezo + 1000 + k * 600 + i * 200)

                for l, ais in enumerate(ai_list):
                    yield from bps.mv(piezo.th, ai0 + ais)

                    det_exposure_time(t, t)
                    name_fmt = (
                        "{sample}_pos2_aiscan_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                    )

                    bpm = xbpm2.sumX.value
                    sample_name = name_fmt.format(
                        sample=name,
                        energy="%6.2f" % e,
                        ai="%3.2f" % ais,
                        wax=wa,
                        xbpm="%4.3f" % bpm,
                    )
                    sample_id(user_name="GF", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)


def SVA_night_12_02(t=1):
    global names, x_hexa, y_hexa, incident_angles, y_hexa_aligned

    names = [
        "MM460_170C_ClO4",
        "MM389_as_un",
        "MM389_as_ClO4",
        "MM389_170C_un",
        "MM389_170C_ClO4",
    ]
    x_hexa = [-17, 18, 9, -6, -15]
    # y_hexa = [-3.2, -3.2, -3.2, -3.2,  3,  3,  3,   3]
    # incident_angl = [ 2.8,  2.5,  2.2,  2.2, 2.2, 2.2, 2.2, 2.2]

    # assert len(x_hexa) == len(names), f'Number of X coordinates ({len(x_hexa)}) is different from number of samples ({len(names)})'
    # assert len(x_hexa) == len(y_hexa), f'Number of X coordinates ({len(x_hexa)}) is different from number of samples ({len(y_hexa)})'
    # assert len(x_hexa) == len(incident_angl), f'Number of X coordinates ({len(x_hexa)}) is different from number of samples ({len(incident_angles)})'

    setDryFlow(5)
    setWetFlow(0)

    y_hexa_aligned = [-3.013, 3.311, 3.32, 3.356, 3.322]
    incident_angles = [1.581, 1.199, 1.849, 1.367, 1.825]
    # for name, xs_hexa, ys_hexa, ais in zip(names[4:], x_hexa[4:], y_hexa[4:], incident_angl[4:]):
    #     yield from bps.mv(stage.x, xs_hexa)
    #     yield from bps.mv(stage.y, ys_hexa)
    #     yield from bps.mv(stage.th, ais)

    #     yield from alignement_gisaxs_hex(angle = 0.45)

    #     incident_angles = incident_angles + [stage.th.position]
    #     y_hexa_aligned = y_hexa_aligned + [stage.y.position]

    print(incident_angles)
    print(y_hexa_aligned)

    assert len(x_hexa) == len(
        names
    ), f"Number of X coordinates ({len(x_hexa)}) is different from number of samples ({len(names)})"
    assert len(x_hexa) == len(
        y_hexa_aligned
    ), f"Number of X coordinates ({len(x_hexa)}) is different from number of samples ({len(y_hexa_aligned)})"
    assert len(x_hexa) == len(
        incident_angles
    ), f"Number of X coordinates ({len(x_hexa)}) is different from number of samples ({len(incident_angles)})"

    humidity = "%3.2f" % readHumidity(verbosity=0)
    # Measure the samples with N2 flow
    offset = 0
    yield from Cl_edge_SVA_measurments_2021_2(t=t, offset=offset, humidity=humidity)

    # # Measure at flow 80 percent
    # setDryFlow(2.)
    # setWetFlow(4.35)

    # yield from bps.sleep(40 * 60)
    # humidity = '%3.2f'%readHumidity(verbosity=0)

    # offset = 0.9
    # yield from Cl_edge_SVA_measurments(t=t, offset = offset, humidity = humidity)

    # # Measure at flow 100 percent

    names = [
        "MM460_as_un",
        "MM460_as_ClO4",
        "MM460_170C_un",
        "MM460_170C_ClO4",
        "MM389_as_un",
        "MM389_as_ClO4",
        "MM389_170C_un",
        "MM389_170C_ClO4",
    ]
    x_hexa = [17, 6, -8.0, -17, 18, 9, -6, -15]
    y_hexa_aligned = [-3.052, -3.06, -2.998, -3.013, 3.311, 3.32, 3.356, 3.322]
    incident_angles = [1.94502, 1.77, 1.747, 1.581, 1.199, 1.849, 1.367, 1.825]

    setDryFlow(0)
    setWetFlow(5)

    yield from bps.sleep(40 * 60)
    humidity = "%3.2f" % readHumidity(verbosity=0)
    offset = 1.5
    yield from Cl_edge_SVA_measurments_2021_2(t=t, offset=offset, humidity=humidity)

    # # Back at flow 0 percent
    setDryFlow(5)
    setWetFlow(0)

    yield from bps.sleep(40 * 60)
    humidity = "%3.2f_post" % readHumidity(verbosity=0)

    offset = 3.0
    yield from Cl_edge_SVA_measurments_2021_2(t=t, offset=offset, humidity=humidity)


def S_edge_measurments_transmission(t=1):
    dets = [pil1M, pil900KW, pil300KW]

    # names = ['P3MEEMT_13k_115C', 'P3MEEMT_23k_115C', 'MM460_170C', 'PB2T_TEG_undoped', 'PB2T_TEG_partialCV', 'PB2T_TEG_partial_dedope',
    # 'PB2T_TEG_doped400mV', 'KClO4_neat']
    # x_piezo = [28100, 20500, 12500, 4700, -800, -6800, -12000, -19000]
    # y_piezo = [  400,   400,   400,  500,  400,   200,    300,    300]

    names = ["P3MEEMT_13k_115C", "P3MEEMT_23k_115C", "MM460_170C"]
    x_piezo = [27400, 19700, 11800]
    y_piezo = [0, -100, -100]

    assert len(x_piezo) == len(
        names
    ), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(
        y_piezo
    ), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"

    energies = [
        2450.0,
        2455.0,
        2460.0,
        2465.0,
        2470.0,
        2473.0,
        2475.0,
        2475.5,
        2476.0,
        2476.5,
        2477.0,
        2477.5,
        2478.0,
        2478.5,
        2479.0,
        2479.5,
        2480.0,
        2480.5,
        2483.0,
        2485.0,
        2487.5,
        2490.0,
        2492.5,
        2495.0,
        2500.0,
        2510.0,
        2515.0,
    ]

    waxs_arc = [23]
    det_exposure_time(t, t)

    for numb, (name, xs, ys) in enumerate(zip(names, x_piezo, y_piezo)):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)

        yss = np.linspace(ys, ys + 1000, 27)

        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(piezo.x, xs)
            yield from bps.mv(waxs, wa)

            name_fmt = "{sample}_saxsredo_{energy}eV_pos1_wa{wax}_bpm{xbpm}"
            for e, ysss in zip(energies, yss):
                yield from bps.mv(energy, e)
                yield from bps.sleep(1)
                yield from bps.mv(piezo.y, ysss)
                bpm = xbpm2.sumX.value
                sample_name = name_fmt.format(
                    sample=name, energy="%6.2f" % e, wax=wa, xbpm="%4.3f" % bpm
                )
                sample_id(user_name="LR", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

            yield from bps.mvr(piezo.x, 400)
            name_fmt = "{sample}_{energy}eV_pos2_wa{wax}_bpm{xbpm}"
            for e, ysss in zip(energies[::-1], yss):
                yield from bps.mv(energy, e)
                yield from bps.sleep(1)
                yield from bps.mv(piezo.y, ysss)
                bpm = xbpm2.sumX.value
                sample_name = name_fmt.format(
                    sample=name, energy="%6.2f" % e, wax=wa, xbpm="%4.3f" % bpm
                )
                sample_id(user_name="LR", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)


def Cl_edge_measurments_transmission(t=1):
    dets = [pil1M, pil900KW, pil300KW]

    # names = ['PB2T_TEG_undoped', 'PB2T_TEG_partialCV', 'PB2T_TEG_partial_dedope', 'PB2T_TEG_doped400mV', 'KClO4_neat']
    # x_piezo = [3800, -1800, -7800, -13300, -20000]
    # y_piezo = [ 400,   200,     0,    300,    300]

    names = ["PB2T_TEG_doped400mV", "KClO4_neat"]
    x_piezo = [-12500, -20000]
    y_piezo = [300, 300]

    assert len(x_piezo) == len(
        names
    ), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(
        y_piezo
    ), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"

    energies = [
        2810.0,
        2820.0,
        2830.0,
        2832.0,
        2834.0,
        2834.5,
        2835.0,
        2835.5,
        2836.0,
        2836.5,
        2837.0,
        2837.5,
        2838.0,
        2838.5,
        2839.0,
        2839.5,
        2840.0,
        2840.5,
        2841.0,
        2841.5,
        2845.0,
        2850.0,
        2855.0,
        2860.0,
        2865.0,
        2870.0,
        2875.0,
        2880.0,
        2890.0,
    ]

    waxs_arc = [2, 23]
    det_exposure_time(t, t)

    for numb, (name, xs, ys) in enumerate(zip(names, x_piezo, y_piezo)):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)

        yss = np.linspace(ys, ys + 1000, 27)

        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(piezo.x, xs)
            yield from bps.mv(waxs, wa)

            name_fmt = "{sample}_saxs_{energy}eV_pos1_wa{wax}_bpm{xbpm}"
            for e, ysss in zip(energies, yss):
                yield from bps.mv(energy, e)
                yield from bps.sleep(1)
                yield from bps.mv(piezo.y, ysss)
                bpm = xbpm2.sumX.value
                sample_name = name_fmt.format(
                    sample=name, energy="%6.2f" % e, wax=wa, xbpm="%4.3f" % bpm
                )
                sample_id(user_name="LR", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

            yield from bps.mvr(piezo.x, 300)
            name_fmt = "{sample}_{energy}eV_pos2_wa{wax}_bpm{xbpm}"
            for e, ysss in zip(energies[::-1], yss):
                yield from bps.mv(energy, e)
                yield from bps.sleep(1)
                yield from bps.mv(piezo.y, ysss)
                bpm = xbpm2.sumX.value
                sample_name = name_fmt.format(
                    sample=name, energy="%6.2f" % e, wax=wa, xbpm="%4.3f" % bpm
                )
                sample_id(user_name="LR", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)


def S_edge_SVA_measurments_2021_3(t=1, offset=1, humidity="test"):

    names = ["PB2T_TEG_doped400mV"]
    x_hexa = [-12500]
    y_hexa = [300]

    dets = [pil1M, pil300KW, pil900KW]
    det_exposure_time(t, t)

    energies = [
        2450.0,
        2455.0,
        2460.0,
        2465.0,
        2470.0,
        2473.0,
        2475.0,
        2475.5,
        2476.0,
        2476.5,
        2477.0,
        2477.5,
        2478.0,
        2478.5,
        2479.0,
        2479.5,
        2480.0,
        2480.5,
        2483.0,
        2485.0,
        2487.5,
        2490.0,
        2492.5,
        2495.0,
        2500.0,
        2510.0,
        2515.0,
    ]

    waxs_arc = [2, 23]
    ai_list = [0.80]

    for name, xs_hexa, incident_ang, ys_hexap in zip(
        names, x_hexa, incident_angles, y_hexa
    ):

        yield from bps.mv(stage.x, xs_hexa + offset)
        xs = xs_hexa + offset

        yield from alignement_gisaxs_hex(angle=0.45)

        yield from bps.mv(stage.y, ys_hexap)
        yield from bps.mv(stage.th, incident_ang)

        ai0 = incident_ang
        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)
            counter = 0

            for k, ais in enumerate(ai_list):
                yield from bps.mv(stage.th, ai0 + ais)

                name_fmt = "{sample}_hum{hum}_{energy}eV_ai{ai}_pos1_wa{wax}_bpm{xbpm}"
                for e in energies:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(1)
                    yield from bps.mv(stage.x, xs + counter * 0.025)
                    counter += 1
                    bpm = xbpm2.sumX.value
                    sample_name = name_fmt.format(
                        sample=name,
                        hum=humidity,
                        energy="%6.2f" % e,
                        ai="%3.2f" % ais,
                        wax=wa,
                        xbpm="%4.3f" % bpm,
                    )
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)

                name_fmt = "{sample}_hum{hum}_{energy}eV_ai{ai}_pos2_wa{wax}_bpm{xbpm}"
                for e in energies[::-1]:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(1)
                    yield from bps.mv(stage.x, xs + counter * 0.025)
                    counter += 1
                    bpm = xbpm2.sumX.value
                    sample_name = name_fmt.format(
                        sample=name,
                        hum=humidity,
                        energy="%6.2f" % e,
                        ai="%3.2f" % ais,
                        wax=wa,
                        xbpm="%4.3f" % bpm,
                    )
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)


def Cl_edge_measurments_2022_1(t=1):
    dets = [pil1M, pil900KW, pil300KW]
    det_exposure_time(t, t)

    # names = ['MM389_submerged', 'MM389_n500mV', 'MM389_n400mV', 'MM389_n300mV', 'MM389_p400mV', 'MM389_n200mV', 'MM389_n100mV', 'MM389_n000mV', 'MM389_p100mV', 'MM389_p200mV',
    # 'MM460_submerged', 'MM460_n500', 'MM460_n400', 'MM460_n300', 'MM460_p400', 'MM460_n200', 'MM460_n100', 'MM460_n000', 'MM460_p100', 'MM460_p200',
    # 'P3PAAT_un_1', 'P3PAAT_do_1','P3PAAT_un_2','P3PAAT_do_2','Polystyrene', 'PVC']
    # x_piezo = [ -50700,-51200,-44600,-33900,-23300,-12600,-1700, 9300, 19600, 30700, 41300, 48600, 48600,
    # -48500,-48700,-41800,-31700,-21300,-10700, -200,10200, 21700, 32800, 42300, 47500, 46900]
    # x_hexap = [    -15,  -4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 15,
    # -15, -4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 15 ]
    # y_piezo = [  -2900, -2850, -2800, -2750, -2700, -2650, -2600, -2550, -2500, -2450, -2400, -2350, -2300,
    # 5800,  5850,  5900,  5950,  6000,  6050,  6100,  6150,  6200,  6250,  6300,  6350,  6400]
    # to finish up last 8 samples at Cl edge:
    names = [
        "MM460_p200",
        "P3PAAT_un_1",
        "P3PAAT_do_1",
        "P3PAAT_un_2",
        "P3PAAT_do_2",
        "Polystyrene",
        "PVC",
    ]
    x_piezo = [-200, 10200, 21700, 32800, 42300, 47500, 46900]
    x_hexap = [0, 0, 0, 0, 0, 4, 15]
    y_piezo = [6100, 6150, 6200, 6250, 6300, 6350, 6400]

    assert len(x_piezo) == len(
        names
    ), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(
        y_piezo
    ), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(
        x_hexap
    ), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexap)})"

    energies = [
        2810.0,
        2820.0,
        2830.0,
        2832.0,
        2834.0,
        2834.5,
        2835.0,
        2835.5,
        2836.0,
        2836.5,
        2837.0,
        2837.5,
        2838.0,
        2838.5,
        2839.0,
        2839.5,
        2840.0,
        2840.5,
        2841.0,
        2841.5,
        2845.0,
        2850.0,
        2855.0,
        2860.0,
        2865.0,
        2870.0,
        2875.0,
        2880.0,
        2890.0,
    ]

    waxs_arc = [0, 20]
    ai0 = 0
    ai_list = [0.80]

    for name, xs, ys, xs_hexap in zip(names, x_piezo, y_piezo, x_hexap):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(stage.x, xs_hexap)

        yield from bps.mv(piezo.th, ai0)
        yield from alignement_gisaxs_doblestack(0.2)

        yield from bps.mv(att2_9.open_cmd, 1)
        yield from bps.sleep(1)
        yield from bps.mv(att2_9.open_cmd, 1)

        ai0 = piezo.th.position
        det_exposure_time(t, t)

        for i, wa in enumerate(waxs_arc):

            # Do not take SAXS when WAXS detector in the way
            dets = [pil900KW, pil300KW] if wa < 10 else [pil1M, pil900KW, pil300KW]

            yield from bps.mv(waxs, wa)
            yield from bps.mv(piezo.x, xs)
            counter = 0

            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                name_fmt = "{sample}_{energy}eV_ai{ai}_pos1_wa{wax}_bpm{xbpm}"
                for e in energies:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 120:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs + counter * 30)
                    counter += 1

                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(
                        sample=name,
                        energy="%6.2f" % e,
                        ai="%3.2f" % ais,
                        wax=wa,
                        xbpm="%4.3f" % bpm,
                    )
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)

                name_fmt = "{sample}_{energy}eV_ai{ai}_pos2_wa{wax}_bpm{xbpm}"
                for e in energies[::-1]:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 120:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs + counter * 30)
                    counter += 1

                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(
                        sample=name,
                        energy="%6.2f" % e,
                        ai="%3.2f" % ais,
                        wax=wa,
                        xbpm="%4.3f" % bpm,
                    )
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)

                # name_fmt = '{sample}_{energy}eV_ai{ai}_pos3_wa{wax}_bpm{xbpm}'
                # for e in energies:
                #     yield from bps.mv(energy, e)
                #     yield from bps.sleep(2)
                #     if xbpm2.sumX.get() < 120:
                #         yield from bps.sleep(2)
                #         yield from bps.mv(energy, e)
                #         yield from bps.sleep(2)
                #     yield from bps.mv(piezo.x, xs + counter * 30)
                #     counter += 1

                #     bpm = xbpm2.sumX.get()
                #     sample_name = name_fmt.format(sample=name, energy='%6.2f'%e, ai ='%3.2f'%ais, wax = wa, xbpm = '%4.3f'%bpm)
                #     sample_id(user_name='LR', sample_name=sample_name)
                #     print(f'\n\t=== Sample: {sample_name} ===\n')
                #     yield from bp.count(dets, num=1)

                # name_fmt = '{sample}_{energy}eV_ai{ai}_pos4_wa{wax}_bpm{xbpm}'
                # for e in energies[::-1]:
                #     yield from bps.mv(energy, e)
                #     yield from bps.sleep(2)
                #     if xbpm2.sumX.get() < 120:
                #         yield from bps.sleep(2)
                #         yield from bps.mv(energy, e)
                #         yield from bps.sleep(2)
                #     yield from bps.mv(piezo.x, xs + counter * 30)
                #     counter += 1

                #     bpm = xbpm2.sumX.get()
                #     sample_name = name_fmt.format(sample=name, energy='%6.2f'%e, ai ='%3.2f'%ais, wax = wa, xbpm = '%4.3f'%bpm)
                #     sample_id(user_name='LR', sample_name=sample_name)
                #     print(f'\n\t=== Sample: {sample_name} ===\n')
                #     yield from bp.count(dets, num=1)


def K_edge_measurments_2022_1(t=0.5):
    dets = [pil1M, pil900KW, pil300KW]
    det_exposure_time(t, t)

    # exploratory K L-edge at 2022-1:
    names = [
        "Acid_PEDOT_n600mV",
        "Acid_PEDOT_p600mV",
        "Acid_PEDOT_exposed",
        "Acid_PEDOT_n300mV",
        "Acid_PEDOT_p300mV",
        "EG_PEDOT_neat",
        "   EG_PEDOT_n600mV",
        "EG_PEDOT_p600mV",
        "EG_PEDOT_exposed",
        "EG_PEDOT_n300mV",
        "Eg_PEDOT_p300mV",
    ]
    x_piezo = [
        -56402,
        -42402,
        -30402,
        -18402,
        -5402,
        7597,
        21597,
        34597,
        43594,
        55597,
        50597,
    ]
    x_hexap = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15]
    y_piezo = [6100, 6100, 6100, 6100, 6100, 6100, 6100, 6100, 6100, 6100, 6100]

    assert len(x_piezo) == len(
        names
    ), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(
        y_piezo
    ), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(
        x_hexap
    ), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexap)})"

    energies = np.asarray(
        np.arange(3590, 3611, 5).tolist()
        + np.arange(3612, 3629, 0.4).tolist()
        + np.arange(3630, 3721, 5).tolist()
    )

    waxs_arc = [0, 20]
    ai0 = 0
    ai_list = [0.60]

    for name, xs, ys, xs_hexap in zip(names, x_piezo, y_piezo, x_hexap):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(stage.x, xs_hexap)

        yield from bps.mv(piezo.th, ai0)
        yield from alignement_gisaxs(0.4)

        yield from bps.mv(att2_9.open_cmd, 1)
        yield from bps.sleep(1)
        yield from bps.mv(att2_9.open_cmd, 1)

        ai0 = piezo.th.position
        det_exposure_time(t, t)

        for i, wa in enumerate(waxs_arc):

            # Do not take SAXS when WAXS detector in the way
            dets = [pil900KW, pil300KW] if wa < 10 else [pil1M, pil900KW, pil300KW]

            yield from bps.mv(waxs, wa)
            yield from bps.mv(piezo.x, xs)
            counter = 0

            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                name_fmt = "{sample}_{energy}eV_ai{ai}_pos1_wa{wax}_bpm{xbpm}"
                for e in energies:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 120:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs - counter * 30)
                    counter += 1

                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(
                        sample=name,
                        energy="%6.2f" % e,
                        ai="%3.2f" % ais,
                        wax=wa,
                        xbpm="%4.3f" % bpm,
                    )
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)
                yield from bps.mv(energy, 3680)
                yield from bps.sleep(2)
                yield from bps.mv(energy, 3640)
                yield from bps.sleep(2)
                yield from bps.mv(energy, 3590)
                yield from bps.sleep(2)

                # name_fmt = '{sample}_{energy}eV_ai{ai}_pos2_wa{wax}_bpm{xbpm}'
                # for e in energies[::-1]:
                #     yield from bps.mv(energy, e)
                #     yield from bps.sleep(2)
                #     if xbpm2.sumX.get() < 120:
                #         yield from bps.sleep(2)
                #         yield from bps.mv(energy, e)
                #         yield from bps.sleep(2)
                #     yield from bps.mv(piezo.x, xs - counter * 30)
                #     counter += 1

                #     bpm = xbpm2.sumX.get()
                #     sample_name = name_fmt.format(sample=name, energy='%6.2f'%e, ai ='%3.2f'%ais, wax = wa, xbpm = '%4.3f'%bpm)
                #     sample_id(user_name='LR', sample_name=sample_name)
                #     print(f'\n\t=== Sample: {sample_name} ===\n')
                #     yield from bp.count(dets, num=1)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)


def S_edge_measurments_2022_1(t=1):
    dets = [pil1M, pil900KW, pil300KW]
    det_exposure_time(t, t)

    names = ["P3HT_TCB1to20_paral_phi8deg"]
    x_piezo = np.asarray([19900])
    x_hexap = [0]
    y_piezo = [5475]

    # names = ['MM389_submerged', 'MM389_n500mV', 'MM389_n400mV', 'MM389_n300mV', 'MM389_p400mV', 'MM389_n200mV', 'MM389_n100mV', 'MM389_n000mV', 'MM389_p100mV', 'MM389_p200mV',
    # 'MM460_submerged', 'MM460_n500', 'MM460_n400', 'MM460_n300', 'MM460_p400', 'MM460_n200', 'MM460_n100', 'MM460_n000', 'MM460_p100', 'MM460_p200',
    # 'P3PAAT_un_1', 'P3PAAT_do_1','P3PAAT_un_2','P3PAAT_do_2','Polystyrene', 'PVC']
    # x_piezo = -200 + np.asarray([ -50700,-51200,-44600,-33900,-23300,-12600,-1700, 9300, 19600, 30700, 41300, 48600, 48600,
    # -48500,-48700,-41800,-31700,-21300,-10700, -200,10200, 21700, 32800, 42300, 47500, 46900])
    # x_hexap = [    -15,  -4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 15,
    # -15, -4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 15 ]
    # y_piezo = [  -2900, -2850, -2800, -2750, -2700, -2650, -2600, -2550, -2500, -2450, -2400, -2350, -2300,
    # 5800,  5850,  5900,  5950,  6000,  6050,  6100,  6150,  6200,  6250,  6300,  6350,  6400]

    # names = ['P3MEEMT_23KDa_115C_600mV', 'P3MEEMT_13KDa_115C_600mV', 'P3MEEMT_13KDa_115C_450mV', 'P3MEEMT_13KDa_115C_400mV', 'P3MEEMT_13KDa_115C_350mV',
    #'P3MEEMT_13KDa_115C_325mV', 'P3MEEMT_13KDa_115C_300mV', 'P3MEEMT_13KDa_115C_275mV', 'P3MEEMT_13KDa_115C_0mV']
    # x_piezo = -5000 + np.asarray([ 37000,  21000, 8000, -6000, -19000, -32000, -43000, -50000, -50000])
    # x_hexap = [     0,      0,    0,     0,      0,      0,      0,     -4,    -16]
    # y_piezo = [  6000,   6000, 6000,  6000,   6000,   6000,   6000,   6000,   6000]

    assert len(x_piezo) == len(
        names
    ), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(
        y_piezo
    ), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(
        x_hexap
    ), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexap)})"

    energies = [
        2450.0,
        2455.0,
        2460.0,
        2465.0,
        2470.0,
        2473.0,
        2475.0,
        2475.5,
        2476.0,
        2476.5,
        2477.0,
        2477.5,
        2478.0,
        2478.5,
        2479.0,
        2479.5,
        2480.0,
        2480.5,
        2483.0,
        2485.0,
        2487.5,
        2490.0,
        2492.5,
        2495.0,
        2500.0,
        2510.0,
        2515.0,
    ]

    waxs_arc = [0, 20]  # new cords 1 degree overlap
    ai0 = 0.0397
    ai_list = [0.80]

    for name, xs, ys, xs_hexap in zip(names, x_piezo, y_piezo, x_hexap):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(stage.x, xs_hexap)

        yield from bps.mv(piezo.th, ai0)
        # yield from alignement_gisaxs(0.20)

        # insert attenuator, factor 10
        yield from bps.mv(att2_9.open_cmd, 1)
        yield from bps.sleep(1)
        yield from bps.mv(
            att2_9.open_cmd, 1
        )  # sometimes doesn't work, belt and suspenders always two twice

        # ai0 = piezo.th.position
        det_exposure_time(t, t)

        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)
            yield from bps.mv(piezo.x, xs)
            counter = 0
            dets = [pil900KW, pil300KW] if wa < 10 else [pil1M, pil900KW, pil300KW]
            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                name_fmt = "{sample}_{energy}eV_ai{ai}_pos1_wa{wax}_bpm{xbpm}"
                for e in energies:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 120:
                        yield from bps.sleep(
                            2
                        )  # used to be 5 when fighting RF noise, can be sped up to
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs - counter * 30)
                    counter += 1

                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(
                        sample=name,
                        energy="%6.2f" % e,
                        ai="%3.2f" % ais,
                        wax=wa,
                        xbpm="%4.3f" % bpm,
                    )
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)

                name_fmt = "{sample}_{energy}eV_ai{ai}_pos2_wa{wax}_bpm{xbpm}"
                for e in energies[::-1]:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 120:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs - counter * 30)
                    counter += 1

                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(
                        sample=name,
                        energy="%6.2f" % e,
                        ai="%3.2f" % ais,
                        wax=wa,
                        xbpm="%4.3f" % bpm,
                    )
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)

                # name_fmt = '{sample}_{energy}eV_ai{ai}_pos3_wa{wax}_bpm{xbpm}'
                # for e in energies:
                #     yield from bps.mv(energy, e)
                #     yield from bps.sleep(2)
                #     if xbpm2.sumX.get() < 120:
                #         yield from bps.sleep(2)
                #         yield from bps.mv(energy, e)
                #         yield from bps.sleep(2)
                #     yield from bps.mv(piezo.x, xs - counter * 30)
                #     counter += 1

                #     bpm = xbpm2.sumX.get()
                #     sample_name = name_fmt.format(sample=name, energy='%6.2f'%e, ai ='%3.2f'%ais, wax = wa, xbpm = '%4.3f'%bpm)
                #     sample_id(user_name='LR', sample_name=sample_name)
                #     print(f'\n\t=== Sample: {sample_name} ===\n')
                # #     yield from bp.count(dets, num=1)

                # name_fmt = '{sample}_{energy}eV_ai{ai}_pos4_wa{wax}_bpm{xbpm}'
                # for e in energies[::-1]:
                #     yield from bps.mv(energy, e)
                #     yield from bps.sleep(2)
                #     if xbpm2.sumX.get() < 120:
                #         yield from bps.sleep(2)
                #         yield from bps.mv(energy, e)
                #         yield from bps.sleep(2)
                #     yield from bps.mv(piezo.x, xs - counter * 30)
                #     counter += 1

                #     bpm = xbpm2.sumX.get()
                #     sample_name = name_fmt.format(sample=name, energy='%6.2f'%e, ai ='%3.2f'%ais, wax = wa, xbpm = '%4.3f'%bpm)
                #     sample_id(user_name='LR', sample_name=sample_name)
                #     print(f'\n\t=== Sample: {sample_name} ===\n')
                #     yield from bp.count(dets, num=1)
    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)


def night_2021_12_15(t=1):
    proposal_id("2021_3", "307296_Richter4")
    yield from S_edge_measurments_2021_3(t=t)

    proposal_id("2021_3", "308274_Ferron5")
    yield from xrr_spol_waxs()


def night_2022_1(t=1):
    #   removed for night 2, kept bps.mv
    #   proposal_id('2022_1', '309251_Richter_Clnight')
    #   yield from Cl_edge_measurments_2022_1(t=t)
    yield from transition_Cl_S_edges()
    yield from bps.mv(xbpm3_pos.y, 1.376)
    proposal_id("2022_1", "309251_Richter_Snight")
    yield from S_edge_measurments_2022_1(t=t)
    #   yield from transition_S_Cl_edges()
    #   yield from bps.mv(xbpm3_pos.y, 1.43)
    #


def Cl_edge_measurments_2021_3_hex(t=1):
    dets = [pil1M, pil900KW, pil300KW]
    det_exposure_time(t, t)

    names = ["20um_blank"]
    x_hexap = [18]

    assert len(x_hexap) == len(
        names
    ), f"Number of X coordinates ({len(x_hexap)}) is different from number of samples ({len(names)})"

    energies = [
        2810.0
    ]  # , 2820.0, 2830.0, 2832.0, 2834.0, 2834.5, 2835.0, 2835.5, 2836.0, 2836.5, 2837.0, 2837.5, 2838.0, 2838.5, 2839.0, 2839.5,
    # 2840.0, 2840.5, 2841.0, 2841.5, 2845.0, 2850.0, 2855.0, 2860.0, 2865.0, 2870.0, 2875.0, 2880.0, 2890.0]

    waxs_arc = [0, 20]  # changed 2022_1 for prpoer waxs center
    ai0 = 0
    ai_list = [0.80]

    for name, xs_hexap in zip(names, x_hexap):
        yield from bps.mv(stage.x, xs_hexap)

        yield from alignement_gisaxs_hex_roughsample(angle=0.45)

        ai0 = stage.th.position
        det_exposure_time(t, t)

        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)
            counter = 0

            for k, ais in enumerate(ai_list):
                yield from bps.mv(stage.th, ai0 + ais)

                name_fmt = "{sample}_{energy}eV_ai{ai}_pos1_wa{wax}_bpm{xbpm}"
                for e in energies:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 120:
                        yield from bps.sleep(5)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(stage.x, xs_hexap + counter * 0.02)
                    counter += 1

                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(
                        sample=name,
                        energy="%6.2f" % e,
                        ai="%3.2f" % ais,
                        wax=wa,
                        xbpm="%4.3f" % bpm,
                    )
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)

                name_fmt = "{sample}_{energy}eV_ai{ai}_pos2_wa{wax}_bpm{xbpm}"
                for e in energies[::-1]:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 120:
                        yield from bps.sleep(5)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(stage.x, xs_hexap + counter * 0.02)
                    counter += 1

                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(
                        sample=name,
                        energy="%6.2f" % e,
                        ai="%3.2f" % ais,
                        wax=wa,
                        xbpm="%4.3f" % bpm,
                    )
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)

            yield from bps.mv(stage.th, ai0)


def run_waxs_waitwater_2022_1(t=1):
    names = ["KClO4_flow_on_AuNps_2450eV"]
    user = "LR"
    det_exposure_time(t, t)
    waxs_arc = [0]
    # Detectors, motors:
    dets = [pil900KW]

    t0 = time.time()
    yield from bps.mv(waxs, waxs_arc)

    for t in np.linspace(0, 299, 300):

        name_fmt = "{sample}_{time}s"
        sample_name = name_fmt.format(sample=names[0], time="%.1f" % (time.time() - t0))
        sample_id(user_name=user, sample_name=sample_name)

        print(f"\n\t=== Sample: {sample_name} ===\n")
        yield from bp.count(dets, num=1)
        yield from bps.sleep(50)

    sample_id(user_name=user, sample_name=sample_name)
    print(f"\n\t=== Sample: {sample_name} ===\n")

    det_exposure_time(0.3, 0.3)


def Cl_edge_measurments_liquid_cell(t=1):
    dets = [pil900KW]
    det_exposure_time(t, t)

    name = "KClO4_2ndload_flowing_300ssleep"

    energies = [2800.0,2810.0,2820.0,2825.0,2830.0,2832.0,2834.0,2834.5,2835.0,2835.5,2836.0,2836.5,2837.0,2837.5,2838.0,
    2838.5,2839.0,2839.5,2840.0,2840.5,2841.0,2841.5,2845.0,2850.0,2855.0,2860.0,2865.0,2870.0,2875.0,2880.0,2890.0]

    waxs_arc = [23]

    for i, wa in enumerate(waxs_arc):
        yield from bps.mv(waxs, wa)
        counter = 0

        name_fmt = "{sample}_{energy}eV_wa{wax}_bpm{xbpm}"
        for e in energies:
            yield from bps.mv(energy, e)
            yield from bps.sleep(300)

            bpm = xbpm3.sumX.get()
            sample_name = name_fmt.format(
                sample=name, energy="%6.2f" % e, wax=wa, xbpm="%4.3f" % bpm
            )
            sample_id(user_name="LR", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)

    yield from bps.mv(energy, 2860)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 2830)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 2810)
    yield from bps.sleep(2)

    yield from bps.sleep(300)

    dets = [pil900KW]
    det_exposure_time(t, t)

    # names = ['KClO4']
    # name = 'KClO4_2ndload_flowing_300ssleep'

    energies = 0.25 + np.asarray([2800.0,2810.0,2820.0,2825.0,2830.0,2832.0,2834.0,2834.5,2835.0,2835.5,2836.0,2836.5,2837.0,2837.5,2838.0,
    2838.5,2839.0,2839.5,2840.0,2840.5,2841.0,2841.5,2845.0,2850.0,2855.0,2860.0,2865.0,2870.0,2875.0,2880.0,2890.0])

    waxs_arc = [23]

    for i, wa in enumerate(waxs_arc):
        yield from bps.mv(waxs, wa)
        counter = 0

        name_fmt = "{sample}_{energy}eV_wa{wax}_bpm{xbpm}"
        for e in energies:
            yield from bps.mv(energy, e)
            yield from bps.sleep(300)
            # yield from bps.mvr(stage.y, -0.02)
            # if xbpm2.sumX.get() < 120:
            #     yield from bps.sleep(5)
            #     yield from bps.mv(energy, e)
            #     yield from bps.sleep(2)

            bpm = xbpm2.sumX.get()
            sample_name = name_fmt.format(
                sample=name, energy="%6.2f" % e, wax=wa, xbpm="%4.3f" % bpm
            )
            sample_id(user_name="LR", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)

    yield from bps.mv(energy, 2860)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 2830)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 2810)
    yield from bps.sleep(2)


def PEDOT_Cl_edge_measurments_2022_1(t=1):
    dets = [pil1M, pil900KW, pil300KW]
    det_exposure_time(t, t)
    #
    # Doped PEDOT PSS Films (run on K) at Cl
    #
    names = [
        "Acid_PEDOT_neat",
        "Acid_PEDOT_n600mV",
        "Acid_PEDOT_p600mV",
        "Acid_PEDOT_exposed",
        "Acid_PEDOT_n300mV",
        "Acid_PEDOT_p300mV",
        "EG_PEDOT_neat",
        "   EG_PEDOT_n600mV",
        "EG_PEDOT_p600mV",
        "EG_PEDOT_exposed",
        "EG_PEDOT_n300mV",
        "Eg_PEDOT_p300mV",
    ]
    x_piezo = [
        -54000,
        -56402,
        -42402,
        -30402,
        -18402,
        -5402,
        7597,
        21597,
        34597,
        43594,
        55597,
        50597,
    ]
    x_hexap = [-15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15]
    y_piezo = [6100, 6100, 6100, 6100, 6100, 6100, 6100, 6100, 6100, 6100, 6100, 6100]

    assert len(x_piezo) == len(
        names
    ), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(
        y_piezo
    ), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(
        x_hexap
    ), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexap)})"

    energies = [
        2810.0,
        2820.0,
        2830.0,
        2832.0,
        2834.0,
        2834.5,
        2835.0,
        2835.5,
        2836.0,
        2836.5,
        2837.0,
        2837.5,
        2838.0,
        2838.5,
        2839.0,
        2839.5,
        2840.0,
        2840.5,
        2841.0,
        2841.5,
        2845.0,
        2850.0,
        2855.0,
        2860.0,
        2865.0,
        2870.0,
        2875.0,
        2880.0,
        2890.0,
    ]

    waxs_arc = [0, 20]
    ai0 = 0
    ai_list = [0.80]

    for name, xs, ys, xs_hexap in zip(names, x_piezo, y_piezo, x_hexap):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(stage.x, xs_hexap)

        yield from bps.mv(piezo.th, ai0)
        yield from alignement_gisaxs(0.4)

        yield from bps.mv(att2_9.open_cmd, 1)
        yield from bps.sleep(1)
        yield from bps.mv(att2_9.open_cmd, 1)

        ai0 = piezo.th.position
        det_exposure_time(t, t)

        for i, wa in enumerate(waxs_arc):

            # Do not take SAXS when WAXS detector in the way
            dets = [pil900KW, pil300KW] if wa < 10 else [pil1M, pil900KW, pil300KW]

            yield from bps.mv(waxs, wa)
            yield from bps.mv(piezo.x, xs)
            counter = 0

            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                name_fmt = "{sample}_{energy}eV_ai{ai}_pos1_wa{wax}_bpm{xbpm}"
                for e in energies:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 120:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs + counter * 30)
                    counter += 1

                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(
                        sample=name,
                        energy="%6.2f" % e,
                        ai="%3.2f" % ais,
                        wax=wa,
                        xbpm="%4.3f" % bpm,
                    )
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)
                yield from bps.mv(energy, 2860)  # step back gracefully
                yield from bps.sleep(2)
                yield from bps.mv(energy, 2830)
                yield from bps.sleep(2)
                yield from bps.mv(energy, 2810)
                yield from bps.sleep(2)

                # name_fmt = '{sample}_{energy}eV_ai{ai}_pos2_wa{wax}_bpm{xbpm}'
                # for e in energies[::-1]:
                #     yield from bps.mv(energy, e)
                #     yield from bps.sleep(2)
                #     if xbpm2.sumX.get() < 120:
                #         yield from bps.sleep(2)
                #         yield from bps.mv(energy, e)
                #         yield from bps.sleep(2)
                #     yield from bps.mv(piezo.x, xs + counter * 30)
                #     counter += 1


def Cl_edge_measurments_2022_1_hex(t=5, sample="test"):
    dets = [pil1M, pil900KW, pil300KW]
    det_exposure_time(t, t)

    names = [sample]
    x_hexap = [-27.6]

    assert len(x_hexap) == len(
        names
    ), f"Number of X coordinates ({len(x_hexap)}) is different from number of samples ({len(names)})"

    energies = [
        2810.0,
        2820.0,
        2830.0,
        2832.0,
        2834.0,
        2834.5,
        2835.0,
        2835.5,
        2836.0,
        2836.5,
        2837.0,
        2837.5,
        2838.0,
        2838.5,
        2839.0,
        2839.5,
        2840.0,
        2840.5,
        2841.0,
        2841.5,
        2845.0,
        2850.0,
        2855.0,
        2860.0,
        2865.0,
        2870.0,
        2875.0,
        2880.0,
        2890.0,
    ]

    waxs_arc = [0, 20]  # changed 2022_1 for propoer waxs center
    #   ai0 = 0
    ai_list = [1.00]  # aligned and set ai before

    for name, xs_hexap in zip(names, x_hexap):
        yield from bps.mv(stage.x, xs_hexap)

        #       yield from alignement_gisaxs_hex_roughsample(angle = 0.45) is already aligned

        ai0 = stage.th.position
        det_exposure_time(t, t)

        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)
            counter = 0

            for k, ais in enumerate(ai_list):
                #               yield from bps.mv(stage.th, ai0 + ais)

                name_fmt = "{sample}_{energy}eV_ai{ai}_pos1_wa{wax}_bpm{xbpm}"
                for e in energies:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 120:
                        yield from bps.sleep(5)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(stage.x, xs_hexap - counter * 0.00)
                    counter += 1

                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(
                        sample=name,
                        energy="%6.2f" % e,
                        ai="%3.2f" % ais,
                        wax=wa,
                        xbpm="%4.3f" % bpm,
                    )
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)

                # yield from bps.mv(stage.x, xs_hexap - counter * 0.10)

                # name_fmt = '{sample}_{energy}eV_ai{ai}_pos2_wa{wax}_bpm{xbpm}'
                # for e in energies[::-1]:

                #     yield from bps.mv(energy, e)
                #     yield from bps.sleep(2)
                #     if xbpm2.sumX.get() < 120:
                #         yield from bps.sleep(2)
                #         yield from bps.mv(energy, e)
                #         yield from bps.sleep(2)
                #     yield from bps.mv(piezo.x, xs_hexap - counter * 00)
                #     counter += 1

                #     bpm = xbpm2.sumX.get()
                #     sample_name = name_fmt.format(sample=name, energy='%6.2f'%e, ai ='%3.2f'%ais, wax = wa, xbpm = '%4.3f'%bpm)
                #     sample_id(user_name='LR', sample_name=sample_name)
                #     print(f'\n\t=== Sample: {sample_name} ===\n')
                #     yield from bp.count(dets, num=1)


#          yield from bps.mv(stage.th, ai0) #


# name_fmt = '{sample}_{energy}eV_ai{ai}_pos3_wa{wax}_bpm{xbpm}'
# for e in energies:
#     yield from bps.mv(energy, e)
#     yield from bps.sleep(2)
#     if xbpm2.sumX.get() < 120:
#         yield from bps.sleep(2)
#         yield from bps.mv(energy, e)
#         yield from bps.sleep(2)
#     yield from bps.mv(piezo.x, xs - counter * 30)
#     counter += 1

#     bpm = xbpm2.sumX.get()
#     sample_name = name_fmt.format(sample=name, energy='%6.2f'%e, ai ='%3.2f'%ais, wax = wa, xbpm = '%4.3f'%bpm)
#     sample_id(user_name='LR', sample_name=sample_name)
#     print(f'\n\t=== Sample: {sample_name} ===\n')
#     yield from bp.count(dets, num=1)

# name_fmt = '{sample}_{energy}eV_ai{ai}_pos4_wa{wax}_bpm{xbpm}'
# for e in energies[::-1]:
#     yield from bps.mv(energy, e)
#     yield from bps.sleep(2)
#     if xbpm2.sumX.get() < 120:
#         yield from bps.sleep(2)
#         yield from bps.mv(energy, e)
#         yield from bps.sleep(2)
#     yield from bps.mv(piezo.x, xs + counter * 30)
#     counter += 1

#     bpm = xbpm2.sumX.get()
#     sample_name = name_fmt.format(sample=name, energy='%6.2f'%e, ai ='%3.2f'%ais, wax = wa, xbpm = '%4.3f'%bpm)
#     sample_id(user_name='LR', sample_name=sample_name)
#     print(f'\n\t=== Sample: {sample_name} ===\n')
#     yield from bp.count(dets, num=1)


def Cl_edge_measurments_2022_1_hex_slide_only(t=5, sample="test"):
    dets = [pil1M, pil900KW, pil300KW]
    det_exposure_time(t, t)

    names = [sample]
    x_hexap = [-3.46]

    assert len(x_hexap) == len(
        names
    ), f"Number of X coordinates ({len(x_hexap)}) is different from number of samples ({len(names)})"

    energies = [
        2810.0,
        2820.0,
        2830.0,
        2832.0,
        2834.0,
        2834.5,
        2835.0,
        2835.5,
        2836.0,
        2836.5,
        2837.0,
        2837.5,
        2838.0,
        2838.5,
        2839.0,
        2839.5,
        2840.0,
        2840.5,
        2841.0,
        2841.5,
        2845.0,
        2850.0,
        2855.0,
        2860.0,
        2865.0,
        2870.0,
        2875.0,
        2880.0,
        2890.0,
    ]

    energies = [2810 for x in energies]

    waxs_arc = [0]  # changed 2022_1 for propoer waxs center
    #   ai0 = 0
    ai_list = [1.00]  # aligned and set ai before

    for name, xs_hexap in zip(names, x_hexap):
        yield from bps.mv(stage.x, xs_hexap)

        #       yield from alignement_gisaxs_hex_roughsample(angle = 0.45) is already aligned

        ai0 = stage.th.position
        det_exposure_time(t, t)

        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)
            counter = 0

            for k, ais in enumerate(ai_list):
                #               yield from bps.mv(stage.th, ai0 + ais)

                name_fmt = "{sample}_{energy}eV_ai{ai}_pos1_wa{wax}_bpm{xbpm}"
                for e in energies:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 120:
                        yield from bps.sleep(5)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(stage.x, xs_hexap - counter * 0.02)
                    counter += 1

                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(
                        sample=name,
                        energy="%6.2f" % e,
                        ai="%3.2f" % ais,
                        wax=wa,
                        xbpm="%4.3f" % bpm,
                    )
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)

    yield from bps.mv(energy, 2860)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 2830)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 2810)
    yield from bps.sleep(2)





def Cl_edge_measurments_2022_3_hex(t=5, x=0, sample="test"):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    names = [sample]
    x_hexap = [x]
    assert len(x_hexap) == len(names), f"Number of X coordinates ({len(x_hexap)}) is different from number of samples ({len(names)})"

    energies = [2810.0, 2820.0, 2830.0, 2832.0, 2834.0, 2834.5, 2835.0, 2835.5, 2836.0, 2836.5, 2837.0, 2837.5, 2838.0, 2838.5, 2839.0,
    2839.5, 2840.0, 2840.5, 2841.0, 2841.5, 2845.0, 2850.0, 2855.0, 2860.0, 2865.0, 2870.0, 2875.0, 2880.0, 2890.0]

    waxs_arc = [0, 20]  # changed 2022_1 for proper waxs center
    ai_list = [0.8]  # aligned and set ai before

    for name, xs_hexap in zip(names, x_hexap):
        yield from bps.mv(stage.x, xs_hexap)

        yield from alignement_gisaxs_hex(angle = 0.8)

        ai0 = stage.th.position
        det_exposure_time(t, t)
        
        yield from bps.mv(stage.th, ai0 + ai_list[0])

        for i, wa in enumerate(waxs_arc):

            yield from bps.mv(waxs, wa)
            dets = [pil900KW] if waxs.arc.position < 15 else [pil900KW, pil1M]

            counter = 0


            name_fmt = "{sample}_pos1_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
            for e in energies:
                yield from bps.mv(energy, e)
                yield from bps.sleep(2)
                if xbpm2.sumX.get() < 50:
                    yield from bps.sleep(5)
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                yield from bps.mv(stage.x, xs_hexap + counter * 0.04)
                counter += 1

                bpm = xbpm2.sumX.get()
                sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, ai="%3.2f"%ai_list[0], wax=wa, xbpm="%4.3f"%bpm)
                sample_id(user_name="LR", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

            
            name_fmt = "{sample}_pos2_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
            for e in energies[::-1]:
                yield from bps.mv(energy, e)
                yield from bps.sleep(2)
                if xbpm2.sumX.get() < 50:
                    yield from bps.sleep(5)
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                yield from bps.mv(stage.x, xs_hexap + counter * 0.04)
                counter += 1

                bpm = xbpm3.sumX.get()
                sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, ai="%3.2f"%ai_list[0], wax=wa, xbpm="%4.3f"%bpm)
                sample_id(user_name="LR", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

        yield from bps.mv(stage.th, ai0)

    yield from bps.sleep(60)


def Cl_edge_measurments_2022_3_hex2(t=5, x=0, sample="test"):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    names = [sample]
    x_hexap = [x]
    assert len(x_hexap) == len(names), f"Number of X coordinates ({len(x_hexap)}) is different from number of samples ({len(names)})"

    # energies = -7+np.asarray([2810.0, 2820.0, 2830.0, 2832.0, 2834.0, 2834.5, 2835.0, 2835.5, 2836.0, 2836.5, 2837.0, 2837.5, 2838.0, 2838.5, 2839.0,
    # 2839.5, 2840.0, 2840.5, 2841.0, 2841.5, 2845.0, 2850.0, 2855.0, 2860.0, 2865.0, 2870.0, 2875.0, 2880.0, 2890.0])

    energies = [2810.0, 2820.0, 2830.0, 2832.0, 2834.0, 2834.5, 2835.0, 2835.5, 2836.0, 2836.5, 2837.0, 2837.5, 2838.0, 2838.5, 2839.0,
    2839.5, 2840.0, 2840.5, 2841.0, 2841.5, 2845.0, 2850.0, 2855.0, 2860.0, 2865.0, 2870.0, 2875.0, 2880.0, 2890.0]

    waxs_arc = [20]  # changed 2022_1 for proper waxs center
    # waxs_arc = [0, 20]  # changed 2022_1 for proper waxs center
    ai_list = [1]  # aligned and set ai before

    for name, xs_hexap in zip(names, x_hexap):
        yield from bps.mv(stage.x, xs_hexap)

        yield from alignement_gisaxs_hex(angle = 0.4)
        yield from bps.mv(stage.x, xs_hexap-0.05)

        ai0 = stage.th.position
        det_exposure_time(t, t)
        
        yield from bps.mv(stage.th, ai0 + ai_list[0])

        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)
            dets = [pil900KW] if waxs.arc.position < 15 else [pil900KW, pil1M]

            counter = 0

            name_fmt = "{sample}_pos1_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
            for e in energies:
                yield from bps.mv(energy, e)
                yield from bps.sleep(2)
                if xbpm2.sumX.get() < 50:
                    yield from bps.sleep(5)
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                yield from bps.mv(stage.x, xs_hexap - counter * 0.03)
                counter += 1

                bpm = xbpm3.sumX.get()
                sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, ai="%3.2f"%ai_list[0], wax=wa, xbpm="%4.3f"%bpm)
                sample_id(user_name="LR", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

            name_fmt = "{sample}_pos2_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
            for e in energies[::-1]:
                yield from bps.mv(energy, e)
                yield from bps.sleep(2)
                if xbpm2.sumX.get() < 50:
                    yield from bps.sleep(5)
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                yield from bps.mv(stage.x, xs_hexap - counter * 0.03)
                counter += 1

                bpm = xbpm3.sumX.get()
                sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, ai="%3.2f"%ai_list[0], wax=wa, xbpm="%4.3f"%bpm)
                sample_id(user_name="LR", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

        yield from bps.mv(stage.th, ai0)

    yield from bps.sleep(60)


def Cl_edge_measurments_2022_3_fullcycle(t=1, sample="test"):
    # yield from Cl_edge_measurments_2022_3_hex2(1, x=10, sample='Load5inner_MM460_160C_100mMKClO4_dope_0p6V_1')
    # yield from Cl_edge_measurments_2022_3_hex2(1, x=11.8, sample='Load5inner_MM460_160C_100mMKClO4_dope_0p4V_2')
    yield from Cl_edge_measurments_2022_3_hex2(1, x=13.5, sample='Load5inner_MM460_160C_100mMKClO4_dope_0p6V_3')

    # yield from Cl_edge_measurments_2022_3_hex2(1, x=-18, sample='MM389repeat_160C_100mMKClO4_dedope_n0p6_2')
    # yield from Cl_edge_measurments_2022_3_hex2(1, x=-16, sample='MM389repeat_160C_100mMKClO4_dope_0p6V_3')
    # yield from Cl_edge_measurments_2022_3_hex2(1, x=-14, sample='MM389repeat_160C_100mMKClO4_mid_0V_4')
    # yield from Cl_edge_measurments_2022_3_hex2(1, x=-14, sample='MM389repeat_160C_100mMKClO4_dedope_n0p6_5')
    # yield from Cl_edge_measurments_2022_3_hex(1, x=-14, sample='MM389_165C_100mMKClO4_mid_0V_5')
    # yield from Cl_edge_measurments_2022_3_hex(1, x=-13, sample='MM389_165C_100mMKClO4_dedope_n0p5V_6')



def Cl_edge_measurments_2022_3_no_energy(t=1, sample="test"):
    yield from bps.mvr(stage.th, 1)
    yield from bps.mv(waxs, 20)


    # dets = [OAV2_writing, pil900KW]
    dets = [OAV2_writing, pil1M]

    det_exposure_time(t, t)

    names = [sample]
    
    for i in range(1000):
        name_fmt = "{sample}_2810.00eV_ai0.8_wa18_num{filenum}"
        sample_name = name_fmt.format(sample=names[0], filenum="%4.4d"%i)
        sample_id(user_name="LR", sample_name=sample_name)
        yield from bp.count(dets, num=1)
    
    yield from bps.mvr(stage.th, 1)





def Cl_edge_measurments_2022_3(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    names = ['MM389_0p6V_KClO4',    'MM460_0p6V_KClO4', 'MM460_usedfrit_0p6V_KClO4', 'blankFrit', 'PSorPVC', 'PSorPVC2']
    x_piezo = [          -38000,                -26000,                      -15000,       -3000,     12000,      35000]
    x_hexap = [               0,                     0,                           0,           0,         0,          0]
    y_piezo = [            5500,                  5500,                        5500,        5500,      5500,       5500]


    # names = ['P3DT_un',         'PBTTT_un', 'PR41_un', 'halfP3MEEMT_un', 'P3PAAT_un', 'P3AAPT_un', 'P3MEEMT_un', 
    #  'P3DT_1p2V_KCLO4', 'PBTTT_1p2V_KClO4', 'RP41_0p7_KClO4','halfP3MEEMT_0.7V_KClO4', 'P3PAAT_0p7_KClO4', 'P3AAPT_0p7_KClO4', 'P3MEEMT_0p7_KClO4']
    # x_piezo = [ -55000,             -53000, -41000, -29000, -17000, -2000, 11000, 
    #             -55000,             -53000, -41000, -29000, -17000, -2000, 11000]
    # x_hexap = [    -10,                  0,      0,      0,      0,     0,     0,
    #                -10,                  0,      0,      0,      0,     0,     0]
    # y_piezo = [   5500,               5500,   5500,   5500,   5500,  5500,  5500, 
    #              -3500,              -3500,  -3500,  -3500,  -3500, -3500, -3500]
    # z_piezo = [  -1000,              -1000,  -1000,  -1000,  -1000, -1000, -1000,
    #               3000,               3000,   3000,   3000,   3000,  3000,  3000]

    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(x_hexap), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexap)})"

    energies = np.asarray([2810.0, 2820.0, 2830.0, 2832.0, 2834.0, 2834.5, 2835.0, 2835.5, 2836.0, 2836.5, 2837.0, 2837.5, 2838.0, 2838.5, 2839.0,
    2839.5, 2840.0, 2840.5, 2841.0, 2841.5, 2845.0, 2850.0, 2855.0, 2860.0, 2865.0, 2870.0, 2875.0, 2880.0, 2890.0])

    waxs_arc = [0, 20]
    ai0 = 0
    ai_list = [0.80]

    for name, xs, ys, xs_hexap in zip(names, x_piezo, y_piezo, x_hexap):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(stage.x, xs_hexap)
        
        yield from bps.mv(piezo.th, ai0)
        yield from alignement_gisaxs_doblestack(0.8)

        ai0 = piezo.th.position
        det_exposure_time(t, t)

        for i, wa in enumerate(waxs_arc):
            # Do not take SAXS when WAXS detector in the way

            yield from bps.mv(waxs, wa)

            dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]

            yield from bps.mv(piezo.x, xs)
            counter = 0

            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                name_fmt = "{sample}_pos1_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs + counter * 50)
                    counter += 1

                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name, energy="%6.2f" % e,ai="%3.2f" % ais, wax=wa,xbpm="%4.3f" % bpm)
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)


                name_fmt = "{sample}_pos2_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies[::-1]:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs + counter * 50)
                    counter += 1

                    bpm = xbpm3.sumX.get()
                    sample_name = name_fmt.format(sample=name,energy="%6.2f" % e,ai="%3.2f" % ais,wax=wa,xbpm="%4.3f" % bpm,)
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)
            yield from bps.mv(piezo.th, ai0)



def S_edge_measurments_2022_3(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    # names = ['P3DT_un',         'PBTTT_un', 'PR41_un', 'halfP3MEEMT_un', 'P3PAAT_un', 'P3AAPT_un', 'P3MEEMT_un', 
    #  'P3DT_1p2V_KCLO4', 'PBTTT_1p2V_KClO4', 'RP41_0p7_KClO4','halfP3MEEMT_0.7V_KClO4', 'P3PAAT_0p7_KClO4', 'P3AAPT_0p7_KClO4', 'P3MEEMT_0p7_KClO4']
    # x_piezo = [ -55000,             -53000, -41000, -29000, -17000, -2000, 11000, 
    #             -55000,             -53000, -41000, -29000, -17000, -2000, 11000]
    # x_hexap =2+np.asarray([    -10,                  0,      0,      0,      0,     0,     0,
    #                -10,                  0,      0,      0,      0,     0,     0])
    # y_piezo = [   5500,               5500,   5500,   5500,   5500,  5500,  5500, 
    #              -3500,              -3500,  -3500,  -3500,  -3500, -3500, -3500]
    # z_piezo = [  -1000,              -1000,  -1000,  -1000,  -1000, -1000, -1000,
    #               3000,               3000,   3000,   3000,   3000,  3000,  3000]

    names = ['AcidPEDOTPSS_as',    'AcidPEDOTPSS_exposed', 'AcidPEDOTPSS_0V', 'AcidPEDOTPSS_dedope_n0p6', 'AcidPEDOTPSS_overdope_p0p6', 'AcidPEDOTPSS_NaCl', 'AcidPEDOTPSS_NaBr', 'AcidPEDOTPSS_RbCl', 'AcidPEDOTPSS_RbBr', 'StandardPEDOTPSS_as', 'StandardPEDOTPSS_RbBr', 'StandardPEDOTPSS_NaBr',
     'P3MEEMT23k115C_0p7_KTFSI', 'P3MEEMT23k115C_0p4_KTFSI', 'P3MEEMT23k115C_un','RivnayFrit_P3MEEET_drop', 'LiTFSI_PEDOTPSS_as', 'LiTFSI_PEDOTPSS_exposed', 'LiTFSI_PEDOTPSS_0V', 'LiTFSI_PEDOTPSS_dedoped_n0p6', 'LiTFSI_PEDOTPSS_redoped_0V', 'LiTFSI_PEDOTPSS_overdoped_p0p6V', 'LiTFSI_PEDOTPSS_RbBr']
    x_piezo = [ -55000,             -55000, -46000, -35000, -24000, -8000, 5000, 17000, 27000, 43000, 52000, 52000,
                -55000,             -50000, -35000, -18000,  -8000, 2000, 17000, 27000, 37000, 47000, 52000]
    x_hexap = [    -10,                  0,      0,      0,      0,     0,     0,    0,     0,     0,     2,    12,
                   -10,                  0,      0,      0,      0,     0,     0,    0,     0,     0,     5]
    y_piezo = [   5500,               5500,   5500,   5500,   5500,  5500,  5500, 5500,  5500,  5500,  5500,  5500, 
                 -3500,              -3500,  -3500,  -3500,  -3500, -3500, -3500,-3500, -3500, -3500, -3500]


    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(x_hexap), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexap)})"

    energies = [2450.0,2455.0,2460.0,2465.0,2470.0,2473.0,2475.0,2475.5,2476.0,2476.5,2477.0,2477.5,2478.0,2478.5,2479.0,2479.5,2480.0,2480.5,
    2483.0,2485.0,2487.5,2490.0,2492.5,2495.0,2500.0,2510.0,2515.0]
    waxs_arc = [0, 20]
    ai0 = 0
    ai_list = [0.80]

    for name, xs, ys, xs_hexap in zip(names, x_piezo, y_piezo, x_hexap):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(stage.x, xs_hexap)

        yield from bps.mv(piezo.th, ai0)
        yield from alignement_gisaxs_doblestack(0.8)

        ai0 = piezo.th.position
        det_exposure_time(t, t)

        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)
            # Do not take SAXS when WAXS detector in the way
            dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]

            yield from bps.mv(piezo.x, xs)
            counter = 0

            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                name_fmt = "{sample}_pos1_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs + counter * 50)
                    counter += 1

                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name, energy="%6.2f" % e,ai="%3.2f" % ais, wax=wa,xbpm="%4.3f" % bpm)
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)


                name_fmt = "{sample}_pos2_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies[::-1]:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs + counter * 50)
                    counter += 1

                    bpm = xbpm3.sumX.get()
                    sample_name = name_fmt.format(sample=name,energy="%6.2f" % e,ai="%3.2f" % ais,wax=wa,xbpm="%4.3f" % bpm,)
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)
            yield from bps.mv(piezo.th, ai0)




    # names= ['P3MEEMT_1p5V_KT4ClB', 'P3HTreg_1p5V_KT4ClB', 'P3MEEMTrr_KT4ClB', 'P3MEEMTrrand_KT4ClB', 'P3MEEMT_DDQ1mgml', 'P3MEEMT_DDQ2p5mgml', 'P3MEEMT_DDQ5mgml']
    # x_piezo = [              28000,                 41000,              51000,                 52000,              28000,                43000, 51000]
    # x_hexap = 2+np.asarray([                  0,                     0,                  2,                    10,                  0,                    0,     7])
    # y_piezo = [               5500,                  5500,               5500,                  5500,              -3500,                -3500,  -3500]
    # z_piezo = [              -1000,                 -1000,              -1000,                 -1000,               3000,                 3000, 3000]


    # assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    # assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    # assert len(x_piezo) == len(x_hexap), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexap)})"

    # waxs_arc = [0, 20]
    # ai0 = 0
    # ai_list = [0.80]

    # for name, xs, ys, xs_hexap in zip(names, x_piezo, y_piezo, x_hexap):
    #     yield from bps.mv(piezo.x, xs)
    #     yield from bps.mv(piezo.y, ys)
    #     yield from bps.mv(stage.x, xs_hexap)

    #     yield from bps.mv(piezo.th, ai0)
    #     yield from alignement_gisaxs_doblestack(0.8)

    #     ai0 = piezo.th.position
    #     det_exposure_time(t, t)

    #     for i, wa in enumerate(waxs_arc):
    #         # Do not take SAXS when WAXS detector in the way
    #         dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]

    #         yield from bps.mv(waxs, wa)
    #         yield from bps.mv(piezo.x, xs)
    #         counter = 0

    #         for k, ais in enumerate(ai_list):
    #             yield from bps.mv(piezo.th, ai0 + ais)

    #             name_fmt = "{sample}_pos1_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
    #             for e in energies:
    #                 yield from bps.mv(energy, e)
    #                 yield from bps.sleep(2)
    #                 if xbpm2.sumX.get() < 50:
    #                     yield from bps.sleep(2)
    #                     yield from bps.mv(energy, e)
    #                     yield from bps.sleep(2)
    #                 yield from bps.mv(piezo.x, xs + counter * 30)
    #                 counter += 1

    #                 bpm = xbpm2.sumX.get()
    #                 sample_name = name_fmt.format(sample=name, energy="%6.2f" % e,ai="%3.2f" % ais, wax=wa,xbpm="%4.3f" % bpm)
    #                 sample_id(user_name="LR", sample_name=sample_name)
    #                 print(f"\n\t=== Sample: {sample_name} ===\n")
    #                 yield from bp.count(dets, num=1)


    #             name_fmt = "{sample}_pos2_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
    #             for e in energies[::-1]:
    #                 yield from bps.mv(energy, e)
    #                 yield from bps.sleep(2)
    #                 if xbpm2.sumX.get() < 50:
    #                     yield from bps.sleep(2)
    #                     yield from bps.mv(energy, e)
    #                     yield from bps.sleep(2)
    #                 yield from bps.mv(piezo.x, xs + counter * 30)
    #                 counter += 1

    #                 bpm = xbpm3.sumX.get()
    #                 sample_name = name_fmt.format(sample=name,energy="%6.2f" % e,ai="%3.2f" % ais,wax=wa,xbpm="%4.3f" % bpm,)
    #                 sample_id(user_name="LR", sample_name=sample_name)
    #                 print(f"\n\t=== Sample: {sample_name} ===\n")
    #                 yield from bp.count(dets, num=1)
    #         yield from bps.mv(piezo.th, ai0)




def night_2022_3(t=1):
    proposal_id("2022_3", "310999_Richter9")
    yield from Cl_edge_measurments_2022_3(t=1)
    yield from transition_Cl_S_edges()
    proposal_id("2022_3", "311003_Freychet6")
    yield from S_edge_measurments_2022_3_guillaume(t=1)



def K_edge_measurments_2022_3(t=0.5):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    # names = ['AcidPEDOTPSS_as',    'AcidPEDOTPSS_exposed', 'AcidPEDOTPSS_0V', 'AcidPEDOTPSS_dedope_n0p6', 'AcidPEDOTPSS_overdope_p0p6', 'AcidPEDOTPSS_NaCl', 'AcidPEDOTPSS_NaBr', 'AcidPEDOTPSS_RbCl', 'AcidPEDOTPSS_RbBr', 'StandardPEDOTPSS_as', 'StandardPEDOTPSS_RbBr', 'StandardPEDOTPSS_NaBr',
    #  'P3MEEMT23k115C_0p7_KTFSI', 'P3MEEMT23k115C_0p4_KTFSI', 'P3MEEMT23k115C_un', 'LiTFSI_PEDOTPSS_as', 'LiTFSI_PEDOTPSS_exposed', 'LiTFSI_PEDOTPSS_0V', 'LiTFSI_PEDOTPSS_dedoped_n0p6', 'LiTFSI_PEDOTPSS_redoped_0V', 'LiTFSI_PEDOTPSS_overdoped_p0p6V', 'LiTFSI_PEDOTPSS_RbBr']
    # x_piezo = [ -55000,             -55000, -46000, -35000, -24000, -8000, 5000, 17000, 27000, 43000, 52000, 52000,
    #             -55000,             -50000, -35000,  -8000, 2000, 17000, 27000, 37000, 47000, 52000]
    # x_hexap = [    -10,                  0,      0,      0,      0,     0,     0,    0,     0,     0,     2,    12,
    #                -10,                  0,      0,      0,     0,     0,    0,     0,     0,     5]
    # y_piezo = [   5500,               5500,   5500,   5500,   5500,  5500,  5500, 5500,  5500,  5500,  5500,  5500, 
    #              -3500,              -3500,  -3500,  -3500, -3500, -3500,-3500, -3500, -3500, -3500]

    names = ['BBLn0p5', 'BBLn0p9']
    x_piezo = [ -49000,    -46000]
    x_hexap = [    -10,         0]
    y_piezo = [   5500,      5500]

    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(x_hexap), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexap)})"

    energies = np.asarray(np.arange(3590, 3611, 5).tolist()+ np.arange(3612, 3629, 0.4).tolist()+ np.arange(3630, 3721, 5).tolist())

    waxs_arc = [0, 20]
    ai0 = 0
    ai_list = [0.80]

    for name, xs, ys, xs_hexap in zip(names, x_piezo, y_piezo, x_hexap):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(stage.x, xs_hexap)

        yield from bps.mv(piezo.th, ai0)
        yield from alignement_gisaxs_doblestack(0.8)

        yield from bps.mv(att2_9.open_cmd, 1)
        yield from bps.sleep(1)
        yield from bps.mv(att2_9.open_cmd, 1)

        ai0 = piezo.th.position
        det_exposure_time(t, t)

        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)
            # Do not take SAXS when WAXS detector in the way
            dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]
            
            yield from bps.mv(piezo.x, xs)
            counter = 0

            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                name_fmt = "{sample}_pos1_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs - counter * 30)
                    counter += 1

                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name,energy="%6.2f" % e,ai="%3.2f" % ais,wax=wa,xbpm="%4.3f" % bpm,)
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)

                yield from bps.mv(energy, 3680)
                yield from bps.sleep(3)
                yield from bps.mv(energy, 3640)
                yield from bps.sleep(3)
                yield from bps.mv(energy, 3590)
                yield from bps.sleep(3)
        
        yield from bps.mv(piezo.th, ai0)


                # name_fmt = '{sample}_{energy}eV_ai{ai}_pos2_wa{wax}_bpm{xbpm}'
                # for e in energies[::-1]:
                #     yield from bps.mv(energy, e)
                #     yield from bps.sleep(2)
                #     if xbpm2.sumX.get() < 120:
                #         yield from bps.sleep(2)
                #         yield from bps.mv(energy, e)
                #         yield from bps.sleep(2)
                #     yield from bps.mv(piezo.x, xs - counter * 30)
                #     counter += 1

                #     bpm = xbpm2.sumX.get()
                #     sample_name = name_fmt.format(sample=name, energy='%6.2f'%e, ai ='%3.2f'%ais, wax = wa, xbpm = '%4.3f'%bpm)
                #     sample_id(user_name='LR', sample_name=sample_name)
                #     print(f'\n\t=== Sample: {sample_name} ===\n')
                #     yield from bp.count(dets, num=1)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)





def S_edge_measurments_2022_3_guillaume(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)


    names = [    'A1',   'A2',    'A3',   'A4',   'A5',   'A6',  'B1',  'B2',  'B3',  'B4',  'B5',  'B6']
    x_piezo = [ 47000,   52000, -54000, -49000, -35000, -21000, -7000,  8000, 23000, 38000, 49000, 52000]
    x_hexap = [     0,      10,    -10,      0,      0,      0,     0,     0,     0,     0,     0,    10]
    y_piezo = [  5500,    5500,  -3500,  -3500,  -3500,  -3500, -3500, -3500, -3500, -3500, -3500, -3500]


    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(x_hexap), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexap)})"

    energies = np.arange(2450, 2470, 5).tolist()+ np.arange(2470, 2480, 0.25).tolist()+ np.arange(2480, 2490, 1).tolist()+ np.arange(2490, 2501, 5).tolist()
    waxs_arc = [0, 20, 40]
    ai0 = 0
    ai_list = [0.80]

    for name, xs, ys, xs_hexap in zip(names, x_piezo, y_piezo, x_hexap):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(stage.x, xs_hexap)

        yield from bps.mv(piezo.th, ai0)
        yield from alignement_gisaxs_doblestack(0.8)

        ai0 = piezo.th.position
        det_exposure_time(t, t)

        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)
            # Do not take SAXS when WAXS detector in the way
            dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]

            yield from bps.mv(piezo.x, xs)
            counter = 0

            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                name_fmt = "{sample}_pos1_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs + counter * 50)
                    counter += 1

                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name, energy="%6.2f" % e,ai="%3.2f" % ais, wax=wa,xbpm="%4.3f" % bpm)
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)

            yield from bps.mv(piezo.th, ai0)





def S_edge_measurments_2023_1(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    names = ['nov_AcidPEDOTPSS_n0p6', 'feb_AcidPEDOTPSS_as', 'new_AcidPEDOTPSS_as']
    x_piezo = [ 15000,-1000, -16000]
    y_piezo = [  5200, 5200,   5200]
    z_piezo = [  7000, 7000,   7000]

    names = ['nov_AcidPEDOTPSS_n0p6']
    x_piezo = [ 15000]
    y_piezo = [  5200]
    z_piezo = [  7000]

    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(z_piezo)})"

    energies = [2450.0,2455.0,2460.0,2465.0,2470.0,2473.0,2475.0,2475.5,2476.0,2476.5,2477.0,2477.5,2478.0,2478.5,2479.0,2479.5,2480.0,2480.5,
    2483.0,2485.0,2487.5,2490.0,2492.5,2495.0,2500.0,2510.0,2515.0]
    waxs_arc = [0, 20]
    ai0 = 0
    ai_list = [0.80]

    for name, xs, ys, zs in zip(names, x_piezo, y_piezo, z_piezo):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)

        yield from bps.mv(piezo.th, ai0)
        yield from alignement_gisaxs(0.8)

        ai0 = piezo.th.position
        det_exposure_time(t, t)

        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)
            # Do not take SAXS when WAXS detector in the way
            dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]

            yield from bps.mv(piezo.x, xs)
            counter = 0

            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                name_fmt = "{sample}_pos1_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs + counter * 50)
                    counter += 1
                    
                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name, energy="%6.2f" % e,ai="%3.2f" % ais, wax=wa,xbpm="%4.3f" % bpm)
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)


                name_fmt = "{sample}_pos2_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies[::-1]:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs + counter * 50)
                    counter += 1

                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name,energy="%6.2f" % e,ai="%3.2f" % ais,wax=wa,xbpm="%4.3f" % bpm,)
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)
            yield from bps.mv(piezo.th, ai0)





def S_edge_measurments_2023_1_energyshiftstudy(t=1):
    dets = [pil1M, pil900KW]

    det_exposure_time(t, t)

    names = ['nov_AcidPEDOTPSS_n0p6_test_lqrgeoffset']
    x_piezo = [ 15000]
    y_piezo = [  5200]
    z_piezo = [  7000]

    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(z_piezo)})"

    energies = [2450.0,2455.0,2460.0,2465.0,2470.0,2473.0,2475.0,2475.5,2476.0,2476.5,2477.0,2477.5,2478.0,2478.5,2479.0,2479.5,
    2480.0,2480.5,2481.0,2482.0,2483.0,2484.0,2485.0,2486.0, 2487.0,2488.0,2489.0,2490.0,2492.5,2495.0,2500.0,2510.0,2515.0]

    # energies = [2470.0,2475.0,2476.5,2477.0,2478.5,2480.0, 2483.0,2485.0,2487.5]

    waxs_arc = [0, 20]
    waxs_arc = [20]

    ai0 = 0
    ai_list = [0.80]

    for name, xs, ys, zs in zip(names, x_piezo, y_piezo, z_piezo):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)

        # yield from bps.mv(piezo.th, ai0)
        # yield from alignement_gisaxs(0.8)

        # ai0 = piezo.th.position
        det_exposure_time(t, t)

        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)
            # Do not take SAXS when WAXS detector in the way
            dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]
            dets = [pil900KW]

            yield from bps.mv(piezo.x, xs)
            counter = 0

            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                # name_fmt = "{sample}_pos1_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                # for e in energies:
                #     yield from bps.mv(energy, e)
                #     yield from bps.sleep(2)
                #     # if xbpm2.sumX.get() < 50:
                #     #     yield from bps.sleep(2)
                #     #     yield from bps.mv(energy, e)
                #     #     yield from bps.sleep(2)
                #     yield from bps.mv(piezo.x, xs + counter * 50)
                #     counter += 1
                    
                #     bpm = xbpm2.sumX.get()
                #     ener = energy.energy.position

                #     sample_name = name_fmt.format(sample=name, energy="%6.2f"%ener, ai="%3.2f" % ais, wax=wa,
                #                                 xbpm="%4.3f"%bpm)
                #     sample_id(user_name="LR", sample_name=sample_name)
                #     print(f"\n\t=== Sample: {sample_name} ===\n")
                #     yield from bp.count(dets, num=1)

                # yield from bp.count(dets, num=1)
                # yield from bp.count(dets, num=1)

                counter = 0
                name_fmt = "{sample}_pos2_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies[::-1]:
                    # yield from bps.mv(energy, e-5)
                    # yield from bps.sleep(2)
                    while abs(energy.energy.position-2450)>20: 
                        yield from bps.mv(energy, energy.energy.position-20)
                        yield from bps.sleep(2)
                    yield from bps.mv(energy, 2450)
                    yield from bps.sleep(2)
                    while abs(e-energy.energy.position)>20: 
                        yield from bps.mv(energy, energy.energy.position+10)
                        yield from bps.sleep(2)

                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    # if xbpm2.sumX.get() < 50:
                    #     yield from bps.sleep(2)
                    #     yield from bps.mv(energy, e)
                    #     yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs + counter * 50)
                    counter += 1

                    bpm = xbpm2.sumX.get()
                    ener = energy.energy.position

                    sample_name = name_fmt.format(sample=name, energy="%6.2f"%ener, ai="%3.2f"%ais, wax=wa,
                                                xbpm="%4.3f"%bpm)                    
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)
            yield from bps.mv(piezo.th, ai0)




def S_edge_measurments_2023_1_night1(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    names = ['EG_PEDOTPSS_as', 'EG_PEDOTPSS_exp','EG_PEDOTPSS_dedope','EG_PEDOTPSS_redope','EG_PEDOTPSS_overdope','acid_PEDOTPSS_as', 'acid_PEDOTPSS_exp','acid_PEDOTPSS_dedope','acid_PEDOTPSS_redope','acid_PEDOTPSS_overdope',      'NaPSS',          'PVC',  'Si',
                 'P3MEEET_as', 'P3MEEET_exp_KCl',  'P3MEEET_dope_KCl','P3MEEET_dedope_KCl',            'InDTP_as',       'InDTP_exp',        'InDTP_dope',        'InDTP_dedope',           'OutDTP_as',            'OutDTP_exp','OutDTP_dope','OutDTP_dedope']
    x_piezo = [        -55000,            -51000,              -41000,              -31000,                -19000,             -7000,                5000,                 16000,                 28000,                   40000,        49000,          52000,-16000,
                       -55000,            -51000,              -41000,              -31000,                -19000,             -7000,                5000,                 16000,                 28000,                   40000,        52000,          52000, ]
    x_hexa = [            -10,                 0,                   0,                   0,                     0,                 0,                   0,                     0,                     0,                       0,            0,              7,    16,
                          -10,                 0,                   0,                   0,                     0,                 0,                   0,                     0,                     0,                       0,            0,             12]
    y_piezo = [          5100,              5100,                5100,                5100,                  5100,              5100,                5100,                  5100,                  5100,                    5100,         5100,           5100,  5100,
                        -3700,             -3700,               -3700,               -3700,                 -3700,             -3700,               -3700,                 -3700,                 -3700,                   -3700,        -3700,          -3700]
    z_piezo = [          7000,              7000,                7000,                7000,                  7000,              7000,                7000,                  7000,                  7000,                    7000,         7000,           7000,  7000,
                         7000,              7000,                7000,                7000,                  7000,              7000,                7000,                  7000,                  7000,                    7000,         7000,           7000]

    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(z_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexa)})"

    energies = [2450.0,2455.0,2460.0,2465.0,2470.0,2473.0,2475.0,2475.5,2476.0,2476.5,2477.0,2477.5,2478.0,2478.5,2479.0,2479.5,
    2480.0,2480.5,2481.0,2482.0,2483.0,2484.0,2485.0,2486.0, 2487.0,2488.0,2489.0,2490.0,2492.5,2495.0,2500.0,2510.0,2515.0]

    waxs_arc = [0, 20]
    ai0 = 0
    ai_list = [0.80]

    for name, xs, ys, zs, xs_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa):
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)

        yield from bps.mv(piezo.th, ai0)
        yield from alignement_gisaxs_doblestack(0.8)

        ai0 = piezo.th.position
        det_exposure_time(t, t)

        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)
            # Do not take SAXS when WAXS detector in the way
            dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]

            yield from bps.mv(piezo.x, xs)
            counter = 0

            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                name_fmt = "{sample}_pos1_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs + counter * 30)
                    counter += 1
                    
                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)


                name_fmt = "{sample}_pos2_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies[::-1]:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs + counter * 30)
                    counter += 1

                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)

            yield from bps.mv(piezo.th, ai0)



def Cl_edge_measurments_2023_1_night1(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    # names = ['EG_PEDOTPSS_as', 'EG_PEDOTPSS_exp','EG_PEDOTPSS_dedope','EG_PEDOTPSS_redope','EG_PEDOTPSS_overdope','acid_PEDOTPSS_as', 'acid_PEDOTPSS_exp','acid_PEDOTPSS_dedope','acid_PEDOTPSS_redope','acid_PEDOTPSS_overdope',      'NaPSS',          'PVC',  'Si',
    #              'P3MEEET_as', 'P3MEEET_exp_KCl',  'P3MEEET_dope_KCl','P3MEEET_dedope_KCl',            'InDTP_as',       'InDTP_exp',        'InDTP_dope',        'InDTP_dedope',           'OutDTP_as',            'OutDTP_exp','OutDTP_dope','OutDTP_dedope']
    # x_piezo = [        -55000,            -51000,              -41000,              -31000,                -19000,             -7000,                5000,                 16000,                 28000,                   40000,        49000,          52000, 52000,
    #                    -55000,            -51000,              -41000,              -31000,                -19000,             -7000,                5000,                 16000,                 28000,                   40000,        52000,          52000, ]
    # x_hexa = [            -10,                 0,                   0,                   0,                     0,                 0,                   0,                     0,                     0,                       0,            0,              7,    16,
    #                       -10,                 0,                   0,                   0,                     0,                 0,                   0,                     0,                     0,                       0,            0,             12]
    # y_piezo = [          5100,              5100,                5100,                5100,                  5100,              5100,                5100,                  5100,                  5100,                    5100,         5100,           5100,  5100,
    #                     -3700,             -3700,               -3700,               -3700,                 -3700,             -3700,               -3700,                 -3700,                 -3700,                   -3700,        -3700,          -3700]
    # z_piezo = [          7000,              7000,                7000,                7000,                  7000,              7000,                7000,                  7000,                  7000,                    7000,         7000,           7000,  7000,
    #                      7000,              7000,                7000,                7000,                  7000,              7000,                7000,                  7000,                  7000,                    7000,         7000,           7000]
    

    names = ['P3MEEET_exp_KCl',  'P3MEEET_dope_KCl','P3MEEET_dedope_KCl',            'InDTP_as',       'InDTP_exp',       'InDTP_dedope',           'OutDTP_as',            'OutDTP_exp', 'OutDTP_dope', 'OutDTP_dedope',  'Si']
    x_piezo = [         -51000,              -41000,              -31000,                -19000,             -7000,                16000,                 28000,                   40000,         52000,           52000, 52000]
    x_hexa = [               0,                   0,                   0,                     0,                 0,                    0,                     0,                       0,             0,              12,    16]
    y_piezo = [          -3700,               -3700,               -3700,                 -3700,             -3700,                -3700,                 -3700,                   -3700,         -3700,           -3700,  5100]
    z_piezo = [           7000,                7000,                7000,                  7000,              7000,                 7000,                  7000,                    7000,          7000,            7000,  7000]


    x_piezo = 2000 + np.asarray(x_piezo)
    
    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(z_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexa)})"

    energies = -7 + np.asarray([2810.0, 2820.0, 2830.0, 2832.0, 2834.0, 2834.5, 2835.0, 2835.5, 2836.0, 2836.5, 2837.0, 2837.5, 2838.0, 2838.5, 2839.0,
    2839.5, 2840.0, 2840.5, 2841.0, 2841.5, 2845.0, 2850.0, 2855.0, 2860.0, 2865.0, 2870.0, 2875.0, 2880.0, 2890.0])
    
    waxs_arc = [0, 20]
    ai0 = 0
    ai_list = [0.80]

    for name, xs, ys, zs, xs_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa):
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)

        yield from bps.mv(piezo.th, ai0)
        yield from alignement_gisaxs_doblestack(0.8)

        ai0 = piezo.th.position
        det_exposure_time(t, t)

        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)
            # Do not take SAXS when WAXS detector in the way
            dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]

            yield from bps.mv(piezo.x, xs)
            counter = 0

            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                name_fmt = "{sample}_pos1_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs + counter * 30)
                    counter += 1
                    
                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)


                name_fmt = "{sample}_pos2_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies[::-1]:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs + counter * 30)
                    counter += 1

                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)

            yield from bps.mv(piezo.th, ai0)



def night_2023_1(t=1):

    #proposal_id("2023_1", "310999_Richter_2")
    #yield from S_edge_measurments_2023_1_night1(t=1)
    proposal_id("2023_1", "310999_Richter_3")
    #yield from transition_S_Cl_edges()
    yield from Cl_edge_measurments_2023_1_night1(t=1)




def Cl_edge_xscan_2023_1(t=1):
    dets = [pil900KW]
    det_exposure_time(t, t)

    # names = ['MM460_KCO4']
    # x_hexa = [-13.5]
    # y_hexa = [1.84]
    
    names = ['P3MEEMT_23K115C_KCl_redo2']
    x_hexa = [-12]
    y_hexa = [1.6]

    assert len(x_hexa) == len(names), f"Number of X coordinates ({len(x_hexa)}) is different from number of samples ({len(names)})"
    assert len(x_hexa) == len(y_hexa), f"Number of X coordinates ({len(x_hexa)}) is different from number of samples ({len(y_hexa)})"

    energies = 2810.0

    waxs_arc = [15]
    ais = 0.80
    ai0 = 1.5

    for name, xs_hexa, ys_hexa in zip(names, x_hexa, y_hexa):
        yield from bps.mv(stage.x, xs_hexa-3.5)
        # yield from bps.mv(stage.y, ys_hexa)

        # yield from bps.mv(stage.th, ai0)
        # yield from alignement_gisaxs_hex(0.4)

        ai0 = stage.th.position
        det_exposure_time(t, t)

        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)
            # Do not take SAXS when WAXS detector in the way
            dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]

            yield from bps.mv(stage.th, ai0 + ais)

            name_fmt = "{sample}_xscan_pos1_{energy}eV_x{x}_ai{ai}_wa{wax}_bpm{xbpm}"
            yield from bps.mv(energy, energies)
            yield from bps.sleep(2)
            yield from bps.sleep(2)

            for xss in np.linspace(xs_hexa, xs_hexa-7, 15):
                yield from bps.mv(stage.x, xss)                
                bpm = xbpm2.sumX.get()
                sample_name = name_fmt.format(sample=name, energy="%6.2f"%energies, x="%1.2f"%stage.x.position, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                sample_id(user_name="LR", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

            # yield from bps.mv(stage.th, ai0)



def Cl_edge_measurments_2023_1_sva(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    # names = ['MM460_KClO4_partialdoped0V']
    # x_hexa = [-18.6]
    
    names = ['P3MEEMT_23k115C_KCldedopped-0.6V']
    x_hexa = [-16.7]

    assert len(x_hexa) == len(names), f"Number of X coordinates ({len(x_hexa)}) is different from number of samples ({len(names)})"

    energies = -9 + np.asarray([2810.0, 2820.0, 2830.0, 2832.0, 2834.0, 2834.5, 2835.0, 2835.5, 2836.0, 2836.5, 2837.0, 2837.5, 2838.0, 2838.5, 2839.0,
    2839.5, 2840.0, 2840.5, 2841.0, 2841.5, 2845.0, 2850.0, 2855.0, 2860.0, 2865.0, 2870.0, 2875.0, 2880.0, 2890.0])
    
    waxs_arc = [15]
    ai_list = [0.80]

    for name, xs_hexa in zip(names, x_hexa):
        yield from bps.mv(stage.x, xs_hexa)

        # No alignement 
        # yield from bps.mv(stage.th, ai0)
        # yield from alignement_gisaxs_hex(0.8)

        ai0 = stage.th.position
        det_exposure_time(t, t)

        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)
            # Do not take SAXS when WAXS detector in the way
            dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]

            counter = 0

            for k, ais in enumerate(ai_list):
                # yield from bps.mv(stage.th, ai0 + ais)

                name_fmt = "{sample}_pos1_{energy}eV_x{x}_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(stage.x, xs_hexa - counter * 0.030)
                    counter += 1
                    
                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, x="%1.2f"%stage.x.position, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)

                name_fmt = "{sample}_pos2_{energy}eV_x{x}_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies[::-1]:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(stage.x, xs_hexa - counter * 0.030)
                    counter += 1

                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, x="%1.2f"%stage.x.position, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)

            # yield from bps.mv(stage.th, ai0)



# names = ['acid_PEDOTPSS_as', 'acid_PEDOTPSS_exp','acid_PEDOTPSS_dedope','acid_PEDOTPSS_redope','acid_PEDOTPSS_overdope','EG_PEDOTPSS_as', 'EG_PEDOTPSS_exp','EG_PEDOTPSS_dedope','EG_PEDOTPSS_redope','EG_PEDOTPSS_overdope',      'NaPSS',          'PVC',  'Si',
    #              'P3MEEET_as', 'P3MEEET_exp_KCl',  'P3MEEET_dope_KCl','P3MEEET_dedope_KCl',            'InDTP_as',       'InDTP_exp',        'InDTP_dope',        'InDTP_dedope',           'OutDTP_as',            'OutDTP_exp','OutDTP_dope','OutDTP_dedope']
    # x_piezo = [        -55000,            -51000,              -41000,              -31000,                -19000,             -7000,                5000,                 16000,                 28000,                   40000,        49000,          52000, 52000,
    #                    -55000,            -51000,              -41000,              -31000,                -19000,             -7000,                5000,                 16000,                 28000,                   40000,        52000,          52000, ]
    # x_hexa = [            -10,                 0,                   0,                   0,                     0,                 0,                   0,                     0,                     0,                       0,            0,              7,    16,
    #                       -10,                 0,                   0,                   0,                     0,                 0,                   0,                     0,                     0,                       0,            0,             12]
    # y_piezo = [          5100,              5100,                5100,                5100,                  5100,              5100,                5100,                  5100,                  5100,                    5100,         5100,           5100,  5100,
    #                     -3700,             -3700,               -3700,               -3700,                 -3700,             -3700,               -3700,                 -3700,                 -3700,                   -3700,        -3700,          -3700]
    # z_piezo = [          7000,              7000,                7000,                7000,                  7000,              7000,                7000,                  7000,                  7000,                    7000,         7000,           7000,  7000,
    #                      7000,              7000,                7000,                7000,                  7000,              7000,                7000,                  7000,                  7000,                    7000,         7000,           7000]
    


def K_edge_measurments_2023_1_night1(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    # names = ['acid_PEDOTPSS_as', 'acid_PEDOTPSS_exp','acid_PEDOTPSS_dedope','acid_PEDOTPSS_redope','acid_PEDOTPSS_overdope', 'PBDF_as', 'PBDF_dope','PBDF_dedope','gNDI_as','gNDI_dope',      'P3MEEET_exp_KClO4',          'P3MEEET_dope_KClO4',  'P3MEEET_dedope_KClO4',
    #              'P3MEEET_as', 'P3MEEET_exp_KCl',  'P3MEEET_dope_KCl','P3MEEET_dedope_KCl',            'InDTP_as',       'InDTP_exp',        'InDTP_dope',        'InDTP_dedope',           'OutDTP_as',            'OutDTP_exp','OutDTP_dope','OutDTP_dedope']
    # x_piezo = [        -52000,            -51000,              -41000,              -31000,                -21000,             -11000,               2000,                 14000,                 24000,                   34000,        46000,          56000, 51000,
    #                    -52000,            -52000,              -42000,              -32000,                -19500,             -7000,               10000,                 15000,                 28000,                   40000,        52500,          52000, ]
    # x_hexa = [            -12,                 0,                   0,                   0,                     0,                 0,                   0,                     0,                     0,                       0,            0,              0,    15,
    #                       -12,                 0,                   0,                   0,                     0,                 0,                   0,                     0,                     0,                       0,            0,             12]
    # y_piezo = [          5100,              5100,                5100,                5100,                  5100,              5100,                5100,                  5100,                  5100,                    5100,         5100,           5100,  5100,
    #                     -3700,             -3700,               -3700,               -3700,                 -3700,             -3700,               -3700,                 -3700,                 -3700,                   -3700,        -3700,          -3700]
    # z_piezo = [          7000,              7000,                7000,                7000,                  7000,              7000,                7000,                  7000,                  7000,                    7000,         7000,           7000,  7000,
    #                      7000,              7000,                7000,                7000,                  7000,              7000,                7000,                  7000,                  7000,                    7000,         7000,           7000]
    
    names = ['acid_PEDOTPSS_as', 'acid_PEDOTPSS_exp','acid_PEDOTPSS_dedope','acid_PEDOTPSS_redope','acid_PEDOTPSS_overdope', 'PBDF_as', 'PBDF_dope','PBDF_dedope','gNDI_as','gNDI_dope',      'P3MEEET_exp_KClO4',          'P3MEEET_dope_KClO4',  'P3MEEET_dedope_KClO4',
                 'P3MEEET_as', 'P3MEEET_exp_KCl',  'P3MEEET_dope_KCl','P3MEEET_dedope_KCl',            'InDTP_as',       'InDTP_exp',        'InDTP_dope',        'InDTP_dedope',           'OutDTP_as',            'OutDTP_exp','OutDTP_dope','OutDTP_dedope']
    x_piezo = [        -52000,            -51000,              -41000,              -31000,                -21000,             -11000,               2000,                 14000,                 24000,                   34000,        46000,          56000, 51000,
                       -52000,            -52000,              -42000,              -32000,                -19500,             -7000,               10000,                 15000,                 28000,                   40000,        52500,          52000, ]
    x_hexa = [            -12,                 0,                   0,                   0,                     0,                 0,                   0,                     0,                     0,                       0,            0,              0,    15,
                          -12,                 0,                   0,                   0,                     0,                 0,                   0,                     0,                     0,                       0,            0,             12]
    y_piezo = [          5100,              5100,                5100,                5100,                  5100,              5100,                5100,                  5100,                  5100,                    5100,         5100,           5100,  5100,
                        -3700,             -3700,               -3700,               -3700,                 -3700,             -3700,               -3700,                 -3700,                 -3700,                   -3700,        -3700,          -3700]
    z_piezo = [          7000,              7000,                7000,                7000,                  7000,              7000,                7000,                  7000,                  7000,                    7000,         7000,           7000,  7000,
                         7000,              7000,                7000,                7000,                  7000,              7000,                7000,                  7000,                  7000,                    7000,         7000,           7000]
    


    x_piezo = np.asarray(x_piezo)
    
    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(z_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexa)})"

    energies = np.asarray(np.arange(3580, 3611, 5).tolist() + 
                          np.arange(3612, 3629, 1).tolist() + 
                          np.arange(3630, 3700, 5).tolist())
    
    waxs_arc = [0, 20]
    ai0 = 0
    ai_list = [0.80]

    for name, xs, ys, zs, xs_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa):
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)

        yield from bps.mv(piezo.th, ai0)
        yield from alignement_gisaxs_doblestack(0.8)

        yield from bps.mv(att2_9.open_cmd, 1)
        yield from bps.sleep(1)
        yield from bps.mv(att2_9.open_cmd, 1)

        ai0 = piezo.th.position
        det_exposure_time(t, t)

        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)
            # Do not take SAXS when WAXS detector in the way
            dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]

            yield from bps.mv(piezo.x, xs)
            counter = 0

            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                name_fmt = "{sample}_pos1_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs - counter * 30)
                    counter += 1
                    
                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)

                yield from bps.mv(energy, 3660)
                yield from bps.sleep(2)
                yield from bps.mv(energy, 3620)
                yield from bps.sleep(2)
                yield from bps.mv(energy, 3580)
                yield from bps.sleep(2)

            yield from bps.mv(piezo.th, ai0)




def K_edge_measurments_2023_2_night1(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    # names = ['acid_PEDOTPSS_as', 'acid_PEDOTPSS_exp','acid_PEDOTPSS_dedope','acid_PEDOTPSS_redope','acid_PEDOTPSS_overdope', 'PBDF_as', 'PBDF_dope','PBDF_dedope','gNDI_as','gNDI_dope',      'P3MEEET_exp_KClO4',          'P3MEEET_dope_KClO4',  'P3MEEET_dedope_KClO4',
    #              'P3MEEET_as', 'P3MEEET_exp_KCl',  'P3MEEET_dope_KCl','P3MEEET_dedope_KCl',            'InDTP_as',       'InDTP_exp',        'InDTP_dope',        'InDTP_dedope',           'OutDTP_as',            'OutDTP_exp','OutDTP_dope','OutDTP_dedope']
    # x_piezo = [        -52000,            -51000,              -41000,              -31000,                -21000,             -11000,               2000,                 14000,                 24000,                   34000,        46000,          56000, 51000,
    #                    -52000,            -52000,              -42000,              -32000,                -19500,             -7000,               10000,                 15000,                 28000,                   40000,        52500,          52000, ]
    # x_hexa = [            -12,                 0,                   0,                   0,                     0,                 0,                   0,                     0,                     0,                       0,            0,              0,    15,
    #                       -12,                 0,                   0,                   0,                     0,                 0,                   0,                     0,                     0,                       0,            0,             12]
    # y_piezo = [          5100,              5100,                5100,                5100,                  5100,              5100,                5100,                  5100,                  5100,                    5100,         5100,           5100,  5100,
    #                     -3700,             -3700,               -3700,               -3700,                 -3700,             -3700,               -3700,                 -3700,                 -3700,                   -3700,        -3700,          -3700]
    # z_piezo = [          7000,              7000,                7000,                7000,                  7000,              7000,                7000,                  7000,                  7000,                    7000,         7000,           7000,  7000,
    #                      7000,              7000,                7000,                7000,                  7000,              7000,                7000,                  7000,                  7000,                    7000,         7000,           7000]
    
    names = ['acid_PEDOTPSS_as', 'acid_PEDOTPSS_exp','acid_PEDOTPSS_dedope','acid_PEDOTPSS_redope','acid_PEDOTPSS_overdope', 'PBDF_as', 'PBDF_dope','PBDF_dedope','gNDI_as','gNDI_dope',      'P3MEEET_exp_KClO4',          'P3MEEET_dope_KClO4',  'P3MEEET_dedope_KClO4',
                 'P3MEEET_as', 'P3MEEET_exp_KCl',  'P3MEEET_dope_KCl','P3MEEET_dedope_KCl',            'InDTP_as',       'InDTP_exp',        'InDTP_dope',        'InDTP_dedope',           'OutDTP_as',            'OutDTP_exp','OutDTP_dope','OutDTP_dedope']
    x_piezo = [        -52000,            -51000,              -41000,              -31000,                -21000,             -11000,               2000,                 14000,                 24000,                   34000,        46000,          56000, 51000,
                       -52000,            -52000,              -42000,              -32000,                -19500,             -7000,               10000,                 15000,                 28000,                   40000,        52500,          52000, ]
    x_hexa = [            -12,                 0,                   0,                   0,                     0,                 0,                   0,                     0,                     0,                       0,            0,              0,    15,
                          -12,                 0,                   0,                   0,                     0,                 0,                   0,                     0,                     0,                       0,            0,             12]
    y_piezo = [          5100,              5100,                5100,                5100,                  5100,              5100,                5100,                  5100,                  5100,                    5100,         5100,           5100,  5100,
                        -3700,             -3700,               -3700,               -3700,                 -3700,             -3700,               -3700,                 -3700,                 -3700,                   -3700,        -3700,          -3700]
    z_piezo = [          7000,              7000,                7000,                7000,                  7000,              7000,                7000,                  7000,                  7000,                    7000,         7000,           7000,  7000,
                         7000,              7000,                7000,                7000,                  7000,              7000,                7000,                  7000,                  7000,                    7000,         7000,           7000]
    


    x_piezo = np.asarray(x_piezo)
    
    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(z_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexa)})"

    energies = np.asarray(np.arange(3580, 3611, 5).tolist() + 
                          np.arange(3612, 3629, 1).tolist() + 
                          np.arange(3630, 3700, 5).tolist())
    
    waxs_arc = [0, 20]
    ai0 = 0
    ai_list = [0.80]

    for name, xs, ys, zs, xs_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa):
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)

        yield from bps.mv(piezo.th, ai0)
        yield from alignement_gisaxs_doblestack(0.8)

        yield from bps.mv(att2_9.open_cmd, 1)
        yield from bps.sleep(1)
        yield from bps.mv(att2_9.open_cmd, 1)

        ai0 = piezo.th.position
        det_exposure_time(t, t)

        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)
            # Do not take SAXS when WAXS detector in the way
            dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]

            yield from bps.mv(piezo.x, xs)
            counter = 0

            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                yield from bps.mv(energy, 3580)
                yield from bps.sleep(2)
                yield from bps.mv(energy, 3620)
                yield from bps.sleep(2)
                yield from bps.mv(energy, 3660)
                yield from bps.sleep(2)


                name_fmt = "{sample}_pos2_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies[::-1]:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs - counter * 30)
                    counter += 1

                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)

            yield from bps.mv(piezo.th, ai0)


def night_2023_2(t=1):
    proposal_id("2023_1", "310999_Richter_6")
    yield from K_edge_measurments_2023_1_night1(t=1)

    proposal_id("2023_1", "310999_Richter_6")
    yield from K_edge_measurments_2023_2_night1(t=1)






def K_edge_xscan_2023_1(t=1):
    dets = [pil900KW]
    det_exposure_time(t, t)

    names = ['blank_silicon']
    x_hexa = [-13]
    y_hexa = [1.50]

    assert len(x_hexa) == len(names), f"Number of X coordinates ({len(x_hexa)}) is different from number of samples ({len(names)})"
    assert len(x_hexa) == len(y_hexa), f"Number of X coordinates ({len(x_hexa)}) is different from number of samples ({len(y_hexa)})"

    energies = 3580

    waxs_arc = [0]
    ais = 0.80
    ai0 = 1.2

    for name, xs_hexa, ys_hexa in zip(names, x_hexa, y_hexa):
        yield from bps.mv(stage.x, xs_hexa-3.5)
        yield from bps.mv(stage.y, ys_hexa)

        yield from bps.mv(stage.th, ai0)
        yield from alignement_gisaxs_hex(0.5)


        ai0 = stage.th.position
        det_exposure_time(t, t)

        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)
            # Do not take SAXS when WAXS detector in the way
            dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]

            yield from bps.mv(stage.th, ai0 + ais)

            name_fmt = "{sample}_xscan_pos1_{energy}eV_x{x}_ai{ai}_wa{wax}_bpm{xbpm}"
            yield from bps.mv(energy, energies)
            yield from bps.sleep(2)
            yield from bps.sleep(2)

            for xss in np.linspace(xs_hexa, xs_hexa-7, 15):
                yield from bps.mv(stage.x, xss)                
                bpm = xbpm2.sumX.get()
                sample_name = name_fmt.format(sample=name, energy="%6.2f"%energies, x="%1.2f"%stage.x.position, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                sample_id(user_name="LR", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

            yield from bps.mv(stage.th, ai0)



def K_edge_measurments_2023_1_sva(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    # names = ['MM460_KClO4_partialdoped0V']
    # x_hexa = [-18.6]
    
    names = ['blank_silicon']
    x_hexa = [-16]

    assert len(x_hexa) == len(names), f"Number of X coordinates ({len(x_hexa)}) is different from number of samples ({len(names)})"

    energies = np.asarray(np.arange(3580, 3611, 5).tolist() + 
                          np.arange(3612, 3629, 1).tolist() + 
                          np.arange(3630, 3700, 5).tolist())
    
    waxs_arc = [0]
    ai_list = [0.80]

    for name, xs_hexa in zip(names, x_hexa):
        yield from bps.mv(stage.x, xs_hexa)

        # No alignement 
        # yield from bps.mv(stage.th, ai0)
        # yield from alignement_gisaxs_hex(0.8)

        ai0 = stage.th.position
        det_exposure_time(t, t)

        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)
            # Do not take SAXS when WAXS detector in the way
            dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]

            counter = 0

            for k, ais in enumerate(ai_list):
                yield from bps.mv(stage.th, ai0 + ais)

                name_fmt = "{sample}_pos1_{energy}eV_x{x}_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(stage.x, xs_hexa - counter * 0.030)
                    counter += 1
                    
                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, x="%1.2f"%stage.x.position, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)


                name_fmt = "{sample}_pos2_{energy}eV_x{x}_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies[::-1]:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(stage.x, xs_hexa - counter * 0.030)
                    counter += 1

                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, x="%1.2f"%stage.x.position, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)

            yield from bps.mv(stage.th, ai0)


def S_edge_measurments_2023_1_night3(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    names = [        'PK_B69',          'PK_B61',            'PK_B48',           'PK_24','              PK_H48',          'PK_H36',            'PK_H24',              'PK_H12',                'PK_H0',            'P3MEEBT_as',      'P3MEEBT_KClO4_0p6', 'P3MEEMT_random115_frit',
                'P3MTEEBT_as',  'P3MTEEBT_KClO4',           'PBDF_as',  'PBDF_doped_KCl',    'PBDF_dedoped_KCl',         'gNDI_as',        'gNDI_doped',   'P3MEEET_exp_KClO4',  'P3MEEET_doped_KClO4',  'P3MEEET_dedoped_KClO4']
    x_piezo = [        -48000,            -50000,              -38000,            -28000,                -16000,             -5000,                6000,                 16000,                  28000,                   40000,                    40000,                    54000,   
                       -44000,            -28000,              -14000,                 0,                 14000,             25000,               35000,                 46000,                  48000,                   54000]
    x_hexa = [            -12,                 0,                   0,                 0,                     0,                 0,                   0,                     0,                      0,                       0,                       14,                       14,
                            0,                 0,                   0,                 0,                     0,                 0,                   0,                     0,                     10,                     14 ]
    y_piezo = [          5100,              5100,                5100,              5100,                  5100,              5100,                5100,                  5100,                   5100,                    5100,                     5100,                     5100,
                        -3700,             -3700,               -3700,             -3700,                 -3700,             -3700,               -3700,                 -3700,                  -3700,                   -3700]
    z_piezo = [          7000,              7000,                7000,              7000,                  7000,              7000,                7000,                  7000,                   7000,                    7000,                     7000,                     7000,
                         7000,              7000,                7000,              7000,                  7000,              7000,                7000,                  7000,                   7000,                    7000]

    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(z_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexa)})"

    energies = [2450.0,2455.0,2460.0,2465.0,2470.0,2473.0,2475.0,2475.5,2476.0,2476.5,2477.0,2477.5,2478.0,2478.5,2479.0,2479.5,
    2480.0,2480.5,2481.0,2482.0,2483.0,2484.0,2485.0,2486.0, 2487.0,2488.0,2489.0,2490.0,2492.5,2495.0,2500.0,2510.0,2515.0]

    waxs_arc = [0, 20]
    ai0 = 0
    ai_list = [0.80]

    for name, xs, ys, zs, xs_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa):
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)

        yield from bps.mv(piezo.th, ai0)
        yield from alignement_gisaxs_doblestack(0.8)

        ai0 = piezo.th.position
        det_exposure_time(t, t)

        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)
            # Do not take SAXS when WAXS detector in the way
            dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]

            yield from bps.mv(piezo.x, xs)
            counter = 0

            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                name_fmt = "{sample}_pos1_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs + counter * 30)
                    counter += 1
                    
                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)


                name_fmt = "{sample}_pos2_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies[::-1]:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs + counter * 30)
                    counter += 1

                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)

            yield from bps.mv(piezo.th, ai0)



def Cl_edge_measurments_2023_1_night3(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    names = [    'P3MEEBT_as',      'P3MEEBT_KClO4_0p6', 'P3MEEMT_random115_frit',
                'P3MTEEBT_as',  'P3MTEEBT_KClO4',           'PBDF_as',  'PBDF_doped_KCl',    'PBDF_dedoped_KCl',         'gNDI_as',        'gNDI_doped',   'P3MEEET_exp_KClO4',  'P3MEEET_doped_KClO4',  'P3MEEET_dedoped_KClO4']
    x_piezo = [         40000,                    40000,                    54000,   
                       -44000,            -28000,              -14000,                 0,                 14000,             25000,               35000,                 46000,                  48000,                   54000]
    x_hexa = [              0,                       14,                       14,
                            0,                 0,                   0,                 0,                     0,                 0,                   0,                     0,                     10,                     14 ]
    y_piezo = [          5100,                     5100,                     5100,
                        -3700,             -3700,               -3700,             -3700,                 -3700,             -3700,               -3700,                 -3700,                  -3700,                   -3700]
    z_piezo = [          7000,                     7000,                     7000,
                         7000,              7000,                7000,              7000,                  7000,              7000,                7000,                  7000,                   7000,                    7000]

    x_piezo = 2000 + np.asarray(x_piezo)
    
    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(z_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexa)})"

    energies = np.asarray([2810.0, 2820.0, 2830.0, 2832.0, 2834.0, 2834.5, 2835.0, 2835.5, 2836.0, 2836.5, 2837.0, 2837.5, 2838.0, 2838.5, 2839.0,
    2839.5, 2840.0, 2840.5, 2841.0, 2841.5, 2845.0, 2850.0, 2855.0, 2860.0, 2865.0, 2870.0, 2875.0, 2880.0, 2890.0])
    
    waxs_arc = [0, 20]
    ai0 = 0
    ai_list = [0.80]

    for name, xs, ys, zs, xs_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa):
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)

        yield from bps.mv(piezo.th, ai0)
        yield from alignement_gisaxs_doblestack(0.8)

        ai0 = piezo.th.position
        det_exposure_time(t, t)

        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)
            # Do not take SAXS when WAXS detector in the way
            dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]

            yield from bps.mv(piezo.x, xs)
            counter = 0

            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                name_fmt = "{sample}_pos1_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs + counter * 30)
                    counter += 1
                    
                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)


                name_fmt = "{sample}_pos2_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies[::-1]:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs + counter * 30)
                    counter += 1

                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)

            yield from bps.mv(piezo.th, ai0)



def night_2023_1(t=1):

    #proposal_id("2023_1", "310999_Richter_2")
    #yield from S_edge_measurments_2023_1_night1(t=1)
    proposal_id("2023_1", "310999_Richter_3")
    #yield from transition_S_Cl_edges()
    yield from Cl_edge_measurments_2023_1_night1(t=1)


def night_2023_3(t=1):

    proposal_id("2023_1", "310999_Richter_9")
    yield from Cl_edge_measurments_2023_1_night3(t=1)
    
    yield from transition_Cl_S_edges()

    proposal_id("2023_1", "310999_Richter_10")
    yield from S_edge_measurments_2023_1_night3(t=1)


def x_scan(t=1):
    # Att 2x and 1x of Sn 30um and exposure time of 5s

    yield from bps.mv(att1_9.open_cmd, 1)
    yield from bps.sleep(1)
    yield from bps.mv(att1_9.open_cmd, 1)
    yield from bps.sleep(1)
    yield from bps.mv(att1_10.open_cmd, 1)
    yield from bps.sleep(1)
    yield from bps.mv(att1_10.open_cmd, 1)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 0)

    yield from bps.mvr(stage.th, 0.2)


    det_exposure_time(t, t)
    dets=[pil900KW]
    name='NDI_T2_3B_wet5mmNaCl'
    x0 = 13
    for x in np.linspace(0, 8, 9):
        yield from bps.mv(stage.x, x0 + x)
        name_fmt = "{sample}_xscan5_pos1_{energy}eV_x{x}_ai{ai}_wa{wax}_bpm{xbpm}"
        bpm = xbpm2.sumX.get()
        sample_name = name_fmt.format(sample=name,energy="%6.2f"%13500, x="%1.2f"%stage.x.position, ai="%3.2f"%0.2, wax='00', xbpm=bpm)
        sample_id(user_name="LR", sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")
        yield from bp.count(dets, num=1)
    
    yield from bps.mvr(stage.th, -0.2)



def ai_scan(t=1):
    # Att 2x and 1x of Sn 30um and exposure time of 5s
    #for samp[le in negative x, chi = 0.297

    yield from bps.mv(att1_9.open_cmd, 1)
    yield from bps.sleep(1)
    yield from bps.mv(att1_9.open_cmd, 1)
    yield from bps.sleep(1)
    yield from bps.mv(att1_10.open_cmd, 1)
    yield from bps.sleep(1)
    yield from bps.mv(att1_10.open_cmd, 1)
    yield from bps.sleep(1)

    yield from bps.mv(waxs, 0)
    ai0=stage.th.position
    det_exposure_time(t, t)
    dets=[pil900KW]

    name='NDI_T2_3B_wet5mmNaCl_alignmentx18'
    
    # xs = [-18+1, -16+1, -14+1]
    xs = [14, 16, 18]
    xs = [18]

    for x in xs:
        yield from bps.mv(stage.x, x)

        for ai in np.linspace(0.08, 0.16, 5):
            yield from bps.mv(stage.th, ai0 + ai)

            name_fmt = "{sample}_pos1_{energy}eV_x{x}_ai{ai}_wa{wax}_bpm{xbpm}"
            bpm = xbpm2.sumX.get()
            sample_name = name_fmt.format(sample=name,energy="%6.2f"%13500, x="%1.2f"%stage.x.position, ai="%3.2f"%ai, wax='00', xbpm=bpm)
            sample_id(user_name="LR", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)

def K_edge_measurments_2023_2_july_night2(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    # top left first
    names = [        'BBL_ascast',            'BBL_doped_n0p8V',           'BBL_doped_n1p2V',               'PBDF_ascast',            'PBDF_doped_n1V',            'PBDF_doped_p1V',       'GNDI_ascast',           'GNDI_n1V',              'GNDI_p1V',              'P3MEEMT_0p7V']
    x_piezo = [            -43500,                      -45000,                       -36000,                      -24500,                      -16000,                       -8500,                3000,                12500,                   21000,                       52000]
    x_hexa = [                -14,                          -2,                            0,                           0,                           0,                           0,                   0,                    0,                       0,                          17]
    y_piezo = [             -3600,                       -3600,                        -3600,                       -3600,                       -3600,                       -3600,               -3600,                -3600,                   -3600,                       -3600]
    z_piezo = [              7000,                        7000,                         7000,                        7000,                        7000,                        7000,                7000,                 7000,                    7000,                        7000]
    

    
    x_piezo = np.asarray(x_piezo)
    
    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples1 ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples2 ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples3 ({len(z_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples4 ({len(x_hexa)})"

    energies = np.asarray(np.arange(3580, 3611, 5).tolist() + 
                          np.arange(3612, 3629, 1).tolist() + 
                          np.arange(3630, 3700, 5).tolist())
    
    waxs_arc = [0, 20]
    ai0_all = 0
    ai_list = [0.80]

    for name, xs, ys, zs, xs_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa):
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)

        yield from bps.mv(piezo.th, ai0_all)
        yield from alignement_gisaxs_doblestack(0.8)

        yield from bps.mv(att2_10.open_cmd, 1)
        yield from bps.sleep(1)
        yield from bps.mv(att2_10.open_cmd, 1)

        ai0 = piezo.th.position
        det_exposure_time(t, t)

        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)
            # Do not take SAXS when WAXS detector in the way
            dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]

            yield from bps.mv(piezo.x, xs)
            counter = 0

            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                name_fmt = "{sample}_pos1_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs - counter * 30)
                    counter += 1

                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)
                
                if waxs.arc.position > 15:
                    det_exposure_time(10, 10)

                    yield from bps.mv(GV7.close_cmd, 1)
                    yield from bps.sleep(5)
                    yield from bps.mv(GV7.close_cmd, 1)
                    yield from bps.sleep(5)

                    name_fmt = "{sample}_{energy}eV_ai{ai}_bpm{xbpm}"
                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)

                    fs.open()
                    yield from bp.count([amptek], num=1)
                    fs.close()

                    yield from bps.mv(GV7.open_cmd, 1)
                    yield from bps.sleep(5)
                    yield from bps.mv(GV7.open_cmd, 1)
                    yield from bps.sleep(5)
                    det_exposure_time(t, t)


                name_fmt = "{sample}_pos2_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies[::-1]:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs - counter * 30)
                    counter += 1

                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)

            yield from bps.mv(piezo.th, ai0)




def Cl_edge_measurments_2023_2_july_day2(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    # top left first
    names = [              'KPSS',       'acid_PEDOTPSS_Au_as',       'acid_PEDOTPSS_Au_exp',   'acid_PEDOTPSS_Au_dedope',   'acid_PEDOTPSS_Au_redope', 'acid_PEDOTPSS_Au_overdope', 'EG_PEDOTPSS_Au_as', 'EG_PEDOTPSS_Au_exp', 'EG_PEDOTPSS_Au_dedope',     'EG_PEDOTPSS_Au_redope', 'EG_PEDOTPSS_Au_asoverdope',      'PVC',     
               'Acid_PEDOT_Si_as',         'Acid_PEDOT_Si_exp',           'Acid_PEDOT_Si_0V',      'Acid_PEDOT_Si_dedope',    'Acid_PEDOT_Si_overdope',            'EG_PEDOT_Si_as',   'EG_PEDOT_Si_exp', 'EG_PEDOT_Si_dedope',    'EG_PEDOT_Si_redope',      'EG_PEDOT_Si_overdope',                 'PBTTT_par','PBTTT_per']
    x_piezo = [             56000,                      -45000,                       -45000,                      -34000,                      -24000,                      -15000,                   0,                11000,                   22000,                       34000,                       44000,      56000,       
                           -43000,                      -43000,                       -32000,                      -22000,                      -11000,                        3000,               15000,                29000,                   41000,                       52000,                       56000,      56000]
    x_hexa = [                 12,                         -14,                            0,                           0,                           0,                           0,                   0,                    0,                       0,                           0,                           0,          0,
                              -11,                           0,                            0,                           0,                           0,                           0,                   0,                    0,                       0,                           0,                           6,         18]
    y_piezo = [             -3600,                       -3600,                        -3600,                       -3600,                       -3600,                       -3600,               -3600,                -3600,                   -3600,                       -3600,                       -3600,      -3600,
                             4900,                        4900,                         4900,                        4900,                        4900,                        4900,                4900,                 4900,                    4900,                        4900,                        4900,       4900]
    z_piezo = [              7000,                        7000,                         7000,                        7000,                        7000,                        7000,                7000,                 7000,                    7000,                        7000,                        7000,       7000,
                             7000,                        7000,                         7000,                        7000,                        7000,                        7000,                7000,                 7000,                    7000,                        7000,                        7000,       7000]
    

    names = [           'EG_PEDOT_Si_dedope',   'EG_PEDOT_Si_redope',      'EG_PEDOT_Si_overdope']
    x_piezo = [                        29000,                  41000,                       52000]
    x_hexa = [                             0,                      0,                           0]
    y_piezo = [                         4900,                   4900,                        4900]
    z_piezo = [                         7000,                   7000,                        7000]
    

    # # top left first
    # names = [              'KPSS',       'acid_PEDOTPSS_Au_as',       'acid_PEDOTPSS_Au_exp',   'acid_PEDOTPSS_Au_dedope',   'acid_PEDOTPSS_Au_redope', 'acid_PEDOTPSS_Au_overdope', 'EG_PEDOTPSS_Au_as', 'EG_PEDOTPSS_Au_exp', 'EG_PEDOTPSS_Au_dedope',     'EG_PEDOTPSS_Au_redope', 'EG_PEDOTPSS_Au_asoverdope',      'PVC',     
    #            'Acid_PEDOT_Si_as',         'Acid_PEDOT_Si_exp',                  'PBTTT_par',                 'PBTTT_per']
    # x_piezo = [             56000,                      -45000,                       -45000,                      -34000,                      -24000,                      -15000,                   0,                11000,                   22000,                       34000,                       44000,      56000,       
    #                        -43000,                      -43000,                        56000,                       56000]
    # x_hexa = [                 12,                         -14,                            0,                           0,                           0,                           0,                   0,                    0,                       0,                           0,                           0,          0,
    #                           -11,                           0,                            6,                          18]
    # y_piezo = [             -3600,                       -3600,                        -3600,                       -3600,                       -3600,                       -3600,               -3600,                -3600,                   -3600,                       -3600,                       -3600,      -3600,
    #                          4900,                        4900,                         4900,                        4900]
    # z_piezo = [              7000,                        7000,                         7000,                        7000,                        7000,                        7000,                7000,                 7000,                    7000,                        7000,                        7000,       7000,
    #                          7000,                        7000,                         7000,                        7000]
    

    x_piezo = -2500 + np.asarray(x_piezo)
    
    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples1 ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples2 ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples3 ({len(z_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples4 ({len(x_hexa)})"

    energies = np.asarray([2810.0, 2820.0, 2830.0, 2832.0, 2834.0, 2834.5, 2835.0, 2835.5, 2836.0, 2836.5, 2837.0, 2837.5, 2838.0, 2838.5, 2839.0,
    2839.5, 2840.0, 2840.5, 2841.0, 2841.5, 2845.0, 2850.0, 2855.0, 2860.0, 2865.0, 2870.0, 2875.0, 2880.0, 2890.0])
    
    waxs_arc = [0, 20]
    ai0_all = 0
    ai_list = [0.80]

    for name, xs, ys, zs, xs_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa):
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)

        yield from bps.mv(piezo.th, ai0_all)
        yield from alignement_gisaxs_doblestack(0.8)

        yield from bps.mv(att2_9.open_cmd, 1)
        yield from bps.sleep(1)
        yield from bps.mv(att2_9.open_cmd, 1)

        ai0 = piezo.th.position
        det_exposure_time(t, t)

        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)
            # Do not take SAXS when WAXS detector in the way
            dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]

            yield from bps.mv(piezo.x, xs)
            counter = 0

            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                name_fmt = "{sample}_pos1_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs - counter * 30)
                    counter += 1

                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)

                name_fmt = "{sample}_pos2_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies[::-1]:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs - counter * 30)
                    counter += 1

                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)

            yield from bps.mv(piezo.th, ai0)




def x_scan_cl(t=1):
    # Att 1x and Al 9um and exposure time of 2s
    #PGBTTT_dry good x -20 to -11.5 th 4.98 and chi 0.201
    #PG2T-TT_dry good x -17.5 to -12 th 2.443 and chi 0.203

    #MM389_dry_nistfrit -21 to -12.5 chi 0 th 4.457 y 0
    #MM460_dry_nistfrit 10 to 18 chi 0 th 3.457 y 0

    yield from bps.mv(att2_9.open_cmd, 1)
    yield from bps.sleep(1)
    yield from bps.mv(att2_9.open_cmd, 1)
    yield from bps.sleep(1)
    yield from bps.mv(waxs, 0)

    yield from bps.mvr(stage.th, 0.8)

    det_exposure_time(t, t)
    dets=[pil900KW, amptek]
    # name='MM389_dry_nistfrit'
    name='PG2T-TT_annealed_dry'

    x0 = 10
    for x in np.linspace(0, 9, 19):
        yield from bps.mv(stage.x, x0 + x)
        name_fmt = "{sample}_xscan1_pos1_{energy}eV_x{x}_ai{ai}_wa{wax}_bpm{xbpm}"
        bpm = xbpm2.sumX.get()
        ener=energy.energy.position
        sample_name = name_fmt.format(sample=name,energy="%6.2f"%ener, x="%1.2f"%stage.x.position, ai="%3.2f"%0.2, wax='00', xbpm=bpm)
        sample_id(user_name="LR", sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")
        yield from bp.count(dets, num=1)
        yield from bps.sleep(2)

    
    yield from bps.mvr(stage.th, -0.8)



def ai_scan_cl(t=1):
    # Att 2x and 1x of Sn 30um and exposure time of 5s
    #for samp[le in negative x, chi = 0.297

    yield from bps.mv(att1_9.open_cmd, 1)
    yield from bps.sleep(1)
    yield from bps.mv(att1_9.open_cmd, 1)
    yield from bps.sleep(1)
    yield from bps.mv(att1_10.open_cmd, 1)
    yield from bps.sleep(1)
    yield from bps.mv(att1_10.open_cmd, 1)
    yield from bps.sleep(1)

    yield from bps.mv(waxs, 0)
    ai0=stage.th.position
    det_exposure_time(t, t)
    dets=[pil900KW]

    name='NDI_T2_3B_wet5mmNaCl_alignmentx18'
    
    # xs = [-18+1, -16+1, -14+1]
    xs = [14, 16, 18]
    xs = [18]

    for x in xs:
        yield from bps.mv(stage.x, x)

        for ai in np.linspace(0.08, 0.16, 5):
            yield from bps.mv(stage.th, ai0 + ai)

            name_fmt = "{sample}_pos1_{energy}eV_x{x}_ai{ai}_wa{wax}_bpm{xbpm}"
            bpm = xbpm2.sumX.get()
            sample_name = name_fmt.format(sample=name,energy="%6.2f"%13500, x="%1.2f"%stage.x.position, ai="%3.2f"%ai, wax='00', xbpm=bpm)
            sample_id(user_name="LR", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)







def KCl_edge_measurments_2023_2_sva(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    # names = ['MM460_KClO4_partialdoped0V']
    # x_hexa = [-18.6]
    
    #ai0 at -17 is 2.78 for PGBTTT_nistfrit
    # names = ['PGBTTT_nistfrit_KCl_redoped_0p6V']
    names = ['PG2T-TT_nistfrit_KCl_redoped_0p6V']

    x_hexa = [14.37]

    assert len(x_hexa) == len(names), f"Number of X coordinates ({len(x_hexa)}) is different from number of samples ({len(names)})"

    energies = -7 + np.asarray([2810.0, 2820.0, 2830.0, 2832.0, 2834.0, 2834.5, 2835.0, 2835.5, 2836.0, 2836.5, 2837.0, 2837.5, 2838.0, 2838.5, 2839.0,
    2839.5, 2840.0, 2840.5, 2841.0, 2841.5, 2845.0, 2850.0, 2855.0, 2860.0, 2865.0, 2870.0, 2875.0, 2880.0, 2890.0])
    
    waxs_arc = [0]
    ai_list = [0.80]

    for name, xs_hexa in zip(names, x_hexa):
        yield from bps.mv(stage.x, xs_hexa)

        # No alignement 
        # yield from bps.mv(stage.th, ai0)
        # yield from alignement_gisaxs_hex(0.8)

        # yield from bps.mv(att2_9.open_cmd, 1)
        # yield from bps.sleep(1)
        # yield from bps.mv(att2_9.open_cmd, 1)
        # yield from bps.sleep(1)

        ai0 = stage.th.position
        det_exposure_time(t, t)

        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)
            # Do not take SAXS when WAXS detector in the way
            dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]

            counter = 0

            for k, ais in enumerate(ai_list):
                yield from bps.mv(stage.th, ai0 + ais)

                name_fmt = "{sample}_pos1_{energy}eV_x{x}_ai{ai}_wa{wax}_bpm{xbpm}"
                x="%1.2f"%stage.x.position
                for e in energies:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(stage.x, xs_hexa - counter * 0.030)
                    counter += 1
                    
                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, x=x, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)

                x="%1.2f"%stage.x.position
                name_fmt = "{sample}_pos2_{energy}eV_x{x}_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies[::-1]:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(stage.x, xs_hexa - counter * 0.030)
                    counter += 1

                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, x=x, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)
            yield from bps.mv(stage.th, ai0)




def KClO4_edge_measurments_2023_2_sva(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    # names = ['MM460_KClO4_partialdoped0V']
    # x_hexa = [-18.6]
    
    #MM460_dry_nistfrit 10 to 18 chi 0 th 3.457 y 0
    # names = ['PG2T-TT_nistfrit_KCl_redoped_0p6V']
    names = ['MM460_nistfrit_KCl04_reredoped_0p1V']

    x_hexa = [15]

    assert len(x_hexa) == len(names), f"Number of X coordinates ({len(x_hexa)}) is different from number of samples ({len(names)})"

    energies = np.asarray([2810.0, 2820.0, 2830.0, 2832.0, 2834.0, 2834.5, 2835.0, 2835.5, 2836.0, 2836.5, 2837.0, 2837.5, 2838.0, 2838.5, 2839.0,
    2839.5, 2840.0, 2840.5, 2841.0, 2841.5, 2845.0, 2850.0, 2855.0, 2860.0, 2865.0, 2870.0, 2875.0, 2880.0, 2890.0])
    
    waxs_arc = [0]
    ai_list = [1.6]

    for name, xs_hexa in zip(names, x_hexa):
        yield from bps.mv(stage.x, xs_hexa)

        # No alignement 
        # yield from bps.mv(stage.th, ai0)
        # yield from alignement_gisaxs_hex(0.8)

        yield from bps.mv(att2_9.open_cmd, 1)
        yield from bps.sleep(1)
        yield from bps.mv(att2_9.open_cmd, 1)
        yield from bps.sleep(1)

        ai0 = stage.th.position
        det_exposure_time(t, t)

        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)
            # Do not take SAXS when WAXS detector in the way
            dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]

            counter = 0

            for k, ais in enumerate(ai_list):
                yield from bps.mv(stage.th, ai0 + ais)

                name_fmt = "{sample}_pos1_{energy}eV_x{x}_ai{ai}_wa{wax}_bpm{xbpm}"
                x="%1.2f"%stage.x.position
                for e in energies:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(stage.x, xs_hexa - counter * 0.030)
                    counter += 1
                    
                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, x=x, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)

                x="%1.2f"%stage.x.position
                name_fmt = "{sample}_pos2_{energy}eV_x{x}_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies[::-1]:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(stage.x, xs_hexa - counter * 0.030)
                    counter += 1

                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, x=x, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)
            yield from bps.mv(stage.th, ai0)


def Cl_edge_measurments_2023_2_july_day2_dinner(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    # top left first
    names = [    'acid_PEDOTPSS_Au_as',      'acid_PEDOTPSS_Au_exp',   'acid_PEDOTPSS_Au_dedope',   'acid_PEDOTPSS_Au_redope', 'acid_PEDOTPSS_Au_overdope',       'PVC',     
                    'Acid_PEDOT_Si_as',         'Acid_PEDOT_Si_exp',          'Acid_PEDOT_Si_0V',      'Acid_PEDOT_Si_dedope',    'Acid_PEDOT_Si_overdope']
    x_piezo = [                 -45000,                      -45000,                      -34000,                      -24000,                      -15000,       56000,       
                                -43000,                      -43000,                      -32000,                      -22000,                      -11000]
    x_hexa = [                     -14,                           0,                           0,                           0,                           0,           0,
                                   -11,                           0,                           0,                           0,                           0]
    y_piezo = [                  -3600,                       -3600,                       -3600,                       -3600,                       -3600,       -3600,
                                  4900,                        4900,                        4900,                        4900,                        4900]
    z_piezo = [                   7000,                        7000,                        7000,                        7000,                        7000,        7000,
                                  7000,                        7000,                        7000,                        7000,                        7000]
    
    x_piezo = -2500 + np.asarray(x_piezo)
    
    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples1 ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples2 ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples3 ({len(z_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples4 ({len(x_hexa)})"

    energies = -7 + np.asarray([2810.0, 2820.0, 2830.0, 2832.0, 2834.0, 2834.5, 2835.0, 2835.5, 2836.0, 2836.5, 2837.0, 2837.5, 2838.0, 2838.5, 2839.0,
    2839.5, 2840.0, 2840.5, 2841.0, 2841.5, 2845.0, 2850.0, 2855.0, 2860.0, 2865.0, 2870.0, 2875.0, 2880.0, 2890.0])
    
    waxs_arc = [0, 20]
    ai0_all = 0
    ai_list = [0.80]

    for name, xs, ys, zs, xs_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa):
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)

        yield from bps.mv(piezo.th, ai0_all)
        yield from alignement_gisaxs_doblestack(0.8)

        yield from bps.mv(att2_9.open_cmd, 1)
        yield from bps.sleep(1)
        yield from bps.mv(att2_9.open_cmd, 1)

        ai0 = piezo.th.position
        det_exposure_time(t, t)

        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)
            # Do not take SAXS when WAXS detector in the way
            dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]

            yield from bps.mv(piezo.x, xs)
            counter = 0

            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                name_fmt = "{sample}_pos1_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs - counter * 30)
                    counter += 1

                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)

                name_fmt = "{sample}_pos2_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies[::-1]:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs - counter * 30)
                    counter += 1

                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)

            yield from bps.mv(piezo.th, ai0)




def S_edge_measurments_2023_2_night3(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)


    # top left first
    # names = [    'acid_PEDOTPSS_Au_as',      'acid_PEDOTPSS_Au_exp',   'acid_PEDOTPSS_Au_dedope',   'acid_PEDOTPSS_Au_redope', 'acid_PEDOTPSS_Au_overdope',       'PVC',     
    #                 'Acid_PEDOT_Si_as',         'Acid_PEDOT_Si_exp',          'Acid_PEDOT_Si_0V',      'Acid_PEDOT_Si_dedope',    'Acid_PEDOT_Si_overdope']
    # x_piezo = [                 -45000,                      -45000,                      -34000,                      -24000,                      -15000,       56000,       
    #                             -43000,                      -43000,                      -32000,                      -22000,                      -11000]
    # x_hexa = [                     -14,                           0,                           0,                           0,                           0,           0,
    #                                -11,                           0,                           0,                           0,                           0]
    # y_piezo = [                  -3600,                       -3600,                       -3600,                       -3600,                       -3600,       -3600,
    #                               4900,                        4900,                        4900,                        4900,                        4900]
    # z_piezo = [                   7000,                        7000,                        7000,                        7000,                        7000,        7000,
    #                               7000,                        7000,                        7000,                        7000,                        7000]
    

    names = [          'Acid_PEDOT_Si_0V',      'Acid_PEDOT_Si_dedope',    'Acid_PEDOT_Si_overdope',            'EG_PEDOT_Si_as',   'EG_PEDOT_Si_exp', 'EG_PEDOT_Si_dedope',    'EG_PEDOT_Si_redope',      'EG_PEDOT_Si_overdope']
    x_piezo = [                    -32000,                      -22000,                      -11000,                        3000,               15000,                29000,                   41000,                       52000]
    x_hexa = [                          0,                           0,                           0,                           0,                   0,                    0,                       0,                           0]
    y_piezo = [                      4900,                        4900,                        4900,                        4900,                4900,                 4900,                    4900,                        4900]
    z_piezo = [                      7000,                        7000,                        7000,                        7000,                7000,                 7000,                    7000,                        7000]
    

    x_piezo = -5000 + np.asarray(x_piezo)


    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(z_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexa)})"

    energies = [2450.0,2455.0,2460.0,2465.0,2470.0,2473.0,2475.0,2475.5,2476.0,2476.5,2477.0,2477.5,2478.0,2478.5,2479.0,2479.5,
    2480.0,2480.5,2481.0,2482.0,2483.0,2484.0,2485.0,2486.0, 2487.0,2488.0,2489.0,2490.0,2492.5,2495.0,2500.0,2510.0,2515.0]

    waxs_arc = [0, 20]
    ai0_all = 0
    ai_list = [0.80]

    for name, xs, ys, zs, xs_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa):
        try:
            yield from bps.mv(stage.x, xs_hexa)
            yield from bps.mv(piezo.x, xs)
            yield from bps.mv(piezo.y, ys)
            yield from bps.mv(piezo.z, zs)

            yield from bps.mv(piezo.th, ai0_all)
            yield from alignement_gisaxs_doblestack(0.8)

            ai0 = piezo.th.position
            det_exposure_time(t, t)

            for i, wa in enumerate(waxs_arc):
                yield from bps.mv(waxs, wa)
                # Do not take SAXS when WAXS detector in the way
                dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]

                yield from bps.mv(piezo.x, xs)
                counter = 0

                for k, ais in enumerate(ai_list):
                    yield from bps.mv(piezo.th, ai0 + ais)

                    name_fmt = "{sample}_pos1_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                    for e in energies:
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                        if xbpm2.sumX.get() < 50:
                            yield from bps.sleep(2)
                            yield from bps.mv(energy, e)
                            yield from bps.sleep(2)
                        yield from bps.mv(piezo.x, xs - counter * 30)
                        counter += 1
                        
                        bpm = xbpm2.sumX.get()
                        sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                        sample_id(user_name="LR", sample_name=sample_name)
                        print(f"\n\t=== Sample: {sample_name} ===\n")
                        yield from bp.count(dets, num=1)


                    name_fmt = "{sample}_pos2_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                    for e in energies[::-1]:
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                        if xbpm2.sumX.get() < 50:
                            yield from bps.sleep(2)
                            yield from bps.mv(energy, e)
                            yield from bps.sleep(2)
                        yield from bps.mv(piezo.x, xs - counter * 30)
                        counter += 1

                        bpm = xbpm2.sumX.get()
                        sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                        sample_id(user_name="LR", sample_name=sample_name)
                        print(f"\n\t=== Sample: {sample_name} ===\n")
                        yield from bp.count(dets, num=1)

                yield from bps.mv(piezo.th, ai0)
        except:
            print(name, 'did not aligned')    




def S_edge_measurments_2023_2_morning3(t=10):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    names = [            'PK_B61',                    'PK_B55',                     'PK_B48',                    'PK_B36',                    'PK_B24',               'PK_H48_50nm',      'PK_H48_100nm',       'PK_H48_150nm',           'PK_H36_50nm',                'PK_H36_100nm',             'PK_H36_150nm',    
                    'PK_H24_50nm',              'PK_H24_100nm',               'PK_H24_150nm',               'PK_H12_50nm',              'PK_H12_100nm',              'PK_H12_150nm',        'PK_H0_50nm',        'PK_H0_100nm',        'PK_H0_150nm']
    x_piezo = [            -42000,                      -38000,                       -34000,                      -22000,                       -7000,                        8000,               21000,                34000,                   46000,                         56000,                     56000,       
                           -42000,                      -43000,                       -30000,                      -18000,                       -5000,                       10000,               22000,                36000,                   41000]
    x_hexa = [                -15,                         -10,                            0,                           0,                           0,                           0,                   0,                    0,                       0,                          0,                         12,
                              -13,                           0,                            0,                           0,                           0,                           0,                   0,                    0,                       7]
    y_piezo = [             -3600,                       -3600,                        -3600,                       -3600,                       -3600,                       -3600,               -3600,                -3600,                   -3600,                       -3600,                       -3600,
                             4900,                        4900,                         4900,                        4900,                        4900,                        4900,                4900,                 4900,                    4900]
    z_piezo = [              7000,                        7000,                         7000,                        7000,                        7000,                        7000,                7000,                 7000,                    7000,                        7000,                        7000,
                             7000,                        7000,                         7000,                        7000,                        7000,                        7000,                7000,                 7000,                    7000]
    
    
    names = [           'PK_B36',                    'PK_B24']
    x_piezo = [           -22000,                       -7000]
    x_hexa = [                 0,                           0]
    y_piezo = [            -3600,                       -3600]
    z_piezo = [             7000,                        7000]
    


    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(z_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexa)})"

    energies = [2450.0,2455.0,2460.0,2465.0,2470.0,2473.0,2475.0,2475.5,2476.0,2476.5,2477.0,2477.5,2478.0,2478.5,2479.0,2479.5,
    2480.0,2480.5,2481.0,2482.0,2483.0,2484.0,2485.0,2486.0, 2487.0,2488.0,2489.0,2490.0,2492.5,2495.0,2500.0,2510.0,2515.0]

    waxs_arc = [20]
    ai0_all = 0
    ai_list = [0.80]

    for name, xs, ys, zs, xs_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa):
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, xs)
        if name != 'PK_B61':
            yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)

        if name != 'PK_B61':
            yield from bps.mv(piezo.th, ai0_all)
            yield from alignement_gisaxs_doblestack(0.8)

        ai0 = piezo.th.position
        det_exposure_time(t, t)

        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)
            # Do not take SAXS when WAXS detector in the way
            dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]

            yield from bps.mv(piezo.x, xs)
            counter = 0

            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                name_fmt = "{sample}_pos1_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs - counter * 70)
                    counter += 1
                    
                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)


                name_fmt = "{sample}_pos2_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies[::-1]:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs - counter * 70)
                    counter += 1

                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)

            yield from bps.mv(piezo.th, ai0)



def flatfield_S_scan(t=1):
    waxs_arc=np.linspace(30, 51.7511, 619)
    name = 'flatfieldscan_Segde_KPSS_pos1_2515eV_ai0.8deg_1s_camserverenergy2450threshold1600eV'
    name_fmt = "{sample}_wa{wax}"
    det=[pil900KW]
    det_exposure_time(t, t)

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)

        sample_name = name_fmt.format(sample=name, wax="%3.3f"%wa)
        sample_id(user_name="LR", sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")
        yield from bp.count(det, num=1)



def flatfield_Cl_scan(t=1):
    waxs_arc=np.linspace(30, 51.7511, 62)
    name = 'flatfieldscan_Clegde_PVC_pos1_2890eV_ai0.8deg_1s_camserverenergy2800threshold1700eV'
    name_fmt = "{sample}_wa{wax}"
    det=[pil900KW]
    det_exposure_time(t, t)

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)

        sample_name = name_fmt.format(sample=name, wax="%3.3f"%wa)
        sample_id(user_name="LR", sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")
        yield from bp.count(det, num=1)



def bpmvspindiode_Sedge(t=1):
    dets = [pil1M]
    det_exposure_time(t, t)

    name = 'direct_beam_Sedge_scannormal'


    energies = [2450.0,2455.0,2460.0,2465.0,2470.0,2473.0,2475.0,2475.5,2476.0,2476.5,2477.0,2477.5,2478.0,2478.5,2479.0,2479.5,
    2480.0,2480.5,2481.0,2482.0,2483.0,2484.0,2485.0,2486.0, 2487.0,2488.0,2489.0,2490.0,2492.5,2495.0,2500.0,2510.0,2515.0]
    
    list_ener = energies + energies[::-1]

    # yield from bp.list_scan([energy, xbpm2, xbpm3, pdcurrent2], energy, list_ener)

    for e in energies:
        yield from bps.mv(energy, e)
        yield from bps.sleep(2)
        if xbpm2.sumX.get() < 50:
            yield from bps.sleep(2)
            yield from bps.mv(energy, e)
            yield from bps.sleep(2)

        fs.open()
        yield from bps.sleep(2)
        bpm2 = xbpm2.sumX.get()
        bpm3 = xbpm3.sumX.get()
        pdc = pdcurrent2.get()
        fs.close()

        name_fmt = "{sample}_pos1_{energy}eV_bpm2_{xbpm2}_bpm3_{xbpm3}_pd_{pd}"

        sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, xbpm2="%4.3f"%bpm2, xbpm3="%4.3f"%bpm3, pd="%4.3f"%pdc)
        sample_id(user_name="LR", sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")

        yield from bp.count([pil1M], num=1)


    for e in energies[::-1]:
        yield from bps.mv(energy, e)
        yield from bps.sleep(2)
        if xbpm2.sumX.get() < 50:
            yield from bps.sleep(2)
            yield from bps.mv(energy, e)
            yield from bps.sleep(2)

        fs.open()
        yield from bps.sleep(2)
        bpm2 = xbpm2.sumX.get()
        bpm3 = xbpm3.sumX.get()
        pdc = pdcurrent2.get()
        fs.close()

        name_fmt = "{sample}_pos2_{energy}eV_bpm2_{xbpm2}_bpm3_{xbpm3}_pd_{pd}"

        sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, xbpm2="%4.3f"%bpm2, xbpm3="%4.3f"%bpm3, pd="%4.3f"%pdc)
        sample_id(user_name="LR", sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")

        yield from bp.count([pil1M], num=1)



def bpmvspindiode_Cledge(t=1):
    dets = [pil1M]
    det_exposure_time(t, t)

    name = 'direct_beam_Cledge_scannormal'

    energies = np.asarray([2810.0, 2820.0, 2830.0, 2832.0, 2834.0, 2834.5, 2835.0, 2835.5, 2836.0, 2836.5, 2837.0, 2837.5, 2838.0, 2838.5, 2839.0,
    2839.5, 2840.0, 2840.5, 2841.0, 2841.5, 2845.0, 2850.0, 2855.0, 2860.0, 2865.0, 2870.0, 2875.0, 2880.0, 2890.0])

    list_ener = energies + energies[::-1]

    # yield from bp.list_scan([energy, xbpm2, xbpm3, pdcurrent2], energy, list_ener)

    for e in energies:
        yield from bps.mv(energy, e)
        yield from bps.sleep(2)
        if xbpm2.sumX.get() < 50:
            yield from bps.sleep(2)
            yield from bps.mv(energy, e)
            yield from bps.sleep(2)

        fs.open()
        yield from bps.sleep(2)
        bpm2 = xbpm2.sumX.get()
        bpm3 = xbpm3.sumX.get()
        pdc = pdcurrent2.get()
        fs.close()

        name_fmt = "{sample}_pos1_{energy}eV_bpm2_{xbpm2}_bpm3_{xbpm3}_pd_{pd}"

        sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, xbpm2="%4.3f"%bpm2, xbpm3="%4.3f"%bpm3, pd="%4.3f"%pdc)
        sample_id(user_name="LR", sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")

        yield from bp.count([pil1M], num=1)


    for e in energies[::-1]:
        yield from bps.mv(energy, e)
        yield from bps.sleep(2)
        if xbpm2.sumX.get() < 50:
            yield from bps.sleep(2)
            yield from bps.mv(energy, e)
            yield from bps.sleep(2)

        fs.open()
        yield from bps.sleep(2)
        bpm2 = xbpm2.sumX.get()
        bpm3 = xbpm3.sumX.get()
        pdc = pdcurrent2.get()
        fs.close()

        name_fmt = "{sample}_pos2_{energy}eV_bpm2_{xbpm2}_bpm3_{xbpm3}_pd_{pd}"

        sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, xbpm2="%4.3f"%bpm2, xbpm3="%4.3f"%bpm3, pd="%4.3f"%pdc)
        sample_id(user_name="LR", sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")

        yield from bp.count([pil1M], num=1)


def bpmvspindiode_Kedge(t=1):
    dets = [pil1M]
    det_exposure_time(t, t)

    name = 'direct_beam_Kedge_scannormal'

    energies = np.asarray(np.arange(3580, 3611, 5).tolist() + 
                          np.arange(3612, 3629, 1).tolist() + 
                          np.arange(3630, 3700, 5).tolist())
    

    list_ener = energies + energies[::-1]

    # yield from bp.list_scan([energy, xbpm2, xbpm3, pdcurrent2], energy, list_ener)

    for e in energies:
        yield from bps.mv(energy, e)
        yield from bps.sleep(2)
        if xbpm2.sumX.get() < 50:
            yield from bps.sleep(2)
            yield from bps.mv(energy, e)
            yield from bps.sleep(2)

        fs.open()
        yield from bps.sleep(2)
        bpm2 = xbpm2.sumX.get()
        bpm3 = xbpm3.sumX.get()
        pdc = pdcurrent2.get()
        fs.close()

        name_fmt = "{sample}_pos1_{energy}eV_bpm2_{xbpm2}_bpm3_{xbpm3}_pd_{pd}"

        sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, xbpm2="%4.3f"%bpm2, xbpm3="%4.3f"%bpm3, pd="%4.3f"%pdc)
        sample_id(user_name="LR", sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")

        yield from bp.count([pil1M], num=1)


    for e in energies[::-1]:
        yield from bps.mv(energy, e)
        yield from bps.sleep(2)
        if xbpm2.sumX.get() < 50:
            yield from bps.sleep(2)
            yield from bps.mv(energy, e)
            yield from bps.sleep(2)

        fs.open()
        yield from bps.sleep(2)
        bpm2 = xbpm2.sumX.get()
        bpm3 = xbpm3.sumX.get()
        pdc = pdcurrent2.get()
        fs.close()

        name_fmt = "{sample}_pos2_{energy}eV_bpm2_{xbpm2}_bpm3_{xbpm3}_pd_{pd}"

        sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, xbpm2="%4.3f"%bpm2, xbpm3="%4.3f"%bpm3, pd="%4.3f"%pdc)
        sample_id(user_name="LR", sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")

        yield from bp.count([pil1M], num=1)



def Cl_edge_measurments_2023_3_Dec1_Night(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    # top left first
    names = [    'Ginger_2',     'Ginger_3',      'Ginger_4',     'Ginger_5',  'Ginger_6',   'Ginger_7',  'Ginger_1a',     'Ginger_1b',       
                 'Ginger_8',      'Ginger_9',          'PVC',         'P3HT']
    x_piezo = [      -28000,          -13000,           4000,          20000,       35000,        52000, -49000,           -43000,
                     -48000,           -42000,        -28000,         -10000]
    x_hexa = [            0,              0,               0,           0,          0,            0,    -12,                0,
                       -10,                0,               0,               0]
    y_piezo = [      4900,             4900,             4900,           4900,        4900,             4900,             4900,           4900,
                      -3600,            -3600,            -3600,          -3600]
    z_piezo = [       7000,             7000,             7000,           7000,         7000,        7000,       7000,          7000,
                      7000,             7000,             7000,           7000]
    
    x_piezo = 0 + np.asarray(x_piezo)
    
    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples1 ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples2 ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples3 ({len(z_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples4 ({len(x_hexa)})"

    # energies = -10 + np.asarray([2810.0, 2820.0, 2830.0, 2832.0, 2834.0, 2834.5, 2835.0, 2835.5, 2836.0, 2836.5, 2837.0, 2837.5, 2838.0, 2838.5, 2839.0,
    # 2839.5, 2840.0, 2840.5, 2841.0, 2841.5, 2845.0, 2850.0, 2855.0, 2860.0, 2865.0, 2870.0, 2875.0, 2880.0, 2890.0])
    
    energies = -10 + np.asarray([2810.0, 2820.0, 2828.0, 2829.0, 2830.0, 2831.0, 2832.0, 2833.0, 2834.0, 2834.5, 2835.0, 2835.5, 2836.0, 2836.5, 2837.0, 2837.5, 2838.0, 2838.5, 2839.0,
    2839.5, 2840.0, 2840.5, 2841.0, 2841.5, 2845.0, 2850.0, 2855.0, 2860.0, 2865.0, 2870.0, 2875.0, 2880.0, 2890.0])

    waxs_arc = [0, 20]
    ai0_all = 0
    ai_list = [0.80]

    for name, xs, ys, zs, xs_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa):
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)

        yield from bps.mv(piezo.th, ai0_all)
        yield from alignement_gisaxs_doblestack(0.8)

        yield from bps.mv(att2_9.open_cmd, 1)
        yield from bps.sleep(1)
        yield from bps.mv(att2_9.open_cmd, 1)

        ai0 = piezo.th.position
        det_exposure_time(t, t)

        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)
            # Do not take SAXS when WAXS detector in the way
            dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]

            yield from bps.mv(piezo.x, xs)
            counter = 0

            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                name_fmt = "{sample}_pos1_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs - counter * 30)
                    counter += 1

                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)

                name_fmt = "{sample}_pos2_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies[::-1]:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs - counter * 30)
                    counter += 1

                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)

            yield from bps.mv(piezo.th, ai0)




def S_edge_measurments_2023_3_Dec1(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    # top left first
    names = [    'Ginger_2',     'Ginger_3',      'Ginger_4',     'Ginger_5',  'Ginger_6',   'Ginger_7',  'Ginger_1a',     'Ginger_1b',       
                 'Ginger_8',      'Ginger_9',          'PVC',         'P3HT']
    x_piezo = [      -28000,          -13000,           4000,          20000,       35000,        52000, -49000,           -43000,
                     -48000,           -42000,        -28000,         -10000]
    x_hexa = [            0,              0,               0,           0,          0,            0,    -12,                0,
                       -10,                0,               0,               0]
    y_piezo = [      4900,             4900,             4900,           4900,        4900,             4900,             4900,           4900,
                      -3600,            -3600,            -3600,          -3600]
    z_piezo = [       7000,             7000,             7000,           7000,         7000,        7000,       7000,          7000,
                      7000,             7000,             7000,           7000]
    
    x_piezo = -2500 + np.asarray(x_piezo)


    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(z_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexa)})"

    energies = [2450.0,2455.0,2460.0,2465.0,2470.0,2473.0,2475.0,2475.5,2476.0,2476.5,2477.0,2477.5,2478.0,2478.5,2479.0,2479.5,
    2480.0,2480.5,2481.0,2482.0,2483.0,2484.0,2485.0,2486.0, 2487.0,2488.0,2489.0,2490.0,2492.5,2495.0,2500.0,2510.0,2515.0]

    waxs_arc = [0, 20]
    ai0_all = 0
    ai_list = [0.80]

    for name, xs, ys, zs, xs_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa):
        try:
            yield from bps.mv(stage.x, xs_hexa)
            yield from bps.mv(piezo.x, xs)
            yield from bps.mv(piezo.y, ys)
            yield from bps.mv(piezo.z, zs)

            yield from bps.mv(piezo.th, ai0_all)
            yield from alignement_gisaxs_doblestack(0.8)

            ai0 = piezo.th.position
            det_exposure_time(t, t)

            for i, wa in enumerate(waxs_arc):
                yield from bps.mv(waxs, wa)
                # Do not take SAXS when WAXS detector in the way
                dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]

                yield from bps.mv(piezo.x, xs)
                counter = 0

                for k, ais in enumerate(ai_list):
                    yield from bps.mv(piezo.th, ai0 + ais)

                    name_fmt = "{sample}_pos1_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                    for e in energies:
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                        if xbpm2.sumX.get() < 50:
                            yield from bps.sleep(2)
                            yield from bps.mv(energy, e)
                            yield from bps.sleep(2)
                        yield from bps.mv(piezo.x, xs - counter * 30)
                        counter += 1
                        
                        bpm = xbpm2.sumX.get()
                        sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                        sample_id(user_name="LR", sample_name=sample_name)
                        print(f"\n\t=== Sample: {sample_name} ===\n")
                        yield from bp.count(dets, num=1)


                    name_fmt = "{sample}_pos2_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                    for e in energies[::-1]:
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                        if xbpm2.sumX.get() < 50:
                            yield from bps.sleep(2)
                            yield from bps.mv(energy, e)
                            yield from bps.sleep(2)
                        yield from bps.mv(piezo.x, xs - counter * 30)
                        counter += 1

                        bpm = xbpm2.sumX.get()
                        sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                        sample_id(user_name="LR", sample_name=sample_name)
                        print(f"\n\t=== Sample: {sample_name} ===\n")
                        yield from bp.count(dets, num=1)

                yield from bps.mv(piezo.th, ai0)
        except:
            print(name, 'did not aligned')    


def night_Dec1(t=1):
    proposal_id("2023_3", "313690_Richter_01")
    yield from Cl_edge_measurments_2023_3_Dec1_Night(t=t)

    yield from transition_Cl_S_edges()

    proposal_id("2023_3", "313690_Richter_02")
    yield from S_edge_measurments_2023_3_Dec1(t=t)





def K_edge_xscan_2023_3(t=1):
    dets = [pil900KW, amptek]
    det_exposure_time(t, t)

    # names = ['PBBTme_dry']
    # x_min = [-22]
    # x_max =  [-12]

    names = ['pgBTTT_KCl_sample3_Vds500mV_Vgs100mV_gradient800mV_try1']
    x_min = [19.1]
    x_max = [10.1]
    

    step= 0.2
    assert len(x_min) == len(names), f"Number of X coordinates ({len(x_hexa)}) is different from number of samples ({len(names)})"
    assert len(x_max) == len(names), f"Number of X coordinates ({len(x_hexa)}) is different from number of samples ({len(y_hexa)})"

    energies = energy.energy.position

    waxs_arc = [0]
    ais = 0.80
    ai0 = stage.th.position

    for name, xmin, xmax in zip(names, x_min, x_max):
        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)
            # Do not take SAXS when WAXS detector in the way
            yield from bps.mv(stage.th, ai0 + ais)

            name_fmt = "{sample}_xscan_{energy}eV_x{x}_ai{ai}_wa{wax}_bpm{xbpm}"
            yield from bps.mv(energy, energies)
            yield from bps.sleep(2)
            yield from bps.sleep(2)

            # for ais in np.linspace(0.1, 0.8, 15):
            for xss in np.linspace(xmin, xmax, int(1+(xmin-xmax)/step)):
                # yield from bps.mv(stage.th, ai0+ais)                

                yield from bps.mv(stage.x, xss)                
                bpm = xbpm2.sumX.get()
                sample_name = name_fmt.format(sample=name, energy="%6.2f"%energies, x="%1.2f"%stage.x.position, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                sample_id(user_name="LR", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

            yield from bps.mv(stage.th, ai0)



def K_edge_timescan_2023_3(t=1):
    dets = [pil900KW, amptek]
    det_exposure_time(t, t)
    energies=energy.energy.position
    ais=0.8
    wa=0
    name = 'pgBTTT_KCl_sample3_Vds500mV_Vgs200mV_reversed_x14.5_timescan_try5'
    # name = 'test_timescan_try5'

    t0 = time.time()
    for i in range(100):
        t1 = time.time()
        name_fmt = "{sample}_{energy}eV_time{times}_ai{ai}_wa{wax}_bpm{xbpm}"
        bpm = xbpm2.sumX.get()
        sample_name = name_fmt.format(sample=name, energy="%6.2f"%energies, times="%1.2f"%(t1-t0), ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
        sample_id(user_name="LR", sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")
        yield from bp.count(dets, num=1)



def Cl_edge_measurments_2023_3_Dec2_dinner(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    # bottom left first
    names = [     'dg00',     'dg25',      'dg50',     'dg75',  'dg100',   'ddg75',  'ddg100',       
                 'acg00',    'acg25',     'acg50',    'acg75', 'acg100',   'ddg00',   'ddg25',     'ddg50',  'Ginger_6']
    x_piezo = [   -42000,     -37000,      -21000,      -7000,     8000,     24000,     41000,
                  -43000,     -37000,      -21000,      -7000,     8000,     24000,     39000,       44000,       45000]
    x_hexa = [       -10,          0,           0,          0,        0,         0,         0,
                     -10,          0,           0,          0,        0,         0,         0,          10,          10]
    y_piezo = [     4900,       4900,        4900,       4900,     4900,      4900,      4900,
                   -3600,      -3600,       -3600,      -3600,    -3600,     -3600,     -3600,       -3600,        4900]
    z_piezo = [     7000,       7000,        7000,       7000,     7000,      7000,      7000,
                    7000,       7000,        7000,       7000,     7000,      7000,      7000,        7000,        7000]
    
    x_piezo = 0 + np.asarray(x_piezo)
    
    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples1 ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples2 ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples3 ({len(z_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples4 ({len(x_hexa)})"

    # energies = -10 + np.asarray([2810.0, 2820.0, 2830.0, 2832.0, 2834.0, 2834.5, 2835.0, 2835.5, 2836.0, 2836.5, 2837.0, 2837.5, 2838.0, 2838.5, 2839.0,
    # 2839.5, 2840.0, 2840.5, 2841.0, 2841.5, 2845.0, 2850.0, 2855.0, 2860.0, 2865.0, 2870.0, 2875.0, 2880.0, 2890.0])
    
    energies = -10 + np.asarray([2810.0, 2820.0, 2828.0, 2829.0, 2830.0, 2831.0, 2832.0, 2833.0, 2834.0, 2834.5, 2835.0, 2835.5, 2836.0, 2836.5, 2837.0, 2837.5, 2838.0, 2838.5, 2839.0,
    2839.5, 2840.0, 2840.5, 2841.0, 2841.5, 2845.0, 2850.0, 2855.0, 2860.0, 2865.0, 2870.0, 2875.0, 2880.0, 2890.0])

 
    energies1 = -10 + np.asarray([2810.0, 2820.0, 2828.0, 2829.0, 2830.0, 2831.0, 2832.0, 2833.0, 2834.0, 2834.5, 2835.0, 2835.5, 2836.0, 2836.5, 2837.0, 2837.5, 2838.0, 2838.5, 2839.0,
    2839.5, 2840.0, 2840.5, 2841.0, 2841.5, 2845.0, 2850.0, 2855.0, 2860.0, 2865.0, 2870.0, 2875.0, 2880.0, 2890.0])

    energies2 =   -7 + np.asarray([2810.0, 2820.0, 2830.0, 2832.0, 2834.0, 2834.5, 2835.0, 2835.5, 2836.0, 2836.5, 2837.0, 2837.5, 2838.0, 2838.5, 2839.0,
    2839.5, 2840.0, 2840.5, 2841.0, 2841.5, 2845.0, 2850.0, 2855.0, 2860.0, 2865.0, 2870.0, 2875.0, 2880.0, 2890.0])
    
    waxs_arc = [0, 20]
    ai0_all = 0
    ai_list = [0.80]

    for name, xs, ys, zs, xs_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa):
        if name == 'Ginger_6':
            ai_list = [1.6, 3.2]
            energies = energies1

        else:
            ai_list = [0.80]
            energies = energies2

        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)

        yield from bps.mv(piezo.th, ai0_all)
        yield from alignement_gisaxs_doblestack(0.8)

        yield from bps.mv(att2_9.open_cmd, 1)
        yield from bps.sleep(1)
        yield from bps.mv(att2_9.open_cmd, 1)

        ai0 = piezo.th.position
        det_exposure_time(t, t)

        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)
            # Do not take SAXS when WAXS detector in the way
            dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]

            yield from bps.mv(piezo.x, xs)
            counter = 0

            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                name_fmt = "{sample}_pos1_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs - counter * 30)
                    counter += 1

                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)

                name_fmt = "{sample}_pos2_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies[::-1]:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs - counter * 30)
                    counter += 1

                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)

            yield from bps.mv(piezo.th, ai0)



def Cl_edge_measurments_2023_3_Dec2_night(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    # bottom left first
    names = [       'acidPEDOT_neat',       'acidPEDOT_exposed_KCl',        'acidPEDOT_dedope_n600mV',      'acidPEDOT_redope_0mV',         'acidPEDOT_overdope_p600mV',        'EG_PEDOT',                 'EG_PEDOT_exposed_KCl',         'EG_PEDOT_dedope_n600mV',      'EG_PEDOT_redope_0mV',      'EG_PEDOT_overdope_p600mV',  
                    'PVC',                  'KPSS',                         'P3HT',                         'PBTTME_as',                    'PBTTME_exp',                       'PBTTME_dedope_n400mV',     'PBTTME_dope_p100mV',           'PBTTME_dope_p400mV',     '     PBTTME_dope_p600mV',        'Ginger_6']             
    x_piezo = [     -49000,                 -49000,                         -37000,                         -24000,                          -10000,                              9000,                     21000,                          32000,                          48000,                       50000,     
                    -50000,                  -51000,                         -40000,                         -24000,                         -10000,                              4000,                      19000,                         33000,                          48000,                       51000]
    x_hexa = [      -12,                    0,                              0,                              0,                              0,                                  0,                        0,                              0,                                 0,                         10,                              
                    -12,                      0,                              0,                             0,                             0,                                 0,                         0,                             0,                                 0,                         10    ]
    y_piezo = [     4900,                   4900,                           4900,                           4900,                           4900,                               4900,                       4900,                           4900,                           4900,                       4900,                   
                    -3600,                  -3600,                          -3600,                          -3600,                          -3600,                              -3600,                      -3600,                          -3600,                          -3600,                       -3600]
    z_piezo = [     7000,                   7000,                           7000,                           7000,                           7000,                               7000,                       7000,                           7000,                           7000,                       7000,      
                    7000,                   7000,                           7000,                           7000,                           7000,                               7000,                       7000,                           7000,                           7000,                       7000]
    
    x_piezo = 0 + np.asarray(x_piezo)
    
    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples1 ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples2 ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples3 ({len(z_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples4 ({len(x_hexa)})"

    # energies = -10 + np.asarray([2810.0, 2820.0, 2830.0, 2832.0, 2834.0, 2834.5, 2835.0, 2835.5, 2836.0, 2836.5, 2837.0, 2837.5, 2838.0, 2838.5, 2839.0,
    # 2839.5, 2840.0, 2840.5, 2841.0, 2841.5, 2845.0, 2850.0, 2855.0, 2860.0, 2865.0, 2870.0, 2875.0, 2880.0, 2890.0])
    
    energies2 =   -7 + np.asarray([2810.0, 2820.0, 2830.0, 2832.0, 2834.0, 2834.5, 2835.0, 2835.5, 2836.0, 2836.5, 2837.0, 2837.5, 2838.0, 2838.5, 2839.0,
    2839.5, 2840.0, 2840.5, 2841.0, 2841.5, 2845.0, 2850.0, 2855.0, 2860.0, 2865.0, 2870.0, 2875.0, 2880.0, 2890.0])
    
    energies1 = -10 + np.asarray([2810.0, 2820.0, 2828.0, 2829.0, 2830.0, 2831.0, 2832.0, 2833.0, 2834.0, 2834.5, 2835.0, 2835.5, 2836.0, 2836.5, 2837.0, 2837.5, 2838.0, 2838.5, 2839.0,
    2839.5, 2840.0, 2840.5, 2841.0, 2841.5, 2845.0, 2850.0, 2855.0, 2860.0, 2865.0, 2870.0, 2875.0, 2880.0, 2890.0])

    waxs_arc = [0, 20]
    ai0_all = 0
    ai_list = [0.80]

    for name, xs, ys, zs, xs_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa):
        if name == 'Ginger_6':
            ai_list = [1.6, 3.2]
            energies = energies1

        else:
            ai_list = [0.80]
            energies = energies2

        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)

        yield from bps.mv(piezo.th, ai0_all)
        yield from alignement_gisaxs_doblestack(0.8)

        yield from bps.mv(att2_9.open_cmd, 1)
        yield from bps.sleep(1)
        yield from bps.mv(att2_9.open_cmd, 1)

        ai0 = piezo.th.position
        det_exposure_time(t, t)

        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)
            # Do not take SAXS when WAXS detector in the way
            dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]

            yield from bps.mv(piezo.x, xs)
            counter = 0

            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                name_fmt = "{sample}_pos1_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs - counter * 30)
                    counter += 1

                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)

                name_fmt = "{sample}_pos2_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies[::-1]:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs - counter * 30)
                    counter += 1

                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)

            yield from bps.mv(piezo.th, ai0)

def S_edge_measurments_2023_3_Dec2_night(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    # bottom left first
    names = [       'acidPEDOT_neat',       'acidPEDOT_exposed_KCl',        'acidPEDOT_dedope_n600mV',      'acidPEDOT_redope_0mV',         'acidPEDOT_overdope_p600mV',        'EG_PEDOT',                 'EG_PEDOT_exposed_KCl',         'EG_PEDOT_dedope_n600mV',      'EG_PEDOT_redope_0mV',      'EG_PEDOT_overdope_p600mV',  
                    'PVC',                  'KPSS',                         'P3HT',                         'PBTTME_as',                    'PBTTME_exp',                       'PBTTME_dedope_n400mV',     'PBTTME_dope_p100mV',           'PBTTME_dope_p400mV',     '     PBTTME_dope_p600mV']             
    x_piezo = [     -49000,                 -49000,                         -37000,                         -24000,                          -10000,                              9000,                     21000,                          32000,                          48000,                       50000,     
                    -50000,                  -51000,                         -40000,                         -24000,                         -10000,                              4000,                      19000,                         33000,                          48000]
    x_hexa = [      -12,                    0,                              0,                              0,                              0,                                  0,                        0,                              0,                                 0,                         10,                              
                    -12,                      0,                              0,                             0,                             0,                                 0,                         0,                             0,                                 0]
    y_piezo = [     4900,                   4900,                           4900,                           4900,                           4900,                               4900,                       4900,                           4900,                           4900,                       4900,                   
                    -3600,                  -3600,                          -3600,                          -3600,                          -3600,                              -3600,                      -3600,                          -3600,                          -3600]
    z_piezo = [     7000,                   7000,                           7000,                           7000,                           7000,                               7000,                       7000,                           7000,                           7000,                       7000,      
                    7000,                   7000,                           7000,                           7000,                           7000,                               7000,                       7000,                           7000,                           7000]
    
    x_piezo = -2500 + np.asarray(x_piezo)

    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(z_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexa)})"

    energies = [2450.0,2455.0,2460.0,2465.0,2470.0,2473.0,2475.0,2475.5,2476.0,2476.5,2477.0,2477.5,2478.0,2478.5,2479.0,2479.5,
    2480.0,2480.5,2481.0,2482.0,2483.0,2484.0,2485.0,2486.0, 2487.0,2488.0,2489.0,2490.0,2492.5,2495.0,2500.0,2510.0,2515.0]

    waxs_arc = [0, 20]
    ai0_all = 0
    ai_list = [0.80]

    for name, xs, ys, zs, xs_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa):
        try:
            yield from bps.mv(stage.x, xs_hexa)
            yield from bps.mv(piezo.x, xs)
            yield from bps.mv(piezo.y, ys)
            yield from bps.mv(piezo.z, zs)

            yield from bps.mv(piezo.th, ai0_all)
            yield from alignement_gisaxs_doblestack(0.8)

            ai0 = piezo.th.position
            det_exposure_time(t, t)

            for i, wa in enumerate(waxs_arc):
                yield from bps.mv(waxs, wa)
                # Do not take SAXS when WAXS detector in the way
                dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]

                yield from bps.mv(piezo.x, xs)
                counter = 0

                for k, ais in enumerate(ai_list):
                    yield from bps.mv(piezo.th, ai0 + ais)

                    name_fmt = "{sample}_pos1_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                    for e in energies:
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                        if xbpm2.sumX.get() < 50:
                            yield from bps.sleep(2)
                            yield from bps.mv(energy, e)
                            yield from bps.sleep(2)
                        yield from bps.mv(piezo.x, xs - counter * 30)
                        counter += 1
                        
                        bpm = xbpm2.sumX.get()
                        sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                        sample_id(user_name="LR", sample_name=sample_name)
                        print(f"\n\t=== Sample: {sample_name} ===\n")
                        yield from bp.count(dets, num=1)


                    name_fmt = "{sample}_pos2_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                    for e in energies[::-1]:
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                        if xbpm2.sumX.get() < 50:
                            yield from bps.sleep(2)
                            yield from bps.mv(energy, e)
                            yield from bps.sleep(2)
                        yield from bps.mv(piezo.x, xs - counter * 30)
                        counter += 1

                        bpm = xbpm2.sumX.get()
                        sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                        sample_id(user_name="LR", sample_name=sample_name)
                        print(f"\n\t=== Sample: {sample_name} ===\n")
                        yield from bp.count(dets, num=1)

                yield from bps.mv(piezo.th, ai0)
        except:
            print(name, 'did not aligned')    


def night_Dec2(t=1):

    proposal_id("2023_3", "313690_Richter_05")
    yield from S_edge_measurments_2023_3_Dec2_night(t=t)

    yield from transition_S_Cl_edges()

    proposal_id("2023_3", "313690_Richter_06")
    yield from Cl_edge_measurments_2023_3_Dec2_night(t=t)




def K_edge_measurments_2023_3_sva(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    names = ['pgBTTT_KCl_sample2_600mV_secondpos']
    x_hexa = [16.1]

    assert len(x_hexa) == len(names), f"Number of X coordinates ({len(x_hexa)}) is different from number of samples ({len(names)})"

    energies = np.asarray(np.arange(3580, 3611, 5).tolist() + 
                          np.arange(3612, 3629, 1).tolist() + 
                          np.arange(3630, 3700, 5).tolist())

    waxs_arc = [0]
    ai_list = [0.8]

    for name, xs_hexa in zip(names, x_hexa):
        yield from bps.mv(stage.x, xs_hexa)

        # No alignement 
        yield from bps.mv(stage.th, ai0)
        yield from alignement_gisaxs_hex(0.8)

        # yield from bps.mv(att2_9.open_cmd, 1)
        # yield from bps.sleep(1)
        # yield from bps.mv(att2_9.open_cmd, 1)
        # yield from bps.sleep(1)

        ai0 = stage.th.position
        det_exposure_time(t, t)

        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)
            # Do not take SAXS when WAXS detector in the way
            dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]

            counter = 0

            for k, ais in enumerate(ai_list):
                yield from bps.mv(stage.th, ai0 + ais)

                name_fmt = "{sample}_pos1_{energy}eV_x{x}_ai{ai}_wa{wax}_bpm{xbpm}"
                x="%1.2f"%stage.x.position
                for e in energies:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(stage.x, xs_hexa - counter * 0.030)
                    counter += 1
                    
                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, x=x, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)

                x="%1.2f"%stage.x.position
                name_fmt = "{sample}_pos2_{energy}eV_x{x}_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies[::-1]:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(stage.x, xs_hexa - counter * 0.030)
                    counter += 1

                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, x=x, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)
            yield from bps.mv(stage.th, ai0)


def Cl_edge_measurments_2023_3_sva(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    names = ['pgBTTT_KCl_sample2_600mV_secondpos_Cledge_goodthreshold']

    x_hexa = [18.1]

    assert len(x_hexa) == len(names), f"Number of X coordinates ({len(x_hexa)}) is different from number of samples ({len(names)})"

    energies =   -7 + np.asarray([2810.0, 2820.0, 2830.0, 2832.0, 2834.0, 2834.5, 2835.0, 2835.5, 2836.0, 2836.5, 2837.0, 2837.5, 2838.0, 2838.5, 2839.0,
    2839.5, 2840.0, 2840.5, 2841.0, 2841.5, 2845.0, 2850.0, 2855.0, 2860.0, 2865.0, 2870.0, 2875.0, 2880.0, 2890.0])

    waxs_arc = [0]
    ai_list = [0.8]

    for name, xs_hexa in zip(names, x_hexa):
        yield from bps.mv(stage.x, xs_hexa)

        # No alignement 
        # yield from bps.mv(stage.th, ai0)
        # yield from alignement_gisaxs_hex(0.8)

        # yield from bps.mv(att2_9.open_cmd, 1)
        # yield from bps.sleep(1)
        # yield from bps.mv(att2_9.open_cmd, 1)
        # yield from bps.sleep(1)

        ai0 = stage.th.position
        det_exposure_time(t, t)

        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)
            # Do not take SAXS when WAXS detector in the way
            dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]

            counter = 0

            for k, ais in enumerate(ai_list):
                yield from bps.mv(stage.th, ai0 + ais)

                name_fmt = "{sample}_pos1_{energy}eV_x{x}_ai{ai}_wa{wax}_bpm{xbpm}"
                x="%1.2f"%stage.x.position
                for e in energies:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(stage.x, xs_hexa - counter * 0.030)
                    counter += 1
                    
                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, x=x, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)

                x="%1.2f"%stage.x.position
                name_fmt = "{sample}_pos2_{energy}eV_x{x}_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies[::-1]:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(stage.x, xs_hexa - counter * 0.030)
                    counter += 1

                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, x=x, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)
            yield from bps.mv(stage.th, ai0)




def Cl_edge_measurments_2023_3_Dec3_dinner(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    # bottom left first
    names = [     'AA_co',    'AA_ht',     'AA_mt',   'AA_hTe', 'AA_mTe',   'AA_mB',   'AA_hB', 'PBBT-Me_realdope_p600mV', 'Ginger_6']
    x_piezo = [    -50000,     -50000,      -40000,     -30000,   -14000,     -2000,     10000,                     45000,      51000]
    x_hexa = [        -14,         -3,           0,          0,        0,         0,         0,                         0,         13]
    y_piezo = [      4900,       4900,        4900,       4900,     4900,      4900,      4900,                      4900,       4900]
    z_piezo = [      7000,       7000,        7000,       7000,     7000,      7000,      7000,                      7000,       7000]
    
    x_piezo = 0 + np.asarray(x_piezo)
    
    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples1 ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples2 ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples3 ({len(z_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples4 ({len(x_hexa)})"

    # energies = -10 + np.asarray([2810.0, 2820.0, 2830.0, 2832.0, 2834.0, 2834.5, 2835.0, 2835.5, 2836.0, 2836.5, 2837.0, 2837.5, 2838.0, 2838.5, 2839.0,
    # 2839.5, 2840.0, 2840.5, 2841.0, 2841.5, 2845.0, 2850.0, 2855.0, 2860.0, 2865.0, 2870.0, 2875.0, 2880.0, 2890.0])
    
    energies = -10 + np.asarray([2810.0, 2820.0, 2828.0, 2829.0, 2830.0, 2831.0, 2832.0, 2833.0, 2834.0, 2834.5, 2835.0, 2835.5, 2836.0, 2836.5, 2837.0, 2837.5, 2838.0, 2838.5, 2839.0,
    2839.5, 2840.0, 2840.5, 2841.0, 2841.5, 2845.0, 2850.0, 2855.0, 2860.0, 2865.0, 2870.0, 2875.0, 2880.0, 2890.0])

 
    energies1 = -10 + np.asarray([2810.0, 2820.0, 2828.0, 2829.0, 2830.0, 2831.0, 2832.0, 2833.0, 2834.0, 2834.5, 2835.0, 2835.5, 2836.0, 2836.5, 2837.0, 2837.5, 2838.0, 2838.5, 2839.0,
    2839.5, 2840.0, 2840.5, 2841.0, 2841.5, 2845.0, 2850.0, 2855.0, 2860.0, 2865.0, 2870.0, 2875.0, 2880.0, 2890.0])

    #
    energies2 =   -7 + np.asarray([2810.0, 2820.0, 2830.0, 2832.0, 2834.0, 2834.5, 2835.0, 2835.5, 2836.0, 2836.5, 2837.0, 2837.5, 2838.0, 2838.5, 2839.0,
    2839.5, 2840.0, 2840.5, 2841.0, 2841.5, 2845.0, 2850.0, 2855.0, 2860.0, 2865.0, 2870.0, 2875.0, 2880.0, 2890.0])
    
    waxs_arc = [0, 20]
    ai0_all = 0
    ai_list = [0.80]

    for name, xs, ys, zs, xs_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa):
        if name == 'Ginger_6':
            ai_list = [0.8, 8.0]
            energies = energies1
        
        elif name == 'PBBT-Me_realdope_p600mV':
            ai_list = [0.80]
            energies = energies2
        
        else:
            ai_list = [0.80]
            energies = energies1

        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)

        yield from bps.mv(piezo.th, ai0_all)
        yield from alignement_gisaxs_doblestack(0.8)

        yield from bps.mv(att2_9.open_cmd, 1)
        yield from bps.sleep(1)
        yield from bps.mv(att2_9.open_cmd, 1)

        ai0 = piezo.th.position
        det_exposure_time(t, t)

        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)
            # Do not take SAXS when WAXS detector in the way
            dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]

            yield from bps.mv(piezo.x, xs)
            counter = 0

            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                name_fmt = "{sample}_pos1_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs - counter * 30)
                    counter += 1

                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)

                name_fmt = "{sample}_pos2_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies[::-1]:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs - counter * 30)
                    counter += 1

                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)

            yield from bps.mv(piezo.th, ai0)

def K_edge_measurments_downsweeponly_2023_3_night3(t=1, offset=0, prefix='pos1'):

    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    names = [       'PBDF_as',    'PBDF_n1000mV',       'PBDF_n800mV',       'PBDF_n600mV',         'PBDF_p200mV',        'PBDF_p1000mV',                   'BBL_as',               'BBL_n600mV', 
                 'BBL_n800mV',     'BBL_n1000mV',      'BBL_n1p200mV',    'BBL_n1top600mV',      'acidPEDOT_neat','acidPEDOT_exposed_KCl',  'acidPEDOT_dedope_n600mV',    'acidPEDOT_redope_0mV', 'acidPEDOT_overdope_p600mV',                         'KPSS',       'P3HT']
    x_piezo = [        -46000,            -45000,              -32000,              -20000,                 -8000,                  4000,                      52000,                      53000,                
                       -50000,            -47000,              -34000,              -20000,                 -6000,                  6000,                      19000,                      32000,                       45000,                          55000,        54000]
    x_hexa = [            -12,                 0,                   0,                   0,                     0,                     0,                          0,                         12,              
                          -12,                 0,                   0,                   0,                     0,                     0,                          0,                          0,                           0,                              0,           12]
    y_piezo = [          4900,              4900,                4900,                4900,                  4900,                  4900,                       4900,                       4900,                  
                        -3600,             -3600,               -3600,               -3600,                 -3600,                 -3600,                      -3600,                      -3600,                       -3600,                          -3600,         -3600]
    z_piezo = [          7000,              7000,                7000,                7000,                  7000,                  7000,                       7000,                       7000,                 
                         7000,              7000,                7000,                7000,                  7000,                  7000,                       7000,                       7000,                        7000,                           7000,           7000]
    
    x_piezo = offset + np.asarray(x_piezo)
    
    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(z_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexa)})"

    energies = np.asarray(np.arange(3580, 3611, 5).tolist() + 
                          np.arange(3612, 3629, 1).tolist() + 
                          np.arange(3630, 3700, 5).tolist())
    
    waxs_arc = [0, 20]
    ai0 = 0
    ai_list = [0.80]

    for name, xs, ys, zs, xs_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa):
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)

        yield from bps.mv(piezo.th, ai0)
        yield from alignement_gisaxs_doblestack(0.8)

        yield from bps.mv(att2_9.open_cmd, 1)
        yield from bps.sleep(1)
        yield from bps.mv(att2_9.open_cmd, 1)

        ai0 = piezo.th.position
        det_exposure_time(t, t)

        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)
            # Do not take SAXS when WAXS detector in the way
            dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]

            yield from bps.mv(piezo.x, xs)
            counter = 0

            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                yield from bps.mv(energy, 3580)
                yield from bps.sleep(2)
                yield from bps.mv(energy, 3620)
                yield from bps.sleep(2)
                yield from bps.mv(energy, 3660)
                yield from bps.sleep(2)


                name_fmt = "{sample}_pos2_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies[::-1]:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs - counter * 30)
                    counter += 1

                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name+prefix,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)

            yield from bps.mv(piezo.th, ai0)


def night_Dec3(t=1):
    proposal_id("2023_3", "313690_Richter_09")
    yield from K_edge_measurments_downsweeponly_2023_3_night3(t=1, offset=0, prefix='position1')
    yield from K_edge_measurments_downsweeponly_2023_3_night3(t=1, offset=-2500, prefix='position2')




def Cl_edge_measurments_2023_3_sva_Dec4(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    names = ['pg2TTT_KCl_sample2_sva_dedopedreturn400mV']
    x_hexa = [18.5]

    assert len(x_hexa) == len(names), f"Number of X coordinates ({len(x_hexa)}) is different from number of samples ({len(names)})"

    energies =   -7 + np.asarray([2810.0, 2820.0, 2830.0, 2832.0, 2834.0, 2834.5, 2835.0, 2835.5, 2836.0, 2836.5, 2837.0, 2837.5, 2838.0, 2838.5, 2839.0,
    2839.5, 2840.0, 2840.5, 2841.0, 2841.5, 2845.0, 2850.0, 2855.0, 2860.0, 2865.0, 2870.0, 2875.0, 2880.0, 2890.0])

    waxs_arc = [0]
    ai_list = [0.8]

    for name, xs_hexa in zip(names, x_hexa):
        yield from bps.mv(stage.x, xs_hexa)

        # No alignement 
        # yield from bps.mv(stage.th, ai0)
        # yield from alignement_gisaxs_hex(0.8)

        # yield from bps.mv(att2_9.open_cmd, 1)
        # yield from bps.sleep(1)
        # yield from bps.mv(att2_9.open_cmd, 1)
        # yield from bps.sleep(1)

        ai0 = stage.th.position
        det_exposure_time(t, t)

        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)
            # Do not take SAXS when WAXS detector in the way
            dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]

            counter = 0

            for k, ais in enumerate(ai_list):
                yield from bps.mv(stage.th, ai0 + ais)

                name_fmt = "{sample}_pos1_{energy}eV_x{x}_ai{ai}_wa{wax}_bpm{xbpm}"
                x="%1.2f"%stage.x.position
                for e in energies:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(stage.x, xs_hexa - counter * 0.020)
                    counter += 1
                    
                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, x=x, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)

                x="%1.2f"%stage.x.position
                name_fmt = "{sample}_pos2_{energy}eV_x{x}_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies[::-1]:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(stage.x, xs_hexa - counter * 0.020)
                    counter += 1

                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, x=x, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)
            yield from bps.mv(stage.th, ai0)



def K_edge_measurments_2023_3_diner4(t=1, offset=0, prefix='pos1'):

    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    names = [       'PBDF_as',    'PBDF_n1000mV',       'PBDF_n800mV', 'PBDF_thick_n1000mV',       'acidPEDOT_as',  'acidPEDOT_dedoped_n600mV',   'acidPEDOT_redoped_n600mVto0V' ]
    x_piezo = [        -50000,            -50000,              -39000,              -30000,                -12000,                  4000,                      19000] 
    x_hexa = [            -13,                 0,                   0,                   0,                     0,                     0,                          0]
    y_piezo = [          4900,              4900,                4900,                4900,                  4900,                  4900,                       4900]
    z_piezo = [          7000,              7000,                7000,                7000,                  7000,                  7000,                       7000]
    
    x_piezo = offset + np.asarray(x_piezo)
    
    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(z_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexa)})"

    energies = np.asarray(np.arange(3580, 3611, 5).tolist() + 
                          np.arange(3612, 3629, 1).tolist() + 
                          np.arange(3630, 3700, 5).tolist())
    
    waxs_arc = [0, 20]
    ai0 = 0
    ai_list = [0.80]

    for name, xs, ys, zs, xs_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa):
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)

        yield from bps.mv(piezo.th, ai0)
        yield from alignement_gisaxs_doblestack(0.8)

        yield from bps.mv(att2_9.open_cmd, 1)
        yield from bps.sleep(1)
        yield from bps.mv(att2_9.open_cmd, 1)

        ai0 = piezo.th.position
        det_exposure_time(t, t)

        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)
            # Do not take SAXS when WAXS detector in the way
            dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]

            yield from bps.mv(piezo.x, xs)
            counter = 0

            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                name_fmt = "{sample}_pos1_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs - counter * 30)
                    counter += 1

                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name+prefix,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)


                name_fmt = "{sample}_pos2_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies[::-1]:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs - counter * 30)
                    counter += 1

                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name+prefix,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)

            yield from bps.mv(piezo.th, ai0)



def S_edge_measurments_2024_1_incidentangle(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    # bottom left first
    names = [  'P3HT_3000', 'P3HT_1500', 'P3HT_1000']             
    x_piezo = [      35000,       16000,       -5000]
    x_hexa = [           0,           0,           0]
    y_piezo = [       7000,        7000,        7000]
    z_piezo = [      -3000,       -3000,       -3000]
    
    names = [  'P3HT_1500', 'P3HT_1000']             
    x_piezo = [      16000,       -5000]
    x_hexa = [           0,           0]
    y_piezo = [       7000,        7000]
    z_piezo = [      -3000,       -3000]


    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(z_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexa)})"

    energies = [2450.0,2455.0,2460.0,2465.0,2470.0,2473.0,2475.0,2475.5,2476.0,2476.5,2477.0,2477.5,2478.0,2478.5,2479.0,2479.5,
    2480.0,2480.5,2481.0,2482.0,2483.0,2484.0,2485.0,2486.0, 2487.0,2488.0,2489.0,2490.0,2492.5,2495.0,2500.0,2510.0,2515.0]

    waxs_arc = [0]
    ai0_all = 0
    ai_list = [0.80, 1.6, 3.2]

    for name, xs, ys, zs, xs_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa):
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)

        yield from bps.mv(piezo.th, ai0_all)
        yield from alignement_gisaxs_doblestack(0.7)

        ai0 = piezo.th.position
        det_exposure_time(t, t)

        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)
            # Do not take SAXS when WAXS detector in the way
            dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]

            yield from bps.mv(piezo.x, xs)
            counter = 0

            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                name_fmt = "{sample}_pos1_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs - counter * 30)
                    counter += 1
                    
                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)


                name_fmt = "{sample}_pos2_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies[::-1]:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs - counter * 30)
                    counter += 1

                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)

            yield from bps.mv(piezo.th, ai0)




def bpmvspindiode_Sedge_2024_1(t=1):
    dets = [pil1M]
    det_exposure_time(t, t)

    name = 'direct_beam_Sedge'


    energies = [2450.0,2455.0,2460.0,2465.0,2470.0,2473.0,2475.0,2475.5,2476.0,2476.5,2477.0,2477.5,2478.0,2478.5,2479.0,2479.5,
    2480.0,2480.5,2481.0,2482.0,2483.0,2484.0,2485.0,2486.0, 2487.0,2488.0,2489.0,2490.0,2492.5,2495.0,2500.0,2510.0,2515.0]
    
    for e in energies:
        yield from bps.mv(energy, e)
        yield from bps.sleep(2)
        if xbpm2.sumX.get() < 50:
            yield from bps.sleep(2)
            yield from bps.mv(energy, e)
            yield from bps.sleep(2)

        fs.open()
        yield from bps.sleep(2)
        bpm2 = xbpm2.sumX.get()
        bpm3 = xbpm3.sumX.get()
        pdc = pdcurrent2.get()
        fs.close()

        name_fmt = "{sample}_pos1_{energy}eV_bpm2_{xbpm2}_bpm3_{xbpm3}_pd_{pd}"

        sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, xbpm2="%4.3f"%bpm2, xbpm3="%4.3f"%bpm3, pd="%4.3f"%pdc)
        sample_id(user_name="LR", sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")

        yield from bp.count([pil1M], num=1)



    for e in energies[::-1]:
        yield from bps.mv(energy, e)
        yield from bps.sleep(2)
        if xbpm2.sumX.get() < 50:
            yield from bps.sleep(2)
            yield from bps.mv(energy, e)
            yield from bps.sleep(2)

        fs.open()
        yield from bps.sleep(2)
        bpm2 = xbpm2.sumX.get()
        bpm3 = xbpm3.sumX.get()
        pdc = pdcurrent2.get()
        fs.close()

        name_fmt = "{sample}_pos2_{energy}eV_bpm2_{xbpm2}_bpm3_{xbpm3}_pd_{pd}"

        sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, xbpm2="%4.3f"%bpm2, xbpm3="%4.3f"%bpm3, pd="%4.3f"%pdc)
        sample_id(user_name="LR", sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")

        yield from bp.count([pil1M], num=1)



def bpmvspindiode_Cledge_2024_1(t=1):
    dets = [pil1M]
    det_exposure_time(t, t)

    name = 'direct_beam_Cledge_att2_9'


    energies = np.asarray([2810.0, 2820.0, 2830.0, 2832.0, 2834.0, 2834.5, 2835.0, 2835.5, 2836.0, 2836.5, 2837.0, 2837.5, 2838.0, 2838.5, 2839.0,
    2839.5, 2840.0, 2840.5, 2841.0, 2841.5, 2845.0, 2850.0, 2855.0, 2860.0, 2865.0, 2870.0, 2875.0, 2880.0, 2890.0])

    
    for e in energies:
        yield from bps.mv(energy, e)
        yield from bps.sleep(2)
        if xbpm2.sumX.get() < 50:
            yield from bps.sleep(2)
            yield from bps.mv(energy, e)
            yield from bps.sleep(2)

        fs.open()
        yield from bps.sleep(2)
        bpm2 = xbpm2.sumX.get()
        bpm3 = xbpm3.sumX.get()
        pdc = pdcurrent2.get()
        fs.close()

        name_fmt = "{sample}_pos1_{energy}eV_bpm2_{xbpm2}_bpm3_{xbpm3}_pd_{pd}"

        sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, xbpm2="%4.3f"%bpm2, xbpm3="%4.3f"%bpm3, pd="%4.3f"%pdc)
        sample_id(user_name="LR", sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")

        yield from bp.count([pil1M], num=1)



    for e in energies[::-1]:
        yield from bps.mv(energy, e)
        yield from bps.sleep(2)
        if xbpm2.sumX.get() < 50:
            yield from bps.sleep(2)
            yield from bps.mv(energy, e)
            yield from bps.sleep(2)

        fs.open()
        yield from bps.sleep(2)
        bpm2 = xbpm2.sumX.get()
        bpm3 = xbpm3.sumX.get()
        pdc = pdcurrent2.get()
        fs.close()

        name_fmt = "{sample}_pos2_{energy}eV_bpm2_{xbpm2}_bpm3_{xbpm3}_pd_{pd}"

        sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, xbpm2="%4.3f"%bpm2, xbpm3="%4.3f"%bpm3, pd="%4.3f"%pdc)
        sample_id(user_name="LR", sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")

        yield from bp.count([pil1M], num=1)



    

def Cl_edge_measurments_2024_1_incidentangle(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    # bottom left first
    names = [  'PVC_4000', 'PVC_2000', 'PVC_1000']             
    x_piezo = [     55000,      55000,      43000]
    x_hexa = [         14,          2,          0]
    y_piezo = [      7000,       7000,       7000]
    z_piezo = [     -3000,      -3000,      -3000]

    names = [  'PVC_1000']             
    x_piezo = [     43000]
    x_hexa = [          0]
    y_piezo = [      7000]
    z_piezo = [     -3000]



    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(z_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexa)})"

    energies =   -10 + np.asarray([2810.0, 2820.0, 2830.0, 2832.0, 2834.0, 2834.5, 2835.0, 2835.5, 2836.0, 2836.5, 2837.0, 2837.5, 2838.0, 2838.5, 2839.0,
    2839.5, 2840.0, 2840.5, 2841.0, 2841.5, 2845.0, 2850.0, 2855.0, 2860.0, 2865.0, 2870.0, 2875.0, 2880.0, 2890.0])

    waxs_arc = [0, 20]
    waxs_arc = [0]

    ai0_all = 0
    ai_list = [0.80, 1.6, 3.2]

    for name, xs, ys, zs, xs_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa):
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)

        yield from bps.mv(piezo.th, ai0_all)
        yield from alignement_gisaxs_doblestack(0.7)

        yield from bps.mv(att2_9.open_cmd, 1)
        yield from bps.sleep(1)
        yield from bps.mv(att2_9.open_cmd, 1)
        yield from bps.sleep(1)

        ai0 = piezo.th.position
        det_exposure_time(t, t)

        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)
            # Do not take SAXS when WAXS detector in the way
            dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]

            yield from bps.mv(piezo.x, xs)
            counter = 0

            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                name_fmt = "{sample}_pos1_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs - counter * 30)
                    counter += 1
                    
                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)

                dets = [pil900KW, amptek]
                det_exposure_time(3, 3)
                yield from bps.sleep(5)

                name_fmt = "{sample}_amptek_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                sample_id(user_name="LR", sample_name=sample_name)

                yield from bp.count(dets, num=1)
                yield from bps.sleep(5)

                det_exposure_time(t, t)
                dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]

                name_fmt = "{sample}_pos2_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies[::-1]:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs - counter * 30)
                    counter += 1

                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)

            yield from bps.mv(piezo.th, ai0)



def Cl_edge_measurments_2024_1_Amalie(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    # bottom left first
    names = [  'P3HT_1500', 'Co_25mmol_FeCl3', 'hT_25mmol_FeCl3', 'mT_25mmol_FeCl3', 'hTe_25mmol_FeCl3', 'mTe_25mmol_FeCl3', 'mB_25mmol_FeCl3', 'hB_25mmol_FeCl3']             
    x_piezo = [      30000,             16000,              4000,             -9000,             -23000,             -35000,            -40000,            -47000]
    x_hexa = [           0,                 0,                 0,                 0,                  0,                  0,               -10,               -16]
    y_piezo = [       7000,              7000,              7000,              7000,               7000,               7000,              7000,              7000]
    z_piezo = [      -3000,             -3000,             -3000,             -3000,              -3000,              -3000,             -3000,             -3000]
    
    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(z_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexa)})"

    energies = -10 + np.asarray([2810.0, 2820.0, 2828.0, 2829.0, 2830.0, 2831.0, 2832.0, 2833.0, 2834.0, 2834.5, 2835.0, 2835.5, 2836.0, 2836.5, 2837.0, 2837.5, 2838.0, 2838.5, 2839.0,
    2839.5, 2840.0, 2840.5, 2841.0, 2841.5, 2845.0, 2850.0, 2855.0, 2860.0, 2865.0, 2870.0, 2875.0, 2880.0, 2890.0])

    waxs_arc = [0, 20]
    ai0_all = 0
    ai_list = [1.6, 3.2]

    for name, xs, ys, zs, xs_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa):
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)

        yield from bps.mv(piezo.th, ai0_all)
        yield from alignement_gisaxs_doblestack(0.7)

        yield from bps.mv(att2_9.open_cmd, 1)
        yield from bps.sleep(1)
        yield from bps.mv(att2_9.open_cmd, 1)
        yield from bps.sleep(1)

        ai0 = piezo.th.position
        det_exposure_time(t, t)

        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)
            # Do not take SAXS when WAXS detector in the way
            dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]

            yield from bps.mv(piezo.x, xs)
            counter = 0

            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                name_fmt = "{sample}_pos1_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs - counter * 30)
                    counter += 1
                    
                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)

                dets = [pil900KW, amptek]
                det_exposure_time(3, 3)
                yield from bps.sleep(5)

                name_fmt = "{sample}_amptek_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                sample_id(user_name="LR", sample_name=sample_name)

                yield from bp.count(dets, num=1)
                yield from bps.sleep(5)

                det_exposure_time(t, t)
                dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]

                name_fmt = "{sample}_pos2_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies[::-1]:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs - counter * 30)
                    counter += 1

                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)


            yield from bps.mv(piezo.th, ai0)




def lee_2024_night1(t=1):
    yield from Cl_edge_measurments_2024_1_incidentangle(t=t)
    yield from Cl_edge_measurments_2024_1_Amalie(t=10)




def Fe_edge_measurments_2024_2(t=1):
    dets = [pil900KW, pil1M]
    det_exposure_time(t, t)

    names = [           'Pg2T-TT', 'SolventTreated', 'Doped-FeCl3-0p02', 'Doped-FeCl3-0p05', 'Doped-FeCl3-0p1', 'Doped-FeCl3-0p2', 'Doped-FeCl3-0p5', 'Doped-FeCl3-1p0', 'Substrate']
    x_piezo = [            -46000,           -42000,             -28000,             -11000,             16000,             30000,             45000,             55000,       57000]
    x_hexa = [                -12,                0,                  0,                  0,                 0,                 0,                 0,                 6,          16]
    y_piezo = [              4000,             4000,               4000,               4000,              4000,              4000,              4000,              4000,        4000]
    z_piezo = [             -3000,            -3000,              -3000,              -3000,             -3000,             -3000,             -3000,             -3000,       -3000]
       
    names = [          'Substrate']
    x_piezo = [                     57000]
    x_hexa = [                   16]
    y_piezo = [             4000]
    z_piezo = [            -3000]
       



    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(z_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexa)})"

    energies = [7100, 7105, 7110, 7112, 7114, 7115, 7116, 7117, 7118, 7119, 7121, 7122, 7123, 7124, 7125, 7126, 7127, 7128, 7129, 7130, 
                7131, 7132, 7133, 7134, 7135, 7136, 7137, 7138, 7139, 7140, 7141, 7142, 7143, 7145, 7147, 7150, 7155, 7160, 7165]

    waxs_arc = [0, 20]
    ai0_all = 1.5
    ai_list = [0.75]

    for name, xs, ys, zs, xs_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa):
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)

        yield from bps.mv(piezo.th, ai0_all)
        yield from alignement_gisaxs_doblestack(0.5)

        yield from bps.mv(att2_6.open_cmd, 1)
        yield from bps.sleep(1)
        yield from bps.mv(att2_6.open_cmd, 1)
        yield from bps.sleep(1)

        ai0 = piezo.th.position
        det_exposure_time(t, t)

        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)
            # Do not take SAXS when WAXS detector in the way

            yield from bps.mv(piezo.x, xs)
            counter = 0

            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                name_fmt = "{sample}_pos1_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 5:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs - counter * 30)
                    counter += 1
                    
                    bpm = xbpm3.sumX.get()
                    sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="LR", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)

                name_fmt = "{sample}_pos2_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies[::-1]:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 5:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs - counter * 30)
                    counter += 1

                    bpm = xbpm3.sumX.get()
                    sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="NS", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)


            yield from bps.mv(piezo.th, ai0)




def S_edge_measurments_2025_1(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    # bottom left first
    names = ['PBTTTC14_as','PBTTTC14_AcN',     'PVC',     'NaPSS', 
        'PBTTTC14_0p02','PBTTTC14_0p05','PBTTTC14_0p1','PBTTTC14_0p2', 'PBTTTC14_0p5' , 'PBTTTC14_1_FeCl3', 'PBTTTC14_0p5_washed', 'PBTTTC14_1_washed' ]             
    x_piezo = [     -49000,      -39000,      -25000,      -10000,
                    -47000,      -30000,      -15000,           0,       20000,       35000,       51000,        55000]
    x_hexa = [          -9,        -0.5,           0,           0,
                        -1,           0,           0,           0,           0,           0,           0,           10]
    y_hexa = [           3,           3,           3,           3,
                      -0.5,        -0.5,        -0.5,        -0.5,        -0.5,        -0.5,        -0.5,        -0.5]
    y_piezo = [          0,           0,           0,           0,
                     -5000,       -5000,       -5000,       -5000,       -5000,       -5000,       -5000,       -5000]
    z_piezo = [       4000,        4000,        4000,        4000,
                      4000,        4000,        4000,        4000,        4000,        4000,        4000,        4000]
    

    # # bottom left first
    # names = [   'MoS2_EMIM_80', 'MoS2_100_ann', 
    #          'MoS2_BBL_print', 'MoS2_new_80', 'MoS2_new_80_ann',
    #          'PBTTTC14_0p02', 'PBTTTC14_0p05', 'PBTTTC14_0p1', 'PBTTTC14_0p2', 'PBTTTC14_0p5' , 'PBTTTC14_1_FeCl3', 'PBTTTC14_0p5_washed', 'PBTTTC14_1_washed' ]             
    # x_piezo = [      12500,       24500,       38000,       50000,        55000,
    #                 -47000,      -30000,      -15000,           0,       20000,       35000,       51000,        55000]
    # x_hexa = [           0,           0,           0,           0,            8,
    #                     -1,           0,           0,           0,           0,           0,           0,           10]
    # y_hexa = [           3,           3,           3,           3,            3,
    #                   -0.5,        -0.5,        -0.5,        -0.5,        -0.5,        -0.5,        -0.5,        -0.5]
    # y_piezo = [          0,           0,           0,           0,            0,
    #                  -5000,       -5000,       -5000,       -5000,       -5000,       -5000,       -5000,       -5000]
    # z_piezo = [       4000,        4000,        4000,        4000,         4000,
    #                   4000,        4000,        4000,        4000,        4000,        4000,        4000,        4000]
    

    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(z_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexa)})"
    assert len(x_piezo) == len(y_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_hexa)})"


    energies1 = [2450.0,2455.0,2460.0,2465.0,2470.0,2473.0,2475.0,2475.5,2476.0,2476.5,2477.0,2477.5,2478.0,2478.5,2479.0,2479.5,
    2480.0,2480.5,2481.0,2482.0,2483.0,2484.0,2485.0,2486.0, 2487.0,2488.0,2489.0,2490.0,2492.5,2495.0,2500.0,2510.0,2515.0]


    # energies2 = [2450.0,2455.0,2460.0,2465.0,2470.0,2472.0,2472.5,2473.0,2473.5,2474.0,2474.5,2475.0,2475.5,2476.0,2476.5,2477.0,2477.5,2478.0,2478.5,2479.0,2479.5,
    # 2480.0,2480.5,2481.0,2481.5,2482.0,2482.5,2483.0,2483.5,2484.0,2484.5,2485.0,2485.5,2486.0,2486.5,2487.0,2487.5,2488.0,2488.5,2489.0,2490.0,2490.5,2491.0,
    # 2491.5,2492.0,2493,2495.0,2500.0,2510.0,2515.0]

    waxs_arc = [0]
    ai0_all = -0.5
    ai_list = [0.80, 1.6, 3.2]

    for name, xs, ys, zs, xs_hexa, ys_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa, y_hexa):
        if 'MoS2' in name:
            energies = energies2
            x_step = 20
        else:
            energies = energies1
            x_step = 30

        yield from bps.mv(stage.x, xs_hexa,
                          stage.y, ys_hexa,
                          piezo.x, xs,
                          piezo.y, ys,
                          piezo.z, zs)

        yield from bps.mv(piezo.th, ai0_all)
        yield from alignement_gisaxs_doblestack(0.7)

        ai0 = piezo.th.position
        det_exposure_time(t, t)

        s = Signal(name='target_file_name', value='')

        @bpp.stage_decorator(dets)
        @bpp.run_decorator(md={'sample_name' :'{target_file_name}'})
        def inner():

            for i, wa in enumerate(waxs_arc):
                yield from bps.mv(waxs, wa)
                # Do not take SAXS when WAXS detector in the way
                dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]

                yield from bps.mv(piezo.x, xs)
                counter = 0

                for k, ais in enumerate(ai_list):
                    yield from bps.mv(piezo.th, ai0 + ais)

                    name_fmt = "{sample}_pos1_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                    for e in energies:
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                        if xbpm2.sumX.get() < 50:
                            yield from bps.sleep(2)
                            yield from bps.mv(energy, e)
                            yield from bps.sleep(2)
                        yield from bps.mv(piezo.x, xs - counter * x_step)
                        counter += 1
                        
                        bpm = xbpm2.sumX.get()
                        sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                        print(f"\n\t=== Sample: {sample_name} ===\n")
                        s.put(sample_name)
                        yield from bps.trigger_and_read(dets + [energy, waxs, xbpm2, xbpm3, ] + [s])


                    name_fmt = "{sample}_pos2_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                    for e in energies[::-1]:
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                        if xbpm2.sumX.get() < 50:
                            yield from bps.sleep(2)
                            yield from bps.mv(energy, e)
                            yield from bps.sleep(2)
                        yield from bps.mv(piezo.x, xs - counter * x_step)
                        counter += 1

                        bpm = xbpm2.sumX.get()
                        sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                        print(f"\n\t=== Sample: {sample_name} ===\n")
                        s.put(sample_name)
                        yield from bps.trigger_and_read(dets + [energy, waxs, xbpm2, xbpm3, ] + [s])

                yield from bps.mv(piezo.th, ai0)

        (yield from inner())




def Cl_edge_measurments_2025_1(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    # # bottom left first
    # names = [  'PBTTTC14_as', 'PBTTTC14_AcN', 'MoS2_new_80', 'MoS2_new_80_ann',
    #          'PBTTTC14_0p02', 'PBTTTC14_0p05', 'PBTTTC14_0p1', 'PBTTTC14_0p2', 'PBTTTC14_0p5' , 'PBTTTC14_1_FeCl3', 'PBTTTC14_0p5_washed', 'PBTTTC14_1_washed' ]             
    # x_piezo = [     -49000,      -39000,       50000,        55000,
    #                 -47000,      -30000,      -15000,           0,       20000,       35000,       51000,        55000]
    # x_hexa = [          -9,        -0.5,           0,            8,
    #                     -1,           0,           0,           0,           0,           0,           0,           10]
    # y_hexa = [           3,           3,           3,            3,
    #                   -0.5,        -0.5,        -0.5,        -0.5,        -0.5,        -0.5,        -0.5,        -0.5]
    # y_piezo = [          0,           0,           0,            0,
    #                  -5000,       -5000,       -5000,       -5000,       -5000,       -5000,       -5000,       -5000]
    # z_piezo = [       4000,        4000,        4000,         4000,
    #                   4000,        4000,        4000,        4000,        4000,        4000,        4000,        4000]
    

    # # bottom left first
    # names = [    'PBTTTC14_1_washed' ]             
    # x_piezo = [         55000]
    # x_hexa = [               10]
    # y_hexa = [            -0.5]
    # y_piezo = [        -5000]
    # z_piezo = [           4000]
    
    names = ['PBTTTC14_as','PBTTTC14_AcN',     'PVC',     'NaPSS', 
        'PBTTTC14_0p02','PBTTTC14_0p05','PBTTTC14_0p1','PBTTTC14_0p2', 'PBTTTC14_0p5' , 'PBTTTC14_1_FeCl3', 'PBTTTC14_0p5_washed', 'PBTTTC14_1_washed' ]             
    x_piezo = [     -49000,      -39000,      -25000,      -10000,
                    -47000,      -30000,      -15000,           0,       20000,       35000,       51000,        55000]
    x_hexa = [          -9,        -0.5,           0,           0,
                        -1,           0,           0,           0,           0,           0,           0,           10]
    y_hexa = [           3,           3,           3,           3,
                      -0.5,        -0.5,        -0.5,        -0.5,        -0.5,        -0.5,        -0.5,        -0.5]
    y_piezo = [          0,           0,           0,           0,
                     -5000,       -5000,       -5000,       -5000,       -5000,       -5000,       -5000,       -5000]
    z_piezo = [       4000,        4000,        4000,        4000,
                      4000,        4000,        4000,        4000,        4000,        4000,        4000,        4000]



    names = ['PBTTTC14_0p2','PBTTTC14_0p5' ,'PBTTTC14_1_FeCl3','PBTTTC14_0p5_washed', 'PBTTTC14_1_washed' ]             
    x_piezo = [         0,       20000,       35000,       51000,        55000]
    x_hexa = [           0,           0,           0,           0,           10]
    y_hexa = [        -0.5,        -0.5,        -0.5,        -0.5,        -0.5]
    y_piezo = [      -5000,       -5000,       -5000,       -5000,       -5000]
    z_piezo = [       4000,        4000,        4000,        4000,        4000]



    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(z_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexa)})"
    assert len(x_piezo) == len(y_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_hexa)})"


    energies1 = -10 + np.asarray([2810.0, 2820.0, 2828.0, 2829.0, 2830.0, 2831.0, 2832.0, 2833.0, 2834.0, 2834.5, 2835.0, 2835.5, 2836.0, 2836.5, 2837.0, 2837.5, 2838.0, 2838.5, 2839.0,
    2839.5, 2840.0, 2840.5, 2841.0, 2841.5, 2845.0, 2850.0, 2855.0, 2860.0, 2865.0, 2870.0, 2875.0, 2880.0, 2890.0])

    energies2 =   -7 + np.asarray([2810.0, 2820.0, 2830.0, 2832.0, 2834.0, 2834.5, 2835.0, 2835.5, 2836.0, 2836.5, 2837.0, 2837.5, 2838.0, 2838.5, 2839.0,
    2839.5, 2840.0, 2840.5, 2841.0, 2841.5, 2845.0, 2850.0, 2855.0, 2860.0, 2865.0, 2870.0, 2875.0, 2880.0, 2890.0])
    
    waxs_arc = [0, 20]
    ai0_all = -0.5
    ai_list = [1.6]

    for name, xs, ys, zs, xs_hexa, ys_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa, y_hexa):

        energies = energies1
        x_step = 30

        if 'PBTTTC14_0p2' not in name:

            yield from bps.mv(stage.x, xs_hexa,
                            stage.y, ys_hexa,
                            piezo.x, xs,
                            piezo.y, ys,
                            piezo.z, zs)

            yield from bps.mv(piezo.th, ai0_all)
            yield from alignement_gisaxs_doblestack(0.7)
            
            yield from bps.mv(att2_9.open_cmd, 1)
            yield from bps.sleep(1)
            yield from bps.mv(att2_9.open_cmd, 1)
            yield from bps.sleep(1)


        ai0 = piezo.th.position
        det_exposure_time(t, t)

        s = Signal(name='target_file_name', value='')

        @bpp.stage_decorator(dets)
        @bpp.run_decorator(md={'sample_name' :'{target_file_name}'})
        def inner():

            for i, wa in enumerate(waxs_arc):
                yield from bps.mv(waxs, wa)
                # Do not take SAXS when WAXS detector in the way
                # dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]

                yield from bps.mv(piezo.x, xs)
                counter = 0

                for k, ais in enumerate(ai_list):
                    yield from bps.mv(piezo.th, ai0 + ais)

                    name_fmt = "{sample}_pos1_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                    for e in energies:
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(1)
                        if xbpm2.sumX.get() < 50:
                            yield from bps.sleep(2)
                            yield from bps.mv(energy, e)
                            yield from bps.sleep(1)
                        yield from bps.mv(piezo.x, xs - counter * x_step)
                        counter += 1
                        
                        bpm = xbpm2.sumX.get()
                        sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                        print(f"\n\t=== Sample: {sample_name} ===\n")
                        s.put(sample_name)
                        yield from bps.trigger_and_read(dets + [energy, waxs, xbpm2, xbpm3, att2_9] + [s])


                    name_fmt = "{sample}_pos2_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                    for e in energies[::-1]:
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(1)
                        if xbpm2.sumX.get() < 50:
                            yield from bps.sleep(2)
                            yield from bps.mv(energy, e)
                            yield from bps.sleep(1)
                        yield from bps.mv(piezo.x, xs - counter * x_step)
                        counter += 1

                        bpm = xbpm2.sumX.get()
                        sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                        print(f"\n\t=== Sample: {sample_name} ===\n")
                        s.put(sample_name)
                        yield from bps.trigger_and_read(dets + [energy, waxs, xbpm2, xbpm3, att2_9] + [s])

                yield from bps.mv(piezo.th, ai0)

        (yield from inner())





def scan_nexafs_Moedge():
    dets = [pil900KW]
    # energies1 =   np.asarray([2810.0, 2820.0, 2830.0, 2832.0, 2834.0, 2834.5, 2835.0, 2835.5, 2836.0, 2836.5, 2837.0, 2837.5, 2838.0, 2838.5, 2839.0,
    # 2839.5, 2840.0, 2840.5, 2841.0, 2841.5, 2845.0, 2850.0, 2855.0, 2860.0, 2865.0, 2870.0, 2875.0, 2880.0, 2890.0])
    
    name='nexafs_MoS2_EMIM_80_ann'
    energies = np.linspace(2450, 2540, 91)    
    y = piezo.y.position
    waxs_arc = [20]

    s = Signal(name='target_file_name', value='')

    @bpp.stage_decorator(dets)
    @bpp.run_decorator(md={'sample_name' :'{target_file_name}'})
    def inner():
        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)

            for i, e in enumerate(energies):
                yield from bps.mv(energy, e)
                yield from bps.sleep(2)

                if xbpm2.sumX.get() < 50:
                    yield from bps.mv(energy, e)
                
                # Metadata
                #e = energy.position.energy / 1000
                wa = str(np.round(float(wa), 1)).zfill(4)
                # sdd = pil1m_pos.z.position / 1000

                # Sample name
                name_fmt = ("{sample}_{energy}eV_wa{wax}_ai0.8deg")
                sample_name = name_fmt.format(sample = name,energy = "%.2f" % e , wax = wa)
                sample_name = sample_name.translate({ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ =, "})
                print(f"\n\n\n\t=== Sample: {sample_name} ===")
                s.put(sample_name)
                
                yield from bps.trigger_and_read(dets + [energy, waxs, xbpm2, xbpm3] + [s])

            yield from bps.mv(energy, 2500)
            yield from bps.sleep(2)
    (yield from inner())










def Cl_edge_measurments_2025_1_sva(t=1):
    dets = [pil900KW]
    det_exposure_time(t, t)

    # names = ['pgBTTT_S1_outer_0p6mV']
    # x_hexa = [18.0]
    # names = ['pgBTTT_S1_outer_m0p10mV']
    # x_hexa = [15.1]

    names = ['PGBTTT_sample5_OMIMCl_p1200mV']
    x_hexa = [-21.2]

    assert len(x_hexa) == len(names), f"Number of X coordinates ({len(x_hexa)}) is different from number of samples ({len(names)})"

    energies = -7 + np.asarray([2810.0, 2820.0, 2830.0, 2832.0, 2834.0, 2834.5, 2835.0, 2835.5, 2836.0, 2836.5, 2837.0, 2837.5, 2838.0, 2838.5, 2839.0,
    2839.5, 2840.0, 2840.5, 2841.0, 2841.5, 2845.0, 2850.0, 2855.0, 2860.0, 2865.0, 2870.0, 2875.0, 2880.0, 2890.0])
    
    waxs_arc = [0]
    ai_list = [1.60]

    for name, xs_hexa in zip(names, x_hexa):
        yield from bps.mv(stage.x, xs_hexa)

        ai0 = stage.th.position
        det_exposure_time(t, t)

        s = Signal(name='target_file_name', value='')

        @bpp.stage_decorator(dets)
        @bpp.run_decorator(md={'sample_name' :'{target_file_name}'})
        def inner():

            for i, wa in enumerate(waxs_arc):
                yield from bps.mv(waxs, wa)
                counter = 0

                for k, ais in enumerate(ai_list):
                    yield from bps.mv(stage.th, ai0 + ais)

                    name_fmt = "{sample}_pos1_{energy}eV_x{x}_ai{ai}_wa{wax}_bpm{xbpm}"
                    for e in energies:
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                        if xbpm2.sumX.get() < 50:
                            yield from bps.mv(energy, e)
                            yield from bps.sleep(2)
                        yield from bps.mv(stage.x, xs_hexa - counter * 0.030)
                        counter += 1
                        
                        bpm = xbpm2.sumX.get()
                        sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, x="%1.2f"%stage.x.position, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                        s.put(sample_name)
                        print(f"\n\t=== Sample: {sample_name} ===\n")
                        yield from bps.trigger_and_read(dets + [energy, waxs, xbpm2, xbpm3, att2_9] + [s])

                    name_fmt = "{sample}_pos2_{energy}eV_x{x}_ai{ai}_wa{wax}_bpm{xbpm}"
                    for e in energies[::-1]:
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                        if xbpm2.sumX.get() < 50:
                            yield from bps.mv(energy, e)
                            yield from bps.sleep(2)
                        yield from bps.mv(stage.x, xs_hexa - counter * 0.030)
                        counter += 1

                        bpm = xbpm2.sumX.get()
                        sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, x="%1.2f"%stage.x.position, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                        s.put(sample_name)
                        print(f"\n\t=== Sample: {sample_name} ===\n")
                        yield from bps.trigger_and_read(dets + [energy, waxs, xbpm2, xbpm3, att2_9] + [s])

        (yield from inner())
        yield from bps.mv(stage.th, ai0)





def Cl_edge_measurments_2025_1_sva_night(t=1, humidity=0, x_off=0, ais=None, ys=None):
    if ais:
        print('ai existing')
        aiss=ais
        yss = ys

    dets = [pil900KW]
    det_exposure_time(t, t)

    names = ['pgBTTT_KClO4_n300mV', 'pgBTTT_KClO4_n100mV', 'pgBTTT_KClO4_p100mV', 'pgBTTT_KClO4_p300mV', 'pgBTTT_KClO4_p450mV', 'pgBTTT_KClO4_p600mV'] 
    x_hexa = -x_off + np.asarray([-24.5, -14, -3.5, 5.5, 16, 27])

    assert len(x_hexa) == len(names), f"Number of X coordinates ({len(x_hexa)}) is different from number of samples ({len(names)})"

    energies = np.asarray([2810.0, 2820.0, 2830.0, 2832.0, 2834.0, 2834.5, 2835.0, 2835.5, 2836.0, 2836.5, 2837.0, 2837.5, 2838.0, 2838.5, 2839.0,
    2839.5, 2840.0, 2840.5, 2841.0, 2841.5, 2845.0, 2850.0, 2855.0, 2860.0, 2865.0, 2870.0, 2875.0, 2880.0, 2890.0])
    
    waxs_arc = [0]
    ai_list = [1.60]
    aiss=[]
    yss=[]
    ai_ini = 4.3

    det_exposure_time(t, t)

    for l, (name, xs_hexa) in enumerate(zip(names, x_hexa)):
        yield from bps.mv(stage.x, xs_hexa)

        if not ais:
            print('ai not existing')
            yield from bps.mv(stage.th, ai_ini)
            yield from alignement_gisaxs_hex(angle = 0.8)
            ai0 = stage.th.position
            y0 = stage.y.position
            aiss = aiss + [ai0]
            yss = yss + [y0]

        else:
            print('ai existing')
            ai0 = ais[l]
            y0 = ys[l]
            yield from bps.mv(stage.y, y0)

        
        print('ailist', aiss)
        print('ylist', yss)

        s = Signal(name='target_file_name', value='')
        @bpp.stage_decorator(dets)
        @bpp.run_decorator(md={'sample_name' :'{target_file_name}'})
        def inner():

            for i, wa in enumerate(waxs_arc):
                yield from bps.mv(waxs, wa)
                counter = 0

                for k, incidentangle in enumerate(ai_list):
                    yield from bps.mv(stage.th, ai0 + incidentangle)

                    name_fmt = "{sample}_hum{humidity}_pos1_{energy}eV_x{x}_ai{ai}_wa{wax}_bpm{xbpm}"
                    for e in energies:
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                        if xbpm2.sumX.get() < 50:
                            yield from bps.mv(energy, e)
                            yield from bps.sleep(2)
                        yield from bps.mv(stage.x, xs_hexa - counter * 0.030)
                        counter += 1
                        
                        bpm = xbpm2.sumX.get()
                        sample_name = name_fmt.format(sample=name, humidity="%1f"%humidity, energy="%6.2f"%e, x="%1.2f"%stage.x.position, ai="%3.2f"%incidentangle, wax=wa, xbpm="%4.3f"%bpm)
                        s.put(sample_name)
                        print(f"\n\t=== Sample: {sample_name} ===\n")
                        yield from bps.trigger_and_read(dets + [energy, waxs, xbpm2, xbpm3, att2_9] + [s])

                    name_fmt = "{sample}_hum{humidity}_pos2_{energy}eV_x{x}_ai{ai}_wa{wax}_bpm{xbpm}"
                    for e in energies[::-1]:
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                        if xbpm2.sumX.get() < 50:
                            yield from bps.mv(energy, e)
                            yield from bps.sleep(2)
                        yield from bps.mv(stage.x, xs_hexa - counter * 0.030)
                        counter += 1

                        bpm = xbpm2.sumX.get()
                        sample_name = name_fmt.format(sample=name, humidity="%1f"%humidity, energy="%6.2f"%e, x="%1.2f"%stage.x.position, ai="%3.2f"%incidentangle, wax=wa, xbpm="%4.3f"%bpm)
                        s.put(sample_name)
                        print(f"\n\t=== Sample: {sample_name} ===\n")
                        yield from bps.trigger_and_read(dets + [energy, waxs, xbpm2, xbpm3, att2_9] + [s])

        (yield from inner())
        yield from bps.mv(stage.th, ai0)
    return aiss, yss



def Cl_edge_measurments_2025_1_sva_night2(t=1, humidity=0, x_off=0, ais=None, ys=None):
    dets = [pil900KW]
    det_exposure_time(t, t)

    names = ['pgBTTT_KClO4_n100mV', 'pgBTTT_KClO4_p100mV', 'pgBTTT_KClO4_p300mV', 'pgBTTT_KClO4_p450mV', 'pgBTTT_KClO4_p600mV', 'pgBTTT_KClO4_n300mV'] 
    x_hexa = -x_off + np.asarray([-14, -3.5, 5.5, 16, 27, -24.5])

    names = ['pgBTTT_KClO4_n300mV'] 
    x_hexa = -x_off + np.asarray([-24.5])

    assert len(x_hexa) == len(names), f"Number of X coordinates ({len(x_hexa)}) is different from number of samples ({len(names)})"

    energies = np.asarray([2810.0, 2820.0, 2830.0, 2832.0, 2834.0, 2834.5, 2835.0, 2835.5, 2836.0, 2836.5, 2837.0, 2837.5, 2838.0, 2838.5, 2839.0,
    2839.5, 2840.0, 2840.5, 2841.0, 2841.5, 2845.0, 2850.0, 2855.0, 2860.0, 2865.0, 2870.0, 2875.0, 2880.0, 2890.0])
    
    waxs_arc = [0]
    ai_list = [1.60]
    det_exposure_time(t, t)

    for l, (name, xs_hexa) in enumerate(zip(names, x_hexa)):
        yield from bps.mv(stage.x, xs_hexa)

        ai0 = ais[l]
        y0 = ys[l]
        yield from bps.mv(stage.y, y0)

        s = Signal(name='target_file_name', value='')
        @bpp.stage_decorator(dets)
        @bpp.run_decorator(md={'sample_name' :'{target_file_name}'})
        def inner():

            for i, wa in enumerate(waxs_arc):
                yield from bps.mv(waxs, wa)
                counter = 0

                for k, incidentangle in enumerate(ai_list):
                    yield from bps.mv(stage.th, ai0 + incidentangle)

                    name_fmt = "{sample}_hum{humidity}_pos1_{energy}eV_x{x}_ai{ai}_wa{wax}_bpm{xbpm}"
                    for e in energies:
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                        if xbpm2.sumX.get() < 50:
                            yield from bps.mv(energy, e)
                            yield from bps.sleep(2)
                        yield from bps.mv(stage.x, xs_hexa - counter * 0.030)
                        counter += 1
                        
                        bpm = xbpm2.sumX.get()
                        sample_name = name_fmt.format(sample=name, humidity="%1f"%humidity, energy="%6.2f"%e, x="%1.2f"%stage.x.position, ai="%3.2f"%incidentangle, wax=wa, xbpm="%4.3f"%bpm)
                        s.put(sample_name)
                        print(f"\n\t=== Sample: {sample_name} ===\n")
                        yield from bps.trigger_and_read(dets + [energy, waxs, xbpm2, xbpm3, att2_9] + [s])

                    name_fmt = "{sample}_hum{humidity}_pos2_{energy}eV_x{x}_ai{ai}_wa{wax}_bpm{xbpm}"
                    for e in energies[::-1]:
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                        if xbpm2.sumX.get() < 50:
                            yield from bps.mv(energy, e)
                            yield from bps.sleep(2)
                        yield from bps.mv(stage.x, xs_hexa - counter * 0.030)
                        counter += 1

                        bpm = xbpm2.sumX.get()
                        sample_name = name_fmt.format(sample=name, humidity="%1f"%humidity, energy="%6.2f"%e, x="%1.2f"%stage.x.position, ai="%3.2f"%incidentangle, wax=wa, xbpm="%4.3f"%bpm)
                        s.put(sample_name)
                        print(f"\n\t=== Sample: {sample_name} ===\n")
                        yield from bps.trigger_and_read(dets + [energy, waxs, xbpm2, xbpm3, att2_9] + [s])

        (yield from inner())
        # yield from bps.mv(stage.th, ai0)


# ailist [4.022]                                                                                                                                                                                                                                
# ylist [2.869]

def night_02_24_25(t=1):
    #0 per humidity
    #setDryFlow(5)
    #setWetFlow(0)
    #humidity=readHumidity()
    #ai_list, y_list = yield from Cl_edge_measurments_2025_1_sva_night(t=t, humidity=humidity, x_off=0, ais=None, ys=None)
    #print(ai_list, y_list)


    ai_list = [4.022, 3.928, 3.823, 4.024, 4.089, 4.488]                                                                                                                                                                                             
    y_list = [2.869, 2.778, 2.741, 2.699, 2.661, 2.559]
    
    ai_list = [4.022]                                                                                                                                                                                             
    y_list = [2.869]

    # ai_list = [3.928, 3.823, 4.024, 4.089, 4.488]                                                                                                                                                                                             
    # y_list = [2.778, 2.741, 2.699, 2.661, 2.559]

    #75 per humidity
    # setDryFlow(1.2)
    # setWetFlow(2.0)
    # print('Equilibrating 75 per humidity')
    # yield from bps.sleep(3600)

    # humidity=readHumidity()
    # yield from Cl_edge_measurments_2025_1_sva_night2(t=t, humidity=humidity, x_off=1.8, ais=ai_list, ys=y_list)
    # print(ai_list, y_list)


    #100 per humidity
    # setDryFlow(0)
    # setWetFlow(5)
    # print('Equilibrating 100 per humidity')
    # yield from bps.sleep(3600)
    humidity=readHumidity()
    yield from Cl_edge_measurments_2025_1_sva_night2(t=t, humidity=humidity, x_off=3.6, ais=ai_list, ys=y_list)



def night_Feb25_25(t=1):

    proposal_id("2023_3", "317550_Richter_08")
    yield from S_edge_measurments_2025_Feb25_night(t=t)

    yield from transition_S_Cl_edges()

    proposal_id("2023_3", "317550_Richter_09")
    yield from Cl_edge_measurments_2025_Feb25_night(t=t)



def S_edge_measurments_2025_Feb25_night(t=1):
    dets = [pil900KW]
    det_exposure_time(t, t)

    # bottom left first
    names = [           'P3HT_as',                   'P3HT_AcN',                    'P3HT_0p02',                    'P3HT_0p05',                       'P3HT_0p1',                          'P3HT_0p2',            'P3HT_0p5',     'P3HT_0p5_washed', 'PBTTT_C14_FeCl3_1p23_NaTFSI_1p23', 'PBTTT_C14_FeCl3_3p08_NaTFSI_308',
    'P3HT_FeCl3_1p23_NaTFSI_1p23', 'P3HT_FeCl3_3p08_NaTFSI_308','pg2TTT_FeCl3_1p23_NaTFSI_1p23', 'Pg2TTT_FeCl3_3p08_NaTFSI_308', 'P3MEEMT_FeCl3_1p23_NaTFSI_1p23', 'P3MEEMT_C14_FeCl3_3p08_NaTFSI_308', 'PBTTT_magicblue_1mM','PGBTTT_magicblue_1mM',             'PVC']             
    x_piezo = [            -48000,                -46000,                         -32000,                         -18000,                            -4000,                               10000,                 25000,                 39000,             51000,                            52000, 
                           -48000,                       -45000,                         -30000,                         -16000,                            -1000,                               13000,                 28000,                 44000,             52000]
    x_hexa = [                -11,                            0,                              0,                              0,                                0,                                   0,                     0,                     0,                 0,                                0,
                              -12,                            0,                              0,                              0,                                0,                                   0,                     0,                     0,                 5]
    y_hexa = [                  3,                            3,                              3,                              3,                                3,                                   3,                     3,                     3,                 3,                                3,
                             -0.5,                         -0.5,                           -0.5,                           -0.5,                             -0.5,                                -0.5,                  -0.5,                  -0.5,              -0.5]
    y_piezo = [                 0,                            0,                              0,                              0,                                0,                                   0,                     0,                     0,                 0,                                0,
                             -5000,                       -5000,                          -5000,                          -5000,                            -5000,                               -5000,                 -5000,                 -5000,             -5000]
    z_piezo = [               4000,                        4000,                           4000,                           4000,                             4000,                                4000,                  4000,                  4000,               4000,                            4000,
                              4000,                        4000,                           4000,                           4000,                             4000,                                4000,                  4000,                  4000,              4000]


    # bottom left first
    names = ['PVC']             
    x_piezo = [             52000]
    x_hexa = [                 5]
    y_hexa = [               -0.5]
    y_piezo = [               -5000]
    z_piezo = [               4000]




    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(z_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexa)})"
    assert len(x_piezo) == len(y_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_hexa)})"

    energies = [2450.0,2455.0,2460.0,2465.0,2470.0,2472.0,2472.5,2473.0,2473.5,2474.0,2474.5,2475.0,2475.5,2476.0,2476.5,2477.0,2477.5,2478.0,2478.5,2479.0,2479.5,
    2480.0,2480.5,2481.0,2481.5,2482.0,2482.5,2483.0,2483.5,2484.0,2484.5,2485.0,2485.5,2486.0,2486.5,2487.0,2487.5,2488.0,2488.5,2489.0,2490.0,2490.5,2491.0,
    2491.5,2492.0,2493,2495.0,2500.0,2510.0,2515.0]

    waxs_arc = [0]
    ai0_all = -0.5
    ai_list = [1.6]

    for name, xs, ys, zs, xs_hexa, ys_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa, y_hexa):
        x_step = 30
        '''
        yield from bps.mv(stage.x, xs_hexa,
                          stage.y, ys_hexa,
                          piezo.x, xs,
                          piezo.y, ys,
                          piezo.z, zs)

        yield from bps.mv(piezo.th, ai0_all)
        yield from alignement_gisaxs_doblestack(0.7)
        '''
        yield from bps.mv(att2_9.open_cmd, 1)
        yield from bps.sleep(1)
        yield from bps.mv(att2_9.open_cmd, 1)
        yield from bps.sleep(1)

        ai0 = piezo.th.position
        det_exposure_time(t, t)

        s = Signal(name='target_file_name', value='')

        @bpp.stage_decorator(dets)
        @bpp.run_decorator(md={'sample_name' :'{target_file_name}'})
        def inner():

            for i, wa in enumerate(waxs_arc):
                yield from bps.mv(waxs, wa)

                yield from bps.mv(piezo.x, xs)
                counter = 0

                for k, ais in enumerate(ai_list):
                    yield from bps.mv(piezo.th, ai0 + ais)

                    name_fmt = "{sample}_pos1_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                    for e in energies:
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                        if xbpm2.sumX.get() < 50:
                            yield from bps.sleep(2)
                            yield from bps.mv(energy, e)
                            yield from bps.sleep(2)
                        yield from bps.mv(piezo.x, xs - counter * x_step)
                        counter += 1
                        
                        bpm = xbpm2.sumX.get()
                        sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                        print(f"\n\t=== Sample: {sample_name} ===\n")
                        s.put(sample_name)
                        yield from bps.trigger_and_read(dets + [energy, waxs, xbpm2, xbpm3, att2_9] + [s])


                    name_fmt = "{sample}_pos2_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                    for e in energies[::-1]:
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                        if xbpm2.sumX.get() < 50:
                            yield from bps.sleep(2)
                            yield from bps.mv(energy, e)
                            yield from bps.sleep(2)
                        yield from bps.mv(piezo.x, xs - counter * x_step)
                        counter += 1

                        bpm = xbpm2.sumX.get()
                        sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                        print(f"\n\t=== Sample: {sample_name} ===\n")
                        s.put(sample_name)
                        yield from bps.trigger_and_read(dets + [energy, waxs, xbpm2, xbpm3, att2_9] + [s])

                yield from bps.mv(piezo.th, ai0)

        (yield from inner())




def Cl_edge_measurments_2025_Feb25_night(t=1):
    dets = [pil900KW]
    det_exposure_time(t, t)

    # bottom left first
    names = [           'P3HT_as',                   'P3HT_AcN',                    'P3HT_0p02',                    'P3HT_0p05',                       'P3HT_0p1',                          'P3HT_0p2',            'P3HT_0p5',     'P3HT_0p5_washed', 'PBTTT_C14_FeCl3_1p23_NaTFSI_1p23', 'PBTTT_C14_FeCl3_3p08_NaTFSI_308',
    'P3HT_FeCl3_1p23_NaTFSI_1p23', 'P3HT_FeCl3_3p08_NaTFSI_308','pg2TTT_FeCl3_1p23_NaTFSI_1p23', 'Pg2TTT_FeCl3_3p08_NaTFSI_308', 'P3MEEMT_FeCl3_1p23_NaTFSI_1p23', 'P3MEEMT_C14_FeCl3_3p08_NaTFSI_308', 'PBTTT_magicblue_1mM','PGBTTT_magicblue_1mM',             'PVC']             
    x_piezo = -3000 + np.asarray([-48000,                -46000,                         -32000,                         -18000,                            -4000,                               10000,                 25000,                 39000,             51000,                            52000, 
                           -48000,                       -45000,                         -30000,                         -16000,                            -1000,                               13000,                 28000,                 44000,             52000])
    x_hexa = [                -11,                            0,                              0,                              0,                                0,                                   0,                     0,                     0,                 0,                                0,
                              -12,                            0,                              0,                              0,                                0,                                   0,                     0,                     0,                 5]
    y_hexa = [                  3,                            3,                              3,                              3,                                3,                                   3,                     3,                     3,                 3,                                3,
                             -0.5,                         -0.5,                           -0.5,                           -0.5,                             -0.5,                                -0.5,                  -0.5,                  -0.5,              -0.5]
    y_piezo = [                 0,                            0,                              0,                              0,                                0,                                   0,                     0,                     0,                 0,                                0,
                             -5000,                       -5000,                          -5000,                          -5000,                            -5000,                               -5000,                 -5000,                 -5000,             -5000]
    z_piezo = [               4000,                        4000,                           4000,                           4000,                             4000,                                4000,                  4000,                  4000,               4000,                            4000,
                              4000,                        4000,                           4000,                           4000,                             4000,                                4000,                  4000,                  4000,              4000]

    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(z_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexa)})"
    assert len(x_piezo) == len(y_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_hexa)})"

    energies = -10 + np.asarray([2810.0, 2820.0, 2828.0, 2829.0, 2830.0, 2831.0, 2832.0, 2833.0, 2834.0, 2834.5, 2835.0, 2835.5, 2836.0, 2836.5, 2837.0, 2837.5, 2838.0, 2838.5, 2839.0,
    2839.5, 2840.0, 2840.5, 2841.0, 2841.5, 2845.0, 2850.0, 2855.0, 2860.0, 2865.0, 2870.0, 2875.0, 2880.0, 2890.0])
    
    waxs_arc = [0]
    ai0_all = -0.5
    ai_list = [1.6]

    for name, xs, ys, zs, xs_hexa, ys_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa, y_hexa):
        x_step = 30

        yield from bps.mv(stage.x, xs_hexa,
                        stage.y, ys_hexa,
                        piezo.x, xs,
                        piezo.y, ys,
                        piezo.z, zs)

        yield from bps.mv(piezo.th, ai0_all)
        yield from alignement_gisaxs_doblestack(0.7)
        
        yield from bps.mv(att2_9.open_cmd, 1)
        yield from bps.sleep(1)
        yield from bps.mv(att2_9.open_cmd, 1)
        yield from bps.sleep(1)

        ai0 = piezo.th.position
        det_exposure_time(t, t)

        s = Signal(name='target_file_name', value='')

        @bpp.stage_decorator(dets)
        @bpp.run_decorator(md={'sample_name' :'{target_file_name}'})
        def inner():

            for i, wa in enumerate(waxs_arc):
                yield from bps.mv(waxs, wa)
                yield from bps.mv(piezo.x, xs)
                counter = 0

                for k, ais in enumerate(ai_list):
                    yield from bps.mv(piezo.th, ai0 + ais)

                    name_fmt = "{sample}_pos1_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                    for e in energies:
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(1)
                        if xbpm2.sumX.get() < 50:
                            yield from bps.sleep(2)
                            yield from bps.mv(energy, e)
                            yield from bps.sleep(1)
                        yield from bps.mv(piezo.x, xs - counter * x_step)
                        counter += 1
                        
                        bpm = xbpm2.sumX.get()
                        sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                        print(f"\n\t=== Sample: {sample_name} ===\n")
                        s.put(sample_name)
                        yield from bps.trigger_and_read(dets + [energy, waxs, xbpm2, xbpm3, att2_9] + [s])


                    name_fmt = "{sample}_pos2_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                    for e in energies[::-1]:
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(1)
                        if xbpm2.sumX.get() < 50:
                            yield from bps.sleep(2)
                            yield from bps.mv(energy, e)
                            yield from bps.sleep(1)
                        yield from bps.mv(piezo.x, xs - counter * x_step)
                        counter += 1

                        bpm = xbpm2.sumX.get()
                        sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                        print(f"\n\t=== Sample: {sample_name} ===\n")
                        s.put(sample_name)
                        yield from bps.trigger_and_read(dets + [energy, waxs, xbpm2, xbpm3, att2_9] + [s])

                yield from bps.mv(piezo.th, ai0)

        (yield from inner())






def scan_nexafs_Caedge():
    dets = [pil900KW]

    name='nexafs_MoS2_EMIM_80_ann'
    energies = np.linspace(4020, 4070, 51)    
    y = piezo.y.position
    waxs_arc = [20]

    s = Signal(name='target_file_name', value='')

    @bpp.stage_decorator(dets)
    @bpp.run_decorator(md={'sample_name' :'{target_file_name}'})
    def inner():
        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)

            for i, e in enumerate(energies):
                yield from bps.mv(energy, e)
                yield from bps.sleep(2)

                if xbpm2.sumX.get() < 50:
                    yield from bps.mv(energy, e)
                
                # Metadata
                #e = energy.position.energy / 1000
                wa = str(np.round(float(wa), 1)).zfill(4)
                # sdd = pil1m_pos.z.position / 1000

                # Sample name
                name_fmt = ("{sample}_{energy}eV_wa{wax}_ai0.8deg")
                sample_name = name_fmt.format(sample = name,energy = "%.2f" % e , wax = wa)
                sample_name = sample_name.translate({ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ =, "})
                print(f"\n\n\n\t=== Sample: {sample_name} ===")
                s.put(sample_name)
                
                yield from bps.trigger_and_read(dets + [energy, waxs, xbpm2, xbpm3] + [s])

            yield from bps.mv(energy, 4050)
            yield from bps.sleep(2)
    (yield from inner())






def Ca_edge_measurments_2025_1_sva(t=1):
    dets = [pil900KW]
    det_exposure_time(t, t)

    names = ['BBL_CaCl2_0V']
    x_hexa = [9.4]
    #x_hexa = [9.9]


    assert len(x_hexa) == len(names), f"Number of X coordinates ({len(x_hexa)}) is different from number of samples ({len(names)})"

    energies = ([4030, 4040, 4045, 4046, 4047, 4048, 4049, 4050, 4051, 4052, 4053, 4053.5, 4054, 4054.5, 4055, 4055.5, 4056, 4056.5,
    4057, 4057.5, 4058, 4058.5, 4059, 4060, 4061, 4062, 4063, 4064, 4065, 4070, 4080])
    
    waxs_arc = [0]
    ai_list = [1.60]

    for name, xs_hexa in zip(names, x_hexa):
        yield from bps.mv(stage.x, xs_hexa)

        ai0 = stage.th.position
        det_exposure_time(t, t)

        s = Signal(name='target_file_name', value='')

        @bpp.stage_decorator(dets)
        @bpp.run_decorator(md={'sample_name' :'{target_file_name}'})
        def inner():

            for i, wa in enumerate(waxs_arc):
                yield from bps.mv(waxs, wa)
                counter = 0

                for k, ais in enumerate(ai_list):
                    yield from bps.mv(stage.th, ai0 + ais)

                    name_fmt = "{sample}_pos1_{energy}eV_x{x}_ai{ai}_wa{wax}_bpm{xbpm}"
                    for e in energies:
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                        if xbpm2.sumX.get() < 50:
                            yield from bps.mv(energy, e)
                            yield from bps.sleep(2)
                        yield from bps.mv(stage.x, xs_hexa - counter * 0.020)
                        counter += 1
                        
                        bpm = xbpm2.sumX.get()
                        sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, x="%1.2f"%stage.x.position, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                        s.put(sample_name)
                        print(f"\n\t=== Sample: {sample_name} ===\n")
                        yield from bps.trigger_and_read(dets + [energy, waxs, xbpm2, xbpm3, att2_9] + [s])

                    name_fmt = "{sample}_pos2_{energy}eV_x{x}_ai{ai}_wa{wax}_bpm{xbpm}"
                    for e in energies[::-1]:
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                        if xbpm2.sumX.get() < 50:
                            yield from bps.mv(energy, e)
                            yield from bps.sleep(2)
                        yield from bps.mv(stage.x, xs_hexa - counter * 0.030)
                        counter += 1

                        bpm = xbpm2.sumX.get()
                        sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, x="%1.2f"%stage.x.position, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                        s.put(sample_name)
                        print(f"\n\t=== Sample: {sample_name} ===\n")
                        yield from bps.trigger_and_read(dets + [energy, waxs, xbpm2, xbpm3, att2_9] + [s])

        (yield from inner())
        yield from bps.mv(stage.th, ai0)



def K_edge_measurments_2025_Feb26_dinner(t=1):
    dets = [pil900KW]
    det_exposure_time(t, t)

    # bottom left first
    names = [                 'KPSS',             'AcidPEDOT_as',                 'AcidPEDOT_ex',                    'AcidPEDOT_n600mV',         'AcidPEDOT_n300mV',                    'AcidPEDOT_0mV',    'AcidPEDOT_p300mV',     'AcidPEDOT_p600mV']             
    x_piezo = [              -48000,                    -40000,                         -38000,                         -28000,                            -14000,                              -1000,                 13000,                  30000]
    x_hexa = [                -13,                          -13,                              0,                              0,                                0,                                   0,                     0,                     0]
    y_hexa = [                  3,                            3,                              3,                              3,                                3,                                   3,                     3,                     3]
    y_piezo = [                 0,                            0,                              0,                              0,                                0,                                   0,                     0,                     0]
    z_piezo = [               4000,                        4000,                           4000,                           4000,                             4000,                                4000,                  4000,                  4000]

    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(z_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexa)})"
    assert len(x_piezo) == len(y_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_hexa)})"

    energies = np.asarray(np.arange(3580, 3611, 5).tolist() + 
                          np.arange(3612, 3629, 1).tolist() + 
                          np.arange(3630, 3700, 5).tolist())
    
        
    waxs_arc = [0]
    ai0_all = -0.5
    ai_list = [1.6, 3.2]

    for name, xs, ys, zs, xs_hexa, ys_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa, y_hexa):
        x_step = 30

        yield from bps.mv(stage.x, xs_hexa,
                        stage.y, ys_hexa,
                        piezo.x, xs,
                        piezo.y, ys,
                        piezo.z, zs)

        yield from bps.mv(piezo.th, ai0_all)
        yield from alignement_gisaxs(0.7)
        
        yield from bps.mv(att2_9.open_cmd, 1)
        yield from bps.sleep(1)
        yield from bps.mv(att2_9.open_cmd, 1)
        yield from bps.sleep(1)

        ai0 = piezo.th.position
        det_exposure_time(t, t)

        s = Signal(name='target_file_name', value='')

        @bpp.stage_decorator(dets)
        @bpp.run_decorator(md={'sample_name' :'{target_file_name}'})
        def inner():

            for i, wa in enumerate(waxs_arc):
                yield from bps.mv(waxs, wa)
                yield from bps.mv(piezo.x, xs)
                counter = 0

                for k, ais in enumerate(ai_list):
                    yield from bps.mv(piezo.th, ai0 + ais)

                    name_fmt = "{sample}_pos1_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                    for e in energies:
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(1)
                        if xbpm2.sumX.get() < 50:
                            yield from bps.sleep(2)
                            yield from bps.mv(energy, e)
                            yield from bps.sleep(1)
                        yield from bps.mv(piezo.x, xs - counter * x_step)
                        counter += 1
                        
                        bpm = xbpm2.sumX.get()
                        sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                        print(f"\n\t=== Sample: {sample_name} ===\n")
                        s.put(sample_name)
                        yield from bps.trigger_and_read(dets + [energy, waxs, xbpm2, xbpm3, att2_9] + [s])


                    name_fmt = "{sample}_pos2_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                    for e in energies[::-1]:
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(1)
                        if xbpm2.sumX.get() < 50:
                            yield from bps.sleep(2)
                            yield from bps.mv(energy, e)
                            yield from bps.sleep(1)
                        yield from bps.mv(piezo.x, xs - counter * x_step)
                        counter += 1

                        bpm = xbpm2.sumX.get()
                        sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                        print(f"\n\t=== Sample: {sample_name} ===\n")
                        s.put(sample_name)
                        yield from bps.trigger_and_read(dets + [energy, waxs, xbpm2, xbpm3, att2_9] + [s])

                yield from bps.mv(piezo.th, ai0)

        (yield from inner())

def K_edge_measurments_2025_Feb26_night(t=1):
    dets = [pil900KW]
    det_exposure_time(t, t)

    # bottom left first 
    names = [                          'PBDF_n1000mV',                  'PBDF_n800mV',                  'PBDF_n600mV',                    'PBDF_n400mV',                          'PBDF_0mV',         'PBDF_p400mV',         'PBDF_p600mV',                       'PBDF_p800mV',     'PBDF_p1000mV',
                                     'BBL_n800mV',                   'BBL_n500mV',                      'BBL_0mV',          'MoS2_BBL_print_n800mV',              'MoS2_80_newIL_n800mV',  'MoS2_80_ann_n800mV',      'MoS2_80_n800mV',             'MoS2_BBL_spray_n800mV', 'BBL_spray_n800mV',   'KPSS', 'BBL_n1200mV']             
    x_piezo = [                                   -48000,                         -36000,                         -22000,                            -8000,                               8000,                 23000,                 38000,                               47000,              56000, 
                                                  -48000,                         -37000,                         -23000,                            -9000,                               3000,                 15000,                 28000,                               40000,              52000,    56000, -50000]
    x_hexa = [                                           0,                              0,                              0,                                0,                                   0,                     0,                     0,                                   5,                  5,
                                                          0,                              0,                              0,                                0,                                   0,                     0,                     0,                                   5,                  5,        5, -10]      
    y_hexa = [                                             3,                              3,                              3,                                3,                                   3,                     3,                     3,                                   3,                  3,
                                                      -0.5,                           -0.5,                           -0.5,                             -0.5,                                -0.5,                  -0.5,                  -0.5,                                -0.5,                  3,        3, -.5]
    y_piezo = [                                          0,                              0,                              0,                                0,                                   0,                     0,                     0,                                   0,                  0,
                                                    -5000,                          -5000,                          -5000,                            -5000,                               -5000,                 -5000,                 -5000,                               -5000,              -5000,    -5000, -5000]
    z_piezo = [                                     4000,                           4000,                           4000,                             4000,                                4000,                  4000,                  4000,                                4000,               4000,
                                                     4000,                           4000,                           4000,                             4000,                                4000,                  4000,                  4000,                                4000,               4000,     4000, 4000]

    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(z_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexa)})"
    assert len(x_piezo) == len(y_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_hexa)})"

    energies = np.asarray(np.arange(3580, 3611, 5).tolist() + 
                          np.arange(3612, 3629, 1).tolist() + 
                          np.arange(3630, 3700, 5).tolist())
    
        
    waxs_arc = [0]
    ai0_all = -0.5
    ai_list = [1.6, 3.2]

    for name, xs, ys, zs, xs_hexa, ys_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa, y_hexa):
        x_step = 30

        yield from bps.mv(stage.x, xs_hexa,
                        stage.y, ys_hexa,
                        piezo.x, xs,
                        piezo.y, ys,
                        piezo.z, zs)

        yield from bps.mv(piezo.th, ai0_all)
        yield from alignement_gisaxs_doblestack(0.7)
        
        yield from bps.mv(att2_9.open_cmd, 1)
        yield from bps.sleep(1)
        yield from bps.mv(att2_9.open_cmd, 1)
        yield from bps.sleep(1)

        ai0 = piezo.th.position
        det_exposure_time(t, t)

        s = Signal(name='target_file_name', value='')

        @bpp.stage_decorator(dets)
        @bpp.run_decorator(md={'sample_name' :'{target_file_name}'})
        def inner():

            for i, wa in enumerate(waxs_arc):
                yield from bps.mv(waxs, wa)
                yield from bps.mv(piezo.x, xs)
                counter = 0

                for k, ais in enumerate(ai_list):
                    yield from bps.mv(piezo.th, ai0 + ais)

                    name_fmt = "{sample}_pos1_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                    for e in energies:
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(1)
                        if xbpm2.sumX.get() < 50:
                            yield from bps.sleep(2)
                            yield from bps.mv(energy, e)
                            yield from bps.sleep(1)
                        yield from bps.mv(piezo.x, xs - counter * x_step)
                        counter += 1
                        
                        bpm = xbpm2.sumX.get()
                        sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                        print(f"\n\t=== Sample: {sample_name} ===\n")
                        s.put(sample_name)
                        yield from bps.trigger_and_read(dets + [energy, waxs, xbpm2, xbpm3, att2_9] + [s])


                    name_fmt = "{sample}_pos2_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                    for e in energies[::-1]:
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(1)
                        if xbpm2.sumX.get() < 50:
                            yield from bps.sleep(2)
                            yield from bps.mv(energy, e)
                            yield from bps.sleep(1)
                        yield from bps.mv(piezo.x, xs - counter * x_step)
                        counter += 1

                        bpm = xbpm2.sumX.get()
                        sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                        print(f"\n\t=== Sample: {sample_name} ===\n")
                        s.put(sample_name)
                        yield from bps.trigger_and_read(dets + [energy, waxs, xbpm2, xbpm3, att2_9] + [s])

                yield from bps.mv(piezo.th, ai0)

        (yield from inner())

def K_edge_measurments_2025_1_sva(t=1):
    dets = [pil900KW]
    det_exposure_time(t, t)

    names = ['BBL_KCl_n500']
    x_hexa = [9.4]
    #x_hexa = [9.9]


    assert len(x_hexa) == len(names), f"Number of X coordinates ({len(x_hexa)}) is different from number of samples ({len(names)})"

    energies = np.asarray(np.arange(3580, 3611, 5).tolist() + 
                          np.arange(3612, 3629, 1).tolist() + 
                          np.arange(3630, 3700, 5).tolist())
    
    waxs_arc = [0]
    ai_list = [1.60]

    for name, xs_hexa in zip(names, x_hexa):
        yield from bps.mv(stage.x, xs_hexa)

        ai0 = stage.th.position
        det_exposure_time(t, t)

        s = Signal(name='target_file_name', value='')

        @bpp.stage_decorator(dets)
        @bpp.run_decorator(md={'sample_name' :'{target_file_name}'})
        def inner():

            for i, wa in enumerate(waxs_arc):
                yield from bps.mv(waxs, wa)
                counter = 0

                for k, ais in enumerate(ai_list):
                    yield from bps.mv(stage.th, ai0 + ais)

                    name_fmt = "{sample}_pos1_{energy}eV_x{x}_ai{ai}_wa{wax}_bpm{xbpm}"
                    for e in energies:
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                        if xbpm2.sumX.get() < 50:
                            yield from bps.mv(energy, e)
                            yield from bps.sleep(2)
                        yield from bps.mv(stage.x, xs_hexa - counter * 0.020)
                        counter += 1
                        
                        bpm = xbpm2.sumX.get()
                        sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, x="%1.2f"%stage.x.position, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                        s.put(sample_name)
                        print(f"\n\t=== Sample: {sample_name} ===\n")
                        yield from bps.trigger_and_read(dets + [energy, waxs, xbpm2, xbpm3, att2_9] + [s])

                    name_fmt = "{sample}_pos2_{energy}eV_x{x}_ai{ai}_wa{wax}_bpm{xbpm}"
                    for e in energies[::-1]:
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                        if xbpm2.sumX.get() < 50:
                            yield from bps.mv(energy, e)
                            yield from bps.sleep(2)
                        yield from bps.mv(stage.x, xs_hexa - counter * 0.030)
                        counter += 1

                        bpm = xbpm2.sumX.get()
                        sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, x="%1.2f"%stage.x.position, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                        s.put(sample_name)
                        print(f"\n\t=== Sample: {sample_name} ===\n")
                        yield from bps.trigger_and_read(dets + [energy, waxs, xbpm2, xbpm3, att2_9] + [s])

        (yield from inner())
        yield from bps.mv(stage.th, ai0)


def K_edge_measurments_2025_Feb27_day(t=1):
    dets = [pil900KW, amptek]
    det_exposure_time(t, t)

    # bottom left first 
    names = ['MoS2_80_ann_n800mV',      'MoS2_80_n800mV',             'MoS2_BBL_spray_n800mV', 'BBL_spray_n800mV'  ]             
    x_piezo = [-5000,                 8000,                               21000,              31000]
    x_hexa = [     0,                     0,                                   0,                  0]      
    y_hexa = [     3,                  3,                                        3,                  3]
    y_piezo = [   40,                 40,                                       40,              40]
    z_piezo = [ 4000,                  4000,                              4000,               4000]

    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(z_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexa)})"
    assert len(x_piezo) == len(y_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_hexa)})"

    energies = np.asarray(np.arange(3580, 3611, 5).tolist() + 
                          np.arange(3612, 3629, 1).tolist() + 
                          np.arange(3630, 3700, 5).tolist())
    
        
    waxs_arc = [0]
    ai0_all = 1.5
    ai_list = [1.6]

    for name, xs, ys, zs, xs_hexa, ys_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa, y_hexa):
        x_step = 30

        yield from bps.mv(stage.x, xs_hexa,
                        stage.y, ys_hexa,
                        piezo.x, xs,
                        piezo.y, ys,
                        piezo.z, zs)

        yield from bps.mv(piezo.th, ai0_all)
        yield from alignement_gisaxs(0.7)
        
        yield from bps.mv(att2_9.open_cmd, 1)
        yield from bps.sleep(1)
        yield from bps.mv(att2_9.open_cmd, 1)
        yield from bps.sleep(1)

        ai0 = piezo.th.position
        det_exposure_time(t, t)

        s = Signal(name='target_file_name', value='')

        @bpp.stage_decorator(dets)
        @bpp.run_decorator(md={'sample_name' :'{target_file_name}'})
        def inner():

            for i, wa in enumerate(waxs_arc):
                yield from bps.mv(waxs, wa)
                yield from bps.mv(piezo.x, xs)
                counter = 0

                for k, ais in enumerate(ai_list):
                    yield from bps.mv(piezo.th, ai0 + ais)

                    name_fmt = "{sample}_pos1_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                    for e in energies:
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(1)
                        if xbpm2.sumX.get() < 50:
                            yield from bps.sleep(2)
                            yield from bps.mv(energy, e)
                            yield from bps.sleep(1)
                        yield from bps.mv(piezo.x, xs - counter * x_step)
                        counter += 1
                        
                        bpm = xbpm2.sumX.get()
                        sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                        print(f"\n\t=== Sample: {sample_name} ===\n")
                        s.put(sample_name)
                        yield from bps.trigger_and_read(dets + [energy, waxs, xbpm2, xbpm3, att2_9] + [s])


                    name_fmt = "{sample}_pos2_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                    for e in energies[::-1]:
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(1)
                        if xbpm2.sumX.get() < 50:
                            yield from bps.sleep(2)
                            yield from bps.mv(energy, e)
                            yield from bps.sleep(1)
                        yield from bps.mv(piezo.x, xs - counter * x_step)
                        counter += 1

                        bpm = xbpm2.sumX.get()
                        sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                        print(f"\n\t=== Sample: {sample_name} ===\n")
                        s.put(sample_name)
                        yield from bps.trigger_and_read(dets + [energy, waxs, xbpm2, xbpm3, att2_9] + [s])

                yield from bps.mv(piezo.th, ai0)

        (yield from inner())



def Cl_edge_measurments_2025_Feb27_day(t=1):
    dets = [pil900KW]
    det_exposure_time(t, t)

    # bottom left first
    names = [      'PBTTT_C14_FeCl3_3p08_NaTFSI_308',  'PBTTT_C14_FeCl3_1p23_NaTFSI_1p23',            'P3HT_1',         'P3HT_0p5',    'P3HT_0p2', 'P3HT_0p05', 'P3HT_0p1' , 'P3HT_0p02', 'P3HT_AcN', 'P3HT_as' ]             
    x_piezo = [                               -48000,                              -36000,              -20000,              -7000,         -3000,       10000,       23000,      38000,       54000,      57000]
    x_hexa = [                                   -12,                                 -12,                 -12,                -12,             0,           0,           0,          0,           0,          6]      
    y_hexa = [                                     3,                                   3,                   3,                  3,             3,           3,           3,          3,           3,          3]
    y_piezo = [                                    0,                                   0,                   0,                  0,             0,           0,           0,          0,           0,          0]
    z_piezo = [                                 4000,                                4000,                4000,               4000,          4000,        4000,        4000,       4000,        4000,       4000]


    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(z_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexa)})"
    assert len(x_piezo) == len(y_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_hexa)})"

    energies = -10 + np.asarray([2810.0, 2820.0, 2828.0, 2829.0, 2830.0, 2831.0, 2832.0, 2833.0, 2834.0, 2834.5, 2835.0, 2835.5, 2836.0, 2836.5, 2837.0, 2837.5, 2838.0, 2838.5, 2839.0,
    2839.5, 2840.0, 2840.5, 2841.0, 2841.5, 2845.0, 2850.0, 2855.0, 2860.0, 2865.0, 2870.0, 2875.0, 2880.0, 2890.0])
    
    waxs_arc = [0]
    ai0_all = 1.0
    ai_list = [1.6, 3.2]

    for name, xs, ys, zs, xs_hexa, ys_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa, y_hexa):
        x_step = 30

        yield from bps.mv(stage.x, xs_hexa,
                        stage.y, ys_hexa,
                        piezo.x, xs,
                        piezo.y, ys,
                        piezo.z, zs)

        yield from bps.mv(piezo.th, ai0_all)
        yield from alignement_gisaxs(0.7)
        
        yield from bps.mv(att2_9.open_cmd, 1)
        yield from bps.sleep(1)
        yield from bps.mv(att2_9.open_cmd, 1)
        yield from bps.sleep(1)

        ai0 = piezo.th.position
        det_exposure_time(t, t)

        s = Signal(name='target_file_name', value='')

        @bpp.stage_decorator(dets)
        @bpp.run_decorator(md={'sample_name' :'{target_file_name}'})
        def inner():

            for i, wa in enumerate(waxs_arc):
                yield from bps.mv(waxs, wa)
                yield from bps.mv(piezo.x, xs)
                counter = 0

                for k, ais in enumerate(ai_list):
                    yield from bps.mv(piezo.th, ai0 + ais)

                    name_fmt = "{sample}_pos1_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                    for e in energies:
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(1)
                        if xbpm2.sumX.get() < 50:
                            yield from bps.sleep(2)
                            yield from bps.mv(energy, e)
                            yield from bps.sleep(1)
                        yield from bps.mv(piezo.x, xs - counter * x_step)
                        counter += 1
                        
                        bpm = xbpm2.sumX.get()
                        sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                        print(f"\n\t=== Sample: {sample_name} ===\n")
                        s.put(sample_name)
                        yield from bps.trigger_and_read(dets + [energy, waxs, xbpm2, xbpm3, att2_9] + [s])


                    name_fmt = "{sample}_pos2_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                    for e in energies[::-1]:
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(1)
                        if xbpm2.sumX.get() < 50:
                            yield from bps.sleep(2)
                            yield from bps.mv(energy, e)
                            yield from bps.sleep(1)
                        yield from bps.mv(piezo.x, xs - counter * x_step)
                        counter += 1

                        bpm = xbpm2.sumX.get()
                        sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                        print(f"\n\t=== Sample: {sample_name} ===\n")
                        s.put(sample_name)
                        yield from bps.trigger_and_read(dets + [energy, waxs, xbpm2, xbpm3, att2_9] + [s])

                yield from bps.mv(piezo.th, ai0)

        (yield from inner())

def S_edge_measurments_2025_Feb27_night_hex_align(t=1):
    dets = [pil900KW]
    det_exposure_time(t, t)

    # bottom left first
    names = [      'W1',       'W2',     'W3',      'W4',     'W5',    'W6',   'P3HT',  'P3HT_F4TCNQ',   'P3HT_EMIMTFSI',        'P3HT_doubledoped',          'AcDOT_C10_155C',   'AcDOT_co_155C',          'Pg2TTT_FeCl3_3p08_NaTFSI_308']     
    x_piezo = [  -48000,     -52000,   -41000,    -32000,   -22000,  -12000,    -3000,          12000,             25000,                     34000,                     48000,             57000,                                   57000]  
    x_hexa = [      -13,          0,        0,         0,        0,       0,        0,              0,                 0,                         0,                         0,                 0,                                      11]
    y_hexa = [        3,          3,        3,         3,        3,       3,        3,              3,                 3,                         3,                         3,                 3,                                       3]
    y_piezo = [       0,          0,        0,         0,        0,       0,        0,              0,                 0,                         0,                         0,                 0,                                       0]
    z_piezo = [    4000,       4000,     4000,      4000,     4000,    4000,     4000,           4000,               4000,                     4000,                      4000,               4000,                                   4000]


    names = [        'Pg2TTT_FeCl3_3p08_NaTFSI_308']     
    x_piezo = [  55000]  
    x_hexa = [      13]
    y_hexa = [         3]
    y_piezo = [      0]
    z_piezo = [  4000]


    # bottom left first
    #names = ['PVC']             
    #x_piezo = [             52000]
    #x_hexa = [                 5]
    #y_hexa = [               -0.5]
    #y_piezo = [               -5000]
    #z_piezo = [               4000]




    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(z_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexa)})"
    assert len(x_piezo) == len(y_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_hexa)})"

    energies = [2450.0,2455.0,2460.0,2465.0,2470.0,2472.0,2472.5,2473.0,2473.5,2474.0,2474.5,2475.0,2475.5,2476.0,2476.5,2477.0,2477.5,2478.0,2478.5,2479.0,2479.5,
    2480.0,2480.5,2481.0,2481.5,2482.0,2482.5,2483.0,2483.5,2484.0,2484.5,2485.0,2485.5,2486.0,2486.5,2487.0,2487.5,2488.0,2488.5,2489.0,2490.0,2490.5,2491.0,
    2491.5,2492.0,2493,2495.0,2500.0,2510.0,2515.0]

    waxs_arc = [0]
    ai0_all = 1
    ai_list = [1.6]

    for name, xs, ys, zs, xs_hexa, ys_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa, y_hexa):
        x_step = 30
        
        yield from bps.mv(stage.x, xs_hexa,
                          stage.y, ys_hexa,
                          piezo.x, xs,
                          piezo.y, ys,
                          piezo.z, zs)

        yield from bps.mv(stage.th, ai0_all)
        #yield from alignement_gisaxs_hex(0.7)
        yield from alignement_gisaxs_doblestack(0.7)

        yield from bps.mv(att2_9.open_cmd, 1)
        yield from bps.sleep(1)
        yield from bps.mv(att2_9.open_cmd, 1)
        yield from bps.sleep(1)

        #ai0 = stage.th.position
        ai0 = piezo.th.position
        det_exposure_time(t, t)

        s = Signal(name='target_file_name', value='')

        @bpp.stage_decorator(dets)
        @bpp.run_decorator(md={'sample_name' :'{target_file_name}'})
        def inner():

            for i, wa in enumerate(waxs_arc):
                yield from bps.mv(waxs, wa)

                yield from bps.mv(piezo.x, xs)
                counter = 0

                for k, ais in enumerate(ai_list):
                    #yield from bps.mv(stage.th, ai0 + ais)
                    yield from bps.mv(piezo.th, ai0 + ais)


                    name_fmt = "{sample}_pos1_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                    for e in energies:
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                        if xbpm2.sumX.get() < 50:
                            yield from bps.sleep(2)
                            yield from bps.mv(energy, e)
                            yield from bps.sleep(2)
                        yield from bps.mv(piezo.x, xs - counter * x_step)
                        counter += 1
                        
                        bpm = xbpm2.sumX.get()
                        sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                        print(f"\n\t=== Sample: {sample_name} ===\n")
                        s.put(sample_name)
                        yield from bps.trigger_and_read(dets + [energy, waxs, xbpm2, xbpm3, att2_9] + [s])


                    name_fmt = "{sample}_pos2_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                    for e in energies[::-1]:
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                        if xbpm2.sumX.get() < 50:
                            yield from bps.sleep(2)
                            yield from bps.mv(energy, e)
                            yield from bps.sleep(2)
                        yield from bps.mv(piezo.x, xs - counter * x_step)
                        counter += 1

                        bpm = xbpm2.sumX.get()
                        sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                        print(f"\n\t=== Sample: {sample_name} ===\n")
                        s.put(sample_name)
                        yield from bps.trigger_and_read(dets + [energy, waxs, xbpm2, xbpm3, att2_9] + [s])

                #yield from bps.mv(stage.th, ai0)
                yield from bps.mv(piezo.th, ai0)

        (yield from inner())

def Cl_edge_measurments_2025_Feb27_evening_hex_align(t=1):
    dets = [pil900KW]
    det_exposure_time(t, t)

    # bottom left first
    names = [  'P3HT_FeCl3_1p23_NaTFSI_1p23', 'P3HT_FeCl3_3p08_NaTFSI_308','pg2TTT_FeCl3_1p23_NaTFSI_1p23', 'Pg2TTT_FeCl3_3p08_NaTFSI_308', 'P3MEEMT_FeCl3_1p23_NaTFSI_1p23', 'P3MEEMT_C14_FeCl3_3p08_NaTFSI_308',                 'PVC', 'PBTTT_magicblue_0p1M_60s', 'pgTTT_magicblue_0p1M_60s',              'NaPSS']     
    x_piezo = [                       -48000,                      -43000,                          -29000,                         -15000,                            -1000,                               12000,                 25000,                      38000,                      53000,                56000]
    x_hexa = [                           -11,                           0,                               0,                              0,                                0,                                   0,                     0,                          0,                          0,                   11]
    y_hexa = [                             3,                           3,                               3,                              3,                                3,                                   3,                     3,                          3,                          3,                    3]
    y_piezo = [                            0,                           0,                               0,                              0,                                0,                                   0,                     0,                          0,                          0,                    0]
    z_piezo = [                         4000,                        4000,                            4000,                           4000,                             4000,                                4000,                  4000,                       4000,                       4000,                 4000]

    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(z_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexa)})"
    assert len(x_piezo) == len(y_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_hexa)})"

    energies = -10 + np.asarray([2810.0, 2820.0, 2828.0, 2829.0, 2830.0, 2831.0, 2832.0, 2833.0, 2834.0, 2834.5, 2835.0, 2835.5, 2836.0, 2836.5, 2837.0, 2837.5, 2838.0, 2838.5, 2839.0,
    2839.5, 2840.0, 2840.5, 2841.0, 2841.5, 2845.0, 2850.0, 2855.0, 2860.0, 2865.0, 2870.0, 2875.0, 2880.0, 2890.0])
    
    waxs_arc = [0]
    ai0_all = 1
    ai_list = [1.6]

    for name, xs, ys, zs, xs_hexa, ys_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa, y_hexa):
        x_step = 30

        yield from bps.mv(stage.x, xs_hexa,
                        stage.y, ys_hexa,
                        piezo.x, xs,
                        piezo.y, ys,
                        piezo.z, zs)

        yield from bps.mv(stage.th, ai0_all)
        yield from alignement_gisaxs_hex(0.7)
        
        yield from bps.mv(att2_9.open_cmd, 1)
        yield from bps.sleep(1)
        yield from bps.mv(att2_9.open_cmd, 1)
        yield from bps.sleep(1)

        ai0 = stage.th.position
        det_exposure_time(t, t)

        s = Signal(name='target_file_name', value='')

        @bpp.stage_decorator(dets)
        @bpp.run_decorator(md={'sample_name' :'{target_file_name}'})
        def inner():

            for i, wa in enumerate(waxs_arc):
                yield from bps.mv(waxs, wa)
                yield from bps.mv(piezo.x, xs)
                counter = 0

                for k, ais in enumerate(ai_list):
                    yield from bps.mv(stage.th, ai0 + ais)

                    name_fmt = "{sample}_pos1_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                    for e in energies:
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(1)
                        if xbpm2.sumX.get() < 50:
                            yield from bps.sleep(2)
                            yield from bps.mv(energy, e)
                            yield from bps.sleep(1)
                        yield from bps.mv(piezo.x, xs - counter * x_step)
                        counter += 1
                        
                        bpm = xbpm2.sumX.get()
                        sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                        print(f"\n\t=== Sample: {sample_name} ===\n")
                        s.put(sample_name)
                        yield from bps.trigger_and_read(dets + [energy, waxs, xbpm2, xbpm3, att2_9] + [s])


                    name_fmt = "{sample}_pos2_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                    for e in energies[::-1]:
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(1)
                        if xbpm2.sumX.get() < 50:
                            yield from bps.sleep(2)
                            yield from bps.mv(energy, e)
                            yield from bps.sleep(1)
                        yield from bps.mv(piezo.x, xs - counter * x_step)
                        counter += 1

                        bpm = xbpm2.sumX.get()
                        sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                        print(f"\n\t=== Sample: {sample_name} ===\n")
                        s.put(sample_name)
                        yield from bps.trigger_and_read(dets + [energy, waxs, xbpm2, xbpm3, att2_9] + [s])

                yield from bps.mv(stage.th, ai0)

        (yield from inner())


def S_edge_measurments_2025_Feb25_evening_hex_align(t=1):
    dets = [pil900KW]
    det_exposure_time(t, t)

    # bottom left first
    names = [  'P3HT_FeCl3_1p23_NaTFSI_1p23', 'P3HT_FeCl3_3p08_NaTFSI_308','pg2TTT_FeCl3_1p23_NaTFSI_1p23', 'Pg2TTT_FeCl3_3p08_NaTFSI_308', 'P3MEEMT_FeCl3_1p23_NaTFSI_1p23', 'P3MEEMT_C14_FeCl3_3p08_NaTFSI_308',                 'PVC', 'PBTTT_magicblue_0p1M_60s', 'pgTTT_magicblue_0p1M_60s',              'NaPSS']     
    x_piezo = [                       -50000,                      -45000,                          -31000,                         -17000,                            -3000,                               10000,                 23000,                      36000,                      51000,                54000]
    x_hexa = [                           -11,                           0,                               0,                              0,                                0,                                   0,                     0,                          0,                          0,                   11]
    y_hexa = [                             3,                           3,                               3,                              3,                                3,                                   3,                     3,                          3,                          3,                    3]
    y_piezo = [                            0,                           0,                               0,                              0,                                0,                                   0,                     0,                          0,                          0,                    0]
    z_piezo = [                         4000,                        4000,                            4000,                           4000,                             4000,                                4000,                  4000,                       4000,                       4000,                 4000]

    # bottom left first
    #names = ['PVC']             
    #x_piezo = [             52000]
    #x_hexa = [                 5]
    #y_hexa = [               -0.5]
    #y_piezo = [               -5000]
    #z_piezo = [               4000]




    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(z_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexa)})"
    assert len(x_piezo) == len(y_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_hexa)})"

    energies = [2450.0,2455.0,2460.0,2465.0,2470.0,2472.0,2472.5,2473.0,2473.5,2474.0,2474.5,2475.0,2475.5,2476.0,2476.5,2477.0,2477.5,2478.0,2478.5,2479.0,2479.5,
    2480.0,2480.5,2481.0,2481.5,2482.0,2482.5,2483.0,2483.5,2484.0,2484.5,2485.0,2485.5,2486.0,2486.5,2487.0,2487.5,2488.0,2488.5,2489.0,2490.0,2490.5,2491.0,
    2491.5,2492.0,2493,2495.0,2500.0,2510.0,2515.0]

    waxs_arc = [0]
    ai0_all = 1
    ai_list = [1.6]

    for name, xs, ys, zs, xs_hexa, ys_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa, y_hexa):
        x_step = 30
        
        yield from bps.mv(stage.x, xs_hexa,
                          stage.y, ys_hexa,
                          piezo.x, xs,
                          piezo.y, ys,
                          piezo.z, zs)

        yield from bps.mv(stage.th, ai0_all)
        yield from alignement_gisaxs_hex(0.7)
        
        yield from bps.mv(att2_9.open_cmd, 1)
        yield from bps.sleep(1)
        yield from bps.mv(att2_9.open_cmd, 1)
        yield from bps.sleep(1)

        ai0 = stage.th.position
        det_exposure_time(t, t)

        s = Signal(name='target_file_name', value='')

        @bpp.stage_decorator(dets)
        @bpp.run_decorator(md={'sample_name' :'{target_file_name}'})
        def inner():

            for i, wa in enumerate(waxs_arc):
                yield from bps.mv(waxs, wa)

                yield from bps.mv(piezo.x, xs)
                counter = 0

                for k, ais in enumerate(ai_list):
                    yield from bps.mv(stage.th, ai0 + ais)

                    name_fmt = "{sample}_pos1_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                    for e in energies:
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                        if xbpm2.sumX.get() < 50:
                            yield from bps.sleep(2)
                            yield from bps.mv(energy, e)
                            yield from bps.sleep(2)
                        yield from bps.mv(piezo.x, xs - counter * x_step)
                        counter += 1
                        
                        bpm = xbpm2.sumX.get()
                        sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                        print(f"\n\t=== Sample: {sample_name} ===\n")
                        s.put(sample_name)
                        yield from bps.trigger_and_read(dets + [energy, waxs, xbpm2, xbpm3, att2_9] + [s])


                    name_fmt = "{sample}_pos2_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                    for e in energies[::-1]:
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                        if xbpm2.sumX.get() < 50:
                            yield from bps.sleep(2)
                            yield from bps.mv(energy, e)
                            yield from bps.sleep(2)
                        yield from bps.mv(piezo.x, xs - counter * x_step)
                        counter += 1

                        bpm = xbpm2.sumX.get()
                        sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                        print(f"\n\t=== Sample: {sample_name} ===\n")
                        s.put(sample_name)
                        yield from bps.trigger_and_read(dets + [energy, waxs, xbpm2, xbpm3, att2_9] + [s])

                yield from bps.mv(stage.th, ai0)

        (yield from inner())

def night_2025_Feb27_25(t=1):

    proposal_id("2023_3", "317550_Richter_12")
    yield from S_edge_measurments_2025_Feb25_night(t=t)

    yield from transition_S_Cl_edges()

    proposal_id("2023_3", "317550_Richter_13")
    yield from Cl_edge_measurments_2025_Feb27_night(t=t)



def Cl_edge_measurments_2025_Feb27_day_align_hex(t=1):
    dets = [pil900KW]
    det_exposure_time(t, t)

    # bottom left first
    #names = [      'PBTTT_C14_FeCl3_3p08_NaTFSI_308_redo',  'PBTTT_C14_FeCl3_1p23_NaTFSI_1p23',            'P3HT_1',         'P3HT_0p5',    'P3HT_0p2', 'P3HT_0p05', 'P3HT_0p1' , 'P3HT_0p02', 'P3HT_AcN', 'P3HT_as' ]             
    #x_piezo = [                               -48000,                              -36000,              -20000,              -7000,         -3000,       10000,       23000,      38000,       54000,      57000]
    #x_hexa = [                                   -12,                                 -12,                 -12,                -12,             0,           0,           0,          0,           0,          6]      
    #y_hexa = [                                     3,                                   3,                   3,                  3,             3,           3,           3,          3,           3,          3]
    #y_piezo = [                                    0,                                   0,                   0,                  0,             0,           0,           0,          0,           0,          0]
    #z_piezo = [                                 4000,                                4000,                4000,               4000,          4000,        4000,        4000,       4000,        4000,       4000]
    
    #restart list after crash
    names = ['P3HT_AcN', 'P3HT_as' ]             
    x_piezo = [   54000,      57000]
    x_hexa = [        0,          6]      
    y_hexa = [        3,          3]
    y_piezo = [       0,          0]
    z_piezo = [    4000,       4000]


    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(z_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexa)})"
    assert len(x_piezo) == len(y_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_hexa)})"

    energies = -10 + np.asarray([2810.0, 2820.0, 2828.0, 2829.0, 2830.0, 2831.0, 2832.0, 2833.0, 2834.0, 2834.5, 2835.0, 2835.5, 2836.0, 2836.5, 2837.0, 2837.5, 2838.0, 2838.5, 2839.0,
    2839.5, 2840.0, 2840.5, 2841.0, 2841.5, 2845.0, 2850.0, 2855.0, 2860.0, 2865.0, 2870.0, 2875.0, 2880.0, 2890.0])
    
    waxs_arc = [0]
    ai0_all = 3
    ai_list = [1.6, 3.2]

    for name, xs, ys, zs, xs_hexa, ys_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa, y_hexa):
        x_step = 30

        yield from bps.mv(stage.x, xs_hexa,
                        stage.y, ys_hexa,
                        piezo.x, xs,
                        piezo.y, ys,
                        piezo.z, zs)

        yield from bps.mv(stage.th, ai0_all)
        yield from alignement_gisaxs_hex(0.7)
        
        yield from bps.mv(att2_9.open_cmd, 1)
        yield from bps.sleep(1)
        yield from bps.mv(att2_9.open_cmd, 1)
        yield from bps.sleep(1)

        ai0 = stage.th.position
        det_exposure_time(t, t)

        s = Signal(name='target_file_name', value='')

        @bpp.stage_decorator(dets)
        @bpp.run_decorator(md={'sample_name' :'{target_file_name}'})
        def inner():

            for i, wa in enumerate(waxs_arc):
                yield from bps.mv(waxs, wa)
                yield from bps.mv(piezo.x, xs)
                counter = 0

                for k, ais in enumerate(ai_list):
                    yield from bps.mv(stage.th, ai0 + ais)

                    name_fmt = "{sample}_pos1_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                    for e in energies:
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(1)
                        if xbpm2.sumX.get() < 50:
                            yield from bps.sleep(2)
                            yield from bps.mv(energy, e)
                            yield from bps.sleep(1)
                        yield from bps.mv(piezo.x, xs - counter * x_step)
                        counter += 1
                        
                        bpm = xbpm2.sumX.get()
                        sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                        print(f"\n\t=== Sample: {sample_name} ===\n")
                        s.put(sample_name)
                        yield from bps.trigger_and_read(dets + [energy, waxs, xbpm2, xbpm3, att2_9] + [s])


                    name_fmt = "{sample}_pos2_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                    for e in energies[::-1]:
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(1)
                        if xbpm2.sumX.get() < 50:
                            yield from bps.sleep(2)
                            yield from bps.mv(energy, e)
                            yield from bps.sleep(1)
                        yield from bps.mv(piezo.x, xs - counter * x_step)
                        counter += 1

                        bpm = xbpm2.sumX.get()
                        sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                        print(f"\n\t=== Sample: {sample_name} ===\n")
                        s.put(sample_name)
                        yield from bps.trigger_and_read(dets + [energy, waxs, xbpm2, xbpm3, att2_9] + [s])

                yield from bps.mv(stage.th, ai0)

        (yield from inner())



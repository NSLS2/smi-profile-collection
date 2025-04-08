def run_night_Pete(t=1):
    # yield from giwaxs_S_edge_Pete(t=t)
    # yield from giwaxs_ai_S_edge_Pete(t=t)
    yield from nexafs_S_edge_Pete(t=1)


def giwaxs_multiprsangles_2020_3(t=1):
    dets = [pil1M, pil300KW]

    names = ["DDP_50", "DDP_25", "DDP_10", "DDP_100", "SEBS"]
    x = [-45000, -25000, -3000, 17000, 43000]
    z = [4190, 1690, -2310, -3310, -3810]
    chi_piezo = [-0.284, -0.129, -0.341, -0.401, -0.435]
    chi_hexa = [-0.256, -0.361, -0.349, -0.289, -0.255]
    th_hexa = [0.287, 0.287, 0.287, 0.287, 0.287]
    th_piezo = [0.76, 0.76, 0.56, 0.5, 0.5]

    waxs_arc = [1, 7.5]

    ai0 = 0
    ai_list = np.arange(0.07, 0.15, 0.002).tolist()
    ai_list = [round(1000 * x, 4) for x in ai_list]
    ai_list = np.asarray(ai_list) / 1000

    dets = [pil1M, pil300KW]

    for name, xs, zs, chi_pi, chi_hexa, th_pi, th_hexa in zip(
        names, x, z, chi_piezo, chi_hexa, th_piezo, th_hexa
    ):
        yield from bps.mv(prs, 0)
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.z, zs)
        yield from bps.mv(piezo.ch, chi_pi)
        yield from bps.mv(stage.ch, chi_hexa)
        yield from bps.mv(piezo.th, th_pi)
        yield from bps.mv(stage.th, th_hexa)

        yield from alignement_gisaxs(angle=0.14)
        yield from bps.mv(att1_9, "Insert")
        yield from bps.sleep(1)
        yield from bps.mv(att1_9, "Insert")

        yield from bps.mv(prs, 20)

        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)
            dets = [pil1M, pil300KW]

            for k, ais in enumerate(ai_list):
                yield from bps.mv(stage.th, th_hexa + ais)

                x_list = [-700, -500, -300, -100, 100, 300, 500, 700]
                for pos, xss in enumerate(x_list):
                    yield from bps.mv(piezo.x, xs + xss)
                    det_exposure_time(t, t)
                    name_fmt = "{sample}_aiscan_14keV_ai{ai}_pos{pos}_prs{prs}_wa{wax}"
                    sample_name = name_fmt.format(
                        sample=name,
                        ai="%4.3f" % ais,
                        pos="%2.2d" % pos,
                        prs="00",
                        wax=wa,
                    )
                    sample_id(user_name="GF", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)

        yield from bps.mv(prs, -70)
        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)
            dets = [pil1M, pil300KW]

            for k, ais in enumerate(ai_list):
                yield from bps.mv(stage.th, th_hexa + ais)
                yield from bps.mv(piezo.x, xs)
                det_exposure_time(t, t)
                name_fmt = "{sample}_aiscan_14keV_ai{ai}_pos{pos}_prs{prs}_wa{wax}"
                sample_name = name_fmt.format(
                    sample=name, ai="%4.3f" % ais, pos="00", prs="90", wax=wa
                )
                sample_id(user_name="GF", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

        yield from bps.mv(prs, -70)
        yield from bps.mv(stage.th, th_hexa + 0.15)
        prs_list = np.linspace(-70, 20, 46)

        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)
            dets = [pil1M, pil300KW]

            for k, prss in enumerate(prs_list):
                yield from bps.mv(prs, prss)
                yield from bps.mv(piezo.x, xs)
                det_exposure_time(t, t)
                name_fmt = "{sample}_prsscan_14keV_ai{ai}_pos{pos}_prs{prs}_wa{wax}"
                sample_name = name_fmt.format(
                    sample=name, ai="0.15", pos="00", prs="%2.2d" % prss, wax=wa
                )
                sample_id(user_name="GF", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

        yield from bps.mv(prs, 20)
        yield from bps.mv(stage.th, th_hexa + 0.2)
        prs_list = np.linspace(20, -70, 46)

        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)
            dets = [pil1M, pil300KW]

            for k, prss in enumerate(prs_list):
                yield from bps.mv(prs, prss)
                yield from bps.mv(piezo.x, xs)
                det_exposure_time(t, t)
                name_fmt = "{sample}_prsscan_14keV_ai{ai}_pos{pos}_prs{prs}_wa{wax}"
                sample_name = name_fmt.format(
                    sample=name, ai="0.20", pos="00", prs="%2.2d" % prss, wax=wa
                )
                sample_id(user_name="GF", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

        det_exposure_time(0.3, 0.3)
        sample_id(user_name="test", sample_name="test")


def giwaxs_S_edge_Pete(t=1):
    dets = [pil1M, pil300KW]

    # names = ['100_DDP_0deg','100_DDP_90deg','75_DDP_0deg''75_DDP_90deg','50_DDP_0deg','50_DDP_90deg','25_DDP_0deg','25_DDP_90deg']
    # x = [-48098, -29098, -21098, -2098, 9901, 52901, 28901, 39900 ]
    # z = [5000, -5000, 5000, -5000, 5000, -5000, 5000, -5000]

    names = ["50_DDP_0deg", "50_DDP_90deg", "25_DDP_0deg", "25_DDP_90deg"]
    x = [52000, 16902, 34902, 45902]
    z = [1000, -5000, 5000, -5000]

    energies = [
        2450.0,
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
        2490.0,
        2495.0,
        2500.0,
        2510.0,
    ]
    waxs_arc = [15, 0]

    ai0 = 0
    ai_list = [0.3, 0.5, 0.8]

    for name, xs, zs in zip(names, x, z):
        print(zs)
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.z, zs)
        yield from bps.mv(piezo.th, ai0)

        yield from alignement_special(angle=0.15)
        ai0 = piezo.th.position

        dets = [pil1M, pil300KW]
        yield from bps.mv(att2_9, "Insert")
        yield from bps.sleep(1)
        yield from bps.mv(att2_9, "Insert")

        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)

            for k, ais in enumerate(ai_list):

                yield from bps.mv(piezo.th, ai0 + ais)
                yield from bps.mv(piezo.x, xs + k * 400)

                det_exposure_time(t, t)
                name_fmt = "{sample}_{energy}eV_ai{ai}_pos1_wa{wax}_bpm{xbpm}"
                for e in energies:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(1)
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

                yield from bps.mv(energy, 2490)
                yield from bps.mv(energy, 2470)
                yield from bps.mv(energy, 2450)


def giwaxs_S_edge_Pete_2121_2(t=1):
    dets = [pil1M, pil300KW]

    # names =   ['sample1a', 'sample1b', 'sample2a', 'sample2b', 'sample3a', 'sample3b', 'sample4a', 'sample4b', 'sample5a', 'sample5b', 'sample6a',
    # 'sample6b','sample7a', 'sample7b']
    # x_piezo = [     50000,      42000,      35000,      28000,      21000,      13500,       6500,      -1500,      -9000,     -16000,     -23000,
    #     -32000,    -40800,     -49500]
    # x_hexa =  [         0,          0,          0,          0,          0,          0,          0,          0,          0,          0,          0,
    #          0,         0,          0]
    # z_piezo = [         0,          0,          0,          0,          0,          0,          0,          0,          0,          0,          0,
    #          0,         0,          0]

    names = [
        "sample8a",
        "sample8b",
        "sample9a",
        "sample9b",
        "sample10a",
        "sample10b",
        "sample11a",
        "sample11b",
        "sample12a",
        "sample12b",
    ]
    x_piezo = [49500, 41000, 33500, 26000, 18000, 10000, 2000, -7000, -14000, -21000]
    x_hexa = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    z_piezo = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    assert len(x_piezo) == len(
        names
    ), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(
        x_hexa
    ), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexa)})"
    assert len(x_piezo) == len(
        z_piezo
    ), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(z_piezo)})"

    dets = [pil1M, pil300KW]
    waxs_arc = [15, 0]

    for name, xs_piezo, xs_hexa, zs_piezo in zip(names, x_piezo, x_hexa, z_piezo):
        ai0 = 0
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, xs_piezo)
        yield from bps.mv(piezo.z, zs_piezo)
        yield from bps.mv(piezo.th, ai0)

        yield from alignement_gisaxs(angle=0.15)
        ai0 = piezo.th.position

        yield from bps.mv(att2_9.open_cmd, 1)
        yield from bps.sleep(1)
        yield from bps.mv(att2_9.open_cmd, 1)

        energies = [
            2450.0,
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
            2490.0,
            2495.0,
            2500.0,
            2510.0,
        ]
        ai_list = [0.3, 0.5, 0.8]

        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)

            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)
                yield from bps.mv(piezo.x, xs_piezo + k * 400)

                det_exposure_time(t, t)
                name_fmt = "{sample}_enscan_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
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

                yield from bps.mv(energy, 2490)
                yield from bps.sleep(2)
                yield from bps.mv(energy, 2470)
                yield from bps.sleep(2)
                yield from bps.mv(energy, 2450)
                yield from bps.sleep(2)

        ai_list = (
            np.arange(0.3, 0.44, 0.05).tolist()
            + np.arange(0.45, 0.6, 0.01).tolist()
            + np.arange(0.6, 1, 0.025).tolist()
        )
        ai_list = [round(1000 * x, 4) for x in ai_list]
        ai_list = np.asarray(ai_list) / 1000
        energies = [2450.0, 2477.0, 2510.0]

        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)

            for k, e in enumerate(energies):
                yield from bps.mv(energy, e)
                yield from bps.sleep(2)

                yield from bps.mv(piezo.x, xs_piezo + 2000 + k * 600 + i * 200)

                for l, ais in enumerate(ai_list):
                    yield from bps.mv(piezo.th, ai0 + ais)

                    det_exposure_time(t, t)
                    name_fmt = "{sample}_aiscan_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"

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

            yield from bps.mv(energy, 2490)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 2470)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 2450)
            yield from bps.sleep(2)


def giwaxs_ai_S_edge_Pete(t=1):
    dets = [pil1M, pil300KW]

    names = [
        "75_DDP_0deg",
        "75_DDP_90deg",
        "50_DDP_0deg",
        "50_DDP_90deg",
        "25_DDP_0deg",
        "25_DDP_90deg",
    ]
    x = [-22098, -8098, 4902, 17902, 35902, 46902]
    z = [5000, -5000, 5000, -5000, 5000, -5000]

    energies = [2450.0, 2477.0, 2510.0]
    waxs_arc = [15, 0]

    ai0 = 0
    ai_list = (
        np.arange(0.3, 0.44, 0.05).tolist()
        + np.arange(0.45, 0.6, 0.01).tolist()
        + np.arange(0.6, 1, 0.025).tolist()
    )
    ai_list = [round(1000 * x, 4) for x in ai_list]
    ai_list = np.asarray(ai_list) / 1000

    dets = [pil1M, pil300KW]

    for name, xs, zs in zip(names, x, z):
        print(zs)
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.z, zs)
        yield from bps.mv(piezo.th, ai0)

        yield from alignement_special(angle=0.15)

        ai0 = piezo.th.position

        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)

            if i == 0:
                dets = [pil1M, pil300KW]
                yield from bps.mv(att2_9, "Insert")
                yield from bps.sleep(1)
                yield from bps.mv(att2_9, "Insert")

            else:
                dets = [pil300KW]
                yield from bps.mv(att2_9, "Insert")
                yield from bps.sleep(1)
                yield from bps.mv(att2_9, "Insert")

            for k, ais in enumerate(ai_list):

                yield from bps.mv(piezo.th, ai0 + ais)
                yield from bps.mv(piezo.x, xs + k * 200)

                det_exposure_time(t, t)
                name_fmt = "{sample}_aiscan_{energy}eV_ai{ai}_pos1_wa{wax}_bpm{xbpm}"
                for e in energies:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(0.5)
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

                yield from bps.mv(energy, 2490)
                yield from bps.mv(energy, 2470)
                yield from bps.mv(energy, 2450)


def nexafs_S_edge_Pete(t=1):

    yield from bps.mv(waxs, 52.5)
    dets = [pil300KW]

    names = ["100_DDP_0deg_vertically_ai0.5deg"]
    x = [-52000]
    z = [-5000]

    energies = [
        2450.0,
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
        2490.0,
        2495.0,
        2500.0,
        2510.0,
    ]

    for name, xs in zip(names, x):
        # yield from bps.mv(piezo.x, xs)

        yield from bps.mv(att2_9, "Retract")
        yield from bps.mv(GV7.close_cmd, 1)
        yield from bps.sleep(1)
        yield from bps.mv(att2_9, "Retract")
        yield from bps.mv(GV7.close_cmd, 1)
        yield from bps.sleep(1)

        # yield from bps.mv(piezo.th, 1.5)

        det_exposure_time(t, t)
        name_fmt = "{sample}_{energy}eV_wa52.5_bpm{xbpm}"
        for e in energies:
            yield from bps.mv(energy, e)
            yield from bps.sleep(0.5)
            bpm = xbpm2.sumX.value
            sample_name = name_fmt.format(
                sample=name, energy="%6.2f" % e, xbpm="%4.3f" % bpm
            )
            sample_id(user_name="GF", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)

        yield from bps.mv(energy, 2490)
        yield from bps.mv(energy, 2470)
        yield from bps.mv(energy, 2450)


def giwaxs_Dudenas(t=1):
    # sample alignement
    global names, x_piezo, z_piezo, incident_angles, y_piezo_aligned, xs_hexa

    # names =  ['sample1a', 'sample1b', 'sample2a', 'sample2b', 'sample3a', 'sample3b', 'sample4a', 'sample4b', 'sample5a', 'sample5b', 'sample6a', 'sample6b', 'sample7a', 'sample7b', 'sample8a', 'sample8b', 'sample9a']
    # x_piezo = [58500, 58500, 51000, 44000, 35500, 27500, 19000, 12000, 3000, -4000, -13000, -22000, -31000, -39500, -48500, -56500, -58500]
    # y_piezo = [ 6800,  6800,  6800,  6800,  6800,  6800,  6800,  6800, 6800,  6800,   6800,   6800,   6800,   6800,   6800,   6800,   6800]
    # z_piezo = [    0,     0,     0,     0,     0,     0,    0,      0,    0,     0,      0,      0,      0,      0,      0,      0,      0]
    # x_hexa =  [   12,     0,     0,     0,     0,     0,    0,      0,    0,     0,      0,      0,      0,      0,      0,      0,     -6]

    # incident_angles = [ 0.09662,   0.2324, 0.667321, 0.021775, 0.090698, -0.042509, -0.196683, -0.259349, -0.158024, -0.335898, -0.133203, 0.539725, 0.416476, -0.148083, -0.124885, -0.017261, 0.034793]
    # y_piezo_aligned = [7155.819, 7172.108, 7140.523, 7068.093, 7031.481,  7053.709,  7060.481,  7043.072,  7022.551,  6988.161,  7002.442, 6952.913, 6921.413,  6880.875,  6864.228,   6856.68, 6882.685]

    # names =  ['sample2a', 'sample2b','sample3a', 'sample3b', 'sample4a', 'sample4b', 'sample5a', 'sample5b', 'sample6a', 'sample6b', 'sample7a', 'sample7b', 'sample8a', 'sample8b', 'sample9a', 'sample9b', 'sample10a',
    # 'sample10b', 'sample11a', 'sample11b']
    # x_piezo = [58500, 58500, 55500, 48500, 41500, 35500, 26500, 20500, 12500, 4500, -3500, -10500, -17500, -25500, -32000, -39000, -47000, -54000, -58500, -58500]
    # y_piezo = [ 6900,  6900,  6900,  6900,  6900,  6900,  6900,  6900,  6900, 6900,  6900,   6900,   6900,   6900,   6900,   6900,   6900,   6900,   6900,   6900]
    # z_piezo = [    0,     0,     0,     0,     0,     0,    0,      0,     0,    0,     0,      0,      0,      0,      0,      0,      0,      0,      0,      0]
    # x_hexa =  [   11,   4.5,     0,     0,     0,     0,    0,      0,     0,    0,     0,      0,      0,      0,      0,      0,      0,      0,   -2.5,    -10]

    names = ["sample12a", "sample12b"]
    x_piezo = [58000, 58000]
    y_piezo = [6900, 6900]
    z_piezo = [0, 0]
    x_hexa = [10, 0.5]

    assert len(x_piezo) == len(
        names
    ), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(
        y_piezo
    ), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(
        z_piezo
    ), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(z_piezo)})"
    assert len(x_piezo) == len(
        x_hexa
    ), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexa)})"

    dets = [pil300KW, pil1M]
    waxs_arc = [1, 7.5]

    ai0 = 0
    ai_list = np.arange(0.06, 0.158, 0.002).tolist()
    ai_list = [round(1000 * x, 4) for x in ai_list]
    ai_list = np.asarray(ai_list) / 1000

    for name, xs, zs, ys, xs_hexa in zip(names, x_piezo, z_piezo, y_piezo, x_hexa):
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)
        yield from bps.mv(piezo.th, 0)

        yield from alignement_gisaxs(angle=0.14)
        yield from bps.mv(att1_9.open_cmd, 1)
        yield from bps.sleep(1)
        yield from bps.mv(att1_9.open_cmd, 1)

        aiss = piezo.th.position

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)

            det_exposure_time(t, t)
            name_fmt = "{sample}_sdd8.3m_14keV_ai{angle}deg_wa{waxs}"

            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, aiss + ais)

                x_list = [-700, -500, -300, -100, 100, 300, 500, 700]
                for pos, xss in enumerate(x_list):
                    yield from bps.mv(piezo.x, xs + xss)
                    det_exposure_time(t, t)
                    name_fmt = "{sample}_aiscan_14keV_ai{ai}_pos{pos}_wa{wax}"
                    sample_name = name_fmt.format(
                        sample=name, ai="%4.3f" % ais, pos="%2.2d" % pos, wax=wa
                    )
                    sample_id(user_name="GF", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)


def giwaxs_S_edge_Pete_2121_3(t=1):
    dets = [pil1M, pil900KW]

    names = ["N22as", "N22an", "SG", "PTB_OTS", "PTB_Ox", "PTB_UVO"]
    x_piezo = [51700, 49500, 34000, 19000, 6000, -6500]
    x_hexa = [12, 0, 0, 0, 0, 0]
    z_piezo = [0, 0, 0, 0, 0, 0]

    assert len(x_piezo) == len(
        names
    ), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(
        x_hexa
    ), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexa)})"
    assert len(x_piezo) == len(
        z_piezo
    ), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(z_piezo)})"

    dets = [pil1M, pil900KW]
    waxs_arc = [20, 0]

    for name, xs_piezo, xs_hexa, zs_piezo in zip(names, x_piezo, x_hexa, z_piezo):
        ai0 = 0.5
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, xs_piezo)
        yield from bps.mv(piezo.z, zs_piezo)
        yield from bps.mv(piezo.th, ai0)

        yield from alignement_gisaxs(angle=0.3)
        ai0 = piezo.th.position

        yield from bps.mv(att2_9.open_cmd, 1)
        yield from bps.sleep(1)
        yield from bps.mv(att2_9.open_cmd, 1)

        energies = [
            2450.0,
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
            2490.0,
            2495.0,
            2500.0,
            2510.0,
        ]
        ai_list = [0.3, 0.5, 0.8]

        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)

            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)
                yield from bps.mv(piezo.x, xs_piezo + k * 400)

                det_exposure_time(t, t)
                name_fmt = "{sample}_enscan_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(3)
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

                yield from bps.mv(energy, 2490)
                yield from bps.sleep(2)
                yield from bps.mv(energy, 2470)
                yield from bps.sleep(2)
                yield from bps.mv(energy, 2450)
                yield from bps.sleep(2)

        ai_list = (
            np.arange(0.3, 0.44, 0.05).tolist()
            + np.arange(0.45, 0.6, 0.01).tolist()
            + np.arange(0.6, 1, 0.025).tolist()
        )
        ai_list = [round(1000 * x, 4) for x in ai_list]
        ai_list = np.asarray(ai_list) / 1000
        energies = [2450.0, 2470, 2477.0, 2480, 2510.0]

        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)

            for k, e in enumerate(energies):
                yield from bps.mv(energy, e)
                yield from bps.sleep(3)

                yield from bps.mv(piezo.x, xs_piezo + 2000 + k * 600 + i * 200)

                for l, ais in enumerate(ai_list):
                    yield from bps.mv(piezo.th, ai0 + ais)

                    det_exposure_time(t, t)
                    name_fmt = "{sample}_aiscan_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"

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

            yield from bps.mv(energy, 2490)
            yield from bps.sleep(3)
            yield from bps.mv(energy, 2470)
            yield from bps.sleep(3)
            yield from bps.mv(energy, 2450)
            yield from bps.sleep(3)


def S_edge_measurments_2021_3_Lee(t=1):
    dets = [pil1M, pil900KW, pil300KW]
    det_exposure_time(t, t)

    # names = ['P3C5T_1','P3C5T_2','P3C5T_3', 'PDOT']
    # x_piezo = [ -22000,   -37000,   -53000, -55000]
    # x_hexap = [      0,        0,        0,    -12]
    # y_piezo = [   3800,     3800,     3800,   3800]

    names = ["EG_PPS", "EG_PPS_dc_thin", "EG_PPS_dc_thick"]
    x_piezo = [-20000, -33000, -45000]
    x_hexap = [0, 0, 0]
    y_piezo = [3800, 3800, 3800]

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

    waxs_arc = [2, 23]
    ai0 = 0.5
    ai_list = [0.5, 0.8]

    for name, xs, ys, xs_hexap in zip(names, x_piezo, y_piezo, x_hexap):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(stage.x, xs_hexap)

        yield from bps.mv(piezo.th, 0.5)
        yield from alignement_gisaxs_quickLee(0.30)

        yield from bps.mv(att2_9.open_cmd, 1)
        yield from bps.sleep(1)
        yield from bps.mv(att2_9.open_cmd, 1)

        ai0 = piezo.th.position
        det_exposure_time(t, t)

        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)
            yield from bps.mv(piezo.x, xs)
            counter = 0

            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                name_fmt = "{sample}_{energy}eV_ai{ai}_pos1_wa{wax}_bpm{xbpm}"
                for e in energies:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(3)
                    yield from bps.mv(piezo.x, xs + counter * 30)
                    counter += 1

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

                name_fmt = "{sample}_{energy}eV_ai{ai}_pos2_wa{wax}_bpm{xbpm}"
                for e in energies[::-1]:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(3)
                    yield from bps.mv(piezo.x, xs + counter * 30)
                    counter += 1

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

                name_fmt = "{sample}_{energy}eV_ai{ai}_pos3_wa{wax}_bpm{xbpm}"
                for e in energies:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(3)
                    yield from bps.mv(piezo.x, xs + counter * 30)
                    counter += 1

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

                name_fmt = "{sample}_{energy}eV_ai{ai}_pos4_wa{wax}_bpm{xbpm}"
                for e in energies[::-1]:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(3)
                    yield from bps.mv(piezo.x, xs + counter * 30)
                    counter += 1

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


def night(t=1):
    yield from giwaxs_S_edge_Pete_2121_3(t=t)
    proposal_id("2021_3", "304296_Richter")
    yield from S_edge_measurments_2021_3_Lee(t=t)


def giwaxs_vert_S_edge_Pete_2121_3(t=1):
    name = "PTB_OTS"  #'N22an'
    dets = [pil900KW]

    energies = [
        2450.0,
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
        2490.0,
        2495.0,
        2500.0,
        2510.0,
    ]

    name_fmt = "{sample}_vertical_{energy}eV_ai0.7deg_wa{wax}_bpm{xbpm}"
    for e in energies:
        yield from bps.mv(energy, e)
        yield from bps.sleep(3)
        bpm = xbpm2.sumX.value
        sample_name = name_fmt.format(
            sample=name, energy="%6.2f" % e, wax="11.5", xbpm="%4.3f" % bpm
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

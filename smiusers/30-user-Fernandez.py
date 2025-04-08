def giwaxs_Fernandez(t=1):
    # sample alignement
    global names, x_piezo, z_piezo, incident_angles, y_piezo_aligned, xs_hexa
    # names =  ['BKGD',  'A1',  'A2', 'A3',   'A4',   'A5',
    #             'A6',  'A7',  'A8', 'A9',  'A10',  'A11',  'A12']
    # x_piezo = [58000, 41000, 21000, 1000, -17000, -37000,
    #            58000, 41000, 21000, 1000, -17000, -37000, -55500]
    # y_piezo = [ 6900,  6900,  6900, 6900,   6900,   6900,
    #            -2200, -2200, -2200,-2200,  -2200,  -2200,  -2200]
    # z_piezo = [    0,     0,     0,    0,      0,       0,
    #             5000,  5000,  5000, 5000,   5000,    5000,   5000]
    # x_hexa =  [    6,      0,    0,    0,      0,       0,
    #                6,      0,    0,    0,      0,       0,     -4]

    # names =  ['A13',  'A14',  'A15', 'A16',   'A17',   'A18',
    #             'A19',  'A20',  'A21', 'A22',  'A23',  'A24',  'A25']
    # x_piezo = [58000, 41000, 21000, 1000, -19000, -39000,
    #            58000, 41000, 21000, 1000, -19000, -39000, -55500]
    # y_piezo = [ 6900,  6900,  6900, 6900,   6900,   6900,
    #            -2200, -2200, -2200,-2200,  -2200,  -2200,  -2200]
    # z_piezo = [    0,     0,     0,    0,      0,       0,
    #             5000,  5000,  5000, 5000,   5000,    5000,   5000]
    # x_hexa =  [    6,      0,    0,    0,      0,       0,
    #                6,      0,    0,    0,      0,       0,     -4]

    names = [
        "A26",
        "A27",
        "A28",
        "A29",
        "A30",
        "BKGD",
        "A01",
        "A02",
        "A03",
        "A04",
        "A05",
        "A06",
        "A07",
    ]
    x_piezo = [
        55000,
        40000,
        17000,
        -2000,
        -25000,
        -47500,
        55000,
        40000,
        17000,
        -2000,
        -25000,
        -42500,
        -57000,
    ]
    y_piezo = [
        6900,
        6900,
        6900,
        6900,
        6900,
        6900,
        -2200,
        -2200,
        -2200,
        -2200,
        -2200,
        -2200,
        -2200,
    ]
    z_piezo = [0, 0, 0, 0, 0, 0, 5000, 5000, 5000, 5000, 5000, 5000, 5000]
    x_hexa = [6, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, -5]

    # incident_angles = [-0.428311, -0.587565, -0.492445, 0.009011, -0.356074, -0.446316, -0.932245, -0.908126, -0.944155, -1.175827, -1.140861, -1.015834, -0.925797]
    # y_piezo_aligned = [ 6493.112,  6492.969,  6482.293, 6473.455,   6459.49,  6445.813, -2312.519, -2349.623, -2362.358, -2396.463,   -2397.1, -2431.483, -2387.921]
    incident_angles = [
        -0.321218,
        -0.45491,
        -0.440744,
        -0.17595,
        -0.394264,
        -0.443751,
        -1.407557,
        -0.820769,
        -1.09834,
        -1.617552,
        -1.093352,
        -0.984098,
        -0.959991,
    ]
    y_piezo_aligned = [
        6489.362,
        6512.907,
        6528.814,
        6534.525,
        6481.937,
        6480.819,
        -2341.031,
        -2307.083,
        -2356.385,
        -2465.571,
        -2386.802,
        -2381.393,
        -2357.137,
    ]

    # smi = SMI_Beamline()
    # yield from smi.modeAlignment(technique='gisaxs')

    # for name, xs_piezo, zs_piezo, ys_piezo, xs_hexa in zip(names, x_piezo, z_piezo, y_piezo, x_hexa):
    #     yield from bps.mv(stage.x, xs_hexa)
    #     yield from bps.mv(piezo.x, xs_piezo)
    #     yield from bps.mv(piezo.y, ys_piezo)
    #     yield from bps.mv(piezo.z, zs_piezo)

    #     if ys_piezo>0:
    #         yield from bps.mv(piezo.th, 0)
    #         yield from alignement_gisaxs_multisample(angle = 0.08)
    #     else:
    #         yield from bps.mv(piezo.th, -1)
    #         yield from alignement_gisaxs_multisample_special(angle = 0.08)

    #     incident_angles = incident_angles + [piezo.th.position]
    #     y_piezo_aligned = y_piezo_aligned + [piezo.y.position]

    # yield from smi.modeMeasurement()

    print(incident_angles)
    print(y_piezo_aligned)

    dets = [pil300KW, pil1M]
    waxs_arc = np.linspace(0, 19.5, 4)
    angle = np.linspace(0.04, 0.18, 15)

    for wa in waxs_arc[::-1]:
        yield from bps.mv(waxs, wa)

        for name, xs, zs, aiss, ys, xs_hexa in zip(
            names, x_piezo, z_piezo, incident_angles, y_piezo_aligned, x_hexa
        ):
            yield from bps.mv(stage.x, xs_hexa)
            yield from bps.mv(piezo.x, xs)
            yield from bps.mv(piezo.y, ys)
            yield from bps.mv(piezo.z, zs)
            yield from bps.mv(piezo.th, aiss)

            det_exposure_time(t, t)
            name_fmt = "{sample}_sdd5m_12keV_ai{angle}deg_wa{waxs}"

            for num, an in enumerate(angle):
                yield from bps.mv(piezo.th, aiss + an)
                # yield from bps.mv(piezo.x, xs - num * 100)

                sample_name = name_fmt.format(
                    sample=name, angle="%3.2f" % an, waxs="%2.1f" % wa
                )
                sample_id(user_name="LF", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")

                yield from bp.count(dets, num=1)

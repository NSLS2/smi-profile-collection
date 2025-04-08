def giwaxs_giri_2021_3(t=0.5):
    user = "GG"

    # names = ['P1-1','P1-2','P2-1','P2-2','P3-1','P3-2','P4-1','P4-2','P5-1','P5-2','P6-1','P6-2','P7-1','P7-2','P8-1','P8-2','P9-1','P9-2']
    # names = ['S1-2','S1-3','S2-1','S2-2','S2-3','S3-1','S3-2','S3-3','S4-1']
    # names = ['S4-2','S4-3', 'S5-1','S5-2','S5-3','S6-1','S6-2','S6-3','S7-1','S7-2','S7-3','S8-1','S8-2','S8-3']
    # names = ['S9-2','S9-3','S10-1','S10-2','S10-3','S11-1','S11-2','S11-3','S12-1','S12-2','S12-3','S13-1','S13-2','S13-3']
    # names = ['S14-1','S14-2','S15-1','S15-2','S16-1','S16-2','S17-1','S17-2','S18-1','S18-2','S19-1','S19-2','S20-1','S20-2','S21-1','S21-2','S22-1']
    # names = ['S22-2','S23-1','S23-2','S24-1','S24-2','S25-1','S25-2','S26-1','S26-2','S27-1','S27-2','S28-1','S28-2','S29-1','S29-2','S30-1','S30-2']
    names = [
        "S31-1",
        "S31-2",
        "S32-1",
        "S32-2",
        "S33-1",
        "S33-2",
        "S34-1",
        "S34-2",
        "S35-1",
        "S35-2",
        "S36-1",
        "S36-2",
        "S37-1",
        "S37-2",
    ]

    x_piezo = [
        59000,
        59000,
        51000,
        43000,
        33000,
        25000,
        17000,
        9000,
        -5000,
        -15000,
        -25000,
        -33000,
        -43000,
        -53000,
    ]
    y_piezo = [
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
    z_piezo = [
        1000,
        1000,
        1000,
        1000,
        1000,
        1000,
        1000,
        1000,
        1000,
        1000,
        1000,
        1000,
        1000,
        1000,
    ]
    x_hexa = [8, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

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

    waxs_arc = [9]
    angle = [0.15]

    dets = [pil900KW]
    det_exposure_time(t, t)

    for name, xs, zs, ys, xs_hexa in zip(names, x_piezo, z_piezo, y_piezo, x_hexa):
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)
        yield from bps.mv(piezo.th, 1)

        yield from alignement_gisaxs(angle=0.1)

        ai0 = piezo.th.position
        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)

            for i, an in enumerate(angle):
                yield from bps.mv(piezo.x, xs)
                yield from bps.mv(piezo.th, ai0 + an)
                name_fmt = "{sample}_16.1keV_ai{angl}deg_wa{waxs}"
                sample_name = name_fmt.format(
                    sample=name, angl="%3.2f" % an, waxs="%2.1f" % wa
                )
                sample_id(user_name=user, sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")

                yield from bp.count(dets, num=1)

            yield from bps.mv(piezo.th, ai0)

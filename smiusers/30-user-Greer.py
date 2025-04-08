def mapping_saxs_Greer(t=5):
    # samples = ['SPYZ_new', 'BOYZ', 'SPXZ', 'BOXZ']

    # x_list = [29000, 9330, -6470, -28870]
    # y_list = [3530, 2190, 3310, 2680]

    # x_range=[[0, 60, 4],[0, 80, 5], [0, 60, 4], [0, 60, 4]]
    # y_range=[[0, -300, 151], [0, -140, 71], [0, -300, 151], [0, -160, 81]]

    samples = ["SPYZ_90deg", "BOYZ_90deg", "SPXZ_90deg", "BOXZ_90deg"]
    name = "JG"
    x_list = [26570, 6780, -11660, -33150]
    y_list = [3250, 2970, 2110, 1960]

    x_range = [[0, -300, 16], [0, -200, 21], [0, -340, 18], [0, -200, 11]]
    y_range = [[0, -60, 31], [0, -60, 31], [0, -60, 31], [0, -60, 31]]

    # Detectors, motors:
    dets = [pil1M, pil300KW, amptek]  # dets = [pil1M,pil300KW]
    det_exposure_time(t, t)

    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    assert len(x_list) == len(
        y_list
    ), f"Number of X coordinates ({len(x_list)}) is different from Y coordinates ({len(y_list)})"
    assert len(x_list) == len(
        x_range
    ), f"Number of X coordinates ({len(x_list)}) is different X ranges ({len(x_range)})"
    assert len(x_list) == len(
        y_range
    ), f"Number of X coordinates ({len(x_list)}) is different Y ranges ({len(y_range)})"

    waxs_range = np.linspace(0, 26, 5)

    for wa in waxs_range:
        yield from bps.mv(waxs, wa)
        for x, y, sample, x_r, y_r in zip(x_list, y_list, samples, x_range, y_range):
            yield from bps.mv(piezo.x, x)
            yield from bps.mv(piezo.y, y)
            name_fmt = "{sam}_wa{waxs}deg"
            sample_name = name_fmt.format(sam=sample, waxs="%2.1f" % wa)
            sample_id(user_name=name, sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")

            yield from bp.rel_grid_scan(
                dets, piezo.x, *x_r, piezo.y, *y_r, 0
            )  # 1 = snake, 0 = not-snake

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def mapping_saxs_test(t=0.1):

    samples = ["test"]
    name = "test"
    x_list = [0]
    y_list = [0]

    x_range = [[0, 0, 2]]
    y_range = [[0, 0, 1]]

    # Detectors, motors:
    dets = [pil1M, pil300KW, amptek]  # dets = [pil1M,pil300KW]
    det_exposure_time(t, t)

    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    assert len(x_list) == len(
        y_list
    ), f"Number of X coordinates ({len(x_list)}) is different from Y coordinates ({len(y_list)})"
    assert len(x_list) == len(
        x_range
    ), f"Number of X coordinates ({len(x_list)}) is different X ranges ({len(x_range)})"
    assert len(x_list) == len(
        y_range
    ), f"Number of X coordinates ({len(x_list)}) is different Y ranges ({len(y_range)})"

    for x, y, sample, x_r, y_r in zip(x_list, y_list, samples, x_range, y_range):
        yield from bps.mvr(piezo.x, x)
        yield from bps.mvr(piezo.y, y)
        name_fmt = "{sam}"
        sample_name = name_fmt.format(sam=sample)
        sample_id(user_name=name, sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")

        yield from bp.rel_grid_scan(
            dets, piezo.x, *x_r, piezo.y, *y_r, 0
        )  # 1 = snake, 0 = not-snake

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)

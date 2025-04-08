####line scan


def aaron_rot(t=5):
    sample_id(user_name="AM", sample_name="tetra2_1741")
    det_exposure_time(t, t)
    # yield from bp.inner_product_scan([pil1M], 121, prs, 60, -60, piezo.x, -2667.5, -2605.5)
    # yield from bp.inner_product_scan([pil1M], 121, prs, 60, -60, piezo.x, -2680, -2610)
    yield from bp.inner_product_scan([pil1M], 15, prs, 60, 46, piezo.x, 5550, 5580)
    yield from bp.inner_product_scan([pil1M], 45, prs, 45, 0, piezo.x, 5580, 5640)
    yield from bp.inner_product_scan([pil1M], 45, prs, 1, -45, piezo.x, 5640, 5641)
    yield from bp.inner_product_scan([pil1M], 15, prs, -46, -60, piezo.x, 5640, 5641)
    # yield from bp.inner_product_scan([pil1M], 10, prs, 34, 25, stage.x, 0.318, 0.254, piezo.y, -580, -580)
    # yield from bp.inner_product_scan([pil1M], 10, prs, 24, 15, stage.x, 0.254, 0.195, piezo.y, -580, -579)
    # yield from bp.inner_product_scan([pil1M], 10, prs, 14, 5, stage.x, 0.195, 0.138, piezo.y, -579, -580)
    # yield from bp.inner_product_scan([pil1M], 5, prs, 4, 0, stage.x, 0.138, 0.118, piezo.y, -580, -577)
    # yield from bp.inner_product_scan([pil1M], 10, prs, 1, -10, stage.x, 0.118, 0.061, piezo.y, -577, -577)
    # yield from bp.inner_product_scan([pil1M], 10, prs, -11, -20, stage.x, 0.061, 0.031, piezo.y, -577, -577)
    # yield from bp.inner_product_scan([pil1M], 10, prs, -21, -30, stage.x, 0.031, 0.002, piezo.y, -577, -575)
    # yield from bp.inner_product_scan([pil1M], 10, prs, -31, -40, stage.x, 0.002, -0.013, piezo.y, -575, -575)
    # yield from bp.inner_product_scan([pil1M], 10, prs, -41, -50, stage.x, -0.013, -0.0175, piezo.y, -575, -575)
    sample_id(user_name="test", sample_name="test")


def test_scan(start=11800, t=10, step=10):
    for i in range(t):
        new_ivu_gap.set(start - i * step)
        yield from bps.sleep(2)


def waxs_aaron_2021_3(t=2):
    user = "AM"

    names = ["Ito_back", "Pt-Azo_back"]

    x_piezo = [19499, 16260]
    y_piezo = [-840, -840]
    z_piezo = [2300, 2300]
    x_hexa = [0, 0]

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

    waxs_arc = [20, 0]
    offset = [0, 100]

    dets = [pil900KW, pil1M]
    det_exposure_time(t, t)

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)

        for name, xs, zs, ys, xs_hexa in zip(names, x_piezo, z_piezo, y_piezo, x_hexa):
            yield from bps.mv(stage.x, xs_hexa)
            yield from bps.mv(piezo.x, xs)
            yield from bps.mv(piezo.y, ys)
            yield from bps.mv(piezo.z, zs)

            for off in offset:
                yield from bps.mv(piezo.x, xs + off)
                name_fmt = "{sample}_16.1keV_pos{pos}_wa{waxs}"
                sample_name = name_fmt.format(
                    sample=name, pos="%1.1d" % off, waxs="%2.1f" % wa
                )
                sample_id(user_name=user, sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")

                yield from bp.count(dets, num=1)

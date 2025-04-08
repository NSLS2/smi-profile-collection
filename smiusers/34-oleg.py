####line scan


def aaron_rot(t=8):
    sample_id(user_name="AM", sample_name="octahedron_plate_cut")
    det_exposure_time(t)
    yield from bp.inner_product_scan(
        [pil1M], 11, prs, 45, 35, stage.x, 0.3834, 0.318, piezo.y, -580, -580
    )
    yield from bp.inner_product_scan(
        [pil1M], 10, prs, 34, 25, stage.x, 0.318, 0.254, piezo.y, -580, -580
    )
    yield from bp.inner_product_scan(
        [pil1M], 10, prs, 24, 15, stage.x, 0.254, 0.195, piezo.y, -580, -579
    )
    yield from bp.inner_product_scan(
        [pil1M], 10, prs, 14, 5, stage.x, 0.195, 0.138, piezo.y, -579, -580
    )
    yield from bp.inner_product_scan(
        [pil1M], 5, prs, 4, 0, stage.x, 0.138, 0.118, piezo.y, -580, -577
    )
    yield from bp.inner_product_scan(
        [pil1M], 10, prs, 1, -10, stage.x, 0.118, 0.061, piezo.y, -577, -577
    )
    yield from bp.inner_product_scan(
        [pil1M], 10, prs, -11, -20, stage.x, 0.061, 0.031, piezo.y, -577, -577
    )
    yield from bp.inner_product_scan(
        [pil1M], 10, prs, -21, -30, stage.x, 0.031, 0.002, piezo.y, -577, -575
    )
    yield from bp.inner_product_scan(
        [pil1M], 10, prs, -31, -40, stage.x, 0.002, -0.013, piezo.y, -575, -575
    )
    yield from bp.inner_product_scan(
        [pil1M], 10, prs, -41, -50, stage.x, -0.013, -0.0175, piezo.y, -575, -575
    )


def custo_scan(username, sample_na, meas_t):
    det_exposure_time(meas_t)
    name_fmt = "{sample}_x_{x_pos}_y_{y_pos}_{expo}s"
    sample_name = name_fmt.format(
        sample=sample_na,
        x_pos=float("%.3f" % piezo.x.position),
        y_pos=float("%.3f" % piezo.y.position),
        expo=meas_t,
    )
    sample_id(user_name=username, sample_name=sample_name)
    yield from bp.count([pil1M], num=1)

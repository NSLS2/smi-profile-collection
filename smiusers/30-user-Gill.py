def gill_giwaxs(exp_time=0.5):
    dets = [pil300KW, pil900KW]
    name = "CEll_RT_overnight"
    # initial_angle_zero = -0.72
    inc_angle = [0.12, 0.22, 0.30, 0.4]
    waxs_arc = [0, 20, 40]
    # yield from bps.mv(stage.th, initial_angle_zero)
    x = [-3.1]
    for i, xsss in enumerate(x):
        yield from bps.mv(stage.x, xsss)
        # yield from bps.mv(prs, ph)
        yield from bps.mv(GV7.open_cmd, 1)
        yield from bps.sleep(1)
        yield from bps.mv(GV7.open_cmd, 1)

        yield from alignement_gisaxs_hex(angle=0.2)

        yield from bps.mv(GV7.close_cmd, 1)
        yield from bps.sleep(1)
        yield from bps.mv(GV7.close_cmd, 1)

        ai_0 = stage.th.position
        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)
            for incident_angle in inc_angle:
                name_fmt = "{sample}_pos{pos}_{angle}deg_wa{wa}"
                yield from bps.mv(stage.th, ai_0 + incident_angle)
                sample_name = name_fmt.format(
                    sample=name,
                    pos="%1.1d" % i,
                    angle="%1.2f" % incident_angle,
                    wa="%2.1f" % wa,
                )
                print(f"\n\t=== Sample: {sample_name} ===\n")
                sample_id(user_name="SG", sample_name=sample_name)
                det_exposure_time(exp_time, exp_time)
                yield from bp.count(dets, num=1)

        yield from bps.mv(stage.th, ai_0)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)


def gill_giwaxs_bkg(exp_time=1):
    dets = [pil300KW, pil900KW]
    name = "CEll_RT_bkg"
    # initial_angle_zero = -0.72
    waxs_arc = [0, 20, 40]
    # yield from bps.mv(stage.th, initial_angle_zero)
    y = [-3, -3.02, -3.04, -3.06, -3.08, -3.10, -3.12, -3.14]
    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)
        for i, ys in enumerate(y):
            yield from bps.mv(stage.y, ys)
            name_fmt = "{sample}_pos{pos}_wa{wa}"
            sample_name = name_fmt.format(sample=name, pos="%1.1d" % i, wa="%2.1f" % wa)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            sample_id(user_name="SG", sample_name=sample_name)
            det_exposure_time(exp_time, exp_time)
            yield from bp.count(dets, num=1)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)

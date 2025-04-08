def rotation_saxs(t=1):

    # sample = ['Hopper2_AGIB_AuPd_top', 'Hopper2_AGIB_AuPd_mid', 'Hopper2_AGIB_AuPd_bot'] #Change filename
    sample = ["AGIB3N_1top", "AGIB3N_1mid", "AGIB3N_1cen"]  # Change filename
    # y_list  = [-6.06, -6.04, -6.02] #hexapod is in mm
    # y_list  = [-10320, -10300, -10280]  #SmarAct is um
    y_list = [4760, 4810, 4860]  # , 5210]  #SmarAct is um

    assert len(y_list) == len(
        sample
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"

    # Detectors, motors:
    # dets = [pil1M, rayonix, pil300KW]
    dets = [pil1M, pil300KW]
    prs_range = [-90, 90, 91]
    waxs_range = [0, 26, 5]  # step of 6.5 degrees
    det_exposure_time(t, t)

    # pil_pos_x = [-0.4997, -0.4997 + 4.3, -0.4997 + 4.3, -0.4997]
    # pil_pos_y = [-59.9987, -59.9987, -59.9987 + 4.3, -59.9987]

    # waxs_po = np.linspace(20.95, 2.95, 4)

    for sam, y in zip(sample, y_list):
        # yield from bps.mv(stage.y, y) #hexapod
        yield from bps.mv(piezo.y, y)  # SmarAct
        name_fmt = "{sam}"
        sample_name = name_fmt.format(sam=sam)
        sample_id(user_name="MK", sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")
        yield from bp.grid_scan(dets, prs, *prs_range, waxs, *waxs_range, 1)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def rotation_saxs_fast(t=1):

    sample = [
        "AGIB3DR_2fast_top",
        "AGIB3DR_2fast_mid",
        "AGIB3DR_2fast_cen",
    ]  # Change filename
    y_list = [5150, 5230, 5310]  # SmarAct is um

    assert len(y_list) == len(
        sample
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"

    # Detectors, motors:
    dets = [pil1M, pil300KW]
    prs_range = np.linspace(-90, 90, 91)
    waxs_range = np.linspace(0, 26, 5)
    det_exposure_time(t, t)
    for sam, y in zip(sample, y_list):
        yield from bps.mv(piezo.y, y)
        for wa in waxs_range:
            yield from bps.mv(waxs, wa)
            for pr in prs_range:
                yield from bps.mv(prs, pr)
                name_fmt = "{sam}_wa{waxs}deg_{prs}deg"
                sample_name = name_fmt.format(
                    sam=sam, waxs="%2.1f" % wa, prs="%3.3d" % pr
                )
                sample_id(user_name="MK", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def rotation_saxs_att(t=1):  # attenuated WAXS, so SAXS recorded separately first

    # sample = ['Disc3_AuPd_top-3', 'Disc3_AuPd_mid-3', 'Disc3_AuPd_bot-3'] #Change filename
    sample = [
        "Hopper1_AGIB_AuPd_top",
        "Hopper1_AGIB_AuPd_mid",
        "Hopper1_AGIB_AuPd_bot",
    ]  # Change filename
    # y_list  = [-6.06, -6.04, -6.02] #hexapod is in mm
    # y_list  = [-10320, -10300, -10280]  #SmarAct is um
    y_list = [-9540, -9520, -9500]  # SmarAct is um

    assert len(y_list) == len(
        sample
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"

    # Detectors, motors:
    # dets = [pil1M, rayonix, pil300KW]
    dets0 = [pil1M]
    dets = [pil300KW]
    det_exposure_time(t, t)

    pil_pos_x = [-0.4997, -0.4997 + 4.3, -0.4997 + 4.3, -0.4997]
    pil_pos_y = [-59.9987, -59.9987, -59.9987 + 4.3, -59.9987]

    waxs_po = np.linspace(20.95, 2.95, 4)

    for sam, y in zip(sample, y_list):
        # yield from bps.mv(stage.y, y) #hexapod
        yield from bps.mv(piezo.y, y)  # SmarAct
        yield from bps.mv(waxs, 70)
        for angle in range(-90, 91, 1):
            yield from bps.mv(prs, angle)

            name_fmt = "{sam}_phi{angle}deg"
            sample_name = name_fmt.format(sam=sam, angle=angle)
            sample_id(user_name="MK", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets0, num=1)

    yield from bps.mv(att1_5, "Insert")
    yield from bps.sleep(1)
    yield from bps.mv(att1_6, "Insert")
    yield from bps.sleep(1)
    for sam, y in zip(sample, y_list):
        # yield from bps.mv(stage.y, y) #hexapod
        yield from bps.mv(piezo.y, y)  # SmarAct
        for i, waxs_pos in enumerate(waxs_po):
            yield from bps.mv(waxs, waxs_pos)
            yield from bps.mv(pil1m_pos.x, pil_pos_x[i])
            yield from bps.mv(pil1m_pos.y, pil_pos_y[i])

            for angle in range(-90, 91, 1):
                yield from bps.mv(prs, angle)

                name_fmt = "{sam}_phi{angle}deg_{waxs_pos}deg"
                sample_name = name_fmt.format(sam=sam, angle=angle, waxs_pos=waxs_pos)
                sample_id(user_name="MK", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)

    yield from bps.mv(att1_5, "Retract")
    yield from bps.sleep(1)
    yield from bps.mv(att1_6, "Retract")
    yield from bps.sleep(1)

    yield from bps.mv(pil1m_pos.x, -0.4997)
    yield from bps.mv(pil1m_pos.y, -59.9987)

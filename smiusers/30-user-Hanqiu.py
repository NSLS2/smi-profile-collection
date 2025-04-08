def run_waxs_Hanqiu(t=1):
    x_list = [8050, 8400, -11100, -12000, -23400]  #
    y_list = [30, 70, -300, -270, -350]
    # Detectors, motors:
    dets = [pil300KW, xbpm3.sumY]
    det_exposure_time(t)
    e_list = [2470, 2485, 2500]
    waxs_arc = [3, 39, 7]  # [2.64, 8.64, 2]
    samples = ["Cell48EE_2B", "Cell48EE_2B", "Cell48FF_B", "Cell48FF_B", "BrokenFilm_1"]
    name_fmt = "{sample}_{energ}eV_{ycoord}um"
    #
    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    for x, s, y in zip(x_list, samples, y_list):
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(piezo.y, y)
        for i_e, e in enumerate(e_list):
            yield from bps.mv(energy, e)
            sample_name = name_fmt.format(sample=s, energ=e, ycoord=y)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            sample_id(user_name="HJ", sample_name=sample_name)
            yield from bp.scan(dets, waxs, *waxs_arc)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.2)

def run_Sarkar(t=1):
    # run with WAXS
    dets = [pil300KW, pil1M]
    waxs_arc = [0, 6.5, 13, 19.5]

    # x_list  = [43000, 37000, 33000, 28000, 22500,  6500, -2500, -8500, -14500, -22500, -29500, -34500, -40500, -44500]
    # y_list =  [-2000, -2000, -2000, -2000, -1600, -2000, -2400, -2000,  -2000,  -2000,  -2000,  -2000,  -2000,  -2000]
    # samples = ['HSL50', 'HSL2', 'HSL1', 'HSLUK', 'HSL2LAM_Ann', 'HSLS2HEX', 'HSL76', 'HSL109', 'AB_220023', 'OH1', 'OH5_9h', 'PO', 'Furan_PO',
    # 'HSL3LAM']

    x_list = [-42200]
    y_list = [-2400]
    samples = ["kapton_bkg"]

    assert len(x_list) == len(
        y_list
    ), f"Number of X coordinates ({len(x_list)}) is different from number of Y coordinates ({len(y_list)})"
    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"

    for wa in waxs_arc[::-1]:
        yield from bps.mv(waxs, wa)

        for x, y, s in zip(x_list, y_list, samples):
            yield from bps.mv(piezo.x, x)
            yield from bps.mv(piezo.y, y)
            yield from bps.sleep(2)

            det_exposure_time(t, t)
            name_fmt = "{sample}_wa{wax}_sdd8.3m_16.1keV"
            sample_name = name_fmt.format(sample=s, wax="%2.2d" % wa)
            sample_id(user_name="AS", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)
            sample_id(user_name="test", sample_name="test")
            det_exposure_time(0.3, 0.3)

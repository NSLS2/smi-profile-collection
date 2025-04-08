# Bolmatov, 9-Nov-2018


def run_saxs_capsRPI(t=1):
    x_list = [-18.9, -14.16, -8.8, -4.2, 0.08, 6.13, 11.6, 18.4]  #
    # Detectors, motors:
    dets = [pil300KW]
    waxs_arc = [2.94, 8.94, 2]  # [2.64, 8.64, 2]
    samples = [
        "LCF-FILM-1",
        "LCF-FILM-2",
        "LCF-FILM-3",
        "LCF-FILM-4",
        "LCF-FILM-5",
        "LCF-FILM-6",
        "LCF-FILM-7",
        "LCF-FILM-8",
    ]
    #    param   = '16.1keV'
    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    det_exposure_time(t)
    for x, sample in zip(x_list, samples):
        yield from bps.mv(stage.x, x)
        sample_id(user_name=sample, sample_name="")
        yield from escan(dets, waxs, *waxs_arc)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5)


def run_saxsRPI(t=1):
    name = "LC"
    x_list = [-18.63, -12.2, -5.85, 0.7, 6.9, 12.95]  #
    # Detectors, motors:
    dets = [pil1M]
    y_range = [-3, -6, 11]
    samples = ["LC-O38-6", "LC-O37-6", "LC-O35-7", "LC-O36-6", "LC-O35-6", "LC-O35-8"]
    #    param   = '16.1keV'
    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    det_exposure_time(t)
    for x, sample in zip(x_list, samples):
        yield from bps.mv(stage.x, x)
        sample_id(user_name=name, sample_name=sample)
        yield from escan(dets, stage.y, *y_range)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5)


def run_saxs_caps_temp_Bolm(name="DB"):
    # Slowest cycle:
    temperatures = [30, 40, 55]
    x_list = [
        -44280,
        -37950,
        -31595,
        -25200,
        -18800,
        -12550,
        -6100,
        225,
        6580,
        13000,
        19300,
        25700,
        32045,
        38390,
    ]
    e_list = [13450, 13475, 13520]
    # Detectors, motors:
    dets = [pil1M, rayonix, pil300KW, ls.ch1_read, xbpm3.sumY]
    y_range = [-2700, -6000, 30]
    waxs_arc = [3, 17, 2]
    samples = [
        "Br",
        "A0",
        "A1",
        "A2",
        "A3",
        "B0",
        "B1",
        "B2",
        "B3",
        "C0",
        "C1",
        "C2",
        "C3",
        "water",
    ]
    name_fmt = "{sample}_{energ}eV_{temperature}C"
    #    param   = '16.1keV'
    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    det_exposure_time(10)
    for i_t, t in enumerate(temperatures):
        yield from bps.mv(ls.ch1_sp, t)
        if i_t > 0:
            yield from bps.sleep(2400)
        for x, s in zip(x_list, samples):
            temp = ls.ch1_read.value
            yield from bps.mv(piezo.x, x)
            for i_e, e in enumerate(e_list):
                yield from bps.mv(energy, e)
                sample_name = name_fmt.format(sample=s, temperature=temp, energ=e)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                sample_id(user_name=name, sample_name=sample_name)
                yield from bp.grid_scan(dets, waxs, *waxs_arc, piezo.y, *y_range, 0)
    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5)
    yield from bps.mv(ls.ch1_sp, 28)


def test_en(en):
    yield from bps.mv(energy, en)

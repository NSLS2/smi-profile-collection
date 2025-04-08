# Aligam GiSAXS sample
#


def run_saxs_SChan(t=1):
    name = "SC_"
    x_list = [20800, 5800, -7700, -22700]  #
    # Detectors, motors:
    dets = [pil1M, pil300KW, rayonix]
    y_range = [-500, 500, 11]  # [2.64, 8.64, 2]
    x_range = [-500, 500, 6]
    samples = ["nPS_97k", "SC1-11_WD", "SC1-12_PS", "SC1-13_CS"]
    #    param   = '16.1keV'
    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    det_exposure_time(t)
    yield from bps.mv(piezo.z, 5000)
    for x, sample in zip(x_list, samples):
        yield from bps.mv(piezo.x, x)
        sample_id(user_name=name, sample_name=sample)
        yield from bp.rel_scan(dets, piezo.y, *y_range)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(1)


def run_saxs_kraus_1(t=1):
    name = "AAK"
    x_list = [41000, 30000, 20400, 6650, -6750]  #
    y_list = [-2500, -500, -3500, -2000, -1000]
    # Detectors, motors:
    dets = [pil1M, pil300KW, rayonix]
    y_range = [
        [-4000, 4000, 161],
        [-3500, 3500, 141],
        [-3000, 3000, 121],
        [-3000, 3000, 121],
        [-3000, 3000, 121],
    ]
    x_range = [
        [-4000, 4000, 33],
        [-3500, 3500, 29],
        [-3000, 3000, 25],
        [-3000, 3000, 25],
        [-3000, 3000, 25],
    ]  # [2.64, 8.64, 2]
    samples = [
        "67-N_0p05",
        "76-4core_0p05",
        "76-6core_0p05",
        "76-8core_0p05",
        "76-10core_0p05",
    ]
    #    param   = '16.1keV'
    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    det_exposure_time(t)
    yield from bps.mv(piezo.z, 5000)
    for x, y, sample, x_range, y_range in zip(
        x_list, y_list, samples, x_range, y_range
    ):
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(piezo.y, y)
        sample_id(user_name=name, sample_name=sample)
        yield from bp.rel_grid_scan(dets, piezo.y, *y_range, piezo.x, *x_range, 0)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5)


def run_saxs_kraus_2(t=1):
    name = "AAK"
    x_list = [21450, 6450, -7950, -23950, -39350]  #
    y_list = [-2500, -1500, -3500, -6500, -4000]
    # Detectors, motors:
    dets = [pil1M, pil300KW, rayonix]
    y_range = [
        [-2500, 2500, 101],
        [-2500, 2500, 101],
        [-2500, 2500, 101],
        [-2500, 2500, 101],
        [-2500, 2500, 67],
    ]
    x_range = [
        [-2500, 2500, 21],
        [-2500, 2500, 21],
        [-2500, 2500, 21],
        [-2500, 2500, 21],
        [-2500, 2500, 21],
    ]  # [2.64, 8.64, 2]
    samples = [
        "76-8core_0p025_c",
        "76-6core_0p025_c",
        "76-4core_0p025_c",
        "67-N_0p025_c",
        "76-10core_0p15",
    ]
    #    param   = '16.1keV'
    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    det_exposure_time(t)
    yield from bps.mv(piezo.z, 5000)
    for x, y, sample, x_range, y_range in zip(
        x_list, y_list, samples, x_range, y_range
    ):
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(piezo.y, y)
        sample_id(user_name=name, sample_name=sample)
        yield from bp.rel_grid_scan(dets, piezo.y, *y_range, piezo.x, *x_range, 0)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5)


def run_saxs_kraus_3(t=1):
    name = "AAK"
    x_list = [40600, 24200, 10600, -4600, -14200, -25800, -35800]  #
    y_list = [-4000, -3500, -4500, -4500, -3500, -4500, -4500]
    # Detectors, motors:
    dets = [pil1M, pil300KW, rayonix]
    y_range = [
        [-2500, 2500, 67],
        [-2500, 2500, 67],
        [-2000, 2000, 54],
        [-2000, 2000, 54],
        [-2500, 2500, 51],
        [-2000, 2000, 41],
        [-2000, 2000, 41],
    ]
    x_range = [
        [-2500, 2500, 21],
        [-2500, 2500, 21],
        [-2000, 2000, 17],
        [-2000, 2000, 17],
        [-2500, 2500, 21],
        [-2000, 2000, 17],
        [-2000, 2000, 17],
    ]  # [2.64, 8.64, 2]
    samples = [
        "76-8core_0p15",
        "76-6core_0p15",
        "76-4core_0p15",
        "67-N_0p15",
        "76-10core_0p25",
        "76-8core_0p25",
        "76-6core_0p25",
    ]
    #    param   = '16.1keV'
    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    det_exposure_time(t)
    yield from bps.mv(piezo.z, 5000)
    for x, y, sample, x_range, y_range in zip(
        x_list, y_list, samples, x_range, y_range
    ):
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(piezo.y, y)
        sample_id(user_name=name, sample_name=sample)
        yield from bp.rel_grid_scan(dets, piezo.y, *y_range, piezo.x, *x_range, 0)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5)


def run_saxs_kraus_4(t=1):
    name = "AAK"
    x_list = [41800, 30500, 17100, 1400, -17300, -38600]  #
    y_list = [3000, 3500, 1500, 1500, 3000, 3000]
    # Detectors, motors:
    dets = [pil1M, pil300KW, rayonix]
    y_range = [
        [-2500, 2500, 51],
        [-2500, 2500, 51],
        [-2500, 2500, 51],
        [-2500, 2500, 51],
        [-2500, 2500, 51],
        [-2500, 2500, 51],
    ]
    x_range = [
        [-2500, 2500, 21],
        [-2500, 2500, 21],
        [-2500, 2500, 21],
        [-2500, 2500, 21],
        [-2500, 2500, 21],
        [-2500, 2500, 21],
    ]  # [2.64, 8.64, 2]
    samples = [
        "76-4core_0p25",
        "67-N_0p25",
        "76-10core_0p50",
        "76-8core_0p50",
        "76-6core_0p50",
        "76-4core_0p50",
    ]
    #    param   = '16.1keV'
    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    det_exposure_time(t)
    yield from bps.mv(piezo.z, 5000)
    for x, y, sample, x_range, y_range in zip(
        x_list, y_list, samples, x_range, y_range
    ):
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(piezo.y, y)
        sample_id(user_name=name, sample_name=sample)
        yield from bp.rel_grid_scan(dets, piezo.y, *y_range, piezo.x, *x_range, 0)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5)


def run_saxs_kraus_5(t=1):
    name = "AAK"
    x_list = [40700, 27900, 8600, -9500, -27400, -42800]  #
    y_list = [4000, 4000, 4000, 5000, 4000, 4000]
    # Detectors, motors:
    dets = [pil1M, pil300KW, rayonix]
    y_range = [
        [-3500, 3500, 71],
        [-3500, 3500, 11],
        [-3500, 3500, 11],
        [-3500, 3500, 11],
        [-3500, 3500, 11],
        [-3500, 3500, 11],
    ]
    x_range = [
        [-3500, 3500, 29],
        [-3500, 3500, 11],
        [-3500, 3500, 11],
        [-3500, 3500, 11],
        [-3500, 3500, 11],
        [-3500, 3500, 11],
    ]  # [2.64, 8.64, 2]
    samples = [
        "67-N_0p5",
        "76-10core_tkp",
        "76-8core_tkp",
        "76-6core_tkp",
        "76-4core_tkp",
        "67-N_tkp",
    ]
    #    param   = '16.1keV'
    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    det_exposure_time(t)
    yield from bps.mv(piezo.z, 5000)
    for x, y, sample, x_range, y_range in zip(
        x_list, y_list, samples, x_range, y_range
    ):
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(piezo.y, y)
        sample_id(user_name=name, sample_name=sample)
        yield from bp.rel_grid_scan(dets, piezo.y, *y_range, piezo.x, *x_range, 0)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5)


def run_saxs_kraus_RZA(t=1):
    name = "AAK"
    x_list = [800, -17800]  #
    y_list = [-5500, 4500]
    # Detectors, motors:
    dets = [pil1M, pil300KW, rayonix]
    y_range = [[1000, 2000, 14], [-4500, 4500, 121]]
    x_range = [[-8000, 8000, 65], [-7000, 7000, 57]]  # [2.64, 8.64, 2]
    samples = ["08-12core_Akron_top", "08-12core_Akron_bottom"]
    #    param   = '16.1keV'
    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    det_exposure_time(t)
    yield from bps.mv(piezo.z, 5000)
    for x, y, sample, x_range, y_range in zip(
        x_list, y_list, samples, x_range, y_range
    ):
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(piezo.y, y)
        sample_id(user_name=name, sample_name=sample)
        yield from bp.rel_grid_scan(dets, piezo.y, *y_range, piezo.x, *x_range, 0)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5)


def run_saxs_kraus_RZA2(t=1):
    name = "AAK"
    x_list = [-36400, 32800, 17000]  #
    y_list = [500, -500, -500]
    # Detectors, motors:
    dets = [pil1M, pil300KW, rayonix]
    y_range = [[-2000, 2000, 4], [-5000, 5000, 81], [-5000, 5000, 21]]
    x_range = [
        [-2000, 2000, 4],
        [-5000, 5000, 41],
        [-5000, 5000, 41],
    ]  # [2.64, 8.64, 2]
    samples = ["2thickKapton", "35-11core_0p0007_dps", "35-11core_0p02_dps"]
    #    param   = '16.1keV'
    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    det_exposure_time(t)
    yield from bps.mv(piezo.z, 5000)
    for x, y, sample, x_range, y_range in zip(
        x_list, y_list, samples, x_range, y_range
    ):
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(piezo.y, y)
        sample_id(user_name=name, sample_name=sample)
        yield from bp.rel_grid_scan(dets, piezo.y, *y_range, piezo.x, *x_range, 0)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5)


def run_saxs_kraus_micro(t=0.5):
    name = "AAK"
    x_list = [40370, 19170, 4270, -13630]  #
    y_list = [-3500, -3000, -3000, -4500]
    # Detectors, motors:
    dets = [pil1M, pil300KW, rayonix]
    y_range = [[-225, 225, 151], [-225, 225, 151], [-225, 225, 151], [-225, 225, 151]]
    x_range = [
        [-750, 750, 41],
        [-750, 750, 41],
        [-750, 750, 41],
        [-750, 750, 41],
    ]  # [2.64, 8.64, 2]
    samples = ["76-10core_0p025", "76-10core_0p05", "76-10core_0p25", "76-6core_0p025"]
    #    param   = '16.1keV'
    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    det_exposure_time(t)
    yield from bps.mv(piezo.z, 5000)
    for x, y, sample, x_range, y_range in zip(
        x_list, y_list, samples, x_range, y_range
    ):
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(piezo.y, y)
        sample_id(user_name=name, sample_name=sample)
        yield from bp.rel_grid_scan(dets, piezo.y, *y_range, piezo.x, *x_range, 0)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5)


def run_saxs_kraus_micro2(t=0.5):
    name = "AAK"
    x_list = [4270, -30230, -13630]  #
    y_list = [-3000, 2000, -4500]
    # Detectors, motors:
    dets = [pil1M, pil300KW, rayonix]
    y_range = [[-225, 225, 151], [-225, 225, 151], [-225, 225, 151]]
    x_range = [[-750, 750, 41], [-750, 750, 41], [-750, 750, 41]]  # [2.64, 8.64, 2]
    samples = ["76-10core_0p25", "76-8core_0p25", "76-6core_0p025"]
    #    param   = '16.1keV'
    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    det_exposure_time(t)
    yield from bps.mv(piezo.z, 5000)
    for x, y, sample, x_range, y_range in zip(
        x_list, y_list, samples, x_range, y_range
    ):
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(piezo.y, y)
        sample_id(user_name=name, sample_name=sample)
        yield from bp.rel_grid_scan(dets, piezo.y, *y_range, piezo.x, *x_range, 0)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5)


def run_waxsRPI(t=1):
    name = "SP"
    x_list = [4000, 4500, 12000, 18000]  #
    # Detectors, motors:
    dets = [pil300KW]
    y_range = [0, 0, 1]
    waxs_arc = [2.85, 44.85, 8]
    samples = [
        "NPS-Cu_1_Shift",
        "NPS-Cu_2_Shift",
        "NPS-Cu_160c_1_Shift",
        "NPS-Cu_160c_2_Shift",
    ]
    #    param   = '16.1keV'
    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    det_exposure_time(t)
    for x, sample in zip(x_list, samples):
        yield from bps.mv(piezo.x, x)
        sample_id(user_name=name, sample_name=sample)
        yield from bp.scan(dets, waxs, *waxs_arc)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5)


def linkam_fast(n=6):
    yield from bps.mv(attn_shutter, "Retract")
    yield from bp.scan([pil1M], stage.y, 0.1, 0.9, n)
    yield from bps.mv(attn_shutter, "Insert")

import sys
import time


det = [pil1M, pdcurrent, pdcurrent1, pdcurrent2]


def bu(user_name, start_y, end_y, acq_t=2, meas_t=2):
    for i, y_val in enumerate(range(start_y, end_y + 1, 50)):
        yield from bps.mv(piezo.y, y_val)
        name_fmt = "nb{i}_pd_{pd}"
        det_exposure_time(acq_t, meas_t)

        yield from bps.mv(att1_9.open_cmd, 1)
        yield from bps.mv(att1_10.open_cmd, 1)

        fs.open()
        yield from bps.sleep(0.3)
        pd_curr = pdcurrent2.value
        fs.close()

        yield from bps.mv(att1_9.close_cmd, 1)
        yield from bps.mv(att1_10.close_cmd, 1)

        yield from bps.sleep(1)

        sample_name = name_fmt.format(i="%2.2d" % (1 + i), pd="%5.5d" % pd_curr)
        sample_id(user_name=user_name, sample_name=sample_name)

        print(f"\n\t=== Sample:{user_name}_{sample_name} ===\n")

        yield from bp.count(det, num=1)


def run_bu_2022_2(name="test", t=1):
    """
    SAXS grid scan on sample with 9 different positions

    """
    user = "GVD"

    # Nanopositioners relative ranges in um
    x_range = [0, 600, 3]
    y_range = [0, 300, 3]

    dets = [pil1M]
    det_exposure_time(t, t)

    # Metadata
    e = energy.position.energy / 1000
    sdd = pil1m_pos.z.position / 1000
    scan_id = db[-1].start["scan_id"] + 1

    # Sample filename
    name_fmt = "{sample}_{energy}keV_sdd{sdd}m_id{scan_id}"
    sample_name = name_fmt.format(
        sample=name, energy="%.2f" % e, sdd="%.1f" % sdd, scan_id=scan_id
    )
    sample_id(user_name=user, sample_name=sample_name)

    # Take measurement
    print(f"\n\t=== Sample: {sample_name} ===\n")
    yield from bp.rel_grid_scan(dets, piezo.x, *x_range, piezo.y, *y_range, 0)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def run_background_bu_2022_2(name="test", t=1):
    """
    SAXS background around the sample

    """
    user = "GVD"
    name = name + "-bkg"

    dets = [pil1M]
    det_exposure_time(t, t)

    # Metadata
    e = energy.position.energy / 1000
    sdd = pil1m_pos.z.position / 1000
    scan_id = db[-1].start["scan_id"] + 1

    # Sample filename
    name_fmt = "{sample}_{energy}keV_sdd{sdd}m_id{scan_id}"
    sample_name = name_fmt.format(
        sample=name, energy="%.2f" % e, sdd="%.1f" % sdd, scan_id=scan_id
    )
    sample_id(user_name=user, sample_name=sample_name)

    # Take measurement
    print(f"\n\t=== Sample: {sample_name} ===\n")
    yield from bp.count(dets)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)

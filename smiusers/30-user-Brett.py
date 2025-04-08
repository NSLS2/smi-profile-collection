def NEXAFS_S_edge(t=0.5):
    yield from bps.mv(waxs, 60)
    dets = [pil300KW]
    name = "NEXAFS_CdSe-CdS-NR-HT-BA-30s"

    energies = np.linspace(2440, 2510, 71)

    det_exposure_time(t, t)
    name_fmt = "{sample}_{energy}eV_xbpm{xbpm}"
    for e in energies:
        yield from bps.mv(energy, e)
        sample_name = name_fmt.format(
            sample=name, energy=e, xbpm="%3.1f" % xbpm3.sumY.value
        )
        sample_id(user_name="CB", sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")
        yield from bp.count(dets, num=1)

    yield from bps.mv(energy, 2480)
    yield from bps.mv(energy, 2470)
    yield from bps.mv(energy, 2450)


def NEXAFS_Ag_edge(t=0.5):
    yield from bps.mv(waxs, 60)
    dets = [pil300KW]
    name = "NEXAFSAgL2_sleeptime_P3HT_ag1nm"

    energies = np.linspace(3480, 3580, 101)

    det_exposure_time(t, t)
    name_fmt = "{sample}_{energy}eV_xbpm{xbpm}"
    for e in energies:
        yield from bps.mv(energy, e)
        yield from bps.sleep(2)
        sample_name = name_fmt.format(
            sample=name, energy=e, xbpm="%3.1f" % xbpm3.sumY.value
        )
        sample_id(user_name="CB", sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")
        yield from bp.count(dets, num=1)

    yield from bps.mv(energy, 3580)
    yield from bps.mv(energy, 3560)
    yield from bps.mv(energy, 3530)


def NEXAFS_Cd_edge(t=0.5):
    yield from bps.mv(waxs, 60)
    dets = [pil300KW]
    name = "NEXAFS_Cd_powder_test"

    energies = np.linspace(3500, 3600, 51)

    det_exposure_time(t, t)
    name_fmt = "{sample}_{energy}eV_xbpm{xbpm}"
    for e in energies:
        yield from bps.mv(energy, e)
        sample_name = name_fmt.format(
            sample=name, energy=e, xbpm="%3.1f" % xbpm3.sumY.value
        )
        sample_id(user_name="CB", sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")
        yield from bp.count(dets, num=1)

    yield from bps.mv(energy, 3580)
    yield from bps.mv(energy, 3560)
    yield from bps.mv(energy, 3530)


def time_resolved_S_edge(t=0.1, t1=10):
    dets = [pil300KW, pil1M]
    name = "P3HT-tr10s-UVon2_ai0.6"
    e = "2490.0"

    det_exposure_time(t, t1)
    name_fmt = "{sample}_{energy}eV_bpm{xbpm}"
    sample_name = name_fmt.format(
        sample=name, energy=e, xbpm="%3.1f" % xbpm3.sumY.value
    )
    sample_id(user_name="CB", sample_name=sample_name)
    print(f"\n\t=== Sample: {sample_name} ===\n")

    yield from bp.count(dets, num=1)


def fly_scan_prsx(det, motor, t=0.1, t1=30, name="test"):

    sample_id(user_name="CB", sample_name=name)

    start = piezo.x.position
    stop = piezo.x.position + 3000

    yield from bps.mv(motor, start)
    pil1M.stage()
    pil300KW.stage()

    det_exposure_time(t, t1)

    print(f"Acquire time before staging: {t}")
    st = pil1M.trigger()
    st1 = pil300KW.trigger()

    yield from list_scan([], motor, [start, stop])
    while not st.done or not st1.done:
        pass

    pil1M.unstage()
    pil300KW.unstage()
    print(f"We are done after {t1}s of waiting")
    # yield from bps.mv(attn_shutter, 'Insert')


def giwaxs_S_edge_calvin(t=1):
    dets = [pil300KW, pil1M]

    name = "SAXS_WAXS_CdSe-CdS-NR-HT-BA-30s"
    energies = [2460, 2475, 2476, 2490, 2510]

    xs = piezo.x.position
    xss = np.linspace(xs, xs + 1200, 5)

    det_exposure_time(t, t)
    name_fmt = "{sample}_{energy}eV_bpm{xbpm}"
    for e, xsss in zip(energies, xss):
        yield from bps.mv(energy, e)
        yield from bps.sleep(2)

        yield from bps.mv(piezo.x, xsss)
        bpm = xbpm3.sumX.value

        sample_name = name_fmt.format(
            sample=name, energy="%6.2f" % e, xbpm="%4.3f" % bpm
        )
        sample_id(user_name="CB", sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")
        yield from bp.count(dets, num=1)

    yield from bps.mv(energy, 2475)
    yield from bps.mv(energy, 2460)


def giwaxs_Ag_edge_calvin(t=1):
    dets = [pil300KW, pil1M]

    name = "SAXS_WAXS_P3HT_1nmA_2"
    energies = [3350, 3357, 3358, 3365]

    xs = piezo.x.position
    xss = np.linspace(xs, xs + 1200, 4)

    det_exposure_time(t, t)
    name_fmt = "{sample}_{energy}eV_bpm{xbpm}"
    for e, xsss in zip(energies, xss):
        yield from bps.mv(energy, e)
        yield from bps.sleep(2)

        yield from bps.mv(piezo.x, xsss)
        bpm = xbpm3.sumX.value

        sample_name = name_fmt.format(
            sample=name, energy="%6.2f" % e, xbpm="%4.3f" % bpm
        )
        sample_id(user_name="CB", sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")
        yield from bp.count(dets, num=1)

    yield from bps.mv(energy, 3400)
    yield from bps.mv(energy, 3430)
    yield from bps.mv(energy, 3460)
    yield from bps.mv(energy, 3500)
    yield from bps.mv(energy, 3530)


def single_giwaxs(t=1, name="test"):
    dets = [pil300KW, pil1M]

    det_exposure_time(t, t)

    sample_id(user_name="CB", sample_name=name)
    print(f"\n\t=== Sample: {name} ===\n")
    yield from bp.count(dets, num=1)


name_tot = "InP_HT1_1x28s_2x0s"


def night_shift_1():
    name = "GISAXS_" + name_tot + "_UV0s" + "_2450eV"
    yield from bps.mvr(piezo.th, -0.6)

    yield from alignement_gisaxs(0.4)

    yield from bps.mvr(piezo.x, 300)
    yield from bps.mvr(piezo.th, 0.6)

    yield from single_giwaxs(name=name)


def night_shift_2():
    name = name_tot + "_2450eV"
    yield from bps.mvr(piezo.x, 300)

    t0 = time.time()
    yield from fly_scan_prsx([pil1M, pil300KW], piezo.x, 0.1, 10, name=name)

    t1 = time.time()
    i = 0
    while t1 - t0 < 600:
        if (t1 - t0) // 60 != i:
            yield from bps.mvr(piezo.x, 300)
            i = (t1 - t0) // 60

            name = name_tot + "_2450eV" + "%smin" % i
            yield from single_giwaxs(name=name)

        yield from bps.sleep(1)
        t1 = time.time()


def night_shift_3():
    name = "GISAXS_" + name_tot + "_UVexpo" + "_2450eV"

    yield from bps.mvr(piezo.x, 300)
    yield from single_giwaxs(name=name)

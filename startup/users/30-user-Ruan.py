def NEXAFS_S_edge(t=0.5):
    yield from bps.mv(waxs, 60)

    dets = [pil300KW]
    name = "17_Phil_pk61_buffer_NEXAFS_3rd"
    # x = [8800]

    energies = np.linspace(2450, 2500, 51)

    # for name, x in zip(names, x):
    # bps.mv(piezo.x, x)
    det_exposure_time(t, t)
    name_fmt = "{sample}_{energy}eV_xbpm{xbpm}"
    for e in energies:
        yield from bps.mv(energy, e)
        sample_name = name_fmt.format(
            sample=name, energy=e, xbpm="%3.1f" % xbpm3.sumY.value
        )
        sample_id(user_name="ZR", sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")
        yield from bp.count(dets, num=1)
        yield from bps.sleep(2)

    yield from bps.mv(energy, 2470)
    yield from bps.sleep(10)


def NEXAFS_Cl_edge(t=0.5):
    yield from bps.mv(waxs, 60)

    dets = [pil300KW]
    name = "7_Le_13_Cl_saxs_solution"
    # x = [8800]

    energies = np.linspace(2800, 2850, 51)

    # for name, x in zip(names, x):
    # bps.mv(piezo.x, x)
    det_exposure_time(t, t)
    name_fmt = "{sample}_{energy}eV_xbpm{xbpm}"
    for e in energies:
        yield from bps.mv(energy, e)
        sample_name = name_fmt.format(
            sample=name, energy=e, xbpm="%3.1f" % xbpm3.sumY.value
        )
        sample_id(user_name="ZR", sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")
        yield from bp.count(dets, num=1)
        yield from bps.sleep(2)

    yield from bps.mv(energy, 2800)
    yield from bps.sleep(10)


def SAXS_Cl_edge(t=1):
    dets = [pil300KW, pil1M]
    name = "7_Le_13_Cl_saxs_solution"
    energies = [2810, 2820, 2826, 2827, 2829, 2832, 2850]
    # energies = [2470]

    det_exposure_time(t, t)
    name_fmt = "{sample}_{energy}eV_xbpm{xbpm}_wa{wa}"
    wa = [0.0, 6.5, 13.0]

    # y0 = piezo.y.position
    # ys = np.linspace(y0, y0+750, 6)

    for wax in wa:
        yield from bps.mv(waxs, wax)
        for k, e in enumerate(energies):
            yield from bps.mv(energy, e)
            # yield from bps.mv(piezo.y, yss)

            sample_name = name_fmt.format(
                sample=name, energy=e, xbpm="%3.1f" % xbpm3.sumY.value, wa="%2.1f" % wax
            )
            sample_id(user_name="OS", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)

        yield from bps.mv(energy, 2810)

    # yield from bps.mvr(piezo.y, 150)
    for wax in wa:
        yield from bps.mv(waxs, wax)

        name_fmt = "{sample}_2810eV_postmeas_xbpm{xbpm}_wa{wa}"
        sample_name = name_fmt.format(
            sample=name, xbpm="%3.1f" % xbpm3.sumY.value, wa="%2.1f" % wax
        )
        sample_id(user_name="OS", sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")
        yield from bp.count(dets, num=1)

    sample_id(user_name="test", sample_name="test")


def NEXAFS_Br_edge(t=0.5):
    yield from bps.mv(waxs, 60)

    dets = [pil300KW]
    name = "1_Le_15_Br_nexafs_solution"
    # x = [8800]

    energies = np.linspace(13450, 13500, 51)

    # for name, x in zip(names, x):
    # bps.mv(piezo.x, x)
    det_exposure_time(t, t)
    name_fmt = "{sample}_{energy}eV_xbpm{xbpm}"
    for e in energies:
        yield from bps.mv(energy, e)
        sample_name = name_fmt.format(
            sample=name, energy=e, xbpm="%3.1f" % xbpm3.sumY.value
        )
        sample_id(user_name="ZR", sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")
        yield from bp.count(dets, num=1)
        yield from bps.sleep(2)

    yield from bps.mv(energy, 13450)
    yield from bps.sleep(10)


def SAXS_Br_edge(t=1):
    dets = [pil300KW, pil1M]
    name = "5_Le_15_Br_saxs"
    energies = [13450, 13465, 13469, 13471, 13478, 13500]
    # energies = [13450]

    det_exposure_time(t, t)
    name_fmt = "{sample}_{energy}eV_xbpm{xbpm}_wa{wa}"
    wa = [0.0, 6.5, 13.0]

    # y0 = piezo.y.position
    # ys = np.linspace(y0, y0+750, 6)

    for wax in wa:
        yield from bps.mv(waxs, wax)
        for k, e in enumerate(energies):
            yield from bps.mv(energy, e)
            # yield from bps.mv(piezo.y, yss)

            sample_name = name_fmt.format(
                sample=name, energy=e, xbpm="%3.1f" % xbpm3.sumY.value, wa="%2.1f" % wax
            )
            sample_id(user_name="OS", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)

        yield from bps.mv(energy, 13450)

    # yield from bps.mvr(piezo.y, 150)
    for wax in wa:
        yield from bps.mv(waxs, wax)

        name_fmt = "{sample}_13450eV_postmeas_xbpm{xbpm}_wa{wa}"
        sample_name = name_fmt.format(
            sample=name, xbpm="%3.1f" % xbpm3.sumY.value, wa="%2.1f" % wax
        )
        sample_id(user_name="OS", sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")
        yield from bp.count(dets, num=1)

    sample_id(user_name="test", sample_name="test")


def SAXS_s_edge(t=1):
    dets = [pil300KW]
    name = "17_Phil_pk61_buffer_saxs"
    energies = [2470, 2477, 2480, 2482, 2484, 2500]
    # energies = [2470]

    det_exposure_time(t, t)
    name_fmt = "{sample}_{energy}eV_xbpm{xbpm}_wa{wa}"
    wa = [0.0, 6.5, 13.0, 19.5]

    yield from bps.mv(GV7.close_cmd, 1)
    yield from bps.sleep(1)
    yield from bps.mv(GV7.close_cmd, 1)

    y0 = piezo.y.position
    ys = np.linspace(y0, y0 + 750, 6)

    for wax in wa:
        yield from bps.mv(waxs, wax)
        for k, (e, yss) in enumerate(zip(energies, ys)):
            yield from bps.mv(energy, e)
            yield from bps.mv(piezo.y, yss)

            sample_name = name_fmt.format(
                sample=name, energy=e, xbpm="%3.1f" % xbpm3.sumY.value, wa="%2.1f" % wax
            )
            sample_id(user_name="OS", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)

        yield from bps.mv(energy, 2470)

    yield from bps.mvr(piezo.y, 150)
    for wax in wa:
        yield from bps.mv(waxs, wax)

        name_fmt = "{sample}_2470eV_postmeas_xbpm{xbpm}_wa{wa}"
        sample_name = name_fmt.format(
            sample=name, xbpm="%3.1f" % xbpm3.sumY.value, wa="%2.1f" % wax
        )
        sample_id(user_name="OS", sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")
        yield from bp.count(dets, num=1)

    sample_id(user_name="test", sample_name="test")

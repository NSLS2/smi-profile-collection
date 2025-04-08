def nexafs_S_edge(t=1):
    dets = [pil900KW]
    # prs 0 deg
    names = ["BPI_20nm_LCE", "cholesteric_film_20nm"]
    x = [-6000, -17000]
    y = [-4100, -4900]

    energies = (
        np.arange(2445, 2470, 5).tolist()
        + np.arange(2470, 2480, 0.25).tolist()
        + np.arange(2480, 2490, 1).tolist()
        + np.arange(2490, 2501, 5).tolist()
    )
    waxs_arc = [40]

    for name, xs, ys in zip(names, x, y):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)

            det_exposure_time(t, t)
            name_fmt = "nexafs_{sample}_{energy}eV_wa{wax}_bpm{xbpm}"
            for e in energies:

                yield from bps.mv(energy, e)
                yield from bps.sleep(3)

                bpm = xbpm2.sumX.value

                sample_name = name_fmt.format(
                    sample=name, energy="%6.2f" % e, wax=wa, xbpm="%4.3f" % bpm
                )
                sample_id(user_name="GF", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 2470)
            yield from bps.mv(energy, 2450)


def S_edge_SAXSWAXS_2021_3(t=1):
    dets = [pil900KW, pil1M]

    names = ["cholesteric_film_20nm"]  #'BPI_20nm_LCE']#
    x = [-15900]  # , -5900]
    y = [-5000]  # , -5600]

    energies = (
        np.arange(2445, 2470, 5).tolist()
        + np.arange(2470, 2480, 0.25).tolist()
        + np.arange(2480, 2490, 1).tolist()
        + np.arange(2490, 2501, 5).tolist()
    )
    waxs_arc = [0, 20]

    for name, xs, ys in zip(names, x, y):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)

        yss = np.linspace(ys, ys + 200, 20)
        xss = np.array([xs, xs + 200, xs + 400])

        yss, xss = np.meshgrid(yss, xss)
        yss = yss.ravel()
        xss = xss.ravel()

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)

            det_exposure_time(t, t)

            name_fmt = "{sample}_sdd5m_{energy}eV_wa{wax}_bpm{xbpm}"
            for e, xsss, ysss in zip(energies, xss, yss):
                yield from bps.mv(energy, e)
                yield from bps.sleep(2)

                yield from bps.mv(piezo.y, ysss)
                yield from bps.mv(piezo.x, xsss)

                bpm = xbpm2.sumX.value

                sample_name = name_fmt.format(
                    sample=name, energy="%6.2f" % e, wax=wa, xbpm="%4.3f" % bpm
                )
                sample_id(user_name="GF", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")

                yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 2470)
            yield from bps.mv(energy, 2450)


def saxs_S_edge_Hoang_2022_2(t=0.5):
    """
    Cycle 2022_2
    Based on Gregory and modified for GU-310422. SAXS ssd 8.3 m.
    """
    user_name = "JH"

    # x and y are positions on the sample, a and b are different rows
    names_a = [
        "0.7_20OBA",
        "0.6_20OBA",
        "40OBA_main",
        "30OBA_main",
        "20OBA_main",
        "10OBA_main",
        "0OBA_main",
    ]
    x_a = [
        39000,
        29000,
        19000,
        5000,
        -7000,
        -22000,
        -37000,
    ]
    y_a = [
        -6800,
        -6800,
        -6800,
        -6500,
        -6500,
        -6500,
        -6500,
    ]

    names_b = [
        "BPIII",
        "BPII",
        "BPI",
        "BP_Chol",
        "0.9_20OBA",
        "0.8_20OBA",
    ]
    x_b = [
        30750,
        16000,
        1000,
        -10700,
        -21700,
        -37500,
    ]
    y_b = [
        6700,
        6700,
        6700,
        6700,
        6700,
        6200,
    ]

    # Combine sample lists
    names = names_a + names_b
    x = x_a + x_b
    y = y_a + y_b

    # Check and correct sample names just in case
    names = [n.translate({ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ "}) for n in names]

    assert len(x) == len(
        names
    ), f"Number of x coordinates ({len(x)}) is different from number of samples ({len(names)})"
    assert len(x) == len(
        y
    ), f"Number of x coordinates ({len(x)}) is different number of y coordinates ({len(y)})"
    assert len(y) == len(
        names
    ), f"Number of y coordinates ({len(y)}) is different from number of samples ({len(names)})"

    # Move all x and y values if needed
    # x = (np.array(x) + 0).tolist()
    # y = (np.array(y) + 0).tolist()

    # Energies for sulphur K edge
    energies = np.concatenate(
        (
            np.arange(2445, 2470, 5),
            np.arange(2470, 2480, 0.25),
            np.arange(2480, 2490, 1),
            np.arange(2490, 2501, 5),
        )
    )

    waxs_arc = [0, 20]

    for name, xs, ys in zip(names, x, y):
        yield from bps.mv(piezo.x, xs, piezo.y, ys)

        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)
            yield from bps.mv(piezo.x, xs + i * 200)
            # Do not read SAXS if WAXS is in the way
            dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]
            det_exposure_time(t, t)

            # Cover a range of 1.5 mm in y to avoid damage
            yss = np.linspace(ys, ys + 1500, len(energies))

            name_fmt = "{sample}_{energy}eV_wa{wax}_sdd{sdd}m_bpm{xbpm}"
            for e, ysss in zip(energies, yss):
                yield from bps.mv(piezo.y, ysss)
                yield from bps.mv(energy, e)
                yield from bps.sleep(2)

                # Metadata
                bpm = xbpm3.sumX.get()
                sdd = pil1m_pos.z.position / 1000
                # wa = waxs.arc.user_readback.value
                wa = str(np.round(wa, 1)).zfill(4)

                sample_name = name_fmt.format(
                    sample=name,
                    energy="%6.2f" % e,
                    wax=wa,
                    sdd="%.1f" % sdd,
                    xbpm="%4.3f" % bpm,
                )
                sample_id(user_name=user_name, sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")

                yield from bp.count(dets, num=1)

            # Go back gently with energy
            yield from bps.mv(energy, 2480)
            yield from bps.mv(energy, 2450)


def saxs_S_edge_temperature_Hoang_2022_2(t=0.5):
    """
    Cycle 2022_2: heating stage temperature cycle SAXS ssd 8.3 m.
    """
    user_name = "JH"

    # x and y are positions on the sample, a and b are different rows
    names_a = [
        "0_6OBA_main",
        "10_6OBA_main",
        "20_6OBA_main",
        "30_6OBA_main",
        "40_6OBA_main",
        "0.6_20OBA",
        "0.7_20OBA",
    ]
    x_a = [
        45000,
        39500,
        36500,
        31750,
        26750,
        22250,
        18650,
    ]
    y_a = [
        -5000,
        -5100,
        -5500,
        -5000,
        -4500,
        -5000,
        -5000,
    ]

    names_b = [
        "0.8_20OBA",
        "0.8_20OBA_R",
        "0.9_20OBA",
        "BP_chol",
        "BPI",
        "BPII",
        "BPIII",
    ]
    x_b = [
        13500,
        9750,
        5000,
        -750,
        -5750,
        -11750,
        -17750,
    ]
    y_b = [
        -5000,
        -4000,
        -5200,
        -5200,
        -5200,
        -5200,
        -5200,
    ]

    # Combine sample lists
    names = names_a + names_b
    x = x_a + x_b
    y = y_a + y_b

    # Check and correct sample names just in case
    names = [n.translate({ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ "}) for n in names]

    assert len(x) == len(
        names
    ), f"Number of x coordinates ({len(x)}) is different from number of samples ({len(names)})"
    assert len(x) == len(
        y
    ), f"Number of x coordinates ({len(x)}) is different number of y coordinates ({len(y)})"
    assert len(y) == len(
        names
    ), f"Number of y coordinates ({len(y)}) is different from number of samples ({len(names)})"

    # Move all x and y values if needed
    # x = (np.array(x) + 0).tolist()
    # y = (np.array(y) + 0).tolist()

    # Energies for sulphur K edge
    # energies = np.concatenate((np.arange(2445, 2470, 5),
    #                            np.arange(2470, 2480, 0.25),
    #                            np.arange(2480, 2490, 1),
    #                            np.arange(2490, 2501, 5),
    #                            ))
    energies = [2452, 2472, 2476, 2478, 2482, 2500]
    temperatures = np.arange(30, 201, 5)  # in C

    waxs_arc = [0, 2]

    for i_t, temperature in enumerate(temperatures):

        t_kelvin = temperature + 273.15
        print(t_kelvin)
        yield from ls.output1.mv_temp(t_kelvin)

        print("Equalising temp")
        temp = ls.input_A.get()
        while abs(temp - t_kelvin) > 1:
            print(abs(temp - t_kelvin))
            yield from bps.sleep(10)
            temp = ls.input_A.get()

        t_celsius = temp - 273.15
        if t_celsius > 34:
            print("Waiting for 300 s...")
            yield from bps.sleep(300)

        for name, xs, ys in zip(names, x, y):
            yield from bps.mv(piezo.x, xs, piezo.y, ys)

            for i, wa in enumerate(waxs_arc):
                yield from bps.mv(waxs, wa)
                # yield from bps.mv(piezo.x, xs + i * 200)
                # Do not read SAXS if WAXS is in the way
                dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]
                det_exposure_time(t, t)

                # Cover a range of 1.5 mm in y to avoid damage
                yss = np.linspace(ys, ys + 180, len(energies))

                name_fmt = "{sample}_temp{temperature}degC_{energy}eV_wa{wax}_sdd{sdd}m_bpm{xbpm}"
                for e, ysss in zip(energies, yss):
                    yield from bps.mv(piezo.y, ysss)
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)

                    # Metadata
                    bpm = xbpm3.sumX.get()
                    sdd = pil1m_pos.z.position / 1000
                    wa = str(np.round(float(wa), 1)).zfill(4)

                    sample_name = name_fmt.format(
                        sample=name,
                        temperature="%3.1f" % temperature,
                        energy="%6.2f" % e,
                        wax=wa,
                        sdd="%.1f" % sdd,
                        xbpm="%4.3f" % bpm,
                    )
                    sample_id(user_name=user_name, sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")

                    yield from bp.count(dets, num=1)

                # Go back gently with energy
                yield from bps.mv(energy, 2480)
                yield from bps.mv(energy, 2450)

    # End of the scan
    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)
    yield from ls.output1.mv_temp(28 + 273.13)


def tensile_continous_Hoang_2022_2(t=0.5):
    """
    Cycle 2022_2: Tensile stage continous measurements

    Set the energy prior to the measurement
    """

    user_name = "test_30deg"

    # Sample name
    name = "test_30deg"

    ene = 2470
    yield from bps.mv(energy, ene)

    t0 = time.time()
    waxs_arc = [0, 2, 16]
    det_exposure_time(t, t)

    # Check and correct sample names just in case
    name = name.translate({ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ "})

    # Continous measurement
    for i in range(1000):

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)
            # Do not read SAXS if WAXS is in the way
            dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]
            t1 = time.time()

            # Metadata
            step = str(i).zfill(3)
            td = str(np.round(t1 - t0, 1)).zfill(6)
            e = energy.position.energy
            wa = str(np.round(float(wa), 1)).zfill(4)
            sdd = pil1m_pos.z.position / 1000
            bpm = xbpm3.sumX.get()

            # Sample name
            name_fmt = (
                "{sample}_step{step}_time{td}s_{energy}eV_wa{wax}_sdd{sdd}m_bpm{xbpm}"
            )
            sample_name = name_fmt.format(
                sample=name,
                step=step,
                td=td,
                energy="%6.2f" % e,
                wax=wa,
                sdd="%.1f" % sdd,
                xbpm="%4.3f" % bpm,
            )
            sample_id(user_name=user_name, sample_name=sample_name)

            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets)

    # End of the scan
    sample_id(user_name="test_30deg", sample_name="test_30deg")
    det_exposure_time(0.5, 0.5)


def tensile_single_Hoang_2022_2(t0, t=0.5):
    """
    Cycle 2022_2: Tensile stage single measurement

    Scan WAXS over different energies and sample rotations. Make sure to specify
    hexapod stage positions for each sample rotation. Also, make t0 in BlueSky by
    t0 = time.time() at the same time the plan in Linkam software is executed.
    Then start the scan by RE(tensile_single_Hoang_2022_2(t0)). Each file name
    will contain time eplased from t0, so detctor frames can be related to the
    Linkam tensile stage plan.

    Params:
        t0 (float): start time of the tensile plan, from time.time()
        t (float): exposure of the single detector frame and also total acquisition
            time.

    """

    user_name = "JH"

    # Sample name
    name = "BPIII_80strain"

    rotations = [0, 15, 30]
    # rotations = [0]

    # Hexapod sample coordinates for different rotations
    hexa_poistions = {
        0: dict(hexa_x=0.3, hexa_y=0.4, hexa_z=7),
        15: dict(hexa_x=2.25, hexa_y=0.3, hexa_z=7),
        30: dict(hexa_x=4.15, hexa_y=0.5, hexa_z=7),
        # 40 : dict(hexa_x=0, hexa_y=0, hexa_z=7),
    }

    energies = [2470, 2478]
    waxs_arc = [0, 2]
    det_exposure_time(t, t)

    # Check and correct sample names just in case
    name = name.translate({ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ "})

    for rot in rotations:

        # Get hexa position from the position dictionary
        x = hexa_poistions[rot]["hexa_x"]
        y = hexa_poistions[rot]["hexa_y"]
        z = hexa_poistions[rot]["hexa_z"]

        yield from bps.mv(prs, rot, stage.x, x, stage.y, y, stage.z, z)

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)
            # Do not read SAXS if WAXS is in the way
            dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]

            yss = np.linspace(y, y + 0.09, len(energies))  # in mm now

            for e, ysss in zip(energies, yss):
                yield from bps.mv(energy, e)
                yield from bps.mv(stage.y, ysss)
                yield from bps.sleep(2)

                t1 = time.time()

                # Metadata
                rot = str(rot).zfill(2)
                td = str(np.round(t1 - t0, 1)).zfill(6)
                # e = energy.position.energy
                wa = str(np.round(float(wa), 1)).zfill(4)
                sdd = pil1m_pos.z.position / 1000
                bpm = xbpm3.sumX.get()

                # Sample name
                name_fmt = (
                    "{sample}_rot{rot}deg_{td}s_{energy}eV_wa{wax}_sdd{sdd}m_bpm{xbpm}"
                )
                sample_name = name_fmt.format(
                    sample=name,
                    rot=rot,
                    td=td,
                    energy="%6.2f" % e,
                    wax=wa,
                    sdd="%.1f" % sdd,
                    xbpm="%4.3f" % bpm,
                )
                sample_id(user_name=user_name, sample_name=sample_name)

                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets)

            yield from bps.mv(energy, 2475)
            yield from bps.sleep(2)

            # Move energy slowly
            if e == 2500:
                yield from bps.mv(energy, 2490)
                yield from bps.mv(energy, 2480)
                yield from bps.mv(energy, 2470)

    # End of the scan
    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)

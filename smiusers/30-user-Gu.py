def saxs_gu_2022_1(t=1):

    xlocs = [
        33000,
        24000,
        15000,
        6000,
        -3000,
        -12000,
        -21000,
        -30000,
        33000,
        24000,
        15000,
        6000,
        -3000,
        -12000,
        -21000,
        -30000,
    ]
    ylocs = [
        5200,
        6000,
        5500,
        6100,
        5600,
        5600,
        5600,
        4700,
        300,
        300,
        600,
        300,
        100,
        100,
        -200,
        -500,
    ]
    zlocs = [
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
        2700,
    ]
    ystage = [
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
    ]
    names = [
        "samA1",
        "samA2",
        "samA3",
        "samA4",
        "samA5",
        "samA6",
        "samA7",
        "samA8",
        "samB1",
        "samB2",
        "samB3",
        "samB4",
        "samB5",
        "samB6",
        "samB7",
        "samB8",
    ]

    user = "YW"
    det_exposure_time(t, t)

    assert len(xlocs) == len(
        names
    ), f"Number of X coordinates ({len(xlocs)}) is different from number of samples ({len(names)})"
    assert len(xlocs) == len(
        ylocs
    ), f"Number of X coordinates ({len(xlocs)}) is different from number of samples ({len(ylocs)})"
    assert len(xlocs) == len(
        zlocs
    ), f"Number of X coordinates ({len(xlocs)}) is different from number of samples ({len(zlocs)})"
    assert len(xlocs) == len(
        ystage
    ), f"Number of X coordinates ({len(xlocs)}) is different from number of samples ({len(ystage)})"
    assert len(xlocs) == len(
        names
    ), f"Number of X coordinates ({len(xlocs)}) is different from number of samples ({len(names)})"

    # Detectors, motors:
    dets = [pil1M]
    waxs_range = [20]

    for wa in waxs_range:
        yield from bps.mv(waxs, wa)
        for sam, x, y, z, y_sta in zip(names, xlocs, ylocs, zlocs, ystage):
            yield from bps.mv(piezo.x, x)
            yield from bps.mv(piezo.y, y)
            yield from bps.mv(piezo.z, z)
            yield from bps.mv(stage.y, y_sta)

            name_fmt = "{sam}_16.1keV_sdd7.0m_wa{waxs}"
            sample_name = name_fmt.format(sam=sam, waxs="%2.1f" % wa)
            sample_id(user_name=user, sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=10)
            yield from bps.sleep(2)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def temp_2021_3(tim=0.5):
    # Slowest cycle:
    temperatures = [115]

    name = "YW"

    samples = ["Trimethyl_benzene", "Pff4TBT", "Toluene", "PS", "P3DT"]
    x_list = [32200, 22500, 13200, 4200, -9800]
    y_list = [-2900, -3700, -3500, -3700, -3700]

    assert len(x_list) == len(
        y_list
    ), f"Number of X coordinates ({len(x_list)}) is different from number of Y coordinates ({len(y_list)})"
    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"

    # Detectors, motors:
    dets = [pil1M]  # ALL detectors

    waxs_arc = [20]
    name_fmt = "{sample}_16.1keV_4.0m_{temperature}C_wa{waxs}"

    det_exposure_time(tim, tim)
    for i_t, t in enumerate(temperatures):
        t_kelvin = t + 273.15
        yield from ls.output1.mv_temp(t_kelvin)
        temp = ls.input_A.get()

        while abs(temp - t_kelvin) > 2.5:
            print(abs(temp - t_kelvin))
            yield from bps.sleep(10)
            temp = ls.input_A.get()

        if i_t != 0:
            yield from bps.sleep(300)

        # temp = ls.input_A.get()
        t_celsius = temp - 273.15

        for j, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)
            for x, y, s in zip(x_list, y_list, samples):
                yield from bps.mv(piezo.x, x)
                yield from bps.mv(piezo.y, y)

                sample_name = name_fmt.format(
                    sample=s, temperature="%3.1f" % t_celsius, waxs="%2.1f" % wa
                )
                yield from bps.mv(piezo.x, x)
                yield from bps.mv(piezo.y, y)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                sample_id(user_name=name, sample_name=sample_name)
                yield from bp.count(dets, num=1)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)

    t_kelvin = 25 + 273.15
    yield from ls.output1.mv_temp(t_kelvin)


def gu_nexafs_S_2021_3(t=1):
    dets = [pil900KW]

    # energies = np.arange(2445, 2470, 5).tolist() + np.arange(2470, 2480, 0.25).tolist() + np.arange(2480, 2490, 1).tolist()+ np.arange(2490, 2501, 5).tolist()
    energies = 2 + np.asarray(
        np.arange(2445, 2470, 5).tolist()
        + np.arange(2470, 2480, 0.25).tolist()
        + np.arange(2480, 2490, 1).tolist()
        + np.arange(2490, 2501, 5).tolist()
    )

    waxs_arc = np.linspace(40, 40, 1)

    # names=['Trimethyl_benzene_redo', 'Pff4TBT_redo_180C']
    # x = [31600, 4400]
    # y = [-3600, -4300]

    # names=['PTB7', 'PCE10', 'Pff4TBT_2ndrun', 'P3DT']
    # x = [ 13600, 19200, 4400, -27000]
    # y = [-4200, -4200, -4700, -4800]

    names = ["Trimethyl_benzene_2ndrun"]
    x = [31600]
    y = [-3400]

    assert len(names) == len(
        x
    ), f"Number of X coordinates ({len(names)}) is different from number of samples ({len(x)})"
    assert len(y) == len(
        x
    ), f"Number of X coordinates ({len(y)}) is different from number of samples ({len(x)})"

    for name, xs, ys in zip(names, x, y):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)

            det_exposure_time(t, t)
            name_fmt = "{sample}_nexafs_{energy}eV_wa{wax}_bpm{xbpm}"
            for e in energies:
                yield from bps.mv(energy, e)
                yield from bps.sleep(1)

                bpm = xbpm2.sumX.value

                sample_name = name_fmt.format(
                    sample=name, energy="%6.2f" % e, wax=wa, xbpm="%4.3f" % bpm
                )
                sample_id(user_name="GF", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 2470)
            yield from bps.mv(energy, 2450)


def gu_saxs_S_2022_1(t=1):
    dets = [pil1M]

    energies = [2450, 2460, 2470, 2475, 2476, 2477, 2478, 2480, 2500]
    waxs_arc = [20]

    names = ["Trimethyl_benzene_2ndrun"]
    x = [31600]
    y = [-3300]
    # names=['PTB7', 'PCE10', 'Pff4TBT_2ndrun', 'P3DT']
    # x = [ 13600, 19200, 4400, -27000]
    # y = [-4200, -4200, -4700, -4800]
    # names=['Trimethyl_benzene', 'Pff4TBT']
    # x = [31600, 4600]
    # y = [-3600, -4300]

    assert len(names) == len(
        x
    ), f"Number of X coordinates ({len(names)}) is different from number of samples ({len(x)})"
    assert len(y) == len(
        x
    ), f"Number of X coordinates ({len(y)}) is different from number of samples ({len(x)})"

    for name, xs, ys in zip(names, x, y):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)

            det_exposure_time(t, t)
            name_fmt = "{sample}_1.6m_{energy}eV_wa{wax}_bpm{xbpm}"
            for i, e in enumerate(energies):
                yield from bps.mv(energy, e)
                yield from bps.sleep(5)
                # yield from bps.mv(piezo.y, ys + i * 50)

                bpm = xbpm2.sumX.value

                sample_name = name_fmt.format(
                    sample=name, energy="%6.2f" % e, wax=wa, xbpm="%4.3f" % bpm
                )
                sample_id(user_name="GF", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 2470)
            yield from bps.mv(energy, 2450)


def gu_saxs_hardxray_2022_1(t=1):
    dets = [pil1M]

    energies = [16100]
    waxs_arc = [20]

    names = ["Trimethyl_benzene", "PCE10", "PTB7", "Pff4TBT", "P3DT"]
    x = [31800, 19200, 14100, 5100, -27000]
    y = [-3300, -3800, -3900, -4000, -4200]

    assert len(names) == len(
        x
    ), f"Number of X coordinates ({len(names)}) is different from number of samples ({len(x)})"
    assert len(y) == len(
        x
    ), f"Number of X coordinates ({len(y)}) is different from number of samples ({len(x)})"

    for name, xs, ys in zip(names, x, y):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)

            det_exposure_time(t, t)
            name_fmt = "{sample}_4.0m_{energy}eV_wa{wax}_exp5s"
            for i, e in enumerate(energies):
                yield from bps.mv(energy, e)
                yield from bps.sleep(5)
                # yield from bps.mv(piezo.y, ys + i * 50)

                sample_name = name_fmt.format(sample=name, energy="%6.2f" % e, wax=wa)
                sample_id(user_name="GF", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)


def wang_temperature_hard_2022_2(t=1):
    """
    WAXS and SAXS using heating stage controlled by Lakeshore

    For reference: 16.1 keV, low divergence, in vacuum, SAXS sdd 8.3 m
    """

    # solid sample position
    samples = [
        "PffBT4T_1",
        "PffBT4T_2",
        "P3OT_1",
        "P3OT_2",
        "P3DT_1",
        "P3DT_2",
        "P3DDT_1",
        "P3DDT_2",
        "PIB_A_DPP_A",
        "PIB_Br_DPP_A",
        "PIB_A_DPP_Br",
        "PIB_Br_DPP_Br",
        "5%P3HT",
        "5%DPP",
    ]
    x_piezo = [
        41600,
        42200,
        34200,
        35400,
        27600,
        27600,
        20800,
        22000,
        12600,
        2600,
        -6400,
        -16400,
        -25500,
        -36500,
    ]
    y_piezo = [
        -3200,
        -3700,
        -4300,
        -4300,
        -4100,
        -3200,
        -3300,
        -3300,
        -3300,
        -4300,
        -4300,
        -4000,
        -3700,
        -4100,
    ]

    # Move all samples
    y_piezo = np.asarray(y_piezo) - 50

    # solution sample position
    # samples = ['blank_SiNx', 'TMB1_1', 'TMB1_2', 'TMB2_1', 'TMB2_2', 'PS_TMB_1', 'PS_TMB_2', 'PffBT4T1_TMB_1', 'PffBT4T1_TMB_2', 'PffBT4T2_TMB_1', 'PffBT4T2_TMB_2', 'P3OT1_TMB_1', 'P3OT1_TMB_2', 'P3DT_TMB_1', 'P3DT_TMB_2', 'P3DDT_TMB_1', 'P3DDT_TMB_2']
    # x_piezo = [       45000,    38900,    37700,    31700,    31700,     25300,      26100,             20600,            21200,            14300,            15100,          8500,          8400,       -1800,         -3100,         -7300,         -8500]
    # y_piezo = [       -3200,    -3000,    -3000,    -3000,    -3500,     -3900,      -2500,             -3700,            -3700,            -3500,            -2700,         -2500,         -3900,       -4100,         -4100,         -4300,         -3050]

    # Correct sample names just in case
    samples = [
        s.translate({ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ =,"}) for s in samples
    ]
    assert len(x_piezo) == len(
        y_piezo
    ), f"Number of X coordinates ({len(x_list)}) is different from number of Y coordinates ({len(y_list)})"
    assert len(x_piezo) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"

    user_name = "YW"
    temperatures = [30]
    waxs_arc = [0, 20]
    name_fmt = "{sample}_{energy}keV_temp{temp}degC_wa{wax}_sdd{sdd}m_id{scan_id}"

    for temperature in temperatures:
        t_kelvin = temperature + 273.15
        yield from ls.output1.mv_temp(t_kelvin)

        # Activate heating range in Lakeshore
        if temperature < 50:
            yield from bps.mv(ls.output1.status, 1)
        else:
            yield from bps.mv(ls.output1.status, 3)

        # Equalise temperature
        print("Equalising temperature")
        start = time.time()
        temp = ls.input_A.get()
        while abs(temp - t_kelvin) > 5:
            print("Difference: {:.1f} K".format(abs(temp - t_kelvin)))
            yield from bps.sleep(10)
            temp = ls.input_A.get()
            # Escape the loop if too much time passes
            if time.time() - start > 3600:
                temp = t_kelvin
        print(
            "Time needed to equilibrate: {:.1f} min".format((time.time() - start) / 60)
        )

        # Wait extra time depending on temperature
        if (56 < temperature) and (temperature < 160):
            yield from bps.sleep(300)
        elif 160 <= temperature:
            yield from bps.sleep(600)

        # Read T and convert to deg C
        temp_degC = ls.input_A.get() - 273.15

        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)

            dets = [pil900KW] if waxs.arc.position < 15 else [pil1M, pil900KW]
            det_exposure_time(t, t)

            for x, y, name in zip(x_piezo, y_piezo, samples):
                yield from bps.mv(piezo.x, x)
                yield from bps.mv(piezo.y, y + i * 50)

                # Metadata
                e = energy.position.energy / 1000
                temp = str(np.round(float(temp_degC), 1)).zfill(5)
                wa = str(np.round(float(wa), 1)).zfill(4)
                sdd = pil1m_pos.z.position / 1000
                scan_id = db[-1].start["scan_id"] + 1

                sample_name = name_fmt.format(
                    sample=name,
                    energy="%.1f" % e,
                    temp=temp,
                    wax=wa,
                    sdd="%.1f" % sdd,
                    scan_id=scan_id,
                )

                print(f"\n\t=== Sample: {sample_name} ===\n")
                sample_id(user_name=user_name, sample_name=sample_name)
                yield from bp.count(dets)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)

    # Turn off the heating and set temperature to 23 deg C
    t_kelvin = 23 + 273.15
    yield from ls.output1.mv_temp(t_kelvin)
    yield from ls.output1.turn_off()


def wang_temperature_tender_2022_2(t=1):
    """
    REMEMBER TO TURN ON HEATING FOR LIQUID RUN

    WAXS and SAXS using heating stage controlled by Lakeshore

    For reference: 2.470 keV, low divergence, in vacuum, SAXS sdd 8.3 m
    for fun

    YWang: I restart it 1:15am 07/21/22. Changed code to skip NEXAFS and 25C. Details can be found in following comments.
    """
    print("REMEMBER TO TURN ON HEATING FOR LIQUID RUN")

    # solution sample position
    samples = [
        "blank_SiNx",
        "TMB1_1",
        "TMB1_2",
        "TMB2_1",
        "TMB2_2",
        "PS_TMB_1",
        "PS_TMB_2",
        "PffBT4T1_TMB_1",
        "PffBT4T1_TMB_2",
        "PffBT4T2_TMB_1",
        "PffBT4T2_TMB_2",
        "P3OT1_TMB_1",
        "P3OT1_TMB_2",
        "P3DT_TMB_1",
        "P3DT_TMB_2",
        "P3DDT_TMB_1",
        "P3DDT_TMB_2",
    ]
    x_piezo = [
        45000,
        39100,
        38200,
        32000,
        32900,
        26800,
        25900,
        20800,
        21400,
        15400,
        14800,
        9000,
        9900,
        -2750,
        -1300,
        -7700,
        -6900,
    ]
    y_piezo = [
        -2500,
        -1900,
        -2000,
        -2000,
        -1700,
        -1700,
        -1700,
        -1700,
        -1800,
        -1800,
        -1800,
        -1300,
        -1200,
        -1200,
        -1200,
        -1400,
        -1400,
    ]

    # Correct sample names just in case
    samples = [
        s.translate({ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ =,"}) for s in samples
    ]
    assert len(x_piezo) == len(
        y_piezo
    ), f"Number of X coordinates ({len(x_piezo)}) is different from number of Y coordinates ({len(y_piezo)})"
    assert len(x_piezo) == len(
        samples
    ), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(samples)})"

    energies_coarse = [2460, 2470, 2472, 2474, 2475, 2476, 2477, 2478, 2480]

    energies_nexafs = np.concatenate(
        (
            np.arange(2445, 2470, 5),
            np.arange(2470, 2480, 0.25),
            np.arange(2480, 2490, 1),
            np.arange(2490, 2501, 5),
        )
    )

    user_name = "YW"
    temperatures = [
        50,
        100,
        150,
        170,
        180,
        190,
        200,
        210,
        220,
        230,
        240,
        250,
    ]  # YWang: I delete 25 here to skip 25C because I have had the SAXS data and most WAXS DATA  1:16 am 07/21/22
    waxs_arc = [0, 20, 40]
    name_fmt = "{sample}_{energy}eV_temp{temp}degC_wa{wax}_sdd{sdd}m_id{scan_id}"

    for temperature in temperatures:
        t_kelvin = temperature + 273.15
        yield from ls.output1.mv_temp(t_kelvin)

        # Activate heating range in Lakeshore
        if temperature < 50:
            yield from bps.mv(ls.output1.status, 1)
        else:
            yield from bps.mv(ls.output1.status, 3)

        # Equalise temperature
        print(f"Equalising temperature to {temperature} deg C")
        start = time.time()
        temp = ls.input_A.get()
        while abs(temp - t_kelvin) > 1:
            print("Difference: {:.1f} K".format(abs(temp - t_kelvin)))
            yield from bps.sleep(10)
            temp = ls.input_A.get()
            # Escape the loop if too much time passes
            if time.time() - start > 1800:
                temp = t_kelvin
        print(
            "Time needed to equilibrate: {:.1f} min".format((time.time() - start) / 60)
        )

        # Wait extra time depending on temperature
        if (35 < temperature) and (temperature < 160):
            yield from bps.sleep(300)
        elif 160 <= temperature:
            yield from bps.sleep(600)

        # Read T and convert to deg C
        temp_degC = ls.input_A.get() - 273.15

        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)

            # YWang: I changed < 25 to <45 to skip NEXAFS  1:16 am 07/21/22
            energies = energies_coarse if waxs.arc.position < 45 else energies_nexafs
            dets = [pil900KW] if waxs.arc.position < 15 else [pil1M, pil900KW]
            det_exposure_time(t, t)

            for j, (x, y, name) in enumerate(zip(x_piezo, y_piezo, samples)):
                yield from bps.mv(piezo.x, x)
                yield from bps.mv(piezo.y, y)

                for e in energies:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)

                    # Metadata
                    # e = energy.position.energy / 1000
                    temp = str(np.round(float(temp_degC), 1)).zfill(5)
                    wa = str(np.round(float(wa), 1)).zfill(4)
                    sdd = pil1m_pos.z.position / 1000
                    scan_id = db[-1].start["scan_id"] + 1

                    sample_name = name_fmt.format(
                        sample=name,
                        energy="%.2f" % e,
                        temp=temp,
                        wax=wa,
                        sdd="%.1f" % sdd,
                        scan_id=scan_id,
                    )

                    print(f"\n\t=== Sample {j + 1}/{len(samples)}: {sample_name} ===\n")
                    sample_id(user_name=user_name, sample_name=sample_name)
                    yield from bp.count(dets)

                yield from bps.mv(energy, 2475)
                yield from bps.mv(energy, 2460)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)

    # Turn off the heating and set temperature to 23 deg C
    t_kelvin = 23 + 273.15
    yield from ls.output1.mv_temp(t_kelvin)
    yield from ls.output1.turn_off()


def wang_temperature_hard_2022_3(t=1):
    """
    WAXS and SAXS using heating stage controlled by Lakeshore

    For reference: 16.1 keV, low divergence, in vacuum, SAXS sdd 8.3 m
    """

    ######### Yunfei solid sample position
    names =   ['SiNx-a', 'SiNx-b', 'SiNx-c', 'Pff1', 'Pff2', 'P3OT1-1', 'P3OT1-2', 'P3DT1-1', 'P3DT1-2', 'TMB4-1', 'TMB4-2',  'SiNx2-1', 'Pff3-1', 'Pff3-2', 'Pff5-1', 'Pff5-2', 'Pff5-3', 'empty-space']
    piezo_x = [   43000,    43600,    43600,  26100,  19500,     14300,     13250,      7200,      6000,   -20000,      -18800,       -25400,   -31400,   -31100,   -38500,   -38100,   -38000,     -41450]   
    piezo_y = [   -5000,    -5000,    -4400,  -4400,  -3800,     -3750,     -5000,     -3650,     -3650,    -2850,      -2900,         -2900,   -2900,     -2900,    -2900,    -2650,    -3450 ,     -3500]
    piezo_z = [4200 for n in names]
    # piezo_z = [4200, 4100, ]

    ######### Guorong solid sample position
    #names =   ['TAMU1', 'TAMU2', 'TAMU3', 'TAMU4', 'TAMU5', 'TAMU6', 'TAMU7', 'TAMU8','TAMU9', 'GM19', 'GER1', 'GER2', 'empty-space']
    #piezo_x = [   47000,  40700,   34300,   27700,   21300,   15200,    9000,    2500,  -3900, -10400, -16600, -23000,   -29300   ]   
    #piezo_y = [  -5250,   -5250,   -5250,   -5250,   -5250,   -5250,   -5250,   -4850,  -4850,  -4850,  -4850,  -4850,     -4850     ]
    #piezo_z = [4200 for n in names]
    # piezo_z = [4200, 4100, ]


    assert len(names) == len(piezo_x), f"Wrong list lenghts"
    assert len(piezo_y) == len(piezo_x), f"Wrong list lenghts"

    user_name = "YW"
    temperatures = [180] #[25, 180]
    waxs_arc = [0, 20]

    for temperature in temperatures:
        t_kelvin = temperature + 273.15
        yield from ls.output1.mv_temp(t_kelvin)

        # Activate heating range in Lakeshore
        if temperature < 50:
            yield from bps.mv(ls.output1.status, 1)
        else:
            yield from bps.mv(ls.output1.status, 3)

        # Equalise temperature
        print(f"Equalising temperature to {temperature:.0f} deg C")
        start = time.time()
        temp = ls.input_A.get()
        while abs(temp - t_kelvin) > 5:
            print("Difference: {:.1f} K".format(abs(temp - t_kelvin)))
            yield from bps.sleep(10)
            temp = ls.input_A.get()
            
            # Escape the loop if too much time passes
            if time.time() - start > 15 * 60:
                temp = t_kelvin
        print(
            "Time needed to equilibrate: {:.1f} min".format((time.time() - start) / 60)
        )

        # Wait extra time depending on temperature
        ######## Yunfei changed both to 1 second. Previous is 300 , 600
        if (56 < temperature) and (temperature < 160):
            yield from bps.sleep(1)
        elif 160 <= temperature:
            yield from bps.sleep(1)

        # Read T and convert to deg C
        temp_degC = ls.input_A.get() - 273.15

        rod_pos = pil1m_bs_rod.x.position

        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)

            dets = [pil900KW] if waxs.arc.position < 15 else [pil1M, pil900KW]
            
            if not ((0 < rod_pos) and (rod_pos < 3)):
                dets.append(pdcurrent)
                dets.append(pdcurrent1)
                dets.append(pdcurrent2)

            det_exposure_time(t, t)

            for name, x, y in zip(names, piezo_x, piezo_y):
                yield from bps.mv(piezo.x, x,
                                  piezo.y, y + i * 0)

                # Metadata
                e = energy.position.energy / 1000
                temp = str(np.round(float(temp_degC), 1)).zfill(5)
                wa = waxs.arc.position + 0.001
                wa = str(np.round(float(wa), 1)).zfill(4)
                sdd = pil1m_pos.z.position / 1000

                if not ((0 < rod_pos) and (rod_pos < 3)):
                    if waxs.arc.position > 15:
                        fs.open()
                        yield from bps.sleep(0.3)
                        curr = pdcurrent2.get()
                        fs.close()
                    else:
                        curr = 0
                    curr = str(np.round(float(curr), 0))
                else:
                    curr = '_rod_'

                
                
                name_fmt = "{sample}_{temp}degC_{energy}keV_wa{wax}_sdd{sdd}m_pd{curr}"
                sample_name = name_fmt.format(
                    sample=name,
                    energy="%.2f" % e,
                    temp=temp,
                    wax=wa,
                    sdd="%.1f" % sdd,
                    #curr='%.0f' % curr,
                    curr = curr,
                )
                sample_name = sample_name.translate(
                    {ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ =, "}
                )
                print(f"\n\n\n\t=== Sample: {sample_name} ===")
                sample_id(user_name=user_name, sample_name=sample_name)
                yield from bp.count(dets)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)

    # Turn off the heating and set temperature to 23 deg C
    #t_kelvin = 23 + 273.15
    #yield from ls.output1.mv_temp(t_kelvin)
    #yield from ls.output1.turn_off()


def read_pd_current():
    """
    Read pin diode current with attenuated beam
    """
    #yield from bps.mv(att1_6.open_cmd, 1)
    #yield from bps.mv(att1_7.open_cmd, 1)
    #yield from bps.sleep(2)

    fs.open()
    yield from bps.sleep(0.3)
    pd_curr = pdcurrent2.get()
    fs.close()

    #yield from bps.mv(att1_6.close_cmd, 1)
    #yield from bps.mv(att1_7.close_cmd, 1)

    #yield from bps.sleep(2)

    return(pd_curr)

def turn_off_heating(temp=23):
    """
    Turn off the heating and set temperature to 23 deg C for Lakeshore
    """
    print(f'Setting temp to {temp} deg C and turning off the heater')
    t_kelvin = temp + 273.15
    yield from ls.output1.mv_temp(t_kelvin)
    yield from ls.output1.turn_off()


def wang_temperature_tender_2022_3(t=2.5):
    """
    Tender X-ray WAXS and SAXS Lakeshore heating stage, coarse energies

    For reference: 2470 eV, low divergence, in vacuum, SAXS sdd 1.6 m
    """

    names =   ['SiNx-a', 'SiNx-b',  'P3OT1-1', 'P3OT1-2', 'P3DT1-1', 'P3DT1-2', 'TMB4-1',          'TMB4-2',  'SiNx2-1',  'Pff5-1', 'Pff5-2', 'Pff5-3', 'empty-space']
    piezo_x = [   43500,    44000,      14700,     13650,      7600,      6400,   -19650,      -18450,       -25400,     -37900,   -37900,   -37700,     -34300]   
    piezo_y = [   -5000,    -5000,      -3800,     -5150,     -5200,     -3800,    -3050,      -3100,         -3100,       -2900,    -3300,    -3500 ,     -3500]
    piezo_z = [5600 for n in names]
    # piezo_z = [4200, 4100, ]

    assert len(names)   == len(piezo_x), f"Wrong list lenghts"
    assert len(piezo_x) == len(piezo_y), f"Wrong list lenghts"
    assert len(piezo_y) == len(piezo_z), f"Wrong list lenghts"

    user_name = "YW"
    temperatures = [25, 200] #[25, 180]
    waxs_arc = [0, 20]
    energies = [2460, 2470, 2472, 2474, 2475, 2476, 2477, 2478, 2480]
    rod_pos = pil1m_bs_rod.x.position

    pin_diode_in_rod_out = not ((0 < rod_pos) and (rod_pos < 3))

    # Add beamstop to sample name
    if pin_diode_in_rod_out:
        names = [n + '-pd' for n in names]
    else:
        names = [n + '-rod' for n in names]

    for temperature in temperatures:
        t_kelvin = temperature + 273.15
        yield from ls.output1.mv_temp(t_kelvin)

        # Activate heating range in Lakeshore
        if temperature < 50:
            yield from bps.mv(ls.output1.status, 1)
        else:
            yield from bps.mv(ls.output1.status, 3)

        # Equalise temperature
        print(f"Equalising temperature to {temperature:.0f} deg C")
        start = time.time()
        temp = ls.input_A.get()
        while abs(temp - t_kelvin) > 5:
            print("Difference: {:.1f} K".format(abs(temp - t_kelvin)))
            yield from bps.sleep(10)
            temp = ls.input_A.get()
            
            # Escape the loop if too much time passes
            if time.time() - start > 15 * 60:
                temp = t_kelvin
        print(
            "Time needed to equilibrate: {:.1f} min".format((time.time() - start) / 60)
        )

        # Wait extra time depending on temperature
        if (56 < temperature) and (temperature < 160):
            yield from bps.sleep(300)
        elif 160 <= temperature:
            yield from bps.sleep(600)

        # Read T and convert to deg C
        temp_degC = ls.input_A.get() - 273.15

        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)

            dets = [pil900KW] if waxs.arc.position < 15 else [pil1M, pil900KW]
            det_exposure_time(t, t)

            if pin_diode_in_rod_out:
                dets.append(pdcurrent)
                dets.append(pdcurrent1)
                dets.append(pdcurrent2)

            for name, x, y in zip(names, piezo_x, piezo_y):
                yield from bps.mv(piezo.x, x,
                                  piezo.y, y + i * 0)

                for e in energies:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                
                
                    # Metadata
                    #e = energy.position.energy / 1000
                    temp = str(np.round(float(temp_degC), 1)).zfill(5)
                    wa = waxs.arc.position + 0.001
                    wa = str(np.round(float(wa), 1)).zfill(4)
                    sdd = pil1m_pos.z.position / 1000

                    if pin_diode_in_rod_out:
                        if waxs.arc.position > 15:
                            fs.open()
                            yield from bps.sleep(0.3)
                            curr = pdcurrent2.get()
                            fs.close()
                        else:
                            curr = 0
                        curr = str(np.round(float(curr), 0))
                    else:
                        curr = '_rod_'

                    name_fmt = "{sample}_{temp}degC_{energy}eV_wa{wax}_sdd{sdd}m_pd{curr}"
                    sample_name = name_fmt.format(
                        sample=name,
                        energy="%.2f" % e,
                        temp=temp,
                        wax=wa,
                        sdd="%.1f" % sdd,
                        #curr='%.0f' % curr,
                        curr = curr,
                    )
                    sample_name = sample_name.translate(
                        {ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ =, "}
                    )
                    print(f"\n\n\n\t=== Sample: {sample_name} ===")
                    sample_id(user_name=user_name, sample_name=sample_name)
                    
                    yield from bp.count(dets)
                yield from bps.mv(energy, 2475)
                yield from bps.mv(energy, 2460)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)

    # Turn off the heating and set temperature to 23 deg C
    yield from turn_off_heating()


def guorong_swaxs_2023_1(t=0.5):
    """
    Take WAXS and SAXS at several sample positions for averaging

    Specify central positions on the samples with xlocs and ylocs,
    then offsets from central positions with x_off and y_off.
    """
    # Row A
    names_A = []#['Perth1', 'Perth2', 'Perth3', 'Perth4', 'Perth5','Perth6','Perth7','Perth8','Perth9','Perth10','Perth11_PI film'  ]
    piezo_x_A = []#[-39000,   -31000, -23000,    -16000,   -8000,    0000,   7000,     14000,   22000,    32000,      40000]
    piezo_y_A = []#[     0,      0,       0,         0,        0,      0,      0,         0,      0,       -1000,      -1000] 
    hexa_y_A  = []#[     -3 for n in names_A ]

    # Row B
    names_B =  ['Sec-PffBT4T_Mag','Sec-PQT-12_Mag','Sec-P3HT_Mag']
    names_B =   [f'{n}-B-rotate00' for n in names_B]
    piezo_x_B = [    15000,   23000,    31000]
    piezo_y_B = [    4200 ,   4200,  4200]
    hexa_y_B  = [   -3 for n in names_B ]

    # # Row C
    # names_C =   [ 'G1','G2','G3','G4','G5','G6','G7','G8','G9','G10','G11-Empty-Al']
    # piezo_x_C = [ -38600,      -30300,     -22000,        -14000,      -6000,    2000,   10000,     18000,   26000,    34000,      42000]
    # piezo_y_C = [ 9000 for n in names_C]
    # hexa_y_C  = [ -3 for n in names_C ] 

    # # Row D
    # names_D =   [ 'D1-058-F1','D2-051','D3-058-F2','D4-JZ1','D5-AgBh','D6-JZ2','D7-Blank_hole','D8-JZ3','D9-Empty_hole','D10-ZJ4','D11-Empty-Al']
    # piezo_x_D = [ -38600,      -30300,     -22000,        -14000,      -6000,    2000,   10000,     18000,   26000,    34000,      42000]
    # piezo_y_D = [ -5000 for n in names_D]
    # hexa_y_D  = [ 10 for n in names_D ] 

    # # Row E
    # names_E =   ['AT1','AT2','AT3','Empty-Al','Empty-Al','Empty-Al','Empty-Al','Empty-Al','Empty-Al','Empty-Al','Empty-Al' ]
    # piezo_x_E = [-38600,      -30300,     -22000,        -14000,      -6000,    2000,   10000,     18000,   26000,    34000,      42000]
    # piezo_y_E = [ 3000 for n in names_E]
    # hexa_y_E  = [ 10 for n in names_E] 

    # Combine lists
    names =   names_A   +   names_B #+   names_C #+   names_D +   names_E #+ names_F #+ names_G
    piezo_x = piezo_x_A + piezo_x_B #+ piezo_x_C #+ piezo_x_D + piezo_x_E #+ piezo_x_F #+ piezo_x_G
    piezo_y = piezo_y_A + piezo_y_B #+ piezo_y_C #+ piezo_y_D + piezo_y_E #+ piezo_y_F #+ piezo_y_G
    hexa_y  = hexa_y_A  +  hexa_y_B #+  hexa_y_C #+  hexa_y_D +  hexa_y_E #+ hexa_y_F #+ hexa_y_G
    
    x_off = [0]
    y_off = [0 ]

    waxs_arc = [0]


    user = "GM"

    # Check and correct sample names just in case
    names = [n.translate({ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ "}) for n in names]

    # Check if the length of xlocs, ylocs and names are the same
    msg = "Wrong number of coordinates, check sample positions!"
    assert len(piezo_x) == len(names), msg
    assert len(piezo_x) == len(piezo_y), msg
    assert len(piezo_x) == len(hexa_y), msg

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)
        # Detectors, disable SAXS when WAXS in the way
        dets = [pil900KW] if waxs.arc.position < 15 else [pil900KW, pil1M]
        det_exposure_time(t, t)

        for name, x, y, hy in zip(names, piezo_x, piezo_y, hexa_y):
            yield from bps.mv(piezo.y, y,
                              piezo.x, x,
                              stage.y, hy)

            for yy, y_of in enumerate(y_off):
                yield from bps.mv(piezo.y, y + y_of)

                for xx, x_of in enumerate(x_off):
                    yield from bps.mv(piezo.x, x + x_of)
                    

                    # Metadata
                    e = energy.position.energy / 1000
                    wa = waxs.arc.position + 0.001
                    wa = str(np.round(float(wa), 1)).zfill(4)
                    sdd = pil1m_pos.z.position / 1000

                    # Sample name
                    name_fmt = ( "{sample}_{energy}keV_wa{wax}_sdd{sdd}m_loc{yy}{xx}")
                    sample_name = name_fmt.format(
                        sample=name,
                        energy="%.2f" % e,
                        wax=wa,
                        sdd="%.1f" % sdd,
                        #loc=int(loc),
                        xx = xx,
                        yy = yy,
                    )
                    sample_id(user_name=user, sample_name=sample_name)
                    print(f"\n\n\n\t=== Sample: {sample_name} ===")
                    yield from bp.count(dets)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def guorong_temperature_cap_2023_1(t=0.5):
    """
    Hard X-ray WAXS and SAXS Lakeshore heating stage
    """

    names =   [ 'Bkg_CB', 'SOE_OX_Tol', 'SOE_Tol','Bkg_Tol','AMA_058_F1','AMA_051','AMA_085_F1',
                'AMA_058_F2','AMA_085-F2','OMA80-2A','OMA86-2A','OMA80-2','OMA86-1','OMA86-1A','OMA86-2']
    piezo_x = [ -42000,     -35600,     -29200,  -22900,  -16500,   -10200,   -3900, 2450, 8750,
                15050, 21350,27650,34000, 40400,46700]   
    piezo_y = [   6500,       6500,     6400,     6300,    6200,      6100,     
                6000, 5900, 5800, 5700, 5600, 5500, 5500,   5500,  5500]


    assert len(names)   == len(piezo_x), f"Wrong list lenghts"
    assert len(piezo_x) == len(piezo_y), f"Wrong list lenghts"

    user_name = "GM"
    temperatures = [40, 80, 120]
    waxs_arc = [20]

    x_off = [0]
    y_off = [-200, 0, 200]

    for temperature in temperatures:
        t_kelvin = temperature + 273.15
        yield from ls.output1.mv_temp(t_kelvin)

        # Activate heating range in Lakeshore
        if temperature < 50:
            yield from bps.mv(ls.output1.status, 1)
        else:
            yield from bps.mv(ls.output1.status, 3)

        # Equalise temperature
        print(f"Equalising temperature to {temperature:.0f} deg C")
        start = time.time()
        temp = ls.input_A.get()
        while abs(temp - t_kelvin) > 5:
            print("Difference: {:.1f} K".format(abs(temp - t_kelvin)))
            yield from bps.sleep(10)
            temp = ls.input_A.get()
            
            # Escape the loop if too much time passes
            if time.time() - start > 15 * 60:
                temp = t_kelvin
        print(
            "Time needed to equilibrate: {:.1f} min".format((time.time() - start) / 60)
        )

        # Wait extra time depending on temperature
        if (56 < temperature) and (temperature < 160):
            yield from bps.sleep(300)
        elif 160 <= temperature:
            yield from bps.sleep(600)

        # Read T and convert to deg C
        temp_degC = ls.input_A.get() - 273.15

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)

            dets = [pil900KW] if waxs.arc.position < 15 else [pil1M, pil900KW]
            det_exposure_time(t, t)

            dets.append(pdcurrent)
            dets.append(pdcurrent1)
            dets.append(pdcurrent2)

            for name, x, y in zip(names, piezo_x, piezo_y):
                yield from bps.mv(piezo.x, x,
                                  piezo.y, y)

                for yy, y_of in enumerate(y_off):
                    yield from bps.mv(piezo.y, y + y_of)

                    for xx, x_of in enumerate(x_off):
                        yield from bps.mv(piezo.x, x + x_of)
                        # Metadata
                        e = energy.position.energy / 1000
                        temp = str(np.round(float(temp_degC), 1)).zfill(5)
                        wa = waxs.arc.position + 0.001
                        wa = str(np.round(float(wa), 1)).zfill(4)
                        sdd = pil1m_pos.z.position / 1000


                        # Sample name
                        name_fmt = ( "{sample}_{temp}_degC_{energy}keV_wa{wax}_sdd{sdd}m_loc{yy}{xx}")
                        sample_name = name_fmt.format(
                            sample=name,
                            energy="%.2f" % e,
                            temp=temp,
                            wax=wa,
                            sdd="%.1f" % sdd,
                            xx = xx,
                            yy = yy,
                        )
                        sample_name = sample_name.translate(
                            {ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ =, "}
                        )
                        print(f"\n\n\n\t=== Sample: {sample_name} ===")
                        sample_id(user_name=user_name, sample_name=sample_name)
                        yield from bp.count(dets)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)

    # Turn off the heating and set temperature to 23 deg C
    yield from turn_off_heating()



def yunfei_hard_temperature_2023_1(t=1):
    """
    Hard X-ray WAXS and SAXS Lakeshore heating stage
    """

    names =   ['empty',  'SiNx1', 'SiNx2', 'TMB11',  'TMB12', 'TMB21',  'TMB22',  'Pff11',  'Pff12', 'Pff13', 'P3DDT1', 'P3DDT2',  'Pff21']
    piezo_x = [  39100,    35100,   35700,   27500,    26300,   17800,    17800,    11200,     9750,    9700,     3300,     2600,    -5200]      
    piezo_y = [  -1850,    -1850,   -1350,  -922.6,   -922.6,    -950,    -2350,    -2500,    -1050,   -2500,     -950,     -950,    -1050]

    
    assert len(names)   == len(piezo_x), f"Wrong list lenghts"
    assert len(piezo_x) == len(piezo_y), f"Wrong list lenghts"

    user_name = "YW"
    temperatures = [180]
    waxs_arc = [20, 0]

    rod_pos = pil1m_bs_rod.x.position
    pin_diode_in_rod_out = not ((0 < rod_pos) and (rod_pos < 3))

    # Add beamstop to sample name
    if pin_diode_in_rod_out:
        names = [n + '-pd' for n in names]
    else:
        names = [n + '-rod' for n in names]

    for temperature in temperatures:
        t_kelvin = temperature + 273.15
        yield from ls.output1.mv_temp(t_kelvin)

        # Activate heating range in Lakeshore
        if temperature < 50:
            yield from bps.mv(ls.output1.status, 1)
        else:
            yield from bps.mv(ls.output1.status, 3)

        # Equalise temperature
        print(f"Equalising temperature to {temperature:.0f} deg C")
        start = time.time()
        temp = ls.input_A.get()
        while abs(temp - t_kelvin) > 5:
            print("Difference: {:.1f} K".format(abs(temp - t_kelvin)))
            yield from bps.sleep(10)
            temp = ls.input_A.get()
            
            # Escape the loop if too much time passes
            if time.time() - start > 15 * 60:
                temp = t_kelvin
        print(
            "Time needed to equilibrate: {:.1f} min".format((time.time() - start) / 60)
        )

        # Wait extra time depending on temperature
        if (56 < temperature) and (temperature <= 150):
            wait_time = 60
            print(f'Sleeping for {wait_time} seconds')
            yield from bps.sleep(wait_time)
        elif 150 < temperature:
            wait_time = 1
            print(f'Sleeping for {wait_time} seconds')
            yield from bps.sleep(wait_time)

        # Read T and convert to deg C
        temp_degC = ls.input_A.get() - 273.15

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)

            dets = [pil900KW] if waxs.arc.position < 15 else [pil1M, pil900KW]
            det_exposure_time(t, t)

            dets.append(pdcurrent)
            dets.append(pdcurrent1)
            dets.append(pdcurrent2)

            for name, x, y in zip(names, piezo_x, piezo_y):
                yield from bps.mv(piezo.x, x,
                                  piezo.y, y)
                # Metadata
                e = energy.position.energy / 1000
                temp = str(np.round(float(temp_degC), 1)).zfill(5)
                wa = waxs.arc.position + 0.001
                wa = str(np.round(float(wa), 1)).zfill(4)
                sdd = pil1m_pos.z.position / 1000

                if pin_diode_in_rod_out:
                    if waxs.arc.position > 15:
                        fs.open()
                        yield from bps.sleep(0.3)
                        curr = pdcurrent2.get()
                        fs.close()
                    else:
                        curr = 0
                    curr = str(np.round(float(curr), 0))
                else:
                    curr = '_rod_'

                # Sample name
                name_fmt = ("{sample}_{temp}degC_{energy}keV_wa{wax}_sdd{sdd}m_pd{curr}_expt{t}s")
                sample_name = name_fmt.format(
                    sample = name,
                    energy = "%.2f" % e,
                    temp = temp,
                    wax = wa,
                    sdd = "%.1f" % sdd,
                    curr = curr,
                    t = t,
                )
                sample_name = sample_name.translate(
                    {ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ =, "}
                )
                print(f"\n\n\n\t=== Sample: {sample_name} ===")
                sample_id(user_name=user_name, sample_name=sample_name)
                yield from bp.count(dets)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)

    # Turn off the heating and set temperature to 23 deg C
    #yield from turn_off_heating()

def wang_temperature_tender_2023_1(t=5):
    """
    Tender X-ray WAXS and SAXS Lakeshore heating stage, coarse energies

    For reference: 2470 eV, low divergence, in vacuum, SAXS sdd 1.6 m
    """

    names =   ['empty', 'Pff11',  'Pff12',  'Pff13',  'Pff14',   'Pff31',  'Pff32',  'Pff33', 'Pff34',  'SiNx1',  'SiNx2',       'Pff42',   'Pff61',  'Pff62',  'Pff63',  'Pff71',  'Pff72',  'Pff73']       
    piezo_x = [  46300,   42300,    43100,    43100,    42500,     26100,    25500,    25500,   25500,    15200,    15200,          8000,    -10400,   -10400,    -9800,   -16700,   -17300,   -17300]   
    piezo_y = [  -3800,   -3800,    -3800,    -2900,    -2900,     -3500,    -3500,    -2900,   -3200,    -3200,    -2600,         -2600,     -2000,    -1700,    -1700,    -1700,    -1700,    -2200]

    piezo_z = [4200 for n in names]
    # piezo_z = [4200, 4100, ]

    assert len(names)   == len(piezo_x), f"Wrong list lenghts"
    assert len(piezo_x) == len(piezo_y), f"Wrong list lenghts"
    assert len(piezo_y) == len(piezo_z), f"Wrong list lenghts"

    user_name = "YW"
    #temperatures = [25, 40, 60, 80, 100, 120, 140, 150, 160, 170, 180] #[25, 180]
    temperatures = [180, 190, 200, 210, 220] #[25, 180]
    waxs_arc = [20, 0] 
    energies = [2460, 2470, 2472, 2474, 2475, 2476, 2477, 2478, 2480, 2490]
    rod_pos = pil1m_bs_rod.x.position

    pin_diode_in_rod_out = not ((0 < rod_pos) and (rod_pos < 3))

    # Add beamstop to sample name
    if pin_diode_in_rod_out:
        names = [n + '-pd' for n in names]
    else:
        names = [n + '-rod' for n in names]

    for temperature in temperatures:
        t_kelvin = temperature + 273.15
        yield from ls.output1.mv_temp(t_kelvin)

        # Activate heating range in Lakeshore
        if temperature < 50:
            yield from bps.mv(ls.output1.status, 1)
        else:
            yield from bps.mv(ls.output1.status, 3)

        # Equalise temperature
        print(f"Equalising temperature to {temperature:.0f} deg C")
        start = time.time()
        temp = ls.input_A.get()
        while abs(temp - t_kelvin) > 5:
            print("Difference: {:.1f} K".format(abs(temp - t_kelvin)))
            yield from bps.sleep(5)
            temp = ls.input_A.get()
            
            # Escape the loop if too much time passes
            if time.time() - start > 15 * 60:
                temp = t_kelvin
        print(
            "Time needed to equilibrate: {:.1f} min".format((time.time() - start) / 60)
        )

        # Wait extra time depending on temperature
        if (56 < temperature) and (temperature <= 150):
            wait_time = 300
            print(f'Sleeping for {wait_time} seconds')
            yield from bps.sleep(wait_time)
        elif 150 < temperature:
            wait_time = 300
            print(f'Sleeping for {wait_time} seconds')
            yield from bps.sleep(wait_time)

        # Read T and convert to deg C
        temp_degC = ls.input_A.get() - 273.15

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)

            dets = [pil900KW] if waxs.arc.position < 15 else [pil1M, pil900KW]
            det_exposure_time(t, t)

            if pin_diode_in_rod_out:
                dets.append(pdcurrent)
                dets.append(pdcurrent1)
                dets.append(pdcurrent2)

            for name, x, y in zip(names, piezo_x, piezo_y):
                yield from bps.mv(piezo.x, x,
                                  piezo.y, y)

                for e in energies:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                
                    # Metadata
                    #e = energy.position.energy / 1000
                    temp = str(np.round(float(temp_degC), 1)).zfill(5)
                    wa = waxs.arc.position + 0.001
                    wa = str(np.round(float(wa), 1)).zfill(4)
                    sdd = pil1m_pos.z.position / 1000

                    if pin_diode_in_rod_out:
                        if waxs.arc.position > 15:
                            fs.open()
                            yield from bps.sleep(0.3)
                            curr = pdcurrent2.get()
                            fs.close()
                        else:
                            curr = 0
                        curr = str(np.round(float(curr), 0))
                    else:
                        curr = '_rod_'

                    # Sample name
                    name_fmt = ("{sample}_{temp}degC_{energy}eV_wa{wax}_sdd{sdd}m_pd{curr}_expt{t}s")
                    sample_name = name_fmt.format(
                        sample = name,
                        energy = "%.2f" % e ,
                        temp = temp,
                        wax = wa,
                        sdd = "%.1f" % sdd,
                        curr = curr,
                        t = t,
                    )
                    sample_name = sample_name.translate(
                        {ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ =, "}
                    )
                    print(f"\n\n\n\t=== Sample: {sample_name} ===")
                    sample_id(user_name=user_name, sample_name=sample_name)
                    
                    yield from bp.count(dets)
                yield from bps.mv(energy, 2475)
                yield from bps.mv(energy, 2460)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)

    # Turn off the heating and set temperature to 23 deg C
    yield from turn_off_heating()

def atten_move_in():
    """
    Move 4x + 2x Sn 60 um attenuators in
    """
    print('Moving attenuators in')

    while att1_7.status.get() != 'Open':
        yield from bps.mv(att1_7.open_cmd, 1)
        yield from bps.sleep(1)
    while att1_6.status.get() != 'Open':
        yield from bps.mv(att1_6.open_cmd, 1)
        yield from bps.sleep(1)

def atten_move_out():
    """
    Move 4x + 2x Sn 60 um attenuators out
    """
    print('Moving attenuators out')
    while att1_7.status.get() != 'Not Open':
        yield from bps.mv(att1_7.close_cmd, 1)
        yield from bps.sleep(1)
    while att1_6.status.get() != 'Not Open':
        yield from bps.mv(att1_6.close_cmd, 1)
        yield from bps.sleep(1)


def guorong_temperature_cap_2023_2(t=0.5):
    """
    Hard X-ray WAXS and SAXS Lakeshore heating stage
    at multiple SAXS detector distances.
    Measure transmission only during the first run
    """

    names =   [ 'Bkg_98v2', 'Bkg_95v5',  'Bkg_7v3', 'Bkg_5v5', 'Bkg_3v7', 'Bkg_1v9', 'P3HT_pTBA', 'PQT12_pTBA',
                   'Bkg_pTBA', 'DPP_CB_fine', 'DPP_DCB_fine', 'DPP_TCB_fine', 'DPP_DCB_Hex_fine', 'DPP_DCB_DMSO_fine', 'PBTTT14_CB' ]
    piezo_x = [     -39000,     -32800,     -26400,     -20000,       -13800,      -7400,      -1000,         5400,
                     11800,      18200,      24600,      31000,        37400,      43800,      50200]   
    piezo_y = [      -4200,      -4300,      -4400,      -4600,        -4800,      -4900,      -5000,         -5100,
                     -5300,      -5400,      -5500,      -5800,        -6200,      -6300,      -6400]

    assert len(names)   == len(piezo_x), f"Wrong list lenghts"
    assert len(piezo_x) == len(piezo_y), f"Wrong list lenghts"

    user_name = "GM"
    temperatures = [ 30, 40, 50, 60, 70, 90, 110, 130, 150, 170 ]
    waxs_arc = [20, 0]

    points = 5
    dy = 100
    dbeam_x = -38500
    dbeam_y = -4000
    stats1_direct = 1

    saxs_dist = [3000]

    current_sdd = pil1m_pos.z.user_setpoint.get()

    if ( abs(current_sdd - saxs_dist[0]) ) > ( abs(current_sdd - saxs_dist[-1]) ):
        saxs_dist = saxs_dist[::-1]

    saxs_dict = {
        3000 : {'sdd': 3000, 'beam_centre': [396, 557], 'bs': 'rod', 'energy': 16100, 'bs_pos': 2.25},
        8300 : {'sdd': 8300, 'beam_centre': [401, 555], 'bs': 'rod', 'energy': 16100, 'bs_pos': 1.40},
    }

    for temperature in temperatures:
        t_kelvin = temperature + 273.15
        yield from ls.output1.mv_temp(t_kelvin)

        # Activate heating range in Lakeshore
        if temperature < 70:
            yield from bps.mv(ls.output1.status, 3)
        else:
            yield from bps.mv(ls.output1.status, 3)

        # Equalise temperature
        print(f"Equalising temperature to {temperature:.0f} deg C")
        start = time.time()
        temp = ls.input_A.get()
        while abs(temp - t_kelvin) > 5:
            print("Difference: {:.1f} K".format(abs(temp - t_kelvin)))
            yield from bps.sleep(10)
            temp = ls.input_A.get()
            
            # Escape the loop if too much time passes
            if time.time() - start > 15 * 60:
                temp = t_kelvin
        print(
            "Time needed to equilibrate: {:.1f} min".format((time.time() - start) / 60)
        )

        # Wait extra time depending on temperature
        if (56 < temperature) and (temperature < 160):
            yield from bps.sleep(300)
        elif 160 <= temperature:
            yield from bps.sleep(600)

        # Read T and convert to deg C
        temp_degC = ls.input_A.get() - 273.15
        temp = str(np.round(float(temp_degC), 1)).zfill(5)

        for sdd in saxs_dist:
            yield from bps.mv(pil1m_pos.z, sdd)

            SAXS_setup = saxs_dict[sdd]
            RE.md['SAXS_setup'] = SAXS_setup
            bs_pos = SAXS_setup['bs_pos']
            yield from bps.mv(pil1m_bs_rod.x, bs_pos)
            print(SAXS_setup)


            for wa in waxs_arc:
                yield from bps.mv(waxs, wa)

                dets = [pil900KW] if waxs.arc.position < 15 else [pil1M, pil900KW]
                det_exposure_time(t, t)

                condition = (
                    ( 19 < waxs.arc.position )
                    and ( waxs.arc.position < 21 )
                    and ( temperature == temperatures[0] )
                    and ( sdd == saxs_dist[0] )
                )

                if condition:
                    yield from atten_move_in()
                    yield from bps.mv(pil1m_bs_rod.x, bs_pos + 5)
                    yield from bps.mv(piezo.x, dbeam_x,
                                      piezo.y, dbeam_y)

                    sample_name = f'empty_{temp}degC_-attn-direct'
                    sample_id(user_name='test', sample_name=sample_name)
                    print(f"\n\n\n\t=== Sample: {sample_name} ===")
                    yield from bp.count([pil1M])
                    stats1_direct = db[-1].table(stream_name='primary')['pil1M_stats1_total'].values[0]

                    yield from bps.mv(pil1m_bs_rod.x, bs_pos)
                    yield from atten_move_out()

                for name, x, y in zip(names, piezo_x, piezo_y):
                    yield from bps.mv(piezo.x, x,
                                      piezo.y, y)

                    # Scan along the capillary
                    for i in range(points):

                        new_y = y + i * dy

                        yield from bps.mv(piezo.y, new_y)

                        if (condition and i == 0):

                            # Take transmission
                            yield from atten_move_in()

                            # Sample
                            yield from bps.mv(pil1m_bs_rod.x, bs_pos + 5)
                            sample_name = f'{name}_loc{i}-attn-sample'
                            sample_id(user_name='test', sample_name=sample_name)
                            print(f"\n\n\t=== Sample: {sample_name} ===")
                            yield from bp.count([pil1M])
                            stats1_sample = db[-1].table(stream_name='primary')['pil1M_stats1_total'].values[0]

                            # Transmission
                            trans = np.round( stats1_sample / stats1_direct, 5)

                            # Revert configuraton
                            yield from bps.mv(pil1m_bs_rod.x, bs_pos)
                            yield from atten_move_out()
                        else:
                            trans = 0

                        # Take normal scans
                        yield from bps.mv(piezo.x, x)
                        sample_name = f'{name}_{temp}degC{get_scan_md()}_loc{i}_trs{trans}'
                        sample_id(user_name=user_name, sample_name=sample_name)
                        print(f"\n\n\n\t=== Sample: {sample_name} ===")
                        yield from bp.count(dets)

        saxs_dist = saxs_dist[::-1]

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)

    # Turn off the heating and set temperature to 23 deg C
    yield from turn_off_heating()




def guorong_temperature_2023_2_redo(t=1, prefix='test'):
    """
    Hard X-ray WAXS and SAXS Lakeshore heating stage
    at multiple SAXS detector distances.
    Measure transmission only during the first run
    """
    # yield from bps.sleep(1500)
    
    names =   [ 'cap', 'bkg_CB', 'bkg_Tol', 'P3HT_CB', 'P3HT_Tol', 'PffBT_CB']
    piezo_x = [-23550,  -10850,      1900,     14350,      27450,      40300]   
    piezo_y = [ -9500,   -9100,     -8800,     -8300,      -7900,      -7300]
    piezo_z = [  2700,    2700,      2700,      2700,       2700,       2700]

    names =   [ 'PffBT_CB']
    piezo_x = [      40100]   
    piezo_y = [      -7700]
    piezo_z = [       2700]

    assert len(names)   == len(piezo_x), f"Wrong list lenghts"
    assert len(piezo_x) == len(piezo_y), f"Wrong list lenghts"
    assert len(piezo_x) == len(piezo_z), f"Wrong list lenghts"

    waxs_arc = [20, 0]

    y_off = [0, 200]

    for name, x, y, z in zip(names, piezo_x, piezo_y, piezo_z):
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(piezo.z, z)

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)

            dets = [pil900KW] if waxs.arc.position < 15 else [pil1M, pil900KW]
            det_exposure_time(t, t)
            
            for yy, y_of in enumerate(y_off):
                yield from bps.mv(piezo.y, y + y_of)

                name_fmt = "{sample}_pos{loc}_wa{wax}"
                sample_name = name_fmt.format(sample=name + '_' + prefix, loc="%.2d"%yy, wax=wa)
                sample_id(user_name="GM", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                
                yield from bp.count(dets)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)

    # Turn off the heating and set temperature to 23 deg C
    # yield from turn_off_heating()

def night_guorong(t=1):
    yield from bps.sleep(600)

    yield from guorong_temperature_2023_2_redo(t=1, prefix='150C')

    yield from turn_off_heating()
    yield from bps.sleep(10800)
    
    yield from guorong_temperature_2023_2_redo(t=1, prefix='RT_afterheating')














def wang_temperature_tender_2025_1(t=5):
    """
    Tender X-ray WAXS and SAXS Lakeshore heating stage, coarse energies
    For reference: 2470 eV, low divergence, in vacuum, SAXS sdd 1.6 m
    """
    
    # names =   ['sa00', 'sa04',  'sa10',  'sa15',  'sa06',   'sa16',  'sa03',  'sa13', 'sa05', 'sa14','empty']       
    # piezo_x = [ 44800,  37200,   26100,   17300,    9600,      700,   -6500,  -16100, -26400, -35400, -42000]   
    # piezo_y = [ -5500,  -4500,   -5200,   -5200,   -4500,    -4700,   -3800,   -4400,  -4700,  -4000,  -4700]

    
    names =   ['sa03']       
    piezo_x = [   -6500]   
    piezo_y = [   -3800]


    assert len(names)   == len(piezo_x), f"Wrong list lenghts"
    assert len(piezo_x) == len(piezo_y), f"Wrong list lenghts"

    user_name = "YW"
    temperatures = [180, 190, 200, 210, 220] #[25, 180]
    waxs_arc = [20, 0]

    # energies = [2470]
    energies = [2470, 2472, 2474, 2475, 2476, 2477, 2478, 2480]

    # Read T and convert to deg C
    temp_degC = ls.input_A.get() - 273.15

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)

        dets = [pil900KW] if waxs.arc.position < 15 else [pil1M, pil900KW]
        det_exposure_time(t, t)

        for name, x, y in zip(names, piezo_x, piezo_y):
            # if name == 
            yield from bps.mv(piezo.x, x,
                              piezo.y, y)

            for e in energies:
                yield from bps.mv(energy, e)
                yield from bps.sleep(2)
                if xbpm2.sumX.get() < 50:
                    yield from bps.sleep(2)
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
            
                # Metadata
                #e = energy.position.energy / 1000
                temp = str(np.round(float(temp_degC), 1)).zfill(5)
                wa = str(np.round(float(wa), 1)).zfill(4)
                sdd = pil1m_pos.z.position / 1000

                # Sample name
                name_fmt = ("{sample}_{temp}degC_{energy}eV_wa{wax}_sdd{sdd}m_expt{t}s")
                sample_name = name_fmt.format(sample = name,energy = "%.2f" % e ,temp = temp,
                                              wax = wa, sdd = "%.1f" % sdd, t = t,)
                sample_name = sample_name.translate({ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ =, "})
                print(f"\n\n\n\t=== Sample: {sample_name} ===")
                sample_id(user_name=user_name, sample_name=sample_name)
                
                yield from bp.count(dets)

            yield from bps.mv(energy, 2470)
            yield from bps.sleep(2)



    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)

    # Turn off the heating and set temperature to 23 deg C
    yield from turn_off_heating()








import bluesky.preprocessors as bpp
import bluesky.plans as bp
import bluesky.plan_stubs as bps
from ophyd import Signal

def energy_Sedge_scan(t=1, name="Test", ai_list: list[int]|None = None, xstep=10, waxs_arc = (0, 20)):
    '''
    Study the beam damage on 1 film to define the opti;am experimental conitions.
    '''

    # names =   ['sa00', 'sa04',  'sa10',  'sa15',  'sa06',   'sa16',  'sa03',  'sa13', 'sa05', 'sa14','empty']       
    # piezo_x = [ 45000,  37200,   26500,   17300,   10200,      700,   -6500,  -16000, -26200, -35000, -42000]   
    # piezo_y = [ -5100,  -4200,   -5200,   -4900,   -4900,    -4900,   -4200,   -5100,  -5100,  -4300,  -5100]

    names =   ['sa00', 'sa04',  'sa10',  'sa15',  'sa06',   'sa16',  'sa03',  'sa13', 'sa05', 'sa14','empty']       
    piezo_x = [ 45000,  37400,   26500,   17500,   10500,      700,   -6500,  -16000, -26200, -35200, -42000]   
    piezo_y = [ -5100,  -4500,   -4800,   -5000,   -4700,    -4800,   -4200,   -5000,  -4600, -3800,  -5100]

    assert len(names)   == len(piezo_x), f"Wrong list lenghts"
    assert len(piezo_x) == len(piezo_y), f"Wrong list lenghts"

    waxs_arc = [0, 20]
    # 63 energies
    energies = [2470, 2472, 2474, 2475, 2476, 2477, 2478, 2480]

    dets = [pil900KW, pil1M]
    det_exposure_time(t, t)

    s = Signal(name='target_file_name', value='')

    @bpp.stage_decorator(dets)
    @bpp.run_decorator(md={'sample_name' :'{target_file_name}'})
    def inner():

        # Read T and convert to deg C
        temp_degC = ls.input_A.get() - 273.15

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)

            for name, x, y in zip(names, piezo_x, piezo_y):
                yield from bps.mv(piezo.x, x,piezo.y, y)

                for e in energies:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)

                    if xbpm2.sumX.get() < 50:
                        yield from bps.mv(energy, e)
                
                    # Metadata
                    #e = energy.position.energy / 1000
                    temp = str(np.round(float(temp_degC), 1)).zfill(5)
                    wa = str(np.round(float(wa), 1)).zfill(4)
                    sdd = pil1m_pos.z.position / 1000

                    print(temp, wa, sdd)

                    # Sample name
                    name_fmt = ("{sample}_{temp}degC_{energy}eV_wa{wax}_sdd{sdd}m_up")
                    sample_name = name_fmt.format(sample = name,energy = "%.2f" % e ,temp = temp, wax = wa, sdd = "%.1f" % sdd)
                    sample_name = sample_name.translate({ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ =, "})
                    print(f"\n\n\n\t=== Sample: {sample_name} ===")
                    s.put(sample_name)
                    
                    yield from bps.trigger_and_read(dets + [energy, waxs, xbpm2, xbpm3, ls.input_A] + [s])

                yield from bps.mv(energy, 2470)
                yield from bps.sleep(2)

    (yield from inner())









import bluesky.preprocessors as bpp
import bluesky.plans as bp
import bluesky.plan_stubs as bps
from ophyd import Signal

def energy_Sedge_scan_withdetmotion(t=1, name="Test", ai_list: list[int]|None = None, xstep=10, waxs_arc = (0, 20)):
    '''
    Study the beam damage on 1 film to define the opti;am experimental conitions.
    '''

    # names =   ['sa00', 'sa04',  'sa10',  'sa15',  'sa06',   'sa16',  'sa03',  'sa13', 'sa05', 'sa14','empty']       
    # piezo_x = [ 45000,  37200,   26500,   17300,   10200,      700,   -6500,  -16000, -26200, -35000, -42000]   
    # piezo_y = [ -5100,  -4200,   -5200,   -4900,   -4900,    -4900,   -4200,   -5100,  -5100,  -4300,  -5100]

    names =   ['sa00', 'sa04',  'sa10',  'sa15',  'sa06',   'sa16',  'sa03',  'sa13', 'sa05', 'sa14','empty']       
    piezo_x = [ 45000,  37400,   26500,   17500,   10500,      700,   -6500,  -16000, -26200, -35200, -42000]   
    piezo_y = [ -5100,  -4500,   -4800,   -5000,   -4700,    -4800,   -4200,   -5000,  -4300, -3800,  -5100]

    assert len(names)   == len(piezo_x), f"Wrong list lenghts"
    assert len(piezo_x) == len(piezo_y), f"Wrong list lenghts"

    waxs_arc = [20, 0]
    # 63 energies
    energies = [2470, 2472, 2474, 2475, 2476, 2477, 2478, 2480]

    dets = [pil900KW, pil1M]
    det_exposure_time(0.5, 2.5)

    s = Signal(name='target_file_name', value='')

    @bpp.stage_decorator(dets)
    @bpp.run_decorator(md={'sample_name' :'{target_file_name}'})
    def inner():

        # Read T and convert to deg C
        temp_degC = ls.input_A.get() - 273.15

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)
            if wa == 0:
                yield from bps.mv(pil1m_pos.x, -50)
                yield from bps.mv(pil1m_pos.y, -61)

                for name, x, y in zip(names, piezo_x, piezo_y):
                    yield from bps.mv(piezo.x, x,piezo.y, y)

                    for e in energies:
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)

                        if xbpm2.sumX.get() < 50:
                            yield from bps.mv(energy, e)
                    
                        # Metadata
                        #e = energy.position.energy / 1000
                        temp = str(np.round(float(temp_degC), 1)).zfill(5)
                        wa = str(np.round(float(wa), 1)).zfill(4)
                        sdd = pil1m_pos.z.position / 1000

                        print(temp, wa, sdd)

                        # Sample name
                        name_fmt = ("{sample}_{temp}degC_{energy}eV_wa{wax}_sdd{sdd}m")
                        sample_name = name_fmt.format(sample = name,energy = "%.2f" % e ,temp = temp, wax = wa, sdd = "%.1f" % sdd)
                        sample_name = sample_name.translate({ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ =, "})
                        print(f"\n\n\n\t=== Sample: {sample_name} ===")
                        s.put(sample_name)
                        
                        yield from bps.trigger_and_read(dets + [energy, waxs, xbpm2, xbpm3, ls.input_A] + [s])

                    yield from bps.mv(energy, 2470)
                    yield from bps.sleep(2)

            if wa == 20:
                yield from bps.mv(pil1m_pos.x, -52)
                yield from bps.mv(pil1m_pos.y, -59)

                for name, x, y in zip(names, piezo_x, piezo_y):
                    yield from bps.mv(piezo.x, x,piezo.y, y)

                    for e in energies:
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)

                        if xbpm2.sumX.get() < 50:
                            yield from bps.mv(energy, e)
                    
                        # Metadata
                        #e = energy.position.energy / 1000
                        temp = str(np.round(float(temp_degC), 1)).zfill(5)
                        wa = str(np.round(float(wa), 1)).zfill(4)
                        sdd = pil1m_pos.z.position / 1000

                        print(temp, wa, sdd)

                        # Sample name
                        name_fmt = ("{sample}_{temp}degC_{energy}eV_wa{wax}_sdd{sdd}m_dl")
                        sample_name = name_fmt.format(sample = name,energy = "%.2f" % e ,temp = temp, wax = wa, sdd = "%.1f" % sdd)
                        sample_name = sample_name.translate({ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ =, "})
                        print(f"\n\n\n\t=== Sample: {sample_name} ===")
                        s.put(sample_name)
                        
                        yield from bps.trigger_and_read(dets + [energy, waxs, xbpm2, xbpm3, ls.input_A] + [s])

                    yield from bps.mv(energy, 2470)
                    yield from bps.sleep(2)

            if wa == 20:
                yield from bps.mv(pil1m_pos.x, -52)
                yield from bps.mv(pil1m_pos.y, -61)

                for name, x, y in zip(names, piezo_x, piezo_y):
                    yield from bps.mv(piezo.x, x,piezo.y, y)

                    for e in energies:
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)

                        if xbpm2.sumX.get() < 50:
                            yield from bps.mv(energy, e)
                    
                        # Metadata
                        #e = energy.position.energy / 1000
                        temp = str(np.round(float(temp_degC), 1)).zfill(5)
                        wa = str(np.round(float(wa), 1)).zfill(4)
                        sdd = pil1m_pos.z.position / 1000

                        print(temp, wa, sdd)

                        # Sample name
                        name_fmt = ("{sample}_{temp}degC_{energy}eV_wa{wax}_sdd{sdd}m_ul")
                        sample_name = name_fmt.format(sample = name,energy = "%.2f" % e ,temp = temp, wax = wa, sdd = "%.1f" % sdd)
                        sample_name = sample_name.translate({ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ =, "})
                        print(f"\n\n\n\t=== Sample: {sample_name} ===")
                        s.put(sample_name)
                        
                        yield from bps.trigger_and_read(dets + [energy, waxs, xbpm2, xbpm3, ls.input_A] + [s])

                    yield from bps.mv(energy, 2470)
                    yield from bps.sleep(2)

            if wa == 20:
                yield from bps.mv(pil1m_pos.x, -50)
                yield from bps.mv(pil1m_pos.y, -61)

                for name, x, y in zip(names, piezo_x, piezo_y):
                    yield from bps.mv(piezo.x, x,piezo.y, y)

                    for e in energies:
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)

                        if xbpm2.sumX.get() < 50:
                            yield from bps.mv(energy, e)
                    
                        # Metadata
                        #e = energy.position.energy / 1000
                        temp = str(np.round(float(temp_degC), 1)).zfill(5)
                        wa = str(np.round(float(wa), 1)).zfill(4)
                        sdd = pil1m_pos.z.position / 1000

                        print(temp, wa, sdd)

                        # Sample name
                        name_fmt = ("{sample}_{temp}degC_{energy}eV_wa{wax}_sdd{sdd}m_ur")
                        sample_name = name_fmt.format(sample = name,energy = "%.2f" % e ,temp = temp, wax = wa, sdd = "%.1f" % sdd)
                        sample_name = sample_name.translate({ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ =, "})
                        print(f"\n\n\n\t=== Sample: {sample_name} ===")
                        s.put(sample_name)
                        
                        yield from bps.trigger_and_read(dets + [energy, waxs, xbpm2, xbpm3, ls.input_A] + [s])

                    yield from bps.mv(energy, 2470)
                    yield from bps.sleep(2)


            if wa == 20:
                yield from bps.mv(pil1m_pos.x, -50)
                yield from bps.mv(pil1m_pos.y, -59)

                for name, x, y in zip(names, piezo_x, piezo_y):
                    yield from bps.mv(piezo.x, x,piezo.y, y)

                    for e in energies:
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)

                        if xbpm2.sumX.get() < 50:
                            yield from bps.mv(energy, e)
                    
                        # Metadata
                        #e = energy.position.energy / 1000
                        temp = str(np.round(float(temp_degC), 1)).zfill(5)
                        wa = str(np.round(float(wa), 1)).zfill(4)
                        sdd = pil1m_pos.z.position / 1000

                        print(temp, wa, sdd)

                        # Sample name
                        name_fmt = ("{sample}_{temp}degC_{energy}eV_wa{wax}_sdd{sdd}m_dr")
                        sample_name = name_fmt.format(sample = name,energy = "%.2f" % e ,temp = temp, wax = wa, sdd = "%.1f" % sdd)
                        sample_name = sample_name.translate({ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ =, "})
                        print(f"\n\n\n\t=== Sample: {sample_name} ===")
                        s.put(sample_name)
                        
                        yield from bps.trigger_and_read(dets + [energy, waxs, xbpm2, xbpm3, ls.input_A] + [s])

                    yield from bps.mv(energy, 2470)
                    yield from bps.sleep(2)

    (yield from inner())


    t_kelvin = 25 + 273.15
    yield from ls.output1.mv_temp(t_kelvin)
    yield from ls.output1.turn_off()
def waxs_S_edge_cherun(t=1):

    dets = [pil300KW, pil1M]

    # yield from bps.mv(stage.th, 0)
    # yield from bps.mv(stage.y, 6)
    # names = ['bar1_sa01_2','bar1_sa02_2','bar1_sa03_2','bar1_sa04_2','bar1_sa05_2','bar1_sa06_2','bar1_sa07_2','bar1_sa08_2'
    # ,'bar1_sa09_2','bar1_sa10_2','bar1_sa11_2','bar1_sa12_2','bar1_sa13_2','bar1_sa14_2']

    # x = [51700,43700,35700,27700,19600,11700,4700,-4200,-12200,-20200,-28200,-36200,-44200,-52200]
    # y = [7600, 7600, 7900, 7900, 7900, 8200, 8771, 8900, 8300, 8700,  8800,  9100,  9300,  9400]

    # energies = np.arange(2450, 2476, 5).tolist() + np.arange(2476, 2486, 0.5).tolist() + np.arange(2486, 2496, 2).tolist()+ np.arange(2496, 2511, 5).tolist()
    # waxs_arc = np.linspace(6.5, 13, 2)

    # for wa in waxs_arc:
    #     yield from bps.mv(waxs, wa)
    #     for name, xs, ys in zip(names, x, y):
    #         yield from bps.mv(piezo.x, xs)
    #         yield from bps.mv(piezo.y, ys)

    #         # yss = np.linspace(ys, ys + 380, 20)
    #         # xss = np.array([xs, xs + 250, xs + 500])

    #         # yss, xss = np.meshgrid(yss, xss)
    #         # yss = yss.ravel()
    #         # xss = xss.ravel()

    #         det_exposure_time(t,t)
    #         name_fmt = '{sample}_{energy}eV_wa{wax}_bpm{xbpm}'
    #         for e in energies:
    #             yield from bps.mv(energy, e)
    #             yield from bps.sleep(1)

    #             # yield from bps.mv(piezo.y, ysss)
    #             # yield from bps.mv(piezo.x, xsss)

    #             bpm = xbpm2.sumX.value

    #             sample_name = name_fmt.format(sample=name, energy='%6.2f'%e, wax = wa, xbpm = '%4.3f'%bpm)
    #             sample_id(user_name='GF', sample_name=sample_name)
    #             print(f'\n\t=== Sample: {sample_name} ===\n')
    #             yield from bp.count(dets, num=1)

    #         yield from bps.mv(energy, 2490)
    #         yield from bps.mv(energy, 2470)
    #         yield from bps.mv(energy, 2450)

    # yield from bps.mv(stage.th, 0)
    # yield from bps.mv(stage.y, 0)

    # names = ['bar2_sa01','bar2_sa02','bar2_sa03','bar2_sa04','bar2_sa05','bar2_sa06','bar2_sa07','bar2_sa08','bar2_sa09'
    # ,'bar2_sa10','bar2_sa11','bar2_sa12','bar2_sa13','bar2_sa14']
    # x = [51800,43300,35200,27300,19200,11800,3300,-4600,-12600,-20600, -28600, -36600, -44600, -52600]
    # y = [3500, 3600, 3700, 3800, 4100, 4800, 4400, 4800, 4900,  5000,   5100,   5500,   5500,  5500]

    # energies = np.arange(2450, 2476, 5).tolist() + np.arange(2476, 2486, 1).tolist() + np.arange(2486, 2496, 3).tolist()+ np.arange(2496, 2511, 5).tolist()
    # waxs_arc = np.linspace(0, 13, 3)

    # for wa in waxs_arc:
    #     yield from bps.mv(waxs, wa)
    #     for name, xs, ys in zip(names, x, y):
    #         yield from bps.mv(piezo.x, xs)
    #         yield from bps.mv(piezo.y, ys)

    #         det_exposure_time(t,t)
    #         name_fmt = '{sample}_{energy}eV_wa{wax}_bpm{xbpm}'
    #         for e in energies:
    #             yield from bps.mv(energy, e)
    #             yield from bps.sleep(1)

    #             bpm = xbpm2.sumX.value

    #             sample_name = name_fmt.format(sample=name, energy='%6.2f'%e, wax = wa, xbpm = '%4.3f'%bpm)
    #             sample_id(user_name='GF', sample_name=sample_name)
    #             print(f'\n\t=== Sample: {sample_name} ===\n')
    #             yield from bp.count(dets, num=1)

    #         yield from bps.mv(energy, 2490)
    #         yield from bps.mv(energy, 2470)
    #         yield from bps.mv(energy, 2450)

    # yield from bps.mv(stage.th, 0)
    # yield from bps.mv(stage.y, 0)
    # names = ['bar3_sa01','bar3_sa02','bar3_sa03','bar3_sa04','bar3_sa05','bar3_sa06','bar3_sa07','bar3_sa08','bar3_sa09'
    # ,'bar3_sa10','bar3_sa11','bar3_sa12','bar3_sa13','bar3_sa14']
    # x = [51800,43600,35900,27900,19600,11800,4000, -4100, -12100, -20100,-28100,-36400,-44100,-52100]
    # y = [-7300,-7100,-7100,-6900,-6700,-6500,-6000,-6200, -6000,  -5800, -5600, -5300, -5200, -4900]

    names = ["bar3_sa07_2"]
    x = [4000]
    y = [-5000]

    energies = (
        np.arange(2450, 2476, 5).tolist()
        + np.arange(2476, 2486, 1).tolist()
        + np.arange(2486, 2496, 3).tolist()
        + np.arange(2496, 2511, 5).tolist()
    )
    waxs_arc = np.linspace(0, 32.5, 6)

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)
        for name, xs, ys in zip(names, x, y):
            yield from bps.mv(piezo.x, xs)
            yield from bps.mv(piezo.y, ys)

            det_exposure_time(t, t)
            name_fmt = "{sample}_{energy}eV_wa{wax}_bpm{xbpm}"
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

            yield from bps.mv(energy, 2490)
            yield from bps.mv(energy, 2470)
            yield from bps.mv(energy, 2450)


def nexafs_S_edge_cherun(t=1):

    yield from bps.mv(waxs, 52.5)
    dets = [pil300KW]

    names = ["nexafs_sam2_ex_situ"]

    # energies = np.arange(2460, 2521, 1).tolist()
    energies = -2.5 + np.asarray(
        np.arange(2450, 2476, 5).tolist()
        + np.arange(2476, 2486, 0.25).tolist()
        + np.arange(2486, 2496, 1).tolist()
        + np.arange(2496, 2511, 5).tolist()
    )
    ys = np.linspace(320, 1320, 59)

    for name in names:

        # yield from bps.mv(piezo.th, 1.5)

        det_exposure_time(t, t)
        name_fmt = "{sample}_{energy}eV_wa52.5_bpm{xbpm}"
        for e, yss in zip(energies, ys):
            yield from bps.mv(piezo.y, yss)
            yield from bps.mv(energy, e)
            yield from bps.sleep(1)
            bpm = xbpm2.sumX.value
            sample_name = name_fmt.format(
                sample=name, energy="%6.2f" % e, xbpm="%4.3f" % bpm
            )
            sample_id(user_name="GF", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)

        yield from bps.mv(energy, 2490)
        yield from bps.mv(energy, 2470)
        yield from bps.mv(energy, 2450)


def instec_insitu_hard_xray(t=0.5):

    dets = [pil900KW, pil1M]
    det_exposure_time(t, t)

    name = "sampleA"
    # temperatures = np.arange(150, 130, -5).tolist() + np.arange(130, 115, -1).tolist() + np.arange(115, 100, -0.5).tolist()
    # temperatures = np.arange(140, 130, -5).tolist() + np.arange(130, 115, -1).tolist() + np.arange(115, 100, -0.5).tolist()
    temperatures = np.arange(119, 100, -1).tolist()
    temperatures = np.arange(90, 84, -1).tolist()

    # temperatures = [120]
    waxs_arc = np.linspace(0, 19.5, 4)

    for i_t, t in enumerate(temperatures):

        t_kelvin = t + 273.15
        yield from ls.output3.mv_temp(t_kelvin)
        yield from bps.sleep(120)

        if i_t != 0:
            yield from bps.mvr(stage.y, 0.025)

        temp = ls.input_C.value
        while abs(temp - t_kelvin) > 0.25:
            print(abs(temp - t_kelvin))
            yield from bps.sleep(10)
            temp = ls.input_A.value

        temp_C = temp - 273.15
        if waxs.arc.position > 15:
            wa_arc = waxs_arc[::-1]
        else:
            wa_arc = waxs_arc

        for j, wa in enumerate(wa_arc):
            yield from bps.mv(waxs, wa)
            name_fmt = "{sample}_{temperature}C_wa{waxs}_sdd1.6m"
            sample_name = name_fmt.format(
                sample=name, offset=0, temperature="%3.1f" % temp_C, waxs="%2.1f" % wa
            )
            print(f"\n\t=== Sample: {sample_name} ===\n")
            sample_id(user_name=name, sample_name=sample_name)
            yield from bp.count(dets, num=1)


def instec_insitu_tender_xray(t=0.5):

    dets = [pil300KW, pil1M]
    det_exposure_time(t, t)

    energies = [2460, 2475]

    x = -0.87

    name = "sampleB_unaligned"

    temperatures = (
        np.arange(140, 125, -5).tolist()
        + np.arange(125, 101, -2).tolist()
        + np.arange(101, 90, -1).tolist()
    )
    waxs_arc = np.linspace(0, 19.5, 4)

    for i_t, t in enumerate(temperatures):

        t_kelvin = t + 273.15
        yield from ls.output3.mv_temp(t_kelvin)

        if i_t != 0:
            yield from bps.mvr(stage.y, 0.025)
            yield from bps.sleep(120)

        temp = ls.input_A.value
        while abs(temp - t_kelvin) > 0.25:
            print(abs(temp - t_kelvin))
            yield from bps.sleep(10)
            temp = ls.input_A.value

        temp_C = temp - 273.15
        if waxs.arc.position > 15:
            wa_arc = waxs_arc[::-1]
        else:
            wa_arc = waxs_arc

        for j, wa in enumerate(wa_arc):
            yield from bps.mv(waxs, wa)

            for k, energ in enumerate(energies):
                yield from bps.mv(energy, energ)
                yield from bps.sleep(1)
                # yield from bps.mv(stage.x, x + (k * 0.1))

                name_fmt = "{sample}_{temperature}C_wa{waxs}_sdd1.6m_{ener}eV"
                sample_name = name_fmt.format(
                    sample=name,
                    offset=0,
                    temperature="%3.1f" % temp_C,
                    waxs="%2.1f" % wa,
                    ener=energ,
                )
                print(f"\n\t=== Sample: {sample_name} ===\n")
                sample_id(user_name=name, sample_name=sample_name)
                yield from bp.count(dets, num=1)

            # yield from bps.mv(energy, 2480)

    yield from ls.output3.mv_temp(303.15)


def single_scan_instec_insitu_hard_2022_2(t=0.5):
    """
    Instec stage macro for single measurement

    Temperature for the measurement has to be driven from CSS screen,
    once the temperature equilibrates, run this to measure.

    While changing samples, disengage the heater, click and change
    Range X to OFF in Lakeshore CSS tab.
    """
    user_name = "user_name"
    name = "Silver_Behenate"

    # Correct names just in case
    name = name.translate({ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ "})
    user_name = user_name.translate({ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ "})

    det_exposure_time(t, t)
    waxs_arc = [0, 20]

    # Read T and convert to deg C
    temp_degC = ls.input_C.get() - 273.15

    # Save time on WAXS arc movement
    waxs_angles = waxs_arc if waxs.arc.position < 15 else waxs_arc[::-1]

    for wa in waxs_angles:
        yield from bps.mv(waxs, wa)
        dets = [pil900KW] if wa < 15 else [pil900KW, pil1M]

        # Metadata
        e = energy.position.energy / 1000
        temp = str(np.round(float(temp_degC), 1)).zfill(5)
        wa = str(np.round(float(wa), 1)).zfill(4)
        sdd = pil1m_pos.z.position / 1000
        scan_id = db[-1].start["scan_id"] + 1
        # bpm = xbpm3.sumX.get()

        # Sample name
        name_fmt = "{sample}_{energy}keV_temp{temp}degC_wa{wax}_sdd{sdd}m_id{scan_id}"
        sample_name = name_fmt.format(
            sample=name,
            energy="%.2f" % e,
            temp=temp,
            wax=wa,
            sdd="%.1f" % sdd,
            scan_id=scan_id,
        )
        print(f"\n\t=== Sample: {sample_name} ===\n")
        sample_id(user_name=name, sample_name=sample_name)
        yield from bp.count(dets)


def tender_single_scan_instec_insitu_2022_2(t=0.5):
    """
    Instec stage macro for single measurement

    Temperature for the measurement has to be driven from CSS screen,
    once the temperature equilibrates, run this to measure.

    While changing samples, disengage the heater, click and change
    Range X to OFF in Lakeshore CSS tab.
    """

    user_name = "RT12127A"
    name = "S_100p"

    # Correct names just in case
    name = name.translate({ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ "})
    user_name = user_name.translate({ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ "})

    det_exposure_time(t, t)
    waxs_arc = [3]

    # Read T and convert to deg C
    temp_degC = ls.input_C.get() - 273.15

    # Save time on WAXS arc movement
    waxs_angles = waxs_arc if waxs.arc.position < 15 else waxs_arc[::-1]

    for wa in waxs_angles:
        yield from bps.mv(waxs, wa)
        dets = [pil900KW] if wa < 15 else [pil900KW, pil1M]

        # Metadata
        e = energy.position.energy
        temp = str(np.round(float(temp_degC), 1)).zfill(5)
        wa = str(np.round(float(wa), 1)).zfill(4)
        sdd = pil1m_pos.z.position / 1000
        scan_id = db[-1].start["scan_id"] + 1
        # bpm = xbpm3.sumX.get()

        # Sample name
        name_fmt = "{sample}_{energy}eV_temp{temp}degC_wa{wax}_sdd{sdd}m_id{scan_id}"
        sample_name = name_fmt.format(
            sample=user_name,
            energy="%.2f" % e,
            temp=temp,
            wax=wa,
            sdd="%.1f" % sdd,
            scan_id=scan_id,
        )
        print(f"\n\t=== Sample: {sample_name} ===\n")
        sample_id(user_name=user_name, sample_name=sample_name)
        yield from bp.count(dets)

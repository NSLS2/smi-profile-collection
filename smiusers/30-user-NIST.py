def Rb_tswaxs(
    t=0.5,
    waxs_arc=[13],
    energies=[
        15150,
        15160,
        15170,
        15180,
        15190,
        15191,
        15192,
        15193,
        15194,
        15195,
        15196,
        15197,
        15198,
        15199,
        15200,
        15201,
        15202,
        15203,
        15204,
        15205,
        15210,
        15215,
        15220,
        15230,
        15240,
        15250,
    ],
):
    # holder 1

    # sample_list = ['F_D230','F_D230_epoxy','F_D400','F_D230_OG','F_D2000','M6B1','M6B2','M6B3','M8B1','M8B2','M8B3','M10B1','M10B2','M10B3','M9B1','M9B2','M9B3','TMCMPD1','TMCMPD2','M7B1','M7B2','M7B3','Kapton_tape1','Kapton_tape1']
    # x_list = [-43000,-37000,-32000,-26000,-20500,-14500,-14500,-13500,-10500,-10500,-11000,-5000,-4000,-3000,2500,2500,3450,11500,10500,15000,15000,14500,18500,19500]
    # y_list = [-250,-250,-250,-250,-250,-250,500,500,1000,500,-500,-500,500,1000,1000,500,750,750,750,750,250,700,700,700]

    # holder 2
    # sample_list = ['water_blank_1','water_blank_2','M6wet_1','M6wet_2','M8wet_1','M8wet_2','M10wet_1','M10wet_2','water_blank_inM10','S_D230_1','S_D230_2','S_D230E_1','S_D230E_2','S_D400_1','S_D400_2','S_D2000_1','S_D2000_2','S_D230_OG_1','S_D230_OG_2','M6_dry_SANS_1','M6_dry_SANS_2','M6_dry_SANS_3','M7_dry_SANS_1','M7_dry_SANS_2','M7_dry_SANS_3','M10_dry_SANS_1','M10_dry_SANS_2','M10_dry_SANS_3']
    # x_list = [-18200,-18200,-12000,-12000,-5600,-5600,700,700,700,13750,13750,20250,20250,26125,26125,32750,32750,39000,39000,-40700,-41700,-39700,-33700,-32700,-31500,-28700,-27700,-25700]
    # y_list = [3000,2000,2000,3500,3500,1000,-500,500,3000,0,3000,0,3000,0,3000,0,3000,1000,3000,2500,1500,3000,3000,1500,3000,3000,1000,1500]
    # def giwaxsTempSingleWaxsSeries(x_list,y_list,th_list,chi_list,sample_list,waxs_arc,num,t=1,user='BP'):

    # holder 3
    # sample_list = ['6SS_A','6SS_B','6SH_A','6SH_B','7SS_A','7SS_B','8SH_A','8SH_B','10SS_A','10SS_B','10SH_A','10SH_B','6CS_A','6CS_B','10CS_A','10CS_B','airblank']
    # x_list = [-42000,-42000,-34000,-32000,-24000,-22000,-16000,-15000,-9000,-10000,-2500,-2500,5500,5500,13500,14500,18500]
    # y_list = [0,-1000,0,0,0,0,-500,-500,-500,500,500,-500,0,1000,1000,0,1000]

    # holder 3, no replicates
    sample_list = [
        "6SS_A",
        "6SH_A",
        "7SS_A",
        "7SS_B",
        "8SH_A",
        "10SS_B",
        "10SH_A",
        "6CS_B",
        "10CS_B",
        "airblank",
    ]
    x_list = [-42000, -34000, -24000, -22000, -16000, -10000, -2500, 5500, 14500, 18500]
    y_list = [0, 0, 0, 0, -500, 500, 500, 1000, 0, 1000]

    # sample_list = ['6SH_A','7SS_A','7SS_B','8SH_A','10SS_B','10SH_A','6CS_B','10CS_B','airblank']
    # x_list = [-34000,-24000,-22000,-16000,-10000,-2500,5500,14500,18500]
    # y_list = [0,0,0,-500,500,500,1000,0,1000]

    user = "PB"
    # print(num)

    for waxspos in waxs_arc:
        for x, y, sample in zip(
            x_list, y_list, sample_list
        ):  # loop over samples on bar
            yield from bps.mv(piezo.x, x)  # move to next sample
            yield from bps.mv(piezo.y, y)  # move to next sample
            # yield from bps.mv(piezo.th, th) #move to next sample
            # yield from bps.mv(piezo.ch, chi) #move to next sample
            # print(x)
            # th_meas = 0.12 + piezo.th.position
            # th_real = 0.12

            # yield from bps.mv(piezo.th,th_meas)
            yield from bps.mv(
                waxs, waxspos
            )  # move the waxs dectector to the measurement position
            waxs_arc = [waxspos]
            # temp = ls.ch1_read.value
            dets = [pil300KW, pil1M]
            det_exposure_time(t, t)
            # yield from bp.scan(dets, waxs, *waxs_arc)# should just be a single point "scan"

            if np.int(waxs.arc.position) < 6 and bsx_pos > 0:
                yield from bps.mv(waxs, waxspos)

            for e in energies:
                yield from bps.mv(energy, e)
                sample_name = "{sample}_saxs2m_waxs{waxspos:5.4f}_en{energy}".format(
                    sample=sample, waxspos=waxspos, energy=e
                )
                sample_id(user_name=user, sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)


def run_saxsmapPT(t=1):
    samples = ["AS1-120", "AS1-110NK", "AS1-110K"]
    x_list = [28500, -51000, -8000]
    y_list = [9300, 3000, 0]

    name = "PT"

    x_range = [[-6500, 11500, 73], [-10000, 10000, 81], [-14000, 14000, 113]]
    y_range = [[-19550, 950, 83], [-13250, 7250, 83], [-10250, 10250, 83]]

    # Detectors, motors:
    dets = [pil1M]  # ,pil300KW] #dets = [pil1M]#
    det_exposure_time(t, t)

    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    for x, y, sample, x_r, y_r in zip(x_list, y_list, samples, x_range, y_range):
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(piezo.y, y)
        sample_id(user_name=name, sample_name=sample)

        for xrs in np.linspace(x_r[0], x_r[1], x_r[2]):
            yield from bps.mv(piezo.x, x + xrs)
            for yrs in np.linspace(y_r[0], y_r[1], y_r[2]):
                print(yrs)
                yield from bps.mv(piezo.y, y + yrs)
                name_fmt = "{sam}_x{x}_y{y}"
                sample_name = name_fmt.format(
                    sam=sample, x="%5.5d" % (x + xrs), y="%5.5d" % (y + yrs)
                )
                sample_id(user_name=name, sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)


def tswaxs(t=15, waxs_arc=[26, 19.5, 13, 6.5, 0]):
    # holder 1

    # sample_list = ['F_D230','F_D230_epoxy','F_D400','F_D230_OG','F_D2000','M6B1','M6B2','M6B3','M8B1','M8B2','M8B3','M10B1','M10B2','M10B3','M9B1','M9B2','M9B3','TMCMPD1','TMCMPD2','M7B1','M7B2','M7B3','Kapton_tape1','Kapton_tape1']
    # x_list = [-43000,-37000,-32000,-26000,-20500,-14500,-14500,-13500,-10500,-10500,-11000,-5000,-4000,-3000,2500,2500,3450,11500,10500,15000,15000,14500,18500,19500]
    # y_list = [-250,-250,-250,-250,-250,-250,500,500,1000,500,-500,-500,500,1000,1000,500,750,750,750,750,250,700,700,700]

    # holder 2
    sample_list = [
        "water_blank_1",
        "water_blank_2",
        "M6wet_1",
        "M6wet_2",
        "M8wet_1",
        "M8wet_2",
        "M10wet_1",
        "M10wet_2",
        "water_blank_inM10",
        "S_D230_1",
        "S_D230_2",
        "S_D230E_1",
        "S_D230E_2",
        "S_D400_1",
        "S_D400_2",
        "S_D2000_1",
        "S_D2000_2",
        "S_D230_OG_1",
        "S_D230_OG_2",
        "M6_dry_SANS_1",
        "M6_dry_SANS_2",
        "M6_dry_SANS_3",
        "M7_dry_SANS_1",
        "M7_dry_SANS_2",
        "M7_dry_SANS_3",
        "M10_dry_SANS_1",
        "M10_dry_SANS_2",
        "M10_dry_SANS_3",
    ]
    x_list = [
        -18200,
        -18200,
        -12000,
        -12000,
        -5600,
        -5600,
        700,
        700,
        700,
        13750,
        13750,
        20250,
        20250,
        26125,
        26125,
        32750,
        32750,
        39000,
        39000,
        -40700,
        -41700,
        -39700,
        -33700,
        -32700,
        -31500,
        -28700,
        -27700,
        -25700,
    ]
    y_list = [
        3000,
        2000,
        2000,
        3500,
        3500,
        1000,
        -500,
        500,
        3000,
        0,
        3000,
        0,
        3000,
        0,
        3000,
        0,
        3000,
        1000,
        3000,
        2500,
        1500,
        3000,
        3000,
        1500,
        3000,
        3000,
        1000,
        1500,
    ]
    # def giwaxsTempSingleWaxsSeries(x_list,y_list,th_list,chi_list,sample_list,waxs_arc,num,t=1,user='BP'):

    user = "PB"
    # print(num)

    for waxspos in waxs_arc:
        for x, y, sample in zip(
            x_list, y_list, sample_list
        ):  # loop over samples on bar
            yield from bps.mv(piezo.x, x)  # move to next sample
            yield from bps.mv(piezo.y, y)  # move to next sample
            # yield from bps.mv(piezo.th, th) #move to next sample
            # yield from bps.mv(piezo.ch, chi) #move to next sample
            # print(x)
            # th_meas = 0.12 + piezo.th.position
            # th_real = 0.12

            # yield from bps.mv(piezo.th,th_meas)
            yield from bps.mv(
                waxs, waxspos
            )  # move the waxs dectector to the measurement position
            waxs_arc = [waxspos]
            # temp = ls.ch1_read.value
            dets = [pil300KW]  # ,pil1M]
            det_exposure_time(t, t)
            sample_name = "{sample}_nosaxs_waxs{waxspos:5.4f}".format(
                sample=sample, waxspos=waxspos
            )
            sample_id(user_name=user, sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            # yield from bp.scan(dets, waxs, *waxs_arc)# should just be a single point "scan"

            if np.int(waxs.arc.position) < 6 and bsx_pos > 0:
                yield from bps.mv(waxs, waxspos)
            yield from bp.count(dets)


def giwaxs_S_edge(t=1):
    dets = [pil300KW, pil1M]

    names = [
        "P3HT_CF",
        "P3HT_blend3",
        "P3HT_600",
        "P3HT_blend2",
        "P3MEEMT_75",
        "P3MEEMT_175",
        "P3HHT_A10",
        "P3HHT_B8",
        "BHJ_90_AS",
        "BHJ_90_AN",
    ]
    x = [-48000, -40000, -32000, -24000, -18000, -10000, -2000, 4000, 12000, 21000]

    # names_PA = ['TP100','TM100','M6','M8','M10']
    # x_PA = [-13500,-24500,-28500,-41500,-47500]

    energies = [
        2450,
        2470,
        2473,
        2475,
        2476,
        2477,
        2478,
        2479,
        2480,
        2481,
        2483,
        2485,
        2490,
        2495,
        2500,
        2510,
    ]
    waxs_arc = [15, 0]

    for name, xs in zip(names, x):
        yield from bps.mv(piezo.x, xs)

        yield from alignement_gisaxs(0.25)

        yield from bps.mvr(piezo.th, 0.7)

        det_exposure_time(t, t)
        name_fmt = "{sample}_{energy}eV_ai0.7_wa{wax}"

        for wa in waxs_arc:
            if wa == 0:
                yield from bps.mv(att2_9, "Retract")
                yield from bps.mv(att2_10, "Insert")
            else:
                yield from bps.mv(att2_10, "Retract")
                yield from bps.mv(att2_9, "Insert")
            yield from bps.mv(waxs, wa)
            yield from bps.mvr(piezo.x, 500)

            for e in energies:
                yield from bps.mv(energy, e)
                sample_name = name_fmt.format(sample=name, energy=e, wax=wa)
                sample_id(user_name="PB", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 2490)
            yield from bps.mv(energy, 2470)
            yield from bps.mv(energy, 2450)
        yield from bps.mvr(piezo.th, -0.7)


def waxs_S_edge(t=1):
    dets = [pil300KW, pil1M]

    names = ["saxs_S_edge_ech2"]
    x = [-41000]

    energies = [
        2450,
        2470,
        2473,
        2475,
        2476,
        2477,
        2478,
        2479,
        2480,
        2481,
        2483,
        2485,
        2490,
        2495,
        2500,
        2510,
    ]
    waxs_arc = [0, 6.5]

    for name, xs in zip(names, x):
        yield from bps.mv(piezo.x, xs)

        det_exposure_time(t, t)
        name_fmt = "saxs_{sample}_{energy}eV_wa{wax}"

        for wa in waxs_arc:
            yield from bps.mvr(piezo.y, 200)
            yield from bps.mv(waxs, wa)

            for e in energies:
                yield from bps.mv(energy, e)
                sample_name = name_fmt.format(sample=name, energy=e, wax=wa)
                sample_id(user_name="PB", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 2490)
            yield from bps.mv(energy, 2470)
            yield from bps.mv(energy, 2450)
        yield from bps.mvr(piezo.y, -400)


def giwaxsTempSingleWaxsSeries(
    x_list, y_list, th_list, chi_list, sample_list, waxs_arc, num, t=1, user="BP"
):
    print(num)
    for waxspos in waxs_arc:
        for x, y, th, chi, sample in zip(
            x_list, y_list, th_list, chi_list, sample_list
        ):  # loop over samples on bar
            yield from bps.mv(piezo.x, x)  # move to next sample
            yield from bps.mv(piezo.y, y)  # move to next sample
            yield from bps.mv(piezo.th, th)  # move to next sample
            yield from bps.mv(piezo.ch, chi)  # move to next sample
            print(x)
            th_meas = 0.12 + piezo.th.position
            th_real = 0.12

            yield from bps.mv(piezo.th, th_meas)
            yield from bps.mv(
                waxs, waxspos
            )  # move the waxs dectector to the measurement position
            waxs_arc = [waxspos]
            temp = ls.ch1_read.value
            dets = [pil300KW, pil1M]
            det_exposure_time(t, t)
            sample_name = (
                "{sample}_inc{th:5.4f}deg_waxs{waxspos:5.4f}_{temp:5.4f}C_{num}".format(
                    sample=sample, th=th_real, waxspos=waxspos, temp=temp, num=num
                )
            )
            sample_id(user_name=user, sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            # yield from bp.scan(dets, waxs, *waxs_arc)# should just be a single point "scan"

            if np.int(waxs.arc.position) < 6 and bsx_pos > 0:
                yield from bps.mv(waxs, waxspos)
            yield from bp.count(dets)


def heatingLoop():
    # Load 1 xpos = [-11000,2000] #2493 is from -2000 to -11000, 2523 is from 2000 to 11000
    xpos = [-6000, 2500]  # 2493 is from -2500 to -12000, 2523 is from 2000 to 11000
    names = ["P3HHT_A", "P3MEEMT"]

    xstep = 200
    quickalignevery = 15  # do a quickalign every n exposures
    sleepbetweenexps = 20
    nscans = 20000  # Arbitrary high number; I don't know how the runengine would handle an infinite loop but effectively this.  End the run with ctrl-c + RE.stop()

    ypos = [5100, 5100]
    thpos = [-1, -0.6]
    chipos = [-0.8, 0.5]
    for i, x in enumerate(xpos):
        yield from bps.mv(piezo.x, x + 2000)
        yield from bps.mv(piezo.ch, chipos[i])
        yield from alignement_gisaxs(0.08)
        ypos[i] = piezo.y.position
        thpos[i] = piezo.th.position

    # continually measure, every 30 minutes re-align and shift 200 um in x
    counter = 0

    print("Alignment Done:")
    print(str(names))
    print(str(xpos))
    print(str(ypos))
    print(str(thpos))

    xmodfwd = np.arange(0, 4500, xstep)
    xmodbck = np.arange(4500, 0, xstep)

    xmod = np.concatenate((xmodfwd, xmodbck))

    while counter < nscans:
        for xmv in xmod:
            lclxpos = xpos + xmv
            yield from giwaxsTempSingleWaxsSeries(
                lclxpos,
                ypos,
                thpos,
                chipos,
                names,
                [9.5, 3],
                counter,
                t=1,
                user="PB1-1",
            )
            sleep(sleepbetweenexps)
            counter += 1
            yield from giwaxsTempSingleWaxsSeries(
                lclxpos,
                ypos,
                thpos,
                chipos,
                names,
                [3, 9.5],
                counter,
                t=1,
                user="PB1-1",
            )
            sleep(sleepbetweenexps)
            counter += 1
            if counter % quickalignevery is 0 or counter % quickalignevery is 1:
                for i, x in enumerate(xpos):
                    yield from bps.mv(waxs, 9.5)
                    yield from bps.mv(piezo.x, x + 2000)
                    yield from bps.mv(piezo.ch, chipos[i])

                    yield from alignement_gisaxs(0.08)
                    ypos[i] = piezo.y.position
                    thpos[i] = piezo.th.position

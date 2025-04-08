def run_waxs_IC(t=1):
    dets = [pil300KW, pil1M]

    names = [
        "2um_725_7m",
        "2um_725_45d_7m",
        "5um_825_7m",
        "5um_825_45d_7m",
        "10um_825_7m",
        "10um_825_45d_7m",
        "AgBh",
    ]
    x = [34000, 36000, 19500, 13500, 4500, -3000, -25000]

    energies = [2405, 2465, 2471, 2473, 2475, 2477, 2479, 2481]

    waxs_arc = [0, 19.5, 4]

    for xs, name in zip(x, names):
        yield from bps.mv(piezo.x, xs)

        if (
            name == "2um_725_45d_7m"
            or name == "5um_825_45d_7m"
            or name == "10um_825_45d_7m"
        ):
            yield from bps.mv(prs, 45)
        else:
            yield from bps.mv(prs, 0)
        det_exposure_time(t, t)
        name_fmt = "{sample}_{energy}eV"
        for i, e in enumerate(energies):

            yield from bps.mv(energy, e)
            sample_name = name_fmt.format(sample=name, energy=e)
            sample_id(user_name="IC", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.scan(dets, waxs, *waxs_arc)
            if e == 2405:
                yield from bps.mv(energy, 2430)
            elif e == 2481:
                yield from bps.mv(energy, 2460)
                yield from bps.mv(energy, 2430)
                yield from bps.mv(energy, 2405)
                name_fmt = "{sample}_2405eV_postedge"
                sample_name = name_fmt.format(sample=name)
                sample_id(user_name="IC", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.scan(dets, waxs, *waxs_arc)

    names = ["10um_825_45d_7m_nexafs_w20"]
    x = [-5000]
    dets = [pil300KW]
    yield from bps.mv(waxs, 20)
    yield from bps.mv(energy, 2420)
    yield from bps.mv(energy, 2440)
    yield from bps.mv(energy, 2450)
    energies = np.linspace(2450, 2531, 163)
    for xs, name in zip(x, names):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(prs, 0)
        det_exposure_time(t, t)
        name_fmt = "{sample}_{energy}eV"
        for i, e in enumerate(energies):
            yield from bps.mv(energy, e)
            sample_name = name_fmt.format(sample=name, energy=e)
            sample_id(user_name="IC", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)
            if e == 2405:
                yield from bps.mv(energy, 2430)
            elif e > 2530.6:
                yield from bps.mv(energy, 2500)
                yield from bps.mv(energy, 2470)
                yield from bps.mv(energy, 2430)
                yield from bps.mv(energy, 2405)
                name_fmt = "{sample}_2405eV_postedge"
                sample_name = name_fmt.format(sample=name)
                sample_id(user_name="IC", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)


def film_Sn_edge2(t=0.5):
    dets = [pil300KW]

    names = [
        "1909_utbVE_40p11cd_ai1p1_2bragg_w3p7",
        "1909_utbVE_40p11cd_ai1p1_2bragg_bkg_w3p7",
    ]
    x = [6700, -5000]

    energies = np.concatenate(
        [np.asarray([3850, 3900, 3920, 3925]), np.arange(3930, 3941, 1)]
    )
    for xs, name in zip(x, names):
        yield from bps.mv(piezo.x, xs)
        det_exposure_time(t, t)
        name_fmt = "{sample}_{energy}eV"
        for e in energies:
            yield from bps.mv(energy, e)

            sample_name = name_fmt.format(sample=name, energy=e)
            sample_id(user_name="IC", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)

            if e == 3850:
                yield from bps.mv(energy, 3875)

            elif e > 3939.5:
                yield from bps.mv(energy, 3920)
                yield from bps.mv(energy, 3890)
                yield from bps.mv(energy, 3850)
                name_fmt = "{sample}_3850eV_postedge"
                sample_name = name_fmt.format(sample=name)
                sample_id(user_name="IC", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)


def film_Sn_edge1(t=0.5):
    dets = [pil300KW]

    names = [
        "1909_bbVE_40p11cd_ai1p1_2bragg_w3p7",
        "1909_bbVE_40p11cd_ai1p1_2bragg_bkg_w3p7",
    ]
    x = [-23000, -17000]

    energies = np.concatenate(
        [
            np.asarray([3850, 3900, 3920]),
            np.arange(3925, 3935, 0.5),
            np.arange(3935, 3946, 1),
        ]
    )
    for xs, name in zip(x, names):
        yield from bps.mv(piezo.x, xs)
        det_exposure_time(t, t)
        name_fmt = "{sample}_{energy}eV"
        for e in energies:
            yield from bps.mv(energy, e)

            sample_name = name_fmt.format(sample=name, energy=e)
            sample_id(user_name="IC", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)

            if e == 3850:
                yield from bps.mv(energy, 3875)

            elif e > 3944.5:
                yield from bps.mv(energy, 3920)
                yield from bps.mv(energy, 3890)
                yield from bps.mv(energy, 3850)
                name_fmt = "{sample}_3850eV_postedge"
                sample_name = name_fmt.format(sample=name)
                sample_id(user_name="IC", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)


def film_Sn_edge(t=0.5):
    dets = [pil300KW]

    names = ["1909_utbVE_40p11CD_ai0p5deg"]

    energies = [3850, 3900, 3920, 3925, 3930, 3935, 3945, 3850]
    waxs_arc = [3, 16, 3]
    i = 0
    for name in names:
        det_exposure_time(t, t)
        name_fmt = "{sample}_{energy}eV"
        for e in energies:
            yield from bps.mv(energy, e)
            if i == 1:
                name_fmt = "{sample}_{energy}eV_postedge"
            sample_name = name_fmt.format(sample=name, energy=e)
            sample_id(user_name="IC", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.scan(dets, waxs, *waxs_arc)

            if e == 3850:
                yield from bps.mv(energy, 3875)

            elif e == 3945:
                yield from bps.mv(energy, 3920)
                yield from bps.mv(energy, 3890)
                yield from bps.mv(energy, 3850)
                i = 1


def fly_scan_ai(det, motor, cycle=1, cycle_t=10, phi=-0.6):
    start = phi + 0
    stop = phi + 4.5
    acq_time = cycle * cycle_t
    yield from bps.mv(motor, start)
    # yield from bps.mv(attn_shutter, 'Retract')
    det.stage()
    det.cam.acquire_time.put(acq_time)
    print(f"Acquire time before staging: {det.cam.acquire_time.get()}")
    st = det.trigger()
    for i in range(cycle):
        yield from list_scan([], motor, [start, stop])
    while not st.done:
        pass
    det.unstage()
    print(f"We are done after {acq_time}s of waiting")
    # yield from bps.mv(attn_shutter, 'Insert')


def ai_scan_multilayer(t=1):
    dets = [pil300KW]

    name = "10nmMLYAHY_noPEB_Exp1"
    energies = [3900, 3930, 4000]
    waxs_arc = [6.5]
    incident_angle = np.linspace(0.5, 2.5, 101)

    det_exposure_time(t, t)
    name_fmt = "{sample}_{energy}eV_ai{alpha_i}_wa{waxs}_{num}"

    ai0 = piezo.th.position

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)
        for e in energies:
            yield from mv_energy(e)
            yield from bps.mvr(piezo.x, 200)
            for i in [0, 1]:
                if i == 0:
                    incident_an = incident_angle
                    met = "fwd"
                else:
                    incident_an = incident_angle[::-1]
                    met = "rev"

                for inc_ang in incident_an:
                    print(inc_ang)
                    yield from bps.mv(piezo.th, ai0 + inc_ang)

                    sample_name = name_fmt.format(
                        sample=name,
                        energy=e,
                        alpha_i="%3.2f" % inc_ang,
                        waxs=wa,
                        num=met,
                    )
                    sample_id(user_name="IC", sample_name=sample_name)

                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)


def ai_scan_multilayer_nightscan(t=1):
    dets = [pil300KW]

    # names = ['10nmSiYAVE_Unexp', '10nmMLYAVE_Unexp', '10nmSiYAHY_Unexp', 'bare_ML']
    names = ["bare_ML"]
    # xs = [-36500, -23000, -1000, 23400]
    xs = [23400]
    energies = np.linspace(3900, 4000, 21)
    waxs_arc = [6.5]
    incident_angle = np.linspace(0.5, 2.5, 101)

    det_exposure_time(t, t)
    name_fmt = "{sample}_{energy}eV_ai{alpha_i}_wa{waxs}"

    ai0 = 0

    for z, (x, name) in enumerate(zip(xs, names)):

        yield from bps.mv(piezo.x, x)
        yield from bps.mv(GV7.open_cmd, 1)
        yield from bps.sleep(10)
        yield from bps.mv(GV7.open_cmd, 1)
        yield from bps.mv(piezo.th, ai0)

        yield from alignement_gisaxs(0.4)

        yield from bps.mv(GV7.close_cmd, 1)
        yield from bps.sleep(10)
        yield from bps.mv(GV7.close_cmd, 1)
        yield from bps.mv(att2_9, "Insert")
        yield from bps.mv(att2_10, "Insert")
        ai0 = piezo.th.position
        for i, wa in enumerate(waxs_arc):
            if i == 0:
                incid_angle = incident_angle
            else:
                incid_angle = incident_angle[::-1]
            yield from bps.mv(waxs, wa)
            energiess = energies
            for j, e in enumerate(energiess):
                yield from bps.mv(energy, e)
                if z == 3:
                    yield from bps.mvr(piezo.x, 0)
                else:
                    yield from bps.mvr(piezo.x, 250)

                for inc_ang in incid_angle:
                    yield from bps.mv(piezo.th, ai0 + inc_ang)

                    sample_name = name_fmt.format(
                        sample=name, energy=e, alpha_i="%3.2f" % inc_ang, waxs=wa
                    )
                    sample_id(user_name="IC", sample_name=sample_name)

                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 3960)
            yield from bps.sleep(5)
            yield from bps.mv(energy, 3920)


"""
def ai_scan_reflectivity_scan(t=1):
    dets = [pil300KW]
    
    #names = ['10nmSiYAVE_Unexp', '10nmMLYAVE_Unexp', '10nmSiYAHY_Unexp', 'bare_ML']
    names = ['bare_ML']
    #xs = [-36500, -23000, -1000, 23400]
    xs = [23400]
    #energies = np.linspace(3900, 4000, 21)
    energies = [3900,3930,4100]
    incident_angle = np.linspace(0.1, 5, 101)
    
    det_exposure_time(t,t) 
    name_fmt = '{sample}_reflectivity_{energy}eV_{direction}_ai{alpha_i}_'

    ai0 = 0
    
    # Loop over samples, doing alignment first
    for z, (x, name) in enumerate(zip(xs, names)):
        
        # Move to sample position
        yield from bps.mv(piezo.x, x)

        # Move waxs out of the way
        yield from bps.mv(wax, 13.5)

        # Open gate valve for alignment
        yield from bps.mv(GV7.open_cmd, 1 )
        yield from bps.sleep(10)
        # Make sure valve is open?
        yield from bps.mv(GV7.open_cmd, 1 )
        # Move incident angle to guessed zero
        yield from bps.mv(piezo.th, ai0)
        # Align theta and z
        yield from alignement_gisaxs(0.4)
        # Close the gate valve
        yield from bps.mv(GV7.close_cmd, 1 )
        yield from bps.sleep(10)
        yield from bps.mv(GV7.close_cmd, 1 )
        
        # Redefine zerp theta based on alignment
        ai0 = piezo.th.position

        # Move the waxs back
        yield from bps.mv(waxs, 0)

        # Insert all Al filters (subject to change based on flux)
        yield from bps.mv(att2_9, 'Insert')
        yield from bps.mv(att2_10, 'Insert')
        yield from bps.mv(att2_11, 'Insert')
        yield from bps.mv(att2_12, 'Insert')

        # Once aligned, loop over energies
        for j, e in enumerate(energies):
            # step carefully through energy

            # Move in x
            yield from bps.mvr(piezo.x,300)

            for d in ['fwd','rev']
                # Define incident angle direction
                if d == 'fwd'    
                    incid_angle = incident_angle
                elif d == 'rev'
                    incid_angle = incident_angle[::-1]

                for inc_ang in incid_angle:
                    yield from bps.mv(piezo.th, ai0 + inc_ang)

                    sample_name = name_fmt.format(sample=name, energy=e, direction=d, alpha_i='%3.2f'%inc_an)
                    sample_id(user_name='IC', sample_name=sample_name)
                    
                    print(f'\n\t=== Sample: {sample_name} ===\n')
                    yield from bp.count(dets, num=1)
            
            yield from bps.mv(energy, 3960)
            yield from bps.sleep(5)
            yield from bps.mv(energy, 3920)
"""


def reflectivity_night(t=1):
    yield from test_reflectivity_scan(t=0.5, nu=1)
    yield from test_reflectivity_scan(t=0.5, nu=2)
    yield from test_reflectivity_scan(t=0.5, nu=3)


def test_reflectivity_scan(t=1, nu=0):
    dets = [pil300KW]
    energy = [3900, 3930, 4100]  #'3900'
    dire = "fwd"
    names = [
        "10nmSiYAHY_Unexp_Ref",
        "10nmMLYAVE_Unexp_Ref",
        "10nmSiYAVE_Unexp_Ref",
        "bare_ML_part2",
        "10nmMLYAHY_noPEB_Exp_Ref",
    ]
    # name = 'bare_ML'
    xs = [-2850, -17850, -36350, 22050, 39050]
    zs = [-2400, -2400, -2400, -2400, -3000]  # 23400
    # x = 22650

    # PUT SAMPLE LOOP HERE
    ai0 = 0

    for x, z, name in zip(xs, zs, names):

        # Move to sample position
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(piezo.z, z)

        # Open gate valve for alignment
        yield from bps.mv(GV7.open_cmd, 1)
        yield from bps.sleep(10)
        # Make sure valve is open?
        yield from bps.mv(GV7.open_cmd, 1)
        # Move incident angle to guessed zero
        yield from bps.sleep(5)

        yield from bps.mv(piezo.th, ai0)
        # Align theta and z
        yield from alignement_gisaxs(0.4)
        # Close the gate valve
        yield from bps.mv(GV7.close_cmd, 1)
        yield from bps.sleep(10)
        yield from bps.mv(GV7.close_cmd, 1)
        yield from bps.sleep(5)

        ai0 = piezo.th.position

        # Move the waxs back
        yield from bps.mv(waxs, 0)

        det_exposure_time(t, t)
        name_fmt = "{sample}_reflectivity_{energy}eV_{direction}_ai{alpha_i}_foil{num}_{number}"

        # Define angular ranges for the scan
        ai_ranges = [
            [0.2, 0.7],
            [0.6, 1.2],
            [0.9, 1.6],
            [1.5, 2.6],
            [2.5, 3.0],
            [2.9, 3.2],
            [3.1, 3.6],
            [3.5, 4.0],
            [3.9, 4.4],
            [4.3, 4.8],
        ]
        ais = [[]] * len(ai_ranges)
        for alphai in np.linspace(0.2, 4.8, 257):
            for i, ai_range in enumerate(ai_ranges):
                if alphai < ai_range[1] and ai_range[0] <= alphai:
                    ais[i] = ais[i] + [alphai]

        # Loop over the energies
        for en in energy:
            # Change energy using slow change defined below
            yield from bps.mvr(piezo.x, 300)

            yield from mv_energy(en)
            for ran_num, aiss in enumerate(ais):
                yield from clean_shit()
                yield from clean_shit()
                yield from function_att(ran_num)
                yield from function_att(ran_num)

                if ran_num < 3.5:
                    yield from bps.mv(waxs.x, 0)
                else:
                    yield from bps.mv(waxs.x, -22.0)

                for ai in aiss:
                    yield from bps.mv(piezo.th, ai0 + ai)

                    sample_name = name_fmt.format(
                        sample=name,
                        energy=en,
                        direction=dire,
                        alpha_i="%4.3f" % ai,
                        num=ran_num,
                        number=nu,
                    )
                    sample_id(user_name="IC", sample_name=sample_name)

                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)


def clean_shit(t=1):
    yield from bps.mv(att2_1, "Retract")
    yield from bps.sleep(t)
    yield from bps.mv(att2_2, "Retract")
    yield from bps.sleep(t)
    yield from bps.mv(att2_3, "Retract")
    yield from bps.sleep(t)
    yield from bps.mv(att2_4, "Retract")
    yield from bps.sleep(t)
    yield from bps.mv(att2_5, "Retract")
    yield from bps.sleep(t)
    yield from bps.mv(att2_6, "Retract")
    yield from bps.sleep(t)
    yield from bps.mv(att2_7, "Retract")
    yield from bps.sleep(t)
    yield from bps.mv(att2_8, "Retract")
    yield from bps.sleep(t)
    yield from bps.mv(att2_9, "Retract")
    yield from bps.sleep(t)
    yield from bps.mv(att2_10, "Retract")
    yield from bps.sleep(t)
    yield from bps.mv(att2_11, "Retract")
    yield from bps.sleep(t)
    yield from bps.mv(att2_12, "Retract")
    yield from bps.sleep(t)


def clean_sh(t=1):
    yield from bps.mv(att2_1, "Insert")
    yield from bps.sleep(t)
    yield from bps.mv(att2_2, "Insert")
    yield from bps.sleep(t)
    yield from bps.mv(att2_3, "Insert")
    yield from bps.sleep(t)
    yield from bps.mv(att2_4, "Insert")
    yield from bps.sleep(t)
    yield from bps.mv(att2_5, "Insert")
    yield from bps.sleep(t)
    yield from bps.mv(att2_6, "Insert")
    yield from bps.sleep(t)
    yield from bps.mv(att2_7, "Insert")
    yield from bps.sleep(t)
    yield from bps.mv(att2_8, "Insert")
    yield from bps.sleep(t)
    yield from bps.mv(att2_9, "Insert")
    yield from bps.sleep(t)
    yield from bps.mv(att2_10, "Insert")
    yield from bps.sleep(t)
    yield from bps.mv(att2_11, "Insert")
    yield from bps.sleep(t)
    yield from bps.mv(att2_12, "Insert")
    yield from bps.sleep(t)


def function_att(ran_num, t=1):
    if ran_num == 0:
        # 5x +1x
        yield from bps.mv(att2_5, "Insert")
        yield from bps.sleep(t)
        yield from bps.mv(att2_9, "Insert")
        yield from bps.sleep(t)
        yield from bps.mv(att2_11, "Insert")
        yield from bps.sleep(t)

    elif ran_num == 1:
        # 4x +1x
        yield from bps.mv(att2_5, "Insert")
        yield from bps.sleep(t)
        yield from bps.mv(att2_11, "Insert")
        yield from bps.sleep(t)

    elif ran_num == 2:
        # 3x +1x
        yield from bps.mv(att2_5, "Insert")
        yield from bps.sleep(t)
        yield from bps.mv(att2_10, "Insert")
        yield from bps.sleep(t)
        yield from bps.mv(att2_9, "Insert")
        yield from bps.sleep(t)

    elif ran_num == 3:
        # 12x
        yield from bps.mv(att2_12, "Insert")
        yield from bps.sleep(t)
        yield from bps.mv(att2_11, "Insert")
        yield from bps.sleep(t)
        yield from bps.mv(att2_10, "Insert")
        yield from bps.sleep(t)

    elif ran_num == 4:
        # 11x
        yield from bps.mv(att2_12, "Insert")
        yield from bps.sleep(t)
        yield from bps.mv(att2_11, "Insert")
        yield from bps.sleep(t)
        yield from bps.mv(att2_9, "Insert")
        yield from bps.sleep(t)

    elif ran_num == 5:
        # 10x
        yield from bps.mv(att2_12, "Insert")
        yield from bps.sleep(t)
        yield from bps.mv(att2_11, "Insert")
        yield from bps.sleep(t)

    elif ran_num == 6:
        # 8x
        yield from bps.mv(att2_12, "Insert")
        yield from bps.sleep(t)
        yield from bps.mv(att2_10, "Insert")
        yield from bps.sleep(t)

    elif ran_num == 7:
        # 7x
        yield from bps.mv(att2_12, "Insert")
        yield from bps.sleep(t)
        yield from bps.mv(att2_9, "Insert")
        yield from bps.sleep(t)

    elif ran_num == 8:
        # 6x
        yield from bps.mv(att2_12, "Insert")
        yield from bps.sleep(t)

    elif ran_num == 9:
        # 5x
        yield from bps.mv(att2_11, "Insert")
        yield from bps.sleep(t)
        yield from bps.mv(att2_9, "Insert")
        yield from bps.sleep(t)


# © Luke Long. Venmo is an acceptable form of payment.
def mv_energy(set_point, t=3, step=30):
    e_diff = set_point - energy.energy.position
    while abs(e_diff) > step:
        print(
            f"LARGE ENERGY DIFFERENCE. TAKING STEP SIZE OF {step}eV. @ GUI: DONT FORGET TO VENMO LUKE"
        )
        yield from bps.mvr(energy, sign(e_diff) * 30)
        yield from bps.sleep(t)
        e_diff = set_point - energy.energy.position
    yield from bps.mv(energy, set_point)


def fluo_scan(t=1):
    dets = [pil300KW]

    name = "10nmMLYAHY_noPEB_Unexp_fluoscan1_"
    energies = np.append(np.linspace(3900, 3990, 181), np.linspace(3990, 4100, 56))

    waxs_arc = [20]
    incident_angle = 0.6

    det_exposure_time(t, t)
    name_fmt = "{sample}_{energy}eV_bpm{bpm}"
    yield from bps.mvr(piezo.th, incident_angle)

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)
        for e in energies:
            yield from bps.mv(energy, e)
            sample_name = name_fmt.format(
                sample=name, energy=e, bpm="%5.2f" % xbpm2.sumX.value
            )
            sample_id(user_name="IC", sample_name=sample_name)

            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)
            # print(inc_ang)
            # yield from bps.sleep(1)

    yield from bps.mvr(piezo.th, -incident_angle)

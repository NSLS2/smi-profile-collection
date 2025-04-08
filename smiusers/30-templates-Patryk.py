###################################
### Templates for macros at SMI ###
###################################


# Metadata
"""
    # Metadata
    td = str(np.round(t1 - t0, 1)).zfill(6)         # time difference in seconds from time.time()
    e = energy.position.energy / 1000               # energy keV
    wa = waxs.arc.position + 0.001                  # WAXS arc angle, deg
    wa = str(np.round(float(wa), 1)).zfill(4)
    temp = ls.input_A.get() - 273.15                # Lakeshore temp controller, deg C
    temp = str(np.round(float(temp), 1)).zfill(5)
    sdd = pil1m_pos.z.position / 1000               # SAXS detector distance
    scan_id = db[-1].start['scan_id'] + 1           # transient scan ID
    bpm = xbpm3.sumX.get()                          # XBPM reading
"""

# Sample name / detector images name formatting
"""
    name_fmt = '{sample}_{energy}keV_{temp}degC_wa{wax}_sdd{sdd}m_id{scan_id}'
    sample_name = name_fmt.format(sample=name, energy='%.2f'%e, temp=temp, wax=wa,
                                  sdd='%.1f'%sdd, scan_id=scan_id)
    print(f'\n\t=== Sample: {sample_name} ===\n')
    sample_id(user_name=user_name, sample_name=sample_name)"""

# Energies for NEXAFS
"""
    Reference: http://skuld.bmsc.washington.edu/scatter/AS_periodic.html

    # Sulphur S K-edge (ref. 2472.0 eV)
    # here SMI scan for lower edge of 2476 eV)
    energies = np.concatenate((np.arange(2445, 2470, 5),
                               np.arange(2470, 2480, 0.25),
                               np.arange(2480, 2490, 1),
                               np.arange(2490, 2501, 5),
                               ))

    # Chlorine Cl K-edge (ref. 2822.4 eV)
    energies = np.concatenate((np.arange(2810, 2820, 5),
                               np.arange(2820, 2825, 1),
                               np.arange(2825, 2835, 0.25),
                               np.arange(2835, 2840, 0.5),
                               np.arange(2840, 2850, 5),
                               np.arange(2850, 2910, 10),
                               ))
    
    # Silver Ag L3-edge (ref.  3351.1 eV)
    energies = np.concatenate((np.arange(3300, 3340, 5),
                               np.arange(3340, 3350, 2),
                               np.arange(3350, 3390, 1),
                               np.arange(3390, 3400, 2),
                               np.arange(3400, 3451, 5),
                              ))
    
    # Energies for Calcium Ca K-edge (ref. 4038.1 eV)
    energies = np.concatenate((np.arange(4030, 4040, 5),
                               np.arange(4040, 4050, 0.25),
                               np.arange(4050, 4060, 1),
                               np.arange(4060, 4070, 2.5),
                               np.arange(4070, 4080, 5),
                               ))
    
    # Energies for tellurium Te L-3 edge (ref. 4341.4 eV)
    energies = np.concatenate((np.arange(4320, 4345, 5),
                               np.arange(4345, 4350, 2.5),
                               np.arange(4350, 4360, 0.4),
                               np.arange(4360, 4380, 2),
                               np.arange(4380, 4401, 5),
                               ))

    # Energies for platinum Pt L-3 edge (ref. 11.5637 keV)
    energies = np.concatenate((np.arange(11530, 11550, 2),
                               np.arange(11550, 11580, 1),
                               np.arange(11580, 11620, 2)
                               ))
                               
"""

def turn_off_heating(temp=23):
    """
    Turn off the heating and set temperature to 23 deg C for Lakeshore
    """
    
    print(f'Setting temp to {temp} deg C and turning off the heater')
    t_kelvin = temp + 273.15
    yield from ls.output1.mv_temp(t_kelvin)
    yield from ls.output1.turn_off()

# Name correction
"""
    # Check and correct sample names just in case
    name = name.translate({ord(c): '_' for c in '!@#$%^&*{}:/<>?\|`~+ =,'})
"""

# Detectors
"""
    # Do not read SAXS if WAXS is in the way
    dets = [pil900KW] if waxs.arc.position < 10 else [pil1M, pil900KW]
"""

# Images as tests and standard exposure
"""
    sample_id(user_name='test', sample_name='test')
    det_exposure_time(0.3, 0.3)
"""

### Controling lakeshore
### Range 3 for high temperature > 120
### range 1 up to 50 deg
def startT():
    """
    Try using range 3 in channel 1
    """
    yield from bps.mv(ls.output1.status, 3)
    print("Start heating up using output1 using range3.")


def stopT():
    yield from ls.output1.turn_off()
    # RE( ls.output1.turn_off()    )
    print("Stop heating up using output1.")


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

                    """
                    # Sample name
                    name_fmt = '{sample}_{energy}keV_temp{temp}degC_wa{wax}_sdd{sdd}m_id{scan_id}'
                    sample_name = name_fmt.format(sample=name, energy='%.2f'%e, temp=temp, wax=wa,
                                      sdd='%.1f'%sdd, scan_id=scan_id)
                    print(f'\n\t=== Sample: {sample_name} ===\n')
                    sample_id(user_name=name, sample_name=sample_name) 
                    yield from bp.count(dets)"""

                # Go back gently with energy
                yield from bps.mv(energy, 2480)
                yield from bps.mv(energy, 2450)

    # End of the scan
    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)
    yield from ls.output1.mv_temp(28 + 273.13)


### Linkam MFS tensile stage hard X-rays
def song_waxs_hard_2022_2(t=1, strain=0):
    """
    Hard X-ray script for MFS stage manual

    Args:
        t (float): detector exposure time,
        strain (float): strain value from Linkam MFS stage for filename metadata
    """

    names = ["p77_cross2_2s"]
    x = [-0.6]
    y = [-1.2]

    user_name = "SZ"

    waxs_arc = [0, 20]
    names = [
        n.translate({ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ =,"}) for n in names
    ]

    for name, xs, ys in zip(names, x, y):
        yield from bps.mv(stage.x, xs)
        yield from bps.mv(stage.y, ys)

        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)
            dets = [pil900KW] if waxs.arc.position < 15 else [pil1M, pil900KW]
            yield from bps.mv(stage.y, ys + i * 0.05)
            det_exposure_time(t, t)
            name_fmt = (
                "{sample}_{energy}keV_strain{strain}_wa{wax}_sdd{sdd}m_id{scan_id}"
            )

            # Metadata
            sdd = pil1m_pos.z.position / 1000
            e = energy.position.energy / 1000
            scan_id = db[-1].start["scan_id"] + 1

            sample_name = name_fmt.format(
                sample=name,
                strain=strain,
                energy="%2.1f" % e,
                wax=wa,
                sdd="%.1f" % sdd,
                scan_id=scan_id,
            )
            sample_id(user_name=user_name, sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets)
            sample_id(user_name="test", sample_name="test")


### Calculate beamstpo on WAXS y postion is in 36-Guillaume beam, line ~160
### calculate waxs beamstop for x is 21-pilatus.py line 359

"""
for temperature in temperatures:
        t_kelvin = temperature + 273.15
        yield from ls.output1.mv_temp(t_kelvin)

        # Activate heating range in Lakeshore
        if temperature < 50:
            yield from bps.mv(ls.output1.status, 1)
        else:
            yield from bps.mv(ls.output1.status, 3)

        # Equalise temperature
        print(f'Equalising temperature to {temperature} deg C')
        start = time.time()
        temp = ls.input_A.get()
        while abs(temp - t_kelvin) >  1:
            print('Difference: {:.1f} K'.format(abs(temp - t_kelvin)))
            yield from bps.sleep(10)
            temp = ls.input_A.get()
            # Escape the loop if too much time passes
            if time.time() - start > 1800:
                temp = t_kelvin
        print('Time needed to equilibrate: {:.1f} min'.format((time.time() - start) / 60))

        # Wait extra time depending on temperature
        if (35 < temperature) and (temperature < 160):
            yield from bps.sleep(300)
        elif 160 <= temperature:
            yield from bps.sleep(600)

        # Read T and convert to deg C
        temp_degC = ls.input_A.get() - 273.15"""

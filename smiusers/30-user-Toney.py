def zihan_alignment():
    """
    Align sample using hexapod
    """
    #proposal_id('2023_1', '000000_tests')

    try:
        yield from alignement_gisaxs_hex(angle=0.5, rough_y=0.5)
    except:
        yield from alignement_gisaxs_hex(angle=0.1, rough_y=0.5)

    #proposal_id('2023_1', '311645_Zhang')


def zihan_giwaxs_2023_1(t=0.5, name='test', dist='unspecified'):
    """
    GIWAXS measurement on a custom stage mounted on the hexapod
    GU-311645 SAF: 310633

    Manually enter the sample name and the squeeze distance
    """


    incident_angles = [0.5, 1.5, 4.36,6.2]
    waxs_arc = [0, 20]
    user_name = "ZZ"

    # Sample flat at ai0
    ai0 = stage.th.position

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)
        
        dets = [pil900KW] #if waxs.arc.position < 15 else [pil900KW, pil1M]
        det_exposure_time(t, t)

        for ai in incident_angles:
            yield from bps.mv(stage.th, ai0 + ai)

            # Metadata
            e = energy.position.energy / 1000
            sdd = pil1m_pos.z.position / 1000
            wa = waxs.arc.position + 0.001
            wa = str(np.round(float(wa), 1)).zfill(4)

            # Sample name
            name_fmt = "{sample}_{dist}mm_{energy}keV_wa{wax}_sdd{sdd}m_ai{ai}"
            sample_name = name_fmt.format(
                sample=name,
                dist=dist,
                energy="%.2f" % e,
                wax=wa,
                sdd="%.1f" % sdd,
                ai=ai,
            )
            sample_name = sample_name.translate(
                {ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ =,"}
            )
            sample_id(user_name=user_name, sample_name=sample_name)
            print(f"\n\n\n\t=== Sample: {sample_name} ===")
            yield from bp.count(dets)

    yield from bps.mv(stage.th, ai0)
    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)


def turn_off_heating(temp=23):
    """
    Turn off the heating and set temperature to 23 deg C for Lakeshore
    """
    print(f'Setting temp to {temp} deg C and turning off the heater')
    t_kelvin = temp + 273.15
    yield from ls.output1.mv_temp(t_kelvin)
    yield from ls.output1.turn_off()

def align_gisaxs_th_zihan(rang=0.3, point=31):
    th0 = piezo.th.position
    yield from bp.rel_scan([pil1M], piezo.th, -rang, rang, point)
    ps(plot=False)
    yield from bps.mv(piezo.th, ps.peak)


def zihan_giwaxs_alignment(angle=0.1, sample_name='test'):
    """
    Quicker alignment
    """

    # Activate the automated derivative calculation
    bec._calc_derivative_and_stats = True

    sample_id(user_name="test", sample_name=sample_name)
    det_exposure_time(0.3, 0.3)

    smi = SMI_Beamline()
    yield from smi.modeAlignment(technique="gisaxs")

    # Set direct beam ROI
    yield from smi.setDirectBeamROI()

    # Scan theta and height
    yield from align_gisaxs_height(800, 16, der=True)
    yield from align_gisaxs_th_zihan(1.5, 27)

    # move to theta 0 + value
    yield from bps.mv(piezo.th, ps.peak + angle)

    # Set reflected ROI
    yield from smi.setReflectedBeamROI(total_angle=angle, technique="gisaxs")

    # Scan theta and height
    yield from align_gisaxs_th_zihan(0.2, 11)
    yield from align_gisaxs_height_rb(150, 16)
    yield from align_gisaxs_th_zihan(0.1, 21) 

    # Close all the matplotlib windows
    plt.close("all")

    # Return angle
    yield from bps.mv(piezo.th, ps.cen - angle)
    yield from smi.modeMeasurement()

    # Deactivate the automated derivative calculation
    bec._calc_derivative_and_stats = False

def zihan_quick_alignment(angle=0.15):
    """
    Short alignement with only alignement on the reflected beam.
    """

    # Activate the automated derivative calculation
    bec._calc_derivative_and_stats = True
    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)

    smi = SMI_Beamline()
    yield from smi.modeAlignment()

    # move to theta 0 + value
    yield from bps.mvr(piezo.th, angle)

    # Set reflected ROI
    yield from smi.setReflectedBeamROI(total_angle=angle)

    # Scan theta and height
    yield from align_gisaxs_height_rb(200, 31)
    yield from align_gisaxs_th_zihan(0.1, 21)

    # Close all the matplotlib windows
    plt.close("all")

    # Return angle
    yield from bps.mv(piezo.th, ps.cen - angle)
    yield from smi.modeMeasurement()

    # Deactivate the automated derivative calculation
    bec._calc_derivative_and_stats = False


def zihan_temperature_giwaxs_2023_1(t=0.5):
    """
    Hard X-ray GIWAXS Lakeshore heating stage.
    """

    names =   [ 'CS1', 'CS2', 'CS3', 'CS4', 'CS5', 'CS6', 'CS7', 'CS1S', 'CS2S', 'CS3S', 'CS4S']
    piezo_x = [ 52900,  43950, 32900, 22900, 12900, 2900, -7100, -17100, -28100, -38100, -47100 ]   
    piezo_y = [       -100, -100, -100, -100]
    piezo_z = [4500 for n in names]
    # piezo_z = [4200, 4100, ]

    assert len(names)   == len(piezo_x), f"Wrong list lenghts"
    assert len(piezo_x) == len(piezo_y), f"Wrong list lenghts"
    assert len(piezo_y) == len(piezo_z), f"Wrong list lenghts"

    user_name = "ZZ"
    temperatures = [#25, 30, 40, 50, 60, 
                    80, 100, 80, 60, 40, 25,
                    40, 60, 80, 100, 120, 140,
                    120, 100, 80, 60, 40, 25] 
    
    waxs_arc = [0, 20]
    incident_angles = [0.50, 1.50, 4.36, 6.20]
    piezo_x_offs = [0, 200, 500]

    ai0 = piezo.th.position

    for p, temperature in enumerate(temperatures):
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
            if time.time() - start > 10 * 60:
                temp = t_kelvin
        print(
            "Time needed to equilibrate: {:.1f} min".format((time.time() - start) / 60)
        )

        # Wait extra time depending on temperature
        #if (56 < temperature) and (temperature < 160):
        #    yield from bps.sleep(300)
        #elif 160 <= temperature:
        #    yield from bps.sleep(600)

        # Read T and convert to deg C
        temp_degC = ls.input_A.get() - 273.15

        for name, x, y, z in zip(names, piezo_x, piezo_y, piezo_z):
            yield from bps.mv(piezo.x, x + p * 200,
                              piezo.y, y,
                              piezo.z, z,
                              piezo.th, ai0)
            # Align sample
            yield from zihan_giwaxs_alignment(0.1)

            # Sample flat at ai0
            ai0 = piezo.th.position

            for wa in waxs_arc:
                yield from bps.mv(waxs, wa)
                dets = [pil900KW] if waxs.arc.position < 15 else [pil1M, pil900KW]
                det_exposure_time(t, t)

                for ai in incident_angles:
                    yield from bps.mv(piezo.th, ai0 + ai)
                    p=0
                    for i, x_off in enumerate(piezo_x_offs):
                        yield from bps.mv(piezo.x, x + p * 200 + x_off)

                        # Metadata
                        e = energy.position.energy / 1000
                        temp = str(np.round(float(temp_degC), 1)).zfill(5)
                        wa = waxs.arc.position + 0.001
                        wa = str(np.round(float(wa), 1)).zfill(4)
                        sdd = pil1m_pos.z.position / 1000


                        name_fmt = "{sample}_{temp}degC_pos{pos}_{energy}eV_wa{wax}_sdd{sdd}m_ai{ai}"
                        sample_name = name_fmt.format(
                            sample=name,
                            pos = i + 1,
                            energy="%.2f" % e,
                            temp=temp,
                            wax=wa,
                            sdd="%.1f" % sdd,
                            ai = ai,
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

def zihan_giwaxs_2023_1(t=0.5):
    """
    Hard X-ray GIWAXS, samples on Lakeshore heating stage but no heating.
    """
   
    names =   [  'Si', 'PET']
    piezo_x = [  -41100, -47100 ]   
    piezo_y = [   690, 690]
    piezo_z = [4500 for n in names]
    # piezo_z = [4200, 4100, ]

    assert len(names)   == len(piezo_x), f"Wrong list lenghts"
    assert len(piezo_x) == len(piezo_y), f"Wrong list lenghts"
    assert len(piezo_y) == len(piezo_z), f"Wrong list lenghts"

    user_name = "ZZ"
    
    waxs_arc = [0, 20]
    incident_angles = [0.5,1.5,4.36,6.2]
    piezo_x_offs = [0]
    temp = 25
    ai0 = piezo.th.position


    for name, x, y, z in zip(names, piezo_x, piezo_y, piezo_z):
        yield from bps.mv(piezo.x, x,
                          piezo.y, y,
                          piezo.z, z,
                          piezo.th, ai0)
        # Align sample
        yield from zihan_giwaxs_alignment(0.1)

        # Sample flat at ai0
        ai0 = piezo.th.position

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)
            dets = [pil900KW] if waxs.arc.position < 15 else [pil1M, pil900KW]
            det_exposure_time(t, t)

            for ai in incident_angles:
                yield from bps.mv(piezo.th, ai0 + ai)
                
                p=0
                for i, x_off in enumerate(piezo_x_offs):
                    yield from bps.mv(piezo.x, x + p * 200 + x_off)

                    # Metadata
                    e = energy.position.energy / 1000
                    temp = str(np.round(float(temp), 1)).zfill(5)
                    wa = waxs.arc.position + 0.001
                    wa = str(np.round(float(wa), 1)).zfill(4)
                    sdd = pil1m_pos.z.position / 1000


                    name_fmt = "{sample}_{temp}degC_pos{pos}_{energy}eV_wa{wax}_sdd{sdd}m_ai{ai}"
                    sample_name = name_fmt.format(
                        sample=name,
                        pos = i + 1,
                        energy="%.2f" % e,
                        temp=temp,
                        wax=wa,
                        sdd="%.1f" % sdd,
                        ai = ai,
                    )
                    sample_name = sample_name.translate(
                        {ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ =, "}
                    )
                    print(f"\n\n\n\t=== Sample: {sample_name} ===")
                    sample_id(user_name=user_name, sample_name=sample_name)
                    
                    yield from bp.count(dets)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)

def Zihan_wip():
    temperatures = [#25, 30, 40, 50, 60, 
            80, 100, 80, 60, 40, 25,
            40, 60, 80, 100, 120, 140,
            120, 100, 80, 60, 40, 25]
    for p, temperature in enumerate(temperatures):
        print(p)
        print(temperature)


def alignment_stage_Zihan_2023_2(angle=1.5, sample_name='test'):
    """
    Alignment for bent samples
    Needs refinement, decided on manual
    """

    bec._calc_derivative_and_stats = True

    sample_id(user_name="test", sample_name=sample_name)
    det_exposure_time(0.5, 0.5)

    smi = SMI_Beamline()
    yield from smi.modeAlignment()

    # Set direct beam ROI
    yield from smi.setDirectBeamROI()

    # Scan height direct
    yield from bp.rel_scan([pil1M], stage.y, -0.3, 0.1, 41)
    ps(der=True)
    yield from bps.mv(stage.y, ps.peak)

    # Scan theta direct
    yield from bp.rel_scan([pil1M], stage.th, -3, 3, 31)
    ps()
    yield from bps.mv(stage.th, ps.cen)

    # Scan x direct (sample centre)
    yield from bp.rel_scan([pil1M], stage.x, -2, 2, 21)
    ps()
    yield from bps.mv(stage.th, ps.cen)

    # move to theta 0 + value
    yield from bps.mvr(stage.th, angle)

    # Set reflected ROI
    yield from smi.setReflectedBeamROI(total_angle=angle, technique="gisaxs")

    # Scan theta reflected
    yield from bp.rel_scan([pil1M], stage.th, -0.2, 2, 21)
    ps()
    yield from bps.mv(stage.th, ps.peak)

    # Scan height reflected
    yield from bp.rel_scan([pil1M], stage.y, -0.05, 0.05, 21)
    ps(der=True)
    yield from bps.mv(stage.y, ps.peak)

    # Scan theta reflected
    yield from bp.rel_scan([pil1M], stage.th, -0.05, 0.05, 21)
    ps()
    yield from bps.mv(stage.th, ps.peak)

    # Close all the matplotlib windows
    plt.close("all")

    # Return angle
    yield from bps.mvr(stage.th, - angle)
    yield from smi.modeMeasurement()

    # Deactivate the automated derivative calculation
    bec._calc_derivative_and_stats = False


def alignment_start(sample_name='alignment'):
    """
    Attenuators in, beamstop out, ROI1 set to direct beam
    """

    smi = SMI_Beamline()
    yield from smi.modeAlignment()

    # Set direct beam ROI
    yield from smi.setDirectBeamROI()

    sample_id(user_name='test', sample_name=sample_name)
    #proposal_id('2023_2', '311645_Zhang')


def alignment_start_angle(angle=0.15):
    """
    Attenuators in, beamstop out, ROI1 set to direct beam
    """

    smi = SMI_Beamline()
    yield from smi.modeAlignment()

    # Set reflected beam ROI
    yield from smi.setReflectedBeamROI(total_angle=angle, technique="gisaxs")


def alignment_stop():
    """
    Attenuators out, beamstop in,
    """

    smi = SMI_Beamline()
    yield from smi.modeMeasurement()
    #proposal_id('2023_2', '311645_Zhang_1')


def zihan_giwaxs_2023_2(t=0.5, name='test', dist='unspecified'):
    """
    GIWAXS measurement on a custom stage mounted on the hexapod
    Manually enter the sample name and the squeeze distance
    """

    incident_angles = [0.5, 1.5, 4.5, 6.5]
    waxs_arc = [0,7,20]
    user_name = "ZZ"

    # Sample flat at ai0
    ai0 = stage.th.position

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)
        
        dets = [pil900KW] if waxs.arc.position < 15 else [pil900KW, pil1M]
        det_exposure_time(t, t)

        for ai in incident_angles:
            yield from bps.mv(stage.th, ai0 + ai)

            sample_name = f'{name}_{dist}mm{get_scan_md()}_ai{ai}'
            sample_id(user_name=user_name, sample_name=sample_name)
            print(f"\n\n\n\t=== Sample: {sample_name} ===")
            yield from bp.count(dets)

    yield from bps.mv(stage.th, ai0)
    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)

    """
    Procedure for manual alignment of bending samples

    get y and x close using cameras

    move z to middle (usuallly z=5)
    
    RE(alignment_start())

    do y scan
    RE(rel_scan([pil1M], stage.y, -0.3, 0.3, 21))
    RE(mv(stage.y, TOPINFLECTION))

    do theta scan
    RE(rel_scan([pil1M], stage.th, -0.5, 0.5, 21)) 
    (larger range for inverted sample)
    RE(mv(stage.th, PEAKCENT))

    do x scan
    RE(mvr(stage.y, 0.05)) 
    (not needed for inverted sample)
    RE(rel_scan([pil1M], stage.x, -1.5, 1.5, 21))
    RE(mv(stage.x, NEGPEAKCENT)) 
    #sometimes there will be two adjacent neg peak, go in the center between them
    RE(mvr(stage.y, -0.05))

    do y scan
    RE(rel_scan([pil1M], stage.y, -0.3, 0.3, 21))
    RE(mv(stage.y, TOPINFLECTION))

    do theta scan
    RE(rel_scan([pil1M], stage.th, -0.2, 0.2, 21))
    RE(mv(stage.th, PEAK))

    optional if you see reflected peak (I think you should):

    # change angle to where you want to align at
    
    RE(alignment_start_angle(angle=0.2))
    RE(mvr(stage.th, 0.2))
    RE(rel_scan([pil1M], stage.th, -0.2, 0.2, 21))
    RE(mv(stage.th, PEAK))
    p

    measure
    RE(alignment_stop())
    RE(zihan_giwaxs_2023_2(...))

    """

def zihan_giwaxs_alignment_2023_2(angle=0.1, sample_name='test'):
    """
    Quicker alignment
    """
    # Activate the automated derivative calculation
    bec._calc_derivative_and_stats = True

    sample_id(user_name="test", sample_name=sample_name)
    det_exposure_time(0.3, 0.3)

    smi = SMI_Beamline()
    yield from smi.modeAlignment(technique="gisaxs")

    # Set direct beam ROI
    yield from smi.setDirectBeamROI()

    # Scan theta and height
    yield from align_gisaxs_height(2000, 21, der=True)
    yield from align_gisaxs_th_zihan(1.5, 31)

    # move to theta 0 + value
    yield from bps.mv(piezo.th, ps.peak + angle)

    # Set reflected ROI
    yield from smi.setReflectedBeamROI(total_angle=angle, technique="gisaxs")

    # Scan theta and height
    yield from align_gisaxs_th_zihan(0.2, 11)
    yield from align_gisaxs_height_rb(150, 16)
    yield from align_gisaxs_th_zihan(0.1, 21) 

    # Close all the matplotlib windows
    plt.close("all")

    # Return angle
    yield from bps.mv(piezo.th, ps.cen - angle)
    yield from smi.modeMeasurement()

    # Deactivate the automated derivative calculation
    bec._calc_derivative_and_stats = False


def zihan_giwaxs_samplebar_2023_2(t=0.5):
    """
    Hard X-ray GIWAXS, samples on regular GI stage
    """

    names =   [   'S8_2' ]
    piezo_x = [  -48000]   
    piezo_y = [   6000]
    piezo_z = [ 4000 for n in names ]
    stage_x = [  -15.5]
    # piezo_z = [4200, 4100, ]

    assert len(names)   == len(piezo_x), f"Wrong list lenghts"
    assert len(piezo_x) == len(piezo_y), f"Wrong list lenghts"
    assert len(piezo_y) == len(piezo_z), f"Wrong list lenghts"
    assert len(piezo_z) == len(stage_x), f"Wrong list lenghts"

    user_name = "ZZ"
    
    waxs_arc = [0, 15]
    incident_angles = [0.14, 0.16, 0.18, 0.20, 0.21]
    ai0 = piezo.th.position

    unaligned_samples = []


    for name, x, y, z, hx in zip(names, piezo_x, piezo_y, piezo_z, stage_x):
        yield from bps.mv(piezo.x, x,
                          piezo.y, y,
                          piezo.z, z,
                          piezo.th, ai0,
                          stage.x, hx,
        )
        # Align sample

        try:
            yield from zihan_giwaxs_alignment_2023_2(0.1, sample_name=name)
        except:
            unaligned_samples.append(name)
            break
        
        # Sample flat at ai0
        ai0 = piezo.th.position

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)
            dets = [pil900KW] if waxs.arc.position < 15 else [pil1M, pil900KW]
            det_exposure_time(t, t)

            for ai in incident_angles:
                yield from bps.mv(piezo.th, ai0 + ai)

                sample_name = f'{name}_{get_scan_md()}_ai{ai}'
                sample_id(user_name=user_name, sample_name=sample_name)
                print(f"\n\n\n\t=== Sample: {sample_name} ===")
                yield from bp.count(dets)

    if unaligned_samples:
        f = RE.md['path'] + '/unaligned_samples.txt'
        with open(f, 'w') as file:
            for row in unaligned_samples:
                s = " ".join(map(str, row))
                file.write(s + '\n')

    yield from bps.mv(piezo.th, ai0)
    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)



def zihan_giwaxs_2024_1(t=0.5, name='Z1-pvsk_on_ito_2', dist='unspecified'):
    """
    GIWAXS measurement on a custom stage mounted on the hexapod
    Manually enter the sample name and the squeeze distance
    """

    incident_angles = [0.5, 4.5]
    waxs_arc = [0, 20]
    user_name = "ZZ"

    # Sample flat at ai0
    ai0 = stage.th.position

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)
        
        dets = [pil900KW] if waxs.arc.position < 15 else [pil900KW, pil1M]
        det_exposure_time(t, t)

        for ai in incident_angles:
            yield from bps.mv(stage.th, ai0 + ai)

            sample_name = f'{name}_{dist}mm{get_scan_md()}_ai{ai}'
            sample_id(user_name=user_name, sample_name=sample_name)
            print(f"\n\n\n\t=== Sample: {sample_name} ===")
            yield from bp.count(dets)

    yield from bps.mv(stage.th, ai0)
    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)

# Align at each angle and then measure
"""
    Procedure for manual alignment of bending samples

    get y and x close using cameras

    move z to middle (usuallly z=5)
    
    RE(alignment_start())

    do y scan
    RE(rel_scan([pil1M], stage.y, -0.3, 0.3, 21))
    RE(mv(stage.y, TOPINFLECTION))

    do theta scan
    RE(rel_scan([pil1M], stage.th, -0.5, 0.5, 21)) 
    (larger range for inverted sample)
    RE(mv(stage.th, PEAKCENT))

    do x scan
    RE(mvr(stage.y, 0.05)) 
    (not needed for inverted sample)
    RE(rel_scan([pil1M], stage.x, -2, 2, 31))
    RE(mv(stage.x, NEGPEAKCENT)) 
    #sometimes there will be two adjacent neg peak, go in the center between them
    RE(mvr(stage.y, -0.05))

    do y scan
    RE(rel_scan([pil1M], stage.y, -0.3, 0.3, 21))
    RE(mv(stage.y, TOPINFLECTION))

    do theta scan
    RE(rel_scan([pil1M], stage.th, -0.2, 0.2, 31))
    RE(mv(stage.th, PEAK))

    optional if you see reflected peak (I think you should):

    # change angle to where you want to align at
    angle = 0.1

    check for stage.z to move sample back to the beam

    Do the stage.y scan, could be broad
    RE(rel_scan([pil1M], stage.y, -0.3, 0.3, 21))
    RE(mv(stage.y, TOPINFLECTION))
    
    RE(alignment_start_angle(angle=angle))
    RE(mvr(stage.th, angle))
    RE(rel_scan([pil1M], stage.th, -0.2, 0.2, 31)) # could use -1, 1, 31 for larger angles to start with
    RE(mv(stage.th, PEAK))
    RE(mvr(stage.th, -angle))

    measure
    RE(alignment_stop())
    RE(zihan_giwaxs_single_2024_1(...))
"""

def zihan_giwaxs_single_2024_1(t=0.5, name='Z1-pvsk_on_ito_2', dist='unspecified', incident_angles=0.5):
    """
    GIWAXS measurement on a custom stage mounted on the hexapod
    Manually enter the sample name and the squeeze distance
    
    Specify incident angle in the function, angle as aligned
    """


    waxs_arc = [0, 20]
    user_name = "ZZ"

    # Sample flat at ai0
    ai0 = stage.th.position

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)
        
        dets = [pil900KW] if waxs.arc.position < 15 else [pil900KW, pil1M]
        det_exposure_time(t, t)

        for ai in incident_angles:
            yield from bps.mv(stage.th, ai0 + ai)

            sample_name = f'{name}_{dist}mm{get_scan_md()}_ai{ai}'
            sample_id(user_name=user_name, sample_name=sample_name)
            print(f"\n\n\n\t=== Sample: {sample_name} ===")
            yield from bp.count(dets)

    yield from bps.mv(stage.th, ai0)
    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)


def S_edge_measurments_2024_1_Toney(t=4):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    # names =   ['', '50-blank-redo', '50-teacl-redo', '255-blank-redo', '255-teacl-redo']          
    # x_piezo = [     -31080,          -15080,                 920,           16920,            33920]            
    # x_hexa =  [           0,          0,          0,          0,          0]           
    # y_piezo = [        3250,       3250,       3250,       3250,       3250]
    # z_piezo = [       -10500,     -10500,    -10500,     -10500,      -10500]  

    # names =   ['Si-1', 'Si-2', 'Si-3', 'Si-4', 'Si-5', 'Si-6', 'Si-7', 'Si-8', 'Si-9', 'Si-10', 'Si-11']          
    # x_piezo = [-48870, -36870, -21870, -17370,  -6370,   2630,  12630,  20630,  29630,   38630,   47630]            
    # x_hexa =  [     0,      0,      0,      0,      0,      0,      0,      0,      0,       0,       0]           
    # y_piezo = [  3250,   3250,   3250,   3250,   3250,   3250,   3250,   3250,   3250,    3250,    3250]
    # z_piezo = [-10500, -10500, -10500, -10500, -10500, -10500, -10500, -10500, -10500,  -10500,  -10500]  

    # names =   ['50-blank', '255-blank', '180-blank']          
    # x_piezo = [     -7610,       10390,       34390]            
    # x_hexa =  [         0,           0,           0]           
    # y_piezo = [      3496,        3496,        3496]
    # z_piezo = [     -9000,      -10500,      -12000]  

    # names =   ['Si-1', 'Si-2', 'Si-3', 'Si-4', 'Si-5', 'Si-6', 'Si-7', 'Si-8', 'Si-9', 'Si-10', 'Si-11']          
    # x_piezo = [-48870, -36870, -21870, -17370,  -6370,   2630,  12630,  20630,  29630,   38630,   47630]            
    # x_hexa =  [     0,      0,      0,      0,      0,      0,      0,      0,      0,       0,       0]           
    # y_piezo = [  3250,   3250,   3250,   3250,   3250,   3250,   3250,   3250,   3250,    3250,    3250]
    # z_piezo = [-10500, -10500, -10500, -10500, -10500, -10500, -10500, -10500, -10500,  -10500,  -10500]  

    # names =   ['Si-2', 'Si-3', 'Si-4', 'Si-5', 'Si-6', 'Si-7', 'Si-8', 'Si-9', 'Si-10', 'Si-11']          
    # x_piezo = [-36870, -21870, -17370,  -6370,   2630,  12630,  20630,  29630,   38630,   47630]            
    # x_hexa =  [     0,      0,      0,      0,      0,      0,      0,      0,       0,       0]           
    # y_piezo = [  3250,   3250,   3250,   3250,   3250,   3250,   3250,   3250,    3250,    3250]
    # z_piezo = [-10500, -10500, -10500, -10500, -10500, -10500, -10500, -10500,  -10500,  -10500] 

    # names =   ['Si-4', 'Si-5', 'Si-6', 'Si-7', 'Si-8', 'Si-9', 'Si-10', 'Si-11']          
    # x_piezo = [-17370,  -6370,   2630,  12630,  20630,  29630,   38630,   47630]            
    # x_hexa =  [     0,      0,      0,      0,      0,      0,       0,       0]           
    # y_piezo = [  3250,   3250,   3250,   3250,   3250,   3250,    3250,    3250]
    # z_piezo = [-10500, -10500, -10500, -10500, -10500, -10500,  -10500,  -10500] 

    names =   ['Si-11', 'Si-10', 'Si-9', 'Si-8', 'Si-7', 'Si-6', 'Si-15', 'Si-14', 'Si-13', 'Si-12']          
    x_piezo = [ -33955,  -24956, -15956,  -6956,   1044,  10044,   19043,   28044,   37044,   46044]            
    x_hexa =  [      0,       0,      0,      0,      0,      0,       0,       0,       0,       0]           
    y_piezo = [   9440,    9440,   9440,   9440,   9440,   9440,    9440,    9440,    9440,    9440]
    z_piezo = [ -11500,  -11500, -11500, -11500, -11500, -11500,  -11500,  -11500,  -11500,  -11500]

    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(z_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexa)})"

    # energies = [2450.0,2455.0,2460.0,2465.0,2470.0,2473.0,2475.0,2475.5,2476.0,2476.5,2477.0,2477.5,2478.0,2478.5,2479.0,2479.5,
    # 2480.0,2480.5,2481.0,2482.0,2483.0,2484.0,2485.0,2486.0, 2487.0,2488.0,2489.0,2490.0,2492.5,2495.0,2500.0,2510.0,2515.0]

    energies = [2445.0,2450.0,2455.0,2460.0,2465.0,2470.0,2472.0,2473.0,2474.0,2474.5,2475.0,2475.5,2476.0,2476.5,2477.0,2477.5,2478.0,
                2478.5,2479.0,2479.5,2480.0,2480.5,2481.0,2482.0,2483.0,2484.0,2485.0,2486.0,2487.0,2488.0,2489.0,2490.0,2492.5,2495.0,
                2500.0,2510.0,2515.0,2530.0,2550.0]

    waxs_arc = [0, 20]
    ai0 = 0
    # ai_list = [0.80]
    ai_list = [1.10]

    for name, xs, ys, zs, xs_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa):
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)

        yield from bps.mv(piezo.th, ai0)
        yield from alignement_gisaxs_doblestack(0.8)

        ai0 = piezo.th.position
        det_exposure_time(t, t)
        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)
            # Do not take SAXS when WAXS detector in the way
            dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]

            yield from bps.mv(piezo.x, xs)
            counter = 0

            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                name_fmt = "{sample}_pos1_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                # name_fmt = "{sample}_pos1_{energy}eV_ai{ai}_wa{wax}_{t}s_bpm{xbpm}"
                for e in energies:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs + counter * 30)
                    counter += 1
                    
                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="CD", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)


                name_fmt = "{sample}_pos2_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                # name_fmt = "{sample}_pos2_{energy}eV_ai{ai}_wa{wax}_{t}s_bpm{xbpm}"
                for e in energies[::-1]:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs + counter * 30)
                    counter += 1

                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="CD", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)

            yield from bps.mv(piezo.th, ai0)
        

def Cl_edge_measurments_2024_1_Toney(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    names =   ['180-teacl', '50-teacl',  '255-teacl']          
    x_piezo = [-31080,             920,           33920]            
    x_hexa =  [ 0,                0,              0]           
    y_piezo = [3250,              3250,         3250]
                        #-3700,             -3700,               -3700,             -3700,                 -3700,             -3700,               -3700,                 -3700,                  -3700,                   -3700]
    z_piezo = [          -10500,          -10500,      -10500]   #           7000,                7000,                  7000,                   7000,                    7000,                     7000,                     7000,
                         #7000,              7000,                7000,              7000,                  7000,              7000,                       7000,              7000,                  7000,              7000,                7000,                  7000,                   7000,                    7000]

    x_piezo = 2000 + np.asarray(x_piezo)
    
    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(z_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexa)})"

    energies = np.asarray([2810.0, 2820.0, 2830.0, 2832.0, 2834.0, 2834.5, 2835.0, 2835.5, 2836.0, 2836.5, 2837.0, 2837.5, 2838.0, 2838.5, 2839.0,
    2839.5, 2840.0, 2840.5, 2841.0, 2841.5, 2845.0, 2850.0, 2855.0, 2860.0, 2865.0, 2870.0, 2875.0, 2880.0, 2890.0])
    
    waxs_arc = [0]
    ai0 = 0
    ai_list = [0.80]

    for name, xs, ys, zs, xs_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa):
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)

        yield from bps.mv(piezo.th, ai0)
        yield from alignement_gisaxs_doblestack(0.8)

        ai0 = piezo.th.position
        det_exposure_time(t, t)

        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)
            # Do not take SAXS when WAXS detector in the way
            dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]

            yield from bps.mv(piezo.x, xs)
            counter = 0

            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                name_fmt = "{sample}_pos1_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs + counter * 30)
                    counter += 1
                    
                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="CD", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)


                name_fmt = "{sample}_pos2_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                for e in energies[::-1]:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs + counter * 30)
                    counter += 1

                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="CD", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)

            yield from bps.mv(piezo.th, ai0)


def waxs_S_edge_chaney_variousprs_2024_1_march(t=8):
    dets = [pil900KW, pil1M]

    prs0 = -1
    yield from bps.mv(prs, prs0)


    # names = ["SiN-0", "SiN-1", "SiN-2", "SiN-3", "SiN-4", "SiN-7",  "SiN-8",  "SiN-9", "SiN-10", "SiN-11"]
    # x =     [  35044,   29044,   23544,   17544,   11044,    5044,    -1255,    -7255,   -13455,   -18956]
    # y =     [  -3648,   -3648,   -3648,   -3848,   -4048,   -3848,    -3848,    -3848,    -3848,    -3848] 

    # names = ["SiN-1", "SiN-2", "SiN-3", "SiN-4", "SiN-7",  "SiN-8",  "SiN-9", "SiN-10", "SiN-11"]
    # x =     [  29044,   23544,   17544,   11044,    5044,    -1255,    -7255,   -13455,   -18956]
    # y =     [  -3648,   -3648,   -3848,   -4048,   -3848,    -3848,    -3848,    -3848,    -3848]

    # names = ["SiN-2", "SiN-3", "SiN-4", "SiN-7",  "SiN-8",  "SiN-9", "SiN-10", "SiN-11"]
    # x =     [  23544,   17544,   11044,    5044,    -1255,    -7255,   -13455,   -18956]
    # y =     [  -3648,   -3848,   -4048,   -3848,    -3848,    -3848,    -3848,    -3848]

    names = ["SiN-0"]
    x =     [ -31200]
    y =     [  -9948] 
 

    assert len(x) == len(y), f"Number of X coordinates ({len(x)}) is different from number of samples ({len(y)})"
    assert len(x) == len(names), f"Number of X coordinates ({len(x)}) is different from number of samples ({len(names)})"

    # energies = (np.arange(2445, 2470, 5).tolist()+ np.arange(2470, 2480, 0.25).tolist()+ np.arange(2480, 2490, 1).tolist()
    #             + np.arange(2490, 2500, 5).tolist()+ np.arange(2500, 2560, 10).tolist())
    
    energies = [2445.0,2450.0,2455.0,2460.0,2465.0,2470.0,2472.0,2473.0,2474.0,2474.5,2475.0,2475.5,2476.0,2476.5,2477.0,2477.5,2478.0,
                2478.5,2479.0,2479.5,2480.0,2480.5,2481.0,2482.0,2483.0,2484.0,2485.0,2486.0,2487.0,2488.0,2489.0,2490.0,2492.5,2495.0,
                2500.0,2510.0,2515.0,2530.0,2550.0]
    
    # waxs_arc = [0, 20, 40]
    waxs_arc = [0, 20]

    for name, xs, ys in zip(names, x, y):
        yield from bps.mv(piezo.x, xs,
                          piezo.y, ys)

        yss = np.linspace(ys, ys + 1200, 63)
        xss = np.array([xs])

        yss, xss = np.meshgrid(yss, xss)
        yss = yss.ravel()
        xss = xss.ravel()

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)
            if wa == 0:
                dets = [pil900KW]
            else:
                dets = [pil900KW, pil1M]

            det_exposure_time(t, t)

            name_fmt = "{sample}_prs0deg_sdd1.8m_{energy}eV_wa{wax}_bpm{xbpm}"
            for e, xsss, ysss in zip(energies, xss, yss):
                yield from bps.mv(energy, e)
                yield from bps.sleep(2)
                if xbpm2.sumX.get() < 50:
                    yield from bps.sleep(2)
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)

                yield from bps.mv(piezo.y, ysss)
                yield from bps.mv(piezo.x, xsss)

                bpm = xbpm3.sumX.get()

                sample_name = name_fmt.format(sample=name, energy="%6.2f" % e, wax=wa, xbpm="%4.3f" % bpm)
                sample_id(user_name="TC", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")

                yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 2500)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 2480)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 2445)


    yield from bps.mv(prs, prs0+35)

    names = ["SiN-0", "SiN-1", "SiN-2", "SiN-3", "SiN-4", "SiN-7",  "SiN-8",  "SiN-9", "SiN-10", "SiN-11"]
    x =     [ -31800,  -25600,  -19700,  -13700,   -7700,   -1700,     4500,    10500,    16700,    22600]
    y =     [  -9948,   -9948,   -9748,  -10148,  -10048,   -9648,    -9748,    -9748,    -9648,    -9748] 

    assert len(x) == len(y), f"Number of X coordinates ({len(x)}) is different from number of samples ({len(y)})"
    assert len(x) == len(names), f"Number of X coordinates ({len(x)}) is different from number of samples ({len(names)})"

    # energies = (np.arange(2445, 2470, 5).tolist()+ np.arange(2470, 2480, 0.25).tolist()+ np.arange(2480, 2490, 1).tolist()
    #             + np.arange(2490, 2500, 5).tolist()+ np.arange(2500, 2560, 10).tolist())

    energies = [2445.0,2450.0,2455.0,2460.0,2465.0,2470.0,2472.0,2473.0,2474.0,2474.5,2475.0,2475.5,2476.0,2476.5,2477.0,2477.5,2478.0,
                2478.5,2479.0,2479.5,2480.0,2480.5,2481.0,2482.0,2483.0,2484.0,2485.0,2486.0,2487.0,2488.0,2489.0,2490.0,2492.5,2495.0,
                2500.0,2510.0,2515.0,2530.0,2550.0]    

    # waxs_arc = [0, 20, 40]
    waxs_arc = [0, 20]

    for name, xs, ys in zip(names, x, y):
        yield from bps.mv(piezo.x, xs,
                          piezo.y, ys)

        yss = np.linspace(ys, ys + 1200, 63)
        xss = np.array([xs])

        yss, xss = np.meshgrid(yss, xss)
        yss = yss.ravel()
        xss = xss.ravel()

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)
            if wa == 0:
                dets = [pil900KW]
            else:
                dets = [pil900KW, pil1M]

            det_exposure_time(t, t)

            name_fmt = "{sample}_prs35deg_sdd1.8m_{energy}eV_wa{wax}_bpm{xbpm}"
            for e, xsss, ysss in zip(energies, xss, yss):
                yield from bps.mv(energy, e)
                yield from bps.sleep(2)
                if xbpm2.sumX.get() < 50:
                    yield from bps.sleep(2)
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)

                yield from bps.mv(piezo.y, ysss)
                yield from bps.mv(piezo.x, xsss)

                bpm = xbpm3.sumX.get()

                sample_name = name_fmt.format(sample=name, energy="%6.2f" % e, wax=wa, xbpm="%4.3f" % bpm)
                sample_id(user_name="TC", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")

                yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 2500)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 2480)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 2445)



    yield from bps.mv(prs, prs0+55)

    names = ["SiN-2", "SiN-3", "SiN-4", "SiN-7",  "SiN-8",  "SiN-9", "SiN-10", "SiN-11"]
    x =     [ -19900,  -14100,   -7900,   -1900,     4100,    10400,    16400,    22300]
    y =     [  -9748,  -10148,  -10048,   -9748,     9748,    -9748,    -9648,    -9748] 

    assert len(x) == len(y), f"Number of X coordinates ({len(x)}) is different from number of samples ({len(y)})"
    assert len(x) == len(names), f"Number of X coordinates ({len(x)}) is different from number of samples ({len(names)})"

    # energies = (np.arange(2445, 2470, 5).tolist()+ np.arange(2470, 2480, 0.25).tolist()+ np.arange(2480, 2490, 1).tolist()
    #             + np.arange(2490, 2500, 5).tolist()+ np.arange(2500, 2560, 10).tolist())
    
    energies = [2445.0,2450.0,2455.0,2460.0,2465.0,2470.0,2472.0,2473.0,2474.0,2474.5,2475.0,2475.5,2476.0,2476.5,2477.0,2477.5,2478.0,
            2478.5,2479.0,2479.5,2480.0,2480.5,2481.0,2482.0,2483.0,2484.0,2485.0,2486.0,2487.0,2488.0,2489.0,2490.0,2492.5,2495.0,
            2500.0,2510.0,2515.0,2530.0,2550.0]
    
    # waxs_arc = [0, 20, 40]
    waxs_arc = [0, 20]

    for name, xs, ys in zip(names, x, y):
        yield from bps.mv(piezo.x, xs,
                          piezo.y, ys)

        yss = np.linspace(ys, ys + 1200, 63)
        xss = np.array([xs])

        yss, xss = np.meshgrid(yss, xss)
        yss = yss.ravel()
        xss = xss.ravel()

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)
            if wa == 0:
                dets = [pil900KW]
            else:
                dets = [pil900KW, pil1M]

            det_exposure_time(t, t)

            name_fmt = "{sample}_prs55deg_sdd1.8m_{energy}eV_wa{wax}_bpm{xbpm}"
            for e, xsss, ysss in zip(energies, xss, yss):
                yield from bps.mv(energy, e)
                yield from bps.sleep(2)
                if xbpm2.sumX.get() < 50:
                    yield from bps.sleep(2)
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)

                yield from bps.mv(piezo.y, ysss)
                yield from bps.mv(piezo.x, xsss)

                bpm = xbpm3.sumX.get()

                sample_name = name_fmt.format(sample=name, energy="%6.2f" % e, wax=wa, xbpm="%4.3f" % bpm)
                sample_id(user_name="TC", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")

                yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 2500)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 2480)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 2445)


def S_edge_measurments_2024_1_Toney_shortened(t=4):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    # names =   ['Si-6', 'Si-7', 'Si-8', 'Si-9', 'Si-10', 'Si-11']          
    # x_piezo = [  2630,  12630,  20630,  29630,   38630,   47630]            
    # x_hexa =  [     0,      0,      0,      0,       0,       0]           
    # y_piezo = [  3250,   3250,   3250,   3250,    3250,    3250]
    # z_piezo = [-10500, -10500, -10500, -10500,  -10500,  -10500]  

    names =   ['Si-16']          
    x_piezo = [ -40956]            
    x_hexa =  [      0]           
    y_piezo = [   9440]
    z_piezo = [ -10500]  

    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(z_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexa)})"

    # energies = [2450.0,2455.0,2460.0,2465.0,2470.0,2473.0,2475.0,2475.5,2476.0,2476.5,2477.0,2477.5,2478.0,2478.5,2479.0,2479.5,
    # 2480.0,2480.5,2481.0,2482.0,2483.0,2484.0,2485.0,2486.0, 2487.0,2488.0,2489.0,2490.0,2492.5,2495.0,2500.0,2510.0,2515.0]

    energies = [2445.0,2450.0,2455.0,2460.0,2465.0,2470.0,2472.0,2473.0,2474.0,2474.5,2475.0,2475.5,2476.0,2476.5,2477.0,2477.5,2478.0,
                2478.5,2479.0,2479.5,2480.0,2480.5,2481.0,2482.0,2483.0,2484.0,2485.0,2486.0,2487.0,2488.0,2489.0,2490.0,2492.5,2495.0,
                2500.0,2510.0,2515.0,2530.0,2550.0]

    waxs_arc = [0, 20]
    ai0 = 0
    ai_list = [1.1]

    for name, xs, ys, zs, xs_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa):
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)

        yield from bps.mv(piezo.th, ai0)
        yield from alignement_gisaxs_doblestack(0.8)

        ai0 = piezo.th.position
        det_exposure_time(t, t)
        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)
            # Do not take SAXS when WAXS detector in the way
            dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]

            yield from bps.mv(piezo.x, xs)
            counter = 0

            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)

                name_fmt = "{sample}_pos1_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                # name_fmt = "{sample}_pos1_{energy}eV_ai{ai}_wa{wax}_{t}s_bpm{xbpm}"
                for e in energies:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs + counter * 30)
                    counter += 1
                    
                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="CD", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)


                name_fmt = "{sample}_pos2_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                # name_fmt = "{sample}_pos2_{energy}eV_ai{ai}_wa{wax}_{t}s_bpm{xbpm}"
                for e in energies[::-1]:
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs + counter * 30)
                    counter += 1

                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="CD", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)

            yield from bps.mv(piezo.th, ai0)


def waxs_S_edge_chaney_variousprs_2024_1_march_shortened(t=8):
    dets = [pil900KW, pil1M]

    prs0 = -1
    yield from bps.mv(prs, prs0)


    # names = ["SiN-0", "SiN-1", "SiN-2", "SiN-3", "SiN-4", "SiN-7",  "SiN-8",  "SiN-9", "SiN-10", "SiN-11"]
    # x =     [  35044,   29044,   23544,   17544,   11044,    5044,    -1255,    -7255,   -13455,   -18956]
    # y =     [  -3648,   -3648,   -3648,   -3848,   -4048,   -3848,    -3848,    -3848,    -3848,    -3848] 

    # names = ["SiN-1", "SiN-2", "SiN-3", "SiN-4", "SiN-7",  "SiN-8",  "SiN-9", "SiN-10", "SiN-11"]
    # x =     [  29044,   23544,   17544,   11044,    5044,    -1255,    -7255,   -13455,   -18956]
    # y =     [  -3648,   -3648,   -3848,   -4048,   -3848,    -3848,    -3848,    -3848,    -3848]

    # names = ["SiN-2", "SiN-3", "SiN-4", "SiN-7",  "SiN-8",  "SiN-9", "SiN-10", "SiN-11"]
    # x =     [  23544,   17544,   11044,    5044,    -1255,    -7255,   -13455,   -18956]
    # y =     [  -3648,   -3848,   -4048,   -3848,    -3848,    -3848,    -3848,    -3848]

    names = ["SiN-0"]
    x =     [ -31200]
    y =     [  -9948] 
 

    assert len(x) == len(y), f"Number of X coordinates ({len(x)}) is different from number of samples ({len(y)})"
    assert len(x) == len(names), f"Number of X coordinates ({len(x)}) is different from number of samples ({len(names)})"

    # energies = (np.arange(2445, 2470, 5).tolist()+ np.arange(2470, 2480, 0.25).tolist()+ np.arange(2480, 2490, 1).tolist()
    #             + np.arange(2490, 2500, 5).tolist()+ np.arange(2500, 2560, 10).tolist())
    
    energies = [2445.0,2450.0,2455.0,2460.0,2465.0,2470.0,2472.0,2473.0,2474.0,2474.5,2475.0,2475.5,2476.0,2476.5,2477.0,2477.5,2478.0,
                2478.5,2479.0,2479.5,2480.0,2480.5,2481.0,2482.0,2483.0,2484.0,2485.0,2486.0,2487.0,2488.0,2489.0,2490.0,2492.5,2495.0,
                2500.0,2510.0,2515.0,2530.0,2550.0]
    
    # waxs_arc = [0, 20, 40]
    waxs_arc = [0, 20]

    for name, xs, ys in zip(names, x, y):
        yield from bps.mv(piezo.x, xs,
                          piezo.y, ys)

        yss = np.linspace(ys, ys + 1200, 63)
        xss = np.array([xs])

        yss, xss = np.meshgrid(yss, xss)
        yss = yss.ravel()
        xss = xss.ravel()

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)
            if wa == 0:
                dets = [pil900KW]
            else:
                dets = [pil900KW, pil1M]

            det_exposure_time(t, t)

            name_fmt = "{sample}_prs0deg_sdd1.8m_{energy}eV_wa{wax}_bpm{xbpm}"
            for e, xsss, ysss in zip(energies, xss, yss):
                yield from bps.mv(energy, e)
                yield from bps.sleep(2)
                if xbpm2.sumX.get() < 50:
                    yield from bps.sleep(2)
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)

                yield from bps.mv(piezo.y, ysss)
                yield from bps.mv(piezo.x, xsss)

                bpm = xbpm3.sumX.get()

                sample_name = name_fmt.format(sample=name, energy="%6.2f" % e, wax=wa, xbpm="%4.3f" % bpm)
                sample_id(user_name="TC", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")

                yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 2500)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 2480)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 2445)


    yield from bps.mv(prs, prs0+35)

    # names = ["SiN-0", "SiN-1", "SiN-2", "SiN-3", "SiN-4", "SiN-7",  "SiN-8",  "SiN-9", "SiN-10", "SiN-11"]
    # x =     [  34544,   28544,   22644,   16643,  10394,     4394,    -1606,    -7855,   -14105,   -19855]
    # y =     [  -3648,   -3648,   -3448,   -3848,  -3848,    -3848,    -3648,    -3848,    -3848,    -3648] 

    assert len(x) == len(y), f"Number of X coordinates ({len(x)}) is different from number of samples ({len(y)})"
    assert len(x) == len(names), f"Number of X coordinates ({len(x)}) is different from number of samples ({len(names)})"

    # energies = (np.arange(2445, 2470, 5).tolist()+ np.arange(2470, 2480, 0.25).tolist()+ np.arange(2480, 2490, 1).tolist()
    #             + np.arange(2490, 2500, 5).tolist()+ np.arange(2500, 2560, 10).tolist())

    energies = [2445.0,2450.0,2455.0,2460.0,2465.0,2470.0,2472.0,2473.0,2474.0,2474.5,2475.0,2475.5,2476.0,2476.5,2477.0,2477.5,2478.0,
                2478.5,2479.0,2479.5,2480.0,2480.5,2481.0,2482.0,2483.0,2484.0,2485.0,2486.0,2487.0,2488.0,2489.0,2490.0,2492.5,2495.0,
                2500.0,2510.0,2515.0,2530.0,2550.0]    

    # waxs_arc = [0, 20, 40]
    waxs_arc = [0, 20]

    for name, xs, ys in zip(names, x, y):
        yield from bps.mv(piezo.x, xs,
                          piezo.y, ys)

        yss = np.linspace(ys, ys + 1200, 63)
        xss = np.array([xs])

        yss, xss = np.meshgrid(yss, xss)
        yss = yss.ravel()
        xss = xss.ravel()

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)
            if wa == 0:
                dets = [pil900KW]
            else:
                dets = [pil900KW, pil1M]

            det_exposure_time(t, t)

            name_fmt = "{sample}_prs35deg_sdd1.8m_{energy}eV_wa{wax}_bpm{xbpm}"
            for e, xsss, ysss in zip(energies, xss, yss):
                yield from bps.mv(energy, e)
                yield from bps.sleep(2)
                if xbpm2.sumX.get() < 50:
                    yield from bps.sleep(2)
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)

                yield from bps.mv(piezo.y, ysss)
                yield from bps.mv(piezo.x, xsss)

                bpm = xbpm3.sumX.get()

                sample_name = name_fmt.format(sample=name, energy="%6.2f" % e, wax=wa, xbpm="%4.3f" % bpm)
                sample_id(user_name="TC", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")

                yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 2500)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 2480)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 2445)



    yield from bps.mv(prs, prs0+55)

    # names = ["SiN-0", "SiN-1", "SiN-2", "SiN-3", "SiN-4", "SiN-7",  "SiN-8",  "SiN-9", "SiN-10", "SiN-11"]
    # x =     [  33500,   27399,   21549,   15550,    9150,    3149,    -2850,    -9050,   -15300,   -21050]
    # y =     [  -3448,   -3448,   -3248,   -3848,   -3848,   -3848,    -3648,    -3848,    -3848,    -3648] 

    assert len(x) == len(y), f"Number of X coordinates ({len(x)}) is different from number of samples ({len(y)})"
    assert len(x) == len(names), f"Number of X coordinates ({len(x)}) is different from number of samples ({len(names)})"

    # energies = (np.arange(2445, 2470, 5).tolist()+ np.arange(2470, 2480, 0.25).tolist()+ np.arange(2480, 2490, 1).tolist()
    #             + np.arange(2490, 2500, 5).tolist()+ np.arange(2500, 2560, 10).tolist())
    
    energies = [2445.0,2450.0,2455.0,2460.0,2465.0,2470.0,2472.0,2473.0,2474.0,2474.5,2475.0,2475.5,2476.0,2476.5,2477.0,2477.5,2478.0,
            2478.5,2479.0,2479.5,2480.0,2480.5,2481.0,2482.0,2483.0,2484.0,2485.0,2486.0,2487.0,2488.0,2489.0,2490.0,2492.5,2495.0,
            2500.0,2510.0,2515.0,2530.0,2550.0]
    
    # waxs_arc = [0, 20, 40]
    waxs_arc = [0, 20]

    for name, xs, ys in zip(names, x, y):
        yield from bps.mv(piezo.x, xs,
                          piezo.y, ys)

        yss = np.linspace(ys, ys + 1200, 63)
        xss = np.array([xs])

        yss, xss = np.meshgrid(yss, xss)
        yss = yss.ravel()
        xss = xss.ravel()

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)
            if wa == 0:
                dets = [pil900KW]
            else:
                dets = [pil900KW, pil1M]

            det_exposure_time(t, t)

            name_fmt = "{sample}_prs55deg_sdd1.8m_{energy}eV_wa{wax}_bpm{xbpm}"
            for e, xsss, ysss in zip(energies, xss, yss):
                yield from bps.mv(energy, e)
                yield from bps.sleep(2)
                if xbpm2.sumX.get() < 50:
                    yield from bps.sleep(2)
                    yield from bps.mv(energy, e)
                    yield from bps.sleep(2)

                yield from bps.mv(piezo.y, ysss)
                yield from bps.mv(piezo.x, xsss)

                bpm = xbpm3.sumX.get()

                sample_name = name_fmt.format(sample=name, energy="%6.2f" % e, wax=wa, xbpm="%4.3f" % bpm)
                sample_id(user_name="TC", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")

                yield from bp.count(dets, num=1)

            yield from bps.mv(energy, 2500)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 2480)
            yield from bps.sleep(2)
            yield from bps.mv(energy, 2445)


def night_2024_3_25():
    yield from S_edge_measurments_2024_1_Toney()
    yield from waxs_S_edge_chaney_variousprs_2024_1_march()


def night_2023_1(t=1):

    #proposal_id("2023_1", "310999_Richter_2")
    #yield from S_edge_measurments_2023_1_night1(t=1)
    proposal_id("2023_1", "310999_Richter_3")
    #yield from transition_S_Cl_edges()
    yield from Cl_edge_measurments_2023_1_night1(t=1)


def night_2023_3(t=1):

    proposal_id("2023_1", "310999_Richter_9")
    yield from Cl_edge_measurments_2023_1_night3(t=1)
    
    yield from transition_Cl_S_edges()

    proposal_id("2023_1", "310999_Richter_10")
    yield from S_edge_measurments_2023_1_night3(t=1)



def transition_Cl_S_edges():
    yield from bps.mv(energy, 2800)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 2780)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 2760)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 2740)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 2720)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 2700)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 2680)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 2660)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 2640)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 2610)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 2580)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 2550)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 2525)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 2500)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 2475)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 2450)
    yield from bps.sleep(2)


def transition_S_Cl_edges():
    yield from bps.mv(energy, 2450)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 2475)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 2500)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 2525)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 2550)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 2580)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 2610)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 2640)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 2660)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 2680)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 2700)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 2720)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 2740)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 2760)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 2780)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 2800)
    yield from bps.sleep(2)

def transition_Cl_high_edges():
    yield from bps.mv(energy, 2800)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 2830)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 2850)
    yield from bps.sleep(2)
    yield from bps.mv(energy, 2880)
    yield from bps.sleep(2)
   
def NEXAFS_P_edge(t=0.5):
    yield from bps.mv(waxs, 45)
    dets = [pil300KW]
    name = "NEXAFS_s3_test_Pedge_nspot1"

    energies = np.linspace(2130, 2180, 51)
    xbpm3_y = np.linspace(1.42, 1.40, 51)

    det_exposure_time(t, t)
    name_fmt = "{sample}_{energy}eV_xbpm{xbpm}"

    for e, xbpm3_ys in zip(energies, xbpm3_y):
        yield from bps.mv(energy, e)
        yield from bps.mv(xbpm3_pos.y, xbpm3_ys)

        yield from bps.sleep(1)

        sample_name = name_fmt.format(
            sample=name, energy=e, xbpm="%3.1f" % xbpm2.sumX.value
        )
        sample_id(user_name="LR", sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")
        yield from bp.count(dets, num=1)


def P_edge_measurments_2024_1_Toney(t=1):
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    names =   [ '180-tbapf6-th9.24' ]          
    x_piezo = [       -28750 ]            
    x_hexa =  [            0 ]           
    y_piezo = [         3000 ]
    z_piezo = [       -10500]  


    # names =   ['50-tbapf6', '180-tbapf6', '255-tbapf6']          
    # x_piezo = [     -45750,       -28750,        -8750]            
    # x_hexa =  [          0,            0,            0]           
    # y_piezo = [       3000,         3000,         3000]
    # z_piezo = [     -10500,       -10500,       -10500]  

    assert len(x_piezo) == len(names), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(y_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(z_piezo), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(z_piezo)})"
    assert len(x_piezo) == len(x_hexa), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexa)})"

    
    energies = np.linspace(2120, 2190, 26)#2170 - 1.78, 2150 - 1.79, 
    #2130 - bpmx -0.54 bpmy 2.08
    #2120 -                 2.12
    #2150 -                 2.06
    #2160 -                 2.07
    #2170
    #2180 - 
    #2190 -                 2.04
    xbpm3_y = np.linspace(2.12, 2.04, 26)

    waxs_arc = [0]
    ai0 = 0
    ai_list = [7.24]
    stage_th_0 = 0
    stage_th_offset = 2

    for name, xs, ys, zs, xs_hexa in zip(names, x_piezo, y_piezo, z_piezo, x_hexa):
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)

        yield from bps.mv(piezo.th, ai0)
        yield from bps.mv(stage.th,stage_th_0)
        yield from alignement_gisaxs_doblestack(0.8)

        ai0 = piezo.th.position
        det_exposure_time(t, t)

        for i, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)
            # Do not take SAXS when WAXS detector in the way
            dets = [pil900KW] if wa < 10 else [pil1M, pil900KW]

            yield from bps.mv(piezo.x, xs)
            counter = 0

            for k, ais in enumerate(ai_list):
                yield from bps.mv(piezo.th, ai0 + ais)
                yield from bps.mv(stage.th, stage_th_offset)

                name_fmt = "{sample}_pos1_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                
                for e, xbpm3_ys in zip(energies, xbpm3_y):
                    yield from bps.mv(energy, e)
                    yield from bps.mv(xbpm3_pos.y, xbpm3_ys)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs + counter * 30)
                    counter += 1
                    
                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name, energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="CD", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)


                name_fmt = "{sample}_pos2_{energy}eV_ai{ai}_wa{wax}_bpm{xbpm}"
                for e, xbpm3_ys in zip(energies[::-1], xbpm3_y[::-1]):
                    yield from bps.mv(energy, e)
                    yield from bps.mv(xbpm3_pos.y, xbpm3_ys)
                    yield from bps.sleep(2)
                    if xbpm2.sumX.get() < 50:
                        yield from bps.sleep(2)
                        yield from bps.mv(energy, e)
                        yield from bps.mv(xbpm3_pos.y, xbpm3_ys)
                        yield from bps.sleep(2)
                    yield from bps.mv(piezo.x, xs + counter * 30)
                    counter += 1

                    bpm = xbpm2.sumX.get()
                    sample_name = name_fmt.format(sample=name,energy="%6.2f"%e, ai="%3.2f"%ais, wax=wa, xbpm="%4.3f"%bpm)
                    sample_id(user_name="CD", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=1)

            yield from bps.mv(piezo.th, ai0)
            yield from bps.mv(stage.th, stage_th_0)

def grazing_swaxs_2024_2(t=1):
    """
    standard GI-S/WAXS
    """
    
    names   = [  'FH02_reanneal_4h',  'FH03_reanneal_4h']
    piezo_x = [ -8500,   47000]
    piezo_y = [   2000 for n in names ]          
    piezo_z = [   3300,   3300   ]
    hexa_x =  [  -7.7,  -8.22]
    
    msg = "Wrong number of coordinates"
    assert len(piezo_x) == len(names), msg
    assert len(piezo_x) == len(piezo_y), msg
    assert len(piezo_x) == len(piezo_z), msg
    assert len(piezo_x) == len(hexa_x), msg

    waxs_arc = [ 0, 20 ]
    x_off = [0]
    incident_angles = [ 0.5, 2.25, 4.5]
    user_name = 'ZZ'

    for name, x, y, z, hx in zip(names, piezo_x, piezo_y, piezo_z, hexa_x):

        yield from bps.mv(piezo.x, x,
                          piezo.y, y,
                          piezo.z, z,
                          stage.x, hx)

        # Align the sample
        try:
            yield from alignement_gisaxs(0.1) #0.1 to 0.15
        except:
            print('\n\n\n\n\n\n\n\n\n\nCould not align, remeasure!!!\n\n\n\n\n\n\n\n\n\n')

        # Sample flat at ai0
        ai0 = piezo.th.position
        det_exposure_time(t, t)

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)
            dets = [pil900KW] if waxs.arc.position < 15 else [pil900KW, pil1M]

            # problems with the beamstop
            yield from bps.mv(waxs.bs_y, -3)

            for xx, x_of in enumerate(x_off):
                yield from bps.mv(piezo.x, x + x_of)
                for ai in incident_angles:
                    yield from bps.mv(piezo.th, ai0 + ai)

                    sample_name = f'{name}{get_scan_md()}_loc{xx}_ai{ai}'

                    sample_id(user_name=user_name, sample_name=sample_name)
                    print(f"\n\n\n\t=== Sample: {sample_name} ===")
                    yield from bp.count(dets)

        yield from bps.mv(piezo.th, ai0)

    sample_id(user_name='test', sample_name='test')
    det_exposure_time(0.5, 0.5)

def grazing_swaxs_2024_2_bg(t=1):
    """
    standard GI-S/WAXS
    """
    
    names   = [  'Copper_stage_bg1',  'Copper_stage_bg2']
    piezo_x = [ 2000,   38000]
    piezo_y = [   1200 for n in names ]          
    piezo_z = [   3300,   3300   ]
    hexa_x =  [  -8.22,  -8.22]
    
    msg = "Wrong number of coordinates"
    assert len(piezo_x) == len(names), msg
    assert len(piezo_x) == len(piezo_y), msg
    assert len(piezo_x) == len(piezo_z), msg
    assert len(piezo_x) == len(hexa_x), msg

    waxs_arc = [ 0, 20 ]
    x_off = [0]
    incident_angles = [ 0.5, 2.25, 4.5]
    user_name = 'ZZ'

    for name, x, y, z, hx in zip(names, piezo_x, piezo_y, piezo_z, hexa_x):

        yield from bps.mv(piezo.x, x,
                          piezo.y, y,
                          piezo.z, z,
                          stage.x, hx)

        # Align the sample
        try:
            yield from alignement_gisaxs(0.1) #0.1 to 0.15
        except:
            print('\n\n\n\n\n\n\n\n\n\nCould not align, remeasure!!!\n\n\n\n\n\n\n\n\n\n')

        # Sample flat at ai0
        ai0 = piezo.th.position
        det_exposure_time(t, t)

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)
            dets = [pil900KW] if waxs.arc.position < 15 else [pil900KW, pil1M]

            # problems with the beamstop
            yield from bps.mv(waxs.bs_y, -3)

            for xx, x_of in enumerate(x_off):
                yield from bps.mv(piezo.x, x + x_of)
                for ai in incident_angles:
                    yield from bps.mv(piezo.th, ai0 + ai)

                    sample_name = f'{name}{get_scan_md()}_loc{xx}_ai{ai}'

                    sample_id(user_name=user_name, sample_name=sample_name)
                    print(f"\n\n\n\t=== Sample: {sample_name} ===")
                    yield from bp.count(dets)

        yield from bps.mv(piezo.th, ai0)

    sample_id(user_name='test', sample_name='test')
    det_exposure_time(0.5, 0.5)


def zihan_giwaxs_line_samplebar_2024_3(t=0.5):
    """
    Hard X-ray GIWAXS, samples on regular GI stage
    """

    names =   [ 'ZZ_Reannal_1p5h_01']
    piezo_x = [  -43000]  # -43000, -800 , 40500
    piezo_y = [  2600]
    piezo_z = [ 0 for n in names ]
    # stage_x = [  -11, ..., 0, 0, 0, ..., 11]
    stage_x = [0 for n in names ]
    # piezo_z = [4200, 4100, ]

    msg = "Wrong number of coordinates"
    assert len(names)   == len(piezo_x), msg
    assert len(piezo_x) == len(piezo_y), msg
    assert len(piezo_y) == len(piezo_z), msg
    assert len(piezo_z) == len(stage_x), msg

    user_name = "ZZ"
    ai0 = piezo.th.position
    waxs_arc = [0, 7, 20]
    incident_angles = [0.5,1.5,3,4.5]
    # x_off = np.arange(0, 25 * 20 + 1, 25) - 250
    # x_off = [-250, -225, -200, -175, -150, -125, -100,  -75,  -50,  -25,    0,
    #            25,   50,   75,  100,  125,  150,  175,  200,  225,  250]
    # x_off = [-250,   -150,-50,0,50,  150,  250]
    x_off=[0]
    unaligned_samples = []


    for name, x, y, z, hx in zip(names, piezo_x, piezo_y, piezo_z, stage_x):
        yield from bps.mv(piezo.x, x,
                          piezo.y, y,
                          piezo.z, z,
                          piezo.th, ai0,
                          stage.x, hx,
        )
        # Align sample
        try:
            yield from alignement_gisaxs(0.1)
        except:
            unaligned_samples.append(name)
            print('\n\n\n\Could not align, remeasure!!!\n\n\n')
            break
        
        # Sample flat at ai0
        ai0 = piezo.th.position
        det_exposure_time(t, t)

        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)
            dets = [pil900KW] if waxs.arc.position < 15 else [pil1M, pil900KW]

            for xx, x_of in enumerate(x_off):
                yield from bps.mv(piezo.x, x + x_of)

                for ai in incident_angles:
                    yield from bps.mv(piezo.th, ai0 + ai)

                    sample_name = f'{name}_{get_scan_md()}_loc{xx}_ai{ai}'
                    sample_id(user_name=user_name, sample_name=sample_name)
                    print(f"\n\n\n\t=== Sample: {sample_name} ===")
                    yield from bp.count(dets)

    if unaligned_samples:
        f = RE.md['path'] + '/unaligned_samples.txt'
        with open(f, 'w') as file:
            for row in unaligned_samples:
                s = " ".join(map(str, row))
                file.write(s + '\n')

    yield from bps.mv(piezo.th, ai0)
    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)

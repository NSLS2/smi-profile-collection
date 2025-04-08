def run_swaxs_reuther_2023_cap(t=1):
    """
    Take WAXS and SAXS at several sample positions for averaging

    Specify central positions on the samples with xlocs and ylocs,
    then offsets from central positions with x_off and y_off.
    """

    names =   [ '529.5_9_mg_ml', '529.4_NATIVE', '529.2_NATIVE', '529.3_NATIVE', '538.2_NATIVE', '538.1_NATIVE', 
               '490_NATIVE_10w%', '460.2_NATIVE_10w%', '460.1_4.76_mg_ml', '476.3_NATIVE','476.2_NATIVE', '476.1_NATIVE']
    piezo_x = [  49800,  24300, 18050, 11800, 5550, -1200, -7200, -13950, -19950, 70-26450, -32700, -39200 ]
    piezo_y = [-192 for n in names]
   # piezo_y = [       -792,    -792, -792,  -792    ]
    hexa_y =  [0 for n in names]  #in mm

    x_off = [0]
    y_off = [0, 200, 400, 600]
 
    waxs_arc = [20, 0]

    user = "JR"

    # Check and correct sample names just in case
    names = [n.translate({ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ "}) for n in names]

    # Check if the length of xlocs, ylocs and names are the same
    msg = "Wrong number of coordinates"
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
                    name_fmt = ( "{sample}_{energy}keV_wa{wax}_sdd{sdd}m_loc{xx}{yy}")
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

# 2023-1 round 2
RE.md['SAF_number'] = 310643

def run_swaxs_reuther_2023_slide(t=1):
    """
    Take WAXS and SAXS at several sample positions for averaging

    Specify central positions on the samples with xlocs and ylocs,
    then offsets from central positions with x_off and y_off.
    """

    names =   [ '476.3_KAP', '527.1_KAP', 'BLANK_KAP', 'BLANK_GLASS', '538.1_GLASS']
    piezo_x = [ 47500, 19100, -6399, -25399, -31899]
    piezo_y = [ 5150,  5150,  4150, 3150, 3150]
    hexa_y =  [0 for n in names]  #in mm

    x_off = [0, 500]
    y_off = [0, 500]
    user = "JR"
    waxs_arc = [20, 0]

    # Check and correct sample names just in case
    names = [n.translate({ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ "}) for n in names]

    # Check if the length of xlocs, ylocs and names are the same
    msg = "Wrong number of coordinates"
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
                    name_fmt = ( "{sample}_{energy}keV_wa{wax}_sdd{sdd}m_loc{xx}{yy}")
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

def align_gisaxs_th_zihan(rang=0.3, point=31):
    th0 = piezo.th.position
    yield from bp.rel_scan([pil1M], piezo.th, -rang, rang, point)
    try:
        ps(plot=False)
        yield from bps.mv(piezo.th, ps.peak)
    except:
        print('\n\n\n\n\Could not aligned well with theta')
    yield from bps.mv(piezo.th, th0)

def zihan_giwaxs_alignment(angle=0.1):
    """
    Quicker alignment
    """

    # Activate the automated derivative calculation
    bec._calc_derivative_and_stats = True

    sample_id(user_name="test", sample_name="test")
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

def reuter_giwaxs_2023_1(t=0.5):
    """
    Hard X-ray GIWAXS, samples on Lakeshore heating stage but no heating.
    """

    names =   [ '523.1', '524.1', '538.1', 'GIWAX_GLASS_BLANK']
    piezo_x = [  58399,   35799,   11799, -4201]   
    piezo_y = [5703 for n in names]
    piezo_z = [  1378, 4178, 1978, 1978]
    #piezo_z = [5100 for n in names]
    stage_x = [13, 13, 13, 13]
    # piezo_z = [4200, 4100, ]

    assert len(names)   == len(piezo_x), f"Wrong list lenghts"
    assert len(piezo_x) == len(piezo_y), f"Wrong list lenghts"
    assert len(piezo_y) == len(piezo_z), f"Wrong list lenghts"

    user = "JR"
    waxs_arc = [20, 0]
    incident_angles = [0.1, 0.5]
    piezo_x_offs = [0, 200, 400]

    ai0 = piezo.th.position

    for name, x, y, z, hexa_x in zip(names, piezo_x, piezo_y, piezo_z, stage_x):
        yield from bps.mv(piezo.x, x,
                          piezo.y, y,
                          piezo.z, z,
                          stage.x, hexa_x,
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
                    wa = waxs.arc.position + 0.001
                    wa = str(np.round(float(wa), 1)).zfill(4)
                    sdd = pil1m_pos.z.position / 1000


                    # Sample name
                    name_fmt = ( "{sample}_{energy}keV_wa{wax}_sdd{sdd}m_loc{xx}{yy}_ai{ai}")
                    sample_name = name_fmt.format(
                        sample = name,
                        energy = "%.2f" % e,
                        wax = wa,
                        sdd = "%.1f" % sdd,
                        #loc=int(loc),
                        xx = 0,
                        yy = i,
                        ai = ai,
                    )
                    sample_id(user_name=user, sample_name=sample_name)
                    print(f"\n\n\n\t=== Sample: {sample_name} ===")
                    yield from bp.count(dets)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)

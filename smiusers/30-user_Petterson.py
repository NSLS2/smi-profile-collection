####line scab


def run_gi_sweden_SAXS(tim=0.5, sample="Test", ti_sl=60):
    # Slowest cycle:
    name = "TP"
    num = 2
    x_interface = [piezo.x.position]

    x_surface = x_interface[0] - 1500
    piezo_y_range = [-20, 20, 41]
    samples = [sample + "_interface"]

    surface_sample = sample + "_surface"
    angle = 0.1

    # Detectors, motors:
    dets = [pil1M, pil1mroi2]  # WAXS detector ALONE
    x_offset = 10
    t0 = time.time()

    yield from bps.mv(piezo.x, x_surface)
    yield from alignement_gisaxs(angle)
    yield from bps.mvr(piezo.th, angle)

    det_exposure_time(tim, tim)
    sample_id(user_name=name, sample_name=surface_sample)
    yield from bp.rel_scan(dets, piezo.y, *piezo_y_range)

    name_fmt = "{sample}_{angle}deg_{ti}sec"
    #    param   = '16.1keV'
    assert len(x_interface) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    for x, s in zip(x_interface, samples):
        yield from bps.mv(piezo.x, x)
        # yield from alignement_gisaxs_shorter(angle)
        # yield from bps.mvr(piezo.th, angle)
        for i in range(num):
            yield from bps.mv(piezo.x, x + x_offset * i)
            t1 = time.time()
            t_min = np.round((t1 - t0))
            sample_name = name_fmt.format(sample=s, angle=angle, ti="%5.5d" % t_min)
            sample_id(user_name=name, sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.rel_scan(dets, piezo.y, *piezo_y_range)

            yield from bps.sleep(ti_sl)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(1, 1)


def gisaxs_KTH_2021_1(t=1):

    global names, x_piezo, z_piezo, incident_angles, y_piezo_aligned, xs_hexa

    # names = ['1BL_DI', '3BL_DI', '5BL_DI', '1BL_NaCl', '3BL_NaCl', '5BL_NaCl', 'Si_wafer', 'PVAm', 'PVAm_CNF', 'PVAm_CNF_PAH', 'PEI']

    # x_piezo = [59000, 55000, 43000, 30000, 17000, 4000, -9000, -22000, -33000, -45000, -50000]
    # y_piezo = [ 7400,  7400,  7400,  7400,  7400, 7400,  7400,   7400,   7400,   7400,   7400]
    # z_piezo = [    0,     0,     0,     0,     0,    0,     0,      0,      0,      0,      0]
    # x_hexa =  [    8,     0,     0,     0,     0,    0,     0,      0,      0,      0,     -6]
    # incident_angles = [0.079829, 0.113749, 0.022469, 0.002876, 0.156458, 0.017894, 0.472448, -0.001836, 0.03759, -0.062716, 0.033808]
    # y_piezo_aligned = [7598.066, 7613.373, 7603.519, 7569.923, 7566.072, 7542.689, 7521.385, 7491.759, 7484.312, 7445.632, 7480.081]

    names = ["PEI_CNF", "PEI_CNF_PAH"]

    x_piezo = [18000, 1000]
    y_piezo = [7400, 7400]
    z_piezo = [0, 0]
    x_hexa = [0, 0]
    incident_angles = []
    y_piezo_aligned = []

    assert len(x_piezo) == len(
        names
    ), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(
        y_piezo
    ), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(
        z_piezo
    ), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(z_piezo)})"
    assert len(x_piezo) == len(
        x_hexa
    ), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexa)})"

    smi = SMI_Beamline()
    yield from smi.modeAlignment(technique="gisaxs")

    for name, xs_piezo, zs_piezo, ys_piezo, xs_hexa in zip(
        names, x_piezo, z_piezo, y_piezo, x_hexa
    ):
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, xs_piezo)
        yield from bps.mv(piezo.y, ys_piezo)
        yield from bps.mv(piezo.z, zs_piezo)
        yield from bps.mv(piezo.th, 0)

        # if ys_piezo>0:
        yield from alignement_gisaxs_multisample(angle=0.08)
        # else:
        #     yield from bps.mv(piezo.th, -1)
        #     yield from alignement_gisaxs_multisample_special(angle = 0.08)

        incident_angles = incident_angles + [piezo.th.position]
        y_piezo_aligned = y_piezo_aligned + [piezo.y.position]

    yield from smi.modeMeasurement()
    print(incident_angles)
    print(y_piezo_aligned)

    angle = [0.1]
    dets = [pil1M]
    det_exposure_time(t, t)

    for name, xs, zs, aiss, ys, xs_hexa in zip(
        names, x_piezo, z_piezo, incident_angles, y_piezo_aligned, x_hexa
    ):
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)
        yield from bps.mv(piezo.th, aiss)

        for an in angle:
            for i in range(1, 11, 1):
                yield from bps.mv(piezo.x, xs - i * 200)
                yield from bps.mv(piezo.th, aiss + an)
                name_fmt = "{sample}_sdd6.2m_16.1keV_ai{angl}deg_pos{pos}"
                sample_name = name_fmt.format(
                    sample=name, angl="%3.2f" % an, pos="%2.2d" % i
                )
                sample_id(user_name="PT", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")

                yield from bp.count(dets, num=1)

    angle = np.linspace(0.08, 0.4, 17)
    dets = [pil1M]
    det_exposure_time(t, t)

    for name, xs, zs, aiss, ys, xs_hexa in zip(
        names, x_piezo, z_piezo, incident_angles, y_piezo_aligned, x_hexa
    ):
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)
        yield from bps.mv(piezo.th, aiss)

        for j, an in enumerate(angle):
            yield from bps.mv(piezo.x, xs - 2500 - j * 50)
            yield from bps.mv(piezo.th, aiss + an)
            name_fmt = "{sample}_sdd6.2m_16.1keV_ai{angl}deg"
            sample_name = name_fmt.format(sample=name, angl="%3.2f" % an)
            sample_id(user_name="PT", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")

            yield from bp.count(dets, num=1)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.1, 0.1)


def run_gi_sweden_GISAXS(tim=0.5, sample="Test", ti_sl=77):
    # Slowest cycle:
    name = "TP"
    num = 1
    x_interface = [piezo.x.position]

    x_surface = x_interface[0] - 500

    piezo_y_range = [-20, 20, 41]
    samples = [sample + "_interface"]

    surface_sample = sample + "_surface"
    angle = 0.1

    # Detectors, motors:
    dets = [pil1M, pil1mroi2]  # WAXS detector ALONE
    x_offset = 10
    t0 = time.time()

    # yield from bps.mv(piezo.x, x_surface)
    # yield from alignement_gisaxs(angle)
    # yield from bps.mvr(piezo.th, angle)

    det_exposure_time(tim, tim)
    sample_id(user_name=name, sample_name=surface_sample)
    # yield from bp.rel_scan(dets, piezo.y, *piezo_y_range)

    # yield from bps.mv(piezo.x, x_interface)

    name_fmt = "{sample}_{angle}deg_{ti}sec"
    #    param   = '16.1keV'
    assert len(x_interface) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    for x, s in zip(x_interface, samples):
        yield from bps.mv(piezo.x, x)
        # yield from alignement_gisaxs_shorter(angle)
        # yield from bps.mvr(piezo.th, angle)
        for i in range(num):
            # x_pos = [piezo.x.position]
            # yield from bps.mv(piezo.x, x_pos+x_offset)
            yield from bps.mv(piezo.x, x + x_offset * i)
            t1 = time.time()
            t_min = np.round((t1 - t0))
            sample_name = name_fmt.format(sample=s, angle=angle, ti="%5.5d" % t_min)
            sample_id(user_name=name, sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.rel_scan(dets, piezo.y, *piezo_y_range)

            yield from bps.sleep(ti_sl)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(1, 1)

def alignment_start(sample_name='alignment'):
    """
    Attenuators in, beamstop out, ROI1 set to direct beam
    """

    smi = SMI_Beamline()
    yield from smi.modeAlignment()

    # Set direct beam ROI
    yield from smi.setDirectBeamROI()

    sample_id(user_name='test', sample_name=sample_name)
    proposal_id('2023_2', '311564_test')


def alignment_start_angle(angle=0.10):
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
    proposal_id('2023_2', '311564_Pettersson')


def alignment_org(angle=0.1):
    """
    Align using an original script
    """
    proposal_id('2023_2', '311564_test')
    yield from alignement_gisaxs_multisample(angle=angle)
    RE.md['ai_0'] = piezo.th.user_setpoint.get()
    proposal_id('2023_2', '311564_Pettersson')

def run_loop_measurement(t=0.5, name='test', loops=4, pump_t=180, total_t=600, jump_x=10):
    """
    RE(run_loop_measurement(t=1, name='1bl_PEI_10mM', loops=7, pump_t=210, total_t=720, jump_x=10))


    Take measurements in the loop

    Sample has to be aligned before starting the script and theta
    angle at 0 deg (flat sample).

    Parameters:
        t (float): detector exposure time of one frame,
        name (str): sample name,
        loops (int): number of loops (measurements taken),
        pump_t (flaot): initial delay to finish pumping,
        total_t (float): total time of one measurement iteration,
        jump_x (foat): relative move in piezo x after each y scan, in um,
            (be careful on the direction, move relative to - jump below).
    """

    incident_angles = [0.1, 0.4]
    waxs_arc = [20, 0]
    user = "TP"

    condition = (
        ( -1 < waxs.arc.position )
        and ( waxs.arc.position < 1 )
        and (waxs_arc[0] == 20)
    )

    if condition:
        waxs_arc = waxs_arc[::-1]
    
    ranges = { 0.1 : [-16, 16, 33],
               0.4 : [-25, 25, 51],
    }

    try:
        ai0 = RE.md['ai_0']
    except:
        yield from bp.count([])
        ai0 = db[-1].start['ai_0']
        print('Failed to acces RE.md')
    print(f'\n\nSample flat at theta = {ai0}')
    
    proposal_id('2023_2', '311564_Pettersson')
    #det_exposure_time(t, t)
    
    t_initial = time.time()

    for i in range(loops):
        t_start = time.time()
        print('Cycle number',i+1,'started at', (t_start - t_initial)/60)

        # Wait initial time for pumping to finish
        print(f'Start pumping now, going to wait for {pump_t} s\n')
        while (time.time() - t_start) < pump_t:
            print(f'Pumping time: {(time.time() - t_start):.1f} s')
            yield from bps.sleep(10)

        # Go over SAXS and WAXS
        t_measurement = ( time.time() - t_initial ) / 60
        for wa in waxs_arc:
            yield from bps.mv(waxs, wa)
            dets = [pil900KW] if waxs.arc.position < 15 else [pil1M, pil900KW]

            for ai in incident_angles:
                yield from bps.mv(piezo.th, ai0 + ai)
                yield from bps.mvr(piezo.x, - jump_x)

                t2 = 2 * t if ai == 0.4 else t
                det_exposure_time(t2, t2)

                try:
                    y_range = ranges[ai]
                except:
                    y_range = [-10, 10, 11]
                
                sample_name = f'{name}{get_scan_md()}_time{t_measurement:.1f}_ai{ai}'
                sample_id(user_name=user, sample_name=sample_name)
                print(f"\n\n\n\t=== Sample: {sample_name} ===")
                yield from bp.rel_scan(dets, piezo.y, *y_range, md=dict(ai=ai))
        
        yield from bps.mv(waxs, waxs_arc[0],
                          piezo.th, ai0)

        # Wait until the total loop time passes
        if i + 1 < loops:
            print(f'Waiting for the loop to last {total_t} s in total\n')
            sleep_count = 0
            while (time.time() - t_start) < total_t:
                sleep_count += 1
                if (sleep_count % 10 == 0):
                    print(f'Total time: {(time.time() - t_start):.1f} s')
                yield from bps.sleep(1)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)


"""
2023-2
Manual alignment 

# direct beam alignment
RE(alignment_start())

# half cut on direct beam
RE(rel_scan([pil1M], piezo.y, -300, 300, 21))
ps(der=True)
RE(mv(piezo.y, ps.cen)) # or replace ps.cen with a valid piezo y position

# th scan (rocking) on direct beam
RE(rel_scan([pil1M], piezo.th, -1, 1, 21))
ps()
RE(mv(piezo.th, ps.cen)) # or replace ps.cen with a valid th position
RE.md['ai_0'] = piezo.th.user_setpoint.get()

# repeat halfcat on direct beam if move in th was substantial
# RE(rel_scan([pil1M], piezo.y, -100, 100, 21))
# ps(der=True)
# RE(mv(piezo.y, ps.cen)) # or replace ps.cen with a valid piezo y position

# Reflected beam alignment
# remember to change angle for values different than 0.1
RE(alignment_start_angle(angle=0.1))
RE(mvr(piezo.th, 0.1))
# alternatively RE(mv(piezo.th,RE.md['ai_0'] + 0.1))

# th scan reflected
RE(rel_scan([pil1M], piezo.th, -0.2, 0.2, 31))
ps()
RE(mv(piezo.th, ps.cen))
RE.md['ai_0'] = piezo.th.user_setpoint.get() - 0.1

# y scan reflected
RE(rel_scan([pil1M], piezo.y, -50, 50, 21))
ps()
RE(mv(piezo.y, ps.cen))  # or replace ps.cen with a valid piezo y position

# final refinement of th
RE(rel_scan([pil1M], piezo.th, -0.025, 0.025, 21))
ps()
RE(mv(piezo.th, ps.cen))
RE.md['ai_0'] = piezo.th.user_setpoint.get() - 0.1

# if aligned and ready for data
RE(alignment_stop())

# if need to change angle of incident from 0.1 to differnt do it now
to thetha 0

RE(mvr(piezo.th, -0.1))
or
RE(mv(piezo.th, RE.md['ai_0']))
"""

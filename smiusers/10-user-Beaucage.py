# Align GiSAXS sample
import numpy as np

# ============================ SMI GI Alignment ===============================#R
alignbspos = 11
measurebspos = 1.15
GV7 = TwoButtonShutter("XF:12IDC-VA:2{Det:1M-GV:7}", name="GV7")


def alignmentmodeBoc():
    """Move gate valves, attenutators, and beamtop into GI alignment mode"""
    yield from bps.mv(waxs, 10)  # move the waxs detector out of the way
    yield from bps.mv(GV7.open_cmd, 1)  # open the SAXS gate valve
    yield from bps.mv(att2_6, "Retract")  # make sure that atten2_6 is out
    # yield from bps.mv(att2_8,"Insert")  # (for 7.5keV) make sure that atten2_8 is out
    yield from SMIBeam().insertFoils(1)  # (for >11keV in vac) 1 = insert
    yield from bps.sleep(1)

    # if bragg.position<8:
    #     yield from bps.mv(att1_5,"Insert")
    #     yield from bps.sleep(1)
    #     yield from bps.mv(att1_7,"Insert")
    #     # yield from SMIBeam().insertFoils(1)   # (for >11keV in vac) 1 = insert
    #     yield from bps.sleep(1)
    # elif bragg.position>8 and bragg.position<9:
    # #for 13.5 keV
    #     yield from bps.mv(att1_12,"Insert")
    #     yield from bps.sleep(1)
    yield from bps.mv(pil1m_bs_rod.x, alignbspos)  # move beamstop out of the way
    sample_id(user_name="test", sample_name="test")  # don't overwrite user data
    det_exposure_time(0.5)


def measurementmodeBoc():
    """Move gate valves, attenutators, and beamtop into GI measurement mode"""
    # yield from bps.mv(att2_8,"Retract") # (for 7.5keV)
    yield from SMIBeam().insertFoils(0)  # (for >11keV)
    yield from bps.mv(pil1m_bs_rod.x, measurebspos)
    yield from bps.sleep(1)
    # uncomment to close SAXS gate valve during measurements
    yield from bps.mv(GV7.close_cmd, 1)
    yield from bps.sleep(1)


def align_gisaxs_height_Boc(rang=0.3, point=31, der=False):
    yield from bp.rel_scan([pil1M], piezo.y, -rang, rang, point)
    ps(der=der)
    yield from bps.mv(piezo.y, ps.cen)


def align_gisaxs_th_Boc(rang=0.3, point=31):
    yield from bp.rel_scan([pil1M], piezo.th, -rang, rang, point)
    ps()
    yield from bps.mv(piezo.th, ps.peak)


def alignBoc(align_height=5000):
    """Do GI alignment"""
    det_exposure_time(0.5)
    sample_id(user_name="test", sample_name="test")
    yield from alignmentmodeBoc()
    yield from bps.mv(piezo.y, align_height)
    yield from bps.mv(pil1M.roi1.min_xyz.min_y, 883)
    yield from align_gisaxs_height_Boc(600, 16, der=True)
    yield from align_gisaxs_th_Boc(1, 11)
    yield from align_gisaxs_height_Boc(300, 11, der=True)
    yield from align_gisaxs_th_Boc(0.5, 11)
    yield from bps.mv(piezo.th, ps.peak + 0.2)
    yield from bps.mv(
        pil1M.roi1.min_xyz.min_y, 883 - 336
    )  # 336 offset = 0.4*3.14/180*8287/0.172
    yield from align_gisaxs_th_Boc(0.3, 31)
    yield from align_gisaxs_height_Boc(200, 21)
    yield from align_gisaxs_th_Boc(0.1, 21)
    yield from bps.mv(piezo.th, ps.cen)
    yield from measurementmodeBoc()


def alignBocBulk(align_height=5000):
    """Do GI alignment, but skip reflectivity step"""
    det_exposure_time(0.5)
    sample_id(user_name="test", sample_name="test")
    yield from alignmentmodeBoc()
    yield from bps.mv(piezo.y, align_height)
    yield from bps.mv(pil1M.roi1.min_xyz.min_y, 883)
    yield from align_gisaxs_height_Boc(600, 16, der=True)
    yield from align_gisaxs_th_Boc(1, 11)
    yield from align_gisaxs_height_Boc(300, 11, der=True)
    yield from align_gisaxs_th_Boc(0.5, 11)
    yield from bps.mv(piezo.th, ps.peak)
    yield from measurementmodeBoc()


# ============================ Custom Run Routines ===============================#


def run_giwaxsBocBoth():
    thresh_map = {}
    thresh_map[13400] = 10
    thresh_map[13473] = 10
    thresh_map[13550] = 10
    thresh_map[15125] = 11
    thresh_map[15199] = 11
    thresh_map[15275] = 11

    for e in [13400, 13473, 13550, 15125, 15199, 15275]:
        yield from bps.mv(energy, e)
        yield from run_giwaxsBoc(t=1.0, tag=f"{e:5d}keV_air")
        # yield from run_giwaxsBocBulk(t=0.5,tag=f'{e:5d}keV_air')


def run_giwaxsBoc(t=0.5, th_step=0.001, x_list_offset=0, tag=""):
    """GIWAXS Run Routine

    Runs a scan along a sample bar allowing for custom waxs_arc and theta_scan
    definitions. Also allows for 'walking' on the sample during measurement to
    avoid beam damage.

    """
    name = "PB"

    # define x-positions on sample bar
    # x_list = [,,,,,,,,,]

    # define names of samples on sample bar
    # sample_list = ['TP14n','TP27n','TM9n','TM15n','TM18n','TM22n','TM39n','TM39r','TM15r','TP27r']

    # x_list = x_list[::-1]
    # sample_list = sample_list[::-1]

    # shift xlist
    x_list = [x + x_list_offset for x in x_list]

    # sanity check
    assert len(x_list) == len(sample_list), f"Sample name/position list is borked"

    # Set up theta and waxs scans
    ## for Nils/Lee VAOI studies
    # th_array = np.arange(0.08,0.280,th_step)
    # waxs_arc = [2.83, 20.83, 4]
    # ## for non VAOI studies
    th_array = np.array([-0.12, 0])
    waxs_arc = [2.83, 22.83, 4]

    # sanity check
    waxs_step = (waxs_arc[1] - waxs_arc[0]) / (waxs_arc[2] - 1)
    assert (
        waxs_step <= 6.00001
    ), f"waxs arc step<6 for proper stitching: waxs_step = {waxs_step}"

    # need to walk around sample to avoid beam_damage
    glob_xoff = 2000
    glob_walk_length = 2000  # microns
    glob_xstep = int(glob_walk_length / th_array.shape[0])

    dets = [pil300KW, pil1M]
    for x, sample in zip(x_list, sample_list):  # loop over samples on bar
        yield from bps.mv(piezo.x, x)  # move to next sample
        yield from bps.mv(piezo.th, 0.05)  # set stage angle to ~0
        yield from alignBoc(6000)  # run alignment routine
        plt.close("all")  # close alignment plots (memory issues)

        th_start = piezo.th.position
        det_exposure_time(t)
        for j, th in enumerate(th_start + th_array):  # loop over incident angles
            # uncomment to walk around sample to avoid beam_damage
            yield from bps.mv(piezo.x, (x - glob_xoff + j * glob_xstep))

            # convert angles to "real" angles
            real_th = 0.2 + th_array[j]  # 0.2 = alignment angle for Si
            yield from bps.mv(piezo.th, th)

            sample_name = sample + "_{th:5.4f}deg".format(th=real_th)
            if tag:
                sample_name += "_" + tag
            sample_id(user_name="PB", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")

            yield from bp.scan(dets, waxs, *waxs_arc)

            # uncomment below for manual snake mode.
            # waxs_arc[1],waxs_arc[0] = waxs_arc[0],waxs_arc[1]

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5)


def run_giwaxsBocBulk(t=1, tag=""):
    name = "PB"
    # x_list = [] # GI bar 1 - Lee samples
    # x_list = [50000,38000,30000,23500,11500,2500,-5500,-12500,-19500,-26500,-33500] # GI bar 2 - Peter membrane dry samples
    # x_list = [11500,2500] # GI bar 2 - Peter membrane dry samples
    # x_list = [] # GI bar 3 - Lee low priority and Nils samples
    x_list = [38000, 30000, 23500, 11500, 2500]  # GI bar 2 - Peter membrane dry samples

    # sample_list = ['BTBT_noAu','BTBT_noPFBT','BTBT_PFBT','BTBT_Au','BTBT_NoOx','BTBT_Ox','DIF_noAu','DIF_Au','DIF_noPFBT','DIF_PFBT'] # GI bar 1 - Lee samples
    # sample_list = ['mLbL_dry_7500','Dow6bulk_dry_7500','Dow7bulk_dry_7500',
    #               'Dow8bulk_dry_7500','Dow10bulk_dry_7500','SWC4bulk_dry_7500','SWC4iTS_dry_7500',
    #               'Dow6iTS_dry_7500','Dow7iTS_dry_7500','Dow8iTS_dry_7500', 'Dow10iTS_dry_7500'] # GI bar 2 - Peter membrane dry samples
    # sample_list = ['Dow10bulk_dry_7500','SWC4bulk_dry_7500'] # GI bar 2 - Peter membrane dry samples
    sample_list = [
        "Dow6bulk_dry_7500",
        "Dow7bulk_dry_7500",
        "Dow8bulk_dry_7500",
        "Dow10bulk_dry_7500",
        "SWC4bulk_dry_7500",
    ]  # GI bar 2 - Peter membrane dry samples

    # th_list = np.arange(0.08,0.280,0.0005) # for Nils/Lee VAOI studies
    th_array = np.array([0.0, 0.15])
    waxs_arc = [2.83, 2.83, 1]

    # sanity check
    # waxs_step = (waxs_arc[1] - waxs_arc[0])/waxs_arc[2]
    # assert waxs_step<=6.00001,f'waxs arc step<6 for proper stitching: waxs_step = {waxs_step}'

    # need to walk around sample to avoid beam_damage
    glob_xoff = 1000
    glob_xstep = 200

    dets = [pil300KW, rayonix]
    assert len(x_list) == len(sample_list), f"Sample name/position list is borked"
    for x, sample in zip(x_list, sample_list):  # loop over samples on bar
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(piezo.th, 0.05)
        yield from alignBocBulk()
        plt.close("all")
        # yield from bps.mv(att2_6,"Insert") # add in attenutator to avoid saturation

        th_start = piezo.th.position
        det_exposure_time(t)
        for j, th in enumerate(th_start + th_array):
            # uncomment to walk around sample to avoid beam_damage
            # yield from bps.mv(piezo.x, (x-glob_xoff+j*glob_xstep))

            # convert angles??
            real_th = 0.2 + th_array[j]  # from critical angle / alignment angle for Si
            yield from bps.mv(piezo.th, th)

            sample_name = sample + "_{th}deg".format(th=real_th)
            if tag:
                sample_name += "_" + tag
            sample_id(user_name=name, sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")

            yield from bp.scan(dets, waxs, *waxs_arc)

            # uncomment below for manual snake mode.
            waxs_arc[1], waxs_arc[0] = waxs_arc[0], waxs_arc[1]

        # yield from bps.mv(att2_6,"Retract")
    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5)


def nexafs_scan(det, energies, incident_angle, ctime):
    sample_name = "{sample}_{th:5.4f}deg_{e:5d}eV_DB".format(
        sample=sample, th=incident_angle, e=int(energies[0])
    )

    # move to theta 0 + value
    yield from bps.mvr(piezo.th, incident_angle)

    # Scan the energies
    det_exposure_time(ctime, ctime)
    yield from bp.scan(
        [pil300KW, pil300kwroi2], energy, energies[0], energies[-1], len(energies)
    )


def giwaxsTempSingleWaxsSeries(
    x_list, y_list, th_list, sample_list, waxs_arc, num, t=1, user="BP"
):
    print(num)
    for waxspos in waxs_arc:
        for x, y, th, sample in zip(
            x_list, y_list, th_list, sample_list
        ):  # loop over samples on bar
            yield from bps.mv(piezo.x, x)  # move to next sample
            yield from bps.mv(piezo.y, y)  # move to next sample
            yield from bps.mv(piezo.th, th)  # move to next sample
            print(x)
            th_meas = 0.10 + piezo.th.position
            th_real = 0.10

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
            yield from bp.count(dets)


def heatingLoop():
    # Load 1 xpos = [-11000,2000] #2493 is from -2000 to -11000, 2523 is from 2000 to 11000
    xpos = [-12000, 1000]  # 2493 is from -2500 to -12000, 2523 is from 2000 to 11000
    names = ["DPP_2493", "DPP_2523"]

    xstep = 200
    quickalignevery = 15  # do a quickalign every n exposures
    sleepbetweenexps = 10
    nscans = 2000  # Arbitrary high number; I don't know how the runengine would handle an infinite loop but effectively this.  End the run with ctrl-c + RE.stop()

    ypos = [7100, 7100]
    thpos = [0.06, 0.06]

    for i, x in enumerate(xpos):
        yield from bps.mv(piezo.x, x + 4500)
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

    xmodfwd = np.arange(0, 9001, xstep)
    xmodbck = np.arange(9001, 0, xstep)

    xmod = np.concatenate((xmodfwd, xmodbck))

    while counter < nscans:
        for xmv in xmod:
            lclxpos = xpos + xmv
            yield from giwaxsTempSingleWaxsSeries(
                lclxpos, ypos, thpos, names, [2.93, 8.93], counter, t=3, user="BP2-1"
            )
            sleep(sleepbetweenexps)
            counter += 1
            yield from giwaxsTempSingleWaxsSeries(
                lclxpos, ypos, thpos, names, [8.93, 2.93], counter, t=3, user="BP2-1"
            )
            sleep(sleepbetweenexps)
            counter += 1
            if counter % quickalignevery is 0 or counter % quickalignevery is 1:
                for i, x in enumerate(xpos):
                    yield from bps.mv(waxs, 8.93)
                    yield from bps.mv(piezo.x, x + 4500)
                    yield from alignement_gisaxs(0.08)
                    ypos[i] = piezo.y.position
                    thpos[i] = piezo.th.position


def afterlunchrun():
    #  xl1 = [-50000,-37500,-25000,-8000,2000,14000,24000]
    #  sl1 = ['TP14n','TP27n','TM9n','TM15n','TM18n','TM22n','TM39n']
    #  ea1 = [13480]
    xl2 = [36500]
    sl2 = ["TM39r"]
    ea2 = [15195, 15200, 15205, 15195]
    xl3 = [41000, 47000]
    sl3 = ["TM15r", "TP27r"]
    ea3 = [15195, 15200, 15205, 15195]
    yield from run_giwaxsEnergyBoc(xl2, sl2, ea2, t=2)
    yield from run_giwaxsEnergyBoc(xl3, sl3, ea3, t=2)


def GIbar2res():
    # Samples for which energy scans are needed
    xl1 = [-48000, -39000, -29000, -19000]
    sl1 = ["TP14r", "TM9r", "TM18r", "TM22r"]
    # Samples for single energy shot
    xl2 = [-9000, 1000, 9000, 20000, 26000, 38000, 46500]
    sl2 = ["TM9b", "TP27b", "TM39b", "TP14b", "SVPS-10PEO", "SVPS-10P2VP", "SVPS"]
    ea_waxs_Rb = [15195, 15200, 15205, 15195]
    ea_waxs_Br = [13480, 13485, 13490, 13495, 13480]
    # yield from run_giwaxsEnergyBoc(xl1,sl1,ea_waxs_Br,t=2)
    yield from run_giwaxsEnergyBoc(xl1, sl1, ea_waxs_Rb, t=2)


def GIbar2nonres():
    # WAXS and SAXS
    xl1 = [-9000, 1000, 9000, 20000]
    sl1 = ["TM9b", "TP27b", "TM39b", "TP14b"]
    # SAXS only
    xl2 = [26000, 38000, 46500]
    sl2 = ["SVPS-10PEO", "SVPS-10P2VP", "SVPS"]

    xl2 = [38000, 46500]
    sl2 = ["SVPS-10P2VP", "SVPS"]

    waxs_arc_nowaxs = [8.9, 8.9, 1]
    waxs_arc_forwaxs = [2.9, 20.9, 4]

    angle_arc_GISAXS = np.linspace(0.08, 0.25, 18)
    angle_arc_GIWAXS = np.linspace(0.1, 0.2, 2)
    # yield from run_gisaxsAngleBoc(xl1,sl1,angle_arc_GIWAXS,waxs_arc_forwaxs)
    yield from run_gisaxsAngleBoc(xl2, sl2, angle_arc_GISAXS, waxs_arc_nowaxs, t=2)


def earlyeveningtransmissionrun():
    ea_nexafs_Br = np.linspace(13450, 13500, 51)
    ea_nexafs_Rb = np.linspace(15150, 15250, 51)
    ea_waxs_Rb = [15195, 15200, 15205, 15195]
    ea_waxs_Br = [13480, 13485, 13490, 13480]
    # Samples for static runs
    xl1 = [43500, 37000, 30500, 23500, 15500, 8500, 2500]
    sl1 = [
        "Dow6bulk",
        "Dow7bulk",
        "Dow8bulk",
        "Dow10bulk",
        "SWC4bulk",
        "Dow6BAbulk",
        "SWC4BAbulk",
    ]
    ea1 = [13480]

    # Sampls for energy scans
    xl2 = [-4500, -11000, -17000, -22000, -26500]
    sl2 = [
        "Dow6bulkRbBr100",
        "Dow7bulkRbBr100",
        "Dow8bulkRbBr100",
        "Dow10bulkRbBr100",
        "SWC4bulkRbBr100",
    ]

    yield from run_saxswaxsEnergyBoc(xl1, sl1, ea1, ea1, t=0.3)
    yield from run_saxswaxsEnergyBoc(xl2, sl2, ea_waxs_Br, ea_nexafs_Br, t=0.3)
    yield from run_saxswaxsEnergyBoc(xl2, sl2, ea_waxs_Rb, ea_nexafs_Rb, t=0.3)


def tuesdaymorningtransmissionrun():
    ea_nexafs_Br = np.linspace(13450, 13500, 51)
    ea_nexafs_Rb = np.linspace(15150, 15250, 51)
    ea_waxs_Rb = [15195, 15200, 15205, 15195]
    ea_waxs_Br = [13480, 13485, 13490, 13495, 13480]
    # Samples for static runs
    xl = [30000.2, 24500.2, 19000.2, 9250.2, -1000.2, -6000.2, -11500.2, -17500.2]
    sl = [
        "Dow6bulkRbBr50",
        "Dow7bulkRbBr50",
        "Dow10bulkRbBr50",
        "SWC4bulkRbBr50",
        "Dow6bulkRbBr500",
        "Dow7bulkRbBr500",
        "Dow10bulkRbBr500",
        "SWC4bulkRbBr500",
    ]

    # yield from run_saxswaxsEnergyBoc([4000],['TapeBlank2'],[13480],[13480],t=1)
    # yield from run_saxswaxsEnergyBoc(xl,sl,ea_waxs_Br,ea_nexafs_Br,t=0.3)
    yield from run_saxswaxsEnergyBoc(xl, sl, ea_waxs_Rb, ea_nexafs_Rb, t=0.3)


def tuesdaylunchtransmission():
    name1 = [
        "AS1-034",
        "AS1-038A",
        "AS1-038B",
        "AS1-038C",
        "AS1-038D",
        "AS1-038E",
        "AS1-036A",
        "AS1-036B",
        "AS1-036C",
        "AS1-036D",
        "AS1-036E",
    ]
    pos1 = [
        -44000,
        -35000,
        -27000,
        -19000,
        -10000,
        -2000,
        8000,
        16500,
        25000,
        33000,
        41500,
    ]  # centers

    name2 = [
        "PT5E-010A",
        "PT5E-010B",
        "PT5E-010C",
        "AS1-040A",
        "AS1-040B",
        "AS1-040C",
        "AS1-040D",
        "AS1-040E",
    ]
    pos2 = [-35000, -27000, -19000, -10000, -2000, 8000, 16500, 25000]

    x_range = [-500, 500, 4]
    y_range = [-250, 225, 4]

    # yield from run_saxsmapBoc(pos1,name1,x_range=x_range,y_range=y_range,t=1,y_cen=-4500)
    yield from run_saxsmapBoc(
        pos2, name2, x_range=x_range, y_range=y_range, t=1, y_cen=10250
    )


def run_giwaxsEnergyBoc(x_list, sample_list, energy_arc_waxs, t=5, tag=""):
    """GIWAXS Run Routine"""
    # x_list = [-50000,-37500,-25000,-8000,2000,14000,24000,36000,41000,47000]

    # define names of samples on sample bar
    # sample_list = ['TP14n','TP27n','TM9n','TM15n','TM18n','TM22n','TM39n','TM39r','TM15r','TP27r']

    ct_nexafs = 0.2
    # x_list = x_list[::-1]
    # sample_list = sample_list[::-1]

    # shift xlist
    # x_list = [x+x_list_offset for x in x_list]

    # sanity check
    assert len(x_list) == len(sample_list), f"Sample name/position list is borked"

    # Set up theta and waxs scans
    ## for Nils/Lee VAOI studies
    # th_array = np.arange(0.08,0.280,th_step)
    # waxs_arc = [2.83, 20.83, 4]
    # ## for non VAOI studies

    th_array = np.array([0.08, 0.14])
    waxs_arc = [2.9, 20.9, 4]
    # energy_arc_waxs = [13480,13485,13490,13480]

    energy_arc_nexafs_Br = np.linspace(13450, 13500, 51)
    energy_arc_nexafs_Rb = np.linspace(15150, 15250, 51)

    dets = [pil300KW, pil1M]
    for x, sample in zip(x_list, sample_list):  # loop over samples on bar
        yield from bps.mv(piezo.x, x)  # move to next sample

        yield from remove_suspender(susp_xbpm2_sum)
        yield from bps.mv(energy, energy_arc_waxs[0])

        yield from bps.sleep(10)
        yield from install_suspender(susp_xbpm2_sum)

        yield from alignement_gisaxs(0.1)  # run alignment routine

        th_meas = np.array([0.10 + piezo.th.position])
        th_real = [0.10]

        # yield from bps.mv(waxs,2.9) #move the waxs dectector to the measurement position
        # det_exposure_time(ct_nexafs, ct_nexafs)
        # yield from nexafs_scan([pil1M], energy_arc_nexafs_Rb, 0.10, ct_nexafs)

        # yield from remove_suspender( susp_xbpm2_sum)
        # yield from bps.mv(energy, 15200)
        # yield from bps.sleep(10)
        # yield from install_suspender( susp_xbpm2_sum)
        #
        # yield from nexafs_scan([pil1M], energy_arc_nexafs_Rb, 0.10, ct_nexafs)

        yield from bps.mv(
            waxs, 2.9
        )  # move the waxs dectector to the measurement position

        det_exposure_time(t, t)
        for i, th in enumerate(th_meas):  # loop over incident angles
            # convert angles to "real" angles
            yield from bps.mv(piezo.th, th)

            for k, e in enumerate(energy_arc_waxs):
                sample_name = "{sample}_{th:5.4f}deg_{e:5d}eV_{num}".format(
                    sample=sample, th=th_real[i], e=e, num=k
                )
                sample_id(user_name="PB", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")

                yield from remove_suspender(susp_xbpm2_sum)
                yield from bps.mv(energy, e)
                yield from bps.sleep(10)
                yield from install_suspender(susp_xbpm2_sum)

                # yield from bp.scan(dets, energy, e, e, 1)
                yield from bp.scan(dets, waxs, *waxs_arc)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)


def run_gisaxsAngleBoc(x_list, sample_list, angle_arc, waxs_arc, t=5, tag=""):
    """GIWAXS Run Routine"""
    # x_list = [-50000,-37500,-25000,-8000,2000,14000,24000,36000,41000,47000]

    # define names of samples on sample bar
    # sample_list = ['TP14n','TP27n','TM9n','TM15n','TM18n','TM22n','TM39n','TM39r','TM15r','TP27r']

    ct_nexafs = 0.2
    # x_list = x_list[::-1]
    # sample_list = sample_list[::-1]

    # shift xlist
    # x_list = [x+x_list_offset for x in x_list]

    # sanity check
    assert len(x_list) == len(sample_list), f"Sample name/position list is borked"

    # Set up theta and waxs scans
    ## for Nils/Lee VAOI studies
    # th_array = np.arange(0.08,0.280,th_step)
    # waxs_arc = [2.83, 20.83, 4]
    # ## for non VAOI studies

    # th_array  = np.array([0.08,0.14])
    # waxs_arc = [2.9, 20.9, 4]
    # energy_arc_waxs = [13480,13485,13490,13480]

    dets = [pil300KW, pil1M]
    for x, sample in zip(x_list, sample_list):  # loop over samples on bar
        yield from bps.mv(piezo.x, x)  # move to next sample

        yield from alignement_gisaxs(0.1)  # run alignment routine

        th_meas = (
            angle_arc + piezo.th.position
        )  # np.array([0.10 + piezo.th.position, 0.20 + piezo.th.position])
        th_real = angle_arc

        # yield from bps.mv(waxs,2.9) #move the waxs dectector to the measurement position
        # det_exposure_time(ct_nexafs, ct_nexafs)
        # yield from nexafs_scan([pil1M], energy_arc_nexafs_Rb, 0.10, ct_nexafs)

        # yield from remove_suspender( susp_xbpm2_sum)
        # yield from bps.mv(energy, 15200)
        # yield from bps.sleep(10)
        # yield from install_suspender( susp_xbpm2_sum)
        #
        # yield from nexafs_scan([pil1M], energy_arc_nexafs_Rb, 0.10, ct_nexafs)

        yield from bps.mv(
            waxs, 2.9
        )  # move the waxs dectector to the measurement position

        det_exposure_time(t, t)
        for i, th in enumerate(th_meas):  # loop over incident angles
            # convert angles to "real" angles
            yield from bps.mv(piezo.th, th)

            sample_name = "{sample}_{th:5.4f}deg__{num}".format(
                sample=sample, th=th_real[i], num=i
            )
            sample_id(user_name="PB", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")

            # yield from bp.scan(dets, energy, e, e, 1)
            yield from bp.scan(dets, waxs, *waxs_arc)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5)


def run_saxswaxsEnergyBoc(
    x_list, sample_list, energy_arc_waxs, energy_arc_nexafs, t=5, tag=""
):
    """GIWAXS Run Routine"""
    # x_list = [-50000,-37500,-25000,-8000,2000,14000,24000,36000,41000,47000]

    # define names of samples on sample bar
    # sample_list = ['TP14n','TP27n','TM9n','TM15n','TM18n','TM22n','TM39n','TM39r','TM15r','TP27r']

    ct_nexafs = 0.2
    # x_list = x_list[::-1]
    # sample_list = sample_list[::-1]

    # shift xlist
    # x_list = [x+x_list_offset for x in x_list]

    # sanity check
    assert len(x_list) == len(sample_list), f"Sample name/position list is borked"

    # Set up theta and waxs scans
    ## for Nils/Lee VAOI studies
    # th_array = np.arange(0.08,0.280,th_step)
    # waxs_arc = [2.83, 20.83, 4]
    # ## for non VAOI studies

    # th_array  = np.array([0.08,0.14])
    waxs_arc = [2.9, 20.9, 4]
    # energy_arc_waxs = [13480,13485,13490,13480]

    # energy_arc_nexafs_Br = np.linspace(13450, 13500, 51)
    # energy_arc_nexafs_Rb = np.linspace(15150,15250,51)

    dets = [pil300KW, pil1M]
    for x, sample in zip(x_list, sample_list):  # loop over samples on bar
        yield from bps.mv(piezo.x, x)  # move to next sample

        yield from bps.mv(
            waxs, 2.9
        )  # move the waxs dectector to the measurement position
        det_exposure_time(ct_nexafs, ct_nexafs)
        yield from remove_suspender(susp_xbpm2_sum)
        yield from bps.mv(energy, energy_arc_nexafs[0])
        yield from bps.sleep(10)
        yield from install_suspender(susp_xbpm2_sum)

        yield from nexafs_scan([pil1M], energy_arc_nexafs, 0.10, ct_nexafs)

        yield from bps.mv(
            waxs, 2.9
        )  # move the waxs dectector to the measurement position

        det_exposure_time(t, t)
        for k, e in enumerate(energy_arc_waxs):
            sample_name = "{sample}_{e:5d}eV_{num}".format(sample=sample, e=e, num=k)
            sample_id(user_name="PB", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")

            yield from remove_suspender(susp_xbpm2_sum)
            yield from bps.mv(energy, e)
            yield from bps.sleep(10)
            yield from install_suspender(susp_xbpm2_sum)

            # yield from bp.scan(dets, energy, e, e, 1)
            yield from bp.scan(dets, waxs, *waxs_arc)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5)


def mondaynightmaps():
    samples = ["PT5E-015A", "PT5E-015B"]
    positions = [-19000, 21000]  # centers
    x_range = [-17500, 17500, 176]
    y_range = [-10000, 10000, 101]

    yield from run_saxsmapBoc(
        positions, samples, x_range=x_range, y_range=y_range, t=0.2
    )


def run_saxsmapBoc(
    x_list, samples, x_range=[-500, 500, 11], y_range=[-250, 250, 11], t=1, y_cen=0
):
    """Simple SAXS/WAXS transmission measurements

    Runs a scan along a transmission bar where, for each sample center in the
    x_list, measurements are taken in a grid defined by x_range and y_range
    about this center.

    """
    name = "PT"

    # Detectors, motors:

    yield from bps.mv(waxs, 8.9)
    dets = [pil1M]  # dets = [pil1M,pil300KW]

    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    det_exposure_time(t, t)
    yield from bps.mv(piezo.y, y_cen)
    yield from bps.mv(piezo.th, 0)
    for x, sample in zip(x_list, samples):
        yield from bps.mv(piezo.x, x)
        sample_id(user_name=name, sample_name=sample)
        # yield from bp.scan(dets, piezo.x, *x_range)  # 1 line scane
        yield from bp.rel_grid_scan(
            dets, piezo.x, *x_range, piezo.y, *y_range, 1
        )  # 1 = snake, 0 = not-snake

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)


def run_saxsBoc(x_list, samples, energies, t=1):
    """Simple SAXS/WAXS transmission measurements

    Runs a scan along a transmission bar where, for each sample center in the
    x_list, measurements are taken in a grid defined by x_range and y_range
    about this center.

    """
    name = "PB"

    # Detectors, motors:
    dets = [pil1M, pil300KW]  # dets = [pil1M,pil300KW]
    x_range = [-500, 500, 11]
    y_range = [-250, 250, 11]

    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    det_exposure_time(t)
    yield from bps.mv(piezo.y, 0)
    yield from bps.mv(piezo.th, 0)
    for x, sample in zip(x_list, samples):
        yield from bps.mv(piezo.x, x)
        sample_id(user_name=name, sample_name=sample)
        # yield from bp.scan(dets, piezo.x, *x_range)  # 1 line scane
        yield from bp.rel_grid_scan(
            dets, piezo.x, *x_range, piezo.y, *y_range, 1
        )  # 1 = snake, 0 = not-snake

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5)


def run_saxsEnergyBoc(t=1, tag=""):
    """Simple SAXS/WAXS transmission measurements

    Runs a scan along a transmission bar where, for each sample center in the
    x_list, measurements are taken in a grid defined by x_range and y_range
    about this center.

    """
    name = "PB"
    x_list = [
        -44000,
        -37500,
        -31500,
        -25000,
        -18500,
        -12000,
        -5500,
        1000,
        7000,
        13000,
        19500,
        26000,
        32500,
        39000,
        45500,
    ]  # tray 1
    # x_list  = [13000,19500,26000,32500,39000,45500] #tray 1
    samples = [
        "cap-H2Oblank",
        "SWC4sol-RbBr20mM",
        "SWC4sol-RbCl20mM",
        "SWC4sol-NaBr20mM",
        "SWC4sol-NaCl20mM",
        "SWC4sol-RbBr100mM",
        "SWC4sol-RbCl100mM",
        "SWC4sol-NaBr100mM",
        "SWC4sol-NaCl100mM",
        "SWC4-THF",
        "SWC4-H2OEXCH",
        "blank-RbBr100mM",
        "blank-RbCl100mM",
        "blank-NaBr100mM",
        "blank-NaCl100mM",
    ]
    # samples = ['SWC4-THF','SWC4-H2OEXCH','blank-RbBr100mM','blank-RbCl100mM','blank-NaBr100mM','blank-NaCl100mM']

    # Detectors, motors:
    dets = [pil300KW]
    x_range = [-500, 500, 11]
    energy_arc = [13400, 13473, 13550, 15125, 15199, 15275]

    # sanity check
    assert len(x_list) == len(samples), f"Sample name/position list is borked"

    det_exposure_time(t)
    yield from bps.mv(piezo.y, 8000)  # 8000 for capillaries
    yield from bps.mv(piezo.th, 0)
    for x, sample in zip(x_list, samples):
        yield from bps.mv(piezo.x, x)

        for k, e in enumerate(energy_arc):

            sample_name = sample + "_{e:5d}eV".format(e=e)
            if tag:
                sample_name += "_" + tag
            sample_id(user_name=name, sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            energy.move(e)
            yield from bps.mv(energy, e)
            sleep(1)

            yield from bp.rel_scan(dets, piezo.x, *x_range)  # 1 line scan

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5)


ROIsizey = "XF:12IDC-ES:2{Det:1M}ROI1:SizeY"
ROIMiny = "XF:12IDC-ES:2{Det:1M}ROI1:MinY"
ROIsizex = "XF:12IDC-ES:2{Det:1M}ROI1:SizeX"
ROIMinx = "XF:12IDC-ES:2{Det:1M}ROI1:MinX"

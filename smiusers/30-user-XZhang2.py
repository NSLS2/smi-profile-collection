##Collect data:

# SMI: 2021/10/29

# create proposal:  proposal_id('2021_3', '30000_YZhang_XZ')    #create the proposal id and folder
# create proposal:  proposal_id('2021_3', '30000_YZhang_Nov')    #create the proposal id and folder
# create proposal:  proposal_id('2021_3', '307961_Dinca')    #create the proposal id and folder


# Energy: 16.1 keV, 0.77009 A
# SAXS distance 5000
# SAXS in vacuum and WAXS in vacuum


# For WAXS,
# WAXS beam center: [  87, 97   ], there is bad pixel here  could check later,  (BS: X: -20.92 )
# Put Att and move bs to check the BC_WAXS, --> [ 87, 97 ]


# beam center [488, 591]


# Fisrt Run, 1 samples, make hexpod Y = -5
# Pizo_Z, 2100


sample_dict = {
    1: "XZ_S1_1_Chitosan_Cu_Fiber_Wet",
    2: "XZ_S2_2_NaCellulose",
    3: "XZ_S2_7_Crab_Chitasan",
    4: "XZ_S2_9_CuNa_CellusloseNaOH",
    5: "XZ_S2_9_CuNa_Celluslose",
}
pxy_dict = {
    1: (-32800, -1000),
    2: (-27300, -700),
    3: (-16000, -1000),
    4: (-2600, -1000),
    5: (20400, -6000),
}

# manually measure each sampls
# Sam1,
# mov_sam(1)
# RE( measure_waxs( t = 1, waxs_angle=0, att='None', dy=0, user_name='', sample= None )  )
# Change CHI to 6 deg, do measrue_S1,, sid00005868 -->  sid00005871
# Change CHI to 0 deg, do measrue_S1,,
# Sam2-5,
#  For sam5, rot chi to 6, sid00005912  -->    sid00005915
# Then measrue SAXS, looks like no signal in SAXS for all samples


# Second Run, 4 samples + MIT_Sample, make hexpod Y = -5
# make hexpod Y = -6
# Pizo_Z, 2100


sample_dict = {
    1: "XZ_S2_1_Wood",
    2: "XZ_S2_4_CrabTendonChitin",
    3: "YG_Standard_Al2O3",
    4: "XZ_S2_5_SquidChitin",
    5: "XZ_S2_6_CrabTendonChitosan",
    6: "Dinca_Unkown_X1",
    7: "Dinca_Unkown_X2",
    8: "Dinca_Unkown_X3",
    9: "Dinca_PowderA",
    10: "Dinca_PowderB",
}

pxy_dict = {
    1: (31789, -8000),
    2: (25800, -700),
    3: (13800, -1000),
    4: (7600, -6000),
    5: (-4400, -6000),
}


# name_sam( 1 )
# 2, looks nice
# 4, squid, looks find
# 5, looks nice
# sample 3, Al2O3, standard sample

# 6-10, DC samples


def measure_Al2O3():
    WA = np.array([0, 5, 7, 10, 15, 20, 25, 27, 30, 35, 40, 45, 47, 50, 55, 60])
    sample = RE.md["sample"]
    pz_list = np.arange(-5000, 5000, 100)
    for wa in WA:
        for pz in pz_list:
            RE(bps.mv(piezo.z, pz))
            sami = sample + "_PZ_%.0f" % piezo.z.position
            RE(
                measure_waxs(
                    t=1, waxs_angle=wa, att="None", dy=0, user_name="", sample=sami
                )
            )


def measure_One():
    WA = np.array(
        [
            0,
            5,
            15,
            25,
        ]
    )
    if abs(waxs.arc.user_readback.value - WA.max()) < 2:
        WA = WA[::-1]
    for wa in WA:
        RE(
            measure_waxs(
                t=1, waxs_angle=wa, att="None", dy=0, user_name="", sample=None
            )
        )


def check_sample_loc(sleep=5):
    ks = list(sample_dict.keys())
    for k in ks:
        mov_sam(k)
        time.sleep(sleep)


def measure_XZ_Run2(Index=[1], N=8):
    # Index = [1,2,3,6,7]
    for i in Index:
        mov_sam(i)
        measure_waxs0_XZ_scany(N=N)
    for i in Index:
        mov_sam(i)
        measure_waxs20_XZ_scany(N=N)


def measure_waxs0_XZ_scany(N=10):
    sample = RE.md["sample"]
    dets = [pil900KW, pil300KW]
    for i in range(N):
        RE(
            measure_waxs(
                t=1, waxs_angle=0, att="None", dy=0, user_name="XZ", sample=sample
            )
        )
        RE(bps.mvr(piezo.y, 500))


def measure_waxs20_XZ_scany(N=10):
    sample = RE.md["sample"]
    dets = [pil900KW, pil300KW]
    for i in range(N):
        RE(
            measure_wsaxs(
                t=1, waxs_angle=20, att="None", dy=0, user_name="XZ", sample=sample
            )
        )
        RE(bps.mvr(piezo.y, 500))


##################################################
############ Some convinent functions#################
#########################################################


def movx(dx):
    RE(bps.mvr(piezo.x, dx))


def movy(dy):
    RE(bps.mvr(piezo.y, dy))


def get_posxy():
    return round(piezo.x.user_readback.value, 2), round(piezo.y.user_readback.value, 2)


def move_waxs(waxs_angle=8.0):
    RE(bps.mv(waxs, waxs_angle))


def move_waxs_off(waxs_angle=8.0):
    RE(bps.mv(waxs, waxs_angle))


def move_waxs_on(waxs_angle=0.0):
    RE(bps.mv(waxs, waxs_angle))


def mov_sam(pos):
    px, py = pxy_dict[pos]
    RE(bps.mv(piezo.x, px))
    RE(bps.mv(piezo.y, py))
    sample = sample_dict[pos]
    print("Move to pos=%s for sample:%s" % (pos, sample))
    RE.md["sample"] = sample


def name_sam(pos):
    sample = sample_dict[pos]
    print("Change sample name at pos=%s to:%s" % (pos, sample))
    RE.md["sample"] = sample


def check_saxs_sample_loc(sleep=5):
    ks = list(sample_dict.keys())
    for k in ks:
        mov_sam(k)
        time.sleep(sleep)


def snap_waxs(t=0.1):
    dets = [pil300KW]
    sample_id(user_name="test", sample_name="test")
    det_exposure_time(t)
    yield from (bp.count(dets, num=1))


def snap_saxs(t=0.1):
    dets = [pil1M]
    sample_id(user_name="test", sample_name="test")
    det_exposure_time(t)
    yield from (bp.count(dets, num=1))


def measure_samples_saxs_map1():
    mov_sam(0)
    # xlist = np.linspace( 38000, 41600, 121 )  #[ 38700,   39100,    39500,  39900, 40100   ]
    # ylist = [ ]
    # first try
    xlist = [
        39500,
    ]
    ylist = np.linspace(-6030, -6030 + 2 * 500, 501)  # NO peaks beam damage?
    # second try
    xlist = [39500 - 500]
    ylist = np.linspace(-6030, -6030 + 4 * 200, 201)  # NO peaks, beam damage?
    # Third try
    xlist = [39500 - 1000]
    ylist = np.linspace(-6030, -6030 + 10 * 100, 101)  # Some peaks
    # Forth try
    xlist = [39500 + 200]
    ylist = np.linspace(-6030, -6030 + 10 * 100, 101)  # No Peaks, beam damage already
    # Fifth try
    xlist = [39500 + 1000]
    ylist = np.linspace(-6030, -6030 + 10 * 100, 101)  # #Some peaks
    # six try
    xlist = np.linspace(38000, 38000 + 60 * 50, 51)  #
    ylist = [-5200]

    # 7 try
    xlist = np.linspace(38000, 38000 + 60 * 50, 51)  #
    ylist = [-4500]

    print(xlist, ylist)
    RE(
        measure_saxs_map(
            xlist,
            ylist,
            user_name="HZ",
            sample=None,
            att="None",
        )
    )


def do_one_map(sam_id, xstart, ystart_up, ystart_bot, dia=3):
    mov_sam(sam_id)
    if dia == 3:
        Nx = 18

    xlist = np.linspace(xstart, xstart + 220 * (Nx - 1), Nx)
    ylist = np.linspace(ystart_up, ystart_up + 30 * 50, 51)
    sample = RE.md["sample"] + "Up"
    RE(
        measure_saxs_map(
            xlist,
            ylist,
            t=1,
            user_name="HZ",
            sample=sample,
            att="None",
        )
    )
    ylist = np.linspace(ystart_bot, ystart_bot + 30 * 50, 51)
    sample = RE.md["sample"] + "Bot"
    RE(
        measure_saxs_map(
            xlist,
            ylist,
            t=1,
            user_name="HZ",
            sample=sample,
            att="None",
        )
    )
    mov_sam(sam_id)
    sample = RE.md["sample"] + "ScanY"
    RE(
        measure_saxs_scany(
            N=220,
            t=1,
            user_name="HZ",
            sample=sample,
            att="None",
        )
    )


def measure_samples_saxs_map():

    do_one_map(1, xstart=35600, ystart_up=-7800, ystart_bot=-1900)
    do_one_map(2, xstart=28400, ystart_up=-7300, ystart_bot=-2900)
    do_one_map(3, xstart=20500, ystart_up=-4200, ystart_bot=300)
    do_one_map(4, xstart=35600, ystart_up=-7800, ystart_bot=-3400)
    do_one_map(5, xstart=14000, ystart_up=-5500, ystart_bot=-1000)
    do_one_map(6, xstart=5000, ystart_up=-6600, ystart_bot=-3600)
    do_one_map(7, xstart=-11700, ystart_up=-7200, ystart_bot=-900)


def measure_saxs_map(
    xlist,
    ylist,
    t=1,
    user_name="HZ",
    sample=None,
    att="None",
):
    if sample is None:
        sample = RE.md["sample"]
    dets = [pil1M]
    for px in xlist:
        yield from bps.mv(piezo.x, px)
        for py in ylist:
            yield from bps.mv(piezo.y, py)
            name_fmt = "{sample}_x{x_pos}_y{y_pos}_det{saxs_z}m_expt{expt}s_att{att}_sid{scan_id:08d}"
            sample_name = name_fmt.format(
                sample=sample,
                x_pos=np.round(piezo.x.position, 2),
                y_pos=np.round(piezo.y.position, 2),
                saxs_z=np.round(pil1m_pos.z.position, 2),
                expt=t,
                att=att,
                scan_id=RE.md["scan_id"],
            )
            det_exposure_time(t, t)
            sample_id(user_name=user_name, sample_name=sample_name)
            yield from bp.count(dets, num=1)


def measure_saxs_scany(
    N,
    t=1,
    user_name="HZ",
    sample=None,
    att="None",
):
    if sample is None:
        sample = RE.md["sample"]
    dets = [pil1M]
    for i in range(N):
        name_fmt = "{sample}_x{x_pos}_y{y_pos}_det{saxs_z}m_expt{expt}s_att{att}_sid{scan_id:08d}"
        sample_name = name_fmt.format(
            sample=sample,
            x_pos=np.round(piezo.x.position, 2),
            y_pos=np.round(piezo.y.position, 2),
            saxs_z=np.round(pil1m_pos.z.position, 2),
            expt=t,
            att=att,
            scan_id=RE.md["scan_id"],
        )
        det_exposure_time(t, t)
        sample_id(user_name=user_name, sample_name=sample_name)
        yield from bp.count(dets, num=1)
        yield from bps.mv(piezo.y, 30)


def measure_pindiol_current():
    fs.open()
    yield from bps.sleep(0.3)
    pd_curr = pdcurrent1.value
    fs.close()
    print("--------- Current pd_curr {}\n".format(pd_curr))
    return pd_curr


def measure_saxs(t=1, att="None", dy=0, user_name="XZ", sample=None):
    if sample is None:
        sample = RE.md["sample"]
    dets = [pil1M]
    # att_in( att )
    if dy:
        yield from bps.mvr(piezo.y, dy)
    name_fmt = (
        "{sample}_x{x_pos}_y{y_pos}_det{saxs_z}m_expt{expt}s_att{att}_sid{scan_id:08d}"
    )
    sample_name = name_fmt.format(
        sample=sample,
        x_pos=np.round(piezo.x.position, 2),
        y_pos=np.round(piezo.y.position, 2),
        saxs_z=np.round(pil1m_pos.z.position, 2),
        expt=t,
        att=att,
        scan_id=RE.md["scan_id"],
    )

    det_exposure_time(t, t)
    sample_id(user_name=user_name, sample_name=sample_name)
    print(f"\n\t=== Sample: {sample_name} ===\n")
    print("Collect data here....")
    yield from bp.count(dets, num=1)
    # att_out( att )
    sample_id(user_name="test", sample_name="test")
    # det_exposure_time(0.5)


def measure_waxs(t=1, waxs_angle=0, att="None", dy=0, user_name="XZ", sample=None):
    if sample is None:
        sample = RE.md["sample"]
    yield from bps.mv(waxs, waxs_angle)
    dets = [pil900KW, pil300KW]
    # att_in( att )
    if dy:
        yield from bps.mvr(piezo.y, dy)
    name_fmt = "{sample}_x{x_pos:05.2f}_y{y_pos:05.2f}_z{z_pos:05.2f}_waxs{waxs_angle:05.2f}_expt{expt}s_sid{scan_id:08d}"
    sample_name = name_fmt.format(
        sample=sample,
        x_pos=piezo.x.position,
        y_pos=piezo.y.position,
        z_pos=piezo.z.position,
        waxs_angle=waxs_angle,
        expt=t,
        scan_id=RE.md["scan_id"],
    )

    det_exposure_time(t, t)
    sample_id(user_name=user_name, sample_name=sample_name)
    print(f"\n\t=== Sample: {sample_name} ===\n")
    print("Collect data here....")
    yield from bp.count(dets, num=1)
    # att_out( att )
    # sample_id(user_name='test', sample_name='test')


def measure_wsaxs(t=1, waxs_angle=20, att="None", dy=0, user_name="XZ", sample=None):
    if sample is None:
        sample = RE.md["sample"]
    yield from bps.mv(waxs, waxs_angle)
    dets = [pil900KW, pil300KW, pil1M]
    # att_in( att )
    if dy:
        yield from bps.mvr(piezo.y, dy)
    name_fmt = "{sample}_x{x_pos:05.2f}_y{y_pos:05.2f}_z{z_pos:05.2f}_det{saxs_z}_waxs{waxs_angle:05.2f}_expt{expt}s_sid{scan_id:08d}"
    sample_name = name_fmt.format(
        sample=sample,
        x_pos=piezo.x.position,
        y_pos=piezo.y.position,
        z_pos=piezo.z.position,
        saxs_z=np.round(pil1m_pos.z.position, 2),
        waxs_angle=waxs_angle,
        expt=t,
        scan_id=RE.md["scan_id"],
    )

    det_exposure_time(t, t)
    sample_id(user_name=user_name, sample_name=sample_name)
    print(f"\n\t=== Sample: {sample_name} ===\n")
    print("Collect data here....")
    yield from bp.count(dets, num=1)
    # att_out( att )
    # sample_id(user_name='test', sample_name='test')


def measure_series_saxs(
    t=[1],
    dys=[
        0,
        -500,
        -1000,
        -1500,
        -2000,
    ],
):
    ks = list(sample_dict.keys())
    for k in ks:
        mov_sam(k)
        for dy in dys:
            for ti in t:
                RE(measure_saxs(t=ti, att="None", dy=dy))


def measure_series_waxs(
    t=[1],
    waxs_angle=20,
    dys=[
        0,
        -500,
        -1000,
        -1500,
        -2000,
    ],
):
    ks = list(sample_dict.keys())[:8]
    for k in ks:
        mov_sam(k)
        for dy in dys:
            for ti in t:
                RE(measure_waxs(t=ti, waxs_angle=waxs_angle, att="None", dy=dy))


def measure_waxs_multi_angles(
    t=1.0,
    att="None",
    dy=0,
    user_name="",
    saxs_on=False,
    waxs_angles=[0.0, 6.5, 13.0],
    inverse_angle=False,
):

    # waxs_angles = np.linspace(0, 65, 11)   #the max range
    # waxs_angles =   np.linspace(0, 65, 11),
    # [ 0. ,  6.5, 13. , 19.5]

    waxs_angle_array = np.array(waxs_angles)
    if inverse_angle:
        waxs_angle_array = waxs_angle_array[::-1]
    dets = [pil300KW]
    max_waxs_angle = np.max(waxs_angle_array)
    for waxs_angle in waxs_angle_array:
        yield from bps.mv(waxs, waxs_angle)
        sample = RE.md["sample"]
        if dy:
            yield from bps.mvr(piezo.y, dy)
        name_fmt = "{sample}_x{x_pos:05.2f}_y{y_pos:05.2f}_z{z_pos:05.2f}_waxs{waxs_angle:05.2f}_expt{expt}s_sid{scan_id:08d}"
        sample_name = name_fmt.format(
            sample=sample,
            x_pos=piezo.x.position,
            y_pos=piezo.y.position,
            z_pos=piezo.z.position,
            waxs_angle=waxs_angle,
            expt=t,
            scan_id=RE.md["scan_id"],
        )
        print(sample_name)
        if saxs_on:
            if waxs_angle == max_waxs_angle:
                dets = [
                    pil1M,
                    pil300KW,
                ]  # waxs, maxs, saxs = [pil300KW, rayonix, pil1M]
            else:
                dets = [pil300KW]

        det_exposure_time(t, t)
        sample_id(user_name=user_name, sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")
        # yield from bp.scan(dets, waxs, *waxs_arc)
        yield from bp.count(dets, num=1)
    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5)


def snap_waxs(t=0.1):
    dets = [pil900KW]
    sample_id(user_name="test", sample_name="test")
    det_exposure_time(t)
    yield from (bp.count(dets, num=1))


def snap_saxs(t=0.1):
    dets = [pil1M]
    sample_id(user_name="test", sample_name="test")
    det_exposure_time(t)
    yield from (bp.count(dets, num=1))


def measure_pindiol_current():
    fs.open()
    yield from bps.sleep(0.3)
    pd_curr = pdcurrent1.value
    fs.close()
    print("--------- Current pd_curr {}\n".format(pd_curr))
    return pd_curr

##Collect data:

# SMI: 2021/9/22


# create proposal:  proposal_id('2021_3', '30000_YZhang')    #create the proposal id and folder
# Energy: 16.1 keV, 0.77009 A
# SAXS distance 5000
# SAXS in vacuum and WAXS in air


# low div beam, 220 X 30 um2
# For 8 meter, beamStopX: 0.7 , 1M: X 0.25 , Center [ 490, 588 ]
# For 5 meter, beamstopX: 1.85 , 1M, X  1.13,   Center, [490, 588 ]
# For 3 meter, beamstopX: 1.9, 1M, X, 1.43 Center, [490, 588 ]
### For 2 meter, beamstopX: 1.8, 1M, X, 1.05 Center, [490, 588 ]


#  RE( shopen() )  # to open the beam and feedback
#  RE( shclose())

#  %run -i

# The beam center on SAXS:  [ 485, 566 ]
# Energy: 16.1 keV, 0.77009 A
# SAXS distance 5000
## For pindiol:
#   No filter, it's saturated ( 125257)
#   Sn30 um, X1, still saturated ( 125257 )  #RE(bps.mv(att1_9.open_cmd, 1))
#   Sn30 um, X2, still saturated ( 125256 )  #RE(bps.mv(att1_10.open_cmd, 1))
#   Sn30 um, X3 (X1 + X2) ,  (67713 )
#   Sn30 um, X4,  (27456)
# Sn30 um, X5,  (11334 )
#   Sn30 um, X8,  (722)


# For WAXS,
# WAXS beam center: [  87, 97   ], there is bad pixel here  could check later,  (BS: X: -20.92 )
# Put Att and move bs to check the BC_WAXS, --> [ 87, 97 ]


# beam center [488, 591]


## For 8 meter, beamStopX: 1.04857 , 1M: X 0.24 , Center [ 490, 588 ]
#
########################
# First Run for HZhang, microfocusing,

# sample_dict = {    0: 'HZ_S21_10nmAu_10nmSalt_SiliconOil',     }
# pxy_dict = {   0:  ( 39400, -5300)  }


########################
# Second Run for HZhang, low divergency

# low div beam, 220 X 30 um2
# Hexpond Y changes from 0 to 1
# For 8 meter, beamStopX: 0.7 , 1M: X 0.247 , Center [ 490, 586 ]


# sample_dict = {    1: 'HZ2_S21_PEG2K_Au10_SilOil_10mMNaCl_R1', 2: 'HZ2_S22_PEG2K_Au10_SilOil_500mMNaCl_R1', 3: 'HZ2_S23_20nmAu_10nmSalt_SiliconOil',
# 4: 'HZ2_S24_PEG2K_Au20_SilOil_500mMNaCl_R1', 5: 'HZ2_S25_PEG2K_Au10_SilOil_10mMNaCl_tubingD_356', 6: 'HZ2_S26_PEG2K_Au10_SilOil_10mMNaCl_tubingD_3000',
# 7: 'HZ2_S27_PEG2K_Au10_SilOil_10mMNaCl_tubingD_223'    }
# pxy_dict = {  1:  ( 37400, -8000), 2:  ( 30000, -7500),  3:  ( 22200, -4500  ),  4:  ( 37400, -8000), 5:  ( 15800, -5500), 6:  ( 7200, -7000), 7:  ( -2200, -6000),
# 7:  ( -10200, -7500),   }  #looks like the 4 is not correct,  the 4 just repeat 1, 5 should sample4, 6 should sample5, 7 should be sample 7. Did not measrue Sample 6


########################
# Third Run for HZhang, low divergency, Thursday night, around 11:30 pm

# low div beam, 220 X 30 um2
# Hexpond Y changes from 0 to -2
# For 8 meter, beamStopX: 0.7 , 1M: X 0.247 , Center [ 490, 586 ]


sample_dict = {
    1: "HZ2_S21_PEG2K_Au10_SilOil_10mMNaCl_R1",
    2: "HZ2_S22_PEG2K_Au10_SilOil_500mMNaCl_R1",
    3: "HZ2_S23_20nmAu_10nmSalt_SiliconOil",
    4: "HZ2_S24_PEG2K_Au20_SilOil_500mMNaCl_R1",
    5: "HZ2_S25_PEG2K_Au10_SilOil_10mMNaCl_tubingD_356",
    6: "HZ2_S26_PEG2K_Au10_SilOil_10mMNaCl_tubingD_3000",
    7: "HZ2_S27_PEG2K_Au10_SilOil_10mMNaCl_tubingD_223",
    8: "HZ3_S31_PEG2K_Au10_SilOil_100mMNaCl_100nM",
    9: "HZ3_S32_PEG2K_Au10_SilOil_100mMNaCl_20nM",
    10: "HZ3_S33_PEG2K_Au10_OA_100mMNaCl_20nM",
    11: "HZ3_S34_PEG2K_Au10_BuOH_100mMNaCl_20nM",
    12: "HZ3_S35_PEG2K_Au10_SilOil_10mMNaCl_20nM",
    13: "HZ3_S36_PEG2K_Au10_SilOil_500mMNaCl_20nM",
}
pxy_dict = {
    1: (37400, -8200),
    2: (30000, -7500),
    3: (22200, -4500),
    4: (15800, -4300),
    5: (7200, -7000),
    6: (-2200, -6000),
    7: (-10200, -7500),
    8: (-16900, -3000),
    9: (-22500, -3660),
    10: (-28800, -2460),
    11: (-33100, -2200),
    12: (-37200, -4600),
    13: (-41100, -5300),
}


def measure_samples_saxs_map_923Ngt():
    for i in [1, 2, 3, 4, 5, 7]:
        do_one_yscan(i)
    do_one_map(6, xstart=-4200, ystart_up=-5600, ystart_bot=-1800)
    do_one_map(8, xstart=-18400, ystart_up=-3000, ystart_bot=1200)
    do_one_map(9, xstart=-24100, ystart_up=-3400, ystart_bot=900)
    do_one_map(10, xstart=-30400, ystart_up=-2460, ystart_bot=1940)
    do_one_map(11, xstart=-34700, ystart_up=-2200, ystart_bot=-700)
    do_one_map(12, xstart=-38500, ystart_up=-4600, ystart_bot=1000)
    do_one_map(13, xstart=-42700, ystart_up=-5200, ystart_bot=-1000)


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


def do_one_yscan(sam_id):
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
        yield from bps.mv(piezo.x, px)  # move to the absolute position
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
        # yield from   bps.mv(piezo.y, 30)  #here is something wrong, should move a relative postion, have to redo this y scan!!!! NOTE at Thursady afternoon (9/23)
        yield from bps.mvr(
            piezo.y, 30
        )  # here is something wrong, should move a relative postion, have to redo this y scan!!!! NOTE at Thursady afternoon (9/23)


def measure_pindiol_current():
    fs.open()
    yield from bps.sleep(0.3)
    pd_curr = pdcurrent1.value
    fs.close()
    print("--------- Current pd_curr {}\n".format(pd_curr))
    return pd_curr


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

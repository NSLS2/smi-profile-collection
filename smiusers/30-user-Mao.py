# proposal_id('2022_1', '309554_Mao')
# in this macro using stage to replace piezo
# for 900kw,
# move_waxs( 0 )  #the beamstop is 15.7
# put att  14-18keV, Sn 60 um, 7X, move beamstop  -10
# for waxs=0 --> find the beam center is [218, 308] on albula
# for waxs=1 --> find the beam center is [218, 280] on albula
# for waxs=2 --> find the beam center is [218, 252] on albula
# for waxs=3 --> find the beam center is [218, 223] on albula
# for waxs=4 --> find the beam center is [218, 194] on albula, part block by chip
# for waxs=5 --> find the beam center is [218, 166] on albula
# for waxs=6 --> find the beam center is [218, 138] on albula
# for waxs=7 --> find the beam center is [218, 110] on albula
# for waxs=8 --> find the beam center is [218, 81] on albula
# for waxs=9 --> find the beam center is [218, 53] on albula
# for waxs=10 --> find the beam center is [218, 25] on albula
# for waxs=11 --> find the beam center touch the edge
# for waxs=12 --> find the beam center is out of the detector

# Mar4, 8m, pindiol beamstop
# direct beam position [ 925, 559 ]
# beamstop [ -199, 9.2]
# 1M, [75, -61, 8000]


def move_8m():
    # direct beam position [ 925, 559 ]
    RE(bps.mv(SAXS.x, 75))
    RE(bps.mv(SAXS.y, -61))
    RE(bps.mv(SAXS.z, 8000))
    RE(bps.mv(pil1m_bs_pd.x, -199))
    RE(bps.mv(pil1m_bs_pd.y, 9.2))


def move_5m():
    # direct beam position [ 961, 561 ]
    RE(bps.mv(SAXS.x, 75))
    RE(bps.mv(SAXS.y, -61))
    RE(bps.mv(SAXS.z, 5000))
    RE(bps.mv(pil1m_bs_pd.x, -198.5))
    RE(bps.mv(pil1m_bs_pd.y, 8.8))


def move_2m():
    # direct beam position [ 921, 561 ]
    RE(bps.mv(SAXS.x, 75))
    RE(bps.mv(SAXS.y, -61))
    RE(bps.mv(SAXS.z, 2000))
    RE(bps.mv(pil1m_bs_pd.x, -198.5))
    RE(bps.mv(pil1m_bs_pd.y, 8.8))


# reminder
# every time when makes changes to this file, save it first (ctrl s), then load in the ipython,
#  %run -i /home/xf12id/.ipython/profile_collection/startup/users/30-user-Mao.py


## procedure:
# close/search hutch
# do vacumm # on CSS-screen, click Auto Evacuate
# unti 2:TCG:7  turn green (the value should be less ~e-3), manually  open the 2:GV-7
# during the vaccum, you can define sample info, i.e.,  sample_dict, pxy_dict
# RE( shopen() )  #open shutter
# restart 900kw ( find the det3 terminal, ), enter ctrl X, wait until the "  * " show up, then enter 'setthreshold energy 16100 autog 11000'
# you are ready to run samples
######### for in-situ humidity
# t0 = set_humidity(80)
# do bleed, click Auto Bleed to Air, after ~ 5s, then open WAXS soft vent, then open WAXS full vent
# utill 2:TCG:7 goes to 700, you can open the chamber door
# close shutter,   RE(shclose())
# open hutch


## plans
# the first batch, 12:10 am  #wood sample
# we alread defined t0  [    ]
#   measure_one_humidity(  t0,  dx=0, dy=0 ,  t=0.5   )
#  should same as  measure_one_humidity_many_cycling(  t0, N = 1,  sleep_time = 10 * 60  )


# mount 8 sample,  #wood sample
# t0 = set_humidity(20) #same as in air
# measure_one_humidity(  t0,  dx=0, dy=0 ,  t=0.5   )
# t0 = set_humidity(80)
# measure_one_humidity_many_cycling(  t0, N = 12,  sleep_time = 10 * 60  ) #run 120 min


# tomorrow morning #crab
# mount 8 sample,
# t0 = set_humidity(20) #same as in air
# measure_one_humidity(  t0,  dx=0, dy=0 ,  t=0.5   )
# t0 = set_humidity(80)
# measure_one_humidity_many_cycling(  t0, N = 12,  sleep_time = 10 * 60  ) #run 120 min
# t0 = set_humidity(0)
# measure_one_humidity_many_cycling(  t0, N = 12,  sleep_time = 10 * 60  ) #run 120 min

# t0 = set_humidity(80)
# measure_one_humidity_many_cycling(  t0, N = 12,  sleep_time = 10 * 60  ) #run 120 min
# t0 = set_humidity(0)
# measure_one_humidity_many_cycling(  t0, N = 12,  sleep_time = 10 * 60  ) #run 120 min


# Then static sample <=20 samples
# will use same setup
# t0 = set_humidity(20) #same as in air
# measure_one_humidity(  t0,  dx=0, dy=0 ,  t=0.5   )


# RUN 1, 6:20 pm,  in-situ
#
# sample_dict = {  4: 'WT-AS-1', 5: 'WT-AS2',6: 'WT-AS-3',7: 'WT-AS-4-4',8: 'WT-yu-super',9: 'WT-yu-dense1',10: 'WT-yu-dense2',11: 'WT-yu-delig-thin'}
# sample_dict = {  4: 'std-Al2O3', 9: 'AgBH'}#
sample_dict = {9: "AgBH"}
pxy_dict = {
    4: (24.9, 0.5),
    5: (18.6, 0.5),
    6: (12.2, 0.5),
    7: (5.8, 0.5),
    8: (-0.6, 0.5),
    9: (-6.8, 0.5),
    10: (-13.1, 0.5),
    11: (-19.5, 0.5),
}


user_name = "YM"


def close_flow():
    wet_old = moxa_in.ch2_sp.get()
    dry_old = moxa_in.ch1_sp.get()
    ch = readHumidity()
    print("Change wet flow from: %s to :%s." % (wet_old, 0))
    print("Change Dry flow from: %s to :%s." % (dry_old, 0))
    setDryFlow(0)
    setWetFlow(0)
    return time.time()


def set_humidity(h):
    """

        #2022/3/4 humidity list
    humidity    wet     dry         eq.time recheck
    80          3       2.35    5 min 75%, struggle
    80          3       2.3     30s 78%;    1 min 80.5;  2min 82.5
    *80          3       2.33    1 min 79%   5 min 80.2%  10 min drop to 79.7
    *70          3       2.5     1 min 61% struggle
    70          3       2.45    1 min 66%
    *70            3       2.42    1 min 69%; 2min 70%; 5 min 70.04%
    *60          3       2.53    30s 60.1%; 1 min 60.7%; 5 min 60.6%
    50          3       3       1 min 42%; 4 min 41.79%
    50          3       2.7       1 min 49.9%; 2 min 50.1%; 5 min 50.3%

    #20220304 conclusion, updated chart
    humidity    wet dry
    80          3   2.33
    70          3   2.42
    60          3   2.53
    50          3   2.7
    42%         3   3
    """
    available_h = [0, 20, 42, 50, 60, 70, 80, 100]
    h_dict = {
        0: [0, 4],
        20: [0, 0],
        42: [3, 3],
        50: [3, 2.7],
        60: [3, 2.53],
        70: [3, 2.42],
        80: [3, 2.33],
        100: [5, 0],
    }
    if h not in available_h:
        print(
            "This humidity: %s is not available. The availalbe are: %s"
            % (h, available_h)
        )
    else:
        wet_old = moxa_in.ch2_sp.get()
        dry_old = moxa_in.ch1_sp.get()
        ch = readHumidity()
        print("Change wet flow from: %s to :%s." % (wet_old, h_dict[h][0]))
        print("Change Dry flow from: %s to :%s." % (dry_old, h_dict[h][1]))
        print("The current humidity is: %s." % ch)
        setWetFlow(h_dict[h][0])
        setDryFlow(h_dict[h][1])
        return time.time()


def get_humidity():
    return readHumidity()


# WA = np.array( [ 0, 5, 15, 25, 45 ])


def measure_one_humidity_many_cycling(t0, N=10, sleep_time=1):
    """suppose the waxs is off the beam"""
    ks = list(sample_dict.keys())  # [:1]
    dx = 0
    n = 30
    for i in range(N):
        if i > 30:
            dy = -0.5 + 0.03 * (i - 30)
        else:
            dy = 0.5 - 0.03 * i
        measure_one_humidity(t0, dx=dx, dy=dy, t=0.5)
        time.sleep(sleep_time)


def measure_one_humidity_continue(t0, N=10, sleep_time=10):
    for i in range(N):
        measure_one_humidity(t0, dx=0, dy=0, t=0.5)
        time.sleep(sleep_time)


# def measure_many_humidity(  t0,  dx=0, dy=0 ,  t=0.5   ):


def measure_one_humidity(t0, dx=0, dy=0, t=0.5):
    """suppose the waxs is off the beam"""
    ks = list(sample_dict.keys())  # [:1]
    # measure_one_humidity_WAXS( t0=t0, ks=ks,  dx=dx, dy=dy ,  t=t   )
    measure_one_humidity_SAXS(t0=t0, ks=ks, dx=dx, dy=dy, t=t)
    # measure_one_humidity_SAXS( t0=t0, ks=ks,  dx=dx, dy=dy ,  t=t   )


def measure_one_humidity_WAXS(t0, ks, dx=0, dy=0, t=0.5):
    WA = np.array([0, 5, 15, 25, 45])  # [:1]
    # WA = np.array( [ 0, 5, 15, 25 ])   # [:1]
    # WA = np.array( [ 0, 5  ])   # [:1]

    for wa in WA:
        # print( wa )
        move_waxs(wa)
        _measure_one(t0=t0, ks=ks, dets=[pil900KW], waxs_angle=wa, dx=dx, dy=dy, t=t)


# def measure_one_humidity_SAXS(  t0,  ks, wa=45,  dx=0, dy=0 ,  t=0.5   ):
def measure_one_humidity_SAXS(t0, ks, wa=25, dx=0, dy=0, t=0.5):
    _measure_one(t0=t0, ks=ks, dets=[pil1M], waxs_angle=wa, dx=dx, dy=dy, t=t)
    RE(bps.mvr(SAXS.y, 30 * 0.172))
    _measure_one(t0=t0, ks=ks, dets=[pil1M], waxs_angle=wa, dx=dx, dy=dy, t=t)
    RE(bps.mvr(SAXS.y, -30 * 0.172))


def _measure_one(t0, ks, dets, waxs_angle, dx=0, dy=0, t=0.5):
    for k in ks:
        mov_sam(k)
        sample = RE.md["sample"]
        movx(dx)
        movy(dy)
        tcur = time.time()
        name_fmt = "{sample}_x{x_pos:05.2f}_y{y_pos:05.2f}_z{z_pos:05.2f}_t{tx}s_h{h}_det{saxs_y}_{saxs_z}_waxs{waxs_angle:05.2f}_expt{expt}s_sid{scan_id:08d}"
        sample_name = name_fmt.format(
            sample=sample,
            x_pos=stage.x.position,
            y_pos=stage.y.position,
            z_pos=stage.z.position,
            tx=np.round((tcur - t0), 1),
            h=np.round(readHumidity(temperature=25, voltage_supply=5, verbosity=1), 2),
            saxs_y=np.round(pil1m_pos.y.position, 2),
            saxs_z=np.round(pil1m_pos.z.position, 2),
            waxs_angle=waxs_angle,
            expt=t,
            scan_id=RE.md["scan_id"],
        )
        det_exposure_time(t, t)
        sample_id(user_name=user_name, sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")
        print("Collect data here....")
        RE(bp.count(dets, num=1))


def test_waxs_move_time():
    t0 = time.time()
    move_waxs(45)
    print("It takes %.2f min to move waxs from 0 to 45." % ((time.time() - t0) / 60))


def measure_saxs(t=1, att="None", dy=0, user_name="YM", sample=None):
    if sample is None:
        sample = RE.md["sample"]
    dets = [pil1M]
    # att_in( att )
    if dy:
        yield from bps.mvr(stage.y, dy)
    name_fmt = (
        "{sample}_x{x_pos}_y{y_pos}_det{saxs_z}m_expt{expt}s_att{att}_sid{scan_id:08d}"
    )
    sample_name = name_fmt.format(
        sample=sample,
        x_pos=np.round(stage.x.position, 2),
        y_pos=np.round(stage.y.position, 2),
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


def measure_waxs(t=1, waxs_angle=0, att="None", dy=0, user_name="YM", sample=None):
    if sample is None:
        sample = RE.md["sample"]
    yield from bps.mv(waxs, waxs_angle)
    dets = [pil900KW, pil300KW]
    # att_in( att )
    if dy:
        yield from bps.mvr(stage.y, dy)
    name_fmt = "{sample}_x{x_pos:05.2f}_y{y_pos:05.2f}_z{z_pos:05.2f}_waxs{waxs_angle:05.2f}_expt{expt}s_sid{scan_id:08d}"
    sample_name = name_fmt.format(
        sample=sample,
        x_pos=stage.x.position,
        y_pos=stage.y.position,
        z_pos=stage.z.position,
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


def measure_pindiol_current():
    fs.open()
    yield from bps.sleep(0.3)
    pd_curr = pdcurrent1.value
    fs.close()
    print("--------- Current pd_curr {}\n".format(pd_curr))
    return pd_curr


def measure_wsaxs(t=1, waxs_angle=20, att="None", dy=0, user_name="XZ", sample=None):
    if sample is None:
        sample = RE.md["sample"]
    yield from bps.mv(waxs, waxs_angle)
    dets = [pil900KW, pil300KW, pil1M]
    # att_in( att )
    if dy:
        yield from bps.mvr(stage.y, dy)
    name_fmt = "{sample}_x{x_pos:05.2f}_y{y_pos:05.2f}_z{z_pos:05.2f}_det{saxs_z}_waxs{waxs_angle:05.2f}_expt{expt}s_sid{scan_id:08d}"
    sample_name = name_fmt.format(
        sample=sample,
        x_pos=stage.x.position,
        y_pos=stage.y.position,
        z_pos=stage.z.position,
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


def measure_waxs_multi_angles(
    t=1.0,
    att="None",
    dy=0,
    user_name="YM",
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
            yield from bps.mvr(stage.y, dy)
        name_fmt = "{sample}_x{x_pos:05.2f}_y{y_pos:05.2f}_z{z_pos:05.2f}_waxs{waxs_angle:05.2f}_expt{expt}s_sid{scan_id:08d}"
        sample_name = name_fmt.format(
            sample=sample,
            x_pos=stage.x.position,
            y_pos=stage.y.position,
            z_pos=stage.z.position,
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


##################################################
############ Some convinent functions#################
#########################################################


def movx(dx):
    RE(bps.mvr(stage.x, dx))


def movy(dy):
    RE(bps.mvr(stage.y, dy))


def get_posxy():
    return round(stage.x.user_readback.value, 2), round(stage.y.user_readback.value, 2)


def move_waxs(waxs_angle=8.0):
    RE(bps.mv(waxs, waxs_angle))


def move_waxs_off(waxs_angle=8.0):
    RE(bps.mv(waxs, waxs_angle))


def move_waxs_on(waxs_angle=0.0):
    RE(bps.mv(waxs, waxs_angle))


def mov_sam(pos):
    px, py = pxy_dict[pos]
    RE(bps.mv(stage.x, px))
    RE(bps.mv(stage.y, py))
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
    dets = [pil900KW]
    sample_id(user_name="test", sample_name="test")
    det_exposure_time(t)
    yield from (bp.count(dets, num=1))


def snap_saxs(t=0.1):
    dets = [pil1M]
    sample_id(user_name="test", sample_name="test")
    det_exposure_time(t)
    yield from (bp.count(dets, num=1))

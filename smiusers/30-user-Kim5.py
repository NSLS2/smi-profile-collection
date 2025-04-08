# Remote access:
# n2sn_list_users
# n2sn_add_user --login yuzhang guacctrl
# n2sn_add_user --login yuzhang guacview

#  https://www.nsls2.bnl.gov/docs/remote/N2SNUserTools.html


# /nsls2/xf12id2/data/images/users/2022_1/308251_Nam


# For 1M
# det2, setthreshold energy 16100 autog 10500

# For 900KW
# camonly
# det3,  setthreshold energy 16100 autog 11000


##Collect data:

# SMI: 2022/3/3 Morning around 11:10 AM
# SAF: 308071   Standard        Beamline 12-ID   proposal:  308251
# create proposal: proposal_id( '2022_1', '308251_Nam' ) #create the proposal id and folder


# Data is saved in
# /nsls2/xf12id2/data/images/users/2022_1/308251_Nam

# Load Samples
# Check locations -X
# pump down,  Auto Evacuate
# Open valves

##Old one
#  go to the second window under,  det@xf12id2-det3:~> camonly
# change the energy threshold:  setthreshold energy 16100 autog 11000
## New one
# ssh -X det@xf12id2-det3 (pwd: Pilatus2)
# ./start_camserver
# setthreshold energy 16100 autog 11000


# align the gisaxs beam stop
# then save it:  beamstop_save()

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


# Y: 4000, Z: 2500
# Energy: 16.1 keV, 0.77009 A
# when finish the one batch, before bleed to air,
# shut down the camserver of 900 kw first
# go the camonly, exit (twice)
# the Auto Bleed to Air

# make the height pizo.y = 4000, Z= 2500
# manually measure sample 1 and 2

# Then run macro for all 19 samples
#     angle_arc = np.array([0.05, 0.08, 0.10, 0.15, 0.2, 0.3 ]) # incident angles
#     waxs_angle_array = np.array( [ 7, 27, 47 ] ) ,


##############
# Acidentally close the bluesky command, has to restart it, by typing bsui
# have to run the  %run -i /home/xf12id/.ipython/profile_collection/startup/99-utils.py
# then run this macro, works!!!


#  RE( shopen() )  # to open the beam and feedback
#  RE( shclose())

## Google doc
#


# # ## First RUN, 18 samples,  y = 1000, Z= 2300  @~12:00 pm, 2:00 finished  # hexY=6
# #np.array(['2022C1_S%s'%i for i in range(1,19)])
# sample_list = ['2022C1_S1', '2022C1_S2', '2022C1_S3', '2022C1_S4', '2022C1_S5',
#        '2022C1_S6', '2022C1_S7', '2022C1_S8', '2022C1_S9', '2022C1_S10',
#        '2022C1_S11', '2022C1_S12', '2022C1_S13', '2022C1_S14',
#        '2022C1_S15', '2022C1_S16', '2022C1_S17', '2022C1_S18']
# pos = np.array([2.7,8.5,13.5,19.1,25.3,30.3,36.7,42.2,48.6,55.9,63.4,70.7,77.3,82.2,88,93.3,98.3,104.5]) - 2.7
# x_list =   -50300 + pos * 1000
# RE(run_giwaxs_Kim())


# ## Second RUN, 17 samples,  y = 1000, Z= 2300  @about 2:00 pm start vent, mount samples, then do vacuum,
# 2:20 pm start measure
# np.array(['2022C1_S%s'%i for i in range(19,36)])
sample_list = [
    "2022C1_S19",
    "2022C1_S20",
    "2022C1_S21",
    "2022C1_S22",
    "2022C1_S23",
    "2022C1_S24",
    "2022C1_S25",
    "2022C1_S26",
    "2022C1_S27",
    "2022C1_S28",
    "2022C1_S29",
    "2022C1_S30",
    "2022C1_S31",
    "2022C1_S32",
    "2022C1_S33",
    "2022C1_S34",
    "2022C1_S35",
]

pos = np.array(
    [
        2.5,
        9.3,
        14,
        19.9,
        26.8,
        32.4,
        36.6,
        41.4,
        46.9,
        52,
        56.7,
        62.1,
        66.8,
        73.8,
        83.4,
        93.85,
        101.5,
    ]
)
x_list = -50300 + (pos - pos[0]) * 1000


# ## Third RUN, 17 samples,  y = 1000, Z= 2300  @about 2:00 pm start vent, mount samples, then do vacuum,
# 6:00 pm start measure
# np.array(['2022C1_S%s'%i for i in range(36,53)])
sample_list = [
    "2022C1_S36",
    "2022C1_S37",
    "2022C1_S38",
    "2022C1_S39",
    "2022C1_S40",
    "2022C1_S41",
    "2022C1_S42",
    "2022C1_S43",
    "2022C1_S44",
    "2022C1_S45",
    "2022C1_S46",
    "2022C1_S47",
    "2022C1_S48",
    "2022C1_S49",
    "2022C1_S50",
    "2022C1_S51",
    "2022C1_S52",
]

pos = np.array(
    [
        3.7,
        9.5,
        16.6,
        22.5,
        27.8,
        34.7,
        40.5,
        46.6,
        52.3,
        59.1,
        66.6,
        73.8,
        79.9,
        86.4,
        92.5,
        99.5,
        105.4,
    ]
)
x_list = -49400 + (pos - pos[0]) * 1000


# ## fourth RUN, 7 samples,  y = 1000, Z= 2300  @about 2:00 pm start vent, mount samples, then do vacuum,
# 6:00 pm start measure
# np.array(['2022C1_S%s'%i for i in range(53,61)])

# sample_list =  ['2022C1_S53', '2022C1_S54', '2022C1_S55', '2022C1_S56',
#        '2022C1_S57', '2022C1_S58', '2022C1_S59', '2022C1_S60']
# #pos = np.array( [2.7,9.1,16.7,23.8,30.5,37.2,44.4,50.5] )
# #x_list =   -49400 + (pos-pos[0]) * 1000
# x_list =   [ -49900,  -43900,  -37300,  -31800,   -25800, -20800,  -16300,  -11300 ]


## For RUN 5, Gao's Sample
sample_list = [
    "2022C1_1_2",
    "2022C1_1_3",
    "2022C1_1_4",
    "2022C1_1_5",
    "2022C1_1_1",
][2:]
x_list = [6400, 17700, 31200, 42200, 49200][2:]
sample_list = ["2022C1_1_8"]
x_list = [-3300]


# create proposal: proposal_id( '2022_1', '308251_Kim' ) #create the proposal id and folder
# the username is wrong, should be Kim, not Gao

### 3/7 Monday, test in air and in vacuum, using large beam
# ##   y = 1000, Z= 2300  @about 4:300 pm start vent, mount samples, then do vacuum,
## For RUN 6,  Kim's 44-47 samples
## change beam stop from pindiode to regular beamstop
# RE(pil1m_bs_pd.mv_out())
#
sample_list = [
    "2022C1_S44_LargeBeam_Vacuum",
    "2022C1_S45_LargeBeam_Vacuum",
    "2022C1_S46_LargeBeam_Vacuum",
    "2022C1_S47_LargeBeam_Vacuum",
]
x_list = [-48100, -39900, -31900, -24400]
# beamstop_save()
# beam center is: [462, 559 ]


### 3/7 Monday, test in air and in vacuum, using large beam
# ##   y = 1000, Z= 2300   hex-y =6
## For RUN 6,  Kim's 44-47 samples
sample_list = [
    "2022C1_S44_LargeBeam_Air",
    "2022C1_S45_LargeBeam_Air",
    "2022C1_S46_LargeBeam_Air",
    "2022C1_S47_LargeBeam_Air",
]
x_list = [-48100, -39900, -31900, -24400]
# beamstop_save()
# beam center is: [462, 559 ]


def mov_sam(i):
    px = x_list[i]
    RE(bps.mv(piezo.x, px))
    print("Move to pos=%s for sample:%s..." % (i + 1, sample_list[i]))


def check_sample_loc(sleep=5):
    ks = sample_list
    i = 0
    for k in ks:
        mov_sam(i)
        time.sleep(sleep)
        i += 1


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


def mov_sam_dict(pos):
    px, py = pxy_dict[pos]
    RE(bps.mv(piezo.x, px))
    RE(bps.mv(piezo.y, py))
    sample = sample_dict[pos]
    print("Move to pos=%s for sample:%s..." % (pos, sample))
    RE.md["sample"] = sample


# Align GiSAXS sample
import numpy as np

username = "Kim"
# username = 'Gao'

# mov_sam( 0 )
def vertical_scan(t=10):
    ## for sample   '2022C1_1_8'
    # hex Y, 4.45
    # scan pz from -1000 to 3000
    # plan to do more x position
    sample_name = sample_list[0]  #'2022C1_1_8'
    ys = np.arange(-1000, 4500, 100)
    waxs_angle_array = np.array(
        [7, 27, 47]
    )  # 4*3.14/(12.39842/16.1)*np.sin((7*6.5+3.5)*3.14/360) = 6.760 A-1
    max_waxs_angle = np.max(waxs_angle_array)
    det_exposure_time(t, t)

    for waxs_angle in waxs_angle_array:  # loop through waxs angles
        yield from bps.mv(waxs, waxs_angle)
        if waxs_angle == max_waxs_angle:
            dets = [pil900KW, pil1M]  # waxs, maxs, saxs = [pil300KW, rayonix, pil1M]
            print("Meausre both saxs and waxs here for w-angle=%s" % waxs_angle)
        else:
            dets = [pil900KW, pil300KW]
        for (i, yi) in enumerate(ys):
            print(i, yi)
            yield from bps.mv(piezo.y, yi)
            name_fmt = (
                "{sample}_waxsP{waxs_angle:05.2f}_y{y:05.2f}_expt{t}s_sid{scan_id:08d}"
            )
            sample_nameX = name_fmt.format(
                sample=sample_name,
                waxs_angle=waxs_angle,
                y=yi,
                t=t,
                scan_id=RE.md["scan_id"],
            )
            sample_id(user_name=username, sample_name=sample_nameX)
            print("The sample name is: %s." % sample_nameX)
            print(dets)
            yield from bp.count(dets, num=1)
    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.1, 0.1)


def manually_measure_one_sample(i, t=1, username=username):
    mov_sam(i)
    sample_name = sample_list[i]

    # sample_name = 'test'
    sample_id(user_name=username, sample_name=sample_name)
    print(f"\n\t=== Sample: {sample_name} ===\n")

    # RE( alignement_gisaxs(0.1) ) #run alignment routine

    angle_arc = 0.15  # 0.05 #0.3 #0.25 #0.2 #0.15 #0.1 #0.08 #0.02 #0.05
    waxs_angle = 47  # 27 #7

    x_meas = x_list[i]
    th_meas = (
        angle_arc + piezo.th.position
    )  # np.array([0.10 + piezo.th.position, 0.20 + piezo.th.position])
    th_real = angle_arc
    det_exposure_time(t, t)
    RE(bps.mv(waxs, waxs_angle))
    dets = [pil900KW, pil300KW]
    RE(bps.mv(piezo.th, th_meas))

    name_fmt = "{sample}_{th:5.4f}deg_waxsP{waxs_angle:05.2f}_x{x:05.2f}_expt{t}s_sid{scan_id:08d}"
    sample_nameX = name_fmt.format(
        sample=sample_name,
        th=th_real,
        waxs_angle=waxs_angle,
        x=x_meas,
        t=t,
        scan_id=RE.md["scan_id"],
    )
    sample_id(user_name=username, sample_name=sample_nameX)
    print("The sample name is: %s." % sample_nameX)
    RE(bp.count(dets, num=1))
    sample_id(user_name="test", sample_name="test")


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


def run_giwaxs_Kim(t=1, username=username):
    # define names of samples on sample bar
    assert len(x_list) == len(sample_list), f"Sample name/position list is borked"
    angle_arc = np.array([0.05, 0.08, 0.10, 0.15, 0.2, 0.3])  # incident angles
    waxs_angle_array = np.array(
        [7, 27, 47]
    )  # 4*3.14/(12.39842/16.1)*np.sin((7*6.5+3.5)*3.14/360) = 6.760 A-1
    # dets = [pil300KW, pil1M] # waxs, maxs, saxs = [pil300KW, rayonix, pil1M]
    max_waxs_angle = np.max(waxs_angle_array)
    x_shift_array = np.linspace(-500, 500, 3)  # measure at a few x positions
    inverse_angle = False
    cts = 0
    for ii, (x, sample) in enumerate(
        zip(x_list, sample_list)
    ):  # loop over samples on bar
        yield from bps.mv(piezo.x, x)  # move to next sample

        # yield from  bps.mv(piezo.y, 4000  ) #move y to 4000

        yield from alignement_gisaxs(0.1)  # run alignment routine
        th_meas = angle_arc + piezo.th.position
        th_real = angle_arc
        det_exposure_time(t, t)
        x_pos_array = x + x_shift_array
        if inverse_angle:
            Waxs_angle_array = waxs_angle_array[::-1]
        else:
            Waxs_angle_array = waxs_angle_array
        for waxs_angle in Waxs_angle_array:  # loop through waxs angles
            yield from bps.mv(waxs, waxs_angle)
            if waxs_angle == max_waxs_angle:
                dets = [
                    pil900KW,
                    pil300KW,
                    pil1M,
                ]  # waxs, maxs, saxs = [pil300KW, rayonix, pil1M]
                print("Meausre both saxs and waxs here for w-angle=%s" % waxs_angle)
            else:
                dets = [pil900KW, pil300KW]

            for x_meas in x_pos_array:  # measure at a few x positions
                yield from bps.mv(piezo.x, x_meas)
                for i, th in enumerate(th_meas):  # loop over incident angles
                    yield from bps.mv(piezo.th, th)
                    if inverse_angle:
                        name_fmt = "{sample}_{th:5.4f}deg_waxsN{waxs_angle:05.2f}_x{x:05.2f}_expt{t}s_sid{scan_id:08d}"
                    else:
                        name_fmt = "{sample}_{th:5.4f}deg_waxsP{waxs_angle:05.2f}_x{x:05.2f}_expt{t}s_sid{scan_id:08d}"
                    sample_name = name_fmt.format(
                        sample=sample,
                        th=th_real[i],
                        waxs_angle=waxs_angle,
                        x=x_meas,
                        t=t,
                        scan_id=RE.md["scan_id"],
                    )
                    sample_id(user_name=username, sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    # yield from bp.scan(dets, energy, e, e, 1)
                    # yield from bp.scan(dets, waxs, *waxs_arc)
                    print(dets)
                    yield from bp.count(dets, num=1)
                    # print( 'HERE#############')
        inverse_angle = not inverse_angle
        cts += 1
    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5)


####
# proposal_id('2020_2', '304841_Kim')
# RE(shopen())
#
# Modify file (sample name, x pos), Save file
#
# Check sample stage (SmarAct Y) is around 7000
#
# %run -i /home/xf12id/.ipython/profile_collection/startup/users/30-user-Kim3.py
# RE(run_giwaxs_Kim(t=1))
# if do ctrl+C: RE.abort()
#
# RE(shclose())
# Vent: "auto bleed to air", open WAXS soft vent at lower left
# Pump: 'Auto evacuate", when in vac, open valves before and after WAXS chamber

# Note
#
# %run -i /home/xf12id/.ipython/profile_collection/startup/36-Guillaume-beam.py
#
# Data/result: /GPFS/xf12id1/data/images/users/2019_2/304848_Kim/


########## Note for 2021-June
# Total 74 samples, 0~6.5A-1 (~9min/sample), except Sample#20-43: 0-8.7A-1 (~12min/sample)
#
# 11am - 1:20pm Bar1, 16 samples, piezo_z ~0
# 1:45pm - 4:15pm, Bar2, 15 samples, piezo_z ~0.4
#
# If beam drifted:
# (1) feedback off
# (2) CMS pitch 1.00058 +/- 0.0002 tweak to get BPM2 sum to be 4.8
# (3) feedback on
#
# piezo_x range: -57400 to 60500
#
# 5pm - 8:40pm, Bar3, 21 samples
# 9:50pm -  10:15pm, Bar5, 3 samples
# 10:45pm - 1:50am, Bar4, 19 samples, piezo_z ~1.75
#
# Data: /nsls2/xf12id2/data/images/users/2021_2/308651_Kim

# Remote access:
# n2sn_list_users
# n2sn_add_user --login yuzhang guacctrl
# n2sn_add_user --login yuzhang guacview

#  https://www.nsls2.bnl.gov/docs/remote/N2SNUserTools.html


# For 1M
# det2, setthreshold energy 16100 autog 10500

# For 900KW
# camonly
# det3,  setthreshold energy 16100 autog 11000


##Collect data:

# SMI: 2021/9/21 Morning around 12:00 AM
# SAF: 308070   Standard        Beamline 12-ID   proposal:  308251
# create proposal: proposal_id( '2021_3', '308251_Kim' ) #create the proposal id and folder
# Load Samples
# Check locations -X
# pump down,  Auto Evacuate
# Open valves
#  go to the second window under,  det@xf12id2-det3:~> camonly
# change the energy threshold:  setthreshold energy 16100 autog 11000
# align the gisaxs beam stop
# then save it:  beamstop_save()
# for 900kw, move to 7 degree, beam location: [218, 109 ]
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

# ## First RUN, 19 samples,  y = 4000, Z= 2500
# x_list = [      50700,  44200,  38700, 32700,  27200,  21200,     15700,  10200,
#                 4700,    -800,  -6300,  -11800, -16300, -21800, -27300,  -32800,
#                 -38300, -43800,  -49300     ]
# sample_list = [ '2021C3_B18', '2021C3_A6',  '2021C2_S2',  '2021C3_S3', '2021C3_S4', '2021C3_S5',  '2021C3_S6',  '2021C3_S7', '2021C3_S8',
#                    '2021C3_S9',  '2021C3_S10', '2021C3_S11', '2021C3_S12', '2021C3_S13', '2021C3_S14', '2021C3_S15', '2021C3_S16',
#                    '2021C3S17',  '2021C3_S18',       ]


# ## Second RUN, 19 samples,  y = 4000, Z= 2500
# x_list = np.array( [      52200,  47200,  41700, 36700,   31200,  25200,  19700,  15200,
#          9700,   4200, -1300,  -5800, -11300, -16800, -22300, -27800,
#        -33300, -38800, -44300 , -49800 ] )
# sample_list = [ '2021C3_S19',  '2021C3_S20', '2021C3_S21', '2021C3_S22', '2021C3_S23', '2021C3_S24', '2021C3_S25', '2021C3_S26',
#                    '2021C3S27',  '2021C3_S28', '2021C3_S29','2021C3_S30','2021C3_S31',  '2021C3_S32', '2021C3_S33', '2021C3_S34',
#                    '2021C3_S35', '2021C3_S36',   '2021C3S37',  '2021C3_S38' ]

# x_list = np.array( [      -49000 ] )
# sample_list = [    '2021C3_S38' ]


## Third RUN, 19 samples,  y = 4000, Z= 4900

# x_list = np.array( [      52000,  47200,  41700, 35700,   29700,  23200,   16700, 10700,
#          4700,   -800,  -7300, -12800, -18300,  -23800, -28800, -34300, ] )
#         # -38800, -44300 , -49800 ] )
# sample_list = [ '2021C3_S39',  '2021C3_S40', '2021C3_S41', '2021C3_S42', '2021C3_S43', '2021C3_S44', '2021C3_S45', '2021C3_S46',
#                    '2021C3_S47',  '2021C3_S48', '2021C3_S49','2021C3_S50','2021C3_S51',  '2021C3_S52', '2021C3_S53', '2021C3_S54',]
#                   # '2021C3_S55', '2021C3_S56',   '2021C3S57',   ]

x_list = np.array([-44300, -49800])
sample_list = [
    "2021C3_S56",
    "2021C3S57",
]


## Forth RUN, 6 samples,  y = 4000, Z= 0

x_list = np.array([49500, 42500, 34000, 27000, 19500, 12000])
sample_list = [
    "2021C3_S58",
    "2021C3_S59",
    "2021C3_S60",
    "2021C3_S61",
    "2021C3_S63",
    "2021C3_S55",
]


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


def manually_measure_one_sample(i, t=1, username="Kim"):
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


def run_giwaxs_Kim(t=1, username="Kim"):
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

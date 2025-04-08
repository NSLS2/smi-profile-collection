##Collect data:

# SMI: 2021/1/30 Morning around 8:30 AM

# SAF: 306811   Standard        Beamline 12-ID   proposal:  304841


# create proposal: proposal_id( '2021-1', '304841_Kim' ) #create the proposal id and folder
# Make the pizo-Y = 7000
# Make the pizo-Z = 1400
# manually find the sample position and create the sample_list and x_list
# Problem there is no beam on the bpm2
# check FS, insert FS:1 and find the beam is off, manually change the pictch to put the beam back to the ROI3
# Now, there is some beam Sum-X, 1.04, Y 1.05, still Low
# Misha called in and told me that NEVER tune the mirror, except a little bit on the VDM pithch angle
# Misha tweek little bit about the pitch (from 1.0053 to 1.0217 ) and roll ( from 0.1358 to 0.1344 )
# The beam current on BPM2 is about 3 (on both x and y) with electron current as 300 mA
# The plot of PIDx and y should be in the middle of the chart (x in a range of -4095 to 4095) (y in a range from -8192 to 8192)
# Misha also change the beam stop,
# Previouly, beamstop is PIN diol (SAXS 2mm), then change to a rod beamstop (SAXS 3mm )
# The position for rod beamstop is: SAXS2mm, [X: 0, Y: 8.47 ]; SAXS3mm, [X: 1.5, Paddle, 288.99, Y: -13 ]


# Beam dump at 10:30 am
# Beam comes back at 1:30 pm
# the beam stop position on the WAXS detector: X -20.92 Y:0
# The beam center on WAXS: [ 88, 96  ]
# The beam center on SAXS:  [459, 567 ]
# Energy: 16.1 keV, 0.77009 A

###############Something Wrong with the sample holder (the post is too low)
## Spend some time to figure out the proper post !!!!
###########
# Re-write the macro and run the long data acq, loop sample, for each sample, then scan the WAXS , three x-pos, and inc-angles
#

## One sample would take:  3 hours

## Sunday morning, find the beam was drafted during the last night scan, manually tweek the DCM pitch and put the beam back
## Run run the samples from C28-D37

##############
# Acidentally close the bluesky command, has to restart it, by typing bsui
# have to run the  %run -i /home/xf12id/.ipython/profile_collection/startup/99-utils.py
# then run this macro, works!!!


#  RE( shopen() )  # to open the beam and feedback
#  RE( shclose())


## Google doc
#  https://docs.google.com/document/d/14QUZpYrB04Zr_XPwjgch7nP1vbYgaS42mUUOBEv5Nx8/edit

## First RUN, 19 samples, only run one sample, Starting ~ 17:00 PM
x_list = [
    52000,
    46400,
    41100,
    35600,
    29600,
    23500,
    17500,
    11500,
    6500,
    500,
    -5500,
    -11500,
    -17500,
    -23500,
    -29500,
    -35500,
    -40500,
    -46000,
    -52000,
]
sample_list = [
    "2021C1_A1",
    "2021C1_A2",
    "2021C1_A3",
    "2021C1_A4",
    "2021C1_A5",
    "2021C1_A6",
    "2021C1_A7",
    "2021C1_A8",
    "2021C1_B9",
    "2021C1_B10",
    "2021C1_B11",
    "2021C1_B12",
    "2021C1_B13",
    "2021C1_B14",
    "2021C1_B15",
    "2021C1_B16",
    "2021C1B17",
    "2021C1_B18",
    "2021C1_B19",
]
## Second Run, run 18 samples (remained on the same bar as the first run)

x_list = [
    46400,
    41100,
    35600,
    29600,
    23500,
    17500,
    11500,
    6500,
    500,
    -5500,
    -11500,
    -17500,
    -23500,
    -29500,
    -35500,
    -40500,
    -46000,
    -52000,
]


sample_list = [
    "2021C1_A2",
    "2021C1_A3",
    "2021C1_A4",
    "2021C1_A5",
    "2021C1_A6",
    "2021C1_A7",
    "2021C1_A8",
    "2021C1_B9",
    "2021C1_B10",
    "2021C1_B11",
    "2021C1_B12",
    "2021C1_B13",
    "2021C1_B14",
    "2021C1_B15",
    "2021C1_B16",
    "2021C1B17",
    "2021C1_B18",
    "2021C1_B19",
]


# Third Run, 18 samples, Start from  ~ 9:40 PM
sample_list = [
    "2021C1_B20",
    "2021C1_B21",
    "2021C1_B22",
    "2021C1_B23",
    "2021C1_B24",
    "2021C1_C25",
    "2021C1_C26",
    "2021C1_C27",
    "2021C1_C28",
    "2021C1_C29",
    "2021C1_C30",
    "2021C1_C31",
    "2021C1_C32",
    "2021C1_C33",
    "2021C1_D34",
    "2021C1_D35",
    "2021C1_D36",
    "2021C1_D37",
]

x_list = [
    -49500,
    -43500,
    -37500,
    -31500,
    -25500,
    -19500,
    -14500,
    -9000,
    -3500,
    2500,
    8500,
    15000,
    22500,
    28500,
    34500,
    41500,
    47500,
    52500,
]


# Fourth Run, the beam drift after C27 (seems like all good up to C27 (includes C37)), Run C37 to D 37
sample_list = [
    "2021C1_C28",
    "2021C1_C29",
    "2021C1_C30",
    "2021C1_C31",
    "2021C1_C32",
    "2021C1_C33",
    "2021C1_D34",
    "2021C1_D35",
    "2021C1_D36",
    "2021C1_D37",
]

x_list = [-3500, 2500, 8500, 15000, 22500, 28500, 34500, 41500, 47500, 52500]


# Fifth Run, 18 samples, Start from  ~  Sunday 12:05pm to 2:44 pm
sample_list = [
    "2021C1_D38",
    "2021C1_D39",
    "2021C1_D40",
    "2021C1_D41",
    "2021C1_E42",
    "2021C1_E43",
    "2021C1_E44",
    "2021C1_E45",
    "2021C1_E46",
    "2021C1_E47",
    "2021C1_E48",
    "2021C1_E49",
    "2021C1_F50",
    "2021C1_F51",
    "2021C1_F52",
    "2021C1_F53",
    "2021C1_F54",
    "2021C1_F55",
]

x_list = [
    51500,
    45000,
    38000,
    31500,
    25500,
    19500,
    12500,
    6500,
    1500,
    -4500,
    -11500,
    -16500,
    -22500,
    -27500,
    -33500,
    -39500,
    -44500,
    -50500,
]


# Six 8 samples, Start from  ~ the first four from Anibal, start from Sun, 3:40 pm -
sample_list = [
    "2021C1_Dennis_S1",
    "2021C1_Dennis_S2",
    "2021C1_Dennis_S3",
    "2021C1_Dennis_S4",
    "2021C1_F56",
    "2021C1_F57",
    "2021C1_F58",
    "2021C1_F59",
]

x_list = [-49500, -38500, -29500, -24000, -18500, -13000, -6500, 0]


# Seventh Run,  11 samples,
sample_list = [
    "2021C1_F60",
    "2021C1_F61",
    "2021C1_F62",
    "2021C1_F63",
    "2021C1_F64",
    "2021C1_F65",
    "2021C1_F66",
    "2021C1_F67",
    "2021C1_F68",
    "2021C1_F69",
    "2021C1_F70",
]

x_list = [51500, 45000, 38700, 31500, 24500, 17400, 10400, 3200, -3900, -10600, -17100]


################## 2021-June ##################
# Bar 1
sample_list = [
    "Bar1_Sam01",
    "Bar1_Sam02",
    "Bar1_Sam03",
    "Bar1_Sam04",
    "Bar1_Sam05",
    "Bar1_Sam06",
    "Bar1_Sam07",
    "Bar1_Sam08",
    "Bar1_Sam09",
    "Bar1_Sam10",
    "Bar1_Sam11",
    "Bar1_Sam12",
    "Bar1_Sam13",
    "Bar1_Sam14",
    "Bar1_Sam15",
    "Bar1_Sam16",
]

x_list = [
    -47500,
    -41500,
    -35500,
    -29500,
    -23000,
    -18000,
    -12000,
    -6000,
    1000,
    8000,
    16000,
    24000,
    31000,
    37000,
    44000,
    50000,
]

# Bar 2
sample_list = [
    "Bar2_Sam17",
    "Bar2_Sam18",
    "Bar2_Sam19",
    "Bar2_Sam20",
    "Bar2_Sam21",
    "Bar2_Sam22",
    "Bar2_Sam23",
    "Bar2_Sam24",
    "Bar2_Sam25",
    "Bar2_Sam26",
    "Bar2_Sam27",
    "Bar2_Sam28",
    "Bar2_Sam29",
    "Bar2_Sam30",
    "Bar2_Sam31",
]

x_list = [
    -48000,
    -41000,
    -35000,
    -27000,
    -19000,
    -12000,
    -5000,
    3000,
    10500,
    16500,
    22500,
    28000,
    35000,
    42000,
    49000,
]

# Bar 3
sample_list = [
    "Bar3_Sam33",
    "Bar3_Sam34",
    "Bar3_Sam35",
    "Bar3_Sam36",
    "Bar3_Sam37",
    "Bar3_Sam38",
    "Bar3_Sam39",
    "Bar3_Sam40",
    "Bar3_Sam41",
    "Bar3_Sam42",
    "Bar3_Sam43",
    "Bar3_Sam44",
    "Bar3_Sam45",
    "Bar3_Sam46",
    "Bar3_Sam47",
    "Bar3_Sam48",
    "Bar3_Sam49",
    "Bar3_Sam50",
    "Bar3_Sam51",
    "Bar3_Sam52",
    "Bar3_Sam32",
]

x_list = [
    -56000,
    -50000,
    -44000,
    -38000,
    -32000,
    -26000,
    -20000,
    -15000,
    -8000,
    -2000,
    3000,
    9000,
    14000,
    22000,
    28000,
    33500,
    37500,
    42500,
    48000,
    53500,
    59500,
]

# Bar 4
sample_list = [
    "Bar4_Sam53",
    "Bar4_Sam54",
    "Bar4_Sam55",
    "Bar4_Sam56",
    "Bar4_Sam57",
    "Bar4_Sam58",
    "Bar4_Sam59",
    "Bar4_Sam60",
    "Bar4_Sam61",
    "Bar4_Sam62",
    "Bar4_Sam63",
    "Bar4_Sam64",
    "Bar4_Sam65",
    "Bar4_Sam66",
    "Bar4_Sam67",
    "Bar4_Sam68",
    "Bar4_Sam69",
    "Bar4_Sam70",
    "Bar4_Sam71",
]

x_list = [
    59000,
    54000,
    48000,
    43000,
    36000,
    30000,
    24000,
    18000,
    11000,
    5000,
    -2000,
    -6000,
    -13000,
    -19000,
    -24000,
    -31000,
    -41000,
    -46000,
    -52000,
]

# Bar 5
# sample_list = [ 'Bar5_Sam72', 'Bar5_Sam73', 'Bar5_Sam74',
#                ]
# x_list = [  -8500, -2500, 4500
#       ]


def mov_sam(i):
    px = x_list[i]
    RE(bps.mv(piezo.x, px))
    print("Move to pos=%s for sample:%s..." % (i + 1, sample_list[i]))


def check_saxs_sample_loc(sleep=5):
    ks = sample_list
    i = 0
    for k in ks:
        mov_sam(i)
        time.sleep(sleep)
        i += 1


# Align GiSAXS sample
import numpy as np


def run_giwaxs_Kim(t=1, username="Kim"):

    # define names of samples on sample bar

    assert len(x_list) == len(sample_list), f"Sample name/position list is borked"

    # angle_arc = np.array([0.1, 0.15, 0.19]) # incident angles
    angle_arc = np.array([0.08, 0.10, 0.15])  # incident angles
    # waxs_angle_array = np.linspace(0, 84, 15)
    # waxs_angle_array = np.linspace(0, 52, 9)   # q=4*3.14/0.77*np.sin((max angle+3.5)/2*3.14159/180)
    # 52/6.5 +1 =8 --> 7.6 A-1 at 16.1 keV
    # waxs_angle_array = np.linspace(0, 65, 11) # 4*3.14/(12.39842/16.1)*np.sin((10*6.5+3.5)*3.14/360) = 9.175 A-1
    waxs_angle_array = np.linspace(
        0, 45.5, 8
    )  # 4*3.14/(12.39842/16.1)*np.sin((7*6.5+3.5)*3.14/360) = 6.760 A-1

    # dets = [pil300KW, pil1M] # waxs, maxs, saxs = [pil300KW, rayonix, pil1M]
    max_waxs_angle = np.max(waxs_angle_array)
    x_shift_array = np.linspace(-500, 500, 3)  # measure at a few x positions
    inverse_angle = False
    cts = 0
    for ii, (x, sample) in enumerate(
        zip(x_list, sample_list)
    ):  # loop over samples on bar

        # print("##### {}, {} #####".format(ii, sample))
        # if 1: #ii>=3:
        #    waxs_angle_array = np.linspace(0, 65, 11)
        # else:
        #    waxs_angle_array = np.linspace(0, 45.5, 8)
        # max_waxs_angle = np.max(  waxs_angle_array )
        # print("## max_waxs_angle {}".format(max_waxs_angle))

        # if cts > 3:
        #    username = 'Kim'
        # else:
        #    username = 'ABosc'

        yield from bps.mv(piezo.x, x)  # move to next sample

        yield from alignement_gisaxs(0.1)  # run alignment routine

        th_meas = (
            angle_arc + piezo.th.position
        )  # np.array([0.10 + piezo.th.position, 0.20 + piezo.th.position])
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
                    pil300KW,
                    pil1M,
                ]  # waxs, maxs, saxs = [pil300KW, rayonix, pil1M]
                print("Meausre both saxs and waxs here for w-angle=%s" % waxs_angle)
            else:
                dets = [pil300KW]

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

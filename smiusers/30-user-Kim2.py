# Align GiSAXS sample
import numpy as np


def run_giwaxs_Kim(t=1):

    # define names of samples on sample bar
    # sample_list = ['A15_HZO_4nm_450C','A16_HZO_6nm_450C','A17_HZO_4nm_500C','A18_HZO_6nm_500C','A19_HZO_4nm_600C','A20_HZO_6nm_600C','A21_HZO_4nm_300C','A22_HZO_6nm_300C','B23_HfZr11_10nm_400C','B24_HfZr37_10nm_400C','B25_HfZr13_10nm_400C','B26_HfZr14_10nm_400C']
    # sample_list =  ['B27_HfZr11_7nm_400C','B28_HfZr37_7nm_400C','B29_HfZr13_7nm_400C','B30_HfZr14_7nm_400C', 'B31_HfZr11_7nm_400C','B32_HfZr12_7nm_400C','B33_HfZr13_7nm_400C','B34_HfZr14_7nm_400C']
    # sample_list = ['C35_O3_10nm_400C', 'C36_H2O_10nm_400C', 'C37_D2O_10nm_400C', 'C38_H2O2_10nm_400C', 'C39_O3_7nm_400C', 'C40_H2O_7nm_400C', 'C41_D2O_7nm_400C']
    sample_list = [
        "C42_H2O2_7nm_400C",
        "D43_Hf_30s_400C",
        "D44_Hf_1min_400C",
        "D45_Hf_2min_400C",
        "D46_TiN_400C",
        "D47_Hf_30s_500C",
        "D48_Hf_1min_500C",
        "D49_Hf_2min_500C",
        "D50_TiN_500C",
        "D51_Hf_30s_550C",
        "D52_Hf_1min_550C",
        "D53_Hf_2min_550C",
        "D54_TiN_550C",
    ]

    # x_list = [-50000, -43000, -32000, -24000, -15000,      -7000, 1000, 9000, 19000, 29000,    42000,  49000]
    # x_list = [-47000, -36000, -22000, -9000, 4000,     20000, 32000, 47000]
    # x_list = [-45000, -32000, -14000, -1000, 16000,    31000, 45000]
    x_list = [
        -45000,
        -37000,
        -27000,
        -20000,
        -12000,
        -3000,
        4000,
        12000,
        20000,
        27000,
        35000,
        42000,
        52000,
    ]

    assert len(x_list) == len(sample_list), f"Sample name/position list is borked"

    # angle_arc = np.array([0.1, 0.15, 0.19]) # incident angles
    angle_arc = np.array([0.08, 0.10, 0.15])  # incident angles
    # waxs_angle_array = np.linspace(0, 84, 15)
    waxs_angle_array = np.linspace(
        0, 52, 9
    )  # q=4*3.14/0.77*np.sin((max angle+3.5)/2*3.14159/180)
    # if 12, 3: up to q=2.199
    # if 18, 4: up to q=3.04
    # if 24, 5: up to q=3.87
    # if 30, 6: up to q=4.70
    # 52/6.5 +1 =8
    dets = [pil300KW, pil1M]  # waxs, maxs, saxs = [pil300KW, rayonix, pil1M]

    x_shift_array = np.linspace(-500, 500, 3)  # measure at a few x positions

    for x, sample in zip(x_list, sample_list):  # loop over samples on bar

        yield from bps.mv(piezo.x, x)  # move to next sample
        yield from alignement_gisaxs(0.1)  # run alignment routine

        th_meas = (
            angle_arc + piezo.th.position
        )  # np.array([0.10 + piezo.th.position, 0.20 + piezo.th.position])
        th_real = angle_arc

        det_exposure_time(t, t)
        x_pos_array = x + x_shift_array

        for waxs_angle in waxs_angle_array:  # loop through waxs angles
            yield from bps.mv(waxs, waxs_angle)

            for x_meas in x_pos_array:  # measure at a few x positions
                yield from bps.mv(piezo.x, x_meas)

                for i, th in enumerate(th_meas):  # loop over incident angles
                    yield from bps.mv(piezo.th, th)

                    sample_name = (
                        "{sample}_{th:5.4f}deg_waxs{waxs_angle:05.2f}_x{x}_{t}s".format(
                            sample=sample,
                            th=th_real[i],
                            waxs_angle=waxs_angle,
                            x=x_meas,
                            t=t,
                        )
                    )
                    sample_id(user_name="Kim", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")

                    # yield from bp.scan(dets, energy, e, e, 1)
                    # yield from bp.scan(dets, waxs, *waxs_arc)
                    yield from bp.count(dets, num=1)

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
# %run -i /home/xf12id/.ipython/profile_collection/startup/users/30-user-Kim2.py
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

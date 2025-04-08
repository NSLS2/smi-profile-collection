# Align GiSAXS sample
import numpy as np


def run_giwaxs_Kim(t=1):

    # define names of samples on sample bar
    sample_list = [
        "7-1_wideangle_10nm_MIM",
        "7-2_wideangle_20nm_MIM",
        "7-3_wideangle_4nm_MIM",
        "7-4_wideangle_Hf0.75",
        "7-5_wideangle_Hf0.25",
        "7-6_wideangle_ZrO2",
    ]

    x_list = [-49800, -38700, -29200, -17800, -11000, -4200]

    assert len(x_list) == len(sample_list), f"Sample name/position list is borked"

    angle_arc = np.array([0.1, 0.15, 0.19])  # incident angles
    waxs_angle_array = np.linspace(
        0, 84, 15
    )  # q=4*3.14/0.77*np.sin((max angle+3.5)/2*3.14159/180)
    # if 12, 3: up to q=2.199
    # if 18, 4: up to q=3.04
    # if 24, 5: up to q=3.87
    # if 30, 6: up to q=4.70
    dets = [pil300KW, rayonix, pil1M]  # waxs, maxs, saxs = [pil300KW, rayonix, pil1M]

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

#
# Modify file (sample name, x pos), Save file
#
# Check sample stage (SmarAct Y) is around 5600, 6000
#
# %run -i /home/xf12id/.ipython/profile_collection/startup/users/30-user-Kim.py
# if do ctrl+C: RE.abort()
#
# Data/result: /GPFS/xf12id1/data/images/users/2019_2/304848_Kim/


# Note
#
# %run -i /home/xf12id/.ipython/profile_collection/startup/36-Guillaume-beam.py

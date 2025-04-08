# Align GiSAXS sample
import numpy as np


def run_giwaxs(t=1):  # 2020C1
    # define names of samples on sample bar

    sample_list = [
        "5_1_MeDPP_glassOTS_PhMe_none",
        "5_2_MeDPP_glassOTS_PhMe_60minVSADCM",
        "SC1_8_60minVSADCM",
        "SC1_8_PEDOTPSS",
    ]
    x_list = [47200.000, 37200.000, 23700.000, 15700.000]

    assert len(x_list) == len(sample_list), f"Sample name/position list is borked"

    angle_arc = np.array([0.08, 0.1, 0.15, 0.2])  # incident angles
    waxs_angle_array = np.linspace(
        0, 19.5, 4
    )  # (0, 18, 4)   # q=4*3.14/0.77*np.sin((max angle+3.5)/2*3.14159/180)
    # if 12, 3: up to q=2.199
    # if 18, 4: up to q=3.04
    dets = [pil300KW]  # waxs, maxs, saxs = [pil300KW, rayonix, pil1M]

    for x, sample in zip(x_list, sample_list):  # loop over samples on bar

        yield from bps.mv(piezo.x, x)  # move to next sample
        yield from bps.mv(piezo.th, 0)
        yield from alignement_gisaxs(0.1)  # run alignment routine

        yield from bps.mv(waxs, 4)
        try:
            yield from bps.mv(waxs, 0)
        except:
            print("ERROR with WAXS, trying again..")
            yield from bps.mv(waxs, 0)

        th_meas = (
            angle_arc + piezo.th.position
        )  # np.array([0.10 + piezo.th.position, 0.20 + piezo.th.position])
        th_real = angle_arc

        det_exposure_time(t, t)
        x_meas = x

        for waxs_angle in waxs_angle_array:  # loop through waxs angles
            yield from bps.mv(waxs, waxs_angle)

            for i, th in enumerate(th_meas):  # loop over incident angles
                yield from bps.mv(piezo.th, th)

                # if sample!='OTS':
                x_meas = x_meas - 50  # shift a bit in x

                yield from bps.mv(piezo.x, x_meas)

                sample_name = (
                    "{sample}_{th:5.4f}deg_waxs{waxs_angle:05.2f}_x{x}_{t}s".format(
                        sample=sample,
                        th=th_real[i],
                        waxs_angle=waxs_angle,
                        x=x_meas,
                        t=t,
                    )
                )
                sample_id(user_name="AB", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")

                # yield from bp.scan(dets, energy, e, e, 1)
                # yield from bp.scan(dets, waxs, *waxs_arc)
                yield from bp.count(dets, num=1)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5)


def run_gisaxsAngle_AB2(t=1):  # 2020C1
    # define names of samples on sample bar

    sample_list = [
        "1_1_MeDPP_glass_thermal_none",
        "1_2_MeDPP_glass_thermal_0.5minVSADCM",
        "1_3_MeDPP_glass_thermal_1minVSADCM",
        "1_4_MeDPP_glass_thermal_5minVSADCM",
        "1_5_MeDPP_glass_thermal_15minVSADCM",
        "1_6_MeDPP_glass_thermal_60minVSADCM",
        "1_7_MeDPP_glass_thermal_240minVSADCM",
    ]
    x_list = [50000, 36800, 22800, 9800, -2500, -16500, -31000]

    # sample_list = ['2_1_MeDPP_glass_thermal_none', '2_2_MeDPP_SiO2_thermal_0.5minVSADCM', '2_3_MeDPP_SiO2_thermal_1minVSADCM', '2_4_MeDPP_SiO2_thermal_5minVSADCM', '2_5_MeDPP_SiO2_thermal_15minVSADCM', '2_6_MeDPP_SiO2_thermal_60minVSADCM', '2_7_MeDPP_SiO2_thermal_240minVSADCM','3_1_MeDPP_SiO2_PhMe_none','3_2_MeDPP_SiO2_PhMe_60minVSADCM','3_3_MeDPP_SiO2_DCM_none','3_4_MeDPP_SiO2_DCM_60minVSADCM','4_1_MeDPP_SiO2_loosepowder_none','4_2_MeDPP_SiO2_loosepowder_shear','4_3_MeDPP_SiO2_compressedpowder_none','4_4_MeDPP_SiO2_compressedpowder_shear']
    # x_list = [-51400,-44400.000, -37400.000, -31400.000,-24400.000, -17400.000,-10400.000,-4400.000,2600.000,8600.000,15600.000,23600.000,29600.000,36600.000,46600.000]

    # sample_list = ['OTS',
    # sample_list = ['5_1_MeDPP_glassOTS_PhMe_none','5_2_MeDPP_glassOTS_PhMe_60minVSADCM','SC1_8_60minVSADCM','SC1_8_PEDOTPSS']
    # x_list = [50250,
    # x_list = [47200.000,37200.000,23700.000,15700.000]

    assert len(x_list) == len(sample_list), f"Sample name/position list is borked"

    angle_arc = np.array([0.08, 0.1, 0.15, 0.2])  # incident angles
    waxs_angle_array = np.linspace(
        0, 19.5, 4
    )  # (0, 18, 4)   # q=4*3.14/0.77*np.sin((max angle+3.5)/2*3.14159/180)
    # if 12, 3: up to q=2.199
    # if 18, 4: up to q=3.04
    dets = [pil300KW]  # waxs, maxs, saxs = [pil300KW, rayonix, pil1M]

    for x, sample in zip(x_list, sample_list):  # loop over samples on bar

        yield from bps.mv(piezo.x, x)  # move to next sample
        yield from bps.mv(piezo.th, 0)
        yield from alignement_gisaxs(0.1)  # run alignment routine

        yield from bps.mv(waxs, 4)
        try:
            yield from bps.mv(waxs, 0)
        except:
            print("ERROR with WAXS, trying again..")
            yield from bps.mv(waxs, 0)

        th_meas = (
            angle_arc + piezo.th.position
        )  # np.array([0.10 + piezo.th.position, 0.20 + piezo.th.position])
        th_real = angle_arc

        det_exposure_time(t, t)
        x_meas = x

        # for waxs_angle in waxs_angle_array: # loop through waxs angles
        for i, th in enumerate(th_meas):  # loop over incident angles
            yield from bps.mv(piezo.th, th)

            for jj in [0, 1, 2, 3]:
                if i == 0 and jj == 0:
                    x_meas = x_meas - 50  # shift a bit in x
                else:
                    x_meas = x_meas - 200  # shift a bit in x
                yield from bps.mv(piezo.x, x_meas)

                for waxs_angle in waxs_angle_array:
                    yield from bps.mv(waxs, waxs_angle)

                    sample_name = (
                        "{sample}_{th:5.4f}deg_x{x}_waxs{waxs_angle:05.2f}_{t}s".format(
                            sample=sample,
                            th=th_real[i],
                            x=x_meas,
                            waxs_angle=waxs_angle,
                            t=t,
                        )
                    )
                    sample_id(user_name="AB2", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")

                    # yield from bp.scan(dets, energy, e, e, 1)
                    # yield from bp.scan(dets, waxs, *waxs_arc)
                    yield from bp.count(dets, num=1)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5)


####

# Data: /GPFS/xf12id1/data/images/users/2019_3/306008_Braunschweig/


# NOTE - this x position is close to the edge of the sample AB_2_5_MeDPP_SiO2_thermal_15minVSADCM_0.0800deg_waxs19.50_x-22400.0_0.5s_000001_WAXS.tif, checked egde pos: -22240

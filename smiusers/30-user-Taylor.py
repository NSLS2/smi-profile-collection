import numpy as np


def run_giwaxs_2020_3(t=0.5):  # 2020C1
    # define names of samples on sample bar

    sample_list = ["JM_1", "JM_2", "JM_3", "JM_4", "JM_5", "JM_6", "JM_7", "JM_8"]
    x_list = [53000, 39000, 24000, 9000, -5500, -2100, -35000, -49000]

    assert len(x_list) == len(sample_list), f"Sample name/position list is borked"
    angle_arc = np.array([0.08, 0.10, 0.12, 0.30])  # incident angles
    waxs_angle_array = np.linspace(
        0, 19.5, 4
    )  # (0, 18, 4)   # q=4*3.14/0.77*np.sin((max angle+3.5)/2*3.14159/180)
    # if 12, 3: up to q=2.199
    # if 18, 4: up to q=3.04

    dets = [pil300KW]  # waxs, maxs, saxs = [pil300KW, rayonix, pil1M]
    for x, sample in zip(x_list, sample_list):  # loop over samples on bar

        yield from bps.mv(piezo.x, x)  # move to next sample
        yield from alignement_gisaxs(0.1)  # run alignment routine

        th_meas = (
            angle_arc + piezo.th.position
        )  # np.array([0.10 + piezo.th.position, 0.20 + piezo.th.position])
        th_real = angle_arc

        det_exposure_time(t, t)
        x_meas = x

        for waxs_angle in waxs_angle_array:
            yield from bps.mv(waxs, waxs_angle)
            for i, th in enumerate(th_meas):  # loop over incident angles
                yield from bps.mv(piezo.th, th)
                # for jj in [  0 ]: # repeated measurements at different x
                #     if i==0 and jj==0:
                #         x_meas = x_meas + 200   # shift a bit in x
                #     else:
                #         x_meas = x_meas + 200   # shift a bit in x
                yield from bps.mv(piezo.x, x_meas + i * 200)

                sample_name = (
                    "{sample}_deg{th:5.3f}_x{x}_waxs{waxs_angle:05.2f}_{t}s".format(
                        sample=sample,
                        th=th_real[i],
                        x=x_meas,
                        waxs_angle=waxs_angle,
                        t=t,
                    )
                )
                sample_id(user_name="AT", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")

                # yield from bp.scan(dets, energy, e, e, 1)
                # yield from bp.scan(dets, waxs, *waxs_arc)
                yield from bp.count(dets, num=1)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5)


def run_giwaxs(t=0.5):  # 2020C1
    # define names of samples on sample bar

    sample_list = ["ZQ_PM6Y6_20pASSQ_No32d"]
    x_list = [-13000]

    assert len(x_list) == len(sample_list), f"Sample name/position list is borked"
    angle_arc = np.array([0.12])  # incident angles
    waxs_angle_array = np.linspace(
        0, 19.5, 4
    )  # (0, 18, 4)   # q=4*3.14/0.77*np.sin((max angle+3.5)/2*3.14159/180)
    # if 12, 3: up to q=2.199
    # if 18, 4: up to q=3.04
    dets = [pil300KW]  # waxs, maxs, saxs = [pil300KW, rayonix, pil1M]
    for x, sample in zip(x_list, sample_list):  # loop over samples on bar

        yield from bps.mv(piezo.x, x)  # move to next sample
        # yield from bps.mv(piezo.th, 0)
        yield from alignement_gisaxs(0.1)  # run alignment routine
        # yield from bps.mv(waxs, 4)
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
        for waxs_angle in waxs_angle_array:
            yield from bps.mv(waxs, waxs_angle)
            for i, th in enumerate(th_meas):  # loop over incident angles
                yield from bps.mv(piezo.th, th)
                for jj in [0]:  # repeated measurements at different x
                    if i == 0 and jj == 0:
                        x_meas = x_meas + 200  # shift a bit in x
                    else:
                        x_meas = x_meas + 200  # shift a bit in x
                    yield from bps.mv(piezo.x, x_meas)

                    sample_name = (
                        "{sample}_deg{th:5.3f}_x{x}_waxs{waxs_angle:05.2f}_{t}s".format(
                            sample=sample,
                            th=th_real[i],
                            x=x_meas,
                            waxs_angle=waxs_angle,
                            t=t,
                        )
                    )
                    sample_id(user_name="AT", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")

                    # yield from bp.scan(dets, energy, e, e, 1)
                    # yield from bp.scan(dets, waxs, *waxs_arc)
                    yield from bp.count(dets, num=1)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5)


def do_twaxs_scanx(meas_t=1):  # 2019_2
    # x_list = [-37000]
    # sample_list = ['blank_kapton']
    # x_list = [-19000, -1000, 17000 ]
    # sample_list = ['2_mg_ml_freestanding_1','2_mg_ml_freestanding_2', '1_5_mg_ml_freestanding_1']

    # x_list = [-32000, -14000, 2000, 22000, 41000]
    # sample_list = ['Kapton_blank_ambient','3_mg_ml_freestanding_annealed_ambient', '3_mg_ml_freestanding_ambient','2_5_mg_ml_freestanding_annealed_ambient','2_5_mg_ml_freestanding_ambient']

    x_list = [11719]
    sample_list = [
        "ultimate_MXene_2",
    ]

    # x_list = [-38280, -23279, 34719]
    # sample_list = ['mechanically_exfoliated_mxene_1', 'mechanically_exfoliated_mxene_2', 'mechanically_exfoliated_on_glass']

    dets = [pil300KW]  # , pil1M, rayonix]

    # waxs_angle_array = np.linspace(0, 24, 5)
    waxs_angle_array = np.linspace(0, 12, 1)
    # x_shift_array = np.linspace(-1000, 1000, 9)
    x_shift_array = np.linspace(-300, 600, 31)
    # y_shift_array = np.linspace(-300, 600, 31)

    name_fmt = "{sample}_waxs{waxsangle}_x{xpos}_y{ypos}_saxs4m_{meas_t}s"  # was 5.1m

    for x, sample in zip(x_list, sample_list):  # loop over samples on bar
        x_pos_array = x + x_shift_array

        for waxs_angle in waxs_angle_array:
            yield from bps.mv(waxs, waxs_angle)

            for x_meas in x_pos_array:
                yield from bps.mv(piezo.x, x_meas)
                det_exposure_time(meas_t, meas_t)

                sample_name = name_fmt.format(
                    sample=sample,
                    waxsangle="%05.2f" % waxs_angle,
                    xpos="%07.1f" % piezo.x.position,
                    ypos="%07.1f" % piezo.y.position,
                    meas_t="%04.1f" % meas_t,
                )
                sample_id(user_name="AT", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")

                # yield from bp.scan(dets, waxs, *waxs_arc)
                yield from bp.count(dets, num=1)


####
"""
============RUN 2===========
   sample_list = [ 'JK_3DPerov_5_No10','JK_3DPerov_10_No12','M_2DPerov_CB_No16','JM_2DPerov_NS_No9','JM_2DPerov_PCBM_No10','JM_2DPerov_ITF_No17' ]  
    x_list = [   -48200,  -32200,  -16200, -1200, 14800,   31800  ] 

============RUN 3===========
    sample_list = [ 'JM_2DPerov_Y6_No13','JM_2DPerov_ITO_No14','JM_2DPerov_PVDF_No15','JM_2DPerov_PEDOT_PVDF_No16','JM_2DPerov_10degCPrecool_No17','JM_2DPerov_RTPrecool_No18' ]  
    x_list = [   -47800,  -32300,  -15800, -800, 15200,   31200  ] 

============RUN 4===========      
    sample_list = [ 'ZQ_Organic_PM6Y6_without_anneal_No19','ZQ_Organic_PM6Y6_No20','ZQ_Organic_PM6Y6_No21','ZQ_Organic_PM6Y6_No22','ZQ_Organic_PM6_No23','ZQ_Organic_Y6_No24' ]  
    x_list = [   -50000,  -34000,  -17000, 7000, 19000,   32000  ] 

===========RUN 4b=========== 
    sample_list = ['ZQ_Organic_PM6Y6_No20b','ZQ_Organic_Y6_No24b' ]  
    x_list = [-28000, 34000 ] 

===========RUN 5=========== 
    sample_list = [ 'ZQ_NeatFilm_PM6_No25','ZQ_NeatFilm_PM6_No26','ZQ_NeatFilm_Y6_No27','ZQ_NeatFilm_Y6_No28','ZQ_NeatFilm_ASSQ_No29','ZQ_NeatFilm_ASSQ_No30' ]  
    x_list = [   -46000,  -32000,  -16000, 0, 16000,   32000  ] 

===========RUN 6=========== 
    sample_list = [ 'ZQ_PM6Y6_20pASSQ_No31b','ZQ_PM6Y6_20pASSQ_No32b','ZQ_PM6Y6_10pASSQ_No33b','ZQ_PM6Y6_10pASSQ_No34b','ZQ_PM6Y6_8pASSQ_No35b','ZQ_PM6Y6_8pASSQ_No36b' ] [3:] 
    x_list = [   -44000,  -29000,  -13000, 5000, 21000, 36000  ]

===========RUN 7=========== 
    sample_list = [ 'ZQ_PM6Y6_6pASSQ_No37','ZQ_PM6Y6_4pASSQ_No38','ZQ_PM6Y6_2pASSQ_No39','ZQ_PM6Y6_25pASSQ_No40','ZQ_PM6Y6_40pASSQ_No41','ZQ_PM6Y6_50pASSQ_No42' ] 
    x_list = [   -46000,  -30000,  -15000, 1000, 16000, 32000  ]

===========RUN 8=========== 
    sample_list = [ 'ZQ_Y6_No24c','ZQ_PM6Y6__20pASSQ_No31c','ZQ_PM6Y6_20pASSQ_No32c','ZQ_PM6Y6_40pASSQ_No41c'] 
    x_list = [   -42000,  -25000,  -7000, 8000]
"""

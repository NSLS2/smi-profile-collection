def ex_situ(meas_t=1):
    # x_list = [45300, 38800, 32600, 26100, 19500, 13500, 7000, 600, -5700, -12100, -18400, -25200, -31500, -37500, -43700]
    # sample_list = ['cap1', 'cap2', 'cap3', 'cap4', 'cap5', 'cap6', 'cap7', 'cap8', 'cap9', 'cap10', 'cap11', 'cap12',  'cap13', 'cap14', 'cap15']

    # x_list_A = [-37500, -31200, -25000, -18300, -12000, -6000]
    # sample_list_A = ['hexane', 'toluene', 'PbS15_hexane_50mgmL','PbS16_hexane_25mgmL','PbS17_hexane_100mgmL','PbS22B_hexane_100mgmL']

    # x_list_B = [-43700, -37200, -31000, -24500, -18300, -11800, -5500]
    # sample_list_B = ['Fe3O4-9_14p9mgmL_toluene', 'Fe3O4-11_23p1mgmL_toluene', 'Fe3O4-14_7p4mgmL_toluene','Fe3O4-15_12p6mgmL_toluene','PbS25_100mgmL_hexane','PbS26_29p7mgmL_hexane','PbS27_31.3mgmL_hexane']

    # x_list_C = [38800, 32500, 25900, 19300, 13200, 7000, 500, -5800, -12100, -18450, -24900, -31350]
    # sample_list_C = ['FICO-6A_mgmL_hexane', 'FICO-6B_mgmL_hexane', 'FICO-6C_mgmL_hexane','FICO-6D_mgmL_hexane','FICO-6E_mgmL_hexane','FICO-6F_mgmL_hexane','FICO-7A2_mgmL_hexane','FICO-7A3_mgmL_hexane','FICO-7B2_mgmL_hexane','FICO-7D2_mgmL_hexane','FICO-2AW_mgmL_hexane','FICO-2AP_mgmL_hexane']

    # x_list_D = [38500, 32400, 25900, 19300, 13100, 6800]
    # sample_list_D = ['10mM_SDS_H2O', 'OLD_A_FICO_6E_1pcOA_50mM_SDS', 'OLD_B_FICO_6E_100mM_SDS','OLD_C_Fe3O4-11_PbS22B_1to1p5_1pcOA_10mM_SDS','OLD_D_Fe3O4-11_PbS22B_1to2_1pcOA_10mM_SDS','OLD_E_Fe3O4-11_PbS22B_1to2p5_1pcOA_10mM_SDS']

    x_list_E = [
        38800,
        32400,
        26100,
        19400,
        13400,
        6900,
        600,
        -5700,
        -12100,
        -18400,
        -25200,
        -31500,
        -37500,
        -44100,
    ]
    sample_list_E = [
        "PbS22B_FICO_7A2_2to1_1pcOA_10mM_SDS",
        "PbS22B_FICO_7A2_3to1_1pcOA_10mM_SDS",
        "PbS22B_FICO_7A2_4p5to1_1pcOA_10mM_SDS",
        "PbS25_PbS15_2to1_1pcoA_10mM_SDS",
        "PbS25_PbS15_1to1_1pcOA_10mM_SDS",
        "PbS25_PbS15_1to2_1pcOA_10mM_SDS",
        "PbS16_PbS15_2to1_1pcOA_10mM_SDS",
        "PbS16_PbS15_1to1_1pcOA_10mM_SDS",
        "PbS16_PbS15_1to2_1pcOA_10mM_SDS",
        "PbS22B_Fe3O4-11_1to1_1pcOA_10mM_SDS",
        "PbS22B_Fe3O4-11_2to1_1pcOA_10mM_SDS",
        "PbS22B_Fe3O4-11_13to1_1pcOA_10mM_SDS",
        "PbS22B_Fe3O4-14_1to1_1pcOA_10mM_SDS",
        "PbS22B_Fe3O4-14_1to2_1pcOA_10mM_SDS",
    ]

    # waxs_arc = [0, 13, 3]
    dets = [pil1M]
    # dets = [pil300KW, pil1M]

    for x, sample in zip(x_list_E, sample_list_E):  # loop over samples on bar
        yield from bps.mv(piezo.x, x)
        det_exposure_time(meas_t, meas_t)

        name_fmt = "{sample}_x{x_pos}_y{y_pos}_sax{saxs_z}m_{meas_t}s_{scan_id}"
        sample_name = name_fmt.format(
            sample=sample,
            x_pos=np.round(piezo.x.position, 2),
            y_pos=np.round(piezo.y.position, 2),
            saxs_z=np.round(pil1m_pos.z.position, 2),
            meas_t=meas_t,
            scan_id=RE.md["scan_id"],
        )
        sample_id(user_name="EM", sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")
        # yield from bp.scan(dets, waxs, *waxs_arc)
        yield from bp.count(dets, num=1)


def in_situ(meas_t=1, t0=0):
    y_list = [6200, 2150, -2200, -6350]
    # y_list = [-6350]

    sample_list = [
        "Kin40_Fe11_PbS22B_1to2_hextol_noOA_200mM-SDS_70C",
        "Kin39_FICO6C_PbS26_1to3_hextol_noOA_200mM-SDS_70C",
        "Kin38_FICO6C_PbS26_1to3p86_hextol_noOA_200mM-SDS_70C",
        "Kin37_FICO7B2_PbS26_1to6_hextol_noOA_200mM-SDS_70C",
    ]
    # sample_list = ['FICO_72A_70C_200mMSDS_noOA_monocrystal']
    # sample_list = ['xtestgreen32', 'xtestyellow31', 'xtestred30', 'xtestblue29']
    # sample_list = ['green', 'yellow', 'red', 'blue']

    dets = [pil300KW, pil1M]
    if t0 < 10:
        t0 = time.time()

    scan_id0 = RE.md["scan_id"] + 1
    yield from bps.sleep(1)
    count = 0

    for ii in range(50000):
        for y, sample in zip(y_list, sample_list):  # loop over samples on bar
            yield from bps.mv(piezo.y, y)
            det_exposure_time(meas_t, meas_t)

            name_fmt = (
                "{sample}_x{x_pos}_y{y_pos}_sax{saxs_z}m_{meas_t}s_t{t}s_{scan_id}"
            )
            sample_name = name_fmt.format(
                sample=sample,
                x_pos=np.round(piezo.x.position, 2),
                y_pos=np.round(piezo.y.position, 2),
                saxs_z=np.round(pil1m_pos.z.position, 2),
                meas_t=meas_t,
                t=np.round(time.time() - t0, 0),
                scan_id=scan_id0 + count,
            )
            count = count + 1

            # name_fmt = '{sample}_{scan_id}_t{t}s_x{x_pos}_y{y_pos}_sax{saxs_z}m_{meas_t}s'
            # sample_name = name_fmt.format(sample=sample, scan_id=scan_id0+count, t=np.round(time.time()-t0, 0), x_pos=np.round(piezo.x.position,2), y_pos=np.round(piezo.y.position,2), saxs_z=np.round(pil1m_pos.z.position,2), meas_t=meas_t)

            sample_id(user_name="EM_insitu", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")

            yield from bps.sleep(1)
            yield from bp.count(dets, num=1)


def in_situ_wrap(meas_t=1, t0=0):
    if t0 < 10:
        t0 = time.time()
    try:
        yield from in_situ(meas_t, t0=t0)
    except:
        print("!!!! ERROR, but proceed in 2 sec!!!!")
        yield from bps.sleep(2)
        yield from in_situ_wrap(meas_t, t0=t0)


#
# Note:
# 2019-12-04 11pm started in-situ with 20ml/min at room temp; RE errors
# 2019-12-05 4pm tube broken, change to thick ones, also lower flow rate to 5 with higher temp
# %run -i /home/xf12id/.ipython/profile_collection/startup/users/30-user-Murray.py

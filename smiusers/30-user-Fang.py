def ex_situ(meas_t=1):
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


sample_id(user_name="Fang", sample_name="test")
sample_list = [
    "Au10_FF",
    "Au10FCC_50",
    "Au10FCC_100",
    "Au10FCC_150",
    "Au10FCC_200",
]
##150 should be 200
##200 should be 500

## Beam center: ( 431, 567 )
## det to sample distance: 5.3 meter
## 16.1 KeV
## beam size: 20 X 200


def movx(dx):
    yield from bps.mvr(piezo.x, dx)


def movy(dy):
    yield from bps.mvr(piezo.y, dy)


def measure_saxs(i, meas_t=1, att="Sn60X4", my=False):
    dets = [pil1M]
    if my:
        yield from bps.mvr(piezo.y, 30)
    det_exposure_time(meas_t, meas_t)
    sample = sample_list[i]
    name_fmt = "{sample}_x{x_pos}_y{y_pos}_sax{saxs_z}m_{meas_t}s_{att}_att_{scan_id}"
    sample_name = name_fmt.format(
        sample=sample,
        x_pos=np.round(piezo.x.position, 2),
        y_pos=np.round(piezo.y.position, 2),
        saxs_z=np.round(pil1m_pos.z.position, 2),
        meas_t=meas_t,
        att=att,
        scan_id=RE.md["scan_id"],
    )
    sample_id(user_name="Fang", sample_name=sample_name)
    print(f"\n\t=== Sample: {sample_name} ===\n")
    # yield from bp.scan(dets, waxs, *waxs_arc)
    yield from bp.count(dets, num=1)


def in_situ(meas_t=1, t0=0):
    y_list = [6200, 2150, -2200, -6350]

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


# print(time.strftime('%Y-%m-%dT%H:%M:%S %Z',time.localtime(time.time())))


# proposal_id('2019_3', '305435_Murray')
# purple OnAxis is beam position in air

# ======== To open bluesky: bsui

# --- Close the hutch
#
# %run -i /home/xf12id/.ipython/profile_collection/startup/users/30-user-Murray.py
#
# --- To take a single measurement:
# sample_id(user_name='EM',sample_name='test') then, on Pilatus1M, enter exposure time and click 'Start'
#
#
# --- Before opening hutch:
# If bluesky is set to running and want to stop just type 'exit'
#
# bsx 1.050000 for saxs_z 8300
# bsx0.350000 for saxs_z 7300
# bsx0.750000 for saxs_z 6300
# bsx1.500000 for saxs_z 5300
#
# --- To move WAXS detector (Pilatus 300K)
#
# %run -i /home/xf12id/.ipython/profile_collection/startup/users/30-user-Fang.py

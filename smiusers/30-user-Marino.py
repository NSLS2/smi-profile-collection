# E. Marino (UPenn, Murray)
# ref: Chopra, Clark
#
# ======================================================================
# proposal_id('2024_3', '315975_Gonzalez', analysis=True)
#
### To complie this file
#
#%run -i /home/xf12id/.ipython/profile_collection/startup/users/30-user-Marino.py
### See which filter combination gives good reading (100~500), diode saturates at 125k
# RE(test_pdcurrent(Natt=3, add_att1_9=1, add_att1_10=0, add_att1_11=0, add_att1_12=0))
# RE(test_pdcurrent(Natt=3, add_att1_9=1, add_att1_10=1))
#
### Take one measurement, or click 'Start'
# RE(ct(t = 1))
#
### Start measurement with the good filter combination
# RE(insitu_EM(t=1, name = 'EXsitu_PbS53_0p1pc_run1dilute', wait_time_sec=10, Natt=3, add_att1_9=1, add_att1_10=1, number_start=1))
#
#
#
# if do ctrl+C: RE.abort()
#
# RE(shopen())
# RE(shclose())
#
# Data: /nsls2/xf12id2/data/images/users/2022_1/309930_Murray/
# Analysis: /nsls2/xf12id2/analysis/2022_1/309930_Murray/
#
# ======================================================================

import numpy as np
import sys, time

# det = [pil1M, pdcurrent, pdcurrent1, pdcurrent2]
# dets = [pil300KW, pil1M]
def ct(dets=[pil1M], t=1):
    det_exposure_time(t, t)
    bp.count(dets, num=1)


def test_pdcurrent(Natt=2, add_att1_9=1, add_att1_10=0, add_att1_11=0, add_att1_12=0):
    if add_att1_9 == 1:
        for aa in np.arange(0, Natt):
            yield from bps.mv(att1_9.open_cmd, 1)
            yield from bps.sleep(0.5)
    else:
        for aa in np.arange(0, Natt):
            yield from bps.mv(att1_9.close_cmd, 1)
            yield from bps.sleep(0.5)

    if add_att1_10 == 1:
        for aa in np.arange(0, Natt):
            yield from bps.mv(att1_10.open_cmd, 1)
            yield from bps.sleep(0.5)
    else:
        for aa in np.arange(0, Natt):
            yield from bps.mv(att1_10.close_cmd, 1)
            yield from bps.sleep(0.5)

    if add_att1_11 == 1:
        for aa in np.arange(0, Natt):
            yield from bps.mv(att1_11.open_cmd, 1)
            yield from bps.sleep(0.5)
    else:
        for aa in np.arange(0, Natt):
            yield from bps.mv(att1_11.close_cmd, 1)
            yield from bps.sleep(0.5)

    if add_att1_12 == 1:
        for aa in np.arange(0, Natt):
            yield from bps.mv(att1_12.open_cmd, 1)
            yield from bps.sleep(0.5)
    else:
        for aa in np.arange(0, Natt):
            yield from bps.mv(att1_12.close_cmd, 1)
            yield from bps.sleep(0.5)

    fs.open()
    yield from bps.sleep(0.3)
    pd_curr = pdcurrent1.value  # Current2Ave, quadEM
    fs.close()
    print("======== Current pd_curr {}\n".format(pd_curr))
    #### Remove atten
    if add_att1_9 == 1:
        for aa in np.arange(0, Natt):
            yield from bps.mv(att1_9.close_cmd, 1)
            yield from bps.sleep(0.5)

    if add_att1_10 == 1:
        for aa in np.arange(0, Natt):
            yield from bps.mv(att1_10.close_cmd, 1)
            yield from bps.sleep(0.5)

    if add_att1_11 == 1:
        for aa in np.arange(0, Natt):
            yield from bps.mv(att1_11.close_cmd, 1)
            yield from bps.sleep(1)

    if add_att1_12 == 1:
        for aa in np.arange(0, Natt):
            yield from bps.mv(att1_12.close_cmd, 1)
            yield from bps.sleep(1)

def measure_EM(t=1, name='in-situ', extra='check'):
    det_exposure_time(t, t)

    dets = [pil1M]
    curr_tempC = LThermal.temperature()
    print("---------  Current temperature (degC)\n {}".format(curr_tempC))

    #### Define sample name & Measure
    t1 = time.time()
    name_fmt = "{sample}_{extra}_{temperature}C_x{}_y{}{md}"
    sample_name = name_fmt.format(
        sample=name,
        extra=extra,
        temperature="%3.1f" % (curr_tempC),
        # pd_curr="%5.5d" % (pd_curr),
        x = "%.2f" % (stage.x.position),
        y = "%.2f" % (stage.y.position),
        md = get_scan_md()
    )
    print(f"\n\t=== Sample: {sample_name} ===\n")
    sample_id(user_name="EM", sample_name=sample_name)


def insitu_EM(
    t=1,
    name="insitu_S1_run1",
    wait_time_sec=30,
    Natt=2,
    add_att1_9=1,
    add_att1_10=1,
    add_att1_11=1,
    add_att1_12=0,
    add_att=0,
    number_start=1,
    use_waxs=0,
    interval_waxs=5,
):

    dets = [pil1M, pdcurrent, pdcurrent1, pdcurrent2]
    det_exposure_time(t, t)

    t0 = time.time()
    number = number_start

    # pil1M.cam.file_path.put(
    #     f"/nsls2/xf12id2/data/images/users/2024_3/315975_Gonzalez/1M/EM_%s" % name
    # )

    # pil1M.cam.file_path.put(
    #     f"/nsls2/data/smi/legacy/results/data/2024_3/315975_Gonzalez/1M/EM_%s" % name
    # )
    while number < 9000:
        # yield from bps.mv(stage.y, yss[number])
        # yield from bps.mv(stage.x, xss[number])

        #### Insert atten & Get pindiode reading
        dets = [pdcurrent, pdcurrent1, pdcurrent2]

        if add_att1_9:
            for aa in np.arange(0, Natt):
                yield from bps.mv(att1_9.open_cmd, 1)
                yield from bps.sleep(1)
        else:
            for aa in np.arange(0, Natt):
                yield from bps.mv(att1_9.close_cmd, 1)
                yield from bps.sleep(0.5)

        if add_att1_10:
            for aa in np.arange(0, Natt):
                yield from bps.mv(att1_10.open_cmd, 1)
                yield from bps.sleep(1)
        else:
            for aa in np.arange(0, Natt):
                yield from bps.mv(att1_10.close_cmd, 1)
                yield from bps.sleep(0.5)

        if add_att1_11:
            for aa in np.arange(0, Natt):
                yield from bps.mv(att1_11.open_cmd, 1)
                yield from bps.sleep(1)
        else:
            for aa in np.arange(0, Natt):
                yield from bps.mv(att1_11.close_cmd, 1)
                yield from bps.sleep(0.5)

        if add_att1_12 == 1:
            for aa in np.arange(0, Natt):
                yield from bps.mv(att1_12.open_cmd, 1)
                yield from bps.sleep(0.5)
        else:
            for aa in np.arange(0, Natt):
                yield from bps.mv(att1_12.close_cmd, 1)
                yield from bps.sleep(0.5)

        fs.open()
        yield from bps.sleep(0.3)
        pd_curr = pdcurrent1.value  # Current2Ave, quadEM
        fs.close()
        print("--------- Current pd_curr {}\n".format(pd_curr))
        #### Remove atten
        if add_att1_9:
            for aa in np.arange(0, Natt):
                yield from bps.mv(att1_9.close_cmd, 1)
                yield from bps.sleep(1)

        if add_att1_10:
            for aa in np.arange(0, Natt):
                yield from bps.mv(att1_10.close_cmd, 1)
                yield from bps.sleep(1)

        if add_att1_11:
            for aa in np.arange(0, Natt):
                yield from bps.mv(att1_11.close_cmd, 1)
                yield from bps.sleep(1)

        if add_att1_12:
            for aa in np.arange(0, Natt):
                yield from bps.mv(att1_12.close_cmd, 1)
                yield from bps.sleep(1)

        dets = [pil1M]

        #### Get temperature reading
        # curr_tempC = ls.input_A_celsius.value
        # ii = 1
        # while curr_tempC > 200 and ii < 50:  # Sometimes reading can be off
        #     yield from bps.sleep(0.2)
        #     curr_tempC = ls.input_A_celsius.value
        #     ii = ii + 1
        curr_tempC = LThermal.temperature()
        print("---------  Current temperature (degC)\n {}".format(curr_tempC))

        #### Take a waxs every 10 measurements / Unused
        if use_waxs == 1:
            if number % interval_waxs == 0:
                yield from bps.mv(waxs, 0)
                dets = [pil300KW]
            else:
                yield from bps.mv(waxs, 13)
                dets = [pil1M]
            det_exposure_time(t, t)

        #### Define sample name & Measure
        t1 = time.time()
        name_fmt = "{sample}_{number}_{temperature}C_t{time}_pd{pd_curr}_x{x}_y{y}{md}"
        sample_name = name_fmt.format(
            sample=name,
            number=number,
            temperature="%3.1f" % (curr_tempC),
            time="%3.1f" % (t1 - t0),
            pd_curr="%5.5d" % (pd_curr),
            x = "%.2f" % (stage.x.position),
            y = "%.2f" % (stage.y.position),
            md = get_scan_md()
        )
        print(f"\n\t=== Sample: {sample_name} ===\n")
        sample_id(user_name="EM", sample_name=sample_name)

        if add_att:
            for aa in np.arange(0, Natt):
                yield from bps.mv(att1_11.open_cmd, 1)
                yield from bps.sleep(0.5)

        yield from bp.count(dets, num=1)

        if add_att:
            for aa in np.arange(0, Natt):
                yield from bps.mv(att1_11.close_cmd, 1)
                yield from bps.sleep(0.5)

        #### Wait
        yield from bps.sleep(wait_time_sec)
        number = number + 1


#####################
## Bar 24 (Labelled BAR 3)
user_name = "EM2_Bar24"
sample_list = [
    "S15_PbS50_02pc_CH",
    "S14_PbS50_04pc_CH",
    "S13_PbS50_06pc_CH",
    "S12_PbS50_08pc_CH",
    "S11_PbS50_10pc_CH",
    "S10_HEXANE",
    "S09_PbS50_0p1pc_HEXANE",
    "S08_PbS50_02pc_HEXANE",
    "S07_PbS50_04pc_HEXANE",
    "S06_PbS50_06pc_HEXANE",
    "S05_PbS50_08pc_HEXANE",
    "S04_PbS50_10pc_HEXANE",
    #'S03_ANISOLE',  'S02_PbS50_0p1pc_ANISOLE', 'S01_PbS50_02pc_ANISOLE'
]
x_list = [
    46150,
    40000,
    33600,
    27400,
    21100,
    14600,
    8200,
    1800,
    -4400,
    -10400,
    -16500,
    -23100,
    # -29200, -35300, -41800
]


#######################################################
def exsitu_EM(t=1, x_range_um=0, Nx=1, Nrep=3, add_att=1, more_scans=0, use_waxs=0):

    assert len(x_list) == len(sample_list), f"Sample name/position list is incorrect!"

    x_shift_array = np.linspace(-x_range_um, x_range_um, Nx)
    Natt = 5  # to ensure attenuator is placed/removed

    ### SAXS
    for ii, (x, sample) in enumerate(zip(x_list, sample_list)):
        print("\n##### {}, {} #####\n".format(ii, sample))

        yield from bps.mv(piezo.x, x)  # move to next sample

        x_pos_array = x + x_shift_array

        for x_meas in x_pos_array:  # measure at a few x positions
            yield from bps.mv(piezo.x, x_meas)

            #### Insert atten & Get pindiode reading
            dets = [pdcurrent, pdcurrent1, pdcurrent2]

            for aa in np.arange(0, Natt):
                yield from bps.mv(att1_9.open_cmd, 1)
                yield from bps.sleep(0.5)
                yield from bps.mv(att1_10.open_cmd, 1)
                yield from bps.sleep(0.5)
                if add_att:
                    yield from bps.mv(att1_11.open_cmd, 1)
                    yield from bps.sleep(1)

            fs.open()
            yield from bps.sleep(0.3)
            pd_curr = pdcurrent1.value
            if ii == 0:
                pd_curr_ref = pd_curr
            fs.close()
            print(
                "--------- Current pd_curr {}, pd_curr_ref {}\n".format(
                    pd_curr, pd_curr_ref
                )
            )
            #### Remove atten
            for aa in np.arange(0, Natt):
                yield from bps.mv(att1_9.close_cmd, 1)
                yield from bps.sleep(0.5)
                yield from bps.mv(att1_10.close_cmd, 1)
                yield from bps.sleep(0.5)
                if add_att:
                    yield from bps.mv(att1_11.close_cmd, 1)
                    yield from bps.sleep(1)

            dets = [pil1M]

            if more_scans == 1:
                Nscan = np.ceil(pd_curr_ref / pd_curr)
            else:
                Nscan = Nrep
            print("\n--------- Nscan = {}---------\n".format(Nscan))

            for nn in np.arange(0, Nscan, 1):
                det_exposure_time(t, t)

                if add_att:
                    for aa in np.arange(0, Natt):
                        yield from bps.mv(att1_10.open_cmd, 1)
                        yield from bps.sleep(0.5)

                    name_fmt = "{sample}_att1-10_x{x}_n{nn}_exp{t}s_pd{pd_curr}"
                else:
                    name_fmt = "{sample}_x{x}_n{nn}_exp{t}s_pd{pd_curr}"

                #### Define sample name & Measure
                t1 = time.time()
                sample_name = name_fmt.format(
                    sample=sample,
                    x="%05.2f" % (x_meas),
                    nn=nn,
                    t="%2.2f" % (t),
                    pd_curr="%5.5d" % (pd_curr),
                )
                print(f"\n\t=== Sample: {sample_name} ===\n")
                sample_id(user_name=user_name, sample_name=sample_name)

                yield from bp.count(dets, num=1)

        if add_att:
            for aa in np.arange(0, Natt):
                yield from bps.mv(att1_10.close_cmd, 1)
                yield from bps.sleep(0.5)

    ### WAXS
    if use_waxs:
        yield from bps.mv(waxs, 0)
        for ii, (x, sample) in enumerate(zip(x_list, sample_list)):
            yield from bps.mv(piezo.x, x)  # move to next sample

            x_pos_array = x + x_shift_array

            for x_meas in x_pos_array:  # measure at a few x positions
                yield from bps.mv(piezo.x, x_meas)

                dets = [pil300KW]
                det_exposure_time(t, t)

                #### Define sample name & Measure
                t1 = time.time()
                name_fmt = "{sample}_x{x}"
                sample_name = name_fmt.format(sample=name, x="%05.2f" % (x_meas))
                print(f"\n\t=== Sample: {sample_name} ===\n")
                sample_id(user_name="EM", sample_name=sample_name)

                yield from bp.count(dets, num=1)
        yield from bps.mv(waxs, 13)


# RE(bps.mv(waxs, 13))
# sample_id(user_name='test', sample_name='test')

def gisaxsElb(meas_t=1):
    dude = "CM"
    waxs_arc = [3.25, 15.25, 3]
    dets = [pil1M, pil300KW, rayonix, xbpm3.sumY]
    # glob_xoff = 1000
    xlocs1 = [
        45600
    ]  # , 33600, 24600, 14600, 3600, -6400, -16400, -26400, -34400, -44400]

    names1 = [
        "KE_G22G1_50nmDiR_10mg-1"
    ]  # ,'KE_G22G1_50nmDiR_10mg-2','KE_G22G1_50nmDiR_5mg-3','KE_G22G1_50nmDiR_5mg-4','KE_G22G1_15nmDiR_5mg-5','KE_G22G1_15nmDiR_10mg-6','KE_G22G1_15nmDiR_10mg-7','KE_G22G1_15nmDiR_1mg-8','KE_G22G1_35nmDiR_20mg-0', 'KE_G22G1_35nmDiR_1mg-10']

    # what we run now
    curr_tray = xlocs1
    curr_names = names1
    assert len(curr_tray) == len(
        curr_names
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    for x, name in zip(curr_tray, curr_names):
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(piezo.th, 0.2)
        # yield from alignCai()
        plt.close("all")
        angle_offset = [0.02, 0.12, 0.32]
        a_off = piezo.th.position
        det_exposure_time(meas_t)
        name_fmt = "{sample}_{angle}deg_x{x_pos}"
        temp = ls.ch1_read.value
        for k in range(0, 3, 1):
            x_meas = x + k * 50
            for j, ang in enumerate(a_off + np.array(angle_offset)):
                yield from bps.mv(piezo.x, x_meas)
                real_ang = 0.08 + angle_offset[j]
                yield from bps.mv(piezo.th, ang)
                sample_name = name_fmt.format(
                    sample=name, angle=real_ang, x_pos=np.round(x_meas, 3)
                )
                sample_id(user_name=dude, sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.scan(dets, waxs, *waxs_arc)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5)


alignbspos = 11
measurebspos = 1.1
GV7 = TwoButtonShutter("XF:12IDC-VA:2{Det:1M-GV:7}", name="GV7")


def alignmentmodeCai():
    # yield from bps.mv(GV7.open_cmd, 1 )
    yield from SMIBeam().insertFoils("Alignement")
    if waxs.arc.position < 8:
        yield from bps.mv(waxs, 8)
    yield from bps.sleep(1)
    yield from bps.mv(pil1m_pos.x, -7)
    yield from bps.mv(pil1m_bs_rod.x, alignbspos)
    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5)


def measurementmodeCai():
    # yield from bps.mv(GV7.close_cmd, 1 )
    yield from bps.mv(pil1m_pos.x, -7)
    yield from bps.mv(pil1m_bs_rod.x, measurebspos)
    yield from bps.sleep(1)
    yield from SMIBeam().insertFoils("Measurement")
    yield from bps.sleep(1)


def align_gisaxs_height_Cai(rang=0.3, point=31, der=False):
    yield from bp.rel_scan([pil1M], piezo.y, -rang, rang, point)
    ps(der=der)
    yield from bps.mv(piezo.y, ps.cen)


def align_gisaxs_th_Cai(rang=0.3, point=31):
    yield from bp.rel_scan([pil1M], piezo.th, -rang, rang, point)
    ps()
    yield from bps.mv(piezo.th, ps.peak)


def align_gisaxsCai():
    align_gisaxs_manualCai(rang=0.2, point=31)
    align_gisaxs_manualCai(rang=0.1, point=21)


def alignCai():
    det_exposure_time(0.5)
    sample_id(user_name="test", sample_name="test")
    yield from alignmentmodeCai()
    yield from bps.mv(pil1M.roi1.min_xyz.min_y, 900)
    yield from align_gisaxs_height_Cai(700, 16, der=True)
    yield from align_gisaxs_th_Cai(1, 11)
    yield from align_gisaxs_height_Cai(300, 11, der=True)
    yield from align_gisaxs_th_Cai(0.5, 16)
    yield from bps.mv(piezo.th, ps.peak + 0.08)
    yield from bps.mv(
        pil1M.roi1.min_xyz.min_y, 900 - 97
    )  # 168 px for 0.1deg at 8.3 m, 330px for 0.25deg at 6.5 m
    yield from align_gisaxs_th_Cai(0.3, 31)
    yield from align_gisaxs_height_Cai(200, 21)
    yield from align_gisaxs_th_Cai(0.05, 21)
    yield from bps.mv(piezo.th, ps.cen)
    yield from measurementmodeCai()


def alignfine():
    det_exposure_time(0.5)
    sample_id(user_name="test", sample_name="test")
    yield from alignmentmodeCai()
    yield from bps.mv(pil1M.roi1.min_xyz.min_y, 900 - 97)
    yield from align_gisaxs_th_Cai(0.25, 31)
    yield from align_gisaxs_height_Cai(220, 25)
    yield from align_gisaxs_th_Cai(0.1, 21)
    yield from bps.mv(piezo.th, ps.cen)
    yield from measurementmodeCai()

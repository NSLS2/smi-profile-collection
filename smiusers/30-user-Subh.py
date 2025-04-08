# Aligam GiSAXS sample
#


def align_gisaxs_height_subh(rang=0.3, point=31, der=False):
    det_exposure_time(0.5)
    sample_id(user_name="test", sample_name="test")
    yield from bp.rel_scan([pil1M, pil1mroi1, pil1mroi2], piezo.y, -rang, rang, point)
    ps(der=der)
    yield from bps.mv(piezo.y, ps.cen)


def align_gisaxs_th_subh(rang=0.3, point=31):
    det_exposure_time(0.5)
    sample_id(user_name="test", sample_name="test")
    yield from bp.rel_scan([pil1M], piezo.th, -rang, rang, point)
    ps()
    yield from bps.mv(piezo.th, ps.peak)


Att_Align1 = att2_6  # att1_12
Att_Align2 = att2_7  # att1_9
GV7 = TwoButtonShutter("XF:12IDC-VA:2{Det:1M-GV:7}", name="GV7")
alignbspossubh = 11.15
measurebspossubh = 1.15


def alignmentmodesubh():
    # Att_Align1.set("Insert")
    # yield from bps.sleep(1)
    yield from bps.mv(att1_2, "Insert")
    yield from bps.sleep(1)
    yield from bps.mv(att1_3, "Insert")
    yield from bps.sleep(1)
    yield from bps.mv(GV7.open_cmd, 1)
    yield from bps.mv(pil1m_bs_rod.x, alignbspossubh)
    if waxs.arc.position < 12:
        yield from bps.mv(waxs, 12)
    sample_id(user_name="test", sample_name="test")


def measurementmodesubh():
    yield from bps.mv(pil1m_bs_rod.x, measurebspossubh)
    yield from bps.sleep(1)
    # Att_Align1.set("Retract")
    # yield from bps.sleep(1)
    yield from bps.mv(att1_2, "Retract")
    yield from bps.sleep(1)
    yield from bps.mv(att1_3, "Retract")
    yield from bps.sleep(1)
    yield from bps.mv(GV7.close_cmd, 1)
    yield from bps.sleep(1)
    # mov(waxs,3)


def alignquick():
    # Att_Align1.set("Insert")
    # yield from bps.sleep(1)
    yield from bps.mv(att1_2, "Insert")
    yield from bps.sleep(1)
    yield from bps.mv(att1_3, "Insert")
    yield from bps.sleep(1)
    yield from bps.mv(GV7.open_cmd, 1)
    yield from bps.mv(pil1m_bs_rod.x, alignbspossubh)
    if waxs.arc.position < 8:
        yield from bps.mv(waxs, 8)
    sample_id(user_name="test", sample_name="test")


def meas_after_alignquick():
    yield from bps.mv(pil1m_bs_rod.x, measurebspossubh)
    yield from bps.sleep(1)
    yield from bps.mv(att1_2, "Retract")
    yield from bps.sleep(1)
    yield from bps.mv(att1_3, "Retract")
    yield from bps.sleep(1)
    # mov(waxs,3)


def alignsubhgi():
    det_exposure_time(0.5)
    sample_id(user_name="test", sample_name="test")
    yield from alignmentmodesubh()
    yield from bps.mv(pil1M.roi1.min_xyz.min_y, 863)
    yield from bps.mv(pil1M.roi1.size.y, 100)
    yield from bps.mv(pil1M.roi1.size.x, 100)

    yield from align_gisaxs_height_subh(1000, 16, der=True)
    yield from align_gisaxs_th_subh(1000, 11)
    yield from align_gisaxs_height_subh(500, 11, der=True)
    yield from align_gisaxs_th_subh(500, 11)

    yield from bps.mv(piezo.th, ps.peak - 100)
    yield from bps.mv(pil1M.roi1.min_xyz.min_y, 783)
    yield from bps.mv(pil1M.roi1.size.y, 10)
    yield from align_gisaxs_th_subh(300, 31)
    yield from align_gisaxs_height_subh(200, 21)
    yield from align_gisaxs_th_subh(100, 21)
    yield from bps.mv(
        piezo.th, ps.cen + 12
    )  # moves the th to 0.012 degrees positive from aligned 0.1
    yield from measurementmodesubh()


def do_grazingsubh(meas_t=1):
    # xlocs = [48403]
    # names = ['BW30-CH-Br-1']
    # Detectors, motors:
    dets = [pil300KW, pil300kwroi2, xbpm3.sumY, xbpm2.sumY]
    xlocs = [0]
    x_offset = np.linspace(2000, -2000, 41)
    names = ["btbtwo3"]
    prealigned = [0]
    for xloc, name, aligned in zip(xlocs, names, prealigned):
        yield from bps.mv(piezo.x, xloc)
        yield from bps.mv(piezo.th, -1300)
        if aligned == 0:
            yield from alignsubhgi()
            plt.close("all")
        angle_offset = np.linspace(-120, 80, 41)
        # angle_offset = array([-120,-115,-110,-105,-100,-95,-90,-85,-80,-75,-70,-65,-60,-55,-50,-45,-40,-35,-30,-25,-20,-15,-10,-5,0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80])
        e_list = [7060]
        a_off = piezo.th.position
        waxs_arc = [3, 21, 4]
        det_exposure_time(meas_t)
        name_fmt = "{sample}_{energ}eV_{angle}deg"
        offset_idx = 0
        # yield from bps.mv(att2_9, 'Insert')
        for i_e, e in enumerate(e_list):
            # yield from bps.mv(energy, e)
            for j, ang in enumerate(a_off - np.array(angle_offset)):
                yield from bps.mv(piezo.x, xloc + x_offset[offset_idx])
                offset_idx += 1
                real_ang = 0.200 + angle_offset[j] / 1000
                yield from bps.mv(piezo.th, ang)
                sample_name = name_fmt.format(sample=name, angle=real_ang, energ=e)
                # print(param)
                sample_id(user_name="NIST", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                # print(RE.md)
                yield from bp.scan(dets, waxs, *waxs_arc)

        sample_id(user_name="test", sample_name="test")
        det_exposure_time(0.5)
        # yield from bps.mv(att2_9, 'Retract')


def align_shortcut():
    yield from alignquick()
    yield from align_gisaxs_height_subh(100, 15)
    yield from meas_after_alignquick()


def do_grazingtemp(meas_t=4):
    # Detectors, motors:
    dets = [pil300KW, pil300kwroi2, xbpm3.sumY, xbpm2.sumY]
    e_list = [20300]
    det_exposure_time(meas_t)
    waxs_arc = [3, 9, 2]

    piezo_x1 = [0, -400, 12]
    piezo_x2 = [-500, -900, 12]
    piezo_x3 = [-1000, -1400, 12]
    piezo_x4 = [-1500, -1900, 12]
    piezo_x5 = [-2000, -2400, 12]
    piezo_x6 = [-2500, -2900, 12]
    piezo_x7 = [-3000, -3400, 12]
    piezo_x8 = [-3500, -3900, 12]

    sample_id(user_name="AK", sample_name="P75B2_50C_0.088deg_20300eV1")
    yield from bp.grid_scan(dets, piezo.x, *piezo_x1, waxs, *waxs_arc, 1)
    yield from align_shortcut()
    det_exposure_time(meas_t)
    sample_id(user_name="AK", sample_name="P75B2_50C_0.088deg_20300eV2")
    yield from bp.grid_scan(dets, piezo.x, *piezo_x2, waxs, *waxs_arc, 1)
    yield from align_shortcut()
    det_exposure_time(meas_t)
    sample_id(user_name="AK", sample_name="P75B2_50C_0.088deg_20300eV3")
    yield from bp.grid_scan(dets, piezo.x, *piezo_x3, waxs, *waxs_arc, 1)
    yield from align_shortcut()
    det_exposure_time(meas_t)
    sample_id(user_name="AK", sample_name="P75B2_50C_0.088deg_20300eV4")
    yield from bp.grid_scan(dets, piezo.x, *piezo_x4, waxs, *waxs_arc, 1)
    yield from align_shortcut()
    det_exposure_time(meas_t)
    sample_id(user_name="AK", sample_name="P75B2_50C_0.088deg_20300eV5")
    yield from bp.grid_scan(dets, piezo.x, *piezo_x5, waxs, *waxs_arc, 1)
    yield from align_shortcut()
    det_exposure_time(meas_t)
    sample_id(user_name="AK", sample_name="P75B2_50C_0.088deg_20300eV6")
    yield from bp.grid_scan(dets, piezo.x, *piezo_x6, waxs, *waxs_arc, 1)
    yield from align_shortcut()
    det_exposure_time(meas_t)
    sample_id(user_name="AK", sample_name="P75B2_50C_0.088deg_20300eV7")
    yield from bp.grid_scan(dets, piezo.x, *piezo_x7, waxs, *waxs_arc, 1)
    yield from align_shortcut()
    det_exposure_time(meas_t)
    sample_id(user_name="AK", sample_name="P75B2_50C_0.088deg_20300eV8")
    yield from bp.grid_scan(dets, piezo.x, *piezo_x8, waxs, *waxs_arc, 1)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5)


def do_singleimage(meas_t=4):
    # Detectors, motors:
    dets = [pil300KW, pil300kwroi2, xbpm3.sumY, xbpm2.sumY]
    e_list = [20300]
    det_exposure_time(meas_t)
    waxs_arc = [3, 9, 2]
    sample_id(user_name="AK", sample_name="PVDFWBcool_50C_0.088deg_20300eV1")
    yield from bp.grid_scan(dets, waxs, *waxs_arc)


def do_grazing_cool(meas_t=4):
    # Detectors, motors:
    dets = [pil300KW, pil300kwroi2, xbpm3.sumY, xbpm2.sumY]
    waxs_arc = [3, 9, 2]
    e_list = [20300]
    det_exposure_time(meas_t)

    xlocs = [0]
    sample_id(user_name="AK", sample_name="PB_50C_0.088deg_20300eV_cool")
    yield from bp.grid_scan(dets, waxs, *waxs_arc)

    xlocs = [10000]
    sample_id(user_name="AK", sample_name="P50B_50C_0.088deg_20300eV_cool")
    yield from bp.grid_scan(dets, waxs, *waxs_arc)

    xlocs = [20000]
    sample_id(user_name="AK", sample_name="PWB_50C_0.088deg_20300eV_cool")
    yield from bp.grid_scan(dets, waxs, *waxs_arc)

    xlocs = [30000]
    sample_id(user_name="AK", sample_name="P50WB_50C_0.088deg_20300eV_cool")
    yield from bp.grid_scan(dets, waxs, *waxs_arc)

    xlocs = [40000]
    sample_id(user_name="AK", sample_name="PVDFWB_50C_0.088deg_20300eV_cool")
    yield from bp.grid_scan(dets, waxs, *waxs_arc)

    xlocs = [50000]
    sample_id(user_name="AK", sample_name="P75WB_50C_0.088deg_20300eV_cool")
    yield from bp.grid_scan(dets, waxs, *waxs_arc)

    xlocs = [60000]
    sample_id(user_name="AK", sample_name="P75WB_100C_0.088deg_20300eV_cool")
    yield from bp.grid_scan(dets, waxs, *waxs_arc)

    xlocs = [70000]
    sample_id(user_name="AK", sample_name="P25WB_50C_0.088deg_20300eV_cool")
    yield from bp.grid_scan(dets, waxs, *waxs_arc)

    xlocs = [80000]
    sample_id(user_name="AK", sample_name="P25B_50C_0.088deg_20300eV_cool")
    yield from bp.grid_scan(dets, waxs, *waxs_arc)

    xlocs = [90000]
    sample_id(user_name="AK", sample_name="P75B2_50C_0.088deg_20300eV_cool")
    yield from bp.grid_scan(dets, waxs, *waxs_arc)


#  sample_id(user_name='test', sample_name='test')
#  det_exposure_time(0.5)


def do_grazing1(meas_t=2):
    # xlocs = [48403]
    # names = ['BW30-CH-Br-1']
    # Detectors, motors:
    dets = [pil300KW, pil300kwroi2, xbpm3.sumY, xbpm2.sumY]
    xlocs = [-37950]
    x_offset = [-200, 0, 200]
    names = ["ctrl1_focused_recheckoldmacro"]
    prealigned = [0]
    for xloc, name, aligned in zip(xlocs, names, prealigned):
        yield from bps.mv(piezo.x, xloc)
        yield from bps.mv(piezo.th, -500)
        if aligned == 0:
            yield from alignYalegi()
            plt.close("all")
        angle_offset = [100, 220, 300]
        e_list = [2460, 2477, 2500]
        a_off = piezo.th.position
        waxs_arc = [3, 87, 15]
        det_exposure_time(meas_t)
        name_fmt = "{sample}_{energ}eV_{angle}deg"
        for i_e, e in enumerate(e_list):
            yield from bps.mv(energy, e)
            yield from bps.mv(piezo.x, xloc + x_offset[i_e])
            for j, ang in enumerate(a_off - np.array(angle_offset)):
                real_ang = 0.3 + angle_offset[j] / 1000
                yield from bps.mv(piezo.th, ang)
                sample_name = name_fmt.format(sample=name, angle=real_ang, energ=e)
                # print(param)
                sample_id(user_name="FA", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                # print(RE.md)
                yield from bp.scan(dets, waxs, *waxs_arc)

        sample_id(user_name="test", sample_name="test")
        det_exposure_time(0.5)

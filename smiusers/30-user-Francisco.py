# %run -i /home/xf12id/.ipython/profile_collection/startup/users/30-user-Francisco.py


def snapYale(
    t=1,
    dets=[
        pil1M,
    ],
):
    det_exposure_time(t)
    yield from bp.count(dets, num=1)


def ROI_yale():
    yield from bps.mv(att2_11, "Insert")
    yield from bps.sleep(5)
    yield from bps.mv(att2_11, "Retract")


def do_grazing(meas_t=0.5):
    dets = [pil300KW, pil300kwroi2, xbpm3.sumY, xbpm2.sumY]
    # xlocs = [ 40000,25500,9000,-6000,-22000]
    # names = ['ctrl_glass','ctrl_assq_thin','ctrl_ASSQ_thick','ctrl_PDCBT_ITIC_pt9weight','ctrl_PDCBT_ITIC_ASSQ_1per_pt9weight']

    xlocs = [9000]
    names = ["ctrl_ASSQ_thick_finescan"]
    assert len(xlocs) == len(
        names
    ), f"Number of X coordinates ({len(x_list)}) is different from number of x offset ({len(samples)})"

    for xloc, name in zip(xlocs, names):
        yield from bps.mv(piezo.x, xloc)
        yield from bps.mv(piezo.th, 0.9)  # ask misha for the value
        yield from alignCai()
        plt.close("all")

        angle_offset = [0.1, 0.22, 0.3]  # ask misha
        a_off = piezo.th.position
        det_exposure_time(meas_t)

        e_list = [2460, 2477, 2500]
        waxs_arc = [2.8, 32.8, 6]
        name_fmt = "{sample}_{energ}eV_{angle}deg"

        offset_idx = 0
        for i_e, e in enumerate(e_list):
            yield from bps.mv(energy, e)
            for j, ang in enumerate(a_off - np.array(angle_offset)):
                x_offset = xloc - offset_idx * 1400
                offset_idx += 1
                real_ang = 0.3 + angle_offset[j]
                yield from bps.mv(piezo.th, ang)
                sample_name = name_fmt.format(sample=name, angle=real_ang, energ=e)

                sample_id(user_name="FA", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")

                yield from bp.inner_product_scan(
                    dets,
                    int(waxs_arc[2]),
                    waxs,
                    float(waxs_arc[0]),
                    float(waxs_arc[1]),
                    piezo.x,
                    x_offset - 600,
                    x_offset + 600,
                )

    det_exposure_time(0.5)


def do_grazing_fine(meas_t=0.5):
    dets = [pil300KW, pil300kwroi2, xbpm3.sumY, xbpm2.sumY]
    det1 = [pil300KW]
    # xlocs = [ -51500, -34700, -20500, -5500, 10000, 25000, 40000]
    # names = ['ctrl_ITO_finescan','P_I_A_90perA_finescan', 'P_I_A_50perA_finescan', 'P_I_A_10perA_finescan', 'P_I_A_01perA_finescan', 'P_I_A_00perA_finescan', 'ctrl_ASSQ_thickagain_finescan']

    # xlocs = [ -11500, -33500, -50000]
    # names = ['P_I_00perA_navy_b', 'P_I_A_01perA_teal_b', 'ctrl_ASSQ_thick_magenta_b']

    xlocs = [-45600, -27500, -10500, 6400]
    names = ["P_I_navy2", "P_I_10perA_green", "P_I_50perA_lightblue", "P_I_90perA_pink"]

    assert len(xlocs) == len(
        names
    ), f"Number of X coordinates ({len(x_list)}) is different from number of x offset ({len(samples)})"

    waxs_arc = np.linspace(2.8, 32.8, 6)
    # waxs_arc = np.linspace(2.8, 32.8, 2)

    for xloc, name in zip(xlocs, names):
        yield from bps.mv(piezo.x, xloc)
        yield from bps.mv(piezo.th, 0.9)
        yield from alignCai()
        plt.close("all")

        angle_offset = [0.22]
        a_off = piezo.th.position
        det_exposure_time(meas_t)

        e_list = [
            2470,
            2475,
            2476,
            2477,
            2478,
            2480,
            2482,
            2484,
            2486,
        ]  # , 2465, 2467, 2470, 2473, 2475, 2477, 2500]
        name_fmt = "{sample}_{energ}eV_{angle}deg_waxs{num}_x{xpos}"

        for i_e, e in enumerate(e_list):
            yield from bps.mv(energy, e)
            for j, ang in enumerate(a_off + np.array(angle_offset)):
                real_ang = 0.3 + angle_offset[j]
                yield from bps.mv(piezo.th, ang)
                for waxs_pos in waxs_arc:
                    yield from bps.mv(waxs, waxs_pos)
                    sample_name = name_fmt.format(
                        sample=name,
                        angle=real_ang,
                        energ=e,
                        num="%05.2f" % waxs_pos,
                        xpos="%07.1f" % piezo.x.position,
                    )
                    sample_id(user_name="FA2", sample_name=sample_name)
                    if waxs_pos < 4:
                        det_exposure_time(0.5)
                        yield from bp.count(det1, num=1)
                        yield from bps.mvr(piezo.x, 200)
                    else:
                        det_exposure_time(5)
                        yield from bp.count(det1, num=1)
                        yield from bps.mvr(piezo.x, 200)

                print(f"\n\t=== Sample: {sample_name} ===\n")

    det_exposure_time(0.5)


alignbspos = 11
measurebspos = 0.7


def test():
    yield from bps.mvr(pil1m_pos.x, 200)


def alignmentmodeCai():
    yield from bps.mv(GV7.open_cmd, 1)
    yield from bps.mv(att2_11, "Insert")

    if waxs.arc.position < 8:
        yield from bps.mv(waxs, 8)
    yield from bps.sleep(1)
    yield from bps.mv(pil1m_pos.x, -4)
    yield from bps.mv(pil1m_bs_rod.x, alignbspos)
    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5)


def measurementmodeCai():
    yield from bps.mv(GV7.close_cmd, 1)
    yield from bps.mv(pil1m_pos.x, -4)
    yield from bps.mv(pil1m_bs_rod.x, measurebspos)
    yield from bps.sleep(1)
    yield from bps.mv(att2_11, "Retract")
    yield from bps.sleep(1)


def align_gisaxs_height_Cai(rang=0.3, point=31, der=False):
    yield from bp.rel_scan([pil1M], piezo.y, -rang, rang, point)
    ps(der=der)
    yield from bps.mv(piezo.y, ps.cen)


def align_gisaxs_th_Cai(rang=0.3, point=31):
    yield from bp.rel_scan([pil1M], piezo.th, -rang, rang, point)
    ps()
    yield from bps.mv(piezo.th, ps.peak)


def alignCai():
    det_exposure_time(0.5)
    sample_id(user_name="test", sample_name="test")
    yield from alignmentmodeCai()
    yield from bps.mv(pil1M.roi1.min_xyz.min_y, 910)
    yield from align_gisaxs_height_Cai(700, 16, der=True)
    yield from align_gisaxs_th_Cai(1, 11)
    yield from align_gisaxs_height_Cai(300, 11, der=True)
    yield from align_gisaxs_th_Cai(0.5, 16)
    yield from bps.mv(piezo.th, ps.peak + 0.3)
    yield from bps.mv(
        pil1M.roi1.min_xyz.min_y, 910 - 487
    )  # 168 px for 0.1deg at 8.3 m, 330px for 0.25deg at 6.5 m 97 for 6 m and 0.08
    yield from align_gisaxs_th_Cai(0.3, 31)
    yield from align_gisaxs_height_Cai(200, 21)
    yield from align_gisaxs_th_Cai(0.05, 21)
    yield from bps.mv(piezo.th, ps.cen)
    yield from measurementmodeCai()


#

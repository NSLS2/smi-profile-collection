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


def do_grazing(meas_t=1):
    dets = [pil1M, pil300KW, rayonix]  # , pil300kwroi2, xbpm3.sumY, xbpm2.sumY]

    # xlocs = [ -43000, -25000, -7000, 10000, 25000, 40000 ]
    # names = ['bar1_C1a_50nm_sam1', 'bar1_C1a_50nm_sam2',  'bar1_C2B1_50nm_sam1',  'bar1_C2B1_50nm_sam2', 'bar1_Nafion_50nm_sam1', 'bar1_Nafion_50nm_sam2']
    # xlocs = [ -43000, -26000, -9000, 8000, 24000 ]
    # names = ['bar1_C1a_50nm_sam1', 'bar1_C1a_50nm_sam2',  'bar1_C2B1_50nm_sam1',  'bar1_C2B1_50nm_sam2', 'bar1_Nafion_50nm_sam1']
    xlocs = [-46000, -31000, -13000, 3500, 21500, 37000]
    names = [
        "bar2_C1a_250nm_sam1",
        "bar2_C1a_250nm_sam2",
        "bar2_C2B1_250nm_sam1",
        "bar2_C2B1_250nm_sam2",
        "bar2_Nafion_250nm_sam1",
        "bar2_Nafion_250nm_sam2",
    ]

    assert len(xlocs) == len(
        names
    ), f"Number of X coordinates ({len(x_list)}) is different from number of x offset ({len(samples)})"

    for xloc, name in zip(xlocs, names):
        yield from bps.mv(piezo.x, xloc)
        yield from bps.mv(piezo.th, 0.1)
        yield from alignCai()
        plt.close("all")

        angle_offset = [-0.05, -0.02, 0, 0.02, 0.1]
        a_off = piezo.th.position  #  yield from bps.mv(piezo.th, ps.peak + 0.1)
        # det_exposure_time(meas_t)

        waxs_arc = np.linspace(2.8, 32.8 + 18, 6 + 3)
        name_fmt = "{sample}_{energ}eV_{angle}deg_waxs{num}_{exposure}s_x{xpos}"

        # offset_idx = 0
        for j, ang in enumerate(a_off + np.array(angle_offset)):
            # x_offset =  xloc - offset_idx * 1800
            # offset_idx += 1
            real_ang = 0.1 + angle_offset[j]
            yield from bps.mv(piezo.th, ang)
            for waxs_pos in waxs_arc:
                yield from bps.mv(waxs, waxs_pos)
                sample_name = name_fmt.format(
                    sample=name,
                    angle="%04.2f" % real_ang,
                    energ="%07.1f" % energy.position.energy,
                    num="%05.2f" % waxs_pos,
                    xpos="%07.0f" % piezo.x.position,
                    exposure=meas_t,
                )
                sample_id(user_name="ET", sample_name=sample_name)
                det_exposure_time(meas_t)
                yield from bp.count(dets, num=1)
                yield from bps.mvr(piezo.x, 200)

                print(f"\n\t=== Sample: {sample_name} ===\n")

    det_exposure_time(0.5)


alignbspos = 11
measurebspos = 0.7


def test():
    yield from bps.mvr(pil1m_pos.x, 200)


def alignmentmodeCai():
    yield from bps.mv(GV7.open_cmd, 1)
    yield from SMIBeam().insertFoils("Alignement")

    if waxs.arc.position < 8:
        yield from bps.mv(waxs, 8)
    yield from bps.sleep(1)
    yield from bps.mv(pil1m_pos.x, -4)
    yield from bps.mv(pil1m_bs_rod.x, alignbspos)
    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5)


def measurementmodeCai():
    # yield from bps.mv(GV7.close_cmd, 1 ) #comment out to use pil1M
    yield from bps.mv(pil1m_pos.x, -4)
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


def alignCai():
    det_exposure_time(0.5)
    sample_id(user_name="test", sample_name="test")
    yield from alignmentmodeCai()
    yield from bps.mv(pil1M.roi1.min_xyz.min_x, 457)
    yield from bps.mv(pil1M.roi1.min_xyz.min_y, 910)
    yield from align_gisaxs_height_Cai(700, 16, der=True)
    yield from align_gisaxs_th_Cai(1, 11)
    yield from align_gisaxs_height_Cai(300, 11, der=True)
    yield from align_gisaxs_th_Cai(0.5, 16)
    yield from bps.mv(piezo.th, ps.peak + 0.1)  # 0.3
    yield from bps.mv(
        pil1M.roi1.min_xyz.min_y, 910 - 168
    )  # 168 px for 0.1deg at 8.3 m, 330px for 0.25deg at 6.5 m 97 for 6 m and 0.08
    yield from align_gisaxs_th_Cai(0.3, 31)
    yield from align_gisaxs_height_Cai(200, 21)
    yield from align_gisaxs_th_Cai(0.05, 21)
    yield from bps.mv(piezo.th, ps.cen)
    yield from measurementmodeCai()


#

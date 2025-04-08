def gocko(meas_t=1):
    dets = [pil300KW, xbpm3.sumY]
    xlocs1 = [-48000, -34000, -23000, -12000, 2000, 15000, 30000, 43000]
    names1 = [
        "BWXLE-new-water30min-CsBrsoaked-THF",
        "BWXLE-new-water30min-CsBrsoaked-DCM",
        "BW30-new-water30min-CsBrsoaked-THF",
        "BW30-new-water30min-CsBrsoaked-DCM",
        "BWXLE-new-sonic1min-CsBrsoaked-THF",
        "BWXLE-new-sonic1min-CsBrsoaked-DCM",
        "BW30-new-sonic1min-CsBrsoaked-THF",
        "BW30-new-sonic1min-CsBrsoaked-DCM",
    ]

    # what we run now
    curr_tray = xlocs1
    curr_names = names1
    assert len(curr_tray) == len(
        curr_names
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    waxs_arc = [2.83, 26.83, 5]
    for x, name in zip(curr_tray, curr_names):
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(piezo.th, 0.9)
        yield from alignCai()
        plt.close("all")
        angle_offset = [-0.05, -0.02, 0, 0.02, 0.05]
        a_off = piezo.th.position
        det_exposure_time(meas_t)
        name_fmt = "{sample}_{angle}deg"
        for j, ang in enumerate(a_off + np.array(angle_offset)):
            yield from bps.mv(piezo.x, (x + j * 0))
            real_ang = 0.1 + angle_offset[j]
            yield from bps.mv(piezo.th, ang)
            sample_name = name_fmt.format(sample=name, angle=float("%.3f" % real_ang))
            sample_id(user_name="BO_13.47keV", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.scan(dets, waxs, *waxs_arc)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5)


def test():
    yield from bps.mv(att1_9, "Insert")


def gocko_res(meas_t=1):

    xlocs1 = [-46000]
    names1 = ["Reso-BWXLE-new-NaClsoaked-water30min-THF"]
    # xlocs1 = [-46000, -35000, -22000, -10000]
    # names1 = ['Reso-BWXLE-new-NaClsoaked-water30min-THF','Reso-BWXLE-new-NaClsoaked-water30min-DCM','Reso-BW30-new-NaClsoaked-water30min-THF','Reso-BW30-new-NaClsoaked-water30min-DCM']
    xoffset = 0
    curr_tray = xlocs1
    curr_names = names1

    # ener = [5008, 5013, 5018, 5023, 5008]
    ener = [5018]

    det2 = [pil300KW, xbpm3.sumY]
    waxs_arc = [2.83, 56.83, 10]
    """
        for x, name in zip(curr_tray, curr_names): 
            yield from bps.mv(piezo.x, x)
            yield from bps.mv(piezo.th, 0.2)
            yield from alignCai()
            a_off = piezo.th.position
            plt.close('all')
            yield from bps.mv(att2_11, 'Insert')
            angle = [-0.12, 0.08, 0.24]
            det_exposure_time(meas_t) 
            name_fmt = '{sample}_{angle}deg_{energy}eV_{num}'
            for j, ang in enumerate( np.array(angle) ):
                yield from bps.mv(piezo.x, (x-xoffset+j*0))
                yield from bps.mv(piezo.th,  a_off + ang)
                i=0
                for energies in ener:
                    energy.move(energies)
                    sample_name = name_fmt.format(sample=name, angle=float('%.3f'%(ang+0.25)), energy = energies, num =i)
                    sample_id(user_name='BO', sample_name=sample_name)
                    print(f'\n\t=== Sample: {sample_name} ===\n')
                    yield from bp.scan(det2, waxs, *waxs_arc)
                    i += 1
        """
    curr_tray = xlocs1
    curr_names = names1
    det1 = [pil1M]

    xoffset = 200
    for x, name in zip(curr_tray, curr_names):
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(piezo.th, 0.2)
        yield from alignCai()
        a_off = piezo.th.position
        plt.close("all")
        yield from bps.mv(att2_5, "Insert")
        yield from bps.mv(att2_11, "Insert")
        yield from bps.sleep(1)
        yield from bps.mv(GV7.open_cmd, 1)
        i = 0
        a_off = piezo.th.position
        angle = [-0.12, 0.08]
        for j, ang in enumerate(angle):
            yield from bps.mv(piezo.x, (x - xoffset + j * 0))
            yield from bps.mv(piezo.th, a_off + ang)
            name_fmt = "{sample}_{angle}deg_{energy}eV_{num}"
            i = 0
            for energies in ener:
                energy.move(energies)
                sample_name = name_fmt.format(
                    sample=name,
                    angle=float("%.3f" % (ang + 0.25)),
                    energy=energies,
                    num=i,
                )
                sample_id(user_name="BO", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(det1, num=1)
                i += 1

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5)


alignbspos = 11
measurebspos = 1.2
GV7 = TwoButtonShutter("XF:12IDC-VA:2{Det:1M-GV:7}", name="GV7")


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
    yield from bps.mv(GV7.close_cmd, 1)
    yield from bps.mv(pil1m_pos.x, -4)
    yield from bps.mv(pil1m_bs_rod.x, measurebspos)
    yield from bps.sleep(1)
    yield from SMIBeam().insertFoils("Measurment")
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
    yield from bps.mv(piezo.th, ps.peak + 0.25)
    yield from bps.mv(
        pil1M.roi1.min_xyz.min_y, 900 - 97
    )  # 168 px for 0.1deg at 8.3 m, 330px for 0.25deg at 6.5 m 97 for 6 m and 0.08
    yield from align_gisaxs_th_Cai(0.3, 31)
    yield from align_gisaxs_height_Cai(200, 21)
    yield from align_gisaxs_th_Cai(0.05, 21)
    yield from bps.mv(piezo.th, ps.cen)
    yield from measurementmodeCai()


def alignfine():
    det_exposure_time(0.5)
    sample_id(user_name="test", sample_name="test")
    yield from alignmentmodeCai()
    yield from bps.mv(pil1M.roi1.min_xyz.min_y, 916 - 330)
    yield from align_gisaxs_th_Cai(0.25, 31)
    yield from align_gisaxs_height_Cai(220, 25)
    yield from align_gisaxs_th_Cai(0.1, 21)
    yield from bps.mv(piezo.th, ps.cen)
    yield from measurementmodeCai()

# from tracemalloc import _TraceTupleT


def sample_alignment():
    yield from bps.mvr(piezo.th, -1)
    yield from quickalign_gisaxs(angle=0.15)
    yield from bps.mvr(piezo.th, 1)
    yield from bps.mv(waxs, 10.3)

    ais.append([piezo.th.position])
    ys.append([piezo.y.position])


# def temp_align(cycle,temp):
def temp_align_waxs(temp):
    yield from bps.mv(waxs, 10.3)

    ai_offset = [
        0,
        -0.00049,
        -0.010885,
        -0.020069,
        -0.027797,
        -0.029081,
        -0.038985,
        -0.040642,
        -0.045495,
        -0.046898,
        -0.050634,
        -0.051935,
        -0.062148,
        -0.069523,
        -0.072856,
        -0.07382,
        -0.082091,
        -0.089965,
        -0.088196,
    ]
    y_offset = [
        0,
        1.3417e01,
        -2.9000e-02,
        -4.1000e-02,
        -5.4000e-02,
        -6.3000e-02,
        -1.3505e01,
        -1.3515e01,
        -1.3541e01,
        -1.3544e01,
        -1.3542e01,
        -1.3533e01,
        -2.6970e01,
        -2.6949e01,
        -2.6897e01,
        -2.6899e01,
        -4.0328e01,
        -5.3758e01,
        -6.7181e01,
    ]
    temp_list = [
        25,
        35,
        45,
        55,
        65,
        70,
        75,
        80,
        85,
        90,
        95,
        100,
        110,
        120,
        130,
        140,
        150,
        160,
        170,
    ]
    idx = np.argmin(abs(np.asarray(temp_list) - temp))

    yield from bps.mvr(piezo.th, 0.2 + ai_offset[idx])
    yield from bps.mvr(piezo.y, y_offset[idx])
    yield from bps.mvr(piezo.x, 50)

    # sample_id(user_name='DD', sample_name='2CsPbBr3-insitu_RTPost%.1f_sdd275m_ai1deg_wa10.3deg_%.1fs'%(temp, time.time()-t0))

    yield from bp.count([pil900KW])

    yield from bps.mvr(piezo.th, -0.2 - ai_offset[idx])
    yield from bps.mvr(piezo.y, -y_offset[idx])


# def temp_align(cycle,temp):
def temp_align_saxs(temp):
    yield from bps.mv(waxs, 20)

    ai_offset = [
        0,
        -0.00049,
        -0.010885,
        -0.020069,
        -0.027797,
        -0.029081,
        -0.038985,
        -0.040642,
        -0.045495,
        -0.046898,
        -0.050634,
        -0.051935,
        -0.062148,
        -0.069523,
        -0.072856,
        -0.07382,
        -0.082091,
        -0.089965,
        -0.088196,
    ]
    y_offset = [
        0,
        1.3417e01,
        -2.9000e-02,
        -4.1000e-02,
        -5.4000e-02,
        -6.3000e-02,
        -1.3505e01,
        -1.3515e01,
        -1.3541e01,
        -1.3544e01,
        -1.3542e01,
        -1.3533e01,
        -2.6970e01,
        -2.6949e01,
        -2.6897e01,
        -2.6899e01,
        -4.0328e01,
        -5.3758e01,
        -6.7181e01,
    ]
    temp_list = [
        25,
        35,
        45,
        55,
        65,
        70,
        75,
        80,
        85,
        90,
        95,
        100,
        110,
        120,
        130,
        140,
        150,
        160,
        170,
    ]
    idx = np.argmin(abs(np.asarray(temp_list) - temp))

    yield from bps.mvr(piezo.th, 0.1 + ai_offset[idx])
    yield from bps.mvr(piezo.y, y_offset[idx])
    yield from bps.mvr(piezo.x, 50)

    # sample_id(user_name='DD', sample_name='2SNPB-insitucycle_num%2.2d_kapton_quenchto%.1f_ai1deg_wa10.3deg_%.1fs'%(cycle, temp, time.time()-t0))
    # sample_id(user_name='DD', sample_name='2CsPbBr3-insitu_well_%.1f_sdd4m_ai0.2deg_wa20deg_%.1fs'%(temp, time.time()-t0))

    # if temp == 120:
    #     time.sleep(60)
    #     for t in range(0,14):
    #         yield from bp.count([pil1M, pil900KW])
    #         time.sleep(50)

    # else:
    yield from bp.count([pil1M, pil900KW])

    yield from bps.mvr(piezo.th, -0.1 - ai_offset[idx])
    yield from bps.mvr(piezo.y, -y_offset[idx])


def temp_ramp():
    yield from bps.mv(att2_1.open_cmd, 1)
    yield from bps.sleep(1)
    yield from bps.mv(att2_1.open_cmd, 1)
    yield from bps.sleep(1)

    yield from bps.mv(waxs, 20)  # 10.3 deg WAXS, 20 deg. SAXS/WAXS
    # tempz = [25, 50, 75, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200]
    # tempz = [28, 50, 75, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200]
    tempz = [28, 50, 75, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200]

    for i, temp in enumerate(tempz):
        if i == 0:
            t_dif = 0
        else:
            diff = tempz[i] - tempz[i - 1]
            t_dif = int(diff / 25 * 60)

        yield from bps.sleep(80 + t_dif)
        print(temp)
        sample_id(
            user_name="DD",
            sample_name="1CsPbBr3-invacuo_WAXS_heat_cycle2_%.1f_sdd4m_ai0.2deg_wa10.3deg_%.1fs"
            % (temp, time.time() - t0),
        )

        # yield from temp_align_saxs(temp)
        yield from temp_align_waxs(temp)


def giwaxs_White_2022_2(t=0.5):
    """
    GIWAXS scans duing 2022_2 cycle
    """

    user_name = "RT"

    # names =   [ '1-5-SC', '2-5-DC', '3-10-SC', '4-10-DC', '5-15-SC', '6-15-DC' ]
    # x_piezo = [    24000,    11000,     -4000,    -17000,    -28000,    -41000 ]
    # y_piezo = [ 3700 for name in names ]
    # z_piezo = [ 0 for name in names ]
    # x_hexa =  [ 0 for name in names ]

    # names =   [ 'K1', 'K9', 'K17', 'K29' ]
    # names =   [ 'K37', 'K5', 'K41', 'K13', 'K21' ]
    # names =   [ 'K2', 'K6', 'K10', 'K14', 'K18', 'K22', 'K26a', 'K26b', 'K30', 'K38',  'K42',  'K50',  'K51' ]
    # names =   [ 'BPA1', 'BPA2', '3FBPA1', '3FBPA2', 'Pure_sapph', '6FBPA1', 'OPPA1' ] #measured at 0.04 and 0.15 degees!!
    # names =   [ '2PACZ_par','2PACZ_Br2','2PACZ_2Fup','Clean_sapph','26FBPA_TiO2_S1','26FBPA_TiO2_S2','BPA_TiO2_S1','BPA_TiO2_S2','3FBPA_TiO2_S1','3FBPA_TiO2_S1','2PACZ_2Fdo' ]
    # names =   ['N2200', '01_MeO', '05_MeO', '10_MeO', '20_MeO', '01_FS', '05_FS', '10_FS', '20_FS', '2PACZ_2F_down_measur_01']
    # names =   [ 'sample_01', 'sample_02', 'sample_03', 'sample_04', 'sample_05', 'sample_06', 'sample_07', 'sample_08', 'sample_09', '2PACZ_2F_down_measur_01', 'sample_10a', 'sample_10b']

    names = ["sample_11"]
    x_piezo = [1500]
    y_piezo = [3600]
    z_piezo = [500]
    x_hexa = [0]

    # Check and correct sample names just in case
    names = [n.translate({ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ "}) for n in names]

    assert len(x_piezo) == len(
        names
    ), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(names)})"
    assert len(x_piezo) == len(
        y_piezo
    ), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(y_piezo)})"
    assert len(x_piezo) == len(
        z_piezo
    ), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(z_piezo)})"
    assert len(x_piezo) == len(
        x_hexa
    ), f"Number of X coordinates ({len(x_piezo)}) is different from number of samples ({len(x_hexa)})"

    # Geometry conditions
    waxs_angles = [0, 2, 20, 22]
    # inc angle handled separatelly for different samples
    # inc_angles = [0.04, 0.15]
    alignment_offset_x = 0  # microns
    det_exposure_time(t, t)

    # Skip samples
    skip = 0

    for name, xs, zs, ys, xs_hexa in zip(
        names[skip:], x_piezo[skip:], z_piezo[skip:], y_piezo[skip:], x_hexa[skip:]
    ):

        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, xs - alignment_offset_x)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)
        yield from bps.mv(piezo.th, 0.5)

        try:
            yield from alignement_gisaxs(0.1)
        except:
            yield from alignement_gisaxs(0.4)

        yield from bps.mv(piezo.x, xs)

        ai0 = piezo.th.position
        for wa in waxs_angles:

            yield from bps.mv(waxs, wa)
            dets = [pil900KW] if wa < 15 else [pil900KW, pil1M]

            inc_angles = [0.11] if name == "2PACZ_2F_down_measur_01" else [0.10, 0.18]

            for xx, ai in enumerate(inc_angles):
                yield from bps.mv(piezo.x, xs + xx * 400)
                yield from bps.mv(piezo.th, ai0 + ai)

                # Metadata
                name_fmt = "{sample}_ai{ai}_{energy}keV_wa{wax}_sdd{sdd}m_bpm{xbpm}"
                bpm = xbpm3.sumX.get()
                e = energy.energy.position / 1000
                sdd = pil1m_pos.z.position / 1000
                # wa = waxs.arc.user_readback.value
                # wa = str(np.round(wa, 1)).zfill(4)

                sample_name = name_fmt.format(
                    sample=name,
                    energy="%.1f" % e,
                    sdd="%.1f" % sdd,
                    wax=str(wa).zfill(4),
                    xbpm="%4.3f" % bpm,
                    ai="%.2f" % ai,
                )
                sample_id(user_name=user_name, sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")

                yield from bp.count(dets, num=1)
            yield from bps.mv(piezo.th, ai0)

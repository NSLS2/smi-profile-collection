# Align GiSAXS sample
import numpy as np


def mapping_saxs_Thed(t=1):
    samples = ["PT10E-001La", "PT10E-001M", "PT10E-001G", "PT10E-001H", "PT10E-001I"]
    x_list = [-45700, -45700, -17600, -2600, 27200]
    y_list = [-1900, 5200, -2600, -1600, -2900]

    name = "PT"

    x_range = [
        [0, 26000, 261],
        [0, 26000, 261],
        [0, 10100, 102],
        [0, 24400, 245],
        [0, 18100, 182],
    ]
    y_range = [[0, 0, 1], [0, 1000, 11], [0, 8500, 86], [0, 8000, 81], [0, 9300, 94]]

    # Detectors, motors:
    dets = [pil1M]  # dets = [pil1M,pil300KW]
    det_exposure_time(t, t)

    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    for x, y, sample, x_r, y_r in zip(x_list, y_list, samples, x_range, y_range):
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(piezo.y, y)
        sample_id(user_name=name, sample_name=sample)
        yield from bp.rel_grid_scan(dets, piezo.y, *y_r, piezo.x, *x_r, 0)

    #     for yrs in np.linspace(y_r[0], y_r[1], y_r[2]):
    #         yield from bps.mv(piezo.y, y+yrs)
    #         for xrs in np.linspace(x_r[0], x_r[1], x_r[2]):
    #             yield from bps.mv(piezo.x, x+xrs)
    #             name_fmt = '{sam}_x{x}_y{y}'
    #             sample_name = name_fmt.format(sam=sample, x='%6.6d'%(x+xrs), y='%6.6d'%(y+yrs))
    #             sample_id(user_name=name, sample_name=sample_name)
    #             #print(f'\n\t=== Sample: {sample_name} ===\n')
    #             yield from bp.count(dets, num=1)

    # #yield from bp.rel_grid_scan(dets, piezo.x, *x_r, piezo.y, *y_r, 0) #1 = snake, 0 = not-snake

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def mapping2_saxs_Thed(t=1):
    samples = [
        "PT10E-001A",
        "PT10E-001B",
        "PT10E-001C",
        "PT10E-001D",
        "PT10E-001E",
        "PT10E-001F",
    ]
    x_list = [37500, 28000, 10100, -4600, -17500, -37100]
    y_list = [-2800, -3100, -2800, 0, -400, -2100]

    name = "PT"

    x_range = [
        [0, 9200, 93],
        [0, 5000, 51],
        [0, 14000, 141],
        [0, 8300, 84],
        [0, 6900, 70],
        [0, 14600, 147],
    ]
    y_range = [
        [0, 7000, 71],
        [0, 9600, 97],
        [0, 9000, 91],
        [0, 6500, 66],
        [0, 6900, 70],
        [0, 7500, 76],
    ]

    # Detectors, motors:
    dets = [pil1M]  # dets = [pil1M,pil300KW]
    det_exposure_time(t, t)

    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    for x, y, sample, x_r, y_r in zip(x_list, y_list, samples, x_range, y_range):
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(piezo.y, y)
        sample_id(user_name=name, sample_name=sample)
        yield from bp.rel_grid_scan(dets, piezo.y, *y_r, piezo.x, *x_r, 0)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def mapping3_saxs_Thed(t=1):
    samples = [
        "PT10E-001B",
        "PT10E-001C",
        "PT10E-001D",
        "PT10E-001E",
        "PT10E-001F",
        "PT10E-001J",
    ]
    x_list = [34000, 12700, 1100, -9800, -28600, -42600]
    y_list = [0, -3000, -3100, -2600, -3200, -2400]

    name = "PT"

    x_range = [
        [0, 10000, 101],
        [0, 15600, 157],
        [0, 7000, 71],
        [0, 7000, 71],
        [0, 14000, 141],
        [0, 14600, 147],
    ]
    y_range = [
        [0, 4500, 46],
        [0, 9000, 91],
        [0, 7000, 71],
        [0, 6500, 66],
        [0, 6700, 68],
        [0, 6500, 66],
    ]

    # Detectors, motors:
    dets = [pil1M]  # dets = [pil1M,pil300KW]
    det_exposure_time(t, t)

    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    for x, y, sample, x_r, y_r in zip(x_list, y_list, samples, x_range, y_range):
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(piezo.y, y)
        sample_id(user_name=name, sample_name=sample)
        yield from bp.rel_grid_scan(dets, piezo.y, *y_r, piezo.x, *x_r, 0)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def capillaries_saxs_Thed(t=1):
    samples = [
        "LT666",
        "LT670",
        "LT671",
        "LT671-2",
        "LT672",
        "LT673",
        "LT676",
        "LT677",
        "LT678",
        "LT679",
        "LT679-2",
        "LT679-3",
        "LT680",
        "LT682",
        "LT683",
        "LT684",
        "LT686",
        "LT690",
        "LT691",
    ]

    x_list = [
        39300,
        32900,
        26500,
        20200,
        13900,
        7500,
        1000,
        -5400,
        -11600,
        -18100,
        -24300,
        -30700,
        -37100,
        -43300,
        36000,
        29900,
        23300,
        17300,
        10800,
    ]
    y_list = [
        3100,
        3100,
        3100,
        3100,
        3100,
        3100,
        3100,
        3100,
        3100,
        3100,
        3100,
        3100,
        3100,
        3100,
        3100,
        3100,
        3100,
        3100,
        3100,
    ]
    z_list = [
        2600,
        2600,
        2600,
        2600,
        2600,
        2600,
        2600,
        2600,
        2600,
        2600,
        2600,
        2600,
        2600,
        2600,
        11600,
        11600,
        11600,
        11600,
        11600,
    ]

    # Detectors, motors:
    dets = [pil1M]  # dets = [pil1M,pil300KW]
    det_exposure_time(t, t)

    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"

    for x, y, z, sample in zip(x_list, y_list, z_list, samples):
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(piezo.y, y)
        yield from bps.mv(piezo.z, z)

        sample_id(user_name="PT_2ndseries", sample_name=sample)
        yield from bp.count(dets, num=10)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.1, 0.1)


def gisaxs_Thed1(t=1):
    samples = [
        "FY5",
        "FY6",
        "FY7",
        "FY8",
        "FY9",
        "FY10",
        "FY11",
        "FY12",
        "FY13",
        "FY14",
    ]

    x_list = [-48000, -34000, -23000, -13000, -3000, 9000, 17000, 27000, 38000, 50000]

    waxs_arc = np.linspace(0, 58.5, 10)
    angle = [0.1, 0.15, 0.2]

    # Detectors, motors:
    dets = [pil1M, pil300KW]
    det_exposure_time(t, t)

    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"

    for x, sample in zip(x_list, samples):
        yield from bps.mv(piezo.x, x)

        sample_id(user_name="PT_gisaxs", sample_name=sample)

        yield from alignement_gisaxs(0.08)

        det_exposure_time(t, t)
        name_fmt = "{sample}_ai{angle}deg_wa{waxs}"
        for j, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)

            for an in angle:
                yield from bps.mvr(piezo.th, an)
                sample_name = name_fmt.format(
                    sample=sample, angle="%3.2f" % an, waxs="%2.1f" % wa
                )
                sample_id(user_name="PT", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")

                yield from bp.count(dets, num=2)
                yield from bps.mvr(piezo.th, -an)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.1, 0.1)


def saxs_well_Thed_2021(t=1):
    # samples = [
    # 'bkg27',      'PT10E_027A', 'PT10E_027B', 'PT10E_027C', 'PT10E_027D', 'PT10E_027E',
    # 'PT10E_027F', 'PT10E_027G', 'PT10E_027H', 'PT10E_027I', 'PT10E_027J', 'PT10E_027K',
    # 'PT10E_027L', 'PT10E_027M', 'PT10E_027N', 'PT10E_027O', 'PT10E_027P', 'PT10E_027Q',
    # 'PT10E_027R', 'PT10E_027S', 'PT10E_027T', 'PT10E_027U', 'PT10E_027V', 'PT10E_027W',

    # 'bkg28',      'PT10E_028A', 'PT10E_028B', 'PT10E_028C', 'PT10E_028D', 'PT10E_028E',
    # 'PT10E_028F', 'PT10E_028G', 'PT10E_028H', 'PT10E_028I', 'PT10E_028J', 'PT10E_028K',
    # 'PT10E_028L', 'PT10E_028M', 'PT10E_028N', 'PT10E_028O', 'PT10E_028P', 'PT10E_028Q',
    # 'PT10E_028R', 'PT10E_028S', 'PT10E_028T', 'PT10E_028U', 'PT10E_028V', 'PT10E_028W',]

    # x_list = [
    #    57500,  47500,  39000,  30000,  21000,  12000,
    #    56800,  48000,  39000,  30500,  21000,  12000,
    #    57500,  48000,  39000,  30500,  21000,  12000,
    #    57500,  48000,  39000,  30000,  21000,  12000,

    #     2000,  -7000, -16000, -25000, -34000, -42000,
    #     2000,  -7000, -16000, -25000, -33500, -42500,
    #     2000,  -7000, -16000, -25000, -34000, -43000,
    #     2000,  -7000, -16000, -25000, -34000, -43000]

    # y_list = [
    #    -6400,  -6200,  -6400,  -6400,  -6400,  -6400,
    #    -1900,  -1500,  -1200,  -1500,  -1500,  -1500,
    #     3900,   3500,   3600,   3600,   3600,   3600,
    #     8200,   8500,   8900,   8900,   8900,   8900,

    #     -6400, -6400,  -6400,  -6400,  -6000,  -6000,
    #     -1000,  -500,   -500,   -500,   -500,   -500,
    #      4000,  4000,   4000,   4000,   4000,   4000,
    #      8800,  8800,   8800,   8700,   8700,   9500]

    # samples = [
    # 'bkg31',      'PT10E_031A', 'PT10E_031B', 'PT10E_031C', 'PT10E_031D', 'PT10E_031E',
    # 'PT10E_031F', 'PT10E_031G', 'PT10E_031H', 'PT10E_031I', 'PT10E_031J', 'PT10E_031K',
    # 'PT10E_031L', 'PT10E_031M', 'PT10E_031N', 'PT10E_031O', 'PT10E_031P', 'PT10E_031Q',
    # 'PT10E_031R', 'PT10E_031S', 'PT10E_031T', 'PT10E_031U', 'PT10E_031V', 'PT10E_031W',

    # 'bkg32',      'PT10E_032A', 'PT10E_032B', 'PT10E_032C', 'PT10E_032D', 'PT10E_032E',
    # 'PT10E_032F', 'PT10E_032G', 'PT10E_032H', 'PT10E_032I', 'PT10E_032J', 'PT10E_032K',
    # 'PT10E_032L', 'PT10E_032M', 'PT10E_032N', 'PT10E_032O', 'PT10E_032P', 'PT10E_032Q',
    # 'PT10E_032R', 'PT10E_032S', 'PT10E_032T', 'PT10E_032U', 'PT10E_032V', 'PT10E_032W',]

    # x_list = [
    #    57500,  47500,  39000,  30000,  21000,  12000,
    #    57000,  48000,  39000,  30000,  21000,  12000,
    #    57300,  48000,  39000,  30000,  21000,  12000,
    #    57000,  48000,  39000,  30800,  22000,  12000,

    #        0,  -9000, -18000, -26000, -35000, -44000,
    #        0,  -9000, -17500, -26000, -35000, -44000,
    #        0,  -9000, -17500, -26500, -35000, -44000,
    #        0,  -8500, -17500, -26500, -35500, -44000]

    # y_list = [
    #    -6800,  -6200,  -6500,  -6500,  -6500,  -6500,
    #    -1900,  -1500,  -1500,  -1500,  -1500,  -1500,
    #     3900,   3400,   3600,   3600,   3600,   3600,
    #     9200,   9200,   9000,   9000,   8900,   8900,

    #     -6000, -6000,  -6000,  -6000,  -6000,  -6000,
    #     -700,  -700,   -700,   -700,   -700,   -700,
    #      4500,  4400,   4400,   4400,   4400,   4400,
    #      9500,  9500,   9500,   9500,   9500,   9500]

    samples = [
        "bkg33",
        "PT10E_033A",
        "PT10E_033B",
        "PT10E_033C",
        "PT10E_033D",
        "PT10E_033E",
        "PT10E_031F",
        "PT10E_033G",
        "PT10E_033H",
        "PT10E_033I",
        "PT10E_033J",
        "PT10E_033K",
        "PT10E_033L",
        "PT10E_033M",
        "PT10E_033N",
        "PT10E_033O",
        "PT10E_033P",
        "PT10E_033Q",
    ]

    x_list = [
        2500,
        -6500,
        -15300,
        -24400,
        -33000,
        -41500,
        3000,
        -6000,
        -15000,
        -24000,
        -33000,
        -41500,
        3000,
        -6000,
        -15000,
        -24000,
        -33000,
        -41500,
    ]

    y_list = [
        -6800,
        -6800,
        -6800,
        -6800,
        -6800,
        -6800,
        -1500,
        -1500,
        -1500,
        -2000,
        -1000,
        -1000,
        4000,
        4000,
        4000,
        4000,
        4000,
        4000,
    ]

    waxs_arc = np.linspace(13, 13, 1)

    # Detectors, motors:
    # dets = [pil300KW, pil1M]
    dets = [pil1M]

    det_exposure_time(t, t)

    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    assert len(x_list) == len(
        y_list
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(y_list)})"

    for j, wa in enumerate(waxs_arc):
        yield from bps.mv(waxs, wa)

        for x, y, sample in zip(x_list, y_list, samples):
            yield from bps.mv(piezo.x, x)
            yield from bps.mv(piezo.y, y)

            sample_id(user_name="PT", sample_name=sample)

            det_exposure_time(t, t)
            name_fmt = "{sample}_sdd5m_16.1keV_wa{waxs}"

            sample_name = name_fmt.format(sample=sample, waxs="%2.1f" % wa)
            sample_id(user_name="PT", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")

            yield from bp.count(dets, num=1)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.1, 0.1)


def saxs_well_Thed_2021_3(t=1):
    # samples = [
    # 'bkg43',      'PT10E_043A', 'PT10E_043B', 'PT10E_043C', 'PT10E_043D', 'PT10E_043E',
    # 'PT10E_043F', 'PT10E_043G', 'PT10E_043H', 'PT10E_043I', 'PT10E_043J', 'PT10E_043K',
    # 'PT10E_043L', 'PT10E_043M', 'PT10E_043N', 'PT10E_043O', 'PT10E_043P', 'PT10E_043Q',
    # 'PT10E_043R', 'PT10E_043S', 'PT10E_043T', 'PT10E_043U', 'PT10E_043V', 'PT10E_043W',

    # 'bkg46',      'PT10E_044A', 'PT10E_044B', 'PT10E_044C', 'PT10E_044D', 'PT10E_044E',
    # 'PT10E_044F', 'PT10E_044G', 'PT10E_044H', 'PT10E_044I', 'PT10E_044J', 'PT10E_044K',
    # 'PT10E_044L', 'PT10E_044M', 'PT10E_044N', 'PT10E_044O', 'PT10E_044P', 'PT10E_044Q',
    # 'PT10E_044R', 'PT10E_044S', 'PT10E_044T', 'PT10E_044U', 'PT10E_044V', 'PT10E_044W']

    # samples = [
    # 'bkg45',      'PT10E_045A', 'PT10E_045B', 'PT10E_045C', 'PT10E_045D', 'PT10E_045E',
    # 'PT10E_045F', 'PT10E_045G', 'PT10E_045H', 'PT10E_045I', 'PT10E_045J', 'PT10E_045K',
    # 'PT10E_045L', 'PT10E_045M', 'PT10E_045N', 'PT10E_045O', 'PT10E_045P', 'PT10E_045Q',
    # 'PT10E_045R', 'PT10E_045S', 'PT10E_045T', 'PT10E_045U', 'PT10E_045V', 'PT10E_045W',

    # 'bkg46',      'PT10E_046A', 'PT10E_046B', 'PT10E_046C', 'PT10E_046D', 'PT10E_046E',
    # 'PT10E_046F', 'PT10E_046G', 'PT10E_046H', 'PT10E_046I', 'PT10E_046J', 'PT10E_046K',
    # 'PT10E_046L', 'PT10E_046M', 'PT10E_046N', 'PT10E_046O', 'PT10E_046P', 'PT10E_046Q',
    # 'PT10E_046R', 'PT10E_046S', 'PT10E_046T']

    # samples = [
    # 'bkg42',      'PT10E_042A', 'PT10E_042B', 'PT10E_042C', 'PT10E_042D', 'PT10E_042E',
    # 'PT10E_042F', 'PT10E_042G', 'PT10E_042H', 'PT10E_042I', 'PT10E_042J', 'PT10E_042K',
    # 'PT10E_042L', 'PT10E_042M', 'PT10E_042N', 'PT10E_042O', 'PT10E_042P', 'PT10E_042Q',
    # 'PT10E_042R', 'PT10E_042S', 'PT10E_042T', 'PT10E_042U', 'PT10E_042V', 'PT10E_042W',

    # 'bkg47',      'PT10E_047A', 'PT10E_047B', 'PT10E_047C', 'PT10E_047D', 'PT10E_047E',
    # 'PT10E_047F', 'PT10E_047G', 'PT10E_047H', 'PT10E_047I', 'PT10E_047J', 'PT10E_047K',
    # 'PT10E_047L', 'PT10E_047M', 'PT10E_047N', 'PT10E_047O', 'PT10E_047P', 'PT10E_047Q',
    # 'PT10E_047R', 'PT10E_047S', 'PT10E_047T', 'PT10E_047U', 'PT10E_047V', 'PT10E_047W']

    # samples = [
    # 'bkg48',      'PT10E_048A', 'PT10E_048B', 'PT10E_048C', 'PT10E_048D', 'PT10E_048E',
    # 'PT10E_048F', 'PT10E_048G', 'PT10E_048H', 'PT10E_048I', 'PT10E_048J', 'PT10E_048K',
    # 'PT10E_048L', 'PT10E_048M', 'PT10E_048N', 'PT10E_048O', 'PT10E_048P', 'PT10E_048Q',
    # 'PT10E_048R', 'PT10E_048S', 'PT10E_048T', 'PT10E_048U', 'PT10E_048V', 'PT10E_048W',

    # 'bkg49',      'PT10E_049A', 'PT10E_049B', 'PT10E_049C', 'PT10E_049D', 'PT10E_049E',
    # 'PT10E_049F', 'PT10E_049G', 'PT10E_049H', 'PT10E_049I', 'PT10E_049J', 'PT10E_049K',
    # 'PT10E_049L', 'PT10E_049M']

    samples = [
        "bkg50",
        "PT10E_050A",
        "PT10E_050B",
        "PT10E_050C",
        "PT10E_050D",
        "PT10E_050E",
        "PT10E_050F",
        "PT10E_050G",
        "PT10E_050H",
        "PT10E_050I",
        "PT10E_050J",
        "PT10E_050K",
        "PT10E_050L",
        "PT10E_050M",
        "PT10E_050N",
        "PT10E_050R",
        "PT10E_050S",
        "PT10E_050T",
    ]

    x_list = [
        19900,
        10900,
        1900,
        -7100,
        -16100,
        -25000,
        19900,
        10900,
        1900,
        -7100,
        -16100,
        -25100,
        19600,
        10600,
        1900,
        19600,
        10600,
        1600,
    ]

    y_list = [
        -6900,
        -6900,
        -6900,
        -7200,
        -7500,
        -7400,
        -2000,
        -2000,
        -2000,
        -2100,
        -2000,
        -2000,
        3100,
        3100,
        3100,
        8500,
        8500,
        8500,
    ]

    waxs_arc = [0, 20]

    # Detectors, motors:
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    assert len(x_list) == len(
        y_list
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(y_list)})"

    for j, wa in enumerate(waxs_arc):
        yield from bps.mv(waxs, wa)

        for x, y, sample in zip(x_list, y_list, samples):
            yield from bps.mv(piezo.x, x)
            yield from bps.mv(piezo.y, y)

            sample_id(user_name="PT", sample_name=sample)

            det_exposure_time(t, t)
            name_fmt = "{sample}_sdd5m_14.0keV_wa{waxs}"

            sample_name = name_fmt.format(sample=sample, waxs="%2.1f" % wa)
            sample_id(user_name="PT", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")

            yield from bp.count(dets, num=1)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.1, 0.1)


def saxs_well_rot_Thed_2021_3(t=1):

    samples = [
        "PT10E_049F",
        "PT10E_049G",
        "PT10E_049H",
        "PT10E_049I",
        "PT10E_049J",
        "PT10E_049K",
        "PT10E_049L",
        "PT10E_049M",
    ]

    x_list = [2600, -6400, -15200, -24000, -32800, -41800, 2500, -6400]

    y_list = [-2000, -1800, -1800, -2100, -1700, -2100, 3100, 3200]

    # samples = ['PT10E_050R', 'PT10E_050S', 'PT10E_050T']

    # x_list = [1600,  10600, 19600]
    # y_list = [[8500,   8500,  8500]]

    waxs_arc = [20, 0]

    # Detectors, motors:
    dets = [pil1M, pil900KW]

    det_exposure_time(t, t)

    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    assert len(x_list) == len(
        y_list
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(y_list)})"

    for j, wa in enumerate(waxs_arc):
        yield from bps.mv(waxs, wa)

        for x, y, sample in zip(x_list, y_list, samples):
            yield from bps.mv(piezo.x, x)
            yield from bps.mv(piezo.y, y)

            for prs_an in np.linspace(-2.5, 2.5, 51):
                # for prs_an in np.linspace(-45, 45, 19):
                yield from bps.mv(prs, prs_an)

                sample_id(user_name="PT", sample_name=sample)

                det_exposure_time(t, t)
                name_fmt = "{sample}_sdd5m_14.0keV_prs{prs}_wa{waxs}"

                sample_name = name_fmt.format(
                    sample=sample, prs="%2.1f" % prs_an, waxs="%2.1f" % wa
                )
                sample_id(user_name="PT", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")

                yield from bp.count(dets, num=1)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.1, 0.1)


def saxs_well_rot_Thed_2021(t=1):
    waxs_arc = np.linspace(0, 58.5, 10)
    dets = [pil1M, pil300KW]
    det_exposure_time(t, t)

    for j, wa in enumerate(waxs_arc):
        yield from bps.mv(waxs, wa)

        samples = [
            "PT10E_019H_0deg",
            "PT10E_019J_0deg",
            "PT10E_019K_0deg",
            "PT10E_019M_0deg",
            "PT10E_019N_0deg",
            "PT10E_019P_0deg",
            "PT10E_019T_0deg",
            "PT10E_019U_0deg",
        ]
        x_list = [26200, 8200, -800, 35000, 26000, 8400, 26000, 17500]
        y_list = [-800, -800, -1000, 4700, 4400, 4600, 9500, 9600]
        assert len(x_list) == len(
            samples
        ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
        assert len(x_list) == len(
            y_list
        ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(y_list)})"

        yield from bps.mv(prs, 0)
        for x, y, sample in zip(x_list, y_list, samples):
            yield from bps.mv(piezo.x, x)
            yield from bps.mv(piezo.y, y)

            name_fmt = "{sample}_wa{waxs}"
            sample_name = name_fmt.format(sample=sample, waxs="%2.1f" % wa)
            sample_id(user_name="PT", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")

            yield from bp.count(dets, num=1)

        samples = [
            "PT10E_019H_-30deg",
            "PT10E_019J_-30deg",
            "PT10E_019K_-30deg",
            "PT10E_019M_-30deg",
            "PT10E_019N_-30deg",
            "PT10E_019P_-30deg",
            "PT10E_019T_-30deg",
            "PT10E_019U_-30deg",
        ]
        x_list = [26800, 9600, 600, 35000, 26900, 9500, 27000, 18500]
        y_list = [-800, -800, -1000, 4700, 4400, 4600, 9500, 9600]
        assert len(x_list) == len(
            samples
        ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
        assert len(x_list) == len(
            y_list
        ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(y_list)})"

        yield from bps.mv(prs, -30)
        for x, y, sample in zip(x_list, y_list, samples):
            yield from bps.mv(piezo.x, x)
            yield from bps.mv(piezo.y, y)

            name_fmt = "{sample}_wa{waxs}"
            sample_name = name_fmt.format(sample=sample, waxs="%2.1f" % wa)
            sample_id(user_name="PT", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")

            yield from bp.count(dets, num=1)

        samples = [
            "PT10E_019H_30deg",
            "PT10E_019J_30deg",
            "PT10E_019K_30deg",
            "PT10E_019M_30deg",
            "PT10E_019N_30deg",
            "PT10E_019P_30deg",
            "PT10E_019T_30deg",
            "PT10E_019U_30deg",
        ]
        x_list = [25500, 7600, -1800, 34200, 25400, 7500, 25200, 16700]
        y_list = [-800, -800, -1000, 4700, 4400, 4600, 9600, 9600]
        assert len(x_list) == len(
            samples
        ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
        assert len(x_list) == len(
            y_list
        ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(y_list)})"

        yield from bps.mv(prs, 30)
        for x, y, sample in zip(x_list, y_list, samples):
            yield from bps.mv(piezo.x, x)
            yield from bps.mv(piezo.y, y)

            name_fmt = "{sample}_wa{waxs}"
            sample_name = name_fmt.format(sample=sample, waxs="%2.1f" % wa)
            sample_id(user_name="PT", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")

            yield from bp.count(dets, num=1)
    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.1, 0.1)


def gisaxs_Thed_2021_1(t=1):

    global names, x_piezo, z_piezo, incident_angles, y_piezo_aligned, xs_hexa

    # names =  ['FY01','FY02','FY03','FY04','FY05','FY06','FY07','FY08','FY09', 'FY10','FY11', 'FY12', 'FY13', 'FY14', 'FY15', 'FY16',]
    # x_piezo = [60000, 53000, 45000, 38000, 31000, 22000, 15500,  9000,  1000, -7000, -17000, -27000, -36000, -44000, -52000, -60000,]
    # y_piezo = [ 6900,  6900,  6900,  6900,  6900,  6900,  6900,  6900,  6900,  6900,   6900,   6900,   6900,   6900,   6900,   6900,]
    # z_piezo = [    0,     0,     0,     0,     0,     0,     0,     0,     0,     0,      0,      0,      0,      0,      0,      0,]
    # x_hexa =  [    6,     6,     6,     6,     6,     6,     6,     6,     6,     0,      0,      0,      0,      0,      0,      0,]
    # incident_angles = [0.225457, 0.07311, 0.13644, 0.131744, 0.090663, 0.203624, 0.140589, 0.117837,
    # 0.066659, 0.060986, 0.083272, 0.055102, 0.472708, 0.080632, 0.063615]
    # y_piezo_aligned = [6674.616, 6664.133, 6655.723, 6652.42, 6628.407, 6619.978, 6615.386, 6607.622, 6604.918, 6625.53,
    # 6612.155, 6594.748, 6568.487, 6559.445, 6552.764, 6552.231]

    # names = ['FY32', 'FY33','FY34','FY35','FY36','DVC1', 'DVC2','DVC3','DVC4','DVC5','DVC6', 'DVC7',
    #     'FY17','FY18','FY19', 'FY20','FY21','FY22','FY23','FY24', 'FY25','FY26','FY27','FY28','FY29','FY30','FY31']

    # x_piezo = [58000, 45000, 34000, 28000, 24000, 13000, 2000, -13000,-25000,-40000,-47000, -55000,
    #            58000, 45000, 31000, 25000, 19000, 13000,  5000, -1000, -8000, -7000,-14000, -27000, -44000, -55000, -60000]
    # y_piezo = [ 6900,  6900,  6900,  6900,  6900,  6900,  6900,  6900,  6900,  6900,  6900,   6900,
    #            -2200, -2200, -2200, -2200, -2200, -2200, -2200, -2200, -2200, -2200, -2200,  -2200,  -2200,  -2200,  -2200]
    # z_piezo = [    0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,      0,
    #                0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,      0,      0,      0,      0]
    # x_hexa =  [    6,      6,    6,     6,     6,     6,     6,     6,     6,     6,     0,     -5,
    #                6,      6,    6,     6,     6,     6,     6,     6,     6,     0,     0,      0,     0,      0,      -5]

    # names = ['FY16', 'FY37','FY38','FY39','FY40', 'FY41', 'FY42','FY43','FY44','FY45', 'FY46','FY47','FY48', 'FY49','FY50',
    # 'FY51','FY52','FY53', 'FY54','FY55','FY56','FY57','FY58','FY59','FY60', 'FY61','FY62','FY63','FY64','FY65','FY66', 'FY67','FY68','FY69', 'DVC8']

    # x_piezo = [60000, 51000, 43000, 35500, 30500, 23000, 17500, 13200,  7000,  2000, -4000, -15000, -21500, -23000, -29000, -35000, -41000, -48000, -54000,
    #            60000, 48000, 35500, 29500, 25000, 21500, 17500, 13200,  8000, -6000,-15000, -17500, -29000, -38000, -48000, -56000]
    # y_piezo = [ 6900,  6900,  6900,  6900,  6900,  6900,  6900,  6900,  6900,  6900,  6900,   6900,   6900,   6900,   6900,   6900,   6900,   6900,   6900,
    #            -2200, -2200, -2200, -2200, -2200, -2200, -2200, -2200, -2200, -2200, -2200,  -2200,  -2200,  -2200,  -2200,  -2200]
    # z_piezo = [    0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,      0,      0,      0,      0,      0,      0,      0,      0,
    #                0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,      0,      0,      0,      0,      0]
    # x_hexa =  [    7,     7,     7,     7,     7,     7,     7,     7,     7,     7,     7,      7,      7,      0,      0,      0,      0,      0,      0,
    #                7,     7,     7,     7,     7,     7,     7,     7,     7,     7,     7,      0,     0,       0,      0,     -5]

    names = [
        "DVC9",
        "DVC10",
        "DVC11",
        "DVC12",
        "DVC13",
        "DVC14",
        "DVC15",
        "DVC16",
        "DVC17",
        "DVC18",
        "WEE1",
        "WEE2",
        "WEE3",
        "WEE4",
        "WEE5",
        "WEE6",
    ]

    x_piezo = [
        58000,
        43000,
        29000,
        15000,
        1000,
        -11000,
        -18000,
        -32000,
        -46000,
        -58000,
        58000,
        43000,
        29000,
        15000,
        1000,
        -11000,
    ]
    y_piezo = [
        6200,
        6200,
        6200,
        6200,
        6200,
        6200,
        6200,
        6200,
        6200,
        6200,
        -2900,
        -2900,
        -2900,
        -2900,
        -2900,
        -2900,
    ]
    z_piezo = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    x_hexa = [7, 7, 7, 7, 7, 7, 0, 0, 0, -4, 7, 7, 7, 7, 7, 7]

    incident_angles = []
    y_piezo_aligned = []

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

    smi = SMI_Beamline()
    yield from smi.modeAlignment(technique="gisaxs")

    for name, xs_piezo, zs_piezo, ys_piezo, xs_hexa in zip(
        names, x_piezo, z_piezo, y_piezo, x_hexa
    ):
        yield from bps.mv(stage.x, xs_hexa)
        yield from bps.mv(piezo.x, xs_piezo)
        yield from bps.mv(piezo.y, ys_piezo)
        yield from bps.mv(piezo.z, zs_piezo)
        yield from bps.mv(piezo.th, 0)

        # if ys_piezo>0:
        yield from alignement_gisaxs_multisample(angle=0.08)
        # else:
        #     yield from bps.mv(piezo.th, -1)
        #     yield from alignement_gisaxs_multisample_special(angle = 0.08)

        incident_angles = incident_angles + [piezo.th.position]
        y_piezo_aligned = y_piezo_aligned + [piezo.y.position]

    yield from smi.modeMeasurement()

    waxs_arc = np.linspace(0, 58.5, 10)
    angle = [0.1, 0.15, 0.2]

    dets = [pil1M, pil300KW]
    det_exposure_time(t, t)

    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)

        for name, xs, zs, aiss, ys, xs_hexa in zip(
            names, x_piezo, z_piezo, incident_angles, y_piezo_aligned, x_hexa
        ):
            yield from bps.mv(stage.x, xs_hexa)
            yield from bps.mv(piezo.x, xs)
            yield from bps.mv(piezo.y, ys)
            yield from bps.mv(piezo.z, zs)
            yield from bps.mv(piezo.th, aiss)

            for an in angle:
                yield from bps.mv(piezo.th, aiss + an)
                name_fmt = "{sample}_sdd5m_14keV_ai{angl}deg_wa{waxs}"
                sample_name = name_fmt.format(
                    sample=name, angl="%3.2f" % an, waxs="%2.1f" % wa
                )
                sample_id(user_name="PT", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")

                yield from bp.count(dets, num=1)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.1, 0.1)


def capillaries_saxs_Thed_2021_3(t=1):
    # samples = ['LT1',  'LT2',  'LT3',  'LT4',  'LT5',  'LT6',  'LT7',  'LT8',  'LT9', 'LT10', 'LT11', 'LT12', 'LT13', 'LT14',
    #           'LT15', 'LT16', 'LT17', 'LT18', 'LT19', 'LT20', 'LT21', 'LT22', 'LT23', 'LT24', 'LT25', 'LT26', 'LT27']

    # x_list = [ 45700,  39300,  33050,  26800,  20500,  13800,   7450,   1200,  -5200, -11800, -18000, -24200, -30850, -36900,
    #            42800,  36350,  29650,  23700,  16900,  10600,   4600,  -2150,  -8450, -14850, -21150, -27600, -33450]
    # y_list = [  2000,   2000,   2000,   2000,   2000,   2000,   2000,   2000,   2000,   2000,   2000,   2000,   2000,   2000,
    #             2000,   2000,   2000,   2000,   2000,   2000,   2000,   2000,   2000,   2000,   2000,   2000,   2000]
    # z_list = [  4000,   4000,   4000,   4000,   4000,   4000,   4000,   4000,   4000,   4000,   4000,   4000,   4000,   4000,
    #            -5000,  -5000,  -5000,  -5000,  -5000,  -5000,  -5000,  -5000,  -5000,  -5000,  -5000,  -5000,  -5000]

    samples = [
        "FY2",
        "FY4",
        "FY6",
        "FY8",
        "FY9",
        "FY10",
        "FY11",
        "FY12",
        "FY13",
        "FY14",
        "FY15",
        "FY16",
        "FY17",
        "FY18",
        "FY19",
        "FY20",
        "FY25",
        "FY26",
        "FY27",
        "FY28",
        "FY29",
        "FY30",
        "FY31",
        "FY32",
        "FY33",
        "FY34",
        "FY35",
        "FY25_abovecloud",
    ]
    x_list = [
        45800,
        39300,
        32950,
        26500,
        20300,
        13900,
        7250,
        1250,
        -5300,
        -11850,
        -18100,
        -24450,
        -30800,
        -37100,
        42650,
        36200,
        29900,
        23650,
        17300,
        10900,
        4200,
        -1950,
        -8450,
        -14850,
        -21100,
        -27600,
        -33700,
        29900,
    ]
    y_list = [
        2000,
        2000,
        2000,
        2000,
        2000,
        2000,
        2000,
        2000,
        2000,
        2000,
        2000,
        2000,
        2000,
        2000,
        1900,
        2000,
        2000,
        2000,
        2000,
        2000,
        2000,
        2000,
        2000,
        2000,
        2000,
        2000,
        2000,
        0,
    ]
    z_list = [
        4000,
        4000,
        4000,
        4000,
        4000,
        4000,
        4000,
        4000,
        4000,
        4000,
        4000,
        4000,
        4000,
        4000,
        -6100,
        -6100,
        -6100,
        -6100,
        -6100,
        -6100,
        -6100,
        -6100,
        -6100,
        -6100,
        -6100,
        -6100,
        -6100,
        -6100,
    ]

    # Detectors, motors:
    dets = [pil1M]
    det_exposure_time(t, t)

    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    assert len(y_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    assert len(z_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"

    for x, y, z, sample in zip(x_list, y_list, z_list, samples):
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(piezo.y, y)
        yield from bps.mv(piezo.z, z)

        sample_id(user_name="PT_5.0m_14.0keV", sample_name=sample)
        yield from bp.count(dets, num=10)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.1, 0.1)


def capillaries_saxs_Thed_2021_1(t=1):
    # samples = ['L1', 'L2', 'L3', 'L4', 'L5', 'L6', 'L7', 'L8', 'L9', 'L10', 'L11', 'L12', 'L13', 'L14', 'L15', 'L16', 'L17', 'L18', 'L19', 'L20',
    # 'L21', 'L22', 'L23', 'L24', 'L25', 'L26']

    # x_list = [43000, 37100, 30300, 24300, 18000, 11300, 5000, -1550, -7950, -14200, -20500, -26900, -33300,
    #           40200, 33700, 27200, 20800, 14100,  8200, 1700, -4800,-11250, -17800, -24000, -29500, -36800]
    # y_list = [    0,     0,  1000,  1000,  1000,  1000, 1000,  1000,  1000,   1000,   1000,   1000,   1000,
    #            1000,  1000,  1000,  1000,  1000,  1000, 1000,  1000,  1000,   1000,   1000,   1000,   1000]
    # z_list = [-8100, -8100, -8100, -8100, -8100, -8100,-8100, -8100, -8100,  -8100,  -8100,  -8100,  -8100,
    #            1500,  1500,  1500,  1500,  1500,  1500, 1500,  1500,  1500,   1500,   1500,   1500,   1500]

    samples = ["L27", "L28", "L29", "L30", "L31", "L32", "L33", "L35", "L36"]
    x_list = [37000, 30850, 23900, 17600, 11350, 5000, -1500, -7400, -13800]
    y_list = [0, 0, 1000, 1000, 1000, 1000, 1000, 1000, 1000]
    z_list = [-8100, -8100, -8100, -8100, -8100, -8100, -8100, -8100, -8100]

    # Detectors, motors:
    dets = [pil1M]  # dets = [pil1M,pil300KW]
    det_exposure_time(t, t)

    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    assert len(y_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    assert len(z_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"

    for x, y, z, sample in zip(x_list, y_list, z_list, samples):
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(piezo.y, y)
        yield from bps.mv(piezo.z, z)

        sample_id(user_name="PT_5.0m_16.1keV", sample_name=sample)
        yield from bp.count(dets, num=10)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.1, 0.1)


def gisaxs_Thed2(t=1):
    samples = ["FY1", "FY2", "FY3", "FY4"]

    x_list = [-41470, -22470, 2530, 27530]

    waxs_arc = np.linspace(13, 13, 1)
    angle = [0.1, 0.15, 0.2]

    # Detectors, motors:
    dets = [pil1M]
    det_exposure_time(t, t)

    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"

    for x, sample in zip(x_list, samples):
        yield from bps.mv(piezo.x, x)
        sample_id(user_name="PT_gisaxs", sample_name=sample)

        yield from alignement_gisaxs(0.08)

        det_exposure_time(t, t)
        name_fmt = "{sample}_ai{angle}deg_wa{waxs}"
        for j, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)

            for an in angle:
                yield from bps.mvr(piezo.th, an)
                sample_name = name_fmt.format(
                    sample=sample, angle="%3.2f" % an, waxs="%2.1f" % wa
                )
                sample_id(user_name="PT", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")

                yield from bp.count(dets, num=2)
                yield from bps.mvr(piezo.th, -an)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.1, 0.1)


def gisaxs_Thed_2021_2(t=1):
    # samples = ['FY1', 'FY2', 'FY3', 'FY4', 'FY5', 'FY6', 'FY7', 'FY8', 'FY9', 'FY10', 'FY11', 'FY12', 'FY13', 'FY14', 'FY15', 'FY16', 'FY17', 'FY18', 'FY19',
    # 'FY20', 'FY23', 'FY24', 'FY25', 'FY26', 'FY27', 'FY28', 'FY29', 'FY30', 'FY31', 'FY32', 'FY33']

    # x_list = [58000, 53000, 48000, 42000, 49000, 41000, 35000, 31000, 26000, 22000, 18000, 13500, 10000, 5000, 1000, -2500, -6000, -10000, -15000, -20000,
    # -24000, -29000, -34000,-38000,-43000,-48000,-41000,-46000,-50000,-54000,-57000]
    # x_hexa = [   13,    13,    13,    13,     0,     0,     0,     0,     0,     0,     0,     0,     0,    0,    0,     0,     0,      0,      0,      0,
    #      0,       0,     0,     0,     0,     0,   -12,   -12,   -12,   -12,   -12]

    # samples = ['FY2', 'FY3', 'FY4', 'FY5', 'FY6', 'FY7', 'FY8', 'FY9', 'FY10', 'FY11', 'FY12', 'FY13', 'FY14', 'FY15', 'FY16', 'FY17', 'FY18', 'FY19',
    # 'FY20', 'FY23', 'FY24', 'FY25', 'FY26', 'FY27', 'FY28', 'FY29', 'FY30', 'FY31', 'FY32', 'FY33']

    # x_list = [53000, 48000, 42000, 49000, 41000, 35000, 31000, 26000, 22000, 18000, 13500, 10000, 5000, 1000, -2500, -6000, -10000, -15000, -20000,
    # -24000, -29000, -34000,-38000,-43000,-48000,-41000,-46000,-50000,-54000,-57000]
    # x_hexa = [   13,    13,    13,     0,     0,     0,     0,     0,     0,     0,     0,     0,    0,    0,     0,     0,      0,      0,      0,
    #      0,       0,     0,     0,     0,     0,   -12,   -12,   -12,   -12,   -12]

    samples = [
        "FY38",
        "FY39",
        "FY40",
        "FY41",
        "FY42",
        "FY43",
        "FY44",
        "FY45",
        "FY46",
        "FY47",
        "FY48",
        "FY49",
        "FY50",
    ]

    x_list = [
        30000,
        24000,
        20000,
        15000,
        11500,
        6000,
        1500,
        -3000,
        -9000,
        -16000,
        -21000,
        -26000,
        -34000,
    ]
    x_hexa = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    waxs_arc = np.linspace(0, 45.5, 8)
    angle = [0.1, 0.15]

    # Detectors, motors:
    dets = [pil1M, pil300KW]
    det_exposure_time(t, t)

    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    assert len(x_list) == len(
        x_hexa
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(x_hexa)})"

    for x, sample, x_hex in zip(x_list, samples, x_hexa):
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(stage.x, x_hex)

        sample_id(user_name="PT", sample_name=sample)

        yield from alignement_gisaxs(0.08)

        ai0 = piezo.th.position

        det_exposure_time(t, t)
        name_fmt = "{sample}_8.3m_16.1keV_ai{angle}deg_wa{waxs}"
        for j, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)

            for an in angle:
                yield from bps.mv(piezo.th, ai0 + an)
                yield from bps.sleep(1)
                sample_name = name_fmt.format(
                    sample=sample, angle="%3.2f" % an, waxs="%2.1f" % wa
                )
                sample_id(user_name="PT", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")

                yield from bp.count(dets, num=1)

        yield from bps.mv(piezo.th, ai0)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.1, 0.1)


def gisaxs_Thed_2021_3(t=1):

    #     samples = ['FY37', 'FY38', 'FY39', 'FY40']
    #     x_list = [  57000,  57000,  55000,  45000]
    #     x_hexa = [     13,      7,      0,      0]

    #     waxs_arc = [2, 22, 42]
    #     angle = np.linspace(0.05, 0.2, 16)

    #   # Detectors, motors:
    #     dets = [pil1M, pil900KW]
    #     det_exposure_time(t,t)

    #     assert len(x_list) == len(samples), f'Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})'
    #     assert len(x_list) == len(x_hexa), f'Number of X coordinates ({len(x_list)}) is different from number of samples ({len(x_hexa)})'

    #     for x, sample, x_hex in zip(x_list,samples, x_hexa):
    #         yield from bps.mv(piezo.x, x)
    #         yield from bps.mv(stage.x, x_hex)

    #         sample_id(user_name='PT', sample_name=sample)

    #         yield from alignement_gisaxs(0.08)
    #         yield from bps.mv(att1_5.open_cmd, 1)

    #         ai0 = piezo.th.position

    #         det_exposure_time(t, t)
    #         name_fmt = '{sample}_8.3m_16.1keV_ai{angle}deg_wa{waxs}'
    #         for j, wa in enumerate(waxs_arc):
    #             yield from bps.mv(waxs, wa)

    #             for an in angle:
    #                 yield from bps.mv(piezo.th, ai0+an)
    #                 yield from bps.sleep(1)
    #                 sample_name = name_fmt.format(sample=sample, angle='%3.2f'%an, waxs='%2.1f'%wa)
    #                 sample_id(user_name='PT', sample_name=sample_name)
    #                 print(f'\n\t=== Sample: {sample_name} ===\n')

    #                 yield from bp.count(dets, num=1)

    #         yield from bps.mv(piezo.th, ai0)

    #     sample_id(user_name='test', sample_name='test')
    #     det_exposure_time(0.1,0.1)

    # samples = ['FY41', 'FY42', 'FY43', 'FY44', 'FY45']
    # x_list = [  35000,  25000,  17000,   9000, - 1000]
    # x_hexa = [      0,      0,      0,      0,      0]
    samples = ["DVC1751A", "DVC1751B", "DVC1751C", "DVC1752A", "DVC1752B", "DVC1752C"]
    x_list = [-3000, -16000, -32000, -43000, -57000, -58000]
    x_hexa = [0, 0, 0, 0, 0, -12]

    waxs_arc = [2, 22, 42]
    angle = [0.05, 0.10, 0.15]

    # Detectors, motors:
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    assert len(x_list) == len(
        x_hexa
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(x_hexa)})"

    for x, sample, x_hex in zip(x_list, samples, x_hexa):
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(stage.x, x_hex)

        sample_id(user_name="PT", sample_name=sample)

        yield from alignement_gisaxs(0.08)
        yield from bps.mv(att1_5.open_cmd, 1)

        ai0 = piezo.th.position

        det_exposure_time(t, t)
        name_fmt = "{sample}_8.3m_16.1keV_ai{angle}deg_wa{waxs}"
        for j, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)

            for an in angle:
                yield from bps.mv(piezo.th, ai0 + an)
                yield from bps.sleep(1)
                sample_name = name_fmt.format(
                    sample=sample, angle="%3.2f" % an, waxs="%2.1f" % wa
                )
                sample_id(user_name="PT", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")

                yield from bp.count(dets, num=1)

        yield from bps.mv(piezo.th, ai0)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.1, 0.1)

    # samples = ['FY46', 'FY47', 'FY48', 'FY49', 'FY50']
    # x_list = [ -11000, -24000, -37000, -50000, -53000]
    # x_hexa = [      0,      0,      0,      0,    -10]
    samples = ["FY51", "FY52", "FY53", "FY54", "FY55", "FY56", "FY57", "FY58"]
    x_list = [58000, 58000, 49500, 45500, 42000, 38000, 29000, 17000]
    x_hexa = [13, 0, 0, 0, 0, 0, 0, 0]

    waxs_arc = [40]
    angle = [0.05, 0.10, 0.15]

    # Detectors, motors:
    dets = [pil1M]
    det_exposure_time(t, t)

    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    assert len(x_list) == len(
        x_hexa
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(x_hexa)})"

    for x, sample, x_hex in zip(x_list, samples, x_hexa):
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(stage.x, x_hex)

        sample_id(user_name="PT", sample_name=sample)

        yield from alignement_gisaxs(0.08)
        # yield from bps.mv(att1_5.open_cmd, 1)

        ai0 = piezo.th.position

        det_exposure_time(t, t)
        name_fmt = "{sample}_8.3m_16.1keV_ai{angle}deg_wa{waxs}"
        for j, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)

            for an in angle:
                yield from bps.mv(piezo.th, ai0 + an)
                yield from bps.sleep(1)
                sample_name = name_fmt.format(
                    sample=sample, angle="%3.2f" % an, waxs="%2.1f" % wa
                )
                sample_id(user_name="PT", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")

                yield from bp.count(dets, num=1)

        yield from bps.mv(piezo.th, ai0)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.1, 0.1)


def gisaxs_2021_2(t=1):

    samples = ["FY40"]

    x_list = [20000]
    x_hexa = [0]

    waxs_arc = np.linspace(0, 45.5, 8)
    angle = [0.1, 0.15]

    # Detectors, motors:
    dets = [pil1M, pil300KW]
    det_exposure_time(t, t)

    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    assert len(x_list) == len(
        x_hexa
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(x_hexa)})"

    for x, sample, x_hex in zip(x_list, samples, x_hexa):
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(stage.x, x_hex)

        sample_id(user_name="PT", sample_name=sample)

        # yield from alignement_gisaxs(0.08)

        ai0 = piezo.th.position

        det_exposure_time(t, t)
        name_fmt = "{sample}_8.3m_16.1keV_ai{angle}deg_wa{waxs}"
        for j, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)

            for an in angle:
                yield from bps.mv(piezo.th, ai0 + an)
                yield from bps.sleep(1)
                sample_name = name_fmt.format(
                    sample=sample, angle="%3.2f" % an, waxs="%2.1f" % wa
                )
                sample_id(user_name="PT", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")

                yield from bp.count(dets, num=1)

        yield from bps.mv(piezo.th, ai0)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.1, 0.1)


def gisaxs_finestep_Thed_2021_2(t=1):

    samples = ["FY21", "FY22"]

    x_list = [58000, 58000]
    x_hexa = [14, 0]

    waxs_arc = np.linspace(0, 45.5, 8)
    angle = np.linspace(0.05, 0.2, 16)

    # Detectors, motors:
    dets = [pil1M, pil300KW]
    det_exposure_time(t, t)

    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    assert len(x_list) == len(
        x_hexa
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(x_hexa)})"

    for x, sample, x_hex in zip(x_list, samples, x_hexa):
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(stage.x, x_hex)

        sample_id(user_name="PT", sample_name=sample)

        yield from alignement_gisaxs(0.08)

        ai0 = piezo.th.position

        det_exposure_time(t, t)
        name_fmt = "{sample}_8.3m_16.1keV_ai{angle}deg_wa{waxs}"
        for j, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)

            for an in angle:
                yield from bps.mv(piezo.th, ai0 + an)
                yield from bps.sleep(2)
                sample_name = name_fmt.format(
                    sample=sample, angle="%3.2f" % an, waxs="%2.1f" % wa
                )
                sample_id(user_name="PT", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")

                yield from bp.count(dets, num=1)

        yield from bps.mv(piezo.th, ai0)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.1, 0.1)


def saxs_well_Thed(t=1):
    samples = [
        "PT10E_002AgB",
        "PT10E_002A",
        "PT10E_002B",
        "PT10E_002C",
        "PT10E_002D",
        "PT10E_002E",
        "PT10E_002F",
        "PT10E_002G",
        "PT10E_002H",
        "PT10E_002I",
        "PT10E_002J",
        "PT10E_002K",
        "PT10E_002L",
        "PT10E_002M",
        "PT10E_002N",
        "PT10E_002O",
        "PT10E_002P",
        "PT10E_002Q",
        "PT10E_002R",
        "PT10E_002S",
        "PT10E_002T",
        "PT10E_002U",
        "PT10E_002V",
        "PT10E_002W",
        "PT10E_003AgB",
        "PT10E_003A",
        "PT10E_003B",
        "PT10E_003C",
        "PT10E_003D",
        "PT10E_003F",
        "PT10E_003G",
        "PT10E_003H",
        "PT10E_003I",
        "PT10E_003J",
        "PT10E_003L",
        "PT10E_003M",
        "PT10E_003N",
        "PT10E_003O",
        "PT10E_003P",
        "PT10E_003R",
        "PT10E_003S",
        "PT10E_003T",
        "PT10E_003U",
        "PT10E_003V",
    ]

    x_list = [
        44360,
        35500,
        26640,
        17880,
        9030,
        230,
        44360,
        35500,
        26640,
        17880,
        9030,
        230,
        44360,
        35500,
        26640,
        17880,
        9030,
        230,
        44360,
        35500,
        26640,
        17880,
        9030,
        230,
        -8970,
        -17770,
        -26570,
        -35370,
        -44170,
        -8970,
        -17770,
        -26570,
        -35370,
        -44170,
        -8970,
        -17770,
        -26570,
        -35370,
        -44170,
        -8970,
        -17770,
        -26570,
        -35370,
        -44170,
    ]

    y_list = [
        -6640,
        -6640,
        -6640,
        -6640,
        -6640,
        -6640,
        -1400,
        -1400,
        -1400,
        -1400,
        -1400,
        -1400,
        3840,
        3840,
        3840,
        3840,
        3840,
        3840,
        9080,
        9080,
        9080,
        9080,
        9080,
        9080,
        -6640,
        -6640,
        -6640,
        -6640,
        -6640,
        -6640,
        -1400,
        -1400,
        -1400,
        -1400,
        -1400,
        -1400,
        3840,
        3840,
        3840,
        3840,
        3840,
        3840,
        9080,
        9080,
        9080,
        9080,
        9080,
        9080,
    ]

    waxs_arc = np.linspace(0, 58.5, 10)

    # Detectors, motors:
    dets = [pil1M, pil300KW]
    det_exposure_time(t, t)

    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"

    for j, wa in enumerate(waxs_arc):
        yield from bps.mv(waxs, wa)

        for x, y, sample in zip(x_list, y_list, samples):
            yield from bps.mv(piezo.x, x)
            yield from bps.mv(piezo.y, y)

            sample_id(user_name="PT", sample_name=sample)

            det_exposure_time(t, t)
            name_fmt = "{sample}_wa{waxs}"

            sample_name = name_fmt.format(sample=sample, waxs="%2.1f" % wa)
            sample_id(user_name="PT", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")

            yield from bp.count(dets, num=1)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.1, 0.1)


def saxs_well2_Thed(t=1):
    samples = [  #'PT10E_003E', 'PT10E_003K','PT10E_003Q', 'PT10E_003W',
        # 'PT10E_004AgB','PT10E_004A','PT10E_004B','PT10E_004C','PT10E_004D', 'PT10E_004E',
        # 'PT10E_004F','PT10E_004G','PT10E_004H','PT10E_004I','PT10E_004J','PT10E_004K',
        # 'PT10E_004L','PT10E_004M','PT10E_004N','PT10E_004O','PT10E_004P','PT10E_004Q',
        "PT10E_004R",
        "PT10E_004S",
        "PT10E_004T",
        "PT10E_004U",
        "PT10E_004V",
        "PT10E_004W",
    ]

    x_list = [  # 19030, 19030, 19030, 19030,
        # 2530, -6270, -15070, -23870, -32670, -41470,
        # 2530, -6270, -15070, -23870, -32670, -41470,
        # 2530, -6270, -15070, -23870, -32670, -41470,
        2530,
        -6270,
        -15070,
        -23870,
        -32670,
        -41470,
    ]

    y_list = [  # -7540, -2300, 2940, 8180,
        # -6640, -6640,-6640,-6640, -6640, -6640,
        # -1400, -1400,-1400,-1400, -1400, -1400,
        # 3840, 3840,3840,3840, 3840, 3840,
        9080,
        9080,
        9080,
        9080,
        9080,
        9080,
    ]

    waxs_arc = np.linspace(13, 13, 1)

    # Detectors, motors:
    dets = [pil1M, pil300KW]
    det_exposure_time(t, t)

    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"

    for j, wa in enumerate(waxs_arc):
        yield from bps.mv(waxs, wa)

        for x, y, sample in zip(x_list, y_list, samples):
            yield from bps.mv(piezo.x, x)
            yield from bps.mv(piezo.y, y)

            sample_id(user_name="PT", sample_name=sample)

            det_exposure_time(t, t)
            name_fmt = "{sample}_wa{waxs}"

            sample_name = name_fmt.format(sample=sample, waxs="%2.1f" % wa)
            sample_id(user_name="PT", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")

            yield from bp.count(dets, num=1)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.1, 0.1)


def run_saxsmapPT(t=1):
    samples = ["AS1-090", "AS1-100"]
    x_list = [12000, 33000]
    y_list = [1500, 1400]

    name = "PT"

    x_range = [[0, 15000, 61], [0, 12500, 51]]
    y_range = [[-5000, 5000, 41], [-3750, 3750, 16]]

    # Detectors, motors:
    dets = [pil1M]  # dets = [pil1M,pil300KW]
    det_exposure_time(t, t)

    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    for x, y, sample, x_r, y_r in zip(x_list, y_list, samples, x_range, y_range):
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(piezo.y, y)
        sample_id(user_name=name, sample_name=sample)

        for xrs in np.linspace(x_r[0], x_r[1], x_r[2]):
            yield from bps.mv(piezo.x, x + xrs)
            for yrs in np.linspace(y_r[0], y_r[1], y_r[2]):
                print(yrs)
                yield from bps.mv(piezo.y, y + yrs)
                name_fmt = "{sam}_x{x}_y{y}"
                sample_name = name_fmt.format(
                    sam=sample, x="%5.5d" % (x + xrs), y="%5.5d" % (y + yrs)
                )
                sample_id(user_name=name, sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                yield from bp.count(dets, num=1)

    # yield from bp.rel_grid_scan(dets, piezo.x, *x_r, piezo.y, *y_r, 0) #1 = snake, 0 = not-snake

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def run_waxslongPT(t=1):
    dets = [pil300KW, pil1M]
    xlocs = [-38000, -33000, -20000, -8000, 5000, 18000, 31000]
    ylocs = [-8400, 0, 0, 0, 0, 0, 0]
    names = [
        "Se_50nm",
        "Se_100nm",
        "Se_200nm",
        "Se_300nm",
        "Se_400nm",
        "Se_1000nm",
        "Se_2000nm",
    ]

    det_exposure_time(t, t)
    # what we run now
    assert len(curr_tray) == len(
        curr_names
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    waxs_range = [0, 58.5, 10]
    for x, y, name in zip(xlocs, ylocs, names):
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(piezo.y, y)
        sample_id(user_name="PT", sample_name=name)
        yield from bp.scan(dets, waxs, *waxs_range)

        sample_id(user_name="test", sample_name="test")
        det_exposure_time(0.3, 0.3)


def run_waxsshortPT(t=0.25):
    dets = [pil300KW, pil1M]
    xlocs = [
        -36000,
        -25000,
        -16000,
        -44000,
        -36500,
        -27000,
        -18000,
        -8000,
        0,
        9000,
        18500,
        27000,
        35500,
        45000,
        -8500,
    ]
    ylocs = [
        -8800,
        -8800,
        -8800,
        6500,
        6500,
        6000,
        6000,
        6000,
        6000,
        6000,
        6000,
        6000,
        6000,
        6500,
        7000,
        -8800,
    ]
    names = [
        "PT7E-012A",
        "PT5E-010A",
        "PT5E-010B",
        "PT5E-016D",
        "PT5E-016E",
        "GMB-018A",
        "GMB-018B",
        "GMB-019",
        "CC1-036A",
        "CC1-036B",
        "CC1-036C",
        "CC1-036D",
        "CC1-036E",
        "CC1-036F",
        "offsetSAXS_tape_blank",
    ]
    user = "PT"
    det_exposure_time(t, t)

    assert len(xlocs) == len(
        names
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"

    # Detectors, motors:
    dets = [pil1M, pil300KW]
    waxs_range = np.linspace(0, 58.5, 10)
    for wa in waxs_range:
        yield from bps.mv(waxs, wa)
        for sam, x, y in zip(names, xlocs, ylocs):
            yield from bps.mv(piezo.y, y)
            yield from bps.mv(piezo.x, x)
            name_fmt = "{sam}_wa{waxs}deg"
            sample_name = name_fmt.format(sam=sam, waxs="%2.1f" % wa)
            sample_id(user_name=user, sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def gisaxs_tempPT(t=1):
    # Slowest cycle:
    temperatures = [120]
    x_list = [-24500, -8500, 7500, 21500]
    y_list = [3354, 3246, 3068, 3700]
    samples = ["DVC_3MPA", "DVC_CystAm", "DVC_u1", "KRH_u1"]

    # Detectors, motors:
    # dets = [pil1M, rayonix, pil300KW,ls.ch1_read, xbpm3.sumY] #ALL detectors
    dets = [pil1M, pil300KW, ls.ch1_read, xbpm3.sumY]  # WAXS detector ALONE
    angle_offset = [0.1, 0.15]
    waxs_range = [0, 58.5, 10]
    waxs_range_rev = [58.5, 0, 10]
    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"

    for i_t, temps in enumerate(temperatures):
        yield from bps.mv(ls.ch1_sp, temps)
        # if i_t > 0:
        # yield from bps.sleep(300)
        for x, y, s in zip(x_list, y_list, samples):
            yield from bps.mv(piezo.x, x)
            yield from bps.mv(piezo.y, y)
            yield from alignement_gisaxs_shorter(0.1)
            ##yield from quickalign_gisaxs(0.1)
            plt.close("all")
            a_off = piezo.th.position
            for i, an in enumerate(angle_offset):
                yield from bps.mv(piezo.th, a_off + an)
                det_exposure_time(t, t)
                temp = ls.ch1_read.value
                name_fmt = "{sample}_{temper}C_{angl}deg"
                yield from bps.mv(piezo.x, x + i * 200)
                sample_name = name_fmt.format(sample=s, temper=temp, angl=an)
                sample_id(user_name="PT", sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                if i == 0:
                    yield from bp.scan(dets, waxs, *waxs_range)
                else:
                    yield from bp.scan(dets, waxs, *waxs_range_rev)
            yield from bps.mv(piezo.th, a_off)

        sample_id(user_name="test", sample_name="test")
        det_exposure_time(0.3, 0.3)


def gisaxs_PT(t=1):
    # Slowest cycle:

    x_list = [1500, -7500, -12500, -17500, -22500, -27000, -35000, -47000]
    samples = [
        "1wtSO1YonGA",
        "5wtSO1YonGA",
        "1wtSO1Yonbare",
        "5wtPS-PMMAonGA",
        "5wtSV129onGA",
        "1wtSO1Yon350C",
        "DVC48A",
        "DVC48E",
    ]

    # Detectors, motors:
    # dets = [pil1M, rayonix, pil300KW,ls.ch1_read, xbpm3.sumY] #ALL detectors
    dets = [pil1M]  # WAXS detector ALONE
    angle_offset = [0.1, 0.15, 0.2]
    waxs_range = [0, 58.5, 10]

    #    param   = '16.1keV'
    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"

    for x, s in zip(x_list, samples):
        yield from bps.mv(piezo.x, x)
        yield from alignement_gisaxs_shorter(0.1)
        # yield from quickalign_gisaxs(0.1)
        plt.close("all")
        a_off = piezo.th.position
        for i, an in enumerate(angle_offset):
            yield from bps.mv(piezo.th, a_off + an)
            det_exposure_time(t, t)
            name_fmt = "{sample}_{angl}deg"
            sample_name = name_fmt.format(sample=s, angl=an)
            sample_id(user_name="FY", sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)

        sample_id(user_name="test", sample_name="test")
        det_exposure_time(0.3, 0.3)


def run_swaxs_Fei_2022_3(t=1):
    """
    Take WAXS and SAXS at nine sample positions for averaging

    Specify central positions on the samples with xlocs and ylocs,
    then offsets from central positions with x_off and y_off. Run
    WAXS arc as the slowest motor.
    """

    # 1 sample row
    names_1   = [   'Q1',   'Q2',   'Q3',   'Q4',   'Q5',   'Q6']
    piezo_x_1 = [ -42800, -33800, -24800, -15800,  -6800,  2200]
    piezo_y_1 = [  -9600,  -9600,  -9600,  -9600,  -9600,  -9600] 

    # 2 sample row
    names_2   = [   'R1',   'R2',   'R3',   'R4',   'R5',   'R6']
    piezo_x_2 = [ -42800, -33800, -24800, -15800,  -6800,   1800]
    piezo_y_2 = [  -4300,  -4300,  -4300,  -4300,  -4300,  -4300]

    # 3 sample row
    names_3   = [   'S1',   'S2',   'S3',   'S4',   'S5',   'S6']
    piezo_x_3 = [ -42800, -33800, -24800, -15800,  -6800,   2000]
    piezo_y_3 = [   1100,   1100,   1100,   1100,   1100,   1100]

    # 4 sample row
    names_4   = [   'T1',   'T2',   'T3',   'T4',   'T5',   'T6']
    piezo_x_4 = [ -42800, -33800, -24800, -15800,  -6800,   2000]
    piezo_y_4 = [   6200,   6200,   6200,   6200,   6200,   6200]

    # Combine rows
    names   = names_1   + names_2   + names_3   + names_4
    piezo_x = piezo_x_1 + piezo_x_2 + piezo_x_3 + piezo_x_4
    piezo_y = piezo_y_1 + piezo_y_2 + piezo_y_3 + piezo_y_4

    # Offsets for taking a few points per sample
    x_off = [-300, 0, 300]
    y_off = [-300, 0, 300]

    waxs_arc = [40, 20, 0]
    user = "FY"
    

    # Check and correct sample names just in case
    names = [n.translate({ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ "}) for n in names]

    # Check if the length of xlocs, ylocs and names are the same
    assert len(piezo_x) == len(names), f"Number of X coordinates ({len(piezo_x)}) is different from number of samples ({len(names)})"
    assert len(piezo_x) == len(piezo_y), f"Number of X coordinates ({len(piezo_x)}) is different from number of samples ({len(piezo_y)})"

    for i, wa in enumerate(waxs_arc):
        yield from bps.mv(waxs, wa)
        # Detectors, disable SAXS when WAXS in the way
        dets = [pil900KW] if waxs.arc.position < 15 else [pil900KW, pil1M]
        det_exposure_time(t, t)

        for name, x, y, in zip(names, piezo_x, piezo_y):

            for yy, y_of in enumerate(y_off):
                yield from bps.mv(piezo.y, y + y_of)

                for xx, x_of in enumerate(x_off):
                    yield from bps.mv(piezo.x, x + x_of)

                    loc = f'{yy}{xx}'

                    # Metadata
                    e = energy.position.energy / 1000
                    wa = waxs.arc.position + 0.001
                    wa = str(np.round(float(wa), 1)).zfill(4)
                    sdd = pil1m_pos.z.position / 1000

                    # Sample name
                    name_fmt = ( "{sample}_{energy}keV_wa{wax}_sdd{sdd}m_loc{loc}")
                    sample_name = name_fmt.format(
                        sample=name,
                        energy="%.2f" % e,
                        wax=wa,
                        sdd="%.1f" % sdd,
                        loc=loc,
                    )
                    sample_id(user_name=user, sample_name=sample_name)
                    print(f"\n\n\n\t=== Sample: {sample_name} ===")
                    yield from bp.count(dets)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def run_swaxs_Fei_2023_1(t=1):
    """
    Take WAXS and SAXS at nine sample positions for averaging

    Specify central positions on the samples with xlocs and ylocs,
    then offsets from central positions with x_off and y_off. Run
    WAXS arc as the slowest motor. SAXS sdd 5.0 m.
    """

    # 1 sample row
    #names_1   = [ '1A1',  '1A2', '1A3', '1B1', '1B2', '1B3', '1C1',  '1C2',  '1C3',  '1D1',  '1D2',  '1D3']
    #piezo_x_1 = [ 46500,  38600, 29700, 22300, 13700,  5700, -2700, -10700, -18700, -26500, -34700, -42900]
    #piezo_y_1 = [ -8150,  -8150, -7750, -7850, -8350, -7850, -7950,  -7550,  -7550,  -7350,  -7250,  -7250] 

    # 2 sample row
    #names_2   = [ '2A1', '2A2', '2A3', '2B1', '2B2', '2B3', '2C1', '2C2',  '2C3',  '2D1',  '2D2',  '2D3'] 
    #piezo_x_2 = [ 47300, 39500, 31300, 23300, 15100,  6900, -1500, -9700, -17900, -26100, -34300, -42500]
    #piezo_y_2 = [  4250,  4550,  4750,  4750,  4650,  4650,  4650,  4950,   5050,   4950,   5150,   5350]

    names_1   = [   'U1',   'U2',   'U3',   'U4',  'U5',  'U6', 'V6',  'V5',   'V4',   'V3',   'V2',   'V1',   'W1',   'W2',   'W3',   'W4',  'W5', 'W6',]
    piezo_x_1 = [ -43100, -34100, -25300, -16300, -8100,  1500, 1300, -7500, -16100, -25300, -34100, -43300, -43100, -34100, -25300, -16500, -7300, 1700,]
    piezo_y_1 = [  -8650,  -9050,  -9050,  -8850, -9050, -9200, 1350,  1350,   1350,   1550,   1550,   1750,   7150,   6950,   6550,   6550,  6500, 6350,]

    names_2   = [   'X1',   'X2',   'X3',   'X4',  'X5', 'X6',   'Y4',  'Y5',  'Y6', 'background',  'Z2',  'Z1',  'Y1',  'Y2',  'Y3'] 
    piezo_x_2 = [ -42900, -33900, -25200, -16200, -7200, 1900,  10900, 20100, 29100,        28900, 20100, 11100, 10700, 19900, 28700]
    piezo_y_2 = [   7200,   7200,   6800,   6800,  6600, 6400,   1400,  1200,   800,        -4400, -4200, -4200, -9000, -9200, -9500]

    # Combine rows
    names   = names_1   + names_2
    piezo_x = piezo_x_1 + piezo_x_2
    piezo_y = piezo_y_1 + piezo_y_2

    # Offsets for taking a few points per sample
    x_off = [-400, 0, 400]
    y_off = [-400, 0, 400]

    waxs_arc = [40, 20, 0]
    user = "FY"
    

    # Check and correct sample names just in case
    names = [n.translate({ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ "}) for n in names]

    # Check if the length of xlocs, ylocs and names are the same
    assert len(piezo_x) == len(names), f"Number of X coordinates ({len(piezo_x)}) is different from number of samples ({len(names)})"
    assert len(piezo_x) == len(piezo_y), f"Number of X coordinates ({len(piezo_x)}) is different from number of samples ({len(piezo_y)})"

    for i, wa in enumerate(waxs_arc):
        yield from bps.mv(waxs, wa)
        # Detectors, disable SAXS when WAXS in the way
        dets = [pil900KW] if waxs.arc.position < 15 else [pil900KW, pil1M]
        det_exposure_time(t, t)

        for name, x, y, in zip(names, piezo_x, piezo_y):

            for yy, y_of in enumerate(y_off):
                yield from bps.mv(piezo.y, y + y_of)

                for xx, x_of in enumerate(x_off):
                    yield from bps.mv(piezo.x, x + x_of)

                    loc = f'{yy}{xx}'

                    # Metadata
                    e = energy.position.energy / 1000
                    wa = waxs.arc.position + 0.001
                    wa = str(np.round(float(wa), 1)).zfill(4)
                    sdd = pil1m_pos.z.position / 1000

                    # Sample name
                    name_fmt = ( "{sample}_{energy}keV_wa{wax}_sdd{sdd}m_loc{loc}")
                    sample_name = name_fmt.format(
                        sample=name,
                        energy="%.2f" % e,
                        wax=wa,
                        sdd="%.1f" % sdd,
                        loc=loc,
                    )
                    sample_id(user_name=user, sample_name=sample_name)
                    print(f"\n\n\n\t=== Sample: {sample_name} ===")
                    yield from bp.count(dets)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)





def run_swaxs_Fei_2023_2(t=1):
    """
    Take WAXS and SAXS at nine sample positions for averaging

    Specify central positions on the samples with xlocs and ylocs,
    then offsets from central positions with x_off and y_off. Run
    WAXS arc as the slowest motor. SAXS sdd 5.0 m.
    """

    # names_1   = [   'A6',   'A5',   'A4',   'A3',   'A2',   'A1',   'B1',   'B2',   'B3',   'B4',   'B5',   'B6',   'C6',   'C5',   'C4',   
    #                 'C3',   'C2',   'C1',   'D1',   'D2',   'D3',   'D4',   'D5',   'D6']
    # piezo_x_1 = [  60600,  50500,  42000,  33500,  24500,  16000,  15500,  24500,  33500,  42500,   51000,  60500,  60500,  51000,  42500, 
    #                33500,  24500,  15500,  15800,  24800,  33800,  42500,  51000,  60500]
    # piezo_y_1 = [  -7700,  -6900,  -7300,  -7300,  -7300,  -6600,  -1800,  -1800,  -2100,  -2100,   -2100,  -2100,   2900,   3100,   3100,   
    #                 3100,  3100,    3600,   7100,   7100,   6800,   6800,   6800,   6800]
    # hexa_y_1 =  [  -1.675, -1.675, -1.675, -1.675, -1.675, -1.675, -1.675, -1.675, -1.675, -1.675, -1.675, -1.675, -1.675, -1.675, -1.675,
    #               -1.675, -1.675, -1.675,      0,      0,      0,      0,      0,      0]
    

    # names_2   = [   'E1',   'E2',   'E3',   'E4',   'E5',   'E6',   'F6',   'F5',   'F4',   'F3',   'F2',   'F1',   'G1',   'G2',   'G3',   
    #                 'G4',   'G5',   'G6',   'H6',   'H5',   'H4',   'H3',   'H2',   'H1']
    # piezo_x_2 = [ -38500, -30000, -20800, -11800,  -2800,   5800,   5900,  -3100, -12100, -21100, -29100,  -38800, -38500,-29500, -20500, 
    #               -11500,  -3000,   5500,   5500,  -3000, -12000, -21000, -30000, -39000]
    # piezo_y_2 = [  -8000,  -8000,  -8000,  -8000,  -8000,  -8000,  -2800,  -2800,  -2800,  -2800,  -2800,   -3100,   2400,  2400,   2400, 
    #                 2400,   2400,   2400,   7500,   7500,   7500,   7500,   7500,   7500]
    # hexa_y_2 =  [      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,       0,       0,    0,      0,
    #                    0,      0,      0,      0,      0,      0,      0,      0,      0]
    
    # names_1   = [   'I1',   'I2',   'I3',   'I4',   'I5',   'I6',   'J6',   'J5',   'J4',   'J3',   'J2',   'J1',   'K1',   'K2',   'K3',   
    #                 'K4',   'K5',   'K6',   'L6',   'L5',   'L4',   'L3',   'L2',   'L1']
    # piezo_x_1 = [  60600,  51000,  42500,  33500,  24500,  16000,  15500,  24500,  33500,  42500,   51000,  60500,  60500,  51000,  42500, 
    #                33500,  24500,  15500,  15500,  24800,  33800,  42500,  51000,  60500]
    # piezo_y_1 = [  -8500,  -7900,  -7900,  -7900,  -7900,  -6900,  -2800,  -3100,  -3100,  -3100,   -3100,  -3100,   1900,   1900,   1900,   
    #                 2200,   2200,   2200,   7400,   7400,   7400,   7400,   7400,   7400]
    # hexa_y_1 =  [      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,       0,       0,    0,      0,
    #                    0,      0,      0,      0,      0,      0,      0,      0,      0]

    # names_2   = [   'U6',   'U5',   'U4',   'U3',   'U2',   'U1',   'V1',   'V2',   'V3',   'V4',   'V5',   'V6',   'W6',   'W5',   'W4',   
    #                 'W3',   'W2',   'W1',   'X1',   'X2',   'X3',   'X4',   'X5',   'X6']
    # piezo_x_2 = [ -38500, -29500, -20800, -11800,  -2800,   6200,   6200,  -3100, -11500, -20500, -29100,  -38100, -38100,-29500, -20900, 
    #               -11900,  -2900,   6300,   6300,  -2700, -11400, -20400, -29400, -38400]
    # piezo_y_2 = [  -8000,  -8400,  -8400,  -8400,  -8800,  -8800,  -4000,  -4000,  -4000,  -4000,  -3500,   -3500,   2000,  2000,   2000, 
    #                 2000,   1500,   1500,   6300,   6300,   6300,   7400,   7400,   7400]
    # hexa_y_2 =  [      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,       0,       0,    0,      0,
    #                    0,      0,      0,      0,      0,      0,      0,      0,      0]

    names_1   = [ 'smA1', 'smA2', 'smA3', 'smA4', 'smA5', 'smB5', 'smB4', 'smB3', 'smB2', 'smB1', 'smC1', 'smC2', 'smC3', 'smC4', 'smC5']
    piezo_x_1 = [  49500,  44500,  39500,  34500,  29500,  29500,  34500,  39200,  44200,  49200,  49000,  44000,  39000,  34000,  29000]
    piezo_y_1 = [  -4300,  -4300,  -4700,  -4700,  -4700,   -100,   -100,   -300,    500,    500,   5800,   5800,   5800,   5200,   5200]
    hexa_y_1 =  [      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0]

    # # Combine rows
    # names   = names_1   + names_2
    # piezo_x = piezo_x_1 + piezo_x_2
    # piezo_y = piezo_y_1 + piezo_y_2
    # hexa_y  = hexa_y_1  + hexa_y_2


    # Combine rows
    names   = names_1   
    piezo_x = piezo_x_1 
    piezo_y = piezo_y_1 
    hexa_y  = hexa_y_1 

    # Offsets for taking a few points per sample
    x_off = [-400, 0, 400]
    y_off = [-400, 0, 400]

    waxs_arc = [40, 20, 0]
    user = "FY"
    

    # Check and correct sample names just in case
    names = [n.translate({ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ "}) for n in names]

    # Check if the length of xlocs, ylocs and names are the same
    assert len(piezo_x) == len(names), f"Number of X coordinates ({len(piezo_x)}) is different from number of samples ({len(names)})"
    assert len(piezo_x) == len(piezo_y), f"Number of X coordinates ({len(piezo_x)}) is different from number of samples ({len(piezo_y)})"
    assert len(piezo_x) == len(hexa_y), f"Number of X coordinates ({len(piezo_x)}) is different from number of samples ({len(hexa_y)})"

    for i, wa in enumerate(waxs_arc):
        yield from bps.mv(waxs, wa)
        # Detectors, disable SAXS when WAXS in the way
        dets = [pil900KW] if waxs.arc.position < 15 else [pil900KW, pil1M]
        det_exposure_time(t, t)

        for name, x, y, y_hexa in zip(names, piezo_x, piezo_y, hexa_y):

            yield from bps.mv(stage.y, y_hexa)

            for yy, y_of in enumerate(y_off):
                yield from bps.mv(piezo.y, y + y_of)

                for xx, x_of in enumerate(x_off):
                    yield from bps.mv(piezo.x, x + x_of)

                    loc = f'{yy}{xx}'

                    # Metadata
                    e = energy.position.energy / 1000
                    wa = waxs.arc.position + 0.001
                    wa = str(np.round(float(wa), 1)).zfill(4)
                    sdd = pil1m_pos.z.position / 1000

                    # Sample name
                    name_fmt = ( "{sample}_{energy}keV_wa{wax}_sdd{sdd}m_loc{loc}")
                    sample_name = name_fmt.format(
                        sample=name,
                        energy="%.2f" % e,
                        wax=wa,
                        sdd="%.1f" % sdd,
                        loc=loc,
                    )
                    sample_id(user_name=user, sample_name=sample_name)
                    print(f"\n\n\n\t=== Sample: {sample_name} ===")
                    yield from bp.count(dets)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def run_swaxs_Fei_2023_3(t=1):
    """
    Take WAXS and SAXS at nine sample positions for averaging

    Specify central positions on the samples with xlocs and ylocs,
    then offsets from central positions with x_off and y_off. Run
    WAXS arc as the slowest motor. SAXS sdd 5.0 m.
    """

    names_1   = [  'A1',  'B1',  'C1',  'D1',  'E1',  'A2',  'B2',  'C2',  'D2', '86AF', '86BF',  '86A',  '86B', 'AJDPI']
    piezo_x_1 = [ 39500, 34500, 30400, 24300, 19500, 38500, 34500, 29500, 24500,   5500,  -4000, -15000, -24000,  -32500]
    piezo_y_1 = [ -3300, -3300, -3700, -3400, -3400,  1600,  1600,  1600,  1600,  -3800,  -3800,  -2200,  -2200,   -4700]
    hexa_y_1 =  [     0,     0,     0,     0,     0,     0,     0,     0,     0,      0,      0,      0,      0,       0]

    names_1   = [ 'AJDPI']
    piezo_x_1 = [  -32500]
    piezo_y_1 = [   -4700]
    hexa_y_1 =  [       0]

    # Combine rows
    names   = names_1   
    piezo_x = piezo_x_1 
    piezo_y = piezo_y_1 
    hexa_y  = hexa_y_1 

    # Offsets for taking a few points per sample
    x_off = [-400, 0, 400]
    y_off = [-400, 0, 400]

    waxs_arc = [40, 20, 0]
    user = "FY"
    

    # Check and correct sample names just in case
    names = [n.translate({ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ "}) for n in names]

    # Check if the length of xlocs, ylocs and names are the same
    assert len(piezo_x) == len(names), f"Number of X coordinates ({len(piezo_x)}) is different from number of samples ({len(names)})"
    assert len(piezo_x) == len(piezo_y), f"Number of X coordinates ({len(piezo_x)}) is different from number of samples ({len(piezo_y)})"
    assert len(piezo_x) == len(hexa_y), f"Number of X coordinates ({len(piezo_x)}) is different from number of samples ({len(hexa_y)})"

    for i, wa in enumerate(waxs_arc):
        yield from bps.mv(waxs, wa)
        # Detectors, disable SAXS when WAXS in the way
        dets = [pil900KW] if waxs.arc.position < 15 else [pil900KW, pil1M]
        det_exposure_time(t, t)

        for name, x, y, y_hexa in zip(names, piezo_x, piezo_y, hexa_y):

            yield from bps.mv(stage.y, y_hexa)

            for yy, y_of in enumerate(y_off):
                yield from bps.mv(piezo.y, y + y_of)

                for xx, x_of in enumerate(x_off):
                    yield from bps.mv(piezo.x, x + x_of)

                    loc = f'{yy}{xx}'

                    # Metadata
                    e = energy.position.energy / 1000
                    wa = waxs.arc.position + 0.001
                    wa = str(np.round(float(wa), 1)).zfill(4)
                    sdd = pil1m_pos.z.position / 1000

                    # Sample name
                    name_fmt = ( "{sample}_{energy}keV_wa{wax}_sdd{sdd}m_loc{loc}")
                    sample_name = name_fmt.format(
                        sample=name,
                        energy="%.2f" % e,
                        wax=wa,
                        sdd="%.1f" % sdd,
                        loc=loc,
                    )
                    sample_id(user_name=user, sample_name=sample_name)
                    print(f"\n\n\n\t=== Sample: {sample_name} ===")
                    yield from bp.count(dets)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)




def run_swaxs_Fei_2024_1(t=1):
    """
    Take WAXS and SAXS at nine sample positions for averaging

    Specify central positions on the samples with xlocs and ylocs,
    then offsets from central positions with x_off and y_off. Run
    WAXS arc as the slowest motor. SAXS sdd 4.0 m.
    """

    names   = [  'A1',  'A2',  'A3',  'A4',  'A5',  'A6',  'B1',  'B2',  'B3',  'B4',  'B5',  'B6',  'C1',  'C2',  'C3',  'C4',  'C5',  'C6',  'D1',  'D2',  'D3',  'D4',  'D5',  'D6',
                 'E1',  'E2',  'E3',  'E4',  'E5',  'E6',  'F1',  'F2',  'F3',  'F4',  'F5',  'F6',  'G1',  'G2',  'G3',  'G4',  'G5',  'G6',  'H1',  'H2',  'H3',  'H4',  'H5',  'H6']
    piezo_x = [ 56500, 46500, 37700, 28700, 20500, 11500, 56700, 47000, 38500, 29500, 20500, 11500, 56700, 47000, 38000, 29000, 20500, 11500, 56500, 47000, 38500, 29500, 20500, 11500, 
                 1800, -7200,-16200,-25200,-34000,-42500,  2000, -7000,-16000,-25000,-34000,-43000,  2000, -7000,-16000,-25000,-34000,-43000,  2000, -7000,-15500,-24500,-33500,-43300]
    piezo_y = [ -7200, -7200, -7200, -7200, -7200, -7000, -2200, -2200, -2200, -2200, -2200, -2000,  2800,  2800,  2800,  2800,  2800,  3500,  8500,  8500,  8500,  8500,  8500,  8500,
                -6800, -6800, -6800, -6800, -6800, -6700, -1500, -1500, -1500, -1500, -1500, -1500,  3500,  3500,  3500,  3500,  3500,  4000, 9800,  9300,  8500,  9600, 10000,  9800]
    hexa_y =  [     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
                    0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0]

    # Offsets for taking a few points per sample
    x_off = [-400, 0, 400]
    y_off = [-400, 0, 400]

    waxs_arc = [40, 20, 0]
    user = "FY"

    # Check and correct sample names just in case
    names = [n.translate({ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ "}) for n in names]

    # Check if the length of xlocs, ylocs and names are the same
    assert len(piezo_x) == len(names), f"Number of X coordinates ({len(piezo_x)}) is different from number of samples ({len(names)})"
    assert len(piezo_x) == len(piezo_y), f"Number of X coordinates ({len(piezo_x)}) is different from number of samples ({len(piezo_y)})"
    assert len(piezo_x) == len(hexa_y), f"Number of X coordinates ({len(piezo_x)}) is different from number of samples ({len(hexa_y)})"

    for i, wa in enumerate(waxs_arc):
        yield from bps.mv(waxs, wa)
        # Detectors, disable SAXS when WAXS in the way
        dets = [pil900KW] if waxs.arc.position < 15 else [pil900KW, pil1M]
        det_exposure_time(t, t)

        for name, x, y, y_hexa in zip(names, piezo_x, piezo_y, hexa_y):

            yield from bps.mv(stage.y, y_hexa)

            for yy, y_of in enumerate(y_off):
                yield from bps.mv(piezo.y, y + y_of)

                for xx, x_of in enumerate(x_off):
                    yield from bps.mv(piezo.x, x + x_of)

                    loc = f'{yy}{xx}'
                    sample_name = f'{name}{get_scan_md()}_loc{loc}'
                    sample_id(user_name='FY', sample_name=sample_name)

                    sample_id(user_name=user, sample_name=sample_name)
                    print(f"\n\n\n\t=== Sample: {sample_name} ===")
                    yield from bp.count(dets)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def run_swaxs_Feicap_2024_1(t=1):
    """
    Take WAXS and SAXS at nine sample positions for averaging

    Specify central positions on the samples with xlocs and ylocs,
    then offsets from central positions with x_off and y_off. Run
    WAXS arc as the slowest motor. SAXS sdd 4.0 m.
    """

    names   = [ 'C01', 'C04', 'C03', 'C05', 'C07', 'C08', 'C09', 'C10', 'C11', 'C12', 'C13', 'C15', 'C17', 'C18']
    piezo_x = [ 45000, 38900, 32000, 26100, 19400, 12900,  7700,   700, -6300,-12700,-18700,-25400,-31000,-37100]
    piezo_y = [  1500,  1500,  1500,  1500,  1500,  1500,  1500,  1500,  1500,  1500,  1500,  1500,  1500,  1500]

    # Offsets for taking a few points per sample
    x_off = [0]
    y_off = [-600, -400, -200, 0, 200, 400, 600]

    waxs_arc = [20]

    # Check and correct sample names just in case
    names = [n.translate({ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ "}) for n in names]

    user='LT'

    # Check if the length of xlocs, ylocs and names are the same
    assert len(piezo_x) == len(names), f"Number of X coordinates ({len(piezo_x)}) is different from number of samples ({len(names)})"
    assert len(piezo_x) == len(piezo_y), f"Number of X coordinates ({len(piezo_x)}) is different from number of samples ({len(piezo_y)})"

    for i, wa in enumerate(waxs_arc):
        yield from bps.mv(waxs, wa)
        # Detectors, disable SAXS when WAXS in the way
        dets = [pil1M]
        det_exposure_time(t, t)

        for name, x, y in zip(names, piezo_x, piezo_y):

            for yy, y_of in enumerate(y_off):
                yield from bps.mv(piezo.y, y + y_of)

                for xx, x_of in enumerate(x_off):
                    yield from bps.mv(piezo.x, x + x_of)

                    loc = f'{xx}{yy}'
                    sample_name = f'{name}{get_scan_md()}_loc{loc}'
                    sample_id(user_name=user, sample_name=sample_name)
                    print(f"\n\n\n\t=== Sample: {sample_name} ===")
                    yield from bp.count(dets)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def run_Fei_manualcap_2024_1(t=1, name='test'):
    """
    Take WAXS and SAXS at nine sample positions for averaging

    Specify central positions on the samples with xlocs and ylocs,
    then offsets from central positions with x_off and y_off. Run
    WAXS arc as the slowest motor. SAXS sdd 4.0 m.
    """

    # Offsets for taking a few points per sample
    y_off = [-600, -400, -200, 0, 200, 400, 600]

    waxs_arc = [20]

    # Check and correct sample names just in case
    user='LT'

    # Check if the length of xlocs, ylocs and names are the same
    for i, wa in enumerate(waxs_arc):
        yield from bps.mv(waxs, wa)
        # Detectors, disable SAXS when WAXS in the way
        dets = [pil1M]
        det_exposure_time(t, t)
        y=piezo.y.position

        for yy, y_of in enumerate(y_off):
            yield from bps.mv(piezo.y, y + y_of)
            loc = f'{yy}'
            sample_name = f'{name}{get_scan_md()}_loc{loc}'
            sample_id(user_name=user, sample_name=sample_name)
            print(f"\n\n\n\t=== Sample: {sample_name} ===")
            yield from bp.count(dets)
    
    yield from bps.mv(piezo.y, y)
    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)





def run_swaxs_Fei_2024_3(t=1):
    """
    Take WAXS and SAXS at nine sample positions for averaging

    Specify central positions on the samples with xlocs and ylocs,
    then offsets from central positions with x_off and y_off. Run
    WAXS arc as the slowest motor. SAXS sdd 4.0 m.
    """

    names   = ['195A','187K','195Ah','187Kh',
                 'A1',  'B1',   'C1',   'D1',  'E1',  'A2',  'B2',  'C2',  'D2',  'E2']
    piezo_x = [ 19500, 28300,  37300,  46000,
               -25100,-30100, -34900, -39900,-44600,-25100,-30000,-35000,-40000,-44200]
    piezo_y = [ -6500, -6500,  -6500,  -6500,
                -5300, -5300,  -5300,  -5600, -5300,   100,  -500,  -500,  -500,  -500]
    hexa_y =  [     0,     0,      0,      0,     
                    0,     0,      0,      0,     0,     0,     0,     0,     0,     0]

    # Offsets for taking a few points per sample
    x_off = [-400, 0, 400]
    y_off = [-400, 0, 400]

    waxs_arc = [40, 20, 0]
    user = "FY"

    # Check and correct sample names just in case
    names = [n.translate({ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ "}) for n in names]

    # Check if the length of xlocs, ylocs and names are the same
    assert len(piezo_x) == len(names), f"Number of X coordinates ({len(piezo_x)}) is different from number of samples ({len(names)})"
    assert len(piezo_x) == len(piezo_y), f"Number of X coordinates ({len(piezo_x)}) is different from number of samples ({len(piezo_y)})"
    assert len(piezo_x) == len(hexa_y), f"Number of X coordinates ({len(piezo_x)}) is different from number of samples ({len(hexa_y)})"

    for i, wa in enumerate(waxs_arc):
        yield from bps.mv(waxs, wa)
        # Detectors, disable SAXS when WAXS in the way
        dets = [pil900KW] if waxs.arc.position < 15 else [pil900KW, pil1M]
        det_exposure_time(t, t)

        for name, x, y, y_hexa in zip(names, piezo_x, piezo_y, hexa_y):

            yield from bps.mv(stage.y, y_hexa)

            for yy, y_of in enumerate(y_off):
                yield from bps.mv(piezo.y, y + y_of)

                for xx, x_of in enumerate(x_off):
                    yield from bps.mv(piezo.x, x + x_of)

                    loc = f'{yy}{xx}'
                    sample_name = f'{name}{get_scan_md()}_loc{loc}'
                    sample_id(user_name='FY', sample_name=sample_name)

                    sample_id(user_name=user, sample_name=sample_name)
                    print(f"\n\n\n\t=== Sample: {sample_name} ===")
                    yield from bp.count(dets)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)





def run_swaxs_Fei_2025_1(t=1):
    """
    Take WAXS and SAXS at nine sample positions for averaging

    Specify central positions on the samples with xlocs and ylocs,
    then offsets from central positions with x_off and y_off. Run
    WAXS arc as the slowest motor. SAXS sdd 4.0 m.
    """

    # names   = [  'A6',  'A5',  'A4',  'A3',  'A2',  'A1',  
    #              'B6',  'B5',  'B4',  'B3',  'B2',  'B1',
    #              'C6',  'C5',  'C4',  'C3',  'C2',  'C1',
    #              'D6',  'D5',  'D4',  'D3',  'D2',  'D1',
                  
    #              'E6',  'E5',  'E4',  'E3',  'E2',  'E1',  
    #              'F6',  'F5',  'F4',  'F3',  'F2',  'F1',
    #              'G6',  'G5',  'G4',  'G3',  'G2',  'G1',
    #              'H6',  'H5',  'H4',  'H3',  'H2',  'H1']
    
    # piezo_x = [ 45500, 37000, 28000, 19500, 10500,  1500, 
    #             45500, 37000, 28000, 19500, 10500,  1500,
    #             45500, 37000, 27500, 19000, 10000,  1500,
    #             45500, 37000, 28000, 19700, 10500,  1500,
                
    #            -10500,-19200,-28200,-37000,-45800,-54300, 
    #            -10500,-19200,-28200,-37300,-45800,-54300,
    #            -10500,-19200,-28200,-37300,-45800,-54300,
    #            -10500,-19200,-28200,-37300,-45800,-54300]
    
    # piezo_y = [ -8800, -8800, -8800, -8500,  -8500,-8500,
    #             -3500, -3500, -3500, -3500,  -3500,-3500,
    #              2000,  2000,  2000,  2000,   2000, 1700,
    #               700,   700,   700,  1500,    700,  700,
                  
    #             -8800, -8800, -8800, -8500,  -8500,-8500,
    #             -3500, -3500, -3500, -3500,  -3500,-3500,
    #              1700,  1700,  1700,  1700,   1700, 1700,
    #               700,   700,   700,  1500,    700, 1000]
    
    # hexa_y =  [     0,     0,     0,     0,      0,    0,
    #                 0,     0,     0,     0,      0,    0,
    #                 0,     0,     0,     0,      0,    0,
    #                 6,     6,     6,     6,      6,    6,

    #                 0,     0,     0,     0,      0,    0,
    #                 0,     0,     0,     0,      0,    0,
    #                 0,     0,     0,     0,      0,    0,
    #                 6,     6,     6,     6,      6,    6]
    
    # hexa_x =  [     0,     0,     0,     0,      0,    0,
    #                 0,     0,     0,     0,      0,    0,
    #                 0,     0,     0,     0,      0,    0,
    #                 0,     0,     0,     0,      0,    0,

    #                 0,     0,     0,     0,      0,   -1,
    #                 0,     0,     0,     0,      0,   -1,
    #                 0,     0,     0,     0,      0,   -1,
    #                 0,     0,     0,     0,      0,   -1]

    # namess   = [[  'I1',  'I2',  'I3',  'I4',  'I5',  'I6',  'M2',  'N2',  'O2',  'P2',  'H1',],
    #              ['J1',  'J2',  'J3',  'J4',  'J5',  'J6',  'G1',],
    #              ['K1',  'K2',  'K3',  'K4',  'K5',  'K6',  'M1',  'N1',  'O1',  'P1',  'F1',],
    #              ['L1',  'L2',  'L3',  'L4',  'L5',  'L6',  'E1']]
    
    # piezo_xs = [[ 46500, 38000, 29500, 20000, 11200,  2500, -7500,-13000,-18000,-23200,-34500,],
    #             [46500, 38000, 29500, 20000, 11200,  2500,-34500,],
    #             [46500, 38000, 29500, 20000, 11200,  2500, -7500,-13000,-18200,-23200,-35000,],
    #             [46500, 38000, 29500, 20000, 11200,  2700,-35000]]
    
    # piezo_ys = [ [-8500, -8500, -8500, -8500, -8500, -8500, -8500, -8500, -8500, -8500, -8500,],
    #             [-3700, -3700, -3700, -3700, -3700, -3700, -3700,],
    #              [1500,  1500,  1500,  1500,  1500,  1500,   500,   500,   500,   500,  1500,],
    #               [900,   900,   900,   900,   900,   900,   900]]
    
    # hexa_ys =  [     [0,     0,     0,     0,      0,    0,     0,     0,     0,     0,     0,],
    #                 [0,     0,     0,     0,      0,    0,     0,],
    #                 [0,     0,     0,     0,      0,    0,     0,     0,     0,     0,     0,],
    #                 [6,     6,     6,     6,      6,    6,     6]]

    names   = [  'G1',  'G2',  'G3',  'G4',  'G5',  'G6', 'C6',   'C5',  'C4',  'C3',  'C2',  'C1']
    piezo_x = [ 14200, 23200, 32200, 41200, 50200, 50000,-24000,-33000,-42500,-51000,-51000,-54000]
    piezo_y = [ -7500, -7500, -7500, -7500, -7500, -7500, -8000, -8000, -8000, -8000, -8000, -8000]
    hexa_y =  [     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0]
    hexa_x =  [   0.1,   0.1,   0.1,   0.1,   0.1,   9.1,   0.1,   0.1,   0.1,   0.1,  -8.9,   -14]

    # Offsets for taking a few points per sample
    x_off = [-400, 0, 400]
    y_off = [-400, 0, 400]

    waxs_arc = [40, 20, 0]
    user = "FY"


    # for names, piezo_x, piezo_y, hexa_y in zip(namess, piezo_xs, piezo_ys, hexa_ys):
    #     # Check and correct sample names just in case
    #     names = [n.translate({ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ "}) for n in names]

    #     # Check if the length of xlocs, ylocs and names are the same
    #     assert len(piezo_x) == len(names), f"Number of X coordinates ({len(piezo_x)}) is different from number of samples ({len(names)})"
    #     assert len(piezo_x) == len(piezo_y), f"Number of X coordinates ({len(piezo_x)}) is different from number of samples ({len(piezo_y)})"
    #     assert len(piezo_x) == len(hexa_y), f"Number of X coordinates ({len(piezo_x)}) is different from number of samples ({len(hexa_y)})"

    for i, wa in enumerate(waxs_arc):
        yield from bps.mv(waxs, wa)
        # Detectors, disable SAXS when WAXS in the way
        dets = [pil900KW] if waxs.arc.position < 15 else [pil900KW, pil1M]
        det_exposure_time(t, t)

        for name, x, y, x_hexa in zip(names, piezo_x, piezo_y, hexa_x):

            yield from bps.mv(stage.x, x_hexa)

            for yy, y_of in enumerate(y_off):
                yield from bps.mv(piezo.y, y + y_of)

                for xx, x_of in enumerate(x_off):
                    yield from bps.mv(piezo.x, x + x_of)
                    yield from bps.sleep(1)

                    loc = f'{yy}{xx}'
                    sample_name = f'{name}{get_scan_md()}_loc{loc}'
                    sample_id(user_name='FY', sample_name=sample_name)

                    sample_id(user_name=user, sample_name=sample_name)
                    print(f"\n\n\n\t=== Sample: {sample_name} ===")
                    yield from bp.count(dets)


    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)

    

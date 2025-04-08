# Align GiSAXS sample
import numpy as np


def mesh_IIT_2022_1(t=1):
    waxs_range = [20, 0]

    name = "JO"
    dets = [pil900KW, pil1M, pil1mroi2, pil1mroi3, pil1mroi4]
    det_exposure_time(t, t)

    """#these samples are very large areas and 3rd priority (lowest) except for the 1st teeth12.
    samples = ['Ared',       'Ablue',       'Cred' ]
    x_list = [ -24000,        -34000,        23000  ]
    y_list = [ -300,          3700,          3700    ]
    z_list = [  5400,          5400,         7400    ]
    hexa_y = [   -7,             -7,          -7      ]
    chi_list = [0,              0,             0        ]
    x_range=[ [0,-10000,41], [0,-5000,21],[0,-5000,21]  ]
    y_range=[ [0,-9000,91], [0,-5000,51],[0,-9000,91]   ]
    """

    samples = ["Cred_2"]
    x_list = [23000]
    y_list = [3700]
    z_list = [7400]
    hexa_y = [-7]
    chi_list = [0]
    x_range = [[0, -5000, 21]]
    y_range = [[0, -9000, 91]]

    assert len(x_list) == len(
        y_list
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(y_list)})"
    assert len(x_list) == len(
        samples
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})"
    assert len(x_list) == len(
        x_range
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(x_range)})"
    assert len(x_list) == len(
        y_range
    ), f"Number of X coordinates ({len(x_list)}) is different from number of samples ({len(y_range)})"

    for x, y, z, chi, hy, sample, x_r, y_r in zip(
        x_list, y_list, z_list, chi_list, hexa_y, samples, x_range, y_range
    ):
        # proposal_id('2021_3', 'Wang%s'%num)
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(piezo.y, y)
        yield from bps.mv(piezo.z, z)
        yield from bps.mv(piezo.ch, chi)
        yield from bps.mv(stage.y, hy)

        for wa in waxs_range:

            if wa < 10:
                dets = [pil900KW]
            else:
                dets = [pil900KW, pil1M, pil1mroi2, pil1mroi3, pil1mroi4]

            yield from bps.mv(waxs, wa)
            name_fmt = "{sam}_wa{waxs}_16.1keV_3m"
            proposal_id("2022_1", "310511_Zhernenkov/%s" % sample)
            sample_name = name_fmt.format(sam=sample, waxs="%2.1f" % wa)
            sample_id(user_name=name, sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.rel_grid_scan(dets, piezo.y, *y_r, piezo.x, *x_r, 0)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)

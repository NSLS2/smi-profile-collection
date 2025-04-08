def saxsafrl(t=2):
    # Slowest cycle:
    name = "BS"
    x_list = -6
    # Detectors, motors:
    dets = [pil1M, pil300KW, ls.ch1_read]
    # y_range = [-0.0, 0.0, 1]
    sample = "water2"
    num = 10000

    pil1M.cam.file_path.put(
        f"/ramdisk/images/users/2020_2/305934_Schantz/1M/%s" % sample
    )
    name_fmt = "{i}_{temperature}C"
    #    param   = '20.4'
    # assert len(x_list) == len(samples), f'Number of X coordinates ({len(x_list)}) is different from number of samples ({len(samples)})'
    det_exposure_time(t, t)
    for i in range(num):
        temp = ls.ch1_read.value
        # fs.open()
        # yield from bps.sleep(0.25)
        # pin = pin_diode.read()['pin_diode_current2_mean_value']['value']
        # pin = pdcurrent2.value
        # print(pin)
        # yield from bps.sleep(0.25)
        # fs.close()
        # sample_name = name_fmt.format(temperature=temp, pinread = float('%.1f'%pin), i = '%4.4d'%i)
        sample_name = name_fmt.format(temperature=temp, i="%4.4d" % (i))
        print(f"\n\t=== Sample: {sample_name} ===\n")
        sample_id(user_name=sample, sample_name=sample_name)
        # yield from bp.count(dets)
        # yield from bp.rel_scan(dets, stage.y, *y_range)
        yield from bp.count(dets, num=1)
        yield from bps.sleep(2)
    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)

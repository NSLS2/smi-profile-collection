def run_simple_energy(t=1):
    """
    Take simple e scan
    """

    name = 'CuNPfullcell-noVapp-escan'

    waxs_arc = [ 40 ]

    #energies = np.arange(8950, 9000 + 1, 1)
    energies = np.arange(8900, 9100 + 1, 5)

    energies =  np.concatenate((
        np.arange(8900, 8975, 5),
        np.arange(8975, 8990, 2),
        np.arange(8990, 9010, 1),
        np.arange(9010, 9101, 5),
        ))

    user = "KR"
    det_exposure_time(t, t)


    for wa in waxs_arc:
        yield from bps.mv(waxs, wa)
        dets = [pil900KW] if waxs.arc.position < 15 else [pil900KW, pil1M]

        for i, nrg in enumerate(energies):
            yield from bps.mv(energy, nrg)
            yield from bps.sleep(2)
            if xbpm2.sumX.get() < 20:
                yield from bps.sleep(2)
                yield from bps.mv(energy, nrg)
                yield from bps.sleep(2)

            sample_name = f'{name}{get_more_md()}'
            sample_id(user_name=user, sample_name=sample_name)
            print(f"\n\n\n\t=== Sample: {sample_name} ===")
            yield from bp.count(dets)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)


def name_sample(name, tstamp):
    """
    Create sample name with metadata

    Args:
        name (str): sample name
        tstamp (time): referenced start time created separately as
            tstamp = time.time()
    """

    eplased = time.time() - tstamp
    sample_name = f'{name}{get_more_md()}_t{eplased:.1f}'
    sample_id(user_name='KR', sample_name=sample_name)
    print(sample_name)

def create_timestamp():
    """
    store in RE.md and print
    """
    RE.md['tstamp'] = time.time()
    print('\nTime stamp created in RE.md')
    tstamp = RE.md['tstamp']
    print(f'tstamp: {tstamp}')

def continous_run(sname='test', t=2, wait=8, frames=2160):
    """
    Take data continously
    
    Create timestamp in BlueSky before running this function as
    create_timestamp()

    Args:
        sname (str): basic sample name,
        t (float): camera exposure time is seconds,
        wait (float): delay between frames,
        frames(int): number of frames to take
    """
    try:
        tstamp = RE.md['tstamp']
    except:
        tstamp = time.time()
        RE.md['tstamp'] = tstamp
    
    det_exposure_time(t, t)

    for i in range(frames):

        print(f'Taking {i + 1} / {frames} frames')

        # update sample name
        name_sample(sname, tstamp)

        # take one fram
        yield from bp.count([pil900KW, pil1M])

        # wait
        print(f'\nWaiting {wait} s')
        yield from bps.sleep(wait)
    
def clear_md():
    """
    Remove time stamp, sample zero, and alignment after changing the cell
    """

    keys = [ 'tstamp', 'alignment_LUT', 'sample_pos0']
    
    for k in keys:
        try:
            RE.md.pop(k)
        except:
            print(f'No {k} key')
# 2023-Sep 18 
#
# 16.1 keV, 200*30um beam, air
# proposal_id('2023_3', '313379_Modestino', analysis=True)
# RE.md['SAF_number'] = 312127
#
# RE.md['SAXS_setup'] = {'sdd': 9200, 'beam_centre': [450, 554], 'bs': 'rod', 'energy': 16100}
# 
# RE(rel_scan([pil1M], stage.y, -2, 2, 15)); ps()
# ---------------------------------------------------------------
# ---------------------------------------------------------------
# 1. [Search hutch and close]
# 2. RE(shopen())
# 3. [Enter sample name and x-position in this 30-user-Modestino.py]
# [Ctrl+s to save this file]
# %run -i /home/xf12id/.ipython/profile_collection/startup/users/30-user-Modestino.py
#
# (Just in case)
# Ctrl+c once/twice; RE.abort()
# bsui
# %run -i /home/xf12id/.ipython/profile_collection/startup/users/30-user-Modestino.py
#
# 4. RE(shclose())
# 5. [To take out sample]
# ---------------------------------------------------------------
# Note: 
# beamstop_save()

def move_waxs(waxs_angle=20):
    yield from bps.mv(waxs, waxs_angle)

# RE(measure_saxs(t=5, user_name="MM", sample='Bar1sam1', xr_list = [-200, 0]))
def measure_saxs(t=1, user_name="MM", sample='Bar1sam1', xr_list = [0], yr_list = [0]):
    x0 = piezo.x.position
    y0 = -4500 #piezo.y.position
    #y0 = piezo.y.position
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)

    for xr in xr_list:
        for yr in yr_list:
            x = x0+xr
            y = y0+yr
            yield from bps.mv(piezo.x, x)
            yield from bps.mv(piezo.y, y)

            sample_name = "{sample}_x{x:06.0f}_y{y:06.0f}_sdd2200_waxs20_{t}s".format(
                sample=sample,
                x=x,
                y=y,
                t=t,
            )
            sample_id(user_name=user_name, sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")

            yield from bp.count(dets, num=1)
    
    yield from bps.mv(piezo.y, y0)


    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)
    
# RE(measure_saxs_bar(t=5, user_name="MM_Bar3", xr_list = [-200, 0], yr_list = [400, 0]))
def measure_saxs_bar(t=1, user_name="MM_Bar2", y0=-6000, xr_list = [-200, 0], yr_list = [400, 0]):
    #z -3000
    dets = [pil1M, pil900KW]
    det_exposure_time(t, t)   

    x_list = [41000, -400, -42000]
    y_list = [-6000, -3500, -500]
    sample_list = ["sam1", "sam2", "sam3"]
    #x0 = piezo.x.position
    #y0 = -3000 #piezo.y.position ##MM 2023-Sep, around 5000

    assert len(x_list) == len(sample_list), f"Sample name/position list is incorrect"
    for x0,y0, sample in zip(x_list, y_list, sample_list):
        for xr in xr_list:
            for yr in yr_list:
                x = x0+xr
                y = y0+yr
                yield from bps.mv(piezo.x, x)
                yield from bps.mv(piezo.y, y)

                sample_name = "{sample}_x{x:06.0f}_y{y:06.0f}_sdd2200_waxs20_{t}s".format(
                    sample=sample,
                    x=x,
                    y=y,
                    t=t,
                )
                sample_id(user_name=user_name, sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")

                yield from bp.count(dets, num=1)
    
    yield from bps.mv(piezo.y, y0)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)


#### In-situ 2024Jan
def measure_insitu(tstatic=5, t=0.2, t2=5, t0=None, syringe=False, user_name="Insitu", sample='test1', n0=0, Nin=2, Nmax=999, time_sleep_sec=15):
    #x0 = -20500 #piezo.x.position #30800 #piezo.x.position
    #y0 = -3000 #piezo.y.position #-600 #piezo.y.position
    x0 = piezo.x.position #30800 #piezo.x.position
    y0 = piezo.y.position #-600 #piezo.y.position
    #z0 = 17500
    dets = [pil1M] #, pil900KW]

    yield from bps.mv(piezo.x, x0)
    yield from bps.mv(piezo.y, y0)
    #yield from bps.mv(piezo.y, z0)

    if t0==None:
        t0 = time.time()
        print(t0)

    ### Static
    t_list = [tstatic, t]
    print("\nStatic in the beginning")
    for t in t_list:
        det_exposure_time(t, t)
        yield from bps.sleep(0.5)
        sample_name = "{sample}_n00_t{time:07.2f}s_x{x:06.0f}_y{y:06.0f}_sdd2200_waxs20_{t}s".format(
            sample=sample,
            time = time.time()-t0,
            x=x0,
            y=y0,
            t=t,
        )
        sample_id(user_name=user_name, sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")
        #sample_id(user_name=user_name, sample_name="test")
        yield from bp.count(dets, num=1)

    ### In-situ
    if 1: ##Somehow maybe this helps with data saving in burst mode
        det_exposure_time(t, t)
        yield from bps.sleep(0.5)
        sample_id(user_name="test", sample_name="test")
        yield from bp.count(dets, num=1)
        
        det_exposure_time(t, t)
        yield from bps.sleep(0.5)
        sample_id(user_name="test", sample_name="test")
        yield from bp.count(dets, num=1)

    #det_exposure_time(t, t)
    
    print("\nStart in-situ")

    for nn in range(Nmax):
        print("\nnn={}, time {:.0f}s".format(nn+n0, (time.time()-t0)))
        # #for xr in xr_list:
        # #    for yr in yr_list:
        x = x0 #+xr
        y = y0 #+yr
        # yield from bps.mv(piezo.x, x)
        # yield from bps.mv(piezo.y, y)

        sample_name = "{sample}_n{nn}_t{time:07.2f}s_x{x:06.0f}_y{y:06.0f}_sdd2200_waxs20_{t}s".format(
            sample=sample,
            nn=nn+n0,
            time = time.time()-t0,
            x=x,
            y=y,
            t=t,
        )
        sample_id(user_name=user_name, sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")

        if nn+n0==0:
            det_exposure_time(t, t2)
            yield from bps.sleep(0.5) ##Somehow maybe this helps with data saving in burst mode
            if syringe==True:
                print(f"!!!!! Syringe pump infusing...\n")
                yield from bps.mv(syringe_pu.x3, 1)

        # elif nn+n0==1: 
        #     det_exposure_time(t, t2)
        #     yield from bps.sleep(0.5)
        #     if syringe==True:
        #         print(f"Syringe pump infusing...\n")
        #         yield from bps.mv(syringe_pu.x3, 1)
        # elif nn+n0 < Nin:
        #     det_exposure_time(t, t2)
        #     yield from bps.sleep(0.5)

        if nn+n0 >= Nin:
            det_exposure_time(t, t)
            yield from bps.sleep(0.5)
        
            print("\nSleeping for {}s".format(time_sleep_sec))
            yield from bps.sleep(time_sleep_sec)           

        
        
        yield from bp.count(dets, num=1)
        #yield from bps.sleep(0.5)  ##Somehow maybe this helps with data saving in burst mode

        #if (time.time()-t0) > time_period_sec:
        # if nn+n0 >= Nin:
        #     print("\nSleeping for {}s".format(time_sleep_sec))
        #     yield from bps.sleep(time_sleep_sec) 
        #     det_exposure_time(t, t)
                

    #yield from bps.mv(piezo.y, y0)
    yield from bps.sleep(0.5)
    print("\nStatic at the end")

    t_list = [tstatic]
    for t in t_list:
        det_exposure_time(t, t)
        yield from bps.sleep(0.5)
        sample_name = "{sample}_n{nn}_t{time:07.2f}s_x{x:06.0f}_y{y:06.0f}_sdd2200_waxs20_{t}s".format(
            sample=sample,
            nn=Nmax,
            time = time.time()-t0,
            x=x,
            y=y,
            t=t,
        )
        sample_id(user_name=user_name, sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")
        #sample_id(user_name=user_name, sample_name="test")
        yield from bp.count(dets, num=1)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)
    #yield from bp.count(dets, num=1)


def measure_scan(t=0.2, t0=None, step=[100, 30], syringe=False, user_name="Insitu", sample='test1', n0=0, Nmax=999, time_sleep_sec=15):
    #x0 = -20500 #piezo.x.position #30800 #piezo.x.position
    #y0 = -3000 #piezo.y.position #-600 #piezo.y.position
    print("\nCheck camera for sample position, should be around x=-20500, y=-4000")
    x0 = piezo.x.position #30800 #piezo.x.position
    y0 = piezo.y.position #-600 #piezo.y.position
    #z0 = 17500
    dets = [pil1M] #, pil900KW]

    yield from bps.mv(piezo.x, x0)
    yield from bps.mv(piezo.y, y0)
    #yield from bps.mv(piezo.y, z0)

    if t0==None:
        t0 = time.time()
        print(t0)

    ### In-situ
    if 1: ##Somehow maybe this helps with data saving in burst mode
        det_exposure_time(t, t)
        yield from bps.sleep(0.5)
        sample_id(user_name="test", sample_name="test")
        yield from bp.count(dets, num=1)
        

    #det_exposure_time(t, t)
    
    print("\nStart in-situ")

    det_exposure_time(t, t)
    yield from bps.sleep(0.5)

    for nn in range(Nmax):
        print("\nnn={}, time {:.0f}s".format(nn+n0, (time.time()-t0)))
        # #for xr in xr_list:
        # #    for yr in yr_list:
        x = x0 + np.mod(nn,10)*step[0]
        y = y0 + np.floor(nn/10)*step[1]
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(piezo.y, y)

        sample_name = "{sample}_n{nn}_t{time:07.2f}s_x{x:06.0f}_y{y:06.0f}_sdd2200_waxs20_{t}s".format(
            sample=sample,
            nn=nn+n0,
            time = time.time()-t0,
            x=x,
            y=y,
            t=t,
        )
        sample_id(user_name=user_name, sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")
    
        print("\nSleeping for {}s".format(time_sleep_sec))
        yield from bps.sleep(time_sleep_sec)         

        if nn==0:
            if syringe==True:
                print(f"!!!!! Syringe pump infusing...\n")
                yield from bps.mv(syringe_pu.x3, 1)
        
        
        yield from bp.count(dets, num=1)
        #yield from bps.sleep(0.5)  ##Somehow maybe this helps with data saving in burst mode

        #if (time.time()-t0) > time_period_sec:
        # if nn+n0 >= Nin:
        #     print("\nSleeping for {}s".format(time_sleep_sec))
        #     yield from bps.sleep(time_sleep_sec) 
        #     det_exposure_time(t, t)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)
    #yield from bp.count(dets, num=1)


#### In-situ
# yield from bps.mv(syringe_pu.x3, 1)
# RE(measure_series(t=0.1, t0=None, user_name="Insitu", sample='test1', Nmax=999))
# RE(measure_series(tstatic=5, t=0.2, t2=180, t0=None, user_name="Insitu", sample='water1', n0=0, Nmax=2, time_period_sec=180, time_sleep_sec=2))
def measure_series(tstatic=5, t=0.2, t2=5, burst=1, t0=None, user_name="Insitu", sample='test1', n0=0, Nmax=999, time_period_sec=200, time_sleep_sec=15):
    x0 = piezo.x.position #30800 #piezo.x.position
    y0 = piezo.y.position #-600 #piezo.y.position
    dets = [pil1M] #, pil900KW]

    if t0==None:
        t0 = time.time()
        print(t0)
   
    if tstatic>0:
        det_exposure_time(tstatic, tstatic)
        sample_name = "{sample}_n00_t{time:07.2f}s_x{x:06.0f}_y{y:06.0f}_sdd2200_waxs20_{t}s".format(
            sample=sample,
            time = time.time()-t0,
            x=x0,
            y=y0,
            t=t,
        )
        sample_id(user_name=user_name, sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")

        #sample_id(user_name=user_name, sample_name="test")
        yield from bp.count(dets, num=1)

    else: ## insitu
    
        if 1:
            det_exposure_time(t, t)
            sample_id(user_name="test", sample_name="test")
            yield from bp.count(dets, num=1)
            
            det_exposure_time(t, t)
            sample_id(user_name="test", sample_name="test")
            yield from bp.count(dets, num=1)

        det_exposure_time(t, t2)

        for nn in range(Nmax):
            print(f"\n\t##### nn {nn} #####\n")
            #for xr in xr_list:
            #    for yr in yr_list:
            x = x0 #+xr
            y = y0 #+yr
            yield from bps.mv(piezo.x, x)
            yield from bps.mv(piezo.y, y)

            sample_name = "{sample}_n{nn}_t{time:07.2f}s_x{x:06.0f}_y{y:06.0f}_sdd2200_waxs20_{t}s".format(
                sample=sample,
                nn=nn+n0,
                time = time.time()-t0,
                x=x,
                y=y,
                t=t,
            )
            sample_id(user_name=user_name, sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")

            if nn==0: 
                print(f"Syringe pump infusing...\n")
                yield from bps.mv(syringe_pu.x3, 1)
            
            yield from bp.count(dets, num=1)

            if (time.time()-t0) > time_period_sec:
                print("\nnn={}, time {:.0f}min; Sleeping for {}s".format(nn+n0, (time.time()-t0)/60, time_sleep_sec))
                yield from bps.sleep(time_sleep_sec) 
                det_exposure_time(t, t)

    #yield from bps.mv(piezo.y, y0)
    time.sleep(1)  
    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)
    #yield from bp.count(dets, num=1)

####
def test_measure(t=1, waxs_angle=0, user_name="test", sample_name='EmptyKapton', dets = [pil1M, pil900KW]):
    yield from bps.mv(waxs, waxs_angle)
    sample_id(user_name=user_name, sample_name=sample_name)
    det_exposure_time(t, t)
    yield from bp.count(dets, num=1)

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5)


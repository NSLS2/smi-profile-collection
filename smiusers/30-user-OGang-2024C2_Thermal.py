

print('Load Fang Lu micro -- 2024C1...')
from datetime import datetime


 

 
 
 


smi = SMI_Beamline()

#user_name = "FLu"
#user_name = "HKim"
#user_name = "MH"
#user_name = "WLiu"
#username = user_name

 
 

''' NOTE

 # SAXS distance , 5 meter
# 1M [  -2.77, -61., 5000  ]
# beam stop [ 1.8, 288.99,  13  ], a rod
# beam center   [ 471, 559     ]
# beamstop_save()



proposal_id('2024_1', '313760_FLu', analysis=True)
/nsls2/data/smi/legacy/results/data/2024_1/313760_FLu

%run -i  ~/.ipython/profile_collection/startup/users/30-user-Flu_2024C1_TSAXS.py


RE( measure_saxs( sample = 'DirectBeam' ) )
RE(SMI.modeMeasurement())
RE( measure_saxs( sample = 'AgBH_5m' ) )

RE( measure_waxs(   sample = 'AgBH_5m', waxs_angle = 20   ) )


t0=time.time();RE(measure_series_multi_angle_wsaxs(waxs_angles=[0,  20   ]));run_time(t0)





Mingxin's T samples
Y: 470
hexY:L -7 


Fang's sample, X -30900, Y: 900, hexY: -1 
proposal_id('2024_2', '313760_Flu_01', analysis=True)


'''




# Run1, pizo motor (SmarAct) Z= ,  sample to SAXS dector distance 5m
dx, dy = 0, 0

user_name = "DS"
username = user_name

#sample_dict = {k: 'S_%03d'%k for k in range(1,16) }
## Run1, S7 - S1, 
# sample_dict = {  8: '3_38_A',  
#                # 10: '2_87_F1',   
# }
# pxy_dict = {  8:  ( 1200, 0     ) ,  
#             #10:  ( 14100, 200     ) ,
 
#   }

# lim_dict = { 8: [ [ 1000, 1400 + 200 ], [-20, 160 + 30 ]], 
#            #   10: [ [ 14100 - 200, 14100 + 200], [200 - 20, 200 + 160 ]], 
# }


sample_dict = {  
                 2: '2-41_v96_8H_1_1',  
                 3: '2-41_v96_8H_1_2',  
                 4: '2-41_v96_8H_2_1', 
                 5: '2-41_v54_8H_1_1',  
                 6: '2-41_v54_8H_1_2',  
                 7: '2-41_v54_8H_2_1', 
                 8: '2-46_v96_8H_1_1',  
                 9: '2-46_v96_8H_1_2',  
                 10: '2-46_v96_8H_2_1', 
                 11: '2-46_v54_8H_1_1',  
                #  12: '2-41_v54_8H_1_2',  
                 13: '2-46_v54_8H_2_1',
                 14: '1xTAE+12-5mM_Mg_Buffer',  
}
pxy_dict = {  
              2:  ( -37018, 528     ) ,  
              3:  ( -30317, 378     ) , 
              4:  ( -24018, -122     ) ,
              5:  ( -18068, -22     ) ,  
              6:  ( -11468, 27     ) , 
              7:  ( -5268, -372     ) , 
              8:  ( 1582, -372     ) ,  
              9:  ( 7281, 127     ) , 
              10:  ( 13982, 127     ) , 
              11:  ( 20081, 278     ) ,  
            #   12:  ( 26685, 28     ) , 
              13:  ( 33131, 27     ) , 
              14:  ( 39331, 478     ) ,  
  
          
 
  }

lim_dict = { 
            2:  [ [ -37018,-37018  + 200 ], [ 528, 528 + 30 ]], 
            3:  [ [ -30317, -30317 + 200 ], [ 378, 378 + 30 ]],
             4:  [ [ -24018, -24018 + 200 ], [ -122, -122 + 30]],
             5:  [ [ -18068, -18068 + 200 ], [ -22, -22 + 30 ]], 
             6:  [ [ -11468, -11468 + 200 ], [ 27, 27 + 30 ]],
             7:  [ [ -5268, -5268 + 200 ], [ -372, -372  + 30 ]],
             8:  [ [  1582,  1582 + 200 ], [ -372, -372 + 30 ]], 
             9:  [ [  7281,  7281 + 200 ], [ 127, 127 + 30 ]],
             10: [ [ 13982, 13982   + 200 ], [ 127, 127 + 30 ]],
             11: [ [ 20081, 20081   + 200 ], [ 278, 278 + 30 ]],
            #  12: [ [ 26685, 26685   + 200 ], [ 28, 28 + 30 ]],
             13: [ [ 33131, 33131   + 200 ], [ 27, 27 + 30 ]],
             14: [ [ 39331, 39331   + 200 ], [ 478, 478 + 30 ]],

            #  10: [ [ 14100 - 200, 14100 + 200], [200 - 20, 200 + 160 ]], 
}








# t0=time.time();RE(measure_series_multi_angle_wsaxs(waxs_angles=[0,  20   ]));run_time(t0)





# def shopen():
#     yield from bps.mv(ph_shutter.open_cmd, 1)
#     yield from bps.sleep(1)
#     # Disabled because of problems with XBPM3 in microfocus    
#     yield from bps.mv(manual_PID_disable_pitch, "0")
#     yield from bps.mv(manual_PID_disable_roll, "0")

   # #Check if te set-up is in-air or not. If so, open t
   # he GV automatically when opening the shutter
    # if get_chamber_pressure(chamber_pressure.waxs) > 1E-02 and get_chamber_pressure(chamber_pressure.maxs) < 1E-02:
    #    yield from bps.mv(GV7.open_cmd, 1 )
    #    yield from bps.sleep(1)
    #    yield from bps.mv(GV7.open_cmd, 1 )
    #    yield from bps.sleep(1)



#####12/15
#energy 8.33, Dis 5 m 



#   t0=time.time();RE(measure_series_multi_angle_wsaxs());run_time(t0)




######################



dx =  0
dy = 0 #-2000
ks = np.array(list((sample_dict.keys())))
pxy_dict = {k: [pxy_dict[k][0] + dx, pxy_dict[k][1] + dy] for k in ks}

x_list = np.array(list((pxy_dict.values())))[:, 0]
y_list = np.array(list((pxy_dict.values())))[:, 1]
sample_list = np.array(list((sample_dict.values())))
##################################################
############ Some convinent functions#################
#########################################################

def Measure_one():
    #ps1 = getSamMap( pos = [ -27760, -2930],  step_size = [100, 100], rot_angle = 0, Nx=20 , Ny=30)
    #Measure_Map(  t = 5 ,  sample = 'O139_100umstep',  pz=7980,  ps=ps1,  username = 'FTeng', )
    ps1 = getSamMap( pos = [ -27800, -1975],  step_size = [100, 100], rot_angle = 0, Nx=25 , Ny=4)
    Measure_Map(  t = 5 ,  sample = 'O139_50um_100umstep',  pz=7980,  ps=ps1,  username = 'FTeng', )
    
    ps2 = getSamMap( pos = [ -27810, -1455],  step_size = [100, 100], rot_angle = 0, Nx=25 , Ny=4)
    Measure_Map(  t = 5 ,  sample = 'O139_20um_100umstep',  pz=7980,  ps=ps2,  username = 'FTeng', )


 

'''
DAPHNE:  
#for TEST
i_dict =  run_RT_temperature(   exposure_t = 0.1 , i_dict = None  ) 
run_HT_time_temperature( T = 29, t_interval=3, t_total = 12,exposure_t = 0.1, i_dict = i_dict)

#for Real RUN
i_dict =  run_RT_temperature(  ) 
run_HT_time_temperature(  i_dict = i_dict )


# Mingxin
#for TEST
tt0, i_dict = run_melting_Tm(   TH=29.2,  Tm = 25 , TH_sleep_time = 10  ) 
run_Tm( tt0, i_dict, Tm=29, exposure_t = 0.1, t_total_T40 = 30, t_interval = 3 ) 
run_melting( Trange = [ 29, 29.1 ], dtemp = 0.1, exposure_t = 0.2,  sleep_time_per_dtemp  = 1  ) 


#for REAL
tt0, i_dict = run_melting_Tm(   TH=29.2,  Tm = 25 , TH_sleep_time = 10  ) 
run_Tm( tt0, i_dict, Tm=29, exposure_t = 0.1, t_total_T40 = 30, t_interval = 3 ) 
run_melting( Trange = [ 29, 29.1 ], dtemp = 0.1, exposure_t = 0.2,  sleep_time_per_dtemp  = 1  ) 





'''



def run_HT_time_temperature( T =  45, t_interval=10*60, t_total = 31*60, exposure_t = 0.1 , i_dict = None  ):
    '''      
    
    '''
    #step one 
    #set Temperature 
    if i_dict is None:
        i_dict = {}
        for  k  in ks:
            i_dict[k] = 0
    RE( gotoT( T ) ) 
    t0 = time.time()
    while (time.time() < ( t0 + t_total ) ):
        t1 = time.time()
        for  k  in ks:             
            mov_sam( k )
            pos_list = getSamMap( xlim = lim_dict[k][0], ylim = lim_dict[k][1] )
            N = len( pos_list )
            print( 'There are %s points available (Cur: %s-th spot) for this sample at pos=%s: %s'%(
                    N, i_dict[k], sample_dict[k], k ))
            RE(bps.mv( piezo.x,  pos_list[i_dict[k]%N][0]  ))
            RE(bps.mv( piezo.y,  pos_list[i_dict[k]%N][1]  ))
            sample = RE.md['sample']
            RE(measure_saxs( exposure_t, sample= sample + '_T_%.2f'%getT() + '_runt_%.0fs'%(time.time()-t0 ) ))
            i_dict[k]+=1
        if   ( t_interval + ( t1 - time.time() ) ) < 0:
            pass
        else:
            time.sleep(  t_interval + ( t1 - time.time() )  )

    Tr = 25 
    print( i_dict )
    RE( setT(Tr)    ) 
    RE( stopT() ) 
    return i_dict
   





def run_RT_temperature(   exposure_t = 0.1 , i_dict = None  ):
    '''  
    
    run_RT_temperature(   exposure_t = 0.1 , i_dict = None  ) ) 


    '''
    #step one 
    #set Temperature 
    if i_dict is None:
        i_dict = {}
        for  k  in ks:
            i_dict[k] = 0
    for  k  in ks:             
        mov_sam( k )
        pos_list = getSamMap( xlim = lim_dict[k][0], ylim = lim_dict[k][1] )
        N = len( pos_list )
        print( 'There are %s points available (Cur: %s-th spot) for this sample at pos=%s: %s'%(
                N, i_dict[k], sample_dict[k], k ))
        RE( bps.mv( piezo.x,  pos_list[i_dict[k]%N][0]  ))
        RE( bps.mv( piezo.y,  pos_list[i_dict[k]%N][1]  ) )
        sample = RE.md['sample']
        RE( measure_saxs( exposure_t, sample= sample + '_T_%.2f'%getT() ) ) 
        #measure_saxs( exposure_t, sample= sample + '_T_%.2f'%getT() + '_runt_%.0fs'%(time.time()-t0 ) )

        i_dict[k]+=1
    print( i_dict )    
    return   i_dict







def run_melting_Tm(   TH=50, exposure_t = 0.2 , Tm = 44 , TH_sleep_time = 1800 ):
    ''' 38 - 48, 0.1 0C/min 
    
    tt0, i_dict = run_melting_Tm(   TH=29.2,  Tm = 25 , TH_sleep_time = 10  ) 


    '''  
    i_dict = {}
    for  k  in ks:
        i_dict[k] = 0
    #at RT, measure each sample at the starting point
    for  k  in ks:             
        mov_sam( k )
        pos_list = getSamMap( xlim = lim_dict[k][0], ylim = lim_dict[k][1] )
        N = len( pos_list )
        print( 'There are %s points available (Cur: %s-th spot) for this sample at pos=%s: %s'%(
                N, i_dict[k], sample_dict[k], k ))
        RE( bps.mv( piezo.x,  pos_list[i_dict[k]%N][0]  ) )
        RE( bps.mv( piezo.y,  pos_list[i_dict[k]%N][1]  ) )
        sample = RE.md['sample']
        RE( measure_saxs( exposure_t, sample= sample + '_T_%.2f'%getT() ) )
        i_dict[k]+=1

    #raise temperature to 50C
    RE(gotoT( TH ))
    #wait for 30mins
    time.sleep( TH_sleep_time  )
    #measure each sample again at the end of 50C
    for  k  in ks:             
        mov_sam( k )
        pos_list = getSamMap( xlim = lim_dict[k][0], ylim = lim_dict[k][1] )
        N = len( pos_list )
        print( 'There are %s points available (Cur: %s-th spot) for this sample at pos=%s: %s'%(
                N, i_dict[k], sample_dict[k], k ))
        RE(bps.mv( piezo.x,  pos_list[i_dict[k]%N][0]  ))
        RE( bps.mv( piezo.y,  pos_list[i_dict[k]%N][1]  ) )
        sample = RE.md['sample']
        RE( measure_saxs( exposure_t, sample= sample + '_T_%.2f'%getT() ) ) 
        i_dict[k]+=1
    #set temperature to 40C
    tt0 = time.time() #Tr = 40
    RE(setT(Tm)   )
    RE( startT() )
    return tt0, i_dict
     
#  RE( gotoT( Tm ))

def run_Tm(   tt0, i_dict,  Tm, exposure_t = 0.2 ,t_total_T40 =  30 * 60, t_interval = 5 * 60 ,   ):
    '''
    run_Tm( tt0, i_dict, Tm=29, exposure_t = 0.1, t_total_T40 = 30, t_interval = 3 ) 
    
    '''


    RE(  gotoT( Tm ) ) 
    t0 = time.time()    
    while (time.time() < ( t0 + t_total_T40 ) ):
        t1 = time.time()
        for  k  in ks:             
            mov_sam( k )
            pos_list = getSamMap( xlim = lim_dict[k][0], ylim = lim_dict[k][1] )
            N = len( pos_list )
            print( 'There are %s points available (Cur: %s-th spot) for this sample at pos=%s: %s'%(
                    N, i_dict[k], sample_dict[k], k ))
            RE ( bps.mv( piezo.x,  pos_list[i_dict[k]%N][0]  ) ) 
            RE(  bps.mv( piezo.y,  pos_list[i_dict[k]%N][1]  ) ) 
            sample = RE.md['sample']
            RE( measure_saxs( exposure_t, sample= sample + '_T_%.2f'%getT() + '_runt_%.0fs'%(time.time()-tt0 ) )            )
            i_dict[k]+=1

        if  (t_interval + ( t1 - time.time() )) > 0:
            time.sleep(  t_interval + ( t1 - time.time() )  )
    Tr = 25 
    RE( setT(Tr)   )
    RE(  stopT() ) 
    

  


def run_melting( Trange = [ 38, 48 ], dtemp = 0.1, exposure_t = 0.2, sleep_time_per_dtemp  = 60   ):
    ''' 38 - 48, 0.1 0C/min 
    
    run_melting( Trange = [ 29, 29.1 ], dtemp = 0.1, exposure_t = 0.2,  sleep_time_per_dtemp  = 1  ) 

    run_melting( Trange = [ 38, 48 ], dtemp = 0.2, exposure_t = 0.1, sleep_time_per_dtemp  = 60)

    '''
    #step one 
    #set Temperature
    T1, T2 = Trange
    tlist = np.arange( T1, T2, dtemp )
    i_dict = {}
    for  k  in ks:
        i_dict[k] = 0
    #i = 0 
    t0 = time.time()
    for T in tlist:     
        RE( gotoT( T ) ) 
        time.sleep( sleep_time_per_dtemp )
        for  k  in ks:             
            mov_sam( k )
            pos_list = getSamMap( xlim = lim_dict[k][0], ylim = lim_dict[k][1] )
            N = len( pos_list )
            print( 'There are %s points available (Cur: %s-th spot) for this sample at pos=%s: %s'%(
                 N, i_dict[k], sample_dict[k], k ))
            RE( bps.mv( piezo.x,  pos_list[i_dict[k]%N][0]  ))
            RE( bps.mv( piezo.y,  pos_list[i_dict[k]%N][1]  ) ) 
            sample = RE.md['sample']
            RE( measure_saxs( exposure_t, sample= sample + '_T_%.2f'%getT() ) ) 
            i_dict[k]+=1
    Tr = 25 
    RE (setT(Tr)       )
    RE( stopT()      ) 









def RE_run_melting( Trange = [ 38, 48 ], dtemp = 0.1, exposure_t = 0.2  ):
    ''' 38 - 48, 0.1 0C/min 
    
    RE( run_melting( Trange = [ 29, 29.1 ], dtemp = 0.1, exposure_t = 0.2  ) ) 


    '''
    #step one 
    #set Temperature
    T1, T2 = Trange
    tlist = np.arange( T1, T2, dtemp )
    i_dict = {}
    for  k  in ks:
        i_dict[k] = 0
    #i = 0 
    t0 = time.time()
    for T in tlist:     
        yield from gotoT( T )
        for  k  in ks:             
            mov_sam_re( k )
            pos_list = getSamMap( xlim = lim_dict[k][0], ylim = lim_dict[k][1] )
            N = len( pos_list )
            print( 'There are %s points available (Cur: %s-th spot) for this sample at pos=%s: %s'%(
                 N, i_dict[k], sample_dict[k], k ))
            yield from bps.mv( piezo.x,  pos_list[i_dict[k]%N][0]  )
            yield from bps.mv( piezo.y,  pos_list[i_dict[k]%N][1]  )
            sample = RE.md['sample']
            measure_saxs( exposure_t, sample= sample + '_T_%.2f'%getT() )
            i_dict[k]+=1
    Tr = 25 
    yield from setT(Tr)       
    yield from stopT()     





def RE_run_Tm(  tt0, i_dict, Tm,  exposure_t = 0.2 ,t_total_T40 =  3 * 60 * 60, t_interval = 5 * 60 ,   ):
    yield from gotoT( Tm )
    t0 = time.time()    
    while (time.time() < ( t0 + t_total_T40 ) ):
        t1 = time.time()
        for  k  in ks:             
            mov_sam_re( k )
            pos_list = getSamMap( xlim = lim_dict[k][0], ylim = lim_dict[k][1] )
            N = len( pos_list )
            print( 'There are %s points available (Cur: %s-th spot) for this sample at pos=%s: %s'%(
                    N, i_dict[k], sample_dict[k], k ))
            yield from bps.mv( piezo.x,  pos_list[i_dict[k]%N][0]  )
            yield from bps.mv( piezo.y,  pos_list[i_dict[k]%N][1]  )
            sample = RE.md['sample']
            measure_saxs( exposure_t, sample= sample + '_T_%.2f'%getT() + '_runt_%.0fs'%(time.time()-tt0 ) )            
            i_dict[k]+=1
        time.sleep(  t_interval + ( t1 - time.time() )  )
    Tr = 25 
    yield from setT(Tr)   
    yield from stopT()

def RE_run_melting_Tm(   TH=50, exposure_t = 0.2 , Tm = 44 , TH_sleep_time = 1800 ):
    ''' 38 - 48, 0.1 0C/min 
    
    RE( run_melting_Tm(   TH=50, exposure_t = 0.2 , Tm = 44 , TH_sleep_time = 1800 ) ) 


    '''  
    i_dict = {}
    for  k  in ks:
        i_dict[k] = 0
    #at RT, measure each sample at the starting point
    for  k  in ks:             
        mov_sam_re( k )
        pos_list = getSamMap( xlim = lim_dict[k][0], ylim = lim_dict[k][1] )
        N = len( pos_list )
        print( 'There are %s points available (Cur: %s-th spot) for this sample at pos=%s: %s'%(
                N, i_dict[k], sample_dict[k], k ))
        yield from bps.mv( piezo.x,  pos_list[i_dict[k]%N][0]  )
        yield from bps.mv( piezo.y,  pos_list[i_dict[k]%N][1]  )
        sample = RE.md['sample']
        measure_saxs( exposure_t, sample= sample + '_T_%.2f'%getT() )
        i_dict[k]+=1


    #raise temperature to 50C
    yield from gotoT( TH )
    #wait for 30mins
    time.sleep( TH_sleep_time  )
    #measure each sample again at the end of 50C
    for  k  in ks:             
        mov_sam_re( k )
        pos_list = getSamMap( xlim = lim_dict[k][0], ylim = lim_dict[k][1] )
        N = len( pos_list )
        print( 'There are %s points available (Cur: %s-th spot) for this sample at pos=%s: %s'%(
                N, i_dict[k], sample_dict[k], k ))
        yield from bps.mv( piezo.x,  pos_list[i_dict[k]%N][0]  )
        yield from bps.mv( piezo.y,  pos_list[i_dict[k]%N][1]  )
        sample = RE.md['sample']
        measure_saxs( exposure_t, sample= sample + '_T_%.2f'%getT() )
        i_dict[k]+=1
    #set temperature to 40C
    tt0 = time #Tr = 40
    yield from setT(Tm)   
    yield from startT()
    return tt0, i_dict


def RE_run_HT_time_temperature( T =  45, t_interval=10*60, t_total = 31*60, exposure_t = 0.1 , i_dict = None  ):
    '''      
    RE(  ) 
    '''
    #step one 
    #set Temperature 
    if i_dict is None:
        i_dict = {}
        for  k  in ks:
            i_dict[k] = 0
    yield from gotoT( T )
    t0 = time.time()
    while (time.time() < ( t0 + t_total ) ):
        t1 = time.time()
        for  k  in ks:             
            mov_sam_re( k )
            pos_list = getSamMap( xlim = lim_dict[k][0], ylim = lim_dict[k][1] )
            N = len( pos_list )
            print( 'There are %s points available (Cur: %s-th spot) for this sample at pos=%s: %s'%(
                    N, i_dict[k], sample_dict[k], k ))
            yield from bps.mv( piezo.x,  pos_list[i_dict[k]%N][0]  )
            yield from bps.mv( piezo.y,  pos_list[i_dict[k]%N][1]  )
            sample = RE.md['sample']
            measure_saxs( exposure_t, sample= sample + '_T_%.2f'%getT() + '_runt_%.0fs'%(time.time()-t0 ) )

            
            i_dict[k]+=1
        time.sleep(  t_interval + ( t1 - time.time() )  )

    Tr = 25 
    print( i_dict )
    yield from setT(Tr)   
    yield from stopT()
    return i_dict
   


def RE_run_RT_temperature(   exposure_t = 0.1 , i_dict = None  ):
    '''  
    
    RE(   run_RT_temperature(   exposure_t = 0.1 , i_dict = None  ) ) 


    '''
    #step one 
    #set Temperature 
    if i_dict is None:
        i_dict = {}
        for  k  in ks:
            i_dict[k] = 0
    for  k  in ks:             
        mov_sam_re( k )
        pos_list = getSamMap( xlim = lim_dict[k][0], ylim = lim_dict[k][1] )
        N = len( pos_list )
        print( 'There are %s points available (Cur: %s-th spot) for this sample at pos=%s: %s'%(
                N, i_dict[k], sample_dict[k], k ))
        yield from bps.mv( piezo.x,  pos_list[i_dict[k]%N][0]  )
        yield from bps.mv( piezo.y,  pos_list[i_dict[k]%N][1]  )
        sample = RE.md['sample']
        measure_saxs( exposure_t, sample= sample + '_T_%.2f'%getT() )
        #measure_saxs( exposure_t, sample= sample + '_T_%.2f'%getT() + '_runt_%.0fs'%(time.time()-t0 ) )

        i_dict[k]+=1
    print( i_dict )    
    return   i_dict
   




# def run_one_temperature( T =  [ 'T0', 45, 'T0C' ] ,  exposure_t = 0.1  ):
#     '''  
    
#     RE(  ) 


#     '''
#     #step one 
#     #set Temperature 
#     i_dict = {}
#     for  k  in ks:
#         i_dict[k] = 0
#     #i = 0 
#     T0 =  getT()
#     for   T in Tlist:     
#         if T == 'T0':
#             pass
#         elif T == 'T0C':
#             yield from gotoT( T0 )
#         else:
#             yield from gotoT( T )
#         for  k  in ks:             
#             mov_sam_re( k )
#             pos_list = getSamMap( xlim = lim_dict[k][0], ylim = lim_dict[k][1] )
#             N = len( pos_list )
#             print( 'There are %s points available (Cur: %s-th spot) for this sample at pos=%s: %s'%(
#                  N, i_dict[k], sample_dict[k], k ))
#             yield from bps.mv( piezo.x,  pos_list[i_dict[k]%N][0]  )
#             yield from bps.mv( piezo.y,  pos_list[i_dict[k]%N][1]  )
#             measure_saxs( exposure_t, sample=  RE.md['sample'] )
#             i_dict[k]+=1
#     Tr = 25 
#     yield from setT(Tr)       
#     yield from stopT()     




def Measure_All():



    ps4 =  getSamMap(  xlim=[-16760,-16760+10], ylim=[3371,  1500 ],  step_size = [100, -50], rot_angle = 0 )
    Measure_Map( sample ='0126TTH_cappilary1',  ps= ps4   ) 



def Check_All():

    ps1 = getSamMap(xlim=[4500, 8500], ylim=[-4390, 610 ] )
    ps2 = getSamMap(xlim=[-14000, -8500], ylim=[ -4520, -1100 ] )
    ps3 = getSamMap(xlim=[-24800,-21100], ylim=[-4630,  -330] )
    N = len(ps1) + len(ps2) + len(ps3)
    print( N, N/3600 )

 




def getSamMap(  xlim=[4500, 8500], ylim=[-4390, 610 ],  step_size = [200, 30], rot_angle = 0 ):
    #change x Y position here

    Ps_grid = []
    px = np.arange( xlim[0],xlim[1]+step_size[0]*0, step_size[0])
    py = np.arange( ylim[0],ylim[1]+step_size[1]*0, step_size[1])
    rot_angle = np.deg2rad(rot_angle)
    delta_x = np.cos(rot_angle)
    delta_y = np.sin(rot_angle)
    rot_matrix = np.array(((delta_x, -delta_y),(delta_y, delta_x)))
    for y in   py:
        for x in   px:
            Ps_grid.append(  [ x,y ]   )
    Ps_grid = np.array(Ps_grid)
    Ps_grid_rot = np.dot(rot_matrix,Ps_grid.T).T 
    return Ps_grid_rot





def Measure_Map(  t = 1 ,  sample = 'O139',  ps=None, pz= 8000,  username = 'FLu', ):
    '''
    Ps = getSamMap()
    Measure_Map( sample = 'test',  ps= Ps[:2]   ) 
    
    '''

    RE(bps.mov( piezo.z, pz  ))
    if ps is None:
        ps = getSamMap( )
    for (px,py) in ps:
        print( px, py )
        RE(bps.mov( piezo.x, px  ))
        RE(bps.mov( piezo.y, py  ))
        dets = [pil1M, pil900KW]
        name_fmt = "{sample}_x{x:05.2f}_y{y:05.2f}_z{z_pos:05.2f}_det{saxs_z:05.2f}m_expt{t}s"
        sample_name = name_fmt.format(
            sample=sample,
            x=np.round(piezo.x.position, 2),
            y=np.round(piezo.y.position, 2),
            z_pos=piezo.z.position,
            saxs_z=np.round(pil1m_pos.z.position, 2),
            t=t,
            #scan_id=RE.md["scan_id"],
        )
        det_exposure_time(t, t)
        # sample_name='test'
        sample_id(user_name=user_name, sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")
        print("Collect data here....")
        RE(  bp.count(dets, num=1) ) 
        if camera:
            #path= '/nsls2/xf12id2/data/images/users/2022_3/308052_YZhang/OAV/'
            #caput( 'XF:12IDC-BI{Cam:SAM}TIFF1:FilePath', path ) 
            caput( 'XF:12IDC-BI{Cam:SAM}TIFF1:FileName', sample_name  )
            caput( 'XF:12IDC-BI{Cam:SAM}TIFF1:WriteFile', 1 )       





from epics import caget, caput

def set_fs5(   ):
    #path= '/nsls2/xf12id2/data/images/users/2022_3/308052_YZhang/OAV/'
    path= '/nsls2/data/smi/legacy/results/data/2024_1/313760_FLu/OAV/'
    caput( 'XF:12IDC-BI{Cam:SAM}TIFF1:FilePath', path ) 




 




def get_current_time():
    return datetime.today().strftime("%Y-%m-%d-%H-%M-%S")



def measure_current_sample(t=1, waxs_angles=[0, 20], sample=None):

    """t0=time.time();RE(measure_one_multi_angle_wsaxs());run_time(t0)"""
    maxA = np.max(waxs_angles)
    for waxs_angle in waxs_angles:
        print("here we go ... ")
        if waxs_angle == maxA:
            yield from measure_wsaxs(t=t, waxs_angle=waxs_angle, sample=sample)
        else:
            yield from measure_waxs(t=t, waxs_angle=waxs_angle, sample=sample)


def measure_saxs(t=1, att="None", dx=0, dy=0, user_name=username, sample=None):

    """RE( measure_saxs( sample = 'AgBH_12keV' ) )"""

    if sample is None:
        # sample = RE.md['sample']
        sample = RE.md["sample_name"]
    dets = [pil1M]
    if dy:
        yield from bps.mvr(piezo.y, dy)
    if dx:
        yield from bps.mvr(piezo.x, dx)
    name_fmt = "{sample}_x{x:05.2f}_y{y:05.2f}_z{z_pos:05.2f}_det{saxs_z:05.2f}m_expt{t}s"


    sample_name = name_fmt.format(
        sample=sample,
        x=np.round(piezo.x.position, 2),
        y=np.round(piezo.y.position, 2),
        z_pos=piezo.z.position,
        saxs_z=np.round(pil1m_pos.z.position, 2),
        t=t,
        #scan_id=RE.md["scan_id"],
    )
    det_exposure_time(t, t)
    # sample_name='test'
    sample_id(user_name=user_name, sample_name=sample_name)
    print(f"\n\t=== Sample: {sample_name} ===\n")
    print("Collect data here....")
    yield from bp.count(dets, num=1)
    #sample_id(user_name="test", sample_name="test")
    #RE.md["sample_name"] = ''
    #RE.md["sample"] = ''


def measure_waxs(
    t=1, waxs_angle=20, att="None", dx=0, dy=0, user_name=username, sample=None
):
    """ 
    RE(  measure_waxs() )  # take default parameters

    RE( measure_waxs( t = 1, waxs_angle = 0   ) )


    """

    if sample is None:
        sample = RE.md["sample"]
        # sample = RE.md['sample_name']
    yield from bps.mv(waxs, waxs_angle)
    #dets = [pil900KW, pil300KW]
    dets = [pil900KW]

    # att_in( att )
    if dx:
        yield from bps.mvr(piezo.x, dx)
    if dy:
        yield from bps.mvr(piezo.y, dy)
    #name_fmt = "{sample}_x{x_pos:05.2f}_y{y_pos:05.2f}_z{z_pos:05.2f}_waxs{waxs_angle:05.2f}_expt{expt}s"
    name_fmt = "{sample}_x{x_pos:05.2f}_y{y_pos:05.2f}_z{z_pos:05.2f}_det{saxs_z}_waxs{waxs_angle:05.2f}_expt{expt}s"

    sample_name = name_fmt.format(
        sample=sample,
        x_pos=piezo.x.position,
        y_pos=piezo.y.position,
        z_pos=piezo.z.position,
        saxs_z=np.round(pil1m_pos.z.position, 2),
        waxs_angle=waxs_angle,
        expt=t,
        #scan_id=RE.md["scan_id"],
    )
    det_exposure_time(t, t)
    sample_id(user_name=user_name, sample_name=sample_name)
    print(f"\n\t=== Sample: {sample_name} ===\n")
    print("Collect data here....")
    yield from bp.count(dets, num=1)
    # att_out( att )
    # sample_id(user_name='test', sample_name='test')

    #RE.md["sample_name"] = ''
    #RE.md["sample"] = ''


def measure_wsaxs(
    t=1, waxs_angle=20, att="None", dx=0, dy=0, user_name=username, sample=None
):
    """RE( measure_wsaxs( sample = 'AgBH_12keV' ) )"""

    if sample is None:
        # sample = RE.md['sample']
        sample = RE.md["sample_name"]
    yield from bps.mv(waxs, waxs_angle)
    #dets = [pil900KW, pil300KW, pil1M]
    dets = [pil900KW,   pil1M]

    if dx:
        yield from bps.mvr(piezo.x, dx)
    if dy:
        yield from bps.mvr(piezo.y, dy)
    name_fmt = "{sample}_x{x_pos:05.2f}_y{y_pos:05.2f}_z{z_pos:05.2f}_det{saxs_z}_waxs{waxs_angle:05.2f}_expt{expt}s"

    sample_name = name_fmt.format(
        sample=sample,
        x_pos=piezo.x.position,
        y_pos=piezo.y.position,
        z_pos=piezo.z.position,
        saxs_z=np.round(pil1m_pos.z.position, 2),
        waxs_angle=waxs_angle,
        expt=t,
        #scan_id=RE.md["scan_id"],
    )

    det_exposure_time(t, t)
    sample_id(user_name=user_name, sample_name=sample_name)
    print(f"\n\t=== Sample: {sample_name} ===\n")
    print("Collect data here....")
    yield from bp.count(dets, num=1)
    # att_out( att )
    # sample_id(user_name='test', sample_name='test')
    #RE.md["sample_name"] = ''
    #RE.md["sample"] = ''


def measure_series_multi_angle_wsaxs(
    t=[1], waxs_angles=[0,  20   ], dys=[0]
):

    """
    
    t0=time.time();RE(measure_series_multi_angle_wsaxs(waxs_angles=[0,  20   ]));run_time(t0)

    

    """

    ks = list(sample_dict.keys())  # [:8 ]
    maxA = np.max(waxs_angles)
    for waxs_angle in waxs_angles:
        for k in ks:
            print(k)
            yield from mov_sam_re(k)
            for dy in dys:
                print(dy)
                print("here we go ... ")
                for ti in t:
                    RE.md["sample_name"] = sample_dict[k]
                    if waxs_angle == maxA:
                        yield from measure_wsaxs(
                            t=ti, waxs_angle=waxs_angle, att="None", dy=dy
                        )
                    else:
                        yield from measure_waxs(
                            t=ti, waxs_angle=waxs_angle, att="None", dy=dy
                        )



def measure_series_saxs(t=[1]):

    """
    t0=time.time();RE(measure_series_saxs());run_time(t0)
    
    """



    ks = list(sample_dict.keys())  # [:8 ]    
    dy = -50
    for k in ks:
        print(k)
        dy=0
        yield from mov_sam_re(k, dy=0)
        for ii, ti in enumerate(t):
            RE.md["sample_name"] = sample_dict[k]
            yield from measure_saxs(t=ti, att="None", dy=dy)



def run_time(t0):
    dt = (time.time() - t0) / 60
    print("The Running time is: %.2f min." % dt)



def snap_waxs(t=0.1):
    dets = [pil900KW]
    sample_id(user_name="test", sample_name="test")
    det_exposure_time(t,t )
    yield from (bp.count(dets, num=1))


def snap_saxs(t=0.1):
    'test '
    dets = [pil1M]
    sample_id(user_name="test", sample_name="test")
    det_exposure_time(t,t )
    yield from (bp.count(dets, num=1))


def mov_sam(pos, dy=0):
    px, py = pxy_dict[pos]
    RE(bps.mv(piezo.x, px))
    RE(bps.mv(piezo.y, py + dy))
    sample = sample_dict[pos]
    print("Move to pos=%s for sample:%s" % (pos, sample))
    RE.md["sample"] = sample
    RE.md["sample_name"] = sample





def name_sam(pos):
    sample = sample_dict[pos]
    print("Move to pos=%s for sample:%s" % (pos, sample))
    RE.md["sample"] = sample
    RE.md["sample_name"] = sample


def check_sample_loc(sleep=1):
    ks = list(sample_dict.keys())
    for k in ks:
        mov_sam(k)
        time.sleep(sleep)


def movx(dx):
    RE(bps.mvr(piezo.x, dx))

def movy(dy):
    RE(bps.mvr(piezo.y, dy))

def get_posxy():
    return round(piezo.x.user_readback.value, 2), round(piezo.y.user_readback.value, 2)

def move_waxs(waxs_angle=8.0):
    RE(bps.mv(waxs, waxs_angle))


def measure_pindiol_current():
    fs.open()
    yield from bps.sleep(0.3)
    pd_curr = pdcurrent1.value
    fs.close()
    print("--------- Current pd_curr {}\n".format(pd_curr))
    return pd_curr


def check_sample_name(name):
    """
    Convert special characters to underscore so detectors will not complain
    """
    name = name.translate({ord(c): "_" for c in "=!@#$%^&*{}:/<>?\|`~+"})
    return name


#########End of the functions


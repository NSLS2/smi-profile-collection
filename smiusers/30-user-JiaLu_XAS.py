'''
2024/7/12, Friday Afternoon
#Scan Energy from 11150 to 11400 for Ir edge

setthreshold energy 16100 autog 11000

/nsls2/data/smi/legacy/results/data/2024_2/00003_YZhang


proposal_id('2024_2', '00003_YZhang')
Energy: 11.5 keV,   low divergence, in air
setthreshold energy 11500 autog 7500


sample_id(user_name = 'YZhang', sample_name = 'test' )
RE(bps.mv(waxs, 0))
RE(bp.count([pil1M, amptek, pil900KW ]))





In [1617]: sample_id(user_name = 'WL', sample_name = 'B0500_Ir_Edge' )
In [1618]: RE(bp.count([pil1M, amptek, pil900KW ]))
In [1621]: RE(bps.mv(waxs, 0))
In [1622]: RE(bp.count([pil1M, amptek, pil900KW ]))
In [1623]: RE(bps.mv(waxs, 20))
In [1624]: RE(bp.count([pil1M, amptek, pil900KW ]))

np.arange( 11150,11185, 5)
np.arange( 11185, 11195,  2 )
np.arange( 11195, 11246,  0.2 )
np.arange(  11246, 11260,  0.5 )
np.arange(  11261, 11282,  1 )
np.arange(  11282, 11345, 1.5 )
np.arange(   11345, 11400, 2 )


RUN1: 
B0500_IrE_FB_Bpst2s
Full beam, dets = [pil1M, pil900KW,  amptek ]
Sleep 2S between each energy
Scan E, E_reverse 

RE( Ir_edge_measurments_2024_7_12(t=1, sample = 'B0500_IrE_FB_Bpst2s'  ) ) 


RUN2: 
B0500_IrE_FB
Full beam, dets = [pil1M, pil900KW,  amptek ]
Sleep 0 between each energy
Scan E #, E_reverse 

RE( Ir_edge_measurments_2024_7_12(t=1, sample = 'B0500_IrE_FB_NoBpst', reverse=False, bps_sleep_time=0 ) )



RUN3
B0500_IrE_AB
Attenuated beam (4X) 
remove the beam stop
Sleep 0 between each energy
Scan E , E_reverse 
RE( Ir_edge_measurments_2024_7_12(t=1, sample = 'B0500_IrE_AB_NoBpst', reverse=True, bps_sleep_time=0 ) )



RUN4
Empty_AB
Attenuated beam (4X) 
remove the beam stop
Sleep 0 between each energy
Scan E 
RE( Ir_edge_measurments_2024_7_12(t=1, sample = 'Emp_IrE_AB_NoBpst', reverse=True, bps_sleep_time=0 ) )


sample_id(user_name = 'YZhang', sample_name = 'test' )
RE(bp.count([pil1M, amptek, pil900KW ]))

 





'''

user_name = 'JLi'


sample_dict = {  
                 1: 'Sam_A',  
                 2: 'Sam_B',  
                 3: 'Sam_C',  
                 4: 'Sam_D',
                 5: 'Sam_Empt',  
                 6: 'Sam_E', 
}
pxy_dict = {  
              1:  ( 45182, -2500     ) ,  
              2:   (32282, -2500) ,
              3:  ( 6882, -2500     ) ,
              4:  ( -12168, -2500   ) ,  
              5:  ( -18519, -2400     ) , 
              6:  ( -31219, -2700     ) ,  
          
 
  }

dx =  0
dy = 200 #-2000
ks = np.array(list((sample_dict.keys())))
pxy_dict = {k: [pxy_dict[k][0] + dx, pxy_dict[k][1] + dy] for k in ks}

x_list = np.array(list((pxy_dict.values())))[:, 0]
y_list = np.array(list((pxy_dict.values())))[:, 1]
sample_list = np.array(list((sample_dict.values())))


def run():    
    '''
    
    run()

    '''
    for  k  in ks:             
        mov_sam( k )
        RE(  S_edge_one_sample( sample = RE.md['sample']) )



def S_edge_one_sample(t=1, sample = None, reverse=False, bps_sleep_time=2,  ):
    '''

    RE( S_edge_one_sample(t=1, sample = 'test'  ) ) 
 


    '''

    dets = [pil1M ] #, pil900KW,  amptek ]
    det_exposure_time(t, t)
    Elist = np.arange( 2460, 2480.2, .2) #[:2]

    name_fmt = "{sample}_pos1_{energy}eV_bpm{xbpm}"
    for e in Elist:        
        yield from bps.mv(energy, e)
        if bps_sleep_time !=0:
            yield from bps.sleep(bps_sleep_time)
        if xbpm2.sumX.get() < 100:
            yield from bps.sleep(2)
            yield from bps.mv(energy, e)
            yield from bps.sleep(2)        
        bpm = xbpm2.sumX.get()
        sample_name = name_fmt.format(sample=sample, energy="%6.2f"%e,  xbpm="%4.3f"%bpm)
        sample_id(user_name=user_name, sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")
        yield from bp.count(dets, num=1)

    if reverse:
        name_fmt = "{sample}_pos2_{energy}eV_wa_{wa}_bpm{xbpm}"
        for e in Elist[::-1]:
            yield from bps.mv(energy, e)
            yield from bps.sleep(2)
            if xbpm2.sumX.get() < 10:
                yield from bps.sleep(2)
                yield from bps.mv(energy, e)
                yield from bps.sleep(2)        
            bpm = xbpm2.sumX.get()
            sample_name = name_fmt.format(sample=sample, energy="%6.2f"%e, wa=20,  xbpm="%4.3f"%bpm)
            sample_id(user_name=user_name, sample_name=sample_name)
            print(f"\n\t=== Sample: {sample_name} ===\n")
            yield from bp.count(dets, num=1)


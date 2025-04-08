


'''

# load this macro
#   %run -i /home/xf12id/.ipython/profile_collection/startup/users/30-user-QYu_2024C3_GIX.py
proposal_id('2024_3', '300010_QYu', analysis=True)
proposal_id('2024_3', '300011_PGuo', analysis=True)
sample_id(user_name='test', sample_name=f'test{get_scan_md()}')




  # SAXS distance , 8 meter
# 1M [  -2.77, -61., 5000  ]
# beam stop [ .9, 288.99,  13  ], a rod
# beam center   [ 475, 555     ]


--> 

# beam center [ 474, 795 ]
# 1M [  -2.77, -20, 8000  ]
# beamstop_save()



pin positiion: 
PX: 10186, 
PZ: 0 
PZ:  1400
chi: 7
theta: 0 

HEX:
X: 0
Y: -8
Z: 7
theta: 2
phi: -5


For AgBH sample
PX: -34500
PZ: 0 
PZ:  1400
chi: 7.6
theta: 0 

HEX:
X: 0
Y: 5
Z: 7
theta: 2
phi: -5



%run -i  ~/.ipython/profile_collection/startup/users/30-user-QYu_2024C3_GIX.py




'''


from epics import caget, caput

# username = 'NREL_SR'
# user_name = 'NREL_SR'


username = 'PGuo'
user_name = 'PGuo'

 
##RU1
#sample_dict = {   1:  'Nov_7_1_SiWafer',   } 
#pxy_dict = {    1:[ 21000, 0 ] ,     }


##RU2, for test the frame number
#sample_dict = {   1:  'Nov_7_1_SiWafer2',   } 
#pxy_dict = {    1:[ 21000, 0 ] ,     }
 
 
##RU3, for test the frame number
#sample_dict = {   1:  'Nov_7_1_SiWafer_AuAseembly',   } 
#pxy_dict = {    1:[ 20600, 0 ] ,     }




##RUX1, load a new Si wafer on the sample holder, need to re-run the alignment
# sample_dict = {   1: '1', 2: 'X111', 3: '55', 4: '26', 5: '111'   } 
# pxy_dict = {    1:[ 50000, 0 ] , 2: [30400, 0  ]  , 3: [15400, 0  ] , 4: [ -600, 0  ] ,  5: [-18100, 0  ]    }



##RUX2, load a new Si wafer on the sample holder, need to re-run the alignment
# sample_dict = {   1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6:'6', 7: '7'   } 
# pxy_dict = {    1:[ -38600, 0 ] , 2: [-23600, 0  ]  , 3: [-12600, 0  ] , 4: [2900, 0  ] ,  5: [18900, 0  ] ,
#             6: [ 34000, 0], 7: [50900, 0 ]   }


# ##RUX3,
# sample_dict = {   1: 'S1A', 2: 'S1B', 3: 'S2A', 4: 'S2B'   } 
# pxy_dict = {    1:[ 48000, 0 ] , 2: [ 21000, 0  ]  , 3: [-3000, 0  ] , 4: [-30000, 0  ]   }


# ##RUX4,
# sample_dict = {   1: 'S3A', 2: 'S3B', 3: 'S4A', 4: 'S4B'   } 
# pxy_dict = {    1:[ 50000, 0 ] , 2: [ 24000, 0  ]  , 3: [-7500, 0  ] , 4: [-32000, 0  ]   }


# # ##RUX5,
# sample_dict = {   1: 'S5A', 2: 'S5B', 3: 'S6A', 4: 'S6B'   } 
# pxy_dict = {    1:[ 48500, 0 ] , 2: [ 23000, 0  ]  , 3: [-1500, 0  ] , 4: [-24500, 0  ]   }


# ##RUX5,
sample_dict = {   1: 'S7A', 2: 'S7B', 3: 'S8A', 4: 'S8B'   } 
pxy_dict = {    1:[ 48500, 0 ] , 2: [ 23000, 0  ]  , 3: [-1500, 0  ] , 4: [-24500, 0  ]   }






ks = np.array(list((sample_dict.keys())))
x_list = np.array(list((pxy_dict.values()))) [:, 0]
y_list = np.array(list((pxy_dict.values()))) [:, 1]
sample_list = np.array(list((sample_dict.values())))





def insitu_tgix_samples(  Aligned_Dict,  run_time= 3600 * 1 , sleep_time = 5      ):  

    '''

    Aligned_Dict =   align_gix_loop_samples()      
    
    RE( insitu_tgix_samples(  Aligned_Dict,  run_time= 3600 * 1 , sleep_time = 5      ) ) 
    

    '''


    t=1
    dets = [pil1M, pil900KW]
    incident_angle=[      0.15   ]  
    angle_arc = np.array( incident_angle )
    #x_shift_array = np.array( [ -400, 0, 400 ])
    x_shift_array = np.array( [ -5000, 0, 5000 ]) #25000 #
    y_shift_array = np.array( [  0  ])

    username = user_name
    align= False 
    camera = False #True
    waxs_angle = 20
    #sleep_time = 60  #how frequently we collect the data
    # bps.mv(waxs, 15)   
    CTS = 0   
    M, _, _ = get_motor(   )   

    ks = list( sample_dict.keys() ) 
    t0 = time.time()
    while (time.time() - t0 ) < run_time:
        print('The CTS is %s ************ '%CTS)
         
        for ii, k in enumerate(ks): #loop samples
            x = pxy_dict[k][0]
            sample = sample_dict[k] 

            yield from bps.mv(M.x, x) #move to next sample              
            TH = Aligned_Dict[ii]['th']  
            YH = Aligned_Dict[ii]['y']  
            yield from bps.mv(M.y, YH)  
            yield from bps.mv(M.th, TH)  
        

            th_meas = angle_arc + TH #piezo.th.position 
            th_real = angle_arc	         
            x_pos_array = x + x_shift_array                
            y_pos_array = YH + y_shift_array
            for j, x_meas in enumerate( x_pos_array) : # measure at a few x positions
                yield from bps.mv(M.x, x_meas)                               
                for i, th in enumerate(th_meas): #loop over incident angles
                    yield from bps.mv(M.th, th)  
                    name_fmt = "{sample}_{th:5.4f}deg_x{x:05.2f}_y{y:05.2f}_z{z_pos:05.2f}_det{saxs_z:05.2f}m_waxs{waxs_angle:05.2f}_expt{t}s"
                    sample_name = name_fmt.format(sample=sample,th=th_real[i],x=np.round(M.x.position, 2),y=np.round(M.y.position, 2), z_pos=M.z.position,saxs_z=np.round(pil1m_pos.z.position, 2), waxs_angle=waxs_angle,t=t )
                    sample_id(user_name=  user_name , sample_name=sample_name)                     
                    print(f'\n\t=== Sample: {sample_name} ===\n') 
                    yield from bp.count( dets, num=1)
                    det_exposure_time(t,t)    
                    if camera: 
                        save_ova( sample_name )
                        save_hex( sample_name )     

        CTS +=1
        time.sleep(  sleep_time  )






def align_gix_loop_samples( inc_ang = 0.15,   ):      
    '''      

    Aligned_Dict =     align_gix_loop_samples(   )  

    #  0.48 -0.384 
      

     '''
    # define names of samples on sample bar     
    M, _, _ = get_motor(  ) 
    N = len( x_list )
    assert len(x_list) == len(sample_list), f'Sample name/position list is borked'  
    print('here')   
    Aligned_Dict = {}
    for ii, (x, sample) in enumerate(zip(x_list,sample_list)):    #loop over samples on bar
        if ii == N-1:
            back_to_measureMode = True
        else:
            back_to_measureMode = False     
        print('Do alignment for sample: %s'%sample )
        RE( bps.mv(M.x, x) ) #move to next sample  
        if motor == 'pizeo':             
            RE( alignement_gisaxs(inc_ang , back_to_measureMode=back_to_measureMode ) ) #run alignment routine          
        else:             
            RE( alignement_gisaxs_hex(inc_ang ,back_to_measureMode=back_to_measureMode ) ) #run alignment routine  
        M, TH, YH = get_motor(  )     
        Aligned_Dict[ii]={}
        Aligned_Dict[ii]['th']  = TH
        Aligned_Dict[ii]['y']  = YH
        print( ii, TH, YH )
        RE( smi.modeMeasurement() ) 
        print('THe alignment is DOne!!!')
    return Aligned_Dict
 

 
print('here@@@@@@@@@@')
def run_gix_loop_wsaxs(t=1, mode = ['saxs', 'waxs' ],  
                       angle_arc = np.array([ 0.08, 0.12, 0.15, 0.2, 0.25,  0.3, .5, 1  ]),
                       waxs_angle_array = np.array( [  0, 10,  15     ] ) ,  
                       x_shift_array =  np.array( [  -1000, 0, 1000 ]), #np.linspace(-1, 1, 5),                      
                       Aligned_Dict = None ):        
       
    '''      
      Aligned_Dict =     align_gix_loop_samples( inc_ang = 0.15  )   

      RE(  run_gix_loop_wsaxs(  Aligned_Dict = Aligned_Dict ) )



     '''    

    assert len(x_list) == len(sample_list), f'Sample name/position list is borked' 
    if Aligned_Dict is None:    
        Aligned_Dict = align_gix_loop_samples( inc_ang = 0.15 )  
    print( Aligned_Dict )  
    M, _, _ = get_motor(   )  
    for waxs_angle in waxs_angle_array: # loop through waxs angles        
        yield from bps.mv(waxs, waxs_angle)     
        dets = get_dets( waxs_angle = waxs_angle, mode = mode )                       
        det_exposure_time(t,t)                  
        for ii, (x, sample) in enumerate(zip(x_list,sample_list)):    #loop over samples on bar                
            yield from bps.mv(M.x, x )             
            TH = Aligned_Dict[ii]['th']  
            YH = Aligned_Dict[ii]['y']  
            yield from bps.mv(M.y, YH)  
            yield from bps.mv(M.th, TH)  
            th_meas = angle_arc + TH #piezo.th.position 
            th_real = angle_arc	         
            x_pos_array = x + x_shift_array   
            for j, x_meas in enumerate( x_pos_array) : # measure at a few x positions
                yield from bps.mv(M.x, x_meas)                 
                for i, th in enumerate(th_meas): #loop over incident angles
                    yield from bps.mv(M.th, th)  
                    name_fmt = "{sample}_{th:5.4f}deg_x{x:05.2f}_y{y:05.2f}_z{z_pos:05.2f}_det{saxs_z:05.2f}m_waxs{waxs_angle:05.2f}_expt{t}s"
                    sample_name = name_fmt.format(sample=sample,th=th_real[i],x=np.round(M.x.position, 2),y=np.round(M.y.position, 2), z_pos=M.z.position,saxs_z=np.round(pil1m_pos.z.position, 2), waxs_angle=waxs_angle,t=t,
                    #scan_id=RE.md["scan_id"],
                )
                    sample_id(user_name=  user_name , sample_name=sample_name)                     
                    print(f'\n\t=== Sample: {sample_name} ===\n') 
                    yield from bp.count( dets, num=1)
                    det_exposure_time(t,t)    
            #print( 'HERE#############')
    sample_id(user_name='test', sample_name='test')
    det_exposure_time(0.5)


 



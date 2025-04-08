##Collect data:

# SMI: 2022/7/8
# proposal_id('2022_2', '308895_SSYang')
# proposal_id('2022_2', '308895_SSYang_0710')


############for test
# 5 m, beam stop:  1.9
# 1M, 0.7 ,  486, 565  #direct beam center
# 1M, X -8.3, 435, 564
# 1M, X -5.3,   452, 565
# 1M, X -2.3,   469, 565
#######################


#  RE( shopen() )  # to open the beam and feedback
#  RE( shclose())

#  %run -i
# 5 m, beam stop:  1.9  paddle 289l Y: -13
# 5m, 1M, x=1.04, Y = -61.4
##the correspond beam center is [ 490, 557 ]
# for transimission, the direct beam is behind the chip gap
# beamstop_save()
# Energy: 12 kev
# SAXS distance 5000
#   setthreshold energy 12000 autog 7000


# gix, move detector 1M  to x=6.04, Y = -61.4  , beam center is [ 519, 557 ]
#  beamstop_save()
# lakeshore, make PID 60, 5, 5
# output channel is 1 input channel is A,


# gix, move detector 1M  to x=6.04, Y =  0  , beam center is [ 516, 916   ]
# 4 m, beam stop:  2.2  paddle 289l Y: -13
#  beamstop_save()

# gix, move detector 1M  to x=11.04, Y =  0  , beam center is [ 545, 916   ]
# 4 m, beam stop:  2.2  paddle 289l Y: -13
#  beamstop_save()

# gix, move detector 1M  to x= -5, Y =  -30  , beam center is [ 453, 740    ]
# 4 m, beam stop:  2.2  paddle 289l Y: -13
#  beamstop_save()

# gix, move detector 1M  to x= -5, Y =  -20  , beam center is [ 453,  798     ]
# 4 m, beam stop:  2.2  paddle 289l Y: -13
#  beamstop_save()
# for heating setup of thin film, PY 3000, hexY = 1, use one post
# for thin film ex-situ, PY 2500 , hexY = 1


"""
#run transimission:
# t0=time.time();measure_series_multi_angle_wsaxs();run_time(t0) 



#run thin film
#   RE( run_T_giwsaxs())
# 
RE( run_T_giwsaxs(   x_list=x_list, sample_list=sample_list,   t=1, username =  username, 
         inc_angles=[  0.05,  0.12, 0.15,  0.18,  0.3 ], waxs_angles = [ 15   ] ,
         x_shift_array = [ -500,   0,    500 ]  ,  
             Tlist= [ 30 , 40 , 50 , 60, 65, 70, 75, 80, 85, 90, 100, 110, 120, 110, 100, 90, 85, 80, 75, 70, 65, 60, 50, 40, 30], 
         saxs_on=True,) )

RE( run_T_giwsaxs(   x_list=x_list, sample_list=sample_list,   t=1, username =  username, 
         inc_angles=[  0.05,  0.12, 0.15,  0.18,  0.3 ], waxs_angles = [ 15   ] ,
         x_shift_array = [ -500,   0,    500 ]  ,  
             Tlist= [ 30 , 40 , 50 , 60, 65, 70, 75, 80, 85, 90, 100, 120, 100, 90, 85, 80, 75, 70, 65, 60, 30], 
         saxs_on=True,) )

RE( run_T_giwsaxs(   x_list=x_list, sample_list=sample_list,   t=1, username =  username, 
         inc_angles=[  0.05,  0.12, 0.15,  0.18,  0.3 ], waxs_angles = [ 15   ] ,
         x_shift_array = [ -500,   0,    500 ]  ,  
             Tlist= [ 30 ], 
         saxs_on=True,) )

"""


from datetime import datetime

username = "SSY"
user_name = "SSY"


# PZ = -4800, Y = -700
#
# # First Run, 9 samples, transmission

# sample_dict = {  1: 'Au-olam_5nm-YZ',  2: 'Au-LC1-0.1', 3: 'Au-LC2-0.1',4: 'Au-LC3-0.1', 5: 'Au-LC1-0.01',
#  6: 'Au-LC2-0.01',7: 'Au-LC3-0.01',8: '5CB', 9:'Au-OLAM-SY' }
# pxy_dict = {  1:  ( -45200, -700  ),  2:  ( -38400, -700  ),  3:  (  -32100, -700  ),
# 4:  (  -26050, -700  ),    5:  (  -19550, -700  ),    6:  (  -13300, -700  ),    7:  (  -6950, -700  ),
# 8:  (  -650, -700  ),    9:  (  -6099, -700  ),
#             } ## No 9 position is not correct.


# sample_dict = {  1:'Au-OLAM-SY_redo' }
# pxy_dict = {  1: ( 6099, -700  ),
#             } ## Re-run No 9 in the same holder


# sample_dict = {  1: 'MG-YLX',  2: 'MG-27', 3: 'MG-28',4: 'MG-427', 5: 'MG-6',
#  6: 'MG-29',7: 'MG-21',8: 'MG-22', 9:'NR-1' ,
#  10: 'NR-2', 11: 'MG-16',12: 'VO2',13: 'FE3O4-23', 14:'FE3O4-24' , 15:'Gd2O3'
#  }

# pxy_dict = {  1:  ( -43950, -700  ),  2:  ( -37550, -700  ),  3:  (  -31700, -700  ),
# 4:  (  -25400, -700  ),    5:  (  -19100, -700  ),    6:  (  -12800, -700  ),    7:  (  -5950, -700  ),
# 8:  (  600, -700  ),    9:  (  6900, -700  ),
# 10:  (  12950, -700  ),    11:  ( 19550, -700  ),    12:  (  25800, -700  ),    13:  (  31900, -700  ),
# 14:  (  38850, -700  ),    15:  (  44600, -700  ),
#             }

# sample_dict = {  1: 'VO2-LC2-0.1',  2: 'VO2-LC2-0.01', 3: 'VO2-LC3-0.1',4: 'VO2-LC3-0.01',
#  5: 'Gd2O3-LC2-0.1',6: 'Gd2O3-LC2-0.01',7: 'Gd2O3-LC3-0.1', 8:'Gd2O3-LC2-0.01',
#  9: 'NR1-LC2-0.1', 10: 'NR1-LC2-0.01',11: 'NR1-LC3-0.1', 12: 'NR1-LC3-0.01' ,
#  13: 'NR2-LC2-0.1', 14: 'NR1-LC2-0.01', 15: 'MG-435'
#  }

# pxy_dict = {  1:  ( -43000, 0  ),  2:  ( -36500, 0  ),  3:  (  -30000, 0  ),
# 4:  (  -23500, 0  ),    5:  (  -17500, 0  ),    6:  (  -11000, 0  ),    7:  (  -5000, 0  ),
# 8:  (  1500, 0  ),    9:  (  8000, 0  ),
# 10:  (  14500, -1000  ),    11:  ( 21000, 0  ),    12:  (  27000, 0  ),  13:  (  33500, 0  ),
# 14:  ( 40000, 0  ),    15:  (  46000, -1000  ),   }


# To be run:# sample_dict = {  1: 'NR2-LC3-0.1',  2: 'NR2-LC3-0.01', 3: 'Fe3O4-LC2-0.1',4: 'Fe3O4-LC2-0.01',
#  5: 'Fe3O4-LC3-0.1',6: 'Fe3O4-LC3-0.01',7: 'LC1S-1', 8:'LC2S-1',
#  9: 'LC3S-1', 10: 'LC2P-1',11: 'LC3P-1',
#  }

# pxy_dict = {  1:  ( -43000, 0  ),  2:  ( -36500, 0  ),  3:  (  -30000, 0  ),
# 4:  (  -23500, 0  ),    5:  (  -17500, 0  ),    6:  (  -11000, 0  ),    7:  (  -5000, 0  ),
# 8:  (  1500, 0  ),    9:  (  8000, 0  ),
# 10:  (  14500, -1000  ),    11:  ( 21000, 0  ),      }

# sample_dict = {  1: 'Au-Ori-2nd',  2: 'Au-C12-2nd', 3: 'Au-PEG-2nd',4: 'Au-LC1-2nd',
#  5: 'Au-LC2-2nd',6: 'Au-LC3-2nd',7: 'Green-LC3', 8:'Yellow-LC3',
#  9: 'NR1-LC3', 10: 'NR2-LC3',11: 'Fe3O4-623-LC3', 12: 'VO2-LC3'
#  }

# pxy_dict = {  1:  ( -46000, 0  ),  2:  ( -38000, 0  ),  3:  (  -30000, 0  ),
# 4:  (  -21000, 0  ),    5:  (  -11000, 0  ),    6:  (  -3000, 0  ),    7:  (  6000, 0  ),
# 8:  (  14000, 0  ),    9:  (  22000, 0  ),
# 10:  (  30000, -1000  ),    11:  ( 42000, 0  ),   12:  ( 52000, 0  ),   }


# sample_dict = {  1: 'VO2-C12',  2: 'VO2-PEG', 3: 'Gd2O3-C12',4: 'Gd2O3-LC2',
#  5: 'Gd2O3-LC3',6: 'Gd2O3-PEG',7: 'Fe3O4-624-LC2', 8:'Fe3O4-624-LC3',
#  }

# pxy_dict = {  1:  ( -46000, 0  ),  2:  ( -36000, 0  ),  3:  (  -27000, 0  ),
# 4:  (  -16000, 0  ),    5:  (  -5000, 0  ),    6:  (  4000, 0  ),    7:  (  14000, 0  ),
# 8:  (  22000, 0  ),     }

# sample_dict = {  1: 'Fe3O4-623-LC2-Ori',  2: 'Fe3O4-623-LC2-75A-10min', 3: 'Fe3O4-623-LC2-150A-10min',
# 4: 'Fe3O4-623-LC3-Ori',  5: 'Fe3O4-623-LC3-75A-10min', 6: 'Fe3O4-623-LC3-150A-10min',
# 7: 'Fe3O4-yellow-LC2-Ori',  8: 'Fe3O4-yellow-LC2-75A-10min', 9: 'Fe3O4-yellow-LC2-150A-10min',
# 10: 'Fe3O4-yellow-LC3-Ori',  11: 'Fe3O4-yellow-LC3-75A-10min', 12: 'Fe3O4-yellow-LC3-150A-10min',
#  }

# pxy_dict = {  1:  ( -44000, 0  ),  2:  ( -36000, 0  ),  3:  (  -28000, 0  ),
# 4:  ( -20000, 0  ),  5:  ( -11000, 0  ),  6:  (  -3000, 0  ),
# 7:  ( 4000, 0  ),  8:  ( 13000, 0  ),  9:  (  21000, 0  ),
# 10:  ( 28000, 0  ),  11:  ( 36000, 0  ),  12:  (  46000, 0  ),    }


# sample_dict = {  1: 'Fe3O4-623-LC2-150-1h',  2: 'Fe3O4-623-LC3-150-1h', 3: 'Fe3O4-yellow-LC2-150A-1h', 4: 'Fe3O4-yellow-LC3-150A-1h',
# 5: 'Fe3O4-623-LC2-100A-10min', 6: 'Fe3O4-623-LC3-100A-10min', 7: 'Fe3O4-yellow-LC2-100A-10min',  8: 'Fe3O4-yellow-LC3-100A-10min',
#  }

# pxy_dict = {  1:  ( -44000, 0  ),  2:  ( -36000, 0  ),  3:  (  -28000, 0  ),  4:  ( -19500, 0  ),
# 5:  ( -11000, 0  ),  6:  (  -2000, 0  ), 7:  ( 6000, 0  ),  8:  ( 15000, 0  ),      }

# sample_dict = {  1: 'Fe3O4-623-LC2-50A-10min',  2: 'Fe3O4-623-LC3-50A-10min', 3: 'Fe3O4-yellow-LC2-50A-10min', 4: 'Fe3O4-yellow-LC3-50A-10min',
# 5: 'Fe3O4-623-LC2-25A-10min', 6: 'Fe3O4-623-LC3-25A-10min', 7: 'Fe3O4-yellow-LC2-25A-10min',  8: 'Fe3O4-yellow-LC3-25reA-10min',
#  }

# pxy_dict = {  1:  ( -44000, 0  ),  2:  ( -32000, 0  ),  3:  (  -19000, 0  ),  4:  ( -5000, 0  ),
# 5:  ( 8500, 0  ),  6:  (  20500, 0  ), 7:  ( 30000, 0  ),  8:  ( 42000, 0  ),      }


# sample_dict = {  1: 'NR2-LC3-0.1',  2: 'NR2-LC3-0.01', 3: 'Fe3O4-LC2-0.1',4: 'Fe3O4-LC2-0.01',
#  5: 'Fe3O4-LC3-0.1',6: 'Fe3O4-LC3-0.01',7: 'LC1S-1', 8:'LC2S-1',
#  9: 'LC3S-1', 10: 'LC2P-1',11: 'LC3P-1',
#  }

# pxy_dict = {  1:  ( -44100, 0  ),  2:  ( -37500, 0  ),  3:  (  -31500, 0  ),
# 4:  (  -25000, 0  ),    5:  (  -18500, 0  ),    6:  (  -12300, 0  ),    7:  (  -6000, 0  ),
# 8:  (  700, 0  ),    9:  (  7000, 0  ),
# 10:  (  13000, -1000  ),    11:  ( 19600, 0  ),      }


# 9 PM to 12 PM

# sample_dict = {  1: '5CB' ,
#  2: 'Au-LC1-0.1-5CB',  3: 'Au-LC1-0.01-5CB',
#  4: 'Au-LC2-0.1-5CB',5: 'Au-LC2-0.01-5CB',
#  6: 'Au-LC3-0.1-5CB',7: 'Au-LC3-0.01-5CB',
#  8: 'VO2-LC2-0.1-5CB', 9:'VO2-LC2-0.01-5CB',
#  10: 'VO2-LC3-0.1-5CB', 11: 'VO2-LC3-0.01-5CB',
#  12: 'Gd2O3-LC2-0.1-5CB', 13: 'Gd2O3-LC2-0.01-5CB',
#  14: 'Gd2O3-LC3-0.1-5CB', 15: 'Gd2O3-LC3-0.01-5CB',

#  }

# pxy_dict = {1: (-43980, -9000),
#  2: (-37580, -9000),
#  3: (-31260, -9000),
#  4: (-24940, -9000),
#  5: (-18620, -9000),
#  6: (-12000, -9000),
#  7: (-5780, -9000),
#  8: (540, -9000),
#  9: (6960, -9000),
#  10: (13180, -9000),
#  11: (19700, -9000),
#  12: (25920, -9000),
#  13: (32340, -9000),
#  14: (38660, -9000),
#  15: (44980, -9000),
#  }


# 12AM to 3 AM
# sample_dict = {  1: 'NR1-LC2-0.1-5CB' ,
#  2: 'NR1-LC2-0.01-5CB',
#  3: 'NR1-LC3-0.1-5CB',
#  4: 'NR1-LC3-0.01-5CB',
#  5: 'NR2-LC2-0.1-5CB',
#  6: 'NR2-LC2-0.01-5CB',
#  7: 'NR2-LC3-0.1-5CB',
#  8: 'NR2-LC3-0.01-5CB',
#  9:'Fe3O4-LC2-0.1-5CB',
#  10: 'Fe3O4-LC2-0.01-5CB',


#  }

# pxy_dict = {1: (-43980, -9000),
#  2: (-37580, -9000),
#  3: (-31260, -9000),
#  4: (-24940, -9000),
#  5: (-18620, -9000),
#  6: (-12000, -9000),
#  7: (-5780, -9000),
#  8: (540, -9000),
#  9: (6960, -9000),
#  10: (13180, -9000),

#  }

# 3AM to 7AM
sample_dict = {
    1: "Fe3O4-LC3-0.1-5CB",
    2: "Fe3O4-LC3-0.01-5CB",
    3: "LC1S-1-5CB",
    4: "LC2S-1-5CB",
    5: "LC3S-1-5CB",
    6: "LC2P-1-5CB",
    7: "LC3P-1-5CB",
    8: "Au-LC1-1-5CB",
    9: "Au-LC2-1-5CB",
    10: "Au-LC3-1-5CB",
    11: "NR1-LC2-1-5CB",
    12: "NR1-LC3-1-5CB",
    13: "NR2-LC2-1-5CB",
    14: "NR2-LC3-1-5CB",
}

pxy_dict = {
    1: (-43980, -9000),
    2: (-37580, -9000),
    3: (-31260, -9000),
    4: (-24940, -9000),
    5: (-18620, -9000),
    6: (-12000, -9000),
    7: (-5780, -9000),
    8: (540, -9000),
    9: (6960, -9000),
    10: (13180, -9000),
    11: (19700, -9000),
    12: (25920, -9000),
    13: (32340, -9000),
    14: (38660, -9000),
}


# Temperature calibrate:30C, 35C, 40C, 45C
####   RE( run_giwaxs())

x_list = np.array(list((pxy_dict.values())))[:, 0]
# y_list = np.array(list( ( pxy_dict.values()) ) )[:,1]
y_list = np.array([[800] * len(x_list)])


sample_list = np.array(list((sample_dict.values())))
ks = np.array(list((sample_dict.keys())))
# pxy_dict =  { k: [ pxy_dict[k][0], 600 ]  for k in ks   }
pxy_dict = {k: [pxy_dict[k][0], -9000] for k in ks}


##################################################
############ Some convinent functions#################
#########################################################


def setT(T):
    T_kelvin = T + 273.15
    yield from ls.output1.mv_temp(T_kelvin)
    # RE( ls.output1.mv_temp(T_kelvin)    )
    print("Set temperature to %.2f oC." % T)


def getT():
    temp_degC = ls.input_A.get() - 273.15
    print("The current temperature is %.2f oC." % temp_degC)
    return temp_degC


def startT_old():
    yield from ls.output1.turn_on()
    # RE( ls.output1.turn_on()    )
    print("Start heating up using output1.")


def startT():
    """
    Try using range 3 in channel 1
    """
    yield from bps.mv(ls.output1.status, 3)
    print("Start heating up using output1 using range3.")


def stopT():
    yield from ls.output1.turn_off()
    # RE( ls.output1.turn_off()    )
    print("Stop heating up using output1.")

    # temp = ls.input_A.value
    # while abs(temp - t_kelvin) > 0.25:
    #     print(abs(temp - t_kelvin))
    #     yield from bps.sleep(10)
    #     temp = ls.input_A.value


def gotoT(T):
    yield from setT(T)
    yield from startT()
    temp = getT()
    while abs(temp - T) > 0.25:
        print(abs(temp - T))
        yield from bps.sleep(10)
        temp = getT()


smi = SMI_Beamline()


def alignement_gisaxs(angle=0.15):
    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)
    smi = SMI_Beamline()
    yield from smi.modeAlignment(technique="gisaxs")
    # Set direct beam ROI
    yield from smi.setDirectBeamROI()
    # Scan theta and height
    yield from align_gisaxs_height(500, 21, der=True)
    yield from align_gisaxs_th(1.5, 27)
    # yield from align_gisaxs_height(300, 11, der=True)
    # yield from align_gisaxs_th(0.5, 16)
    # move to theta 0 + value
    yield from bps.mv(piezo.th, ps.peak + angle)
    # Set reflected ROI
    yield from smi.setReflectedBeamROI(total_angle=angle, technique="gisaxs")
    # Scan theta and height
    yield from align_gisaxs_th(0.2, 31)
    yield from align_gisaxs_height(150, 21)
    yield from align_gisaxs_th(0.025, 21)
    # Close all the matplotlib windows
    plt.close("all")
    # Return angle
    yield from bps.mv(piezo.th, ps.cen - angle)
    yield from smi.modeMeasurement()


def alignement_gisaxs_try(angle=0.15):
    sample_id(user_name="test", sample_name="test")
    bec._calc_derivative_and_stats = True
    det_exposure_time(0.3, 0.3)
    smi = SMI_Beamline()
    yield from smi.modeAlignment(technique="gisaxs")
    # Set direct beam ROI
    yield from smi.setDirectBeamROI()
    # Scan theta and height
    yield from align_gisaxs_height(500, 21, der=True)
    yield from align_gisaxs_th(1.5, 27)
    # yield from align_gisaxs_height(300, 11, der=True)
    # yield from align_gisaxs_th(0.5, 16)
    # move to theta 0 + value
    yield from bps.mv(piezo.th, ps.peak + angle)
    try:
        # Set reflected ROI
        yield from smi.setReflectedBeamROI(total_angle=angle, technique="gisaxs")
        # Scan theta and height
        yield from align_gisaxs_th(0.2, 31)
        yield from align_gisaxs_height(150, 21)
        yield from align_gisaxs_th(0.025, 21)
        # Close all the matplotlib windows
        plt.close("all")
        # Return angle
        yield from bps.mv(piezo.th, ps.cen - angle)
    except:
        pass
    yield from smi.modeMeasurement()


def align_gix():
    yield from alignement_gisaxs(0.1)  # run alignment routine


def run_gisaxs(
    x_list=x_list,
    sample_list=sample_list,
    t=1,
    username=username,
    inc_angles=[0.05, 0.15, 0.3],
    x_shift_array=[-500, -400, -300, -200, -100, 0, 100, 200, 300, 400, 500],
):

    # define names of samples on sample bar
    assert len(x_list) == len(sample_list), f"Sample name/position list is borked"
    inc_angles = np.array(inc_angles)  # incident angles
    # 4*3.14/(12.39842/16.1)*np.sin((7*6.5+3.5)*3.14/360) = 6.760 A-1
    x_shift_array = np.array(x_shift_array)
    dets = [pil1M]
    for ii, (x, sample) in enumerate(
        zip(x_list, sample_list)
    ):  # loop over samples on bar
        yield from bps.mv(piezo.x, x)  # move to next sample
        # yield from  bps.mv(piezo.y, 4000  ) #move y to 4000
        yield from alignement_gisaxs(0.1)  # run alignment routine
        TH = piezo.th.position
        th_meas = inc_angles + piezo.th.position
        th_real = inc_angles
        det_exposure_time(t, t)
        x_pos_array = x + x_shift_array
        for x_meas in x_pos_array:  # measure at a few x positions
            yield from bps.mv(piezo.x, x_meas)
            for i, th in enumerate(th_meas):  # loop over incident angles
                yield from bps.mv(piezo.th, th)
                name_fmt = "{sample}_{th:5.4f}deg_x{x:05.2f}_y{y:05.2f}_z{y:05.2f}_det{saxs_z:05.2f}m_expt{t}s_sid{scan_id:08d}"
                sample_name = name_fmt.format(
                    sample=sample,
                    th=th_real[i],
                    x=np.round(piezo.x.position, 2),
                    y=np.round(piezo.y.position, 2),
                    z=np.round(piezo.z.position, 2),
                    saxs_z=np.round(pil1m_pos.z.position, 2),
                    t=t,
                    scan_id=RE.md["scan_id"],
                )
                sample_id(user_name=username, sample_name=sample_name)
                print(f"\n\t=== Sample: {sample_name} ===\n")
                # yield from bp.scan(dets, energy, e, e, 1)
                # yield from bp.scan(dets, waxs, *waxs_arc)
                print(dets)
                yield from bp.count(dets, num=1)
                # print( 'HERE#############')
    yield from bps.mv(piezo.th, TH)
    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5)


# def test():
#     yield from RE( bps.mv(piezo.y,  3266  )  )


def run_T_wsaxs(
    x_list=x_list,
    sample_list=sample_list,
    t=1,
    username=username,
    waxs_angles=[0, 15],
    Tlist=[
        30,
        31,
        32,
        32.5,
        33,
        33.5,
        34,
        34.5,
        35,
        35.5,
        36,
        36.5,
        37,
        37.5,
        38,
        38.5,
        39,
        39.5,
        40,
        40.5,
        41,
        41.5,
        42,
        43,
        44,
        45,
        44,
        43,
        42,
        41,
        40.5,
        40,
        39.5,
        39,
        38.5,
        38,
        37.5,
        37,
        36.5,
        36,
        35.5,
        35,
        34.5,
        34,
        33.5,
        33,
        32,
    ],
    saxs_on=True,
):

    """RE(  run_T_wsaxs() )"""
    # [ 32, 33, 34, 35, 36,  37 , 38,  39,  40, 41, 42, 43, 44, 45, 46, 47, 46, 45, 44, 43, 42, 41, 40, 39, 38, 37, 36, 35, 34, 33,  ],

    for (cts, T) in enumerate(Tlist):
        yield from setT(T)
        yield from startT()
        temp = getT()
        while abs(temp - T) > 0.25:
            print(abs(temp - T))
            yield from bps.sleep(10)
            temp = getT()
        print("Run here for T=%s ..." % T)
        yield from measure_series_multi_angle_wsaxs_yield(
            t=[t], waxs_angles=waxs_angles, dys=[0]
        )
        # easure_series_multi_angle_wsaxs(  t= [t], waxs_angles= waxs_angles,  dys = [ 0 ]   )

    yield from setT(25)
    yield from stopT()


def run_T_giwsaxs(
    x_list=x_list,
    sample_list=sample_list,
    t=1,
    username=username,
    inc_angles=[0.05, 0.12, 0.15, 0.18, 0.3],
    waxs_angles=[15],
    x_shift_array=[-500, 0, 500],
    Tlist=[
        30,
        40,
        50,
        60,
        65,
        70,
        75,
        80,
        85,
        90,
        100,
        120,
        100,
        90,
        85,
        80,
        75,
        70,
        65,
        60,
        30,
    ],
    saxs_on=True,
):

    """RE(  run_T_giwsaxs() )"""
    # [ 30 , 40 , 50 , 60, 65, 70, 75, 80, 85, 90, 100, 120, 100, 90, 85, 80, 75, 70, 65, 60, 30],
    YPOS = {}
    ThPOS = {}
    for (cts, T) in enumerate(Tlist):
        yield from setT(T)
        yield from startT()
        temp = getT()
        while abs(temp - T) > 0.25:
            print(abs(temp - T))
            yield from bps.sleep(10)
            temp = getT()
        # yield from bps.sleep(120)
        if cts in [0]:  # T = 30, 60, 90, 60
            align = True

        else:
            align = False

        yield from run_giwsaxs(
            x_list=x_list,
            sample_list=sample_list,
            t=t,
            username=username,
            inc_angles=inc_angles,
            waxs_angles=waxs_angles,
            x_shift_array=x_shift_array,
            saxs_on=True,
            align=align,
            YPOS=YPOS,
            ThPOS=ThPOS,
            T=T,
        )

    yield from setT(25)
    yield from stopT()


def run_giwsaxs(
    x_list=x_list,
    sample_list=sample_list,
    t=1,
    username=username,
    inc_angles=[0.05, 0.15, 0.3],
    waxs_angles=[0, 20],
    x_shift_array=[0],
    YPOS={},
    ThPOS={},
    saxs_on=True,
    align=True,
    T=25,
):
    # define names of samples on sample bar
    assert len(x_list) == len(sample_list), f"Sample name/position list is borked"
    inc_angles = np.array(inc_angles)  # incident angles
    th_real = inc_angles
    waxs_angles = np.array(waxs_angles)  # arc waxs angles
    # 4*3.14/(12.39842/16.1)*np.sin((7*6.5+3.5)*3.14/360) = 6.760 A-1
    x_shift_array = np.array(x_shift_array)
    max_waxs_angle = np.max(waxs_angles)
    inverse_angle = False
    cts = 0

    for ii, (x, sample) in enumerate(
        zip(x_list, sample_list)
    ):  # loop over samples on bar
        yield from bps.mv(piezo.x, x)  # move to next sample
        if align:
            # RE( bps.mv(piezo.th, 0 ) )
            yield from alignement_gisaxs(0.15)  # run alignment routine
            YPOS[ii] = piezo.y.position
            ThPOS[ii] = piezo.th.position
            print(YPOS, ThPOS)
        else:
            yield from bps.mv(piezo.y, YPOS[ii])
            yield from bps.mv(piezo.th, ThPOS[ii])

        TH = ThPOS[ii]  # piezo.th.position
        th_meas = inc_angles + ThPOS[ii]  # piezo.th.position

        det_exposure_time(t, t)
        x_pos_array = x + x_shift_array
        if inverse_angle:
            Waxs_angles = waxs_angles[::-1]
        else:
            Waxs_angles = waxs_angles
        for waxs_angle in Waxs_angles:  # loop through waxs angles
            yield from bps.mv(waxs, waxs_angle)
            if waxs_angle == max_waxs_angle:
                if saxs_on:
                    dets = [pil900KW, pil1M, pil300KW]
                else:
                    dets = [pil900KW, pil300KW]
                print("Meausre both saxs and waxs here for w-angle=%s" % waxs_angle)
            else:
                dets = [pil900KW, pil300KW]
            for x_meas in x_pos_array:  # measure at a few x positions
                yield from bps.mv(piezo.x, x_meas)
                for i, th in enumerate(th_meas):  # loop over incident angles
                    yield from bps.mv(piezo.th, th)
                    if inverse_angle:
                        name_fmt = "{sample}_{th:5.4f}deg_waxsN{waxs_angle:05.2f}_x{x:05.2f}_y{y:05.2f}_z{y:05.2f}_det{saxs_z:05.2f}m_expt{t}s_T{T}_sid{scan_id:08d}"
                    else:
                        name_fmt = "{sample}_{th:5.4f}deg_waxsP{waxs_angle:05.2f}_x{x:05.2f}_y{y:05.2f}_z{y:05.2f}_det{saxs_z:05.2f}m_expt{t}s_T{T}_sid{scan_id:08d}"
                    sample_name = name_fmt.format(
                        sample=sample,
                        th=th_real[i],
                        waxs_angle=waxs_angle,
                        x=np.round(piezo.x.position, 2),
                        y=np.round(piezo.y.position, 2),
                        z=np.round(piezo.z.position, 2),
                        saxs_z=np.round(pil1m_pos.z.position, 2),
                        t=t,
                        T=T,
                        scan_id=RE.md["scan_id"],
                    )
                    sample_id(user_name=username, sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    # yield from bp.scan(dets, energy, e, e, 1)
                    # yield from bp.scan(dets, waxs, *waxs_arc)
                    print(dets)
                    yield from bp.count(dets, num=1)
                    # print( 'HERE#############')
        inverse_angle = not inverse_angle
        cts += 1
    yield from bps.mv(piezo.th, TH)
    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5)


def check_sample_loc(sleep=5):
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


def move_waxs_off(waxs_angle=8.0):
    RE(bps.mv(waxs, waxs_angle))


def move_waxs_on(waxs_angle=0.0):
    RE(bps.mv(waxs, waxs_angle))


def mov_sam(pos):
    px, py = pxy_dict[pos]
    RE(bps.mv(piezo.x, px))
    RE(bps.mv(piezo.y, py))
    sample = sample_dict[pos]
    print("Move to pos=%s for sample:%s" % (pos, sample))
    RE.md["sample"] = sample
    RE.md["sample_name"] = sample


def mov_sam_re(pos):
    px, py = pxy_dict[pos]
    yield from bps.mv(piezo.x, px)
    yield from bps.mv(piezo.y, py)
    sample = sample_dict[pos]
    print("Move to pos=%s for sample:%s" % (pos, sample))
    RE.md["sample"] = sample
    RE.md["sample_name"] = sample


def check_saxs_sample_loc(sleep=5):
    ks = list(sample_dict.keys())
    for k in ks:
        mov_sam(k)
        time.sleep(sleep)


def snap_waxs(t=0.1):
    dets = [pil300KW]
    sample_id(user_name="test", sample_name="test")
    det_exposure_time(t)
    yield from (bp.count(dets, num=1))


def snap_saxs(t=0.1):
    dets = [pil1M]
    sample_id(user_name="test", sample_name="test")
    det_exposure_time(t)
    yield from (bp.count(dets, num=1))


def measure_pindiol_current():
    fs.open()
    yield from bps.sleep(0.3)
    pd_curr = pdcurrent1.value
    fs.close()
    print("--------- Current pd_curr {}\n".format(pd_curr))
    return pd_curr


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
    name_fmt = "{sample}_x{x:05.2f}_y{y:05.2f}_z{z_pos:05.2f}_det{saxs_z:05.2f}m_expt{t}s_sid{scan_id:08d}"
    sample_name = name_fmt.format(
        sample=sample,
        x=np.round(piezo.x.position, 2),
        y=np.round(piezo.y.position, 2),
        z_pos=piezo.z.position,
        saxs_z=np.round(pil1m_pos.z.position, 2),
        t=t,
        scan_id=RE.md["scan_id"],
    )
    det_exposure_time(t, t)
    # sample_name='test'
    sample_id(user_name=user_name, sample_name=sample_name)
    print(f"\n\t=== Sample: {sample_name} ===\n")
    print("Collect data here....")
    yield from bp.count(dets, num=1)
    sample_id(user_name="test", sample_name="test")


def measure_waxs(
    t=1, waxs_angle=0, att="None", dx=0, dy=0, user_name=username, sample=None
):
    """RE( measure_waxs( sample = 'AgBH_12keV' ) )"""

    if sample is None:
        # sample = RE.md['sample']
        sample = RE.md["sample_name"]
    yield from bps.mv(waxs, waxs_angle)
    dets = [pil900KW, pil300KW]
    # att_in( att )
    if dx:
        yield from bps.mvr(piezo.x, dx)
    if dy:
        yield from bps.mvr(piezo.y, dy)
    name_fmt = "{sample}_x{x_pos:05.2f}_y{y_pos:05.2f}_z{z_pos:05.2f}_waxs{waxs_angle:05.2f}_expt{expt}s_sid{scan_id:08d}"
    sample_name = name_fmt.format(
        sample=sample,
        x_pos=piezo.x.position,
        y_pos=piezo.y.position,
        z_pos=piezo.z.position,
        waxs_angle=waxs_angle,
        expt=t,
        scan_id=RE.md["scan_id"],
    )
    det_exposure_time(t, t)
    sample_id(user_name=user_name, sample_name=sample_name)
    print(f"\n\t=== Sample: {sample_name} ===\n")
    print("Collect data here....")
    yield from bp.count(dets, num=1)
    # att_out( att )
    # sample_id(user_name='test', sample_name='test')


def measure_wsaxs(
    t=1, waxs_angle=15, att="None", dx=0, dy=0, user_name=username, sample=None
):
    """RE( measure_wsaxs( sample = 'AgBH_12keV' ) )"""

    if sample is None:
        # sample = RE.md['sample']
        sample = RE.md["sample_name"]
    yield from bps.mv(waxs, waxs_angle)
    dets = [pil900KW, pil300KW, pil1M]
    if dx:
        yield from bps.mvr(piezo.x, dx)
    if dy:
        yield from bps.mvr(piezo.y, dy)
    name_fmt = "{sample}_x{x_pos:05.2f}_y{y_pos:05.2f}_z{z_pos:05.2f}_det{saxs_z}_waxs{waxs_angle:05.2f}_expt{expt}s_sid{scan_id:08d}"

    sample_name = name_fmt.format(
        sample=sample,
        x_pos=piezo.x.position,
        y_pos=piezo.y.position,
        z_pos=piezo.z.position,
        saxs_z=np.round(pil1m_pos.z.position, 2),
        waxs_angle=waxs_angle,
        expt=t,
        scan_id=RE.md["scan_id"],
    )

    det_exposure_time(t, t)
    sample_id(user_name=user_name, sample_name=sample_name)
    print(f"\n\t=== Sample: {sample_name} ===\n")
    print("Collect data here....")
    yield from bp.count(dets, num=1)
    # att_out( att )
    # sample_id(user_name='test', sample_name='test')


def measure_series_multi_angle_wsaxs_yield(
    t=[1], waxs_angles=[0, 15], dys=[0, -2000, -2000, -2000, -2000]
):

    """t0=time.time();measure_series_multi_angle_wsaxs();run_time(t0)"""

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


def measure_series_multi_angle_wsaxs(
    t=[1], waxs_angles=[0, 15], dys=[0, -2000, -2000, -2000, -2000]
):

    """t0=time.time();measure_series_multi_angle_wsaxs();run_time(t0)"""

    ks = list(sample_dict.keys())  # [:8 ]
    maxA = np.max(waxs_angles)
    for waxs_angle in waxs_angles:
        for k in ks:
            print(k)
            mov_sam(k)
            for dy in dys:
                print(dy)
                print("here we go ... ")
                for ti in t:
                    RE.md["sample_name"] = sample_dict[k]
                    if waxs_angle == maxA:
                        RE(
                            measure_wsaxs(
                                t=ti, waxs_angle=waxs_angle, att="None", dy=dy
                            )
                        )
                    else:
                        RE(measure_waxs(t=ti, waxs_angle=waxs_angle, att="None", dy=dy))


def measure_series_saxs(
    t=[1],
    dys=[
        0,
        -500,
        -1000,
        -1500,
        -2000,
    ],
):
    ks = list(sample_dict.keys())
    for k in ks:
        mov_sam(k)
        for dy in dys:
            for ti in t:
                RE(measure_saxs(t=ti, att="None", dy=dy))


def measure_series_waxs(
    t=[1],
    waxs_angle=20,
    dys=[
        0,
        -500,
        -1000,
        -1500,
        -2000,
    ],
):
    ks = list(sample_dict.keys())[:8]
    for k in ks:
        mov_sam(k)
        for dy in dys:
            for ti in t:
                RE(measure_waxs(t=ti, waxs_angle=waxs_angle, att="None", dy=dy))


def measure_series_wsaxs(
    t=[1], waxs_angle=15, dys=[0, -1000, -2000, -3000, -4000, -6000, -8000, -10000]
):
    ks = list(sample_dict.keys())  # [:8 ]
    for k in ks:
        mov_sam(k)
        for dy in dys:
            for ti in t:
                RE(measure_wsaxs(t=ti, waxs_angle=waxs_angle, att="None", dy=dy))


def run_time(t0):
    dt = (time.time() - t0) / 60
    print("The Running time is: %.2f min." % dt)


def measure_waxs_multi_angles(
    t=1.0,
    att="None",
    dy=0,
    user_name="",
    saxs_on=False,
    waxs_angles=[0.0, 6.5, 13.0],
    inverse_angle=False,
):

    # waxs_angles = np.linspace(0, 65, 11)   #the max range
    # waxs_angles =   np.linspace(0, 65, 11),
    # [ 0. ,  6.5, 13. , 19.5]

    waxs_angle_array = np.array(waxs_angles)
    if inverse_angle:
        waxs_angle_array = waxs_angle_array[::-1]
    dets = [pil300KW]
    max_waxs_angle = np.max(waxs_angle_array)
    for waxs_angle in waxs_angle_array:
        yield from bps.mv(waxs, waxs_angle)
        # sample = RE.md['sample']
        sample = RE.md["sample_name"]
        if dy:
            yield from bps.mvr(piezo.y, dy)
        name_fmt = "{sample}_x{x_pos:05.2f}_y{y_pos:05.2f}_z{z_pos:05.2f}_waxs{waxs_angle:05.2f}_expt{expt}s_sid{scan_id:08d}"
        sample_name = name_fmt.format(
            sample=sample,
            x_pos=piezo.x.position,
            y_pos=piezo.y.position,
            z_pos=piezo.z.position,
            waxs_angle=waxs_angle,
            expt=t,
            scan_id=RE.md["scan_id"],
        )
        print(sample_name)
        if saxs_on:
            if waxs_angle == max_waxs_angle:
                dets = [
                    pil1M,
                    pil300KW,
                ]  # waxs, maxs, saxs = [pil300KW, rayonix, pil1M]
            else:
                dets = [pil300KW]

        det_exposure_time(t, t)
        sample_id(user_name=user_name, sample_name=sample_name)
        print(f"\n\t=== Sample: {sample_name} ===\n")
        # yield from bp.scan(dets, waxs, *waxs_arc)
        yield from bp.count(dets, num=1)
    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5)


def snap_waxs(t=0.1):
    dets = [pil900KW]
    sample_id(user_name="test", sample_name="test")
    det_exposure_time(t)
    yield from (bp.count(dets, num=1))


def snap_saxs(t=0.1):
    dets = [pil1M]
    sample_id(user_name="test", sample_name="test")
    det_exposure_time(t)
    yield from (bp.count(dets, num=1))


def measure_pindiol_current():
    fs.open()
    yield from bps.sleep(0.3)
    pd_curr = pdcurrent1.value
    fs.close()
    print("--------- Current pd_curr {}\n".format(pd_curr))
    return pd_curr

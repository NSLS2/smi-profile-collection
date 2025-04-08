##Collect data:

# SMI: 2021/10/28
# proposal_id('2021_3', '308895_SSYang')
# proposal_id('2021_3', '308895_SSYang1031')
# Align the beamline to 16.1 keV
# %run -i /home/xf12id/.ipython/profile_collection/startup/11-energy.py
# energy.target_harmonic.set(17)
# energy.move(16100)
# on the SMI H-V focusing mirrors, change stripe to Rh for the three mirrors ( HFM, VFM, VDM, )
# Tweak DCM pitch
#


# Will add a window
#
# SAXS distance 5000
# SAXS in vacuum and WAXS in air

##for run <=4
# 5 m, beam stop:  1.9
# 5m, 1M, x=1, Y = -60
# the correspond beam center is [ 490, 565 ]
# beamstop_save()
# 5 m, beam stop:  1.9
# 5m, 1M, x=1, Y = -40
# the correspond beam center is [ 490, 682  ]
# beamstop_save()


##for the run >=5
# 5 m, beam stop:  1.9
# 5m, 1M, x=-5, Y = -40
# the correspond beam center is [ 454, 682  ]
# beamstop_save()


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

# The beam center on SAXS:  [ 485, 566 ]
# Energy: 16.1 keV, 0.77009 A
# SAXS distance 5000


## For pindiol:
#   No filter, it's saturated ( 125257)
#   Sn30 um, X1, still saturated ( 125257 )  #RE(bps.mv(att1_9.open_cmd, 1))
#   Sn30 um, X2, still saturated ( 125256 )  #RE(bps.mv(att1_10.open_cmd, 1))
#   Sn30 um, X3 (X1 + X2) ,  (67713 )
#   Sn30 um, X4,  (27456)
# Sn30 um, X5,  (11334 )
#   Sn30 um, X8,  (722)
# For WAXS,
# WAXS beam center: [  87, 97   ], there is bad pixel here  could check later,  (BS: X: -20.92 )
# Put Att and move bs to check the BC_WAXS, --> [ 87, 97 ]
# #beam center [488, 591]
## For 8 meter, beamStopX: 1.04857 , 1M: X 0.24 , Center [ 490, 588 ]
#


from datetime import datetime

username = "SSY"
# PZ = -600
# # First Run, 3 samples,
# sample_dict = {  1: 'PbS_Si_1',  2: 'PbS_Si_2', 3: 'PbS_Si_3',   }
# pxy_dict = {  1:  ( 23100, 5098  ),  2:   ( -900, 5098  ),  3:   ( -23900, 5098  ),     }

# # 2 Run, 2 samples,
# sample_dict = {  1: 'Pt-Fe3O4_TEM_1',  2: 'Pt-Fe3O4_TEM_2'  }
# pxy_dict = {  1:  ( 19100, 4668  ),  2:   ( -22900, 4668  )    }

# # 3 Run,   samples,  not finished due to alignment problem
# sample_dict = {  1: 'Fe3O4_OO_LC',  2: 'Fe3O4_LC1', 3: 'Fe3O4_LC2', 4: 'Fe3O4_LC3', 5: 'Fe3O4_916', 6: 'Fe3O4_1017' }
# pxy_dict = {  1:  ( 32100, 5099  ),  2:   ( 24100, 5099  ), 3:  ( 11100, 5099  ), 4:  ( -900, 5099  ), 5:
#  ( -10900, 5099  ), 6:  ( -23900, 5099  )    }
# 4 th run,
ypos = 4389  # 5099
sample_dict = {
    1: "Fe3O4_OO_LC",
}
pxy_dict = {
    1: (49100, ypos),
}
# run 5
ypos = 4039
sample_dict = {
    2: "Fe3O4_LC1",
    3: "Fe3O4_LC2",
    4: "Fe3O4_LC3",
    5: "Fe3O4_916",
    6: "Fe3O4_1017",
    7: "Au_azo_G1",
    8: "Au_azo_G2",
    9: "Au_G1",
}
pxy_dict = {
    2: (39100, ypos),
    3: (30100, ypos),
    4: (19100, ypos),
    5: (10100, ypos),
    6: (1100, ypos),
    7: (-10900, ypos),
    8: (-21900, ypos),
    9: (-33900, ypos),
}


# PZ = -600
# hexpod Z = -5
##Run 6 In-Situ
sample_name = "PbS_inSitu_test1"
# 8 ml, liquid interface py = 0
# 'PbS_inSitu_test1', the sample is broken down into small pieces during X-ray measurements
# after measurements, found that there is two groove etched by Sulfide(?)


##Run 7 In-Situ
sample_name = "Au-G1_inSitu1"
# 6 ml, liquid interface py = 2400


##Run 8 In-Situ
sample_name = "AuAZO-G2_inSitu1"
# 6 ml, liquid interface py = 2400
# t= 553 s  open UV light
# t=2459 s UV off
# t=3535 s UV on again

##Run 9 in_Situ
sample_name = "Fe3O4-inSitu1"
# 6 ml, liquid interface py = 3200


##Run 10 in_Situ
sample_name = "Fe3O4-inSitu2"
# 6 ml, liquid interface py = 3200

##Run 11 in_Situ
sample_name = "Fe3O4-inSitu2-open"
# 6 ml, liquid interface py = 3200

##Run 12 in_Situ
sample_name = "Au-azoG2-inSitu"
# 6 ml, liquid interface py = 3300
# UV 60 S

##Run 12 in_Situ
sample_name = "Au-azoG2-inSitu2"
# 6 ml, liquid interface py = 3200


##Run 12 in_Situ
sample_name = "Au-azoG2-inSitu3"
# 6 ml, liquid interface py = 3100
# UV 60 S

##Run 12 in_Situ
sample_name = "Au-azoG2-inSitu4"
# 6 ml, liquid interface py = 3100
# UV 0 S
# UV off at 1400 s


##Run 13 in_Situ
sample_name = "Au-azoG2-inSitu5"
# 6 ml, liquid interface py = 3100
# 20 ul toluene
# UV off

##Run 14 in_Situ
sample_name = "Au-azoG2-inSitu6"
# 6 ml, liquid interface py = 3100
# 20 ul toluene
# UV off

##Run 15 in_Situ
sample_name = "Au-azoG2-inSitu_Serial2"
# 6 ml, liquid interface py = 3100
# UV off
# UV on
# No signals

##Run 16 in_Situ
sample_name = "Au-azoG2-inSitu_Serial2_1"
# 6 ml, liquid interface py = 3100
# UV off


##Run 17 in_Situ
sample_name = "Au-azoG2-inSitu_Serial2_2"
# 6 ml, liquid interface py = 3100
# UV off


##Run 18 in_Situ
sample_name = "Au-azoG2-inSitu_Serial2_3"
# 6 ml, liquid interface py = 3100
# UV on

##Run 19 in_Situ
sample_name = "Au-azoG2-inSitu_Serial2_4"
# 6 ml, liquid interface py = 3100
# UV on

##Run 19 in_Situ
sample_name = "Au-azoG2-inSitu_Serial2_5"
# 6 ml, liquid interface py = 3100
# UV on


##Run 20 in_Situ
sample_name = "Au-azoG2-inSitu_Serial2_6"
# 6 ml, liquid interface py = 3100
# UV on Toluene 20 ul


##Run 21 in_Situ
sample_name = "Au-azoG2-inSitu_Serial2_7"
# 6 ml, liquid interface py = 3100
# UV on Toluene

##Run 22 in_Situ
sample_name = "Au-azoG2-inSitu_Serial2_8"
# 6 ml, liquid interface py = 3100
# UV off

##Run 23 in_Situ
sample_name = "Au-azoG2-inSitu_Serial2_9"
# 6 ml, liquid interface py = 3100
# UV off

##Run 24 in_Situ
sample_name = "Au-azoG2-inSitu_Serial2_10"
# 6 ml, liquid interface py = 3100
# UV off Toluene 20 ul

##Run 25 in_Situ
sample_name = "Au-azoG2-inSitu_Serial2_11"
# 6 ml, liquid interface py = 3100

##Run 26 in_Situ
sample_name = "Fe3O4_910_1"
# 6 ml, liquid interface py = 3100

##Run 27 in_Situ
sample_name = "Pt-Fe3O4_1"
# 6 ml, liquid interface py = 3100

##Run 28 in_Situ
sample_name = "Pt-Fe3O4_2"
# 6 ml, liquid interface py = 3100

##Run 29 in_Situ
sample_name = "Pt-Fe3O4_3"
# 6 ml, liquid interface py = 3100

##Run 30 in_Situ
sample_name = "Pt-G1_1"
# 6 ml, liquid interface py = 3100

##Run 31 in_Situ
sample_name = "Pt-G1_2"
# 6 ml, liquid interface py = 3100

##Run 32 in_Situ
sample_name = "Pt_1"
# 6 ml, liquid interface py = 3100

##Run 33 in_Situ
sample_name = "Pt_-azo-G2_1"
# 6 ml, liquid interface py = 3100


##Run 34 in_Situ
sample_name = "Pt_-azo-G2_2"
# 6 ml, liquid interface py = 3100

##Run 35 in_Situ
sample_name = "Co3O4_1"
# 6 ml, liquid interface py = 3100


##Run 36 in_Situ
sample_name = "Pt_2"
# 6 ml, liquid interface py = 3100

##Run 37 in_Situ
sample_name = "Au-azo-G1-1"
# 6 ml, liquid interface py = 3100

##Run 38 in_Situ
sample_name = "Au-azo-G1-1"
# 6 ml, liquid interface py = 3100
# UV on

##Run 38 in_Situ
sample_name = "Au-azo-G1-3"
# 6 ml, liquid interface py = 3100
# UV on
# toluene 20 ul

##Run 39 in_Situ
sample_name = "Au-azo-G1-4"
# 6 ml, liquid interface py = 3100
# UV off


##Run 40 in_Situ
sample_name = "Au-azo-G1-5"
# 6 ml, liquid interface py = 3100
# UV off
# toluene 20 ul

##Run 41 in_Situ
sample_name = "Au-azo-G1-6"
# 6 ml, liquid interface py = 3100
# UV off
# run_in_situ_RT_UV_swaxs()


##Run 42, In_situ HT
ypos = 6644
sample_dict = {
    1: "TestSample1_T50",
    2: "TestSample2_T50",
}
pxy_dict = {
    1: (-700, ypos),
    2: (27300, 6300),
}
# run_gisaxs_in_situHT()


##Run 43, In_situ HT
ypos = 6644
sample_dict = {
    1: "Au_LC1_RT",
    2: "Au_LC2_RT",
    3: "Au_LC3_RT",
    4: "Au_LC4_RT",
}
pxy_dict = {
    1: (-15700, ypos),
    2: (-700, ypos),
    3: (16300, ypos),
    4: (31300, 6300),
}
# run_gisaxs_in_situHT()


##Run 44, In_situ HT 01:00 211030
ypos = 6744
sample_dict = {
    1: "Au_LC1_RT",
    2: "Au_LC2_RT",
    3: "Au_LC3_RT",
    4: "Au_LC4_RT",
}
pxy_dict = {
    1: (-17700, 6744),
    2: (-3700, 6744),
    3: (12300, 6744),
    4: (30300, 6744),
}
# run_gisaxs_in_situHT()

##Run 45, In_situ HT 01:45 211030
ypos = 6744
sample_dict = {
    1: "Au_LC1_50",
    2: "Au_LC2_50",
    3: "Au_LC3_50",
    4: "Au_LC4_50",
}
pxy_dict = {
    1: (-17700, 6744),
    2: (-3700, 6744),
    3: (12300, 6744),
    4: (30300, 6744),
}
# run_gisaxs_in_situHT()

##Run 45, In_situ HT 02:25 211030
ypos = 6744
sample_dict = {
    1: "Au_LC1_70",
    2: "Au_LC2_70",
    3: "Au_LC3_70",
    4: "Au_LC4_70",
}
pxy_dict = {
    1: (-17700, 6744),
    2: (-3700, 6744),
    3: (12300, 6744),
    4: (30300, 6744),
}
# run_gisaxs_in_situHT()


##Run 46, In_situ HT 03:05 211030
ypos = 6744
sample_dict = {
    1: "Au_LC1_90",
    2: "Au_LC2_90",
    3: "Au_LC3_90",
    4: "Au_LC4_90",
}
pxy_dict = {
    1: (-17700, 6744),
    2: (-3700, 6744),
    3: (12300, 6744),
    4: (30300, 6744),
}
# run_gisaxs_in_situHT()

##Run 47, In_situ HT 03:45 211030
ypos = 6744
sample_dict = {
    1: "Au_LC1_110",
    2: "Au_LC2_110",
    3: "Au_LC3_110",
    4: "Au_LC4_110",
}
pxy_dict = {
    1: (-17700, 6744),
    2: (-3700, 6744),
    3: (12300, 6744),
    4: (30300, 6744),
}
# run_gisaxs_in_situHT()


##Run 48, In_situ HT 04:15 211030
ypos = 6744
sample_dict = {
    1: "Au_LC1_50_cool",
    2: "Au_LC2_50_cool",
    3: "Au_LC3_50_cool",
    4: "Au_LC4_50_cool",
}
pxy_dict = {
    1: (-17700, 6744),
    2: (-3700, 6744),
    3: (12300, 6744),
    4: (30300, 6744),
}
# run_gisaxs_in_situHT()


##Run 49, In_situ HT 04:45 211030
ypos = 6744
sample_dict = {
    1: "Au_LC1_RT_cool",
    2: "Au_LC2_Rt_cool",
    3: "Au_LC3_Rt_cool",
    4: "Au_LC4_Rt_cool",
}
pxy_dict = {
    1: (-17700, 6744),
    2: (-3700, 6744),
    3: (12300, 6744),
    4: (30300, 6744),
}
# run_gisaxs_in_situHT()

##Run 50, In_situ HT 05:15 211030
ypos = 6744
sample_dict = {
    1: "Au_LC1_5CB_RT",
    2: "Au_LC2_5CB_RT",
    3: "Au_LC3_5CB_RT",
    4: "Au_LC4_5CB_RT",
    5: "5CB_RT",
}
pxy_dict = {
    1: (-20700, 6744),
    2: (-9700, 6744),
    3: (5300, 6744),
    4: (20300, 6744),
    5: (33300, 6744),
}
# run_gisaxs_in_situHT()


##Run 51, In_situ HT 05:53 211030
ypos = 6744
sample_dict = {
    1: "Pt_LC1_RT",
    2: "Pt_LC2_RT",
    3: "Pt_LC3_RT",
    4: "Pt_LC4_RT",
}
pxy_dict = {
    1: (-16700, 6744),
    2: (-1700, 6744),
    3: (12300, 6744),
    4: (31300, 6744),
}
# run_gisaxs_in_situHT()

##Run 52, In_situ HT 06:15 211030
ypos = 6744
sample_dict = {
    1: "Au_LC1_5CB_RT_1",
    2: "Au_LC2_5CB_RT_1",
    3: "Au_LC3_5CB_RT_1",
    4: "Au_LC4_5CB_RT_1",
    5: "5CB_RT_1",
}
pxy_dict = {
    1: (-20700, 6744),
    2: (-7700, 6744),
    3: (6300, 6744),
    4: (20300, 6744),
    5: (33300, 6744),
}
# run_gisaxs_in_situHT()


##Run 53, In_situ HT 06:35 211030
ypos = 6744
sample_dict = {
    1: "Au_LC1_5CB_50_1",
    2: "Au_LC2_5CB_50_1",
    3: "Au_LC3_5CB_50_1",
    4: "Au_LC4_5CB_50_1",
    5: "5CB_50_1",
}
pxy_dict = {
    1: (-20700, 6744),
    2: (-7700, 6744),
    3: (6300, 6744),
    4: (20300, 6744),
    5: (33300, 6744),
}
# run_gisaxs_in_situHT()

##Run 54, In_situ HT 06:55 211030
ypos = 6744
sample_dict = {
    1: "Au_LC1_5CB_80_1",
    2: "Au_LC2_5CB_80_1",
    3: "Au_LC3_5CB_80_1",
    4: "Au_LC4_5CB_80_1",
    5: "5CB_80_1",
}
pxy_dict = {
    1: (-20700, 6744),
    2: (-7700, 6744),
    3: (6300, 6744),
    4: (20300, 6744),
    5: (33300, 6744),
}
# run_gisaxs_in_situHT()

##Run 55, In_situ HT 06:55 211030
ypos = 6744
sample_dict = {
    1: "Au_LC1_5CB_110_1",
    2: "Au_LC2_5CB_110_1",
    3: "Au_LC3_5CB_110_1",
    4: "Au_LC4_5CB_110_1",
    5: "5CB_110_1",
}
pxy_dict = {
    1: (-20700, 6744),
    2: (-7700, 6744),
    3: (6300, 6744),
    4: (20300, 6744),
    5: (33300, 6744),
}
# run_gisaxs_in_situHT()

##Run 56, In_situ HT 07:40 211030
ypos = 6744
sample_dict = {
    1: "Au_LC1_5CB_50_cool_1",
    2: "Au_LC2_5CB_50_cool_1",
    3: "Au_LC3_5CB_50_cool_1",
    4: "Au_LC4_5CB_50_cool_1",
    5: "5CB_50_cool_1",
}
pxy_dict = {
    1: (-20700, 6744),
    2: (-7700, 6744),
    3: (6300, 6744),
    4: (20300, 6744),
    5: (33300, 6744),
}
# run_gisaxs_in_situHT()

##Run 57, In_situ Evap 07:40 211030
ypos = 1015
sample_dict = {1: "Test"}
pxy_dict = {1: (7000, 1015)}
# run_gisaxs_in_situ_evap

##Run 58, In_situ Evap 08:25 211030
ypos = 610
sample_dict = {1: "PbS-Evap_30ul_open-1"}
pxy_dict = {1: (7000, 610)}
# run_gisaxs_in_situ_evap

##Run 59, In_situ Evap 08:45 211030
ypos = 610
sample_dict = {1: "PbS-Evap_30ul_close-1"}
pxy_dict = {1: (7000, 610)}
# run_gisaxs_in_situ_evap

##Run 60, In_situ Evap 08:55 211030
ypos = 610
sample_dict = {1: "PbS-Evap_30ul_close-2"}
pxy_dict = {1: (7000, 610)}
# run_gisaxs_in_situ_evap

##Run 61, In_situ Evap 09:15 211030
ypos = 610
sample_dict = {1: "PbS-Evap_30ul_close_Tvaper-3"}
pxy_dict = {1: (4000, 610)}
# run_gisaxs_in_situ_evap


##Run 62, In_situ Evap 09:50 211030
ypos = 610
sample_dict = {1: "Fe3O4-Evap_50ul_close_-1"}
pxy_dict = {1: (4000, 810)}
# run_gisaxs_in_situ_evap


##Run 63, In_situ Evap 09:50 211030
ypos = 610
sample_dict = {1: "Fe3O4-Evap_50ul_close_-1"}
pxy_dict = {1: (4000, 810)}
# run_gisaxs_in_situ_evap


##Run64_TEST
ypos = 610
sample_dict = {1: "Pt-Fe3O4-Grid-1", 2: "Pt-Fe3O4-slow-Si-1", 3: "Pt-Fe3O4-Grid_-2"}
pxy_dict = {1: (-12000, ypos), 2: (5000, ypos), 3: (23000, ypos)}
# run_gisaxs_in_situ_evap


# ypos = 700
# sample_dict = {    2: 'Pt-Fe3O4-slow-Si-1'   }
# pxy_dict = {   2:  (5000, ypos  )   }

ypos = 610
sample_dict = {
    1: "Pt-Fe3O4-Grid-1",
}
pxy_dict = {1: (-12000, ypos)}

ypos = 700
sample_dict = {3: "Pt-Fe3O4-Grid_-2"}
pxy_dict = {3: (23000, ypos)}


##Run65_TEST

ypos = 0
sample_dict = {1: "Au-Azo-G1-Si-1", 2: "Pt-Fe3O4-slow-Si-1", 3: "Ai-Azo-G2-Si_-1"}
pxy_dict = {1: (-14000, ypos), 2: (5000, ypos), 3: (23000, -250)}

# ypos = 900
# sample_dict = {    2: 'Pt-Fe3O4-slow-Si-1' , 3: 'Ai-Azo-G2-Si_-1'  }
# pxy_dict = {   2:  (5000, 900  ) , 3: (23000, 900) }


# ypos = 900
# sample_dict = {    2: 'test1' , 3: 'test2'  }
# pxy_dict = {   2:  (5000, 900  ) , 3: (23000, 900) }


##Run66 Pt-Fe3O4 on Si drop cast 50 ul 22:45
ypos = 0
sample_dict = {2: "Pt-Fe3O4-slow-vap-Si-1"}
pxy_dict = {2: (5400, 500)}

##Run67 Pt-Fe3O4 on Si drop cast 50 ul dry ChCl3 sva 23:41
ypos = 0
sample_dict = {
    1: "Au-Azo-G1-Si-_SVA-1",
    2: "Pt-Fe3O4-slow-vap-Si-SVA-1",
    3: "Ai-Azo-G2-Si_SVA-1",
}
pxy_dict = {1: (-14000, 300), 2: (5400, 500), 3: (23000, 300)}

##Run68 Pt-Fe3O4 on Si drop cast 50 ul dry ChCl3 sva 23:41 UV on 00:15  UV on 00:35
ypos = 0
sample_dict = {
    1: "Au-Azo-G1-Si-_SVA-2",
    2: "Pt-Fe3O4-slow-vap-Si-SVA-2",
    3: "Ai-Azo-G2-Si_SVA-2",
}
pxy_dict = {1: (-14000, 450), 2: (5400, 500), 3: (23000, 300)}


##Run69 Au-Azo-G2 on Si drop cast 50 ul 1:00 UV on 1:22
ypos = 0
sample_dict = {
    1: "Au-Azo-G1-Si-_Spin-2",
    2: "Au-Azo-G2-slow-vap-Si-SVA-2",
    3: "Ai-Azo-G2-Si_SVA-3",
}
pxy_dict = {1: (-14000, 500), 2: (5400, 500), 3: (23000, 300)}


##Run70 Au-Azo-G2 on Si drop cast 50 ul 1:00 UV on 1:22 CHCl3 01:39 UV off 2:05
ypos = 0
sample_dict = {
    1: "Au-Azo-G1-Si-_Spin-SVA-2",
    2: "Au-Azo-G2-slow-vap-Si-SVA-3",
    3: "Ai-Azo-G2-Si_SVA-4",
}
pxy_dict = {1: (-14000, 550), 2: (5400, 500), 3: (23000, 300)}


##Run71 Pt-Fe3O4 slow
ypos = 0
sample_dict = {1: "Pt-Fe3O4-15h-Si-1"}
pxy_dict = {1: (13000, 200)}


##Run72 Pt-Fe3O4 slow
ypos = 0
sample_dict = {1: "Pt-Fe3O4-2h-Si-1", 2: "Pt-Fe3O4-15h-Si-1", 3: "Pt-Fe3O4-spin-Si-1"}
pxy_dict = {1: (1000, 300), 2: (13000, 200), 3: (13000, 300)}

##Run73 Pt-Fe3O4 slow
ypos = 0
sample_dict = {1: "Pt-Fe3O4-spin-Si-1"}
pxy_dict = {1: (30000, 400)}

##Run74 Pt-Fe3O4 slow
ypos = 0
sample_dict = {1: "Pt-Fe3O4-insitu-Si-1", 3: "Pt-Fe3O4-1h-Si-1"}
pxy_dict = {1: (-3000, 700), 3: (30000, 550)}

##Run75 Pt-Fe3O4 slow
ypos = 0
sample_dict = {1: "Pt-Fe3O4-2h-Si-1"}
pxy_dict = {1: (13000, 400)}

##Run76 Pt-Fe3O4 slow
ypos = 0
sample_dict = {1: "Pt-Fe3O4-insitu-Si-2", 2: "Pt-Fe3O4-1h-Si-1"}
pxy_dict = {1: (-4000, 600), 2: (31000, 500)}

##Run77 Pt-Fe3O4 slow
ypos = 0
sample_dict = {1: "Pt-Fe3O4-4h-Si-1"}
pxy_dict = {1: (13000, 400)}

##Run78 Pt-Fe3O4 slow
ypos = 0
sample_dict = {
    1: "Au-LC1-RT-Si-1",
    2: "Au-LC2-RT-Si-1",
    3: "Au-LC3-RT-Si-1",
    4: "Au-LC4-RT-Si-1",
    5: "Au-G1-RT-Si-1",
}
pxy_dict = {
    1: (-11000, 6800),
    2: (3000, 6800),
    3: (17000, 6800),
    4: (30000, 6800),
    5: (43000, 6800),
}

##Run79 Pt-Fe3O4 slow
ypos = 0
sample_dict = {
    1: "Au-LC1-40-Si-1",
    2: "Au-LC2-40-Si-1",
    3: "Au-LC3-40-Si-1",
    4: "Au-LC4-40-Si-1",
    5: "Au-G1-40-Si-1",
}
pxy_dict = {
    1: (-11000, 6800),
    2: (3000, 6800),
    3: (17000, 6800),
    4: (30000, 6800),
    5: (43000, 6800),
}


##Run80 Pt-Fe3O4 slow
ypos = 0
sample_dict = {
    1: "Au-LC1-80-Si-1",
    2: "Au-LC2-80-Si-1",
    3: "Au-LC3-80-Si-1",
    4: "Au-LC4-80-Si-1",
    5: "Au-G1-80-Si-1",
}
pxy_dict = {
    1: (-11000, 6800),
    2: (3000, 6800),
    3: (17000, 6800),
    4: (30000, 6800),
    5: (43000, 6800),
}


##Run81 Pt-Fe3O4 slow
ypos = 0
sample_dict = {
    1: "Au-LC1-120-Si-1",
    2: "Au-LC2-120-Si-1",
    3: "Au-LC3-120-Si-1",
    4: "Au-LC4-120-Si-1",
    5: "Au-G1-120-Si-1",
}
pxy_dict = {
    1: (-11000, 6800),
    2: (3000, 6800),
    3: (17000, 6900),
    4: (30000, 6800),
    5: (43000, 6800),
}


##Run82 Pt-Fe3O4 slow
ypos = 0
sample_dict = {1: "Pt-Fe3O4-6h-Si-1"}
pxy_dict = {1: (13000, 400)}


##Run83 Pt-Fe3O4 slow
ypos = 0
sample_dict = {1: "Pt-Fe3O4-insitu-Si-3", 2: "Pt-Fe3O4-15h-Si-3", 3: "Pt-Fe3O4-1h-Si-3"}
pxy_dict = {1: (-4000, 600), 2: (13000, 400), 3: (31000, 500)}
####   RE( run_giwaxs())

x_list = np.array(list((pxy_dict.values())))[:, 0]
y_list = np.array(list((pxy_dict.values())))[:, 1]
sample_list = np.array(list((sample_dict.values())))
##################################################
############ Some convinent functions#################
#########################################################


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


def run_gisaxs_in_situSVP(
    N=200,
    sleep_time=2,
    x_list=x_list,
    sample_list=sample_list,
    expt=1,
    username=username,
    inc_angles=[0.05, 0.15, 0.3],
    x_shift_array=[-1000, 0, 1000],
):

    # define names of samples on sample bar
    assert len(x_list) == len(sample_list), f"Sample name/position list is borked"
    inc_angles = np.array(inc_angles)  # incident angles
    x_shift_array = np.array(x_shift_array)

    t0 = time.time()  # define t0
    td = time.gmtime()
    ts = time.strftime("%Y-%m-%d-%H-%M-%S", td)
    print(ts)
    dets = [pil900KW, pil1M, pil300KW]
    YPOS = {}
    ThPOS = {}
    th_real = inc_angles

    RE(bps.mv(waxs, 20))

    for i in range(N):  # loop time
        for ii, (x, sample) in enumerate(
            zip(x_list, sample_list)
        ):  # loop over samples on bar
            RE(bps.mv(piezo.x, x))  # move to next sample
            RE(bps.mv(piezo.y, y_list[ii]))
            if i == 0:
                RE(bps.mv(piezo.th, 0))
                RE(alignement_gisaxs(0.1))  # run alignment routine
                YPOS[ii] = piezo.y.position
                ThPOS[ii] = piezo.th.position
                print(YPOS, ThPOS)
            else:
                RE(bps.mv(piezo.y, YPOS[ii]))
                RE(bps.mv(piezo.th, ThPOS[ii]))

            th_meas = inc_angles + ThPOS[ii]
            x_pos_array = x + x_shift_array
            for x_meas in x_pos_array:  # measure at a few x positions
                RE(bps.mv(piezo.x, x_meas))  # move to x position
                for iii, th in enumerate(th_meas):  # loop over incident angles
                    RE(bps.mv(piezo.th, th))
                    ti = time.time()
                    treal = ti - t0
                    name_fmt = "{sample}_{th:5.4f}deg_ts{ts:s}_dt{dt:.0f}_x{x:05.2f}_y{y:05.2f}_z{y:05.2f}_det{saxs_z:05.2f}m_expt{t}s_sid{scan_id:08d}"
                    sample_name = name_fmt.format(
                        sample=sample,
                        th=th_real[iii],
                        ts=ts,
                        dt=treal,
                        x=np.round(piezo.x.position, 2),
                        y=np.round(piezo.y.position, 2),
                        z=np.round(piezo.z.position, 2),
                        saxs_z=np.round(pil1m_pos.z.position, 2),
                        t=expt,
                        scan_id=RE.md["scan_id"],
                    )
                    print(sample_name)
                    sample_id(user_name=username, sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    det_exposure_time(expt, expt)
                    RE(bp.count(dets, num=1))

        time.sleep(sleep_time)


def run_gisaxs_in_situ_evap(
    N=200,
    sleep_time=10,
    x_list=x_list,
    sample_list=sample_list,
    t=1,
    username=username,
    inc_angles=[0.05, 0.15, 0.3, 0],
    x_shift_array=[-1000, 0, 1000],
):

    # define names of samples on sample bar
    assert len(x_list) == len(sample_list), f"Sample name/position list is borked"
    inc_angles = np.array(inc_angles)  # incident angles
    x_shift_array = np.array(x_shift_array)

    t0 = time.time()
    td = time.gmtime()
    ts = time.strftime("%Y-%m-%d-%H-%M-%S", td)
    print(ts)
    dets = [pil900KW, pil1M]
    YPOS = {}

    th_meas = inc_angles + piezo.th.position
    th_real = inc_angles
    for i in range(N):
        for ii, (x, sample) in enumerate(
            zip(x_list, sample_list)
        ):  # loop over samples on bar
            RE(bps.mv(piezo.x, x))  # move to next sample
            # if i==0:
            # RE( alignement_gisaxs(0.1) ) #run alignment routine
            # YPOS[ii] =  piezo.y.position
            # else:
            # RE( bps.mv(piezo.y, YPOS[ii] ) )#move to next sample
            # RE( alignement_gisaxs(0.1) ) #run alignment routine
            # YPOS[ii] =  piezo.y.position

            det_exposure_time(t, t)
            x_pos_array = x + x_shift_array
            for x_meas in x_pos_array:  # measure at a few x positions
                RE(bps.mv(piezo.x, x_meas))
                for iii, th in enumerate(th_meas):  # loop over incident angles
                    RE(bps.mv(piezo.th, th))
                    ti = time.time()
                    treal = ti - t0
                    name_fmt = "{sample}_{th:5.4f}deg_ts{ts:s}_dt{dt:.0f}_x{x:05.2f}_y{y:05.2f}_z{y:05.2f}_det{saxs_z:05.2f}m_expt{t}s_sid{scan_id:08d}"
                    sample_name = name_fmt.format(
                        sample=sample,
                        th=th_real[iii],
                        ts=ts,
                        dt=treal,
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
                    RE(bp.count(dets, num=1))

        time.sleep(sleep_time)


def run_gisaxs_in_situHT(
    N=1,
    sleep_time=10,
    x_list=x_list,
    sample_list=sample_list,
    t=1,
    username=username,
    inc_angles=[0.05, 0.15, 0.3],
    x_shift_array=[-1000, 0, 1000],
):

    # define names of samples on sample bar
    assert len(x_list) == len(sample_list), f"Sample name/position list is borked"
    inc_angles = np.array(inc_angles)  # incident angles
    x_shift_array = np.array(x_shift_array)

    t0 = time.time()
    td = time.gmtime()
    ts = time.strftime("%Y-%m-%d-%H-%M-%S", td)
    print(ts)
    dets = [pil900KW, pil1M]
    YPOS = {}

    for i in range(N):
        for ii, (x, sample) in enumerate(
            zip(x_list, sample_list)
        ):  # loop over samples on bar
            RE(bps.mv(piezo.x, x))  # move to next sample
            if i == 0:
                RE(alignement_gisaxs(0.1))  # run alignment routine
                YPOS[ii] = piezo.y.position
            else:
                RE(bps.mv(piezo.y, YPOS[ii]))  # move to next sample
                # RE( alignement_gisaxs(0.1) ) #run alignment routine
                # YPOS[ii] =  piezo.y.position

            th_meas = inc_angles + piezo.th.position
            th_real = inc_angles
            det_exposure_time(t, t)
            x_pos_array = x + x_shift_array
            for x_meas in x_pos_array:  # measure at a few x positions
                RE(bps.mv(piezo.x, x_meas))
                for iii, th in enumerate(th_meas):  # loop over incident angles
                    RE(bps.mv(piezo.th, th))
                    ti = time.time()
                    treal = ti - t0
                    name_fmt = "{sample}_{th:5.4f}deg_ts{ts:s}_dt{dt:.0f}_x{x:05.2f}_y{y:05.2f}_z{y:05.2f}_det{saxs_z:05.2f}m_expt{t}s_sid{scan_id:08d}"
                    sample_name = name_fmt.format(
                        sample=sample,
                        th=th_real[iii],
                        ts=ts,
                        dt=treal,
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
                    RE(bp.count(dets, num=1))

        time.sleep(sleep_time)


def run_in_situ_RT_UV_swaxs(
    sample_name=sample_name, dx=0, N=200, sleep_time=10, dead_time=90, uv_time=120
):
    t0 = time.time()
    for i in range(N):
        ti = time.time()
        treal = ti - t0 + dead_time
        uv_timeR = ti - t0 + uv_time
        sample_i = sample_name + "_t_%.1f_uvt_%.1f" % (treal, uv_timeR)
        print("This is the %s run with time= %.0f for sam=%s" % (i, treal, sample_i))
        RE(bps.mv(waxs, 20))
        RE(
            measure_saxs(
                t=1.1, att="None", dx=dx, dy=0, user_name=username, sample=sample_i
            )
        )
        # run WAXS, if not run, just put a # in front of this line
        # RE( measure_waxs( t = 1.1, att='None', dx=dx, dy=0, user_name=username, sample= sample_i )  )
        # RE(snap_saxs( 1 ) )
        time.sleep(sleep_time)


def run_in_situ_HT_swaxs_single(
    sample_i,
    dx=0,
):
    RE(bps.mv(waxs, 20))
    RE(
        measure_saxs(
            t=1.1, att="None", dx=dx, dy=0, user_name=username, sample=sample_i
        )
    )
    # run WAXS, if not run, just put a # in front of this line
    RE(
        measure_waxs(
            t=1.1,
            waxs_angle=20,
            att="None",
            dx=dx,
            dy=0,
            user_name=username,
            sample=sample_i,
        )
    )


def run_in_situ_HT_swaxs(
    sample_name=sample_name,
    dx=0,
    N=200,
    sleep_time=10,
):
    t0 = time.time()
    td = time.gmtime()
    ts = time.strftime("%Y-%m-%d-%H-%M-%S", td)
    print(ts)
    for i in range(N):
        ti = time.time()
        treal = ti - t0
        sample_i = sample_name + "_tstart_%s_dt_%.0f" % (ts, treal)
        print("This is the %s run with time= %.0f for sam=%s" % (i, treal, sample_i))
        RE(bps.mv(waxs, 20))
        RE(
            measure_saxs(
                t=1.1, att="None", dx=dx, dy=0, user_name=username, sample=sample_i
            )
        )
        # run WAXS, if not run, just put a # in front of this line
        RE(
            measure_waxs(
                t=1.1, att="None", dx=dx, dy=0, user_name=username, sample=sample_i
            )
        )

        time.sleep(sleep_time)


def run_in_situ_RT_saxs(
    sample_name=sample_name, dx=0, N=100, sleep_time=10, dead_time=8 * 60
):
    t0 = time.time()
    for i in range(N):
        ti = time.time()
        treal = ti - t0 + dead_time
        sample_i = sample_name + "_t_%.1f" % treal
        print("This is the %s run with time= %.0f for sam=%s" % (i, treal, sample_i))
        RE(
            measure_saxs(
                t=1.1, att="None", dx=dx, dy=0, user_name=username, sample=sample_i
            )
        )
        # RE(snap_saxs( 1 ) )
        time.sleep(sleep_time)


def run_in_situ_RT_waxs(
    sample_name=sample_name, dx=0, N=100, sleep_time=10, dead_time=8 * 60
):
    t0 = time.time()
    for i in range(N):
        ti = time.time()
        treal = ti - t0 + dead_time
        sample_i = sample_name + "_t_%.1f" % treal
        print("This is the %s run with time= %.0f for sam=%s" % (i, treal, sample_i))
        RE(
            measure_waxs(
                t=1.1, att="None", dx=dx, dy=0, user_name=username, sample=sample_i
            )
        )
        # RE(snap_saxs( 1 ) )
        time.sleep(sleep_time)


def run_in_situ_RT_swaxs(
    sample_name=sample_name, dx=0, N=100, sleep_time=10, dead_time=90
):
    t0 = time.time()
    for i in range(N):
        ti = time.time()
        treal = ti - t0 + dead_time
        sample_i = sample_name + "_t_%.1f" % treal
        print("This is the %s run with time= %.0f for sam=%s" % (i, treal, sample_i))
        RE(bps.mv(waxs, 20))
        RE(
            measure_saxs(
                t=1.1, att="None", dx=dx, dy=0, user_name=username, sample=sample_i
            )
        )
        RE(
            measure_waxs(
                t=1.1, att="None", dx=dx, dy=0, user_name=username, sample=sample_i
            )
        )
        # RE(snap_saxs( 1 ) )
        time.sleep(sleep_time)


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


def run_giwaxs(
    x_list=x_list,
    sample_list=sample_list,
    t=1,
    username=username,
    inc_angles=[0.05, 0.15, 0.3],
    waxs_angles=[0, 20],
    x_shift_array=[-500, -400, -300, -200, -100, 0, 100, 200, 300, 400, 500],
    saxs_on=True,
):
    # define names of samples on sample bar
    assert len(x_list) == len(sample_list), f"Sample name/position list is borked"
    inc_angles = np.array(inc_angles)  # incident angles
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
        # yield from  bps.mv(piezo.y, 4000  ) #move y to 4000
        yield from alignement_gisaxs(0.1)  # run alignment routine
        TH = piezo.th.position
        th_meas = inc_angles + piezo.th.position
        th_real = inc_angles
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
                        name_fmt = "{sample}_{th:5.4f}deg_waxsN{waxs_angle:05.2f}_x{x:05.2f}_y{y:05.2f}_z{y:05.2f}_det{saxs_z:05.2f}m_expt{t}s_sid{scan_id:08d}"
                    else:
                        name_fmt = "{sample}_{th:5.4f}deg_waxsP{waxs_angle:05.2f}_x{x:05.2f}_y{y:05.2f}_z{y:05.2f}_det{saxs_z:05.2f}m_expt{t}s_sid{scan_id:08d}"
                    sample_name = name_fmt.format(
                        sample=sample,
                        th=th_real[i],
                        waxs_angle=waxs_angle,
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
    if sample is None:
        sample = RE.md["sample"]
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
    if sample is None:
        sample = RE.md["sample"]
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
    t=1, waxs_angle=20, att="None", dx=0, dy=0, user_name=username, sample=None
):
    if sample is None:
        sample = RE.md["sample"]
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
        sample = RE.md["sample"]
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

'''
20240727

314415	Standard	Approved	GUP-311773: Understanding of the microstructure of liquid and polymer electrolyte in lithium metal battery	Enyuan Hu


proposal_id('2024_2', '314415_EHu')  #for Hu's samples


# SAXS distance , 5 meter, in air
# 1M [ -4.84, -57.84, 5000  ]
# beam stop [ 1.94, 288.99,  13  ], a rod
# beam center [ 458, 577 ],
# beamstop_save()




'''

print('Load  micro -- 2024July27...')
from datetime import datetime



##############Run 
user_name = "EHu"
username = user_name
#{ i: 'S%03d'%i for i in range(1, 16 ) }

# #RUN 1, Sample from S1 to S15  
# sample_dict = {1: 'S001',
#  2: 'S002',
#  3: 'S003',
#  4: 'S004',
#  5: 'S005',
#  6: 'S006',
#  7: 'S007',
#  8: 'S008',
#  9: 'S009',
#  10: 'S010',
#  11: 'S011',
#  12: 'S012',
#  13: 'S013',
#  14: 'S014',
#  15: 'S015'}


# # pxy_dict = {  1:  (   44500, -5000 ),  2:  (   38100, -5000 ),  3:  (   32100, -5000 ), 4:  (  25700, -5000 ),
# #              5:  (  19000, -5000 ),
# # 6:  (  12500, -5000 ),  7:  (  6100, -5000 ),  8:  (   100, -5000 ),  9:  (  -6300, -5000 ),
# # 10:  ( -12500, -5000 ), 
# # 11:  ( -19100, -5000 ),  
# # 12:  (  -25300, -5000 ), 
# #  13:  ( -31700, -5000 ), 
# # 14:  (   -38302, -5000 ),
# # 15: (-44700, -5000)

# #       }

# pxy_dict = {15: [44500 -200, -5000],
#  14: [38100 - 200, -5000],
#  13: [32100 - 400, -5000],
#  12: [25700 - 200 , -5000   ],
#  11: [19000, -5000],
#  10: [12500  , -5000 ],
#  9: [6100, -5000],
#  8: [100 - 200 , -5000],
#  7: [-6300 - 200, -5000],
#  6: [-12500- 200, -5000],
#  5: [-19100 - 200, -5000],
#  4: [-25300, -5000],
#  3: [-31700 - 200, -5000],
#  2: [-38302 + 200, -5000],
#  1: [-44700, -5000]}




# #RUN 2, Sample from S16 to S30   
# sample_dict = { i: 'S%03d'%( i + 15)  for i in range(1, 16 ) }
# pxy_dict = {15: [44500 - 200, -5000],
#  14: [38100 - 200, -5000],
#  13: [32100 - 400 - 150, -5000],
#  12: [25700 - 200 -150 , -5000   ],
#  11: [19000 - 300, -5000],
#  10: [12500  , -5000 ],
#  9: [6100, -5000],
#  8: [100 - 200 - 200 , -5000],
#  7: [-6300 - 200 - 200, -5000],
#  6: [-12500- 200 -300, -5000],
#  5: [-19100 - 200, -5000],
#  4: [-25300 - 500, -5000],
#  3: [-31700 - 200 - 300, -5000],
#  2: [-38302 + 200 - 400, -5000],
#  1: [-44700 -200, -5000]}

# #RUN 3, Sample from S31 to S45   
# sample_dict = { i: 'S%03d'%( i + 30)  for i in range(1, 16 ) }
# pxy_dict = {15: [44500 - 200 -300, -5000],
#  14: [38100 - 300, -5000],
#  13: [32100 - 400 - 250, -5000],
#  12: [25700 - 200 -550 , -5000   ],
#  11: [19000 - 300, -5000],
#  10: [12500 -500, -5000 ],
#  9: [6100 -400, -5000],
#  8: [100 - 200 - 600 , -5000],
#  7: [-6300 - 200 - 300, -5000],
#  6: [-12500- 200 -600, -5000],
#  5: [-19100 - 600, -5000],
#  4: [-25300 - 500, -5000],
#  3: [-31700 - 200 - 400, -5000],
#  2: [-38302 + 200 - 500, -5000],
#  1: [-44700 -300, -5000]}



# #RUN 4, Sample from S46 to S60   
# sample_dict = { i: 'S%03d'%( i + 45 )  for i in range(1, 16 ) }
# pxy_dict = {15: [44500 - 200, -5000],
#  14: [38100 - 200, -5000],
#  13: [32100 - 400 - 150, -5000],
#  12: [25700 - 200 -150 , -5000   ],
#  11: [19000 - 300, -5000],
#  10: [12500  , -5000 ],
#  9: [6100, -5000],
#  8: [100 - 200 - 200 , -5000],
#  7: [-6300 - 200 - 200, -5000],
#  6: [-12500- 200 -300, -5000],
#  5: [-19100 - 200, -5000],
#  4: [-25300 - 500, -5000],
#  3: [-31700 - 200 - 300, -5000],
#  2: [-38302 + 200 - 400, -5000],
#  1: [-44700 -200, -5000]}


# #RUN 4.5, Sample from S46 to S60   
# sample_dict = { i: 'S%03d'%( i + 45 )  for i in range(15, 16 ) }
# pxy_dict = {15: [44500 - 200, -5000 - 2000],
# }



#RUN 5, Sample from S61 to S75   
# sample_dict = { i: 'S%03d'%( i + 60)  for i in range(1, 15 ) }
# pxy_dict = {
#  #15: [44500 - 200 -300, -5000],
#  14: [38100 - 300 - 300, -5000],
#  13: [32100 - 400 - 250, -5000],
#  12: [25700 - 200 -550 , -5000   ],
#  11: [19000 - 300 - 300, -5000],
#  10: [12500 -500 + 200, -5000 ],
#  9: [6100 -400, -5000],
#  8: [100 - 200 - 600 , -5000],
#  7: [-6300 - 200 - 300, -5000],
#  6: [-12500- 200 -600, -5000],
#  5: [-19100 - 600, -5000],
#  4: [-25300 - 500, -5000],
#  3: [-31700 - 200 - 400, -5000],
#  2: [-38302 + 200 - 500, -5000],
#  1: [-44700 -300, -5000]}




#RUN 6, HKim's Sample  
# user_name = "HKim"
# username = user_name
# proposal_id('2024_2', '313765_YZhang2')   
# sample_dict = { 1: 'Cu95nm_old_capillary',  2: 'Cu95nm_new_capillary' }
# pxy_dict = {
 
#  1: [38100 - 300 , -5000],
#  2: [ 44050, -5000],
#  }


# #RUN 6.5, HKim's Sample  
# user_name = "HKim"
# username = user_name
# proposal_id('2024_2', '313765_YZhang2')   
# sample_dict = { 1: 'Cu95nm_old_tubing',  2: 'Cu95nm_new_tubing' }
# pxy_dict = {
#  #15: [44500 - 200 -300, -5000],
#  2: [38100 - 300 , -5000],
#  1: [32100 - 400 - 250, -5000],
#  }
 

#proposal_id('2024_2', '313765_YZhang2')   
# sample_dict = { 1: 'Cu95nm_new_tubing'  }
# pxy_dict = {
#  #15: [44500 - 200 -300, -5000],
#  #2: [38100 - 300 , -5000],
#  1: [ -7200, 5000 ],
#  }


# proposal_id('2024_2', '313765_YZhang2')   
# sample_dict = { 1: 'Cu95nm_new_Kapton'  }
# pxy_dict = {
#  #15: [44500 - 200 -300, -5000],
#  #2: [38100 - 300 , -5000],
#  1: [ -8000, 0 ],
#  }




# sample_dict = { 1: 'Cu95nm_old_tubing'  }
# pxy_dict = {
#  #15: [44500 - 200 -300, -5000],
#  #2: [38100 - 300 , -5000],
#  1: [ 0, 1780 ],
#  }





#RUN 7, TLi's Sample  
# user_name = "TLi"
# username = user_name
# #proposal_id('2024_2', '00005_TLi')  

# sample_dict = { i: 'I%03d'%( i )  for i in range(1, 7 ) }
# sample_dict[7] = 'ACN'
# sample_dict2 = { i: 'MA%03d'%( i - 7 )  for i in range(8, 13 ) }
# sample_dict.update( sample_dict2 )


# pxy_dict = {
#  #15: [44500 - 200 -300, -5000],
# #  14: [38100 - 300 - 300, -5000],
# #  13: [32100 - 400 - 250, -5000],
#  12: [25700 - 200  -150, -5000   ],
#  11: [19000 - 300 - 300 + 150, -5000],
#  10: [12500 -500 + 400 - 250, -5000 ],
#  9: [6100 -400+100, -5000],
#  8: [100 - 200 - 600 + 150 - 150 , -5000],
#  7: [-6300 - 200 - 300, -5000 - 1000 - 3000  ],
#  6: [-12500- 200 -600, -5000 + 500 - 3000 ],
#  #5: [-19100 - 600 - 2000, -5000 - 3000 ],
#  5: [ -20100, -5000 - 3000 - 200 - 1000 ],
#  4: [-25300 - 500, -5000  - 1000 ] ,
#  3: [-31700 - 200 - 400, -5000],
#  2: [-38302 + 200 - 500, -5000],
#  1: [-44700 -300, -5000]}

# sample_dict = {   }
# sample_dict[5] = 'I005'
 
# pxy_dict = {

#  5: [ -19700, -5000 - 3000 - 200 - 1000 ],
# }






# # # #RUN 8, TLi's Sample  
# user_name = "TLi"
# username = user_name
# #proposal_id('2024_2', '00005_TLi')  
# sample_dict = { i: 'J%03d'%( i )  for i in range(1, 5 ) }
# sample_dict[5] = 'MB001'
# sample_dict[6] = 'J005'
# sample_dict2 = { i: 'MB%03d'%( i - 5 )  for i in range(7, 11 ) }
# sample_dict[11] = 'DJ'
# sample_dict[12] = 'MB006'
# sample_dict[13] = 'MB007'
# sample_dict.update( sample_dict2 )


# pxy_dict = {
#  #15: [44500 - 200 -300, -5000],
# #  14: [38100 - 300 - 300, -5000],
# 13: [32100 - 400 - 250, -5000],
#  12: [25700 - 200 - 400   , -5000   ],
#  11: [19000 - 300 - 300 + 150, -5000],
#  10: [12500 -500 + 400 - 400, -5000 ],
#  9: [6100 -400+100, -5000],
#  8: [100 - 200 - 600 + 150 , -5000], 
#  7: [-6300 - 200 - 300, -5000],
#  6: [-12500- 200 -600, -5000 + 500],
#  5: [-19100 - 600 - 200, -5000],
#  4: [-25300 - 500, -5000],
#  3: [-31700 - 200 - 400, -5000],
#  2: [-38302   - 500, -5000],
#  1: [-44700 -300, -5000]}




# # #RUN 9, TLi's Sample  
# user_name = "TLi"
# username = user_name
# #proposal_id('2024_2', '00005_TLi')  
# sample_dict = { i: 'G%03d'%( i + 2 )  for i in range(1, 6 ) }
# sample_dict2 = { i: 'J%03d'%( i +20 )  for i in range(6, 14 ) }
# sample_dict[14] = 'G001'
# sample_dict[15] = 'G002' 
# sample_dict.update( sample_dict2 )
# pxy_dict = {
#  15: [44500 - 200  , -5000 -1000],
#   14: [38100 - 300 - 300, -5000 - 1000],
# 13: [32100 - 400 - 250 - 100, -5000],
#  12: [25700 - 200 - 400   , -5000   ],
#  11: [19000 - 300 - 300 + 150, -5000],
#  10: [12500 -500 + 200, -5000 ],
#  9: [6100 -400+100, -5000],
#  8: [100 - 200 - 600 + 150 , -5000], 
#  7: [-6300 - 200 - 300, -5000],
#  6: [-12500- 200 -600, -5000 + 500],
#  5: [-19100 - 600 - 200 +200, -5000],
#  4: [-25300 - 500, -5000],
#  3: [-31700 - 200 - 400, -5000],
#  2: [-38302   - 500 + 200, -5000],
#  1: [-44700 -300, -5000]}




#RUN 10, Sample from S75 to S94   
#   proposal_id('2024_2', '314415_EHu')

# sample_dict = { i: 'S%03d'%( i + 74 )  for i in range(1,  21 ) }

# pxy_dict = {
#  #15: [44500 - 200 -300, -5000],
#  14: [38100 - 300 - 300, -5000],
#  13: [32100 - 400 - 250, -5000],
#  12: [25700 - 200 -550 , -5000   ],
#  11: [19000 - 300 - 300, -5000],
#  10: [12500 -500 + 200, -5000 ],
#  9: [6100 -400, -5000],
#  8: [100 - 200 - 600 , -5000],
#  7: [-6300 - 200 - 300, -5000],
#  6: [-12500- 200 -600, -5000],
#  5: [-19100 - 600, -5000],
#  4: [-25300 - 500, -5000],
#  3: [-31700 - 200 - 400, -5000],
#  2: [-38302 + 200 - 500, -5000],
#  1: [-44700 -300, -5000]}


# # #RUN 9, TLi's Sample  
# user_name = "TLi"
# username = user_name
# proposal_id('2024_2', '00005_TLi')  
# sample_dict = { i: 'XL%03d'%( i   )  for i in range(1, 11 ) }
# sample_dict2 = { i: 'MD%03d'%( i -10 )  for i in range(11, 16 ) }
 
# sample_dict.update( sample_dict2 )
# pxy_dict = {
#  15: [44500   , -5000  - 1000 ],
#   14: [38100 - 300  , -5000  ],
# 13: [32100 - 400 - 250 - 100, -5000],
#  12: [25700 - 200 - 400 + 150  , -5000   ],
#  11: [19000 - 300 - 300 + 150, -5000],
#  10: [12500 -500 + 400, -5000 ],
#  9: [6100 -400+300, -5000],
#  8: [100 - 200 - 600 + 300 , -5000], 
#  7: [-6300 - 200 - 300, -5000],
#  6: [-12500- 200 -600 + 150 , -5000  ],
#  5: [-19100 - 600 - 200 +200 + 150 , -5000],
#  4: [-25300 - 500 + 150, -5000],
#  3: [-31700 - 200 - 400 + 100, -5000],
#  2: [-38302   - 500 + 300, -5000],
#  1: [-44700  - 500, -5000]}


# # #RUN 10, TLi's Sample  
# user_name = "TLi"
# username = user_name
# proposal_id('2024_2', '00005_TLi')  

# sample_dict = { i: 'JW%03d'%( i + 37   )  for i in range(3, 14 ) }
# sample_dict2 = { i: 'ZY%03d'%( i -13 )  for i in range(14, 16 ) }
# sample_dict[1] = 'MD006'
# sample_dict[2] = 'H2O'
# sample_dict.update( sample_dict2 )
# pxy_dict = {
#  15: [44500   , -5000    ],
#   14: [38100 - 300  , -5000  ],
# 13: [32100 - 400  , -5000],
#  12: [25700  - 400 + 150  , -5000   ],
#  11: [19000 - 300   + 150, -5000],
#  10: [12500 -200 + 400, -5000 ],
#  9: [6100  +300, -5000],
#  8: [100 - 200   + 300 , -5000], 
#  7: [-6300 - 200 - 300, -5000],
#  6: [-12500  -600 + 150 , -5000  ],
#  5: [-19100 - 600 - 200 +200 + 150 , -5000],
#  4: [-25300   + 150, -5000],
#  3: [-31700 - 200 - 400 + 300, -5000],
#  2: [-38302   - 100 + 300, -5000],
#  1: [-44700   , -5000]}



#    RE( shclose() );move_waxs(0)

# #RUN 11, TLi's Sample  
# user_name = "TLi"
# username = user_name
# proposal_id('2024_2', '00005_TLi')  

# sample_dict = { i: 'ZY%03d'%( i + 2   )  for i in range(1, 6 ) }
# sample_dict2 = { i: 'Jiaqi%03d'%( i - 5 )  for i in range(6, 16 ) } 
# sample_dict.update( sample_dict2 )
# pxy_dict = {
#  15: [44500 + 150    , -5000 - 1000    ],
#   14: [38100    , -5000  ],
# 13: [32100 - 400  , -5000],
#  12: [25700  - 400 + 150  , -5000   ],
#  11: [19000 - 300   + 150, -5000],
#  10: [12500 -200 + 400, -5000 ],
#  9: [6100  +300 - 200, -5000],
#  8: [100 - 200     , -5000], 
#  7: [-6300  - 300, -5000],
#  6: [-12500  -600 + 150 + 150 , -5000  ],
#  5: [-19100 - 600   + 150 + 150 , -5000],
#  4: [-25300   + 150, -5000],
#  3: [-31700 - 200 - 400 + 300, -5000],
#  2: [-38302   - 100 + 300, -5000],
#  1: [-44700   , -5000]}




# # #RUN 12, TLi's Sample  
# user_name = "TLi"
# username = user_name
# proposal_id('2024_2', '00005_TLi')  

# sample_dict = {   }
# sample_dict[ 1 ] = 'H001'
# sample_dict[ 2 ] = 'H002'
# sample_dict[ 3 ] = 'BK'
# sample_dict2 = { i: 'H%03d'%( i   )  for i in range(4, 10 ) }  
# sample_dict3 = { i: 'Jiaqi%03d'%( i  +1  )  for i in range(10, 16 ) } 
# sample_dict.update( sample_dict2 )
# sample_dict.update( sample_dict3)

# pxy_dict = {
#  15: [44500 + 150    , -5000      ],
#   14: [38100    , -5000  ],
# 13: [32100 - 400  , -5000],
#  12: [25700  - 400 + 150  , -5000   ],
#  11: [19000 - 300   + 150, -5000],
#  10: [12500 -200 + 400 + 200, -5000 ],
#  9: [6100  + 500 + 300, -5000],
#  8: [100 - 200     , -5000], 
#  7: [-6300  - 300, -5000],
#  6: [-12500  -600 + 150 + 150 , -5000  ],
#  5: [-19100 - 300 + 150 , -5000],
#  4: [-25300   + 150, -5000],
#  3: [-31700 - 200 - 400 + 300, -5000],
#  2: [-38302   - 100 + 300 + 150 , -5000],
#  1: [-44700 +500  , -5000]}



# # #RUN 13, TLi's Sample  
# user_name = "TLi"
# username = user_name
# proposal_id('2024_2', '00005_TLi')   
# sample_dict = { i: 'Jiaqi%03d'%( i  + 16  )  for i in range(1, 14 ) } 
# pxy_dict = {
# # 15: [44500 + 150    , -5000      ],
# #  14: [38100    , -5000  ],
# 13: [32100 - 400  , -5000],
#  12: [25700   + 150 -800 , -5000   ],
#  11: [19000 - 300   + 150, -5000],
#  10: [12500 -200 - 200  , -5000 ],
#  9: [6100  +200, -5000],
#  8: [100 - 200     , -5000], 
#  7: [-6300  - 300, -5000],
#  6: [-12500  -600 -100 , -5000  ],
#  5: [-19100  -600 , -5000],
#  4: [-25300    , -5000],
#  3: [-31700 - 200 - 400 + 300, -5000],
#  2: [-38302   - 100   + 150 , -5000],
#  1: [-44700 +200   , -5000]}



# #RUN 14, Jim's Sample  
# user_name = "IHan"
# username = user_name
# proposal_id('2024_2', '00006_IHan')   
# sample_dict = {   } 
# sample_dict[ 2 ] = 'Blank'
# sample_dict[ 4 ] = 'Pt_DIW'
# sample_dict[ 6 ] = 'ZnK_1p5'


# pxy_dict = {
 
#  6: [-12500  -600 + 200 , -5000  ],
#  4: [-25300 -300   , -5000 +1000],
#  2: [-38302   - 100   + 150 , -5000],
#  }


# #RUN 15, Jim's Sample  
# user_name = "IHan"
# username = user_name
# proposal_id('2024_2', '00006_IHan')   
# sample_dict = {   } 
# sample_dict[ 2 ] = 'Blank'
# sample_dict[ 4 ] = 'Pt_DIW'
# sample_dict[ 6 ] = 'ZnK_1p5'


# pxy_dict = {
 
#  6: [-12500  -600 + 200 , -5000  ],
#  4: [-25300 -300   , -5000 +1000],
#  2: [-38302   - 100   + 150 , -5000],
#  }

# #RUN 16, Jim's Sample  
# user_name = "IHan"
# username = user_name
# proposal_id('2024_2', '00006_IHan')   
# sample_dict = {   } 
# sample_dict[ 1 ] = 'S3'
# sample_dict[ 2 ] = 'S2'
# sample_dict[ 3 ] = 'S1'


# pxy_dict = {
 
#  1: [ 32550 , -5000  ],
#  2: [-1660  , -5000  ],
#  3: [ -20310 , -5000],
#  }



# #RUN 17, NWang's Sample  
# user_name = "EHu"
# username = user_name
# proposal_id('2024_2', '314415_EHu')  
# sample_dict = { i: 'N%03d'%( i  + 74  )  for i in range(1, 21  ) } 
# pxy_dict = {

# 1: [ 42400, 1100  ],
# 2 : [39000, 1100 ],
# 3: [ 35600, 1100  ],
# 4 : [ 31600, 1100 ],
# 5 : [ 27600, 1100 ],
# 6 : [ 22999, 1100 ],
# 7 : [ 18299, 1100 ],
# 8 : [ 14498, 1100 ],
# 9 : [ 9198, 1100 ],
# 10 : [ 4598, 1100 ], 
# 11 : [ -1301, 1100 ], 
# 12 : [ -6001, 499.9 ],
# 13 : [ -11202, 1200 ],
# 14 : [ -16502, 1200 ],
# 15 : [ -21502, 499.9 ],
# 16 : [ -26402, 799.9 ],
# 17 : [ -31002, 799.9 ],
# 18 : [ -36402, 799.9 ],
# 19 : [ -40802, 799.9 ],
# 20 : [ -45402, 799.9 ],
#  }



# #RUN 18, NWang's Sample  
user_name = "EHu"
username = user_name
proposal_id('2024_2', '314415_EHu')  
sample_dict = { i: 'N%03d'%( i  + 94  )  for i in range(1, 19  ) } 
pxy_dict = {

18: [ 44397, 1999.9  ],
17 : [ 39297, 1999.9 ],
16 : [ 34697, 1999.9 ],
15 : [ 30197, 1599.9 ],
14 : [ 25497, 1599.9 ],
13 : [ 20497, 1599.9 ],
12 : [ 15598, 1599.9 ],
11 : [ 9798, 1599.90 ], 
10 : [ 4497, 1599.9 ], 
9 : [ -902, 1599.9 ],
8 : [ -6902, 1599.9 ],
7 : [ -11801, 1099 ],
6 : [ -17701, 1099.9 ],
5 : [ -22901, 1099.9 ],
4 : [ -27601, 1099.9 ],
3 : [ -33201, 1099.9 ],
2 : [ -38700, 1599.9 ],
1 : [ -43700, 799.9 ],
 }

## pos_dic={
# 6:[ 34996,-4200],
# 7:[ 23997,-882.3],
# 8:[ 9497.0,-882.3],
# Ir:[ -43003.15,-2037.81]}  #hexpod = 0.5
#
##pos_dic2={
# 0:[-24966,-10346.8],
# 4:[8496.7,-10808.8]}   #hexpod = -9.0






#RE( measure_waxs( waxs_angle = 0, user_name = user_name, sample = RE.md['sample'] ) )
# RE( measure_wsaxs( t=1, waxs_angle=20, user_name= user_name, sample= RE.md['sample']  )) 





dx =  0 # #500 + 150 #0 #-400 + 200
dy =  0 #5000 + 1000
ks = np.array(list((sample_dict.keys())))
pxy_dict = {k: [pxy_dict[k][0] + dx, pxy_dict[k][1] + dy] for k in ks}

#x_list = np.array(list((pxy_dict.values())))[:, 0]
#y_list = np.array(list((pxy_dict.values())))[:, 1]
#sample_list = np.array(list((sample_dict.values())))


##################################################
############ Some convinent functions#################
#########################################################
# def mov_sam(  i  ):
#     #i = i - 1 
#     px = pxy_dict[i][0]       
#     py = pxy_dict[i][1]       
#     RE(  bps.mv(piezo.x, px) )
#     RE(  bps.mv(piezo.y, py) )
#     print('Move to pos=%s for sample:%s...'%(i , sample_dict[i] ))





def measure_series_multi_angle_wsaxs( t= [ 1 ], waxs_angles=[0,  20 ], dys = [ 0  ] ):

    """
    
    t0=time.time();RE(measure_series_multi_angle_wsaxs());run_time(t0)

    t0=time.time();RE( measure_series_multi_angle_wsaxs( t= [ 1 ], waxs_angles=[  15 ], dys = [ 0  ] )  );run_time(t0)
    
  


    """

    ks = list(sample_dict.keys())  # [:8 ]
    maxA = np.max(waxs_angles)
    for waxs_angle in waxs_angles:
        yield from bps.mv(waxs, waxs_angle)  
        for k in ks:
            print(k)
            yield from mov_sam_re(k)
            for dy in dys:
                print(dy)
                print("here we go ... ")
                for ti in t:
                    RE.md["sample_name"] = sample_dict[k]
                    sample = sample_dict[k]
                    if waxs_angle == maxA:
                        yield from measure_wsaxs(
                            t=ti, waxs_angle=waxs_angle, att="None", dy=dy, sample = sample
                        )
                    else:
                        yield from measure_waxs(
                            t=ti, waxs_angle=waxs_angle, att="None", dy=dy, sample = sample
                        )







def do_line_trans_scan( sample ='4AMP_C_',  t=1,  scan_range = [ 0,  100 ], 
                 scan_step  = 2,  method='V',  camera=True,   username = username,  ):
    
    ''''
 
    RE(   do_line_trans_scan(    )     )
    
    
    '''
    YH = piezo.y.position 
    XH = piezo.x.position 
    TH = piezo.th.position 


    waxs_angle = 20 
    dets = [ pil900KW,  pil1M ] #
    #dets = [ pil900KW  ] #

    yield from bps.mv(waxs, waxs_angle)  
    if method == 'V':
        vals =  np.arange( scan_range[0], scan_range[-1]+scan_step, scan_step  ) + YH     
    elif method == 'H':
        vals =  np.arange( scan_range[0], scan_range[-1]+scan_step, scan_step  ) + XH   
    det_exposure_time(t,t) 
    for v in vals:
        if method == 'V':
            yield from bps.mv(piezo.y, v)                  
        elif method == 'H':      
                yield from bps.mv(piezo.x, v)  
        name_fmt = '{sample}_x{x:05.2f}_y{y:05.2f}_th{th:05.2f}_waxs{waxs_angle:05.2f}_expt{t}s' 
        sample_name = name_fmt.format( sample = sample, x= piezo.x.position ,  y= piezo.y.position,
                                       th=piezo.th.position,
                                       waxs_angle=waxs_angle, t=t )  
        sample_id(user_name=  username , sample_name=sample_name)                     
        print(f'\n\t=== Sample: {sample_name} ===\n')  
        yield from bp.count( dets, num=1)  
        yield from bps.sleep(2)
       
    yield from bps.mv(piezo.x, XH)        
    yield from bps.mv(piezo.y, YH )  
       





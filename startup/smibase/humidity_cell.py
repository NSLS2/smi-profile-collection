import time
import numpy as np
from .ioLogik import moxa_in, moxa_out


def readHumidity(temperature=25, voltage_supply=5, verbosity=3):
    voltage_out = moxa_out.ch1_read.get()
    corr_voltage_out = voltage_out * (5.0 / voltage_supply)
    coeff_offset = 0.816887
    coeff_slope = 0.028813
    sensor_RH = (corr_voltage_out - coeff_offset) / coeff_slope
    true_RH = sensor_RH / (1.0546 - 0.00216 * temperature)  # T in [degC]
    if verbosity >= 3:
        print("Raw sensor RH = {:.3f} pct.".format(sensor_RH))
        print(
            "T-corrected RH = {:.3f} pct at {:.3f} degC.".format(true_RH, temperature)
        )
    return np.round(true_RH, 2)


def readHumidity2(temperature=25, voltage_supply=5, verbosity=3):
    voltage_out = moxa_out.ch2_read.get()
    corr_voltage_out = voltage_out * (5.0 / voltage_supply)
    coeff_offset = 0.816887
    coeff_slope = 0.028813
    sensor_RH = (corr_voltage_out - coeff_offset) / coeff_slope
    true_RH = sensor_RH / (1.0546 - 0.00216 * temperature)  # T in [degC]
    if verbosity >= 3:
        print("Raw sensor RH = {:.3f} pct.".format(sensor_RH))
        print(
            "T-corrected RH = {:.3f} pct at {:.3f} degC.".format(true_RH, temperature)
        )
    return np.round(true_RH, 2)


# moxa_in.ch4_sp.put(5)


def setDryFlow(voltage=None):
    if voltage == None or voltage > 5 or voltage < 0:
        print("Input voltage betwee 0 and 5V")
    moxa_in.ch1_sp.put(0)
    time.sleep(0.5)
    moxa_in.ch1_sp.put(voltage)


def setWetFlow(voltage=0):
    if voltage == None or voltage > 5 or voltage < 0:
        print("Input voltage betwee 0 and 5V")
    moxa_in.ch3_sp.put(0)
    time.sleep(0.5)
    moxa_in.ch3_sp.put(voltage)


"""

humidity list

humidity,    wet,     dry         2nd day, recheck
48           3         3

71           3         2.5                      
80           3         2.4/2.35        ###        

56           3         2.8  
60           3         2.7              ### 

43           3         3.3              
41           3         3.4              
40           3         3.45/3.6       ### 

20       2.5/2.4       3             ### 

#2022/3/4 humidity list
humidity    wet     dry         eq.time recheck
80          3       2.35    5 min 75%, struggle
80          3       2.3     30s 78%;    1 min 80.5;  2min 82.5
*80          3       2.33    1 min 79%   5 min 80.2%  10 min drop to 79.7
*70          3       2.5     1 min 61% struggle
70          3       2.45    1 min 66%
*70            3       2.42    1 min 69%; 2min 70%; 5 min 70.04%
*60          3       2.53    30s 60.1%; 1 min 60.7%; 5 min 60.6%
50          3       3       1 min 42%; 4 min 41.79%
50          3       2.7       1 min 49.9%; 2 min 50.1%; 5 min 50.3%

#20220304 conclusion, updated chart
humidity    wet dry 
80          3   2.33
70          3   2.42
60          3   2.53
50          3   2.7
42%         3   3



"""

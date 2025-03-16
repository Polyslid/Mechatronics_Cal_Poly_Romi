"""
Mecha 12
edited: 2/17/2025   
Line Sensor code for the Romi
"""
import pyb
from pyb import Pin
import math
from time import ticks_ms, ticks_diff, sleep_ms
import array

class Line_Sensor:

    def __init__(self, CTRL, ADC1, ADC3, ADC5, ADC7, ADC9, ADC11, ADC13):

        # Set up ctrl pin for sensor lights
        self.ctrl = Pin(CTRL, mode=Pin.OUT_PP)
        self.ctrl.high()
        # Set up each sensor pin as ADC
        self.adc1 = pyb.ADC(ADC1)
        self.adc3 = pyb.ADC(ADC3)
        self.adc5 = pyb.ADC(ADC5)
        self.adc7 = pyb.ADC(ADC7)
        self.adc9 = pyb.ADC(ADC9)
        self.adc11 = pyb.ADC(ADC11)
        self.adc13 = pyb.ADC(ADC13)

    def update(self):
        line_13 = self.adc13.read()
        line_11 = self.adc11.read()
        line_9 = self.adc9.read()
        line_7 = self.adc7.read()
        line_5 = self.adc5.read()
        line_3 = self.adc3.read()
        line_1 = self.adc1.read()
        line_sensor_array = array.array("f", [line_1, line_3,
                                               line_5, line_7, line_9, 
                                               line_11, line_13])
        count = 0 # Initialize count for loop
        set_zero = 0
        Black = array.array("f", [2671.0, 2315.0, 2299.0, 2348.0, 2247.0, 2126.0, 2278.0])
        White = array.array("f", [261.0, 233.0, 241.0, 234.0, 227.0, 235.0, 249.0])
        # Uses calibrated values to normalize obtained ADC values to percentages
        # 0-100% with 100% being same amount of "black" as calibrated values
        for val in line_sensor_array:
            # curr_diff = line_sensor_array[count] - self.White[count]
            curr_diff = line_sensor_array[count] - White[count]
            # blck_diff = self.Black[count] - self.White[count]
            blck_diff = Black[count] - White[count]
            line_sensor_array[count] = (curr_diff/blck_diff)*100
            # Compensates for when ADC values go below calibrated white values
            if line_sensor_array[count] < 0:
                line_sensor_array[count] = 0
            # Used to determine if all sensors are detecting "white"
            # If the percentage is less than 3%, add to count
            if line_sensor_array[count] < 3:
                set_zero += 1
            count += 1
       
        centroid = 0
        count = -3
        total_sensor_height = 0
        total_height = 0
        max_value = max(line_sensor_array)
        # Sums the (index * corresponding percent values) and total percent values
        # Used to calculate the centroid of the line sensor
        for val in line_sensor_array:
            total_sensor_height = total_sensor_height + (val*count)
            total_height = total_height + val
            count += 1
        
        # If all sensors detect "white", set centroid in center
        if set_zero == 7:
            return line_sensor_array, max_value, 0
        # Calculate centroid using obtained sums
        try:
            centroid = total_sensor_height/total_height
        except ZeroDivisionError:
            return line_sensor_array, max_value, 0
        return line_sensor_array, max_value, centroid
    
    def calibration(self):
        input("Start Black Calibration")
        line_13 = self.adc13.read()
        line_11 = self.adc11.read()
        line_9 = self.adc9.read()
        line_7 = self.adc7.read()
        line_5 = self.adc5.read()
        line_3 = self.adc3.read()
        line_1 = self.adc1.read()
        self.Black = array.array("f", [line_1, line_3, line_5,
                                        line_7, line_9, line_11,
                                          line_13])
        input("Start White Calibration")
        line_13 = self.adc13.read()
        line_11 = self.adc11.read()
        line_9 = self.adc9.read()
        line_7 = self.adc7.read()
        line_5 = self.adc5.read()
        line_3 = self.adc3.read()
        line_1 = self.adc1.read()
        self.White = array.array("f", [line_1, line_3, line_5,
                                        line_7, line_9, line_11,
                                          line_13])
        return self.Black, self.White
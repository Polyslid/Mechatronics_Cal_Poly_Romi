"""
Mecha 12
edited: 2/13/2025   
Encoder code for the Romi
"""

"""
CURRENT ISSUES AS OF 2/4/2025:

MOVES FORWARD MORE THAN BACKWARD IF FORWARD FIRST FROM STARTUP AND VICE VERSA

"""
import pyb
import math
from time import ticks_ms, ticks_diff, sleep_ms

class Encoder:

    def __init__(self, tim, chA_pin, chB_pin):

        self.AR = 0xFFFF

        # Initialize timer for encoders
        self.tim = pyb.Timer(tim, period=self.AR, prescaler=0)
        self.tim.channel(2, pin=chA_pin, mode=pyb.Timer.ENC_AB)
        self.tim.channel(1, pin=chB_pin, mode=pyb.Timer.ENC_AB)

        self.position = 0
        self.delta = 0
        self.delta1 = 0
        self.delta2 = 0
        self.delta3 = 0
        self.delta4 = 0
        self.delta5 = 0
        self.delta6 = 0
        self.delta7 = 0
        self.dt = 0
        self.dt1 = 0
        self.dt2 = 0
        self.dt3 = 0
        self.dt4 = 0
        self.dt5 = 0
        self.dt6 = 0
        self.current_count = 0
        self.previous_count = self.tim.counter()

        self.start_time = None                  # Will start time later
        self.previous_time = ticks_ms()         # Initially, previous time is also the start time
        self.current_time = self.previous_time  # Initialize current_time

        self.elapsed_time = 0                   # Needs to be initialized before update() is ran

        # print(f"Time elapsed: {ticks_diff(self.current_time, self.start_time)}")

    def update(self): 
        
        self.current_count = self.tim.counter()

        if self.start_time is None and self.current_count != 0:  # First movement detected
            # print("DEBUG: First encoder reading detected, starting timer!")
            self.start_time = ticks_ms()  # Reset start time
        
        # Multiple self.deltas used to make a running average
        self.delta7 = self.delta6
        self.delta6 = self.delta5
        self.delta5 = self.delta4
        self.delta4 = self.delta3
        self.delta3 = self.delta2
        self.delta2 = self.delta1
        self.delta1 = self.delta
        self.delta = self.current_count - self.previous_count


        # Compute time since last update
        self.current_time = ticks_ms()   # Get current time
        # Multiple self.dts used to make a running average
        self.dt6 = self.dt5
        self.dt5 = self.dt4
        self.dt4 = self.dt3
        self.dt3 = self.dt2
        self.dt2 = self.dt1
        self.dt1 = self.dt
        self.dt = ticks_diff(self.current_time, self.previous_time)
        if self.start_time is not None:
            self.elapsed_time = ticks_diff(self.current_time, self.start_time)
        # self.elapsed_time = ticks_diff(self.current_time, self.start_time)   # Time since start

        if self.delta > ((self.AR+1)/2):
            self.delta -= self.AR+1
        
        if self.delta < -((self.AR+1)/2):
            self.delta += self.AR+1
        
        #Position and delta are in ticks
        self.position += self.delta

        self.previous_count = self.current_count
        self.previous_time = self.current_time

    def get_position(self):
        #Convert from ticks to meters
        self.pos = (self.position/1440) * (70/1000) * math.pi
        return self.pos

    def get_velocity(self):
        #Convert from ticks/us to m/s 
        deltas = (self.delta + self.delta1 + self.delta2 + self.delta3
                  + self.delta4 + self.delta5 + self.delta6 + self.delta7)
        dts = (self.dt + self.dt1 + self.dt2 + self.dt3 + self.dt4 + self.dt5 + self.dt6)
        self.delta_m = (deltas/(8*1440)) * (70/1000) * math.pi
        return self.delta_m/(dts/(7*1000))
    
    # Used to reset the encoder to 0
    def zero(self):
        self.position = 0
        self.prev_count = 0
        self.delta = 0
        self.delta1 = 0
        self.delta2 = 0
        self.delta3 = 0
        self.delta4 = 0
        self.delta5 = 0
        self.delta6 = 0
        self.delta7 = 0
        self.dt = 0
        self.dt1 = 0
        self.dt2 = 0
        self.dt3 = 0
        self.dt4 = 0
        self.dt5 = 0
        self.dt6 = 0
        self.previous_count = self.tim.counter()
        self.start_time = None
        self.elapsed_time = 0

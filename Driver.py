"""
Mecha 12
edited: 2/13/2025
Driver code for the Romi
"""

from pyb import Timer, Pin

class driver:
    def __init__(self, PWM, DIR, nSLP, tim, channel):

        #Enable pin: low to brake
        self.enable = Pin(nSLP, mode=Pin.OUT_PP)

        #Effective directional pin: low is forward, high is reverse
        self.phase = Pin(DIR, mode=Pin.OUT_PP)

        #Timer objects for PWM signals to control speed
        # tim4 = Timer(4, freq=1000)
        self.pwm = tim.channel(channel, pin=PWM, mode=Timer.PWM, pulse_width_percent=0)

    def set_effort(self, effort):

        # print(f"set_effort called with effort: {effort}")  # Debug print


        # if 100 >= effort >= -100:
        self.pwm.pulse_width_percent(abs(effort))

        self.enable.high()
        if effort < 0:
            self.phase.high()
        else:
            self.phase.low()

        # else:
        #     raise ValueError("Please input a speed from -100 to 100.")

    def enable_motor(self):
        # print("enable_motor() called")  # Debug print
        self.enable.value(1)    # Enable motor
        self.set_effort(0)      # Set effort to 0 (brake mode)

    def disable_motor(self):
        # print("disable_motor() called")  # Debug print
        self.enable.value(0)    # Disable motor
        self.pwm.pulse_width_percent(0) # Stop PWM output
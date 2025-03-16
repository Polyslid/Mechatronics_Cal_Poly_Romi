"""
Mecha 12
edited: 3/4/2025   
PID code for the Romi
"""

from time import ticks_ms, ticks_diff

class PID:
    def __init__(self, line_kp, line_ki, line_kd, imu_kp, imu_ki, imu_kd):
        self.line_kp = line_kp
        self.line_ki = line_ki
        self.line_kd = line_kd
        self.line_error = 0
        self.line_last_error = 0
        self.line_integral = 0

        self.imu_kp = imu_kp
        self.imu_ki = imu_ki
        self.imu_kd = imu_kd
        self.imu_error = 0
        self.imu_last_error = 0
        self.imu_integral = 0

        self.previous_time = ticks_ms()
        self.current_time = self.previous_time
        self.actual = 0
    
    def line_PID(self, actual, current):
        self.current_time = ticks_ms()
        
        # Determines time difference in seconds
        dt = ticks_diff(self.current_time, self.previous_time)/1000

        # Actual will always be 0
        self.line_error = actual - current

        # Integral value used for ki calculation
        self.line_integral += self.line_error * dt
        p = self.line_kp * self.line_error
        i = self.line_ki * self.line_integral
        d = self.line_kd * ((self.line_error - self.line_last_error)/dt)
        
        motor_speed = (p + i + d)

        self.line_last_error = self.line_error
        self.previous_time = self.current_time

        return motor_speed
    
    def imu_PID(self, desired, current):
        self.current_time = ticks_ms()

        # Determines time difference in seconds
        dt = ticks_diff(self.current_time, self.previous_time)/1000

        # Actual will be input from main
        self.imu_error = desired - current

        if self.imu_error > 360:
            self.imu_error -= 360
        elif self.imu_error < 0:
            self.imu_error += 360

        # Integral value used for ki calculation
        self.imu_integral += self.imu_error * dt

        p = self.imu_kp * self.imu_error
        i = self.imu_ki * self.imu_integral
        d = self.imu_kd * ((self.imu_error - self.imu_last_error)/dt)

        motor_speed = (p + i + d)

        self.imu_last_error = self.imu_error
        self.previous_time = self.current_time
        
        return motor_speed
    
    def reset_PID(self):
        self.line_error = 0
        self.line_last_error = 0
        self.line_integral = 0
        self.imu_error = 0
        self.imu_last_error = 0
        self.imu_integral = 0
        self.previous_time = ticks_ms()
        self.current_time = self.previous_time
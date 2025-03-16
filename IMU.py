"""
IMU Driver
Edited: 2/18/2025
"""

from time import sleep_ms
import struct

class IMU:
    def __init__(self, i2c):
        print(i2c)
        self.i2c = i2c

        #REGISTER MAP
        self.IMU = 0x28
        self.OPR_MODE = 0x3D
        self.CALIB_STAT = 0x35

        self.ACC_OFFSET = 0x55  # First address for acc_offset
        # self.ACC_OFFSET = [0x55, 0x56,
        #                    0x57, 0x58,
        #                    0x59, 0x5A]
        
        self.MAG_OFFSET = 0x5B  # First address for mag_offset
        # self.MAG_OFFSET = [0x5B, 0x5C,
        #                     0x5D, 0x5E,
        #                     0x5F, 0x60]
        
        self.GYRO_OFFSET = 0x61 # First address for gyro_offset
        # self.GYRO_OFFSET = [0x61, 0x62,
        #                     0x63, 0x64,
        #                     0x65, 0x66]

        self.ACC_RADIUS = 0x67
        # self.ACC_RADIUS = [0x67, 0x68]
        
        self.MAG_RADIUS = 0x69
        # self.MAG_RADIUS = [0x69, 0x6A]

        self.EUL_X_LSB = 0x1A
        self.EUL_X_MSB = 0x1B
        self.GYRO_X_LSB = 0x14
        self.GYRO_X_MSB = 0x15

        #FUSION MODES
        self.IMU_MODE = 0b1000
        self.COMPASS = 0b1001
        self.M4G = 0b1010
        self.NDOF_FMC_OFF = 0b1011
        self.NDOF = 0b1100

    def configure(self):
        # Put IMU in CONFIG mode
        self.i2c.mem_write(0x00, self.IMU, self.OPR_MODE)
        sleep_ms(200)

        # Write Calibration Coefficients
        self.cal_coeff_write()

        # Set desired mode
        self.i2c.mem_write(self.IMU_MODE, self.IMU, self.OPR_MODE)
        sleep_ms(200)

        # Read back mode to verify
        actual_mode = self.i2c.mem_read(1, self.IMU, self.OPR_MODE)[0]
        if actual_mode != self.IMU_MODE:
            print(f"Warning: Mode set to {actual_mode} instead of {self.IMU_MODE}")

    def cal_status(self):
        self.status_data = bytes(self.i2c.mem_read(1, self.IMU, self.CALIB_STAT))
        self.byte_value = struct.unpack("b", self.status_data)[0]

        self.sys_status = (self.byte_value >> 6) & 0b11  # First 2 bits
        self.gyro_status = (self.byte_value >> 4) & 0b11  # Next 2 bits
        self.acc_status = (self.byte_value >> 2) & 0b11  # Next 2 bits
        self.mag_status = self.byte_value & 0b11
        self.status = [self.sys_status, self.gyro_status, self.acc_status, self.mag_status]

        return self.status

    def cal_coeff_read(self):
        pass
        # coeff = bytearray(22)

        # self.i2c.mem_read(coeff, self.IMU, self.ACC_OFFSET)

        # return coeff
        # acc_x, acc_y, acc_z = struct.unpack("<hhh", buf)
        # return acc_x, acc_y, acc_z
        # if sensor == "acc":
        #     for address in self.ACC_OFFSET:
        #         self.i2c.mem_read(buf, self.IMU, address)
        #     acc_x, acc_y, acc_z = struct.unpack(">hhh", buf)
        #     return acc_x, acc_y, acc_z
        # elif sensor == "mag":
        #     for address in self.MAG_OFFSET:
        #         self.i2c.mem_read(buf, self.IMU, address)
        #     mag_x, mag_y, mag_z = struct.unpack(">hhh", buf)
        #     return mag_x, mag_y, mag_z
        # elif sensor == "gyro":
        #     for address in self.GYRO_OFFSET:
        #         self.i2c.mem_read(buf, self.IMU, address)
        #     gyro_x, gyro_y, gyro_z = struct.unpack(">hhh", buf)
        #     return gyro_x, gyro_y, gyro_z

    def cal_coeff_write(self):

        # Get binary data for calibration coefficients
        with open("calibration_coeff.bin", "rb") as f:
            cal_coeff = f.read()

        # Write calibration coefficients to IMU
        self.i2c.mem_write(cal_coeff[:6], self.IMU, self.ACC_OFFSET)
        self.i2c.mem_write(cal_coeff[6:12], self.IMU, self.MAG_OFFSET)
        self.i2c.mem_write(cal_coeff[12:18], self.IMU, self.GYRO_OFFSET)
        self.i2c.mem_write(cal_coeff[18:20], self.IMU, self.ACC_RADIUS)
        self.i2c.mem_write(cal_coeff[20:22], self.IMU, self.MAG_RADIUS)

    def read_Euler(self):
        euler_data = self.i2c.mem_read(2, self.IMU, self.EUL_X_LSB)

        yaw = struct.unpack("<h", euler_data) [0]

        yaw /= 16.0

        return yaw   

    def read_angular_vel(self):
        angvel_data = self.i2c.mem_read(2, self.IMU, self.GYRO_X_LSB)
        angvel = struct.unpack("<h", angvel_data) [0]
        
        return angvel

    ## Used to read the ambient temperature 
    # def get_Temp(self):
    #     Temp_data = self.i2c.mem_read(2, self.IMU, 0x34)
    #     Temp = struct.unpack("<h", Temp_data) [0]
    #   
    #     return Temp
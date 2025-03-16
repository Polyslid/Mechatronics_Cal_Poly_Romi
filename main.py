"""
MECHA 12
edited: 3/10/2025
SCHEDULER FOR ROMI
"""

from Line_Sensor import Line_Sensor
from pyb import I2C, Timer, Pin
from nb_input import NB_Input
from Encoder import Encoder
from Driver import driver
from PID import PID
from IMU import IMU
import task_share
import cotask
import gc

# from pyb import USB_VCP   # For USB input non-blocking code

def motor(shares):
    Leffort, Reffort = shares
    
    while True:
        Right_Effort = Reffort.get()
        Left_Effort = Leffort.get()

        Left_Motor.enable_motor()                                                            
        Right_Motor.enable_motor()
        Left_Motor.set_effort(Left_Effort)
        Right_Motor.set_effort(Right_Effort)

        Reffort.put(Right_Effort)
        Leffort.put(Left_Effort)
          
        yield 0 

def sensor(shares):
    Leffort, Reffort, heading = shares
    initial_heading = heading.get()
    initial_heading90 = initial_heading + 90
    initial_headingminus90 = initial_heading - 85
    initial_headingback = initial_heading + 182
    if initial_heading90 > 360:
        initial_heading90 = initial_heading90 - 360
    if initial_headingminus90 < 0:
        initial_headingminus90 = initial_headingminus90 + 360
    if initial_headingback > 360:
        initial_headingback = initial_headingback - 360
    
    count = 0
    count2 = 0
    state = 0
    state1 = 0
    state2 = 2
    stateEND = 0

    while True:
        Left_Encoder.update()
        Right_Encoder.update()
        line_array, max, centroid = line_sensor.update()
        current_heading = imu.read_Euler()
        
        if state == state1:
            if (1 <= Left_Encoder.get_position() <= 1.155):   
                Leffort.put(40)
                Reffort.put(40)

            elif (1.498 <= Left_Encoder.get_position() <= 1.575):
                Leffort.put(40)
                Reffort.put(40)

            elif (3.9 <= Left_Encoder.get_position() <= 4.54):
                if count < 50:
                    Leffort.put(0)
                    Reffort.put(0)
                elif 50 <= count <= 150:
                    Left_Base_Speed = Leffort.get()
                    Right_Base_Speed = Reffort.get()
                    speed_change = Line_PID.imu_PID(initial_headingback, current_heading)
                    Leffort.put(Left_Base_Speed + speed_change)
                    Reffort.put(Right_Base_Speed - speed_change)

                elif count == 151:
                    Leffort.put(40)
                    Reffort.put(40)
                elif count >= 152:
                    Left_Base_Speed = Leffort.get()
                    Right_Base_Speed = Reffort.get()
                    speed_change = Line_PID.imu_PID(initial_headingback, current_heading)
                    Leffort.put(Left_Base_Speed + speed_change)
                    Reffort.put(Right_Base_Speed - speed_change)
                count += 1

            elif (4.54 <= Left_Encoder.get_position() <= 4.75):
                if count2 < 100:
                    Leffort.put(0)
                    Reffort.put(0)
                elif 100 <= count2 < 150:
                    speed_change = 1
                    Left_Base_Speed = Leffort.get()
                    Right_Base_Speed = Reffort.get()
                    Leffort.put(Left_Base_Speed + speed_change)
                    Reffort.put(Right_Base_Speed - speed_change)
                    if (initial_headingminus90-5) <= current_heading <= (initial_headingminus90+5):
                        count2 = 150
                elif count2 >= 150:
                    Leffort.put(20)
                    Reffort.put(20)
                elif 0 in (LBump0.value(), LBump1.value(), LBump2.value(), RBump3.value(), RBump4.value(), RBump5.value()):
                    state = state2
                    Left_Encoder.zero()
                    Right_Encoder.zero()
                count2 += 1
            else:
                Right_Base_Speed = Reffort.get()
                Left_Base_Speed = Leffort.get()
                speed_change = Line_PID.line_PID(0, centroid)
                Leffort.put(Left_Base_Speed - speed_change)
                Reffort.put(Right_Base_Speed + speed_change)
                count = 0
                if 0 in (LBump0.value(), LBump1.value(), LBump2.value(), RBump3.value(), RBump4.value(), RBump5.value()):
                    state = state2
                    current_Lpos = Left_Encoder.get_position()
                    
                       
        if state == state2:
            if stateEND == 0:
                print(f"EPos0: {float(Left_Encoder.get_position())}")
                if ((current_Lpos-Left_Encoder.get_position()) > .10):
                    Leffort.put(-20)
                    Reffort.put(-20)    
                else:
                    stateEND = 1
                    current_Lpos = Left_Encoder.get_position()

            if stateEND == 1:
                Leffort.put(20)
                Reffort.put(-20)
                print(f"EPos1: {float(Left_Encoder.get_position())}")
                if (initial_heading-5) <= current_heading <= (initial_heading+5):
                    stateEND = 2
                    current_Lpos = Left_Encoder.get_position()
                    Leffort.put(20)
                    Reffort.put(20)
                    
            if stateEND == 2:
                print(f"EPos2: {float(Left_Encoder.get_position())}")
                if ((Left_Encoder.get_position()-current_Lpos) <= .40):
                    Leffort.put(20)
                    Reffort.put(20)
                else:
                    stateEND = 3
                    current_Lpos = Left_Encoder.get_position()
            
            if stateEND == 3:
                Leffort.put(-20)
                Reffort.put(20)
                if (initial_headingminus90-5) <= current_heading <= (initial_headingminus90+5):
                    stateEND = 4
                    current_Lpos = Left_Encoder.get_position()
                    Leffort.put(20)
                    Reffort.put(20)
            
            if stateEND == 4:
                print(f"EPos4: {float(Left_Encoder.get_position())}")
                if ((Left_Encoder.get_position()-current_Lpos) <= .22):
                    Leffort.put(20)
                    Reffort.put(20)
                else:
                    stateEND = 5
                    Left_Encoder.zero()
                    Right_Encoder.zero()

            if stateEND == 5:
                Leffort.put(-20)
                Reffort.put(20)
                if (initial_headingback-5) <= (current_heading-10) <= (initial_headingback+5):
                    stateEND = 6
                    current_Lpos = Left_Encoder.get_position()
                    Leffort.put(20)
                    Reffort.put(20)
            if stateEND == 6:
                Leffort.put(20)
                Reffort.put(20)
                if ((Left_Encoder.get_position()-current_Lpos) >= .40):
                    Leffort.put(0)
                    Reffort.put(0)
            
        yield 0

def user(shares):
    Leffort, Reffort= shares

    while True:
        ## Non-blocking input to store the effort value entered by user without blocking scheduler
        if nb_in.any():
            input = nb_in.get()
            if input == '':
                Leffort.put(0)
                Reffort.put(0)
            elif -100 <= int(input) <= 100:
                speed = int(input)
                Leffort.put(speed)
                Reffort.put(speed)

        yield 0 # Prevents errors but does nothing


if __name__ == "__main__":
    print("Testing ME405 stuff in cotask.py and task_share.py\r\n"
          "Press Ctrl-C to stop and show diagnostics.\r\n"
          " ") 
    
    ## For USB Connection
    # nb_in = NB_Input (USB_VCP (), echo=True)

    ## For Bluetooth Connection
    uart = pyb.UART(3, 115200)
    pyb.repl_uart(uart)
    nb_in = NB_Input (uart, echo=True)

    # Initialize Motor and Encoder objects
    tim4 = Timer(4, freq=500)
    Left_Motor  = driver(Pin.cpu.B7, Pin.cpu.H0, Pin.cpu.H1, tim4, 2)
    Right_Motor = driver(Pin.cpu.B6, Pin.cpu.B2, Pin.cpu.A9, tim4, 1)
    Left_Encoder  = Encoder(3, Pin.cpu.A7, Pin.cpu.A6)
    Right_Encoder = Encoder(2, Pin.cpu.A1, Pin.cpu.A0)
    line_sensor = Line_Sensor(Pin.cpu.C8, Pin.cpu.C2, Pin.cpu.C3, 
                              Pin.cpu.A4, Pin.cpu.B0, Pin.cpu.C1, 
                              Pin.cpu.C0, Pin.cpu.B1)
    LBump0 = pyb.Pin(Pin.cpu.B4, pyb.Pin.IN, pull=pyb.Pin.PULL_UP)
    LBump1 = pyb.Pin(Pin.cpu.B5, pyb.Pin.IN, pull=pyb.Pin.PULL_UP)
    LBump2 = pyb.Pin(Pin.cpu.B3, pyb.Pin.IN, pull=pyb.Pin.PULL_UP)
    RBump5 = pyb.Pin(Pin.cpu.C9, pyb.Pin.IN, pull=pyb.Pin.PULL_UP)
    RBump4 = pyb.Pin(Pin.cpu.B8, pyb.Pin.IN, pull=pyb.Pin.PULL_UP)
    RBump3 = pyb.Pin(Pin.cpu.B9, pyb.Pin.IN, pull=pyb.Pin.PULL_UP)
    Line_PID = PID(0.1, 0.02, 0.1, 0.02, 0.01, 0.008)
    
    """ The line sensor calibration is already hard coded in but if you choose to
        recalibrate you can use the calibration function in the Line_Sensor class"""
    # line_sensor.calibration()

    #Initalize I2C and IMU
    i2c = I2C(2)
    i2c = I2C(2, I2C.CONTROLLER)
    i2c.init(I2C.CONTROLLER, baudrate=100000)

    imu = IMU(i2c)
    imu.configure()
    yaw_init = imu.read_Euler()
    

    # Shared Queues for motor data   
    # Stores left motor position in queue
    Lpos  = task_share.Queue('f', 16, thread_protect=False,
                              name= "Left Position")     
    # Stores left motor position in queue
    Rpos  = task_share.Queue('f', 16, thread_protect=False,
                              name= "Right Position")   
    # Stores elapsed time for left motor in sec
    Ltime = task_share.Queue('I', 16, thread_protect=False,
                              name = "Left Elapsed Time")    
    # Stores elapsed time for right motor in sec
    Rtime = task_share.Queue('I', 16, thread_protect=False,
                              name = "Right Elapsed Time")
    heading = task_share.Queue('I', 16, thread_protect=False,
                                name = "Heading Angle")
    
    # Store initial heading for reference datum
    heading.put(int(yaw_init))
    
    ## Shared Variables
    # Stores user_in motor effort
    Leffort = task_share.Share('f', thread_protect=False,
                                name="Left Motor Effort")  
    # Stores user_in motor effort
    Reffort = task_share.Share('f', thread_protect=False,
                                name="Right Motor Effort")  

    ## Scheduler tasks
    task1 = cotask.Task(user, name="Task_1", priority=0, period=1,
                        profile=True, trace=False, shares=(Leffort, Reffort))  
    
    task2 = cotask.Task(motor, name="Task_2", priority=2, period=10,
                        profile=True, trace=False, shares=(Leffort, Reffort))
    
    task3 = cotask.Task(sensor, name="Task_3", priority=2, period=10,
                        profile=True, trace=False, shares=(Leffort, Reffort, heading))

    cotask.task_list.append(task1)
    cotask.task_list.append(task2)
    cotask.task_list.append(task3)

    # Run the memory garbage collector to ensure memory is as defragmented as
    # possible before the real-time scheduler is started
    gc.collect()

    # Run the scheduler with the chosen scheduling algorithm. Quit if ^C pressed
    while True:
        try:
            cotask.task_list.pri_sched()
        except KeyboardInterrupt:
            break
        except StopIteration:
            print('\n' + str (cotask.task_list))
            print(task_share.show_all())
            print(task1.get_trace())
            print('')
            break

    Left_Motor.disable_motor()
    Right_Motor.disable_motor()
    ## Print a table of task data and a table of shared information data
    # print('\n' + str (cotask.task_list))
    # print(task_share.show_all())
    # print(task1.get_trace())
    # print('')
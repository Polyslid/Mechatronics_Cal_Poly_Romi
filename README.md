# MECHA-12 Romi Term Project
## BY: Indigo Garcia, Aiden Peltier, Jason Reyes

## Overview
This project consists of a robot named Romi that will travel through a premade track with multiple checkpoints. A black line connects each of these checkpoints to each other that Romi will use to reach each 
checkpoint via a line sensor, however between each checkpoint there is an obstacle that hinders the capabilities of the line sensor or removes the possibility of using it entirely. In order to compensate for this,
other means of navigation are required, such as an IMU that determiens the robots orientation.

There are various files that are combined into this project to make sure that Romi works properly and is able to follow the track. There is the Driver, Encoder, PID, IMU, and Line_Sensor files.
<p align="center">
<kbd>
  <img src="https://github.com/user-attachments/assets/967b4769-db4d-4fd8-982d-29c7daceaba2" width="550">

</kbd>
<p align="center">
Figure 1: Romi
</p>

## Romi Assembly
The Romi utilizes a line sensor, an array of bump sensors, an IMU, an encoder, and dc motors. To power these components and manipulate them using python, they are connected to an STM32. Figure 2 shows the table used to store the pin locations for the STM and the NUCLEO for each component on the Romi and Figure 3 shows the wiring diagram for the system.

<p align="center">
<kbd>
  <img src="https://github.com/user-attachments/assets/36602828-658d-4343-9903-017cd2d0b346" width="480"> <img src="https://github.com/user-attachments/assets/f32ddeb4-cbfd-441c-a72a-a78b14b9aff7" width="480">
</kbd>
<p align="center">
  Figure 2: Wiring Pins Table

<p align="center">
<kbd>
  <img src="https://github.com/user-attachments/assets/4bc507ce-2ef8-4c46-858a-eee9f5a8c650">
</kbd>
<p align="center">
Figure 3: Wiring Diagram
</p>

## Driver
The Driver file (seen here Driver.py) is used to enable, disable, and set the effort for the motors used in Romi. By using PWM it is able to set the speed at which the wheels turn by using a percentage between -100 and 100. With negative values rotating backwards with respect to the Romi's front direction.

## Encoder
The Encoder file is used to calculate the distance Romi has traveled and the velocity it is moving at. By using a running average of the difference in time that the encoder code is running based upon a tim.counter and a running average of the total time that has passed since initialization, it is possible to calculate the distance traveled by Romi using self.pos = (self.position/1440) ⋅ (70/1000) ⋅ math.pi and the velocity using self.delta_m/(dts/(7⋅1000)). In the velocity equation self.delta_m is the change in distance calculated from (deltas/(8⋅1440)) ⋅ (70/1000) ⋅ math.pi after the combination of all the deltas (change in time) together. The division by 1440 is the resolution specific to the encoder, while the ratio of 70/1000 is the Romi wheel diamter. Essentially, this equation converts the ticks measured by the encoder into meters. 

## PID
The PID file includes the PID for both the line sensor and the IMU. By taking in the desired centroid of 0 and the actual centroid location detected on the line sensor, it is possible to calculate the error and use it to determine the propotional, integral, and derivative control. For each of these controls there is also a set gain that is obtained from the main file. The PID for the line sensor can be seen in the Figure 4 below. 
<p align="center">
<kbd>
  <img src=https://github.com/user-attachments/assets/42d00e26-bd62-4501-b9a1-6b2f0b76550c>
</kbd>
<p align="center">
Figure 4: Line Sensor PID
</p>

For the IMU, the desired heading of the IMU and the actual heading is inputted to determine the error. The PID performs same exact process as the line sensor but with different gain values that have already been collected when the PID class is initialized. The IMU PID can be seen in the Figure 5 below. 
<p align="center">
<kbd>
  <img src=https://github.com/user-attachments/assets/83ad1b52-17f7-4bc0-a2f5-d18215bfb797>
</kbd>
<p align="center">
Figure 5: IMU PID
</p>

## Line Sensor
The Line_Sensor file is the primary file for determining the centroid, list of sensor percentages, and max percentage for the line sensor. By using the ADC input of each GPIO pin used, it is possible to obtain a value for each sensor that can be compared to set calibrated values obtained via the calibration def in the same line_sensor file. By comparing the calibration values and the actual current values, a percentage is obtained for each sensor and the centroid is calculated using a for loop seen in Figure 6 below.
<p align="center">
<kbd>
  <img src=https://github.com/user-attachments/assets/eecde3d9-1ff8-48dc-941e-841fc3e541c5>
</kbd>
</p>
<p align="center">
Figure 6: Centroid Calculation
</p>

## IMU
The IMU reads the Romi's relative heading using it's built-in accelerometer and gyrometer. The IMU is essential to keeping the Romi driving straight when line following is not possible. The Romi's intial heading value is stored as a reference datum to make degree turns respective to the intial heading. Using the IMU with the it's PID, the Romi can drive straight in any desired direction.

## Main
After obtaining each of these files, they are used within the main file which is formatted as a scheduler using the cotask.py and task_share.py files. The resulting task diagram can be observed in Figure 5. The user interface task was given the highest priority because it is used at the beginning of the program and allows the user initiate a non-resetting emergency stop. The user task uses non-blocking input code using nb_input.py to get the effort from the user. The user could also manually stop the Romi at any time by pressing enter. When the user task receives an input from the user, it stores that effort value in the Leffort and Reffort share. Each motor has an individual effort so that the PID can control each motor to make adjustments in the Romi dynamics. After the effort is sent to the motor task, the sensor task takes over and adjusts the effort values based off the PID results that are obtained by comparing the desired results and the actual to get an error. The motor and sensor task have the same priority and run in round-robin style because they rely on one another and should be performed one after the other. As the sensors update, the signals are sent to the controllers. The controllers send effort to the motors for effort adjustments, and the cycle continues. 

<p align="center">
<kbd>
  <img src="https://github.com/user-attachments/assets/e8ca44e2-458e-4169-98ad-a037038e2b35" width="550">
</kbd>
</p>
<p align="center">
Figure 7: Scheduler Task Diagram
</p>

In order to have Romi travel through sections of the track easier, two finite state machines (FSM) were made. One of the FMSs were used to have ROMI make it through the entire track and then enter the second FSM when the wall is detected using the bump sensor. The other FSM is built into the second state of the first FSM and is just for the very end where it must make multiple turns and adjustments to make it back to the start of the track. The first FSM can be seen in Figure 8 and contains only two states.
<p align="center">
<kbd>
  <img src="https://github.com/user-attachments/assets/69f2e127-e385-4843-a04a-2402f4d50f73">
</kbd>
</p>
<p align="center">
Figure 8: First FSM for Entire Track
</p>

Within the second state, the second FSM performs multiple adjustments depending on the Romi's heading and travel distance. This FSM can be seen in Figure 9. 
<p align="center">
<kbd>
  <img src="https://github.com/user-attachments/assets/bfd29601-3a0d-4fec-9784-a234242eb586">
</kbd>
</p>
<p align="center">
Figure 9: Second FSM for Ending of Track
</p>

Within the FSMs, the sensor task switches between the line sensor and IMU PID's depending on where on the track the Romi is. The Romi uses the encoder to determine where on the track it is based on the distance from the start and changes its speed depending on the distance it is at. After reaching certain distances on the track, it has a slight pause where it is able to locate the proper heading, adjust, and then drive straight. A counter is started that controls how long the Romi pauses. This was implemented to make the Romi more robust and keep a consistent heading with respect to the initial. This is especially important for the grid portion of the track because it requires the Romi to travel for a longer distance. By finding the heading first, it minimizes drift and prevents any accumulated error from the previous states effecting future states.


## Demo
Here is a demonstration video of the Romi Robot in action:

https://github.com/user-attachments/assets/16161666-6769-4098-9238-770e0adbcabe

<p align="center">
Figure 10: Demo Video
</p>






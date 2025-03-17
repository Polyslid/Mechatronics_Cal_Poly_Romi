## Overview
This project consists of a robot named Romi that will travel through a premade track with multiple checkpoints. A black line connects each of these checkpoints to each other that Romi will use to reach each 
checkpoint via a line sensor, however between each checkpoint there is an obstacle that hinders the capabilities of the line sensor or removes the possibility of using it entirely. In order to compensate for this,
other means of navigation are required, such as an IMU that determiens the robots orientation.

There are various files that are combined into this project to make sure that Romi works properly and is able to follow the track. There is the Driver, Encoder, PID, IMU, and Line_Sensor files.
## Driver
The Driver file is used to enable, disable, and set the effort for the motors used in Romi. By using PWM it is able to set the speed at which the wheels turn by using a percentage between -100 and 100. 

## Encoder
The Encoder file is used to calculate the distance Romi has traveled and the velocity it is moving at. By using a running average of the difference in time that the encoder code is running based upon a tim.counter and a running average of the total time that has passed since initialization, it is possible to calculate the distance traveled by Romi using self.pos = (self.position/1440) * (70/1000) * math.pi and the velocity using self.delta_m/(dts/(7*1000)).

## PID
The PID file includes the PID for both the line sensor and the IMU. By taking in the desired centroid of 0 and the actual centroid location detected on the line sensor, it is possible to calculate the error and use it to determine the propotional, integral, and derivative control. For each of these controls there is also a set gain that is obtained from the main file. The PID for the line sensor can be seen in the Figure 1 below. 

<kbd>
  <img ![image](https://github.com/user-attachments/assets/bdedcb7b-b9c4-4b11-9011-caade55e2f6c)
</kbd>
<p align="center">
Figure 1: Line Sensor PID
</p>

For the IMU, the desired heading of the IMU and the actual heading is inputted to determine the error and do the same exact PID process as the line sensor. The IMU PID can be seen in the Figure 2 below. 

![Blank diagram (17)](https://github.com/user-attachments/assets/a015c602-f380-4213-91cc-fef94f264e4b)
<p align="center">
Figure 2: IMU PID
</p>

#Line Sensor
The Line_Sensor file is the primary file for determining the centroid, list of sensor percentages, and max percentage for the line sensor. By using the ADC input of each GPIO pin used, it is possible to obtain a value for each sensor that can be compared to set calibrated values obtained via the calibration def in the same line_sensor file. By comparing the calibration values and the actual current values, a percentage is obtained for each sensor and the centroid is calculated using a for loop seen in the figure below.

![image](https://github.com/user-attachments/assets/eecde3d9-1ff8-48dc-941e-841fc3e541c5)
<p align="center">
Figure 3: Centroid Calculation
</p>

#Main
After obtaining each of these files, they are used within the main file which is formatted as a scheduler using the cotask.py and task_share.py files. The resulting task diagarm can be observed in 
Figure 4. 





https://github.com/user-attachments/assets/16161666-6769-4098-9238-770e0adbcabe

<p align="center">
Figure 4: Demo Video
</p>






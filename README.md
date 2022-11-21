# 6-DOF-Manipulator-Robot
Autonomous 6 DOF manipulator robot program integrated with distance sensor. The program is ros-based and the servos are controlled using arduino (arm_robot.ino).

### Usage
1. roscore

2. rosrun rosserial_python serial_node.py

3. rosrun arm_robot kinematics.py

### Inverse Kinematics Simulation
1. roscore

2. rosrun arm_robot simulation.py

#!/usr/bin/python3.9
import rospy
from arm_robot.msg import servo
import numpy as np
from std_msgs.msg import Float32

def distance_cb(msg):
    global goal_x, found, x, x_object
    x_object = msg.data
    if(x_object <= 1):
        pass
    else:
        goal_x = x_object + x
        print("distance\t: ", x_object)

        if(x_object < 20): # perlu tuning jaraknya lagi
            found = True
        else:
            found = False

def distance_subscriber():
    distance_sub = rospy.Subscriber("/distance", Float32, distance_cb)
    
def servo_publisher():
    global servo0, servo1, servo2, servo3, servo4, servo5, rate
    servo_pub = rospy.Publisher("/servo", servo, queue_size=1)
    rate = rospy.Rate(2)

    msg = servo()
    msg.servo0 = servo0
    msg.servo1 = servo1
    msg.servo2 = servo2 + np.deg2rad(30)
    msg.servo3 = servo3  + np.deg2rad(15)
    msg.servo4 = servo4
    msg.servo5 = servo5
    servo_pub.publish(msg)

def robot_coordinate():
    global x, z, theta1, theta2, theta3
    global link1, link2, link3

    theta1_s = theta1
    theta2_s = -theta2 - np.deg2rad(30)
    theta3_s = theta3 + np.deg2rad(20)
    z = link1*np.sin(theta1_s) + link2*np.sin(theta1_s + theta2_s) + link3*np.sin(theta1_s + theta2_s + theta3_s)
    x = link1*np.cos(theta1_s) + link2*np.cos(theta1_s + theta2_s) + link3*np.cos(theta1_s + theta2_s + theta3_s)

    if(x < 0):
        x = x * -1

def initial_position():
    global theta0,theta1,theta2,theta3,theta4,theta5, published
    theta0 = float(np.deg2rad(0)) #base arm yaw
    theta1 = float(np.deg2rad(90)) #shoulder-upper arm pitch
    theta2 = float(np.deg2rad(100)) #upper-lower arm pitch
    theta3 = float(np.deg2rad(40)) #lower arm-wrist pitch
    theta4 = float(np.deg2rad(80)) #grip roll
    theta5 = float(np.deg2rad(0)) #grip yaw

    #initial end-effector coordinate
    published = True
    robot_coordinate()

def inverse_kinematics(x, z):
    global theta1,theta2,theta3,published, link1, link2, link3

    b = x - link3*np.cos(theta3)
    c = np.sqrt(b**2 + z**2)
    alpha1 = np.arctan(z/b)


    alpha2 = (link1**2 + c**2 - link2**2)/(2*link1*c)
    if(alpha2 >= 0.54):
        alpha2 = np.arccos(np.minimum(1, alpha2))
    else:
        alpha2 = np.arccos(np.maximum(-1, alpha2))

    theta1 = alpha1 + alpha2 #servo 1

    theta2 = (link1**2 + link2**2 - c**2)/(2*link1*link2)

    if(theta2 >= 0.54):
        theta2 = np.pi - np.arccos(np.minimum(1, theta2))
    else:
        theta2 = np.pi - np.arccos(np.maximum(-1, theta2))

    theta2 = np.minimum(theta2, np.deg2rad(150))

    beta1 = (link2**2 + c**2 - link1**2)/(2*link2*c)
    if(beta1 >= 0.54):
        beta1 = np.arccos(np.minimum(1, beta1))
    else:
        beta1 = np.arccos(np.maximum(-1, beta1))
    beta2 = np.arctan(b/z)

    theta3 = beta1 + beta2 + 1.5708 - np.pi - 0.5 #servo 3 #0.5 errornya


    published = True

def robot_active(): #robot algorithm is here
    global published, theta0, theta1, theta2, theta3, theta4, theta5, found, state, x_object, x
    global goal_x, goal_z, grap_time, release_time, rotate_time, init_pose, count
    if state=="searching":
        print("===SEARCHING===")
        #---SERVO GA KUAT MUTERRRRRRRRRR--------#
        # theta0 += 0.3
        # published = True
        if(found):
            state="reaching"
        # if(theta0 >= np.deg2rad(180)):
        #     theta0 = 0

    elif state=="reaching":
        print("===REACHING===")
        # 3 dof inverse kinematics
        print("goal_z: ", goal_z)
        print("goal_x: ",goal_x)
        inverse_kinematics(goal_x, goal_z)
        # if(x_object < 6): #perlu tuning jaraknya lagi
        #     state = "grab"
        #     published = False
        state = "grab"
        published = False

    elif state=="grab":
        print("===GRAB===")
        # rotate the grip servo
        # sudut belum tau
        theta5 = np.deg2rad(30)
        if(grap_time == 69):
            state = "rotate"
        elif(grap_time > 4):
            published = True
            grap_time += 1
            if(grap_time > 6):
                # back to initial position 
                theta0 = float(np.deg2rad(0)) #base arm yaw
                theta1 = float(np.deg2rad(90)) #shoulder-upper arm pitch
                theta2 = float(np.deg2rad(100)) #upper-lower arm pitch
                theta3 = float(np.deg2rad(50)) #lower arm-wrist pitch
                theta4 = float(np.deg2rad(80)) #grip roll
                grap_time = 69
        else:
            grap_time += 1

    elif state=="rotate":
        print("===ROTATE===")
        # rotate the base yaw 180 degree
        theta0 = np.pi
        if(rotate_time == 0):
            published = True
        rotate_time += 1
        if(rotate_time > 4):
            rotate_time = 0
            state = "release"

    elif state=="release":
        print("===RELEASE===")
        # rotate the grip servo to release
        theta5 = np.deg2rad(0)
        if(release_time == 0):
            published = True
        release_time += 1
        if(release_time > 4):
            release_time = 0
            init_pose = False
            count = 0
            found = False
            state = "searching"
    
def main():
    global link1, link2, link3, servo0, servo1, servo2, servo3, servo4, servo5, state, found
    global theta0, theta1, theta2, theta3, theta4, theta5
    global grap_time, release_time, rotate_time
    global x_object, goal_x, goal_y, goal_z
    global x, z
    rospy.init_node("arm_robot_node")
    published = bool(False)
    init_pose = bool(False)
    state = str("searching")
    found = bool(False)

    #----time variable----#
    count = float(0)
    grap_time = int(0)
    release_time = int(0)
    rotate_time = int(0)
    rate = rospy.Rate(1)

    #----link length----#
    link1 = 14.2 #upper arm len
    link2 = 9.4 #lower arm len
    link3 = 17.6 #wrist len

    #----angle of each servo----#
    theta0 = float() #base arm yaw
    theta1 = float() #shoulder-upper arm pitch
    theta2 = float() #upper-lower arm pitch
    theta3 = float() #lower arm-wrist pitch
    theta4 = float() #grip roll
    theta5 = float() #grip yaw

    #----servo angle----#
    servo0 = float()
    servo1 = float()
    servo2 = float()
    servo3 = float()
    servo4 = float()
    servo5 = float()

    #----coordinates----#
    x = float()
    y = float()
    z = float()

    x_object = float()

    goal_x = float()
    goal_y = float()
    goal_z = float()
    while(not rospy.is_shutdown()):
        distance_subscriber()
        if(published):
            #----Publish servo angle---#
            servo0 = theta0
            servo1 = theta1
            servo2 = theta2
            servo3 = theta3
            servo4 = theta4
            servo5 = theta5
            
            servo_publisher()

        if(not init_pose):
            count = 0
            initial_position()
            init_pose = True
            print("===INITIAL POSITION===")
            robot_coordinate()
            print("x\t: ", x, "\nz\t: ", z)
            published = True
            
        
        elif(init_pose and count > 8):
            print("====ROBOT READY====")
            robot_active()
        
        # track robot coordinate
        print("===COORDINATE===")
        robot_coordinate()
        print("x\t: ", x,"\nz\t: ", z)
        goal_z = z

        # track robot state
        print("STATE\t: ", state)

        # track servo angle
        print("====SERVO ANGLE====")
        print("Servo0\t: ",np.rad2deg(servo0))
        print("Servo1\t: ",np.rad2deg(servo1))
        print("Servo2\t: ",np.rad2deg(servo2))
        print("Servo3\t: ",np.rad2deg(servo3))
        print("Servo4\t: ",np.rad2deg(servo4))
        print("Servo5\t: ",np.rad2deg(servo5))
        #track time
        print("Time\t: ", count, " seconds")
        count += 1
        
        rate.sleep()
        

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSException:
        pass

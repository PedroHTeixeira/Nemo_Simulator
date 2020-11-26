#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from geometry_msgs.msg import PointStamped
import time

def callback(msg):
    x = msg.point.x
    y = msg.point.y
    z = msg.point.z
    return follower(x,y,z)

def follower(x,y,z):
    pub = rospy.Publisher('cmd_vel',Twist, queue_size=10)
    move_nemo= Twist()
    
    if x > 3:
        move_nemo.angular.z=-1
        pub.publish(move_nemo)
        time.sleep(1)
        move_nemo.angular.z=0
        move_nemo.linear.y=1
        if y < -3:
            move_nemo.linear.y=1
        pub.publish(move_nemo)
        time.sleep(2)
    elif x < -3:
        move_nemo.angular.z=1
        pub.publish(move_nemo)
        time.sleep(1)
        move_nemo.angular.z=0
        move_nemo.linear.y=1
        if y < -2:
            move_nemo.linear.y=1
        pub.publish(move_nemo)
        time.sleep(2)
    else:
        move_nemo.linear.y=0
    if z>3:
        move_nemo.linear.z=-1
        move_nemo.linear.y=-1
    else:
        move_nemo.linear.z=0
        if y < -3:
            move_nemo.linear.y=1
        elif y > 3:
            move_nemo.linear.y=1
    
    pub.publish(move_nemo)

rospy.init_node('follow')
time.sleep(20)
rospy.Subscriber("/sonar_data", PointStamped, callback)
rospy.spin()
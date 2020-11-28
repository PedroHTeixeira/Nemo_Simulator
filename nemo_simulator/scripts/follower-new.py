#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from geometry_msgs.msg import PointStamped
from std_msgs.msg import Int64
import time

x=0
y=0
z=0
w=0

def callback(msg):
    global x
    global y
    global z
    x = msg.point.x
    y = msg.point.y
    z = msg.point.z

def callback2(msg):
    global w
    w=msg

def follow():
    rospy.init_node('follow')
    time.sleep(20)
    rospy.Subscriber("/sonar_data", PointStamped, callback)
    rospy.Subscriber("/warning", Int64, callback2)
    pub = rospy.Publisher('cmd_vel',Twist, queue_size=10)
    move_nemo= Twist()
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        if w==1:
            time.sleep(2.20)
        else:
            if x > 4:
                move_nemo.angular.z=-3
                pub.publish(move_nemo)
                time.sleep(1)
                move_nemo.angular.z=0
                move_nemo.linear.y=0.75
                pub.publish(move_nemo)
                time.sleep(2)
                move_nemo.linear.y=0
            elif x < -4:
                move_nemo.angular.z=3
                pub.publish(move_nemo)
                time.sleep(1)
                move_nemo.angular.z=0
                move_nemo.linear.y=-0.75
                pub.publish(move_nemo)
                time.sleep(2)
                move_nemo.linear.y=0
            else:
                move_nemo.linear.y=0
                move_nemo.angular.z=1
            if z>3:
                move_nemo.linear.z=-1
                move_nemo.linear.y=-1
            else:
                move_nemo.linear.z=0
                if y < -3:
                    move_nemo.linear.y=-1
                elif y > 3:
                    move_nemo.linear.y=1


            pub.publish(move_nemo)
            rate.sleep()

if __name__ == '__main__':
    try:
        follow()
    except rospy.ROSInterruptException:
        pass
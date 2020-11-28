#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PointStamped
from std_msgs.msg import Int64
from geometry_msgs.msg import Twist
import time


def callback(msg):
    pub = rospy.Publisher('cmd_vel',Twist, queue_size=10)
    rate = rospy.Rate(10) # 10hz
    x = msg.point.x
    move_nemo= Twist()
    if x > 300 and x < 900:
        move_nemo.angular.z = 0
        move_nemo.linear.y = 3
    elif x < 300:
        if x < 100:
            if x == 0:
                move_nemo.angular.z = 3
            else:
                move_nemo.angular.z = 2
        else:
            move_nemo.angular.z = 1
    elif x > 900:
        if x >1100:
            if x > 1200:
                move_nemo.angular.z = -3
            else:
                move_nemo.angular.z = -2
        else:
            move_nemo.angular.z = -1
    pub.publish(move_nemo)
    rate.sleep()

def security():
    rospy.init_node('limits')
    time.sleep(20)
    rospy.Subscriber("/nemo_position_camera", PointStamped, callback)
    rospy.spin()

if __name__ == '__main__':
    try:
        security()
    except rospy.ROSInterruptException:
        pass
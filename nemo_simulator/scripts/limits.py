#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PointStamped
from std_msgs.msg import Int64
from geometry_msgs.msg import Twist
import time


def callback(msg):
    pub = rospy.Publisher('cmd_vel',Twist, queue_size=10)
    pub2 = rospy.Publisher('/warning',Int64, queue_size=10)
    rate = rospy.Rate(10) # 10hz
    pub2.publish(1)
    x = msg.point.x
    y = msg.point.y
    move_nemo= Twist()
    if x > 580 and x < 620:
        move_nemo.angular.z = 0
        move_nemo.linear.y = 4
    elif x < 580:
        move_nemo.angular.z = 0.5
    elif x > 620:
        move_nemo.angular.z = -0.5
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
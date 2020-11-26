#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
import time

def talker():
    pub = rospy.Publisher('cmd_vel',Twist, queue_size=10)
    rospy.init_node('auto_move')
    time.sleep(15)
    move_nemo= Twist()
    move_nemo.angular.z=4
    pub.publish(move_nemo)
    time.sleep(2.80)
    move_nemo.angular.z=0
    pub.publish(move_nemo)

if __name__ == '__main__':
    try: 
        talker()
    except rospy.ROSInterruptException:
        pass
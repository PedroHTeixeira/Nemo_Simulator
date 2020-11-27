#!/usr/bin/env python
import rospy
from nav_msgs.msg      import Odometry
from std_msgs.msg import Int64
from geometry_msgs.msg import Twist
import time
x=0
y=0

def callback(msg):
    global x
    global y
    x = msg.pose.pose.position.x
    y = msg.pose.pose.position.y

def security():
    rospy.init_node('limits')
    time.sleep(20)
    rospy.Subscriber("/Odom", Odometry, callback)
    pub = rospy.Publisher('cmd_vel',Twist, queue_size=10)
    pub2 = rospy.Publisher('warning',Int64, queue_size=10)
    move_nemo= Twist()
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        if x > 10:
            pub2.publish(1)
            move_nemo.linear.x = -4
            pub.publish(move_nemo)
            time.sleep(2)
            move_nemo.linear.x=0
            pub.publish(move_nemo)
            rate.sleep()
        elif x < -10:
            pub2.publish(1)
            move_nemo.linear.x = +4
            pub.publish(move_nemo)
            time.sleep(2)
            move_nemo.linear.x=0
            pub.publish(move_nemo)
            rate.sleep()
        else:
            pub2.publish(0)
            rate.sleep()
        if y > 10:
            pub2.publish(1)
            move_nemo.linear.y = -4
            pub.publish(move_nemo)
            time.sleep(2)
            move_nemo.linear.y=0
            pub.publish(move_nemo)
            rate.sleep()
        elif y < -10:
            pub2.publish(1)
            move_nemo.linear.y = 4
            pub.publish(move_nemo)
            time.sleep(2)
            move_nemo.linear.y=0
            pub.publish(move_nemo)
            rate.sleep()
        else:
            pub2.publish(0)
            rate.sleep()

if __name__ == '__main__':
    try:
        security()
    except rospy.ROSInterruptException:
        pass
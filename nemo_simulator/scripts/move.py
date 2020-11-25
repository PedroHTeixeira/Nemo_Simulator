#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from geometry_msgs.msg import PointStamped

def callback(msg):
    y = msg.point.y


def talker():
    pub = rospy.Publisher('cmd_vel',Twist, queue_size=10)
    rospy.init_node('move')
    while not rospy.is_shutdown():
       move_nemo= Twist()
       move_nemo.linear.x=input("Movimentacao em x")
       move_nemo.linear.y=input("Movimentacao em y")
       if y < 2.0 and move_nemo.linear.y>0:
           move_nemo.linear.y=0
       move_nemo.linear.z=input("Movimentacao em z")
       move_nemo.angular.z=input("Movimentacao em Giro")
       pub.publish(move_nemo)

if __name__ == '__main__':
    try:
        rospy.Subscriber("/sonar_data", PointStamped, callback)
        get value of y from callback function when it is returning 
        talker()
    except rospy.ROSInterruptException:
        pass
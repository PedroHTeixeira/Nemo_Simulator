#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from geometry_msgs.msg import PointStamped

def talker():
    pub = rospy.Publisher('cmd_vel',Twist, queue_size=10)
    rospy.init_node('move')
    while not rospy.is_shutdown():
       move_nemo= Twist()
       move_nemo.linear.x=input("Movimentacao em x")
       move_nemo.linear.y=input("Movimentacao em y")
       move_nemo.linear.z=input("Movimentacao em z")
       move_nemo.angular.z=input("Movimentacao em Giro")
       pub.publish(move_nemo)

if __name__ == '__main__':
    try: 
        talker()
    except rospy.ROSInterruptException:
        pass
#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PointStamped
from std_msgs.msg import Int64
from geometry_msgs.msg import Twist
import time

class Follow_Red():

    def __init__(self):
        self.pub = rospy.Publisher('cmd_vel',Twist, queue_size=10)
        self.sub = rospy.Subscriber("/nemo_position_camera", PointStamped, self.callback)

    def callback(self,msg):
        
        rate = rospy.Rate(10) # 10hz

        #Get the x of the position of the Cylinder
        x = msg.point.x

        #Create a Twist message for the speed
        move_nemo= Twist()

        #Depending on the Position the robot will move diferently
        if x > 320 and x < 720:
            move_nemo.angular.z = 0
            move_nemo.linear.y = 3.35
        elif x < 320:
            if x < 220:
                if x < 120:
                    move_nemo.angular.z = 9
                else:
                    move_nemo.angular.z = 8
            else:
                move_nemo.angular.z = 7
        elif x > 720:
            if x >820:
                if x > 920:
                    move_nemo.angular.z = -9
                else:
                    move_nemo.angular.z = -8
            else:
                move_nemo.angular.z = -7
        self.pub.publish(move_nemo)
        rate.sleep()

def security():
    rospy.init_node('limits')
    time.sleep(20)
    Follow_Red()
    rospy.spin()

if __name__ == '__main__':
    try:
        security()
    except rospy.ROSInterruptException:
        pass
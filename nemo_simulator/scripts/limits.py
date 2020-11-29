#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PointStamped
from std_msgs.msg import Int64
from geometry_msgs.msg import Twist
import time
import math 

class Follow_Red():

    def __init__(self):
        self.pub = rospy.Publisher('cmd_vel',Twist, queue_size=10)
        self.sub = rospy.Subscriber("/nemo_position_camera", PointStamped, self.callback)
        self.sub2 = rospy.Subscriber("/sonar_data", PointStamped, self.callback2)

    def callback2(self,msg):
        self.distance = math.sqrt(math.pow(msg.point.x, 2) + math.pow(msg.point.y, 2))
        print(self.distance)

    def callback(self,msg):

        rate = rospy.Rate(10) # 10hz

        #Get the x of the position of the Cylinder
        x = msg.point.x

        #Create a Twist message for the speed
        move_nemo= Twist()

        #Depending on the Position the robot will move diferently
        
        if(x <= 320):
            cilindro = 0
        elif(480 <= x <= 560):
            cilindro = 1
        elif(x >= 720):
            cilindro = 2

        #Depending on the Position the robot will move diferently

        if(cilindro == 0):      # x <= 320 
            move_nemo.angular.z = 4
        if(cilindro == 1):      # 320 < x < 720
            move_nemo.angular.z = 0
            if self.distance <=3:
                move_nemo.linear.y = 0
            else:
                move_nemo.linear.y = 2.9
        if(cilindro == 2):      # 720 <= x
            move_nemo.angular.z = -4
        
        # if x > 300 and x < 700:
        #     move_nemo.angular.z = 0
        #     if(self.distance <= 3): # Probable collision
        #         move_nemo.linear.y = 0
        #     else:              # No collision
        #         move_nemo.linear.y = 4
        # elif x <= 300:
        #     if x < 220:
        #         if x < 120:
        #             move_nemo.angular.z = 4
        #         else:
        #             move_nemo.angular.z = 3
        #     else:
        #         move_nemo.angular.z = 2
        # elif x >= 700:
        #     if x >820:
        #         if x > 920:
        #             move_nemo.angular.z = -4
        #         else:
        #             move_nemo.angular.z = -3
        #     else:
        #         move_nemo.angular.z = -2
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
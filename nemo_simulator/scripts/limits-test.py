#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PointStamped
from std_msgs.msg import Int64
from geometry_msgs.msg import Twist
import time
import math 
from nav_msgs.msg import Odometry

class Follow_Red():

    def __init__(self):
        self.pub = rospy.Publisher('cmd_vel',Twist, queue_size=10)
        self.sub = rospy.Subscriber("/nemo_position_camera", PointStamped, self.callback)
        self.sub2 = rospy.Subscriber("/sonar_data", PointStamped, self.callback2)
        self.sub4 = rospy.Subscriber("/odom", Odometry, self.callback4)
        self.sub3 = rospy.Subscriber('/lost', Int64, self.callback3) 
        self.cilindro = 1
        self.quarter = 0

    def callback4(self,msg):
        self.x = msg.pose.pose.position.x
        self.y = msg.pose.pose.position.y
        if self.x <0 or self.y < 0:
            self.quarter =1 

    def callback3(self,msg):
        if msg.data == 1:
            self.cilindro=4
        

    def callback2(self,msg):
        self.distance = math.sqrt(math.pow(msg.point.x, 2) + math.pow(msg.point.y, 2))
        

    def callback(self,msg):

        rate = rospy.Rate(10) # 10hz

        #Get the x of the position of the Cylinder
        x = msg.point.x

        #Create a Twist message for the speed
        move_nemo= Twist()
        
        if(x <= 320):
            self.cilindro = 0
        elif(500 <= x <= 540):
            self.cilindro = 1
        elif(x >= 720):
            self.cilindro = 2

        #Depending on the Position the robot will move diferently

        if(self.cilindro == 0):      # x <= 320 
            move_nemo.angular.z = 4
        if(self.cilindro == 1):      # 320 < x < 720
            if self.quarter == 0:
                move_nemo.angular.z = 0
                move_nemo.linear.y = 3.75
            else:
                try:
                    if self.distance <=1.5:
                        move_nemo.angular.z = 0
                        move_nemo.linear.y = 1
                    else:
                        move_nemo.angular.z = 0
                        move_nemo.linear.y = 3.75
                except:
                    move_nemo.angular.z = 0
                    move_nemo.linear.y = 3.75
                
        if(self.cilindro == 2):      # 720 <= x
            move_nemo.angular.z = -4
        
        self.pub.publish(move_nemo)
        
     

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
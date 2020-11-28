#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PointStamped
from std_msgs.msg import Int64
from geometry_msgs.msg import Twist
import time
y_distance=0
x_distance=0

def callback2(msg):
    global y_distance
    global x_distance
    y_distance =msg.point.y
    x_distance=msg.point.x
    
def callback(msg):
    pub = rospy.Publisher('cmd_vel',Twist, queue_size=10)
    pub2 = rospy.Publisher('/warning',Int64, queue_size=10)
    rate = rospy.Rate(10) # 10hz
    pub2.publish(1)
    x = msg.point.x
    move_nemo= Twist()
    #if y_distance>3 or y_distance<-3 or x_distance>3 or x_distance<-3:
    if x > 300 and x < 900:
        move_nemo.angular.z = 0
        move_nemo.linear.y = 4
        pub.publish(move_nemo)
    elif x > 900:
        if x>1100:
            if x> 1300:
                move_nemo.angular.z = -4
            else:
                move_nemo.angular.z = -2
            pub.publish(move_nemo)
        else:
            move_nemo.angular.z = -1
            pub.publish(move_nemo)
    elif x < 300:
        if x<100:
            if x==0:
                move_nemo.angular.z = 4
            else:
                move_nemo.angular.z = 2
            pub.publish(move_nemo)
        else:
            move_nemo.angular.z = 1
            pub.publish(move_nemo)
    # else :
    #     move_nemo.angular.z=0
    #     move_nemo.linear.y=0
    #     pub.publish(move_nemo) 
    rate.sleep()

def security():
    rospy.init_node('limits')
    time.sleep(20)
    rospy.Subscriber("/nemo_position_camera", PointStamped, callback)
    rospy.Subscriber("/sonar_data", PointStamped, callback2)
    rospy.spin()

if __name__ == '__main__':
    try:
        security()
    except rospy.ROSInterruptException:
        pass
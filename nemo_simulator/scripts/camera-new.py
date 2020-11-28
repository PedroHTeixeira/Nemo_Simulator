#!/usr/bin/env python
import cv2
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import time
import numpy as np
from geometry_msgs.msg import PointStamped
from std_msgs.msg import Float64MultiArray 
from std_msgs.msg import Int64


class DataHandler():

    def __init__(self):
        #Publishers and Subscribers
        self.pub2=rospy.Publisher("nemo_position_camera",PointStamped,queue_size=10)
        self.sub = rospy.Subscriber("camera/image_raw", Image, self.callback)
        self.pub=rospy.Publisher("camera/image_interpreted",Image,queue_size=10)
        self.pub3=rospy.Publisher("camera/image_masked_contours",Image,queue_size=10)
        self.pub5=rospy.Publisher("camera/image_masked_corners",Image,queue_size=10)
        self.pub4=rospy.Publisher("camera/image_masked",Image,queue_size=10)
        self.pub0=rospy.Publisher("contours",Float64MultiArray,queue_size=10)
        self.pub_Stalker=rospy.Publisher('lost',Int64,queue_size=10)

    def callback(self,msg):
        rate = rospy.Rate(10)

        #Bridge that connects the msg in ROS to a cv Image
        bridge = CvBridge()
        cv_image = bridge.imgmsg_to_cv2(msg, "bgr8")

        #Changing colorsapces
        hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)

        # Color Range
        light_red=(0,149,140)
        dark_red=(0,255,177)
        mask = cv2.inRange(hsv,light_red,dark_red)

        #Mask Corrections
        mask = cv2.dilate(mask, None, iterations=2)
        mask = cv2.erode(mask, None, iterations=2)

        #Create Contours and Corners
        contour_mask, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        contour_mask_2, contours_2, hierarchy_2 = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        #Create Blank Image
        dimensions = cv_image.shape
        blank_image = np.zeros((dimensions[0],dimensions[1],3), np.uint8)

        #Draw the Corners and change colorspaces
        img_lucca = cv2.drawContours(blank_image, contours_2, -1, (255,255,255), 3)
        img_lucca= cv2.cvtColor(img_lucca, cv2.COLOR_BGR2GRAY)

        #Draw the Contours and change colorspaces
        img_ctr = cv2.drawContours(blank_image, contours, -1, (255,255,255), 3)
        img_ctr = cv2.cvtColor(img_ctr, cv2.COLOR_BGR2GRAY)

        #Use moments to find the center of the red cylinder
        m=cv2.moments(img_ctr,False)
        try:
            cx,cy = m['m10']/m['m00'], m['m01']/m['m00']

            #Create a msg that contains the position of the center of the red cylinder
            position = PointStamped()
            position.point.x=cx
            position.point.y=cy

            #Draw a circle on that position
            cv2.circle(cv_image,(int(cx),int(cy)), 25, (255,0,0), -1)

            #Publish the position
            self.pub2.publish(position)

            #Tell stalker that the robot found red
            self.pub_Stalker.publish(0)

            #Add the corners to a msg and publish it 
            message =Float64MultiArray() 
            message.data = contours_2
            self.pub0.publish(message)
        except ZeroDivisionError:
            #If moments can't find the cylinder it should show it on the screen
            cv2.putText(cv_image,'Red Not Found',(10,500), cv2.FONT_HERSHEY_SIMPLEX, 4,(0,0,255),6,cv2.LINE_AA)

            #Tell stalker that the robot is lost
            self.pub_Stalker.publish(1)

        #Publish all the images created
        self.pub5.publish(bridge.cv2_to_imgmsg(img_lucca, "mono8"))
        self.pub.publish(bridge.cv2_to_imgmsg(cv_image, "bgr8"))
        self.pub3.publish(bridge.cv2_to_imgmsg(img_ctr,"mono8"))
        self.pub4.publish(bridge.cv2_to_imgmsg(mask,"mono8"))
    
def reader():
    rospy.init_node('interpreter')
    time.sleep(20)
    DataHandler()
    rospy.spin()

if __name__ == '__main__':
    try:
        reader()
    except rospy.ROSInterruptException:
        pass
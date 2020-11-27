#!/usr/bin/env python
import cv2
import rospy
from std_msgs.msg import Int64
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import time
import numpy as np
from geometry_msgs.msg import PointStamped

def callback(msg):
    rate = rospy.Rate(10)
    bridge = CvBridge()
    cv_image = bridge.imgmsg_to_cv2(msg, "bgr8")
    hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
    light_red=(0,150,134)
    dark_red=(0,255,177)
    mask = cv2.inRange(hsv,light_red,dark_red)
    mask = cv2.dilate(mask, None, iterations=2)
    mask = cv2.erode(mask, None, iterations=2)
    m=cv2.moments(mask,False)
    try:
        cx,cy = m['m10']/m['m00'], m['m01']/m['m00']
    except ZeroDivisionError:
        height, width, channels = mask.shape
        cy,cx= height/2 , width/2
    position = PointStamped()
    position.point.x=cx
    position.point.y=cy
    mask_c = cv2.cvtColor(cv_image, cv2.COLOR_HSV2BGR)
    cv2.circle(mask_c,(int(cx),int(cy)), 50, (0,0,255), -1)
    pub=rospy.Publisher("camera/image_interpreted",Image,queue_size=10)
    pub2=rospy.Publisher("nemo_position_camera",PointStamped,queue_size=10)
    pub.publish(bridge.cv2_to_imgmsg(mask_c, "bgr8"))
    pub2.publish(position)
    rate.sleep()

def reader():
    rospy.init_node('interpreter')
    time.sleep(20)
    rospy.Subscriber("camera/image_raw", Image, callback)
    rospy.spin()

if __name__ == '__main__':
    reader()
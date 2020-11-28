#!/usr/bin/env python
import cv2
import rospy
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
    dimensions=mask.shape
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    blank_image = np.zeros((dimensions[0],dimensions[1],3), np.uint8)
    img_ctr=cv2.drawContours(blank_image, contours, -1, (0,255,0), 3)
    m=cv2.moments(img_ctr,False)
    try:
        cx,cy = m['m10']/m['m00'], m['m01']/m['m00']
        position = PointStamped()
        position.point.x=cx
        position.point.y=cy
        cv2.circle(cv_image,(int(cx),int(cy)), 25, (255,0,0), -1)
        pub2=rospy.Publisher("nemo_position_camera",PointStamped,queue_size=10)
        pub2.publish(position)
    except ZeroDivisionError:
        cv2.putText(cv_image,'Red Not Found',(10,500), cv2.FONT_HERSHEY_SIMPLEX, 4,(0,0,255),6,cv2.LINE_AA)
    pub=rospy.Publisher("camera/image_interpreted",Image,queue_size=10)
    pub3=rospy.Publisher("camera/image_masked",Image,queue_size=10)
    pub.publish(bridge.cv2_to_imgmsg(cv_image, "bgr8"))
    pub3.publish(bridge.cv2_to_imgmsg(mask,"mono8"))
    
    rate.sleep()

def reader():
    rospy.init_node('interpreter')
    time.sleep(20)
    rospy.Subscriber("camera/image_raw", Image, callback)
    rospy.spin()

if __name__ == '__main__':
    try:
        reader()
    except rospy.ROSInterruptException:
        pass
    
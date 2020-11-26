#!/usr/bin/env python
# Movimentacao ponto A ao ponto B

import rospy
from geometry_msgs.msg import Twist
from geometry_msgs.msg import PointStamped
from geometry_msgs.msg import Point
from nav_msgs.msg      import Odometry

from tf.transformations import euler_from_quaternion 
# Necessario para a conversao para Euler

import math # Necessario para o uso do arctg

x1 = 0
x2 = 0
y1 = 0
y2 = 0
roll = 0
pitch = 0
yaw = 0
deltax = 0
deltay = 0
teta = 0
nemobloco = 0
marlinbloco = 0

#--------------------------------------------------------------------------------------------#

def odometria(msg):
    global x1,y1,roll,pitch,yaw

    x1 = msg.pose.pose.position.x # Marlin
    y1 = msg.pose.pose.position.y

    quat = msg.pose.pose.orientation # Quaternion da posicao do Marlin

    (roll, pitch, yaw) = euler_from_quaternion([quat.x,quat.y,quat.z,quat.w]) # Transformada
 

#--------------------------------------------------------------------------------------------#

def sonar(msg):
    global deltax,deltay

    deltax = msg.point.x
    deltay = msg.point.y


def loop():

    rospy.init_node('Stalker')

    rospy.Subscriber("/sonar_data", PointStamped, sonar)
    rospy.Subscriber('/odom', Odometry, odometria) 

    move = Twist()

    #--------------------------------------------------------------------------------------------#

    while not rospy.is_shutdown():
        global nemobloco,marlinbloco

        x2 = x1 - deltax # Nemo
        y2 = y1 - deltay
        teta = math.atan2(deltax,deltay)
        teta = math.degrees(teta)

        pub = rospy.Publisher('cmd_vel',Twist, queue_size=10)

        #frente = move.linear.x=3
        #tras= move.linear.x= -3
        #direita = move.linear.y=3
        #esquerda = move.linear.y=-3
        #horario = move.angular.z= 3
        #antihorario = move.angular.z= -3
        #paradax = move.linear.x=0
        #paraday = move.linear.y=0
         
        if(x2 - x1 > 2):
            move.linear.x = 2
        if(x2 - x1 < -2):
            move.linear.x = -2
        if(y2 - y1 > 2):
            move.linear.y = 2
        if(y2 - y1 < -2):
            move.linear.y = -2
        
        if(-2 < x2 - x1 < 2 and -2 < y2 - y1 < 2):
            move.linear.x = 0
            move.linear.y = 0

        if(0 < x2 <= 10 and 0 < y2 <= 10): # Nemo esta no bloco a (bloco 1)
            nemobloco = 1
        if(0 < x2 <= 10 and -10 <= y2 < 0): # Nemo esta no bloco b (bloco 2)
            nemobloco = 2
        if(-10 <= x2 < 0 and -10 <= y2 < 0): # Nemo esta no bloco c (bloco 3)
            nemobloco = 3
        if(-10 <= x2 < 0 and 0 < y2 <= 10): # Nemo esta no bloco d (bloco 4)
            nemobloco = 4
        if(0 < x1 <= 10 and 0 < y1 <= 10): # Marlin esta no bloco a (bloco 1)
            marlinbloco = 1
        if(0 < x1 <= 10 and -10 <= y1 < 0): # Marlin esta no bloco b (bloco 2)
            marlinbloco = 2
        if(-10 <= x1 < 0 and -10 <= y1 < 0): # Marlin esta no bloco c (bloco 3)
            marlinbloco = 3
        if(-10 <= x1 < 0 and 0 < y1 <= 10): # Marlin esta no bloco d (bloco 4)
            marlinbloco = 4


        rospy.loginfo(marlinbloco)

        pub.publish(move)
        
#--------------------------------------------------------------------------------------------#

if __name__ == '__main__':
    try: 
        loop()
    except rospy.ROSInterruptException:
        pass

#--------------------------------------------------------------------------------------------#

time.sleep(20)
rospy.spin()

#--------------------------------------------------------------------------------------------#
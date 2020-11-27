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
marlinavenida = 0
marlinrua = 0

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
        global nemobloco,marlinbloco,marlinavenida,marlinrua

        x2 = x1 - deltax # Nemo
        y2 = y1 - deltay
        teta = math.atan2(deltax,deltay)#                                           ^  Eixo y
        teta = math.degrees(teta)#                                                  |
        #                                                                           |
        pub = rospy.Publisher('cmd_vel',Twist, queue_size=10) #               Rua Ikuhara
        #                                                                     ------------
        #direita = move.linear.x=3      #                                     |          |
        #esquerda= move.linear.x= -3    #                                     |          |
        #frente = move.linear.y=3       #                       Avenida Daumas|          | Avenida Pavani     --> Eixo x
        #tras = move.linear.y=-3        #                                     |          |
        #horario = move.angular.z= 3    #                                     ------------
        #antihorario = move.angular.z=-3#                                      Rua Koppe
        #paradax = move.linear.x=0
        #paraday = move.linear.y=0

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

        if(2.6 <= x1 <= 3.4 and -5 <= y1 <= 5): # Marlin esta na avenida Pavani (avenida 1)
            marlinavenida = 1
        elif(-3.4 <= x1 <= -2.6 and -5 <= y1 <= 5): # Marlin esta na avenida Daumas (avenida 2)
            marlinavenida = 2
        else:
            marlinavenida = 0

        if(-5 <= x1 <= 5 and 3.6 <= y1 <= 4.4): # Marlin esta na rua Ikuhara (rua 1)
            marlinrua = 1
        elif(-5 <= x1 <= 5 and -3.4 <= y1 <= -2.6): # Marlin esta na rua Koppe (rua 2)
            marlinrua = 2
        else:
            marlinrua = 0

        #if(marlinavenida == 1 and marlinrua == 1): # Search Bloco 1
        #if(marlinavenida == 1 and marlinrua == 2): # Search Bloco 2
        #if(marlinavenida == 2 and marlinrua == 1): # Search Bloco 4
        #if(marlinavenida == 2 and marlinrua == 2): # Search Bloco 3
        
        if(marlinbloco == 1 and (marlinavenida == 0 and marlinrua == 0)): # Marlin perdido no bloco 1
            if(5 - x1 > 0):
                move.linear.x=3
            elif(5 - x1 == 0):
                move.linear.y=-3
            else:
                move.linear.x=-3

        if(marlinbloco == 2 and (marlinavenida == 0 and marlinrua == 0)): # Marlin perdido no bloco 2
            if(5 - x1 > 0):
                move.linear.x=3
            elif(5 - x1 == 0):
                move.linear.y=3
            else:
                move.linear.x=-3

        if(marlinbloco == 3 and (marlinavenida == 0 and marlinrua == 0)): # Marlin perdido no bloco 3
            if(-5 - x1 > 0):
                move.linear.x=3
            elif(-5 - x1 == 0):
                move.linear.y=3
            else:
                move.linear.x=-3

        if(marlinbloco == 4 and (marlinavenida == 0 and marlinrua == 0)): # Marlin perdido no bloco 4
            if(-5 - x1 > 0):
                move.linear.x=3
            elif(-5 - x1 == 0):
                move.linear.y=-3
            else:
                move.linear.x=-3
            
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
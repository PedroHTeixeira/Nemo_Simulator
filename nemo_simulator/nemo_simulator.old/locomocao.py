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
StalkerMode = False
SearchMode  = True

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
        global nemobloco,marlinbloco,marlinlocalizacao,Searchmode,StalkerMode,yaw

        r = rospy.Rate(4)

        x2 = x1 - deltax # Nemo
        y2 = y1 - deltay
        teta = math.atan2(deltax,deltay)#                                           ^  Eixo y                                             |
        #                                                                           |
        pub = rospy.Publisher('cmd_vel',Twist, queue_size=10) #               Rua Ikuhara
        #                                                            (--7;6) ------------ (7; 6)
        #direita = move.linear.x=3      #                                     |          |
        #esquerda= move.linear.x= -3    #                                     |          |
        #frente = move.linear.y=3       #                       Avenida Daumas|          | Avenida Pavani     --> Eixo x
        #tras = move.linear.y=-3        #                                     |          |
        #horario = move.angular.z= 3    #                           (-7;-6.2) ------------(7;-6.2)
        #antihorario = move.angular.z=-3#                                      Rua Koppe
        #paradax = move.linear.x=0
        #paraday = move.linear.y=0
        
        # Funcoes para identificacao de posicoes
        if(0 < x2 <= 10 and 0 < y2 <= 10):          # Nemo esta no bloco a (bloco 1)
            nemobloco = 1
        if(0 < x2 <= 10 and -10 <= y2 < 0):         # Nemo esta no bloco b (bloco 2)
            nemobloco = 2
        if(-10 <= x2 < 0 and -10 <= y2 < 0):        # Nemo esta no bloco c (bloco 3)
            nemobloco = 3
        if(-10 <= x2 < 0 and 0 < y2 <= 10):         # Nemo esta no bloco d (bloco 4)
            nemobloco = 4

        if(0 < x1 <= 10 and 0 < y1 <= 10):          # Marlin esta no bloco a (bloco 1)
            marlinbloco = 1
        if(0 < x1 <= 10 and -10 <= y1 < 0):         # Marlin esta no bloco b (bloco 2)
            marlinbloco = 2
        if(-10 <= x1 < 0 and -10 <= y1 < 0):        # Marlin esta no bloco c (bloco 3)
            marlinbloco = 3
        if(-10 <= x1 < 0 and 0 < y1 <= 10):         # Marlin esta no bloco d (bloco 4)
            marlinbloco = 4

        # Ruas e interseccoes
        if(5 <= y1 <= 6 and 6 <= x1 <= 7):   # Interseccao do bloco 1
            marlinlocalizacao = 1
        elif(-6.4 <= y1 <= 5 and 6 <= x1 <= 7):  # Rua Pavani
            marlinlocalizacao = 2
        elif(-7.4 <= y1 <= -6.4 and 6 <= x1 <= 7): # Interseccao do bloco 2
            marlinlocalizacao = 3
        elif(-7.4 <= y1 <= -6.4 and -6 <= x1 <= 6): # Rua Koppe
            marlinlocalizacao = 4
        elif(-7.4 <= y1 <= -6.4 and -7 <= x1 <= -6): # Interseccao do bloco 3
            marlinlocalizacao = 5
        elif(-6.4 <= y1 <= 5 and -7 <= x1 <= -6):   # Rua Daumas
            marlinlocalizacao = 6
        elif(5 <= y1 <= 6 and -7 <= x1 <= -6):     # Interseccao do bloco 4
            marlinlocalizacao = 7
        elif(5 <= y1 <= 6 and -6 <= x1 <= 6):   # Rua Ikuhara
            marlinlocalizacao = 8
        else:                               # Perdido
            marlinlocalizacao = 0

        # Comandos caso Marlin esteja procurando Nemo (SearchMode)
        if(SearchMode == True):

            # Marlin esta perdido
            if(marlinlocalizacao == 0 and marlinbloco == 1):
                    if(7 - x1 >= 0.5):
                        move.linear.x=3
                    elif(-0.5 < 7 - x1 < 0.5 and y1 > 6):
                        move.linear.y=-3
                    else:
                        move.linear.x=-3
            if(marlinlocalizacao == 0 and marlinbloco == 2):
                    if(7 - x1 >= 0.5):
                        move.linear.x=3
                    elif(-0.5 < 7 - x1 < 0.5 and y1 < -6.2):
                        move.linear.y=3
                    else:
                        move.linear.x=-3     
            if(marlinlocalizacao == 0 and marlinbloco == 3):
                    if(-7 - x1 >= 0.5):
                        move.linear.x=3
                    elif(-0.5 < -7 - x1 < 0.5 and y1 < -6.2):
                        move.linear.y=3
                    else:
                        move.linear.x=-3
            if(marlinlocalizacao == 0 and marlinbloco == 4):
                    if(-7 - x1 >= 0.5):
                        move.linear.x=3
                    elif(-0.5 < -7 - x1 < 0.5 and y1 > 6):
                        move.linear.y=-3
                    else:
                        move.linear.x=-3
                
            # Marlin esta nas interseccoes
            if(marlinlocalizacao == 1):   # Int 1
                if(marlinbloco == nemobloco): # Marlin e Nemo no mesmo bloco 1
                    move.linear.x = 0
                    move.linear.y = 0
                    move.angular.z = -2
                else:
                    if (yaw < 3.08):
                        move.angular.z = -2
                    elif (yaw > 3.20):
                        move.angular.z = 2
                    else:
                        move.angular.z = 0
                        rospy.sleep(1)
                        move.linear.x = 0
                        move.linear.y = 2
            elif(marlinlocalizacao == 3): # Int 2
                if(marlinbloco == nemobloco): # Marlin e Nemo no mesmo bloco 2
                    move.linear.x = 0
                    move.linear.y = 0
                    move.angular.z = -2
                else:
                    if (yaw < 4.65):
                        move.angular.z = -2
                    elif (yaw > 4.77):
                        move.angular.z = 2
                    else:
                        move.angular.z = 0
                        rospy.sleep(1)
                        move.linear.x = 0
                        move.linear.y = 2
            elif(marlinlocalizacao == 5): # Int 3
                if(marlinbloco == nemobloco): # Marlin e Nemo no mesmo bloco 3
                    move.linear.x = 0
                    move.linear.y = 0
                    move.angular.z = -2
                else:
                    if (yaw < 6.22):
                        move.angular.z = -2
                    elif (yaw > 6.34):
                        move.angular.z = 2
                    else:
                        move.angular.z = 0
                        rospy.sleep(1)
                        move.linear.x = 0
                        move.linear.y = 2
            elif(marlinlocalizacao == 7): # Int 4
            
                if(marlinbloco == nemobloco): # Marlin e Nemo no mesmo bloco 4
                    move.linear.x = 0
                    move.linear.y = 0
                    move.angular.z = -2
                else:
                    if (yaw < 1.51):
                        move.angular.z = -2
                    elif (yaw > 1.63):
                        move.angular.z = 2
                    else:
                        move.angular.z = 0
                        rospy.sleep(1)
                        move.linear.x = 0
                        move.linear.y = 2

            # Marlin esta nas ruas
            elif(marlinlocalizacao == 2 or marlinlocalizacao == 4 or marlinlocalizacao == 6 or marlinlocalizacao == 6): 
                move.linear.x = 0
                move.linear.y = 2
                move.angular.z = 0

        rospy.loginfo(yaw)

        pub.publish(move)
        r.sleep()
        
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
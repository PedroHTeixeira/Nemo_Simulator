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
        global nemobloco,marlinbloco,marlinavenida,marlinrua,Searchmode,StalkerMode

        x2 = x1 - deltax # Nemo
        y2 = y1 - deltay
        teta = math.atan2(deltax,deltay)#                                           ^  Eixo y
        teta = math.degrees(teta)#                                                  |
        #                                                                           |
        pub = rospy.Publisher('cmd_vel',Twist, queue_size=10) #               Rua Ikuhara
        #                                                            (-5;4.3) ------------ (5; 4.3)
        #direita = move.linear.x=3      #                                     |          |
        #esquerda= move.linear.x= -3    #                                     |          |
        #frente = move.linear.y=3       #                       Avenida Daumas|          | Avenida Pavani     --> Eixo x
        #tras = move.linear.y=-3        #                                     |          |
        #horario = move.angular.z= 3    #                           (-5;-3.3) ------------(5; -3.3)
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

        if(2.2 <= x1 <= 3.8 and -5 <= y1 <= 5):     # Marlin esta na avenida Pavani (avenida 1)
            marlinavenida = 1
        elif(-3.8 <= x1 <= -2.2 and -5 <= y1 <= 5): # Marlin esta na avenida Daumas (avenida 2)
            marlinavenida = 2
        else:                                       # Marlin esta fora de avenidas
            marlinavenida = 0
        if(-5 <= x1 <= 5 and 3.2 <= y1 <= 4.8):     # Marlin esta na rua Ikuhara (rua 1)
            marlinrua = 1
        elif(-5 <= x1 <= 5 and -3.8 <= y1 <= -2.2): # Marlin esta na rua Koppe (rua 2)
            marlinrua = 2
        else:                                       # marlin esta fora de ruas
            marlinrua = 0
        
        # Rotacoes horarias no meio dos blocos, a fim de achar Nemo
        if(marlinavenida == 1 and marlinrua == 1 and nemobloco == 1): # Search Bloco 1
            move.angular.z= 3
        if(marlinavenida == 1 and marlinrua == 2 and nemobloco == 2): # Search Bloco 2
            move.angular.z= 3
        if(marlinavenida == 2 and marlinrua == 1 and nemobloco == 4): # Search Bloco 4
            move.angular.z= 3
        if(marlinavenida == 2 and marlinrua == 2 and nemobloco == 3): # Search Bloco 3
            move.angular.z= 3
        
        # Comandos caso Marlin esteja procurando Nemo (SearchMode)
        if(SearchMode == True):

            # Caso Marlin se perca
            if(marlinbloco == 1 and (marlinavenida == 0 and marlinrua == 0)): # Marlin perdido no bloco 1
                if(5 - x1 >= 1):
                    move.linear.x=2
                elif(-1 < 5 - x1 < 1 and y1 > 4.8):
                    move.linear.y=-2
                else:
                    move.linear.x=-2
            if(marlinbloco == 2 and (marlinavenida == 0 and marlinrua == 0)): # Marlin perdido no bloco 2
                if(5 - x1 >= 1):
                    move.linear.x=2
                elif(-1 < 5 - x1  < 1 and y1 < -3.8):
                    move.linear.y=2
                else:
                    move.linear.x=-2
            if(marlinbloco == 2 and (marlinavenida == 0 and marlinrua == 0)): # Marlin perdido no bloco 3
                if(-5 - x1 >= 1):
                    move.linear.x=2
                elif(-1 < -5 - x1  < 1 and y1 < -3.8):
                    move.linear.y=2
                else:
                    move.linear.x=-2
            if(marlinbloco == 4 and (marlinavenida == 0 and marlinrua == 0)): # Marlin perdido no bloco 4
                if(-5 - x1 >= 1):
                    move.linear.x=2
                elif( -1< -5 - x1 < 1 and y1 > 4.8):
                    move.linear.y=-2
                else:
                    move.linear.x=-2

            # Caso Marlin esteja em uma avenida ou rua
            if(marlinbloco != nemobloco):
                if(marlinavenida == 1): # Marlin esta em avenida Pavani
                    move.linear.x=0
                    move.linear.y=0 #-3
                if(marlinavenida == 2): # Marlin esta em avenida Daumas
                    move.linear.x=0
                    move.linear.y=0 #3
                if(marlinrua == 1):     # Marlin esta em rua Ikuhara
                    move.linear.x=0 #3
                    move.linear.y=0
                if(marlinrua == 2):     # Marlin esta em rua Koppe
                    move.linear.x=0 #-3
                    move.linear.y=0
        

        rospy.loginfo(marlinrua)

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
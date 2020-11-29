#!/usr/bin/env python
# Lucca Gandra e Pedro Teixeira 
# Projeto final Capacitacao Nautilus 

import rospy
from geometry_msgs.msg import Twist
from geometry_msgs.msg import PointStamped
from geometry_msgs.msg import Point
from nav_msgs.msg      import Odometry
from std_msgs.msg      import Int64
import time

from tf.transformations import euler_from_quaternion 
# Necessario para a conversao para Euler

import math # Necessario para o uso do arctg

x1 = 0
x2 = 0
y1 = 0
y2 = 0
yaw = 0
deltax = 0
deltay = 0
nemobloco = 0
marlinbloco = 0
andar = True
SearchMode  = True
horario = True
w=0
finding_nemo = False
#--------------------------------------------------------------------------------------------#
def lost(msg):
    global SearchMode, w

    if msg.data == 1 and w==0:
        time.sleep(2)
        pub_speed=rospy.Publisher("cmd_vel",Twist,queue_size=10)
        stop=Twist()
        stop.linear.x=0
        stop.linear.y=0
        stop.linear.z=0
        stop.angular.z=0
        pub_speed.publish(stop)
        w=1
        SearchMode = True
    elif msg.data == 1 and w ==1:
        SearchMode = True 
    elif msg.data ==0 and w ==1:
        SearchMode = False
        pub_speed=rospy.Publisher("cmd_vel",Twist,queue_size=10)
        stop=Twist()
        stop.linear.x=0
        stop.linear.y=0
        stop.linear.z=0
        stop.angular.z=0
        pub_speed.publish(stop)
        w=0
    else:
        SearchMode = False



#--------------------------------------------------------------------------------------------#

def odometria(msg):
    global x1,y1,yaw

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
    rospy.Subscriber('/lost', Int64, lost) 
    pub = rospy.Publisher('cmd_vel',Twist, queue_size=10)
    move = Twist()

    #--------------------------------------------------------------------------------------------#

    while not rospy.is_shutdown():
        global nemobloco,marlinbloco,andar,horario,finding_nemo

        x2 = x1 - deltax # Nemo
        y2 = y1 - deltay
        
                  

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
        if(4.5 <= y1 <= 6.5 and 5.5 <= x1 <= 7.5):   # Interseccao do bloco 1
            marlinlocalizacao = 1
        elif(-6.4 <= y1 <= 5 and 5.5 <= x1 <= 7.5):  # Rua Pavani
            marlinlocalizacao = 2
        elif(-7.9 <= y1 <= -5.9 and 5.5 <= x1 <= 7.5): # Interseccao do bloco 2
            marlinlocalizacao = 3
        elif(-7.9 <= y1 <= -5.9 and -6 <= x1 <= 6): # Rua Koppe
            marlinlocalizacao = 4
        elif(-7.9 <= y1 <= -5.9 and -7.5 <= x1 <= -5.5): # Interseccao do bloco 3
            marlinlocalizacao = 5
        elif(-6.4 <= y1 <= 5 and -7.5 <= x1 <= -5.5):   # Rua Daumas
            marlinlocalizacao = 6
        elif(4.5 <= y1 <= 6.5 and -7.5 <= x1 <= -5.5):     # Interseccao do bloco 4
            marlinlocalizacao = 7
        elif(4.5 <= y1 <= 6.5 and -6 <= x1 <= 6):   # Rua Ikuhara
            marlinlocalizacao = 8
        else:                               # Perdido
            marlinlocalizacao = 0


        print("Marlin-Bloco:",marlinbloco)
        print("Nemo-Bloco:",nemobloco)
        print("Marlin-Localizacao:",marlinlocalizacao)

        # Comandos caso Marlin esteja procurando Nemo (SearchMode)
        if(SearchMode == True):
            if finding_nemo == False:
                if andar == False:
                    if(yaw < -0.03):
                        move.angular.z = 3
                    if(yaw > 0.03):
                        move.angular.z = -3

                if -0.03 < yaw < 0.03:
                    andar = True
                else:
                    andar = False

            finding_nemo = False

            if andar == True:
                # Ida ao centro do bloco para localizar Nemo ou para Marlin se auto localizar
                if marlinbloco == 1:              # No bloco 1
                    if marlinlocalizacao == 0:
                        if 7 - x1 >= 0.5 :
                            move.linear.x=3
                            move.linear.y=0
                        elif -0.5 < 7 - x1 and 7 - x1 < 0.5 and y1 > 6:
                            move.linear.y=-3
                            move.linear.x=0
                        else:
                            move.linear.x=-3
                            move.linear.y=0
                    if marlinlocalizacao == 2:
                        move.linear.x = 0
                        move.linear.y = 3
                    if marlinlocalizacao == 8:
                        move.linear.x = 3
                        move.linear.y = 0
                    if marlinlocalizacao == 1:
                        if nemobloco == marlinbloco :
                            move.linear.x = 0
                            move.linear.y = 0
                            move.angular.z = -3
                            finding_nemo = True
                if marlinbloco == 2 :              # No bloco 2
                    if marlinlocalizacao == 0 :
                        if(7 - x1 >= 0.5):
                            move.linear.x=3
                            move.linear.y=0
                        elif -0.5 < 7 - x1 and 7 - x1 < 0.5 and y1 < -6.4 :
                            move.linear.y=3
                            move.linear.x=0
                        else:
                            move.linear.x=-3
                            move.linear.y=0
                    if marlinlocalizacao == 2:
                        move.linear.x = 0
                        move.linear.y = -3
                    if marlinlocalizacao == 4: 
                        move.linear.x = 3
                        move.linear.y = 0
                    if marlinlocalizacao == 3:
                        if nemobloco == marlinbloco:
                            move.linear.x = 0
                            move.linear.y = 0
                            move.angular.z = -3
                            finding_nemo = True
                if marlinbloco == 3:              # No bloco 3
                    if marlinlocalizacao == 0:
                        if -7 - x1 >= 0.5:
                            move.linear.x=3
                            move.linear.y=0
                        elif -0.5 < -7 - x1 and -7 - x1 < 0.5 and y1 < -6.4:
                            move.linear.y=3
                            move.linear.x=0
                        else:
                            move.linear.x=-3
                            move.linear.y=0
                    if marlinlocalizacao == 4:
                        move.linear.x = -3
                        move.linear.y = 0
                    if marlinlocalizacao == 6: 
                        move.linear.x = 0
                        move.linear.y = -3
                    if marlinlocalizacao == 5:
                        if nemobloco == marlinbloco:
                            move.linear.x = 0
                            move.linear.y = 0
                            move.angular.z = -3
                            finding_nemo = True
                if marlinbloco == 4:              # No bloco 4
                    if marlinlocalizacao == 0:
                        if -7 - x1 >= 0.5:
                            move.linear.x=3
                            move.linear.y=0
                        elif -0.5 < -7 - x1 and -7 - x1 < 0.5 and y1 > 6:
                            move.linear.y=-3
                            move.linear.x=0
                        else:
                            move.linear.x=-3
                            move.linear.y=0
                    if marlinlocalizacao == 8:
                        move.linear.x = -3
                        move.linear.y = 0
                    if marlinlocalizacao == 6 : 
                        move.linear.x = 0
                        move.linear.y = 3
                    if marlinlocalizacao == 7 :
                        if nemobloco == marlinbloco :
                            move.linear.x = 0
                            move.linear.y = 0
                            move.angular.z = -3
                            finding_nemo = True
                
                # Caso bloco do Nemo seja diferente do de Marlin
                if marlinbloco != nemobloco and marlinlocalizacao != 0:
                    if marlinbloco - nemobloco > 0 or marlinbloco - nemobloco == -3 :
                        horario = False
                    else:
                        horario = False

                    if horario == True: # Horario
                        if(marlinlocalizacao == 1):
                            move.linear.x = 0
                            move.linear.y = -3
                            move.angular.z = 0
                        if(marlinlocalizacao == 2):
                            move.linear.x = 0
                            move.linear.y = -3
                            move.angular.z = 0
                        if(marlinlocalizacao == 3):
                            move.linear.x = -3
                            move.linear.y = 0
                            move.angular.z = 0
                        if(marlinlocalizacao == 4):
                            move.linear.x = -3
                            move.linear.y = 0
                            move.angular.z = 0
                        if(marlinlocalizacao == 5):
                            move.linear.x = 0
                            move.linear.y = 3
                            move.angular.z = 0
                        if(marlinlocalizacao == 6):
                            move.linear.x = 0
                            move.linear.y = 3
                            move.angular.z = 0
                        if(marlinlocalizacao == 7):
                            move.linear.x = 3
                            move.linear.y = 0
                            move.angular.z = 0
                        if(marlinlocalizacao == 8):
                            move.linear.x = 0
                            move.linear.y = 3
                            move.angular.z = 0

                    else:                # Anti horario
                        if(marlinlocalizacao == 1):
                            move.linear.x = -3
                            move.linear.y = 0
                            move.angular.z = 0
                        if(marlinlocalizacao == 2):
                            move.linear.x = 0
                            move.linear.y = 3
                            move.angular.z = 0
                        if(marlinlocalizacao == 3):
                            move.linear.x = 0
                            move.linear.y = 3
                            move.angular.z = 0
                        if(marlinlocalizacao == 4):
                            move.linear.x = 3
                            move.linear.y = 0
                            move.angular.z = 0
                        if(marlinlocalizacao == 5):
                            move.linear.x = 3
                            move.linear.y = 0
                            move.angular.z = 0
                        if(marlinlocalizacao == 6):
                            move.linear.x = 0
                            move.linear.y = -3
                            move.angular.z = 0
                        if(marlinlocalizacao == 7):
                            move.linear.x = 0
                            move.linear.y = -3
                            move.angular.z = 0
                        if(marlinlocalizacao == 8):
                            move.linear.x = -3
                            move.linear.y = 0
                            move.angular.z = 0
            pub.publish(move)
        # Comandos caso Marlin tenha encontrado Nemo (StalkerMode)
        else:
            pass
            

#--------------------------------------------------------------------------------------------#

if __name__ == '__main__':
    try:
        time.sleep(20) 
        loop()
    except rospy.ROSInterruptException:
        pass

#--------------------------------------------------------------------------------------------#
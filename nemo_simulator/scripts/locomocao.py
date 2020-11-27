#!/usr/bin/env python
# Movimentacao ponto A ao ponto B

import rospy
from geometry_msgs.msg import Twist
from geometry_msgs.msg import PointStamped
from geometry_msgs.msg import Point
from nav_msgs.msg      import Odometry

from tf.transformations import euler_from_quaternion 
# Necessario para a conversao para Euler

from math import atan2 # Necessario para o uso do arctg

x = 0.0 # Coordenada x, em coordenada arbitraria
y = 0.0 # Coordenada y, em coordenada arbitraria
yaw = 0 # Yaw, em graus

def locomocao(msg):
    global x
    global y
    global yaw


    x = msg.pose.pose.position.x
    y = msg.pose.pose.position.y

    quat = msg.pose.pose.orientation # Quaternion da posicao do Marlin

    (roll, pitch, yaw) = euler_from_quaternion([quat.x,quat.y,quat.z,quat.w]) # Transformada

rospy.init_node ('teste') # Inicializacao

sub = rospy.Subscriber('/odon', Odometry, locomocao) # Recebe a mensagem (Subscriber)

pub = rospy.Publisher('cmd_vel',Twist, queue_size=10) # Envia a mensagem (Publisher)
#Envia os comandos para o Marlin

velocidade = Twist()

tempo = rospy.Rate(4)

destino = Point ()
destino.x = 2
destino.y = 2

while not rospy.is_shutdown(): # Loop do sistema

    deltax = destino.x - x   # Obtencao dos deltas
    deltay = destino.y - y

    angulocarrinhos = atan2(deltax,deltay)

    if abs(angulocarrinhos - yaw) > 0.1:
        velocidade.linear.x = 0.0
        velocidade.angular.z = 3
    else:
        velocidade.linear.x = 3
        velocidade.angular.z = 0.0
    
    tempo.sleep()
    pub.publish(velocidade)

    
if __name__ == '__main__':
    try: 
        locomocao()
    except rospy.ROSInterruptException:
        pass
'''   
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
        '''
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
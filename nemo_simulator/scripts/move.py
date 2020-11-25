import rospy
import std_msgs.msg 

def talker():
    pub = rospy.Publisher('cmd_vel',Vector3)
    rospy.init_node('move')
    while not rospy.is_shutdown():
        x=input("Velocidade de x")
        y=input("Velocidade de y")
        z=input("Velocidade de z")
        yaw=input("Giro em z")
        vel=[a,b,c]
        pub.publish(vel)

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
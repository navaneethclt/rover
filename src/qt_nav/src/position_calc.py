#!/usr/bin/env python
import rospy
from nav_msgs.msg import Odometry
import numpy as np
from geometry_msgs.msg import Twist
import sys
import time
from math import cos,sin

class Position_calc:
    __prev_linear_vel = np.array([0.0,0.0,0.0])
    __prev_angular_vel = np.array([0.0,0.0,0.0])
    __linear_pos = np.array([0.0,0.0,0.0])
    __angular_pos = np.array([0.0,0.0,0.0])
    __time = time.time();
    def __init__(self):
     self.pub = rospy.Publisher('Position_calc',Twist,queue_size = 10)
     self.sub = rospy.Subscriber ('/odom', Odometry, self.get_position)

    def get_position (self,msg):

     angular = msg.twist.twist.angular

     linear = msg.twist.twist.linear

     dt =time.time()-Position_calc.__time
     
     
     angular_vel = np.array([angular.x,angular.y,angular.z])
     Position_calc.__angular_pos =  Position_calc.__angular_pos +np.array( Position_calc.__prev_angular_vel+angular_vel)*dt*0.5
     
     yaw = Position_calc.__angular_pos[2]

     linear_vel = np.array([linear.x*cos(yaw),linear.x*sin(yaw),linear.z])

     Position_calc.__time = time.time()
     Position_calc.__linear_pos =  Position_calc.__linear_pos+ np.array( Position_calc.__prev_linear_vel+linear_vel)*dt*0.5
     
     
     
     Position_calc.__prev_linear_vel = linear_vel
     Position_calc.__prev_angular_vel = angular_vel
     

     
     pos_msg = Twist()
     pos_msg.linear.x = Position_calc.__linear_pos[0]
     pos_msg.linear.y = Position_calc.__linear_pos[1]
     pos_msg.linear.z = Position_calc.__linear_pos[2]

     pos_msg.angular.x = Position_calc.__angular_pos[0] 
     pos_msg.angular.y = Position_calc.__angular_pos[1] 
     pos_msg.angular.z = Position_calc.__angular_pos[2] 
     self.pub.publish(pos_msg)
     #print(linear)
     # print(pos_msg)

def main(args):
      
     rospy.init_node('my_Position_calc')
     r = rospy.Rate(100)
     while not rospy.is_shutdown():
      ic =Position_calc()
      r.sleep()
      
if __name__=='__main__':
     main(sys.argv) 
     
     














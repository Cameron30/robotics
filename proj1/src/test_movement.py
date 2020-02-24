#!/usr/bin/env python

import rospy
import math
import random
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64

def my_callback(msg):

	global angle
	global clockwise
	
	#converting from angles to radians
	angle = 15
	clockwise = [1, -1]
	relative_angle = angle * 2 * PI / 360
	
	distance_moved = msg.data
	
	#1ft = 0.3048m
	if msg.data < 0.3048:
		move.linear.x = 0.1

	if msg.data >= 0.3048:
		msg.angular.z = relative_angle * random.choice(clockwise)
		msg.data = 0
		move.linear.x = 0
		
	pub.publish(move)

if __name__ == '__main__':

	rospy.init_node('test_movement')

	sub = rospy.Subscriber('moved_distance', Float64, my_callback)
	pub = rospy.Publisher('/cmd_vel', Twist, queue_size = '1')
	move = Twist()

	rospy.spin()

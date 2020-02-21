#!/usr/bin/env python

import time
import rospy
from geometry_msgs.msg import Twist

def main():
	rospy.init_node('move_node')

	publisher = rospy.Publisher('/cmd_vel_mux/input/teleop', Twist, queue_size=10)

	while not rospy.is_shutdown():
		msg = Twist()
		#msg.linear.x = .2 
		#publisher.publish(msg)

if __name__ == '__main__':
	main()

#!/usr/bin/env python

import time
import rospy
from geometry_msgs.msg import Twist
from kobuki_msgs.msg import BumperEvent

def shutdown(self):
        # stop turtlebot
        rospy.loginfo("Stop TurtleBot")
        # a default Twist has linear.x of 0 and angular.z of 0.  So it'll stop TurtleBot
        cmd_vel.publish(Twist())
        # sleep just makes sure TurtleBot receives the stop command prior to shutting down the 		# script
        rospy.sleep(1)
def processBump(data):
	print ("Bump")
	global bump
	if (data.state == BumperEvent.PRESSED):
		bump = True
	else:
		bump = False
	rospy.loginfo("Bumper Event")
	rospy.loginfo(data.bumper)

def main():
	rospy.init_node('move_node')

	publisher = rospy.Publisher('/cmd_vel_mux/input/teleop', Twist, queue_size=10)
	sub_bump = rospy.Subscriber('/mobile_base/events/bumper', BumperEvent, processBump)

	r = rospy.Rate(10)
	
	msg = Twist()
	msg.linear.x = 0.2
	while not rospy.is_shutdown():
		publisher.publish(msg)
		r.sleep()

if __name__ == '__main__':
	try:
		main()
	except rospy.Service.Exception as exc:
		rospy.loginfo("Location_Monitor_node terminated.")
		print("Service did not process request: " + str(exc))

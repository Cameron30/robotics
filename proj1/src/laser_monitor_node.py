#!/usr/bin/env python

import rospy
import numpy
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from kobuki_msgs.msg import BumperEvent

bump = False
obstacle = False
toTurn = 1

def shutdown(self):
        # stop turtlebot
        rospy.loginfo("Stop TurtleBot")
        # a default Twist has linear.x of 0 and angular.z of 0.  So it'll stop TurtleBot
        pub_teleop.publish(Twist())
        # sleep just makes sure TurtleBot receives the stop command prior to shutting down the 		# script
        rospy.sleep(1)

#convert index location to degrees
def rangeToDegrees(index):
	centeredIndex = index - 320
	return (centeredIndex * .09375)

def callbackLaser(msg):
	#get the ranges array
	ranges = msg.ranges

	#global boolean to know whether to dodge or not
	global obstacle
	global toTurn
	toTurn = 0

	#set up the np array
	ranges = numpy.array(ranges)
	ranges = ranges[::-1]
	degrees = numpy.array([0])

	#if nan, display the angle in degrees (left is negative, right is positive)
	#otherwise, add to array
	for i in range(len(ranges)):
		if (numpy.isnan(ranges[i]) or ranges[i] < .45) and (numpy.isnan(ranges[i - 1]) or ranges[i - 1] < .45):
			degrees = numpy.append(degrees, rangeToDegrees(i))

	#get the average object location in degrees, and the way to turn
	meanDeg = numpy.mean(degrees)
	
	if meanDeg > 0 or len(degrees) > 1:
		obstacle = True
		toTurn = numpy.sign(meanDeg)
		
		print("Reacting to obstacle:", degrees, meanDeg, toTurn)
	else:
		obstacle = False

def callbackLocation(msg):
	x = msg.pose.pose.position.x
	y = msg.pose.pose.position.y

def callbackBump(data):
	global bump
	if (data.state == BumperEvent.PRESSED):
		bump = True
	else:
		bump = False

def processBehavior(pub_teleop, r):
	msg = Twist()
	global bump
	global obstacle
	global toTurn

	if bump:
		#stop any movement
		pub_teleop.publish(Twist())
		print("Reacting to bump")
	elif obstacle:
		#avoid (this would work for both symmetric and asymmetric)
		msg.angular.z = .7 * toTurn
		#reset boolean
		obstacle = False
		counter = 0

		while(counter < 100):
			pub_teleop.publish(msg)
			counter += 1
			
	else:
		#TODO: Rotate then move for a second
		msg.linear.x = .1
		pub_teleop.publish(msg)

def main():
	global bump
	
	#initialize this node
	rospy.init_node('laser_monitor')

	#subscribe to laser scan, odometry, and bumper
	sub_scan = rospy.Subscriber("/scan", LaserScan, callbackLaser)
	sub_odom = rospy.Subscriber("/odom", Odometry, callbackLocation)
	sub_bump = rospy.Subscriber('/mobile_base/events/bumper', BumperEvent, callbackBump)

	#publish to the robot movement
	pub_teleop = rospy.Publisher('/cmd_vel_mux/input/teleop', Twist, queue_size=10)
	

	#TODO: Add any other required pub/sub

	#initialize some variables
	r = rospy.Rate(10)
	while not rospy.is_shutdown() and not bump:
		#process the behaviors in order then sleep (for a second)
		processBehavior(pub_teleop, r)
		r.sleep()

if __name__ == '__main__':
	main()

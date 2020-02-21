#!/usr/bin/env python

import rospy
import numpy
from sensor_msgs.msg import LaserScan

#convert index location to degrees
def rangeToDegrees(index):
	centeredIndex = index - 320
	return (centeredIndex * .09375)

def callbackLaser(msg):
	#get the ranges array
	ranges = msg.ranges

	#set up the np array
	ranges = numpy.array(ranges)
	ranges = ranges[::-1]
	degrees = numpy.array([0])

	#if nan, display the angle in degrees (left is negative, right is positive)
	#otherwise, add to array
	for i in range(len(ranges)):
		if numpy.isnan(ranges[i]) and numpy.isnan(ranges[i - 1]):
			degrees = numpy.append(degrees, rangeToDegrees(i))

	#get the average object location in degrees, and the way to turn
	meanDeg = numpy.mean(degrees)
	toTurn = numpy.sign(meanDeg) * 45

	print('Mean degree:', meanDeg, 'Way to turn:', toTurn)



def main():

	rospy.init_node('laser_monitor')
	rospy.Subscriber("/scan", LaserScan, callbackLaser)

	rospy.spin()

if __name__ == '__main__':
	main()

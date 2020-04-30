#!/usr/bin/env python

import rospy
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Point, Twist
import math
from math import atan2

x = 0.0
y = 0.0 
theta = 0.0

def newOdom(msg):
	global x
	global y
	global theta

	x = msg.pose.pose.position.x
	y = msg.pose.pose.position.y

	rot_q = msg.pose.pose.orientation
	(roll, pitch, theta) = euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w])

def getDistancesAndPaths(intermediateNodes, landmarkNodes):
	distances = []
	path = []

	for node in landmarkNodes:
		partialDist = []
		partialPath = []
		for destNode in landmarkNodes:
			if node is not destNode:
				if (destNode[0] == node[0] or destNode[1] == node[1]):
					partialDist.append(abs(destNode[0] - node[0]) + abs(destNode[1] - node[1]))
					partialPath.append([destNode])
				else:
					tempDistances = []
					tempPath = []
					for intNode in intermediateNodes:
						if ((intNode[0] == destNode[0] and intNode[1] == node[1]) or 
							(intNode[1] == destNode[1] and intNode[0] == node[0])):

							tempDistances.append(abs(destNode[0] - intNode[0]) + 
								abs(destNode[1] - intNode[1])
								+ abs(node[0] - intNode[0])
								+ abs(node[1] - intNode[1]))	

							tempPath.append([intNode, destNode])
							break
						else:
							for intNode_2 in intermediateNodes:

								if intNode_2 is not intNode: 
									if ((intNode[0] == intNode_2[0]) and 
										(node[1] == intNode[1] and destNode[1] == intNode_2[1])):

										tempDistances.append(abs(node[0] - intNode[0]) + 
											abs(node[1] - intNode[1])
												+ abs(intNode[0] - intNode_2[0])
												+ abs(intNode[1] - intNode_2[1])
												+ abs(intNode_2[0] - destNode[0])
												+ abs(intNode_2[1] - destNode[1]))
										tempPath.append([intNode, intNode_2, destNode])

									elif ((intNode[0] == intNode_2[0]) and 
										(node[1] == intNode_2[1] and destNode[1] == intNode[1])):

										tempDistances.append(abs(node[0] - intNode_2[0]) + 
											abs(node[1] - intNode_2[1])
												+ abs(intNode[0] - intNode_2[0])
												+ abs(intNode[1] - intNode_2[1])
												+ abs(intNode[0] - destNode[0])
												+ abs(intNode[1] - destNode[1]))
										tempPath.append([intNode_2, intNode, destNode])
					while len(tempDistances) > 1:
						if (tempDistances[0] > tempDistances[1]):
							tempDistances.pop(0)
							tempPath.pop(0)
						else:
							tempDistances.pop(1)
							tempPath.pop(1)

					partialDist.append(tempDistances[0])
					partialPath.append(tempPath[0])
			else:
				partialDist.append(9999)
				partialPath.append(9999)

		distances.append(partialDist)
		path.append(partialPath)

	return distances, path	

def buildRoute(start, travel, distances, path):
	orders = []
	possibleDistances = []

	for i in path:
		print (i)

	if len(travel) == 1:
		possibleDistances.append(distances[start - 1][travel[0]-1])
		orders.append(travel[0])
	elif len(travel) == 2:
		orders.append([travel[0], travel[1]])
		possibleDistances.append(distances[start - 1][travel[0] - 1] + distances[travel[0] - 1][travel[1] - 1])

		orders.append([travel[1], travel[0]])
		possibleDistances.append(distances[start - 1][travel[1] - 1] + distances[travel[1] - 1][travel[0] - 1])
	elif len(travel) == 3:
		for node in travel:
			for destNode in travel:
				if destNode is not node:
					for finalNode in travel:
						if finalNode is not node and finalNode is not destNode:
							orders.append([node, destNode, finalNode])
							possibleDistances.append(distances[start - 1][node - 1] 
								+ distances[node - 1][destNode - 1] 
								+ distances[destNode - 1][finalNode - 1])
	elif len(travel) == 4:
		for node in travel:
			for destNode in travel:
				if destNode is not node:
					for semifinalNode in travel:
							if semifinalNode is not node and semifinalNode is not destNode:
								for finalNode in travel:
									if finalNode is not semifinalNode and finalNode is not destNode and finalNode is not node:
										orders.append([node, destNode, semifinalNode, finalNode])
										possibleDistances.append(distances[start - 1][node - 1] 
											+ distances[node - 1][destNode - 1] 
											+ distances[destNode - 1][semifinalNode - 1]
											+ distances[semifinalNode - 1][finalNode - 1])

	while len(possibleDistances) > 1:
		if (possibleDistances[0] > possibleDistances[1]):
			possibleDistances.pop(0)
			orders.pop(0)
		else:
			possibleDistances.pop(1)
			orders.pop(1)

	finalPath = []

	if isinstance(orders[0], int):
		orders = [orders]

	if len(orders[0]) > 1:
		for i in range(len(orders[0])):
			if i == 0:
				finalPath.append(path[start - 1][orders[0][i] - 1])
			else:
				finalPath.append(path[orders[0][i - 1] - 1][orders[0][i] - 1])

	else:
		finalPath.append(path[start - 1][orders[0][0] - 1])

	return possibleDistances[0], finalPath				
	
def getInput():	
	global x
	global y

	intermediateNodes = [[7.75,0],[7.75,8.5],[33,8.5],[33,0]]

	landmarkNodes = [[0,0],[33,0],[7.75,1.5],[5.75,8.5],[19.75,8.5]]	

	travel = []

	for i in range(len(landmarkNodes)):
		if(abs(landmarkNodes[i][0]-x) < .1 and abs(landmarkNodes[i][1]-y) < .1):
			current = i + 1

	numbers = raw_input()

	for num in numbers:
		travel.append(int(num))

	distances, path = getDistancesAndPaths(intermediateNodes, landmarkNodes)


	finalDistance, finalPath = buildRoute(current, travel, distances, path)


	nodes = []

	for nodeGroup in finalPath:
		if len(nodeGroup[0]) > 0:
			for node in nodeGroup:
				nodes.append(node)
		else:
			nodes.append(node)


	print('Distance:', finalDistance, 'Path:', nodes)

	return finalDistance, nodes

def moveToNode(pub_teleop, node):
	global x
	global y
	global theta

	speed = Twist()

	r = rospy.Rate(1)

	while not rospy.is_shutdown():
    		inc_x = node[0] -x
    		inc_y = node[1] -y

    		angle_to_goal = atan2(inc_y, inc_x)
		
		rot_speed = (angle_to_goal - theta)

		if (rot_speed > math.pi):
			rot_speed -= 2 * math.pi
    		if abs(angle_to_goal - theta) > 0.1:
        		speed.linear.x = 0.0
        		speed.angular.z = rot_speed
    		elif abs(inc_x) > .1 or abs(inc_y) > .1:
        		speed.linear.x = 0.5
        		speed.angular.z = 0.0
		else:
			return True

    		pub_teleop.publish(speed)
    		r.sleep() 

def main():
	#initialize this node
	rospy.init_node('nodeTraversal')

	sub = rospy.Subscriber("/odom", Odometry, newOdom)
	pub_teleop = rospy.Publisher('/cmd_vel_mux/input/teleop', Twist, queue_size=10)

	r = rospy.Rate(10)
	while not rospy.is_shutdown():
		distance, nodes = getInput()

		for node in nodes:
   			complete = moveToNode(pub_teleop, node)	

		r.sleep()

if __name__ == '__main__':
	main()




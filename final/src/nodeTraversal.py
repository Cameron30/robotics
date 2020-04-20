#!/usr/bin/env python

import rospy

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

	if len(travel) == 1:
		possibleDistances.append(distances[start - 1][travel[0]])
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
	print (possibleDistances, 'Orders:', orders)

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
	intermediateNodes = [[7.75,0],[7.75,8.5],[31.5,8.5],[31.5,0]]

	landmarkNodes = [[0,0],[31.5,0],[7.75,1.5],[5.75,8.5],[19.75,8.5]]	

	travel = []

	current = 1

	numbers = raw_input()

	for num in numbers:
		travel.append(int(num))

	distances, path = getDistancesAndPaths(intermediateNodes, landmarkNodes)


	finalDistance, finalPath = buildRoute(current, travel, distances, path)

	print('Distance:', finalDistance, 'Path:', finalPath)

def main():
	#initialize this node
	rospy.init_node('nodeTraversal')
	

	r = rospy.Rate(10)
	while not rospy.is_shutdown():
		#process the behaviors in order then sleep (for a second)
		getInput()
		r.sleep()

if __name__ == '__main__':
	main()




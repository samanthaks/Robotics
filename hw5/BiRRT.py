import sys
import random
import math
import numpy as np 
import matplotlib.path as mplPath
import matplotlib.pyplot as plt
import matplotlib.patches as patches

global obstacles

def isCollision(line1, obstacles):
	for obstacle in obstacles:
		for i in range(0, len(obstacle)):
			if(i==len(obstacle)-1):
				line2 = [tuple(obstacle[0]), tuple(obstacle[i])]
				if isIntersection(line1,line2):
					return True

			else:
				line2 = [tuple(obstacle[i]),tuple(obstacle[i+1])]
				if isIntersection(line1, line2):
					return True

	return False

		
def isIntersection(line1,line2):
	p1 = line1[0]
	p2 = line1[1]
	p3 = line2[0]
	p4 = line2[1]

	A1 = (p1[1] - p2[1])
	B1 = (p2[0] - p1[0])
	C1 = (p1[0]*p2[1] - p2[0]*p1[1]) * -1

	A2 = (p3[1] - p4[1])
	B2 = (p4[0] - p3[0])
	C2 = (p3[0]*p4[1] - p4[0]*p3[1]) * -1
    	
	det  = A1 * B2 - B1 * A2
	det_x = C1 * B2 - B1 * C2
	det_y = A1 * C2 - C1 * A2
    
	if det != 0:
		x = det_x / det
		y = det_y / det
		
		if (p1[0] <= int(x) <= p2[0] or p2[0] <= int(x) <= p1[0]) and (p1[1] <= int(y) <= p2[1] or p2[1] <= int(y) <= p1[1]) and (p3[0] <= int(x) <= p4[0] or p4[0] <= int(x) <= p3[0]) and (p3[1] <= int(y) <= p4[1] or p4[1] <= int(y) <= p3[1]):
			return (int(x),int(y))
		
		#else:
			
	else:
		return False

def generate_point():
	return [random.randint(0,700), random.randint(0,700)]

def distance(point_1, point_2):
	x1 = point_1[0]
	y1 = point_1[1]
	x2 = point_2[0]
	y2 = point_2[1]
	return math.sqrt((x2-x1)**2 + (y2-y1)**2)

def get_min_distance(new_point,tree):
	min_dist = 10000000000
	connecting_point = []
	for tree_point in list(tree):
		dist = distance(tree_point, new_point)
		if dist < min_dist:
			min_dist = dist
			connecting_point = tree_point
	return min_dist, connecting_point

def path_finder(args):
	#print(args)
	start_file = open(args[1],'r')
	obstacles_file = open(args[2],'r')
	epsilon = args[3]

	start = start_file.readline()
	start = list(map(int, start.split()))
	end = start_file.readline()
	end = list(map(int, end.split()))

	fig = plt.figure()

	line = obstacles_file.readline()
	obstacles = []
	if line != "":
		num_obstacles = int(line)
		line = obstacles_file.readline()		
		while line != "":
			vertices = int(line)
			polypath = []
			for vertex in range(vertices):
				point = obstacles_file.readline()
				points = point.split(" ")
				polypath.append([int(points[0]), int(points[1])])
			obstacle =  mplPath.Path(polypath)
			obstacles.append(polypath)
			ax = fig.add_subplot(111)
			patch = patches.PathPatch(obstacle, lw=0)
			ax.add_patch(patch)
			line = obstacles_file.readline()
    
	
	ax.set_xlim(0,700)
	ax.set_ylim(700,0)
	'''plt.show()'''

	nodes1 = {}
	nodes2 = {}
	
	start = tuple(start)
	end = tuple(end)
	tree1 = set()
	tree2 = set()
	tree1.add(start)
	tree2.add(end)

	new_point1 = start
	new_point2 = end
	
	# plot(start)
	count = 0 
	check1 = 10000000
	check2 = 10000000
	goal_radius = 50
	N = 1000
	
	while (check1 > goal_radius or isCollision([new_point_check1,(int(store2[0]),int(store2[1]))],obstacles)) and (check2 > goal_radius or isCollision([new_point_check2,(int(store1[0]),int(store1[1]))],obstacles))  and count < N:
		new_point1 = generate_point()
		new_point_check1 = new_point1

		new_point2 = generate_point()
		new_point_check2 = new_point2
		
		min_distance1,parent1 = get_min_distance(new_point1,tree1)
		min_distance2,parent2 = get_min_distance(new_point2,tree2)

		if min_distance1 > int(epsilon):
			angle = math.atan2(new_point1[1] - parent1[1], new_point1[0] - parent1[0])
			new_point1 = [parent1[0] + int(epsilon) * math.cos(angle), parent1[1] + int(epsilon) * math.sin(angle)]
			new_point_check1 = [int(parent1[0] + int(epsilon) * math.cos(angle)), int(parent1[1] + int(epsilon) * math.sin(angle))]

		if min_distance2 > int(epsilon):
			angle = math.atan2(new_point2[1] - parent2[1], new_point2[0] - parent2[0])
			new_point2 = [parent2[0] + int(epsilon) * math.cos(angle), parent2[1] + int(epsilon) * math.sin(angle)]
			new_point_check2 = [int(parent2[0] + int(epsilon) * math.cos(angle)), int(parent2[1] + int(epsilon) * math.sin(angle))]


		
		
		while tuple(new_point1) in tree1 or isCollision([(int(parent1[0]),int(parent1[1])),tuple(new_point_check1)],obstacles):
			new_point1 = generate_point()
			new_point_check1 = new_point1
			min_distance1,parent1 = get_min_distance(new_point1,tree1)

			if min_distance1 > int(epsilon):
				angle = math.atan2(new_point1[1] - parent1[1], new_point1[0] - parent1[0])
				new_point1 = [parent1[0] + int(epsilon) * math.cos(angle), parent1[1] + int(epsilon) * math.sin(angle)]
				new_point_check1 = [int(parent1[0] + int(epsilon) * math.cos(angle)), int(parent1[1] + int(epsilon) * math.sin(angle))]



		while tuple(new_point2) in tree2 or isCollision([(int(parent2[0]),int(parent2[1])),tuple(new_point_check2)],obstacles):
			new_point2 = generate_point()
			new_point_check2 = new_point2
			min_distance2,parent2 = get_min_distance(new_point2,tree2)

			if min_distance2 > int(epsilon):
				angle = math.atan2(new_point2[1] - parent2[1], new_point2[0] - parent2[0])
				new_point2 = [parent2[0] + int(epsilon) * math.cos(angle), parent2[1] + int(epsilon) * math.sin(angle)]
				new_point_check2 = [int(parent2[0] + int(epsilon) * math.cos(angle)), int(parent2[1] + int(epsilon) * math.sin(angle))]


		
		plt.plot([parent1[0],new_point1[0]],[parent1[1],new_point1[1]],'r')
		plt.plot([parent2[0],new_point2[0]],[parent2[1],new_point2[1]],'b')
		nodes1[tuple(new_point1)] = parent1
		tree1.add(tuple(new_point1))

		nodes2[tuple(new_point2)] = parent2
		tree2.add(tuple(new_point2))

		check2, store1 = get_min_distance(new_point2,tree1)
		check1, store2 = get_min_distance(new_point1,tree2)
	
		count+=1

	nodes1[tuple(new_point1)] = parent1
	nodes2[tuple(new_point2)] = parent2

	if check2 < goal_radius:
		current1 = store1
		current2 = new_point2
	else:
		current1 = new_point1
		current2 = store2

	plt.plot([current1[0],current2[0]],[current1[1],current2[1]],'b')
	
	#print(list(tree))
	plt.scatter(56,18, c ='r')
	plt.scatter(448,542, c='b')
	plt.scatter(448,542,s=3)
	
	for entry in list(tree1):
		plt.scatter(entry[0],entry[1],s=10,c='r')

	for entry in list(tree2):
		plt.scatter(entry[0],entry[1],s=10,c='b')

	
	while current1 != start:
		plt.scatter(current1[0],current1[1],s=10,c='k',zorder=3)
		current1 = nodes1[tuple(current1)]
	
	while current2 != end:
		plt.scatter(current2[0],current2[1],s=10,c='k',zorder=3)
		current2 = nodes2[tuple(current2)]
	
	#plt.plot([new_point[0],end[0]],[new_point[1],end[1]],'k')
	plt.show()


if __name__ == '__main__':
	if len(sys.argv) != 4:
		print("EXITING")
		print("Incorrect number of command line arguments")
		print("Example: python3 path_finder.py start_goal.txt world_obstacles.txt DISTANCE")
	else:
		path_finder(sys.argv)

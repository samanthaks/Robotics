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

	nodes = {}
	start = tuple(start)
	tree = set()
	tree.add(start)
	new_point = start
	new_point_check = start

	
	# plot(start)
	count =0 
	goal_radius = 50
	N = 1000
	while (distance(new_point,tuple(end)) > goal_radius or isCollision([new_point_check,end],obstacles)) and count != N:
		new_point = generate_point()
		new_point_check = new_point
		min_distance,parent = get_min_distance(tuple(new_point),tree)

		if min_distance > int(epsilon):
			angle = math.atan2(new_point[1] - parent[1], new_point[0] - parent[0])
			new_point = [parent[0] + int(epsilon) * math.cos(angle), parent[1] + int(epsilon) * math.sin(angle)]
			new_point_check = [int(parent[0] + int(epsilon) * math.cos(angle)), int(parent[1] + int(epsilon) * math.sin(angle))]


		
		
		while tuple(new_point) in tree or isCollision([(int(parent[0]),int(parent[1])),new_point_check],obstacles):
			new_point = generate_point()
			new_point_check = new_point
			min_distance,parent = get_min_distance(new_point,tree)

			if min_distance > int(epsilon):
				angle = math.atan2(new_point[1] - parent[1], new_point[0] - parent[0])
				new_point = [parent[0] + int(epsilon) * math.cos(angle), parent[1] + int(epsilon) * math.sin(angle)]
				new_point_check = [int(parent[0] + int(epsilon) * math.cos(angle)), int(parent[1] + int(epsilon) * math.sin(angle))]

	

		current_point = new_point
		plt.plot([parent[0],new_point[0]],[parent[1],new_point[1]],'k')
		nodes[tuple(current_point)] = parent
		tree.add(tuple(current_point))
		#print(tree)
		print(len(tree))
		count+=1

	nodes[tuple(end)] = new_point
	
	#print(list(tree))
	plt.scatter(56,18, s=25,c ='r')
	plt.scatter(448,542)
	plt.scatter(448,542,s=3)
	for entry in list(tree):
		plt.scatter(entry[0],entry[1],s=10,c='k')

	current = end
	while current != start:
		plt.scatter(current[0],current[1],s=20,c='r',zorder = 5)
		current = nodes[tuple(current)]

	plt.scatter(current[0],current[1],s=20,c='r',zorder = 5)
	plt.plot([new_point[0],end[0]],[new_point[1],end[1]],'k')
	plt.show()


if __name__ == '__main__':
	if len(sys.argv) != 4:
		print("EXITING")
		print("Incorrect number of command line arguments")
		print("Example: python3 path_finder.py start_goal.txt world_obstacles.txt DISTANCE")
	else:
		path_finder(sys.argv)


	

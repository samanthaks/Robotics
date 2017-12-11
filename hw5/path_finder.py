import sys
import random
import numpy as np 
import matplotlib.path as mplPath
import matplotlib.pyplot as plt
import matplotlib.patches as patches

global obstacles

def isCollision(point):
	for obstacle in obstacles:
		if obstacle.contains_point(point):
			return true

	return false

def generate_point():
	return [random.randint(0,600), random.randint(0,600)]

def distance(point_1, point_2):
	x1 = point_1[0]
	y1 = point_1[1]
	x2 = point_2[0]
	y2 = point_2[1]
	return sqrt((x2-x1)**2 + (y2-y1)**2)

def get_min_distance(new_point,tree):
	min_dist = 10000000000
	connecting_point = []
	for tree_point in list(tree):
		dist = distance(tree_point, new_point)
		if dist < min_dist:
			min_dist = dist
			connecting_point = tree_point
	return min_dist, tree_point

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
			print(polypath)
			obstacle =  mplPath.Path(polypath)
			obstacles.append(obstacle)
			ax = fig.add_subplot(111)
			patch = patches.PathPatch(obstacle, facecolor='red', lw=0)
			ax.add_patch(patch)
			line = obstacles_file.readline()

	ax.set_xlim(0,600)
	ax.set_ylim(0,600)
	plt.show()

	nodes = {}
	tree = set([start])
	current_point = []
		
	# plot(start)

	while current_point != end:
		new_point = generate_point()
		if new_point in tree: #or collision(new_point):
			break	

		min_distance,parent = get_min_distance(new_point,tree)

		while(min_distance > epsilon):
			new_point = generate_point()
			min_distance,parent = get_min_distance(new_point,tree)
	
		current_point = new_point	
		nodes[current_point] = parent
		tree.add(current_point)
		# plot_line(parent, current_point)


if __name__ == '__main__':
	if len(sys.argv) != 4:
		print("EXITING")
		print("Incorrect number of command line arguments")
		print("Example: python3 path_finder.py start_goal.txt world_obstacles.txt DISTANCE")
	else:
		path_finder(sys.argv)

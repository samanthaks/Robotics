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
		
					
		
	
	


if __name__ == '__main__':
	if len(sys.argv) != 4:
		print("EXITING")
		print("Incorrect number of command line arguments")
		print("Example: python3 path_finder.py start_goal.txt world_obstacles.txt DISTANCE")
	else:
		path_finder(sys.argv)

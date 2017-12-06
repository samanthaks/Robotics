import sys
import random

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
	start = list(map(int, start.split())
	end = start_file.readline()
	end = list(map(int, end.split())
	
					
		
	
	


if __name__ == '__main__':
	if len(sys.argv) != 4:
		print("EXITING")
		print("Incorrect number of command line arguments")
		print("Example: python3 path_finder.py start_goal.txt world_obstacles.txt DISTANCE")
	else:
		path_finder(sys.argv)

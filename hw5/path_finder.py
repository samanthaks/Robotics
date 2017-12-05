import sys

def path_finder(args):
	print(args)

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print("EXITING")
		print("Incorrect number of command line arguments")
		print("Example: python3 path_finder.py DISTANCE")
	else:
		path_finder(sys.argv)
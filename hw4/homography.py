# image is the four corners
import cv2
import numpy as np
import math

def mouse_callback(event, x, y, flags, params):
	if event == cv2.EVENT_LBUTTONDOWN:
		global clicks
		clicks.append([x,y])
		cv2.circle(img, (x,y), 5, (255,192,203), -1)
		cv2.imshow("image", img)
		#if len(clicks) == 4:
			#return
			#homography(img, np.array(clicks))

def homography(im_source, pts_source):
	cm_width = 30
	cm_height = 22.5

	in_width = cm_width * 0.393701
	in_height = cm_height * 0.393701

	px_width = round(in_width * 50)
	px_height = round(in_height * 50)

	pts_roadway = np.array([[0,0],[px_width,0],[px_width,px_height],[0,px_height]])

	transform, status = cv2.findHomography(pts_source, pts_roadway)

	im_roadway = cv2.warpPerspective(im_source, transform,(px_width,px_height))
	cv2.imwrite("homography_img.jpg",im_roadway)
	
	return im_roadway,transform # returns homographied image

def transform_img(img, transform):
	cm_width = 30
	cm_height = 22.5

	in_width = cm_width * 0.393701
	in_height = cm_height * 0.393701

	px_width = round(in_width * 50)
	px_height = round(in_height * 50)

	homographied_image = cv2.warpPerspective(img, transform,(px_width,px_height))
	return homographied_image

def b_and_w(im_homography):
	# gaussian blur
	#im_homography = cv2.GaussianBlur(im_homography,(5,5),0)
	#cv2.imshow("test",im_homography)

	yellow_bounds = [[10,100,100],[40,255,255]]
	lower = yellow_bounds[0]
	upper = yellow_bounds[1]

	lower = np.array(lower, dtype="uint8")
	upper = np.array(upper, dtype="uint8")
	
	hsv = cv2.cvtColor(im_homography, cv2.COLOR_BGR2HSV)
	cv2.imwrite('hsv_image.jpg',hsv)
	im_hsv = cv2.imread('hsv_image.jpg')

	mask = cv2.inRange(im_hsv, lower, upper)
	output = cv2.bitwise_and(im_hsv, im_hsv, mask=mask)
	output = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
		
	ret, thresh1 = cv2.threshold(output, 0, 255, cv2.THRESH_BINARY)
	_, contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	contour_list = []

	for contour in contours:
		area = cv2.contourArea(contour)
		if area > 10000:
			contour_list.append(contour)
			

	
            
        
	image = np.zeros(thresh1.shape, np.uint8)        
	cv2.drawContours(image, contour_list,  -1, (255,0,0), 3)
	

	#cv2.imshow("ret", thresh1)
	return image


def canny_lines(b_and_w):
	edges = cv2.Canny(b_and_w,100,200)
	#cv2.imshow("lines",edges)
	return(edges)

def hough(edges, new_hom):
	#img = cv2.imread('homography_img.jpg')
	#cv2.imshow('hom',new_hom)
	#cv2.waitKey(10000)
	img = new_hom
	height, width = img.shape[:2]
	lines = cv2.HoughLines(edges, 1, np.pi/90, 75)
	line_1 = []
	line_2 = []
	for line in lines:
		line = line[0]
		rho = line[0]
		theta = line[1]
		a = np.cos(theta)
		b = np.sin(theta)
		x0 = a*rho
		y0 = b*rho
		x1 = int(x0 + 1000*(-b))
		y1 = int(y0 + 1000*(a))
		x2 = int(x0 - 1000*(-b))
		y2 = int(y0 - 1000*(a))

		if line_1 == []:
			line_1 = [x1,y1,x2,y2,rho,theta]
		elif line_2 == [] and ((abs(line_1[0] - x1) > 30 or abs(line_1[2] - x2) > 30) or (abs(line_1[1] - y1) > 30 or abs(line_1[3] - y2) > 30)):
			line_2 = [x1,y1,x2,y2,rho,theta]
			
	if not line_2 == []:	
		ctr_x1 = round((line_1[0] + line_2[0])/2)
		ctr_y1 = round((line_1[1] + line_2[1])/2)
		ctr_x2 = round((line_1[2] + line_2[2])/2)
		ctr_y2 = round((line_1[3] + line_2[3])/2)
		#cv2.line(img,(ctr_x1,ctr_y1),(ctr_x2,ctr_y2),(0,0,255),2)
		#cv2.imshow('hough_lines',img)
		#cv2.waitKey(5000)
		return([ctr_x1,ctr_y1,ctr_x2,ctr_y2],line_1[4],math.degrees(line_1[5]))	
	else:
		#cv2.line(img,(line_1[0],line_1[1]),(line_1[2],line_1[3]),(0,0,255),2)	
		#cv2.imshow('hough_lines',img)
		#cv2.waitKey(5000)
		return(line_1[:4],line_1[4],math.degrees(line_1[5]))


def main():
	global img
	global clicks

	clicks = list()
	img = cv2.imread('image.jpg')

	cv2.namedWindow('image', cv2.WINDOW_NORMAL)
	cv2.setMouseCallback('image', mouse_callback) 
	
	cv2.imshow("image",img)
	key = cv2.waitKey(0) & 0xFF

	if key == ord('c'):
		if len(clicks) == 4:
			im_hom,transform = homography(img, np.array(clicks))

			new_img = cv2.imread('image.jpg')
			
			# code with the homography cropping
			
			new_hom = transform_img(new_img, transform)
	
			black_and_white = b_and_w(new_hom)
			edges = canny_lines(black_and_white)

			cv2.imshow("test",edges)
			cv2.waitKey(0)

			hough_coords, hough_rho, hough_angle = hough(edges, new_hom)
			#print(hough_angle)
			#print(hough_rho)
			
			'''
			# code without
			black_and_white = b_and_w(new_img)
			edges = canny_lines(black_and_white)
			hough_coords, hough_rho, hough_angle = hough(edges, new_img)
			point_1 = hough_coords[:2]
			point_2 = hough_coords[2:]
			
			source_point_1 = np.array([point_1[0],point_1[1],1])
			source_point_2 = np.array([point_2[0],point_2[1],1])
			roadway_point_1 = transform.dot(source_point_1)	
			roadway_point_2 = transform.dot(source_point_2)
			roadway_1 = [int(roadway_point_1[0]/roadway_point_1[2]), int(roadway_point_1[1]/roadway_point_1[2])]	
			roadway_2 = [int(roadway_point_2[0]/roadway_point_2[2]), int(roadway_point_2[1]/roadway_point_2[2])]
			print(roadway_1)
			print(roadway_2)
			return
			slope = (roadway_2[1] - roadway_1[1])/(roadway_2[0] - roadway_1[0])
			intercept = roadway_1[1] - (slope * roadway_1[0])
			print(slope)
			print(intercept)
			# y = slope(x) + intercept
			x1 = -1000
			x2 = 1000
			y1 = int((slope * x1) + intercept)
			y2 = int((slope * x2) + intercept)
			print(x1,y1)
			print(x2,y2)
			homog = transform_img(new_img, transform)	
			cv2.line(homog,(x1,y1),(x2,y2),(0,0,255),2)	
			cv2.imshow('hough_lines',homog)
			cv2.waitKey(0)

			'''
			if (hough_rho > 0 and hough_angle > 5 and hough_angle < 90):
				turn_angle = hough_angle
				print("turn " + str(turn_angle) + " degrees right")
			elif (hough_rho < 0 and hough_angle > 95 and hough_angle < 175):
				turn_angle = -(180 - hough_angle)
				print("turn " + str(turn_angle) + " degrees left")
			else:
				print("parallel")		
main()

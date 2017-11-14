

# image is the four corners
import cv2
import numpy as np

img = cv2.imread('image.jpg')

def mouse_callback(event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN:
        	global clicks
        	clicks.append([x,y])
        	print(clicks)
        	if len(clicks) == 4:
        		homography(img, np.array(clicks))

def homography(im_source, pts_source):
	print("Hi")
	print(pts_source)
	cm_width = 30
	cm_height = 22.5

	in_width = cm_width * 0.393701
	in_height = cm_height * 0.393701

	px_width = round(in_width * 50)
	px_height = round(in_height * 50)

	pts_roadway = np.array([[0,0],[px_width,0],[px_width,px_height],[0,px_height]])

	transform, status = cv2.findHomography(pts_source, pts_roadway)

	im_roadway = cv2.warpPerspective(im_source, transform,(px_width,px_height))

	cv2.imshow("roadway", im_roadway)

clicks = list()
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.setMouseCallback('image',  mouse_callback) 



# show the images
cv2.imshow("image", img)
cv2.waitKey(0)
import cv2
import numpy as np
import time
import io 
from homography import mouse_callback, homography


if __name__ == '__main__' :

	## capture image 
	# capture_image()

	## read + show image 
	img = cv2.imread('image.jpg')
	clicks = list()
	cv2.namedWindow('image', cv2.WINDOW_NORMAL)
	clicks = cv2.setMouseCallback('image', mouse_callback) 

	cv2.imshow("image", img)
	cv2.waitKey(0)

	homography(img, np.array(clicks))
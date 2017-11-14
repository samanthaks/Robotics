import cv2
import numpy as np
import time

clicks = list()

def mouse_callback(event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN:
        	global clicks
        	clicks.append([x,y])
        	print(clicks)

img = cv2.imread('image.png',0)
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.setMouseCallback('image',  mouse_callback)        

# show the images
cv2.imshow("image", img)
cv2.waitKey(0)
        
    

# import the necessary packages
import numpy as np
import cv2

def detect_stop(image):

    boundaries = [([0, 0, 200], [200, 200, 255])] #orange

    im = cv2.imread(image)
    # hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)

    for (lower, upper) in boundaries:
        lower = np.array(lower,dtype = "uint8")
        upper = np.array(upper, dtype = "uint8")
        mask = cv2.inRange(im, lower, upper)
        output = cv2.bitwise_and(im, im, mask = mask)
        gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
                         
        ret,thresh1 = cv2.threshold(gray,0,255,cv2.THRESH_BINARY)
        _, contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contour_list = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 500:
                contour_list.append(contour)

        maximum = 0
        biggest_contour = None
        for contour in contour_list:
            temp = cv2.contourArea(contour)
            if temp > maximum:
                maximum = temp
                biggest_contour = contour

        cnt = biggest_contour

        moments = cv2.moments(cnt)
        if (moments['m00'] >0):
            cx = int(moments['m10'] / moments['m00'])
            cy = int(moments['m01'] / moments['m00'])

            pos_y = cx
        else:
            pos_y = False
        return(pos_y)
        # cv2.drawContours(im, biggest_contour, -1, (255,0,0), 2)
        # cv2.imshow('Objects Detected', im)
        # cv2.waitKey(0)


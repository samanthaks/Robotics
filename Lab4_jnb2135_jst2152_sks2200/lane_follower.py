# image is the four corners
import cv2
import numpy as np
import math
import move_robot as mr
import capture_img as ci
from picamera import PiCamera
from gopigo import *

def mouse_callback(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        global clicks
        clicks.append([x,y])
        cv2.circle(img, (x,y), 5, (255,192,203), -1)
        cv2.imshow("image", img)

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
    cv2.imwrite('testing.jpg',homographied_image)
    return homographied_image

def b_and_w(im_homography, yellow_bounds=[[0,100,200],[60,255,255]]):
#def b_and_w(im_homography, yellow_bounds=[[0,100,100],[60,255,255]]):

    # gaussian blur
    #im_homography = cv2.GaussianBlur(im_homography,(5,5),0)
    #cv2.imshow("test",im_homography)
    #yellow_bounds = [[10,200,100],[60,255,255]]  
    #yellow_bounds = [[30,20,0],[70,150,255]]
    lower = yellow_bounds[0]
    upper = yellow_bounds[1]

    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")

    height,width = im_homography.shape[:2]
    print(im_homography[width/2][0])
    
    hsv = cv2.cvtColor(im_homography, cv2.COLOR_BGR2HSV)
    cv2.imwrite('hsv_image.jpg',hsv)
    im_hsv = cv2.imread('hsv_image.jpg')

    mask = cv2.inRange(im_hsv, lower, upper)
    output = cv2.bitwise_and(im_hsv, im_hsv, mask=mask)
    output = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
        
    ret, thresh1 = cv2.threshold(output, 0, 255, cv2.THRESH_BINARY)
    #cv2.imshow('bandw',thresh1)
    #cv2.waitKey(5000)

    _, contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contour_list = []

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 3000:
            contour_list.append(contour)
             
    image = np.zeros(thresh1.shape, np.uint8)        
    cv2.drawContours(image, contour_list,  -1, (255,0,0), 3)
    cv2.fillPoly(image, pts=contour_list, color=(255,255,255))
    #cv2.imshow("plz work",image)
    #cv2.imshow("ret", thresh1)
    return image


def canny_lines(b_and_w):
    edges = cv2.Canny(b_and_w,100,200)
    cv2.imshow("lines",edges)
    cv2.waitKey(2000)
    return(edges)

def hough(edges, new_hom):
    # not 60 to 120, and rho is positive
    #img = cv2.imread('homography_img.jpg')
    #cv2.imshow('hom',new_hom)
    #cv2.waitKey(10000)
    img = new_hom
    height, width = img.shape[:2]
    lines = cv2.HoughLines(edges, 1, np.pi/90, 40)
    line_1 = []
    line_2 = []

    if lines == None:
        return(None, None, None, False)
        #mr.turn_left_degrees(10)
        #ci.capture_img(camera)
        #try_again = cv2.imread('current_image.jpg')
        #hough(edges,try_again)
    all_lines = []
    orange = False
    for line in lines:
        line = line[0]
        rho = line[0]
        theta = line[1]
        if(rho > 0 and math.degrees(theta) > 80 and math.degrees(theta) < 100):
            orange = True
        else:
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a*rho
            y0 = b*rho
            x1 = int(x0 + 1000*(-b))
            y1 = int(y0 + 1000*(a))
            x2 = int(x0 - 1000*(-b))
            y2 = int(y0 - 1000*(a))
            all_lines.append([x1,y1,x2,y2,rho,theta])
        #cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)  


        #if line_1 == []:
        #    line_1 = [x1,y1,x2,y2,rho,theta]
        #elif line_2 == [] and ((abs(line_1[0] - x1) > 30 or abs(line_1[2] - x2) > 30) or (abs(line_1[1] - y1) > 30 or abs(line_1[3] - y2) > 30)):
        #    line_2 = [x1,y1,x2,y2,rho,theta]
    if all_lines == []:
        return(None, None, None, orange)
    line = all_lines[0]
    cv2.line(img,(line[0],line[1]),(line[2],line[3]),(0,0,255),2)
    #cv2.imshow('hough_lines',img)
    #cv2.waitKey(5000)
    return(line[:4],line[4],math.degrees(line[5]), orange)
    #if line_1[5] < line_2[5]:
    #    choose = '1'
    #else:
    #    choose = '2'

    #if choose == '1':
    #    return(line_1[:4],line_1[4],math.degrees(line_1[5]))
    #else:
    #    return(line_2[:4],line_2[4],math.degrees(line_2[5]))
            
    # if not line_2 == []:    
    #     ctr_x1 = round((line_1[0] + line_2[0])/2)
    #     ctr_y1 = round((line_1[1] + line_2[1])/2)
    #     ctr_x2 = round((line_1[2] + line_2[2])/2)
    #     ctr_y2 = round((line_1[3] + line_2[3])/2)
    #     #cv2.line(img,(ctr_x1,ctr_y1),(ctr_x2,ctr_y2),(0,0,255),2)
    #     #cv2.imshow('hough_lines',img)
    #     #cv2.waitKey(5000)
    #     return([ctr_x1,ctr_y1,ctr_x2,ctr_y2],line_1[4],math.degrees(line_1[5])) 
    # else:
    #     #cv2.line(img,(line_1[0],line_1[1]),(line_1[2],line_1[3]),(0,0,255),2)  
    #     #cv2.imshow('hough_lines',img)
    #     #cv2.waitKey(5000)
    #     return(line_1[:4],line_1[4],math.degrees(line_1[5]))

def get_dist(hough_rho, img):
    height,width = img.shape[:2]
    x_of_robot = width/2
    x_of_line = abs(hough_rho)
    # positive if robot is to left of line, negative if right of line
    print('robot: ' + str(x_of_robot))
    print('line: ' + str(x_of_line))
    print(x_of_line - x_of_robot)
    return(x_of_line - x_of_robot)

def move_to_orange(transform):
    orange = True
    while orange:
        found_perpendicular = False
        print("moving forward to orange")
        mr.move_forward()
        print("turning right 3 degrees to adjust")
        mr.turn_right_degrees(10)
        mr.turn_left_degrees(7)
        ci.capture_img(camera)
        img = cv2.imread('current_image.jpg')
        new_hom = transform_img(img, transform)
        black_and_white = b_and_w(new_hom)
        edges = canny_lines(black_and_white)
        lines = cv2.HoughLines(edges, 1, np.pi/90, 40)
        if not lines == None:
            for line in lines:
                line = line[0]
                rho = line[0]
                theta = line[1]
                if(rho > 0 and math.degrees(theta) > 70 and math.degrees(theta) < 110):
                    found_perpendicular = True
                    break

        if not found_perpendicular:
            print("didn't find orange")
            orange = False
    return


def main():
    global img
    global clicks
    global camera

    camera = PiCamera()

    enable_encoders()


    clicks = list()
    turned = -1
    #img = cv2.imread('calibration_image.jpg')
    ci.capture_img(camera)
    img = cv2.imread('current_image.jpg')
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.setMouseCallback('image', mouse_callback) 
    
    cv2.imshow("image",img)
    key = cv2.waitKey(0) & 0xFF

    if key == ord('c'):
        if len(clicks) == 4:
            im_hom,transform = homography(img, np.array(clicks))
            ci.capture_img(camera)

            while True:
                new_img = cv2.imread('current_image.jpg')
            
                # code with the homography cropping
            
                new_hom = transform_img(new_img, transform)
    
                black_and_white = b_and_w(new_hom)
                edges = canny_lines(black_and_white)
                #cv2.imshow("bandw",black_and_white)
                #cv2.waitKey(5000)

                # cv2.imshow("test",black_and_white)
                #cv2.waitKey(0)

                hough_coords, hough_rho, hough_angle, orange = hough(edges, new_hom)
                if orange:
                    print("saw orange")
                    move_to_orange(transform)
                    print("U-turn")
                    mr.left_uturn()

                else:
                    retry = 0
                    while hough_coords == None and retry < 4:
                        print("lost the hough lines, trying new boundaries...")
                        time.sleep(0.5)
                        if turned == 0:
                            mr.turn_right_degrees(6)
                        if turned == 1:
                            mr.turn_left_degrees(6)

                        black_and_white = b_and_w(new_hom, yellow_bounds=[[0,50,150],[60,255,255]])
                        edges = canny_lines(black_and_white)
                        hough_coords, hough_rho, hough_angle, orange = hough(edges, new_hom)
                        retry += 1

                    # if(hough_coords == None): #again
                    #     print("couldn't find hough lines. exiting")
                    #     return #exit

                    print("hough angle: " + str(hough_angle))
                    print("hough rho: " + str(hough_rho))

                    cv2.line(new_hom,(hough_coords[0],hough_coords[1]),(hough_coords[2],hough_coords[3]),(0,0,255),2)   
                    #cv2.imshow('hough_lines',new_hom)
                    #cv2.waitKey(5000)
                    #return

                    if (hough_rho > 0 and hough_angle > 10 and hough_angle < 88):
                        turn_angle = hough_angle
                        print("turn " + str(turn_angle) + " degrees right")
                        if turn_angle < 6:
                            mr.turn_right_degrees(turn_angle + 6)
                            mr.turn_left_degrees(6)
                        else:
                            mr.turn_right_degrees(turn_angle)
                        turned = 1
                    elif (hough_rho > 0 and hough_angle > 90) or (hough_rho < 0 and hough_angle > 92 and hough_angle < 178):
                        turn_angle = 180 - hough_angle
                        print("turn " + str(turn_angle) + " degrees left")
                        if turn_angle < 6:
                            mr.turn_left_degrees(turn_angle + 6)
                            mr.turn_right_degrees(6)
                        else:
                            mr.turn_left_degrees(turn_angle)
                        turned = 0
                    else:
                        print("parallel")
                        dist = get_dist(hough_rho, new_hom)
                        if(dist < -300):
                            mr.move_left_to_line(dist)
                            print("move left to line")
                            turned = 0
                        elif(dist > 300):
                            mr.move_right_to_line(dist)
                            print("move right to line")
                            turned = 1
                        else:   
                            mr.move_forward()   
        
                ci.capture_img(camera)
main()

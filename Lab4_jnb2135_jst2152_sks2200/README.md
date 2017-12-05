#Lab 4
###Group 12 [jnb2135, jst2152, sks2200]
###Youtube link: https://youtu.be/gAadmgO2Q78

You can find our main in lane_follower.py and helper functions in lane_follower.py, capture_img.py, move_robot.py
We made the following assumptions about our robot/environment: 
-the robot will never be perpendicular to the yellow line
-the yellow line will always be in the robot's range of view

##Values calculated from ta_supplied_image_set:
calculated_angle_offset = 20.0000046545 degrees
Since rho is positive and theta = 159.99999534548672 degrees, this is a left turn by 180 - 159.99999534548672 degrees 
calculated_distance_offset = 222.5 pixels
NOTE: our code works to find the calculated distance offset ONLY after we turn the robot parallel to the line. So this value is pretty meaningless since the robot is at an angle.
homography_transform_matrix = 
[[ -3.55543822e+01  -4.92913026e+01   6.44019151e+03]
 [  1.81983461e+00  -1.62875198e+02   1.25714175e+04]
 [ -2.07807273e-03  -1.42646478e-01   1.00000000e+00]]
distance_to_camera_from_homography = 13.5 cm

##Values calculated from student_captured_image_set
calculated_angle_offset = 33.99999866940647 degrees
Since rho is positive and theta = 33.99999866940647 degrees, this is a right turn by ~34 degrees
calculated_distance_offset = 312.5 pixels
NOTE: our code works to find the calculated distance offset ONLY after we turn the robot parallel to the line. So this value is pretty meaningless since the robot is at an angle.
homography_transform_matrix = 
[[ 7.68763101+00  9.71832599e+00   -8.33745340e+02]
 [  1.84015205e+00  3.29387216e+01   -1.17916943e+03]
 [ 1.92453148e-03  3.13002122e-02   1.00000000e+00]]
distance_to_camera_from_homography = 36 cm

##Questions:
1) Describe the overall architecture of your implementation.
(algorithm is described in more detail in part 3)
We have a file called lane_follower.py which has a main function that executes all the image capturing and processing in a loop. This function calls multiple helper functions in the same file that perform actions such as filtering by color, getting the homography transform, etc. This function also calls a function in another file, capture_img.py to take pictures. This function also calls functions in a file called move_robot.py that handles the actual robot's turning and moving. 

2) What method did your group use to calculate the distance from the center line?
See get_dist() in lane_follower.py
***We first aligned the robot parallel to the yellow line*** using the angle of the hough line (the theta that cv2.HoughLines() spits out). Next, with the yellow line parallel, we got the hough line's rho (this is also just spit out by cv2.HoughLines()). Since rho is the distance from the origin (image upper left corner) to the yellow line and since the yellow line is exactly vertical, rho is thus equal to the distance from the lefthand side of the image to the yellow line. We know that the robot is also facing vertical, as it took the image. We also know that the robot's position is always the width of the image divided by 2. So we have the yellow line's distance from the lefthand side of the image as well as the robot's distance from the lefthand side of the image (both in pixels). We could thus find the distance between them simply by subtraction.

3) What method did your group use to calculate the angle offset from the center line?
We used the angle (theta) returned by the cv2.HoughLines() function. This theta is sort of tricky because if rho is positive, we had to turn the robot by 180-theta, whereas if rho is positive, we turned the robot by theta.

4) Describe your control flow algorithm based on distance, angle, and whatever other metrics you used.
First a note: we did orange detection differently than what was suggested. We found that in the track room, since the tape is extremely reflective, some angles reflect light such that the yellow tape reflects essentially white, and the orange tape reflects essentially a light yellow. Thus, there was no way (we found) for us to really define boundaries to differentiate between orange and yellow since we needed to make the yellow boundary range large enough to capture both true yellow and this weird white reflected color. So we did something different. We made the assumption that in the demo, the TA's wouldn't be harsh enough (hehe) to start the robot in a direction perpendicular to the yellow line. So this is what we did:
-if the robot captures an image with both the yellow line and the orange line in it, we assume the orange will be approximately perpendicular to the robot. So, we get all the hough lines from the image. This gives us a few approx. vertical hough lines (from the yellow line) and a few approx. horizontal hough lines (from the orange line). We then note that the orange is in our field of view. We continue moving forward and checking that we see horizontal hough lines (aka orange). If we no longer see horizontal hough lines (orange is out of field of view), we know that we are close to the orange line and thus we do our U-turn. 
-In a perfect world, we could just pick a pixel at roughly the bottom of the image field of view and if it's orange, we know we are close to the orange line and do a U-turn. However, the lighting really screwed everything up so we chose to go this route, although we did make a bunch of assumptions. The rest of the algorithm is as follows:

-robot gets homography transform matrix using a 30x22.5 cm rectangle
(user clicks 4 points and then the letter 'c')

on repeat:
-robot takes image and saves as HSV
-robot takes HSV image and turns it to black and white, looking between specific yellow boundaries as defined in the code. Robot gets contours and fills them to make blobs of white, and only returns the blobs that are larger than a certain area. This removes noise.
-robot gets canny lines from the black and white image
-robot calculates all hough lines
-if there are horizontal hough lines then start checking for when they can no longer be detected -- then we do the U-turn
-if there are only vertical hough lines, then choose a line and get its theta
	-if it's outside a certain threshold, rotate the robot by theta
	-now the robot should be parallel
	-get the distance from the yellow line to the robot using the hough line's rho
		-if the distance is greater than a certain threshold, rotate the robot 90 degrees to face the line, move the robot forward by this distance, and then rotate it back parallel by 90 degrees


5) What is the purpose of the distance offset from the camera to the homography transform?
So, we actually didn't implement the robot to need this, since we align it parallel to the line first and we also do a different orange line detection implementation than what was suggested -- but we still completely understand what was supposed to be done. When calculating the distance between the robot and the yellow line, in other implementations, usually the robot is not necessarily parallel to the line. The image the robot takes is a bit in front of the robot, just because of the camera angle. Thus, when we do the homography transform, the distance between the bottom middle of the image and the bottom coordinate of the yellow line is NOT reflective of the actual distance to the robot. Instead, we could have applied the homography transform to the robot's actual position (using the distance offset). Then we could extend the yellow line hough line down to the robot's actual y position to calculate the distance between them.

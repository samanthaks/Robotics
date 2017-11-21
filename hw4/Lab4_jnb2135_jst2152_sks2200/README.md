#Lab 4
###Group 12 [jnb2135, jst2152, sks2200]
###Youtube link: <url>

You can find our main in lane_follower.py and helper functions in <list of .py files>
We made the following assumptions about our robot/environment: <assumptions>

##Values calculated from ta_supplied_image_set:
calculated_angle_offset = <angle_offset>
calculated_distance_offset = <distance_offset in cm>
homography_transform_matrix = <matrix>
distance_to_camera_from_homography = <distance in cm>

##Values calculated from student_captured_image_set
calculated_angle_offset = <angle_offset>
calculated_distance_offset = <distance_offset in cm>
homography_transform_matrix = <matrix>
distance_to_camera_from_homography = <distance in cm>

##Questions:
1) Describe the overall architecture of your implementation.


2) What method did your group use to calculate the distance from the center line?
We first aligned the robot parallel to the yellow line. From the hough lines rho, we obtained the horizontal distance from the left hand side of the image to the yellow line. We knew the robot's position was the width of the image/2. We then calculated the distance using these values to find the pixel distance.

3) What method did your group use to calculate the angle offset from the center line?
We used the angle returned by the cv2.HoughLines() function.

4) Describe your control flow algorithm based on distance, angle, and whatever other metrics you used.


5) What is the purpose of the distance offset from the camera to the homography transform?

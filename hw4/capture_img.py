import cv2
import numpy as np
import time
from picamera import PiCamera
import io 
from gopigo import *

def capture_img():
	stream = io.BytesIO()
	camera = PiCamera()
    camera.resolution = (320, 240)
    time.sleep(2)
    camera.capture(stream, format='jpeg')
    buff = np.fromstring(stream.getvalue(), dtype=np.uint8)
    image = cv2.imdecode(buff, 1)
    cv2.imwrite("image.jpg", image)

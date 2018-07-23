from picamera.array import PiRGBArray
from picamera import PiCamera
import logging
import utils.rpi_logging as rpi_logging
import numpy as np
import time
import cv2

'''This script continuously saves captured image to a given folder.
'''

CAMERA_RESOLUTION = (640, 480)
CAMERA_FRAME_RATE = 2
SAVE_EVERY_FRAME = 4

MAX_SAVED_FRAMES_NUM = 3
IMAGE_FOLDER = '/tmp/'

rpi_logging.config_logging(logging.DEBUG)

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = CAMERA_RESOLUTION
camera.framerate = CAMERA_FRAME_RATE
rawCapture = PiRGBArray(camera, size=CAMERA_RESOLUTION)

# allow the camera to warmup
time.sleep(0.1)

frame_cnt = 0
saved_frame_cnt = 0

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image
  image = frame.array

  if frame_cnt % SAVE_EVERY_FRAME == 0:
    # use timestamp in milliseconds as file name
    image_name = IMAGE_FOLDER + str(int(time.time()*1000)) + '.jpg'
    cv2.imwrite(image_name, image)
    saved_frame_cnt += 1
    logging.info('saved image to %s', image_name)

  # clear the stream in preparation for the next frame
  rawCapture.truncate(0)
  
  frame_cnt += 1
  
  if saved_frame_cnt == MAX_SAVED_FRAMES_NUM:
    break

logging.info('%d captured images are saved to %s', saved_frame_cnt, IMAGE_FOLDER)

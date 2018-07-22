# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import logging
import numpy as np
import time
import cv2

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 2
rawCapture = PiRGBArray(camera, size=(640, 480))

FOREGROUND_INTENSITY = 255
MIN_FOREGROUND_PIXEL_NUM = 50
LEARNING_RATE = -1
HISTORY=100

# kernel to filter noise
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))

# allow the camera to warmup
time.sleep(0.1)

# a background subtractor based on MoG models
fgbg = cv2.BackgroundSubtractorMOG(history=HISTORY, nmixtures=5, backgroundRatio=0.7)

# warm up background subtractor
WARMUP_FRAMES = 20
frame_cnt = 0
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
  image = frame.array

	# show the frame
  # cv2.imshow("Frame", image)
  fgmask = fgbg.apply(image, learningRate=LEARNING_RATE)
  frame_cnt += 1
  # clear the stream in preparation for the next frame
  rawCapture.truncate(0)
  if frame_cnt == WARMUP_FRAMES:
    logging.warn('warm up of background subtractor finished')
    break

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
  image = frame.array

	# show the frame
  # cv2.imshow("Frame", image)
  fgmask = fgbg.apply(image, learningRate=LEARNING_RATE)
  
  cv2.imshow("Foreground", fgmask)
  # print 'shape:', fgmask.shape
  # background will be masked by 0 (black), foreground is 255 (white)
  # print 'values:', fgmask[0][0:10] 
  
  filtered = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
  
  occ = np.where(filtered == FOREGROUND_INTENSITY)
  if len(occ[0]) > MIN_FOREGROUND_PIXEL_NUM:
    cv2.rectangle(image,(occ[1].min(),occ[0].min()),(occ[1].max(),occ[0].max()),(0,0,255),2)
    # event time in milliseconds
    event_time = int(time.time()*1000)
    logging.warn('event detected at timestamp (in ms) %d', event_time)
    cv2.imwrite('cv_images/' + str(event_time) + ".jpg", image)

  
  # contours, hierarchy = cv2.findContours(filtered, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  # cv2.drawContours(filtered, contours, -1, 255, 3)
  
  # cv2.imshow('Filtered', filtered)
  
  #if len(contours) > 0:
  #  for count in contours:
  #    x,y,w,h = cv2.boundingRect(count)
  #    cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
      
  cv2.imshow("Frame", image)
  
  key = cv2.waitKey(1) & 0xFF
  
  # clear the stream in preparation for the next frame
  rawCapture.truncate(0)

	# if the `q` key was pressed, break from the loop
  if key == ord("q"):
		break

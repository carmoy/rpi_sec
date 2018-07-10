#!/usr/bin/python

import argparse
import logging
import usb_capturer
import object_detector
import simple_reporter

LOGGING_FORMAT = '%(asctime)s,%(msecs)d %(levelname)-5s ' \
'[%(filename)s:%(lineno)d] %(message)s'
DATE_FORMAT = '%d-%m-%Y:%H:%M:%S'

DEFAULT_CAPTURED_IMAGE_PATH = 'test_data/captured_image.jpg'

def main():
  # command line flags
  parser = argparse.ArgumentParser()
  parser.add_argument("--log_to_file", 
  help="a file name that log messages are saved to", type=str)
  args = parser.parse_args()
  
  # Configures logging string format. Example:
  # 07-07-2018:19:27:18,701 ERROR [run_security_monitor.py:13] error_msg
  # Note that tensorflow logging messages have their own format.
  if args.log_to_file:
    logging.basicConfig(filename=args.log_to_file, \
    format=LOGGING_FORMAT, datefmt=DATE_FORMAT, \
    level=logging.DEBUG)
  else:
    logging.basicConfig(format=LOGGING_FORMAT, datefmt=DATE_FORMAT, \
    level=logging.DEBUG)
  
  # initialization
  capturer = usb_capturer.UsbCapturer()
  detector = object_detector.ObjectDetector()
  reporter = simple_reporter.SimpleReporter()

  while True:
    try:
      capturer.capture(DEFAULT_CAPTURED_IMAGE_PATH)
      res, image_np = detector.run_inference_for_single_image(DEFAULT_CAPTURED_IMAGE_PATH)
      reporter.update_detection_result(res, image_np)
    except:
      logging.error('Exception happens. Exit the main loop')
      break

if __name__ == "__main__":
  main()

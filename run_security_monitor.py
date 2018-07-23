#!/usr/bin/python

import argparse
import utils.rpi_logging as rpi_logging
import logging
import usb_capturer
import object_detector
import simple_reporter

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
    rpi_logging.config_logging_to_file(args.log_to_file, logging.DEBUG)
  else:
    rpi_logging.config_logging(logging.DEBUG)
  
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
      logging.exception('Exception happens. Exit the main loop')
      break


if __name__ == "__main__":
  main()

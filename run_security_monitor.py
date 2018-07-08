#!/usr/bin/python

import logging
import usb_capturer
import object_detector

LOGGING_FORMAT = '%(asctime)s,%(msecs)d %(levelname)-5s ' \
'[%(filename)s:%(lineno)d] %(message)s'
DATE_FORMAT = '%d-%m-%Y:%H:%M:%S'

def main():
  # Configures logging string format. Example:
  # 07-07-2018:19:27:18,701 ERROR [run_security_monitor.py:13] error_msg
  # Note that tensorflow logging messages have their own format.
  logging.basicConfig(format=LOGGING_FORMAT, datefmt=DATE_FORMAT, \
  level=logging.DEBUG)
  
  #capturer = usb_capturer.UsbCapturer()
  #capturer.capture('test.image')
  logging.error('test error')
  # logger.warning('test warning')
  detector = object_detector.ObjectDetector()

if __name__ == "__main__":
  main()

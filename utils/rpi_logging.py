import logging

# Configures logging string format. Example:
# 07-07-2018:19:27:18,701 ERROR [run_security_monitor.py:13] error_msg
LOGGING_FORMAT = '%(asctime)s,%(msecs)d %(levelname)-5s ' \
'[%(filename)s:%(lineno)d] %(message)s'

DATE_FORMAT = '%d-%m-%Y:%H:%M:%S'

def config_logging_to_file(log_file_name, log_level):
  '''log_level can be logging.DEBUG, logging.INFO, etc.
  '''
  logging.basicConfig(filename=log_file_name, format=LOGGING_FORMAT, \
  datefmt=DATE_FORMAT, level=log_level)
  
def config_logging(log_level):
  '''log_level can be logging.DEBUG, logging.INFO, etc.
  '''
  logging.basicConfig(format=LOGGING_FORMAT, datefmt=DATE_FORMAT, \
  level=log_level)
  

if __name__ == "__main__":
  # testing logging format
  
  # config_logging(logging.INFO)
  # logging.warn('this is a warning message')
  
  config_logging_to_file('/tmp/test_log.txt', logging.INFO)
  logging.error('this is an error message')

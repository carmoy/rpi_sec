import datetime
import time

def timestamp_to_datetime_str(ts, format_str):
  '''Converts a timestamp value to a string representation of date time.
  Args:
    ts: timestamp value
    format_str: a string to show the format of date time
  '''
  return datetime.datetime.fromtimestamp(ts).strftime(format_str)

def datetime_str_to_timestamp(datetime_str, format_str):
  '''Converts a date time string to a timestamp, assuming that the datetime is
  in the local time zone.
  '''
  return time.mktime(datetime.datetime.strptime(datetime_str, \
  format_str).timetuple())
  

if __name__=='__main__':
  datetime_format = '%Y-%m-%d %H:%M:%S'
  motion_format = '%Y%m%d%H%M%S'
  # some test code  
  # 2018-07-15 00:44:32
  print timestamp_to_datetime_str(1531640672, datetime_format)  
  # 20180715004432
  print timestamp_to_datetime_str(1531640672, motion_format)  
  # 1531640672
  print datetime_str_to_timestamp('20180715004432', motion_format)

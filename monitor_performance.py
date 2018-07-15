from utils import monitor_cpu
from utils import monitor_memory
import csv
import datetime
import logging
import time

FILE_NAME_TEMPLATE = 'test_data/perf-{suffix}.csv'
DATETIME_FORMAT='%Y-%m-%d-%H-%M-%S'

# column names of the csv file
TIMESTAMP = 'timestamp'
CPU_USAGE = 'cpu_usage'
MEM_USAGE = 'mem_usage'

if __name__=='__main__':
  # save the performance result to a csv file
  suffix_str=datetime.datetime.now().strftime(DATETIME_FORMAT)
  file_name = FILE_NAME_TEMPLATE.format(suffix=suffix_str)
  # check cpu and memory usage and then sleep
  sleep_time = 1
  
  cpu_monitor = monitor_cpu.GetCpuLoad()
  logging.warn('%s is created', file_name)
  csv_file = open(file_name, 'w')
  csv_writer = csv.DictWriter(csv_file, 
  fieldnames=[TIMESTAMP, CPU_USAGE, MEM_USAGE])
  csv_writer.writeheader()
  
  # refresh the last cpu time recorded in the cpu monitor
  cpu_monitor.get_aggregate_cpu_load()
  while True:
    try:
      time.sleep(sleep_time)
      
      one_entry = {TIMESTAMP:time.time(), 
      CPU_USAGE:cpu_monitor.get_aggregate_cpu_load(), 
      MEM_USAGE: monitor_memory.get_memory_usage()}
      csv_writer.writerow(one_entry)
    except KeyboardInterrupt:
      csv_file.close()
      logging.warn('%s is closed', file_name)
      sys.exit("Finished")  

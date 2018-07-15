import os
import time
import logging

'''Based on https://askubuntu.com/questions/9642/how-can-i-monitor-the-memory-usage
'''

def get_memory_usage():
  mem=os.popen('free ').readlines()
  """ Output of free in Raspbian is like:
                total        used        free      shared  buff/cache   available
  Mem:         896800      295936      273744       38612      327120      510260
  Swap:        102396       86904       15492

  Memory usage is defined as used_Mem/total_Mem
  """
  logging.debug(str(mem))
  tokens = mem[1].split()
  return float(tokens[2])/float(tokens[1])

if __name__=='__main__':
  while True:
    try:
      time.sleep(1)
      print get_memory_usage()
    except KeyboardInterrupt:
      sys.exit("Finished")  

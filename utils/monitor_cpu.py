#!/usr/bin/python 
# -*- coding: utf-8 -*-

'''
Copied from https://stackoverflow.com/questions/23367857/accurate-calculation-of-cpu-usage-given-in-percentage-in-linux
with some changes

Created on 04.12.2014

@author: plagtag
'''
from time import sleep
import sys
import logging

class GetCpuLoad(object):
  '''
  classdocs
  '''


  def __init__(self):
    '''
    @parent class: GetCpuLoad
    @date: 04.12.2014
    @author: plagtag
    @info: 
    '''
    #self.percentage = percentage
    self.cpustat = '/proc/stat'
    self.sep = ' ' 
    self._last_cpu_time = self.getcputime()
    logging.info('Initial CPU time: %s', str(self._last_cpu_time))

  def getcputime(self):
    '''
    http://stackoverflow.com/questions/23367857/accurate-calculation-of-cpu-usage-given-in-percentage-in-linux
    read in cpu information from file
    The meanings of the columns are as follows, from left to right:
        0cpuid: number of cpu
        1user: normal processes executing in user mode
        2nice: niced processes executing in user mode
        3system: processes executing in kernel mode
        4idle: twiddling thumbs
        5iowait: waiting for I/O to complete
        6irq: servicing interrupts
        7softirq: servicing softirqs

    #the formulas from htop 
         user    nice   system  idle      iowait irq   softirq  steal  guest  guest_nice
    cpu  74608   2520   24433   1117073   6176   4054  0        0      0      0


    Idle=idle+iowait
    NonIdle=user+nice+system+irq+softirq+steal
    Total=Idle+NonIdle # first line of file for all cpus

    CPU_Percentage=((Total-PrevTotal)-(Idle-PrevIdle))/(Total-PrevTotal)
    '''
    cpu_infos = {} #collect here the information
    with open(self.cpustat,'r') as f_stat:
      lines = [line.split(self.sep) for content in f_stat.readlines() for line in content.split('\n') if line.startswith('cpu')]

      #compute for every cpu
      for cpu_line in lines:
        if '' in cpu_line: cpu_line.remove('')#remove empty elements
        cpu_line = [cpu_line[0]]+[float(i) for i in cpu_line[1:]]#type casting
        cpu_id,user,nice,system,idle,iowait,irq,softrig,steal,guest,guest_nice = cpu_line

        Idle=idle+iowait
        NonIdle=user+nice+system+irq+softrig+steal

        Total=Idle+NonIdle
        #update dictionionary
        cpu_infos.update({cpu_id:{'total':Total,'idle':Idle}})
        
    logging.debug('Get CPU time: %s', str(cpu_infos))
    return cpu_infos

  def getcpuload(self):
    '''
    CPU_Percentage=((Total-PrevTotal)-(Idle-PrevIdle))/(Total-PrevTotal)
    
    Returns:
      a dictionary of cpu load. Key is cpu name, and value is the cpu
      load between 0 - 1. The value is the average CPU load between the
      previous call and this call.
    '''    
    current_cpu_time = self.getcputime()

    cpu_load = {}

    for cpu in current_cpu_time:
      Total = current_cpu_time[cpu]['total']
      PrevTotal = self._last_cpu_time[cpu]['total']

      Idle = current_cpu_time[cpu]['idle']
      PrevIdle = self._last_cpu_time[cpu]['idle']
      CPU_Percentage = 0
      if Total != PrevTotal:
        CPU_Percentage=((Total-PrevTotal)-(Idle-PrevIdle))/(Total-PrevTotal)
      cpu_load.update({cpu: CPU_Percentage})
    
    # update stored cpu time
    self._last_cpu_time = current_cpu_time
    
    logging.debug('CPU load: %s', str(cpu_load))
    
    return cpu_load
    
  def get_aggregate_cpu_load(self):
    '''Returns aggregate cpu load between the previous call and this
    call.
    '''
    return self.getcpuload()['cpu']


if __name__=='__main__':
  x = GetCpuLoad()
  while True:
    try:
      logging.info('Aggregate CPU load: %f', x.get_aggregate_cpu_load())
      sleep(1)
    except KeyboardInterrupt:
      sys.exit("Finished")  

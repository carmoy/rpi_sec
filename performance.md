
<img src="figs/perf-2018-07-15.jpg" alt="Usage and Events" width="1000px"/>

The above figure shows the CPU and memry usages for over 17 hours while Motion was running and saving detected events. The configuration of Motion is [here](motion_configs/motion-2018-07-15.conf). Note that `output_pictures` is set to `best` which is more CPU intensive compared to other modes.

Both CPU and memory usage are within reasonable range. 

Memory usage is pretty flat. 

While a lot of events were detected, CPU usage increases a little bit (compare the CPU usage before hour 9 and after hour 9). The Pi Camera is not IR camera, so before sunrise (hour 6), it barely captures anything , so its CPU usage is lower compared to after hour 6.

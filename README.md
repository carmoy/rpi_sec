# Hardware

## Raspberry Pi

I bought a CanaKit Raspberry Pi 3 B+ (B Plus) Complete Starter Kit (16 GB Edition, Premium Clear Case) from [Amazon](https://www.amazon.com/gp/product/B07BLRSKBV/). However later I found there are better buying options on Amazon since not all pieces in the complete starter kit are useful. Its spec are listed in the following table

|   |   |
---|---
CPU           | quad-core, 1.4GHz 
RAM           | 1GB               
Storage       | 16G Micro-SD  

One can run commands such as `cat /proc/meminfo`, `free -m`, `gpio -v`, `df -h` and etc. to check the hardware specs. Note that `Hardware` in the output of `cpuinfo` is always `BCM2835` for different RPI boards. The `Revision` number (mine is `a020d3`) is useful to determin the version of the board.

I installed the board in the case, and connected it with a mouse, a keyboard, and a monitor.

I powered it on, and installed the OS that is preloaded in the micro SD card that comes with the starter kit.


<img src="figs/pi_box.jpg" alt="Pi box in case" width="250px"/>

## USB Webcam

I bought a [Logitech C270 webcam](https://www.amazon.com/dp/B004FHO5Y6). The Raspberry Pi board has four USB ports, and I connected the webcam to one of them.

```
$ lsusb
...
Bus 001 Device 005: ID 046d:0825 Logitech, Inc. Webcam C270
...
```

`fswebcam` package can be used to manage the webcam. To install it, run:

```
sudo apt-get install fswebcam
```

The following command will use the webcam to take a picture and save it as the specified file name. See `man fsweb` for more options.

```
fswebcam image.jpg
```

### Failure in the 2nd attempt to access the webcam

My Raspberry Pi ran into a problem: when I tried to take a second picture after a couple of minutes since I took the first picture, `fswebcam` failed to open the webcam device and says the device is busy. See [here](https://raspberrypi.stackexchange.com/questions/76971/fswebcam-every-other-attempt-results-in-device-busy) for more discussion.

 I found the solution [here](https://www.raspberrypi.org/forums/viewtopic.php?f=28&t=197089) works for me: it was fixed by appending `dwc_otg.fiq_fsm_mask=0x3` to `/boot/cmdline.txt`, and then rebooting Raspberry Pi.

## Costs

|Item|Cost|From|
---|---|---
Raspberry Starter Kit |$69.99      | [Amazon](https://www.amazon.com/gp/product/B07BLRSKBV/) 
Logitech C270 Webcam  |$19.99      | Fry's                

# Software

## Tensorflow

1. I installed Tensorflow by following [Pete Warden's post](https://petewarden.com/2017/08/). The most receint successful build,    `tensorflow-1.9.0rc0-cp27` was picked (as of 07/2018).

   ```
   sudo apt-get install libblas-dev liblapack-dev python-dev \
   libatlas-base-dev gfortran python-setuptools
   sudo pip2 install \
   http://ci.tensorflow.org/view/Nightly/job/nightly-pi/304/artifact/output-artifacts/tensorflow-1.9.0rc0-cp27-none-      linux_armv7l.whl
   ```

2. Then I installed [Tensorflow Object Detection Api](https://github.com/tensorflow/models/tree/master/research/object_detection). My installation is adapted from their [installation instruction](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/installation.md).

* First install dependencies. Note that `--no-cache-dir` is used to avoid memory error when installing matplotlib.

     ```
     sudo apt-get install protobuf-compiler python-pil python-lxml python-tk
     pip install --user Cython
     pip install --user contextlib2
     pip install --user jupyter
     pip install --no-cache-dir --user matplotlib
     ```
     
 * Then install Thensorflow Object Detection Api.
 
   ```
   $ mkdir tensorflow && cd tensorflow/
   tensorflow$ git clone https://github.com/tensorflow/models.git
   tensorflow$ cd models/research/
   tensorflow/models/research$ protoc object_detection/protos/*.proto --python_out=.
   # ls object_detection/protos/ show that python files are compiled from proto files.
   ```
 
   Then add the path to `PYTHONPATH`. In `~/.bashrc`, append the following line:
 
   ```
   export PYTHONPATH=$PYTHONPATH:<absolute path of tensorflow/models/research/>:\
                     <absolute path of tensorflow/models/research/>/slim
   ```
 * Finally, test the installation:
 
   ```
   $ python tensorflow/models/research/object_detection/builders/model_builder_test.py
   ...............
   ----------------------------------------------------------------------
   Ran 15 tests in 0.772s

   OK

   ```
 
   One can also run [object_detection_tutorial](object_detection_tutorial.ipynb) to learn how to use the object detection api.

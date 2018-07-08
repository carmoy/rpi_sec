import subprocess
import logging

DEFAULT_DEVICE = 'v4l2:/dev/video0'
DEFAULT_INPUT_ID = '0'
DEFAULT_RESOLUTION = '1280x960'

# example command:
# fswebcam -d v4l2:/dev/video0 -i 0 -r 1280x960 --no-banner image.jpg
FSWEBCAM_TEMPLATE = 'fswebcam -d {device} -i {input_id}' + \
' -r {resolution} --no-banner {file_path}'

def run_command(cmd_args):
  p = subprocess.Popen(cmd_args, stdout=subprocess.PIPE, \
  stderr=subprocess.PIPE)
  retval = p.wait()
  out, err = p.communicate()
  return retval, out, err


"""This class is a wrapper of fswebcam.
"""

class UsbCapturer:
  def __init__(self):
    #TODO: might need add a rotation parameter here, since the detector
    # module does not accept rotated pictures 
    self._device = DEFAULT_DEVICE
    self._input_id = DEFAULT_INPUT_ID
    self._resolution = DEFAULT_RESOLUTION
    
  def capture(self, file_path):
    """Calls fswebcam to take a picture, and save it to the given file 
    path.
    
    Args:
      file_path: the file path to save the captured picture.
      
    Returns:
      True if a file is successfully saved to the given path. False if
      otherwise. Error messages are logged.
    """
    command = FSWEBCAM_TEMPLATE.format(device = self._device, \
    input_id = self._input_id, resolution = self._resolution, \
    file_path = file_path)
    logging.info(command)
    retval, _, err = run_command(command.split())
    if retval != 0:
      logging.error(err)
      return False
    else:
      logging.info('Captured image is successfully saved to %s.', \
      file_path)
      return True

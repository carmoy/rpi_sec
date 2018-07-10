import logging
import time
import os
from PIL import Image
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util

DEFAULT_LABEL_PATH = 'test_data/data/mscoco_label_map.pbtxt'
DEFAULT_NUM_CLASSES = 90
DEFAULT_DETECTION_RESULTS_DIR = 'detection_results'

# helper function to log detection result
def log_detection_result(result):
  logging.info('%d object(s) are detected.', result['num_detections'])

class SimpleReporter:
  def __init__(self):
    self._detection_results_dir = DEFAULT_DETECTION_RESULTS_DIR
    self._last_detection_result = None
    
    self._label_path = DEFAULT_LABEL_PATH
    label_map = label_map_util.load_labelmap(self._label_path)
    categories = \
    label_map_util.convert_label_map_to_categories(label_map, \
    max_num_classes=DEFAULT_NUM_CLASSES, use_display_name=True)
    self._category_index = label_map_util.create_category_index(categories)
    logging.info('labels from %s is loaded.', self._label_path)
    
  def update_detection_result(self, detection_result, image_np):
    '''If changes are found in the given detection result. Updates the
    last detection result with the given one and visualize it.
    '''
    log_detection_result(detection_result)
    if self._detection_result_changed(detection_result):
      self._last_detection_result = detection_result
      logging.info('last detection result is updated.')
      self._visualize_detection(image_np)
      
    
  def _detection_result_changed(self, detection_result):
    '''Compares the given detection result to the last detection result
    saved by the reporter.
    A simple heuristic is used for comparison: compare the number of 
    objects detected.
    TODO: add a better heuristic
    '''
    if self._last_detection_result is None:
      logging.info('received with the first detection result.')
      return True
    if self._last_detection_result['num_detections'] != detection_result['num_detections']:
      logging.info('number of objects detected changed from %d to %d.', \
      self._last_detection_result['num_detections'], 
      detection_result['num_detections'])
      return True
    logging.info('No changes found in the given detection result'\
    ' compared to the last saved detection result.')
    return False
    
  def _visualize_detection(self, image_np):
    '''Visulize the last detection result on the given image.
    '''
    vis_util.visualize_boxes_and_labels_on_image_array(
        image_np,
        self._last_detection_result['detection_boxes'],
        self._last_detection_result['detection_classes'],
        self._last_detection_result['detection_scores'],
        self._category_index,
        instance_masks=self._last_detection_result.get('detection_masks'),
        use_normalized_coordinates=True,
        line_thickness=8,
        min_score_thresh=0.3)
    im = Image.fromarray(image_np)
    #TODO: might need to find a better way of naming
    image_path = os.path.join(self._detection_results_dir, \
    str(int(time.time())) + ".jpg")
    im.save(image_path)
    logging.info('visulized detection result is saved to %s.', image_path)
    

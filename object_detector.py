import logging
import tensorflow as tf

DEFAULT_MODEL_PATH = 'test_data/ssdlite_mobilenet_v2_coco_2018_05_09/' \
'frozen_inference_graph.pb'

class ObjectDetector:
  def __init__(self):    
    self._model_path = DEFAULT_MODEL_PATH
    
    self._detection_graph = tf.Graph()
    with self._detection_graph.as_default():
      od_graph_def = tf.GraphDef()
      with tf.gfile.GFile(self._model_path, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')
        
    logging.info('model %s is loaded into memory', self._model_path)

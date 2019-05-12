import os
import time
import shutil
import cv2
import numpy as np
import tensorflow as tf

from setting import *
from utils.image_libs import *

class object_model():
    def __init__(self, model_path):
        self.model_path = model_path
        self.detection_graph = tf.Graph()
        with self.detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(model_path, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')

        with self.detection_graph.as_default():
            self.tf_config = tf.ConfigProto(gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction = GPU_MEMORY_LIMIT), )
            self.session = tf.Session(graph = self.detection_graph, config = self.tf_config)
            self.image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')
            self.num_detections = self.detection_graph.get_tensor_by_name('num_detections:0')
            self.detection_boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')
            self.detection_scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
            self.detection_classes = self.detection_graph.get_tensor_by_name('detection_classes:0')

    def interface(self, image_np):
        (boxes, scores, label_id, num) = self.session.run(
            [self.detection_boxes, self.detection_scores, self.detection_classes, self.num_detections],
            feed_dict = {
                self.image_tensor: image_np[np.newaxis, :, :, :]
            },
        )

        label_dict = label_handle(self.model_path.rsplit('/', 1)[0])
        return boxes, scores, label_id, label_dict

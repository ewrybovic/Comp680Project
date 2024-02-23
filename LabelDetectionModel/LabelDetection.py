import os
import cv2

import tensorflow as tf
import numpy as np

from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
from object_detection.builders import model_builder
from object_detection.utils import config_util
import matplotlib.pyplot as plt

class LabelDetection:
    def __init__(self) -> None:
        
        self.PATH_TO_CFG =  "pipeline.config"
        self.PATH_TO_CKPT = "checkpoint\\ckpt-3"
        self.PATH_TO_LABELS = "label_map.pbtxt"
        self.category_index = label_map_util.create_category_index_from_labelmap(self.PATH_TO_LABELS,use_display_name=True)

        # Load pipeline config and build a detection model
        configs = config_util.get_configs_from_pipeline_file(self.PATH_TO_CFG)
        model_config = configs['model']
        self.detection_model = model_builder.build(model_config=model_config, is_training=False)

        # Restore checkpoint
        ckpt = tf.compat.v2.train.Checkpoint(model=self.detection_model)
        ckpt.restore(self.PATH_TO_CKPT).expect_partial()

    def detect_label(self, image):
        min_thresh = 0.4
        image, shapes = self.detection_model.preprocess(image)
        prediction_dict = self.detection_model.predict(image, shapes)
        detections = self.detection_model.postprocess(prediction_dict, shapes)

        num_detections = int(detections.pop('num_detections'))
        detections = {key: value[0, :num_detections].numpy()
                    for key, value in detections.items()}
        detections['num_detections'] = num_detections

        # detection_classes should be ints.
        detections['detection_classes'] = detections['detection_classes'].astype(np.int64)

        label_id_offset = 1
        image_np_with_detections = image_np.copy()

        viz_utils.visualize_boxes_and_labels_on_image_array(
                    image_np_with_detections,
                    detections['detection_boxes'],
                    detections['detection_classes']+label_id_offset,
                    detections['detection_scores'],
                    self.category_index,
                    use_normalized_coordinates=True,
                    max_boxes_to_draw=5,
                    min_score_thresh=min_thresh,
                    agnostic_mode=False)

        plt.imshow(cv2.cvtColor(image_np_with_detections, cv2.COLOR_BGR2RGB))
        plt.show()
        plt.savefig("image_np_with_detections")

        for x in range(len(detections['detection_scores'])):
            if detections['detection_scores'][x] >=min_thresh:
                print(detections['detection_scores'][x])
                print(detections['detection_boxes'][x])
        

if __name__ == '__main__':
    wrapper = LabelDetection()

    image_path = "test-images\\IMG_1133.jpg"
    image_np = np.array(cv2.imread(image_path))

    input_tensor = tf.convert_to_tensor(np.expand_dims(image_np, 0), dtype=tf.float32)

    wrapper.detect_label(input_tensor)
    
    print('Done')

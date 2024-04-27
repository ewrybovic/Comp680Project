import os
import cv2

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

from pathlib import Path
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
from object_detection.builders import model_builder
from object_detection.utils import config_util

class LabelDetection:
    def __init__(self, PATH_TO_CFG: str, PATH_TO_CKPT: str, PATH_TO_LABELS: str) -> None:

        self.category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS,use_display_name=True)

        # Load pipeline config and build a detection model
        configs = config_util.get_configs_from_pipeline_file(PATH_TO_CFG)
        model_config = configs['model']
        self.detection_model = model_builder.build(model_config=model_config, is_training=False)

        # Restore checkpoint
        ckpt = tf.compat.v2.train.Checkpoint(model=self.detection_model)
        ckpt.restore(PATH_TO_CKPT).expect_partial()
    
    def preprocess_image(self, image):
        # Convert to tensor
        image_tensor = np.float32(image)
        image_tensor = np.expand_dims(image_tensor, 0)
        image_tensor = tf.convert_to_tensor(image_tensor)

        return image_tensor
    
    def crop_image(self, image, box):
        print(box)
        x1 = int(box[0] * image.shape[0])
        y1 = int(box[1] * image.shape[1])

        x2 = int(box[2] * image.shape[0])
        y2 = int(box[3] * image.shape[1])

        return image[x1:x2, y1:y2]

    def detect_label(self, image, debug = False):
        min_thresh = 0.1
        top_score = 0
        top_boxes = []

        # process the input image and convert to tensor
        input_tensor = self.preprocess_image(image)

        input_tensor, shapes = self.detection_model.preprocess(input_tensor)
        prediction_dict = self.detection_model.predict(input_tensor, shapes)
        detections = self.detection_model.postprocess(prediction_dict, shapes)

        num_detections = int(detections.pop('num_detections'))
        detections = {key: value[0, :num_detections].numpy()
                    for key, value in detections.items()}
        detections['num_detections'] = num_detections

        # detection_classes should be ints.
        detections['detection_classes'] = detections['detection_classes'].astype(np.int64)

        # detections are ordered from greatest to least, so we only care about the first one
        if len(detections['detection_scores']) > 0 and detections['detection_scores'][0] >=min_thresh:
            top_score = detections['detection_scores'][0]
            top_boxes = detections['detection_boxes'][0]

        print(top_score)
        print(top_boxes)
        print(len(top_boxes))

        cropped_image = None
        if len(top_boxes) != 0:
            cropped_image = self.crop_image(image, top_boxes)

        if debug:
            label_id_offset = 1
            image_np_with_detections = image.copy()

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
            plt.savefig("image_np_with_detections")

            if len(cropped_image) > 0:
                cv2.imwrite("cropped_image.jpg", cropped_image)

        return cropped_image
        
if __name__ == '__main__':
    CFG = Path(Path.cwd(), "pipeline.config")
    CKPT = Path(Path.cwd(), "checkpoint", "ckpt-3")
    LABELS = Path(Path.cwd(), "label_map.pbtxt")

    wrapper = LabelDetection(CFG, CKPT, LABELS)

    image_path = str(Path.cwd() / "test-images" / "butter.jpg")
    image = cv2.imread(image_path)

    detected_label = wrapper.detect_label(image, debug=True)
    cv2.imwrite("cropped_image.jpg", detected_label)

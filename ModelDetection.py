import os
import tensorflow as tf
import numpy as np
from PIL import Image
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
from object_detection.builders import model_builder
from object_detection.utils import config_util
import matplotlib.pyplot as plt

class ModelDetection:
    def __init__(self) -> None:
        
        self.PATH_TO_MODEL_DIR = "training\\model\\"
        self.PATH_TO_CFG = self.PATH_TO_MODEL_DIR + "pipeline.config"
        self.PATH_TO_CKPT = self.PATH_TO_MODEL_DIR + "checkpoint\\ckpt-3"
        self.PATH_TO_LABELS = self.PATH_TO_MODEL_DIR + "..\\annotations\\label_map.pbtxt"
        self.category_index = label_map_util.create_category_index_from_labelmap(self.PATH_TO_LABELS,use_display_name=True)

        # Load pipeline config and build a detection model
        configs = config_util.get_configs_from_pipeline_file(self.PATH_TO_CFG)
        model_config = configs['model']
        self.detection_model = model_builder.build(model_config=model_config, is_training=False)

        # Restore checkpoint
        ckpt = tf.compat.v2.train.Checkpoint(model=self.detection_model)
        ckpt.restore(self.PATH_TO_CKPT).expect_partial()

    def detect_label(self, image):
        image, shapes = self.detection_model.preprocess(image)
        prediction_dict = self.detection_model.predict(image, shapes)
        detections = self.detection_model.postprocess(prediction_dict, shapes)

        num_detections = int(detections.pop('num_detections'))
        print("Num detections: " + str(num_detections))


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
                max_boxes_to_draw=200,
                min_score_thresh=.30,
                agnostic_mode=False)

        plt.figure()
        plt.imshow(image_np_with_detections)
        plt.savefig("image_np_with_detections")

if __name__ == '__main__':
    wrapper = ModelDetection()

    image_path = "training\\images\\eval-images\\label-12.jpg"
    image_np = np.array(Image.open(image_path))

    input_tensor = tf.convert_to_tensor(np.expand_dims(image_np, 0), dtype=tf.float32)

    wrapper.detect_label(input_tensor)
    
    print('Done')

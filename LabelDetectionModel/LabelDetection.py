import os.path
import cv2

import tensorflow as tf
import numpy as np

import matplotlib.pyplot as plt

from PIL import Image, ImageDraw

class LabelDetection:
    def __init__(self) -> None:

        self.interpreter = tf.lite.Interpreter(model_path=os.path.join("tflite-model", "model.tflite"))
        self.interpreter.allocate_tensors()

        self.input_details = self.interpreter.get_input_details()

    def detect_label(self, image):
        min_thresh = 0.3

        # Check image size
        image_resize = self.resize_image(image, False)

        image_tensor = np.float32(image_resize)
        image_tensor = np.expand_dims(image_tensor, 0)
        
        self.interpreter.set_tensor(self.input_details[0]['index'], image_tensor)

        self.interpreter.invoke()

        scores = self.get_output_tensor(0)
        boxes = self.get_output_tensor(1)
        count = int(self.get_output_tensor(2))

        results = []
        for i in range(count):
            if scores[i] >= min_thresh:
                result = {
                    'bounding_box': boxes[i],
                    'score': scores[i]
                }
                results.append(result)

        print(results)

        image = self.draw_bounding_box(image, results)

        cv2.imwrite("image_detections.jpg", image)
        

    def get_output_tensor(self, index):
        output_details = self.interpreter.get_output_details()[index]
        tensor = np.squeeze(self.interpreter.get_tensor(output_details['index']))
        return tensor

    def convert_to_tensor(self, image):
        image_np = np.array(image)
        return tf.convert_to_tensor(np.expand_dims(image_np, 0), dtype=tf.float32)

    def resize_image(self, image, set_borders):
        size = image.shape
        vertical_border = 0
        horizontal_border = 0
        print(size)
        
        if size[0] != 640 or size[1] != 640:
            
            if set_borders:
                # Check if horizontal or vertical bar is needed to be added by checking apect ratio(640x640 is 1 aspect ratio)
                if 1 >= size[0]/size[1]:
                    vertical_border = int((size[1]-size[0])/2)
                else:
                    horizontal_border = int((size[0]-size[1])/2)

                # Add border to image to get it to corerct aspect ratio 
                image = cv2.copyMakeBorder(image, vertical_border, vertical_border, horizontal_border, horizontal_border, cv2.BORDER_CONSTANT)

            image = cv2.resize(image, (640,640), interpolation=cv2.INTER_LINEAR)

        return image
        
    def draw_bounding_box(self, image, results):
        (height, width, _) = image.shape

        for result in results:
            bounding_box = result['bounding_box']
            score = str(result['score'])

            y1, x1, y2, x2 = bounding_box

            # to not draw the bounding box out of frame
            x1 = int(max(1, x1*width))
            x2 = int(min(width, x2*width))
            y1 = int(max(1, y1*height))
            y2 = int(min(height, y2*height))

            print((x1, y1))
            print((x2, y2))

            cv2.rectangle(image, (x1,y1), (x2,y2), (255,0,0), 10)
            cv2.putText(image, score, (x1, min(y1, height-20)), cv2.FONT_HERSHEY_SIMPLEX, 3,(0,0,255),5,cv2.LINE_AA)

        return image

if __name__ == '__main__':
    wrapper = LabelDetection()

    #image_path = "test-images\\IMG_1133.jpg"
    #image_np = np.array(cv2.imread(image_path))

    #input_tensor = tf.convert_to_tensor(np.expand_dims(image_np, 0), dtype=tf.float32)
    image = cv2.imread("test-images\\IMG_1133.jpg")
    wrapper.detect_label(image)
    
    print('Done')

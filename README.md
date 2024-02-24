# Comp680Project

Required Libraries
    OpenCV: pip install opencv-python
    Tensorflow: pip install tensorflow(If on windows, you need python 3.11)

To label training images:
    pip install labelImg
    to run open cmd and run labelImg. Currently there is an error that you need to fix manually. I used this video to fix it:https://www.youtube.com/watch?v=5jHPuwo8z1o

Tensorflow Object model used:
    To install the object detection api: https://tensorflow-object-detection-api-tutorial.readthedocs.io/en/latest/install.html

    https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/tf2_detection_zoo.md
    using: SSD MobileNet v2 320x320 (http://download.tensorflow.org/models/object_detection/tf2/20200711/ssd_mobilenet_v2_320x320_coco17_tpu-8.tar.gz)

    This model compresses the image to 320x320, has a good balance between speed and accuracy
    need numpy 1.17.4

To run the LabelDetection with TFLite
    Download the TFLite file from google drive: https://drive.google.com/file/d/1pClM18mbNuFsA36tdubX2K8nFdC_x9ph/view?usp=drive_link
    Put data into LabelDetectionModel\tflite-model
    
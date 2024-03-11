import cv2
import numpy

from pathlib import Path
from PIL import Image
from pytesseract import pytesseract
from enum import Enum

class OperatingSystem(Enum):
    WINDOWS = 1
    MAC = 2

class LabelReader:
    def __init__(self, operating_system: OperatingSystem) -> None:
        if operating_system == OperatingSystem.WINDOWS:
            # Point to the executable
            path_to_exe = 'D:\\Program Files\\Tesseract-OCR\\tesseract.exe'
            pytesseract.tesseract_cmd = path_to_exe

    def process_text(self, text: str) -> dict:
        text = text.splitlines()
        label_data = {
            "Calories": 0,
            "Total Fat": 0,
            "Saturated Fat": 0,
            "Trans Fat": 0,
            "Polyunsaturated Fat": 0,
            "Sodium": 0,
            "Total Carbohydrate": 0,
            "Dietary Fiber": 0,
            "Total Sugars": 0,
            "Protein": 0
        }

        for line in text:
            print(line)

        return label_data

    def read_label(self, image, debug=False) -> dict:
        # Check if OpenCV image, convert to PIL
        if isinstance(image, numpy.ndarray):
            gry = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            thr = cv2.adaptiveThreshold(gry, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 15, 22)
            
            if debug:
                cv2.imwrite("processed_image.jpg", thr)

        label_data = self.process_text(pytesseract.image_to_string(thr))
        return label_data
    
    ''' TESTING THIS
    def keras_read_label(self, image, debug = False):
        
        import keras_ocr
        pipeline = keras_ocr.pipeline.Pipeline()

        # return list of (word, box)
        predition_groups = pipeline.recognize([image])

        for word,_ in predition_groups[0]:
            print(word)'''


if __name__ == '__main__':
    reader = LabelReader(OperatingSystem.WINDOWS)

    image_path = str(Path.cwd() / "test_image" / "croppped_image.jpg")
    image = cv2.imread(image_path)

    text = reader.read_label(image, debug=True)
    print(text)
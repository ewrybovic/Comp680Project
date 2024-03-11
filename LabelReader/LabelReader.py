import cv2
import numpy

from pathlib import Path
from PIL import Image
from pytesseract import pytesseract
from enum import Enum

class LabelReader:
    def __init__(self, is_Windows = False) -> None:
        if is_Windows:
            # Point to the executable
            path_to_exe = 'D:\\Program Files\\Tesseract-OCR\\tesseract.exe'
            pytesseract.tesseract_cmd = path_to_exe

    def process_text(self, text: str) -> dict:
        text = text.splitlines()
        label_data = {
            "Calories": -1,
            "Total Fat": -1,
            "Saturated Fat": -1,
            "Trans Fat": -1,
            "Polyunsaturated Fat": -1,
            "Sodium": -1,
            "Total Carbohydrate": -1,
            "Dietary Fiber": -1,
            "Total Sugars": -1,
            "Protein": -1
        }

        # This is so unoptimized, but I have a kid and a job lol
        for line in text:
            for key in label_data:
                if key in line:
                    split = line.split(" ")
                    num_words_in_key = len(key.split(" "))

                    # Remove the mg or g from string, also gets o and O confused with 0
                    value = int(split[num_words_in_key].replace('g','').replace('m','').replace('O','0'))
                    label_data[key] = value

        return label_data

    def read_label(self, image: numpy.ndarray, debug=False) -> dict:

        # Do some preprocessing
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        thr = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 15, 22)
        
        if debug:
            cv2.imwrite("processed_image.jpg", thr)

        label_data = self.process_text(pytesseract.image_to_string(thr))
        return label_data


if __name__ == '__main__':

    # The way pytesseract has to be installed in windows makes windows point to the exe, but not for MAC/Linux
    reader = LabelReader(is_Windows=True)

    image_path = str(Path.cwd() / "test_image" / "test_image.jpg")
    image = cv2.imread(image_path)

    text = reader.read_label(image, debug=True)
    print(text)
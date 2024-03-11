import cv2
import numpy

from pathlib import Path
from pytesseract import pytesseract

class LabelReader:
    def __init__(self, is_Windows = False) -> None:
        if is_Windows:
            # Point to the executable
            path_to_exe = 'D:\\Program Files\\Tesseract-OCR\\tesseract.exe'
            pytesseract.tesseract_cmd = path_to_exe

    def process_text(self, text: str) -> dict:
        text = text.splitlines()
        label_data = {}

        items_to_find = ["Calories",
            "Total Fat",
            "Saturated Fat",
            "Trans Fat",
            "Polyunsaturated Fat",
            "Sodium",
            "Total Carbohydrate",
            "Dietary Fiber"
            "Total Sugars",
            "Protein"]

        # This is so unoptimized, but I have a kid and a job lol
        for line in text:
            for item in items_to_find:
                if item in line:
                    split = line.split(" ")
                    num_words_in_item = len(item.split(" "))

                    # Remove the mg or g from string, also gets o and O confused with 0
                    value = int(split[num_words_in_item].replace('g','').replace('m','').replace('O','0'))
                    label_data[item] = value

                    # Remove found entry from the list
                    items_to_find.remove(item)

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
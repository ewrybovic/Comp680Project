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
        text = text.lower().splitlines()
        print(text)
        label_data = {}

        items_to_find = ["calories",
            "total fat",
            "saturated fat",
            "trans fat",
            "polyunsaturated fat",
            "monounsaturated fat",
            "cholesterol",
            "sodium",
            "total carbohydrate",
            "dietary fiber",
            "total sugars",
            "protein"]

        # This is so unoptimized, but I have a kid and a job lol
        for line in text:
            for item in items_to_find:
                if item in line:

                    print("Found: ", item, " in ", line)

                    try:
                        # Replace og and omg to 0g and 0mg
                        line = line.replace('og', '0g').replace('omg', '0mg')

                        split = line.split(" ")
                        num_words_in_item = len(item.split(" "))

                        # Remove the mg or g from string, also gets o and O confused with 0
                        value = int(split[num_words_in_item].replace('g','').replace('m','').replace('O','0'))
                        label_data[item] = value

                        # Remove found entry from the list
                        items_to_find.remove(item)
                    except:
                        print("Error parsing " , item)

        return label_data

    def read_label(self, image: numpy.ndarray, debug=False) -> dict:

        # Do some preprocessing, #TODO add sharpening
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        thr = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)
        
        if debug:
            cv2.imwrite("processed_image.jpg", thr)

        label_data = self.process_text(pytesseract.image_to_string(image))
        print(label_data)
        return label_data


if __name__ == '__main__':

    # The way pytesseract has to be installed in windows makes windows point to the exe, but not for MAC/Linux
    reader = LabelReader(is_Windows=True)

    image_path = str(Path.cwd() / "test_image" / "test_image.jpg")
    image = cv2.imread(image_path)

    text = reader.read_label(image, debug=True)
    print(text)
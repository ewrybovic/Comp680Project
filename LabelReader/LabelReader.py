import cv2
import numpy
import re

from pathlib import Path
from pytesseract import pytesseract

class LabelReader:
    def __init__(self, path_to_superres_model: str, is_Windows = False) -> None:
        if is_Windows:
            # Point to the executable
            path_to_exe = 'D:\\Program Files\\Tesseract-OCR\\tesseract.exe'
            pytesseract.tesseract_cmd = path_to_exe
        
        print("Loading OpenCV SuperRes model")

        # Load the SuperResoultion model for opencv
        self.superres = cv2.dnn_superres.DnnSuperResImpl.create()
        self.superres.readModel(path_to_superres_model)
        self.superres.setModel('espcn', 3)

        print("Model loaded")

    def process_text(self, text: str) -> dict:
        text = text.lower().splitlines()
        print(text)
        label_data = {}

        items_to_find = ["calories",
            "total fat",
            "saturated fat",
            "saturatod fat",
            "trans fat",
            "polyunsaturated fat",
            "monounsaturated fat",
            "cholesterol",
            "sodium",
            "total carbohydrate",
            "total carbohydrato",
            "dietary fiber",
            "total sugars",
            "protein",
            "protoin"] # PyTesseract gets this confused sometimes

        # This is so unoptimized, but I have a kid and a job lol
        for _, line in enumerate(text):
            # Clean the string to only include alphanumeric, % and spaces.
            line = re.sub(r'[^a-zA-Z0-9%. ]', '', line)

            # Remove the trailing space
            line = line.rstrip()

            for item in items_to_find:
                if item in line:
                    print(f"Found: {item} in \"{line}\"")

                    # PyTesseract can think the e is an o
                    if item is "protoin":
                        item = "protein"
                    elif item is "total carbohydrato":
                        item = "total carbohydrate"
                    elif item is "saturatod fat":
                        item = "saturated fat"

                    try:
                        # Replace og and omg to 0g and 0mg
                        line = line.replace('og', '0g').replace('omg', '0mg')

                        split = line.split(" ")
                        num_words_in_item = len(line.split(" "))

                        # don't want the % Daily value, want the grams/miligrams
                        if '%' in line:
                            str_amount = split[num_words_in_item - 2]
                        else: 
                            str_amount = split[num_words_in_item - 1]

                        # Pytesseract will sometimes confuse the letter 9 with g so to solve
                        # If no g is found in string but a 9 is found, replace the 9 with g
                        if 'g' not in str_amount and '9' in str_amount:
                            str_amount = str_amount.replace('9', 'g')
                        
                        # PYtesseract will sometimes not read the space (ie if its "Fat 7g" it can sometimes be read as "Fat7g" so I remove all letters except g
                        str_amount = re.sub(r'[^g\d.]', '', str_amount)

                        print(str_amount)

                        # Remove the mg or g from string, also gets o and O confused with 0
                        value = float(str_amount.replace('g','').replace('m','').replace('O','0'))
                        label_data[item] = value

                        # Remove found entry from the list
                        items_to_find.remove(item)
                    except Exception as e:
                        print("Error parsing " , item)
                        print(e)

        return label_data

    def read_label(self, image: numpy.ndarray, upres=True, sharpen=True, threshold=True, debug=False) -> dict:
        # Sharpen image
        if sharpen:
            kernel = numpy.array([[0,-1,0], [-1,5,-1], [0,-1,-0]])
            image = cv2.filter2D(image, -1, kernel)

        # Super res the image
        if upres:
            print("Supersampling the image")
            image = self.superres.upsample(image)
            print("Done supersampling")

        # Do some preprocessing
        if threshold:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            #(_, image) = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

        if debug:
            cv2.imwrite("processed_image.jpg", image)

        label_data = self.process_text(pytesseract.image_to_string(image))
        print(label_data)
        return label_data
    
if __name__ == '__main__':

    # The way pytesseract has to be installed in windows makes windows point to the exe, but not for MAC/Linux
    reader = LabelReader(path_to_superres_model="ESPCN_x3.pb",is_Windows=True)

    image_path = str(Path.cwd() / "test_image" / "cropped_image.jpg")
    label_img = cv2.imread(image_path)

    text = reader.read_label(label_img, upres=True,sharpen=True, threshold=True, debug=True)
    print(text)
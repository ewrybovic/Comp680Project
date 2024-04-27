import cv2
import numpy

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
                        num_words_in_item = len(split)
                        str_amount = split[num_words_in_item]

                        # Pytesseract will sometimes confuse the letter 9 with g so to solve
                        # If no g is found in string but a 9 is found, replace the 9 with g
                        if 'g' not in str_amount and '9' in str_amount:
                            str_amount = str_amount.replace('9', 'g')
                        
                        print(str_amount)

                        # Remove the mg or g from string, also gets o and O confused with 0
                        value = int(str_amount.replace('g','').replace('m','').replace('O','0'))
                        label_data[item] = value

                        # Remove found entry from the list
                        items_to_find.remove(item)
                    except:
                        print("Error parsing " , item)

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
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            image = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)

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

    text = reader.read_label(label_img, upres=True,sharpen=True, threshold=False, debug=True)
    print(text)
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

    def read_label(self, image) -> dict:
        # Check if OpenCV image, convert to PIL
        if isinstance(image, numpy.ndarray):
            color_coverted = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(color_coverted)

        label_data = self.process_text(pytesseract.image_to_string(image))
        return label_data

    def test_read_label(self, img):
        # Convert the image to gray scale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Performing OTSU threshold
        ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
        
        # Specify structure shape and kernel size. 
        # Kernel size increases or decreases the area 
        # of the rectangle to be detected.
        # A smaller value like (10, 10) will detect 
        # each word instead of a sentence.
        rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))
        
        # Applying dilation on the threshold image
        dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1)
        
        # Finding contours
        contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, 
                                                        cv2.CHAIN_APPROX_NONE)
        
        # Creating a copy of image
        im2 = img.copy()
        
        
        # Looping through the identified contours
        # Then rectangular part is cropped and passed on
        # to pytesseract for extracting text from it
        # Extracted text is then written into the text file
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            
            # Drawing a rectangle on copied image
            rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # Cropping the text block for giving input to OCR
            cropped = im2[y:y + h, x:x + w]
            
            # Open the file in append mode
            file = open("recognized.txt", "a")
            
            # Apply OCR on the cropped image
            print(pytesseract.image_to_string(cropped)) 

if __name__ == '__main__':
    reader = LabelReader(OperatingSystem.WINDOWS)

    image_path = str(Path.cwd() / "test_image" / "test_image.png")
    image = cv2.imread(image_path)

    text = reader.test_read_label(image)
    print(text)
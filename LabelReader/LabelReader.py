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

    def read_label(self, image) -> str:
        # Check if OpenCV image, convert to PIL
        if isinstance(image, numpy.ndarray):
            color_coverted = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(color_coverted)

        return pytesseract.image_to_string(image)

if __name__ == '__main__':
    reader = LabelReader(OperatingSystem.WINDOWS)

    image_path = str(Path.cwd() / "test_image" / "test_image.png")
    image = cv2.imread(image_path)

    text = reader.read_label(image)
    print(text)
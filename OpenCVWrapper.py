import os
import cv2 as cv

class OpenCVWrapper:
    def __init__(self) -> None:
        pass

    # This will open file locations to cv images, will change when we get the file fron the client
    def openimage(self, img):
        cv_img = cv.imread(img)
        print (cv_img.nbytes)


if __name__ == '__main__':
    wrapper = OpenCVWrapper()
    wrapper.openimage(os.getcwd() + '\\test-images\\powder.jpg')

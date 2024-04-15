from threading import Thread
import cv2
import numpy as np


def adjust_gamma(image, gamma=1.0):
    invGamma = 1.0 / gamma
    table = np.array([
      ((i / 255.0) ** invGamma) * 255
      for i in np.arange(0, 256)])
    return cv2.LUT(image.astype(np.uint8), table.astype(np.uint8))


class VideoGet:
    """
    Class that continuously gets frames from a VideoCapture object
    with a dedicated thread.
    """

    def __init__(self, src=0, gamma=1.0):
        self.stream = cv2.VideoCapture(src)
        self.gamma = gamma
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False

    def start(self):
        Thread(target=self.get, args=()).start()
        return self

    def get(self):
        while not self.stopped:
            if not self.grabbed:
                self.stop()
            else:
                (self.grabbed, image) = self.stream.read()
                self.frame = adjust_gamma(image, gamma=self.gamma)

    def stop(self):
        self.stopped = True

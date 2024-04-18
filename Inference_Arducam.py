from threading import Thread
import tensorflow
import cv2  # used to capture data from the webcam
from cvzone.HandTrackingModule import HandDetector  # pre-build ML model for Hand Tracking
from cvzone.ClassificationModule import Classifier
import numpy as np
import math
import time
import tensorflow as tf

detector = HandDetector(maxHands=1)
detector2 = HandDetector(maxHands=1)
synth_classifier = Classifier("SynthModeModels/Lens_Keras/keras_model.h5", "SynthModeModels/Lens_Keras/labels.txt")
chord_classifier = Classifier("ChordModeModels/Lens_Keras/keras_model.h5", "ChordModeModels/Lens_Keras/labels.txt")

# constants
offset = 20
imgSize = 300


class Inference:

    def __init__(self, frame=None):
        self.frame = frame
        self.stopped = False
        self.prediction = None
        self.index = 9
        self.framerate = 0
        self.synth_mode = True

    def start(self):
        Thread(target=self.inference, args=()).start()
        return self

    def inference(self):
        start_time = time.time()
        x = 0.25  # displays the frame rate every 1 second
        counter = 0

        while not self.stopped:
            try:
                # read webcam data and find any hands detected within it
                image = self.frame
                hands, img = detector.findHands(image, draw=False)
                if hands:
                    # assign a variable to our detected hand and get its dimensions
                    hand0 = hands[0]
                    x0, y0, w0, h0 = hand0['bbox']

                    offset_height = int(h0 * 0.15)
                    offset_width = int(w0 * 0.15)
                    img_cropped = img[y0 - offset_height:y0 + h0 + offset_height, x0 - offset_width: x0 + w0 + offset_width]
                    imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255

                    # find the aspect ratio of the image to determine how to resize
                    aspectRatio = h0 / w0

                    # resize the image based on the height, then center it on top of the background
                    if aspectRatio > 1:
                        k = imgSize / h0
                        w0cal = math.ceil(k * w0)
                        imgResize = cv2.resize(img_cropped, (w0cal, imgSize))
                    # resize the image based on the width, then center it on top of the background
                    else:
                        k = imgSize / w0
                        h0cal = math.ceil(k * h0)
                        imgResize = cv2.resize(img_cropped, (imgSize, h0cal))

                    hands, imgResize = detector2.findHands(imgResize, draw=True)
                    if hands:
                        hand0 = hands[0]
                        x0, y0, w0, h0 = hand0['bbox']

                        # find the aspect ratio of the image to determine how to resize
                        aspectRatio = h0 / w0

                        # resize the image based on the height, then center it on top of the background
                        if aspectRatio > 1:
                            k = imgSize / h0
                            w0cal = math.ceil(k * w0)
                            imgResize = cv2.resize(imgResize, (w0cal, imgSize))
                            imgResizeShape = imgResize.shape
                            wGap = math.ceil((imgSize - w0cal) / 2)
                            imgWhite[:, wGap:w0cal + wGap] = imgResize
                        # resize the image based on the width, then center it on top of the background
                        else:
                            k = imgSize / w0
                            h0cal = math.ceil(k * h0)
                            imgResize = cv2.resize(imgResize, (imgSize, h0cal))
                            imgResizeShape = imgResize.shape
                            hGap = math.ceil((imgSize - h0cal) / 2)
                            imgWhite[hGap:h0cal + hGap, :] = imgResize

                        if self.synth_mode is True:
                            self.prediction, self.index = synth_classifier.getPrediction(imgWhite)
                        else:
                            self.prediction, self.index = chord_classifier.getPrediction(imgWhite)
                    else:
                        self.prediction = None
                        self.index = 9
                else:
                    self.prediction = None
                    self.index = 9

                counter += 1
                if (time.time() - start_time) > x:
                    self.framerate = round(counter / (time.time() - start_time), 2)
                    counter = 0
                    start_time = time.time()

            except Exception as e:
                self.prediction = None
                self.index = 9
                print(e)

    def stop(self):
        self.stopped = True
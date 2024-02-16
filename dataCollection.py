import cv2  # used to capture data from the webcam
from cvzone.HandTrackingModule import HandDetector  # pre-build ML model for Hand Tracking
import numpy as np
import math
import time

# assigns a variable for our webcam output and a variable for our hand detector
cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)

# constants
offset = 20
imgSize = 300

folder = "Data/Octave"
counter = 0

while True:
    # read webcam data and find any hands detected within it
    success, img = cap.read()
    hands, img = detector.findHands(img)

    if hands:
        # assign a variable to our detected hand and get its dimensions
        hand0 = hands[0]
        x0, y0, w0, h0 = hand0['bbox']

        # create a cropped image displaying just the hand (plus an offset), and the background white screen
        imgCrop0 = img[y0 - offset:y0 + h0 + offset, x0 - offset: x0 + w0 + offset]
        imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255

        # find the aspect ratio of the image to determine how to resize
        aspectRatio = h0 / w0

        # resize the image based on the height, then center it on top of the background
        if aspectRatio > 1:
            k = imgSize / h0
            w0cal = math.ceil(k * w0)
            imgResize = cv2.resize(imgCrop0, (w0cal, imgSize))
            imgResizeShape = imgResize.shape
            wGap = math.ceil((imgSize - w0cal) / 2)
            imgWhite[:, wGap:w0cal + wGap] = imgResize
        # resize the image based on the width, then center it on top of the background
        else:
            k = imgSize / w0
            h0cal = math.ceil(k * h0)
            imgResize = cv2.resize(imgCrop0, (imgSize, h0cal))
            imgResizeShape = imgResize.shape
            hGap = math.ceil((imgSize - h0cal) / 2)
            imgWhite[hGap:h0cal + hGap, :] = imgResize

        cv2.imshow("ImageCrop0", imgCrop0)
        cv2.imshow("ImageWhite", imgWhite)

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == ord("s"):
        counter += 1
        cv2.imwrite(f'{folder}/Image_{time.time()}.jpg', imgWhite)
        print(counter)

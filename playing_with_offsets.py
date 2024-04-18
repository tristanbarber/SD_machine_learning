import cv2  # used to capture data from the webcam
from cvzone.HandTrackingModule import HandDetector  # pre-build ML model for Hand Tracking
import numpy as np
import math
import time
from PIL import Image


def adjust_gamma(image, gamma=1.0):
    invGamma = 1.0 / gamma
    table = np.array([
      ((i / 255.0) ** invGamma) * 255
      for i in np.arange(0, 256)])
    return cv2.LUT(image.astype(np.uint8), table.astype(np.uint8))


# assigns a variable for our webcam output and a variable for our hand detector
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 3840)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160)
detector = HandDetector(maxHands=1)
detector2 = HandDetector(maxHands=1)

# constants
offset = 20
offset0 = 100
imgSize = 300

gamma_adjustment = 1.5

folder = "Data/7"
counter = 0

while True:
    try:
        # read webcam data and find any hands detected within it
        success, img = cap.read()
        img = cv2.resize(img, (1280, 720))
        img_copy = img
        img = adjust_gamma(img, gamma_adjustment)
        hands, img = detector.findHands(img, draw=False)

        if hands:
            # assign a variable to our detected hand and get its dimensions
            hand0 = hands[0]
            x0, y0, w0, h0 = hand0['bbox']

            offset_height = int(h0 * 0.15)
            offset_width = int(w0 * 0.15)
            img_cropped = img[y0 - offset_height:y0 + h0 + offset_height, x0 - offset_width: x0 + w0 + offset_width]

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

                imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255

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

                cv2.imshow("resized image", imgWhite)

        cv2.imshow("Original Image", img_copy)
        cv2.imshow("hand_image", img)
        key = cv2.waitKey(1)
        if key == ord("s"):
            counter += 1
            cv2.imwrite(f'{folder}/Image_{time.time()}.jpg', imgWhite)
            print(counter)

    except:
        pass

import cv2  # used to capture data from the webcam
from cvzone.HandTrackingModule import HandDetector  # pre-build ML model for Hand Tracking
from cvzone.ClassificationModule import Classifier
import numpy as np
import math
import time
import pygame
from Note import Note

pygame.init()
bits = 16
sample_rate = 44100
pygame.mixer.pre_init(sample_rate, bits, channels=2)

octave = 2
key_sig = 1
accidental = False
synth_mode = True

# assigns a variable for our webcam output and a variable for our hand detector
cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)
synth_classifier = Classifier("SynthModeModels/Keras/keras_model.h5", "SynthModeModels/Keras/labels.txt")
chord_classifier = Classifier("ChordModeModels/Keras/keras_model.h5", "ChordModeModels/Keras/labels.txt")

# constants
offset = 20
imgSize = 300

folder = "Data/Mode"
counter = 0

labels = ["A", "B", "C", "D", "E", "F", "G", "1", "2", "3", "4", "5", "6", "7", "KeySig", "Octave", "Mode",
          "Accidental", "Sustain"]

while True:
    # read webcam data and find any hands detected within it
    success, img = cap.read()
    imgOutput = img.copy()
    hands, img = detector.findHands(img)

    if hands:
        # assign a variable to our detected hand and get its dimensions
        hand0 = hands[0]
        x0, y0, w0, h0 = hand0['bbox']

        # create a cropped image displaying just the hand (plus an offset), and the background white screen
        # use imgOutput to get rid of skeleton artifacts from hand tracker
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

        if synth_mode == True:
            prediction, index = synth_classifier.getPrediction(imgWhite)
        else:
            prediction, index = chord_classifier.getPrediction(imgWhite)

        cv2.putText(imgOutput, labels[index], (x0, y0 - 20), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 2)

        # cv2.imshow("ImageCrop0", imgCrop0)
        # cv2.imshow("ImageWhite", imgWhite)

        if synth_mode == True:
            if index == 0 and prediction[0] > 0.8:
                Note('Bb' + str(octave)).play() if accidental else Note('A' + str(octave)).play()
                print("playing A or Bb")
            elif index == 1 and prediction[1] > 0.8:
                Note('Bb' + str(octave)).play() if accidental else Note('B' + str(octave)).play()
                print("playing B or Bb")
            elif index == 2 and prediction[2] > 0.8:
                Note('C#' + str(octave)).play() if accidental else Note('C' + str(octave)).play()
                print("playing C or C#")
            elif index == 3 and prediction[3] > 0.8:
                Note('Eb' + str(octave)).play() if accidental else Note('D' + str(octave)).play()
                print("playing D or Eb")
            elif index == 4 and prediction[4] > 0.8:
                Note('Eb' + str(octave)).play() if accidental else Note('E' + str(octave)).play()
                print("playing E or Eb")
            elif index == 5 and prediction[5] > 0.8:
                Note('F#' + str(octave)).play() if accidental else Note('F' + str(octave)).play()
                print("playing F or B#")
            elif index == 6 and prediction[6] > 0.8:
                Note('Ab' + str(octave)).play() if accidental else Note('G' + str(octave)).play()
                print("playing G or Ab")
            elif index == 7 and prediction[7] > 0.8:
                if octave == 7:
                    octave = 2
                else:
                    octave += 1
                print("octave = " + str(octave))
                time.sleep(2)
            elif index == 8 and prediction[8] > 0.8:
                accidental = ~accidental
                print("accidental = " + str(accidental))
                time.sleep(2)
        else:
            if index == 0 and prediction[0] > 0.8:
                note_array = [Note('C4'), Note('E4')]
                Note.play_chord(note_array)
            elif index == 1 and prediction[1] > 0.8:
                continue
            elif index == 2 and prediction[2] > 0.8:
                continue
            elif index == 3 and prediction[3] > 0.8:
                continue
            elif index == 4 and prediction[4] > 0.8:
                continue
            elif index == 5 and prediction[5] > 0.8:
                continue
            elif index == 6 and prediction[6] > 0.8:
                continue
            elif index == 7 and prediction[7] > 0.8:
                if key_sig == 12:
                    key_sig = 1
                else:
                    key_sig += 1
                print("octave = " + str(key_sig))
                time.sleep(2)

    cv2.imshow("Image", imgOutput)
    cv2.imshow("Image", img)

    key = cv2.waitKey(1)
    if key == ord("m"):
        synth_mode = ~synth_mode
        print(synth_mode)
        print("Mode switched")
    elif key == ord("q"):
        print("exiting")
        break





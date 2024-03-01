import cv2  # used to capture data from the webcam
from cvzone.HandTrackingModule import HandDetector  # pre-build ML model for Hand Tracking
from cvzone.ClassificationModule import Classifier
import numpy as np
import math
import time
import pygame
from Note import Note
from VideoGet import VideoGet
from VideoShow import VideoShow
from Inference import Inference
from threading import Thread


class SoundGen:

    def __init__(self, synth_mode=True, octave=2, accidental=False):
        self.synth_mode = synth_mode
        self.stopped = False
        self.prediction = None
        self.index = None
        self.octave = octave
        self.accidental = accidental

    def start(self):
        Thread(target=self.play_sound, args=()).start()
        return self

    def play_sound(self):

        while not self.stopped:
            if self.synth_mode:
                if self.index == 0 and self.prediction[0] > 0.8:
                    Note('Bb' + str(self.octave)).play() if self.accidental else Note('A' + str(self.octave)).play()
                    print("playing A or Bb")
                elif self.index == 1 and self.prediction[1] > 0.8:
                    Note('Bb' + str(self.octave)).play() if self.accidental else Note('B' + str(self.octave)).play()
                    print("playing B or Bb")
                elif self.index == 2 and self.prediction[2] > 0.8:
                    Note('C#' + str(self.octave)).play() if self.accidental else Note('C' + str(self.octave)).play()
                    print("playing C or C#")
                elif self.index == 3 and self.prediction[3] > 0.8:
                    Note('Eb' + str(self.octave)).play() if self.accidental else Note('D' + str(self.octave)).play()
                    print("playing D or Eb")
                elif self.index == 4 and self.prediction[4] > 0.8:
                    Note('Eb' + str(self.octave)).play() if self.accidental else Note('E' + str(self.octave)).play()
                    print("playing E or Eb")
                elif self.index == 5 and self.prediction[5] > 0.8:
                    Note('F#' + str(self.octave)).play() if self.accidental else Note('F' + str(self.octave)).play()
                    print("playing F or B#")
                elif self.index == 6 and self.prediction[6] > 0.8:
                    Note('Ab' + str(self.octave)).play() if self.accidental else Note('G' + str(self.octave)).play()
                    print("playing G or Ab")
                elif self.index == 7 and self.prediction[7] > 0.8:
                    if self.octave >= 7:
                        self.octave = 2
                    else:
                        self.octave += 1
                    print("octave = " + str(self.octave))
                    time.sleep(1)
                elif self.index == 8 and self.prediction[8] > 0.8:
                    self.accidental = ~self.accidental
                    print("accidental = " + str(self.accidental))
                    time.sleep(1)


        '''
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
        '''

    def stop(self):
        self.stopped = True


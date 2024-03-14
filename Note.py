from threading import Thread
from utils import NOTE_MAP
import pygame
import math
import numpy
import numpy as np

pygame.init()
bits = 16
sample_rate = 44100
pygame.mixer.pre_init(sample_rate, bits, channels=2)


def sine_x(amp, freq, t):
    return int(round(amp * math.sin(2 * math.pi * freq * t)))


class Note:
    def __init__(self, duration=1):
        self.duration = duration
        self.stopped = False
        self.sound = None
        self.volume = 1

    def start(self, note, volume):
        self.stopped = False

        main_note = note[0].upper()
        note = main_note + note[1:]
        frequency = NOTE_MAP[note]

        self.volume = volume

        print("Playing" + str(note))

        Thread(target=self.sine(frequency), args=()).start()

        return self

    def sine(self, frequency, duration=5):
        if self.sound is None and self.stopped is False:

            num_samples = int(round(duration * sample_rate))  # Get the sample rate

            amplitude = 2 ** (16 - 1) - 1  # Assuming 16-bit audio

            samples = numpy.zeros((num_samples, 2), dtype=np.int16)
            for s in range(num_samples):
                samples[s] = sine_x(amplitude, frequency, float(s) / sample_rate)

            self.sound = pygame.mixer.Sound(samples)
            self.sound.play(loops=-1)

            self.sound.set_volume(self.volume)

    def stop(self):
        self.stopped = True
        try:
            self.sound.stop()
            self.sound = None
        except Exception as e:
            pass
        # pygame.mixer.quit()

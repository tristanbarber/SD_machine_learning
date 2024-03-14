from threading import Thread
import math
import numpy
import numpy as np
import time
import pygame


def sine_x(amp, freq, t):
    return int(round(amp * math.sin(2 * math.pi * freq * t)))


class Tone:

    def __init__(self, frequency=0):
        self.frequency = frequency
        self.stopped = False
        self.sound = None

    def start(self):
        Thread(target=self.sine, args=()).start()
        return self

    def sine(self, duration=1):
        while not self.stopped:
            if self.sound is None:
                pygame.init()
                bits = 16
                sample_rate = 44100
                pygame.mixer.pre_init(sample_rate, bits, channels=2)

                num_samples = int(round(duration * sample_rate))  # Get the sample rate

                amplitude = 2 ** (16 - 1) - 1  # Assuming 16-bit audio

                samples = numpy.zeros((num_samples, 2), dtype=np.int16)
                for s in range(num_samples):
                    samples[s] = sine_x(amplitude, self.frequency, float(s) / sample_rate)

                self.sound = pygame.mixer.Sound(samples)
                self.sound.play(loops=-1)

    def stop(self):
        self.stopped = True
        pygame.mixer.quit()



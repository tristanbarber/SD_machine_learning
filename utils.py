from concurrent.futures import thread
import math
import numpy as np
import time
import pygame
from pygame.locals import *
import json

pygame.init()


def read_file(path):
    with open(path, 'r') as f:
        return f.read()


def read_json(path):
    return json.loads(read_file(path))


def get_note_map():
    return read_json('frequency_map.json')


def play_tone(frequency, sample_rate=44100, duration=1):

    bits = 16
    pygame.mixer.pre_init(sample_rate, bits, 2)

    num_samples = int(round(duration * sample_rate))  # Get the sample rate

    amplitude = 2 ** (16 - 1) - 1  # Assuming 16-bit audio

    samples = numpy.zeros((num_samples, 2), dtype=np.int16)
    for s in range(num_samples):
        samples[s] = sine_x(amplitude, frequency, float(s) / sample_rate)

    sound = pygame.mixer.Sound(samples)
    one_sec = 1000  # Milliseconds
    sound.play(loops=1, maxtime=int(duration * one_sec))
    time.sleep(duration)


NOTE_MAP = read_json('frequency_map.json')

import math
import numpy
import numpy as np
import time
import pygame


def sine_x(amp, freq, t):
    return int(round(amp * math.sin(2 * math.pi * freq * t)))


def sine(frequency, duration=1):
    pygame.init()
    bits = 16
    sample_rate = 44100
    pygame.mixer.pre_init(sample_rate, bits, channels=2)

    num_samples = int(round(duration * sample_rate))  # Get the sample rate

    amplitude = 2 ** (16 - 1) - 1  # Assuming 16-bit audio

    samples = numpy.zeros((num_samples, 2), dtype=np.int16)
    for s in range(num_samples):
        samples[s] = sine_x(amplitude, frequency, float(s) / sample_rate)

    sound = pygame.mixer.Sound(samples)
    one_sec = 1000  # Milliseconds
    sound.play(loops=1, maxtime=int(duration * one_sec))
    time.sleep(duration)


# Example usage
# tone = Tone()
# tone.sine(440, 10)

# Clean up
pygame.mixer.quit()



import numpy as np
import time
import pygame
import json

pygame.init()


def read_file(path):
    with open(path, 'r') as f:
        return f.read()


def read_json(path):
    return json.loads(read_file(path))


def get_note_map():
    return read_json('frequency_map.json')


NOTE_MAP = read_json('frequency_map.json')

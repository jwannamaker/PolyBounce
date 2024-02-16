'''
    _summary_: Utility function module for the hexkeys project.
'''

import os
import random
import pygame
import numpy as np
from pygame import Vector2

MAIN_DIR = os.path.split(os.path.abspath(__file__))[0]
DATA_DIR = os.path.join(MAIN_DIR, 'data')

SCREEN_SIZE = Vector2(1280, 720)
CENTER = Vector2(SCREEN_SIZE // 2)

GRAVITY = Vector2(0, 10)

RING_PADDING = 50
RING_SIDES = {
    'up_left', 
    'up', 
    'up_right', 
    'down_right', 
    'down', 
    'down_left'
}
RING_PALLETE = {
    'white': (250, 250, 250),
    'pink': (201, 93, 177),
    'light-purple': (137, 100, 187),
    'blue': (157, 169, 214),
    'light-blue': (170, 224, 241),
    'cyan': (144, 239, 240)
}

PALLETE = {
    'white': (255, 255, 255),
    'pink': (201, 93, 177),
    'light-purple': (137, 100, 187),
    'blue': (157, 169, 214),
    'light-blue': (170, 224, 241),
    'cyan': (144, 239, 240)
}
BACKGROUND_PALLETE = {
    'black': (10, 10, 10),
    'magenta': (129, 55, 113),
    'dark-purple': (63, 45, 112),
    'grey-blue': (83, 91, 113)
}

def load_font():
    font_file = os.path.join(DATA_DIR, 'Emulogic-zrEw.ttf')
    return pygame.font.Font(font_file, 12)

def rotate_vector(angle, x, y):
    '''
    After rotation the vector is noted by
    x' = x * cos(theta) - y * sin(theta)
    y' = x * sin(theta) + y * cos(theta)
    '''
    a = np.cos(angle)
    b = np.sin(angle)
    R = np.matrix((a, -b), (b, a))
    return np.matmul(((a, -b), (b, a)), (x, y))
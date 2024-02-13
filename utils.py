'''
    _summary_: Utility function module for the hexkeys project.
'''

import os
import pygame
import numpy as np

MAIN_DIR = os.path.split(os.path.abspath(__file__))[0]
DATA_DIR = os.path.join(MAIN_DIR, 'data')

SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
CENTER = np.array((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

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
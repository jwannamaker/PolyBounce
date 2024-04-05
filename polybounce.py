import random

import pygame
from pygame import Vector2

from game import Game
from scripts.ui import UI
from scripts.ball import Ball
from scripts.polygon import Polygon

class PolyBounceUI(UI):
    PALLETE = {
        'blue': (150, 170, 200),
        'cyan': (144, 239, 240),
        'drk-purple': (63, 45, 112),
        'lt-blue': (170, 224, 241),
        'lt-purple': (150, 100, 187),
        'magenta': (129, 55, 113),
        'mid-blue': (83, 91, 113),
        'pink': (201, 93, 177), 
        'red': (255, 100, 100),
        'white': (250, 250, 250)
    }
    
    def __init__(self):
        self.IMG_DIR = 'data/images/'
        self.FONT_DIR = 'data/fonts/'

        self.SCREEN_SIZE = Vector2(1280, 720)
        self.CENTER = Vector2(self.SCREEN_SIZE // 2)
        
        PALLETE = {
            'blue': (150, 170, 200),
            'cyan': (144, 239, 240),
            'drk-purple': (63, 45, 112),
            'lt-blue': (170, 224, 241),
            'lt-purple': (150, 100, 187),
            'magenta': (129, 55, 113),
            'mid-blue': (83, 91, 113),
            'pink': (201, 93, 177), 
            'red': (255, 100, 100),
            'white': (250, 250, 250)
        }
        super().__init__()

class PolyBounce(Game):
    
    
    def __init__(self):
        super().__init__(title='PolyBounce', 
                         ui_type=PolyBounceUI, 
                         player_type=Ball, 
                         enemy_type=Polygon)
        
        # Entities setup
        
        
        # Now that all the game objects are created, I can add collision handling for them
        
        
if __name__ == "__main__":
    PolyBounce().start()
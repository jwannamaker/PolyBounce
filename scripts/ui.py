import random

import pygame
from pygame import Vector2

class UI:
    """ A general interface for my personal games. Handles the actual pygame
    rendering pipline including a player, enemies, and display boxes. Aiming 
    to be as reuseable as possible.
    """
    def __init__(self):
        self.display_types = {
            'box': pygame.sprite.Sprite,
            'player': pygame.sprite.Sprite,
            'enemy': pygame.sprite.Sprite
        }
        
        self.SCREEN_SIZE = Vector2(100, 100)
        self.CENTER = Vector2(self.SCREEN_SIZE // 2)
        
        self.PALLETE = {}
        
        self.entities = {
            'moving': pygame.sprite.Group(),
            'still': pygame.sprite.Group()
        }
        self.screen = pygame.Surface(self.SCREEN_SIZE)
        
    def load_font(self, font_filename):
        font_file = self.FONT_DIR + font_filename
        self.font = pygame.font.Font(font_file, 12)
    
    def get_color(self, color_str):
        return pygame.Color(self.PALLETE[color_str].value)

    def get_shuffled_colors(self, N):
        """ Shuffles the colors and returns N of them without repeats. """
        random.shuffle(self.PALLETE)
        return random.sample(self.PALLETE, N)
        
    def create_sprite_for_entity(self, entity_type, entity):
        new_sprite = self.display_types[entity_type]()
        if entity_type in UI.display_types.keys():
            new_sprite.image = entity.create_image()
            new_sprite.rect = entity.create_rect()
        
    def update_all(self):
        pass


class PolyBounceUI(UI):
    def __init__(self):
        self.IMG_DIR = 'data/images/'
        self.FONT_DIR = 'data/fonts/'

        self.SCREEN_SIZE = Vector2(1280, 720)
        self.CENTER = Vector2(self.SCREEN_SIZE // 2)
        
        self.PALLETE = {
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

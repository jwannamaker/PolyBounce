import random
from abc import ABC, abstractmethod

import pygame
from pygame import Vector2, Rect, Color, Surface

class UI:
    """ A general interface/abstract class for my personal games. Handles the actual pygame
    rendering pipline including a player, enemies, and display boxes. Aiming 
    to be as clear and reuseable as possible.
    """
    def __init__(self, 
                 font_dir: str, 
                 palette: dict[str, tuple[int, int, int]], 
                 screen_size: tuple[int, int]):
        self.FONT_DIR = (font_dir)
        self.PALETTE = palette
        self.SCREEN_SIZE = Vector2(screen_size)
        self.CENTER = Vector2(self.SCREEN_SIZE // 2)
        
        self.entities = {
            'moving': pygame.sprite.Group(),
            'still': pygame.sprite.Group()
        }
        self.font = pygame.font.SysFont('Arial', 18)    # Load default font
        self.screen = Surface(self.SCREEN_SIZE)
        
    def load_font(self, font_filename, font_size=18):
        font_file = self.FONT_DIR + font_filename
        self.font = pygame.font.Font(font_file, font_size)
    
    def get_color(self, color_str):
        return Color(self.PALETTE[color_str])

    def get_shuffled_colors(self, N):
        """ Shuffles the colors and returns N of them without repeats. """
        random.shuffle(self.PALETTE.keys())
        return random.sample(self.PALETTE, N)
    
    def draw_all(self, surface):
        """ I might need to create a different subsurface for each entity this
        is called for.
        """
        for entity_group in self.entities.values():
            for entity in entity_group:
                entity.draw(surface)
        
    def update_moving(self):
        for entity in self.entities['moving']:
            entity.update()

class BorderedBox:
    type = {
        'current_level': {
            'relative_position': 'top-left',
            'rect': Rect(left_top=(0, 0), width_height=(100, 100))},
        'color_queue': {
            'relative_position': 'left',
            'rect': Rect(left_top=(0, 0), width_height=(100, 100))},
        'high_score': {
            'relative_position': 'top-right',
            'rect': Rect(left_top=(0, 0), width_height=(100, 100))},
        'player_score': {
            'relative_position': 'mid-right',
            'rect': Rect(left_top=(0, 0), width_height=(100, 100))}
    }
    
    def __init__(self, ui: UI, box_type, column_denominator):
        """ Makes a subsurface from the game's screen.
        TODO: Needs to be added to the game's list of updatable objects.
        """
        self.ui = ui
        self.box_surface = ui.screen.subsurface(BorderedBox.type[box_type])
        self.column_width = ui.SCREEN_SIZE.x / column_denominator
        self.elements = {
            'text': [],
            'image': []
        }
    
    def add_element(self, element_type, element):
        if element_type == 'text':
            self.add_text(element)
        elif element_type == 'image':
            self.add_image(element)
        
        if self.elements.get(element_type) == None:
            self.elements['element_type'] = element
    
    def add_image(self, image):
        self.elements['image'].append(image)
    
    def add_text(self, text):
        self.elements['text'].append('{:20s} {:5f}'.format(text))
        
    def update(self):
        """ Observe. Use a call from wherever the source of the displayed info 
        is coming from. 
        """
        pass
    
    def draw(self, screen):
        for element in self.elements:
            for i, line in enumerate(element):
                screen.blit(self.ui.font.render(line, True, Color('white')), 
                                    (self.ui.SCREEN_SIZE.x / 2, self.column_width))
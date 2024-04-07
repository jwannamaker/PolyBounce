import random
from abc import ABC, abstractmethod

import pygame
from pygame import Vector2, Rect, Color, Surface, Font

from game import Game
from scripts.entity import Asset, FixedPosition

class UI:
    def __init__(self, 
                palette: dict[str, tuple[int, int, int]],
                font_dir: str): 
        self.PALETTE = palette
        self.FONT_DIR = font_dir
        self.font = pygame.font.SysFont('Arial', 18)    # Load default font
        self.SCREEN_SIZE = pygame.display.get_window_size()
        self.CENTER = Vector2(self.SCREEN_SIZE // 2)
        
    def load_font(self, font_filename, font_size=18):
        font_file = self.FONT_DIR + font_filename
        self.font = pygame.font.Font(font_file, font_size)
    
    def get_color(self, color_str):
        return Color(self.PALETTE[color_str])

    def get_shuffled_colors(self, N):
        random.shuffle(self.PALETTE.keys())
        return random.sample(self.PALETTE, N)

class TextBox(FixedPosition):
    def __init__(self, asset: Asset, screen_position: tuple[float, float], text: str | list[str]):
        super().__init__(asset, screen_position)
        self.text = text
    
    def draw(self, screen: Surface, font: Font):
        self.image.blit(font.render(self.text, True, self.color), 
                        (15, 15), 
                        (self.rect.width-15, self.rect.height-15))
        screen.blit(self.image, 
                    self.screen_position,
                    (self.rect.width, self.rect.height))
   
    def update(self, text):
        if self.text != text:
            self.draw()
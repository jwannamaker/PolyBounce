from __future__ import annotations

import json
import random
from abc import ABC, abstractmethod

import pygame
from pygame import Surface, Color, Font

class UI:
    PALETTE: dict[str, list[tuple[int, int, int]]]
    FONT_DIR: str
    SCREEN_SIZE: tuple[int, int]
    CENTER: tuple[int, int]
    font: Font

class Game:
    def __init__(self):
        self.ui: UI = UI()
        self.all_entities = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.fps = 60
        self.frame_start: float = 0.0 # milliseconds
        self.running = False
        self.screen: Surface = Surface((100, 100))
        pygame.init()
        pygame.display.set_mode(self.screen.get_size())
    
    def grab_palette(self, json_filename: str):
        with open(json_filename, 'r') as palette_file:
            self.ui.PALETTE = json.load(palette_file)
            
        for key in self.ui.PALETTE.keys():
            self.ui.PALETTE[key] = [tuple(value) for value in self.ui.PALETTE[key]]
        
    def load_font(self, font_filename: str, font_size: int = 18):
        font_file = self.ui.FONT_DIR + font_filename
        self.ui.font = pygame.font.Font(font_file, font_size)
    
    def get_color(self, color_name: str) -> Color:
        return Color(self.ui.PALETTE[color_name][0])
    
    def get_gradients(self, color_name: str, gradients: int) -> list[Color]:
        return [Color(self.ui.PALETTE[color_name][i]) for i in range(gradients)]

    def get_shuffled_colors(self, N):
        colors = list(self.ui.PALETTE.keys())
        colors.remove('white')
        colors.remove('black')
        random.shuffle(colors)
        
        return random.sample(colors, N)
    
    def set_fps(self, fps):
        self.fps = fps
    
    def start(self):
        self.running = True
        self.main_loop()
    
    def get_dt(self):
        """ Capture the time since the last frame. """
        current_ticks = pygame.time.get_ticks()
        return current_ticks - self.frame_start
    
    def main_loop(self):
        while self.running:
            self.frame_start = pygame.time.get_ticks()
            self.handle_user_input()
            self.process_game_logic()
            self.render()
        pygame.quit()
    
    @abstractmethod
    def handle_user_input(self):
        pass
    
    @abstractmethod
    def process_game_logic(self):
        pass
        
    @abstractmethod
    def render(self):
        pass

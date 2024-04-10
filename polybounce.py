import random
import json
import numpy as np
from enum import Enum, auto
from abc import ABC, abstractmethod

import pygame
from pygame import Surface, Color, Font, Vector2
import pymunk

from scripts.entity import Asset, REG_POLY, POLY, CIRCLE, Movable, FixedPosition
from scripts.physics import PhysicsEngine

WALL_THICKNESS = 50

class RING_SIZE(Enum):
    INNER = 100
    MIDDLE = 150
    OUTER = 200

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
        self.screen: Surface = None
    
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

class Player(Movable):
    def __init__(self, game: Game, asset: Asset):
        self.game = game
        self.groups = [self.game.all_entities, self.game.player_group]
        super().__init__(self.groups, asset.shape, asset.color, asset.position)
        self.level_score = 0
        self.total_score = 0
        
    def save_and_clear_score(self):
        # TODO: save the score in a json for highscores
        self.total_score += self.level_score
        self.level_score = 0
    
    def get_score(self):
        """ Calculate the score base_imaged on the current number of hits times the
        level the hits happened on.
        """
        return self.level_score + Player.total_score
    
    def current_level(self):
        """ Return the current level this player is on in the game. """
        pass
    
    def level_up(self):
        """ Increase the mass or something. Making it easier to break through 
        blocks.
        """
        pass

class Enemy(Movable):
    def __init__(self, game: Game, asset: Asset):
        self.groups = [self.game.all_]
        super().__init__(asset)
        self.hits_taken = 0
        self.hits_to_die = 1
        
    def take_hit(self, hit_strength: int = 1) -> bool:
        self.hits_taken += hit_strength
        if self.hits_taken >= self.hits_to_die:
            # TODO: DETACH FROM PHYSICS ENGINE OBSERVERS
            self.kill()
        
class RingFactory:
    def __init__(self, game: Game, N: int) -> None:
        self.game = game
        self.N = N
        self.base_colors = self.game.get_shuffled_colors(self.N)
        self.colors = self.game.get_gradients(self.base_colors, self.N)
    
    def create_ring(self, size: RING_SIZE, angular_velocity: float) -> list[pymunk.Shape]:
        outer_radius = size
        inner_radius = size - WALL_THICKNESS
        
        outer_points = REG_POLY.get_vertices(self.N, outer_radius)
        inner_points = REG_POLY.get_vertices(self.N, inner_radius)
        
        # Splitting and regrouping vertices into (inner_start, OUTER_start, OUTER_END, inner_END)
        for i in self.N:
            self.base_colors[i]

class Side(Movable):
    def __init__(self,
                 game: Game,
                 asset: Asset):
        super().__init__()

class TextBox(FixedPosition):
    def __init__(self, asset: Asset, screen_position: tuple[float, float], text: str):
        super().__init__(asset)
        self.text = text
        self.screen_position = screen_position
    
    def draw(self, screen: Surface, font: Font):
        self.image.blit(font.render(self.text, True, self.color), 
                        (15, 15), 
                        (self.rect.width - 15, self.rect.height - 15))
        screen.blit(self.image, 
                    self.screen_position,
                    (self.rect.width, self.rect.height))
   
    def update(self, text):
        if self.text != text:
            self.text = text
            self.draw()
    
class PolyBounce(Game):
    def __init__(self):
        super().__init__()
        self.grab_palette('data/palette.json')
        
        self.fps = 60
        self.frame_start: float = 0.0 # milliseconds
        self.running = False
        pygame.init()
        self.screen = pygame.display.set_mode(pygame.display.get_desktop_sizes()[0])
        pygame.display.set_caption('PolyBounce')
        pygame.display.toggle_fullscreen()
        self.ui.SCREEN_SIZE = (self.screen.get_size()[0], self.screen.get_size()[1])
        self.ui.CENTER = (self.ui.SCREEN_SIZE[0] // 2, self.ui.SCREEN_SIZE[1] // 2)
        pygame.display.message_box('Welcome to PolyBounce!', 
                                   'Your Color Meters are on the right -->\n\
                                    Fill them up by bouncing on the correct color rings!\n\n\
                                    Press [ENTER] to toggle Falling.\n\
                                    Press [ESC] to Quit.')
        self.background = Surface(self.screen.get_size())
        self.background.fill((0, 0, 0))
        
        self.all_entities = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        
        self.player_asset = Asset(CIRCLE(radius=10), self.get_color('white'), self.ui.CENTER)
        self.player = Player(self, self.player_asset, self.ui.CENTER)
        self.enemy 
    
    def reset_player(self):
        self.player.level_score = 0
    
    def handle_user_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                
            if event.type == pygame.KEYUP:
                # TODO: Implement the player input with EventManager
                if event.key == pygame.K_RETURN:    
                    self.player.stop_moving()
                pass
    
    def process_game_logic(self):
        """ Retrieve the position data from the PhysicsEngine. """
        position = self.ui.CENTER
        self.player_group.update(position)
    
    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.all_entities.draw(self.screen)
        
        # TODO: Add some logic here to address the need for semi-fixed framerate?
        # self.clock.tick_busy_loop(self.fps)
        PhysicsEngine.step_by(self.get_dt())
        pygame.display.flip()
    
if __name__ == "__main__":
    PolyBounce().start()
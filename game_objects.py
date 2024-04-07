import random

import pygame
from pygame import Surface

from scripts.entity import Asset, Movable, FixedPosition
from scripts.physics import PhysicsEngine

class Player(Movable):
    def __init__(self, game, asset: Asset, start_position: tuple[float, float]):
        super().__init__(asset, start_position)
        
        self.score = 0
        self.colors_to_play: set[str] = {}
        
    def reinit_stats(self):
        self.score = 0
    
    def calculate_score(self):
        """ Calculate the score base_imaged on the current number of hits times the
        level the hits happened on.
        """
        pass
    
    def current_level(self):
        """ Return the current level this player is on in the game. """
        pass
    
    def level_up(self):
        """ Increase the mass or something. Making it easier to break through 
        blocks.
        """
        pass

class Enemy(Movable):
    def __init__(self, asset: Asset, start_position: tuple[float, float]):
        super().__init__(asset, start_position)

class Game:
    def __init__(self, title):
        self.all_entities = pygame.sprite.Group()
        self.fps = 60
        self.frame_start: float = 0.0 # milliseconds
        self.running = False
        pygame.init()
        self.screen = pygame.display.set_mode((pygame.display.get_desktop_sizes()[0]))
        pygame.display.set_caption(title)
        pygame.display.message_box('Welcome to PolyBounce!')
        self.background = Surface(self.screen.get_size()).convert()
        self.background.fill((0, 0, 0))
        
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
    
    def handle_user_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    
            if event.type == pygame.KEYUP:
                # TODO: Implement the 
                pass
    
    def process_game_logic(self):
        """ Apply updates to all the game objects according to current game 
        state. Retrieve the position data from the PhysicsEngine.
        """
        self.all_entities.update()
    
    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.all_entities.draw(self.screen)
        
        # TODO: Add some logic here to address the need for semi-fixed framerate?
        # self.clock.tick_busy_loop(self.fps)
        PhysicsEngine.step_by(self.get_dt())
        pygame.display.flip()
    
    def create_next_level(self, difficulty_dict):
        #TODO Use the defined difficulty dictionary to create the correct difficulty per level.
        pass


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
    pass

class Level:
    """ Level is an asset factory. """
    def __init__(self, game: Game, level_number: int, difficulty: dict):
        self.game = game
        self.level_number = level_number
        self.difficulty = difficulty
        self.enemies_spawned = 0

    def spawn_enemies(self):
        """ Spawn enemies based on current level's difficulty. """
        new_sprite = Asset(Asset.CIRCLE,
                           random.choice(self.game.PALLETE.keys()),
                           self.screen)
        self.game.all_entities.add(new_sprite)
        self.enemies_spawned += 1 # Increase per each SIDE that's spawned

    def reset_player_position(self):
        """ Reset player position to starting position. """
        self.game.player.reinit_position

    def increase_difficulty(self):
        """Increase difficulty for the next level"""
        self.level_number += 1
        self.difficulty = self.calculate_next_difficulty()
        self.enemies_spawned = 0

    def calculate_next_difficulty(self, k):
        # Example: increase enemy count and spawn rate for the next level
        next_difficulty = {
            
        }
        return next_difficulty
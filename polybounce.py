import random
import numpy as np
from abc import ABC, abstractmethod

import pygame
from pygame import Vector2, Surface, Color, Font
import pymunk

from scripts.entity import Asset, Movable, FixedPosition
from scripts.physics import PhysicsEngine

class Game(ABC):
    def __init__(self):
        self.all_entities = pygame.sprite.Group()
        self.fps = 60
        self.frame_start: float = 0.0 # milliseconds
        self.running = False
        self.screen: Surface = None
        
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
    total_score = 0
    
    def __init__(self, game: Game, asset: Asset, start_position: tuple[float, float]):
        super().__init__(asset, start_position)
        self.game = game
        self.level_score = 0
        self.colors_to_play: set[str] = {}
        
    def save_and_clear_score(self):
        Player.total_score += self.level_score
        self.level_score = 0
    
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
    
    def draw(self, screen):
        pass
    
    def update(self):
        pass

class Enemy(Movable):
    def __init__(self, asset: Asset, start_position: tuple[float, float]):
        super().__init__(asset, start_position)
        
    def draw(self, screen):
        pass
    
    def update(self):
        pass

class Polygon:
    """ Polygon is Factory of Sides. """
    def __init__(self, N, physics_engine: PhysicsEngine):
        self.N = N
        self.theta = (np.pi * 2) / self.N
        
        self.body.body_type = pymunk.Body.KINEMATIC
        self.start_angle = self.body.angle
        self.rotating = False 
        
    def get_vertices(self, radius):
        """ Offset is the distance for x, y to the center of the regular polygon 
        vertices generated from this method.
        """
        offset_x = self.radius
        offset_y = self.radius
        tilt = (np.pi - self.theta) / 2
        vertices = []
        for i in range(1, self.N + 1):
            x = (radius * np.cos(tilt + self.theta * i)) + offset_x
            y = (radius * np.sin(tilt + self.theta * i)) + offset_y
            vertices.append((x, y))
        return vertices
    
    def get_subsurface(self):
        """ New surface inherits palette, colorkey, and alpha settings. """
        return self.image.subsurface((0, 0, self.radius * 2, self.radius * 2))
    
    def get_color_at(self, x, y):
        local_coord = pymunk.pygame_util.from_pygame((x, y))
        return self.image.get_at(local_coord)
    
    def get_sides(self):
        colors = self.game.get_shuffled_colors(self.N)
        for i, color in enumerate(colors):
            j = i + 1 if i < self.N - 1 else 0
            inner = [self.inner_vertices[i], self.inner_vertices[j]]
            outer = [self.vertices[i], self.vertices[j]]
            points = [inner[0], outer[0], outer[1], inner[1]]
            
            new_shape = self.create_side_shape(color, points)
            new_sprite = self.create_side_sprite(color, points)
            
            self.side_sprites.add(new_sprite)
            self.side_shapes.append(new_shape)
    
    def remove_side(self, color):
        
        pass
    
    def cw_rotate(self, dt):
        if self.rotating:
            self.body.angular_velocity = max(20, self.body.angular_velocity + 1)
        
    def ccw_rotate(self, dt):   
        if self.rotating:
            self.body.angular_velocity = min(-20, self.body.angular_velocity - 1)
        
    def render(self):
        for side in self.sides:
            self.game.screen.blit(side.image, self.rect.topleft)
        self.game.screen.blit(self.image, self.rect.topleft)

class Side:
    def __init__(self, 
                 polygon: Polygon, 
                 radius: float, 
                 start_angle: float,    # radians 
                 end_angle: float,      # radians 
                 wall_thickness: int = 50):      
        self.polygon = polygon
        self.start_angle = start_angle
        self.end_angle = end_angle
        self.wall_thickness = wall_thickness
        
        self.outer_radius = radius
        self.inner_radius = self.outer_radius - self.wall_thickness
        self.vertices = self.get_vertices()
        
    def get_vertices(self):
        """ Uses polar coordinates to get the inner and outer vertices ordered
        into a convex hull (aka inner outer Outer Inner). The vertices are 
        """
        center = (self.outer_radius, self.outer_radius)
        
        inner_start = pygame.math.Vector2(center) + pygame.math.Vector2().from_polar((self.inner_radius, -self.start_angle))
        inner_end = pygame.math.Vector2(center) + pygame.math.Vector2().from_polar((self.inner_radius, -self.end_angle))
        outer_start = pygame.math.Vector2(center) + pygame.math.Vector2().from_polar((self.outer_radius, -self.start_angle))
        outer_end = pygame.math.Vector2(center) + pygame.math.Vector2().from_polar((self.outer_radius, -self.end_angle))
        
        return [inner_start, outer_start, outer_end, inner_end]

class TextBox(FixedPosition):
    def __init__(self, asset: Asset, screen_position: tuple[float, float], text: str):
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
            self.text = text
            self.draw()

class UI:
    PALETTE: dict[str, tuple[int, int, int]]
    
    def __init__(palette: dict[str, tuple[int, int, int]],
                font_dir: str): 
        UI.PALETTE = palette
        FONT_DIR = font_dir
        font = pygame.font.SysFont('Arial', 18)    # Load default font
        SCREEN_SIZE = pygame.display.get_window_size()
        CENTER = Vector2(SCREEN_SIZE // 2)
        
    def load_font(self, font_filename, font_size=18):
        font_file = self.FONT_DIR + font_filename
        self.font = pygame.font.Font(font_file, font_size)
    
    def get_color(self, color_str):
        return Color(self.PALETTE[color_str])

    def get_shuffled_colors(self, N):
        random.shuffle(self.PALETTE.keys())
        return random.sample(self.PALETTE, N)

class Level:
    """ Level is an asset factory. """
    def __init__(self, game: Game, level_number: int, difficulty: dict):
        self.game = game
        self.level_number = level_number
        self.difficulty = difficulty
        self.enemies_spawned = 0

    def spawn_enemies(self):
        """ Spawn enemies based on current level's difficulty. """
        enemy = Asset(Asset.POLY(), )
        self.game.all_entities.add(enemy)
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
            'Player': [i for i in range(k)],
            'Ring Side Count': [i for i in range(k)],
            'Ring Colors': [i for i in range(k)]
        }
        return next_difficulty
    
class PolyBounce(Game):
    def __init__(self):
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
        self.fps = 60
        self.frame_start: float = 0.0 # milliseconds
        self.running = False
        
        pygame.init()
        self.screen = pygame.display.set_mode((pygame.display.get_desktop_sizes()[0]))
        pygame.display.set_caption('PolyBounce')
        pygame.display.message_box('Welcome to PolyBounce!', 
                                   'Fill up the Color Meters by bouncing on the appropriate Rings.\n\n\
                                       Press [ENTER] to toggle Falling.')
        self.background = Surface(self.screen.get_size()).convert()
        self.background.fill((0, 0, 0))
        
        self.all_entities = pygame.sprite.Group()
        self.player = Player(self, Asset.CIRCLE(radius=10), self.PALLETE['white'],)
        self.difficulty = {'Color Queue': {random.sample(self.PALLETE.keys(), 3)}, 
                           'Rings': [random.sample(self.PALLETE.keys(), random.choice(3, 4)) for _ in range(3)]}
        self.levels = Level(self, 0, {'Player Meters': [3, 3, 3],
                                      'Rings Sizes': [3, 4, 5]})

    
    def handle_user_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    
            if event.type == pygame.KEYUP:
                # TODO: Implement the player input with EventManager
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
    
if __name__ == "__main__":
    PolyBounce().start()
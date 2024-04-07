import random
import numpy as np

import pygame
from pygame import Vector2
import pymunk

from game_objects import Game, Level, UI
from scripts.physics import PhysicsEngine

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

class PolyBounceUI(UI):
    def __init__(self):
        self.IMG_DIR = 'data/images/'
        self.FONT_DIR = 'data/fonts/'

        self.SCREEN_SIZE = Vector2(1280, 720)
        self.CENTER = Vector2(self.SCREEN_SIZE // 2)
        
        
        super().__init__()

class PolyBounce(Game):
    def __init__(self):
        super().__init__('PolyBounce')
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
        self.difficulty = {'Color Queue': {random.sample(self.PALLETE.keys(), 3)}, 
                           'Rings': [random.sample(self.PALLETE.keys(), random.choice(3, 4)) for _ in range(3)]}
        self.levels = [Level(self, 0, )]
        
        
        # Now that all the game objects are created, I can add collision handling for them
   
if __name__ == "__main__":
    PolyBounce().start()
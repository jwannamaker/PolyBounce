""" polygon.py contains the definition for the Polygon class and the Side class.
"""

import numpy as np
from collections import deque

import pygame
from pygame import gfxdraw
import pymunk

from ui import UI
from entity import Enemy, Entity
from physics import PhysicsEngine


class Side(Enemy):
    """ This is a single side of a Polygon. Only holds the absolute minimum
    needed to create a Pymunk representation, and a Pygame representation. The
    Game will determine the rest.
    """
    def __init__(self, entity: Entity, radius, start_angle, end_angle, wall_thickness=50):      
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
        
        vertices = [inner_start, outer_start, outer_end, inner_end]
        return vertices
        

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
        colors = UI.get_shuffled_colors(self.N)
        for i, color in enumerate(colors):
            j = i + 1 if i < self.N - 1 else 0
            inner = [self.inner_vertices[i], self.inner_vertices[j]]
            outer = [self.vertices[i], self.vertices[j]]
            points = [inner[0], outer[0], outer[1], inner[1]]
            
            new_shape = self.create_side_shape(color, points)
            new_sprite = self.create_side_sprite(color, points)
            
            self.side_sprites.add(new_sprite)
            self.side_shapes.append(new_shape)
    
    def create_side_sprite(self, color, points):
        """ Uses the points to create an image and a rect and returns it. """
        side = pygame.sprite.Sprite()
        side.image = self.get_subsurface()
        gfxdraw.filled_polygon(side.image, points, PolyBounceUI.get_color(color))
        side.rect = side.image.get_rect()
        side.mask = pygame.mask.from_surface(side.image)
        return side
        
    def remove_side(self, color):
        pass
    
    def cw_rotate(self, dt):
        if self.rotating:
            self.body.angular_velocity = max(20, self.body.angular_velocity + 1)
        
    def ccw_rotate(self, dt):   
        if self.rotating:
            self.body.angular_velocity = min(-20, self.body.angular_velocity - 1)
        
    def render(self):
        for side in self.side_sprites:
            self.game.screen.blit(side.image, self.rect.topleft)
        self.game.screen.blit(self.image, self.rect.topleft)

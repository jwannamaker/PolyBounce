import copy
from typing import NamedTuple, Optional
from abc import ABC, abstractmethod

import numpy as np
import pygame
from pygame import Rect, mask, Surface, Color

class CIRCLE(NamedTuple):
    radius: int
    
    def get_center(self) -> tuple[int, int]:
        return (self.radius, self.radius)

class REG_POLY(NamedTuple):
    N: int
    radius: int
    vertices: Optional[list[list[int, int]]]
    
    def get_center(self) -> tuple[int, int]:
        return (self.radius, self.radius)
    
    @staticmethod
    def get_vertices(N: int, radius: float) -> list[tuple[int, int]]:
        # radius = round(radius, 2)
        offset_x = radius
        offset_y = radius
        theta = (2 * np.pi) / N    # Exterior angle, the radians between each vertex.
        tilt = (np.pi - theta) / 2  # Causes the generated polygon to always have a 'floor'.
        vertices = []
        for i in range(1, N + 1):
            x = (radius * np.cos(tilt + theta * i)) + offset_x
            y = (radius * np.sin(tilt + theta * i)) + offset_y
            vertices.append((x, y))
        return vertices
        
class POLY(NamedTuple):
    width: int
    height: int
    vertices: list[tuple[int, int]]

class BOX(NamedTuple):
    width: int
    height: int
    
    def get_corners(self) -> list[tuple[int, int]]:
        return [(0, 0), 
                (0, self.height), 
                (self.width, self.height),
                (self.width, 0)]

class Asset(pygame.sprite.Sprite):
    def __init__(self, 
                 groups: list[pygame.sprite.Group],
                 shape: CIRCLE | POLY | REG_POLY | BOX, 
                 color: Color, 
                 position: tuple[int, int], 
                 surface: Optional[Surface] = None):
        self.groups = groups
        super().__init__(groups)
        self.shape = shape
        self.color = color
        self.position = list(position)
        self.surface = surface
        self.left_top = (int(0), int(0))
        self.width_height = (0, 0)
        
        if isinstance(self.shape, CIRCLE):
            self.image = self.create_circle_image()
        elif isinstance(self.shape, POLY):
            self.image = self.create_poly_image()
        elif isinstance(self.shape, REG_POLY):
            self.image = self.create_reg_poly_image()
        elif isinstance(self.shape, BOX):
            self.image = self.create_box_image()
        
        self.rect = self.image.get_rect(center=self.position)
        self.mask = mask.from_surface(self.image)
    
    def create_circle_image(self) -> Surface:
        self.width_height = (self.shape.radius*2, self.shape.radius*2)
        if self.surface == None:
            self.surface = Surface(self.width_height)
            self.image = self.surface.subsurface(self.left_top, self.width_height)
        else:
            self.image = Surface(self.width_height)
        pygame.draw.circle(self.image, 
                           self.color, 
                           self.shape.get_center(), 
                           self.shape.radius)
        return self.image
    
    def create_poly_image(self) -> Surface:
        self.width_height = (self.shape.width, self.shape.height)
        if self.surface == None:
            self.surface = Surface(self.width_height)
            self.image = self.surface.subsurface(self.left_top, self.width_height)
        else:
            self.image = Surface(self.width_height)
        pygame.draw.polygon(self.image, 
                            self.color, 
                            self.shape.vertices, 
                            width=0)
        return self.image
    
    def create_reg_poly_image(self) -> Surface:
        self.width_height = (round(self.shape.radius*2), round(self.shape.radius*2))
        if self.surface == None:
            self.surface = Surface(self.width_height)
            self.image = self.surface.subsurface(self.left_top, self.width_height)
        else:
            self.image = Surface(self.width_height)
        print('color_name: ' + str(self.color))
        pygame.draw.polygon(self.image, 
                            self.color, 
                            REG_POLY.get_vertices(self.shape.N, self.shape.radius), 
                            width=-1)
        return self.image
    
    def create_box_image(self) -> Surface:
        self.width_height = (self.shape.width, self.shape.height)
        inner_left_top = (self.left_top[0]+15, self.left_top[1]+15)
        inner_width_height = (self.shape.width-15, self.shape.height-15)
        if self.surface == None:
            self.surface = Surface((self.shape.width, self.shape.height)).set_clip((inner_left_top, inner_width_height))
            self.image = self.surface.subsurface(self.left_top, self.width_height)
        else:
            self.image = Surface(self.width_height)
        pygame.draw.rect(self.image,
                         self.color, 
                         (self.left_top, self.width_height), 
                         border_radius=5)
        return self.image

class Movable(Asset):
    @abstractmethod
    def draw(self, surface: Surface) -> None:
        surface.blit(self.image, self.rect.topleft, self.width_height)
    
    @abstractmethod
    def update(self, dt: float) -> None:
        """ The position of this object is expected to change every frame. This
        method needs to do something every time it gets called.
        """
        # TODO: Implement calling to PhysicsEngine for the position of the shape
        # TODO: Convert the position from PhysicsEngine to Pygame coordinates, adjust rect.topleft
        self.rect.topleft = ((self.position[0] - self.width_height[0]), 
                             (self.position[1] - self.width_height[1]))
        
    @abstractmethod
    def test_notified(self, data) -> None:
        print(data)

class FixedPosition(Asset):
    @abstractmethod
    def draw(self, surface: Surface) -> None:
        """ This method will ONLY change the data displayed on this Entity. It 
        will be drawn in the same position every time.
        """
        surface.blit(self.image, self.rect.topleft, self.image.get_size())
    
    @abstractmethod
    def update(self, dt: float) -> None:
        """ This method needs to call check_change() if there are any changes 
        before calling draw().
        """
        # TODO: Implement calling to PhyscicsEngine/Player/Enemy/whatever 
        pass
    
    @abstractmethod
    def test_notified(self, data) -> None:
        print(data)
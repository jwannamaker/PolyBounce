import copy
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import NamedTuple, Optional

import numpy as np
import pygame
from pygame import mask, Surface, Color

class Shape(ABC):
    def __init__(self):
        self.center_offset: tuple[int, int] = self.get_center_offset()
        self.width: tuple[int] = self.get_width()
        self.height: tuple[int] = self.get_height()
    
    @abstractmethod
    def get_center_offset(self) -> tuple[int, int]:
        pass
    
    @abstractmethod
    def get_width(self) -> tuple[int]:
        pass
    
    @abstractmethod
    def get_height(self) -> tuple[int]:
        pass

@dataclass
class CIRCLE(Shape):
    radius: int
    
    def __post_init__(self):
        super().__init__()
    
    def get_center_offset(self) -> tuple[int, int]:
        return (self.radius, self.radius)
    
    def get_width(self) -> tuple[int]:
        return (self.radius * 2)
    
    def get_height(self) -> tuple[int]:
        return (self.radius * 2)

@dataclass
class POLY(Shape):
    vertices: list[tuple[int, int]]
    
    def __post_init__(self):
        super().__init__()
    
    def get_center_offset(self) -> tuple[int, int]:
        raise ValueError('Irregular Polygon')
    
    def get_width(self) -> tuple[int]:
        raise ValueError('Irregular Polygon')
    
    def get_height(self) -> tuple[int]:
        raise ValueError('Irregular Polygon')
    
@dataclass
class REG_POLY(Shape):
    N: int
    radius: int
    
    def __post_init__(self):
        super().__init__()
    
    def get_center_offset(self) -> tuple[int, int]:
        return (self.radius, self.radius)

    def get_width(self) -> tuple[int]:
        return self.radius
    
    def get_height(self) -> tuple[int]:
        return self.radius
    
    def get_vertices(self) -> list[tuple[int, int]]:
        theta = (2 * np.pi) / self.N    # Exterior angle, the radians between each vertex.
        tilt = (np.pi - theta) / 2  # Causes the generated polygon to always have a 'floor'.
        vertices = []
        for i in range(1, self.N + 1):
            x = (self.radius * np.cos(tilt + theta * i)) + self.get_center_offset()[0]
            y = (self.radius * np.sin(tilt + theta * i)) + self.get_cetner_offset()[1]
            vertices.append((x, y))
        return vertices

@dataclass
class BOX(Shape):
    width: int
    height: int
    
    def __post_init__(self):
        super().__init__()
        
    def get_center_offset(self) -> tuple[int, int]:
        return (self.width / 2, self.height / 2)
                
    def get_width(self) -> int:
        return self.width

    def get_height(self) -> int:
        return self.height
    
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
        
        self.image.set_colorkey((0, 0, 0))
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
import copy
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import NamedTuple, Optional

import numpy as np
import pygame
from pygame import mask, Surface, Color, Rect
from pygame import gfxdraw


class Shape(ABC):
    def __init__(self):
        self.center_offset: tuple[int, int] = self.get_center_offset()
        self.width: int = self.get_width()
        self.height: int = self.get_height()

    @abstractmethod
    def get_center_offset(self) -> tuple[int, int]:
        pass

    @abstractmethod
    def get_width(self) -> int:
        pass

    @abstractmethod
    def get_height(self) -> int:
        pass

    def get_blank_surface(self) -> Surface:
        return Surface([self.get_width(), self.get_height()])

    @abstractmethod
    def get_image_rect(self, color: Color) -> tuple[Surface, Rect]:
        pass


@dataclass
class CIRCLE(Shape):
    radius: int

    def __post_init__(self):
        super().__init__()

    def get_center_offset(self) -> tuple[int, int]:
        return self.radius, self.radius

    def get_width(self) -> int:
        return self.radius * 2

    def get_height(self) -> int:
        return self.radius * 2

    def get_image(self, color: Color) -> tuple[Surface, Rect]:
        image = super().get_blank_surface()
        rect = pygame.draw.circle(image, color, self.get_center_offset(), self.radius)
        return image, rect


@dataclass
class POLY(Shape):
    vertices: list[tuple[int, int]]

    def __post_init__(self):
        super().__init__()

    def get_center_offset(self) -> tuple[int, int]:
        return self.get_width() // 2, self.get_height() // 2

    def get_width(self) -> int:
        self.vertices.sort(key=lambda vertex: vertex[0])
        min_x = self.vertices[0][0]
        max_x = self.vertices[len(self.vertices)][0]
        return max_x - min_x

    def get_height(self) -> int:
        self.vertices.sort(key=lambda vertex: vertex[1])
        min_y = self.vertices[0][1]
        max_y = self.vertices[len(self.vertices)][1]
        return max_y - min_y

    def get_image_rect(self, color: Color) -> tuple[Surface, Rect]:
        image = super().get_blank_surface()
        gfxdraw.filled_polygon(image, self.vertices, color)
        return image, image.get_rect()


@dataclass
class REG_POLY(Shape):
    N: int
    radius: int

    def __post_init__(self):
        super().__init__()

    def get_center_offset(self) -> tuple[int, int]:
        return self.radius, self.radius

    def get_width(self) -> int:
        return self.radius

    def get_height(self) -> int:
        return self.radius

    def get_vertices(self) -> list[tuple[int, int]]:
        theta = (2 * np.pi) / self.N  # Exterior angle, the radians between each vertex.
        tilt = (np.pi - theta) / 2  # Causes the generated polygon to always have a 'floor'.
        vertices = []
        for i in range(1, self.N + 1):
            x = (self.radius * np.cos(tilt + theta * i)) + self.get_center_offset()[0]
            y = (self.radius * np.sin(tilt + theta * i)) + self.get_center_offset()[1]
            vertices.append((x, y))
        return vertices

    def get_image_rect(self, color: Color) -> tuple[Surface, Rect]:
        image = super().get_blank_surface()
        gfxdraw.filled_polygon(image, self.get_vertices(), color)
        return image, image.get_rect()


@dataclass
class BOX(Shape):
    width: int
    height: int
    border: int

    def __post_init__(self):
        super().__init__()

    def get_center_offset(self) -> tuple[int, int]:
        return self.width // 2, self.height // 2

    def get_width(self) -> int:
        return self.width

    def get_height(self) -> int:
        return self.height

    def get_corners(self) -> list[tuple[int, int]]:
        return [(0, 0),
                (0, self.height),
                (self.width, self.height),
                (self.width, 0)]

    def get_image_rect(self, color: Color) -> tuple[Surface, Rect]:
        image = super().get_blank_surface()
        pygame.draw.rect(image, color, self.get_corners(), border_radius=5)
        image.set_clip([self.border, self.border, self.width - self.border, self.height - self.border])
        return image, image.get_rect()


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

        self.image, self.rect = self.shape.get_image_rect(self.color)
        self.image.set_colorkey([0, 0, 0])
        self.mask = mask.from_surface(self.image)

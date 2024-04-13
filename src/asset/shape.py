from abc import ABC, abstractmethod
from dataclasses import dataclass

import numpy as np
import pygame
from pygame import Surface, Color, Rect
from pygame import gfxdraw


class Shape(ABC):
    def __init__(self):
        self.center_offset: tuple[float, float] = self.get_center_offset()
        self.width: float = self.get_width()
        self.height: float = self.get_height()

    @abstractmethod
    def get_center_offset(self) -> tuple[float, float]:
        pass

    @abstractmethod
    def get_width(self) -> float:
        pass

    @abstractmethod
    def get_height(self) -> float:
        pass

    def get_blank_surface(self) -> Surface:
        return Surface([self.get_width(), self.get_height()])

    @abstractmethod
    def get_image_rect(self, color: Color) -> tuple[Surface, Rect]:
        pass


@dataclass
class CIRCLE(Shape):
    radius: float

    def __post_init__(self):
        super().__init__()

    def get_center_offset(self) -> tuple[float, float]:
        return self.radius, self.radius

    def get_width(self) -> float:
        return self.radius * 2

    def get_height(self) -> float:
        return self.radius * 2

    def get_image_rect(self, color: Color) -> tuple[Surface, Rect]:
        image = super().get_blank_surface()
        rect = pygame.draw.circle(image, color, self.get_center_offset(), self.radius)
        return image, rect


@dataclass
class POLY(Shape):
    vertices: list[tuple[float, float]]

    def __post_init__(self):
        super().__init__()

    def get_center_offset(self) -> tuple[float, float]:
        return self.get_width() / 2, self.get_height() / 2

    def get_width(self) -> float:
        self.vertices.sort(key=lambda vertex: vertex[0])
        min_x = self.vertices[0][0]
        max_x = self.vertices[len(self.vertices)][0]
        return max_x - min_x

    def get_height(self) -> float:
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
    radius: float

    def __post_init__(self):
        super().__init__()

    def get_center_offset(self) -> tuple[float, float]:
        return self.radius, self.radius

    def get_width(self) -> float:
        return self.radius

    def get_height(self) -> float:
        return self.radius

    def get_vertices(self) -> list[tuple[float, float]]:
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
    width: float
    height: float
    border: int

    def __post_init__(self):
        super().__init__()

    def get_center_offset(self) -> tuple[float, float]:
        return self.width / 2, self.height / 2

    def get_width(self) -> float:
        return self.width

    def get_height(self) -> float:
        return self.height

    def get_corners(self) -> list[tuple[float, float]]:
        return [(0, 0),
                (0, self.height),
                (self.width, self.height),
                (self.width, 0)]

    def get_image_rect(self, color: Color) -> tuple[Surface, Rect]:
        image = super().get_blank_surface()
        pygame.draw.rect(image, [70, 70, 70], [0, 0, self.width, self.height], border_radius=25)
        pygame.draw.rect(image, color, [self.border,
                                        self.border,
                                        self.width-(self.border*2),
                                        self.height-(self.border*2)], border_radius=25)
        return image, image.get_rect()

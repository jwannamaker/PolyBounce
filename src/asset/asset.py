from typing import Optional

import pygame
from pygame import mask, Surface, Color

from asset.shape import Shape


class Asset(pygame.sprite.Sprite):
    def __init__(self,
                 groups,
                 shape: Shape,
                 color: Color,
                 position: tuple[float, float],
                 surface: Optional[Surface] = None):
        self.groups = groups
        super().__init__(groups)
        self.shape = shape
        self.color = color
        self.position = [position[0], position[1]]
        self.surface = surface

        self.image, self.rect = self.shape.get_image_rect(self.color)
        self.rect.center = self.position
        self.image.set_colorkey([0, 0, 0])
        self.mask = mask.from_surface(self.image)

    def draw(self, surface: Surface) -> None:
        surface.blit(self.image, list(self.rect.topleft))

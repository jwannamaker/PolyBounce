import pygame
from pygame import Color, Font

from fixedposition import FixedPosition
from asset.asset import Asset
from asset.shape import BOX

class BorderedBox(FixedPosition):
    def __init__(self,
                 game,
                 fixed_text: str,
                 bg_color: Color,
                 font_color: Color,
                 width: float,
                 height: float,
                 border: int,
                 position: tuple[float, float]):
        self.game = game
        self.font: Font = self.game.font
        self.fixed_text = fixed_text
        self.asset = Asset([self.game.all_entities, self.game.HUD],
                           BOX(round(width), round(height), border),
                           bg_color,
                           position)
        self.fixed_position = position
        font_width, font_height = self.font.size(self.fixed_text)
        # get a rect and position the center at the shape's center
        self.font.align = pygame.FONT_CENTER
        self.fixed_font_image = self.font.render(self.fixed_text, False, font_color)
        self.fixed_font_rect = self.fixed_font_image.get_rect(center=self.asset.shape.get_center_offset())
        self.asset.image.blit(self.fixed_font_image,
                              [self.asset.shape.get_center_offset()[0]-(font_width/2),
                               self.asset.shape.get_center_offset()[1]-(font_height/2)])

    def draw(self, surface) -> None:
        self.asset.draw(surface)

    def update(self, dt: float) -> None:
        self.asset.position = self.fixed_position

    def set_text(self, new_text: str) -> None:
            if self.text != new_text:
                self.text = new_text
                self.asset.draw()
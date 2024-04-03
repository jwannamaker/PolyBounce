import pygame
from pygame import Vector2

from ui import UI
    
class Entity(pygame.sprite.Sprite):
    """ Entity should have the option to be rendered through Pygame, but 
    shouldn't have to 'render' through Pymunk.
    """
    def __init__(self, ui: UI, groups, entity_type, color):
        self.groups = groups
        super().__init__(self.groups)
        self.entity_type = entity_type
        self.color = color
        self.init_sprite()
        
    def init_sprite(self):
        self.draw(self.image)
        self.image = pygame.Surface((self.radius * 2, self.radius * 2))
        self.image.set_colorkey((0, 0, 0))
    
    def create_mask(self):
        self.rect = pygame.Rect(self.image.get_rect())
        self.rect.topleft = (self.game.ui.CENTER.x - self.radius, 
                             self.game.ui.CENTER.y - self.radius)
        self.mask = pygame.mask.from_surface(self.image)
    
    def update(self):
        self.rect.center = Vector2(self.body.position)
    
    def draw(self, image_surface):
        pass
    
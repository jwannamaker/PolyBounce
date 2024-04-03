import pygame

from ui import UI
from game import Game
from player import Player
from entity import Entity

class Ball(Entity):
    def __init__(self, game, groups, radius, entity_type='player'):
        super().__init__(game, groups, radius, entity_type)
        
        
        self.draw()
        
        
        
    def draw(self, image_surface):
        pygame.draw.circle(image_surface, self.game.ui.get_color(self.color), [self.radius, self.radius], self.radius)
        self.image = image_surface
        
    def render(self):
        pygame.draw.circle(self.image, self.game.ui.get_color(self.color), [self.radius, self.radius], self.radius)
        self.game.screen.blit(self.image, self.rect.topleft)
        
if __name__ == '__main__':
    game = Game('Ball Test', UI, Ball, Entity)
    ball = Ball()
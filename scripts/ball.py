import pygame

from game import Game
from entity import Player

class Ball(Player):
    def __init__(self, game: Game, groups, radius, entity_type='player'):
        super().__init__(game, groups, radius, entity_type)
        self.image = pygame.draw.circle(self.image, 
                                        self.game.ui)
        
        self.draw()
        
        
        
    def draw(self, image_surface):
        pygame.draw.circle(image_surface, self.game.ui.get_color(self.color), [self.radius, self.radius], self.radius)
        
    def render(self):
        pygame.draw.circle(self.image, self.game.ui.get_color(self.color), [self.radius, self.radius], self.radius)
        self.game.screen.blit(self.image, self.rect.topleft)

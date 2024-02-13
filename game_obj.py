import pygame

class GameObj:
    '''
        
    '''
    def __init__(self, position, sprite, radius, velocity):
        self.position = pygame.Vector2(position)
        self.sprite = sprite
        self.radius = radius
        self.velocity = pygame.Vector2(velocity)
    
    def draw(self, surface):
        blit_position = self.position - pygame.Vector2(self.radius)
        surface.blit(self.sprite, blit_position)
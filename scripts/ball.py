'''
    _summary_: Game object class for the player in hexkeys
'''

from scripts.utils import *
from scripts.entity import PhysicsEntity

class Ball(PhysicsEntity):
    def __init__(self, game, radius, position=CENTER):
        super().__init__(game, radius, position)
        
        super().set_visual_properties()
        self.render()
        
        # pymunk setup
        self.body = pymunk.Body(0, 0, pymunk.Body.DYNAMIC)
        self.shape = pymunk.Circle(self.body, self.radius)
        self.body.moment = pymunk.moment_for_circle(10, 0, self.radius)
        super().set_physics_properties('player')
        
    def render(self):
        pygame.draw.circle(self.image, get_color(self.color), [self.radius, self.radius], self.radius)
        self.game.screen.blit(self.image, self.rect.topleft)
        
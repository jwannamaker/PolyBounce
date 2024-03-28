'''
    _summary_: Game object class for the player in hexkeys
'''

from polybounce.utils import *
from polybounce.entity import PhysicsEntity

class Ball(PhysicsEntity):
    def __init__(self, radius, position):
        super().__init__(radius, position)
        
        # pymunk setup
        self.body = pymunk.Body(0, 0, pymunk.Body.DYNAMIC)
        self.body.position = float(self.position.x), float(self.position.y)
        self.shape = pymunk.Circle(self.body, self.radius)
        self.body.moment = pymunk.moment_for_circle(10, 0, self.radius)
        
    def update(self, dt):
        ''' 
        Update the ball according to 
            the timestep (dt), 
            the velocity adjustments by checking if shift is being held down or not
        '''
        self.shape.collision_type = PALLETE_DICT[self.color].collision_type
        self.position = pymunk.pygame_util.to_pygame(self.body.position, self.image)
        
    def draw(self):
        pygame.draw.circle(self.image, PALLETE_DICT[self.color].value, [self.radius, self.radius], self.radius)
        
    def add_key_held(self, key):
        self.keys_held.append(key)
        
    def remove_key_held(self, key):
        self.keys_held.remove(key)
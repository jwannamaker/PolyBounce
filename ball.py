'''
    _summary_: Game object class for the player in hexkeys
'''

from utils import *

class Ball(pygame.sprite.Sprite):
    def __init__(self, space, radius, color=random.choice(list(POLY_PALLETE.keys()))):
        super().__init__()
        self.radius = radius
        self.color = color
        self.position = CENTER.copy()
        self.prev_position = self.position.copy()
        self.velocity = Vector2(0, 0)
        self.keys_held = []
        
        self.image = pygame.Surface((self.radius * 2, self.radius * 2))
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0, 0, 0))
        
        pygame.draw.circle(self.image, self.color, [self.radius, self.radius], self.radius)
        self.rect = pygame.FRect(self.image.get_rect())
        self.rect.topleft = self.position - Vector2(self.radius)
        self.prev_rect = self.rect.copy()
        
        self.mask = pygame.mask.from_surface(self.image)
        
        # pymunk setup
        self.body = pymunk.Body(0, 0, pymunk.Body.DYNAMIC)
        self.body.position = float(self.position.x), float(self.position.y)
        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.density = 1
        self.shape.elasticity = 0.9
        self.shape.friction = 0.78
        self.body.moment = pymunk.moment_for_circle(10, 0, self.radius)
        self.shape.collision_type = 1
        space.add(self.body, self.shape)

    def get_color(self):
        return self.color
    
    def change_color(self, color):
        ''' 
        Change the color and collision type of the ball according to color
        '''
        self.color = color
        self.shape.collision_type = POLY_PALLETE[color]
            
    def update(self, dt):
        ''' 
        Update the ball according to 
            the timestep (dt), 
            the velocity adjustments by checking if shift is being held down or not
        '''
        # self.shape.collision_type = POLY_PALLETE[self.color] # getting the collision type based on the current color
        self.position = pymunk.pygame_util.to_pygame(self.body.position, self.image)
        
    def draw(self, surface):
        '''
            Draws the ball on the specified surface by first calculating where 
            the topleft is positioned. Necessary because .blit() takes the 
            topleft as the second argument.
        '''
        pygame.draw.circle(self.image, self.color, [self.radius, self.radius], self.radius)
        self.rect.topleft = self.position - Vector2(self.radius)
        surface.blit(self.image, self.rect.topleft) 
        
    def add_key_held(self, key):
        self.keys_held.append(key)
        
    def remove_key_held(self, key):
        self.keys_held.remove(key)
'''
    _summary_: Game object class for the player in hexkeys
'''
from hexkey_utils import *

GRAVITY = np.array([0, 2])

class Ball():
    def __init__(self, mass, radius, color):
        # pygame.sprite.Sprite.__init__(self)
        
        self.mass = mass
        self.radius = radius
        self.color = color
        
        self.position = np.array([SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2])
        self.velocity = np.array([0.0, 0.0])
        self.acceleration = np.array([0.0, 0.0])
        
        self.keys_held = []
        
        # self.image = pygame.Surface((self.radius * 2, self.radius * 2))
        # self.image.fill((255, 255, 255))
        # self.image.set_colorkey((255, 255, 255))
        
        pygame.draw.circle(pygame.display.get_surface(), self.color, self.position.astype(int), self.radius)
        # self.rect = self.image.get_rect()
        
    def update(self):
        self.acceleration = GRAVITY
        self.velocity += self.acceleration
        self.position += self.velocity
        
        if len(self.keys_held) > 0:
            # TODO: Adjust the velocity accordingly
            print('Movements to apply: ' + str(self.keys_held))
            
        # Checking if hit left wall, correct position to be within the wall and bounce off
        if self.position[0] - self.radius < 0:
            self.position[0] = self.radius
            self.velocity[0] *= -0.3    # Negative to reverse direction, < 1 to simulate loss of momentum
            
        # Checking if hit right wall
        if self.position[0] + self.radius >= SCREEN_WIDTH:
            self.position[0] = SCREEN_WIDTH - self.radius
            self.velocity[0] *= -0.9    # Bounce off with a dampening effect
            
        # Checking if hit top wall
        if self.position[1] - self.radius < 0:
            self.position[1] = self.radius
            self.velocity[1] *= -0.3   

        # Checking if hit bottom wall
        if self.position[1] + self.radius >= SCREEN_HEIGHT:
            self.position[1] = SCREEN_HEIGHT - self.radius
            self.velocity[1] *= -0.9
        
        pygame.draw.circle(pygame.display.get_surface(), self.color, self.position.astype(int), self.radius)
        # self.rect.move(self.position.astype(float))
        
    def add_key_held(self, key):
        self.keys_held.append(key)
        
    def remove_key_held(self, key):
        self.keys_held.remove(key)
'''
    _summary_: Game object class for the player in hexkeys
'''
from utils import *

GRAVITY = np.array([0, 5])

class Ball(pygame.sprite.Sprite):
    def __init__(self, radius, color):
        # print(str(super()), self.groups())
        super().__init__()
        self.radius = radius
        self.color = color
        self.position = CENTER
        # self.mass = mass
        
        self.velocity = np.array([0.0, 0.0])
        self.acceleration = np.array([0.0, 0.0])
        
        self.keys_held = []
        
        self.image = pygame.Surface((self.radius * 2, self.radius * 2))
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0, 0, 0))
        
        pygame.draw.circle(self.image, self.color, [self.radius, self.radius], self.radius)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.position.astype(int) - self.radius
        
    def draw(self, surface):
        self.rect.topleft = self.position - self.radius
        surface.blit(self.image, self.rect.topleft) 
    
    def update(self):
        self.acceleration = GRAVITY
        self.velocity += self.acceleration
        
        # Applying any user input for movement 
        if self.keys_held.count('left'):
            self.velocity[0] += -0.5  # Left is -X
        if self.keys_held.count('right'):
            self.velocity[0] += 0.5   # Right is +X
        self.position += self.velocity
            
        # Checking if hit left wall, correct position to be within the wall and bounce off
        if self.position[0] - self.radius < 0:
            self.position[0] = self.radius
            self.velocity[0] *= -0.2    # Negative to reverse direction, < 1 to simulate loss of momentum
            
        # Checking if hit right wall
        if self.position[0] + self.radius >= SCREEN_WIDTH:
            self.position[0] = SCREEN_WIDTH - self.radius
            self.velocity[0] *= -0.2    # Bounce off with a dampening effect
            
        # Checking if hit top wall
        if self.position[1] - self.radius < 0:
            self.position[1] = self.radius
            self.velocity[1] *= -0.9   

        # Checking if hit bottom wall
        if self.position[1] + self.radius >= SCREEN_HEIGHT:
            self.position[1] = SCREEN_HEIGHT - self.radius
            self.velocity[1] *= -0.9
        
        self.rect.topleft = self.position.astype(int) - self.radius
        
    def add_key_held(self, key):
        self.keys_held.append(key)
        
    def remove_key_held(self, key):
        self.keys_held.remove(key)
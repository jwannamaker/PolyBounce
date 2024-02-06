'''
    _summary_: Game object class for the player in hexkeys
'''
from hexkey_utils import *

GRAVITY = np.array([0, 1])

class Ball(pygame.sprite.Sprite):
    def __init__(self, radius, color):
        pygame.sprite.Sprite.__init__(self)
        
        self.radius = radius
        self.color = color
        
        self.falling = False
        self.position = np.array([SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2])
        self.velocity = np.array([0.0, 0.0])
        self.acceleration = np.array([0.0, 0.0])
        
        self.image = pygame.Surface((self.radius * 2, self.radius * 2))
        self.image.fill((255, 255, 255))
        self.image.set_colorkey((255, 255, 255))
        pygame.draw.circle(self.image, self.color, self.position.astype(int), self.radius)
        self.rect = self.image.get_rect()
        
    def update(self, screen):
        
        # Checking if hit left/right wall
        if self.position[0] - self.radius < 0 or self.position[0] + self.radius > SCREEN_WIDTH:
            self.velocity[0] = -self.velocity[0]
            
        # Checking if hit top/bottom wall
        if self.position[1] - self.radius < 0 or self.position[1] + self.radius > SCREEN_HEIGHT:
            self.velocity[1] = -self.velocity[1]
            if self.velocity[1] == 0:
                self.position[1] = SCREEN_HEIGHT - self.radius
        
        self.acceleration = GRAVITY
        self.velocity += self.acceleration
        self.position += self.velocity
        pygame.draw.circle(screen, self.color, self.position.astype(int), self.radius)
    
    def freeze(self):
        self.acceleration = 0.0
        self.velocity = 0.0
        
    def move_up(self):
        # TODO increase the velocity upwards
        self.acceleration[1] += -1.0
        # self.velocity[1] += -1.0
        
    def move_down(self):
        # TODO increase the velocity downwards
        self.acceleration[1] += 1.0
        # self.velocity[1] += 1.0
        
    def move_left(self):
        # TODO increase the velocity leftwards
        self.acceleration[0] += -1.0
        # self.velocity[0] += -1.0
        
    def move_right(self):
        # TODO increase the velocity rightwards
        self.acceleration[0] += 1.0
        # self.velocity[0] += 1.0
        
        
        
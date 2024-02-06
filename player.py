'''
    _summary_: Game object class for the player in hexkeys
'''
from hexkey_utils import *

GRAVITY = np.array([0, 9.81])

class Ball(pygame.sprite.Sprite):
    def __init__(self, radius, color):
        pygame.sprite.Sprite.__init__(self)
        
        self.radius = radius
        self.color = color
        
        self.falling = False
        self.position = np.array([SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2])
        self.velocity = np.array([0.0, 1.0])
        self.acceleration = np.array([0.0, 9.81])
        
        self.image = pygame.Surface((self.radius * 2, self.radius * 2))
        self.image.fill((255, 255, 255))
        self.image.set_colorkey((255, 255, 255))
        pygame.draw.circle(self.image, self.color, self.position.astype(int), self.radius)
        self.rect = self.image.get_rect()
        
    def update(self, screen):
        
        if self.position[0] - self.radius < 0 or self.position[0] + self.radius > SCREEN_WIDTH:
            self.velocity[0] = -self.velocity[0]
        if self.position[1] - self.radius < 0 or self.position[1] + self.radius > SCREEN_HEIGHT:
            self.velocity[1] = -self.velocity[1]
        
        self.acceleration /= 2
        self.velocity += self.acceleration
        self.position += self.velocity
        # self.rect.move_ip()
        pygame.draw.circle(screen, self.color, self.position.astype(int), self.radius)
    
    def jump(self):
        # TODO can only jump if the ball is on the ground
        print('Jumping the ball')
        # TODO define the increase in height amount
        # TODO remember projectile motion, gravity is working the whole time
        
        
        
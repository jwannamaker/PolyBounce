'''
    _summary_: Game object class for the player in hexkeys
'''
from hexkey_utils import *

GRAVITY = pygame.Vector2(0, 9.81)

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png('ball.png')
        self.radius = 64
        self.falling = False
        self.position = CENTER
        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = pygame.Vector2(0, 0)
        
        # self.surface = pygame.Surface((self.radius * 2, self.radius * 2))
        # self.rect = pygame.Rect((CENTER.x - self.radius, CENTER.y - self.radius), (CENTER.x + self.radius, CENTER.y + self.radius))
        
    def update(self):
        keys = pygame.key.get_pressed()
        
        if keys[K_w] and self.position.y - self.radius > 0:
            self.position.y -= self.velocity.y
        if keys[K_s] and self.position.y + self.radius < SCREEN_HEIGHT:
            self.position.y += self.velocity.y
        
        if keys[K_a] and self.position.x - self.radius > 0:
            self.position.x -= self.velocity.x
        if keys[K_d] and self.position.x + self.radius < SCREEN_WIDTH:
            self.position.x += self.velocity.x
        
        
        self.rect.move_ip(self.position.x, self.position.y)
    
    def jump(self):
        # TODO can only jump if the ball is on the ground
        print('Jumping the ball')
        # TODO define the increase in height amount
        # TODO remember projectile motion, gravity is working the whole time
        self.physics()
    
    def physics(self):
        self.acceleration = GRAVITY
        
        self.velocity.y += self.acceleration.y * 0.1
        
        self.position.y += self.velocity.y * 0.1
        # TODO boundary check this
        
        
        
        
        
        
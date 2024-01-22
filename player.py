'''
    _summary_: Game object class for the player in hexkeys
'''
import pygame
from hexkey_utils import *

GRAVITY = pygame.Vector2(0, 9.81)

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("ball.png", -1)
        self.radius = 64
        self.falling = False
        self.position = CENTER
        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = pygame.Vector2(0, 0)
        
    def update(self, dt):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_w] and self.position.y - self.radius > 0:
            self.velocity.y *= -10
            self.position.y -= self.velocity.y * dt
        if keys[pygame.K_s] and self.position.y + self.radius < SCREEN_HEIGHT:
            self.velocity.y *= 10
            self.position.y += self.velocity.y * dt
        
        if keys[pygame.K_a] and self.position.x - self.radius > 0:
            self.velocity.x *= -10
            self.position.x -= self.velocity.x * dt
        if keys[pygame.K_d] and self.position.x + self.radius < SCREEN_WIDTH:
            self.velocity.x *= 10
            self.position.x += self.velocity.x * dt
        
        
        self.rect.move_ip(self.position.x, self.position.y)
    
    def jump(self):
        pass
    
    def physics(self):
        self.acceleration = GRAVITY
        
        self.velocity.y += self.acceleration.y * 0.1
        
        self.position.y += self.velocity.y * 0.1
        
        
        
        
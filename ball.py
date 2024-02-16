'''
    _summary_: Game object class for the player in hexkeys
'''
from utils import *

class Ball(pygame.sprite.Sprite):
    def __init__(self, radius, ring_group, color=random.choice(list(PALLETE.values()))):
        super().__init__()
        self.radius = radius
        self.color = color
        self.position = CENTER.copy()
        self.velocity = Vector2(0, 0)
        self.keys_held = []
        
        self.image = pygame.Surface((self.radius * 2, self.radius * 2))
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0, 0, 0))
        
        pygame.draw.circle(self.image, self.color, [self.radius, self.radius], self.radius)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.position - Vector2(self.radius)
        self.prev_rect = self.rect.copy()
        
        self.ring_group = ring_group
        self.mask = pygame.mask.from_surface(self.image)
    
    def collision(self, type):
        # collision_sprites = pygame.sprite.spritecollide(self, self.ring_group, False, pygame.sprite.collide_circle)
        collision_sprites = pygame.sprite.spritecollide(self, self.ring_group, False, pygame.sprite.collide_mask)
        if collision_sprites:
            for sprite in collision_sprites:
                offset_x = self.rect.topleft[0] - sprite.rect.topleft[0]
                offset_y = self.rect.topleft[1] - sprite.rect.topleft[1]
                overlap = sprite.mask.overlap(self.mask, (offset_x, offset_y))
                
                # Convert the overlap coordinate into a coordinate on the screen
                collision_x = overlap[0] + sprite.rect.topleft[0]
                collision_y = overlap[1] + sprite.rect.topleft[1]
                if type == 'horizontal':
                    # Collision is on the right
                    if self.rect.right >= collision_x and self.prev_rect.right <= collision_x:
                        self.position.x = collision_x - self.radius
                        self.rect.right = collision_x
                        self.velocity.x *= -1
                        
                    # Collision is on the left
                    if self.rect.left <= collision_x and self.prev_rect.left >= collision_x:
                        self.position.x = collision_x + self.radius
                        self.rect.left = collision_x
                        self.velocity.x *= -1
                    
                if type == 'vertical':
                    # Collision is on the bottom
                    if self.rect.bottom >= collision_y and self.prev_rect.bottom <= collision_y:
                        self.position.y = collision_y - self.radius
                        self.rect.bottom = collision_y
                        self.velocity.y *= -1
                
                    # Collision is on the top
                    if self.rect.top <= collision_y and self.prev_rect.top >= collision_y:
                        self.position.y = collision_y + self.radius
                        self.rect.top = collision_y
                        self.velocity.y *= -1
    
    def update(self):
        self.prev_rect = self.rect.copy()
        
        # Applying any user input for movement 
        if self.keys_held.count('left'):
            self.velocity.x -= 0.5
        if self.keys_held.count('right'):
            self.velocity.x += 0.5
        if self.keys_held.count('up'):
            self.velocity.y -= 0.5
        if self.keys_held.count('down'):
            self.velocity.y += 0.5
            
        # Checking if hit left wall 
        if self.position.x - self.radius <= 0:
            self.position.x = self.radius # Correct position to be within the wall and then bounce off
            self.velocity.x *= -0.2    # Negative to reverse direction, < 1 to simulate loss of momentum
            
        # Checking if hit right wall
        if self.position.x + self.radius >= SCREEN_SIZE.x:
            self.position.x = SCREEN_SIZE.x - self.radius
            self.velocity.x *= -0.2    # Bounce off with a dampening effect
            
        # Checking if hit top wall
        if self.position.y - self.radius <= 0:
            self.position.y = self.radius
            self.velocity.y *= -0.9

        # Checking if hit bottom wall
        if self.position.y + self.radius >= SCREEN_SIZE.y:
            self.position.y = SCREEN_SIZE.y - self.radius
            self.velocity.y *= -0.9
            
        self.rect.topleft = self.position - Vector2(self.radius)
        
        self.collision('horizontal')    # Detect collision along x-axis
        self.position.x += self.velocity.x
        
        self.collision('vertical')      # Detect collision along y-axis
        self.position.y += self.velocity.y
        
        
    def draw(self, surface):
        '''
            Draws the ball on the specified surface by first calculating where 
            the topleft is positioned. Necessary because .blit() takes the 
            topleft as the second argument.
        '''
        surface.blit(self.image, self.rect.topleft) 
        
    def get_slope(self):
        '''
            Return the slope of the ball, from the previous position and the 
            curernt one
        '''
        dx = self.position.x - self.prev_position.x
        dy = self.position.y - self.prev_position.y
        return Vector2(dx, dy)
        
    def add_key_held(self, key):
        self.keys_held.append(key)
        
    def remove_key_held(self, key):
        self.keys_held.remove(key)
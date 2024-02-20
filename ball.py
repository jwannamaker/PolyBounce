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
        self.prev_position = self.position.copy()
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
        collision_sprites = pygame.sprite.spritecollide(self, self.ring_group, False, pygame.sprite.collide_mask)
        if collision_sprites:
            for sprite in collision_sprites:
            # sprite = collision_sprites[0]
                offset_x = self.rect.topleft[0] - sprite.rect.topleft[0]
                offset_y = self.rect.topleft[1] - sprite.rect.topleft[1]
                relative = sprite.mask.overlap(self.mask, (offset_x, offset_y))
                
                # Convert the overlap coordinate into a coordinate on the screen
                x = relative[0] + sprite.rect.topleft[0]
                y = relative[1] + sprite.rect.topleft[1]
                collision = Vector2(x, y)
                print('Collision Detected @', collision)
                collision_side = sprite.get_closest_side(collision)     # normalized vector 
                bounced_velocity = self.velocity.reflect(collision_side)
                if type == 'horizontal':
                    # Collision is on the right
                    if self.rect.right >= collision.x and self.prev_rect.right <= collision.x:
                        self.rect.right = collision.x
                        self.position.x = collision.x - self.radius
                        self.velocity.x = bounced_velocity.x
                        
                    # Collision is on the left
                    if self.rect.left <= collision.x and self.prev_rect.left >= collision.x:
                        self.rect.left = collision.x
                        self.position.x = collision.x + self.radius
                        self.velocity.x = bounced_velocity.x 
                
                if type == 'vertical':
                    # Collision is on the bottom
                    if self.rect.bottom >= collision.y and self.prev_rect.bottom <= collision.y:
                        self.rect.bottom = collision.y
                        self.position.y = collision.y - self.radius
                        self.velocity.y = bounced_velocity.y
                        
                    # Collision is on the top
                    if self.rect.top <= collision.y and self.prev_rect.top >= collision.y:
                        self.rect.top = collision.y
                        self.position.y = collision.y + self.radius
                        self.velocity.y = bounced_velocity.y
            
    def update(self, dt):
        self.prev_rect = self.rect.copy()
        self.prev_position = self.position.copy()
        
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
        
        # self.velocity += self.acceleration
        self.position.x += self.velocity.x
        self.collision('horizontal')    # Detect collision along x-axis
        
        self.position.y += self.velocity.y
        self.collision('vertical')      # Detect collision along y-axis
        
        self.rect.topleft = self.position - Vector2(self.radius)
        
    def draw(self, surface):
        '''
            Draws the ball on the specified surface by first calculating where 
            the topleft is positioned. Necessary because .blit() takes the 
            topleft as the second argument.
        '''
        surface.blit(self.image, self.rect.topleft) 
        
    def add_key_held(self, key):
        self.keys_held.append(key)
        
    def remove_key_held(self, key):
        self.keys_held.remove(key)
'''
    _summary_: Game object class for the player in hexkeys
'''

from utils import *

class Ball(pygame.sprite.Sprite):
    def __init__(self, space, radius, color=random.choice(list(PALLETE.values()))):
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
        
        self.mask = pygame.mask.from_surface(self.image)
        
        self.body = pymunk.Body(0, 0, pymunk.Body.DYNAMIC)
        self.shape = pymunk.Circle(self.body, self.radius, (float(self.position.x), float(self.position.y)))
        self.shape.density = 1
        self.shape.elasticity = 0.7
        space.add(self.body)
    
    # def collision(self, type):
    #     collision_sprites = pygame.sprite.spritecollide(self, self.ring_group, False, pygame.sprite.collide_mask)
    #     if collision_sprites:
    #         for sprite in collision_sprites:
    #         # sprite = collision_sprites[0]
    #             offset_x = self.rect.topleft[0] - sprite.rect.topleft[0]
    #             offset_y = self.rect.topleft[1] - sprite.rect.topleft[1]
    #             relative = sprite.mask.overlap(self.mask, (offset_x, offset_y))
                
    #             # Convert the overlap coordinate into a coordinate on the screen
    #             x = relative[0] + sprite.rect.topleft[0]
    #             y = relative[1] + sprite.rect.topleft[1]
    #             collision = Vector2(x, y)
    #             print('Collision Detected @', collision)
    #             collision_side = sprite.get_closest_side(collision)     # normalized vector 
    #             bounced_velocity = self.velocity.reflect(collision_side)
    #             if type == 'horizontal':
    #                 # Collision is on the right
    #                 if self.rect.right >= collision.x and self.prev_rect.right <= collision.x:
    #                     self.rect.right = collision.x
    #                     self.position.x = collision.x - self.radius
    #                     self.velocity.x = bounced_velocity.x
                        
    #                 # Collision is on the left
    #                 if self.rect.left <= collision.x and self.prev_rect.left >= collision.x:
    #                     self.rect.left = collision.x
    #                     self.position.x = collision.x + self.radius
    #                     self.velocity.x = bounced_velocity.x 
                
    #             if type == 'vertical':
    #                 # Collision is on the bottom
    #                 if self.rect.bottom >= collision.y and self.prev_rect.bottom <= collision.y:
    #                     self.rect.bottom = collision.y
    #                     self.position.y = collision.y - self.radius
    #                     self.velocity.y = bounced_velocity.y
                        
    #                 # Collision is on the top
    #                 if self.rect.top <= collision.y and self.prev_rect.top >= collision.y:
    #                     self.rect.top = collision.y
    #                     self.position.y = collision.y + self.radius
    #                     self.velocity.y = bounced_velocity.y
            
    def update(self, dt):
        self.prev_rect = self.rect.copy()
        self.prev_position = self.position.copy()
        
        # Applying any user input for movement 
        if self.keys_held.count('left'):
            self.velocity.x -= 0.5
        if self.keys_held.count('right'):
            self.velocity.x += 0.5
        if self.keys_held.count('up'):
            # self.velocity.y -= 0.5
            self.body.apply_force_at_local_point([0, -10], [self.radius/2, 0])
        if self.keys_held.count('down'):
            # self.velocity.y += 0.5
            self.body.apply_force_at_local_point([0, 10], [self.radius/2, 0])
        self.position = Vector2(self.body.position)
        
        
        # self.rect.topleft = self.position - Vector2(self.radius)
        
    def draw(self, surface):
        '''
            Draws the ball on the specified surface by first calculating where 
            the topleft is positioned. Necessary because .blit() takes the 
            topleft as the second argument.
        '''
        self.rect.topleft = self.position - Vector2(self.radius)
        surface.blit(self.image, self.rect.topleft) 
        
    def add_key_held(self, key):
        self.keys_held.append(key)
        
    def remove_key_held(self, key):
        self.keys_held.remove(key)
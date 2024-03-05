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
        space.add(self.body, self.shape)
    
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

    def change_color(self, data):
        ''' 
        Change the color of the ball according to the dict item passed in data.
        (color, collision_type)
        '''
        self.color, self.shape.collision_type = data
            
    def update(self, dt):
        ''' 
        Update the ball according to 
            the timestep (dt), 
            the velocity adjustments by checking if shift is being held down or not
        '''
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
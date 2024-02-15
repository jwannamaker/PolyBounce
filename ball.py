'''
    _summary_: Game object class for the player in hexkeys
'''
from utils import *

class Ball(pygame.sprite.Sprite):
    def __init__(self, radius, color=random.choice(list(PALLETE.values()))):
        super().__init__()
        self.radius = radius
        self.color = color
        self.position = Vector2(CENTER)
        
        self.velocity = Vector2()
        self.acceleration = Vector2(GRAVITY)
        
        self.keys_held = []
        
        self.image = pygame.Surface((self.radius * 2, self.radius * 2))
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0, 0, 0))
        
        pygame.draw.circle(self.image, self.color, [self.radius, self.radius], self.radius)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.position - Vector2(self.radius)
        
        self.mask = pygame.mask.from_surface(self.image)
        
    def draw(self, surface):
        '''
            Draws the ball on the specified surface by first calculating where 
            the topleft is positioned. Necessary because .blit() takes the 
            topleft as the second argument.
        '''
        self.rect.topleft = self.position - Vector2(self.radius)
        surface.blit(self.image, self.rect.topleft) 
        
    # def collides_with(self, other):
        # '''
        #     Returns True is the distance from the center of the ball to the center 
        #     of the other object is less than or equal to the sum of their radii.
        # '''
        # distance = self.position.distance_to(other.position)
        # return distance <= self.radius + other.radius
        # return pygame.sprite.collide_mask(self, other)
    
    def update(self, inner_ring):
        # self.acceleration = GRAVITY
        
        # Applying any user input for movement 
        if self.keys_held.count('left'):
            self.velocity.x += -0.5  # Left is -X
        if self.keys_held.count('right'):
            self.velocity.x += 0.5   # Right is +X
        self.position += self.velocity
            
        # Checking if hit left wall, correct position to be within the wall and bounce off
        if self.position.x - self.radius < 0:
            self.position.x = self.radius
            self.velocity.x *= -0.2    # Negative to reverse direction, < 1 to simulate loss of momentum
            
        # Checking if hit right wall
        if self.position.x + self.radius >= SCREEN_SIZE.x:
            self.position.x = SCREEN_SIZE.x - self.radius
            self.velocity.x *= -0.2    # Bounce off with a dampening effect
            
        # Checking if hit top wall
        if self.position.y - self.radius < 0:
            self.position.y = self.radius
            self.velocity.y *= -0.9

        # Checking if hit bottom wall
        if self.position.y + self.radius >= SCREEN_SIZE.y:
            self.position.y = SCREEN_SIZE.y - self.radius
            self.velocity.y *= -0.9
            
        # Checking if hit ring, then bounce off
        collision = pygame.sprite.collide_mask(self, inner_ring)
        if collision:
            offset_x = self.rect.topleft[0] - inner_ring.rect.topleft[0]
            offset_y = self.rect.topleft[1] - inner_ring.rect.topleft[1]
            overlap = inner_ring.mask.overlap_area(self.mask, (offset_x, offset_y))
            
            to_center_x = self.position.distance_to((CENTER.x, 0))
            to_center_y = self.position.distance_to((0, CENTER.y))
            
            self.velocity.x += self.velocity.project(CENTER).x
            self.velocity.y += self.velocity.project(CENTER).y
            self.position -= self.velocity
            # self.velocity.project
            
            # self.position.x += self.velocity.x * np.cos(self.position.x)
            # self.position.y -= self.velocity.y * np.sin(self.position.y)
        else:
            self.velocity += self.acceleration
            

        self.rect.topleft = self.position - Vector2(self.radius)
        
    def add_key_held(self, key):
        self.keys_held.append(key)
        
    def remove_key_held(self, key):
        self.keys_held.remove(key)
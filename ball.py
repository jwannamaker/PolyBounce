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
        
        self.speed = Vector2(0, 0)
        self.direction = Vector2(0, 1)
        self.acceleration = Vector2(GRAVITY)
        
        self.keys_held = []
        
        self.image = pygame.Surface((self.radius * 2, self.radius * 2))
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0, 0, 0))
        
        pygame.draw.circle(self.image, self.color, [self.radius, self.radius], self.radius)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.position - Vector2(self.radius)
        self.prev_rect = self.rect.copy()
        
        self.mask = pygame.mask.from_surface(self.image)
        
    def draw(self, surface):
        '''
            Draws the ball on the specified surface by first calculating where 
            the topleft is positioned. Necessary because .blit() takes the 
            topleft as the second argument.
        '''
        self.rect.topleft = self.position - Vector2(self.radius)
        surface.blit(self.image, self.rect.topleft) 
        
    def move_x(self, dx):
        self.position.x += dx
        
    def move_y(self, dy):
        self.position.y -= dy
        
    # def collides_with(self, other):
        # '''
        #     Returns True is the distance from the center of the ball to the center 
        #     of the other object is less than or equal to the sum of their radii.
        # '''
        # distance = self.position.distance_to(other.position)
        # return distance <= self.radius + other.radius
        # return pygame.sprite.collide_mask(self, other)
    
    def update(self, dt):
        self.prev_rect = self.rect.copy()
        
        self.speed += self.acceleration * dt
        # Applying any user input for movement 
        if self.keys_held.count('left'):
            self.speed.x += 1
        if self.keys_held.count('right'):
            self.speed.x -= 1
            
        # Checking if hit left wall, correct position to be within the wall and bounce off
        if self.position.x - self.radius < 0:
            self.position.x = self.radius
            self.direction.x *= -0.2    # Negative to reverse direction, < 1 to simulate loss of momentum
            
        # Checking if hit right wall
        if self.position.x + self.radius >= SCREEN_SIZE.x:
            self.position.x = SCREEN_SIZE.x - self.radius
            self.direction.x *= -0.2    # Bounce off with a dampening effect
            
        # Checking if hit top wall
        if self.position.y - self.radius < 0:
            self.position.y = self.radius
            self.direction.y *= -0.9

        # Checking if hit bottom wall
        if self.position.y + self.radius >= SCREEN_SIZE.y:
            self.position.y = SCREEN_SIZE.y - self.radius
            self.direction.y *= -0.9
        
        if self.direction.magnitude() != 0:
            self.direction.normalize_ip()
        self.position.x += self.direction.x * self.speed.x * dt
        self.position.y += self.direction.y * self.speed.y * dt
        self.rect.topleft = self.position - Vector2(self.radius)
        
    def add_key_held(self, key):
        self.keys_held.append(key)
        
    def remove_key_held(self, key):
        self.keys_held.remove(key)
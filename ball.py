'''
    _summary_: Game object class for the player in hexkeys
'''
from utils import *

class Ball(pygame.sprite.Sprite):
    def __init__(self, radius, color):
        super().__init__()
        self.radius = radius
        self.color = color
        self.position = Vector2(CENTER)
        
        self.velocity = Vector2()
        self.acceleration = Vector2()
        
        self.keys_held = []
        
        self.image = pygame.Surface((self.radius * 2, self.radius * 2))
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0, 0, 0))
        
        pygame.draw.circle(self.image, self.color, [self.radius, self.radius], self.radius)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.position - Vector2(self.radius)
        
    def draw(self, surface):
        '''
            Draws the ball on the specified surface by first calculating where 
            the topleft is positioned. Necessary because .blit() takes the 
            topleft as the second argument.
        '''
        self.rect.topleft = self.position - Vector2(self.radius)
        surface.blit(self.image, self.rect.topleft) 
        
    def collides_with(self, other):
        '''
            Returns True is the distance from the center of the ball to the center 
            of the other object is less than or equal to the sum of their radii.
        '''
        distance = self.position.distance_to(other.position)
        return distance <= self.radius + other.radius
    
    def update(self):
        self.acceleration = GRAVITY
        self.velocity += self.acceleration
        
        # Applying any user input for movement 
        if self.keys_held.count('left'):
            self.velocity[0] += -0.5  # Left is -X
        if self.keys_held.count('right'):
            self.velocity[0] += 0.5   # Right is +X
        self.position += self.velocity
            
        # Checking if hit left wall, correct position to be within the wall and bounce off
        if self.position[0] - self.radius < 0:
            self.position[0] = self.radius
            self.velocity[0] *= -0.2    # Negative to reverse direction, < 1 to simulate loss of momentum
            
        # Checking if hit right wall
        if self.position[0] + self.radius >= SCREEN_SIZE.x:
            self.position[0] = SCREEN_SIZE.x - self.radius
            self.velocity[0] *= -0.2    # Bounce off with a dampening effect
            
        # Checking if hit top wall
        if self.position[1] - self.radius < 0:
            self.position[1] = self.radius
            self.velocity[1] *= -0.9   

        # Checking if hit bottom wall
        if self.position[1] + self.radius >= SCREEN_SIZE.y:
            self.position[1] = SCREEN_SIZE.y - self.radius
            self.velocity[1] *= -0.9
        
        self.rect.topleft = self.position - Vector2(self.radius)
        
    def add_key_held(self, key):
        self.keys_held.append(key)
        
    def remove_key_held(self, key):
        self.keys_held.remove(key)
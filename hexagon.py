import pygame, random
from hexkey_utils import *

RING_PADDING = 50
RING_SIDES = {
    'up_left', 
    'up', 
    'up_right', 
    'down_right', 
    'down', 
    'down_left'
}
RING_PALLETE = {
    'white': (255, 255, 255),
    'pink': (201, 93, 177),
    'light-purple': (137, 100, 187),
    'blue': (157, 169, 214),
    'light-blue': (170, 224, 241),
    'cyan': (144, 239, 240)
}
SIZE = (300, 300)

class Hexagon(pygame.sprite.Sprite):
    '''Hexagon ring rotates using  A (counterclockwise) and D (clockwise).

    Args:
        pygame (pygame.sprite.Sprite): base class
    '''
    
    
    def __init__(self, radius, N=6, inner_ring=None):
        pygame.sprite.Sprite.__init__(self)
        self.N = N            # number of sides
        self.center = CENTER
        self.radius = radius    
        # self.active = False     # active ==> ball currently inside
        self.theta = self.get_theta()
        self.vertices = self.get_vertices()
        # self.lines = 
        
        # self.base_surface = pygame.display.get_surface()
        self.image = pygame.Surface(SIZE, pygame.SRCALPHA, 32)
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.center.x - self.radius, self.center.y - self.radius)
        self.mask = pygame.mask.from_surface(self.image)  # get the surface from the area bounded by the shape for the mask
        
    
    def get_theta(self):
        return (2 * np.pi) / self.N
    
    def get_vertices(self):
        vertices = []
        for i in range(self.N):
            theta = i * self.theta
            x = (self.radius * np.cos(theta)) + self.center.x
            y = (self.radius * np.sin(theta)) + self.center.y
            vertices.append(pygame.Vector2(x, y))
        return vertices

    def draw(self):
        # TODO Create a transparent surface to draw on
        # new_surface = pygame.Surface.subsurface(self.base_surface, self.center, SIZE)
        # new_surface = pygame.Surface(SIZE, pygame.SRCALPHA, 32)
        
        # TODO Draw the polygon onto the transparent surface
        pygame.draw.aalines(self.image, random.choice(list(RING_PALLETE.values())), False, self.vertices)
        
        
        
    def update(self):
        pygame.draw.aalines(pygame.display.get_surface(), random.choice(list(RING_PALLETE.values())), False, self.vertices)
        
        
        
    def cw_rotate(self):
        # TODO
        pass
        
    def ccw_rotate(self):
        #TODO
        pass
    
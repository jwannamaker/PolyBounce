import pygame
from utils import *

class Polygon(pygame.sprite.Sprite):
    '''Polygon ring rotates using  Q (counterclockwise) and E (clockwise).

    Args:
        pygame (pygame.sprite.Sprite): base class
    '''
    
    def __init__(self, radius, color, N):
        super().__init__()
        self.radius = radius    
        self.color = color
        self.position = Vector2(CENTER)
        self.N = N            # number of sides
        
        self.active = False     # active ==> ball currently inside
        self.keys_held = []
        
        self.theta = self.get_theta()
        self.vertices = self.get_vertices()
        self.image = pygame.Surface((self.radius * 2, self.radius * 2))
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0, 0, 0))
        pygame.draw.lines(self.image, self.color, True, self.vertices)
        self.rect = self.image.get_rect(center = self.position)
        # get the surface from the area bounded by the shape for the mask
        self.mask = pygame.mask.from_surface(self.image)  
    
    def get_theta(self):
        return (2 * np.pi) / self.N
    
    def get_vertices(self):
        vertices = []
        for i in range(self.N):
            theta = i * self.theta
            x = (self.radius * np.cos(theta)) + self.radius
            y = (self.radius * np.sin(theta)) + self.radius
            vertices.append(np.array((x, y)))
        return vertices

    # def get_vectors(self):
    #     vectors = []
    #     for p in self.vertices:
    #         pygame.
    #         vectors.append(self.position.astype(float), p)
    #     return vectors
    
    def draw(self, surface):
        blit_position = self.position - Vector2(self.radius)
        surface.blit(self.image, blit_position)
        
    def update(self):
        # self.rect.x, self.rect.y = self.position.astype(int) - self.radius
        self.rect = pygame.draw.lines(self.image, self.color, True, self.vertices)
        self.rect.topleft = self.position - Vector2(self.radius)
        
    def cw_rotate(self):
        # new_vertices = []
        # for p in self.vertices:
        #     result = np.array((0.0, 0.0))
        #     result = rotate_vector(-1.0 * self.theta / 2.0, p[0], p[1])
        #     new_vertices.append(result)
        # self.vertices = new_vertices
        angle = self.theta / 2.0
        
        
        
    def ccw_rotate(self):
        # new_vertices = []
        # for p in self.vertices:
        #     result = np.array((0.0, 0.0))
        #     result = rotate_vector(self.theta / 2.0, p[0], p[1])
        #     new_vertices.append(result)
        # self.vertices = new_vertices
            
        pass
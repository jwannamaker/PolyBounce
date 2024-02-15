import pygame
from utils import *

class Line(pygame.sprite.Sprite):
    '''
        Represents a line for the side of a Polygon
    '''
    def __init__(self, start, end, image, color, thickness=3):
        super().__init__()
        self.start = Vector2(start)
        self.end = Vector2(end)
        
        self.thickness = thickness
        self.color = color
        
        self.length = self.get_length()
        self.rect = pygame.draw.line(image, self.color, self.start, self.end, self.thickness)
        
        
    def get_length(self):
        return self.start.distance_to(self.end)
    
    

class Polygon(pygame.sprite.Sprite):
    '''Polygon ring rotates using  Q (counterclockwise) and E (clockwise).

    Args:
        pygame (pygame.sprite.Sprite): base class
    '''
    
    def __init__(self, radius, N, color=random.choice(list(PALLETE.values()))):
        super().__init__()
        self.radius = radius    
        self.color = color
        self.position = Vector2(CENTER)
        self.N = N              # number of sides
        
        # self.active = False     # active ==> ball currently inside
        # self.keys_held = []
        
        self.theta = self.get_theta()
        self.vertices = self.get_vertices()
        self.image = pygame.Surface((self.radius * 2, self.radius * 2))
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0, 0, 0))
        # pygame.draw.lines(self.image, self.color, True, self.vertices, 3)
        self.sides = self.draw_lines()
        self.rect = self.image.get_rect(center = self.position)
        
        # get the surface from the area bounded by the shape for the mask
        self.mask = pygame.mask.from_surface(self.image)  
    
    def get_theta(self):
        '''
            Returns the calculation for the internal angle in radians. Used for 
            drawing the vertices of the polygon. Shifted so the first vertex is
            at the top. 
        '''
        return (2 * np.pi) / self.N
    
    def get_vertices(self):
        vertices = []
        for i in range(self.N):
            theta = i * self.theta
            x = (self.radius * np.cos(theta)) + self.radius
            y = (self.radius * np.sin(theta)) + self.radius
            vertices.append(np.array((x, y)))
        return vertices
        
    def draw_lines(self):
        lines = []
        for i in range(0, len(self.vertices)):
            start = self.vertices[i]
            end = self.vertices[i + 1] if i + 1 < len(self.vertices) else self.vertices[0]
            pygame.draw.line(self.image, random.choice(list(RING_PALLETE.values())), start, end, 2)
            lines.append([start, end])
        self.mask = pygame.mask.from_surface(self.image)
        return lines
    
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
        # self.rect = pygame.draw.lines(self.image, self.color, True, self.vertices)
        # self.draw_lines()
        # self.rect.topleft = self.position - Vector2(self.radius)
        pass
        
    def cw_rotate(self):
        # new_vertices = []
        # for p in self.vertices:
        #     result = np.array((0.0, 0.0))
        #     result = rotate_vector(-1.0 * self.theta / 2.0, p[0], p[1])
        #     new_vertices.append(result)
        # self.vertices = new_vertices
        # angle = self.theta / 2.0
        pass
        
        
    def ccw_rotate(self):
        # new_vertices = []
        # for p in self.vertices:
        #     result = np.array((0.0, 0.0))
        #     result = rotate_vector(self.theta / 2.0, p[0], p[1])
        #     new_vertices.append(result)
        # self.vertices = new_vertices
            
        pass
    
    def get_normal_at(self, point):
        # TODO: return the matrix representing the line if the point 'collides' 
        # with a side of this ring 
            
        print(str(point))
import pygame
from utils import *

"""
class PolySegment(pygame.sprite.Sprite):
    '''
        Represents a segment of a polygon. Helps the collision detection, amongst
        many other things.
        
        Requirements: Return some way to determine the slope of the line that 
        the ball has collided with
    '''
    def __init__(self, start, end, color, thickness = 3):
        super().__init__()
        
        self.start = Vector2(start)
        self.end = Vector2(end)
        self.color = color
        self.thickness = thickness
        
    def draw(self, surface):
        pygame.draw.line(surface, self.color, self.start, self.end, self.thickness)
        points = [self.end, (surface.get_rect().centerx, surface.get_rect().centery), self.start]
        pygame.draw.lines(surface, PALLETE['white'], True, points, self.thickness)
        
    def get_length(self):
        return self.start.distance_to(self.end)
    
    def get_normal(self):
        unit_z_vector = Vector3(0, 0, 1)
        side_vector = Vector3(self.end.x - self.start.x, self.end.y - self.start.y, 0)
        normal = unit_z_vector.cross(side_vector)
        print('Side vector:', side_vector, '; Normal Vector:', normal)
        return normal
"""

class Polygon(pygame.sprite.Sprite):
    '''Polygon ring rotates using  Q (counterclockwise) and E (clockwise).

    Args:
        pygame (pygame.sprite.Sprite): base class
    '''
    
    def __init__(self, radius, N, wall_thickness = 50, color = random.choice(list(PALLETE.values()))):
        super().__init__()
        self.radius = radius    
        self.color = color
        self.wall_thickness = wall_thickness
        self.position = Vector2(CENTER)
        self.N = N                  # number of sides

        # self.active = False     # active ==> ball currently inside
        # self.keys_held = []
        
        self.theta = self.get_theta()
        self.vertices = self.get_vertices(self.radius)
        self.inner_vertices = self.get_vertices(self.radius - self.wall_thickness)
        self.image = pygame.Surface((self.radius * 2, self.radius * 2))
        self.image.fill((0, 0, 0))
        self.draw_ring()
        self.image.set_colorkey((0, 0, 0))
        
        self.rect = self.image.get_rect() 
        self.rect.center = self.position
        # get the surface from the area bounded by the shape for the mask
        self.mask = pygame.mask.from_surface(self.image)
    
    def get_theta(self):
        '''
            Returns the calculation for the internal angle in radians. Used for 
            drawing the vertices of the polygon. Shifted so the first vertex is
            at the top. 
        '''
        return (2 * np.pi) / self.N
    
    def get_vertices(self, radius, tilt = 1.5 * np.pi):
        vertices = []
        for i in range(1, self.N + 1):
            x = (radius * np.cos(tilt + self.theta * i)) + self.radius
            y = (radius * np.sin(tilt + self.theta * i)) + self.radius
            vertices.append(Vector2(x, y))
        return vertices
        
    def draw_ring(self):
        pygame.draw.polygon(self.image, random.choice(list(RING_PALLETE.values())), self.vertices)
        pygame.draw.polygon(self.image, (0, 0, 0), self.inner_vertices)
    
    def draw(self, surface):
        blit_position = self.position - Vector2(self.radius)
        surface.blit(self.image, blit_position)
    
    
    
    def get_closest_side(self, point):
        '''
            Returns the two points from the inner vertices that are closest to 
            the passed point.
        '''
        distances = list(map(point.distance_to, self.inner_vertices))
        distances_dict = dict(zip(distances, self.inner_vertices))
        
        # Get the shortest distance from the point to a vertex and remove from distances
        closest_distance = min(distances_dict.keys())
        closest_vertex = distances_dict.pop(closest_distance)
        
        # Get the next shortest distance from the point to the remaining vertices and remove from distances
        next_distance = min(distances_dict.keys())
        next_vertex = distances_dict.pop(next_distance)
        
        # Return the vector representing the slope of the closest side
        return get_slope(Vector2(closest_vertex), Vector2(next_vertex))
    
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
    
    # def get_normal_at(self, point):
    #     # TODO: return the matrix representing the line if the point 'collides' 
    #     # with a side of this ring 
            
    #     print(str(point))
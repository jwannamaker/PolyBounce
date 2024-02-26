'''
    Summary of this file
'''

from utils import *

class Side(pygame.sprite.Sprite):
    '''
        Represents one side of a Polygon. Using for better organization of data.
        
        Inherits Sprite in order to use collision of masks; Kill individual sides
        instead of the whole polygon.
    '''
    def __init__(self, parent, *, prev_side=None, next_side=None, inner_vertices, outer_vertices):
        super().__init__()
        self.prev_side = prev_side
        self.next_side = next_side
        self.points = [inner_vertices[0], outer_vertices[1], outer_vertices[0], outer_vertices[1]]
        self.color = self.get_color()
        self.shape = pymunk.Poly(self.parent.body, self.points, radius=1)
        
        # sprite attributes
        self.image = self.parent.get_subsurface() # as a subsurface, the colorkey should already be set
        self.draw()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.parent.mask.draw(self.mask, (0, 0))    # add this mask to the parent mask
        
    def get_color(self):
        color = pygame.Color(255, 0, 0, 255) # bc RED is a good error color to me
        if self.prev_side and self.next_side:
            while color == self.prev_side.color or color == self.next_side.color:
                color.update(random.choice(list(RING_PALLETE.values())))
        else:
            color.update(random.choice(list(RING_PALLETE.values())))
        return color
    
    def draw(self):
        gfxdraw.filled_polygon(self.image, self.shape.get_vertices(), self.color)
        
        
        
class Polygon(pygame.sprite.Sprite):
    '''Polygon ring rotates using  Q/A (counterclockwise) and E/D (clockwise).

    Args:
        pygame (pygame.sprite.Sprite): base class
    '''
    
    def __init__(self, space, radius, N, wall_thickness=50):
        super().__init__()
        self.radius = radius
        self.N = N          
        self.wall_thickness = wall_thickness

        # self.active = False     # active ==> ball currently inside
        self.rotation_state = None
        
        # Calculated properties
        self.inner_radius = self.radius - self.wall_thickness
        self.position = Vector2(CENTER)
        self.theta = (2 * np.pi) / self.N   # Internal angle in radians
        
        # Pygame properties
        self.image = pygame.Surface((self.radius * 2, self.radius * 2))
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0, 0, 0))
        self.vertices = self.get_vertices(self.radius, self.radius)
        self.inner_vertices = self.get_vertices(self.inner_radius, self.radius)
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        # self.draw_ring()
        self.mask = pygame.mask.from_surface(self.image)
        self.color_sides()
        
        # pymunk setup
        # TODO: figure out how to deal with Kinematic body types so it can rotate
        # but otherwise behave like a static body type
        self.body = pymunk.Body(0, 0, pymunk.Body.STATIC)
        self.body.position = float(CENTER.x), float(CENTER.y)
        sides = self.get_vertices(self.inner_radius)
        Polygon.attach_segments(sides, self.body, space)
    
    def get_vertices(self, radius, offset=0, tilt=-np.pi/2):
        ''' 
            Offset represents the offset of the center of the regular polygon 
            vertices generated from this method.
        '''
        vertices = []
        for i in range(1, self.N + 1):
            x = (radius * np.cos(tilt + self.theta * i)) + offset
            y = (radius * np.sin(tilt + self.theta * i)) + offset
            vertices.append(Vector2(x, y))
        return vertices
        
    def get_sides(self):
        '''
            This method organizes all the necessary properties of each side into
            a list attribute of this Polygon.
        '''
        self.sides.append(Side(self, ))
        for i in range(self.N):
            self.sides.append()
        
    
    @staticmethod
    def attach_segments(vertices, body, space):
        '''
            Returns the line segments connecting all the passed vertices together,
            adding to the specified body and making all segments neighbors.
            
            Effectively creates a polygon for pymunk purposes.
        '''
        space.add(body)
        for i in range(len(vertices)):
            j = i + 1 if i < len(vertices)-1 else 0
            point_a = vertices[i][0], vertices[i][1]
            point_b = vertices[j][0], vertices[j][1]
            segment = pymunk.Segment(body, point_a, point_b, 1)
            segment.set_neighbors(point_a, point_b) # there is a neighbor present at both endpoints of this segment
            segment.density = 100
            segment.elasticity = 0.5
            segment.friction = 0.7
            space.add(segment)
        # return segment_list
    
    def get_subsurface(self):
        return self.image.subsurface((0, 0, self.radius * 2, self.radius * 2))
    
    def draw(self, surface):
        blit_position = self.position - Vector2(self.radius)
        surface.blit(self.image, blit_position)
    
    def update(self, dt):
        '''
            Updates each side of the polygon
        '''
        
        
        # TODO Apply some amount of rotation if needed, checking in self.rotation_state
        
    def cw_rotate(self, dt):
        print(f'Applying angular velocity of {dt} for time length {dt}')
        
    def ccw_rotate(self, dt):   
        print(f'Applying angular velocity of {dt} for time legnth {dt}')
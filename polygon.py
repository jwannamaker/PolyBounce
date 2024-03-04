'''
polygon.py contains the definition for the Polygon class and the Side class.
'''

from utils import *

class Side(pygame.sprite.Sprite):
    '''
        Represents one side of a Polygon. Using for better organization of data.
        
        Inherits Sprite in order to use collision of masks; Kill individual sides
        instead of the whole polygon.
    '''
    def __init__(self, parent, *, points):
        super().__init__()
        self.parent = parent
        self.points = points
        
        # pymunk setup
        self.shape = pymunk.Poly(self.parent.body, self.points, radius=1)
        self.shape.density = 1
        self.shape.elasticity = 0.4
        self.shape.friction = 0.4
        
        # pygame setup, sprite attributes
        self.image = self.parent.get_subsurface()   # new surface inherits palette, colorkey, and alpha settings
        self.color = random.choice(list(RING_PALLETE.values()))
        self.draw()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.parent.mask.draw(self.mask, (0, 0))    # add this mask to the parent mask
        
        # game logic
        
            
    def add_neighbor(self, type, neighbor):
        pass    
    
    def update_color(self, prev_side, next_side):
        '''
        Returns a random color that doesn't match either the color of the 
        previous side or the color of the next side (if either are provided).
        '''
        color = self.color        # stays that same if conditions are already met
        # bumps out of loop once the color is NOT equal to previous color AND NOT 
        # equal to next color
        while color == prev_side.color or color == next_side.color:
            color = random.choice(list(RING_PALLETE.values()))
        self.color = color
    
    def draw(self):
        gfxdraw.filled_polygon(self.image, self.shape.get_vertices(), self.color)
        
        
        
class Polygon(pygame.sprite.Sprite):
    '''
    Polygon ring rotates using  Q/A (counterclockwise) and E/D (clockwise).
    '''
    
    def __init__(self, space, radius, N, wall_thickness=50):
        super().__init__()
        self.radius = radius
        self.N = N          
        self.wall_thickness = wall_thickness
        
        # Calculated properties
        self.inner_radius = self.radius - self.wall_thickness
        self.position = Vector2(CENTER)
        self.theta = (2 * np.pi) / self.N   # Internal angle in radians
        
        # pymunk setup
        # TODO: figure out how to deal with Kinematic body types so it can rotate
        # but otherwise behave like a static body type
        self.body = pymunk.Body(0, 0, pymunk.Body.STATIC)
        self.body.position = float(CENTER.x), float(CENTER.y)
        sides = self.get_vertices(self.inner_radius)
        Polygon.attach_segments(sides, self.body, space)

        # Game logic setup
        self.rotating = False
        
        # Pygame properties
        self.image = pygame.Surface((self.radius * 2, self.radius * 2))
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0, 0, 0))
        self.vertices = self.get_vertices(self.radius, self.radius)
        self.inner_vertices = self.get_vertices(self.inner_radius, self.radius)
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        self.mask = pygame.mask.from_surface(self.image)
        self.sides = []
        self.get_sides()
    
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
        for i in range(self.N):
            j = i + 1 if i < self.N - 1 else 0
            inner = (self.inner_vertices[i][0], self.inner_vertices[i][1]), (self.inner_vertices[j][0], self.inner_vertices[j][1])
            outer = (self.vertices[i][0], self.vertices[i][1]), (self.vertices[j][0], self.vertices[j][1])
            new_side = Side(self, points=[inner[0], inner[1], outer[0], outer[1]])
            self.sides.append(new_side)
            
        # updating all the colors so that none of them have the same color adjacent
        # TODO fix this to include 'weight's for each color choice. All unique
        prev = self.N - 1
        curr = 0
        next = 1
        for i in range(self.N):
            curr = (curr + 1) % self.N
            prev = (prev + 1) % self.N
            next = (next + 1) % self.N
            self.sides[curr].update_color(self.sides[prev], self.sides[next])
    
    @staticmethod
    def attach_segments(vertices, body, space):
        '''
            Returns the line segments connecting all the passed vertices together,
            adding to the specified body and making all segments neighbors.
            
            Effectively creates a polygon for pymunk purposes.
        '''
        space.add(body)
        for i in range(len(vertices)):
            j = i + 1 if i < len(vertices) - 1 else 0
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
        '''
            The returned subsurface inherits the colorkey, palette, and alpha 
            settings of this surface.
        '''
        return self.image.subsurface((0, 0, self.radius * 2, self.radius * 2))
    
    def draw(self, surface):
        for side in self.sides:
            side.draw()
        
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

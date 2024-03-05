'''
polygon.py contains the definition for the Polygon class and the Side class.
'''

from utils import *
from side import Side


class Polygon(pygame.sprite.Sprite):
    '''
    Polygon ring rotates using  Q/A (counterclockwise) and E/D (clockwise).
    **Is not a sprite, but contains a group of sprites?
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
        self.space = space
        self.body = pymunk.Body(0, 0, pymunk.Body.STATIC)
        self.body.position = float(CENTER.x), float(CENTER.y)
        Polygon.attach_segments(self.get_vertices(self.inner_radius), self.body, space)

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
        self.space.add(self.body)
        for i in range(self.N):
            j = i + 1 if i < self.N - 1 else 0
            inner = (self.inner_vertices[i][0], self.inner_vertices[i][1]), (self.inner_vertices[j][0], self.inner_vertices[j][1])
            outer = (self.vertices[i][0], self.vertices[i][1]), (self.vertices[j][0], self.vertices[j][1])
            new_side = Side(self, points=[inner[0], inner[1], outer[0], outer[1]])
            self.sides.append(new_side)
            self.space.add(new_side.shape)
        
        # updating all the colors so that none of them have the same color adjacent
        prev = 0
        curr = 1
        for i in range(self.N):
            curr += 1 % self.N - 1 
            prev += 1 % self.N - 1
            self.sides[curr].update_color(self.sides[prev])
    
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

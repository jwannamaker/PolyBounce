'''
polygon.py contains the definition for the Polygon class and the Side class.
'''

from utils import *

class Side(NamedTuple):
    '''
    Represents one side of a Polygon. Using for better organization of data.
    '''
    color: pygame.Color
    shape: pymunk.Shape
            
class SideSprite(pygame.sprite.Sprite):
    ''' 
    IDK if i reALLY need this class in particular? ig I'll be finding out ??
    Inherits Sprite in order to use collision of masks; Kill individual sides
    instead of the whole polygon.
    '''
    def __init__(self):
        super().__init__()
    
    def update(self):
        pass
    
    def draw(self):
        gfxdraw.filled_polygon(self.image, self.shape.get_vertices(), self.color)
        
        
class Polygon(pygame.sprite.Sprite):
    '''
    Polygon ring rotates using  Q/A (counterclockwise) and E/D (clockwise).
    **Holds a group of sprites as a dict for the sides
    '''
    
    def __init__(self, space: pymunk.Space, radius: int, N: int, wall_thickness=50):
        super().__init__()
        self.radius = radius
        self.N = N          
        self.wall_thickness = wall_thickness
        
        # Calculated properties
        self.position = Vector2(CENTER)
        self.theta = (2 * np.pi) / self.N               # Exterior angle in radians
        self.inner_radius = self.radius - self.wall_thickness
        
        # pymunk setup
        # TODO: figure out how to deal with Kinematic body types so it can rotate
        # but otherwise behave like a static body type
        self.space = space
        self.body = pymunk.Body(0, 0, pymunk.Body.STATIC)
        self.body.position = float(CENTER.x), float(CENTER.y)
        attach_segments(self.get_vertices(self.inner_radius), self.body, self.space)

        # Game logic setup
        self.angle = 0              # Angle of rotation of the whole polygon
        self.rotating = False       # State of rotation of the whole polygon
        
        # Pygame.Sprite properties
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
        
    def get_side_colors(self):
        random.shuffle(POLY_PALLETE)
        return random.sample(POLY_PALLETE, self.N)
    
    def get_sides(self):
        '''
            This method organizes all the necessary properties of each side into
            a datastructure of this Polygon.
        '''
        colors = self.get_side_colors()
        for i in range(self.N):
            j = i + 1 if i < self.N - 1 else 0
            inner = (self.inner_vertices[i][0], self.inner_vertices[i][1]), (self.inner_vertices[j][0], self.inner_vertices[j][1])
            outer = (self.vertices[i][0], self.vertices[i][1]), (self.vertices[j][0], self.vertices[j][1])
            points = [inner[0], inner[1], outer[0], outer[1]]
            
            # pymunk setup
            side_shape = pymunk.Poly(self.body, points, radius=1)
            side_shape.density = 1
            side_shape.elasticity = 0.4
            side_shape.friction = 0.4
            
            # pygame setup, sprite attributes
            side_sprite = pygame.sprite.Sprite(self.groups())
            side_sprite.update = self.update    # not sure if this line is really going to work
            side_sprite.image = self.get_subsurface()   # new surface inherits palette, colorkey, and alpha settings
            self.draw_side()
            self.rect = self.image.get_rect()
            mask = pygame.mask.from_surface(self.image)
            self.mask.draw(mask, (0, 0))    # add this mask to the parent mask
            
            # game logic setup
            # using the color of the side to determine the collision type
            side_shape.collision_type = POLY_PALLETE[colors[i]]
        
            new_side = Side(side_shape, side_sprite)
            self.sides.append(new_side)
        self.space.add(self.body)
    
    def get_subsurface(self):
        '''
            The returned subsurface inherits the colorkey, palette, and alpha 
            settings of this surface.
        '''
        return self.image.subsurface((0, 0, self.radius * 2, self.radius * 2))
    
    def get_color_at(self, x, y):
        '''
            Get the color at the given x and y coordinates using pymunk utils and
            pygame masks
        '''
        local_coord = pymunk.pygame_util.from_pygame((x, y))
        return self.image.get_at(local_coord)
    
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
        pass
        
    def ccw_rotate(self, dt):   
        pass

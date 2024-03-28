'''
polygon.py contains the definition for the Polygon class and the Side class.
'''

from polybounce.utils import *
from polybounce.entity import PhysicsEntity

class Side(NamedTuple):
    '''
    Represents one side of a Polygon. Using for better organization of data.
    '''
    color: pygame.Color
    shape: pymunk.Shape
    
class Polygon(PhysicsEntity):
    '''
    Polygon ring rotates using  Q/A (counterclockwise) and E/D (clockwise).
    **Holds a group of sprites as a dict for the sides
    '''
    def __init__(self, radius: int, N: int, wall_thickness=50):
        super().__init__(radius)
        self.N = N          
        self.wall_thickness = wall_thickness
        self.theta = (2 * np.pi) / self.N         # Exterior angle in radians
        self.inner_radius = self.radius - self.wall_thickness
 
        # pymunk setup
        self.body.body_type = pymunk.Body.KINEMATIC
        attach_segments(self.get_vertices(self.inner_radius), self.body, self.space)
        self.vertices = self.get_vertices(self.radius, self.radius)
        self.inner_vertices = self.get_vertices(self.inner_radius, self.radius)
        
        self.sides = []
        self.get_sides()
        
        self.rotating = False       # State of rotation of the whole polygon
        
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
            a datastructure of this Polygon.
        '''
        colors = get_shuffled_colors(self.N)
        for i, color in enumerate(colors):
            j = i + 1 if i < self.N - 1 else 0
            inner = (self.inner_vertices[i][0], self.inner_vertices[i][1]), (self.inner_vertices[j][0], self.inner_vertices[j][1])
            outer = (self.vertices[i][0], self.vertices[i][1]), (self.vertices[j][0], self.vertices[j][1])
            points = [inner[0], inner[1], outer[0], outer[1]]
            
            # pymunk setup
            side_shape = pymunk.Poly(self.body, points, radius=1)
            side_shape.filter = pymunk.ShapeFilter(group=1)
            
            # pygame setup, sprite attributes
            side_sprite = pygame.sprite.Sprite()
            
             # new surface inherits palette, colorkey, and alpha settings
            side_sprite.image = self.image.subsurface((0, 0, self.radius * 2, self.radius * 2))
            self.mask.draw(side_sprite.mask, (0, 0))    # add this mask to the polygon mask
            
            # game logic setup
            # using the color of the side to determine the collision type
            side_shape.collision_type = PALLETE_DICT[color].collision_type
        
            new_side = Side(pygame.Color(PALLETE_DICT[color].value), side_shape, side_sprite)
            self.sides.append(new_side)
    
    def get_color_at(self, x, y):
        '''
            Get the color at the given x and y coordinates using pymunk utils and
            pygame masks
        '''
        local_coord = pymunk.pygame_util.from_pygame((x, y))
        return self.image.get_at(local_coord)
    
    def draw_side(self, side):
        gfxdraw.filled_polygon(side.sprite.image, side.shape.get_vertices(), side.color)
    
    def draw(self, surface):
        for side in self.sides:
            side.draw()
    
    def update(self, dt):
        '''
            Updates each side of the polygon
        '''
        
        
        # TODO Apply some amount of rotation if needed, checking in self.rotation_state
        
    def cw_rotate(self, dt):
        if self.rotating:
            self.body.angular_velocity = max(20, self.body.angular_velocity + 1)
        rotating = False
        
    def ccw_rotate(self, dt):   
        if self.rotating:
            self.body.angular_velocity = min(-20, self.body.angular_velocity - 1)
        rotating = False

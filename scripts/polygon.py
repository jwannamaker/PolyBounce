'''
polygon.py contains the definition for the Polygon class and the Side class.
'''

import numpy as np
from scripts.utils import *
from scripts.entity import PhysicsEntity

class Side(PhysicsEntity):
    def __init__(self, polygon: PhysicsEntity, points, color):
        super().__init__(polygon.game, polygon.radius, polygon.position)
        self.body = polygon.body
        self.shape = pymunk.Poly(polygon.body, points, get_color(color))
        super().set_physics_properties()
        
        self.image = polygon.get_subsurface()
        self.color = color
        super().set_visual_properties()
    
    def update(self):
        pass
    
        
class Polygon(PhysicsEntity):
    '''
    Polygon ring rotates using  Q/A (counterclockwise) and E/D (clockwise).
    **Holds a group of sprites for the sides
    '''
    def __init__(self, game, radius, N, wall_thickness=50):
        super().__init__(game, radius, CENTER)
        self.N = N          
        self.wall_thickness = wall_thickness
        self.theta = (2 * np.pi) / self.N         # Exterior angle in radians
        self.inner_radius = self.radius - self.wall_thickness
 
        self.vertices = self.get_vertices(self.radius, self.radius)
        self.inner_vertices = self.get_vertices(self.inner_radius, self.radius)
        
        
        self.sides = pygame.sprite.Group()
        self.get_side_bricks()
        
        self.body.moment = pymunk.moment_for_circle(100, self.inner_radius, self.radius)
        self.body.shape = pymunk.Circle(self.body, self.radius, self.position)
        self.body.shape.sensor = True
        super().set_physics_properties()
        
        # self.sides = {}
        # self.get_sides()
        
        self.start_angle = self.body.angle
        self.rotating = False       # rotation process complete or not per one keypress
        
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
    
    def get_subsurface(self):
        ''' New surface inherits palette, colorkey, and alpha settings. '''
        return self.image.subsurface((0, 0), (self.radius * 2, self.radius * 2))
    
    def get_side_bricks(self):
        colors = get_shuffled_colors(self.N)
        for i, color in enumerate(colors):
            j = i + 1 if i < self.N - 1 else 0
            inner = (self.inner_vertices[i].x, self.inner_vertices[i].y), (self.inner_vertices[j].x, self.inner_vertices[j].y)
            outer = (self.vertices[i].x, self.vertices[i].y), (self.vertices[j].x, self.vertices[j].y)
            points = [inner[0], inner[1], outer[0], outer[1]]
            
            new_side = create_brick(self, points, color)
            
            self.sides.add(new_side)
            print('new side:', i, color)
    
    def get_color_at(self, x, y):
        local_coord = pymunk.pygame_util.from_pygame((x, y))
        return self.image.get_at(local_coord)
    
    def draw_side(self, side):
        gfxdraw.filled_polygon(side.sprite.image, side.shape.get_vertices(), side.color)
        
    def cw_rotate(self, dt):
        if self.rotating:
            self.body.angular_velocity = max(20, self.body.angular_velocity + 1)
        
    def ccw_rotate(self, dt):   
        if self.rotating:
            self.body.angular_velocity = min(-20, self.body.angular_velocity - 1)
        

'''
polygon.py contains the definition for the Polygon class and the Side class.
'''

import numpy as np
from scripts.utils import *
from scripts.entity import PhysicsEntity

class Side(NamedTuple):
    sprite: pygame.sprite.Sprite
    shape: pymunk.Shape

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
        self.sides = {} # key: color (str)
                        # value: Side NamedTuple(sprite, shape)
        self.get_sides()
        self.body.moment = pymunk.moment_for_circle(100, self.inner_radius, self.radius)
        super().set_physics_properties('non-player')
        super().set_visual_properties()
        
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
    
    def get_color_at(self, x, y):
        local_coord = pymunk.pygame_util.from_pygame((x, y))
        return self.image.get_at(local_coord)
    
    def get_sides(self):
        colors = get_shuffled_colors(self.N)
        for i, color in enumerate(colors):
            j = i + 1 if i < self.N - 1 else 0
            inner = (self.inner_vertices[i].x, self.inner_vertices[i].y), (self.inner_vertices[j].x, self.inner_vertices[j].y)
            outer = (self.vertices[i].x, self.vertices[i].y), (self.vertices[j].x, self.vertices[j].y)
            points = [inner[0], inner[1], outer[0], outer[1]]
            
            new_shape = self.create_side_shape(color, points)
            new_sprite = self.create_side_sprite(color, points)
            self.sides[color] = Side(sprite=new_sprite, shape=new_shape)
    
    
    def create_side_shape(self, color, points):
        ''' Creates a shape (pymunk.Poly), adding it the body of the polygon and returns it. '''
        side_shape = pymunk.Poly(self.body, points, radius=1)
        side_shape.collision_type = get_collision_type(color)
        return side_shape
    
    def create_side_sprite(self, color, points):
        ''' Uses the points to create a subsprite and returns it. '''
        side = pygame.sprite.Sprite()
        side.image = self.get_subsurface()
        gfxdraw.filled_polygon(side.image, points, get_color(color))
        side.rect = side.image.get_rect()
        side.mask = pygame.mask.from_surface(side.image)
        return side
        
    def remove_side(self, side: Side):
        pass
    
    def cw_rotate(self, dt):
        if self.rotating:
            self.body.angular_velocity = max(20, self.body.angular_velocity + 1)
        
    def ccw_rotate(self, dt):   
        if self.rotating:
            self.body.angular_velocity = min(-20, self.body.angular_velocity - 1)
        
    def render(self):
        for side in self.sides.values():
            print(side.shape.get_vertices())

        self.game.screen.blit(self.image, self.rect.topleft)
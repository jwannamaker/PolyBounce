'''
polygon.py contains the definition for the Polygon class and the Side class.
'''

import numpy as np
from scripts.utils import *
from scripts.entity import PhysicsEntity


class Polygon(PhysicsEntity):
    '''
    Polygon ring rotates using  Q/A (counterclockwise) and E/D (clockwise).
    **Holds a group of sprites for the sides
    '''
    def __init__(self, game, groups, radius, N, entity_type='non-player'):
        super().__init__(game, groups, radius, entity_type)
        self.N = N          
        self.wall_thickness = 50
        self.theta = (2 * np.pi) / self.N         # Exterior angle in radians
        self.inner_radius = self.radius - self.wall_thickness
        self.vertices = self.get_vertices(self.radius)
        self.inner_vertices = self.get_vertices(self.inner_radius)
        
        self.side_sprites = pygame.sprite.Group()
        self.side_shapes = []
        self.get_sides()
        
        super().set_visual_properties()
        super().set_physics_properties()
        # self.body.moment = pymunk.moment_for_circle(100, self.inner_radius, self.radius)
        self.body.body_type = pymunk.Body.KINEMATIC
        self.start_angle = self.body.angle
        self.rotating = False       # rotation process complete or not per one keypress
        
    def get_vertices(self, radius):
        ''' 
            Offset represents the offset of the center of the regular polygon 
            vertices generated from this method.
        '''
        offset_x = self.radius
        offset_y = self.radius
        tilt = (np.pi - self.theta) / 2
        vertices = []
        for i in range(1, self.N + 1):
            x = (radius * np.cos(tilt + self.theta * i)) + offset_x
            y = (radius * np.sin(tilt + self.theta * i)) + offset_y
            vertices.append((x, y))
        return vertices
    
    def get_subsurface(self):
        ''' New surface inherits palette, colorkey, and alpha settings. '''
        return self.image.subsurface((0, 0, self.radius * 2, self.radius * 2))
    
    def get_color_at(self, x, y):
        local_coord = pymunk.pygame_util.from_pygame((x, y))
        return self.image.get_at(local_coord)
    
    def get_sides(self):
        colors = get_shuffled_colors(self.N)
        for i, color in enumerate(colors):
            j = i + 1 if i < self.N - 1 else 0
            inner = [self.inner_vertices[i], self.inner_vertices[j]]
            outer = [self.vertices[i], self.vertices[j]]
            points = [inner[0], outer[0], outer[1], inner[1]]
            
            new_shape = self.create_side_shape(color, points)
            new_sprite = self.create_side_sprite(color, points)
            
            self.side_sprites.add(new_sprite)
            self.side_shapes.append(new_shape)

    
    def create_side_shape(self, color, points):
        ''' Creates a shape (pymunk.Poly), adding it the body of the polygon and returns it. '''
        side_shape = pymunk.Poly(self.body, points, radius=1)
        side_shape.collision_type = get_collision_type(color)
        
        return side_shape
    
    def create_side_sprite(self, color, points):
        ''' Uses the points to create an image and a rect and returns it. '''
        side = pygame.sprite.Sprite()
        side.image = self.get_subsurface()
        gfxdraw.filled_polygon(side.image, points, get_color(color))
        side.rect = side.image.get_rect()
        side.mask = pygame.mask.from_surface(side.image)
        return side
        
    def remove_side(self, color):
        pass
    
    def cw_rotate(self, dt):
        if self.rotating:
            self.body.angular_velocity = max(20, self.body.angular_velocity + 1)
        
    def ccw_rotate(self, dt):   
        if self.rotating:
            self.body.angular_velocity = min(-20, self.body.angular_velocity - 1)
        
    def render(self):
        for side in self.side_sprites:
            self.game.screen.blit(side.image, self.rect.topleft)
        self.game.screen.blit(self.image, self.rect.topleft)


# class Side(PhysicsEntity):
#     def __init__(self, polygon: Polygon, start_angle, end_angle, color, entity_type='non-player'):
#         super().__init__(polygon.game, polygon.groups, polygon.radius, start_angle, end_angle, )
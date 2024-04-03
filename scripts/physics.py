import pymunk
from pymunk import pygame_util

from entity import Entity
from player import Player
from enemy import Enemy
from ui import UI

class PhysicsEngine:
    """ Handles creation and updating of all game objects that need to be 
    physically simulated. Provides easy access to the Pymunk processes for my 
    purposes, without making other classes or functions overly complex. 
    """
    def __init__(self, ui_type):
        self.ui_type = ui_type
        self.space = pymunk.Space()
        self.space.gravity = (0, 1500)
        
        screen_corners = [(0, 0), 
                          (0, ui_type.SCREEN_SIZE.y), 
                          (ui_type.SCREEN_SIZE.x, ui_type.SCREEN_SIZE.y), 
                          (ui_type.SCREEN_SIZE.x, 0)]
        self.create_walls(screen_corners)
        
        # Now that all the game objects are created, I can add collision handling for them
        self.handler = self.space.add_collision_handler(1, 2) # 1 - ball, 2 - nonball ---> Can easily transition into using bitmasking for this
        self.handler.data['ball'] = self.player_ball
        self.handler.data['inner_ring'] = self.inner_ring
        self.handler.begin = PhysicsEngine.begin
        self.handler.pre_solve = PhysicsEngine.pre_solve
        self.handler.post_solve = PhysicsEngine.post_solve
        self.handler.separate = PhysicsEngine.separate
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
           
    def get_collision_type(self, color_str, entity_type):
        """ Generates a bitmask given the entity type and the color.
        """
        return self.ui_type.PALLETE[color_str]

    def add_to_space(self, body, shape):
        """ Every body starts in the center of the screen. """
        body.position = [float(self.ui_type.CENTER.x), float(self.ui_type.CENTER.y)]

        shape.elasticity = 0.999
        shape.friction = 0.67
        self.space.add(body, shape)
            
    
    def create_walls(self, corners):
        """ The body is already added to the space, since we access the given
        static_body.
        
        We give the radius of 3 and set the neighbors to get the generated
        Segments to play nicely with each other and not get the other Shapes/
        Bodies caught on weird geometries.
        """
        for i in range(len(corners)):
            j = (i + 1) % len(corners)
            segment = pymunk.Segment(self.space.static_body, corners[i], corners[j], 3)
            segment.set_neighbors(corners[i], corners[j]) 
            segment.density = 100
            segment.elasticity = 0.999
            segment.friction = 0.49
            self.space.add(segment) 
            # I know, I'm not calling self.add_to_space() 
            # I wish I was 
            # but it's gonna work out nice and easy like that. 
            # Shhhhh, it's okay. Don't worry about this little thing.
                   
    def attach_segments(self, vertices, body):
        """ Returns the line segments connecting all the passed vertices
        together, adding to the specified body and making all segments 
        neighbors. Effectively creates a non-filled polygon from line segments 
        for pymunk.
        """
        segment_list = []
        self.space.add(body)
        for i in range(len(vertices)):
            j = i + 1 if i < len(vertices) - 1 else 0
            point_a = vertices[i][0], vertices[i][1]
            point_b = vertices[j][0], vertices[j][1]
            segment = pymunk.Segment(body, point_a, point_b, 3)
            
            # Neighbor present at both endpoints of this segment
            segment.set_neighbors(point_a, point_b) 
            segment.density = 100
            segment.elasticity = 1
            segment.friction = 0.7
            segment.collision_type = 2  # NOT ball type
            segment_list.append(segment)
        self.space.add(*segment_list)
    
    def create_circle(self, radius):
        mass = pymunk.area_for_circle(inner_radius=0, outer_radius=radius) * 2
        moment = pymunk.moment_for_circle(mass, inner_radius=0, outer_radius=radius)
        circle_body = pymunk.Body(mass, moment)
        circle_shape = pymunk.Circle(circle_body, radius)
        self.add_to_space(circle_body, circle_shape)
     
    def create_side(self, points):
        """ The mass and moment here are really just symbolic, since they don't 
        get used for a KINEMATIC body_type. I wanted them here for strictly
        reference and completion.
        """
        mass = pymunk.area_for_poly(points)
        moment = pymunk.moment_for_poly(mass, points)
        side_body = pymunk.Body(mass, moment, pymunk.Body.KINEMATIC)
        side_shape = pymunk.Poly(body=side_body, 
                                 vertices=points, 
                                 transform=pymunk.Transform.translated(), radius=1)
        self.add_to_space(side_body, side_shape)
    
    @staticmethod
    def begin(arbiter: pymunk.Arbiter, space: pymunk.Space, data: dict):
        print('Collision began this step')
        print('Must get from pygame mask collision now what the s are')
        print('Then populate the data dict with that collision information')
        collision_ = data['inner_ring'].get_at(arbiter.contact_point_set)
        data['ball'] = 'ball obj placeholder'
        data['side'] = 'side obj placeholder'

    @staticmethod
    def pre_solve(arbiter: pymunk.Arbiter, space: pymunk.Space, data: dict):
        print('pre_solve')

    @staticmethod
    def post_solve(arbiter: pymunk.Arbiter, space: pymunk.Space, data: dict):
        print('post_solve')
    
    @staticmethod
    def separate(arbiter: pymunk.Arbiter, space: pymunk.Space, data: dict):
        print('separate')
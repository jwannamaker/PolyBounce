from typing import Optional

import pymunk
from pymunk import pygame_util
import pygame
from pygame import Surface

from scripts.asset import Asset, BOX

''''
class EventHandler(NamedTuple):
    """ EventHandler bundles together the Asset (the observer to event changes) 
    with the function that will be called when the event occurs.
    """
    asset: Asset
    event_func: callable
    
    def run_event(self, data):
        self.asset.event_func(data)
    
class EventManager:
    """ EventManager allows the use of a subscription model for changes. It uses
    EventHandlers that get triggered when a certain 'event_type' is passed to 
    (method) notify_observers 
    """
    def __init__(self):
        self.observers: dict[str, set[EventHandler]] = {}
    
    def attach_observer(self, event_type: str, handler: EventHandler):
        self.observers[event_type] = handler
    
    def detach_observer(self, event_type: str, handler: EventHandler):
        if event_type in self.observers:
            self.observers[event_type].remove(handler)
        
    def notify_observers(self, event_type, data):
        if event_type in self.observers:
            for handler in self.observers[event_type].value():
                handler.run_event(data)
'''

class Singleton(type):
    _instance = None
    
    def __call__(cls, *args, **kwargs):
        if cls is not cls._instance:
            cls._instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instance

class PhysicsEngine(metaclass=Singleton):
    """ Handles creation and updating of all game objects that need to be 
    physically simulated. Provides easy access to the Pymunk processes for my 
    purposes, without making other classes or functions overly complex. 
    """
    
    space = pymunk.Space()
    space.gravity = (0, 1200)
    collision_handlers = []
    observers: dict[list[Asset]] = {}
        
    def add_collision_handler(shape, other_shape):
        """ TODO: Generates a bitmask given the entity type and the color. """
        handler = PhysicsEngine.space.add_collision_handler(1, 2)
        handler.begin = PhysicsEngine.begin
        handler.pre_solve = PhysicsEngine.pre_solve
        handler.post_solve = PhysicsEngine.post_solve
        handler.separate = PhysicsEngine.separate
        PhysicsEngine.collision_handlers.append(handler)

    def add_to_space(position: tuple[float, float], body: pymunk.Body, shape: pymunk.Shape):
        body.position = list(position)
        shape.elasticity = 0.999
        shape.friction = 0.45
        PhysicsEngine.space.add(body, shape)
    
    def create_walls(screen_size: tuple[int, int]):
        """ The body is already added to the space, since we access the given
        static_body.
        """
        corners = BOX(screen_size[0], screen_size[1]).get_corners()
        for i in range(len(corners)):
            j = (i + 1) % len(corners)
            segment = pymunk.Segment(PhysicsEngine.space.static_body, corners[i], corners[j], 1)
            segment.set_neighbors(corners[i], corners[j]) 
            segment.density = 100
            segment.elasticity = 0.999
            segment.friction = 0.49
            PhysicsEngine.space.add(segment)
                   
    def attach_segments(vertices: list[tuple[float, float]], body: pymunk.Body):
        """ Returns the line segments connecting all the passed vertices
        together, adding to the specified body and making all segments 
        neighbors. Effectively creates a non-filled polygon from line segments 
        for pymunk.
        """
        segment_list = []
        PhysicsEngine.space.add(body)
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
            segment.collision_type = 2  # TODO: more specific collision filters
            segment_list.append(segment)
        PhysicsEngine.space.add(*segment_list)
    
    def create_circle(radius: float) -> pymunk.Shape:
        mass = pymunk.area_for_circle(inner_radius=0, outer_radius=radius) * 2
        moment = pymunk.moment_for_circle(mass, inner_radius=0, outer_radius=radius)
        circle_body = pymunk.Body(mass, moment)
        circle_shape = pymunk.Circle(circle_body, radius)
        PhysicsEngine.add_to_space(circle_body, circle_shape)
        return circle_shape
     
    def create_poly(points: list[tuple[float, float]], 
                    center_position: tuple[float, float],
                    angular_velocity: float) -> pymunk.Shape:
        # TODO: Alter the way that bodies for sides are created ? So not every side segment has its own body
        mass = pymunk.area_for_poly(points)
        moment = pymunk.moment_for_poly(mass, points)
        side_body = pymunk.Body(mass, moment, pymunk.Body.KINEMATIC)
        side_body.angular_velocity = angular_velocity
        side_shape = pymunk.Poly(body=side_body, 
                                 vertices=points,
                                 radius=1)
        PhysicsEngine.add_to_space(center_position, side_body, side_shape)
        return side_shape
    
    def get_points(shape: pymunk.Shape) -> list[tuple[int, int]]:
        return shape.get_vertices()
    
    def get_centroid(shape: pymunk.Shape) -> tuple[int, int]:
        return shape.center_of_gravity
    
    '''
    @staticmethod
    def add_observer(observer_asset: Asset, observed_shape: pymunk.Shape):
        if str(observed_shape) not in PhysicsEngine.observers.keys():
            PhysicsEngine.observers[str(observed_shape)] = (observed_shape, observer_asset)
    
    @staticmethod
    def remove_observer(observer):
        if observer in PhysicsEngine.observers.values():
            

    @staticmethod
    def notify_observers(event_type, data: Optional[any]):
        
        if event_type == 'testing_event':
            for observer in PhysicsEngine.observers:
                observer[0].test_notified(data)
            # TODO: complete this method so that the position goes out to the
            # subscribed shapes' Polygons.
        if event_type == 'update':
            for observer in PhysicsEngine.observers:
                observer[0].notified(observer[1])
                    
        if event_type == 'step_by':
            for shape in PhysicsEngine.observers.keys():
                PhysicsEngine.space.reindex_shape(shape)
    '''
    def start_simulation(screen: Surface):
        draw_options = pygame_util.DrawOptions(screen)
        clock = pygame.time.Clock()
        PhysicsEngine.space.debug_draw(draw_options)
        while True:
            screen.fill((0, 0, 0))
            PhysicsEngine.space.debug_draw(draw_options)
            pygame.display.flip()
            clock.tick(60)
            PhysicsEngine.space.step(1.0 / 60.0)
            if (pygame.time.get_ticks() // 1000) % 2 == 0:
                print(pygame.time.get_ticks() // 1000)
            if pygame.time.get_ticks() // 1000 >= 15:
                return
    
    @staticmethod
    def begin(arbiter: pymunk.Arbiter, space: pymunk.Space, data: dict):
        print('begin')
        PhysicsEngine.notify_observers('collision_begin', {'arbiter': arbiter})
        
    @staticmethod
    def pre_solve(arbiter: pymunk.Arbiter, space: pymunk.Space, data: dict):
        print('pre_solve')
        PhysicsEngine.notify_observers('collision_pre_solve', {'arbiter': arbiter})

    @staticmethod
    def post_solve(arbiter: pymunk.Arbiter, space: pymunk.Space, data: dict):
        print('post_solve')
        PhysicsEngine.notify_observers('collision_post_solve', {'arbiter': arbiter})
    
    @staticmethod
    def separate(arbiter: pymunk.Arbiter, space: pymunk.Space, data: dict):
        """ Remove the side hit from the space if data indicates the correct
        conditions were met.
        """
        print('separate')
        PhysicsEngine.notify_observers('collision_separate', {'arbiter': arbiter})
        side_shape = arbiter.shapes[0]
        PhysicsEngine.space.remove(side_shape)
        
    @staticmethod
    def step_by(dt: float):
        PhysicsEngine.space.step(dt)
        PhysicsEngine.notify_observers('step_by')
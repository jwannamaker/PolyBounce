import math

import pymunk
from pymunk import pygame_util
import pygame
from pygame import Surface

from asset.shape import BOX
from asset import Asset

GRAVITY_STRENGTH = 3.8e5


class PhysicsEngine:
    """ Handles creation and updating of all game objects that need to be 
    physically simulated. Provides easy access to the Pymunk processes for my 
    purposes, without making other classes or functions overly complex. 
    """

    game = None
    GAME_CENTER = (0, 0)
    space = None
    collision_handlers = []
    # observers: dict[list[Asset]] = {}


    @staticmethod
    def set_game(game):
        PhysicsEngine.space = pymunk.Space()
        PhysicsEngine.game = game
        PhysicsEngine.GAME_CENTER = pymunk.Vec2d(*game.CENTER)
        print('the physics engine is set! CENTER @', str(PhysicsEngine.GAME_CENTER))

    @staticmethod
    def planet_gravity(body: pymunk.Body, gravity: float, damping: float, dt: float):
        distance_squared = body.position.get_dist_sqrd(PhysicsEngine.GAME_CENTER)
        G = (
            body.position - (pymunk.Vec2d(PhysicsEngine.game.CENTER[0], PhysicsEngine.game.CENTER[1]))
            * -GRAVITY_STRENGTH
            / (distance_squared * math.sqrt(distance_squared))
        )
        # Replacing the built-in velocity with this one
        pymunk.Body.update_velocity(body, G, damping, dt)

    @staticmethod
    def add_collision_handler(shape, other_shape):
        """ TODO: Generate a bitmask given the entity type and the color. """
        handler = PhysicsEngine.space.add_collision_handler(1, 2)
        handler.begin = PhysicsEngine.begin
        handler.pre_solve = PhysicsEngine.pre_solve
        handler.post_solve = PhysicsEngine.post_solve
        handler.separate = PhysicsEngine.separate
        PhysicsEngine.collision_handlers.append(handler)

    @staticmethod
    def add_to_space(position: tuple[float, float], body: pymunk.Body, shape: pymunk.Shape):
        body.position = list(position)
        body.velocity_func = PhysicsEngine.planet_gravity

        # Setting the initial velocity and putting into orbit
        r = body.position.get_distance((300, 300))
        v = math.sqrt(GRAVITY_STRENGTH / r) / r
        body.velocity = (body.position - PhysicsEngine.GAME_CENTER).perpendicular() * v

        # Setting the angular velocity according to its orbital period
        body.angular_velocity = v
        body.angle = math.atan2(body.position.y, body.position.x)

        # Setting the mass somewhere else instead of here will be best
        # shape.mass = 1
        shape.elasticity = 0.01
        shape.friction = 0.45
        PhysicsEngine.space.add(body, shape)

    @staticmethod
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

    @staticmethod
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

    @staticmethod
    def create_circle(radius: float) -> pymunk.Shape:
        mass = pymunk.area_for_circle(inner_radius=0, outer_radius=radius) * 2
        moment = pymunk.moment_for_circle(mass, inner_radius=0, outer_radius=radius)
        circle_body = pymunk.Body(mass, moment)
        circle_shape = pymunk.Circle(circle_body, radius)
        PhysicsEngine.add_to_space(circle_body, circle_shape)
        return circle_shape

    @staticmethod
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

    @staticmethod
    def get_points(shape: pymunk.Shape) -> list[tuple[float, float]]:
        return shape.get_vertices()

    @staticmethod
    def get_centroid(shape: pymunk.Shape) -> tuple[float, float]:
        return shape.center_of_gravity

    
    @staticmethod
    def begin(arbiter: pymunk.Arbiter, space: pymunk.Space, data: dict):
        print('begin')
        PhysicsEngine.notify_game('collision_begin', {'arbiter': arbiter})
        
    @staticmethod
    def pre_solve(arbiter: pymunk.Arbiter, space: pymunk.Space, data: dict):
        print('pre_solve')
        PhysicsEngine.notify_game('collision_pre_solve', {'arbiter': arbiter})

    @staticmethod
    def post_solve(arbiter: pymunk.Arbiter, space: pymunk.Space, data: dict):
        print('post_solve')
        PhysicsEngine.notify_game('collision_post_solve', {'arbiter': arbiter})
    
    @staticmethod
    def separate(arbiter: pymunk.Arbiter, space: pymunk.Space, data: dict):
        """ Remove the side hit from the space if data indicates the correct
        conditions were met.
        """
        print('separate')
        PhysicsEngine.notify_game('collision_separate', {'arbiter': arbiter})
        side_shape = arbiter.shapes[0]
        PhysicsEngine.space.remove(side_shape)
        
    @staticmethod
    def step_by(dt: float):
        PhysicsEngine.space.step(dt)

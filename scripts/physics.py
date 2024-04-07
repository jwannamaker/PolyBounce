import pymunk

from scripts.entity import Asset

class PhysicsEngine:
    """ Handles creation and updating of all game objects that need to be 
    physically simulated. Provides easy access to the Pymunk processes for my 
    purposes, without making other classes or functions overly complex. 
    """
    space = pymunk.Space()
    space.gravity = (0, 1200)
    observers = []
    
    def __init__(self):
        """ Creates the collision handlers. """
        self.handler = self.space.add_collision_handler(1, 2)
        self.handler.begin = PhysicsEngine.begin
        self.handler.pre_solve = PhysicsEngine.pre_solve
        self.handler.post_solve = PhysicsEngine.post_solve
        self.handler.separate = PhysicsEngine.separate
    
    def get_collision_type(self, color_str, entity_type):
        """ TODO: Generates a bitmask given the entity type and the color. """
        return self.ui.PALETTE[color_str]

    def add_to_space(position: tuple[float, float], body: pymunk.Body, shape: pymunk.Shape):
        body.position = list(position)
        shape.elasticity = 0.999
        shape.friction = 0.67
        PhysicsEngine.space.add(body, shape)
    
    def create_walls(screen_size: tuple[int, int]):
        """ The body is already added to the space, since we access the given
        static_body.
        """
        corners = Asset.BOX(screen_size[0], screen_size[1]).get_corners()
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
    
    def create_circle(radius: float):
        mass = pymunk.area_for_circle(inner_radius=0, outer_radius=radius) * 2
        moment = pymunk.moment_for_circle(mass, inner_radius=0, outer_radius=radius)
        circle_body = pymunk.Body(mass, moment)
        circle_shape = pymunk.Circle(circle_body, radius)
        PhysicsEngine.add_to_space(circle_body, circle_shape)
        return circle_shape._id
     
    def create_side(points: list[tuple[float, float]]) -> pymunk.Body.id:
        """ The mass and moment here are really just symbolic, since they don't 
        get used for a KINEMATIC body_type. I wanted them here for strictly
        reference and completion.
        """
        mass = pymunk.area_for_poly(points)
        moment = pymunk.moment_for_poly(mass, points)
        side_body = pymunk.Body(mass, moment, pymunk.Body.KINEMATIC)
        side_shape = pymunk.Poly(body=side_body, 
                                 vertices=points, 
                                 transform=pymunk.Transform.translated(), 
                                 radius=1)
        PhysicsEngine.add_to_space(side_body, side_shape)
        return side_shape._id
    
    @staticmethod
    def add_observer(observer, shape):
        if observer not in PhysicsEngine.observers:
            PhysicsEngine.observers.append(observer)

    @staticmethod
    def remove_observer(observer):
        if observer in PhysicsEngine.observers:
            PhysicsEngine.observers.remove(observer)

    @staticmethod
    def notify_observers(event_type, data):
        for observer in PhysicsEngine.observers:
            observer.update(event_type, data)
            # TODO: complete this method so that the position goes out to the
            # subscribed shapes' Polygons.

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
'''
side.py contains the definition for the Side class.
'''

from utils import *

class Side:
    '''
        Represents one side of a Polygon. Using for better organization of data.
        
        Inherits Sprite in order to use collision of masks; Kill individual sides
        instead of the whole polygon.
    '''
    
    def __init__(self, parent: pygame.sprite.Sprite | pymunk.Body, *, points: list):
        self.parent = parent
        self.points = points
        
        # pymunk setup
        self.shape = pymunk.Poly(self.parent.body, self.points, radius=1)
        self.shape.density = 1
        self.shape.elasticity = 0.4
        self.shape.friction = 0.4
        
        # pygame setup, sprite attributes
        self.image = self.parent.get_subsurface()   # new surface inherits palette, colorkey, and alpha settings
        self.color = random.choice(list(POLY_PALLETE.keys()))
        self.draw()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.parent.mask.draw(self.mask, (0, 0))    # add this mask to the parent mask
        
        
        # game logic
        # using the color of the side to determine the collision type
        self.shape.collision_type = 2 # POLY_PALLETE[self.color]
        self.neighbors = dict().fromkeys(['left', 'right', 'top', 'bottom']) # should only have left, right, above, below neighbors
            
    def add_neighbor(self, type: str, neighbor):
        # TODO: Add neighbors in the polygon class, when the sides are created
        self.neighbors[type] = neighbor    
    
    def update_color(self, prev_side):
        '''
        Returns a random color that doesn't match the color of the previous side,
        then updates the collision type based on that color
        TODO: Change method so the color can't match the color of the existing 
        neighbors.
        '''
        while self.color == prev_side.color:
            self.color = random.choice(list(POLY_PALLETE.keys()))
        self.shape.collision_type = POLY_PALLETE[self.color]
    
    def draw(self):
        gfxdraw.filled_polygon(self.image, self.shape.get_vertices(), self.color)
        
        


from scripts.utils import *
    
class PhysicsEntity(pygame.sprite.Sprite):
    def __init__(self, game, groups, radius, entity_type):
        self.groups = groups
        super().__init__(self.groups)
        self.game = game
        self.radius = radius
        self.entity_type = entity_type
        
        self.image = pygame.Surface((self.radius * 2, self.radius * 2))
        self.image.set_colorkey((0, 0, 0))
        self.color = random.choice(PALLETE)
        
        self.body = pymunk.Body(0, 0, pymunk.Body.DYNAMIC) # can be modified in the derived class constructor
        self.body.position = [CENTER.x, -CENTER.y]
        self.shape: pymunk.Shape = None # must be defined in the derived class constructor
    
    def set_visual_properties(self):
        ''' must be called in derived class constructor '''
        self.rect = pygame.Rect(self.image.get_rect())
        self.rect.topleft = (CENTER.x - self.radius, CENTER.y - self.radius)
        self.mask = pygame.mask.from_surface(self.image)
    
    def set_physics_properties(self):
        ''' must be called in derived class constructor '''
        self.body.position = [CENTER.x, CENTER.y]
        if self.entity_type == 'player':
            self.shape.density = 10
            self.shape.elasticity = 0.999
            self.shape.friction = 0.825
            self.game.space.add(self.body, self.shape)
        elif self.entity_type == 'non-player':
            self.game.space.add(self.body)
            for shape in self.side_shapes:
                shape.density = 10
                shape.elasticity = 0.999
                shape.friction = 0.789
                self.game.space.add(shape)
    
    def update(self):
        self.rect.center = Vector2(self.body.position)
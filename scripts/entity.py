from scripts.utils import *
    
class PhysicsEntity(pygame.sprite.Sprite):
    def __init__(self, game, radius, entity_type):
        super().__init__()
        self.game = game
        self.radius = radius
        self.entity_type = entity_type
        
        self.image = pygame.Surface((self.radius * 2, self.radius * 2))
        self.image.set_colorkey((0, 0, 0))
        self.color = random.choice(PALLETE)
        
        self.body = pymunk.Body(0, 0, pymunk.Body.DYNAMIC) # can be modified in the derived class constructor
        self.shape: pymunk.Shape = None # must be defined in the derived class constructor
    
    def set_visual_properties(self):
        ''' must be called in derived class constructor '''
        self.rect = pygame.Rect(self.image.get_rect())
        self.rect.topleft = (CENTER.x - self.radius, CENTER.y - self.radius)
        self.mask = pygame.mask.from_surface(self.image)
    
    def set_physics_properties(self):
        ''' must be called in derived class constructor '''
        self.body.position = pymunk.pygame_util.from_pygame((self.rect.top + self.radius, self.rect.left + self.radius), self.image)
        if self.entity_type == 'player':
            self.shape.density = 10
            self.shape.elasticity = 0.456
            self.shape.friction = 0.825
            self.game.space.add(self.body, self.shape)
        elif self.entity_type == 'non-player':
            self.game.space.add(self.body)
            for shape in self.side_shapes:
                shape.density = 1
                shape.elasticity = 0.999
                shape.friction = 0.789
                self.game.space.add(shape)
    
    def update(self):
        if self.entity_type == 'player':
            self.rect.center = Vector2(self.body.position[0], self.body.position[1])
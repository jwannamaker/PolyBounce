from scripts.utils import *
    
class PhysicsEntity(pygame.sprite.Sprite):
    def __init__(self, game, radius, position=CENTER):
        super().__init__()
        self.game = game
        self.radius = radius
        self.position = round(position[0]), round(position[1]) # may need to change this between Vec2/Vector2/tuple
        self.entity_type = 'non-player'
        
        self.image = pygame.Surface((self.radius * 2, self.radius * 2))
        self.image.set_colorkey((0, 0, 0))
        self.color = random.choice(PALLETE)
        
        self.body = pymunk.Body(0, 0, pymunk.Body.DYNAMIC) # can be modified in the derived class constructor
        self.shape: pymunk.Shape = None # must be defined in the derived class constructor
    
    def set_visual_properties(self):
        ''' must be called in derived class constructor '''
        self.rect = pygame.Rect(self.image.get_rect())
        self.rect.center = self.position
        self.mask = pygame.mask.from_surface(self.image)
    
    def set_physics_properties(self, entity_type):
        ''' must be called in derived class constructor '''
        self.entity_type = entity_type
        self.body.position = self.position
        if entity_type == 'player':
            self.shape.density = 10
            self.shape.elasticity = 0.456
            self.shape.friction = 0.825
            self.game.space.add(self.body, self.shape)
        elif entity_type == 'non-player':
            for side in self.sides.values():
                side.shape.density = 1
                side.shape.elasticity = 0.999
                side.shape.friction = 0.789
            self.game.space.add(self.body)
    
    def update(self):
        self.position = Vector2(self.body.position[0], self.body.position[1])
        self.rect.topleft = self.position - Vector2(self.radius)
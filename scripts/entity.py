from scripts.utils import *
    
class PhysicsEntity(pygame.sprite.Sprite):
    def __init__(self, game, radius, position=CENTER):
        super().__init__()
        self.game = game
        self.radius = radius
        self.position = from_pygame(position)
        self.image = pygame.Surface((self.radius * 2, self.radius * 2))
        self.image.set_colorkey((0, 0, 0))
        self.color = random.choice(PALLETE)
        
        self.body = pymunk.Body(0, 0, pymunk.Body.DYNAMIC)
        self.shape = pymunk.Circle(self.body, self.radius, self.position)
        # set the mass, moment in derived classes
        # Then call physics/visual setup methods
    
    def set_visual_properties(self):
        self.rect = pygame.Rect(self.image.get_rect())
        self.rect.center = self.position
        self.mask = pygame.mask.from_surface(self.image)
    
    def set_physics_properties(self):
        self.body.position = self.position
        if len(self.shapes) >= 1:
            self.body.shapes.density = 1
            self.body.shapes.elasticity = 0.999
            self.body.shapes.friction = 0.78
            self.game.space.add(self.body)
        else:
            self.body.shape.density = 10
            self.body.shape.elasticity = 0.4
            self.body.shape.friction = 0.85
            self.game.space.add(self.body, self.body.shape)
    
    def draw(self):
        self.rect.topleft = self.position - Vector2(self.radius)
        self.game.screen.blit(self.image, self.rect.topleft)
        
    def update(self):
        self.shape.collision_type = get_collision_type(self.color)
        self.position = pymunk.pygame_util.to_pygame(self.body.position, self.image)
    
    def add_key_held(self, key):
        self.keys_held.append(key)
        
    def remove_key_held(self, key):
        self.keys_held.remove(key)
        
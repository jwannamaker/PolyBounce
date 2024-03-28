from polybounce.utils import *

class Entity(pygame.sprite.Sprite):
    screen = pygame.display.set_mode(SCREEN_SIZE)
   
    def __init__(self, radius, position=CENTER):
        super().__init__()
        self.radius = radius
        self.position = position
        self.color = random.choice(PALLETE)
        
        #---- move these into their derived classes
        self.draw()
        self.set_sprite_properties()
        
    def set_sprite_properties(self):
        self.image = pygame.Surface((self.radius * 2, self.radius * 2))
        self.image.set_colorkey((0, 0, 0))
        self.rect = pygame.FRect(self.image.get_frect())
        self.rect.center = self.position
        self.mask = pygame.mask.from_surface(self.image)
        
    def draw(self, surface):
        self.rect.topleft = self.position - Vector2(self.radius)
        surface.blit(self.image, self.rect.topleft)
    
class PhysicsEntity(Entity):
    pymunk.pygame_util.positive_y_is_up = True
    space = pymunk.space.Space()
    space.gravity = (0, 10)
    
    def __init__(self, radius, position):
        super().init(radius, position)
        self.

        # ----Call in derived classes
    
    def set_shape_properties(self):
        self.body.position = self.position
        self.shape.density = 1
        self.shape.elasticity = 0.999
        self.shape.friction = 0.78
        PhysicsEntity.space.add(self.body, self.shape)
        
    def update(self):
        self.shape.collision_type = PALLETE_DICT[self.color].collision_type
        self.position = pymunk.pygame_util.to_pygame(self.body.position, self.image)
        
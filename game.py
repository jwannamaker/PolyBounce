import pygame

from scripts.ui import UI
from scripts.player import Player
from scripts.enemy import Enemy

class Game:
    def __init__(self, title, ui: UI, player: Player, enemy: Enemy):
        self.ui = ui
        self.player = player
        self.enemy = enemy
        
        self.entities = pygame.sprite.Group()
        
        # Delay the pygame initialization until all attributes are concrete
        self.init_pygame(title)
        self.set_fps(50)
        
    def get_level_difficulty(self):
        """ Needs to return a number and a list of what Polygon(s) to create for 
        the next relevant level. Uses the SINGLETON self.player attribute.
        """
        pass
    
    def create_level(self, difficulty_dict):
        """ This will use the defined difficulty dictionary to create the 
        correct sifficulty per level.
        """
        pass
    
    def set_fps(self, fps):
        self.fps = fps
        
    def init_pygame(self, title):
        pygame.init()
        self.screen = pygame.display.set_mode(self.ui().SCREEN_SIZE)
        pygame.display.set_caption(title)
        self.dt = 1 / self.fps
        self.running = False
        
    def handle_user_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    
            if event.type == pygame.KEYUP:
                pass
    
    def process_game_logic(self):
        """ Apply updates to all the game objects according to current game 
        state. Retrieve the position data from the PhysicsEngine.
        """
        self.ui.update_all()
        self.entities.update()
    
    def main_loop(self):
        while self.running:
            self.handle_user_input()
            self.process_game_logic()
            self.render()
        pygame.quit()
        
    def start(self):
        self.running = True
        self.main_loop()
        
                
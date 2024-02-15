from utils import *
from polygon import Polygon
from ball import Ball

class PolyBounce:
    '''
        Goal: Bounce the ball on the right color of the innermost ring,
        to clear it and infinitely progress to the next ring.
        
    '''
    def __init__(self):
        # pygame setup
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption('Johnny Tries Physics and Stuff!')
        self.clock = pygame.time.Clock()
        self.fps = 1
        
        # font setup
        pygame.font.init()
        self.font = load_font()
        
        # background setup
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.background.fill(BACKGROUND_PALLETE['black'])
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()
        
        # game objects setup
        self.player_ball = Ball(10)
        self.player_group = pygame.sprite.RenderClear(self.player_ball)
        self.inner_ring = Polygon(200, 5)
        self.ring_group = pygame.sprite.RenderClear(self.inner_ring)
        
        self.running = False
    
    def start(self):
        self.running = True
        self.main_loop()
    
    def handle_user_input(self):
        '''
            Poll for user events, updating lists containing with movements 
            that need to be applied to game objects.
        '''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    break
                if event.key == pygame.K_LSHIFT:
                    self.player_ball.add_key_held('boost')
                
                if event.key == pygame.K_w:
                    self.player_ball.add_key_held('up')
                if event.key == pygame.K_s:
                    self.player_ball.add_key_held('down')
                if event.key == pygame.K_a:
                    self.player_ball.add_key_held('left')
                if event.key == pygame.K_d:
                    self.player_ball.add_key_held('right')
                
                if event.key == pygame.K_SPACE:
                    self.player_ball.add_key_held('jump')
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LSHIFT:
                    self.player_ball.remove_key_held('boost')
                    
                if event.key == pygame.K_w:
                    self.player_ball.remove_key_held('up')
                if event.key == pygame.K_s:
                    self.player_ball.remove_key_held('down')
                if event.key == pygame.K_d:
                    self.player_ball.remove_key_held('right')
                if event.key == pygame.K_a:
                    self.player_ball.remove_key_held('left')
                
                if event.key == pygame.K_SPACE:
                    self.player_ball.remove_key_held('jump')
                    
                if event.key == pygame.K_q:
                    self.inner_ring.ccw_rotate()
                if event.key == pygame.K_e:
                    self.inner_ring.cw_rotate()
    
    def process_game_logic(self):
        self.player_ball.update(self.inner_ring)
        self.inner_ring.update()
    
    def update_game_state(self):
        '''
            Draw the new state of each object in the game onto the screen.
        '''
        self.screen.blit(self.background, (0, 0))
        self.player_ball.draw(self.screen)
        self.inner_ring.draw(self.screen)
        dt = self.clock.tick(self.fps) / 1000
        pygame.display.flip()
        
    def main_loop(self):
        while self.running:
            self.handle_user_input()
            self.process_game_logic()
            self.update_game_state()
        pygame.quit()
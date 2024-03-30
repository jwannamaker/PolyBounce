'''
    Summary of this file here
'''

from scripts.utils import *
from scripts.polygon import Polygon
from scripts.ball import Ball

class PolyBounce:
    def __init__(self):
        # pygame setup
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption('PolyBounce')
        pygame.font.init()
        self.font = load_font()
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.background.fill(pygame.Color('black'))
        self.clock = pygame.time.Clock()
        self.fps = 50
        self.dt = 1 / self.fps       
        self.running = False
        
        # Entities setup
        self.space = pymunk.space.Space()
        self.space.gravity = (0, 100)
        
        screen_corners = [(0, 0), (0, SCREEN_SIZE.y), (SCREEN_SIZE.x, SCREEN_SIZE.y), (SCREEN_SIZE.x, 0)]
        create_walls(screen_corners, self.space)
        self.inner_ring = Polygon(self, radius=250, N=6)
        self.mid_ring = Polygon(self, radius=300, N=6)
        self.outer_ring = Polygon(self, radius=350, N=6)
        self.ring_group = pygame.sprite.Group(self.inner_ring, self.mid_ring, self.outer_ring)
        
        self.player_ball = Ball(self, radius=25)
        self.player_group = pygame.sprite.Group(self.player_ball)
        
        # Now that all the game objects are created, I can add collision handling for them
        self.handler = self.space.add_collision_handler(1, 2) # 1 - ball, 2 - nonball ---> Can easily transition into using bitmasking for this
        self.handler.data['ball'] = self.player_ball
        self.handler.data['inner_ring'] = self.inner_ring
        self.handler.begin = begin
        self.handler.pre_solve = pre_solve
        self.handler.post_solve = post_solve
        self.handler.separate = separate
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        
    def start(self):
        self.running = True
        self.main_loop()
    
    def set_fps(self, fps):
        self.fps = fps
        
    def display_stats(self):
        player_info = []
        player_info.append('{:15s} {:17.2f}'.format('SCORE', 0))
        player_info.append('{:15s} {:8.2f} {:8.2f}'.format('Position', self.player_ball.body.position[0], self.player_ball.body.position[1]))
        player_info.append('{:15s} {:8.2f} {:8.2f}'.format('Velocity', self.player_ball.body.velocity[0], self.player_ball.body.velocity[1]))
        # TODO Make some fancy display rect for the text to go onto and then blit that onto the screen
        
        for i, line in enumerate(player_info):
            self.screen.blit(self.font.render(line, True, pygame.Color('white')), (SCREEN_SIZE.x / 2, 20 * i))
    
    def handle_user_input(self):
        '''
            Poll for user events, updating lists containing with movements 
            that need to be applied to game objects.
        '''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_q:
                    self.inner_ring.ccw_rotate(self.dt)
                if event.key == pygame.K_e:
                    self.inner_ring.cw_rotate(self.dt)
    
    def process_game_logic(self):
        '''
            Updates the game objects (player_group, ring_group, etc) according 
            to the current game state.
        '''
        self.handler.data['inner_ring'] = self.inner_ring
        self.ring_group.update()
        self.player_group.update()
    
    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.display_stats()
        for ring in self.ring_group:
            ring.render()
        self.player_ball.render()
        
        # TODO: Add some logic to address the need for semi-fixed framerate?
        self.clock.tick(self.fps)
        self.space.step(self.dt)
        self.space.debug_draw(self.draw_options)
        pygame.display.flip()
        
    def main_loop(self):
        while self.running:
            self.handle_user_input()
            self.process_game_logic()
            self.render()
        pygame.quit()
        
if __name__ == "__main__":
    PolyBounce().start()
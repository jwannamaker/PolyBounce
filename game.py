'''
    Summary of this file here
'''

from utils import *
from polygon import Polygon
from ball import Ball

class PolyBounce:
    '''
    End Product:
        The Rings will: 
            Continually generate with random N = [3 - 7]
            All smoothly shrink towards the center once the ball 'clears' a ring
            Smoothly rotate CCW or CW when the player presses A or D respectively
            
        The Ball will:
            Change color according to the last Ring wall it touched
            Stay 'trapped' within the innermost ring until it clears
        
    '''
    def __init__(self):
        # pygame setup
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption('PolyBounce')
        pygame.font.init()
        self.font = load_font()
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.background.fill(pygame.Color('black'))
        self.screen.blit(self.background, (0, 0))
        self.clock = pygame.time.Clock()
        self.fps = 10
        self.dt = 1 / self.fps       
        self.running = False
        
        # Pymunk setup
        self.space = pymunk.Space()
        self.space.gravity = (0, 10)
        
        # Entities setup
        screen_corners = [(0, 0), (0, SCREEN_SIZE.y), (SCREEN_SIZE.x, SCREEN_SIZE.y), (SCREEN_SIZE.x, 0)]
        create_walls(screen_corners, self.space)
        self.inner_ring = Polygon(self.space, 250, 6)
        self.mid_ring = Polygon(self.space, 300, 6)
        self.outer_ring = Polygon(self.space, 350, 6)
        self.ring_group = pygame.sprite.Group(self.inner_ring, self.mid_ring, self.outer_ring)
        
        self.player_ball = Ball(self.space, 25)
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
        # self.space.debug_draw(self.draw_options)
        # player_info.append('{:15s} {:8.2f} {:8.2f}'.format('Info', self.player_ball.body., self.player_ball.position[1]))
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
                if event.key == pygame.K_LSHIFT:
                    self.player_ball.add_key_held('slow')
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LSHIFT:
                    self.player_ball.remove_key_held('slow')
                    
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
        self.ring_group.update(self.dt)
        self.player_group.update(self.dt)
    
    def draw(self):
        '''
            Draw the new state of each object in the game onto the screen.
        '''
        self.screen.blit(self.background, (0, 0))
        # drawing some lines for the purpose of debugging/analyzing output values
        # pygame.draw.line(self.screen, (255, 0, 0), (self.player_ball.position[0], 0), (self.player_ball.position[0], SCREEN_SIZE[1]))
        # pygame.draw.line(self.screen, (255, 0, 0), (0, self.player_ball.position[1]), (SCREEN_SIZE[0], self.player_ball.position[1]))
        # pygame.display.update()
        self.display_stats()
        self.ring_group.draw(self.screen)
        self.player_ball.draw(self.screen)
        
        # TODO: Add some logic to address the need for semi-fixed framerate
        self.clock.tick(self.fps)
        self.space.step(self.dt)
        # self.space.debug_draw(self.draw_options)
        pygame.display.flip()
        
    def main_loop(self):
        while self.running:
            self.handle_user_input()
            self.process_game_logic()
            self.draw()
        pygame.quit()
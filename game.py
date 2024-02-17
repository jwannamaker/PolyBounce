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
        self.dt = 0
        
        # font setup
        pygame.font.init()
        self.font = load_font()
        
        # background setup
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.background.fill(BACKGROUND_PALLETE['black'])
        self.screen.blit(self.background, (0, 0))
        self.running = False
        
        # game objects setup
        self.inner_ring = Polygon(350, 5)
        # self.outer_ring = Polygon(250, 6)
        # self.outer_outer_ring = Polygon(300, 6)
        self.ring_group = pygame.sprite.Group(self.inner_ring)
        
        self.player_ball = Ball(20, self.ring_group)
        self.player_group = pygame.sprite.RenderClear(self.player_ball)
        
    def start(self):
        self.running = True
        self.main_loop()
    
    def set_fps(self, fps):
        self.fps = fps
        
    def display_stats(self):
        player_info = []
        player_info.append('{:15s} {:8.2f} {:8.2f}'.format('Position', self.player_ball.position[0], self.player_ball.position[1]))
        player_info.append('{:15s} {:8.2f} {:8.2f}'.format('Velocity', self.player_ball.velocity[0], self.player_ball.velocity[1]))
        
        # TODO Make some fancy display rect for the text to go onto and then blit that onto the screen
        
        for i, line in enumerate(player_info):
            self.screen.blit(self.font.render(line, True, PALLETE['white']), (0, SCREEN_SIZE.y - 40 + 20 * i))
    
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
        # Checks if the player ball is currently inside of the inscribed circle of the ring
        # if pygame.sprite.spritecollide(self.player_ball, self.ring_group, False, pygame.sprite.collide_mask):
        #     if self.player_ball.position != CENTER:
        #         self.player_ball.velocity *= -1
            # player_mask = self.player_ball.mask
            # ring_mask = self.inner_ring.mask
            # offset_x = self.player_ball.rect.topleft[0] - self.inner_ring.rect.topleft[0]
            # offset_y = self.player_ball.rect.topleft[1] - self.inner_ring.rect.topleft[1]
            # overlap_amount = ring_mask.overlap_area(player_mask, (offset_x, offset_y))
            # if overlap_amount >= 1:
            #     dx = ring_mask.overlap_area(player_mask, (offset_x + 1, offset_y)) - ring_mask.overlap_area(player_mask, (offset_x - 1, offset_y))
            #     dy = ring_mask.overlap_area(player_mask, (offset_x, offset_y + 1)) - ring_mask.overlap_area(player_mask, (offset_x, offset_y - 1))     
                # self.player_ball.position.x += dx
                # self.player_ball.position.y += dy
            
        self.player_ball.update()
        self.ring_group.update()
    
    def update_game_state(self):
        '''
            Draw the new state of each object in the game onto the screen.
        '''
        self.screen.blit(self.background, (0, 0))
        # drawing some lines for the purpose of debugging/analyzing output values
        pygame.draw.line(self.screen, (255, 0, 0), (self.player_ball.position.x, 0), (self.player_ball.position.x, SCREEN_SIZE.y))
        pygame.draw.line(self.screen, (255, 0, 0), (0, self.player_ball.position.y), (SCREEN_SIZE.x, self.player_ball.position.y))
        self.display_stats()
        self.player_ball.draw(self.screen)
        self.ring_group.draw(self.screen)
        self.dt = self.clock.tick(self.fps) / 1000
        pygame.display.flip()
        
    def main_loop(self):
        while self.running:
            self.handle_user_input()
            self.process_game_logic()
            self.update_game_state()
        pygame.quit()
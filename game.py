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
    
    def set_fps(self, fps):
        self.fps = fps
    
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
            
        self.player_ball.update(self.dt)
        self.inner_ring.update()
    
    def update_game_state(self):
        '''
            Draw the new state of each object in the game onto the screen.
        '''
        self.screen.blit(self.background, (0, 0))
        # drawing some lines for the purpose of debugging/analyzing output values
        pygame.draw.line(self.screen, (255, 0, 0), (self.player_ball.position.x, 0), (self.player_ball.position.x, SCREEN_SIZE.y))
        pygame.draw.line(self.screen, (255, 0, 0), (0, self.player_ball.position.y), (SCREEN_SIZE.x, self.player_ball.position.y))
        self.player_ball.draw(self.screen)
        self.inner_ring.draw(self.screen)
        self.dt = self.clock.tick(self.fps) / 1000
        pygame.display.flip()
        
    def main_loop(self):
        while self.running:
            self.handle_user_input()
            self.process_game_logic()
            self.update_game_state()
        pygame.quit()
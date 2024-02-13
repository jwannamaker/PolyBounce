'''

'''
# from prettytable import PrettyTable, SINGLE_BORDER
import pygame
from utils import *
from player import *
from polygon import * 

def main():
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Johnny Tries Physics and Other Things!')
    clock = pygame.time.Clock()
    dt = 0          # Time passed in milliseconds since the last frame
    fps = 60
    
    # font setup
    pygame.font.init()
    font = load_font()

    # background setup
    background = pygame.Surface(screen.get_size()).convert()
    background.fill(BACKGROUND_PALLETE['black'])
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # player object setup - initialized with start position
    player_ball = Ball(10, PALLETE['light-purple'])
    # player_group = pygame.sprite.GroupSingle()
    # player_group.add(player_ball)
    
    first_ring = Polygon(100, RING_PALLETE['cyan'], 5)
    # second_ring = Polygon(150, RING_PALLETE['pink'], 6)
    
    
    
    # event loop
    running = True
    while running:
        dt = clock.tick(fps) / 1000
        
        # poll for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT:
                    player_ball.add_key_held('boost')
                
                if event.key == pygame.K_w:
                    player_ball.add_key_held('up')
                if event.key == pygame.K_s:
                    player_ball.add_key_held('down')
                if event.key == pygame.K_a:
                    player_ball.add_key_held('left')
                if event.key == pygame.K_d:
                    player_ball.add_key_held('right')
                
                if event.key == pygame.K_SPACE:
                    player_ball.add_key_held('jump')
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LSHIFT:
                    player_ball.remove_key_held('boost')
                    
                if event.key == pygame.K_w:
                    player_ball.remove_key_held('up')
                if event.key == pygame.K_s:
                    player_ball.remove_key_held('down')
                if event.key == pygame.K_d:
                    player_ball.remove_key_held('right')
                if event.key == pygame.K_a:
                    player_ball.remove_key_held('left')
                
                if event.key == pygame.K_SPACE:
                    player_ball.remove_key_held('jump')
                    
                if event.key == pygame.K_q:
                    first_ring.ccw_rotate()
                if event.key == pygame.K_e:
                    first_ring.cw_rotate()
                
        
        screen.blit(background, (0, 0))
        player_ball.update()
        player_ball.draw(screen)
        first_ring.update()
        first_ring.draw(screen)
        # ring_group.remove(player_ball)
        
        pygame.display.flip()
        
    pygame.quit()

if __name__ == '__main__':
    main()
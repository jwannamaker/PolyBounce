'''

'''
from prettytable import PrettyTable, SINGLE_BORDER
import pygame
from hexkey_utils import *
from player import *
from polygon import * 

def main():
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Johnny Tries Physics!')
    clock = pygame.time.Clock()
    dt = 0          # Time passed in milliseconds since the last frame
    fps = 60
    
    # font setup
    pygame.font.init()
    font = load_font()

    # background setup
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((10, 10, 10))
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # player object setup - initialized with start position
    player_ball = Ball(mass=5, radius=10, color=PALLETE['light-purple'])
    # sprites = pygame.sprite.Group(player_ball)
    
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
                
                if event.key == pygame.K_d:
                    # player_ball.velocity[0] += 5
                    player_ball.add_key_held('right')
                if event.key == pygame.K_a:
                    # player_ball.velocity[0] += -5
                    player_ball.add_key_held('left')
                if event.key == pygame.K_w:
                    # player_ball.acceleration[1] += -0.1
                    player_ball.add_key_held('up')
                if event.key == pygame.K_s:
                    # player_ball.acceleration[1] += 0.1
                    player_ball.add_key_held('down')
                
                if event.key == pygame.K_SPACE:
                    player_ball.add_key_held('jump')
                    # if player_ball.position[1] >= 4 * (SCREEN_HEIGHT / 5):
                    #     player_ball.velocity[1] += -10
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LSHIFT:
                    player_ball.remove_key_held('boost')
                
                if event.key == pygame.K_d:
                    
                    player_ball.remove_key_held('right')
                if event.key == pygame.K_a:
                    
                    player_ball.remove_key_held('left')
                if event.key == pygame.K_w:
                    
                    player_ball.remove_key_held('up')
                if event.key == pygame.K_s:
                    
                    player_ball.remove_key_held('down')
                
                if event.key == pygame.K_SPACE:
                    player_ball.remove_key_held('jump')
                
        
        
        screen.fill(BACKGROUND_PALLETE['black'])
        
        player_ball.update()
        pygame.display.flip()
        
    pygame.quit()

if __name__ == '__main__':
    main()
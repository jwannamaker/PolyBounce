'''

'''
import pygame
from tabulate import tabulate
from hexkey_utils import *
from player import *
from polygon import * 

def main():
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Johnny\'s First Video Game!')
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
    player_ball = Ball(10, PALLETE['light-purple'])
    # sprites = pygame.sprite.Group(player_ball)
    
    # event loop
    running = True
    while running:
        dt = clock.tick(fps) / 1000
        
        # poll for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_w:
                    player_ball.move_up()
                if event.key == pygame.K_s:
                    player_ball.move_down()
                if event.key == pygame.K_a:
                    player_ball.move_left()
                if event.key == pygame.K_d:
                    player_ball.move_right()

                if event.key == pygame.K_SPACE:
                    player_ball.freeze()
                if event.key == pygame.K_LSHIFT:
                    print(f'{dt}: LSHIFT')
        
        
        screen.fill(BACKGROUND_PALLETE['black'])
        headers = ['X', 'Y']
        table = [player_ball.position, 
                player_ball.velocity, 
                player_ball.acceleration]
        # info_msg =  '-------------------------------\n' + \
        #             f'Position X: {player_ball.position[0]:8.2f}\n' + \
        #             f'Position Y: {player_ball.position[1]:8.2f}\n\n' + \
        #             '-------------------------------\n' + \
        #             f'Velocity X: {player_ball.velocity[0]:8.2f}\n' + \
        #             f'Velocity Y: {player_ball.velocity[1]:8.2f}\n'
        # screen.blit(font.render(tabulate(table, headers), True, PALLETE['white']), (0, 0))
        player_ball.update(screen)
        # sprites.draw(screen)
        pygame.display.flip()
        
    pygame.quit()

if __name__ == '__main__':
    main()
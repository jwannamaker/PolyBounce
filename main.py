'''

'''
import pygame
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
    sprites = pygame.sprite.Group(player_ball)
    
    # event loop
    running = True
    while running:
        dt = clock.tick(fps) / 1000
        
        # poll for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                player_ball.falling = False
                if event.key == pygame.K_w:
                    print(f'{dt}: W')
                if event.key == pygame.K_s:
                    print(f'{dt}: S')
                if event.key == pygame.K_a:
                    print(f'{dt}: A')
                if event.key == pygame.K_d:
                    print(f'{dt}: D')

                if event.key == pygame.K_SPACE:
                    # TODO player_ball call
                    print(f'{dt}: SPACE')
                if event.key == pygame.K_LSHIFT:
                    # TODO player_ball call
                    print(f'{dt}: LSHIFT')
            else: # elif event.type == pygame.KEYUP:
                
                
                # TODO Move player_ball according to kinematics. 
                # TODO It falls + bounces on the surface of the shape it is in
                print('falling...')
                player_ball.falling = True
        
        
        screen.fill(BACKGROUND_PALLETE['black'])
        info_msg =  '=== Player Position ====\n' + \
                    f'X: {player_ball.position[0]:8.2f}\n' + \
                    f'Y: {player_ball.position[1]:8.2f}'
        screen.blit(font.render(info_msg, True, BACKGROUND_PALLETE['grey-blue']), (0, 0))
        player_ball.update(screen)
        sprites.draw(screen)
        pygame.display.flip()
        
    pygame.quit()

if __name__ == '__main__':
    main()
import pygame
from player import *
from hexagon import *
from hexkey_utils import *

def main():
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0
    fps = 60
    
    # font setup
    pygame.font.init()
    font = load_font()

    # background setup
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    refresh_background(background)
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # player setup - initialized with start position
    player_ball = Ball()
    ring = Hexagon(60)
    sprites = pygame.sprite.Group(player_ball, ring)
    
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
                    # TODO ring call
                    print('Switch current ring up')
                if event.key == pygame.K_s:
                    # TODO ring call
                    print('Switch current ring down')
                    
                if event.key == pygame.K_a:
                    # TODO ring call
                    print('Move current ring counterclockwise')
                    ring.ccw_rotate()
                if event.key == pygame.K_d:
                    # TODO ring call
                    print('Move current ring clockwise')
                    ring.cw_rotate()

                if event.key == pygame.K_SPACE:
                    # TODO player_ball call
                    print('JUMP player_ball')
                if event.key == pygame.K_LSHIFT:
                    # TODO player_ball call
                    print('FREEZE player_ball')
            else: # elif event.type == pygame.KEYUP:
                
                
                # TODO Move player_ball according to kinematics. 
                # TODO It falls + bounces on the surface of the shape it is in
                print('player_ball falling')
                player_ball.falling = True
        
        
        screen.fill(BACKGROUND_PALLETE['black'])
        info_msg =  '=== Player Position ====\n' + \
                    f'X: {player_ball.position.x:8.2f}\n' + \
                    f'Y: {player_ball.position.y:8.2f}'
        screen.blit(font.render(info_msg, True, BACKGROUND_PALLETE['grey-blue']), (0, 0))
        sprites.update()
        sprites.draw(screen)
        pygame.display.flip()
        
    pygame.quit()

if __name__ == '__main__':
    main()
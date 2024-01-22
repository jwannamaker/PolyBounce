import pygame
from player import *
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
    sprite = pygame.sprite.GroupSingle(player_ball)
    
    # event loop
    running = True
    while running:
        dt = clock.tick(fps) / 1000
        
        # poll for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        player_ball.update(dt)
        
        refresh_background(screen)
        screen.blit(background, (0, 0))
        
        
        info_msg = "=== Player Position ====\nX: {:8.2f}\nY: {:8.2f}".format(player_ball.position.x, player_ball.position.y)
        show_stats(screen, font, info_msg)
        
        sprite.draw(screen)
        pygame.display.flip()     # ? --> what's the difference between flip and update?
        
    pygame.quit()

if __name__ == "__main__":
    main()
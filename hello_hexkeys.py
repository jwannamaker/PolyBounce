import pygame
from hexkey_utils import *

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0                      # delta time - time since last frame

# font setup
pygame.font.init()
font = init_font()

# player setup - initialized with start position
CENTER = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
player_pos = pygame.Vector2(CENTER)

# event loop
while running:
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    refresh_background(screen)
    regular_polygon(screen, CENTER, 100, 6)
    
    info_msg = "X: {:8f}\nY: {:8f}".format(player_pos.x, player_pos.y)
    screen.blit(font.render("X: " + str(player_pos.x) + "\nY: " + str(player_pos.y), True, (255, 255, 255)), (0, 0))
    pygame.draw.circle(screen, "blue", player_pos, 50)
    
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_w] and player_pos.y - 50 > 0:
        player_pos.y -= 100 * dt
    if keys[pygame.K_s] and player_pos.y + 50 < screen.get_height():
        player_pos.y += 100 * dt
    
    if keys[pygame.K_a] and player_pos.x - 50 > 0:
        player_pos.x -= 100 * dt
    if keys[pygame.K_d] and player_pos.x + 50 < screen.get_width():
        player_pos.x += 100 * dt
    
    
    pygame.display.update()     # ? --> what's the difference between flip and update?
    
    # limits FPS
    dt = clock.tick(60) / 1000
pygame.quit()
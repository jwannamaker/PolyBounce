import pygame
from hexkey_utils import *

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0          # delta time - time since last frame

# font setup
pygame.font.init()
font = init_font()
text = font.render("Game Start!", True, (255, 255, 255))

# player setup - initialized with start position
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

# event loop
while running:
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill("black")    # wipe screen from last frame
    screen.blit(text, (0, 0))
    pygame.draw.circle(screen, "blue", player_pos, 30)
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= 100 * dt
    if keys[pygame.K_s]:
        player_pos.y += 100 * dt
    if keys[pygame.K_a]:
        player_pos.x -= 100 * dt
    if keys[pygame.K_d]:
        player_pos.x += 100 * dt
    
    
    pygame.display.update() # ? --> what's the difference between flip and update?
    
    # limits FPS to 60
    dt = clock.tick(60) / 1000
pygame.quit()
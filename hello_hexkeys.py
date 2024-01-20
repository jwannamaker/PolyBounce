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

while running:
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill("grey")
    screen.blit(text, (0, 0))
    pygame.display.update()
    
    # FPS
    dt = clock.tick(60) / 1000
pygame.quit()
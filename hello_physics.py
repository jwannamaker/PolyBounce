import pygame
import numpy as np

# Pygame setup
pygame.init()
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Game loop flag and clock
running = True
clock = pygame.time.Clock()
dt = 0

# Physics variables
gravity = pygame.Vector2(0, 9.81)  # Gravity vector
time_step = 0.1  # Time step for the physics simulation
ball_pos = pygame.Vector2(screen_width / 2, screen_height / 2)  # Ball's position
ball_vel = pygame.Vector2(0, 0)  # Ball's velocity
ball_acc = pygame.Vector2(0, 0)  # Ball's acceleration

# Ball properties
ball_radius = 15
ball_color = WHITE

# Main game loop
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Physics update
    # Apply gravity to acceleration
    ball_acc = gravity
    # Update velocity
    ball_vel += ball_acc * time_step
    # Update position
    ball_pos += ball_vel * time_step
    # Boundary check to simulate floor
    if ball_pos.y >= screen_height - ball_radius:
        ball_pos.y = screen_height - ball_radius
        ball_vel.y *= -0.9  # A simple collision response, bouncing back with damping
    
    # Drawing
    screen.fill(BLACK)
    pygame.draw.circle(screen, ball_color, ball_pos, ball_radius)

    # Update display
    pygame.display.flip()

    # Frame rate
    dt = clock.tick(60) / 1000 # 60 frames per second

# Quit the game
pygame.quit()
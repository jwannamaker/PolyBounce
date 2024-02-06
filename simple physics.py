import pygame
import numpy as np

pygame.init()

window_width = 1200
window_height = 720
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Pygame Physics Tutorial')

clock = pygame.time.Clock()

# Setting up the object attributes
position = np.array([window_width / 2, window_height / 2])
velocity = np.array([1.0, 0])
acceleration = np.array([0.1, 0])

object_radius = 10

running = True
while running:
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_w:
                print('Move up')
            if event.key == pygame.K_s:
                print('Move down')
                
            if event.key == pygame.K_a:
                print('Move left')
            if event.key == pygame.K_d:
                print('Move right')

            if event.key == pygame.K_SPACE:
                print('JUMP player_ball')
            if event.key == pygame.K_LSHIFT:
                print('FREEZE player_ball')
        else: # elif event.type == pygame.KEYUP:
            
            
            # TODO Move player_ball according to kinematics. 
            # TODO It falls + bounces on the surface of the shape it is in
            print('free falling')
        
    screen.fill((0, 0, 0))
    
    #TODO: Update game state
    velocity += acceleration
    position += velocity
    
    # Detect collisions with the edges of the screen
    if position[0] - object_radius < 0 or position[0] + object_radius > window_width:
        velocity[0] = -velocity[0] # redirects to "bounce" back the object in the opposite x-direction
    if position[1] - object_radius < 0 or position[1] + object_radius > window_height:
        velocity[1] = -velocity[1] # redirects to "bounce" back the object in the oppisite y-direction
        
    
    # Drawing the object onto the screen
    pygame.draw.circle(screen, (255, 0, 0), position.astype(int), 10)
    
    pygame.display.flip()
    
    clock.tick(60)
    
pygame.quit()

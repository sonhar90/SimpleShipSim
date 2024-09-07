import pygame
import numpy as np
import time
from ShipModel import Ship

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Simple Ship Control System Simulation")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
font_small = pygame.font.Font(None, 24)
original_ship_image = pygame.image.load('boat.png')
ship_image = pygame.transform.scale(original_ship_image, (200, 200))

# Create the ship object
ship = Ship()

# -----------------
# --- Main loop ---
# -----------------
running = True
last_time = time.time()

while running: 
    
    # Handling events - that is keys getting pressed on the keyboard
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                ship.rps += 1.6667  # Increase RPM
            elif event.key == pygame.K_DOWN:
                ship.rps -= 1.6667  # Decrease RPM
            elif event.key == pygame.K_c:
                ship.control_active = not ship.control_active  # Toggle control
                if not ship.control_active:
                    ship.rps = 0

    # Calculate how long it is since last run (i.e. the step size), and update the ship dynamics according to this
    current_time = time.time()
    dt = current_time - last_time
    last_time = current_time
    
    ship.update_dynamics(dt) 

    # Below this line it is just about creating the pygame window 
    # Clear screen and draw
    screen.fill((135, 206, 235))  # Fill the background with sky blue color
    pygame.draw.rect(screen, (0, 105, 148), [0, 350, 800, 250])  # Draw the ocean

    # Draw the ship using the image
    ship_center = (400 + ship.position * 10, 320)
    ship_rect = ship_image.get_rect(center=ship_center)
    screen.blit(ship_image, ship_rect)

    # Red triangle pointing upwards for the setpoint
    setpoint_center = (400 + ship.setpoint * 10, 360)
    setpoint_triangle = [(setpoint_center[0] - 10, setpoint_center[1] + 20), (setpoint_center[0] + 10, setpoint_center[1] + 20), setpoint_center]
    pygame.draw.polygon(screen, (255, 0, 0), setpoint_triangle)  # Draw red triangle

    # Add text for RPM, velocity, position, and control status
    text_rpm = font.render(f'RPM: {round(ship.rps*60, 1)}', True, (0, 0, 0))
    text_vel = font.render(f'Velocity: {round(ship.velocity, 2)}', True, (0, 0, 0))
    text_pos = font.render(f'Position: {round(ship.position, 2)}', True, (0, 0, 0))
    text_ctrl = font.render(f'Control: {ship.control_active}', True, (0, 0, 0))
    screen.blit(text_rpm, (10, 10))
    screen.blit(text_vel, (180, 10))
    screen.blit(text_pos, (380, 10))
    screen.blit(text_ctrl, (580, 10))

    text_info_1 = font_small.render(f'Use UP / DOWN arrows to increase / decrease RPM', True, (0, 0, 0))
    text_info_2 = font_small.render(f'Press C button to engage position control', True, (0, 0, 0))
    screen.blit(text_info_1, (10, 550))
    screen.blit(text_info_2, (10, 570))

    # Update the display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

import pygame
import numpy as np
import time
from ShipModel import Ship
import matplotlib.pyplot as plt

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

# Setup for Matplotlib
plt.ion()  # Interactive mode on
fig, ax = plt.subplots(figsize=(8, 6))
position_data = []
setpoint_data = []
time_data = []

# Configure the plot
ax.set_title('Ship Position and Setpoint Over Time')
ax.set_xlabel('Time (s)')
ax.set_ylabel('Position / Setpoint (m)')
line1, = ax.plot(time_data, position_data, 'b-', label='Position')  # Line for position
line2, = ax.plot(time_data, setpoint_data, 'g-', label='Setpoint')  # Line for setpoint
ax.legend()

# Initialize timing
start_time = time.time()

# Define the window length (60 seconds)
window_length = 60

# -----------------
# --- Main loop ---
# -----------------
running = True
last_time = start_time

while running:
    # Handling events - that is keys getting pressed on the keyboard or mouse
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
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Update the setpoint based on where the user clicked
            mouse_x, mouse_y = event.pos
            new_setpoint = (mouse_x - 400) / 10  # Convert from screen coordinates to position
            ship.setpoint = new_setpoint

    # Calculate how long it is since last run (i.e. the step size), and update the ship dynamics according to this
    current_time = time.time()
    dt = current_time - last_time
    last_time = current_time
    
    ship.update_dynamics(dt)
    
    # Update data for plotting
    elapsed_time = current_time - start_time
    position_data.append(ship.position)
    setpoint_data.append(ship.setpoint)
    time_data.append(elapsed_time)
    
    # Remove old data to keep only the last 60 seconds
    while time_data and time_data[-1] - time_data[0] > window_length:
        time_data.pop(0)
        position_data.pop(0)
        setpoint_data.pop(0)
    
    # Update the lines for both position and setpoint
    line1.set_xdata(time_data)
    line1.set_ydata(position_data)
    line2.set_xdata(time_data)
    line2.set_ydata(setpoint_data)
    
    # Rescale the plot to fit the last 60 seconds
    ax.set_xlim(max(0, elapsed_time - window_length), elapsed_time)
    ax.relim()
    ax.autoscale_view()

    plt.draw()
    plt.pause(0.001)

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

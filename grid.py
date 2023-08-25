import pygame
import sys
import math

# Initialize pygame
pygame.init()

def move(left_vel, right_vel, dt=1):
    global x, y, theta

    # Convert velocities from [-100, 100] to [-ROBOT_SPEED, ROBOT_SPEED]
    left_vel = (left_vel / 100) * ROBOT_SPEED
    right_vel = (right_vel / 100) * ROBOT_SPEED

    # Calculate linear and angular velocities
    v = (left_vel + right_vel) / 2
    omega = (right_vel - left_vel) / ROBOT_WIDTH

    # Update robot's position and orientation
    x += v * math.cos(theta) * dt
    y += v * math.sin(theta) * dt
    theta -= omega * dt

def get_rotated_corners(x, y, width, height, theta):
    """Get the corners of a rotated rectangle."""
    half_width = width / 2
    half_height = height / 2

    # Define corners so that the shorter end is the front
    # Adjusted to start facing right
    corners = [
        (-half_width, -half_height),
        (half_width, -half_height),
        (half_width, half_height),
        (-half_width, half_height)
    ]

    rotated_corners = []
    for (dx, dy) in corners:
        new_x = x + dx * math.cos(theta) - dy * math.sin(theta)
        new_y = y + dx * math.sin(theta) + dy * math.cos(theta)
        rotated_corners.append((new_x, new_y))

    return rotated_corners

def get_aabb(corners):
    """Compute the axis-aligned bounding box of a polygon given its corners."""
    min_x = min(c[0] for c in corners)
    max_x = max(c[0] for c in corners)
    min_y = min(c[1] for c in corners)
    max_y = max(c[1] for c in corners)

    # Add some padding for safety (optional)
    padding = 1  # Adjust as needed
    return (min_x - padding, min_y - padding, max_x + padding, max_y + padding)

def check_collision(robot_corners, pillars):
    """Check if the robot collides with any pillar or the arena boundaries."""
    robot_aabb = get_aabb(robot_corners)

    # Convert robot's AABB to grid cells
    robot_grid_aabb = (
        robot_aabb[0] // CELL_SIZE,
        robot_aabb[1] // CELL_SIZE,
        robot_aabb[2] // CELL_SIZE,
        robot_aabb[3] // CELL_SIZE
    )

    # Check collision with arena boundaries
    if (robot_grid_aabb[0] < 0 or robot_grid_aabb[2] >= GRID_SIZE or
        robot_grid_aabb[1] < 0 or robot_grid_aabb[3] >= GRID_SIZE):
        return True

    # Check collision with pillars
    for pillar in pillars:
        pillar_grid_aabb = (
            pillar[0] // CELL_SIZE,
            pillar[1] // CELL_SIZE,
            (pillar[0] + PILLAR_SIZE) // CELL_SIZE,
            (pillar[1] + PILLAR_SIZE) // CELL_SIZE
        )
        if (robot_grid_aabb[2] >= pillar_grid_aabb[0] and robot_grid_aabb[0] <= pillar_grid_aabb[2] and
            robot_grid_aabb[3] >= pillar_grid_aabb[1] and robot_grid_aabb[1] <= pillar_grid_aabb[3]):
            return True

    return False

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Constants
CELL_SIZE = 20  # 5cm
GRID_SIZE = 40 # 200cm

SCREEN_WIDTH = CELL_SIZE * GRID_SIZE
SCREEN_HEIGHT = CELL_SIZE * GRID_SIZE

ROBOT_WIDTH = 5 * CELL_SIZE  # 25cm
ROBOT_HEIGHT = 4 * CELL_SIZE # 20cm
ROBOT_SPEED = CELL_SIZE // 4  # Adjust as needed for smoother movement

PILLAR_SIZE = CELL_SIZE * 2 # 5cm

# Pillars position (you can add more)
pillars = [
    [2 * CELL_SIZE, 2 * CELL_SIZE], # 15cm, 15cm or grid 3, 3
    # [32 * CELL_SIZE, 3 * CELL_SIZE], # 160cm, 15cm or grid 32, 3
    # [3 * CELL_SIZE, 32 * CELL_SIZE], # 15cm, 160cm or grid 3, 32
    # [32 * CELL_SIZE, 32 * CELL_SIZE] # 160cm, 160cm or grid 32, 32
]

# Robot parameters
x, y = 8 * CELL_SIZE, 8 * CELL_SIZE # Robot's position
theta = 0  # Robot's orientation

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('MDP Simulator')

# Main loop
running = True
while running:
    # Store the previous position and orientation
    prev_x, prev_y, prev_theta = x, y, theta
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle movement
    keys = pygame.key.get_pressed()

    # Forward and backward movement
    if keys[pygame.K_UP]:
        move(100, 100)
    elif keys[pygame.K_DOWN]:
        move(-100, -100)

    # Turning while moving forward or backward
    if keys[pygame.K_UP] and keys[pygame.K_LEFT]:
        move(50, 100)  # Forward and turn left
    elif keys[pygame.K_UP] and keys[pygame.K_RIGHT]:
        move(100, 50)  # Forward and turn right
    elif keys[pygame.K_DOWN] and keys[pygame.K_LEFT]:
        move(-100, -50)  # Backward and turn right (like reversing a car)
    elif keys[pygame.K_DOWN] and keys[pygame.K_RIGHT]:
        move(-50, -100)  # Backward and turn left


    # Check for collisions
    if check_collision(get_rotated_corners(x, y, ROBOT_WIDTH, ROBOT_HEIGHT, theta), pillars):
        # If there's a collision, revert to the previous position and orientation
        x, y, theta = prev_x, prev_y, prev_theta

    # Drawing
    screen.fill(WHITE)

    # Optionally draw the grid (for visualization)
    for i in range(GRID_SIZE):
        pygame.draw.line(screen, (220, 220, 220), (i * CELL_SIZE, 0), (i * CELL_SIZE, SCREEN_HEIGHT))
        pygame.draw.line(screen, (220, 220, 220), (0, i * CELL_SIZE), (SCREEN_WIDTH, i * CELL_SIZE))

    # Draw robot
    corners = get_rotated_corners(x, y, ROBOT_WIDTH, ROBOT_HEIGHT, theta)
    pygame.draw.polygon(screen, RED, corners)

    # Draw an indicator for the robot's front
    front_x = x + (ROBOT_WIDTH / 2) * math.cos(theta)
    front_y = y + (ROBOT_WIDTH / 2) * math.sin(theta)
    pygame.draw.line(screen, WHITE, (x, y), (front_x, front_y), 3)

    # Draw pillars
    for pillar in pillars:
        pygame.draw.rect(screen, BLUE, (pillar[0], pillar[1], PILLAR_SIZE, PILLAR_SIZE))

    pygame.display.flip()


pygame.quit()
sys.exit()

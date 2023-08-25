import pygame
import sys
import math

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
ROBOT_WIDTH = 80
ROBOT_HEIGHT = 40
ROBOT_SPEED = 5
TURN_RATE = math.pi / 36  # 5 degrees per frame
PILLAR_SIZE = 80

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('MDP Simulator')

# Robot parameters
x, y = SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2
theta = 0  # Robot's orientation

# Pillars position (you can add more)
pillars = [
    [150, 150],
    [650, 150],
    [150, 650],
    [650, 650]
]

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

    return (min_x, min_y, max_x, max_y)

def check_collision(robot_corners, pillars):
    """Check if the robot collides with any pillar or the arena boundaries."""
    robot_aabb = get_aabb(robot_corners)

    # Check collision with arena boundaries
    if robot_aabb[0] < 0 or robot_aabb[2] > SCREEN_WIDTH or robot_aabb[1] < 0 or robot_aabb[3] > SCREEN_HEIGHT:
        return True

    # Check collision with pillars
    for pillar in pillars:
        pillar_aabb = (pillar[0], pillar[1], pillar[0] + PILLAR_SIZE, pillar[1] + PILLAR_SIZE)
        if (robot_aabb[2] > pillar_aabb[0] and robot_aabb[0] < pillar_aabb[2] and
            robot_aabb[3] > pillar_aabb[1] and robot_aabb[1] < pillar_aabb[3]):
            return True

    return False


def move(left_vel, right_vel, dt=1):
    global x, y, theta

    # Convert velocities from [-100, 100] to [-ROBOT_SPEED, ROBOT_SPEED]
    left_vel = (left_vel / 100) * ROBOT_SPEED
    right_vel = (right_vel / 100) * ROBOT_SPEED

    # Calculate linear and angular velocities
    v = (left_vel + right_vel) / 2
    omega = (left_vel - right_vel) / ROBOT_WIDTH  # Adjusted the difference here

    # Update robot's position and orientation
    x += v * math.cos(theta) * dt
    y += v * math.sin(theta) * dt
    theta += omega * dt  # Adjusted the subtraction here for correct turning



# Main loop
running = True
while running:
    # Store the previous position and orientation
    prev_x, prev_y, prev_theta = x, y, theta
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # To move right, left_vel is more than right_vel
    # To move left, right_vel is more than left_vel
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        move(100, 100)
    if keys[pygame.K_DOWN]:
        move(-100, -100)
    if keys[pygame.K_LEFT]:
        move(-100, 100)
    if keys[pygame.K_RIGHT]:
        move(100, -100)

    # Drawing
    screen.fill(WHITE)

    # Draw robot as a rotated rectangle
    corners = get_rotated_corners(x, y, ROBOT_WIDTH, ROBOT_HEIGHT, theta)
    pygame.draw.polygon(screen, RED, corners)

    # Draw an indicator for the robot's front
    front_x = x + (ROBOT_WIDTH / 2) * math.cos(theta)
    front_y = y + (ROBOT_WIDTH / 2) * math.sin(theta)  # No subtraction here as we're adding the sine component
    pygame.draw.line(screen, WHITE, (x, y), (front_x, front_y), 3)

    # Check for collisions
    if check_collision(get_rotated_corners(x, y, ROBOT_WIDTH, ROBOT_HEIGHT, theta), pillars):
        # If there's a collision, revert to the previous position and orientation
        x, y, theta = prev_x, prev_y, prev_theta

    # Draw pillars
    for pillar in pillars:
        pygame.draw.rect(screen, BLUE, (pillar[0], pillar[1], PILLAR_SIZE, PILLAR_SIZE))

    pygame.display.flip()

pygame.quit()
sys.exit()

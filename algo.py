import pygame
import sys
import math
<<<<<<< Updated upstream
=======
import queue
import time
>>>>>>> Stashed changes

# Initialize pygame
pygame.init()

<<<<<<< Updated upstream
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
=======
# Constants for the grid system
GRID_SIZE = 20
CELL_SIZE = 10
ROBOT_GRID_SIZE = 3

# Scaling for visualization
SCALE_FACTOR = 3

# Screen dimensions
BUTTON_PANEL_WIDTH = 250  # Adjust as needed
SCREEN_WIDTH = GRID_SIZE * CELL_SIZE * SCALE_FACTOR + BUTTON_PANEL_WIDTH

SCREEN_HEIGHT = GRID_SIZE * CELL_SIZE * SCALE_FACTOR

BUTTON_WIDTH = 60
BUTTON_HEIGHT = 40
BUTTON_SPACING = 10

# Colors
WHITE = (255, 255, 255)
RED = (210, 43, 43)
GREEN = (0, 255, 0)
BLUE = (0, 150, 255)
LIGHT_GRAY = (220, 220, 220)
DARK_GRAY = (128, 128, 128)
BLACK = (0, 0, 0)
LIGHT_RED = (255, 200, 200)
YELLOW = (200, 200, 0)



def scaled(value):
    return value * SCALE_FACTOR

def adjust_y(y, height):
    return SCREEN_HEIGHT - y - height


class Robot:
    def __init__(self, x, y, direction='E'):
        self.x = x
        self.y = y
        self.direction = direction
        self.turning_radius = 4

    def check_within_arena(self, new_x, new_y):
        # Check if the entire 3x3 robot footprint is within the arena
        return 0 <= new_x <= GRID_SIZE - 3 and 0 <= new_y <= GRID_SIZE - 3

    def check_collision(self, new_x, new_y, pillar_x, pillar_y):
        # Check if any part of the 3x3 robot footprint overlaps with the 3x3 pillar footprint
        for dx in range(3):  # Robot footprint width
            for dy in range(3):  # Robot footprint height
                for pdx in range(-1, 2):  # Pillar footprint width
                    for pdy in range(-1, 2):  # Pillar footprint height
                        if new_x + dx == pillar_x + pdx and new_y + dy == pillar_y + pdy:
                            return True
        return False

    def move(self, dx, dy, new_direction):
        new_x = self.x + dx
        new_y = self.y + dy

        # Check for collision with pillars
        for pillar in pillars:
            if self.check_collision(new_x, new_y, pillar.x, pillar.y):
                print("Collision detected!")
                return  # Collision detected with pillar
            
        # Check for collision with arena boundaries
        if not self.check_within_arena(new_x, new_y):
            print("Collision detected with arena boundary!")
            return  # Collision detected with arena boundary

        # Update position and direction
        self.x = new_x
        self.y = new_y
        self.direction = new_direction

    def move_forward(self):
        dx, dy = 0, 0
        if self.direction == 'E':
            dx = 1
        elif self.direction == 'W':
            dx = -1
        elif self.direction == 'N':
            dy = 1
        elif self.direction == 'S':
            dy = -1

        self.move(dx, dy, self.direction)

    def move_backward(self):
        dx, dy = 0, 0
        if self.direction == 'E':
            dx = -1
        elif self.direction == 'W':
            dx = 1
        elif self.direction == 'N':
            dy = -1
        elif self.direction == 'S':
            dy = 1

        self.move(dx, dy, self.direction)

    def move_forward_right(self):
        dx, dy = 0, 0
        new_direction = ''
        if self.direction == 'N':
            dx, dy = self.turning_radius, self.turning_radius
            new_direction = 'E'
        elif self.direction == 'E':
            dx, dy = self.turning_radius, -self.turning_radius
            new_direction = 'S'
        elif self.direction == 'S':
            dx, dy = -self.turning_radius, -self.turning_radius
            new_direction = 'W'
        elif self.direction == 'W':
            dx, dy = -self.turning_radius, self.turning_radius
            new_direction = 'N'

        self.move(dx, dy, new_direction)

    def move_forward_left(self):
        dx, dy = 0, 0
        new_direction = ''
        if self.direction == 'N':
            dx, dy = -self.turning_radius, self.turning_radius
            new_direction = 'W'
        elif self.direction == 'W':
            dx, dy = -self.turning_radius, -self.turning_radius
            new_direction = 'S'
        elif self.direction == 'S':
            dx, dy = self.turning_radius, -self.turning_radius
            new_direction = 'E'
        elif self.direction == 'E':
            dx, dy = self.turning_radius, self.turning_radius
            new_direction = 'N'

        self.move(dx, dy, new_direction)

    def move_backward_right(self):
        dx, dy = 0, 0
        new_direction = ''
        if self.direction == 'N':
            dx, dy = self.turning_radius, -self.turning_radius
            new_direction = 'W'
        elif self.direction == 'E':
            dx, dy = -self.turning_radius, -self.turning_radius
            new_direction = 'N'
        elif self.direction == 'S':
            dx, dy = -self.turning_radius, self.turning_radius
            new_direction = 'E'
        elif self.direction == 'W':
            dx, dy = self.turning_radius, self.turning_radius
            new_direction = 'S'

        self.move(dx, dy, new_direction)

    def move_backward_left(self):
        dx, dy = 0, 0
        new_direction = ''
        if self.direction == 'N':
            dx, dy = -self.turning_radius, -self.turning_radius
            new_direction = 'E'
        elif self.direction == 'E':
            dx, dy = -self.turning_radius, self.turning_radius
            new_direction = 'S'
        elif self.direction == 'S':
            dx, dy = self.turning_radius, self.turning_radius
            new_direction = 'W'
        elif self.direction == 'W':
            dx, dy = self.turning_radius, -self.turning_radius
            new_direction = 'N'

        self.move(dx, dy, new_direction)


    def draw(self, screen):
        adjusted_y = adjust_y(scaled(self.y * CELL_SIZE), scaled(CELL_SIZE * 3))
        pygame.draw.rect(screen, RED, (scaled(self.x * CELL_SIZE), adjusted_y, scaled(CELL_SIZE * 3), scaled(CELL_SIZE * 3)), 2)

        # Define body dimensions
        body_width = scaled(CELL_SIZE * 2)
        body_height = scaled(CELL_SIZE)
        if self.direction in ['N', 'S']:
            body_width, body_height = body_height, body_width

        body_x = scaled(self.x * CELL_SIZE) + (scaled(CELL_SIZE * 3) - body_width) / 2
        body_y = adjust_y(scaled(self.y * CELL_SIZE), scaled(CELL_SIZE * 3)) + (scaled(CELL_SIZE * 3) - body_height) / 2

        # Define wheel and headlight sizes
        wheel_width = scaled(CELL_SIZE * 0.3)
        wheel_height = scaled(CELL_SIZE * 0.3)
        headlight_width = scaled(CELL_SIZE * 0.15)
        headlight_height = scaled(CELL_SIZE * 0.2)

        # Adjust positions based on direction
        if self.direction in ['E', 'W']:
            wheel_positions = [
                (body_x, body_y - wheel_height),
                (body_x + body_width - wheel_width, body_y - wheel_height),
                (body_x, body_y + body_height),
                (body_x + body_width - wheel_width, body_y + body_height)
            ]
        else:  # 'N' and 'S'
            wheel_positions = [
                (body_x - wheel_width, body_y),
                (body_x - wheel_width, body_y + body_height - wheel_height),
                (body_x + body_width, body_y),
                (body_x + body_width, body_y + body_height - wheel_height)
            ]

        # Headlight positions 
        if self.direction == 'E':
            headlight_positions = [
                (body_x + body_width, body_y + 0.25 * body_height),
                (body_x + body_width, body_y + 0.75 * body_height - headlight_height)
            ]
        elif self.direction == 'W':
            headlight_positions = [
                (body_x - headlight_width, body_y + 0.25 * body_height),
                (body_x - headlight_width, body_y + 0.75 * body_height - headlight_height)
            ]
        elif self.direction == 'N':
            headlight_positions = [
                (body_x + 0.25 * body_width, body_y - headlight_height),
                (body_x + 0.75 * body_width - headlight_width, body_y - headlight_height)
            ]
        elif self.direction == 'S':
            headlight_positions = [
                (body_x + 0.25 * body_width, body_y + body_height),
                (body_x + 0.75 * body_width - headlight_width, body_y + body_height)
            ]

        # Draw wheels
        for wx, wy in wheel_positions:
            pygame.draw.rect(screen, BLACK, (wx, wy, wheel_width, wheel_height))

        # Draw body
        pygame.draw.rect(screen, DARK_GRAY, (body_x, body_y, body_width, body_height))

        # Draw headlights
        for hx, hy in headlight_positions:
            pygame.draw.rect(screen, YELLOW, (hx, hy, headlight_width, headlight_height))

class Pillar:
    def __init__(self, x, y, image_direction='N'):
        self.x = x
        self.y = y
        self.boolReached = False
        self.image_direction = image_direction

    def draw(self, screen):
        border_thickness = 1  

        # Draw the pillar boundary with borders
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if self.y + dy < 0 or self.y + dy >= GRID_SIZE or self.x + dx < 0 or self.x + dx >= GRID_SIZE:
                    continue # Do not draw if out of bounds
                adjusted_y = adjust_y(scaled((self.y + dy) * CELL_SIZE), scaled(CELL_SIZE))
                pygame.draw.rect(screen, LIGHT_RED, (scaled((self.x + dx) * CELL_SIZE), adjusted_y, scaled(CELL_SIZE), scaled(CELL_SIZE)))
                pygame.draw.rect(screen, DARK_GRAY, (scaled((self.x + dx) * CELL_SIZE), adjusted_y, scaled(CELL_SIZE), scaled(CELL_SIZE)), 1)
                
        # Draw the pillar center
        color = GREEN if self.boolReached else RED
        adjusted_y = adjust_y(scaled(self.y * CELL_SIZE), scaled(CELL_SIZE))
        
        pygame.draw.rect(screen, color, (scaled(self.x * CELL_SIZE) + border_thickness, 
                                        adjusted_y + border_thickness, 
                                        scaled(CELL_SIZE) - 2 * border_thickness, 
                                        scaled(CELL_SIZE) - 2 * border_thickness))

        # Draw the image direction indicator
        quarter_cell = scaled(CELL_SIZE) / 4
        adjusted_y = adjust_y(scaled(self.y * CELL_SIZE), scaled(CELL_SIZE))

        if self.image_direction == 'N':
            pygame.draw.rect(screen, BLUE, 
                            (scaled(self.x * CELL_SIZE) + border_thickness, 
                            adjusted_y + 3 * quarter_cell, 
                            scaled(CELL_SIZE) - 2 * border_thickness, 
                            quarter_cell - border_thickness))
        elif self.image_direction == 'S':
            pygame.draw.rect(screen, BLUE, 
                            (scaled(self.x * CELL_SIZE) + border_thickness, 
                            adjusted_y + border_thickness, 
                            scaled(CELL_SIZE) - 2 * border_thickness, 
                            quarter_cell - border_thickness))
        elif self.image_direction == 'E':
            pygame.draw.rect(screen, BLUE, 
                            (scaled(self.x * CELL_SIZE) + 3 * quarter_cell, 
                            adjusted_y + border_thickness, 
                            quarter_cell - border_thickness, 
                            scaled(CELL_SIZE) - 2 * border_thickness))
        elif self.image_direction == 'W':
            pygame.draw.rect(screen, BLUE, 
                            (scaled(self.x * CELL_SIZE) + border_thickness, 
                            adjusted_y + border_thickness, 
                            quarter_cell - border_thickness, 
                            scaled(CELL_SIZE) - 2 * border_thickness))
            
class Button:
    def __init__(self, x, y, width, height, text, color, action=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.action = action

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont(None, 25)
        text_surf = font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=(self.x + self.width/2, self.y + self.height/2))
        screen.blit(text_surf, text_rect)

    def is_over(self, pos):
        return self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height


# Sample pillars
pillars = [
    Pillar(5, 5, 'N'), 
    # Pillar(15, 5, 'E'), 
    # Pillar(5, 15, 'S'), 
    # Pillar(15, 15, 'W'), 
    # Pillar(19, 15, 'W')
]
#END GOAL FOR EACH PILLAR IS State(pillar.x-4, pillar.y-1, pillar.image_direction)


# Initialize robot
robot = Robot(1, 1, 'E')
# Starting position for the top-left button
start_x = SCREEN_WIDTH - BUTTON_PANEL_WIDTH + (BUTTON_PANEL_WIDTH - 3*BUTTON_WIDTH - 2*BUTTON_SPACING) / 2
start_y = 100  # Adjust this value to position the table vertically as desired

buttons = [
    Button(start_x, start_y, BUTTON_WIDTH, BUTTON_HEIGHT, "Fwd-L", LIGHT_GRAY, robot.move_forward_left),
    Button(start_x + BUTTON_WIDTH + BUTTON_SPACING, start_y, BUTTON_WIDTH, BUTTON_HEIGHT, "Fwd", LIGHT_GRAY, robot.move_forward),
    Button(start_x + 2*(BUTTON_WIDTH + BUTTON_SPACING), start_y, BUTTON_WIDTH, BUTTON_HEIGHT, "Fwd-R", LIGHT_GRAY, robot.move_forward_right),
    Button(start_x, start_y + BUTTON_HEIGHT + BUTTON_SPACING, BUTTON_WIDTH, BUTTON_HEIGHT, "Bwd-L", LIGHT_GRAY, robot.move_backward_left),
    Button(start_x + BUTTON_WIDTH + BUTTON_SPACING, start_y + BUTTON_HEIGHT + BUTTON_SPACING, BUTTON_WIDTH, BUTTON_HEIGHT, "Bwd", LIGHT_GRAY, robot.move_backward),
    Button(start_x + 2*(BUTTON_WIDTH + BUTTON_SPACING), start_y + BUTTON_HEIGHT + BUTTON_SPACING, BUTTON_WIDTH, BUTTON_HEIGHT, "Bwd-R", LIGHT_GRAY, robot.move_backward_right)
]

def draw_arena():
    screen.fill(WHITE)

    # Draw buttons
    for button in buttons:
        button.draw(screen)

    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            adjusted_y = adjust_y(scaled(y * CELL_SIZE), scaled(CELL_SIZE))
            pygame.draw.rect(screen, DARK_GRAY, (scaled(x * CELL_SIZE), adjusted_y, scaled(CELL_SIZE), scaled(CELL_SIZE)), 1)

    
    # Draw pillars
    for pillar in pillars:
        pillar.draw(screen)
    
    # Draw robot
    robot.draw(screen)

    pygame.display.flip()


#NEW CODE FOR ALGO FROM A STATE TO PILLAR

def calc_dist(state, pillar):
    # Calculate the distance between the state and the pillar
    x1, y1 = state.x, state.y
    x2, y2 = pillar.x, pillar.y
    distance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    return distance

# Define state representation
class State:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.turning_radius = 4
        self.parent = None


    def check_within_arena(self, new_x, new_y):
        # Check if the entire 3x3 robot footprint is within the arena
        return 0 <= new_x <= GRID_SIZE - 3 and 0 <= new_y <= GRID_SIZE - 3

    def check_collision(self, new_x, new_y, pillar_x, pillar_y):
        # Check if any part of the 3x3 robot footprint overlaps with the 3x3 pillar footprint
        for dx in range(3):  # Robot footprint width
            for dy in range(3):  # Robot footprint height
                for pdx in range(-1, 2):  # Pillar footprint width
                    for pdy in range(-1, 2):  # Pillar footprint height
                        if new_x + dx == pillar_x + pdx and new_y + dy == pillar_y + pdy:
                            return True
        return False

    def check_move(self, dx, dy, new_direction):
        new_x = self.x + dx
        new_y = self.y + dy

        # Check for collision with pillars
        for pillar in pillars:
            if self.check_collision(new_x, new_y, pillar.x, pillar.y):
                return None # Collision detected with pillar
            
        # Check for collision with arena boundaries
        if not self.check_within_arena(new_x, new_y):
            return None # Collision detected with arena boundary

        # Update position and direction
        return State(new_x,new_y,new_direction)

    def move_forward(self):
        dx, dy = 0, 0
        if self.direction == 'E':
            dx = 1
        elif self.direction == 'W':
            dx = -1
        elif self.direction == 'N':
            dy = 1
        elif self.direction == 'S':
            dy = -1

        return self.check_move(dx, dy, self.direction), "F"

    def move_backward(self):
        dx, dy = 0, 0
        if self.direction == 'E':
            dx = -1
        elif self.direction == 'W':
            dx = 1
        elif self.direction == 'N':
            dy = -1
        elif self.direction == 'S':
            dy = 1

        return self.check_move(dx, dy, self.direction), "B"

    def move_forward_right(self):
        dx, dy = 0, 0
        new_direction = ''
        if self.direction == 'N':
            dx, dy = self.turning_radius, self.turning_radius
            new_direction = 'E'
        elif self.direction == 'E':
            dx, dy = self.turning_radius, -self.turning_radius
            new_direction = 'S'
        elif self.direction == 'S':
            dx, dy = -self.turning_radius, -self.turning_radius
            new_direction = 'W'
        elif self.direction == 'W':
            dx, dy = -self.turning_radius, self.turning_radius
            new_direction = 'N'

        return self.check_move(dx, dy, new_direction), "FR"

    def move_forward_left(self):
        dx, dy = 0, 0
        new_direction = ''
        if self.direction == 'N':
            dx, dy = -self.turning_radius, self.turning_radius
            new_direction = 'W'
        elif self.direction == 'W':
            dx, dy = -self.turning_radius, -self.turning_radius
            new_direction = 'S'
        elif self.direction == 'S':
            dx, dy = self.turning_radius, -self.turning_radius
            new_direction = 'E'
        elif self.direction == 'E':
            dx, dy = self.turning_radius, self.turning_radius
            new_direction = 'N'

        return self.check_move(dx, dy, new_direction), "FL"

    def move_backward_right(self):
        dx, dy = 0, 0
        new_direction = ''
        if self.direction == 'N':
            dx, dy = self.turning_radius, -self.turning_radius
            new_direction = 'W'
        elif self.direction == 'E':
            dx, dy = -self.turning_radius, -self.turning_radius
            new_direction = 'N'
        elif self.direction == 'S':
            dx, dy = -self.turning_radius, self.turning_radius
            new_direction = 'E'
        elif self.direction == 'W':
            dx, dy = self.turning_radius, self.turning_radius
            new_direction = 'S'

        return self.check_move(dx, dy, new_direction), "BR"

    def move_backward_left(self):
        dx, dy = 0, 0
        new_direction = ''
        if self.direction == 'N':
            dx, dy = -self.turning_radius, -self.turning_radius
            new_direction = 'E'
        elif self.direction == 'E':
            dx, dy = -self.turning_radius, self.turning_radius
            new_direction = 'S'
        elif self.direction == 'S':
            dx, dy = self.turning_radius, self.turning_radius
            new_direction = 'W'
        elif self.direction == 'W':
            dx, dy = self.turning_radius, -self.turning_radius
            new_direction = 'N'

        return self.check_move(dx, dy, new_direction), "BL"
    
end_goals = []
for pillar in pillars:
    if pillar.image_direction == 'N':
        direction = 'S'
        end_goals.append(State(pillar.x-1, pillar.y+1, direction))
    if pillar.image_direction == 'S':
        direction = 'N'
        end_goals.append(State(pillar.x-1, pillar.y-4, direction))
    if pillar.image_direction == 'E':
        direction = 'W'
        end_goals.append(State(pillar.x+4, pillar.y-1, direction))
    if pillar.image_direction == 'W':
        direction = 'E'
        end_goals.append(State(pillar.x-4, pillar.y-1, direction))


class PrioritizedItem:
    def __init__(self, item, priority):
        self.item = item
        self.priority = priority

    def __lt__(self, other):
        # Compare based on priority (total_cost)
        return self.priority < other.priority

def a_star_search(start_state, end_goal):
    # Initialize the open and closed sets
    open_set = queue.PriorityQueue()
    closed_set = set()

    # Initialize dictionaries to keep track of actions and costs
    actions = {start_state: []}
    costs = {start_state: 0}

    # Add the start state to the open set with priority 0
    open_set.put(PrioritizedItem(start_state, 0))

    while not open_set.empty():
        current_item = open_set.get()
        current_state = current_item.item

        if current_state.x == end_goal.x and current_state.y == end_goal.y and current_state.direction == end_goal.direction:
            # Found the goal state, return the sequence of actions
            return actions[current_state]

        if current_state in closed_set:
            continue

        closed_set.add(current_state)

        # Generate possible successor states
        successor_states = [
            current_state.move_forward(),
            current_state.move_backward(),
            current_state.move_forward_right(),
            current_state.move_forward_left(),
            current_state.move_backward_right(),
            current_state.move_backward_left()
        ]
        print(f"current State: {current_state.x},{current_state.y},{current_state.direction}")
        for successor in successor_states:
            new_state, action = successor
            if new_state:
                # Calculate the cost for this action
                if action == "F" or "B":
                    action_cost = 10
                else:
                    action_cost = 50

                # Calculate the estimated cost to reach the goal (heuristic)
                estimated_cost = calc_dist(new_state, end_goal)  # You need to implement calc_dist

                # Calculate the total cost
                total_cost = costs[current_state] + action_cost + estimated_cost

                if new_state not in costs or total_cost < costs[new_state]:
                    # Update the action and cost dictionaries
                    actions[new_state] = actions[current_state] + [action]
                    costs[new_state] = total_cost

                    # Add the new_state to the open set with the total_cost as the priority
                    open_set.put(PrioritizedItem(new_state, total_cost))

    # If no path is found, return None
    return None



def main():
    global robot, pillars  # Allow modification of global variables
    # Choose an end goal (e.g., end_goals[0])
    end_goal = end_goals[0]
    print(f"end goal: {end_goal.x},{end_goal.y},{end_goal.direction}")
    # Find the shortest path from the starting state to the end goal
    start_state = State(1, 1, 'E')
    shortest_path = a_star_search(start_state, end_goal)
    if shortest_path:
        # Print the sequence of actions in the shortest path
        for action in shortest_path:
            print(action)
    else:
        print("No path found to the end goal.")
    draw_arena()
    for action in shortest_path:
        time.sleep(1)
        if action == "F":
            robot.move_forward()
        elif action == "B":
            robot.move_backward()
        elif action == "FL":
            robot.move_forward_left()
        elif action == "FR":
            robot.move_forward_right()
        elif action == "BL":
            robot.move_backward_left()
        elif action == "BR":
            robot.move_backward_right()
        draw_arena()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.is_over(pygame.mouse.get_pos()):
                        if button.action:
                            button.action()
        draw_arena()
        pygame.time.Clock().tick(60)


if __name__ == "__main__":
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Robot Simulator")
    main()
>>>>>>> Stashed changes

import pygame
import sys

# Initialize pygame
pygame.init()

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
    # Pillar(5, 5, 'N'), 
    # Pillar(15, 5, 'E'), 
    # Pillar(5, 15, 'S'), 
    # Pillar(15, 15, 'W'), 
    Pillar(19, 15, 'W')
]

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

def main():
    global robot, pillars  # Allow modification of global variables
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

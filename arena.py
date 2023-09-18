import matplotlib.pyplot as plt
import matplotlib.patches as patches
from params import ARENA_WIDTH, ARENA_HEIGHT, CELL_SIZE

def draw_arena_boundary():
    """Draw the actual boundary of the arena."""
    boundary = patches.Rectangle((0, 0), ARENA_WIDTH, ARENA_HEIGHT, 
                                 fill=False, edgecolor='black', linewidth=2)
    plt.gca().add_patch(boundary)

def world2grid(robot):
    x = robot.x
    y = robot.y
    degrees = robot.degrees

    # Convert world position to grid position
    grid_x = int(x / CELL_SIZE)
    grid_y = int(y / CELL_SIZE)
    
    # Convert degrees to closest cardinal direction
    if (0 <= degrees <= 45) or (315 <= degrees < 360):
        strDirection = "R"  # Right
    elif 45 <= degrees < 135:
        strDirection = "U"  # Up
    elif 135 <= degrees < 225:
        strDirection = "L"  # Left
    else:
        strDirection = "D"  # Down

    return (grid_x, grid_y), strDirection
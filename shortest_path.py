import matplotlib.pyplot as plt
import math
import reeds_shepp as rs
from reeds_shepp import path_length
from pillars import get_pillars
from robot import Robot
from params import ARENA_WIDTH, ARENA_HEIGHT, CELL_SIZE
from arena import draw_arena_boundary, world2grid

# Set up the figure and axis
fig, ax = plt.subplots()
ax.set_title('MDP Simulator', fontsize=16)

def main():
    PADDING = 50  # cm beyond the arena for visualization purposes
    ax.set_xlim(-PADDING, ARENA_WIDTH + PADDING)
    ax.set_ylim(-PADDING, ARENA_HEIGHT + PADDING)
    
    # Draw the grid, including the padding area
    for i in range(-PADDING, ARENA_WIDTH + PADDING + CELL_SIZE, CELL_SIZE):
        ax.axvline(i, color='gray', linestyle='--', linewidth=0.5)
        ax.axhline(i, color='gray', linestyle='--', linewidth=0.5)
    
    # Draw the arena boundary
    draw_arena_boundary()

    start_robot = Robot(20, 0, 0, 'lightblue')
    start_robot.draw(True)

    #? Checking Collision
    # pillar_data = [(50, 50, 'E'), (150, 150, 'S')]
    # pillars = get_pillars(pillar_data)

    # robot = Robot(14.352, 8.928, 63.768, 'lightblue', pillars)
    # robot.draw()

    # for pillar in pillars:
    #     pillar.draw(ax)

    # collision = robot.collision_detected(robot.x, robot.y, robot.degrees)
    # print(collision)  # It will print True if there's a collision, otherwise False.

    # plt.show()


    #? Finding path
    pillar_data = [(30, 150, 'S'), (150, 150, 'W')]
    pillars = get_pillars(pillar_data)

    robot = Robot(0, 0, 0, pillars) # Robot starts at (0, 0) facing right

    for pillar in pillars:
        pillar.draw(ax)

    PATH = [(0,0,0), (20, 0, 0)] # Force robot to move forward at start to allow for turn
    for pillar in pillars:
        pillar.draw(ax)
        PATH.append(pillar.getWaypoint())

    path_robots = []
    for waypoint in PATH:
        path_robots.append(Robot(waypoint[0], waypoint[1], waypoint[2], 'lightblue'))
        
    for probot in path_robots:
        probot.draw()

    path_length = 0
    final_path = []

    for i in range(len(PATH) - 1):
        paths = rs.get_sorted_paths(PATH[i], PATH[i+1])

        # Check if no path exist
        if not paths:
            print("No path exists between {} and {}.".format(PATH[i], PATH[i+1]))
            continue

        valid_path_found = False
        for potential_path in paths:
            collision_detected, end_x, end_y, end_degrees = robot.simulate_reeds_shepps_path(potential_path, robot.sim_x, robot.sim_y, robot.degrees)
            
            if not collision_detected:
                # If there is no collision, it's a valid path.
                print(f"Path Found and Added!: {potential_path}, length: {rs.path_length(potential_path)}")
                final_path.append(potential_path)
                path_length += rs.path_length(potential_path)
                valid_path_found = True
                
                # Update the robot's position and orientation for the next segment
                robot.sim_x, robot.sim_y, robot.degrees = end_x, end_y, end_degrees
                break

        if not valid_path_found:
            print(f"No valid paths found between {PATH[i]} and {PATH[i+1]}.")

        # Now you have your final path (which is a list of paths) and its length.
        print("Final Path Length:", path_length)

    # for path in final_path:
    #     print("Path:")
    #     for instruction in path:
    #         print(instruction)

    # print(f"Number of paths: {len(final_path)}")

    robot.follow_reeds_shepps(final_path)

    #print(f"Shortest path length: {path_length} cm")
    plt.show()

if __name__ == '__main__':
    main()

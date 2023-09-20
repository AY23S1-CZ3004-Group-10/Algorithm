import matplotlib.pyplot as plt
import reeds_shepp as rs
from pillars import get_pillars
from robot import Robot
from params import ARENA_WIDTH, ARENA_HEIGHT, CELL_SIZE
from arena import draw_arena_boundary, world2grid
import itertools
import math

def visualize(position, circles=False, color='orange'):
    pillar_data = [(80, 80, 'E'), (110, 20, 'E'), (190, 60, 'W'), (170, 180, 'S'), (70, 120, 'N'), (0, 80, 'E')]
    # pillar_data = [(100, 70, 'E')]
    pillars = get_pillars(pillar_data)

    robot = Robot(position[0], position[1], position[2], pillars, color)
    robot.draw(circles)

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


    #? Finding path
    # [105, 75, 180, 0], [135, 25, 0, 1], [195, 95, 180, 2], [175, 185, -90, 3], [75, 125, 90, 4], [15, 185, -90, 5]
    # pillar_data = [(80, 80, 'E'), (110, 20, 'E'), (190, 60, 'W'), (170, 180, 'S'), (70, 120, 'N'), (0, 80, 'E')]
    pillar_data = [(180, 180, 'S'), (20, 170, 'E'), (180, 20, 'W')]
    pillars = get_pillars(pillar_data)

    robot = Robot(20, 20, 0, pillars) # Robot starting position
    for pillar in pillars:
        pillar.draw(ax)

    waypoints = []
    for pillar in pillars:
        pillar.draw(ax)
        waypoints.append(pillar.getWaypoint())

    print("Waypoints:", waypoints)

    path_robots = [Robot(robot.x, robot.y, robot.degrees, get_pillars([]), 'lightblue')]
    for waypoint in waypoints:
        path_robots.append(Robot(waypoint[0], waypoint[1], waypoint[2], get_pillars([]), 'lightblue'))

    for probot in path_robots:
        probot.draw(False)

    #hamiltonian path test
    perms = list(itertools.permutations(waypoints))

    def calc_distance(path):
            # Create all target points, including the start.
            dist = math.sqrt(((path[0][0] - robot.x) ** 2) +
                                  ((path[0][1] - robot.y) ** 2))
            for i in range(len(path) - 1):
                dist += math.sqrt(((path[i][0] - path[i + 1][0]) ** 2) +
                                  ((path[i][1] - path[i + 1][1]) ** 2))
            return dist
    PATHS = sorted(perms, key=calc_distance)

    def has_final_path(PATH):
        path_length = 0
        for i in range(len(PATH) - 1):
            print(f"Finding path from {PATH[i]} to {PATH[i+1]}...")
            paths = rs.get_sorted_paths(PATH[i], PATH[i+1])

            # Check if no path exist
            if not paths:
                print("No path exists between {} and {}.".format(PATH[i], PATH[i+1]))
                return False

            valid_path_found = False
            for potential_path in paths:
                collision_detected, end_x, end_y, end_degrees = robot.simulate_reeds_shepps_path(potential_path, robot.sim_x, robot.sim_y, robot.sim_degrees)

                if not collision_detected:
                    # If there is no collision, it's a valid path.
                    print(f"Path Found and Added!: {potential_path}, length: {rs.path_length(potential_path)}")
                    final_path.append(potential_path)
                    path_length += rs.path_length(potential_path)
                    valid_path_found = True

                    # Update the robot's position and orientation for the next segment
                    robot.sim_x, robot.sim_y, robot.sim_degrees = end_x, end_y, end_degrees
                    break

            if not valid_path_found:
                print(f"No valid paths found between {PATH[i]} and {PATH[i+1]}.")
                return False

        # Now you have your final path (which is a list of paths) and its length.
        print("Final Path Length:", path_length)
        return True

    final_path = []
    for PATH in PATHS:
        # insert starting point
        l = list(PATH)
        l.insert(0, (robot.x, robot.y, robot.degrees))
        PATH = tuple(l)
        if has_final_path(PATH):
            break
        final_path = []

    if not final_path:
        print("No Paths Found at All!")


    for path in final_path:
        print("Path:")
        for instruction in path:
            print(instruction)

    print(f"Number of paths: {len(final_path)}")

    robot.follow_reeds_shepps(final_path)

    #print(f"Shortest path length: {path_length} cm")
    plt.show()

    # #? Finding path
    # # [105, 75, 180, 0], [135, 25, 0, 1], [195, 95, 180, 2], [175, 185, -90, 3], [75, 125, 90, 4], [15, 185, -90, 5]
    # # pillar_data = [(30, 150, 'S'), (150, 150, 'W')]
    # pillar_data = [(100,60,'N'), (100,20,'E'), (190,90,'W'), (50,180,'S')]
    # pillars = get_pillars(pillar_data)

    # robot = Robot(20, 20, 0, pillars) # Robot starts at (0, 0) facing right

    # PATH = [(robot.x, robot.y, robot.degrees)] # Force robot to move forward at start to allow for turn
    # for pillar in pillars:
    #     pillar.draw(ax)
    #     PATH.append(pillar.getWaypoint())

    # print(f"Waypoints: {PATH}")

    # #hamiltonian path test
    # perms = list(itertools.permutations(PATH))
    # def calc_distance(path):
    #         # Create all target points, including the start.
    #         dist = 0
    #         for i in range(len(path) - 1):
    #             dist += math.sqrt(((path[i][0] - path[i + 1][0]) ** 2) +
    #                               ((path[i][1] - path[i + 1][1]) ** 2))
    #         return dist
    # PATHS = sorted(perms, key=calc_distance)

    # def compute_final_path(PATH):
    #     path_length = 0
    #     for i in range(len(PATH) - 1):
    #         paths = rs.get_sorted_paths(PATH[i], PATH[i+1])

    #         # Check if no path exist
    #         if not paths:
    #             print("No path exists between {} and {}.".format(PATH[i], PATH[i+1]))
    #             return False

    #         valid_path_found = False
    #         for potential_path in paths:
    #             collision_detected, end_x, end_y, end_degrees = robot.simulate_reeds_shepps_path(potential_path, robot.sim_x, robot.sim_y, robot.degrees)
                
    #             if not collision_detected:
    #                 # If there is no collision, it's a valid path.
    #                 print(f"Path Found and Added!: {potential_path}, length: {rs.path_length(potential_path)}")
    #                 final_path.append(potential_path)
    #                 path_length += rs.path_length(potential_path)
    #                 valid_path_found = True
                    
    #                 # Update the robot's position and orientation for the next segment
    #                 robot.sim_x, robot.sim_y, robot.sim_degrees = end_x, end_y, end_degrees
    #                 break

    #         if not valid_path_found:
    #             print(f"No valid paths found between {PATH[i]} and {PATH[i+1]}.")
    #             return False

    #         # Now you have your final path (which is a list of paths) and its length.
    #         print("Final Path Length:", path_length)
    #     return True
    
    # for PATH in PATHS:
    #     path_robots = []

    #     for waypoint in PATH:
    #         path_robots.append(Robot(waypoint[0], waypoint[1], waypoint[2], 'lightblue'))
            
    #     for probot in path_robots:
    #         probot.draw()
        
    #     final_path = []
    #     if compute_final_path(PATH):
    #         break
    #     final_path = []
    # if not final_path:
    #     print("NO PATHS FOUND AT ALL")

    # for path in final_path:
    #     print("Path:")
    #     for instruction in path:
    #         print(instruction)

    # print(f"Number of paths: {len(final_path)}")

    # robot.follow_reeds_shepps(final_path)

    # #print(f"Shortest path length: {path_length} cm")
    # plt.show()

if __name__ == '__main__':
    main()

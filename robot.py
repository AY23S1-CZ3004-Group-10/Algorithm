import math
from utils import rad2deg
from matplotlib import patches
import matplotlib.pyplot as plt
from reeds_shepp import Steering, Gear
from pillars import get_pillars
from params import ARENA_WIDTH, ARENA_HEIGHT, ROBOT_ACTUAL_WIDTH, ROBOT_ACTUAL_LENGTH, ROBOT_FOOTPRINT_WIDTH, ROBOT_FOOTPRINT_HEIGHT, MIN_RADIUS

class Robot:
    def __init__(self, x, y, degrees, pillars, color='lightblue'):
        self.x = x
        self.y = y
        self.degrees = degrees # 0 degrees is facing right, 90 degrees is facing up, etc.
        self.pillars = pillars
        self.color = color
    
        self.min_radius = MIN_RADIUS
        self.sim_x = x
        self.sim_y = y
        self.sim_degrees = degrees

    def draw_arc(self, radius, angle_deg, color='green'):
        """Draws an arc with given radius and angle."""
        if radius > 0: # Left turn
            circle_x, circle_y = self.get_left_circle_center(self.x, self.y)
            start_angle = self.degrees - 90
        else: # Right turn
            circle_x, circle_y = self.get_right_circle_center(self.x, self.y)
            start_angle = self.degrees + 90

        # Print debugging information
        # print(f"Draw Arc - Radius: {radius}, Start Angle: {start_angle}, Arc Angle: {angle_deg}")

        # Rotate turning circle centers based on the given degrees around (x, y)
        r_circle_x, r_circle_y = self.rotate_point(circle_x, circle_y, self.x, self.y, self.degrees)

        end_angle = start_angle + angle_deg  # Here's the change to determine the end angle based on the passed angle's sign
        circle = patches.Arc((r_circle_x, r_circle_y), 2*abs(radius), 2*abs(radius),
                     angle=0, theta1=min(start_angle, end_angle), theta2=max(start_angle, end_angle),  
                     color=color, linestyle="--")

        plt.gca().add_patch(circle)

        # Update robot's position and orientation
        self.degrees += angle_deg
        self.x += radius * (math.sin(math.radians(self.degrees)) - math.sin(math.radians(self.degrees - angle_deg)))
        self.y -= radius * (math.cos(math.radians(self.degrees)) - math.cos(math.radians(self.degrees - angle_deg)))

    def execute_maneuver(self, e):
        # print(f"Executing maneuver - Steering: {e.steering}, Gear: {e.gear}, Param: {e.param}")
        color = 'green' if e.gear == Gear.FORWARD else 'red'

        if e.steering == Steering.LEFT:
            radius = self.min_radius
            angle = rad2deg(e.param / self.min_radius)
            if e.gear == Gear.BACKWARD:
                angle = -angle
            self.draw_arc(radius, angle, color)
        elif e.steering == Steering.RIGHT:
            radius = -self.min_radius
            angle = rad2deg(e.param / self.min_radius)
            if e.gear == Gear.FORWARD:
                angle = -angle
            self.draw_arc(radius, angle, color)
        elif e.steering == Steering.STRAIGHT:
            dx = (1 if e.gear == Gear.FORWARD else -1) * e.param * math.cos(math.radians(self.degrees))
            dy = (1 if e.gear == Gear.FORWARD else -1) * e.param * math.sin(math.radians(self.degrees))
            plt.arrow(self.x, self.y, dx, dy, head_width=2, head_length=2, fc=color, ec=color)
            self.x += dx
            self.y += dy

    def follow_reeds_shepps(self, path):
        for subpath in path:
            for e in subpath:
                self.execute_maneuver(e)
            # print(f"Robot position: ({self.x}, {self.y}, {self.degrees})")
            # self.draw()

    def rotate_point(self, x, y, x_center, y_center, theta_degrees):
        """Rotate a point around a given center."""
        theta = math.radians(theta_degrees)
        x_translated = x - x_center
        y_translated = y - y_center
        x_rotated = x_translated * math.cos(theta) - y_translated * math.sin(theta)
        y_rotated = x_translated * math.sin(theta) + y_translated * math.cos(theta)
        x_rotated += x_center
        y_rotated += y_center
        return x_rotated, y_rotated
    
    def get_left_circle_center(self, x, y):
        """Get the center of the robot's left turning circle (0-degree orientation)."""
        return x, y + self.min_radius

    def get_right_circle_center(self, x, y):
        """Get the center of the robot's right turning circle (0-degree orientation)."""
        return x, y - self.min_radius

    def draw(self, view_turning_circles=False):
        self.draw_robot(self.x, self.y, self.degrees, self.color)

        if view_turning_circles:
            self.draw_turning_circles(self.x, 
                                      self.y, 
                                      self.min_radius, self.degrees)

    def draw_robot(self, x, y, degrees, color):
        # Variables to adjust the robot's actual representation based on orientation
        robot_width, robot_length = ROBOT_ACTUAL_WIDTH, ROBOT_ACTUAL_LENGTH
        
        # Compute the robot's footprint without rotation first
        footprint_x, footprint_y = x, y
        
        # Rotate the robot footprint around (x, y)
        footprint_x_rot, footprint_y_rot = self.rotate_point(footprint_x, footprint_y, x, y, degrees)
        
        footprint_color = 'red' if self.collision_detected(self.x, self.y, self.degrees) else 'lightgrey'

        footprint = patches.Rectangle((footprint_x_rot, footprint_y_rot), ROBOT_FOOTPRINT_WIDTH, ROBOT_FOOTPRINT_HEIGHT, 
                                    facecolor=footprint_color, alpha=0.5, edgecolor='black', linewidth=1, angle=degrees)
        plt.gca().add_patch(footprint)

        # Calculate actual robot starting point to keep it centered in the footprint
        robot_x = x + (ROBOT_FOOTPRINT_WIDTH - robot_width) / 2
        robot_y = y + (ROBOT_FOOTPRINT_HEIGHT - robot_length) / 2
        
        # Rotate robot rectangle based on the given degrees around (x, y)
        robot_x_rot, robot_y_rot = self.rotate_point(robot_x, robot_y, x, y, degrees)
        
        robot = patches.Rectangle((robot_x_rot, robot_y_rot), robot_width, robot_length, 
                                facecolor=color, edgecolor='black', linewidth=1, angle=degrees)
        plt.gca().add_patch(robot)

        # Center coordinates of the footprint for arrow placement (before rotation)
        cx = x + ROBOT_FOOTPRINT_WIDTH / 2
        cy = y + ROBOT_FOOTPRINT_HEIGHT / 2

        # Arrow's tip assuming robot is at 0-degree orientation (pointing right, before rotation)
        arrow_tip_x = cx + ROBOT_FOOTPRINT_WIDTH / 2
        arrow_tip_y = cy

        # Rotate the center of the footprint based on the given degrees around (x, y)
        r_cx, r_cy = self.rotate_point(cx, cy, x, y, degrees)
        
        # Rotate arrow's tip based on the given degrees around (x, y)
        r_arrow_tip_x, r_arrow_tip_y = self.rotate_point(arrow_tip_x, arrow_tip_y, x, y, degrees)

        # Calculate the delta values for the arrow shaft
        dx = r_arrow_tip_x - r_cx
        dy = r_arrow_tip_y - r_cy

        # Draw the arrow
        plt.arrow(r_cx, r_cy, dx, dy, head_width=5, head_length=5, fc='red', ec='red')

    def draw_turning_circles(self, x, y, min_radius, degrees):
        # Calculate turning circle centers assuming 0-degree orientation
        left_circle_x = x
        left_circle_y = y + self.min_radius

        right_circle_x = x
        right_circle_y = y - self.min_radius

        # Rotate turning circle centers based on the given degrees around (x, y)
        r_left_circle_x, r_left_circle_y = self.rotate_point(left_circle_x, left_circle_y, x, y, degrees)
        r_right_circle_x, r_right_circle_y = self.rotate_point(right_circle_x, right_circle_y, x, y, degrees)

        # Draw the turning circles with updated design
        left_circle = patches.Circle((r_left_circle_x, r_left_circle_y), min_radius, fill=False, edgecolor='orange', linestyle='--', linewidth=1)
        right_circle = patches.Circle((r_right_circle_x, r_right_circle_y), min_radius, fill=False, edgecolor='orange', linestyle='--', linewidth=1)
        
        plt.gca().add_patch(left_circle)
        plt.gca().add_patch(right_circle)

    def simulate_reeds_shepps_path(self, path, start_x, start_y, start_degrees):
        """
        Simulate the robot's movement along the given path to check for collisions
        without actually drawing it. Returns True if a collision is detected, 
        and False otherwise.
        """
        # print(f"Simulating Reeds-Shepp Path...")
        # print(f"Simulation started at ({start_x}, {start_y}, {start_degrees})")
        temp_x, temp_y, temp_degrees = start_x, start_y, start_degrees

        for e in path:
            # print(f"Simulating maneuver - Steering: {e.steering}, Gear: {e.gear}, Param: {e.param}")

            # Divide each segment into checkpoints to monitor for collisions
            check_points = [e.param / 4, e.param / 2, 3 * e.param / 4, e.param]

            # Initialize previous checkpoint for interval calculation
            prev_checkpoint = 0

            for checkpoint in check_points:
                interval = checkpoint - prev_checkpoint
                prev_checkpoint = checkpoint

                # Calculate robot's movement for the current element but don't draw it
                dx, dy, d_angle = 0, 0, 0

                if e.steering == Steering.LEFT:
                    radius = self.min_radius
                    d_angle = rad2deg(interval / self.min_radius)
                    if e.gear == Gear.BACKWARD:
                        d_angle = -d_angle

                elif e.steering == Steering.RIGHT:
                    radius = -self.min_radius
                    d_angle = rad2deg(interval / self.min_radius)
                    if e.gear == Gear.FORWARD:
                        d_angle = -d_angle

                elif e.steering == Steering.STRAIGHT:
                    dx = (1 if e.gear == Gear.FORWARD else -1) * interval * math.cos(math.radians(temp_degrees))
                    dy = (1 if e.gear == Gear.FORWARD else -1) * interval * math.sin(math.radians(temp_degrees))

                # Apply the changes
                temp_degrees += d_angle
                temp_degrees = temp_degrees % 360  # Ensure degree is in [0, 360)
                if e.steering in [Steering.LEFT, Steering.RIGHT]:
                    angle_before = temp_degrees - d_angle
                    dx = radius * (math.sin(math.radians(temp_degrees)) - math.sin(math.radians(angle_before)))
                    dy = -radius * (math.cos(math.radians(temp_degrees)) - math.cos(math.radians(angle_before)))
                temp_x += dx
                temp_y += dy

                # Check for collision
                if self.collision_detected(temp_x, temp_y, temp_degrees):
                    # print("Collision detected.")
                    return True, None, None, None

                # print(f"Checkpoint at Param {checkpoint}: Robot Position: ({temp_x}, {temp_y}, {temp_degrees})")

        return False, temp_x, temp_y, temp_degrees




    
    def calculate_footprint_corners(self, x, y, degrees):
        # Corners when the robot is facing right (0 degrees)
        bl = (x, y)
        br = (x + ROBOT_FOOTPRINT_WIDTH, y)
        tr = (x + ROBOT_FOOTPRINT_WIDTH, y + ROBOT_FOOTPRINT_HEIGHT)
        tl = (x, y + ROBOT_FOOTPRINT_HEIGHT)

        # print(f"Before Rotation: ({bl}, {br}, {tr}, {tl})")

        # Rotate the corners based on the given degrees around (x, y)
        bl_rot = self.rotate_point(bl[0], bl[1], x, y, degrees)
        br_rot = self.rotate_point(br[0], br[1], x, y, degrees)
        tr_rot = self.rotate_point(tr[0], tr[1], x, y, degrees)
        tl_rot = self.rotate_point(tl[0], tl[1], x, y, degrees)

        # print(f"After Rotation: ({bl_rot}, {br_rot}, {tr_rot}, {tl_rot})")
        
        return [bl_rot, br_rot, tr_rot, tl_rot]

    # Check if a point is within a pillar's collision zone
    def pillar_collision(self, x, y, pillar):
        # Define pillar collision zone boundary
        # 10 and 20 because true coord is bottom left corner of the pillar
        x_min = pillar.x - pillar.PADDING
        x_max = pillar.x + pillar.PADDING + 10
        y_min = pillar.y - pillar.PADDING
        y_max = pillar.y + pillar.PADDING + 10

        # print(f"Checking if ({x}, {y}) is within ({x_min}, {y_min}) and ({x_max}, {y_max})")
        
        # Check if the point lies within the boundary
        if x_min < x < x_max and y_min < y < y_max:
            return True
        return False

    def collision_detected(self, x, y, degrees):
        corners = self.calculate_footprint_corners(x, y, degrees)
        # print(f"Robot Footprint Corners: {corners}")

        # Create edge midpoints based on the corners
        edge_midpoints = [
            ((corners[0][0] + corners[1][0]) / 2, (corners[0][1] + corners[1][1]) / 2),  # top edge
            ((corners[1][0] + corners[2][0]) / 2, (corners[1][1] + corners[2][1]) / 2),  # right edge
            ((corners[2][0] + corners[3][0]) / 2, (corners[2][1] + corners[3][1]) / 2),  # bottom edge
            ((corners[3][0] + corners[0][0]) / 2, (corners[3][1] + corners[0][1]) / 2)   # left edge
        ]

        points_to_check = corners + edge_midpoints
        # print(f"Points to Check: {points_to_check}")

        PADDING = 10
            
        # Check each point against the arena boundary
        for px, py in points_to_check:
            if px < 0 - PADDING or px > ARENA_WIDTH + PADDING or py < 0 - PADDING or py > ARENA_HEIGHT + PADDING:
                # print(f"Robot Position: ({x}, {y}, {degrees})")
                # print(f"Boundary Collision at Point: ({px}, {py})")
                return True
            
        # Check for pillar collisions
        for pillar in self.pillars:
            for px, py in points_to_check:
                if self.pillar_collision(px, py, pillar):
                    # print(f"Robot Position: ({x}, {y}, {degrees})")
                    # print(f"Pillar Collision at Point: ({px}, {py}) with Pillar at ({pillar.x}, {pillar.y})")
                    return True
            
        return False
        
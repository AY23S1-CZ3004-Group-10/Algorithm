# **Robot Navigation System**

## Overview
This Robot Navigation System simulates and visualizes the movement of a robot in an arena with pillars as obstacles. The robot maneuvers based on Reeds-Shepp paths, which consider both forward and backward movements, and can be visualized using arcs and straight lines. The visualization is rendered using matplotlib.

## Key Features
Robot Class: Represents the robot's state and provides methods to simulate its movement in the arena.
Reeds-Shepp Paths: Provides a set of maneuvers (arcs and straight paths) that the robot can follow.
Visualization: Allows visual representation of the robot's movements, turning circles, and obstacles using matplotlib.
Collision Detection: Ensures that the robot avoids collisions with pillars, which are represented as obstacles in the arena.

## How To Use
1. Setup:
Install required libraries:
```bash
pip install matplotlib
```
Ensure all the necessary files are in the same directory.

2. Simulation:
- Instantiate a robot: `robot = Robot(x, y, degrees)`
- Visualize its movement using the provided Reeds-Shepp paths: `robot.follow_reeds_shepps(path)`


3. Visualization:
- Draw the robot with: `robot.draw()`
- Optionally, you can visualize turning circles with `robot.draw(view_turning_circles=True)`

4. Collision Detection:
- During simulation, the robot checks for potential collisions with pillars.
- The robot's footprint (bounding box) will be highlighted in red if there's a potential collision.

5. Pillars:
- The `pillars.py` module provides methods to add pillars (obstacles) in the arena. Use `get_pillars` to generate a list of pillars.

## Modules
1. robot.py:
- Contains the `Robot` class.
- Provides methods to execute Reeds-Shepp maneuvers, draw the robot, and check for collisions.

2. reeds_shepp.py:
- Defines the possible maneuvers and gears that the robot can follow.
- Contains the `Steering` and `Gear` enums.
 
3. pillars.py:
- Generates a list of pillar objects that can act as obstacles.
- Each pillar has an `x` and `y` coordinate in the arena.

4. utils.py:
- Contains utility functions like `rad2deg` to convert radians to degrees.

5. params.py:
- Defines parameters such as the dimensions of the arena, the robot's dimensions, and the minimum turning radius.
  
## Acknowledgements
The navigation approach uses Reeds-Shepp paths, which take into account both forward and backward movements of the robot.
Credit to [Reeds-Shepp-Curves](https://github.com/nathanlct/reeds-shepp-curves)

Feel free to modify or expand upon this README based on additional details or features of your project!
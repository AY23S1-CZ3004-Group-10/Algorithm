# **Robot Simulator**

## **Requirements**
- Python 3.x
- Pygame

## **Installation**
1. Install Python from **[python.org](https://www.python.org/)**.
2. Install Pygame by running **`pip install pygame`** in your terminal.

## **Running the Simulator**
1. Clone the repository or download the source code.
2. Navigate to the directory containing the source code.
3. Run **`python <filename>.py`** to start the simulator.

## **Controls**

The simulator provides a panel of buttons to control the robot's movement:
- **Fwd**: Move the robot one cell forward in its current direction.
- **Bwd**: Move the robot one cell backward in its current direction.
- **Fwd-L**: Move the robot forward and turn it left.
- **Fwd-R**: Move the robot forward and turn it right.
- **Bwd-L**: Move the robot backward and turn it left.
- **Bwd-R**: Move the robot backward and turn it right.

## **Features**
- **Grid-based Arena**: The arena is a grid where each cell can either be empty or contain a pillar.
- **Pillars**: Pillars are obstacles that the robot must avoid.
- **Collision Detection**: The simulator checks for collisions between the robot and pillars or the arena boundaries.

## **Assumptions**
- The robot is assumed to have a 3x3 footprint.
- Pillars also have a 3x3 footprint, with the coordinates representing the center of the pillar.

## **Future Work**
- Add more advanced navigation features.
- Implement a path-finding algorithm.
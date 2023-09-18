import matplotlib.pyplot as plt
import matplotlib.patches as patches
from params import WAYPOINT_DISTANCE

class Pillar:
    def __init__(self, x, y, card_dir, scanned=False):
        assert card_dir in ['N', 'S', 'E', 'W'], "card_dir must be one of 'N', 'S', 'E', 'W'"

        self.x = x
        self.y = y
        self.card_dir = card_dir  # could be an enum or string indicating direction
        self.scanned = scanned
    
    def draw(self, ax):
        # The actual pillar cell
        pillar_color = 'green' if self.scanned else 'red'
        pillar_rect = patches.Rectangle((self.x, self.y), 10, 10, facecolor=pillar_color)
        ax.add_patch(pillar_rect)

        # The surrounding cells for collision zone
        infl_color = (1, 0.5, 0, 0.5)  # translucent orange using RGBA format
        for i in [-10, 0, 10]:
            for j in [-10, 0, 10]:
                if i == 0 and j == 0:  # Skip the actual pillar cell
                    continue
                cell = patches.Rectangle((self.x + i, self.y + j), 10, 10, facecolor=infl_color)
                ax.add_patch(cell)

        # Card size
        card_size = 7
        thickness = 3
        if self.card_dir == 'N':
            ax.add_patch(patches.Rectangle((self.x + 5 - card_size/2, self.y + 10 - thickness), card_size, thickness, facecolor='black'))
        elif self.card_dir == 'S':
            ax.add_patch(patches.Rectangle((self.x + 5 - card_size/2, self.y), card_size, thickness, facecolor='black'))
        elif self.card_dir == 'E':
            ax.add_patch(patches.Rectangle((self.x + 10 - thickness, self.y + 5 - card_size/2), thickness, card_size, facecolor='black'))
        elif self.card_dir == 'W':
            ax.add_patch(patches.Rectangle((self.x, self.y + 5 - card_size/2), thickness, card_size, facecolor='black'))

    def getWaypoint(self):
        # Distance from the center of the pillar to the desired waypoint (pillar radius + robot footprint/2 + distance to snap)
        offset_distance = 15 + 15 + WAYPOINT_DISTANCE
        offset_center = 15  # Half the robot's dimension
        
        pillar_center_x = self.x + 5  # Center x of the pillar
        pillar_center_y = self.y + 5  # Center y of the pillar
        
        if self.card_dir == 'N':
            return (pillar_center_x - offset_center, pillar_center_y + offset_distance, 270)  # Robot is located north of the card and faces south.
        elif self.card_dir == 'S':
            return (pillar_center_x + offset_center, pillar_center_y - offset_distance, 90)  # Robot is located south of the card and faces north.
        elif self.card_dir == 'E':
            return (pillar_center_x + offset_distance, pillar_center_y + offset_center, 180)  # Robot is located to the east of the card and faces west.
        elif self.card_dir == 'W':
            return (pillar_center_x - offset_distance, pillar_center_y - offset_center, 0)    # Robot is located to the west of the card and faces east.
        
def get_pillars(pillar_data):
    pillars = [Pillar(x, y, card_dir) for x, y, card_dir in pillar_data]
    return pillars
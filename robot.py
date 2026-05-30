# robot.py
# Part a) - Software programming for industrial robotic systems

import time  # We use this to simulate robot movement time

class IndustrialRobot:
    """
    This class represents an industrial robot.
    It can move to positions, pick up items, and place them.
    """

    def __init__(self, name):
        self.name = name
        self.status = "idle"          # Robot starts doing nothing
        self.position = (0, 0, 0)     # x, y, z coordinates
        self.holding_item = None      # Robot holds nothing at start
        print(f"[ROBOT] {self.name} initialized and ready.")

    def move_to(self, x, y, z):
        """Move the robot arm to a specific position"""
        self.status = "moving"
        print(f"[ROBOT] Moving to position ({x}, {y}, {z})...")
        time.sleep(1)  # Simulates time taken to move
        self.position = (x, y, z)
        self.status = "idle"
        print(f"[ROBOT] Reached position ({x}, {y}, {z}).")
        return True

    def pick(self, item_name):
        """Pick up an item"""
        if self.holding_item:
            print(f"[ROBOT] Already holding {self.holding_item}. Cannot pick.")
            return False
        self.status = "picking"
        print(f"[ROBOT] Picking up {item_name}...")
        time.sleep(0.5)
        self.holding_item = item_name
        self.status = "idle"
        print(f"[ROBOT] Picked up {item_name}.")
        return True

    def place(self):
        """Place down the item being held"""
        if not self.holding_item:
            print("[ROBOT] Nothing to place.")
            return False
        self.status = "placing"
        print(f"[ROBOT] Placing {self.holding_item}...")
        time.sleep(0.5)
        placed_item = self.holding_item
        self.holding_item = None
        self.status = "idle"
        print(f"[ROBOT] Placed {placed_item} at {self.position}.")
        return True

    def get_status(self):
        """Return current robot status"""
        return {
            "name": self.name,
            "status": self.status,
            "position": self.position,
            "holding": self.holding_item
        }
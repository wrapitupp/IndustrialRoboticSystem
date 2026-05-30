# simulator.py
# PyBullet 3D Robot Simulation - connects to our existing robot.py

import pybullet as p
import pybullet_data
import time

class RobotSimulator:
    """
    Opens a 3D simulation window with a real Kuka robot arm.
    Connects to our existing robot commands (move, pick, place).
    """

    def __init__(self):
        # Start PyBullet with a visible 3D window
        self.client = p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())

        # Set up the environment
        p.setGravity(0, 0, -9.81)
        p.resetDebugVisualizerCamera(
            cameraDistance=1.5,
            cameraYaw=50,
            cameraPitch=-35,
            cameraTargetPosition=[0, 0, 0]
        )

        # Load a flat ground plane
        self.plane = p.loadURDF("plane.urdf")

        # Load the Kuka robot arm (comes built into PyBullet!)
        self.robot = p.loadURDF(
            "kuka_iiwa/model.urdf",
            basePosition=[0, 0, 0],
            useFixedBase=True  # Robot is bolted to the ground
        )

        self.num_joints = p.getNumJoints(self.robot)
        print(f"[SIMULATOR] Kuka arm loaded with {self.num_joints} joints.")
        print("[SIMULATOR] 3D window is open — you can rotate with your mouse!")

    def move_to(self, x, y, z):
        """
        Move the robot arm smoothly to a position.
        Maps our x,y,z coords to real robot joint angles.
        """
        print(f"[SIMULATOR] Moving arm to ({x}, {y}, {z})...")

        # Scale down input coords to robot's range
        target = [
            max(-1.0, min(1.0, x / 20.0)),
            max(-1.0, min(1.0, y / 20.0)),
            max( 0.0, min(1.5, z / 20.0 + 0.5))
        ]

        # Calculate joint angles using inverse kinematics
        joint_angles = p.calculateInverseKinematics(
            self.robot,
            endEffectorLinkIndex=6,
            targetPosition=target
        )

        # Apply angles to each joint smoothly
        for i in range(self.num_joints):
            p.setJointMotorControl2(
                bodyIndex=self.robot,
                jointIndex=i,
                controlMode=p.POSITION_CONTROL,
                targetPosition=joint_angles[i],
                force=500
            )

        # Simulate movement over time so it looks smooth
        for _ in range(300):
            p.stepSimulation()
            time.sleep(1.0 / 240.0)

        print(f"[SIMULATOR] Arm reached ({x}, {y}, {z})")

    def pick(self, item_name):
        """Simulate picking - arm closes down"""
        print(f"[SIMULATOR] Picking {item_name}...")

        # Move arm slightly down to simulate grabbing
        joint_angles = p.calculateInverseKinematics(
            self.robot,
            endEffectorLinkIndex=6,
            targetPosition=[0.3, 0.3, 0.1]
        )
        for i in range(self.num_joints):
            p.setJointMotorControl2(
                bodyIndex=self.robot,
                jointIndex=i,
                controlMode=p.POSITION_CONTROL,
                targetPosition=joint_angles[i],
                force=500
            )
        for _ in range(200):
            p.stepSimulation()
            time.sleep(1.0 / 240.0)

        print(f"[SIMULATOR] {item_name} picked!")

    def place(self):
        """Simulate placing - arm moves back up"""
        print("[SIMULATOR] Placing item...")

        # Return arm to neutral upright position
        neutral = [0.0] * self.num_joints
        for i in range(self.num_joints):
            p.setJointMotorControl2(
                bodyIndex=self.robot,
                jointIndex=i,
                controlMode=p.POSITION_CONTROL,
                targetPosition=neutral[i],
                force=500
            )
        for _ in range(200):
            p.stepSimulation()
            time.sleep(1.0 / 240.0)

        print("[SIMULATOR] Item placed, arm back to neutral.")

    def disconnect(self):
        """Close the simulation window"""
        p.disconnect()
        print("[SIMULATOR] Simulation closed.")
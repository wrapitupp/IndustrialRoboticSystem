# test_robot.py
# Part d) - Test software performance for robotic system

import time
import unittest
from robot import IndustrialRobot
from database import RobotDatabase

class TestRobotPerformance(unittest.TestCase):
    """
    These are automated tests that check if the robot
    and database are working correctly and fast enough.
    """

    def setUp(self):
        """This runs before every single test — sets up a fresh robot"""
        self.robot = IndustrialRobot("TestBot")
        self.db = RobotDatabase("test_events.db")

    def tearDown(self):
        """This runs after every test — cleans up"""
        self.db.close()

    # -------------------------
    # ROBOT TESTS
    # -------------------------

    def test_01_robot_initial_state(self):
        """Test that robot starts with correct default values"""
        status = self.robot.get_status()
        self.assertEqual(status["status"], "idle")
        self.assertEqual(status["position"], (0, 0, 0))
        self.assertIsNone(status["holding"])
        print("\n✅ PASS: Robot initializes correctly")

    def test_02_robot_move_performance(self):
        """Test that robot moves correctly and within time limit"""
        start = time.time()
        result = self.robot.move_to(10, 20, 30)
        duration = time.time() - start

        self.assertTrue(result)
        self.assertEqual(self.robot.position, (10, 20, 30))
        self.assertLess(duration, 3.0)  # Must complete within 3 seconds
        print(f"\n✅ PASS: Robot moved in {duration:.2f}s (limit: 3.0s)")

    def test_03_robot_pick_performance(self):
        """Test that robot picks an item correctly and fast enough"""
        start = time.time()
        result = self.robot.pick("Steel Bolt")
        duration = time.time() - start

        self.assertTrue(result)
        self.assertEqual(self.robot.holding_item, "Steel Bolt")
        self.assertLess(duration, 2.0)  # Must complete within 2 seconds
        print(f"\n✅ PASS: Robot picked item in {duration:.2f}s (limit: 2.0s)")

    def test_04_robot_cannot_pick_twice(self):
        """Test that robot refuses to pick when already holding something"""
        self.robot.pick("Item A")
        result = self.robot.pick("Item B")  # Should fail

        self.assertFalse(result)
        self.assertEqual(self.robot.holding_item, "Item A")  # Still holds first item
        print("\n✅ PASS: Robot correctly refuses double pick")

    def test_05_robot_place_performance(self):
        """Test that robot places item correctly and fast enough"""
        self.robot.pick("Circuit Board")
        start = time.time()
        result = self.robot.place()
        duration = time.time() - start

        self.assertTrue(result)
        self.assertIsNone(self.robot.holding_item)
        self.assertLess(duration, 2.0)  # Must complete within 2 seconds
        print(f"\n✅ PASS: Robot placed item in {duration:.2f}s (limit: 2.0s)")

    def test_06_robot_cannot_place_empty(self):
        """Test that robot refuses to place when holding nothing"""
        result = self.robot.place()
        self.assertFalse(result)
        print("\n✅ PASS: Robot correctly refuses empty place")

    def test_07_full_workflow_performance(self):
        """Test a complete move → pick → place cycle and total time"""
        start = time.time()

        self.robot.move_to(5, 5, 0)
        self.robot.pick("Engine Part")
        self.robot.move_to(15, 15, 0)
        self.robot.place()

        duration = time.time() - start
        self.assertLess(duration, 10.0)  # Full cycle under 10 seconds
        print(f"\n✅ PASS: Full cycle completed in {duration:.2f}s (limit: 10.0s)")

    # -------------------------
    # DATABASE TESTS
    # -------------------------

    def test_08_database_logs_event(self):
        """Test that database saves events correctly"""
        self.db.log_event("MOVE", "Moved to (1,1,1)", (1, 1, 1), "success")
        events = self.db.get_all_events()

        self.assertGreater(len(events), 0)
        self.assertEqual(events[0][2], "MOVE")   # event_type column
        self.assertEqual(events[0][5], "success") # status column
        print("\n✅ PASS: Database logs events correctly")

    def test_09_database_performance(self):
        """Test that database can log 100 events quickly"""
        start = time.time()

        for i in range(100):
            self.db.log_event("TEST", f"Event {i}", (0, 0, 0), "success")

        duration = time.time() - start
        self.assertLess(duration, 3.0)  # 100 logs under 3 seconds
        print(f"\n✅ PASS: Logged 100 events in {duration:.2f}s (limit: 3.0s)")


# --- Run the tests ---
if __name__ == "__main__":
    print("=" * 50)
    print("   ROBOT SYSTEM PERFORMANCE TEST REPORT")
    print("=" * 50)
    unittest.main(verbosity=2)
# File: navigation_manager_test.py

import sys
import unittest
from os.path import dirname, join, abspath

sys.path.insert(0, abspath(join(dirname(__file__), '..')))
from environments import navigation_manager


class TestNavigationManager(unittest.TestCase):
    def setUp(self):
        self.nav_manager = navigation_manager.NavigationManager()

    def test_init(self):
        self.assertIsNone(self.nav_manager.current_task)

    def test_set_task(self):
        self.nav_manager.set_task('Move to waypoint')
        self.assertEqual(self.nav_manager.current_task, 'Move to waypoint')

    def test_execute_task_without_task_set(self):
        result = self.nav_manager.execute_task()
        self.assertFalse(result)

    def test_execute_task_with_task_set(self):
        self.nav_manager.set_task('Move to waypoint')
        result = self.nav_manager.execute_task()
        self.assertTrue(result)

    def test_handle_stuck(self):
        result = self.nav_manager.handle_stuck()
        self.assertEqual(result, "Unstuck logic executed")


if __name__ == '__main__':
    unittest.main()

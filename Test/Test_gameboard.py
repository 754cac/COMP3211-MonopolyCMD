import unittest
from unittest.mock import patch, MagicMock
from gameboard import Gameboard, check_design
import json

class TestGameboard(unittest.TestCase):

    def setUp(self):
        self.gameboard = Gameboard()

    def test_load_default_gameboard(self):
        # Mock the JSON data to include 'enforce_square_design'
        mock_json_data = json.dumps({
            "enforce_square_design": True,
            "size": 4,
            "properties": [],
            "functions": []
        })
        
        with patch('builtins.open', unittest.mock.mock_open(read_data=mock_json_data)), \
             patch('vars.DEFAULT_GAMEBOARD_DESIGN_PATH', new_callable=MagicMock):
            self.gameboard.load_default_gameboard()
            self.assertEqual(self.gameboard.actual_layout['size'], 4)

    def test_check_design_valid(self):
        design = {
            "enforce_square_design": True,
            "size": 4,
            "properties": [
                {"location": 1, "name": "Property1", "price": 100, "rent": 10, "is_ownable": True}
            ],
            "functions": [
                {"location": 2, "name": "Go", "role": "function", "is_ownable": False},
                {"location": 3, "name": "Just Visiting / In Jail", "role": "function", "is_ownable": False},
                {"location": 4, "name": "Go To Jail", "role": "function", "is_ownable": False}
            ]
        }
        self.assertTrue(check_design(design))

    def test_check_design_invalid(self):
        design = {
            "enforce_square_design": True,
            "size": 4,
            "properties": [
                {"location": 1, "name": "Property1", "price": 100, "rent": 10, "is_ownable": True}
            ],
            "functions": [
                {"location": 2, "name": "Go", "role": "function", "is_ownable": False},
                {"location": 4, "name": "Go To Jail", "role": "function", "is_ownable": False}
            ]
        }
        self.assertFalse(check_design(design))

if __name__ == '__main__':
    unittest.main()
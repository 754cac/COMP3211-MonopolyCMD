import unittest
from unittest.mock import patch, MagicMock
from gameboard import Gameboard, check_design, available_functions
import json

class TestGameboard(unittest.TestCase):

    def setUp(self):
        self.gameboard = Gameboard()

    def test_load_default_gameboard_valid(self):
        # 測試加載有效的默認棋盤設計
        mock_json_data = json.dumps({
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
        })

        with patch('builtins.open', unittest.mock.mock_open(read_data=mock_json_data)), \
             patch('vars.DEFAULT_GAMEBOARD_DESIGN_PATH', new_callable=MagicMock):
            self.gameboard.load_default_gameboard()
            self.assertEqual(self.gameboard.actual_layout['size'], 4)
            self.assertEqual(len(self.gameboard.actual_layout['layout']), 4)
            self.assertEqual(self.gameboard.go_location, 2)
            self.assertEqual(self.gameboard.jail_location, 3)

    def test_load_default_gameboard_invalid(self):
        # 測試加載無效的默認棋盤設計
        mock_json_data = json.dumps({
            "enforce_square_design": True,
            "size": 4,
            "properties": [],
            "functions": []
        })

        with patch('builtins.open', unittest.mock.mock_open(read_data=mock_json_data)), \
             patch('vars.DEFAULT_GAMEBOARD_DESIGN_PATH', new_callable=MagicMock):
            with patch('builtins.print') as mock_print:
                self.gameboard.load_default_gameboard()
                mock_print.assert_any_call("Error: Go does not exist.")
                self.assertEqual(self.gameboard.actual_layout, {})

    def test_square_checker_property_valid(self):
        # 測試有效的 property 格子
        property_square = {
            "location": 1,
            "name": "Property1",
            "price": 100,
            "rent": 10,
            "role": "property",
            "is_ownable": True
        }
        self.assertTrue(Gameboard.square_checker(property_square, "property"))

    def test_square_checker_function_valid(self):
        # 測試有效的 function 格子
        function_square = {
            "location": 2,
            "name": "Go",
            "role": "function",
            "is_ownable": False
        }
        self.assertTrue(Gameboard.square_checker(function_square, "function"))

    def test_square_checker_invalid_type(self):
        # 測試無效的格子類型
        invalid_square = {
            "location": 1,
            "name": "Property1",
            "price": 100,
            "rent": 10,
            "role": "property",
            "is_ownable": True
        }
        with self.assertRaises(ValueError):
            Gameboard.square_checker(invalid_square, "invalid_type")

    def test_square_checker_missing_field(self):
        # 測試缺少必要字段的格子
        invalid_property_square = {
            "location": 1,
            "name": "Property1",
            "price": 100,
            "is_ownable": True  # 缺少 "rent" 和 "role"
        }
        with self.assertRaises(AssertionError):
            Gameboard.square_checker(invalid_property_square, "property")


    def test_check_design_error_board_size(self):
        design = {
            "enforce_square_design": True,
            "size": 5,  # 非 4 的倍數
            "properties": [],
            "functions": [{"location": 1, "name": "Go", "role": "function", "is_ownable": False}]
        }
        with patch('builtins.print') as mock_print:
            self.assertFalse(check_design(design))
            mock_print.assert_called_with("Error: Board Size must be equal to sum of properties and functions!")

    def test_check_design_error_missing_go(self):
        design = {
            "enforce_square_design": True,
            "size": 4,
            "properties": [
                {"location": 1, "name": "Property1", "price": 100, "rent": 10, "is_ownable": True},
                {"location": 1, "name": "Property2", "price": 150, "rent": 15, "is_ownable": True}  # 重複的 location
            ],
            "functions": [{"location": 4, "name": "Go", "role": "function", "is_ownable": False}]
        }
        with patch('builtins.print') as mock_print:
            self.assertFalse(check_design(design))
            mock_print.assert_called_with("Error: Duplicate locations detected.")

    def test_check_design_error_duplicate_locations(self):
        design = {
            "enforce_square_design": True,
            "size": 4,
            "properties": [
                {"location": 1, "name": "Property1", "price": 100, "rent": 10, "is_ownable": True},
                {"location": 1, "name": "Property2", "price": 150, "rent": 15, "is_ownable": True}  # 重複的 location
            ],
            "functions": [{"location": 4, "name": "Go", "role": "function", "is_ownable": False}]  # 添加 "Go"
        }
        with patch('builtins.print') as mock_print:
            self.assertFalse(check_design(design))
            mock_print.assert_called_with("Error: Duplicate locations detected.")

    def test_check_design_error_just_visiting_missing(self):
        # 測試缺少 "Just Visiting / In Jail" 格子
        design = {
            "enforce_square_design": True,
            "size": 4,
            "properties": [],
            "functions": [
                {"location": 4, "name": "Go To Jail", "role": "function", "is_ownable": False},
                {"location": 1, "name": "Go", "role": "function", "is_ownable": False}  # 添加 "Go"
            ]
        }
        with patch('builtins.print') as mock_print:
            self.assertFalse(check_design(design))
            mock_print.assert_called_with("Error: Just Visiting / In Jail needs to exist if Go To Jail exists")

if __name__ == '__main__':
    unittest.main()
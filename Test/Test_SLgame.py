import unittest
from unittest.mock import patch, mock_open, MagicMock
from game import Game
import json
import vars
from pathlib import Path

class TestGameSaveLoad(unittest.TestCase):

    def setUp(self):
        self.game = Game()
        self.game.game_state = {
            "game_id": "test_game_id",
            "game_over": False,
            "current_round": 1,
            "current_player_id": 'player1'
        }
        self.game.player_orders = {1: 'player1'}
        self.game.game_parameters = {
            "random_player_orders": False,
            "chance_multiplier": 1,
            "jailbreak_price": 50,
            "tax_amount_rate": 0.1,
            "go_money": 200,
            "maximum_rounds": 10,
            "minimum_player": 2,
            "maximum_player": 4
        }
        self.game.players = {
            'player1': MagicMock(id='player1', name='TestPlayer', location=0, money=100, owned_properties=[],
                                 is_jailed=False, jailed_rounds_count_down=0, is_retired=False, gameboard_size=10,
                                 game_id='test_game_id')
        }
        self.game.gameboard = MagicMock()
        self.game.gameboard.design_file_name = 'default_design.json'
        self.game.gameboard.game_id = 'test_game_id'

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    def test_save_game_state(self, mock_json_dump, mock_file):
        save_file_name = 'test_save.json'
        save_file_path = vars.BASE_SAVE_STATE_PATH / save_file_name
        self.game.save_game_state(save_file_name)
        mock_file.assert_called_once_with(str(save_file_path), 'w')
        mock_json_dump.assert_called_once()

    @patch('builtins.open', new_callable=mock_open, read_data='{"game_state": {}, "player_orders": {}, "game_parameters": {}, "players": {}, "gameboard": {}}')
    @patch('json.load')
    def test_load_game_state(self, mock_json_load, mock_file):
        mock_json_load.return_value = {
            "game_state": self.game.game_state,
            "player_orders": {1: 'player1'},
            "game_parameters": self.game.game_parameters,
            "players": {
                'player1': {
                    "name": "TestPlayer",
                    "id": "player1",
                    "location": 0,
                    "money": 100,
                    "owned_properties": [],
                    "is_jailed": False,
                    "jailed_rounds_count_down": 0,
                    "is_retired": False,
                    "gameboard_size": 10,
                    "game_id": "test_game_id"
                }
            },
            "gameboard": {
                "design_file_name": "default_design.json",
                "game_id": "test_game_id"
            }
        }

        load_file_name = 'test_save.json'
        load_file_path = vars.BASE_SAVE_STATE_PATH / load_file_name
        result = self.game.load_game_state(load_file_name)
        self.assertTrue(result)
        mock_file.assert_called_once_with(str(load_file_path), 'r')
        mock_json_load.assert_called_once()

if __name__ == '__main__':
    unittest.main()
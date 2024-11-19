import unittest
from unittest.mock import MagicMock, patch
from game import Game
from player import Player
from gameboard import Gameboard

class TestGame(unittest.TestCase):

    def setUp(self):
        self.game = Game()
        
        # Mock gameboard and player
        self.game.gameboard = MagicMock(spec=Gameboard)
        self.mock_player = MagicMock(spec=Player)
        self.mock_player.id = 'player1'
        self.mock_player.name = 'TestPlayer'
        self.mock_player.location = 0
        self.mock_player.owned_properties = []
        self.mock_player.is_retired = False
        self.mock_player.money = 100
        self.mock_player.is_jailed = False
        self.mock_player.jailed_rounds_count_down = 0
        
        self.game.players = {self.mock_player.id: self.mock_player}
        self.game.player_orders = {1: self.mock_player.id}

    def test_change_property_ownership(self):
        self.game.gameboard.actual_layout = {'layout': {0: {'is_ownable': True, 'ownership': None}}}
        self.game.change_property_ownership(self.mock_player)
        self.assertEqual(self.game.gameboard.actual_layout['layout'][0]['ownership'], 'player1')

    def test_retire_player(self):
        self.mock_player.retired = MagicMock()
        self.game.retire_player(self.mock_player)
        self.assertTrue(self.mock_player.retired.called)
        self.assertEqual(self.game.player_orders, {1: 'player1'})

    def test_show_player_status(self):
        self.mock_player.show_status = MagicMock()
        self.game.show_player_status(self.mock_player.id)
        self.mock_player.show_status.assert_called_once()

    def test_show_all_players_status(self):
        self.game.show_all_players_status()

    def test_show_game_status(self):
        self.game.gameboard.actual_layout = {'layout': {0: {'is_ownable': True, 'name': 'mock_property', 'price': 100, 'rent': 10, 'ownership': None}}} 
        self.game.show_game_status()

    @patch('game.vars')
    def test_new_game(self, mock_vars):
        mock_vars.secure_random_string.return_value = 'game123'
        mock_vars.handle_question_with_options.return_value = '0'
        mock_vars.DEFAULT_RANDOM_PLAYER_ORDERS = False
        mock_vars.DEFAULT_CHANCE_MULTIPLIER = 1
        mock_vars.DEFAULT_JAILBREAK_PRICE = 50
        mock_vars.DEFAULT_TAX_AMOUNT_RATE = 0.1
        mock_vars.DEFAULT_GO_MONEY = 200
        mock_vars.DEFAULT_MAXIMUM_ROUNDS = 10
        mock_vars.DEFAULT_MINIMUM_PLAYER = 2
        mock_vars.DEFAULT_MAXIMUM_PLAYER = 4
        
        self.assertTrue(self.game.new_game())

    def test_play_one_round(self):
        self.game.play_one_round()

    def test_save_and_load_game_state(self):
        with patch('game.json.dump') as mock_dump, patch('game.json.load', return_value={
            'game_state': {
                'game_id': 'mock_game_id',
                'game_over': False,
                'current_round': 1,
                'current_player_id': 'player1'
            },
            'player_orders': {1: 'player1'},
            'game_parameters': {
                'random_player_orders': False,
                'chance_multiplier': 0,
                'jailbreak_price': 0,
                'tax_amount_rate': 0,
                'go_money': 0,
                'maximum_rounds': 0,
                'minimum_player': 0,
                'maximum_player': 0
            },
            'players': {
                'player1': {
                    'name': 'TestPlayer',
                    'id': 'player1',
                    'location': 0,
                    'money': 100,
                    'owned_properties': [],
                    'is_jailed': False,
                    'jailed_rounds_count_down': 0,
                    'is_retired': False,
                    'gameboard_size': 'mock_size',
                    'game_id': 'mock_game_id'
                }
            },
            'gameboard': {
                'design_file_name': 'mock_design_file',
                'actual_layout': {'layout': {0: {'is_ownable': True, 'name': 'mock_property', 'price': 100, 'rent': 10, 'ownership': None}}}
            }
        }):
            self.mock_player.gameboard_size = 'mock_size'  
            self.mock_player.game_id = 'mock_game_id'
            self.game.gameboard.design_file_name = 'mock_design_file'
            self.game.gameboard.game_id = 'mock_game_id'
            self.game.save_game_state('test_save.json')
            
            mock_dump.assert_called_once()
            saved_data = mock_dump.call_args[0][0]
            print("Test saved data:", saved_data) 
            
            self.assertTrue(self.game.load_game_state('test_save.json'))

if __name__ == '__main__':
    unittest.main()
import unittest
from unittest.mock import MagicMock, patch
from game import Game
from player import Player
from gameboard import Gameboard
import logging

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
        self.game.player_orders = {1: '1', 2: '2'}
        self.game.players = {
            "1": Player("Player1", 10, "game_1"),
            "2": Player("Player2", 10, "game_1")
        }
        self.game.players["1"].owned_properties = [0, 1]
        self.game.gameboard.actual_layout = {
            'layout': {
                0: {'ownership': '1', 'owner_name': 'Player1', 'is_ownable': True},
                1: {'ownership': '1', 'owner_name': 'Player1', 'is_ownable': True},
                2: {'ownership': None, 'owner_name': '', 'is_ownable': True},
                3: {'ownership': None, 'owner_name': '', 'is_ownable': False}
            }
        }

    def test_change_property_ownership(self):
        self.game.gameboard.actual_layout = {'layout': {0: {'is_ownable': True, 'ownership': None}}}
        self.game.change_property_ownership(self.mock_player)
        self.assertEqual(self.game.gameboard.actual_layout['layout'][0]['ownership'], 'player1')

    def test_retire_player(self):
        self.mock_player.retired = MagicMock()
        self.game.retire_player(self.mock_player)
        self.assertTrue(self.mock_player.retired.called)
        self.assertEqual(self.game.player_orders, {1: '1', 2: '2'})

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

        inputs = iter(['2', 'a', 'b'])

        with patch('builtins.input', lambda _: next(inputs)):
            self.assertTrue(self.game.new_game())
    

    def test_play_one_round(self):
        self.game.play_one_round()

    def test_change_property_ownership_retire(self):
        # Act
        self.game.change_property_ownership(self.game.players["1"], active_retire_player=True)
        
        # Assert
        for prop in self.game.players["1"].owned_properties:
            self.assertIsNone(self.game.gameboard.actual_layout['layout'][prop]['ownership'])
            self.assertEqual(self.game.gameboard.actual_layout['layout'][prop]['owner_name'], '')

    def test_change_property_ownership_buy(self):
        player = self.game.players["2"]
        player.location = 2
        self.game.change_property_ownership(player)
        
        self.assertEqual(self.game.gameboard.actual_layout['layout'][player.location]['ownership'], player.id)
        self.assertEqual(self.game.gameboard.actual_layout['layout'][player.location]['owner_name'], player.name)

    def test_change_property_ownership_not_ownable(self):
        player = self.game.players["2"]
        player.location = 3
        with self.assertLogs(level='INFO') as log:
            self.game.change_property_ownership(player)
            self.assertIn('Not ownable.', log.output)

    def test_retire_player(self):
        self.game.retire_player(self.game.players["1"])
        self.assertTrue(self.game.players["1"].is_retired)

    def test_show_player_status(self):
        with self.assertLogs(level='INFO') as log:
            self.game.show_player_status("1")
            self.assertTrue("Player Player1 (ID: 1)", log.output)

    def test_play_one_round_player_retirement(self):
        player = self.game.players["1"]
        player.money = 0
        self.game.play_one_round()
        self.assertFalse(player.is_retired)

if __name__ == '__main__':
    unittest.main()
import unittest
from unittest.mock import patch, MagicMock
from player import Player
import vars

class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.player = Player("TestPlayer", 10, "game_1")

    def test_initialization(self):
        self.assertEqual(self.player.name, "TestPlayer")
        self.assertEqual(self.player.gameboard_size, 10)
        self.assertEqual(self.player.game_id, "game_1")
        self.assertEqual(self.player.location, vars.PLAYER_DEFAULT_PROPERTIES['location'])
        self.assertEqual(self.player.money, vars.PLAYER_DEFAULT_PROPERTIES['money'])
        self.assertEqual(self.player.owned_properties, vars.PLAYER_DEFAULT_PROPERTIES['owned_properties'])
        self.assertFalse(self.player.is_jailed)
        self.assertFalse(self.player.is_retired)

    @patch('player.randint', return_value=3)
    def test_roll_dice(self, mock_randint):
        dice = self.player.roll_dice()
        self.assertEqual(dice, [3, 3])

    def test_move(self):
        self.player.move(5)
        self.assertEqual(self.player.location, vars.PLAYER_DEFAULT_PROPERTIES['location'] + 5)

    def test_buy_property(self):
        self.player.buy_property(2, 100)
        self.assertIn(2, self.player.owned_properties)
        self.assertEqual(self.player.money, vars.PLAYER_DEFAULT_PROPERTIES['money'] - 100)

    def test_adjust_location(self):
        self.player.location = 12
        self.player.adjust_location()
        self.assertEqual(self.player.location, 2)

    def test_jailed(self):
        self.player.jailed(5)
        self.assertTrue(self.player.is_jailed)
        self.assertEqual(self.player.location, 5)

    @patch('player.vars.handle_question_with_options', return_value='y')
    @patch('player.Player.roll_dice', return_value=[2, 2])
    def test_jailbreak(self, mock_roll_dice, mock_handle_question_with_options):
        self.player.is_jailed = True
        self.player.jailed_rounds_count_down = 1
        self.player.money = 200
        dice = self.player.jailbreak(50)
        self.assertFalse(self.player.is_jailed)
        self.assertEqual(self.player.money, 150)
        self.assertEqual(dice, [2, 2])

    def test_retired(self):
        self.player.retired()
        self.assertTrue(self.player.is_retired)
        self.assertEqual(self.player.money, 0)
        self.assertEqual(self.player.owned_properties, [])

    @patch('builtins.print')
    def test_show_status(self, mock_print):
        self.player.show_status()
        mock_print.assert_called()

if __name__ == '__main__':
    unittest.main()
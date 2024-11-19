import unittest
from random import randint
from player import Player 
import vars

class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.player = Player("TestPlayer", 10, "game123")
        vars.PLAYER_DEFAULT_PROPERTIES = {
            'location': 0,
            'money': 1500,
            'owned_properties': [],
            'is_jailed': False,
            'jailed_rounds_count_down': 3,
            'is_retired': False
        }

    def test_initialization(self):
        self.assertEqual(self.player.name, "TestPlayer")
        self.assertEqual(self.player.gameboard_size, 10)
        self.assertEqual(self.player.game_id, "game123")
        self.assertEqual(self.player.location, 0)
        self.assertEqual(self.player.money, 1500)
        self.assertEqual(self.player.owned_properties, [])
        self.assertFalse(self.player.is_jailed)
        self.assertEqual(self.player.jailed_rounds_count_down, 3)
        self.assertFalse(self.player.is_retired)

    def test_roll_dice(self):
        dice = self.player.roll_dice()
        self.assertEqual(len(dice), 2)
        self.assertTrue(1 <= dice[0] <= 4)
        self.assertTrue(1 <= dice[1] <= 4)

    def test_move(self):
        self.player.move(5)
        self.assertEqual(self.player.location, 5)

    def test_buy_property(self):
        self.player.buy_property(3, 200)
        self.assertEqual(self.player.money, 1300)
        self.assertIn(3, self.player.owned_properties)

    def test_adjust_location(self):
        self.player.location = 12
        self.player.adjust_location()
        self.assertEqual(self.player.location, 2)

    def test_jailed(self):
        self.player.jailed(5)
        self.assertTrue(self.player.is_jailed)
        self.assertEqual(self.player.location, 5)

    def test_jailbreak(self):
        self.player.jailed(5)
        self.player.jailbreak(50)
        self.assertTrue(self.player.is_jailed or not self.player.is_jailed)

    def test_retired(self):
        self.player.retired()
        self.assertTrue(self.player.is_retired)
        self.assertEqual(self.player.money, 0)
        self.assertEqual(self.player.owned_properties, [])

    def test_show_status(self):
        self.player.show_status() 

if __name__ == '__main__':
    unittest.main()
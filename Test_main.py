import unittest
from unittest import mock
from game import Game
import vars

class TestGame(unittest.TestCase):

    def setUp(self):
        self.game = Game()

    def test_new_game(self):
        self.game.new_game = mock.Mock(return_value=True)
        game_initialized = self.game.new_game()
        self.assertTrue(game_initialized)

    def test_load_game_state(self):
        self.game.load_game_state = mock.Mock(return_value=True)
        save_file_name = "test_save_file"
        game_initialized = self.game.load_game_state(save_file_name)
        self.assertTrue(game_initialized)

    def test_play(self):
        self.game.play = mock.Mock()
        self.game.play()
        self.game.play.assert_called_once()

if __name__ == '__main__':
    unittest.main()


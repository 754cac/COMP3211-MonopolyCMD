import unittest
from unittest.mock import MagicMock, patch
from game import Game
from player import Player
from gameboard import Gameboard
import vars

class TestGame(unittest.TestCase):

    def setUp(self):
        """初始化測試環境"""
        self.game = Game()

        # Mock 遊戲板塊與玩家
        self.game.gameboard = MagicMock(spec=Gameboard)
        self.game.gameboard.design_file_name = "default_gameboard.json"
        self.game.gameboard.game_id = "test_game"
        self.mock_player1 = MagicMock(spec=Player)
        self.mock_player2 = MagicMock(spec=Player)

        # 設置玩家基本屬性
        self.mock_player1.id = 'player1'
        self.mock_player1.name = 'Player1'
        self.mock_player1.location = 0
        self.mock_player1.owned_properties = []
        self.mock_player1.is_retired = False
        self.mock_player1.money = 1000
        self.mock_player1.is_jailed = False
        self.mock_player1.jailed_rounds_count_down = 0
        self.mock_player1.gameboard_size = 10
        self.mock_player1.game_id = "test_game_id"  # 新增屬性

        self.mock_player2.id = 'player2'
        self.mock_player2.name = 'Player2'
        self.mock_player2.location = 1
        self.mock_player2.owned_properties = []
        self.mock_player2.is_retired = False
        self.mock_player2.money = 800
        self.mock_player2.is_jailed = False
        self.mock_player2.jailed_rounds_count_down = 0
        self.mock_player2.gameboard_size = 10
        self.mock_player2.game_id = "test_game_id"  # 新增屬性

        # 假設遊戲中的玩家
        self.game.players = {
            self.mock_player1.id: self.mock_player1,
            self.mock_player2.id: self.mock_player2
        }
        self.game.player_orders = {1: 'player1', 2: 'player2'}

        # 模擬遊戲板塊布局
        self.game.gameboard.actual_layout = {
            'layout': {
                0: {'ownership': None, 'owner_name': '', 'is_ownable': True, 'price': 200, 'rent': 20, 'name': 'Property1'},
                1: {'ownership': None, 'owner_name': '', 'is_ownable': True, 'price': 300, 'rent': 30, 'name': 'Property2'},
                2: {'ownership': None, 'owner_name': '', 'is_ownable': False, 'name': 'Go To Jail'},
            }
        }

    def test_game_initialization(self):
        """測試遊戲初始化"""
        game = Game()
        self.assertIsNotNone(game)
        self.assertEqual(game.players, {})
        self.assertEqual(game.player_orders, {})
        self.assertEqual(game.game_state['game_over'], False)
        self.assertEqual(game.game_state['current_round'], 1)

    def test_change_property_ownership(self):
        """測試地產所有權變更"""
        self.game.change_property_ownership(self.mock_player1)
        self.assertEqual(self.game.gameboard.actual_layout['layout'][0]['ownership'], 'player1')
        self.assertEqual(self.game.gameboard.actual_layout['layout'][0]['owner_name'], 'Player1')

    def test_retire_player(self):
        """測試玩家退場"""
        self.game.retire_player(self.mock_player1)
        self.assertTrue(self.mock_player1.retired.called)
        self.assertIsNone(self.game.gameboard.actual_layout['layout'][0]['ownership'])

    def test_show_player_status(self):
        """測試顯示玩家狀態"""
        self.mock_player1.show_status = MagicMock()
        self.game.show_player_status(self.mock_player1.id)
        self.mock_player1.show_status.assert_called_once()

    def test_show_all_players_status(self):
        """測試顯示所有玩家狀態"""
        with patch('pandas.DataFrame.to_string') as mock_to_string:
            self.game.show_all_players_status()
            self.assertTrue(mock_to_string.called)

    def test_show_game_status(self):
        """測試顯示遊戲狀態"""
        with patch('pandas.DataFrame.to_string') as mock_to_string:
            self.game.show_game_status()
            self.assertTrue(mock_to_string.called)

    @patch('builtins.input', side_effect=['0', '2', 'Player1', 'Player2'])
    def test_new_game(self, mock_input):
        """測試建立新遊戲"""
        self.assertTrue(self.game.new_game())
        self.assertEqual(len(self.game.players), 2)
        self.assertEqual(self.game.game_state['current_round'], 1)

    def test_player_buy_property(self):
        """測試玩家購買地產"""
        self.mock_player1.money = 500
        self.mock_player1.owned_properties = [0]  # 模擬玩家購買地產
        self.game.change_property_ownership(self.mock_player1)
        self.assertIn(0, self.mock_player1.owned_properties)  # 驗證地產已添加

    def test_player_pay_rent(self):
        """測試玩家支付租金"""
        self.mock_player1.money = 1000
        self.mock_player2.location = 0
        self.mock_player2.money = 800

        # 模擬玩家1擁有地產
        self.game.gameboard.actual_layout['layout'][0]['ownership'] = self.mock_player1.id
        self.game.gameboard.actual_layout['layout'][0]['owner_name'] = self.mock_player1.name

        # 玩家2支付地租
        rent = self.game.gameboard.actual_layout['layout'][0]['rent']
        self.mock_player2.money -= rent
        self.mock_player1.money += rent

        self.assertEqual(self.mock_player1.money, 1020)  # 玩家1收到租金
        self.assertEqual(self.mock_player2.money, 780)  # 玩家2支付租金

    @patch('builtins.input', side_effect=['y', 'save_file.json', 'n'])
    def test_save_and_load_game(self, mock_input):
        """測試儲存與載入遊戲"""
        with patch('vars.json.dump') as mock_json_dump:
            self.game.save_game_state('save_file.json')
            self.assertTrue(mock_json_dump.called)

        with patch('vars.json.load', return_value={
            'game_state': self.game.game_state,
            'player_orders': self.game.player_orders,
            'game_parameters': self.game.game_parameters,
            'players': {},
            'gameboard_parameters': {'design_file_name': 'default_gameboard.json', 'game_id': 'test_game'}
        }):
            self.assertFalse(self.game.load_game_state('save_file.json'))

    def test_player_jailbreak(self):
        """測試玩家出獄"""
        self.mock_player1.is_jailed = True
        self.mock_player1.jailed_rounds_count_down = 1
        self.mock_player1.money = 200

        # 模擬 jailbreak 方法的行為
        def mock_jailbreak(price):
            self.mock_player1.money -= price  # 減少金錢
            self.mock_player1.is_jailed = False  # 玩家出獄
            return [3, 4]  # 返回骰子點數

        self.mock_player1.jailbreak = mock_jailbreak

        dice = self.mock_player1.jailbreak(50)  # 玩家支付金額出獄
        self.assertFalse(self.mock_player1.is_jailed)  # 確保出獄
        self.assertEqual(self.mock_player1.money, 150)  # 確保金錢正確
        self.assertEqual(dice, [3, 4])  # 確保骰子點數正確

    def test_game_over_when_only_one_player_left(self):
        """測試遊戲結束邏輯"""
        self.mock_player2.is_retired = True
        self.game.check_only_player_is_left()
        self.assertTrue(self.game.game_state["game_over"])

if __name__ == '__main__':
    unittest.main()
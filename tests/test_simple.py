import unittest
from src.core.game import Game
from unittest.mock import patch

class TestSimple(unittest.TestCase):
    @patch('builtins.input', side_effect=['Cardeal Test', '0', '0', '50', '50', '50', '50', '0'] + ['0']*20)
    def test_basic_game_flow(self, mock_input):
        game = Game()
        game.start_game()
        self.assertIsNotNone(game.player)
        self.assertEqual(game.player.name, 'Cardeal Test')
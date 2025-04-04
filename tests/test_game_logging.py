import unittest
from datetime import datetime
from src.utils.game_logging import GameLogger

class TestGameLogging(unittest.TestCase):
    def setUp(self):
        self.logger = GameLogger()

    def test_log_action(self):
        """Testa o registro de ações"""
        self.logger.log_action("persuadir", "Cardinal Test", True, 15.5)
        
        # Verifica se a ação foi registrada no histórico
        latest_action = self.logger.history[-1]
        self.assertEqual(latest_action['type'], "persuadir")
        self.assertEqual(latest_action['target'], "Cardinal Test")
        self.assertEqual(latest_action['success'], True)
        self.assertEqual(latest_action['impact'], "+15.5%")
        
        # Verifica se as estatísticas foram atualizadas
        self.assertEqual(self.logger.action_stats['persuadir']['total'], 1)
        self.assertEqual(self.logger.action_stats['persuadir']['success'], 1)

    def test_log_support_change(self):
        """Testa o registro de mudanças no suporte"""
        self.logger.log_support_change("Zelanti", "Cardinal Test", 30.0, 45.0)
        
        latest_change = self.logger.support_history[-1]
        self.assertEqual(latest_change['faction'], "Zelanti")
        self.assertEqual(latest_change['candidate'], "Cardinal Test")
        self.assertEqual(latest_change['old_support'], 30.0)
        self.assertEqual(latest_change['new_support'], 45.0)
        self.assertEqual(latest_change['change'], 15.0)

    def test_log_stats(self):
        """Testa o registro de estatísticas gerais"""
        self.logger.log_stat("votos_round", 25)
        self.logger.log_stat("votos_round", 30)
        
        self.assertIn("votos_round", self.logger.stats)
        self.assertEqual(len(self.logger.stats["votos_round"]), 2)
        self.assertEqual(self.logger.stats["votos_round"][-1], 30)

    def test_action_success_rate(self):
        """Testa o cálculo da taxa de sucesso das ações"""
        # Registra algumas ações com sucessos e falhas
        self.logger.log_action("persuadir", "Cardinal1", True, 10)
        self.logger.log_action("persuadir", "Cardinal2", False, 0)
        self.logger.log_action("persuadir", "Cardinal3", True, 15)
        
        stats = self.logger.action_stats["persuadir"]
        self.assertEqual(stats["total"], 3)
        self.assertEqual(stats["success"], 2)
        # Taxa de sucesso deve ser aproximadamente 66.7%
        success_rate = (stats["success"] / stats["total"]) * 100
        self.assertAlmostEqual(success_rate, 66.67, places=2)

    def test_timestamp_format(self):
        """Testa o formato do timestamp nos registros"""
        self.logger.log_action("persuadir", "Cardinal Test", True, 10)
        timestamp = self.logger.history[-1]['timestamp']
        
        # Verifica se o timestamp está no formato correto
        try:
            datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            self.fail("Timestamp não está no formato correto")
import unittest
from src.core.game_mechanics import GameMechanics
from src.core.models import Cardinal, Faction
from src.utils.game_utils import normalize_support

class TestGameMechanics(unittest.TestCase):
    def setUp(self):
        self.cardinal_origem = Cardinal("Test1", "Moderado", "Jovem", "Europa", 70, 70, 70, 70)
        self.cardinal_alvo = Cardinal("Test2", "Conservador", "Veterano", "Asia", 60, 60, 60, 60)
        
    def test_apply_action_impact(self):
        result = GameMechanics.apply_action_impact(self.cardinal_origem, self.cardinal_alvo, "persuadir", 15)
        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 5)  # Impacto mínimo
        self.assertLessEqual(result, 25)    # Impacto máximo atualizado para 25

    def test_support_normalization(self):
        """Testa se a normalização de suporte mantém a soma em 100%"""
        support = {"A": 50, "B": 150, "C": 0}
        normalize_support(support)
        self.assertAlmostEqual(sum(support.values()), 100.0, places=2)
        self.assertTrue(all(v >= 2.0 for v in support.values()))

    def test_action_impact_limits(self):
        """Testa se os impactos das ações respeitam os limites"""
        result = GameMechanics.apply_action_impact(self.cardinal_origem, self.cardinal_alvo, "persuadir", 15)
        self.assertGreaterEqual(result, 5)
        self.assertLessEqual(result, 25)

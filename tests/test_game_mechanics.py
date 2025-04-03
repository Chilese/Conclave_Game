import unittest
from game_mechanics import apply_action_impact, update_support
from Cardinal import Cardinal
from Faction import Faction

class TestGameMechanics(unittest.TestCase):
    def setUp(self):
        self.cardinal_origem = Cardinal("Test1", "Moderado", "Jovem", "Europa", 70, 70, 70, 70)
        self.cardinal_alvo = Cardinal("Test2", "Conservador", "Veterano", "Asia", 60, 60, 60, 60)
        
    def test_apply_action_impact(self):
        result = apply_action_impact(self.cardinal_origem, self.cardinal_alvo, "persuadir", 15)
        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 5)  # Impacto mínimo
        self.assertLessEqual(result, 50)    # Impacto máximo

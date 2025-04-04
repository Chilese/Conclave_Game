import unittest
from src.core.models import Cardinal, Candidate, Faction

class TestModels(unittest.TestCase):
    def setUp(self):
        self.cardinal = Cardinal("Test Cardinal", "Moderado", "Jovem", "Europa", 70, 70, 70, 70)
        self.candidate = Candidate("Test Candidate", "Conservador", "Veterano", "Asia", 80, 80, 80, 80)
        self.faction = Faction("Test Faction", "Progressista", 50)

    def test_cardinal_validation(self):
        """Testa a validação de atributos do Cardinal"""
        with self.assertRaises(ValueError):
            Cardinal("Test", "Moderado", "Jovem", "Europa", -1, 70, 70, 70)
        with self.assertRaises(ValueError):
            Cardinal("Test", "Moderado", "Jovem", "Europa", 101, 70, 70, 70)

    def test_cardinal_equality(self):
        """Testa a comparação de igualdade entre Cardeais"""
        cardinal1 = Cardinal("Test", "Moderado", "Jovem", "Europa", 70, 70, 70, 70)
        cardinal2 = Cardinal("Test", "Moderado", "Jovem", "Asia", 60, 60, 60, 60)
        cardinal3 = Cardinal("Different", "Moderado", "Jovem", "Europa", 70, 70, 70, 70)
        
        self.assertEqual(cardinal1, cardinal2)  # Mesmo nome e ideologia
        self.assertNotEqual(cardinal1, cardinal3)  # Nome diferente

    def test_candidate_inheritance(self):
        """Testa se Candidate herda corretamente de Cardinal"""
        self.assertIsInstance(self.candidate, Cardinal)
        self.assertEqual(self.candidate.vote_count, 0)

    def test_faction_support_update(self):
        """Testa a atualização de suporte na Facção"""
        self.faction.update_candidate_support(self.candidate, 75)
        self.assertEqual(self.faction.candidate_support[self.candidate], 75)
        
        # Testa limites
        self.faction.update_candidate_support(self.candidate, 150)
        self.assertEqual(self.faction.candidate_support[self.candidate], 100)
        
        self.faction.update_candidate_support(self.candidate, -10)
        self.assertEqual(self.faction.candidate_support[self.candidate], 0)

    def test_faction_relationship_adjustment(self):
        """Testa o ajuste de relacionamento com o jogador"""
        # Primeiro ajuste positivo
        self.faction.adjust_relationship_with_player(50)
        self.assertEqual(self.faction.relationship_with_player, 50)
        
        # Segundo ajuste para atingir limite superior
        self.faction.adjust_relationship_with_player(60)
        self.assertEqual(self.faction.relationship_with_player, 100)
        
        # Ajuste negativo grande
        self.faction.adjust_relationship_with_player(-200)
        self.assertEqual(self.faction.relationship_with_player, -100)
        
        # Tentativa de reduzir ainda mais
        self.faction.adjust_relationship_with_player(-50)
        self.assertEqual(self.faction.relationship_with_player, -100)  # Deve manter o limite inferior
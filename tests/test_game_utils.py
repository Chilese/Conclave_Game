import unittest
from src.utils.game_utils import (
    distribute_members_among_factions,
    calculate_votes,
    check_majority,
    adjust_votes_to_total
)
from src.core.models import Cardinal, Faction

class TestGameUtils(unittest.TestCase):
    def setUp(self):
        self.candidate1 = Cardinal("Card1", "Moderado", "Jovem", "Europa", 70, 70, 70, 70)
        self.candidate2 = Cardinal("Card2", "Conservador", "Veterano", "Asia", 80, 80, 80, 80)
        self.factions = [
            Faction("Faction1", "Moderado", 100),
            Faction("Faction2", "Conservador", 50),
            Faction("Faction3", "Progressista", 55)
        ]
        
        # Configura suporte inicial para os testes
        self.factions[0].candidate_support = {self.candidate1: 60, self.candidate2: 40}
        self.factions[1].candidate_support = {self.candidate1: 30, self.candidate2: 70}
        self.factions[2].candidate_support = {self.candidate1: 45, self.candidate2: 55}

    def test_distribute_members(self):
        """Testa a distribuição de membros entre facções"""
        # Teste com distribuição exata
        distribution = distribute_members_among_factions(90, 3)
        self.assertEqual(sum(distribution), 90)
        self.assertEqual(len(distribution), 3)
        
        # Teste com resto
        distribution = distribute_members_among_factions(100, 3)
        self.assertEqual(sum(distribution), 100)
        self.assertEqual(len(distribution), 3)
        # O resto deve ser distribuído para as primeiras facções
        self.assertTrue(max(distribution) - min(distribution) <= 1)

    def test_calculate_votes(self):
        """Testa o cálculo de votos com peso por rodada"""
        # Configura suporte inicial claro
        self.factions[0].candidate_support = {self.candidate1: 80, self.candidate2: 20}
        self.factions[1].candidate_support = {self.candidate1: 20, self.candidate2: 80}
        self.factions[2].candidate_support = {self.candidate1: 50, self.candidate2: 50}
        
        # Calcula votos para duas rodadas
        votes_round_1 = calculate_votes(self.factions, 1)
        votes_round_2 = calculate_votes(self.factions, 2)
        
        total_voters = sum(f.num_members for f in self.factions)
        
        # Testes básicos
        self.assertEqual(sum(votes_round_1.values()), total_voters)
        self.assertEqual(sum(votes_round_2.values()), total_voters)
        
        # Verifica se o candidato com mais suporte tem mais votos na rodada 1
        self.assertGreater(votes_round_1[self.candidate1], votes_round_1[self.candidate2])
        
        # Verifica se o peso da rodada está afetando os votos
        ratio_round_1 = votes_round_1[self.candidate1] / votes_round_1[self.candidate2]
        ratio_round_2 = votes_round_2[self.candidate1] / votes_round_2[self.candidate2]
        
        # As proporções devem ser diferentes entre as rodadas
        self.assertNotAlmostEqual(ratio_round_1, ratio_round_2, places=2)

    def test_check_majority(self):
        """Testa a verificação de maioria"""
        total_voters = 300
        candidate_votes = {
            self.candidate1: 180,  # Não atinge 2/3
            self.candidate2: 120
        }
        
        winner, required, leader = check_majority(candidate_votes, total_voters)
        self.assertIsNone(winner)  # Não deve ter vencedor
        self.assertEqual(required, 201)  # 2/3 de 300 + 1
        self.assertEqual(leader, self.candidate1)  # Líder atual
        
        # Testa com maioria atingida
        candidate_votes[self.candidate1] = 210
        winner, required, leader = check_majority(candidate_votes, total_voters)
        self.assertEqual(winner, self.candidate1)

    def test_adjust_votes_total(self):
        """Testa o ajuste do total de votos"""
        total_electors = 200
        candidate_votes = {
            self.candidate1: 90,
            self.candidate2: 85
        }
        
        adjusted = adjust_votes_to_total(candidate_votes, total_electors)
        
        # Verifica se o total foi ajustado corretamente
        self.assertEqual(sum(adjusted.values()), total_electors)
        
        # Verifica se as proporções foram mantidas aproximadamente
        original_ratio = 90 / 85
        new_ratio = adjusted[self.candidate1] / adjusted[self.candidate2]
        self.assertAlmostEqual(original_ratio, new_ratio, places=1)
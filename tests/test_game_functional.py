import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
import sys
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

from src.core.game import Game
from src.core.models import Cardinal, Candidate

class SmartInputMock:
    def __init__(self, initial_inputs):
        self.initial_inputs = initial_inputs
        self.input_counter = 0
    
    def mock_input(self, prompt):
        """Simula entrada do usuário de forma contextual baseado no prompt"""
        logger.debug(f"Prompt recebido: {prompt}")
        
        if self.input_counter < len(self.initial_inputs):
            value = self.initial_inputs[self.input_counter]
            logger.debug(f"Usando entrada pré-definida [{self.input_counter}]: {value}")
            self.input_counter += 1
            return value
            
        # Respostas contextuais baseadas no prompt
        prompt_lower = prompt.lower()
        response = "0"  # valor padrão
        
        if "nome" in prompt_lower:
            response = "Cardeal João"
        elif "idade" in prompt_lower or "região" in prompt_lower:
            response = "0"
        elif any(attr in prompt_lower for attr in ["influence", "charisma", "scholarship", "discretion"]):
            response = "50"
        elif "escolha" in prompt_lower or "confirma" in prompt_lower:
            response = "0"
            
        logger.debug(f"Resposta gerada para prompt: {response}")
        return response

class TestGameFunctional(unittest.TestCase):
    def setUp(self):
        self.held_output = StringIO()
        self.original_stdout = sys.stdout
        sys.stdout = self.held_output
        
        # Configuração básica para inicialização
        self.basic_inputs = [
            "Cardeal João",  # Nome do cardeal
            "0",            # Idade
            "0",            # Região
            "50",           # Influence
            "50",           # Charisma
            "50",           # Scholarship
            "50",           # Discretion
            "0",            # Candidato favorito
        ]

    def tearDown(self):
        sys.stdout = self.original_stdout
        self.held_output.close()

    def _create_input_mock(self, initial_inputs=None):
        """Cria um mock inteligente para entrada do usuário"""
        smart_mock = SmartInputMock(initial_inputs or self.basic_inputs)
        mock = MagicMock()
        mock.side_effect = smart_mock.mock_input
        return mock

    @patch('builtins.input')
    def test_game_initialization(self, mock_input):
        """Testa a inicialização do jogo com entradas do usuário"""
        mock_input.side_effect = self._create_input_mock().mock_input
        
        game = Game()
        game.start_game()
        
        # Verifica se o cardeal foi criado corretamente
        self.assertEqual(game.player.name, "Cardeal João")
        self.assertEqual(game.player.influence, 50)
        self.assertEqual(game.player.charisma, 50)
        self.assertEqual(game.player.scholarship, 50)
        self.assertEqual(game.player.discretion, 50)
        
        output = self.held_output.getvalue()
        self.assertIn("Bem-vindo ao Conclave!", output)
        self.assertIn("Seu cardeal Cardeal João", output)

    @patch('builtins.input')
    def test_negotiation_phase(self, mock_input):
        """Testa uma rodada completa de negociação"""
        mock_input.side_effect = self._create_input_mock().mock_input
        
        game = Game()
        game.start_game()
        game.dialogues_and_negotiations_phase()
        
        self.assertEqual(game.interactions_this_cycle, 3)
        self.assertGreater(len(game.logger.history), 0)
        
        output = self.held_output.getvalue()
        self.assertIn("Fase de Negociações", output)
        self.assertIn("Interações restantes:", output)

    @patch('builtins.input')
    def test_voting_phase(self, mock_input):
        """Testa uma rodada de votação"""
        mock_input.side_effect = self._create_input_mock().mock_input
        
        game = Game()
        game.start_game()
        result = game.voting_rounds_phase()
        
        output = self.held_output.getvalue()
        self.assertIn("=== Fase de Votação ===", output)
        self.assertIn("Total de votos:", output)
        
        # Verifica se houve registro da votação
        voting_logs = [log for log in game.logger.history if "votação" in str(log).lower()]
        self.assertGreater(len(voting_logs), 0)

    @patch('builtins.input')
    def test_complete_game_round(self, mock_input):
        """Testa um ciclo completo do jogo"""
        mock_input.side_effect = self._create_input_mock().mock_input
        
        game = Game()
        game.start_game()
        
        # Executa uma rodada completa
        game.dialogues_and_negotiations_phase()
        game.voting_rounds_phase()
        
        self.assertEqual(game.rounds, 1)
        self.assertGreaterEqual(len(game.logger.history), 4)  # 3 ações + 1 votação
        
        output = self.held_output.getvalue()
        self.assertIn("Fase de Negociações", output)
        self.assertIn("Fase de Votação", output)

if __name__ == '__main__':
    unittest.main()
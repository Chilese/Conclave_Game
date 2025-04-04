from typing import List, Optional
import random
from ..core.models import Cardinal, Candidate, Faction
from ..events.event_system import EventManager
from ..utils.game_logging import GameLogger
from ..utils.game_utils import normalize_support, distribute_members_among_factions
from ..core.game_mechanics import GameMechanics
from ..ui.interface import (
    get_input, display_info, display_options,
    display_voting_results, display_feedback
)

class Game:
    """Classe principal do jogo que gerencia toda a lógica e estado."""
    
    def __init__(self):
        self.total_cardinals = 206
        self.npc_cardinals = 205
        self.rounds = 0
        self.interactions_this_cycle = 0
        self.player: Optional[Cardinal] = None
        self.favorite_candidate: Optional[Candidate] = None
        self.factions: List[Faction] = []
        self.event_manager = EventManager()
        self.logger = GameLogger()
        
    def start_game(self) -> None:
        """Inicializa e começa o jogo."""
        display_info("Bem-vindo ao Conclave!")
        self.player = self._configure_player_cardinal()
        self._initialize_factions()
        self.favorite_candidate = self._choose_favorite_candidate()
        self.player.ideology = self.favorite_candidate.ideology
        self._setup_event_listeners()
        self._display_initial_status()
        
    def run(self) -> None:
        """Executa o loop principal do jogo."""
        self.start_game()
        
        while True:
            self.interactions_this_cycle = 0
            self.dialogues_and_negotiations_phase()
            
            display_info("\nIniciando a votação...")
            if self.voting_rounds_phase():
                display_info("Um candidato venceu! O jogo terminou.")
                break
            else:
                display_info("Nenhuma maioria alcançada. Retornando para mais negociações...")
            
            self.logger.display_action_history()
            self.rounds += 1

    def _configure_player_cardinal(self) -> Cardinal:
        """Configura o cardeal do jogador."""
        name = input("Digite o nome do seu cardeal: ")
        age = get_input("Escolha sua faixa etária:", options=["Jovem", "Vétérano"])
        region = get_input("Escolha sua região:", options=["Europa", "Américas", "Ásia", "África"])
        
        display_info("Distribua 200 pontos entre seus atributos (0-100):")
        attributes = self._configure_attributes()
        
        return Cardinal(
            name=name,
            ideology=None,  # Será definido após escolher candidato favorito
            age=age,
            region=region,
            **attributes
        )

    def _configure_attributes(self) -> dict:
        """Configura os atributos do cardeal do jogador."""
        remaining = 200
        attributes = {}
        
        for attr in ["influence", "charisma", "scholarship", "discretion"]:
            value = get_input(
                f"{attr.title()} (restam {remaining})",
                min_val=0,
                max_val=remaining
            )
            attributes[attr] = value
            remaining -= value
            
        return attributes

    def _initialize_factions(self) -> None:
        """Inicializa as facções do jogo com seus candidatos."""
        faction_data = [
            ("Conservadores", "Conservador"),
            ("Moderados", "Moderado"),
            ("Progressistas", "Progressista")
        ]
        
        # Distribui os cardeais NPCs entre as facções
        distribution = distribute_members_among_factions(self.npc_cardinals, len(faction_data))
        
        # Nomes dos candidatos por ideologia
        candidate_names = {
            "Conservador": [
                ("Giovanni Rossi", "Veterano", "Itália"),
                ("Francisco Silva", "Veterano", "Brasil"),
                ("Thomas Wright", "Jovem", "Estados Unidos"),
                ("Heinrich Mueller", "Veterano", "Alemanha"),
                ("Liu Chen", "Jovem", "China")
            ],
            "Moderado": [
                ("Marco Bellini", "Jovem", "Itália"),
                ("Jean Dubois", "Veterano", "França"),
                ("James Smith", "Veterano", "Inglaterra"),
                ("Paulo Santos", "Jovem", "Portugal"),
                ("Matteo Romano", "Veterano", "Itália")
            ],
            "Progressista": [
                ("Roberto Gomes", "Jovem", "Brasil"),
                ("Michael Brown", "Jovem", "Estados Unidos"),
                ("Antonio Ferreira", "Veterano", "Portugal"),
                ("Hans Schmidt", "Veterano", "Alemanha"),
                ("Pierre Leclerc", "Jovem", "França")
            ]
        }
        
        for (name, ideology), num_members in zip(faction_data, distribution):
            faction = Faction(name, ideology, num_members)
            
            # Cria 5 candidatos para cada facção
            for candidate_name, age, region in candidate_names[ideology]:
                # Gera atributos balanceados para cada candidato
                base_attributes = 60
                variation = 20
                attributes = {
                    "influence": base_attributes + random.randint(-variation, variation),
                    "charisma": base_attributes + random.randint(-variation, variation),
                    "scholarship": base_attributes + random.randint(-variation, variation),
                    "discretion": base_attributes + random.randint(-variation, variation)
                }
                
                candidate = Candidate(
                    name=candidate_name,
                    ideology=ideology,
                    age=age,
                    region=region,
                    **attributes
                )
                
                # Adiciona suporte inicial balanceado
                faction.candidate_support[candidate] = 20.0  # Suporte inicial igual
            
            # Normaliza o suporte para garantir 100%
            normalize_support(faction.candidate_support)
            self.factions.append(faction)

    def _choose_favorite_candidate(self) -> Candidate:
        """Permite ao jogador escolher seu candidato favorito."""
        display_info("\nEscolha seu candidato favorito:")
        candidates = [c for f in self.factions for c in f.candidate_support.keys()]
        choice = get_input("Candidato:", options=[c.name for c in candidates])
        return candidates[choice]

    def _setup_event_listeners(self) -> None:
        """Configura os listeners de eventos."""
        self.event_manager.subscribe("persuasion_attempt", self._handle_persuasion)
        self.event_manager.subscribe("alliance_proposed", self._handle_alliance)
        self.event_manager.subscribe("rumor_manipulation", self._handle_rumor)

    def _display_initial_status(self) -> None:
        """Exibe o status inicial do jogo."""
        display_info(f"\nSeu cardeal {self.player.name}:")
        display_info(f"Ideologia: {self.player.ideology}")
        display_info(f"Candidato favorito: {self.favorite_candidate.name}")
        display_info(f"Total de cardeais eleitores: {self.total_cardinals}")

    def dialogues_and_negotiations_phase(self) -> None:
        """Executa uma rodada de negociações."""
        self.rounds += 1
        display_info(f"\n=== Rodada {self.rounds} - Fase de Negociações ===")
        
        while self.interactions_this_cycle < 3:
            self._handle_player_action()
            
        self.event_manager.update(self)

    def _handle_player_action(self) -> None:
        """Processa uma ação do jogador."""
        cardinals = [c for f in self.factions for c in f.candidate_support.keys()]
        target_idx = get_input("Escolha um cardeal para interagir:", options=[c.name for c in cardinals])
        target = cardinals[target_idx]
        
        action_idx = get_input("Escolha uma ação:", options=["Persuadir", "Propor Aliança", "Manipular Rumores"])
        action_types = ['persuadir', 'propor_alianca', 'manipular_rumores']
        action_type = action_types[action_idx]
        
        result = GameMechanics.execute_action(self.player, target, action_type, self)
        
        if result['success']:
            self.interactions_this_cycle += 1
            self.logger.log_action(action_type, target.name, True, result['impact'])
            display_info(f"Interações restantes: {3 - self.interactions_this_cycle}")
        else:
            display_info(f"Ação falhou: {result['message']}")

    def voting_rounds_phase(self) -> bool:
        """Executa uma rodada de votação."""
        display_info("\n=== Fase de Votação ===")
        
        candidate_votes = GameMechanics.calculate_votes(self.factions, self.rounds)
        
        # Adiciona o voto do jogador
        vote_idx = get_input("Seu voto:", options=[c.name for c in candidate_votes.keys()])
        player_vote = list(candidate_votes.keys())[vote_idx]
        candidate_votes[player_vote] += 1
        
        display_voting_results(candidate_votes, self.total_cardinals)
        
        # Verifica se há vencedor
        winner = self._check_winner(candidate_votes)
        if winner:
            display_info(f"\n{winner.name} foi eleito Papa!")
            return True
            
        # Redistribui suporte
        GameMechanics.redistribute_support_after_voting(
            self.factions, 
            candidate_votes, 
            self.total_cardinals, 
            self.favorite_candidate
        )
        return False

    def _check_winner(self, candidate_votes: dict) -> Optional[Candidate]:
        """Verifica se há um vencedor na votação."""
        required_majority = int(self.total_cardinals * 2 / 3) + 1
        
        for candidate, votes in candidate_votes.items():
            if votes >= required_majority:
                return candidate
        return None

    # Handlers de eventos
    def _handle_persuasion(self, **kwargs) -> None:
        target = kwargs.get('target')
        if target and target.discretion > 70:
            self.event_manager.trigger("counter_persuasion", **kwargs)

    def _handle_alliance(self, **kwargs) -> None:
        if kwargs.get('new_support', 0) > kwargs.get('previous_support', 0) * 1.5:
            self.event_manager.trigger("alliance_chain_reaction", **kwargs)

    def _handle_rumor(self, **kwargs) -> None:
        if not kwargs.get('success', False):
            self.event_manager.trigger("rumor_backfire", **kwargs)
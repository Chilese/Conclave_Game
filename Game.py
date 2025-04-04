import random
from Cardinal import Cardinal
from Candidate import Candidate
from Faction import Faction
from Event import Event
from Interactions import persuade, propose_alliance, manipulate_rumors, calcular_previa_impacto
from data import get_initial_factions, get_influential_cardinals
from ui import get_input, show_menu, display_info, display_voting_results
from rules import calculate_votes, check_majority
from utils import normalize_support
from events.GameEventManager import GameEventManager
from actions import execute_action  # Adicionar esta importação
from game_log import GameLog
from game_statistics import GameStatistics

# Constantes para valores fixos
TOTAL_CARDINALS = 206
NPC_CARDINALS = 205

class Game:
    def __init__(self):
        """Inicializa o estado do jogo."""
        self.player = None
        self.total_cardinals = TOTAL_CARDINALS
        self.factions = get_initial_factions(NPC_CARDINALS)
        self.influential_cardinals = get_influential_cardinals()
        self.candidates = self._select_candidates()
        self.current_phase = "preparation"
        self.events = [
            Event("Escândalo Revelado", 2, "negative"),
            Event("Elogio Público", 1, "positive"),
            Event("Crise de Confiança", 2, "negative")
        ]
        self.active_events = []
        self.rounds = 0
        self.interactions_this_cycle = 0
        self.game_log = GameLog()
        self.game_statistics = GameStatistics()
        self._setup_event_listeners()

    def _select_candidates(self):
        """Seleciona um cardeal influente de cada facção como candidato inicial."""
        candidates = []
        for faction in self.factions:
            faction_cardinals = [c for c in self.influential_cardinals if c.ideology == faction.ideology]
            if faction_cardinals:
                candidate = random.choice(faction_cardinals)
                candidates.append(candidate)
        return candidates

    def configure_player_cardinal(self):
        """Configura o cardeal do jogador."""
        name = input("Digite o nome do seu cardeal: ")
        age = get_input("Escolha sua faixa etária:", ["Jovem", "Vétérano"], "Vétérano")
        region = get_input("Escolha sua região:", ["Europa", "Américas", "Ásia", "África"], "Europa")

        display_info("Distribua 200 pontos entre Influência, Carisma, Erudição e Discrição (0-100):")
        influence, charisma, erudition, discretion = self.configure_cardinal()

        return Cardinal(name, None, age, region, influence, charisma, erudition, discretion)

    def configure_cardinal(self):
        remaining = 200
        attributes = {}
        for attr in ["Influência", "Carisma", "Erudição", "Discrição"]:
            value = int(get_input(f"{attr} (restam {remaining})", 0, remaining))
            attributes[attr] = value
            remaining -= value
        return attributes["Influência"], attributes["Carisma"], attributes["Erudição"], attributes["Discrição"]

    def choose_favorite_candidate(self):
        """Permite ao jogador escolher seu candidato favorito."""
        candidate_names = [c.name for c in self.candidates]
        candidate_choice = get_input("Escolha seu candidato favorito:", candidate_names, 0)
        return self.candidates[int(candidate_choice)]

    def start_game(self):
        """Configura o cardeal do jogador e o integra ao colégio."""
        display_info("Bem-vindo ao Conclave!")
        self.player = self.configure_player_cardinal()
        self.favorite_candidate = self.choose_favorite_candidate()
        self.player.ideology = self.favorite_candidate.ideology

        display_info(f"Seu cardeal {self.player.name}: Ideologia={self.player.ideology}, Influência={self.player.influence}, Carisma={self.player.charisma}, Erudição={self.player.scholarship}, Discrição={self.player.discretion}")
        display_info(f"Você escolheu {self.favorite_candidate.name} como seu candidato favorito.")
        display_info(f"Você é um dos {self.total_cardinals} cardeais eleitores do Conclave.")

        self.setup_context()

    def setup_context(self):
        """Configura o suporte inicial das facções."""
        display_info(f"\nConclave iniciado com {self.total_cardinals} cardeais eleitores.")
        for faction in self.factions:
            for cardinal in self.influential_cardinals:
                if cardinal.ideology == faction.ideology:
                    support = random.randint(10, 40)
                else:
                    support = random.randint(0, 15)
                faction.candidate_support[cardinal] = support
            normalize_support(faction.candidate_support)
            display_info(f"{faction.name}: Suporte inicial distribuído.")

    def log_action(self, message):
        """Registra uma ação no log."""
        self.game_log.log_message(message)

    def display_action_log(self):
        """Exibe o log de ações para o jogador."""
        self.game_log.display_history()

    def record_statistic(self, stat_name, value):
        """Registra uma estatística."""
        self.game_statistics.record_stat(stat_name, value)

    def display_statistics(self):
        """Exibe as estatísticas do jogo."""
        self.game_statistics.display_statistics()

    def display_strategic_context(self):
        """Exibe o contexto estratégico de forma mais clara."""
        display_info(f"\nStatus do Conclave - Rodada {self.rounds}", separator=True)
        
        # Suporte ao candidato favorito
        display_info("\n🎯 Seu Candidato:", separator=False)
        display_info(f"  {self.favorite_candidate.name} ({self.favorite_candidate.ideology})")
        
        display_info("\nSuporte por Facção:", separator=False)
        for faction in self.factions:
            support = faction.candidate_support.get(self.favorite_candidate, 0)
            bar = "█" * int(support / 2)  # Barra de progresso visual
            display_info(f"  {faction.name:12} [{bar:<50}] {support:.1f}%")
        
        # Top 3 rivais
        display_info("\n🔄 Principais Rivais:", separator=False)
        rivals = sorted(
            [c for c in self.candidates if c != self.favorite_candidate],
            key=lambda c: sum(f.candidate_support.get(c, 0) for f in self.factions),
            reverse=True
        )[:3]
        
        for rival in rivals:
            total = sum(f.candidate_support.get(rival, 0) for f in self.factions)
            display_info(f"  {rival.name:12} - {total:.1f}% de suporte total")
        
        display_info("", separator=True)

    def dialogues_and_negotiations_phase(self):
        """Executa uma rodada de negociações."""
        self.rounds += 1
        self.display_strategic_context()
        display_info(f"\nRodada {self.rounds} - Fase de Negociações:")
        
        # Gera novo evento apenas no início da rodada
        if random.random() < 0.3 and self.events:
            event = random.choice(self.events)
            self.active_events.append({"event": event, "remaining": event.duration})
            display_info(f"Evento: {event.name}")
            event.apply(self.factions, self.influential_cardinals)

        # Mapeamento de índices para tipos de ação
        action_types = {
            0: 'persuadir',
            1: 'propor_alianca',
            2: 'manipular_rumores'
        }

        # Executa as interações do jogador
        while self.interactions_this_cycle < 3:
            choice = show_menu("Escolha um cardeal para interagir:", [c.name for c in self.influential_cardinals])
            target = self.influential_cardinals[choice]
            display_info(f"Interagindo com {target.name} ({target.ideology})")
            action_idx = get_input("Escolha uma ação:", ["Persuadir", "Propor Aliança", "Manipular Rumores"], None)

            # Converte o índice da ação para o tipo de ação
            action_type = action_types[action_idx]

            # Calcula o impacto antes da ação
            proceed = calcular_previa_impacto(action_idx, self.player, target, self.favorite_candidate)
            if not proceed:
                display_info("Ação cancelada. Escolha outro cardeal ou ação.")
                continue
            
            # Executa a ação usando o tipo de ação correto
            result = execute_action(self.player, target, action_type, self)
            
            if result['success']:
                self.interactions_this_cycle += 1
                display_info(result['message'])
                display_info(f"Interações restantes neste ciclo: {3 - self.interactions_this_cycle}")
                
                if self.interactions_this_cycle >= 3:
                    break
            else:
                display_info(f"Ação falhou: {result['message']}")

        # Verifica e atualiza eventos apenas ao final da rodada
        for active in self.active_events[:]:
            active["remaining"] -= 1
            if active["remaining"] <= 0:
                display_info(f"Evento {active['event'].name} terminou.")
                self.active_events.remove(active)

    def display_faction_support(self):
        """Exibe o suporte percentual de cada candidato em cada facção, ordenado e com separadores."""
        display_info("\nSuporte Atual das Facções aos Candidatos:")
        for faction in self.factions:
            display_info(f"\n{faction.name} ({faction.ideology}):")
            # Ordena candidatos por suporte decrescente
            sorted_candidates = sorted(faction.candidate_support.items(), key=lambda x: x[1], reverse=True)
            for candidate, support in sorted_candidates:
                display_info(f"  {candidate.name}: {support:.2f}%")
            display_info("-" * 40)  # Separador visual

    def voting_rounds_phase(self):
        """Realiza uma votação com total fixo de 206 votos."""
        display_info(f"\nRodada de Votação {self.rounds + 1}:")
        self.display_faction_support()
        
        candidate_votes = calculate_votes(self.factions, self.rounds)
        total_npc_votes = sum(candidate_votes.values())
        if total_npc_votes != NPC_CARDINALS:
            raise ValueError(f"Erro: Votos dos NPCs devem ser {NPC_CARDINALS}, mas são {total_npc_votes}")
        
        vote_choice = show_menu("Escolha em quem votar:", [c.name for c in self.influential_cardinals])
        player_vote = self.influential_cardinals[vote_choice]
        display_info(f"Você votou em {player_vote.name}.")
        candidate_votes[player_vote] = candidate_votes.get(player_vote, 0) + 1
        
        total_votes = sum(candidate_votes.values())
        if total_votes != TOTAL_CARDINALS:
            raise ValueError(f"Erro: Total de votos deve ser {TOTAL_CARDINALS}, mas é {total_votes}")
        
        # Usar nova função de exibição
        display_voting_results(candidate_votes, total_votes)
        
        display_info(f"\nResumo da Rodada {self.rounds + 1}:")
        for faction in self.factions:
            display_info(f"\n{faction.name} ({faction.ideology}):")
            for candidate, support in faction.candidate_support.items():
                display_info(f"  {candidate.name}: {support:.2f}%")
        self.game_log.log_message(f"Resumo da Rodada {self.rounds + 1} exibido.")

        total_voters = self.total_cardinals
        winner, required_votes, current_leader = check_majority(candidate_votes, total_voters)
        
        if winner:
            display_info(f"{winner.name} foi eleito Papa com {candidate_votes[winner]} votos!")
            display_info(f"Votos necessários para vitória: {required_votes}")
            return True
        else:
            display_info(f"Nenhum candidato alcançou a maioria de {required_votes} votos.")
            display_info(f"Líder atual: {current_leader.name} com {candidate_votes[current_leader]} votos")
            self.adjust_faction_support(candidate_votes)
            return False

    def adjust_faction_support(self, candidate_votes):
        """Ajusta o suporte com consolidação estratégica."""
        top_candidates = sorted(candidate_votes.items(), key=lambda x: x[1], reverse=True)[:5 if self.rounds < 2 else 3]
        for faction in self.factions:
            for cardinal in self.influential_cardinals:
                if cardinal not in faction.candidate_support or faction.candidate_support[cardinal] < 1:
                    faction.candidate_support[cardinal] = 1
            for candidate, votes in top_candidates:
                if candidate in faction.candidate_support:
                    faction.candidate_support[candidate] += 10 + (self.rounds * 3)
            
            # Protege o suporte ao candidato favorito manualmente
            if self.favorite_candidate in faction.candidate_support:
                faction.candidate_support[self.favorite_candidate] = max(
                    15.0, faction.candidate_support[self.favorite_candidate] + 10.0
                )
            
            # Normaliza o suporte sem o argumento `favorite_candidate`
            normalize_support(faction.candidate_support)

    def _setup_event_listeners(self):
        GameEventManager.subscribe("persuasion_attempt", self._handle_persuasion)
        GameEventManager.subscribe("alliance_proposed", self._handle_alliance)
        GameEventManager.subscribe("rumor_manipulation", self._handle_rumor)

    def _handle_persuasion(self, event_data):
        target = event_data["target"]
        if target.discretion > 70:
            self._trigger_reaction_event("counter_persuasion", event_data)

    def _handle_alliance(self, event_data):
        if event_data["new_support"] > event_data["previous_support"] * 1.5:
            self._trigger_reaction_event("alliance_chain_reaction", event_data)

    def _handle_rumor(self, event_data):
        if not event_data["success"]:
            self._trigger_reaction_event("rumor_backfire", event_data)

    def _trigger_reaction_event(self, event_type, original_data):
        for faction in self.factions:
            if faction != original_data["faction"]:
                self._apply_reaction_effect(event_type, faction, original_data)

    def run(self):
        """Executa o loop principal do jogo."""
        self.start_game()
        while True:
            # Reseta o contador no início de cada rodada
            self.interactions_this_cycle = 0
            
            # Executa uma única rodada de negociações
            self.dialogues_and_negotiations_phase()
            
            # Inicia a votação após as 3 interações
            display_info("\nIniciando a votação...")
            if self.voting_rounds_phase():
                display_info("Um candidato venceu! O jogo terminou.")
                break
            else:
                display_info("Nenhuma maioria alcançada. Retornando para mais negociações...")
            self.display_action_log()
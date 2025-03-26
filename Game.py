import random
from Cardinal import Cardinal
from Candidate import Candidate
from Faction import Faction
from Event import Event
from Interactions import persuade, propose_alliance, manipulate_rumors, calcular_previa_impacto
from data import get_initial_factions, get_influential_cardinals
from ui import get_input, show_menu, display_info
from rules import calculate_votes, check_majority
from utils import normalize_support
from events.GameEventManager import GameEventManager

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
        self.action_log = []
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
        self.action_log.append(message)

    def display_action_log(self):
        """Exibe o log de ações para o jogador."""
        display_info("\nHistórico de Ações:")
        for action in self.action_log:
            display_info(f"- {action}")

    def display_strategic_context(self):
        """Exibe o contexto estratégico de forma mais clara."""
        display_info(f"\nStatus do Conclave - Rodada {self.rounds}", separator=True)
        
        # Suporte ao candidato favorito
        display_info("\n🎯 Seu Candidato:", separator=False)
        display_info(f"  {self.favorite_candidate.name} ({self.favorite_candidate.ideology})")
        
        display_info("\nSuporte por Facção:", separator=False)
        for faction in self.factions:
            support = faction.candidate_support.get(self.favorite_candidate, 0)
            bar = "█" * int(support/2)  # Barra de progresso visual
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

        # Executa as interações do jogador
        while True:
            choice = show_menu("Escolha um cardeal para interagir:", [c.name for c in self.influential_cardinals])
            target = self.influential_cardinals[choice]
            display_info(f"Interagindo com {target.name} ({target.archetype})")
            action = get_input("Escolha uma ação:", ["Persuadir", "Propor Aliança", "Manipular Rumores"], None)

            # Calcula o impacto antes da ação
            proceed = calcular_previa_impacto(action, self.player, target, self.favorite_candidate)
            if not proceed:
                display_info("Ação cancelada. Escolha outro cardeal ou ação.")
                continue  # Volta ao início do loop para nova escolha
            
            # Se chegou aqui, a ação foi confirmada
            try:
                target_faction = next(f for f in self.factions if f.ideology == target.ideology)
            except StopIteration:
                display_info(f"Nenhuma facção encontrada para a ideologia {target.ideology}.")
                return

            # Executa a ação e registra o impacto
            previous_support = target_faction.candidate_support.get(self.favorite_candidate, 0)
            if action == "Persuadir":
                persuade(self.player, target, self.favorite_candidate, self.factions)
                self.log_action(f"Você persuadiu {target.name}.")
            elif action == "Propor Aliança":
                propose_alliance(self.player, target, self.favorite_candidate, self.factions)
                self.log_action(f"Você propôs uma aliança com {target.name}.")
            elif action == "Manipular Rumores":
                manipulate_rumors(self.player, target, self.favorite_candidate, self.factions, self.candidates)
                self.log_action(f"Você manipulou rumores contra {target.name}.")

            # Calcula o suporte após a ação
            new_support = target_faction.candidate_support.get(self.favorite_candidate, 0)
            change = new_support - previous_support

            display_info("\n=== Resultado da Interação ===")
            display_info(f"Ação: {action}")
            display_info(f"Alvo: {target.name}")
            display_info(f"Resultado: {'Sucesso!' if change > 0 else 'Impacto Limitado' if change == 0 else 'Resultado Negativo!'}")
            display_info(f"\nSuporte ao {self.favorite_candidate.name} na facção {target_faction.name}:")
            display_info(f"  Antes: {previous_support:.1f}%")
            display_info(f"  Depois: {new_support:.1f}%")
            display_info(f"  Mudança: {change:+.1f}%")
            
            if change > 0:
                display_info("\nSua ação foi bem sucedida e aumentou o suporte ao seu candidato!")
            elif change < 0:
                display_info("\nAtenção! Sua ação teve um efeito negativo e reduziu o suporte ao seu candidato.")
            else:
                display_info("\nSua ação teve um impacto neutro. Considere usar uma abordagem diferente da próxima vez.")
            
            display_info("\nDica: Compare o resultado real com a prévia para aprender como suas ações funcionam!")
            break  # Sai do loop após uma ação bem-sucedida

        # Verifica e atualiza eventos APENAS ao final da rodada
        if self.interactions_this_cycle >= 3:  # Última interação da rodada
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
        display_info(f"Total de votos computados: {total_votes}")
        for candidate, votes in candidate_votes.items():
            display_info(f"{candidate.name}: {votes} votos")
            candidate.vote_count = votes

        display_info(f"\nResumo da Rodada {self.rounds + 1}:")
        for faction in self.factions:
            display_info(f"\n{faction.name} ({faction.ideology}):")
            for candidate, support in faction.candidate_support.items():
                display_info(f"  {candidate.name}: {support:.2f}%")
        self.log_action(f"Resumo da Rodada {self.rounds + 1} exibido.")

        total_voters = self.total_cardinals
        winner = check_majority(candidate_votes, total_voters)
        if winner:
            display_info(f"{winner.name} foi eleito Papa com {candidate_votes[winner]} votos!")
            return True
        else:
            display_info("Nenhum candidato alcançou a maioria de 2/3. Nova rodada de negociações.")
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
            while self.interactions_this_cycle < 3:
                self.dialogues_and_negotiations_phase()
                self.interactions_this_cycle += 1
                display_info(f"Interações concluídas no ciclo: {self.interactions_this_cycle}/3")

            display_info("\nIniciando a votação...")
            if self.voting_rounds_phase():
                display_info("Um candidato venceu! O jogo terminou.")
                break
            else:
                display_info("Nenhuma maioria alcançada. Retornando para mais negociações...")
                self.interactions_this_cycle = 0
            self.display_action_log()
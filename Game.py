import random
from Cardinal import Cardinal
from Candidate import Candidate
from Faction import Faction
from Event import Event
from Interactions import persuade, propose_alliance, manipulate_rumors, calcular_previa_impacto
from data import get_initial_factions, get_influential_cardinals
from ui import get_input, show_menu, display_info
from rules import calculate_votes, check_majority
from utils import normalize_support  # Importa função utilitária

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
        self.action_log = []  # Adicionado: Log de ações

    def _select_candidates(self):
        """Seleciona um cardeal influente de cada facção como candidato inicial."""
        candidates = []
        for faction in self.factions:
            faction_cardinals = [c for c in self.influential_cardinals if c.ideology == faction.ideology]
            if faction_cardinals:
                candidate = random.choice(faction_cardinals)
                candidates.append(candidate)
        return candidates

    def normalize_support(self, support_dict):
        """Normaliza os valores de suporte para que somem 100%."""
        normalize_support(support_dict)  # Usa a função centralizada

    def configure_player_cardinal(self):
        """Configura o cardeal do jogador."""
        name = input("Digite o nome do seu cardeal: ")
        age = get_input("Escolha sua faixa etária:", ["Jovem", "Vétérano"], "Vétérano")
        region = get_input("Escolha sua região:", ["Europa", "Américas", "Ásia", "África"], "Europa")

        display_info("Distribua 200 pontos entre Influência, Carisma, Erudição e Discrição (0-100):")
        influence = int(get_input("Influência:", list(range(0, 101)), 50))
        remaining = 200 - influence
        charisma = int(get_input(f"Carisma (restam {remaining}):", list(range(0, remaining + 1)), 50))
        remaining -= charisma
        scholarship = int(get_input(f"Erudição (restam {remaining}):", list(range(0, remaining + 1)), 50))
        remaining -= scholarship
        discretion = int(get_input(f"Discrição (restam {remaining}):", list(range(0, remaining + 1)), remaining))

        return Cardinal(name, None, age, region, influence, charisma, scholarship, discretion)

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
            self.normalize_support(faction.candidate_support)
            display_info(f"{faction.name}: Suporte inicial distribuído.")

    def log_action(self, message):
        """Registra uma ação no log."""
        self.action_log.append(message)

    def display_action_log(self):
        """Exibe o log de ações para o jogador."""
        display_info("\nHistórico de Ações:")
        for action in self.action_log:
            display_info(f"- {action}")

    def dialogues_and_negotiations_phase(self):
        """Executa uma rodada de negociações."""
        self.rounds += 1
        display_info(f"\nRodada {self.rounds} - Fase de Negociações:")
        
        if random.random() < 0.3 and self.events:
            event = random.choice(self.events)
            self.active_events.append({"event": event, "remaining": event.duration})
            display_info(f"Evento: {event.name}")
            event.apply(self.factions, self.influential_cardinals)

        for active in self.active_events[:]:
            active["remaining"] -= 1
            if active["remaining"] <= 0:
                display_info(f"Evento {active['event'].name} terminou.")
                self.active_events.remove(active)

        choice = show_menu("Escolha um cardeal para interagir:", [c.name for c in self.influential_cardinals])
        target = self.influential_cardinals[choice]
        display_info(f"Interagindo com {target.name} ({target.archetype})")
        action = get_input("Escolha uma ação:", ["Persuadir", "Propor Aliança", "Manipular Rumores"], None)

        # Adicionado: Exibe a prévia do impacto antes de realizar a ação
        calcular_previa_impacto(action, self.player, target, self.favorite_candidate)

        try:
            target_faction = next(f for f in self.factions if f.ideology == target.ideology)
        except StopIteration:
            display_info(f"Nenhuma facção encontrada para a ideologia {target.ideology}.")
            return

        if action == "Persuadir":
            persuade(self.player, target, self.favorite_candidate, self.factions)
            self.log_action(f"Você persuadiu {target.name}.")
        elif action == "Propor Aliança":
            propose_alliance(self.player, target, self.favorite_candidate, self.factions)
            self.log_action(f"Você propôs uma aliança com {target.name}.")
        elif action == "Manipular Rumores":
            manipulate_rumors(self.player, target, self.favorite_candidate, self.factions, self.candidates)
            self.log_action(f"Você manipulou rumores contra {target.name}.")

    def display_faction_support(self):
        """Exibe o suporte percentual de cada candidato em cada facção."""
        display_info("\nSuporte Atual das Facções aos Candidatos:")
        for faction in self.factions:
            display_info(f"\n{faction.name} ({faction.ideology}):")
            for candidate, support in faction.candidate_support.items():
                display_info(f"  {candidate.name}: {support:.2f}%")

    def voting_rounds_phase(self):
        """Realiza uma votação com total fixo de 206 votos."""
        display_info(f"\nRodada de Votação {self.rounds + 1}:")
        self.display_faction_support()  # Adicionado para fornecer visão geral antes da votação
        
        # Calcula os votos dos NPCs (205)
        candidate_votes = calculate_votes(self.factions, self.rounds)
        
        # Verifica que os votos dos NPCs somam 205
        total_npc_votes = sum(candidate_votes.values())
        if total_npc_votes != NPC_CARDINALS:
            raise ValueError(f"Erro: Votos dos NPCs devem ser {NPC_CARDINALS}, mas são {total_npc_votes}")
        
        # Voto do jogador
        vote_choice = show_menu("Escolha em quem votar:", [c.name for c in self.influential_cardinals])
        player_vote = self.influential_cardinals[vote_choice]
        display_info(f"Você votou em {player_vote.name}.")
        candidate_votes[player_vote] = candidate_votes.get(player_vote, 0) + 1
        
        # Verifica o total final
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
        # Adiciona o resumo ao log de ações
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
            # Mantém suporte mínimo
            for cardinal in self.influential_cardinals:
                if cardinal not in faction.candidate_support or faction.candidate_support[cardinal] < 1:
                    faction.candidate_support[cardinal] = 1
            
            # Reforça os mais votados
            for candidate, votes in top_candidates:
                if candidate in faction.candidate_support:
                    faction.candidate_support[candidate] += 10 + (self.rounds * 3)
            
            # Normaliza para 100%
            total_support = sum(faction.candidate_support.values())
            if total_support > 0:
                for candidate in faction.candidate_support:
                    faction.candidate_support[candidate] = (faction.candidate_support[candidate] / total_support) * 100

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
            self.display_action_log()  # Exibe o log de ações no final do turno
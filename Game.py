import random
from Cardinal import Cardinal
from Candidate import Candidate
from Faction import Faction
from Event import Event
from Interactions import Interactions
from data import get_initial_factions, get_influential_cardinals
from ui import get_input, show_menu, display_info
from rules import calculate_votes, check_majority

class Game:
    def __init__(self):
        """Inicializa o estado do jogo."""
        self.player = None
        self.total_cardinals = 206  # Total de eleitores (205 NPCs + jogador)
        self.factions = get_initial_factions(self.total_cardinals - 1)  # 205 NPCs distribuídos
        self.influential_cardinals = get_influential_cardinals()  # 5 influentes por facção
        self.candidates = self._select_candidates()  # 1 candidato por facção
        self.current_phase = "preparation"
        self.events = [
            Event("Escândalo Revelado", 2, "negative"),
            Event("Elogio Público", 1, "positive"),
            Event("Crise de Confiança", 2, "negative")
        ]
        self.active_events = []  # Eventos ativos
        self.rounds = 0
        self.interactions_this_cycle = 0  # Contador de interações

    def _select_candidates(self):
        """Seleciona um cardeal influente de cada facção como candidato (exclui o jogador inicialmente)."""
        candidates = []
        for faction in self.factions:
            faction_cardinals = [c for c in self.influential_cardinals if c.ideology == faction.ideology and c != self.player]
            if faction_cardinals:
                candidate = random.choice(faction_cardinals)
                candidates.append(candidate)
        return candidates

    def start_game(self):
        """Configura o cardeal do jogador e o integra ao colégio."""
        display_info("Bem-vindo ao Conclave!")
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

        candidate_names = [c.name for c in self.candidates]
        candidate_choice = get_input("Escolha seu candidato favorito:", candidate_names, 0)
        self.favorite_candidate = self.candidates[int(candidate_choice)]
        
        ideology = self.favorite_candidate.ideology
        self.player = Cardinal(name, ideology, age, region, influence, charisma, scholarship, discretion)
        
        # Adiciona o jogador à lista de cardeais influentes
        self.influential_cardinals.append(self.player)
        
        display_info(f"Seu cardeal {name}: Ideologia={ideology}, Influência={influence}, Carisma={charisma}, Erudição={scholarship}, Discrição={discretion}")
        display_info(f"Você escolheu {self.favorite_candidate.name} como seu candidato favorito.")
        display_info(f"Você é um dos {self.total_cardinals} cardeais eleitores do Conclave.")

        self.setup_context()

    def setup_context(self):
        """Configura o suporte inicial das facções."""
        display_info(f"\nConclave iniciado com {self.total_cardinals} cardeais eleitores.")
        for faction in self.factions:
            for cardinal in self.influential_cardinals:
                if cardinal.ideology == faction.ideology:
                    support = random.randint(5, 30)
                    faction.candidate_support[cardinal] = support
                else:
                    faction.candidate_support[cardinal] = random.randint(0, 10)
            # Normalizar o suporte para soma = 100%
            total_support = sum(faction.candidate_support.values())
            if total_support > 0:
                for candidate in faction.candidate_support:
                    faction.candidate_support[candidate] = (faction.candidate_support[candidate] / total_support) * 100
            display_info(f"{faction.name}: Suporte inicial distribuído entre cardeais.")

    def dialogues_and_negotiations_phase(self):
        """Executa uma rodada de negociações."""
        self.rounds += 1
        display_info(f"\nRodada {self.rounds} - Fase de Negociações:")
        
        if random.random() < 0.2 and self.events:
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

        if action == "Persuadir":
            Interactions.persuade(self.player, target, self.favorite_candidate, self.factions)
        elif action == "Propor Aliança":
            Interactions.propose_alliance(self.player, target, self.favorite_candidate, self.factions)
        elif action == "Manipular Rumores":
            Interactions.manipulate_rumors(self.player, target, self.favorite_candidate, self.factions, self.candidates)

    def voting_rounds_phase(self):
        """Realiza uma votação, incluindo o voto do jogador, e verifica se há um vencedor."""
        display_info("\nRodada de Votação:")
        
        # Calcula os votos dos NPCs (205 eleitores)
        candidate_votes = calculate_votes(self.factions)
        
        # Permite que o jogador vote
        vote_choice = show_menu("Escolha em quem votar:", [c.name for c in self.influential_cardinals])
        player_vote = self.influential_cardinals[vote_choice]
        display_info(f"Você votou em {player_vote.name}.")
        
        # Adiciona o voto do jogador ao total
        candidate_votes[player_vote] = candidate_votes.get(player_vote, 0) + 1
        
        total_votes = sum(candidate_votes.values())
        display_info(f"Total de votos computados: {total_votes}")  # Debug
        for candidate, votes in candidate_votes.items():
            display_info(f"{candidate.name}: {votes} votos")
            candidate.vote_count = votes

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
        """Ajusta o suporte das facções para os candidatos mais votados."""
        top_candidates = sorted(candidate_votes.items(), key=lambda x: x[1], reverse=True)[:2]
        for faction in self.factions:
            for candidate, _ in top_candidates:
                if candidate in faction.candidate_support:
                    faction.candidate_support[candidate] += 15
                else:
                    faction.candidate_support[candidate] = 5
            # Normalizar o suporte para soma = 100%
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
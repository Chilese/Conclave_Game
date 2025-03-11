import random
from Cardinal import Cardinal
from Candidate import Candidate
from Faction import Faction
from Event import Event
from data import get_initial_factions, get_initial_candidates, get_influential_cardinals
from ui import get_input, show_menu, display_info
from rules import calculate_votes, check_majority

class Game:
    def __init__(self):
        self.player = None
        self.factions = get_initial_factions()
        self.candidates = get_initial_candidates()
        self.influential_cardinals = get_influential_cardinals()
        self.current_phase = "preparation"
        self.events = [
            Event("Escândalo Revelado", lambda: self.apply_scandal(), 2, "negative"),
            Event("Elogio Público", lambda: self.apply_praise(), 1, "positive"),
            Event("Crise de Confiança", lambda: self.apply_crisis(), 2, "negative")
        ]
        self.active_events = []  # Lista de eventos ativos com duração restante
        self.rounds = 0
        self.total_cardinals = random.randint(230, 270)
        self.voting_cardinals = self.total_cardinals - 50  # 200 eleitores aproximados

    def apply_scandal(self):
        faction = random.choice(self.factions)
        for cardinal in self.influential_cardinals:
            if cardinal.ideology == faction.ideology:
                cardinal.influence = max(0, cardinal.influence - 10)
        display_info(f"Escândalo! Influência dos cardeais {faction.name} caiu.")

    def apply_praise(self):
        faction = random.choice(self.factions)
        for cardinal in self.influential_cardinals:
            if cardinal.ideology == faction.ideology:
                cardinal.charisma = min(100, cardinal.charisma + 10)
        display_info(f"Elogio Público! Carisma dos cardeais {faction.name} aumentou.")

    def apply_crisis(self):
        faction = random.choice(self.factions)
        for cardinal in self.influential_cardinals:
            if cardinal.ideology == faction.ideology:
                cardinal.discretion = max(0, cardinal.discretion - 10)
        display_info(f"Crise de Confiança! Discrição dos cardeais {faction.name} caiu.")

    def start_game(self):
        display_info("Bem-vindo ao Conclave!")
        name = input("Digite o nome do seu cardeal: ")
        # Removido: ideology = get_input("Escolha sua ideologia:", ["Conservador", "Moderado", "Progressista"], "Moderado")
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

        # Escolha do candidato favorito
        candidate_names = [c.name for c in self.candidates]
        candidate_choice = get_input("Escolha seu candidato favorito:", candidate_names, 0)
        self.favorite_candidate = self.candidates[int(candidate_choice)]
        
        # O jogador herda a ideologia do candidato favorito
        ideology = self.favorite_candidate.ideology
        self.player = Cardinal(name, ideology, age, region, influence, charisma, scholarship, discretion)
        
        display_info(f"Seu cardeal {name}: Ideologia={ideology}, Influência={influence}, Carisma={charisma}, Erudição={scholarship}, Discrição={discretion}")
        display_info(f"Você escolheu {self.favorite_candidate.name} como seu candidato favorito.")

        # Montagem do contexto
        self.setup_context()

    def setup_context(self):
        display_info(f"\nConclave iniciado com {self.total_cardinals} cardeais, dos quais {self.voting_cardinals} são eleitores.")
        for faction in self.factions:
            faction_cardinals = [c for c in self.influential_cardinals if c.ideology == faction.ideology]
            strength = sum((c.influence + c.charisma) // 2 for c in faction_cardinals) // 5
            faction.candidate_support[self.candidates[self.factions.index(faction)]] = strength
            display_info(f"{faction.name}: Força {strength}/100")
        leading_faction = max(self.factions, key=lambda f: f.candidate_support.get(self.candidates[self.factions.index(f)], 0))
        display_info(f"Os {leading_faction.name} estão liderando com uma vantagem inicial.")

    def dialogues_and_negotiations_phase(self):
        self.rounds += 1
        display_info(f"\nRodada {self.rounds} - Fase de Negociações:")
        
        # Verificar eventos
        if random.random() < 0.2 and self.events:  # 20% de chance
            event = random.choice(self.events)
            self.active_events.append({"event": event, "remaining": event.duration})
            display_info(f"Evento: {event.name}")
            event.effect()

        # Atualizar eventos ativos
        for active in self.active_events[:]:
            active["remaining"] -= 1
            if active["remaining"] <= 0:
                display_info(f"Evento {active['event'].name} terminou.")
                self.active_events.remove(active)

        choice = show_menu("Escolha um cardeal para interagir:", [c.name for c in self.influential_cardinals] + ["Sair"])
        if choice == len(self.influential_cardinals):  # Sair
            return
        target = self.influential_cardinals[choice]
        display_info(f"Interagindo com {target.name} ({target.archetype})")
        action = get_input("Escolha uma ação:", ["Persuadir", "Propor Aliança", "Manipular Rumores"], None)

        if action == "Persuadir":
            result = (self.player.charisma + self.player.scholarship) - (target.charisma + target.scholarship + target.modifiers["persuasion"])
            if result > 5:
                self.player.influence = min(100, self.player.influence + random.randint(3, 7))
                target_faction = next(f for f in self.factions if f.ideology == target.ideology)
                target_faction.candidate_support[self.favorite_candidate] = min(100, target_faction.candidate_support.get(self.favorite_candidate, 0) + 10)
                display_info("Sucesso! Influência aumentada.")
            else:
                self.player.influence = max(0, self.player.influence - random.randint(2, 5))
                display_info("Falha! Influência reduzida.")

        elif action == "Propor Aliança":
            result = (self.player.influence + self.player.discretion) - (target.influence + target.discretion + target.modifiers["alliance"])
            if result > 5:
                self.player.influence = min(100, self.player.influence + random.randint(5, 10))
                target_faction = next(f for f in self.factions if f.ideology == target.ideology)
                target_faction.candidate_support[self.favorite_candidate] = min(100, target_faction.candidate_support.get(self.favorite_candidate, 0) + 15)
                display_info("Sucesso! Aliança formada.")
            else:
                self.player.discretion = max(0, self.player.discretion - random.randint(3, 8))
                display_info("Falha! Discrição reduzida.")

        elif action == "Manipular Rumores":
            result = (self.player.discretion + self.player.scholarship) - (target.discretion + target.scholarship + target.modifiers["rumors"])
            if result > 5:
                self.player.discretion = min(100, self.player.discretion + random.randint(4, 8))
                target_faction = next(f for f in self.factions if f.ideology == target.ideology)
                rival = random.choice([c for c in self.candidates if c != self.favorite_candidate])
                target_faction.candidate_support[rival] = max(0, target_faction.candidate_support.get(rival, 0) - 10)
                display_info("Sucesso! Rumores espalhados.")
            else:
                self.player.influence = max(0, self.player.influence - random.randint(2, 6))
                display_info("Falha! Influência reduzida.")

    def voting_rounds_phase(self):
        display_info("\nRodada de Votação:")
        candidate_votes = calculate_votes(self.factions)
        for candidate, votes in candidate_votes.items():
            display_info(f"{candidate.name}: {votes} votos")
            candidate.vote_count = votes

        total_voters = sum(faction.num_members for faction in self.factions)
        winner = check_majority(candidate_votes, total_voters)
        if winner:
            display_info(f"{winner.name} foi eleito Papa!")
            return True
        display_info("Nenhum candidato alcançou a maioria. Nova rodada de negociações.")
        return False

    def run(self):
        self.start_game()
        while True:
            if self.rounds >= 3:  # Pelo menos 3 rodadas antes da votação
                if self.voting_rounds_phase():
                    break
            self.dialogues_and_negotiations_phase()
import random
from Cardinal import Cardinal
from Candidate import Candidate
from Faction import Faction
from NonElector import NonElector
from data import get_initial_factions, get_initial_candidates, get_initial_non_electors
from ui import get_input, show_menu, display_info
from rules import calculate_votes, check_majority

class Game:
    def __init__(self):
        self.player = None
        self.factions = get_initial_factions()
        self.candidates = get_initial_candidates()
        self.non_electors = get_initial_non_electors()
        self.current_phase = "information_gathering"
        self.events = []

    def start_game(self):
        display_info("Bem-vindo ao Conclave!")
        name = input("Digite o nome do seu cardeal: ")
        ideology = get_input("Escolha a ideologia do seu cardeal:", ["Conservador", "Moderado", "Progressista"], "Moderado")
        age = get_input("Escolha a faixa etária do seu cardeal:", ["Jovem e adaptável", "Vétérano e autoritário"], "Vétérano")
        bloc = get_input("Escolha o bloco regional do seu cardeal:", ["Europa", "Américas", "Ásia", "África"], "Europa")

        influence = random.randint(1, 10)
        charisma = random.randint(1, 10)
        scholarship = random.randint(1, 10)
        strategy = random.randint(1, 10)
        discretion = random.randint(1, 10)

        self.player = Cardinal(name, ideology, age, bloc, influence, charisma, scholarship, strategy, discretion)
        display_info(f"Seu cardeal {name} foi criado com os seguintes atributos:")
        display_info(f"Ideologia: {ideology}")
        display_info(f"Idade: {age}")
        display_info(f"Bloco regional: {bloc}")
        display_info(f"Influência: {influence}")
        display_info(f"Carisma: {charisma}")
        display_info(f"Erudição: {scholarship}")
        display_info(f"Estratégia: {strategy}")
        display_info(f"Discrição: {discretion}")

    def information_gathering_phase(self):
        display_info("Fase de coleta de informação:")
        while True:
            choice = show_menu("Escolha um cardeal não eleitor para falar:", [n.name for n in self.non_electors])
            if choice == 0:
                break
            elif 1 <= choice <= len(self.non_electors):
                selected = self.non_electors[choice - 1]
                display_info(f"Falando com {selected.name}:")
                for info in selected.information:
                    display_info(info)
            else:
                display_info("Escolha inválida. Tente novamente.")

    def dialogues_and_negotiations_phase(self):
        display_info("Fase de diálogos e negociações:")
        while True:
            choice = show_menu("Escolha uma facção para interagir ou saia:", [f.name for f in self.factions])
            if choice == 0:
                break
            elif 1 <= choice <= len(self.factions):
                selected_faction = self.factions[choice - 1]
                display_info(f"Interagindo com {selected_faction.name}:")
                action = get_input("Escolha uma ação:", ["Persuadir a apoiar meu candidato", "Oferecer favor para ganhar suporte"], None)
                if action == "Persuadir a apoiar meu candidato":
                    success_chance = self.player.charisma * 10
                    if random.randint(1, 100) <= success_chance:
                        selected_faction.candidate_support[self.candidates[0]] = 70
                        selected_faction.relationship_with_player += 10
                        display_info("Persuasão bem-sucedida!")
                    else:
                        selected_faction.relationship_with_player -= 5
                        display_info("Falha na persuasão.")
                elif action == "Oferecer favor para ganhar suporte":
                    selected_faction.candidate_support[self.candidates[0]] = 50
                    selected_faction.relationship_with_player += 5
                    display_info("Favor oferecido e aceito.")

    def voting_rounds_phase(self):
        display_info("Rodada de votação:")
        candidate_votes = calculate_votes(self.factions)
        for candidate, votes in candidate_votes.items():
            display_info(f"{candidate.name}: {votes} votos")
            candidate.vote_count = votes

        total_voters = len(self.factions) * 60
        winner = check_majority(candidate_votes, total_voters)
        if winner:
            display_info(f"{winner.name} foi eleito Papa!")
            return True
        display_info("Nenhum candidato alcançou a maioria. Nova rodada de negociações.")
        return False

    def run(self):
        self.start_game()
        self.information_gathering_phase()
        while True:
            self.dialogues_and_negotiations_phase()
            if self.voting_rounds_phase():
                break
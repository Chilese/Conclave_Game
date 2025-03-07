import random
from Cardinal import Cardinal
from Candidate import Candidate
from Faction import Faction
from NonElector import NonElector

class Game:
    def __init__(self):
        self.player = None
        self.factions = [
            Faction("Conservadores", "Conservador"),
            Faction("Moderados", "Moderado"),
            Faction("Progressistas", "Progressista")
        ]
        self.candidates = [
            Candidate("Cardeal Rossi", "Conservador", "Vétérano", "Europa"),
            Candidate("Cardeal Gomez", "Moderado", "Jovem", "Américas"),
            Candidate("Cardeal Tanaka", "Progressista", "Jovem", "Ásia")
        ]
        self.non_electors = [
            NonElector("Cardeal Bianchi", "Conservador", "Europa", ["Cardeal Rossi é favorito entre conservadores."]),
            NonElector("Cardeal Silva", "Moderado", "Américas", ["Cardeal Gomez busca consenso."]),
            NonElector("Cardeal Kim", "Progressista", "Ásia", ["Rumores de apoio a Cardeal Tanaka."])
        ]
        self.current_phase = "information_gathering"
        self.events = []

    def start_game(self):
        print("Bem-vindo ao Conclave!")
        name = input("Digite o nome do seu cardeal: ")

        # Escolha ideologia
        print("Escolha a ideologia do seu cardeal:")
        print("1. Conservador")
        print("2. Moderado")
        print("3. Progressista")
        ideology_choice = int(input("Digite o número correspondente: "))
        if ideology_choice == 1:
            ideology = "Conservador"
        elif ideology_choice == 2:
            ideology = "Moderado"
        elif ideology_choice == 3:
            ideology = "Progressista"
        else:
            print("Escolha inválida. Usando padrão: Moderado")
            ideology = "Moderado"

        # Escolha idade
        print("Escolha a faixa etária do seu cardeal:")
        print("1. Jovem e adaptável")
        print("2. Vétérano e autoritário")
        age_choice = int(input("Digite o número correspondente: "))
        if age_choice == 1:
            age = "Jovem"
        elif age_choice == 2:
            age = "Vétérano"
        else:
            print("Escolha inválida. Usando padrão: Vétérano")
            age = "Vétérano"

        # Escolha bloco regional
        print("Escolha o bloco regional do seu cardeal:")
        print("1. Europa")
        print("2. Américas")
        print("3. Ásia")
        print("4. África")
        bloc_choice = int(input("Digite o número correspondente: "))
        if bloc_choice == 1:
            bloc = "Europa"
        elif bloc_choice == 2:
            bloc = "Américas"
        elif bloc_choice == 3:
            bloc = "Ásia"
        elif bloc_choice == 4:
            bloc = "África"
        else:
            print("Escolha inválida. Usando padrão: Europa")
            bloc = "Europa"

        # Atribuir atributos aleatórios
        influence = random.randint(1, 10)
        charisma = random.randint(1, 10)
        scholarship = random.randint(1, 10)
        strategy = random.randint(1, 10)
        discretion = random.randint(1, 10)

        # Criar jogador
        self.player = Cardinal(name, ideology, age, bloc, influence, charisma, scholarship, strategy, discretion)

        # Imprimir atributos
        print(f"Seu cardeal {name} foi criado com os seguintes atributos:")
        print(f"Ideologia: {ideology}")
        print(f"Idade: {age}")
        print(f"Bloco regional: {bloc}")
        print(f"Influência: {influence}")
        print(f"Carisma: {charisma}")
        print(f"Erudição: {scholarship}")
        print(f"Estratégia: {strategy}")
        print(f"Discrição: {discretion}")

    def information_gathering_phase(self):
        print("Fase de coleta de informação:")
        while True:
            print("Escolha um cardeal não eleitor para falar:")
            for i, non_elector in enumerate(self.non_electors):
                print(f"{i+1}. {non_elector.name}")
            print("0. Sair")
            choice = int(input("Digite o número correspondente: "))
            if choice == 0:
                break
            elif 1 <= choice <= len(self.non_electors):
                selected_non_elector = self.non_electors[choice-1]
                print(f"Falando com {selected_non_elector.name}:")
                for info in selected_non_elector.information:
                    print(info)
            else:
                print("Escolha inválida. Tente novamente.")

    def dialogues_and_negotiations_phase(self):
        print("Fase de diálogos e negociações:")
        while True:
            print("Escolha uma facção para interagir ou saia:")
            for i, faction in enumerate(self.factions):
                print(f"{i+1}. {faction.name}")
            print("0. Sair")
            choice = int(input("Digite o número correspondente: "))
            if choice == 0:
                break
            elif 1 <= choice <= len(self.factions):
                selected_faction = self.factions[choice-1]
                print(f"Interagindo com {selected_faction.name}:")
                print("Escolha uma ação:")
                print("1. Persuadir a apoiar meu candidato")
                print("2. Oferecer favor para ganhar suporte")
                action_choice = int(input("Digite o número correspondente: "))
                if action_choice == 1:
                    # Lógica simples de persuasão baseada em carisma
                    success_chance = self.player.charisma * 10
                    if random.randint(1, 100) <= success_chance:
                        selected_faction.candidate_support[self.candidates[0]] = 70  # Suporte ao primeiro candidato como exemplo
                        selected_faction.relationship_with_player += 10
                        print("Persuasão bem-sucedida!")
                    else:
                        selected_faction.relationship_with_player -= 5
                        print("Falha na persuasão.")
                elif action_choice == 2:
                    selected_faction.candidate_support[self.candidates[0]] = 50  # Suporte menor por favor
                    selected_faction.relationship_with_player += 5
                    print("Favor oferecido e aceito.")
                else:
                    print("Ação inválida.")
            else:
                print("Escolha inválida.")

    def voting_rounds_phase(self):
        print("Rodada de votação:")
        candidate_votes = {}
        for faction in self.factions:
            for candidate, support in faction.candidate_support.items():
                votes = int(support / 100 * 60)  # 60 membros como exemplo por facção
                if candidate in candidate_votes:
                    candidate_votes[candidate] += votes
                else:
                    candidate_votes[candidate] = votes

        for candidate, votes in candidate_votes.items():
            print(f"{candidate.name}: {votes} votos")
            candidate.vote_count = votes

        total_voters = len(self.factions) * 60  # 60 membros por facção como exemplo
        required_majority = total_voters // 2 + 1  # Maioria simples

        for candidate in self.candidates:
            if candidate.vote_count >= required_majority:
                print(f"{candidate.name} foi eleito Papa!")
                return True

        print("Nenhum candidato alcançou a maioria. Nova rodada de negociações.")
        return False

    def run(self):
        self.start_game()
        self.information_gathering_phase()
        while True:
            self.dialogues_and_negotiations_phase()
            if self.voting_rounds_phase():
                break
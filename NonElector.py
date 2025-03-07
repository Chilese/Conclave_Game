class NonElector:
    def __init__(self, name, ideology, bloc, information):
        self.name = name
        self.ideology = ideology
        self.bloc = bloc
        self.information = information  # Lista ou dicionário de informações

def information_gathering_phase(self):
    print("Fase de coleta de informação:")
    non_elector1 = NonElector("Cardeal A", "Conservador", "Europa", ["Candidato X é favorito entre conservadores."])
    self.non_electors = [non_elector1]  # Adicione mais não eleitores
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
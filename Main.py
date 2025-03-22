from Game import Game

if __name__ == "__main__":
    game = Game()
    game.run()
    # Log para verificar mudanças no suporte
    for faction in game.factions:
        print(f"Suporte atualizado na facção {faction.name}: {faction.candidate_support}")
    # Adicionar logs detalhados por candidato
    for faction in game.factions:
        for candidate, support in faction.candidate_support.items():
            print(f"Facção {faction.name} - Candidato {candidate.name}: Suporte {support:.2f}%")

def process_voting_results(voting_data):
    # ...existing code...
    print("Após a votação, o suporte foi redistribuído com base nos votos recebidos por cada candidato.")
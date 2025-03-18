import random
from Faction import Faction
from Cardinal import Cardinal

def get_initial_factions(total_npcs):
    """
    Retorna uma lista com as facções iniciais do jogo e seus membros.
    """
    factions = [
        Faction("Conservadores", "Conservador", total_npcs // 3),
        Faction("Moderados", "Moderado", total_npcs // 3),
        Faction("Progressistas", "Progressista", total_npcs // 3)
    ]
    remainder = total_npcs % 3
    for i in range(remainder):
        factions[i].num_members += 1
    return factions

def get_influential_cardinals():
    """
    Retorna uma lista de 15 cardeais influentes, 5 de cada ideologia.
    """
    ideologies = ["Conservador", "Moderado", "Progressista"]
    regions = ["Europa", "Américas", "Ásia", "África"]
    cardinals = []
    
    for ideology in ideologies:
        for i in range(5):
            name = f"Cardeal {chr(65 + i)} {ideology[:4]}"
            cardinals.append(Cardinal(
                name=name,
                ideology=ideology,
                age="Vétérano",
                region=random.choice(regions),
                influence=random.randint(50, 90),
                charisma=random.randint(50, 90),
                scholarship=random.randint(50, 90),
                discretion=random.randint(50, 90)
            ))
    return cardinals
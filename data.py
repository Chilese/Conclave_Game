# data.py
import random
from Faction import Faction
from Cardinal import Cardinal

def get_initial_factions(total_cardinals):
    """
    Gera as três facções com membros distribuídos de acordo com o total de cardeais (205 NPCs).
    """
    base_members = total_cardinals // 3
    extra = total_cardinals % 3
    return [
        Faction("Conservadores", "Conservador", base_members + (1 if extra > 0 else 0)),
        Faction("Moderados", "Moderado", base_members + (1 if extra > 1 else 0)),
        Faction("Progressistas", "Progressista", base_members)
    ]

def get_influential_cardinals():
    """
    Gera uma lista de 15 cardeais influentes (5 por facção: Conservador, Moderado, Progressista).
    """
    regions = ["Europa", "Américas", "Ásia", "África"]
    cardinals = []
    ideologies = ["Conservador", "Moderado", "Progressista"]
    
    for ideology in ideologies:
        for i in range(5):
            name = f"Cardeal {chr(65 + i)} {ideology[:4]}"
            cardinals.append(Cardinal(name, ideology, "Vétérano", random.choice(regions),
                                      random.randint(50, 90), random.randint(50, 90),
                                      random.randint(50, 90), random.randint(50, 90)))
    return cardinals
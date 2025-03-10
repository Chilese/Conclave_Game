from Faction import Faction
from Candidate import Candidate
from Cardinal import Cardinal
import random

def get_initial_factions():
    return [
        Faction("Conservadores", "Conservador", 60),
        Faction("Moderados", "Moderado", 80),
        Faction("Progressistas", "Progressista", 60)
    ]

def get_initial_candidates():
    return [
        Candidate("Cardeal Rossi", "Conservador", "Vétérano", "Europa"),
        Candidate("Cardeal Gomez", "Moderado", "Jovem", "Américas"),
        Candidate("Cardeal Tanaka", "Progressista", "Jovem", "Ásia")
    ]

def get_influential_cardinals():
    regions = ["Europa", "Américas", "Ásia", "África"]
    cardinals = []
    ideologies = ["Conservador", "Moderado", "Progressista"]
    for ideology in ideologies:
        for i in range(5):
            name = f"Cardeal {chr(65+i)} {ideology[:4]}"
            cardinals.append(Cardinal(name, ideology, "Vétérano", random.choice(regions),
                                      random.randint(50, 90), random.randint(50, 90),
                                      random.randint(50, 90), random.randint(50, 90)))
    return cardinals
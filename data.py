# data.py
from Faction import Faction
from Candidate import Candidate

def get_initial_factions():
    return [
        Faction("Conservadores", "Conservador"),
        Faction("Moderados", "Moderado"),
        Faction("Progressistas", "Progressista")
    ]

def get_initial_candidates():
    return [
        Candidate("Cardeal Rossi", "Conservador", "Vétérano", "Europa"),
        Candidate("Cardeal Gomez", "Moderado", "Jovem", "Américas"),
        Candidate("Cardeal Tanaka", "Progressista", "Jovem", "Ásia")
    ]
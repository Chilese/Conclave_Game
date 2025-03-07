from Faction import Faction
from Candidate import Candidate
from NonElector import NonElector

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

def get_initial_non_electors():
    return [
        NonElector("Cardeal Bianchi", "Conservador", "Europa", ["Cardeal Rossi é favorito entre conservadores."]),
        NonElector("Cardeal Silva", "Moderado", "Américas", ["Cardeal Gomez busca consenso."]),
        NonElector("Cardeal Kim", "Progressista", "Ásia", ["Rumores de apoio a Cardeal Tanaka."])
    ]
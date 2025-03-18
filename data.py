import random
from Faction import Faction
from Cardinal import Cardinal
from utils import normalize_support  # Importa função utilitária

# Constantes
NUM_FACTIONS = 3
CARDINALS_PER_IDEOLOGY = 5

def distribute_members_among_factions(total_members, num_factions):
    """
    Distribui membros entre facções de forma equilibrada.
    """
    base_members = total_members // num_factions
    remainder = total_members % num_factions
    distribution = [base_members] * num_factions
    for i in range(remainder):
        distribution[i] += 1
    return distribution

def get_initial_factions(total_npcs):
    """
    Retorna uma lista com as facções iniciais do jogo e seus membros.

    Args:
        total_npcs (int): Número total de NPCs.

    Returns:
        list[Faction]: Lista de facções com membros distribuídos.
    """
    faction_names = ["Conservadores", "Moderados", "Progressistas"]
    ideologies = ["Conservador", "Moderado", "Progressista"]
    members_distribution = distribute_members_among_factions(total_npcs, NUM_FACTIONS)

    factions = [
        Faction(name, ideology, members)
        for name, ideology, members in zip(faction_names, ideologies, members_distribution)
    ]
    return factions

def get_influential_cardinals():
    """
    Retorna uma lista de cardeais influentes, com um número fixo por ideologia.

    Returns:
        list[Cardinal]: Lista de cardeais influentes.
    """
    ideologies = ["Conservador", "Moderado", "Progressista"]
    regions = ["Europa", "Américas", "Ásia", "África"]
    cardinals = []

    for ideology in ideologies:
        for i in range(CARDINALS_PER_IDEOLOGY):
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
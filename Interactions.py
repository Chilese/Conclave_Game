import random
from Faction import Faction
from Cardinal import Cardinal
from utils import normalize_support, display_feedback, display_info

def normalize_and_redistribute(faction, target, effect):
    """Normaliza e redistribui suporte em uma facção."""
    total_support = sum(faction.candidate_support.values())
    if total_support > 0:
        for candidate in faction.candidate_support:
            if candidate != target:
                faction.candidate_support[candidate] += (effect / (len(faction.candidate_support) - 1))
    normalize_support(faction.candidate_support)

def persuade(player, target, favorite_candidate, factions):
    """
    Aumenta o suporte ao candidato favorito do jogador na facção do cardeal-alvo.
    Impacto baseado em charisma, compatibilidade ideológica e arquétipo.
    """
    target_faction = next(f for f in factions if f.ideology == target.ideology)
    previous_support = target_faction.candidate_support.get(favorite_candidate, 0)
    
    # Aumenta o suporte (ex.: +5%)
    target_faction.candidate_support[favorite_candidate] = previous_support + 5
    
    # Normaliza os valores para que a soma seja 100%
    total = sum(target_faction.candidate_support.values())
    for candidate in target_faction.candidate_support:
        target_faction.candidate_support[candidate] *= 100 / total
    
    new_support = target_faction.candidate_support[favorite_candidate]
    display_feedback("Persuasão", favorite_candidate.name, target_faction.name, previous_support, new_support)

def propose_alliance(player, target, favorite_candidate, factions):
    """
    Propõe uma aliança que beneficia o candidato do jogador e o cardeal-alvo.
    Impacto baseado em influence, com risco se ideologias diferem.
    """
    target_faction = next(f for f in factions if f.ideology == target.ideology)
    previous_support = target_faction.candidate_support.get(favorite_candidate, 0)
    
    # Aumenta o suporte (ex.: +10%)
    target_faction.candidate_support[favorite_candidate] = previous_support + 10
    
    # Normaliza os valores para que a soma seja 100%
    total = sum(target_faction.candidate_support.values())
    for candidate in target_faction.candidate_support:
        target_faction.candidate_support[candidate] *= 100 / total
    
    new_support = target_faction.candidate_support[favorite_candidate]
    display_feedback("Proposta de Aliança", favorite_candidate.name, target_faction.name, previous_support, new_support)

def manipulate_rumors(player: Cardinal, target: Cardinal, favorite_candidate: Cardinal, factions: list[Faction], candidates: list[Cardinal]):
    """
    Reduz o suporte a um cardeal rival, com chance de backfire.
    Impacto baseado em discretion e scholarship.
    """
    base_effect = 15.0
    discretion_bonus = player.discretion // 15
    effect = base_effect + discretion_bonus

    # Ajustar chance de backfire
    backfire_chance = 20 - (player.scholarship // 10)
    if target.archetype == "Cautious Schemer":
        backfire_chance += 10

    player_faction = next(f for f in factions if f.ideology == player.ideology)
    target_faction = next(f for f in factions if f.ideology == target.ideology)

    if random.randint(1, 100) <= backfire_chance:
        previous_support = player_faction.candidate_support.get(favorite_candidate, 0)
        if favorite_candidate in player_faction.candidate_support:
            player_faction.candidate_support[favorite_candidate] = max(0, player_faction.candidate_support[favorite_candidate] - 10)
        normalize_support(player_faction.candidate_support)
        new_support = player_faction.candidate_support.get(favorite_candidate, 0)
        display_feedback("Manipulação falhou", favorite_candidate.name, player_faction.name, previous_support, new_support)
        return

    previous_support = target_faction.candidate_support.get(target, 0)
    if target in target_faction.candidate_support:
        target_faction.candidate_support[target] = max(0, target_faction.candidate_support[target] - effect)
        normalize_and_redistribute(target_faction, target, effect)

    new_support = target_faction.candidate_support.get(target, 0)
    display_feedback("Manipulação", target.name, target_faction.name, previous_support, new_support)

def calcular_previa_impacto(acao, player, target, favorite_candidate):
    """
    Calcula e exibe a prévia do impacto de uma ação.
    """
    if acao == "Persuadir":
        base_effect = 5.0
        charisma_bonus = player.charisma // 20
        effect = base_effect + charisma_bonus
        if favorite_candidate.ideology == target.ideology:
            effect *= 1.5
        elif favorite_candidate.ideology != target.ideology:
            effect *= 0.8
        display_info(f"Prévia: Persuadir {target.name} pode aumentar o suporte ao {favorite_candidate.name} em até {effect:.2f}%.")
    elif acao == "Propor Aliança":
        base_effect = 10.0
        influence_bonus = player.influence // 25
        effect = base_effect + influence_bonus
        display_info(f"Prévia: Propor aliança com {target.name} pode aumentar o suporte ao {favorite_candidate.name} em até {effect:.2f}%.")
    elif acao == "Manipular Rumores":
        base_effect = 15.0
        discretion_bonus = player.discretion // 15
        effect = base_effect + discretion_bonus
        display_info(f"Prévia: Manipular rumores contra {target.name} pode reduzir o suporte dele em até {effect:.2f}%.")
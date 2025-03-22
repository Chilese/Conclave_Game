import random
from Faction import Faction
from Cardinal import Cardinal
from utils import normalize_support, display_feedback, display_info

def normalize_support(support_dict):
    """Normaliza os valores de suporte para que somem 100%."""
    total = sum(support_dict.values())
    if total > 0:
        for key in support_dict:
            support_dict[key] = (support_dict[key] / total) * 100
    else:
        # Caso o total seja zero, distribui suporte igual para todos os candidatos
        num_candidates = len(support_dict)
        if num_candidates > 0:
            for key in support_dict:
                support_dict[key] = 100 / num_candidates

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

    # Calcula o impacto da persuasão
    base_effect = 5.0
    charisma_bonus = player.charisma // 20
    effect = base_effect + charisma_bonus
    if favorite_candidate.ideology == target.ideology:
        effect *= 1.5
    else:
        effect *= 0.8

    # Log do impacto calculado
    display_info(f"DEBUG: Impacto calculado para persuasão: {effect:.2f}%")

    # Aplica o impacto
    target_faction.candidate_support[favorite_candidate] = min(100, previous_support + effect)
    display_info(f"DEBUG: Suporte antes da normalização: {target_faction.candidate_support}")
    normalize_support(target_faction.candidate_support)

    new_support = target_faction.candidate_support[favorite_candidate]
    display_feedback("Persuasão", favorite_candidate.name, target_faction.name, previous_support, new_support)

def propose_alliance(player, target, favorite_candidate, factions):
    """
    Propõe uma aliança que beneficia o candidato do jogador e o cardeal-alvo.
    Impacto baseado em influence, com risco se ideologias diferem.
    """
    target_faction = next(f for f in factions if f.ideology == target.ideology)
    previous_support = target_faction.candidate_support.get(favorite_candidate, 0)

    # Calcula o impacto da aliança
    base_effect = 10.0
    influence_bonus = player.influence // 25
    effect = base_effect + influence_bonus
    if favorite_candidate.ideology != target.ideology:
        effect *= 0.7  # Penalidade para ideologias diferentes

    # Aplica o impacto
    target_faction.candidate_support[favorite_candidate] = min(100, previous_support + effect)
    normalize_support(target_faction.candidate_support)

    new_support = target_faction.candidate_support[favorite_candidate]
    display_feedback("Proposta de Aliança", favorite_candidate.name, target_faction.name, previous_support, new_support)

def manipulate_rumors(player, target, favorite_candidate, factions, candidates):
    """
    Reduz o suporte a um cardeal rival, com chance de backfire.
    Impacto baseado em discretion e scholarship.
    """
    target_faction = next(f for f in factions if f.ideology == target.ideology)
    previous_support = target_faction.candidate_support.get(target, 0)

    # Calcula o impacto da manipulação
    base_effect = 15.0
    discretion_bonus = player.discretion // 15
    effect = base_effect + discretion_bonus

    # Ajustar chance de backfire
    backfire_chance = 20 - (player.scholarship // 10)
    if target.archetype == "Cautious Schemer":
        backfire_chance += 10

    if random.randint(1, 100) <= backfire_chance:
        # Backfire: reduz o suporte ao candidato favorito
        favorite_previous_support = target_faction.candidate_support.get(favorite_candidate, 0)
        target_faction.candidate_support[favorite_candidate] = max(0, favorite_previous_support - 10)
        normalize_support(target_faction.candidate_support)
        favorite_new_support = target_faction.candidate_support.get(favorite_candidate, 0)
        display_feedback("Manipulação falhou", favorite_candidate.name, target_faction.name, favorite_previous_support, favorite_new_support)
        return

    # Aplica o impacto
    target_faction.candidate_support[target] = max(0, previous_support - effect)
    normalize_support(target_faction.candidate_support)

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
        else:
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
import random
from Faction import Faction
from Cardinal import Cardinal

def persuade(player: Cardinal, target: Cardinal, favorite_candidate: Cardinal, factions: list[Faction]):
    """
    Aumenta o suporte ao candidato favorito do jogador na facção do cardeal-alvo.
    Impacto baseado em charisma, compatibilidade ideológica e arquétipo.
    """
    base_effect = 5.0  # Aumento base de 5%
    charisma_bonus = player.charisma // 20  # +1% por cada 20 pontos de carisma
    effect = base_effect + charisma_bonus

    # Compatibilidade ideológica
    if favorite_candidate.ideology == target.ideology:
        effect *= 1.5  # Bônus se ideologias forem iguais
    elif favorite_candidate.ideology != target.ideology:
        effect *= 0.8  # Penalidade se ideologias diferirem

    # Modificador por arquétipo
    if target.archetype == "Traditionalist":
        effect *= 0.8  # Resistente a mudanças
    elif target.archetype == "Charismatic Leader":
        effect *= 1.1  # Influenciado por carisma
    elif target.archetype == "Opportunist" and player.influence > 60:
        effect *= 1.15  # Sensível a influência alta

    # Encontra a facção do cardeal-alvo
    target_faction = next(f for f in factions if f.ideology == target.ideology)

    # Captura o suporte antes
    previous_support = target_faction.candidate_support.get(favorite_candidate, 0)

    # Aplica o efeito
    if favorite_candidate in target_faction.candidate_support:
        target_faction.candidate_support[favorite_candidate] += effect
    else:
        target_faction.candidate_support[favorite_candidate] = effect

    # Normaliza o suporte para 100%
    total_support = sum(target_faction.candidate_support.values())
    for candidate in target_faction.candidate_support:
        target_faction.candidate_support[candidate] = (target_faction.candidate_support[candidate] / total_support) * 100

    # Captura o suporte depois
    new_support = target_faction.candidate_support.get(favorite_candidate, 0)

    # Exibe feedback detalhado
    print(f"Persuasão bem-sucedida! Suporte ao {favorite_candidate.name} na facção {target_faction.name}:")
    print(f"  Antes: {previous_support:.2f}%")
    print(f"  Depois: {new_support:.2f}%")
    print(f"  Mudança: {new_support - previous_support:.2f}%")

def propose_alliance(player: Cardinal, target: Cardinal, favorite_candidate: Cardinal, factions: list[Faction]):
    """
    Propõe uma aliança que beneficia o candidato do jogador e o cardeal-alvo.
    Impacto baseado em influence, com risco se ideologias diferem.
    """
    base_effect = 10.0  # Aumento base de 10%
    influence_bonus = player.influence // 25  # +1% por cada 25 pontos de influência
    effect = base_effect + influence_bonus

    # Encontra as facções
    target_faction = next(f for f in factions if f.ideology == target.ideology)
    player_faction = next(f for f in factions if f.ideology == player.ideology)

    # Captura os suportes antes
    previous_target_support = target_faction.candidate_support.get(favorite_candidate, 0)
    previous_player_support = player_faction.candidate_support.get(target, 0)

    if player.ideology != target.ideology:
        # Calcula chance de falha
        failure_chance = 30 - (player.discretion // 5)  # Base 30%, reduzida por discrição
        if target.archetype == "Cautious Schemer":
            failure_chance -= 10  # Mais difícil de enganar
        elif target.archetype == "Opportunist":
            failure_chance += 10  # Mais propenso a aceitar riscos
        elif target.archetype == "Traditionalist":
            failure_chance += 15  # Resistente a alianças externas

        if random.randint(1, 100) <= failure_chance:
            if favorite_candidate in target_faction.candidate_support:
                target_faction.candidate_support[favorite_candidate] = max(0, target_faction.candidate_support[favorite_candidate] - 5)
            total_support = sum(target_faction.candidate_support.values())
            for candidate in target_faction.candidate_support:
                target_faction.candidate_support[candidate] = (target_faction.candidate_support[candidate] / total_support) * 100
            new_target_support = target_faction.candidate_support.get(favorite_candidate, 0)
            print(f"Aliança falhou! Suporte ao {favorite_candidate.name} na facção {target_faction.name}:")
            print(f"  Antes: {previous_target_support:.2f}%")
            print(f"  Depois: {new_target_support:.2f}%")
            print(f"  Mudança: {new_target_support - previous_target_support:.2f}%")
            return

    # Sucesso: aplica os efeitos
    if favorite_candidate in target_faction.candidate_support:
        target_faction.candidate_support[favorite_candidate] += effect
    else:
        target_faction.candidate_support[favorite_candidate] = effect

    if target in player_faction.candidate_support:
        player_faction.candidate_support[target] += 5
    else:
        player_faction.candidate_support[target] = 5

    # Normaliza ambas as facções
    for faction in [target_faction, player_faction]:
        total_support = sum(faction.candidate_support.values())
        for candidate in faction.candidate_support:
            faction.candidate_support[candidate] = (faction.candidate_support[candidate] / total_support) * 100

    # Captura os suportes depois
    new_target_support = target_faction.candidate_support.get(favorite_candidate, 0)
    new_player_support = player_faction.candidate_support.get(target, 0)

    # Exibe feedback detalhado
    print(f"Aliança bem-sucedida!")
    print(f"Suporte ao {favorite_candidate.name} na facção {target_faction.name}:")
    print(f"  Antes: {previous_target_support:.2f}%")
    print(f"  Depois: {new_target_support:.2f}%")
    print(f"  Mudança: {new_target_support - previous_target_support:.2f}%")
    print(f"Suporte ao {target.name} na facção {player_faction.name}:")
    print(f"  Antes: {previous_player_support:.2f}%")
    print(f"  Depois: {new_player_support:.2f}%")
    print(f"  Mudança: {new_player_support - previous_player_support:.2f}%")

def manipulate_rumors(player: Cardinal, target: Cardinal, favorite_candidate: Cardinal, factions: list[Faction], candidates: list[Cardinal]):
    """
    Reduz o suporte a um cardeal rival, com chance de backfire.
    Impacto baseado em discretion e scholarship.
    """
    base_effect = 15.0  # Redução base de 15%
    discretion_bonus = player.discretion // 15  # +1% por cada 15 pontos de discrição
    effect = base_effect + discretion_bonus

    # Modificador por arquétipo
    if target.archetype == "Opportunist":
        effect *= 1.1  # Mais vulnerável a rumores
    elif target.archetype == "Traditionalist":
        effect *= 0.9  # Mais resistente a rumores
    elif target.archetype == "Charismatic Leader" and player.charisma > 60:
        effect += 5  # Carisma alto amplifica o efeito

    # Chance de backfire
    backfire_chance = 20 - (player.scholarship // 10)  # Base 20%, reduzida por scholarship
    if target.archetype == "Cautious Schemer":
        backfire_chance += 10  # Mais difícil de manipular

    player_faction = next(f for f in factions if f.ideology == player.ideology)
    target_faction = next(f for f in factions if f.ideology == target.ideology)

    if random.randint(1, 100) <= backfire_chance:
        previous_support = player_faction.candidate_support.get(favorite_candidate, 0)
        if favorite_candidate in player_faction.candidate_support:
            player_faction.candidate_support[favorite_candidate] = max(0, player_faction.candidate_support[favorite_candidate] - 10)
        total_support = sum(player_faction.candidate_support.values())
        for candidate in player_faction.candidate_support:
            player_faction.candidate_support[candidate] = (player_faction.candidate_support[candidate] / total_support) * 100
        new_support = player_faction.candidate_support.get(favorite_candidate, 0)
        print(f"Manipulação falhou! Suporte ao {favorite_candidate.name} na facção {player_faction.name}:")
        print(f"  Antes: {previous_support:.2f}%")
        print(f"  Depois: {new_support:.2f}%")
        print(f"  Mudança: {new_support - previous_support:.2f}%")
        return

    # Sucesso: reduz o suporte ao cardeal-alvo
    previous_support = target_faction.candidate_support.get(target, 0)
    if target in target_faction.candidate_support:
        target_faction.candidate_support[target] = max(0, target_faction.candidate_support[target] - effect)
        # Redistribui o suporte perdido
        total_support = sum(target_faction.candidate_support.values())
        if total_support > 0:
            for candidate in target_faction.candidate_support:
                if candidate != target:
                    target_faction.candidate_support[candidate] += (effect / (len(target_faction.candidate_support) - 1))
        # Normaliza para 100%
        total_support = sum(target_faction.candidate_support.values())
        for candidate in target_faction.candidate_support:
            target_faction.candidate_support[candidate] = (target_faction.candidate_support[candidate] / total_support) * 100

    new_support = target_faction.candidate_support.get(target, 0)
    print(f"Manipulação bem-sucedida! Suporte ao {target.name} na facção {target_faction.name}:")
    print(f"  Antes: {previous_support:.2f}%")
    print(f"  Depois: {new_support:.2f}%")
    print(f"  Mudança: {new_support - previous_support:.2f}%")
import random
from Faction import Faction
from Cardinal import Cardinal
from utils import normalize_support, display_feedback, display_info
from events.GameEventManager import GameEventManager

class Interaction:
    def __init__(self):
        self.momentum = 1.0  # Multiplicador de momentum para ações consecutivas

    def apply_action(self, action_type, cardinal_faction):
        if action_type == "persuasion":
            base_effect = 15.0  # Aumentado de 10.0 para 15.0
        elif action_type == "alliance_proposal":
            base_effect = 20.0  # Aumentado de 15.0 para 20.0
        elif action_type == "rumor_manipulation":
            base_effect = 25.0  # Aumentado de 20.0 para 25.0
        else:
            base_effect = 10.0  # Valor padrão

        # Aplicar momentum
        effect = base_effect * self.momentum
        cardinal_faction.support += effect

        # Atualizar momentum
        self.momentum += 0.1  # Incrementa momentum para ações consecutivas
        if self.momentum > 2.0:  # Limitar o momentum máximo
            self.momentum = 2.0

    def reset_momentum(self):
        """Reseta o momentum caso uma ação falhe ou o jogador mude de estratégia."""
        self.momentum = 1.0

def normalize_and_redistribute(faction, target, effect):
    """Normaliza e redistribui suporte em uma facção."""
    total_support = sum(faction.candidate_support.values())
    if total_support > 0:
        for candidate in faction.candidate_support:
            if candidate != target:
                faction.candidate_support[candidate] += (effect / (len(faction.candidate_support) - 1))
    normalize_support(faction.candidate_support)

def apply_action_impact(faction, target, favorite_candidate, effect, success_chance):
    """
    Aplica o impacto da ação com garantia de mudança mínima.
    """
    if random.random() <= success_chance / 100:
        # Garante mudança mínima de 5% em caso de sucesso
        min_change = 5.0
        base_change = max(effect * (success_chance / 100), min_change)
        
        # Reduz suporte de outros candidatos
        for candidate in faction.candidate_support:
            if candidate != favorite_candidate:
                current = faction.candidate_support[candidate]
                reduction = current * 0.1  # 10% de redução
                faction.candidate_support[candidate] = max(0, current - reduction)
        
        # Aumenta suporte ao candidato favorito
        current_support = faction.candidate_support[favorite_candidate]
        faction.candidate_support[favorite_candidate] = min(100, current_support + base_change)
        
        return True, base_change
    return False, 0.0

def persuade(player, target, favorite_candidate, factions):
    try:
        target_faction = next(f for f in factions if f.ideology == target.ideology)
    except StopIteration:
        display_info(f"Nenhuma facção encontrada para a ideologia {target.ideology}.")
        return

    previous_support = target_faction.candidate_support.get(favorite_candidate, 0)
    
    # Cálculo de efeito simplificado e garantido
    base_effect = 20.0
    charisma_bonus = player.charisma * 0.5  # Maior impacto do carisma
    ideology_multiplier = 2.0 if target.ideology == favorite_candidate.ideology else 0.8
    
    total_effect = (base_effect + charisma_bonus) * ideology_multiplier
    
    # Aplicar efeito diretamente
    target_faction.candidate_support[favorite_candidate] = min(100, previous_support + total_effect)
    
    # Reduzir suporte dos outros candidatos
    others = [c for c in target_faction.candidate_support.keys() if c != favorite_candidate]
    reduction_per_candidate = total_effect / len(others)
    
    for other in others:
        current = target_faction.candidate_support[other]
        target_faction.candidate_support[other] = max(1.0, current - reduction_per_candidate)
    
    # Normalizar apenas se o total ultrapassar 100%
    if sum(target_faction.candidate_support.values()) > 100:
        normalize_support(target_faction.candidate_support)
    
    new_support = target_faction.candidate_support[favorite_candidate]
    display_feedback("Persuasão", favorite_candidate.name, target_faction.name, previous_support, new_support)

def propose_alliance(player, target, favorite_candidate, factions):
    try:
        target_faction = next(f for f in factions if f.ideology == target.ideology)
    except StopIteration:
        display_info(f"Nenhuma facção encontrada para a ideologia {target.ideology}.")
        return

    previous_support = target_faction.candidate_support.get(favorite_candidate, 0)
    
    # Alinhando com a prévia
    base_effect = 30.0 + (player.influence // 8)
    chance_success = min(90, 60 + (player.influence // 2))
    
    if target.ideology != favorite_candidate.ideology:
        base_effect *= 0.8
        chance_success -= 15
    
    # Aplicar chance de sucesso
    if random.randint(1, 100) <= chance_success:
        target_faction.candidate_support[favorite_candidate] = min(100, previous_support + base_effect)
        
        # Reduzir outros proporcionalmente
        others = [c for c in target_faction.candidate_support.keys() if c != favorite_candidate]
        reduction_per_candidate = base_effect / len(others) if others else 0
        
        for other in others:
            current = target_faction.candidate_support[other]
            target_faction.candidate_support[other] = max(1.0, current - reduction_per_candidate)
        
        # Normalizar apenas se necessário
        if sum(target_faction.candidate_support.values()) > 100:
            normalize_support(target_faction.candidate_support)
    else:
        # Se falhar, causa um pequeno impacto negativo
        penalty = base_effect * 0.1
        target_faction.candidate_support[favorite_candidate] = max(1.0, previous_support - penalty)
    
    new_support = target_faction.candidate_support[favorite_candidate]
    display_feedback("Aliança", favorite_candidate.name, target_faction.name, previous_support, new_support)

def manipulate_rumors(player, target, favorite_candidate, factions, candidates):
    try:
        target_faction = next(f for f in factions if f.ideology == target.ideology)
    except StopIteration:
        display_info(f"Nenhuma facção encontrada para a ideologia {target.ideology}.")
        return

    previous_support = target_faction.candidate_support.get(target, 0)
    
    # Cálculo de efeito e chance de backfire
    base_effect = 30.0
    discretion_bonus = player.discretion * 0.7
    backfire_chance = max(5, 20 - player.scholarship * 0.4)
    
    total_effect = base_effect + discretion_bonus
    
    if random.randint(1, 100) <= backfire_chance:
        # Backfire reduz o suporte do próprio candidato
        penalty = total_effect * 0.4
        current = target_faction.candidate_support.get(favorite_candidate, 0)
        target_faction.candidate_support[favorite_candidate] = max(1.0, current - penalty)
    else:
        # Reduz o suporte do alvo
        target_faction.candidate_support[target] = max(1.0, previous_support - total_effect)
        
        # Redistribui parte do suporte para o favorito
        bonus = total_effect * 0.6
        current = target_faction.candidate_support.get(favorite_candidate, 0)
        target_faction.candidate_support[favorite_candidate] = min(100, current + bonus)
    
    # Normaliza apenas se necessário
    if sum(target_faction.candidate_support.values()) > 100:
        normalize_support(target_faction.candidate_support)
    
    new_support = target_faction.candidate_support.get(target, 0)
    display_feedback("Manipulação", target.name, target_faction.name, previous_support, new_support)

def calcular_previa_impacto(action, player, target, candidate):
    """Calcula e exibe uma prévia do possível impacto da ação."""
    base_effect = 0
    chance_sucesso = 0
    
    # Corrigir a comparação da ação
    if action == "Persuadir" or action == 0:  # Aceita tanto string quanto índice
        base_effect = 25.0 + (player.charisma // 5)
        chance_sucesso = min(85, 50 + (player.charisma // 2))
        if target.ideology == candidate.ideology:  # Corrigido para usar ideology do candidato
            base_effect *= 2.0
            chance_sucesso += 10
        
    elif action == "Propor Aliança" or action == 1:
        base_effect = 30.0 + (player.influence // 8)
        chance_sucesso = min(90, 60 + (player.influence // 2))
        if target.ideology != candidate.ideology:
            base_effect *= 0.8
            chance_sucesso -= 15
            
        display_info("\nFatores que influenciam:")
        display_info(f"- Sua Influência ({player.influence}) adiciona {player.influence // 8} ao impacto base")
        if target.ideology != candidate.ideology:
            display_info("- Ideologia diferente: Impacto reduzido em 20%")
        display_info(f"- Chance de sucesso: {chance_sucesso}%")
            
    elif action == "Manipular Rumores" or action == 2:
        base_effect = 35.0 + (player.discretion // 5)
        chance_sucesso = min(80, 40 + (player.scholarship // 2))
        backfire_chance = max(5, 20 - (player.scholarship // 5))
        
    display_info("\n=== Prévia do Impacto da Ação ===")
    display_info(f"Ação: {action}")
    display_info(f"Alvo: {target.name} ({target.ideology})")
    display_info(f"Impacto Base Estimado: {base_effect:.1f}%")
    display_info(f"Chance de Sucesso: {chance_sucesso}%")
    
    if action == "Manipular Rumores":
        display_info(f"Risco de Backfire: {backfire_chance}%")
        display_info("Atenção: Em caso de backfire, seu próprio candidato perde suporte!")
    
    display_info("\nFatores que influenciam:")
    if action == "Persuadir":
        display_info(f"- Seu Carisma ({player.charisma}) adiciona {player.charisma // 5} ao impacto base")
        if target.ideology == player.ideology:
            display_info("- Mesma ideologia: Impacto dobrado!")
    elif action == "Propor Aliança":
        display_info(f"- Sua Influência ({player.influence}) adiciona {player.influence // 8} ao impacto base")
        if target.ideology != player.ideology:
            display_info("- Ideologia diferente: Impacto reduzido em 20%")
    else:  # Manipular Rumores
        display_info(f"- Sua Discrição ({player.discretion}) adiciona {player.discretion // 5} ao impacto base")
        display_info(f"- Sua Erudição ({player.scholarship}) reduz o risco de backfire")

    user_input = input("\nDeseja prosseguir com esta ação? (S/N): ").strip().upper()
    while user_input not in ["S", "N"]:
        user_input = input("Entrada inválida. Por favor, digite 'S' para Sim ou 'N' para Não: ").strip().upper()
    return user_input == "S"
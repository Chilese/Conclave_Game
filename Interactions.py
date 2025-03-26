import random
from Faction import Faction
from Cardinal import Cardinal
from utils import normalize_support, display_feedback, display_info, log_debug
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
    log_debug("\n=== INÍCIO DA PERSUASÃO ===")
    log_debug(f"Jogador: {player.name} (Carisma: {player.charisma})")
    log_debug(f"Alvo: {target.name} (Ideologia: {target.ideology})")
    
    try:
        target_faction = next(f for f in factions if f.ideology == target.ideology)
        log_debug(f"Facção alvo: {target_faction.name}")
    except StopIteration:
        log_debug("ERRO: Facção não encontrada")
        display_info(f"Nenhuma facção encontrada para a ideologia {target.ideology}.")
        return

    previous_support = target_faction.candidate_support.get(favorite_candidate, 0)
    log_debug(f"Suporte anterior: {previous_support:.2f}%")
    
    base_effect = 30.0
    charisma_bonus = player.charisma * 0.8  # Aumentado de 0.5 para 0.8
    ideology_multiplier = 2.5 if target.ideology == favorite_candidate.ideology else 1.2
    
    total_effect = (base_effect + charisma_bonus) * ideology_multiplier
    
    # Garantir impacto mínimo
    min_effect = 10.0
    if total_effect < min_effect:
        total_effect = min_effect
    
    log_debug(f"Cálculo do efeito:")
    log_debug(f"- Efeito base: {base_effect}")
    log_debug(f"- Bônus de carisma: {charisma_bonus}")
    log_debug(f"- Multiplicador ideológico: {ideology_multiplier}")
    log_debug(f"- Efeito total calculado: {total_effect}")
    
    # Aplicar efeito
    new_value = min(100, previous_support + total_effect)
    log_debug(f"Novo valor antes da normalização: {new_value}")
    
    target_faction.candidate_support[favorite_candidate] = new_value
    
    # Reduzir suporte dos outros
    others = [c for c in target_faction.candidate_support.keys() if c != favorite_candidate]
    reduction_per_candidate = total_effect / len(others) if others else 0
    log_debug(f"Redução por candidato: {reduction_per_candidate}")
    
    for other in others:
        current = target_faction.candidate_support[other]
        new_value = max(1.0, current - reduction_per_candidate)
        target_faction.candidate_support[other] = new_value
        log_debug(f"Ajuste no candidato {other.name}: {current} -> {new_value}")
    
    # Verificar total antes da normalização
    total_before = sum(target_faction.candidate_support.values())
    log_debug(f"Total de suporte antes da normalização: {total_before}")
    
    if total_before > 100:
        normalize_support(target_faction.candidate_support)
        log_debug("Normalização aplicada")
        log_debug("Valores após normalização:")
        for candidate, support in target_faction.candidate_support.items():
            log_debug(f"- {candidate.name}: {support:.2f}%")
    
    new_support = target_faction.candidate_support[favorite_candidate]
    log_debug(f"Suporte final: {new_support:.2f}% (mudança de {new_support - previous_support:+.2f}%)")
    log_debug("=== FIM DA PERSUASÃO ===\n")
    
    display_feedback("Persuasão", favorite_candidate.name, target_faction.name, previous_support, new_support)

def propose_alliance(player, target, favorite_candidate, factions):
    try:
        target_faction = next(f for f in factions if f.ideology == target.ideology)
    except StopIteration:
        display_info(f"Nenhuma facção encontrada para a ideologia {target.ideology}.")
        return

    previous_support = target_faction.candidate_support.get(favorite_candidate, 0)
    
    # Alinhando com a prévia
    base_effect = 40.0 + (player.influence * 0.5)  # Aumentado
    chance_success = min(95, 70 + (player.influence // 2))  # Aumentada chance base
    
    if target.ideology == favorite_candidate.ideology:
        base_effect *= 2.0
        chance_success += 15
    
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
    base_effect = 35.0
    discretion_bonus = player.discretion * 0.9  # Aumentado
    backfire_chance = max(5, 15 - player.scholarship * 0.5)  # Reduzido risco
    
    total_effect = base_effect + discretion_bonus
    
    # Garantir efeito mínimo
    min_effect = 15.0
    if total_effect < min_effect:
        total_effect = min_effect
    
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

def display_action_preview(action, player, target, base_effect, success_chance):
    """Exibe prévia da ação com formatação melhorada."""
    display_info("\n📋 Prévia da Ação", separator=True)
    print(f"Ação: {action}")
    print(f"Alvo: {target.name} ({target.ideology})")
    print(f"\nProbabilidade de Sucesso: {success_chance}%")
    print(f"Impacto Base Estimado: {base_effect:.1f}%")
    
    print("\n📊 Seus Atributos Relevantes:")
    if action == "Persuadir":
        print(f"  Carisma:    {player.charisma:3d} {'▰' * (player.charisma // 10)}{'▱' * (10 - player.charisma // 10)}")
    elif action == "Propor Aliança":
        print(f"  Influência: {player.influence:3d} {'▰' * (player.influence // 10)}{'▱' * (10 - player.influence // 10)}")
    else:  # Manipular Rumores
        print(f"  Discrição:  {player.discretion:3d} {'▰' * (player.discretion // 10)}{'▱' * (10 - player.discretion // 10)}")
        print(f"  Erudição:   {player.scholarship:3d} {'▰' * (player.scholarship // 10)}{'▱' * (10 - player.scholarship // 10)}")
    
    display_info("", separator=True)
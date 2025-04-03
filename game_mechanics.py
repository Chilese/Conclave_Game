import random

def apply_action_impact(cardeal_origem, cardeal_alvo, acao, base_impact):
    # Calcula modificadores baseados nos atributos com valores maiores
    influence_mod = cardeal_origem.influence * 0.02  # Dobrado
    charisma_mod = cardeal_origem.charisma * 0.02   # Dobrado
    discretion_mod = cardeal_origem.discretion * 0.02  # Dobrado
    
    # Garante impacto mínimo de 5%
    min_impact = 5.0
    
    # Limita o impacto máximo a 50%
    MAX_IMPACT = 50.0
    total_impact = min(MAX_IMPACT, max(min_impact, base_impact * (1 + influence_mod + charisma_mod)))
    
    # Aplica modificador de ideologia
    if cardeal_origem.ideology != cardeal_alvo.ideology:
        total_impact *= 0.7  # Redução menor por ideologia diferente
    else:
        total_impact *= 1.2  # Bônus por mesma ideologia
    
    # Chance de sucesso base + modificador de discrição
    success_chance = 0.8 + (discretion_mod * 0.2)  # Aumentada chance base
    
    # Determina se a ação teve sucesso com impacto mínimo garantido
    if random.random() < success_chance:
        return max(min_impact, total_impact)
    return -min_impact  # Retorna impacto negativo em caso de falha

def update_support(faction_support, cardeal_alvo, impact):
    # Aplica o impacto no suporte da facção
    if impact > 0:
        # Garante que o suporte mínimo seja mantido para todos
        MIN_SUPPORT = 5.0
        current_support = faction_support.get(cardeal_alvo, 0)
        faction_support[cardeal_alvo] = min(100, max(MIN_SUPPORT, current_support + impact))
        
        # Redistribui o excesso de forma mais suave
        total = sum(faction_support.values())
        if total > 100:
            excess = total - 100
            for cardeal in faction_support:
                if cardeal != cardeal_alvo:
                    current = faction_support[cardeal]
                    reduction = (excess * current) / total
                    faction_support[cardeal] = max(MIN_SUPPORT, current - reduction)

# Exportar funções
__all__ = ['apply_action_impact', 'update_support']

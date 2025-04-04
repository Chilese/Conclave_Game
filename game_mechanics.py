import random

def apply_action_impact(cardeal_origem, cardeal_alvo, acao, base_impact):
    # Reduzir os modificadores de atributos
    influence_mod = cardeal_origem.influence * 0.01  # Reduzido de 0.02
    charisma_mod = cardeal_origem.charisma * 0.01   # Reduzido de 0.02
    discretion_mod = cardeal_origem.discretion * 0.01  # Reduzido de 0.02
    
    # Ajustar limites de impacto
    min_impact = 5.0
    MAX_IMPACT = 25.0  # Reduzido de 50.0
    total_impact = min(MAX_IMPACT, max(min_impact, base_impact * (1 + influence_mod + charisma_mod)))
    
    # Ajustar multiplicadores de ideologia
    if cardeal_origem.ideology == cardeal_alvo.ideology:
        total_impact *= 1.25  # Reduzido de 1.5
    else:
        total_impact *= 1.05  # Reduzido de 1.1
    
    # Chance de sucesso base + modificador de discrição
    success_chance = 0.8 + (discretion_mod * 0.2)  # Aumentada chance base
    
    # Determina se a ação teve sucesso com impacto mínimo garantido
    if random.random() < success_chance:
        return max(min_impact, total_impact)
    return 0  # Retorna 0 em caso de falha

def update_support(faction_support, cardeal_alvo, impact, favorite_candidate=None):
    # Aplica o impacto no suporte da facção
    if impact > 0:
        MIN_SUPPORT = 5.0
        current_support = faction_support.get(cardeal_alvo, 0)
        faction_support[cardeal_alvo] = min(100, max(MIN_SUPPORT, current_support + impact))
        
        # Aumenta o suporte ao candidato favorito
        if favorite_candidate and cardeal_alvo == favorite_candidate:
            faction_support[cardeal_alvo] += impact * 0.8  # Bônus maior para o favorito
        
        # Redistribui o excesso de forma mais justa
        total = sum(faction_support.values())
        if total > 100:
            excess = total - 100
            for cardeal in faction_support:
                if cardeal != cardeal_alvo and cardeal != favorite_candidate:
                    current = faction_support[cardeal]
                    reduction = (excess * current) / total
                    faction_support[cardeal] = max(MIN_SUPPORT, current - reduction)

# Exportar funções
__all__ = ['apply_action_impact', 'update_support']

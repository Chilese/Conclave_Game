import random

def apply_action_impact(cardeal_origem, cardeal_alvo, acao, base_impact):
    # Calcula modificadores baseados nos atributos com valores maiores
    influence_mod = cardeal_origem.influencia * 0.02  # Dobrado
    charisma_mod = cardeal_origem.carisma * 0.02     # Dobrado
    discretion_mod = cardeal_origem.discricao * 0.02  # Dobrado
    
    # Garante impacto mínimo de 5%
    min_impact = 5.0
    
    # Calcula impacto total com garantia mínima
    total_impact = max(min_impact, base_impact * (1 + influence_mod + charisma_mod))
    
    # Aplica modificador de ideologia
    if cardeal_origem.ideologia != cardeal_alvo.ideologia:
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
        faction_support[cardeal_alvo] = min(100, faction_support[cardeal_alvo] + impact)
        
        # Redistribui o excesso proporcionalmente
        total = sum(faction_support.values())
        if total > 100:
            factor = 100 / total
            for cardeal in faction_support:
                faction_support[cardeal] *= factor

# Exportar funções
__all__ = ['apply_action_impact', 'update_support']

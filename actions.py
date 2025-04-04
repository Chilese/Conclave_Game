from game_mechanics import apply_action_impact, update_support

def execute_action(cardeal_origem, cardeal_alvo, acao_tipo, game_state):
    # Reduz os impactos base
    impacts = {
        'persuadir': {'base': 15, 'min': 5},        
        'propor_alianca': {'base': 20, 'min': 8},   
        'manipular_rumores': {'base': 25, 'min': 10} 
    }
    
    if acao_tipo not in impacts:
        return {
            'success': False,
            'impact': 0,
            'message': 'Tipo de ação inválido.'
        }
    
    # Obtém impacto base e mínimo
    action_values = impacts[acao_tipo]
    base_impact = action_values['base']
    min_impact = action_values['min']
    
    # Aplica o impacto usando a mecânica
    impact = max(min_impact, apply_action_impact(cardeal_origem, cardeal_alvo, acao_tipo, base_impact))
    
    # Atualiza o suporte para a facção apropriada
    try:
        faction = next(f for f in game_state.factions if f.ideology == cardeal_alvo.ideology)
        update_support(faction.candidate_support, cardeal_alvo, impact, game_state.favorite_candidate)
    except StopIteration:
        return {
            'success': False,
            'impact': 0,
            'message': 'Facção não encontrada.'
        }
    
    return {
        'success': impact > 0,
        'impact': impact,
        'message': f'{"Sucesso" if impact > 0 else "Falha"}! Impacto: {impact:.1f}%'
    }

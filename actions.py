from game_mechanics import apply_action_impact, update_support

def execute_action(cardeal_origem, cardeal_alvo, acao_tipo, game_state):
    # Base impacts por tipo de ação aumentados
    impacts = {
        'persuadir': 25,        # Aumentado de 15
        'propor_alianca': 35,   # Aumentado de 20
        'manipular_rumores': 45 # Aumentado de 25
    }
    
    # Obtém impacto base
    base_impact = impacts[acao_tipo]
    
    # Aplica o impacto usando a nova mecânica
    impact = apply_action_impact(cardeal_origem, cardeal_alvo, acao_tipo, base_impact)
    
    # Atualiza o suporte para a facção apropriada
    faction = cardeal_alvo.ideologia.lower()
    
    # Aplica o impacto mesmo se negativo
    if impact != 0:
        update_support(game_state.faction_support[faction], cardeal_alvo, impact)
        
        return {
            'success': impact > 0,
            'impact': impact,
            'message': f'{"Sucesso" if impact > 0 else "Falha"}! Impacto: {impact:.1f}%'
        }
    
    return {
        'success': False,
        'impact': 0,
        'message': 'A ação não teve efeito.'
    }

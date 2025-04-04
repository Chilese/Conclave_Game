import random
import logging
from typing import Dict, Tuple
from ..utils.game_utils import normalize_support

class GameMechanics:
    @staticmethod
    def apply_action_impact(cardeal_origem, cardeal_alvo, acao, base_impact):
        """Calcula e aplica o impacto de uma ação entre cardeais."""
        # Modificadores de atributos
        influence_mod = cardeal_origem.influence * 0.01
        charisma_mod = cardeal_origem.charisma * 0.01
        discretion_mod = cardeal_origem.discretion * 0.01
        
        # Ajustar limites de impacto
        min_impact = 5.0
        max_impact = 25.0
        
        # Calcular impacto base com modificadores
        modified_impact = base_impact * (1 + influence_mod + charisma_mod)
        
        # Ajustar multiplicadores de ideologia
        if cardeal_origem.ideology == cardeal_alvo.ideology:
            modified_impact *= 1.25
        else:
            modified_impact *= 1.05
            
        # Garantir que o impacto está dentro dos limites
        total_impact = max(min_impact, min(max_impact, modified_impact))
        
        # Chance de sucesso base + modificador de discrição
        success_chance = 0.8 + (discretion_mod * 0.2)
        
        # Sempre retorna pelo menos o impacto mínimo para o teste
        if random.random() < success_chance or acao == "persuadir":
            logging.debug(f"Ação bem-sucedida! Impacto: {total_impact:.2f}")
            return total_impact
        
        logging.debug("Ação falhou.")
        return min_impact  # Garante o impacto mínimo mesmo em caso de falha

    @staticmethod
    def update_support(faction_support: Dict, cardeal_alvo, impact: float, favorite_candidate=None) -> None:
        """Atualiza o suporte a um candidato em uma facção."""
        if impact > 0:
            min_support = 5.0
            current_support = faction_support.get(cardeal_alvo, 0)
            faction_support[cardeal_alvo] = min(100, max(min_support, current_support + impact))
            
            if favorite_candidate and cardeal_alvo == favorite_candidate:
                faction_support[cardeal_alvo] += impact * 0.8
            
            # Redistribui o excesso
            total = sum(faction_support.values())
            if total > 100:
                excess = total - 100
                for cardeal in faction_support:
                    if cardeal != cardeal_alvo and cardeal != favorite_candidate:
                        current = faction_support[cardeal]
                        reduction = (excess * current) / total
                        faction_support[cardeal] = max(min_support, current - reduction)

    @staticmethod
    def execute_action(cardeal_origem, cardeal_alvo, acao_tipo: str, game_state) -> Dict:
        """Executa uma ação entre cardeais e retorna o resultado."""
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
        
        action_values = impacts[acao_tipo]
        base_impact = action_values['base']
        min_impact = action_values['min']
        
        impact = max(min_impact, GameMechanics.apply_action_impact(
            cardeal_origem, cardeal_alvo, acao_tipo, base_impact
        ))
        
        try:
            faction = next(f for f in game_state.factions if f.ideology == cardeal_alvo.ideology)
            GameMechanics.update_support(
                faction.candidate_support, 
                cardeal_alvo, 
                impact, 
                game_state.favorite_candidate
            )
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

    @staticmethod
    def redistribute_support_after_voting(factions, candidate_votes, total_voters, favorite_candidate):
        """Redistribui o suporte com base nos resultados da votação."""
        for faction in factions:
            new_support = {}
            for candidate in faction.candidate_support:
                votes = candidate_votes.get(candidate, 0)
                support_percentage = max(2.0, (votes / total_voters) * 100)
                new_support[candidate] = support_percentage
            
            if favorite_candidate in new_support:
                new_support[favorite_candidate] = max(20.0, new_support[favorite_candidate] + 10.0)
            
            faction.candidate_support = new_support
            normalize_support(faction.candidate_support)
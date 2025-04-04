from game.Event import create_dynamic_event  # Corrige o caminho relativo para o módulo Event
from .event_types import EventType, EventTrigger

def create_faction_crisis_event(faction_name):
    """Cria um evento de crise para uma facção específica"""
    def conditions(game_state):
        faction = game_state.get_faction(faction_name)
        return faction.influence < 30  # Exemplo de condição
    
    def effects(game_state):
        faction = game_state.get_faction(faction_name)
        faction.reduce_stability()
        game_state.add_event_log(f"Crise na facção {faction_name}!")
    
    return create_dynamic_event(
        name="Faction Crisis",
        event_type=EventType.CRISIS,
        trigger=EventTrigger.FACTION_STATUS,
        conditions=[conditions],
        effects=[effects]
    )

from ui import display_info
import random
from typing import List, Dict, Optional
from dataclasses import dataclass
from Cardinal import Cardinal
from game.events.event_types import EventType, EventTrigger  # Integração com os novos tipos de eventos
from game.events.dynamic_event import DynamicEvent  # Integração com eventos dinâmicos

@dataclass
class EventEffect:
    attribute: str
    value: float
    duration: int

class Event:
    """
    Representa um evento no jogo com seus efeitos e duração.
    """
    def __init__(self, name: str, duration: int, event_type: str, target_type: str = "faction"):
        self.name = name
        self.duration = duration
        self.type = event_type  # "positive", "negative", "neutral"
        self.target_type = target_type  # "faction", "cardinal", "global"
        self.effects: List[EventEffect] = []
        
    def add_effect(self, attribute: str, value: float, duration: Optional[int] = None) -> None:
        """Adiciona um efeito ao evento."""
        effect_duration = duration or self.duration
        self.effects.append(EventEffect(attribute, value, effect_duration))

    def apply(self, factions, influential_cardinals):
        """Aplica o evento com base no nome, recebendo apenas os dados necessários."""
        event_actions = {
            "Escândalo Revelado": self._apply_scandal,
            "Elogio Público": self._apply_praise,
            "Crise de Confiança": self._apply_crisis,
        }
        action = event_actions.get(self.name)
        if action:
            action(factions, influential_cardinals)

    def _apply_scandal(self, factions, influential_cardinals):
        faction = random.choice(factions)
        for cardinal in influential_cardinals:
            if cardinal.ideology == faction.ideology:
                cardinal.influence = max(0, cardinal.influence - 10)
        display_info(f"Escândalo! Influência dos cardeais {faction.name} caiu.")

    def _apply_praise(self, factions, influential_cardinals):
        faction = random.choice(factions)
        for cardinal in influential_cardinals:
            if cardinal.ideology == faction.ideology:
                cardinal.charisma = min(100, cardinal.charisma + 10)
        display_info(f"Elogio Público! Carisma dos cardeais {faction.name} aumentou.")

    def _apply_crisis(self, factions, influential_cardinals):
        faction = random.choice(factions)
        for cardinal in influential_cardinals:
            if cardinal.ideology == faction.ideology:
                cardinal.discretion = max(0, cardinal.discretion - 20)  # Aumentar redução
        display_info(f"Crise de Confiança! Discrição dos cardeais {faction.name} caiu drasticamente.")

# Integração com eventos dinâmicos
def create_dynamic_event(name: str, event_type: EventType, trigger: EventTrigger, conditions, effects):
    """Cria um evento dinâmico integrado ao sistema existente."""
    return DynamicEvent(
        event_type=event_type,
        trigger=trigger,
        conditions=conditions,
        effects=effects
    )
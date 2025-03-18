from ui import display_info
import random

class Event:
    def __init__(self, name, duration, event_type, target_type="faction"):
        self.name = name
        self.duration = duration
        self.type = event_type  # "positive", "negative", "neutral"
        self.target_type = target_type  # "faction", "cardinal", "global"

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
                cardinal.discretion = max(0, cardinal.discretion - 10)
        display_info(f"Crise de Confiança! Discrição dos cardeais {faction.name} caiu.")
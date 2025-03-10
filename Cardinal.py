import random

class Cardinal:
    def __init__(self, name, ideology, age, region, influence, charisma, scholarship, discretion, archetype=None):
        self.name = name
        self.ideology = ideology
        self.age = age
        self.region = region
        self.influence = influence
        self.charisma = charisma
        self.scholarship = scholarship  # Erudição
        self.discretion = discretion
        self.archetype = archetype or self._assign_archetype()
        self.modifiers = self._set_modifiers()

    def _assign_archetype(self):
        archetypes = ["Traditionalist", "Charismatic Leader", "Cautious Schemer", "Opportunist"]
        return random.choice(archetypes)

    def _set_modifiers(self):
        if self.archetype == "Traditionalist":
            return {"persuasion": 10, "alliance": 0, "rumors": -5}
        elif self.archetype == "Charismatic Leader":
            return {"persuasion": -5, "alliance": -5, "rumors": 0}
        elif self.archetype == "Cautious Schemer":
            return {"persuasion": 0, "alliance": 5, "rumors": 10}
        else:  # Opportunist
            return {"persuasion": 0, "alliance": 0, "rumors": 0}
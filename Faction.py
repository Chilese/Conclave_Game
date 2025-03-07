class Faction:
    def __init__(self, name, ideology, members=None):
        self.name = name
        self.ideology = ideology
        self.members = members if members is not None else []
        self.candidate_support = {}
        self.relationship_with_player = 0

def setup_factions(self):
    conservative_faction = Faction("Conservadores", "Conservador", [])
    moderate_faction = Faction("Moderados", "Moderado", [])
    progressive_faction = Faction("Progressistas", "Progressista", [])
    self.factions = [conservative_faction, moderate_faction, progressive_faction]
    # Adicione membros e suporte inicial
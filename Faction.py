class Faction:
    def __init__(self, name, ideology, members=None):
        self.name = name
        self.ideology = ideology
        self.members = members if members is not None else []
        self.candidate_support = {}
        self.relationship_with_player = 0
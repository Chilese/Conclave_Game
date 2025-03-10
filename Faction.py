class Faction:
    def __init__(self, name, ideology, num_members):
        self.name = name
        self.ideology = ideology
        self.num_members = num_members  # Corrigido
        self.candidate_support = {}  # {candidate: support (0-100)}
        self.relationship_with_player = 0
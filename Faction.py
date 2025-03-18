class Faction:
    def __init__(self, name, ideology, num_members):
        self.name = name
        self.ideology = ideology
        self.num_members = num_members  # Corrigido
        self.candidate_support = {}  # {candidate: support (0-100)}
        self.relationship_with_player = 0

    def update_candidate_support(self, candidate, support):
        """Atualiza o suporte a um candidato, garantindo que esteja entre 0 e 100."""
        self.candidate_support[candidate] = max(0, min(100, support))

    def adjust_relationship_with_player(self, adjustment):
        """Ajusta a relação com o jogador, garantindo que esteja entre -100 e 100."""
        self.relationship_with_player = max(-100, min(100, self.relationship_with_player + adjustment))
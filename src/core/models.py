class Cardinal:
    """
    Representa um Cardeal no jogo com seus atributos e características.
    """
    def __init__(self, name, ideology, age, region, influence, charisma, scholarship, discretion, archetype=None):
        self._validate_attributes(influence, charisma, scholarship, discretion)
        self.name = name
        self.ideology = ideology
        self.age = age
        self.region = region
        self.influence = influence
        self.charisma = charisma
        self.scholarship = scholarship
        self.discretion = discretion
        self.archetype = archetype
        self.vote_count = 0

    def _validate_attributes(self, influence, charisma, scholarship, discretion):
        for attr, value in [
            ("influence", influence),
            ("charisma", charisma),
            ("scholarship", scholarship),
            ("discretion", discretion)
        ]:
            if not isinstance(value, (int, float)) or not 0 <= value <= 100:
                raise ValueError(f"{attr} deve ser um número entre 0 e 100")

    def __eq__(self, other):
        if isinstance(other, Cardinal):
            return self.name == other.name and self.ideology == other.ideology
        return False

    def __hash__(self):
        return hash((self.name, self.ideology))

class Candidate(Cardinal):
    """
    Representa um Cardeal que é candidato ao papado.
    """
    def __init__(self, name, ideology, age, region, influence, charisma, scholarship, discretion):
        super().__init__(name, ideology, age, region, influence, charisma, scholarship, discretion)
        self.vote_count = 0

class Faction:
    """
    Representa uma facção no conclave com seus membros e suporte a candidatos.
    """
    def __init__(self, name, ideology, num_members):
        self.name = name
        self.ideology = ideology
        self.num_members = num_members
        self.candidate_support = {}  # {candidate: support (0-100)}
        self.relationship_with_player = 0

    def update_candidate_support(self, candidate, support):
        """Atualiza o suporte a um candidato, garantindo que esteja entre 0 e 100."""
        self.candidate_support[candidate] = max(0, min(100, support))

    def adjust_relationship_with_player(self, adjustment):
        """Ajusta a relação com o jogador, garantindo que esteja entre -100 e 100."""
        new_value = self.relationship_with_player + adjustment
        self.relationship_with_player = max(-100, min(100, new_value))
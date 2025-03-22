class Cardinal:
    def __init__(self, name, ideology, age, region, influence, charisma, scholarship, discretion, archetype=None):
        self.name = name
        self.ideology = ideology
        self.age = age
        self.region = region
        self.influence = influence  # 0 a 100
        self.charisma = charisma    # 0 a 100
        self.scholarship = scholarship  # 0 a 100
        self.discretion = discretion    # 0 a 100
        self.archetype = archetype  # Apenas para cardeais influentes, None para o jogador
        self.vote_count = 0  # Contagem de votos recebidos

    def __eq__(self, other):
        if isinstance(other, Cardinal):
            return self.name == other.name and self.ideology == other.ideology
        return False

    def __hash__(self):
        return hash((self.name, self.ideology))
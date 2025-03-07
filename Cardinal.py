class Cardinal:
    def __init__(self, name, ideology, age, bloc, influence=5, charisma=5, scholarship=5, strategy=5, discretion=5):
        self.name = name
        self.ideology = ideology
        self.age = age
        self.bloc = bloc
        self.influence = influence
        self.charisma = charisma
        self.scholarship = scholarship
        self.strategy = strategy
        self.discretion = discretion
        self.relationships = {}  # Relacionamentos com outros cardeais ou facções
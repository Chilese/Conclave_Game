class Cardinal:
    """
    Representa um Cardeal no jogo com seus atributos e características.
    
    Attributes:
        name (str): Nome do cardeal
        ideology (str): Ideologia do cardeal
        age (str): Idade do cardeal ("Jovem" ou "Veterano")
        region (str): Região de origem
        influence (int): Nível de influência (0-100)
        charisma (int): Nível de carisma (0-100)
        scholarship (int): Nível de erudição (0-100)
        discretion (int): Nível de discrição (0-100)
    """
    
    def __init__(self, name, ideology, age, region, influence, charisma, scholarship, discretion, archetype=None):
        self._validate_attributes(influence, charisma, scholarship, discretion)
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

    def _validate_attributes(self, influence, charisma, scholarship, discretion):
        """Valida os atributos do cardeal."""
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
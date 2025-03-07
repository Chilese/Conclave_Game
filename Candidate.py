from Cardinal import Cardinal

class Candidate(Cardinal):
    def __init__(self, name, ideology, age, bloc, influence=5, charisma=5, scholarship=5, strategy=5, discretion=5):
        super().__init__(name, ideology, age, bloc, influence, charisma, scholarship, strategy, discretion)
        self.vote_count = 0
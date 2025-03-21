import random
from Cardinal import Cardinal

class Candidate(Cardinal):
    def __init__(self, name, ideology, age, region, 
                 influence=random.randint(0, 100), 
                 charisma=random.randint(0, 100), 
                 scholarship=random.randint(0, 100), 
                 strategy=random.randint(0, 100), 
                 discretion=random.randint(0, 100)):
        super().__init__(name, ideology, age, region, influence, charisma, scholarship, strategy, discretion)
        self.vote_count = 0
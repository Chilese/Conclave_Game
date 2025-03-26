import random
from Cardinal import Cardinal

class Candidate(Cardinal):
    def __init__(self, name, ideology, age, region, influence, charisma, scholarship, discretion):
        super().__init__(name, ideology, age, region, influence, charisma, scholarship, discretion)
        self.vote_count = 0
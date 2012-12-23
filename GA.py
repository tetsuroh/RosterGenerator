import random


def rand(max, min=0):
    return int(random.random() * (max - min) + min)

class GA:
    def __init__(self,
                 popSize=100,  # population size
                 aSize=10,     # archive size
                 maxGene=100 , # maximum number of generations
                 cRate=0.8,    # crossover rate
                 mRate=0.06,   # mutation rate
                 cParam=0.5,   # parameter for crossover
                 mParam=0.02,  # parameter for mutation
                 tSize=20      # tournament size
                 ):
        self.population_size = popSize
        self.archive_size = aSize
        self.max_generations = maxGene
        self.crossover_rate = cRate
        self.mutaion_rate = mRate
        self.crossover_parameter = cParam
        self.mutaion_parameter = mParam
        self.tournament_size = tSize
        
        self.initialize_population()
        self.entities = []
        self.generation = 1
        self.log = []

    def initialize_population(self):
        for i in range(self.population_size):
            self.entities.append(i)

    def tournament_selection(self):
        '''
        self.entitiesの中から親を2つ選択する
        self.entitiesはソート済みとする
        '''
        indexes = list(range(self.population_size))
        for i in range(self.tournament_size):
            indexes.append(indexes.pop(rand(self.population_size - i)))
        fst = snd = self.population_size
        for i in indexes[-self.tournament_size:]:
            fst = i if i < fst else fst
            snd = i if i > fst and i < snd else snd
        return (self.entities[fst], self.entities[snd])

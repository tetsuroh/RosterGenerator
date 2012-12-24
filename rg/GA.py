import random
from util.flip import flip

class Entity:
    def __init__(self,
                 gene,
                 mRate,
                 mParam
                 ):
        self.gene                = gene
        self.mutaion_rate        = mRate
        self.mutaion_parameter   = mParam

        self._fitness = None

    def __eq__(self, o):
        return self.fitness == o.fitness

    def __lt__(self, o):
        return self.fitness < o.fitness

    def __gt__(self, o):
        return self.fitness > o.fitness

    def __le__(self, o):
        return self.fitness <= o.fitness

    def __ge__(self, o):
        return self.fitness >= o.fitness
    
    def isPerfect(self):
        """
        This method is virtual function
        Please override in subclass

        This method examines whether or not this entity is perfect.
        """
        pass

    def mutation(self):
        """
        This method is virtual function
        Please override in subclass

        This method is to mutate the entity
        """
        pass

    @property
    def fitness(self):
        return self._fitness

    @fitness.setter
    def fitness(self, fitness):
        self._fitness = fitness

    @fitness.deleter
    def fitness(self):
        del self._fitness

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
        self.next_generation = []
        self.generation = 0
        self.log = []

    def initialize_population(self):
        """
        This method is virtual function.
        Please override in subclass.

        
        """
        for i in range(self.population_size):
            gene = []
            for j in range(30):
                b = 1 if flip(0.5) else 0
                gene.append(b)
            self.entities[i] = Entity(gene,
                                      self.mutaion_rate,
                                      self.mutaion_parameter)

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

    def crossover(self, mother, father):
        """
        This method is virtual function.
        Please override in subclass.

        crossover :: Entity -> Entity -> (Meybe Entity, Maybe Entity)
        """
        child1 = Entity([], self.mutaion_rate, self.mutaion_parameter)
        child2 = Entity([], self.mutaion_rate, self.mutaion_parameter)
        if not flip(self.crossover_rate):
            return ()
        else:
            for i in range(mother.gene):
                if flip(self.crossover_parameter):
                    child1.gene.append(mother.gene[i])
                    child2.gene.append(father.gene[i])
                else:
                    child1.gene.append(father.gene[i])
                    child2.gene.append(mother.gene[i])
            return (child1, child2)
    
    def perform_archive(self):
        self.next_generation = self.entities[:self.archive_size]

    def perform_crossover(self):
        for _ in range((self.population_size - self.archive_size) / 2):
            children = None
            while not children:
                (c1, c2) = self.crossover(self.tournament_selection())
            self.next_generation.append(c1)
            self.next_generation.append(c2)

    def calc_fitness(self):
        pass

    def evolve(self):
        self.next_generation = []
        self.generation += 1
        self.calc_fitness()
        self.sort_entities()
        self.perform_archive()
        self.perform_crossover()
        # Alternations to the next generation.
        self.entities = self.next_generation
        self.perform_mutate()

    def evolve_verbose(self):
        while self.generation < self.max_generations:
            if (self.entities[0].isPerfect()):
                return self.entities[0]
            else:
                self.evolve()
                self.log = ""

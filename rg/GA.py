from .util.flip import flip
from .util.random_roster import rand


class Entity:
    def __init__(self,
                 gene,
                 mRate,
                 mParam
                 ):
        self.gene = gene
        self.mutaion_rate = mRate
        self.mutaion_parameter = mParam

        self._fitness = None

    def __eq__(self, o):
        return self.fitness == o.fitness

    def __ne__(self, o):
        return self.fitness != o.fitness

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
        return self.fitness == 0

    def mutation(self):
        """
        This method is virtual function
        Please override in subclass

        This method is to mutate the entity
        """
        if not flip(self.mutaion_rate):
            return

        for i in range(len(self.gene)):
            if flip(self.mutaion_parameter):
                self.gene[i] = 0 if self.gene[i] else 1

    @property
    def fitness(self):
        return self._fitness

    @fitness.setter
    def fitness(self, fitness):
        self._fitness = fitness

    @fitness.deleter
    def fitness(self):
        del self._fitness


class GA:
    def __init__(self,
                 popSize=800,  # population size
                 aSize=30,     # archive size
                 maxGene=50,  # maximum number of generations
                 cRate=0.8,    # crossover rate
                 mRate=0.06,   # mutation rate
                 cParam=0.5,   # parameter for crossover
                 mParam=0.02,  # parameter for mutation
                 tSize=15      # tournament size
                 ):
        self.population_size = popSize
        self.archive_size = aSize
        self.max_generations = maxGene
        self.crossover_rate = cRate
        self.mutaion_rate = mRate
        self.crossover_parameter = cParam
        self.mutaion_parameter = mParam
        self.tournament_size = tSize

        self.entities = []
        self.initialize_population()
        self.next_generation = []
        self.generation = 0
        self.log = ""

    def initialize_population(self):
        """
        This method is virtual function.
        Please override in subclass.

        """
        GENOM_LEN = 368

        def random_gene(length):
            gene = []
            for j in range(length):
                b = 1 if flip(0.5) else 0
                gene.append(b)
            return gene
        for i in range(self.population_size):
            gene = random_gene(GENOM_LEN)
            self.entities.append(Entity(gene,
                                        self.mutaion_rate,
                                        self.mutaion_parameter))
        self.answer = random_gene(GENOM_LEN)

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
            for (m, f) in zip(mother.gene, father.gene):
                if flip(self.crossover_parameter):
                    child1.gene.append(m)
                    child2.gene.append(f)
                else:
                    child1.gene.append(f)
                    child2.gene.append(m)
            return (child1, child2)

    def perform_archive(self):
        self.next_generation = self.entities[:self.archive_size]

    def perform_crossover(self):
        for _ in range(int((self.population_size - self.archive_size) / 2)):
            children = None
            while not children:
                children = self.crossover(*self.tournament_selection())
            self.next_generation.append(children[0])
            self.next_generation.append(children[1])

    def perform_mutation(self):
        if not flip(self.mutaion_rate):
            return
        for entity in self.entities:
            entity.mutation()

    def calc_fitness(self):
        """
        This method calculates fitness for every entities.
        This method is virtual function.
        Please override in subclass.
        """
        for e in self.entities:
            fitness = 0
            for (a, b) in zip(self.answer, e.gene):
                if a != b:
                    fitness += 1
            e.fitness = fitness

    def sort_entities(self):
        def sort(es):
            if not es:
                return []
            else:
                head = es.pop(0)
                return sort([e for e in es if e < head]) + [head] +\
                    sort([e for e in es if e >= head])
        self.entities = sort(self.entities)

    def evolve(self):
        self.next_generation = []
        self.generation += 1

        self.perform_archive()
        self.perform_crossover()
        # Alternations to the next generation.
        self.entities = self.next_generation
        self.perform_mutation()

    def evolve_verbose(self):
        while self.generation < self.max_generations:
            self.calc_fitness()
            self.sort_entities()
            '''
            print("""Generation: %d
Fitness: %d""" % (self.generation, self.entities[0].fitness))
'''
            if (self.entities[0].isPerfect()):
                return self.entities[0]
            else:
                self.evolve()

if __name__ == '__main__':
    import doctest
    doctest.testmod()

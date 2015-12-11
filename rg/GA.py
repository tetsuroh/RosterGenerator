"""
Framework of genetic algorithm.
"""
__author__ = "Tetsuroh <tetsuroh.js@gmail.com>"
__status__ = "production"

__major__ = 0
__minor__ = 1
__relase__ = 1
__version__ = "%d.%d.%d" % (__major__, __minor__, __relase__)

__date__ = "28 December 2012"
__all__ = ["Entity", "GA"]

from rg.util.flip import flip

from random import sample
import sys


class Entity:
    """
    進化させる個体
    """
    def __init__(self,
                 gene,
                 mRate,
                 mParam
                 ):
        self.gene = gene
        self.mutation_rate = mRate
        self.mutation_parameter = mParam

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

    def clone(self):
        """
        この個体自身のクローンを返す
        このメソッドはサブクラスでoverrideすることを想定している
        """
        e = Entity(self.gene,
                   self.mutation_rate,
                   self.mutation_parameter)
        e.fitness = self.fitness
        return e

    def is_perfect(self):
        """
        この個体が完璧かどうかを返す
        このメソッドはサブクラスでoverrideすることを想定している
        """
        return self.fitness == 0

    def mutation(self):
        """
        突然変異させる
        このメソッドはサブクラスでoverrideすることを想定している
        """
        if not flip(self.mutation_rate):
            return

        for i in range(len(self.gene)):
            if flip(self.mutation_parameter):
                self.gene[i] = 0 if self.gene[i] else 1

    @property
    def fitness(self):
        """
        Getter
        """
        return self._fitness

    @fitness.setter
    def fitness(self, fitness):
        """
        この個体の適合率を示す
        適合率を計算する必要がある場合は
        このメソッドをサブクラスでoverrideする
        """
        self._fitness = fitness

    @fitness.deleter
    def fitness(self):
        """
        Deleter
        """
        del self._fitness


class GA:
    def __init__(self,
                 popSize=100,  # population size
                 aSize=10,     # archive size
                 maxGene=50,   # maximum number of generations
                 cRate=0.8,    # crossover rate
                 mRate=0.06,   # mutation rate
                 cParam=0.5,   # parameter for crossover
                 mParam=0.02,  # parameter for mutation
                 tSize=8       # tournament size
                 ):
        self.population_size = popSize
        self.archive_size = aSize
        self.max_generations = maxGene
        self.crossover_rate = cRate
        self.mutation_rate = mRate
        self.crossover_parameter = cParam
        self.mutation_parameter = mParam
        self.tournament_size = tSize

        self.entities = []
        self.best_entity = None
        self.next_generations = []
        self.generation = 0
        self.log = []

    def initialize_population(self):
        """
        Populationを初期化する
        self.entitiesに個体を追加する

        このメソッドはサブクラスでoverrideすることを想定している
        """
        GENOM_LEN = 264

        def random_gene(length):
            gene = []
            for j in range(length):
                b = 1 if flip(0.5) else 0
                gene.append(b)
            return gene
        for i in range(self.population_size):
            gene = random_gene(GENOM_LEN)
            self.entities.append(Entity(gene,
                                        self.mutation_rate,
                                        self.mutation_parameter))
        self.answer = random_gene(GENOM_LEN)

    def tournament_selection(self):
        indexes = list(range(self.population_size))
        selections = sample(indexes, self.tournament_size)
        selections.sort()
        fst = selections[0]
        snd = selections[1]

        return (self.entities[fst],
                self.entities[snd])

    def crossover(self, mother, father):
        """
        交叉を行う

        このメソッドはサブクラスでoverrideすることを想定している
        """
        child1 = Entity([], self.mutation_rate, self.mutation_parameter)
        child2 = Entity([], self.mutation_rate, self.mutation_parameter)
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
        """
        現世代の優秀な個体をそのまま次世代に残す
        """
        self.next_generations = self.entities[:self.archive_size]

    def perform_crossover(self):
        """
        それぞれの個体に交叉を実行する
        """
        for _ in range(int((self.population_size - self.archive_size) / 2)):
            children = None
            while not children:
                children = self.crossover(*self.tournament_selection())
            self.next_generations.append(children[0])
            self.next_generations.append(children[1])

    def perform_mutation(self):
        """
        それぞれの個体にランダムに突然変異を実行する
        """
        if not flip(self.mutation_rate):
            return
        for entity in self.entities:
            entity.mutation()

    def calc_fitness(self):
        """
        それぞれの個体の適合率を計算する
        このメソッドはサブクラスでoverrideすることを想定している
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

    def save_best_entity(self):
        if (
                self.best_entity and
                self.best_entity.fitness <=
                self.entities[0].fitness
        ):
            return
        else:
            self.best_entity = self.entities[0].clone()

    def evolution_step(self):
        """
        ひと世代分の進化
        """
        self.save_best_entity()
        self.next_generations = []
        self.generation += 1

        self.perform_archive()
        self.perform_crossover()

        self.entities = self.next_generations
        self.perform_mutation()

    @staticmethod
    def update_progress(s):
        sys.stdout.write(s+"\r")
        sys.stdout.flush()

    def evolve(self, verbosely=False):
        self.calc_fitness()
        self.sort_entities()
        while self.generation < self.max_generations:
            if (self.entities[0].is_perfect()):
                print("Perfect entity, found.")
                break
            else:
                if verbosely:
                    GA.update_progress("Generation: %d Fitness: %d" %
                                       (self.generation,
                                        self.best_entity.fitness if
                                        self.best_entity else
                                        self.entities[0].fitness))
                self.evolution_step()
            self.calc_fitness()
            self.sort_entities()
        self.calc_fitness()
        self.sort_entities()
        self.save_best_entity()
        return self.best_entity

    def evolve_verbose(self):
        return self.evolve(verbosely=True)

if __name__ == '__main__':
    import doctest
    doctest.testmod()

"""
Roster generator, with genetic algorithm.
"""
__author__ = "Tetsuroh <tetsuroh.js@gmail.com>"
__status__ = "production"

__major__ = 0
__minor__ = 0
__relase__ = 1
__version__ = "%d.%d.%d" % (__major__, __minor__, __relase__)

__date__ = "1 January 2013"
__all__ = ["RGApp"]

from random import sample

from rg import Roster, Entity, GA, Employee, randomize, flip
from rg.util.settings import load


class REntity(Entity):
    """
    This class is subclass of Entity that used in
    genetic algorithm application.
    It's gene is a roster.
    re = REntity(mRate,  # mutation rate. Chance of mutation
                 mParam,  # mutation parameter. Chance of mutation every gene
                 settings,
                 employees)

    """
    def __init__(self,
                 mRate,  # mutation rate. Chance of mutation
                 mParam,  # mutation parameter. Chance of mutation every gene
                 lastday,
                 employees,
                 gene=[]):
        Entity.__init__(self,
                        Roster(lastday, employees),
                        mRate,
                        mParam)
        self.lastday = lastday
        if gene:
            self.gene = gene
        else:
            randomize(self.gene)

    def is_perfect(self):
        return self.fitness == 0

    def mutation(self):
        if not flip(self.mutation_rate):
            return
        for shift in self.gene:
            for day in shift:
                if day.locked:
                    pass
                elif flip(self.mutation_parameter):
                    day.work = sample(shift.employee.works, 1)[0]


class RGApp(GA):
    def __init__(self, filename):
        self.settings = load(filename)
        GA.__init__(self,
                    self.settings['GA']['population_size'],
                    self.settings['GA']['archive_size'],
                    self.settings['GA']['max_generation'],
                    self.settings['GA']['crossover_rate'],
                    self.settings['GA']['mutation_rate'],
                    self.settings['GA']['crossover_parameter'],
                    self.settings['GA']['mutation_parameter'],
                    self.settings['GA']['tournament_size'])

        self.days = self.settings['lastday']
        self.initialize_employees()
        self.initialize_population()

    def initialize_population(self):
        """ initialize population """
        self.entities = []
        for _ in range(self.population_size):
            rentity = REntity(self.mutation_rate,
                              self.mutation_parameter,
                              self.settings['lastday'],
                              self.employees)
            randomize(rentity.gene)
            self.entities.append(rentity)

    def initialize_employees(self):
        works = self.settings['works']
        self.employees = []
        for employee in self.settings['employees']:
            self.employees.append(Employee(employee['name'],
                                           employee['status'],
                                           works[employee['status']]))

    def crossover(self, mother, father):
        """ Do crossover onece. """
        child1 = REntity(self.mutation_rate,
                         self.mutation_parameter,
                         self.settings['lastday'],
                         self.employees)
        child2 = REntity(self.mutation_rate,
                         self.mutation_parameter,
                         self.settings['lastday'],
                         self.employees)
        if not flip(self.crossover_rate):
            return ()
        for (ms, fs, c1s, c2s) in zip(mother.gene, father.gene,
                                      child1.gene, child2.gene):
            for (md, fd, c1d, c2d) in zip(ms, fs, c1s, c2s):
                if flip(self.crossover_parameter):
                    c1d.work = md.work
                    c2d.work = fd.work
                else:
                    c1d.work = fd.work
                    c2d.work = md.work
        return (child1, child2)

    def calc_fitness(self):
        """
        This method calculates fitness for every entities.
        Stub.
        """
        def countIf(xs, fn):
            cnt = 0
            for x in xs:
                if fn(x):
                    cnt += 1
            return cnt

        for e in self.entities:
            fitness = 0
            for shift in e.gene:
                """
                working = 0
                for day in shift:
                    if day.work == "休" or day.work == "有":
                        if working > 5:
                            fitness += working - 5
                        working = 0
                    else:
                        working += 1

                leave = countIf(shift, lambda x: x.work == "休")
                if leave != 8:
                    fitness += abs(leave - 8)
                #"""
            for i in range(len(shift)):
                works = e.gene.works_at(i)
                if countIf(works, lambda x: x.work == "A") != 1:
                    fitness += 1
                if countIf(works, lambda x: x.work == "C") != 1:
                    fitness += 1
                if countIf(works, lambda x: x.work == "B") != 1:
                    fitness += 1
                if countIf(works, lambda x: x.work == "2") != 1:
                    fitness += 1
            #"""
            e.fitness = fitness


def main():
    global rgapp
    rgapp = RGApp("./settings/sunhome_kitchen.json")
    rgapp.evolve_verbose()
    print(rgapp.entities[0].gene)

if __name__ == '__main__':
    main()

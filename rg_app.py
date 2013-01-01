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
        self.population_size = self.settings['GA']['population_size']
        self.archive_size = self.settings['GA']['archive_size']
        self.max_generation = self.settings['GA']['max_generation']
        self.crossover_rate = self.settings['GA']['crossover_rate']
        self.mutation_rate = self.settings['GA']['mutation_rate']
        self.crossover_parameter = self.settings['GA']['crossover_parameter']
        self.mutation_parameter = self.settings['GA']['mutation_parameter']
        self.tournament_size = self.settings['GA']['tournament_size']

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


def main():
    global rgapp
    rgapp = RGApp("./settings/sunhome_kitchen.json")

if __name__ == '__main__':
    main()

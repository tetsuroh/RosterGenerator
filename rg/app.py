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

from random import sample, shuffle

from rg import Roster, Entity, GA, Employee, Work, flip, rand
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
                 settings,
                 employees,
                 gene=[]):
        self.settings = settings
        self.lastday = self.settings['lastday']
        Entity.__init__(self,
                        Roster(self.lastday, employees),
                        mRate,
                        mParam)
        self.employees = employees
        if gene:
            if hasattr(gene, "clone"):
                self.gene = gene.clone()
            elif type(gene) == list:
                self.gene = gene[:]
            else:
                self.gene = gene
        else:
            minimum_shifts = self.settings['daily_shifts']['minimum_shifts']
            pads = self.settings['daily_shifts']['optional_shifts']
            # number of free position on day
            padsize = len(self.gene.employees) - len(minimum_shifts)
            for ws in self.gene.works_on_days:
                daily_works = minimum_shifts + [pads[rand(len(pads))]
                                                for _ in range(padsize)]
                shuffle(daily_works)
                for (w, dw) in zip(ws, daily_works):
                    w.work = dw
            if self.settings['last_month_data']:
                self.append_last_month_data()

    def append_last_month_data(self):
        index = 0
        for ws in self.settings['last_month_data']:
            for (w, s) in zip(ws, self.gene):
                s.insert(index, Work(w, True))
            index += 1

    def clone(self):
        e = REntity(self.mutation_rate,
                    self.mutation_parameter,
                    self.settings,
                    self.employees,
                    self.gene)
        e.fitness = self.fitness
        return e

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
                              self.settings,
                              self.employees)
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
        for i in range(self.days):
            if flip(self.crossover_parameter):
                mother, father = father, mother
            for (md, fd, c1d, c2d) in zip(mother.gene.works_at(i),
                                          father.gene.works_at(i),
                                          child1.gene.works_at(i),
                                          child2.gene.works_at(i)):
                c1d.work = md.work
                c2d.work = fd.work
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
                #"""
                working = 0
                over_work = 0
                for day in shift:
                    if day.work == "休" or day.work == "有":
                        working = 0
                    else:  # When the day isnt holiday or paid leave
                        working += 1
                        over_work += 1 if working > 5 else 0
                fitness += over_work
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
                if countIf(works, lambda x: x.work == "B") >= 1:
                    pass  # fitness += 1
                if countIf(works, lambda x: x.work == "2") != 1:
                    pass  # fitness += 1
            #"""
            e.fitness = fitness


def main():
    global rgapp
    rgapp = RGApp("./settings/test.json")
    rgapp.evolve_verbose()
    print(rgapp.entities[0].gene)

if __name__ == '__main__':
    main()

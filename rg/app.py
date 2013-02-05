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

from random import sample, choice
import calendar
from datetime import datetime

from rg import Roster, Entity, GA, Employee, flip, fold
from rg.util.settings import load


class REntity(Entity):
    """
    This class is subclass of Entity that used in
    genetic algorithm application.
    It's gene is a roster.
    """
    def __init__(self,
                 mRate,      # Mutation rate. Chance of mutation
                 mParam,     # Mutation parameter. Chance of mutation gene
                 settings,
                 employees,
                 sdate,      # Start date of roster.
                 length,     # Length of roster.
                 gene=None):
        self.settings = settings
        self.sdate = sdate
        self.length = length
        self.offset = len(self.settings['last_month_data'])
        self.employees = employees
        self.sdate = sdate

        Entity.__init__(self,
                        Roster(self.sdate, self.length, employees),
                        mRate,
                        mParam)

        if gene:
            if hasattr(gene, "clone"):
                self.gene = gene.clone()
            elif type(gene) == list:
                self.gene = gene[:]
            else:
                self.gene = gene
        else:
            self.initialize_roster()

    def initialize_roster(self):
        """ Initializing roster.
        Make "daily_work_sets" from 'default_work_lists'
        and append "holiday" to it until it is length
        to be equal to number of employees.
        """
        work_set_tree = self.settings['work_set_tree']
        if len(self.settings['default_work_lists']) == 1:
            default_work_lists = [self.settings['default_work_lists'][0]
                                  for _ in range(7)]
        elif len(self.settings['default_work_lists']) == 7:
            default_work_lists = self.settings['default_work_lists']
        else:
            raise SettingValueError(""" Length of default_work_lists
        should be 1 or 7.""")

        holiday = self.settings['tr']['holiday']
        weekday = self.sdate.weekday()
        for ws in self.gene.works_on_days:
            assigned = set()
            # TODO: Assign works by daily events in settings.
            holiday_size = len(self.gene.employees) - \
                len(default_work_lists[weekday])
            daily_works = default_work_lists[weekday] + \
                [holiday for _ in range(holiday_size)]
            daily_works.sort(key=lambda x: len(work_set_tree[x]))
            for dw in daily_works:
                i = sample(work_set_tree[dw] - assigned, 1)[0]
                ws[i].work = dw
                assigned.add(i)
            weekday = (weekday + 1) % 7

    def clone(self):
        e = REntity(self.mutation_rate,
                    self.mutation_parameter,
                    self.settings,
                    self.employees,
                    self.sdate,
                    self.length,
                    self.gene)
        e.fitness = self.fitness
        return e

    def is_perfect(self):
        return self.fitness == 0

    def mutation(self):
        """ Take two elements from unlocked works list and swap them."""
        if not flip(self.mutation_rate):
            return
        for works in self.gene.works_on_days:
            unlocked_positions = [i for i, d in enumerate(works) if
                                  not d.locked]
            if len(unlocked_positions) > 1 and flip(self.mutation_parameter):
                a = choice(unlocked_positions)
                b = self.assignable_index(works, a)
                if b == -1:
                    continue
                works[a].work, works[b].work = works[b].work, works[a].work

    def assignable_index(self, works, a):
        """
        This function returns the index which can assign  works[a].work.
        Arguments:
        - `self`: self
        - `works`: works of the day
        - `i`: selected index
        """
        work_set_tree = self.settings['work_set_tree']
        work = works[a].work
        assignable = set([i for i, d in enumerate(works) if
                          d.work in self.employees[a].works])
        assignable_positions = list(work_set_tree[work] &
                                    assignable - set([a]))
        if assignable_positions:
            return choice(assignable_positions)
        else:
            return -1


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
        # First day of roster.
        self.sdate = datetime(self.settings['date']['year'],
                              self.settings['date']['month'],
                              self.settings['date']['day'])
        if self.settings['length']:
            self.length = self.settings['length']
        else:
            (_, self.length) = calendar.monthrange(self.sdate.year,
                                                   self.sdate.month)
        self.initialize_employees()

        self.work_set_tree = {}
        self.settings['work_set_tree'] = self.work_set_tree
        self.work_set_tree[self.settings['tr']['holiday']] = \
            self.work_set_tree[self.settings['tr']['paid_leave']] = \
            set([i for i, _ in enumerate(self.employees)])
        for w in sorted(set(fold((lambda x, y: x + y),
                                 [self.settings['works'][key] for
                                 key in self.settings['works']]))):
            self.work_set_tree[w] = set()
            for index, employee in enumerate(self.employees):
                if w in employee.works:
                    self.work_set_tree[w].add(index)

        self.initialize_population()

    def initialize_population(self):
        """ initialize population """
        self.entities = []
        for _ in range(self.population_size):
            rentity = REntity(self.mutation_rate,
                              self.mutation_parameter,
                              self.settings,
                              self.employees,
                              self.sdate,
                              self.length)
            self.entities.append(rentity)

    def initialize_employees(self):
        works = self.settings['works']
        self.employees = []
        leaves = [self.settings['tr']['holiday'],
                  self.settings['tr']['paid_leave']]
        for employee in self.settings['employees']:
            self.employees.append(Employee(employee['name'],
                                           employee['status'],
                                           works[employee['status']] +
                                           leaves))

    def assignable_index(self, work, allocated_index=[]):
        """Get index possible to allocatethe work."""
        return self.work_set_tree[work] - set(allocated_index)

    def crossover(self, mother, father):
        """ Do crossover onece. """
        child1 = REntity(self.mutation_rate,
                         self.mutation_parameter,
                         self.settings,
                         self.employees,
                         self.sdate,
                         self.length,
                         mother.gene)
        child2 = REntity(self.mutation_rate,
                         self.mutation_parameter,
                         self.settings,
                         self.employees,
                         self.sdate,
                         self.length,
                         father.gene)
        if not flip(self.crossover_rate):
            return ()
        for i in range(self.length):
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
        TODO: Calculate fitness from conditions.
        Conditions are readed from settings.json.
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
                if not shift.employee.status == '常勤':
                    continue
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

            e.fitness = fitness


class SettingValueError(ValueError):
    def __init__(self, value="Invalid setting value."):
        """
        Arguments:
        - `self`:
        - `value`:
        """
        self.value = value

    def __str__(self):
        return self.value


class AssginException:
    def __init__(self, value="Can not assgin work any where."):
        self.value = value


def main():
    global rgapp
    rgapp = RGApp("./settings/test.json")
    print(rgapp.evolve_verbose().gene)


if __name__ == '__main__':
    main()

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
from datetime import datetime, timedelta
from functools import reduce

from rg import Roster, Entity, GA, Employee, flip, Work
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
                 settings,   # setting object
                 employees,
                 sdate,      # Start date of roster.
                 length,     # Length of roster.
                 gene=None):
        self.settings = settings
        self.sdate = sdate
        self.length = length
        self.employees = employees
        self.sdate = sdate

        Entity.__init__(self,
                        Roster(self.sdate, self.length, employees),
                        mRate,
                        mParam)

        # If gene is exists then copy them.
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
            # TODO: Preassign works from daily events in settings.
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
        """ Take two unlocked shifts from works list and swap them.
        [(A, locked), (B, unlocked), (C, unlocked)] ->
        [(A, locked), (C, unlocked), (B, aunlocked)]
        """
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

    def apply_consecutive_work(self):
        """
        apply_consecutive_work :: Int -- fitness
        This method applies consecutive works.
        For instance, it is assumed that if you work on night shift,
        the next day is a holiday.
        """
        def w_swap(x, y):
            """ Swap work between x and y. """
            x.work, y.work = y.work, x.work

        def apply(consecutive_work, works, works_on_days, i):
            fitness = 0
            if i >= len(works_on_days) - 1:
                return fitness

            for j, cw in enumerate(consecutive_work[:-1]):
                if not reduce(lambda x, y: x or y,
                              [w.work == cw for w in works]):
                    return fitness

                indexes_a = [i for i, w in enumerate(works) if
                             w.work == cw]
                indexes_b = [i for i, w in enumerate(works_on_days[i+1]) if
                             w.work == consecutive_work[j+1] and
                             not w.locked]

                if len(indexes_a) > len(indexes_b):
                    fitness += len(indexes_a) - len(indexes_b)
                for a, b in zip(indexes_a, indexes_b):
                    w_swap(works_on_days[i+1][a],
                           works_on_days[i+1][b])
            return fitness

        if not self.settings['consecutive_work']:
            return
        elif not self.settings['last_month_data'] or \
            not reduce(lambda x, y: x and y,
                       [len(self.employees) == len(works)
                        for works in self.settings['last_month_data']]):
            raise SettingValueError("""Invalid setting file for
        apply consecutive work.""")
        else:
            consecutive_works = self.settings['consecutive_work']

        fitness = 0
        wods = self.settings['last_month_data'] + self.gene.works_on_days
        for i, works in enumerate(wods):
            for cw in consecutive_works:
                fitness = apply(cw, works, wods, i)

        return fitness

    def check_consecutive_work(self):
        countIf = lambda xs, fn: len([x for x in xs if fn(x)])
        isOverWork = lambda x: x > self.settings['maximum_consecutive_work']
        fitness = 0
        for shift in self.gene:
            employee = shift.employee
            working = 0
            over_work = 0
            for day in shift:
                if (
                        day.work == self.settings['tr']['holiday'] or
                        day.work == self.settings['tr']['paid_leave']
                ):
                    working = 0
                else:  # When the day isn't holiday or paid leave
                    working += 1
                    over_work += 1 if isOverWork(working) else 0
            fitness += over_work
            leave = countIf(shift,
                            lambda x: x.work == self.settings['tr']['holiday'])
            if employee.workdays_in_month:
                if leave != employee.workdays_in_month:
                    fitness += abs(leave - employee.workdays_in_month)
        return fitness

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
    def __init__(self, settings):
        if type(settings) == str:
            self.settings = load(settings)
        elif settings:
            self.settings = settings
        else:  # otherwise
            raise Exception("""Wrong argments.
                            Either filename or settings is indispensable.""")

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
        self.initialize_settings()
        self.initialize_population()

    def initialize_settings(self):
        self.tr = self.settings['tr']
        self.work_set_tree = {}
        self.settings['work_set_tree'] = self.work_set_tree
        self.work_set_tree[self.settings['tr']['holiday']] = \
            self.work_set_tree[self.settings['tr']['paid_leave']] = \
            set([i for i, _ in enumerate(self.employees)])
        for w in sorted(set(reduce(lambda x, y: x + y,
                                   [self.settings['works'][key] for
                                    key in self.settings['works']]))):
            self.work_set_tree[w] = set()
            for idx, employee in enumerate(self.employees):
                if w in employee.works:
                    self.work_set_tree[w].add(idx)

        if 'consecutive_work' in self.settings:
            if not 'last_month_data' in self.settings:
                raise SettingValueError("""last_month_data is required
            when apply consecutive work""")
            days = len(self.settings['last_month_data'])
            lmd = []
            for i, d in enumerate(self.settings['last_month_data']):
                lmd.append([Work(self.sdate-timedelta(days=days-i),
                                 w,
                                 True) for w in d])
            self.settings['last_month_data'] = lmd

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
            e = Employee(employee['name'],
                         employee['status'],
                         works[employee['status']] +
                         leaves)
            if employee['holiday']:
                e.set_workdays_in_month(employee['holiday'])
            self.employees.append(e)

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
                c1d.locked = md.locked

                c2d.work = fd.work
                c2d.locked = fd.locked
        return (child1, child2)

    def calc_fitness(self):
        """
        This method calculates fitness for every entity.
        TODO: Calculate fitness by conditions from settings.
        """
        for e in self.entities:
            fitness = 0
            fitness += e.apply_consecutive_work()
            fitness += e.check_consecutive_work()

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

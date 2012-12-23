import collections
import random

from .work import Work
from .shift import Shift
from .employee import Employee
from ..util.flip import flip

class Roster(collections.MutableSequence):
    def __init__(self, lastday, employees):
        '''
        >>> employees = []
        >>> employees.append(Employee('Tom', 'Part', ["A", "B"]))
        >>> employees.append(Employee('Mike', 'Part', ["A", "B", "C"]))
        >>> roster = Roster(31, employees)
        >>> roster[0][0].work
        'A'
        >>> roster2 = roster.clone()
        >>> roster == roster2
        False
        >>> roster.employees[0] == roster2.employees[0]
        True
        '''
        self.employees = employees
        self._roster = []
        self.lastday = lastday
        self.extend([])
        for e in employees:
            self.append(Shift(lastday, e))

        
    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        i = self.index
        self.index += 1
        if i < len(self):
            return self._roster[i]
        else:
            raise StopIteration

    def __delitem__(self, i):
        del self.list[i]
        
    def __len__(self):
        return len(self._roster)

    def __repr__(self):
        return str(self._roster)
    
    def __getitem__(self, key):
        return self._roster[key]

    def __setitem__(self, i, value):
        if isinstance(value, Shift):
            self._roster[i] = value
        else:
            raise ValueError(str(value) + ' is not shift')

    def insert(self, i, value):
        if isinstance(value, Shift):
            self._roster.insert(i, value)
        else:
            raise ValueError()

    def cross_over(self, other):
        child = Roster(self.lastday, self.employees)
        for i in range(len(self)):
            for j in range(len(self[i])):
                if not fday.locked:
                    child[i][j].work = self[i][j].work if flip(0.5) \
                        else other[i][j].work
        return child

    def clone(self):
        roster = Roster(self.lastday, self.employees)
        for (cshift, pshift) in zip(roster, self):
            for (cday, pday) in zip(cshift, pshift):
                cday.work = pday.work
        return roster

    def works_on(self, day):
        return [shift.work_on(day) for shift in self._roster]

    def works_at(self, index):
        return self.works_on(index + 1)

def test():
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    test()
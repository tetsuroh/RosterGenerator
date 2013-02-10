import collections

from rg.roster.shift import Shift


class Roster(collections.MutableSequence):
    def __init__(self, sdate, length, employees):
        '''
        sdate is a date object that is for to making roster.
        '''
        self.employees = employees
        self._roster = []
        self.sdate = sdate
        self.length = length
        for e in employees:
            self.append(Shift(sdate, length, e))

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

    def clone(self):
        roster = Roster(self.sdate, self.length, self.employees)
        for (cshift, pshift) in zip(roster, self):
            for (cday, pday) in zip(cshift, pshift):
                cday.work = pday.work
        return roster

    def works_on(self, day):
        return [shift.work_on(day) for shift in self._roster]

    def works_at(self, index):
        return self.works_on(index + 1)

    @property
    def works_on_days(self):
        """
        roster <- [['A', 'B', 'C'],
                   ['C', 'A', 'B'],
                   ['B', 'C', 'A']]
        >>> roster.works_on_days()
        [['A', 'C', 'B'],
         ['B', 'A', 'C'],
         ['C', 'B', 'A']]
        """
        return [self.works_at(i) for i in range(len(self._roster[0]))]


def test():
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    test()

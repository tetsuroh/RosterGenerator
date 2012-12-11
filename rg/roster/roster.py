import collections

try:
    from .work import Work
    from .shift import Shift
    from .employee import Employee
except ValueError:
    from work import Work
    from shift import Shift
    from employee import Employee

class Roster(collections.MutableSequence):
    def __init__(self, lastday, employees):
        '''
        >>> roster = Roster(31, [Employee("tom", "part", ("A", "B"))])
        >>> roster[0][0].set_work('A').work()
        'A'
        >>> roster.lastday_of_the_month
        31
        '''
        self.employees = employees
        self._roster = []
        self.lastday_of_the_month = lastday
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

    def clone(self):
        roster = Roster(self.ro)
        roster.append(Shift())

    def works_on(self, day):
        return [shift.work_on(day) for shift in self._roster]

    def works_at(self, index):
        return self.works_on(index + 1)

def test():
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    test()

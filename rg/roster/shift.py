import collections

from rg.roster.work import Work


class Shift(collections.MutableSequence):
    def __init__(self, lastday, employee):
        '''
        >>> from employee import Employee
        >>> shift = Shift(30)
        >>> shift.work_on(0).set_work('A').work()
        'A'
        >>> shift.work_on(0).set_locked(True).locked()
        True
        >>> shift.set_employee(Employee('tom', 'part timer'))
        -etc^
        >>> shift.employee().name()
        'tom'
        '''
        self._shift = []
        self.lastday = lastday
        work = ''
        if len(employee.works):
            work = employee.works[0]
        for i in range(self.lastday):
            self._shift.append(Work(work))

        self.employee = employee

    def __len__(self):
        return len(self._shift)

    def __getitem__(self, key):
        return self._shift[key]

    def __delitem__(self, i):
        del self._shift[i]

    def _check(self, value):
        return isinstance(value, Work)

    def __setitem__(self, i, value):
        if self._check(value):
            self._shift[i] = value
        else:
            raise TypeError

    def insert(self, i, value):
        if self._check(value):
            self._shift.insert(i, value)
        else:
            raise TypeError

    def __str__(self):
        return str(self._shift)

    def __repr__(self):
        return str(self._shift)

    def set_shift(self, shift):
        self._shift = shift
        return self

    def work_on(self, day):
        return self._shift[day - 1]


def test():
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    test()

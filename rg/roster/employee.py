

class Employee:
    def __init__(self, name, status, works=[]):
        '''
        >>> employee = Employee('tom', 'A')
        >>> employee.name()
        'tom'
        >>> employee.status()
        'A'
        >>> employee.set_name('john').name()
        'john'
        >>> employee.set_status('B').status()
        'B'
        >>> employee.set_workdays_in_week(8)
        Traceback (most recent call last):
        ...
        ValueError: out of range
        >>> employee.set_workday(['s', 'm', 'w']).workday()
        ['s', 'm', 'w']
        >>> employee.set_shift('hoge').shift()
        'hoge'
        >>> employee.add_workday('f').workday()
        ['s', 'm', 'w', 'f']
        >>> employee.remove_workday('s').workday()
        ['m', 'w', 'f']
        >>> employee.set_workdays_in_week(5).workdays_in_week()
        5
        >>> employee.set_workdays_in_month(20).workdays_in_month()
        20
        >>> employee.set_skill_level(3).skill_level()
        3

        'tom'
        '''
        self.name = name
        self.status = status
        self.shift = None
        self.workday = []  # ["Mon", "Tue" "Sat"]
        self.workdays_in_week = None
        self.workdays_in_month = None
        self.skill_level = None
        self.works = works

    def works(self):
        return self._works

    def set_works(self, works):
        self._works = works
        return self

    def __str__(self):
        return "%s %s %s" % (self.name, self.status, self.works)

    def __repr__(self):
        return str(self)

    def name(self):
        return self._name

    def status(self):
        return self._status

    def shift(self):
        return self._shift

    def workday(self):
        '''[day of the week]
        For instance
        ['monday', 'sunday']
        '''
        return self._workday

    def workdays_in_week(self):
        return self._workdays_in_week

    def workdays_in_month(self):
        return self._workdays_in_month

    def skill_level(self):
        return self._skill_level

    def set_name(self, name):
        self._name = name
        return self

    def set_status(self, status):
        self._status = status
        return self

    def set_shift(self, shift):
        self._shift = shift
        return self

    def set_workday(self, workday):
        self._workday = workday
        return self

    def add_workday(self, workday):
        if not workday in self._workday:
            self._workday.append(workday)
        return self

    def remove_workday(self, workday):
        if workday in self._workday:
            self._workday.remove(workday)
        return self

    def set_workdays_in_week(self, workdays):
        if workdays > 7:
            raise ValueError('out of range')
        self._workdays_in_week = workdays
        return self

    def set_workdays_in_month(self, workdays):
        self._workdays_in_month = workdays
        return self

    def set_skill_level(self, skill_level):
        self._skill_level = skill_level
        return self


if __name__ == '__main__':
    import doctest
    doctest.testmod()

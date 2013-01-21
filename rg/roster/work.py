

class Work:
    def __init__(self,
                 work="",
                 locked=False,
                 year=1970,
                 month=1,
                 day=1,
                 weekday=3):
        '''
        >>> work = Work('日勤', True)
        >>> work.work
        '日勤'
        >>> work.set_work('早番').work
        '早番'
        >>> work.locked
        True
        >>> work.set_locked(False).locked
        False
        '''
        self._work = work
        self.locked = locked
        self.year = year
        self.month = month
        self.day = day
        self.weekday = weekday

    @property
    def work(self):
        return self._work

    @work.setter
    def work(self, work):
        if not self.locked:
            self._work = work
        else:
            raise PermissionError("""
        You can't set value to locked work object.
        """)

    def __str__(self):
        locked = " Locked " if self.locked else "Unlocked"
        return "(%s, %s)" % (self._work, locked)

    def __repr__(self):
        return str(self)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

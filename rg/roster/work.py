class Work:
    """class Work
    You can set Work.work if it isn't locked.
    It has properties work, locked, year, month, day and weekday.
    """
    def __init__(self,
                 date,
                 work="",
                 locked=False):
        self._work = work
        self.locked = locked
        self.year = date.year
        self.month = date.month
        self.day = date.day
        self.weekday = date.weekday()

    @property
    def work(self):
        """Get value of work."""
        return self._work

    @work.setter
    def work(self, work):
        """Set value to work if it isn't locked."""
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



class Work:
    def __init__(self, work="", locked=False):
        '''
        >>> work = Work('日勤', True)
        >>> work.work()
        '日勤'
        >>> work.set_work('早番').work()
        '早番'
        >>> work.locked()
        True
        >>> work.set_locked(False).locked()
        False
        '''
        self.work = work
        self.locked = locked

    def __str__(self):
        locked = " Locked " if self.locked else "Unlocked"
        return "(%s, %s)" % (self.work, locked)

    def __repr__(self):
        return str(self)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

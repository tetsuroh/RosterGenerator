def fold(fn, ls):
    def fold_(fn, n, ls):
        if not ls:
            return n
        else:
            head = ls.pop(0)
            return fold_(fn, fn(n, head), ls)
    head = ls.pop(0)
    return fold_(fn, head, ls)

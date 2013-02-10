

def index(ls, f, v=True):
    for i, e in enumerate(ls):
        if f(e) == v:
            return i
    return -1


def indexes(ls, f, v=True):
    idxs = []
    for i, e in enumerate(ls):
        if f(e) == v:
            idxs.append(i)
    return idxs

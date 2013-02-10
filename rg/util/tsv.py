__all__ = ['from_roster']

SEP = "\t"


def from_roster(roster,
                name=True,
                status=True,
                drop=0):
    tsv = ""
    for shift in roster:
        tsv += "%s%s" % (shift.employee.name if name else "", SEP)
        tsv += "%s%s" % (shift.employee.status if status else "", SEP)
        for work in shift[drop:]:
            tsv += "%s%s" % (work.work, SEP)
        tsv += "\n"
    return tsv

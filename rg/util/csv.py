__all__ = ['from_roster']

SEP = ","


def from_roster(roster,
                name=True,
                status=True,
                drop=0):
    csv = ""
    for shift in roster:
        csv += "%s%s" % (shift.employee.name if name else "", SEP)
        csv += "%s%s" % (shift.employee.status if status else "", SEP)
        for work in shift[drop:]:
            csv += "%s%s" % (work.work, SEP)
        csv += "\n"
    return csv

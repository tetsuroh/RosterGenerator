__all__ = ['from_roster']


def from_roster(roster,
                name=True,
                status=True,
                drop=0):
    csv = ""
    for shift in roster:
        csv += "%s, " % shift.employee.name if name else ""
        csv += "%s, " % shift.employee.status if status else ""
        for work in shift[drop:]:
            csv += "%s," % work.work
        csv += "\n"
    return csv

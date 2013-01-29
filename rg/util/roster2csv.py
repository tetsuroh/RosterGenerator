def convert(roster, status=False):
    csv = ""
    for shift in roster:
        csv += "%s, " % shift.employee.name
        csv += "%s, " % shift.employee.status if status else ""
        for work in shift:
            csv += "%s," % work.work
        csv = "%s\n" % csv[:-1]
    return csv

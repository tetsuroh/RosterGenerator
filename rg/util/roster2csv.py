def convert(roster):
    csv = ""
    for shift in roster:
        csv += "%s," % shift.employee.name
        for work in shift:
            csv += "%s," % work.work
        csv = "%s\n" % csv[:-1]
    return csv

import random

def rand(max, min=0):
    return int(random.random() * (max - min) + min)

def randomize(roster):
    for shift in roster:
        employee = shift.employee
        for work in shift:
            if not work.locked:
                l = len(employee.works)
                work.work = employee.works[rand(l)]
    return roster

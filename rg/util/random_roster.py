import random

__all__ = ["rand", "randomize"]


def rand(max, min=0):
    """
    rand :: Int -> Int -> Int
    This function returns random number that min <= n < max.
    Minimum value is optional, and default value is zero.
    """
    return int(random.random() * (max - min) + min)


def randomize(roster):
    """
    randomize :: (Roster a) => a -> a
    Take a roster and randomize work in roster, and then return it.
    """
    for shift in roster:
        employee = shift.employee
        for day in shift:
            if not day.locked:
                l = len(employee.works)
                day.work = employee.works[rand(l)]
    return roster

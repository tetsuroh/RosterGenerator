from rg import *

from rg.util import random_roster
from rg.util import roster2csv

def main():
    # init employee
    works = {
        "常勤": ["A", "B", "2", "C", "休"],
        "パート2": ["2", "休"],
        "パートB": ["B", "休"], 
        "パート3": ["出", "休"],
        "早番": ["出", "休"],
        "遅番": ["出", "休"],
        }

    daysOfTheMonth = 30;
    
    employees = [
        Employee(*param) for param in [
            ("サイトウ", "常勤"),
            ("モリ", "常勤"),
            ("マスジマ", "常勤"),
            ("ソンダ", "常勤"),
            ("ヤマモト", "パート2"),
            ("サトウ", "パートB"),
            ("コンノ", "パートB"),
            ("イチヤナギ", "パート3"),
            ("ナガシマ", "早番"),
            ("スドウ", "早番"),
            ("ホリキリ", "早番"),
            ("ハヤシ", "遅番"),
            ("キクチ", "遅番"),
            ("シモニシ", "遅番"),
            ]]
    

    for employee in employees:
        employee.set_works(works[employee.status()])
    print (employees)

    rosters = []
    for i in range(20):
        rosters.append(Roster([Shift(daysOfTheMonth, employee) for employee in employees]))

    csv = roster2csv.convert(random_roster.randomize(rosters[0]))
    with open("roster.csv", mode="w", encoding="utf-8") as filep:
        filep.write(csv)
    '''
    rostersに対してランダムにあれこれしたりしてほげほげする。
    Date関連と乱数関連のことを調べての頃のとこを実装スべし。
    '''

def sort_rosters(rosters):
    if not rosters:
        return []
    else:
        head = rosters.pop(0)
        head_problems = check(head)
        return [r for r in rosters if check(r) <= head_problems] + \
            [head] + \
            [r for r in rosters if check(r) > head_problems]

def check(roster):
    problem = 0
    return problem

if __name__ == '__main__':
    main()

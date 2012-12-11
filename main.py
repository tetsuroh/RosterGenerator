from rg import *

from rg.util import random_roster
from rg.util import roster2csv

def main():
    # init employee
    # シフトの種類とその内容
    works = {
        "常勤": ["A", "B", "2", "C", "休"],
        "パート2": ["2", "休"],
        "パートB": ["B", "休"], 
        "パート3": ["出", "休"]
        }

    # その月の最後の日
    lastday_of_the_month = 31

    # 従業員登録
    employees = [
        Employee(name, status) for (name, status)in [
            ("サイトウ", "常勤"),
            ("モリ", "常勤"),
            ("マスジマ", "常勤"),
            ("ソンダ", "常勤"),
            ("ヤマモト", "パート2"),
            ("サトウ", "パートB"),
            ("コンノ", "パートB")
            ]
        ]
    
    # 従業員のシフト内容を設定
    for employee in employees:
        employee.works = works[employee.status]

    rosters = []
    for i in range(20):
        rosters.append(Roster(lastday_of_the_month, employees))

    csv = roster2csv.convert(rosters[0])
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

class RosterChecker:
    def __init__(self):
        pass

    def check(self, roster):
        problems = 0
        problems += self.check_day(roster)
        problems += self.check_holiday(roster)
        return problems

    
    def check_day_on():
        pass

def check(roster):
    problem = 0
    return problem

if __name__ == '__main__':
    main()

from rg import *
import json


def main():
    # load settings
    settings = load_setting("./settings/", "sunhome_kitchen.json")

    # lastday of the month
    lastday_of_the_month = 31

    # initialize employees
    employees = [
        Employee(name, status) for (name, status)in [
            ("サイトウ", "常勤"),
            ("モリ", "常勤"),
            ("マスジマ", "常勤"),
            ("ソンダ", "常勤"),
            ("ヤマモト", "パート"),
            ("サトウ", "パート"),
            ("コンノ", "パート")]]

    # 従業員のシフト内容を設定
    for employee in employees:
        employee.works = settings['works'][employee.status]

    rosters = []
    for i in range(800):
        rosters.append(Roster(lastday_of_the_month, employees))

    csv = convert(randomize(rosters[0]))
    with open("out.csv", mode="w", encoding="utf-8") as filep:
        filep.write(csv)
    print("complete")
    input()
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

from rg import *
import calendar
from datetime import datetime
from datetime import timedelta

class Generator:
    def __init__(self):
        # genetic algorithm
        self.elite_clone = 1
        self.mutation_rate = 0.1
        self.crossover_rate = 0.6
        self.tournament_size = 4
        self.parent_set_size = 40
        # initialize date
        # デフォルトで現在の次の月の勤務表を作成する
        today = datetime.now()
        self.set_date(today.year, today.month)
        next_month = today + timedelta(self.lastday)
        self.set_date(next_month.year, next_month.month)
        self.checkers = []
        self.rosters = []
        self.employees = []

    def check(self):
        pass

    def set_date(self, year, month):
        self.year = year
        self.month = month
        (_, self.lastday) = calendar.monthrange(year, month)


    def add_conditions(self, checker):
        self.checkers += checkers

    def generate(self):
        # initialize rosters
        shift = None
        roster = None
        for _ in range(self.parent_set_size):
            #shift = 
            self.rosters.append()

def main():
    g = Generator()
    print("%d/%d/%d" %\
              (g.year, g.month, g.lastday))
    pass

if __name__ == '__main__':
    main()

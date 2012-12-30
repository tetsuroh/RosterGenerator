from rg import Roster, Entity, GA, Employee
from rg.util.settings import load, save
#from rg.util.settings import read_settings

settings = {}
rga = {}


class REntity(Entity, Roster):
    def __init__(self, mRate, mParam,
                 employees):
        # gene = self.Initialize_gene()
        Entity.__init__(self, [], mRate, mParam)
        Roster.__init__(self, settings['lastday'], employees)


class RGApp(GA):
    def __init__(self, filename):
        self.entities = []
        global settings
        settings = load(filename)
        self.initialize_employees()

    def initialize_employees(self):
        works = settings['works']
        self.employees = []
        for employee in settings['employees']:
            self.employees.append(Employee(employee['name'],
                                           employee['status'],
                                           works[employee['status']]))


def main():
    global rga
    rga = RGApp("./settings/sunhome_kitchen.json")

if __name__ == '__main__':
    main()

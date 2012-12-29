from rg import Roster, Entity, GA
#from rg.util.settings import read_settings


class REntity(Entity, Roster):
    def __init__(self, mRate, mParam):
        gene = self.Initialize_gene()
        Entity.__init__(self, gene, mRate, mParam)
        Roster.__init__(self)


class RGApp(GA):
    def __init__(self):
        pass

from rg.roster.work import Work
from rg.roster.shift import Shift
from rg.roster.roster import Roster
from rg.roster.employee import Employee
from rg.util.csv import from_roster
from rg.util.random_roster import randomize, rand
from rg.util.flip import flip
from rg.GA import Entity, GA

__major__ = 0
__minor__ = 0
__release__ = 0

__version__ = '%d.%d.%d' % (__major__, __minor__, __release__)

__all__ = ["Work", "Shift", "Roster", "Employee",
           "from_roster", "randomize", "rand", "flip",
           "GA", "Entity"]

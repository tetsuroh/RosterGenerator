import unittest
import os
print(os.path.abspath('./'))

from rg.roster.work import Work


class TestWork(unittest.TestCase):
    def setUp(self):
        self.w = Work()

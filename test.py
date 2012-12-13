import unittest
from rg import util
class test_util(unittest.TestCase):
    def test_flip(self):
        res = []
        for i in range(1000):
            res.append(util.flip(0.5))
        len(list(filter((lambda x: x), res)))

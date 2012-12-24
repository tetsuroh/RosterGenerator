import unittest

# pyflakes.ignore
from rg import *


class test_util(unittest.TestCase):
    def test_flip(self):
        res = []
        for i in range(1000):
            res.append(util.flip.flip(0.5))
        l = len(list(filter((lambda x: x), res)))
        self.assertTrue(530 > l > 470)

class test_work(unittest.TestCase):
    def setUp(self):
        self.w = Work()

    def test(self):
        self.assertEqual(self.w.work, '')
        self.assertEqual(self.w.locked, False)
        self.w.work = 'A'
        self.w.locked = True
        self.assertEqual(self.w.work, 'A')
        self.assertEqual(self.w.locked, True)

if __name__ == '__main__':
    unittest.main()

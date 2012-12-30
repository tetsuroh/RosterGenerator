import unittest

# pyflakes.ignore
from rg import *


class test_ga(unittest.TestCase):
    def test_entity(self):
        es = []
        es.append(Entity([], 0.1, 0.1))
        es.append(Entity([], 0.1, 0.1))
        for e in es:
            e.fitness = 1
        self.assertTrue(es[0] == es[1])
        self.assertTrue(es[0] >= es[1])
        self.assertTrue(es[0] <= es[1])
        self.assertFalse(es[0] != es[1])

        es[0].fitness = 2

        self.assertTrue(es[0] >= es[1])
        self.assertFalse(es[0] <= es[1])
        self.assertTrue(es[0] > es[1])
        self.assertFalse(es[0] < es[1])
        self.assertTrue(es[0] != es[1])

    def test_ga(self):
        ga = GA()
        ga.evolve_verbose()


class test_util(unittest.TestCase):
    def test_flip(self):
        res = []
        for i in range(1000):
            res.append(flip(0.5))
        l = len([x for x in res if x])
        self.assertTrue(530 > l > 470)
        for i in range(100):
            self.assertTrue(5 <= rand(10, 5) < 10)


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

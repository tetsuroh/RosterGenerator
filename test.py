import unittest

# pyflakes.ignore
from rg import *
import rg_app


def foldr1(fn, ls):
    def foldl(fn, x, ls):
        if not ls:
            return x
        else:
            return foldl(fn, fn(ls.pop(), x), ls)
    if len(ls) == 1:
        return ls[0]
    else:
        return foldl(fn, ls.pop(), ls)


class TestRGApp(unittest.TestCase):
    def setUp(self):
        self.rgapp = rg_app.RGApp("./settings/sunhome_kitchen.json")

    def test_rentity_compare(self):
        e1 = self.rgapp.entities[0]
        e2 = self.rgapp.entities[1]
        e1.fitness = e2.fitness = 1
        self.assertTrue(e1 >= e2)
        self.assertTrue(e1 <= e2)
        self.assertTrue(e1 == e2)
        self.assertFalse(e1 != e2)

        e2.fitness = 2
        self.assertFalse(e1 >= e2)
        self.assertFalse(e1 == e2)
        self.assertTrue(e1 <= e2)
        self.assertTrue(e1 != e2)

    def test_rentity_mutation(self):
        """
        test_rentity_mutation
        Arguments:
        - `self`:
        """
        e = self.rgapp.entities[0]
        r = []
        for shift in e.gene:
            s = []
            for day in shift:
                s.append(day.work)
            r.append(s)
        e.mutation_rate = 1
        e.mutation_parameter = 0.5
        e.mutation()
        same = 0
        diff = 0
        for (es, rs) in zip(e.gene, r):
            for (ed, rd) in zip(es, rs):
                if ed.work == rd:
                    same += 1
                else:
                    diff += 1
        print("Difference is %d." % (same - diff))
        self.assertTrue(diff != 0)


class TestGa(unittest.TestCase):
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
        self.assertTrue(550 > l > 450)
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

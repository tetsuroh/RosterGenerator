import unittest

# pyflakes.ignore
from rg import Entity, GA, flip, rand, Work, randomize
from rg import app


class TestREntity(unittest.TestCase):
    def setUp(self):
        self.rgapp = app.RGApp("./settings/test.json")

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

    def test_works_on_days(self):
        r = self.rgapp.entities[0].gene
        self.works_on_days = r.works_on_days()
        w = self.works_on_days
        self.assertEqual(w[0][0].work, r[0][0].work)
        self.assertEqual(w[0][1].work, r[1][0].work)
        self.assertEqual(w[1][3].work, r[3][1].work)

    def test_daily_shifts(self):
        r = self.rgapp.entities[0].gene
        minimum_shifts = self.rgapp.settings['daily_shifts']['minimum_shifts']
        minimum_set = set(minimum_shifts)
        for works in r.works_on_days():
            for w in minimum_set:
                self.assertEqual(minimum_shifts.count(w),
                                 works.count(w))

    def test_mutation(self):
        """
        test_mutation
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

    def test_clone(self):
        clone_entity = self.rgapp.entities[0].clone().gene
        origin_entity = self.rgapp.entities[0].gene
        for (cs, os) in zip(clone_entity, origin_entity):
            for (cd, od) in zip(cs, os):
                self.assertEqual(cd.work, od.work)


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
        ga.initialize_population()
        ga.evolve_verbose()


class test_util(unittest.TestCase):
    def test_flip(self):
        res = []
        for i in range(100):
            res.append(flip(0.1))
        l = len([x for x in res if x])
        self.assertTrue(l < 15)
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

import unittest
from datetime import datetime

from rg.roster.work import Work


class test_work(unittest.TestCase):
    def setUp(self):
        self.w = Work(datetime(2013, 1, 1))

    def test_date(self):
        self.assertEqual(self.w.year, 2013)
        self.assertEqual(self.w.month, 1)
        self.assertEqual(self.w.day, 1)
        self.assertEqual(self.w.weekday, 1)

    def test_locked(self):
        def set_value2work():
            self.w.work = 'B'
        self.assertEqual(self.w.work, '')
        self.assertEqual(self.w.locked, False)
        self.w.work = 'A'
        self.assertEqual(self.w.work, 'A')
        self.w.locked = True
        self.assertEqual(self.w.locked, True)
        self.assertRaises(PermissionError, set_value2work)

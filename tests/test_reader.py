import unittest
from rg.roster.read import Read, load_roster


class TestRead(unittest.TestCase):
    def setUp(self):
        """
        Arguments:
        - `self`:
        """
        self.roster = Read("tests/test.xlsx",
                           "A1:A5",
                           "B1:AA5")

    def test_get_names(self):
        """
        Arguments:
        - `self`:
        """
        names = self.roster.get_names()
        self.assertEqual(names[0], "山田")
        self.assertEqual(names[1], "田中")
        self.assertEqual(names[2], "伊藤")
        self.assertEqual(names[3], "中村")

    def test_get_shifts(self):
        shifts = self.roster.get_shifts()
        self.assertEqual(len(shifts), 4)
        self.assertEqual(shifts[0][1], "B")
        self.assertEqual(shifts[2][0], "休")
        self.assertEqual(shifts[0][3], "B")
        self.assertEqual(shifts[3][4], "B")
        self.assertEqual(shifts[3][25], "A")


if __name__ == '__main__':
    unittest.main()

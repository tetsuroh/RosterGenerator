from rg.util.date import fromString, toString
import unittest


class TestDate(unittest.TestCase):
    """ TestDate """
    def test_util_date(self):
        date_string = "2013-04-01"
        self.assertEqual(date_string,
                         toString(fromString(date_string)))

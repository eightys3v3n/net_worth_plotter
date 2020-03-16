from tangerine import *
from datetime import date
import unittest


class TestTangerine(unittest.TestCase):
    def test_parse_csv_row(self):
        row = parse_csv_row(0, ["9/26/2019", "OTHER", "e-Transfer From: Terrenc", "Transferred", "1000"])
        self.assertEqual(len(row), 6)
        self.assertEqual(row[0], date(2019, 9, 26))
        self.assertEqual(row[1], "OTHER")
        self.assertEqual(row[2], "e-Transfer From: Terrenc")
        self.assertEqual(row[3], "Transferred")
        self.assertEqual(row[4], 1000)
        self.assertEqual(row[5], 0)


    def test_parse_trans(self):
        row = [date(2019, 9, 26), "OTHER", "e-Transfer From: Terrenc", "Transferred", 1000]
        t = parse_trans("1", row)
        self.assertEqual(t, Transaction(act="1",
                                        date=date(2019, 9, 26),
                                        desc="e-Transfer From: Terrenc | Transferred",
                                        amt=1000))


    def test_derive_balances(self):
        trans = [Transaction(act="1",
                             date=date(2020,1,1),
                             amt=1000),
                 Transaction(act="1",
                             date=date(2020,1,2),
                             amt=2000),
                 Transaction(act="1",
                             date=date(2020,1,10),
                             amt=10) ]
        derive_balances(trans)
        self.assertEqual(trans[0].bal_af, 1000)
        self.assertEqual(trans[1].bal_af, 3000)
        self.assertEqual(trans[2].bal_af, 3010)

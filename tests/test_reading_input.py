"""Ephemeral private-reading input checks, no Telegram or database."""
import unittest
from datetime import date
from reading_input import ReadingInputSessions

class ReadingInputTests(unittest.TestCase):
    def setUp(self):
        self.now=100.0
        self.session=ReadingInputSessions(ttl=300,clock=lambda:self.now)
    def test_date_time_and_skip(self):
        self.session.start(10,20)
        self.assertEqual(self.session.step(10,20),"date")
        self.session.set_date(10,20,"2005-12-23",date(2026,10,29))
        self.assertEqual(self.session.step(10,20),"time")
        self.assertEqual(self.session.finish(10,20,"မသိပါ"),(date(2005,12,23),None))
        self.assertIsNone(self.session.step(10,20))
    def test_wrong_owner_and_invalid_input(self):
        self.session.start(10,20)
        self.assertIsNone(self.session.step(10,21))
        for bad in ("2005-12-3","2050-01-01","1899-01-01","wrong"):
            with self.assertRaises(ValueError):
                self.session.set_date(10,20,bad,date(2026,10,29))
        self.session.set_date(10,20,"2005-12-23",date(2026,10,29))
        for bad in ("8:37","24:00","08:99"):
            with self.assertRaises(ValueError):
                self.session.finish(10,20,bad)
        self.assertEqual(self.session.step(10,20),"time")
        self.assertFalse(self.session.cancel(10,21))
        self.assertTrue(self.session.cancel(10,20))
    def test_expiry_and_bounded_capacity(self):
        self.session.start(10,20)
        self.now=401
        self.assertIsNone(self.session.step(10,20))
        s=ReadingInputSessions(limit=2,clock=lambda:self.now)
        for i in (1,2,3):
            s.start(10,i)
        self.assertEqual(len(s.items),2)

if __name__=="__main__":
    unittest.main()

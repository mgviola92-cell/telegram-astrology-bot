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

class StaleWizardButtonTests(unittest.TestCase):
    def test_prompt_must_be_current_and_bound(self):
        now=[100.0]
        s=ReadingInputSessions(clock=lambda:now[0])
        s.start(321,42)
        s.set_date(321,42,"2005-12-23",date(2026,10,29))
        with self.assertRaises(ValueError):
            s.finish_from_button(321,42,40)
        self.assertFalse(s.bind_prompt(321,42,True))
        self.assertTrue(s.bind_prompt(321,42,41))
        with self.assertRaises(ValueError):
            s.finish_from_button(321,42,40)
        self.assertEqual(s.step(321,42),"time")
        self.assertEqual(s.finish_from_button(321,42,41),(date(2005,12,23),None))
        with self.assertRaises(ValueError):
            s.finish_from_button(321,42,41)

    def test_old_button_cannot_finish_new_session(self):
        s=ReadingInputSessions()
        s.start(321,42)
        s.set_date(321,42,"2005-12-23",date(2026,10,29))
        self.assertTrue(s.bind_prompt(321,42,41))
        s.start(321,42)
        s.set_date(321,42,"2007-05-14",date(2026,10,29))
        self.assertTrue(s.bind_prompt(321,42,55))
        with self.assertRaises(ValueError):
            s.finish_from_button(321,42,41)
        self.assertEqual(s.finish_from_button(321,42,55),(date(2007,5,14),None))

    def test_expired_button_denied(self):
        now=[100.0]
        s=ReadingInputSessions(ttl=300,clock=lambda:now[0])
        s.start(1,2)
        s.set_date(1,2,"2005-12-23",date(2026,10,29))
        s.bind_prompt(1,2,17)
        now[0]+=301
        with self.assertRaises(ValueError):
            s.finish_from_button(1,2,17)

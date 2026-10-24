import unittest
from datetime import date, timedelta
from profile_commands import parse_consent_command

class ConsentParsingTests(unittest.TestCase):
 def test_explicit_marker(self):
    self.assertEqual(parse_consent_command("/savebirth 2005-12-23 အတည်ပြု"),"2005-12-23")
 def test_no_silent_consent(self):
    with self.assertRaises(ValueError):parse_consent_command("/savebirth 2005-12-23")
 def test_unrelated_command_rejected(self):
    with self.assertRaises(ValueError):parse_consent_command('/other 2005-12-23 confirmed')
 def test_wrong_consent(self):
    with self.assertRaises(ValueError):parse_consent_command("/savebirth 2005-12-23 yes")
 def test_reject_future_birth(self):
    future=date.today()+timedelta(days=367)
    with self.assertRaises(ValueError):parse_consent_command("/savebirth "+future.isoformat()+" အတည်ပြု")
 def test_reject_bad_date(self):
    with self.assertRaises(ValueError):parse_consent_command("/savebirth 2005-02-30 အတည်ပြု")
if __name__=="__main__":unittest.main()

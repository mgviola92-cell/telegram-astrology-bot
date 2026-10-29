import unittest
from datetime import date, datetime, timezone
from astro_core import SIGNS, TRADITIONAL_RULERS
from profection_reading import profection_reading

class TraditionalProfectionTests(unittest.TestCase):
    def test_birth_year_starts_first_house(self):
        x=profection_reading(date(2000,1,1),date(2000,1,1),"Gemini")
        self.assertEqual((x["house"],x["sign"],x["lord_of_year"]),(1,"Gemini","Mercury"))
        self.assertFalse(x["prediction_supported"])

    def test_every_rising_sign_and_twelve_years(self):
        birth=date(2000,1,1)
        for ascending_index,asc in enumerate(SIGNS):
            for age in range(0,24):
                with self.subTest(asc=asc,age=age):
                    result=profection_reading(birth,date(2000+age,1,1),asc)
                    self.assertEqual(result["house"],age%12+1)
                    target=(ascending_index+age)%12
                    self.assertEqual(result["sign"],SIGNS[target])
                    self.assertEqual(result["lord_of_year"],TRADITIONAL_RULERS[target])
                    self.assertIn("user-provided",result["rising_sign_source"])

    def test_birthday_boundary_and_twelve_year_return(self):
        birth=date(2005,12,23)
        before=profection_reading(birth,date(2026,12,22),"Aries")
        after=profection_reading(birth,date(2026,12,23),"Aries")
        self.assertEqual(before["age_completed"],20)
        self.assertEqual(after["age_completed"],21)
        self.assertEqual(before["house"],9)
        self.assertEqual(after["house"],10)
        self.assertEqual(profection_reading(birth,date(2017,12,23),"Aries")["house"],1)

    def test_february_29_birth_uses_march_1_in_non_leap_years(self):
        b=date(2000,2,29)
        for target,years in ((date(2023,2,28),22),(date(2023,3,1),23),
                             (date(2024,2,28),23),(date(2024,2,29),24),
                             (date(2025,2,28),24),(date(2025,3,1),25)):
            with self.subTest(target=target):
                value=profection_reading(b,target,"Aries")
                self.assertEqual(value["age_completed"],years)
                self.assertEqual(value["house"],years%12+1)
                self.assertTrue(value["leap_day_birthday_march_first"])

    def test_traditional_rulers_not_modern_swaps(self):
        for ascending,ruler in (("Scorpio","Mars"),("Aquarius","Saturn"),
                                ("Pisces","Jupiter")):
            with self.subTest(rising=ascending):
                result=profection_reading(date(2000,1,1),date(2000,1,1),ascending)
                self.assertEqual(result["lord_of_year"],ruler)

    def test_reject_nondate_or_unknown_ascendant(self):
        with self.assertRaises(ValueError):
            profection_reading(date(2000,1,1),date(2005,1,1),"Unknown")
        with self.assertRaises(ValueError):
            profection_reading(datetime(2000,1,1,tzinfo=timezone.utc),date(2005,1,1),"Leo")
        with self.assertRaises(ValueError):
            profection_reading(date(2000,1,1),datetime(2005,1,1),"Leo")

    def test_birth_after_target_rejected(self):
        with self.assertRaises(ValueError):
            profection_reading(date(2005,12,23),date(2000,1,1),"Leo")

if __name__=="__main__":
    unittest.main()

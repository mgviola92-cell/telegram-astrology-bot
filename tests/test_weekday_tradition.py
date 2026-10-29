"""All eight Burmese weekday animal/direction correspondences."""
import unittest
from datetime import datetime,timezone
from weekday_tradition import weekday_animal_info,TRADITIONS,RULE_ID,LIMITS
from myanmar_core import myanmar_birth_day

class WeekdayTraditionTests(unittest.TestCase):
    def test_all_eight_categories_have_animal_and_direction(self):
        self.assertEqual(len(TRADITIONS),8)
        samples=[
            ("2024-01-01 08:37","ကျား","အရှေ့","Moon"),
            ("2024-01-02 08:37","ခြင်္သေ့","အရှေ့တောင်","Mars"),
            ("2024-01-03 08:37","အစွယ်ရှိဆင်","တောင်","Mercury"),
            ("2024-01-03 12:30","အစွယ်မဲ့ဆင် (ဟိုင်း)","အနောက်မြောက်","Rahu"),
            ("2024-01-04 08:37","ကြွက်","အနောက်","Jupiter"),
            ("2024-01-05 08:37","ပူး","မြောက်","Venus"),
            ("2024-01-06 08:37","နဂါး","အနောက်တောင်","Saturn"),
            ("2024-01-07 08:37","ဂဠုန်","အရှေ့မြောက်","Sun"),
        ]
        for raw,animal,direction,planet in samples:
            born=datetime.strptime(raw,"%Y-%m-%d %H:%M")
            with self.subTest(day=raw):
                result=weekday_animal_info(born)
                self.assertEqual(result["animal"],animal)
                self.assertEqual(result["direction"],direction)
                self.assertEqual(result["planet"],planet)
                self.assertEqual(result["planet"],myanmar_birth_day(born)["planetary_association"])
                self.assertEqual(result["rule_id"],RULE_ID)
                self.assertFalse(result["prediction_supported"])
                self.assertFalse(result["profile_saved"])

    def test_wednesday_cutoff_and_caveat_is_explicit(self):
        early=weekday_animal_info(datetime(2024,1,3,11,59))
        noon=weekday_animal_info(datetime(2024,1,3,12,0))
        self.assertEqual(early["planet"],"Mercury")
        self.assertEqual(noon["planet"],"Rahu")
        self.assertIn("၁၈",LIMITS)
        self.assertIn("၁၂",LIMITS)

    def test_reject_future_concept_and_naive_only(self):
        with self.assertRaises(ValueError):
            weekday_animal_info(datetime(1800,1,3,12))
        with self.assertRaises(ValueError):
            weekday_animal_info(datetime(2024,1,3,12,tzinfo=timezone.utc))
        with self.assertRaises(ValueError):
            weekday_animal_info("2024-01-03 12:30")

if __name__=="__main__":
    unittest.main()

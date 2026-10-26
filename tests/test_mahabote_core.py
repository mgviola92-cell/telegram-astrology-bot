import copy
import unittest
from datetime import date, time, datetime
from mahabote_core import calculate_mahabote, WEEKDAYS, PLANETS, BURMESE_HOUSES
from mahabote_reading import interpret_mahabote, THEMES
from myanmar_calendar import calculate_myanmar_calendar, HOUSES

class MahaboteCalculationTests(unittest.TestCase):
    def test_research_worked_example_1990_may14_monday_puti(self):
        result=calculate_mahabote(date(1990,5,14))
        self.assertEqual(result["myanmar_year"],1352)
        self.assertEqual(result["weekday_code"],2)
        self.assertEqual(result["house_index"],6)
        self.assertEqual(result["house"],"Puti")
        self.assertEqual(result["placements"]["Puti"]["planet"],"Moon")

    def test_upstream_mmcal_cpp_2024_jan1_marana(self):
        # Independent yan9a/mmcal C++ cedate.cpp regression vector.
        chart=calculate_mahabote(date(2024,1,1))
        self.assertEqual(chart["myanmar_year"],1385)
        self.assertEqual(chart["weekday_code"],2)
        self.assertEqual(chart["house"],"Marana")

    def test_full_seven_house_planets_unique(self):
        dates=(date(1900,1,1),date(1950,12,31),date(1990,5,14),
               date(2005,12,23),date(2024,1,1),date(2026,10,27),
               date(2099,11,30),date(2100,12,30))
        for day in dates:
            with self.subTest(day=day):
                chart=calculate_mahabote(day)
                self.assertEqual(set(chart["placements"]),set(HOUSES))
                self.assertEqual({x["weekday_code"] for x in chart["placements"].values()},set(range(7)))
                self.assertEqual({x["planet"] for x in chart["placements"].values()},set(PLANETS))
                self.assertEqual(chart["placements"][chart["house"]]["weekday_code"],chart["weekday_code"])
                self.assertEqual(chart["house"],calculate_myanmar_calendar(day)["mahabote"])
                self.assertEqual(chart["evidence"]["derived_facts"]["birth_house"],chart["house"])

    def test_every_weekday_has_unique_house_in_one_week(self):
        from datetime import timedelta
        start=date(2026,10,26)
        charts=[calculate_mahabote(start+timedelta(days=i)) for i in range(7)]
        # Test a week far from the Myanmar New Year boundary.
        self.assertEqual(len({c["house"] for c in charts}),7)

    def test_wednesday_rahu_affects_label_but_not_house(self):
        day=date(2024,1,3)
        midnight=calculate_mahabote(day,time(0,0))
        morning=calculate_mahabote(day,time(11,59))
        afternoon=calculate_mahabote(day,time(12,0))
        late=calculate_mahabote(day,time(23,59))
        self.assertFalse(morning["rahu_wednesday_afternoon"])
        self.assertTrue(afternoon["rahu_wednesday_afternoon"])
        self.assertEqual({x["house"] for x in (midnight,morning,afternoon,late)},
                         {morning["house"]})
        self.assertEqual(morning["weekday_code"],4)
        self.assertIn("ရာဟု",afternoon["eight_day_weekday_label"])
        self.assertEqual(morning["placements"],afternoon["placements"])

    def test_house_readings_distinct_and_evidence_checked(self):
        self.assertEqual(set(THEMES),set(HOUSES))
        chart=calculate_mahabote(date(1990,5,14))
        interpretation=interpret_mahabote(chart)
        self.assertEqual(interpretation["house"],"Puti")
        self.assertFalse(interpretation["prediction_supported"])
        self.assertNotEqual(interpretation["calculation_rule_id"],
                            interpretation["interpretation_rule_id"])

    def test_reject_forged_calculation_or_house(self):
        chart=calculate_mahabote(date(1990,5,14))
        modified=copy.deepcopy(chart)
        modified["house"]="Binga"
        with self.assertRaises(ValueError):
            interpret_mahabote(modified)
        modified=copy.deepcopy(chart)
        modified["evidence"]["input_assumptions"]["local_birth_date"]="1990-05-15"
        with self.assertRaises(ValueError):
            interpret_mahabote(modified)

    def test_reject_invalid_date_and_time(self):
        with self.assertRaises(ValueError):
            calculate_mahabote(date(1800,1,1))
        with self.assertRaises(TypeError):
            calculate_mahabote(datetime(2024,1,1))
        from datetime import timezone
        with self.assertRaises(ValueError):
            calculate_mahabote(date(2024,1,1),time(12,0,tzinfo=timezone.utc))

if __name__=="__main__":
    unittest.main()

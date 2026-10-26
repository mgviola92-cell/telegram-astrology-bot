import copy
import unittest
from datetime import date, datetime
from astro_core import life_path
from bazi_core import calculate_bazi
from myanmar_calendar import calculate_myanmar_calendar
from reading_facts import reading_facts

def bazi_fixture():
    return calculate_bazi(datetime(2005,12,23,8,37),sect=2,timezone_verified="Asia/Yangon")

class ReadingFactsTests(unittest.TestCase):
    def test_actual_numerology_engine(self):
        result=life_path(date(1999,12,31))
        reading=reading_facts("numerology",result)
        self.assertEqual(reading["facts"]["life_path"],result["number"])
        self.assertFalse(reading["prediction_supported"])

    def test_actual_myanmar_calendar_engine(self):
        result=calculate_myanmar_calendar(date(2024,1,1))
        reading=reading_facts("myanmar_calendar",result)
        self.assertEqual(reading["facts"]["myanmar_year"],result["myanmar_year"])
        self.assertEqual(reading["facts"]["mahabote"],result["mahabote"])

    def test_bazi_evidence_fixture_consistent(self):
        self.assertEqual(reading_facts("bazi",bazi_fixture())["facts"]["day_master"],bazi_fixture()["day_master"])

    def test_reject_missing_evidence(self):
        with self.assertRaises(ValueError):
            reading_facts("numerology",{"number":11})

    def test_reject_modified_numerology_without_matching_evidence(self):
        original=life_path(date(1999,12,31))
        modified=copy.deepcopy(original)
        modified["number"]=8 if original["number"] != 8 else 9
        with self.assertRaises(ValueError):
            reading_facts("numerology",modified)

    def test_reject_modified_myanmar_year_without_matching_evidence(self):
        original=calculate_myanmar_calendar(date(2024,1,1))
        modified=copy.deepcopy(original)
        modified["myanmar_year"]+=1
        with self.assertRaises(ValueError):
            reading_facts("myanmar_calendar",modified)

    def test_reject_modified_myanmar_day_without_matching_evidence(self):
        modified=copy.deepcopy(calculate_myanmar_calendar(date(2024,1,1)))
        modified["day"]+=1
        with self.assertRaises(ValueError):
            reading_facts("myanmar_calendar",modified)

    def test_reject_modified_bazi_pillar_without_matching_evidence(self):
        modified=bazi_fixture()
        modified["pillars"]["year"]="甲子" if modified["pillars"]["year"]!="甲子" else "乙丑"
        with self.assertRaises(ValueError):
            reading_facts("bazi",modified)

    def test_reject_inconsistent_day_master(self):
        modified=bazi_fixture()
        modified["day_master"]="甲" if modified["day_master"]!="甲" else "辛"
        with self.assertRaises(ValueError):
            reading_facts("bazi",modified)

    def test_reject_missing_input_provenance(self):
        modified=bazi_fixture()
        del modified["evidence"]["input_assumptions"]
        with self.assertRaises(ValueError):
            reading_facts("bazi",modified)

    def test_reject_forged_matching_numerology_evidence(self):
        original=life_path(date(1999,12,31))
        modified=copy.deepcopy(original)
        modified["number"]=8 if original["number"]!=8 else 9
        modified["evidence"]["derived_facts"]["life_path"]=modified["number"]
        with self.assertRaises(ValueError):
            reading_facts("numerology",modified)

    def test_reject_forged_matching_calendar_evidence(self):
        original=calculate_myanmar_calendar(date(2024,1,1))
        modified=copy.deepcopy(original)
        modified["myanmar_year"]+=1
        modified["evidence"]["derived_facts"]["myanmar_year"]+=1
        with self.assertRaises(ValueError):
            reading_facts("myanmar_calendar",modified)

    def test_reject_invalid_source_birth_date(self):
        modified=copy.deepcopy(life_path(date(1999,12,31)))
        modified["evidence"]["input_assumptions"]["birth_date"]="invalid-date"
        with self.assertRaises(ValueError):
            reading_facts("numerology",modified)

    def test_reject_forged_bazi_result_and_matching_evidence(self):
        modified=bazi_fixture()
        modified["pillars"]["year"]="甲子" if modified["pillars"]["year"]!="甲子" else "乙丑"
        modified["evidence"]["derived_facts"]["pillars"]=modified["pillars"].copy()
        with self.assertRaises(ValueError):
            reading_facts("bazi",modified)

    def test_reject_wrong_bazi_birth_time(self):
        modified=bazi_fixture()
        modified["evidence"]["input_assumptions"]["birth_wall_clock"]="2005-12-24T08:37:00"
        with self.assertRaises(ValueError):
            reading_facts("bazi",modified)

    def test_reject_unknown_system(self):
        with self.assertRaises(ValueError):
            reading_facts("unreviewed_prediction",bazi_fixture())

if __name__=="__main__":
    unittest.main()

import copy
import unittest
from datetime import date
from myanmar_day_signals import calculate_day_signals
from myanmar_signal_reading import describe_day_signals, BOOLEAN_LABELS

class MyanmarSignalsReadingTests(unittest.TestCase):
    def test_all_translations_are_unique(self):
        self.assertEqual(len({name for _,name in BOOLEAN_LABELS}),len(BOOLEAN_LABELS))

    def test_primary_reference_2024_jan1_no_day_markers(self):
        signals=calculate_day_signals(date(2024,1,1))
        reading=describe_day_signals(signals)
        self.assertEqual(reading["active_labels"],[])
        self.assertEqual(reading["nagahle_direction"],"တောင်")
        self.assertFalse(reading["prediction_supported"])

    def test_reject_modified_marker_without_matching_evidence(self):
        signals=calculate_day_signals(date(2024,1,1))
        altered=copy.deepcopy(signals)
        altered["markers"]["sabbath"]=True
        with self.assertRaises(ValueError):
            describe_day_signals(altered)

    def test_reject_forged_marker_with_matching_evidence(self):
        signals=calculate_day_signals(date(2024,1,1))
        altered=copy.deepcopy(signals)
        altered["markers"]["sabbath"]=True
        altered["evidence"]["derived_facts"]["sabbath"]=True
        with self.assertRaises(ValueError):
            describe_day_signals(altered)

    def test_reject_changed_origin_date(self):
        signals=calculate_day_signals(date(2024,1,1))
        altered=copy.deepcopy(signals)
        altered["evidence"]["input_assumptions"]["local_gregorian_date"]="2024-01-02"
        with self.assertRaises(ValueError):
            describe_day_signals(altered)

    def test_reject_unknown_rule_id(self):
        signals=calculate_day_signals(date(2024,1,1))
        signals["evidence"]["rule_id"]="UNRESEARCHED"
        with self.assertRaises(ValueError):
            describe_day_signals(signals)

if __name__=="__main__":
    unittest.main()

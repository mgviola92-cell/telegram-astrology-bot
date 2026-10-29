"""Strict source-backed seven-house report with no hidden predictions."""
import copy
import unittest
from datetime import date,time
from html import unescape
from mahabote_core import calculate_mahabote,HOUSES,BURMESE_HOUSES
from mahabote_reading import interpret_mahabote,THEMES
from mahabote_report import render_mahabote_report,PLANET_NAMES,MAX_TELEGRAM_TEXT

class MahaboteReportTests(unittest.TestCase):
    def report(self,day,clock=None):
        chart=calculate_mahabote(day,clock)
        return chart,render_mahabote_report(chart,interpret_mahabote(chart))

    def test_every_house_shown_once_and_birth_house_highlighted(self):
        for day in (date(1990,5,14),date(2005,12,23),date(2024,1,3),
                    date(2026,10,29),date(1900,1,1),date(2099,12,30)):
            with self.subTest(day=day):
                chart,text=self.report(day)
                self.assertLess(len(text),MAX_TELEGRAM_TEXT)
                self.assertNotIn("\\n",text)
                self.assertEqual(text.count("★ "),1)
                self.assertIn("★ "+BURMESE_HOUSES[chart["house"]],text)
                self.assertIn("ဖွားအိမ်၏ ရိုးရာသင်္ကေတအနက်",text)
                self.assertIn("အခြားအိမ်များ၏ သင်္ကေတအညွှန်း",text)
                self.assertIn("မွေးအချက်အလက်",text)
                self.assertIn("မသိမ်း",text)
                for house in HOUSES:
                    planet=chart["placements"][house]["planet"]
                    self.assertIn(PLANET_NAMES[planet],text)
                    self.assertIn(THEMES[house][0],text)
                self.assertEqual(set(chart["placements"]),set(HOUSES))

    def test_birth_house_is_only_full_interpretation(self):
        chart,text=self.report(date(1990,5,14))
        self.assertIn(THEMES[chart["house"]][1],unescape(text))
        for other in HOUSES:
            if other!=chart["house"]:
                self.assertNotIn(THEMES[other][1],unescape(text))

    def test_rahu_name_separate_from_seven_house_math(self):
        morning=calculate_mahabote(date(2024,1,3),time(11,59))
        afternoon=calculate_mahabote(date(2024,1,3),time(12,0))
        self.assertEqual(morning["placements"],afternoon["placements"])
        text=render_mahabote_report(afternoon,interpret_mahabote(afternoon))
        self.assertIn("ရာဟု",text)
        self.assertIn("အိမ်အသစ် မတိုး",text)
        self.assertEqual(text.count("★ "),1)

    def test_tampered_chart_or_reading_denied(self):
        chart=calculate_mahabote(date(2005,12,23))
        reading=interpret_mahabote(chart)
        for field,bad in (("house","Puti"),("myanmar_year",99)):
            forged=copy.deepcopy(chart)
            forged[field]=bad
            with self.subTest(field=field),self.assertRaises(ValueError):
                render_mahabote_report(forged,reading)
        forged=reading.copy()
        forged["theme"]="အတည်မပြုနိုင်သော ဟောကိန်း"
        with self.assertRaises(ValueError):
            render_mahabote_report(chart,forged)

    def test_missing_evidence_and_types_rejected(self):
        chart=calculate_mahabote(date(2005,12,23))
        reading=interpret_mahabote(chart)
        chart.pop("evidence")
        with self.assertRaises(ValueError):
            render_mahabote_report(chart,reading)
        with self.assertRaises(ValueError):
            render_mahabote_report([],reading)

if __name__=="__main__":
    unittest.main()

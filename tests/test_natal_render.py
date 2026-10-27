import copy
import unittest
from datetime import datetime, date
from natal_pipeline import assemble_natal
from natal_render import render_natal_preview, MAX_TELEGRAM_CHARS
from western_chart import chart_from_longitudes

def fixture_provider(instant,path):
    if path!="test-only.bsp":
        raise ValueError("Unexpected ephemeris fixture")
    return chart_from_longitudes(
        {"Sun":270.4,"Moon":42.0,"Mars":358.5,"Venus":310.0},
        verified_source="CI synthetic positions: not physical ephemeris"
    )

class NatalPreviewRendererTests(unittest.TestCase):
    def make_chart(self):
        return assemble_natal(
            datetime(2005,12,23,8,37),
            "Asia/Yangon",16.85,96.15,"test-only.bsp",
            evaluation_date=date(2026,10,27),position_provider=fixture_provider,
        )

    def test_bounded_telegram_html_output(self):
        rendered=render_natal_preview(self.make_chart())
        self.assertIn("Development Preview",rendered)
        self.assertIn("Sun",rendered)
        self.assertIn("House",rendered)
        self.assertIn("Whole Sign Houses",rendered)
        self.assertIn("Independent Full Natal Benchmark",rendered)
        self.assertNotIn(chr(92)+"n",rendered)
        self.assertLess(len(rendered),MAX_TELEGRAM_CHARS)

    def test_missing_provenance_fails_closed(self):
        record=self.make_chart()
        record["position_evidence"]=None
        with self.assertRaises(ValueError):
            render_natal_preview(record)

    def test_unsupported_status_fails_closed(self):
        record=self.make_chart()
        record["status"]="verified-and-guaranteed"
        with self.assertRaises(ValueError):
            render_natal_preview(record)

    def test_bad_or_incomplete_houses_rejected(self):
        record=self.make_chart()
        record["rising"]["whole_sign_houses"].pop()
        with self.assertRaises(ValueError):
            render_natal_preview(record)

    def test_bad_planet_position_rejected(self):
        record=self.make_chart()
        record["planets"]["Sun"]["longitude"]=float("nan")
        with self.assertRaises(ValueError):
            render_natal_preview(record)

    def test_html_escaping_planet_label(self):
        record=self.make_chart()
        record["planets"]["<fake>"]=record["planets"].pop("Mars")
        rendered=render_natal_preview(record)
        self.assertIn("&lt;fake&gt;",rendered)
        self.assertNotIn("<fake>",rendered)

if __name__=="__main__":
    unittest.main()

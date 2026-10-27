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

    def test_true_vs_mean_frame_caveat_is_visible(self):
        chart=self.make_chart()
        result=render_natal_preview(chart)
        self.assertIn("True Ecliptic",result)
        self.assertIn("Mean Sidereal",result)
        self.assertIn("ယာယီ",result)

    def test_missing_mixed_frame_disclosure_rejected(self):
        chart=self.make_chart()
        chart.pop("coordinate_conventions")
        with self.assertRaisesRegex(ValueError,"coordinate-frame"):
            render_natal_preview(chart)

    def test_false_claim_of_frame_alignment_rejected(self):
        chart=self.make_chart()
        chart["coordinate_conventions"]["cross_frame_alignment_verified"]=True
        with self.assertRaisesRegex(ValueError,"coordinate-frame"):
            render_natal_preview(chart)

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

    def test_reject_forged_rising_sign(self):
        record=self.make_chart()
        record["rising"]["rising_sign"]="Aries" if record["rising"]["rising_sign"]!="Aries" else "Taurus"
        with self.assertRaisesRegex(ValueError,"Rising sign|Houses"):
            render_natal_preview(record)

    def test_reject_modified_ascendant_houses(self):
        record=self.make_chart()
        record["rising"]["ascendant_longitude"]=float("nan")
        with self.assertRaisesRegex(ValueError,"ascendant"):
            render_natal_preview(record)

    def test_reject_planet_sign_without_coordinate_match(self):
        record=self.make_chart()
        record["planets"]["Sun"]["sign"]="Pisces"
        with self.assertRaisesRegex(ValueError,"sign differs"):
            render_natal_preview(record)

    def test_reject_planet_house_mismatch(self):
        record=self.make_chart()
        old=record["planets"]["Sun"]["whole_sign_house"]
        record["planets"]["Sun"]["whole_sign_house"]=(old%12)+1
        with self.assertRaisesRegex(ValueError,"house differs"):
            render_natal_preview(record)

    def test_reject_forged_aspect_rows(self):
        record=self.make_chart()
        record["aspects"]=[]
        with self.assertRaisesRegex(ValueError,"Aspects differ"):
            render_natal_preview(record)

    def test_html_escaping_planet_label(self):
        record=self.make_chart()
        record["planets"]["<fake>"]=record["planets"].pop("Mars")
        from western_aspects import calculate_aspects
        record["aspects"]=calculate_aspects({name:item["longitude"] for name,item in record["planets"].items()})["aspects"]
        rendered=render_natal_preview(record)
        self.assertIn("&lt;fake&gt;",rendered)
        self.assertNotIn("<fake>",rendered)

if __name__=="__main__":
    unittest.main()

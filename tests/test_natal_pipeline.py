import unittest
from datetime import datetime, date, timezone
from natal_pipeline import assemble_natal

def fake_positions(utc, path):
    assert utc.tzinfo is not None
    assert path == "fixture.bsp"
    return {
        "points": {
            "Sun": {"sign":"Aries","longitude":10.0},
            "Moon":{"sign":"Taurus","longitude":42.0},
            "Mars":{"sign":"Pisces","longitude":358.0},
        },
        "aspects":[],
        "evidence":{"input_assumptions":{"test_only":True}},
    }

class NatalPipelineTests(unittest.TestCase):
    def setUp(self):
        self.birth = datetime(2005, 12, 23, 8, 37)
        self.args = (self.birth,"Asia/Yangon",16.85,96.15,"fixture.bsp")

    def chart(self, **kw):
        return assemble_natal(*self.args, position_provider=fake_positions, **kw)

    def test_utc_conversion(self):
        result=self.chart()
        self.assertEqual(result["birth"]["utc"],"2005-12-23T02:07:00+00:00")
        self.assertEqual(result["birth"]["iana_timezone"],"Asia/Yangon")

    def test_houses_and_profection(self):
        result=self.chart(evaluation_date=date(2025,12,23))
        sign=result["rising"]["rising_sign"]
        self.assertEqual(result["rising"]["whole_sign_houses"][0]["sign"],sign)
        self.assertEqual(result["annual_profection"]["house"],(20%12)+1)
        self.assertEqual(set(x["whole_sign_house"] for x in result["planets"].values()).issubset(set(range(1,13))),True)

    def test_reject_unknown_timezone(self):
        with self.assertRaises(ValueError):
            assemble_natal(self.birth,"Bad/Zone",16.85,96.15,"fixture.bsp",position_provider=fake_positions)

    def test_reject_missing_location(self):
        with self.assertRaises(ValueError):
            assemble_natal(self.birth,"Asia/Yangon",float("nan"),96.15,"fixture.bsp",position_provider=fake_positions)

    def test_reject_future_birth(self):
        with self.assertRaises(ValueError):
            assemble_natal(datetime(2099,1,1),"Asia/Yangon",16.85,96.15,"fixture.bsp",position_provider=fake_positions)

    def test_reject_before_birth_profection(self):
        with self.assertRaises(ValueError):
            self.chart(evaluation_date=date(2004,12,23))

    def test_reject_missing_kernel_path(self):
        with self.assertRaises(ValueError):
            assemble_natal(self.birth,"Asia/Yangon",16.85,96.15,"",position_provider=fake_positions)

    def test_reject_invalid_position_provider(self):
        with self.assertRaises(ValueError):
            assemble_natal(*self.args,position_provider=lambda _utc,_path: {"points":{},"aspects":[]})

    def test_no_user_data_persistence(self):
        result=self.chart()
        self.assertNotIn("telegram_user_id",result)
        self.assertFalse(result["birth"]["true_solar_time_applied"])

if __name__ == "__main__":
    unittest.main()

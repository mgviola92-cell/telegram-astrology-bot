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

    def test_local_date_not_prior_utc_date(self):
        local = datetime(2005,1,1,0,10)
        result=assemble_natal(local,"Asia/Yangon",16.85,96.15,"fixture.bsp",
            position_provider=fake_positions)
        self.assertTrue(result["birth"]["utc"].startswith("2004-12-31"))
        self.assertEqual(result["annual_profection"]["house"],1)

    def test_reject_nonexistent_dst(self):
        with self.assertRaisesRegex(ValueError,"does not exist"):
            assemble_natal(datetime(2024,3,10,2,30),"America/Los_Angeles",
                34.05,-118.25,"fixture.bsp",position_provider=fake_positions)

    def test_reject_ambiguous_dst(self):
        with self.assertRaisesRegex(ValueError,"Ambiguous"):
            assemble_natal(datetime(2024,11,3,1,30),"America/Los_Angeles",
                34.05,-118.25,"fixture.bsp",position_provider=fake_positions)

    def test_explicit_dst_fold(self):
        local=datetime(2024,11,3,1,30)
        a=assemble_natal(local,"America/Los_Angeles",34.05,-118.25,
            "fixture.bsp",fold=0,position_provider=fake_positions)
        b=assemble_natal(local,"America/Los_Angeles",34.05,-118.25,
            "fixture.bsp",fold=1,position_provider=fake_positions)
        self.assertNotEqual(a["birth"]["utc"],b["birth"]["utc"])

    def test_inconsistent_planet_sign_rejected(self):
        def inconsistent(_utc,_path):
            return {"points":{"Sun":{"sign":"Taurus","longitude":10.0}},"aspects":[]}
        with self.assertRaisesRegex(ValueError,"inconsistent zodiac sign"):
            assemble_natal(*self.args,position_provider=inconsistent)

    def test_reject_forged_aspects_that_disagree_with_positions(self):
        def inconsistent_aspects(_utc,_path):
            return {
                "points":{"Sun":{"sign":"Aries","longitude":10.0},
                          "Moon":{"sign":"Aries","longitude":11.0}},
                "aspects":[],
            }
        with self.assertRaisesRegex(ValueError,"aspects disagree"):
            assemble_natal(*self.args,position_provider=inconsistent_aspects)

    def test_accept_aspects_recomputed_from_verified_longitudes(self):
        from western_chart import chart_from_longitudes
        def consistent(_utc,_path):
            return chart_from_longitudes(
                {"Sun":10.0,"Moon":11.0},
                verified_source="CI calculation fixture only"
            )
        record=assemble_natal(*self.args,position_provider=consistent)
        self.assertEqual(record["aspects"][0]["aspect"],"conjunction")

    def test_missing_planet_longitude_rejected(self):
        def incomplete(_utc,_path):
            return {"points":{"Sun":{"sign":"Aries"}},"aspects":[]}
        with self.assertRaisesRegex(ValueError,"ecliptic longitude"):
            assemble_natal(*self.args,position_provider=incomplete)

    def test_nonfinite_planet_longitude_rejected(self):
        def invalid(_utc,_path):
            return {"points":{"Sun":{"sign":"Aries","longitude":float("nan")}},"aspects":[]}
        with self.assertRaises(ValueError):
            assemble_natal(*self.args,position_provider=invalid)

    def test_no_user_data_persistence(self):
        result=self.chart()
        self.assertNotIn("telegram_user_id",result)
        self.assertFalse(result["birth"]["true_solar_time_applied"])

if __name__ == "__main__":
    unittest.main()

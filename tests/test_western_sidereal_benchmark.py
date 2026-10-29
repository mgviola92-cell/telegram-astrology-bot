"""Independent published Greenwich mean sidereal time vector checks."""
import unittest
from datetime import datetime,timezone,timedelta
from western_houses import calculate_whole_sign_chart,julian_day,greenwich_mean_sidereal
from western_sidereal_benchmark import (
    verify_gmst_reference_vectors,angular_difference,
    EXAMPLE_1987_GMST,EXAMPLE_1987_JD,RULE_ID,
)

class SiderealReferenceTests(unittest.TestCase):
    def test_mixed_1987_and_j2000_reference_vectors(self):
        result=verify_gmst_reference_vectors()
        self.assertEqual(result["rule_id"],RULE_ID)
        self.assertEqual(len(result["vectors"]),2)
        self.assertFalse(result["independent_natal_positions_benchmarked"])
        self.assertFalse(result["ascendant_vs_external_chart_benchmarked"])
        self.assertFalse(result["ut1_correction_applied"])
        self.assertLess(result["vectors"][0]["angular_residual_degrees"],0.00002)
        self.assertAlmostEqual(result["vectors"][0]["julian_day"],EXAMPLE_1987_JD,places=7)
        self.assertAlmostEqual(result["vectors"][0]["reference_degrees"],EXAMPLE_1987_GMST,places=7)

    def test_julian_day_is_timezone_invariant_for_same_instant(self):
        utc=datetime(2000,1,1,12,tzinfo=timezone.utc)
        local=utc.astimezone(timezone(timedelta(hours=6,minutes=30)))
        self.assertEqual(julian_day(local),julian_day(utc))
        self.assertAlmostEqual(julian_day(local),2451545.0,places=8)

    def test_mean_longitude_shift_matches_explicit_local_sidereal(self):
        instant=datetime(2024,1,1,0,tzinfo=timezone.utc)
        for longitude in (-150,-90,0,96.15,179.9):
            with self.subTest(longitude=longitude):
                chart=calculate_whole_sign_chart(instant,longitude,16.85)
                expected=(greenwich_mean_sidereal(julian_day(instant))+longitude)%360
                self.assertLess(angular_difference(chart["local_mean_sidereal_deg"],expected),1e-7)
                self.assertFalse(chart["metadata"]["planetary_frame_compatible_without_conversion"])

    def test_wrap_distance_and_missing_timezone(self):
        self.assertAlmostEqual(angular_difference(359.9,0.1),0.2)
        with self.assertRaises(ValueError):
            julian_day(datetime(2024,1,1,12))

if __name__=="__main__":
    unittest.main()

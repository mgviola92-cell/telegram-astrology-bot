import math
import unittest
from western_ascendant_audit import vector_horizon_audit
from western_houses import ascendant_from_sidereal, mean_obliquity, julian_day
from datetime import datetime, timezone

class AscendantIndependentGeometryTests(unittest.TestCase):
    def test_eastern_horizon_identity_across_world_latitudes(self):
        epsilon=mean_obliquity(julian_day(datetime(2024,10,27,12,tzinfo=timezone.utc)))
        count=0
        for lat in (-64,-50,-23.5,0,16.85,23.5,45,64):
            for theta in range(0,360,5):
                with self.subTest(lat=lat,lst=theta):
                    computed=vector_horizon_audit(theta,lat,epsilon)
                    self.assertAlmostEqual(
                        computed["ascendant_longitude"],
                        ascendant_from_sidereal(theta,lat,epsilon),
                        places=10
                    )
                    self.assertLess(abs(computed["horizon_altitude_residual"]),1e-10)
                    self.assertGreater(computed["east_direction_cosine"],0)
                    self.assertFalse(computed["true_ecliptic_planetary_frame_matches"])
                    count+=1
        self.assertEqual(count,576)

    def test_wraparound_at_360_sidereal_degrees(self):
        a=vector_horizon_audit(0,16.85,23.44)
        b=vector_horizon_audit(360,16.85,23.44)
        self.assertAlmostEqual(a["ascendant_longitude"],b["ascendant_longitude"],places=9)

    def test_reject_invalid_latitudes_and_nonfinite_angles(self):
        for values in ((0,80,23.44),(0,0,float("nan")),
                       (0,0,False),(float("inf"),0,23.44)):
            with self.subTest(values=values):
                with self.assertRaises(ValueError):
                    vector_horizon_audit(*values)

if __name__=="__main__":
    unittest.main()

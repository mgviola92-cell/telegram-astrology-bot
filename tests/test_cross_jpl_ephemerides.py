"""Cross-JPL ephemeris consistency checks with two real SPK datasets.

DE421 (2008) and DE440s (2020) are separately generated JPL ephemerides,
both evaluated through Skyfield. Agreement is NOT an independent software
or astrological forecast accuracy benchmark.
"""
import os
import unittest
from datetime import datetime,timezone
from western_chart import geocentric_chart, TARGETS

@unittest.skipUnless(os.getenv("JPL_EPHEMERIS_PATH") and os.getenv("JPL_SECOND_EPHEMERIS_PATH"),
                     "Both authentic DE421 and DE440s ephemerides required")
class CrossEphemerisChecks(unittest.TestCase):
    def test_two_real_jpl_ephemerides_agree_for_birth_era(self):
        for moment in (
            datetime(1905,5,14,12,tzinfo=timezone.utc),
            datetime(2000,1,1,12,tzinfo=timezone.utc),
            datetime(2024,10,27,6,tzinfo=timezone.utc),
            datetime(2049,6,15,12,tzinfo=timezone.utc),
        ):
            first=geocentric_chart(moment,os.environ["JPL_EPHEMERIS_PATH"])
            second=geocentric_chart(moment,os.environ["JPL_SECOND_EPHEMERIS_PATH"])
            self.assertEqual(set(first["points"]),set(TARGETS))
            self.assertEqual(set(second["points"]),set(TARGETS))
            for name in TARGETS:
                with self.subTest(epoch=moment,body=name):
                    a=first["points"][name]["longitude"]
                    b=second["points"][name]["longitude"]
                    d=abs(a-b)
                    separation=min(d,360-d)
                    # Conservative 0.03-degree tolerance; not a claim of
                    # milliarcsecond agreement or independent implementation.
                    self.assertLess(separation,0.03)

if __name__=="__main__":
    unittest.main()

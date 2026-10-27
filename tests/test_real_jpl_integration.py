"""Real JPL DE421 integration test: runs only with a downloaded SPK.

Compares the project's output against direct Skyfield calculations from the
same authentic kernel: this is an end-to-end integration test, not an
independent cross-ephemeris astronomical accuracy benchmark.
"""
import os
import unittest
from datetime import datetime, timezone
from pathlib import Path

from jpl_kernel_audit import audit_kernel_file
from western_chart import TARGETS, geocentric_chart
from western_aspects import calculate_aspects


@unittest.skipUnless(os.getenv("JPL_EPHEMERIS_PATH"), "Real .bsp path not configured")
class RealJplIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.path=os.environ["JPL_EPHEMERIS_PATH"]
        if not Path(cls.path).is_file():
            raise AssertionError("JPL_EPHEMERIS_PATH does not point to a file")

    def test_real_kernel_planets_and_exact_tdb_coverage(self):
        from skyfield.api import load, load_file
        from skyfield.framelib import ecliptic_frame
        from contextlib import closing
        ts=load.timescale()
        for utc in (
            datetime(2000,1,1,12,tzinfo=timezone.utc),
            datetime(2005,12,23,2,7,tzinfo=timezone.utc),
            datetime(2024,1,1,0,tzinfo=timezone.utc),
            datetime(2049,6,15,12,tzinfo=timezone.utc),
        ):
            with self.subTest(utc=utc):
                audit=audit_kernel_file(self.path,utc)
                self.assertTrue(audit["valid"])
                actual=geocentric_chart(utc,self.path)
                self.assertEqual(set(actual["points"]),set(TARGETS))
                self.assertTrue(actual["evidence"]["input_assumptions"]["apparent_positions"])
                t=ts.from_datetime(utc)
                with closing(load_file(self.path)) as kernel:
                    earth=kernel["earth"]
                    for label,body in TARGETS.items():
                        _,longitude,_=earth.at(t).observe(kernel[body]).apparent().frame_latlon(ecliptic_frame)
                        self.assertAlmostEqual(actual["points"][label]["longitude"],longitude.degrees%360,places=7)
                expected=calculate_aspects({k:v["longitude"] for k,v in actual["points"].items()})
                self.assertEqual(actual["aspects"],expected["aspects"])

    def test_date_outside_real_de421_refused(self):
        with self.assertRaises(ValueError):
            geocentric_chart(datetime(2080,1,1,tzinfo=timezone.utc),self.path)


if __name__=="__main__":
    unittest.main()

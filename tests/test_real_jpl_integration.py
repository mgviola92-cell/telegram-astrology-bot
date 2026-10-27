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

    def test_real_mean_ecliptic_matches_independent_vector_rotation(self):
        import math
        from skyfield.api import load, load_file
        from skyfield.framelib import mean_equator_and_equinox_of_date
        from western_houses import mean_obliquity
        from contextlib import closing
        ts=load.timescale()
        for utc in (
            datetime(2000,1,1,12,tzinfo=timezone.utc),
            datetime(2005,12,23,2,7,tzinfo=timezone.utc),
            datetime(2024,10,27,6,tzinfo=timezone.utc),
        ):
            with self.subTest(utc=utc):
                result=geocentric_chart(
                    utc,self.path,coordinate_frame="mean_ecliptic_of_date"
                )
                self.assertEqual(
                    result["evidence"]["input_assumptions"]["coordinate_frame"],
                    "mean_ecliptic_of_date"
                )
                t=ts.from_datetime(utc)
                e=math.radians(mean_obliquity(float(t.ut1)))
                with closing(load_file(self.path)) as kernel:
                    earth=kernel["earth"]
                    for label,body in TARGETS.items():
                        position=earth.at(t).observe(kernel[body]).apparent()
                        xyz=position.frame_xyz(mean_equator_and_equinox_of_date).au
                        expected=math.degrees(
                            math.atan2(xyz[1]*math.cos(e)+xyz[2]*math.sin(e),
                                       xyz[0])
                        )%360
                        self.assertAlmostEqual(result["points"][label]["longitude"],
                                               expected,places=7)

    def test_full_natal_pipeline_uses_real_mean_frame_consistently(self):
        from natal_pipeline import assemble_natal
        from natal_render import render_natal_preview
        from datetime import date
        result=assemble_natal(
            datetime(2005,12,23,8,37),
            "Asia/Yangon",16.85,96.15,self.path,
            evaluation_date=date(2026,10,27)
        )
        flags=result["coordinate_conventions"]
        self.assertFalse(flags["mixed_true_mean_frames"])
        self.assertTrue(flags["cross_frame_alignment_verified"])
        self.assertTrue(flags["planet_house_assignments_provisional"])
        self.assertEqual(
            result["position_evidence"]["input_assumptions"]["coordinate_frame"],
            "mean_ecliptic_of_date"
        )
        html=render_natal_preview(result)
        self.assertIn("Mean Equinox",html)
        self.assertIn("Development Preview",html)

    def test_date_outside_real_de421_refused(self):
        with self.assertRaises(ValueError):
            geocentric_chart(datetime(2080,1,1,tzinfo=timezone.utc),self.path)


if __name__=="__main__":
    unittest.main()

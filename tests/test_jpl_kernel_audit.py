import unittest
from datetime import datetime, timezone
from types import SimpleNamespace
from jpl_kernel_audit import validate_kernel_segments

SEGMENT_CHAINS=((0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(0,7),(0,8),(0,9),(0,10),
                (3,301),(3,399),(1,199),(2,299),(4,499))
TARGET_CODES=tuple(target for _,target in SEGMENT_CHAINS)
SOURCE_NAMES=("earth","sun","moon","mercury","venus","mars",
              "jupiter barycenter","saturn barycenter",
              "uranus barycenter","neptune barycenter","pluto barycenter")

class FakeKernel:
    def __init__(self, *, missing=None, year_coverage=(1900,2100)):
        self.missing=missing
        self.segments=[
            SimpleNamespace(center=center,target=target,spk_segment=SimpleNamespace(
                start_jd=2415020.5 if year_coverage[0]==1900 else 2460000.5,
                end_jd=2488069.5 if year_coverage[1]==2100 else 2460500.5))
            for center,target in SEGMENT_CHAINS
        ]
    def __getitem__(self,key):
        if key==self.missing:
            raise KeyError(key)
        if key not in SOURCE_NAMES:
            raise KeyError(key)
        return key

class KernelAuditTests(unittest.TestCase):
    def test_existing_target_chains_and_date(self):
        result=validate_kernel_segments(FakeKernel(),datetime(2024,1,1,tzinfo=timezone.utc))
        self.assertTrue(result["valid"])
        self.assertTrue(result["planet_centers_and_barycenters_distinguished"])
        self.assertGreater(result["target_count"],5)

    def test_exact_tdb_julian_day_boundary_is_enforced(self):
        kernel=FakeKernel()
        instant=datetime(2024,1,1,tzinfo=timezone.utc)
        valid=validate_kernel_segments(kernel,instant,tdb_jd=2460310.5)
        self.assertEqual(valid["epoch_timescale"],"TDB")
        self.assertEqual(valid["birth_jd"],2460310.5)
        with self.assertRaisesRegex(ValueError,"lacks an active barycentric path"):
            validate_kernel_segments(kernel,instant,tdb_jd=2500000.0)

    def test_bad_tdb_date_rejected(self):
        kernel=FakeKernel()
        instant=datetime(2024,1,1,tzinfo=timezone.utc)
        for bad in (float("nan"),float("inf"),True,"2460000"):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    validate_kernel_segments(kernel,instant,tdb_jd=bad)

    def test_mars_barycenter_supported_without_mars_center(self):
        class BarycenterOnly(FakeKernel):
            def __getitem__(self,key):
                if key=="mars":
                    raise KeyError(key)
                if key=="mars barycenter":
                    return key
                return super().__getitem__(key)
        kernel=BarycenterOnly()
        kernel.segments=[x for x in kernel.segments if x.target!=499]
        result=validate_kernel_segments(kernel,datetime(2024,1,1,tzinfo=timezone.utc))
        self.assertFalse(result["mars_center_available"])
        self.assertTrue(result["valid"])

    def test_reject_mars_barycenter_missing_if_center_absent(self):
        class BothAbsent(FakeKernel):
            def __getitem__(self,key):
                if key in ("mars","mars barycenter"):
                    raise KeyError(key)
                return super().__getitem__(key)
        with self.assertRaisesRegex(ValueError,"mars or mars barycenter"):
            validate_kernel_segments(BothAbsent(),datetime(2024,1,1,tzinfo=timezone.utc))

    def test_missing_named_target(self):
        with self.assertRaisesRegex(ValueError,"missing required objects"):
            validate_kernel_segments(
                FakeKernel(missing="pluto barycenter"),
                datetime(2024,1,1,tzinfo=timezone.utc)
            )

    def test_inner_planet_center_missing_from_spk(self):
        kernel=FakeKernel()
        kernel.segments=[x for x in kernel.segments if x.target!=199]
        with self.assertRaisesRegex(ValueError,"lacks an active barycentric path"):
            validate_kernel_segments(kernel,datetime(2024,1,1,tzinfo=timezone.utc))

    def test_reject_unconnected_target_with_valid_name(self):
        kernel=FakeKernel()
        # Body still exists but is no longer reachable from barycenter 0.
        replacement=next(x for x in kernel.segments if x.target==301)
        replacement.center=777
        with self.assertRaisesRegex(ValueError,"lacks an active barycentric path"):
            validate_kernel_segments(kernel,datetime(2024,1,1,tzinfo=timezone.utc))

    def test_reject_missing_earth_barycenter_bridge(self):
        kernel=FakeKernel()
        kernel.segments=[x for x in kernel.segments if x.target!=3]
        with self.assertRaisesRegex(ValueError,"lacks an active barycentric path"):
            validate_kernel_segments(kernel,datetime(2024,1,1,tzinfo=timezone.utc))

    def test_kernel_out_of_range_date(self):
        kernel=FakeKernel(year_coverage=(2023,2024))
        with self.assertRaisesRegex(ValueError,"lacks an active barycentric path"):
            validate_kernel_segments(kernel,datetime(2040,1,1,tzinfo=timezone.utc))

    def test_refuses_naive_birth_instant(self):
        with self.assertRaises(ValueError):
            validate_kernel_segments(FakeKernel(),datetime(2024,1,1))

    def test_refuses_absent_segments(self):
        kernel=FakeKernel()
        kernel.segments=[]
        with self.assertRaisesRegex(ValueError,"no segments"):
            validate_kernel_segments(kernel,datetime(2024,1,1,tzinfo=timezone.utc))

if __name__=="__main__":
    unittest.main()

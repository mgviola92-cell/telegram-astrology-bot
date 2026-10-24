import unittest
from datetime import datetime,timezone,timedelta
from western_houses import *
class HouseTests(unittest.TestCase):
 def test_j2000(self): self.assertAlmostEqual(julian_day(datetime(2000,1,1,12,tzinfo=timezone.utc)),2451545.0,places=7)
 def test_gmst(self): self.assertAlmostEqual(greenwich_mean_sidereal(2451545),280.46061837,places=6)
 def test_eps(self): self.assertAlmostEqual(mean_obliquity(2451545),23.439291111,places=6)
 def test_quadrants(self):
  for a,e in ((0,90),(90,180),(180,270),(270,0)):
   self.assertAlmostEqual(ascendant_from_sidereal(a,0,23.44),e,places=5)
 def test_house_ring(self):
  h=whole_sign_houses(359.9)
  self.assertEqual(h[0]['sign'],'Pisces')
  self.assertEqual(h[1]['sign'],'Aries')
  self.assertEqual(h[-1]['sign'],'Aquarius')
 def test_timezone(self):
  a=datetime(2024,1,1,6,tzinfo=timezone(timedelta(hours=6)))
  b=datetime(2024,1,1,tzinfo=timezone.utc)
  self.assertEqual(julian_day(a),julian_day(b))
 def test_poles_rejected(self):
  with self.assertRaises(ValueError): calculate_whole_sign_chart(datetime.now(timezone.utc),0,80)
 def test_coords_required(self):
  with self.assertRaises(ValueError): calculate_whole_sign_chart(datetime.now(timezone.utc),float('nan'),0)
 def test_aware_required(self):
  with self.assertRaises(ValueError):calculate_whole_sign_chart(datetime(2024,1,1),0,0)
 def test_full_chart(self):
  x=calculate_whole_sign_chart(datetime(2024,1,1,tzinfo=timezone.utc),96.15,16.85)
  self.assertEqual(len(x['whole_sign_houses']),12)
  self.assertEqual(len({r['sign'] for r in x['whole_sign_houses']}),12)
  self.assertEqual(x['rising_sign'],x['whole_sign_houses'][0]['sign'])
if __name__=='__main__':unittest.main()

import unittest
from datetime import date
from astro_core import annual_profection, age_on, life_path, reduce_number

class CoreTests(unittest.TestCase):
    def test_birthday_boundary(self):
        self.assertEqual(age_on(date(2000,11,5),date(2026,11,4)),25)
        self.assertEqual(age_on(date(2000,11,5),date(2026,11,5)),26)
    def test_profection_full_cycle(self):
        a=date(2000,1,1)
        for age in range(0,60):
            out=annual_profection(a,date(2000+age,1,1),'Aries')
            self.assertEqual(out['house'],age%12+1)
        self.assertEqual(annual_profection(a,date(2024,1,1),'Aries')['house'],1)
        self.assertEqual(annual_profection(a,date(2025,1,1),'Aries')['lord_of_year'],'Venus')
    def test_profection_wrapped_sign(self):
        result=annual_profection(date(2000,1,1),date(2001,1,1),'Pisces')
        self.assertEqual(result['sign'],'Aries')
        self.assertEqual(result['house'],2)
    def test_invalid_ascendant(self):
        with self.assertRaises(ValueError): annual_profection(date(2000,1,1),date(2024,1,1),'Unknown')
    def test_life_path(self):
        self.assertEqual(life_path(date(1990,7,25))['number'],6)
        self.assertEqual(reduce_number(29),11)
        self.assertEqual(reduce_number(29,False),2)
    def test_sources_attached(self):
        self.assertIn('rule_id',life_path(date(2000,1,1))['evidence'])

if __name__ == '__main__': unittest.main()

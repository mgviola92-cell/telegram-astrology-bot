import unittest
from western_aspects import angular_separation, calculate_aspects

class AspectsTests(unittest.TestCase):
    def test_wraparound(self):
        self.assertEqual(angular_separation(359,1),2)
    def test_conjunction(self):
        self.assertEqual(calculate_aspects({'Sun':359,'Moon':1})['aspects'][0]['aspect'],'conjunction')
    def test_square(self):
        self.assertEqual(calculate_aspects({'Mars':0,'Venus':90})['aspects'][0]['aspect'],'square')
    def test_trine(self):
        self.assertEqual(calculate_aspects({'A':0,'B':120})['aspects'][0]['aspect'],'trine')
    def test_opposition(self):
        self.assertEqual(calculate_aspects({'A':0,'B':180})['aspects'][0]['aspect'],'opposition')
    def test_sextile(self):
        self.assertEqual(calculate_aspects({'A':0,'B':60})['aspects'][0]['aspect'],'sextile')
    def test_no_major_aspect(self):
        self.assertEqual(calculate_aspects({'A':0,'B':45})['aspects'],[])
    def test_nonfinite_rejected(self):
        with self.assertRaises(ValueError):calculate_aspects({'A':float('nan')})
    def test_invalid_orb(self):
        with self.assertRaises(ValueError):calculate_aspects({'A':1,'B':2},orb_policy={'bad':(90,99)})
    def test_evidence(self):
        self.assertEqual(calculate_aspects({'A':10,'B':10})['evidence']['rule_id'],'WEST-ASPECTS-GEOMETRY-001')

if __name__=='__main__':unittest.main()

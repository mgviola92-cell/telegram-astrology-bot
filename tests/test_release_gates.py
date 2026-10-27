"""Release-gate assertions: public UI must not advertise provisional natal."""
import unittest
from pathlib import Path
from native_ui import FEATURES, COMMAND_GUIDES, section_keyboard, feature_keyboard
from evidence_ui import RULES
from bazi_seasons import RULE_ID as SEASON_RULE
from dayun_reading import RULE_ID as DAYUN_RULE
from profection_reading import RULE_ID as PROFECTION_RULE

class AstrologyReleaseGateTests(unittest.TestCase):
    def test_sensitive_natal_development_gate_default_disabled(self):
        template=Path(__file__).resolve().parents[1].joinpath(".env.example").read_text(encoding="utf-8")
        self.assertIn("ENABLE_WESTERN_NATAL=0",template)
        self.assertNotIn("ENABLE_WESTERN_NATAL=1",template)
        self.assertNotIn("natal",COMMAND_GUIDES)
        self.assertNotIn(("Natal Chart","natal"),FEATURES["western"][2])

    def test_ready_methods_are_available_by_guide_only(self):
        self.assertIn(("Da Yun Cycles","dayun"),FEATURES["bazi"][2])
        self.assertIn(("Annual Profection","profection"),FEATURES["western"][2])
        self.assertIn("dayun",COMMAND_GUIDES)
        self.assertIn("profection",COMMAND_GUIDES)

    def test_every_new_rule_has_readable_evidence(self):
        for key in (SEASON_RULE,DAYUN_RULE,PROFECTION_RULE,
                    "WEST-TROPICAL-LONGITUDES-001","WEST-ASC-WHOLE-SIGN-001"):
            with self.subTest(key=key):
                self.assertIn(key,RULES)
                for field in ("heading","method","source","limits"):
                    self.assertTrue(RULES[key][field].strip())

    def test_no_excluded_vedic_features_in_public_menu(self):
        all_features=" ".join(str((k,v)) for k,v in FEATURES.items()).lower()
        self.assertNotIn("vedic",all_features)
        self.assertNotIn("jyotish",all_features)
        self.assertNotIn("kundli",all_features)
        self.assertNotIn("dasha",all_features)

if __name__=="__main__":
    unittest.main()

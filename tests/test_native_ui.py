import unittest
from aiogram.types import InlineKeyboardMarkup
from native_ui import (
    SECTIONS, FEATURES, COMMAND_GUIDES, button,
    home_keyboard, section_keyboard, feature_keyboard,
    guide_keyboard, home_text, feature_text, guide_text,
)

class NativeUiTests(unittest.TestCase):
    def all_buttons(self,keyboard):
        self.assertIsInstance(keyboard,InlineKeyboardMarkup)
        return [b for row in keyboard.inline_keyboard for b in row]
    def test_clean_english_labels_and_myanmar_exception(self):
        charts=self.all_buttons(section_keyboard("charts"))
        labels=[b.text for b in charts]
        for label in ("မြန်မာဗေဒင်","Western Astrology","BaZi","Numerology","Tarot"):
            self.assertIn(label,labels)
        self.assertFalse(any("🃏" in x or "🔮" in x or "🌌" in x for x in labels))
    def test_every_navigation_target_exists(self):
        keyboards=[home_keyboard()]
        keyboards += [section_keyboard(s) for s in SECTIONS]
        keyboards += [feature_keyboard(f) for f in FEATURES]
        keyboards += [guide_keyboard(g) for g in COMMAND_GUIDES]
        for kb in keyboards:
            for b in self.all_buttons(kb):
                with self.subTest(target=b.callback_data):
                    self.assertLessEqual(len(b.callback_data.encode("utf-8")),64)
                    parts=b.callback_data.split(":")
                    self.assertEqual(parts[0],"ui")
                    if len(parts)==2:
                        self.assertIn(parts[1],("home","tarot","library","study"))
                    elif parts[1]=="category":
                        self.assertIn(parts[2],SECTIONS)
                    elif parts[1]=="feature":
                        self.assertIn(parts[2],FEATURES)
                    elif parts[1]=="guide":
                        self.assertIn(parts[2],COMMAND_GUIDES)
                    elif parts[1]=="reading":
                        self.assertIn(parts[2],("start","skip"))
                    else:
                        self.fail("Unknown navigation type")
    def test_unfinished_feature_not_claimed_ready(self):
        self.assertIn(("Annual Profection","profection"),FEATURES["western"][2])
        self.assertNotIn("natal",COMMAND_GUIDES)
        self.assertIn(("နေ့စဉ်ပြက္ခဒိန်","daily"),FEATURES["daily"][2])
        self.assertFalse(FEATURES["compatibility"][2])
    def test_guides_do_not_embed_user_data(self):
        for command in COMMAND_GUIDES:
            with self.subTest(command=command):
                self.assertIn("<code>",guide_text(command))
                self.assertIn("မသိမ်း",guide_text(command))
        self.assertNotIn("2005-12-23",home_text())
    def test_group_home_has_only_public_calendar_action(self):
        from native_ui import group_home_keyboard,group_home_text
        buttons=self.all_buttons(group_home_keyboard())
        self.assertEqual([b.callback_data for b in buttons],["group:today"])
        self.assertNotIn("2005-12-23",group_home_text())
        self.assertNotIn("Save Birth Date",group_home_text())
        self.assertIn("/today",group_home_text())

    def test_back_and_home_on_feature(self):
        for feature in FEATURES:
            actions=[b.text for b in self.all_buttons(feature_keyboard(feature))]
            self.assertIn("Back",actions)
            self.assertIn("Home",actions)
    def test_owner_controls_not_exposed(self):
        self.assertNotIn("owner",FEATURES)
        for section in SECTIONS.values():
            self.assertNotIn("owner",[item[1] for item in section[1]])

    def test_all_buttons_are_nonempty_and_clean(self):
        keyboards=[home_keyboard()]
        keyboards.extend(section_keyboard(s) for s in SECTIONS)
        keyboards.extend(feature_keyboard(f) for f in FEATURES)
        keyboards.extend(guide_keyboard(g) for g in COMMAND_GUIDES)
        for keyboard in keyboards:
            for b in self.all_buttons(keyboard):
                self.assertTrue(b.text.strip())
                self.assertFalse(any(ord(c)>0x1F000 for c in b.text),
                                 "Decorative emoji in button label: "+b.text)

    def test_invalid_callbacks_rejected(self):
        with self.assertRaises(ValueError):
            button("test","x"*65)
        with self.assertRaises(KeyError):
            section_keyboard("nonexistent")
        with self.assertRaises(KeyError):
            feature_text("nonexistent")
if __name__=="__main__":unittest.main()

import json
import tempfile
import unittest
from pathlib import Path
from tarot_core import DECK
from tarot_media import parse_media_registry, load_media_registry, card_photo_file_id, coverage

class TarotMediaTests(unittest.TestCase):
 def test_empty_registry_still_allows_text_fallback(self):
    r=parse_media_registry("{}")
    self.assertIsNone(card_photo_file_id("The Star",r))
    self.assertEqual(coverage(r)["mapped"],0)
 def test_complete_card_registry(self):
    r=parse_media_registry(json.dumps({card:"AgAC"+str(i) for i,card in enumerate(DECK)}))
    self.assertEqual(coverage(r)["mapped"],78)
    self.assertTrue(coverage(r)["complete"])
    self.assertEqual(card_photo_file_id("The Star",r),r["The Star"])
 def test_reject_unknown_card(self):
    with self.assertRaises(ValueError):parse_media_registry('{"Imaginary Card":"AgACx"}')
 def test_reject_url_and_path_instead_of_telegram_file_id(self):
    for invalid in ("https://cdn.example/pic.jpg","/tmp/card.png","abc def"):
        with self.subTest(value=invalid),self.assertRaises(ValueError):
            parse_media_registry(json.dumps({"The Star":invalid}))
 def test_reject_invalid_document_structure(self):
    for raw in ("[]","null","not-json"):
        with self.assertRaises(ValueError):parse_media_registry(raw)
 def test_read_file_from_disk(self):
    with tempfile.TemporaryDirectory() as folder:
        p=Path(folder)/"registry.json"
        p.write_text('{"The Star":"AgACopaque"}',encoding="utf-8")
        self.assertEqual(load_media_registry(str(p))["The Star"],"AgACopaque")
 def test_no_path_means_disabled(self):
    self.assertEqual(load_media_registry(None),{})
if __name__=="__main__":unittest.main()

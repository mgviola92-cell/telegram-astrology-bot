"""Low-bandwidth Telegram media policy without real API requests."""
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from tarot_delivery import TarotAssetPolicy, cached_photo_registry, valid_file_id

class DeliveryTests(unittest.TestCase):
    def setUp(self):
        cached_photo_registry.cache_clear()
    def test_default_file_id_is_reused_as_is(self):
        with patch.dict(os.environ,{"TAROT_MEDIA_MODE":"telegram"}):
            policy=TarotAssetPolicy()
            self.assertEqual(policy.asset("AgACopaque"),"AgACopaque")
            self.assertIsNone(policy.asset("https://example.com/img.jpg"))
            self.assertIsNone(policy.asset("/tmp/image.png"))
    def test_unknown_mode_fails_closed_to_text(self):
        p=TarotAssetPolicy()
        with patch.dict(os.environ,{"TAROT_MEDIA_MODE":"unknown"}):
            self.assertIsNone(p.asset("AgACopaque"))

    def test_text_mode_sends_no_media_even_if_configured(self):
        policy=TarotAssetPolicy()
        with patch.dict(os.environ,{"TAROT_MEDIA_MODE":"text"}):
            self.assertIsNone(policy.asset("AgACopaque"))
            self.assertIsNone(policy.photo("The Star","/missing/path.json"))
    def test_manifest_cached_not_reread_on_each_card(self):
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/"manifest.json"
            path.write_text(json.dumps({"The Star":"AgACstar","The Sun":"AgACsun"}),encoding="utf8")
            policy=TarotAssetPolicy()
            with patch.dict(os.environ,{"TAROT_MEDIA_MODE":"telegram"}):
                self.assertEqual(policy.photo("The Star",str(path)),"AgACstar")
                path.unlink()
                self.assertEqual(policy.photo("The Sun",str(path)),"AgACsun")
                self.assertEqual(cached_photo_registry.cache_info().misses,1)
    def test_failed_media_not_retried_and_ram_bounded(self):
        p=TarotAssetPolicy(max_rejections=1)
        with patch.dict(os.environ,{"TAROT_MEDIA_MODE":"telegram"}):
            p.mark_failed("AgACbroken")
            self.assertIsNone(p.asset("AgACbroken"))
            p.mark_failed("AgACanother")
            self.assertEqual(p.asset("AgACanother"),"AgACanother")
            self.assertEqual(len(p._bad_ids),1)
    def test_reject_file_paths_whitespace_and_typed_invalid_input(self):
        for value in ("", "x","hello world","https://t.me/file","C:\\img.png",None,123):
            self.assertFalse(valid_file_id(value))
    def test_no_files_exist_until_explicit_manifest_configured(self):
        with patch.dict(os.environ,{"TAROT_MEDIA_MODE":"telegram"}):
            p=TarotAssetPolicy()
            self.assertIsNone(p.photo("The Star",""))

if __name__=="__main__":
    unittest.main()

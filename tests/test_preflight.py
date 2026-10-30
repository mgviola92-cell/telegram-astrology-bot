"""Preflight tests never require Telegram network or live secrets."""
import unittest
from unittest.mock import patch
import preflight

class PreflightTests(unittest.TestCase):
    def test_source_mode_no_secrets_required(self):
        with patch.object(preflight.importlib,"import_module",return_value=object()):
            r=preflight.inspect_environment(mode="ci",environ={})
        self.assertTrue(r["passed"])
        self.assertFalse(any(x["name"].startswith("telegram_") for x in r["checks"]))
    def test_missing_dependencies_reported(self):
        with patch.object(preflight.importlib,"import_module",side_effect=ImportError("absent")):
            r=preflight.inspect_environment(mode="ci",environ={})
        self.assertFalse(r["passed"])
        self.assertEqual(len([x for x in r["checks"] if x["name"].startswith("dependency:") and not x["passed"]]),4)
    def test_deploy_config_fails_closed(self):
        with patch.object(preflight.importlib,"import_module",return_value=object()):
            r=preflight.inspect_environment(mode="deploy",environ={})
        self.assertFalse(r["passed"])
        self.assertFalse(next(x for x in r["checks"] if x["name"]=="telegram_token")["passed"])
    def test_unpaired_profile_settings(self):
        with patch.object(preflight.importlib,"import_module",return_value=object()):
            r=preflight.inspect_environment(mode="deploy",environ={"PROFILE_DB_PATH":"/tmp/profiles.sqlite3"})
        self.assertFalse(next(x for x in r["checks"] if x["name"]=="profile_config_paired")["passed"])
    def test_natal_release_gate_and_bad_flag_rejected(self):
        with patch.object(preflight.importlib,"import_module",return_value=object()):
            review=preflight.inspect_environment(mode="deploy",environ={
                "TELEGRAM_BOT_TOKEN":"123:TEST","ENABLE_WESTERN_NATAL":"1"})
            self.assertFalse(next(x for x in review["checks"]
                if x["name"]=="natal_release_review_approved")["passed"])
            malformed=preflight.inspect_environment(mode="deploy",environ={
                "TELEGRAM_BOT_TOKEN":"123:TEST","ENABLE_WESTERN_NATAL":"true"})
            self.assertFalse(next(x for x in malformed["checks"]
                if x["name"]=="natal_flag_valid")["passed"])

    def test_optional_tarot_manifest_and_file_id_validation(self):
        from tempfile import TemporaryDirectory
        from pathlib import Path
        import json
        with TemporaryDirectory() as folder:
            path=Path(folder)/"tarot.json"
            path.write_text(json.dumps({"The Star":"AAAA1234"}),encoding="utf-8")
            env={"TELEGRAM_BOT_TOKEN":"123:TEST","TAROT_CARD_PHOTOS_JSON":str(path)}
            with patch.object(preflight.importlib,"import_module",return_value=object()):
                passing=preflight.inspect_environment(mode="deploy",environ=env)
                self.assertTrue(passing["passed"])
                stat=next(x["detail"] for x in passing["checks"]
                    if x["name"]=="optional:tarot_photo_coverage")
                self.assertIn("1/78",stat)
                env["TAROT_CARD_PHOTOS_JSON"]=str(Path(folder)/"missing.json")
                missing=preflight.inspect_environment(mode="deploy",environ=env)
                self.assertFalse(next(x for x in missing["checks"]
                    if x["name"]=="tarot_manifest_valid")["passed"])
                env["TAROT_CARD_PHOTOS_JSON"]=str(path)
                env["TAROT_SHUFFLE_FILE_ID"]="https://example.invalid/a"
                invalid=preflight.inspect_environment(mode="deploy",environ=env)
                self.assertFalse(next(x for x in invalid["checks"]
                    if x["name"]=="tarot_asset_valid:TAROT_SHUFFLE_FILE_ID")["passed"])

    def test_optional_tarot_assets_do_not_block_deploy(self):
        from tempfile import TemporaryDirectory
        from pathlib import Path
        with TemporaryDirectory() as directory:
            from cryptography.fernet import Fernet
            env={"TELEGRAM_BOT_TOKEN":"111:dummy","PROFILE_DB_PATH":str(Path(directory)/"profiles.sqlite3"),
                 "PROFILE_ENCRYPTION_KEY":Fernet.generate_key().decode("ascii")}
            with patch.object(preflight.importlib,"import_module",return_value=object()):
                result=preflight.inspect_environment(mode="deploy",environ=env)
        self.assertTrue(result["passed"])
        self.assertIn("optional:TAROT_SHUFFLE_FILE_ID",[x["name"] for x in result["checks"]])
    def test_render_profile_storage_requires_explicit_persistent_disk_confirmation(self):
        from tempfile import TemporaryDirectory
        from pathlib import Path
        from cryptography.fernet import Fernet
        with TemporaryDirectory() as directory:
            config={"TELEGRAM_BOT_TOKEN":"123:test", "RENDER":"true",
                    "PROFILE_DB_PATH":str(Path(directory)/"birth.sqlite3"),
                    "PROFILE_ENCRYPTION_KEY":Fernet.generate_key().decode("ascii")}
            with patch.object(preflight.importlib,"import_module",return_value=object()):
                r=preflight.inspect_environment(mode="deploy",environ=config)
                self.assertFalse(r["passed"])
                guard=next(c for c in r["checks"] if c["name"]=="render_profile_persistence_confirmed")
                self.assertFalse(guard["passed"])
                config["PROFILE_PERSISTENT_DISK_CONFIRMED"]="1"
                verified=preflight.inspect_environment(mode="deploy",environ=config)
                self.assertTrue(verified["passed"])
                config.pop("PROFILE_DB_PATH")
                config.pop("PROFILE_ENCRYPTION_KEY")
                without_profiles=preflight.inspect_environment(mode="deploy",environ=config)
                self.assertTrue(without_profiles["passed"])

    def test_reject_unknown_media_mode(self):
        with patch.object(preflight.importlib,"import_module",return_value=object()):
            bad=preflight.inspect_environment(mode="deploy",environ={"TELEGRAM_BOT_TOKEN":"123:test","TAROT_MEDIA_MODE":"reupload"})
        self.assertFalse(next(c for c in bad["checks"] if c["name"]=="tarot_media_mode")["passed"])

    def test_natal_kernel_only_required_when_enabled(self):
        with patch.object(preflight.importlib,"import_module",return_value=object()):
            r=preflight.inspect_environment(mode="deploy",environ={
                "TELEGRAM_BOT_TOKEN":"111:dummy","ENABLE_WESTERN_NATAL":"1"})
        self.assertFalse(next(x for x in r["checks"] if x["name"]=="jpl_kernel_present")["passed"])
    def test_group_settings_require_persistent_render_disk_and_real_directory(self):
        from pathlib import Path
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as temp:
            config={"TELEGRAM_BOT_TOKEN":"333:test","RENDER":"1",
                    "GROUP_SETTINGS_DB_PATH":str(Path(temp)/"small.sqlite3")}
            with patch.object(preflight.importlib,"import_module",return_value=object()):
                result=preflight.inspect_environment(mode="deploy",environ=config)
                self.assertFalse(result["passed"])
                self.assertFalse(next(x for x in result["checks"] if x["name"]=="render_group_settings_disk_confirmed")["passed"])
                config["GROUP_SETTINGS_PERSISTENT_DISK_CONFIRMED"]="1"
                accepted=preflight.inspect_environment(mode="deploy",environ=config)
                self.assertTrue(accepted["passed"])
                config["GROUP_SETTINGS_DB_PATH"]=str(Path(temp)/"missing"/"small.sqlite3")
                bad=preflight.inspect_environment(mode="deploy",environ=config)
                self.assertFalse(next(x for x in bad["checks"] if x["name"]=="group_settings_db_directory")["passed"])

    def test_group_db_cannot_share_profile_store_file(self):
        from pathlib import Path
        from tempfile import TemporaryDirectory
        from cryptography.fernet import Fernet
        with TemporaryDirectory() as tmp:
            shared=str(Path(tmp)/"private.sqlite3")
            config={"TELEGRAM_BOT_TOKEN":"333:test",
                    "GROUP_SETTINGS_DB_PATH":shared,
                    "PROFILE_DB_PATH":shared,
                    "PROFILE_ENCRYPTION_KEY":Fernet.generate_key().decode("ascii")}
            with patch.object(preflight.importlib,"import_module",return_value=object()):
                report=preflight.inspect_environment(mode="deploy",environ=config)
            self.assertFalse(next(x for x in report["checks"] if x["name"]=="group_db_separate_from_birth_profiles")["passed"])

    def test_optional_jpl_path_must_exist_if_configured(self):
        with patch.object(preflight.importlib,"import_module",return_value=object()):
            r=preflight.inspect_environment(mode="deploy",environ={
                "TELEGRAM_BOT_TOKEN":"111:dummy","JPL_EPHEMERIS_PATH":"/nonexistent/kernel.bsp"})
        self.assertFalse(next(x for x in r["checks"] if x["name"]=="jpl_kernel_optional_path")["passed"])
    def test_reject_bad_mode(self):
        with self.assertRaises(ValueError):
            preflight.inspect_environment(mode="other",environ={})
    def test_does_not_echo_secrets(self):
        env={"TELEGRAM_BOT_TOKEN":"123:KEEP_PRIVATE","PROFILE_ENCRYPTION_KEY":"VERY_SECRET",
             "PROFILE_DB_PATH":"/tmp/local.sqlite3"}
        with patch.object(preflight.importlib,"import_module",return_value=object()):
            r=preflight.inspect_environment(mode="deploy",environ=env)
        for check in r["checks"]:
            for secret in ("KEEP_PRIVATE","VERY_SECRET"):
                self.assertNotIn(secret,str(check))
if __name__=="__main__": unittest.main()

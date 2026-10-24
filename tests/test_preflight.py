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
    def test_natal_kernel_only_required_when_enabled(self):
        with patch.object(preflight.importlib,"import_module",return_value=object()):
            r=preflight.inspect_environment(mode="deploy",environ={
                "TELEGRAM_BOT_TOKEN":"111:dummy","ENABLE_WESTERN_NATAL":"1"})
        self.assertFalse(next(x for x in r["checks"] if x["name"]=="jpl_kernel_present")["passed"])
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

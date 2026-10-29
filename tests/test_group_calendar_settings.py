"""Group-specific policy storage: no profile data, no background jobs."""
import sqlite3
import tempfile
import unittest
from pathlib import Path
from group_calendar_settings import GroupCalendarSettings

class GroupSettingsTests(unittest.TestCase):
    def test_memory_default_true_and_override(self):
        g=GroupCalendarSettings()
        self.assertTrue(g.enabled(-1001))
        self.assertFalse(g.persistent)
        self.assertTrue(g.set_enabled(-1001,False,expected=True))
        self.assertFalse(g.enabled(-1001))
        self.assertTrue(g.enabled(-1002))
        self.assertFalse(g.set_enabled(-1001,False,expected=True))
        self.assertFalse(g.enabled(-1001))
        self.assertTrue(g.set_enabled(-1001,True,expected=False))
        self.assertTrue(g.enabled(-1001))
        self.assertEqual(len(g._cache),0)
    def test_old_button_cannot_reverse_new_state(self):
        g=GroupCalendarSettings()
        self.assertTrue(g.set_enabled(-1001,False,expected=True))
        self.assertFalse(g.set_enabled(-1001,False,expected=True))
        self.assertFalse(g.enabled(-1001))
        self.assertTrue(g.set_enabled(-1001,True,expected=False))
        self.assertTrue(g.enabled(-1001))
    def test_disabled_override_not_evicted_in_memory(self):
        g=GroupCalendarSettings(limit=1)
        g.set_enabled(-101,False)
        with self.assertRaises(OverflowError):
            g.set_enabled(-102,False)
        self.assertFalse(g.enabled(-101))
        self.assertTrue(g.enabled(-102))
    def test_persistent_only_saves_disabled_overrides(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=str(Path(tmp)/"group.sqlite3")
            a=GroupCalendarSettings(path,limit=1)
            self.assertTrue(a.enabled(-101))
            a.set_enabled(-101,False)
            a.set_enabled(-102,False)
            b=GroupCalendarSettings(path,limit=1)
            self.assertFalse(b.enabled(-101))
            self.assertFalse(b.enabled(-102))
            b.set_enabled(-101,True)
            self.assertTrue(GroupCalendarSettings(path).enabled(-101))
            with sqlite3.connect(path) as db:
                rows=db.execute("SELECT chat_id,enabled FROM group_today_settings").fetchall()
                self.assertEqual(rows,[(-102,0)])
                columns=[x[1] for x in db.execute("PRAGMA table_info(group_today_settings)")]
                self.assertEqual(columns,["chat_id","enabled"])
    def test_render_ephemeral_disk_guard(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=str(Path(tmp)/"settings.sqlite3")
            with self.assertRaises(ValueError):
                GroupCalendarSettings.from_environment({"RENDER":"true","GROUP_SETTINGS_DB_PATH":path})
            s=GroupCalendarSettings.from_environment({
                "RENDER":"true","GROUP_SETTINGS_DB_PATH":path,
                "GROUP_SETTINGS_PERSISTENT_DISK_CONFIRMED":"1"})
            self.assertTrue(s.persistent)
            self.assertFalse(GroupCalendarSettings.from_environment({"RENDER":"true"}).persistent)
    def test_invalid_inputs_rejected(self):
        g=GroupCalendarSettings()
        for value in (0,100,None,True,-2**65):
            with self.subTest(value=value),self.assertRaises(ValueError):
                g.enabled(value)
        for arg in (1,"false",None):
            with self.assertRaises(ValueError):
                g.set_enabled(-1001,arg)
        with self.assertRaises(ValueError):
            GroupCalendarSettings(limit=0)
        with self.assertRaises(ValueError):
            GroupCalendarSettings(":memory:")
    def test_restart_clears_temporary_mode(self):
        a=GroupCalendarSettings()
        a.set_enabled(-1001,False)
        b=GroupCalendarSettings()
        self.assertTrue(b.enabled(-1001))

if __name__=="__main__":
    unittest.main()

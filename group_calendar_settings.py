"""Small per-group calendar settings, optional persistent SQLite.

No user profiles, birth data, media, background polling or scheduled writes.
Disabled overrides only: an enabled group costs no persistent DB row.
Memory-only mode is explicitly temporary and resets at process restart.
One worker only. Persistent mode caches at most 1024 active group values.
"""
import os
import sqlite3
from collections import OrderedDict
from pathlib import Path
from threading import RLock

class GroupCalendarSettings:
    def __init__(self, db_path=None, *, limit=1024, on_render=False, disk_confirmed=False):
        if type(limit) is not int or limit<=0:
            raise ValueError("Positive cache capacity required")
        if db_path is not None and (not isinstance(db_path,str) or not db_path.strip() or db_path==":memory:"):
            raise ValueError("Configured group settings need a persistent SQLite path")
        if db_path and on_render and not disk_confirmed:
            raise ValueError("Render group settings require a verified persistent disk")
        self.db_path=db_path
        self.limit=limit
        self._cache=OrderedDict()
        self._lock=RLock()
        if self.db_path:
            parent=Path(self.db_path).expanduser().parent
            if not parent.is_dir():
                raise ValueError("Group settings database directory must exist")
            with self._connect() as db:
                db.execute("PRAGMA journal_mode=WAL")
                db.execute("""CREATE TABLE IF NOT EXISTS group_today_settings (
                    chat_id INTEGER PRIMARY KEY,
                    enabled INTEGER NOT NULL CHECK (enabled IN (0,1))
                )""")

    @classmethod
    def from_environment(cls, env=None):
        env=os.environ if env is None else env
        path=(env.get("GROUP_SETTINGS_DB_PATH") or "").strip() or None
        neon=(env.get("ASTROLOGY_DATABASE_URL") or "").strip()
        if neon:
            if path:
                raise ValueError("Neon and SQLite group settings cannot both be configured")
            from neon_persistence import NeonGroupCalendarSettings
            return NeonGroupCalendarSettings(neon)
        return cls(path,on_render=bool(env.get("RENDER")),
                   disk_confirmed=env.get("GROUP_SETTINGS_PERSISTENT_DISK_CONFIRMED")=="1")

    def _connect(self):
        return sqlite3.connect(self.db_path,timeout=5)

    @staticmethod
    def _validate(chat_id):
        # Normal Telegram group IDs are negative, unlike private user IDs.
        if type(chat_id) is not int or chat_id >= 0 or chat_id<=-(2**63):
            raise ValueError("Expected a negative Telegram group ID")

    @property
    def persistent(self):
        return self.db_path is not None

    def enabled(self,chat_id):
        self._validate(chat_id)
        with self._lock:
            if chat_id in self._cache:
                self._cache.move_to_end(chat_id)
                return self._cache[chat_id]
            if not self.persistent:
                return True
            with self._connect() as db:
                row=db.execute("SELECT enabled FROM group_today_settings WHERE chat_id=?",
                               (chat_id,)).fetchone()
            value=bool(row[0]) if row is not None else True
            self._remember(chat_id,value)
            return value

    def _remember(self,chat_id,value):
        if chat_id not in self._cache and len(self._cache)>=self.limit:
            if self.persistent:
                self._cache.popitem(last=False)
            elif value is False:
                # Never evict a disabled temporary group: that would silently
                # turn its calendar back on.
                raise OverflowError("Temporary group setting limit reached")
        if value is True and not self.persistent:
            self._cache.pop(chat_id,None)
        else:
            self._cache[chat_id]=value
            self._cache.move_to_end(chat_id)

    def set_enabled(self,chat_id,enabled,*,expected=None):
        self._validate(chat_id)
        if type(enabled) is not bool:
            raise ValueError("enabled must be boolean")
        if expected is not None and type(expected) is not bool:
            raise ValueError("expected must be boolean")
        with self._lock:
            current=self.enabled(chat_id)
            if expected is not None and current!=expected:
                return False
            if current==enabled:
                return True
            if self.persistent:
                with self._connect() as db:
                    if enabled:
                        db.execute("DELETE FROM group_today_settings WHERE chat_id=?",(chat_id,))
                    else:
                        db.execute("INSERT INTO group_today_settings(chat_id,enabled) VALUES (?,0) "
                                   "ON CONFLICT(chat_id) DO UPDATE SET enabled=0",(chat_id,))
            self._remember(chat_id,enabled)
            return True

    def disable_all_temporary(self):
        """Not exposed to chat users; used only in unit tests."""
        if self.persistent:
            raise ValueError("Persistent config must not be reset")
        with self._lock:
            self._cache.clear()

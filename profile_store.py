"""Encrypted, consent-gated birth profiles backed by SQLite.

No plaintext birth dates, names, locations, astrology readings, or images are
written to disk. A Fernet key MUST be supplied externally and backed up
securely; losing that key makes all stored profiles unrecoverable.
"""
import json
import sqlite3
import time
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Mapping
from cryptography.fernet import Fernet, InvalidToken

MAX_PAYLOAD_BYTES=4096
FIELDS=frozenset({"birth_date", "birth_time", "birth_timezone", "latitude", "longitude_east", "label"})

class ProfileStore:
    def __init__(self, db_path: str, encryption_key: str | bytes, *, now=None):
        if not encryption_key:
            raise ValueError("PROFILE_ENCRYPTION_KEY is required")
        if not db_path or db_path==":memory:":
            raise ValueError("Use a persistent SQLite path; memory databases are not supported here")
        self._crypto=Fernet(encryption_key.encode("ascii") if isinstance(encryption_key,str) else encryption_key)
        self._db_path=str(Path(db_path))
        self._now=now or (lambda:int(time.time()))
        with self._connection() as conn:
            conn.execute("""CREATE TABLE IF NOT EXISTS birth_profiles (
                user_id INTEGER PRIMARY KEY,
                encrypted_payload BLOB NOT NULL,
                updated_unix INTEGER NOT NULL,
                consent_unix INTEGER NOT NULL
            )""")
            # No username, phone number, DOB, location, assets or Telegram token columns.
            conn.execute("CREATE INDEX IF NOT EXISTS idx_profile_update ON birth_profiles(updated_unix)")

    @contextmanager
    def _connection(self):
        conn=sqlite3.connect(self._db_path,timeout=10)
        try:
            conn.execute("PRAGMA busy_timeout=10000")
            conn.execute("PRAGMA journal_mode=WAL")
            yield conn
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def _validate_user(user_id:int):
        if type(user_id) is not int or user_id<=0 or user_id>=2**63:
            raise ValueError("Expected a positive Telegram user ID")

    def save(self, user_id:int, profile:Mapping, *, explicit_consent:bool=False):
        self._validate_user(user_id)
        if explicit_consent is not True:
            raise PermissionError("Explicit consent is required before saving birth information")
        if not isinstance(profile,Mapping) or not profile:
            raise ValueError("Profile fields required")
        if not set(profile)<=FIELDS:
            raise ValueError("Unsupported or sensitive profile field")
        if "birth_date" not in profile:
            raise ValueError("birth_date is required")
        if not all(isinstance(k,str) and isinstance(v,(str,int,float)) and not isinstance(v,bool)
                   for k,v in profile.items()):
            raise ValueError("Invalid profile types")
        try:
            datetime.strptime(str(profile["birth_date"]),"%Y-%m-%d")
        except ValueError as exc:
            raise ValueError("Expected birth_date YYYY-MM-DD") from exc
        encoded=json.dumps(dict(profile),ensure_ascii=False,separators=(",",":")).encode("utf-8")
        if len(encoded)>MAX_PAYLOAD_BYTES:
            raise ValueError("Profile too large")
        sealed=self._crypto.encrypt(encoded)
        at=int(self._now())
        with self._connection() as conn:
            conn.execute("""INSERT INTO birth_profiles(user_id,encrypted_payload,updated_unix,consent_unix)
                VALUES (?,?,?,?)
                ON CONFLICT(user_id) DO UPDATE SET encrypted_payload=excluded.encrypted_payload,
                    updated_unix=excluded.updated_unix,consent_unix=excluded.consent_unix""",
                (user_id,sealed,at,at))

    def read(self,user_id:int):
        self._validate_user(user_id)
        with self._connection() as conn:
            row=conn.execute("SELECT encrypted_payload FROM birth_profiles WHERE user_id=?", (user_id,)).fetchone()
        if row is None:return None
        try:
            return json.loads(self._crypto.decrypt(row[0]).decode("utf-8"))
        except (InvalidToken,UnicodeDecodeError,ValueError) as exc:
            raise ValueError("Profile unreadable: wrong encryption key or corrupted data") from exc

    def delete(self,user_id:int)->bool:
        self._validate_user(user_id)
        with self._connection() as conn:
            result=conn.execute("DELETE FROM birth_profiles WHERE user_id=?", (user_id,))
            return result.rowcount>0

    def delete_older_than(self, cutoff_unix:int)->int:
        if type(cutoff_unix) is not int or cutoff_unix<=0:
            raise ValueError("Invalid retention cutoff")
        with self._connection() as conn:
            result=conn.execute("DELETE FROM birth_profiles WHERE updated_unix<?",(cutoff_unix,))
            return result.rowcount

"""Encrypted, consent-gated birth profiles backed by SQLite.

No plaintext birth dates, names, locations, astrology readings, or images are
written to disk. A Fernet key MUST be supplied externally and backed up
securely; losing that key makes all stored profiles unrecoverable.
"""
import json
import sqlite3
import time
from contextlib import contextmanager
from datetime import date, datetime
from math import isfinite
from pathlib import Path
from typing import Mapping
from cryptography.fernet import Fernet, InvalidToken, MultiFernet

MAX_PAYLOAD_BYTES=4096
FIELDS=frozenset({"birth_date", "birth_time", "birth_timezone", "latitude", "longitude_east", "label"})

class ProfileStore:
    def __init__(self, db_path: str, encryption_key: str | bytes, *, now=None, old_keys=()):
        if not encryption_key:
            raise ValueError("PROFILE_ENCRYPTION_KEY is required")
        if not db_path or db_path==":memory:":
            raise ValueError("Use a persistent SQLite path; memory databases are not supported here")
        if isinstance(old_keys, (bytes, str)):
            raise ValueError("old_keys must be a sequence of key values, not one string")
        keys=[encryption_key,*old_keys]
        self._crypto=MultiFernet([
            Fernet(key.encode("ascii") if isinstance(key,str) else key)
            for key in keys
        ])
        self._db_path=str(Path(db_path))
        self._now=now or (lambda:int(time.time()))
        with self._connection() as conn:
            # WAL mode persists in the SQLite database header. Set it once
            # at initialization rather than repeating a write-oriented PRAGMA
            # on every short-lived read connection.
            conn.execute("PRAGMA journal_mode=WAL")
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
            try:
                yield conn
            except BaseException:
                conn.rollback()
                raise
            else:
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
        if not isinstance(profile["birth_date"], str):
            raise ValueError("birth_date must be YYYY-MM-DD")
        try:
            birth_date=date.fromisoformat(profile["birth_date"])
            if birth_date.isoformat()!=profile["birth_date"]:
                raise ValueError("Noncanonical birth date")
            if birth_date > date.today():
                raise ValueError("Birth date cannot be in the future")
        except ValueError as exc:
            raise ValueError("Expected valid birth_date YYYY-MM-DD") from exc
        for field in ("latitude","longitude_east"):
            if field in profile:
                number=profile[field]
                if not isinstance(number,(float,int)) or isinstance(number,bool) or not isfinite(number):
                    raise ValueError(f"Invalid {field}")
                low,high=(-90,90) if field=="latitude" else (-180,180)
                if not low<=number<=high:
                    raise ValueError(f"Invalid {field} range")
        if "birth_time" in profile:
            try:
                datetime.strptime(profile["birth_time"],"%H:%M")
            except (ValueError,TypeError) as exc:
                raise ValueError("birth_time requires HH:MM") from exc
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

    def rotate_encrypted_profiles(self)->int:
        """Re-encrypt existing ciphertext under the primary key, atomically.

        Deploy with new key first and all prior keys in old_keys. Verify all
        records are readable before removing old keys from secure configuration.
        Backups made before rotation may still require older keys.
        """
        with self._connection() as conn:
            entries=conn.execute("SELECT user_id, encrypted_payload FROM birth_profiles").fetchall()
            rotations=[(self._crypto.rotate(row[1]),row[0]) for row in entries]
            for encrypted, user_id in rotations:
                conn.execute("UPDATE birth_profiles SET encrypted_payload=? WHERE user_id=?",(encrypted,user_id))
        return len(rotations)

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

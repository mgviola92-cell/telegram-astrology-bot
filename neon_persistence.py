"""Low-query encrypted Neon persistence for the Render Free astrology bot.

Profiles require explicit user consent, and only a Fernet-encrypted
birth_date is sent to PostgreSQL. No names, photos, birth-location
coordinates, raw birth dates or astrology predictions are database columns.

Group preferences store one row only for *disabled* groups. Both classes
use short-lived TLS connections, no scheduled queries, no background
polling and no large connection pool. If Neon is unavailable, group
calendar browsing fails closed rather than accidentally enabling a
previously disabled group's calendar.
"""
import json
import os
import time
from collections import OrderedDict
from datetime import date
from threading import RLock
from urllib.parse import urlsplit, parse_qs

import psycopg
from cryptography.fernet import Fernet, InvalidToken


def verified_neon_url(url: str) -> str:
    """Require Neon-hosted TLS connection; never include URLs in errors."""
    if not isinstance(url,str) or not url or len(url)>2048:
        raise ValueError("Neon database URL is missing or invalid")
    try:
        parts=urlsplit(url)
        query=parse_qs(parts.query)
        valid=(parts.scheme in ("postgresql","postgres")
               and bool(parts.username) and bool(parts.password)
               and parts.hostname is not None
               and parts.hostname.endswith(".neon.tech")
               and (query.get("sslmode") or [""])[-1] in ("require","verify-ca","verify-full"))
    except (ValueError,TypeError,AttributeError):
        valid=False
    if not valid:
        raise ValueError("Neon connection requires a postgres URL with TLS and credentials")
    return url


class NeonBirthStore:
    """Encrypted, explicit-consent date-only profile storage."""

    def __init__(self, database_url: str, encryption_key: str, *, now=None):
        self._dsn=verified_neon_url(database_url)
        if not isinstance(encryption_key,str) or not encryption_key:
            raise ValueError("A Fernet encryption key is required")
        try:
            self._crypto=Fernet(encryption_key.encode("ascii"))
        except (ValueError,TypeError,UnicodeError) as exc:
            raise ValueError("Invalid Fernet encryption key") from exc
        self._now=now or (lambda:int(time.time()))

    def _connect(self):
        return psycopg.connect(self._dsn,connect_timeout=8)

    @staticmethod
    def _check_user(user_id):
        if type(user_id) is not int or user_id<=0 or user_id>=2**63:
            raise ValueError("A positive Telegram user ID is required")

    def save(self,user_id,profile,*,explicit_consent=False):
        self._check_user(user_id)
        if explicit_consent is not True:
            raise PermissionError("Explicit birth-data consent is required")
        if type(profile) is not dict or set(profile)!={"birth_date"}:
            raise ValueError("Only a birth_date can be saved with this command")
        raw=profile["birth_date"]
        if type(raw) is not str or len(raw)!=10:
            raise ValueError("Birth date must be canonical YYYY-MM-DD")
        try:
            born=date.fromisoformat(raw)
        except (ValueError,TypeError) as exc:
            raise ValueError("Invalid birth date") from exc
        if born.isoformat()!=raw or born>date.today():
            raise ValueError("Invalid or future birth date")
        cipher=self._crypto.encrypt(json.dumps(
            {"birth_date":raw},separators=(",",":")).encode("utf-8"))
        now=int(self._now())
        with self._connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO astrology_birth_profiles "
                    "(user_id,encrypted_payload,updated_unix,consent_unix) "
                    "VALUES (%s,%s,%s,%s) "
                    "ON CONFLICT (user_id) DO UPDATE SET "
                    "encrypted_payload=EXCLUDED.encrypted_payload,"
                    "updated_unix=EXCLUDED.updated_unix,"
                    "consent_unix=EXCLUDED.consent_unix",
                    (user_id,cipher,now,now),
                )

    def read(self,user_id):
        self._check_user(user_id)
        with self._connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT encrypted_payload FROM astrology_birth_profiles "
                    "WHERE user_id=%s",(user_id,))
                row=cursor.fetchone()
        if row is None:
            return None
        try:
            record=json.loads(self._crypto.decrypt(bytes(row[0])).decode("utf-8"))
        except (InvalidToken,ValueError,UnicodeDecodeError) as exc:
            raise ValueError("Encrypted profile could not be decrypted") from exc
        if (type(record) is not dict or set(record)!={"birth_date"}
                or type(record["birth_date"]) is not str):
            raise ValueError("Invalid saved birth profile")
        return record

    def delete(self,user_id):
        self._check_user(user_id)
        with self._connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM astrology_birth_profiles WHERE user_id=%s",
                               (user_id,))
                return cursor.rowcount>0


class NeonGroupCalendarSettings:
    """Persistent per-group disabled flags, in a single short DB query."""

    def __init__(self,database_url:str,*,limit:int=1024):
        self._dsn=verified_neon_url(database_url)
        if type(limit) is not int or limit<=0:
            raise ValueError("Positive group cache capacity required")
        self._cache=OrderedDict()
        self._lock=RLock()
        self.limit=limit

    @property
    def persistent(self):
        return True

    @staticmethod
    def _check_chat(chat_id):
        if type(chat_id) is not int or chat_id>=0 or chat_id<=-(2**63):
            raise ValueError("Expected a negative Telegram group ID")

    def _connect(self):
        return psycopg.connect(self._dsn,connect_timeout=8)

    def _remember(self,chat_id,enabled):
        if chat_id in self._cache:
            del self._cache[chat_id]
        elif len(self._cache)>=self.limit:
            self._cache.popitem(last=False)
        self._cache[chat_id]=enabled

    def enabled(self,chat_id):
        self._check_chat(chat_id)
        with self._lock:
            if chat_id in self._cache:
                self._cache.move_to_end(chat_id)
                return self._cache[chat_id]
            try:
                with self._connect() as conn:
                    with conn.cursor() as cursor:
                        cursor.execute(
                            "SELECT enabled FROM astrology_group_settings WHERE chat_id=%s",
                            (chat_id,))
                        row=cursor.fetchone()
            except psycopg.Error:
                # A DB outage must not bypass a group's previously configured
                # disabled calendar setting. Do not cache outage results.
                return False
            state=bool(row[0]) if row is not None else True
            self._remember(chat_id,state)
            return state

    def set_enabled(self,chat_id,enabled,*,expected=None):
        self._check_chat(chat_id)
        if type(enabled) is not bool:
            raise ValueError("enabled must be boolean")
        if expected is not None and type(expected) is not bool:
            raise ValueError("expected must be boolean")
        with self._lock:
            try:
                with self._connect() as conn:
                    with conn.cursor() as cursor:
                        # Do not use cached data when changing admin settings:
                        # stale buttons must compare against persisted state.
                        cursor.execute(
                            "SELECT enabled FROM astrology_group_settings WHERE chat_id=%s",
                            (chat_id,))
                        row=cursor.fetchone()
                        current=bool(row[0]) if row is not None else True
                        if expected is not None and current!=expected:
                            self._remember(chat_id,current)
                            return False
                        if current!=enabled:
                            if enabled:
                                cursor.execute(
                                    "DELETE FROM astrology_group_settings WHERE chat_id=%s",
                                    (chat_id,))
                            else:
                                cursor.execute(
                                    "INSERT INTO astrology_group_settings(chat_id,enabled) "
                                    "VALUES (%s,FALSE) ON CONFLICT(chat_id) "
                                    "DO UPDATE SET enabled=FALSE",(chat_id,))
            except psycopg.Error as exc:
                # Existing caller catches OSError and shows a private error
                # to the admin; do not echo the DB exception or secrets.
                raise OSError("Persistent group settings temporarily unavailable") from None
            self._remember(chat_id,enabled)
            return True

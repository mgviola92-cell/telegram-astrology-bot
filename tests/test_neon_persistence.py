"""Neon schema-safe SQL, no plaintext and opt-in behavior unit checks.

All fake database operations are local mocks; no secret or network needed.
"""
import unittest
from unittest.mock import patch,MagicMock
from cryptography.fernet import Fernet
from neon_persistence import NeonBirthStore,NeonGroupCalendarSettings,verified_neon_url

DSN="postgresql://astrology_user:NONLIVE@ep-example.us-west-2.aws.neon.tech/astrology_db?sslmode=require"
KEY=Fernet.generate_key().decode()

class DummyCursor:
    def __init__(self,answers=None):
        self.calls=[]
        self.answers=iter(answers or [])
        self.rowcount=1
    def __enter__(self):return self
    def __exit__(self,*exc):return False
    def execute(self,sql,params):
        self.calls.append((sql,params))
    def fetchone(self):
        return next(self.answers,None)

class DummyConn:
    def __init__(self,cursor):
        self.cursor_obj=cursor
    def __enter__(self):return self
    def __exit__(self,*exc):return False
    def cursor(self):return self.cursor_obj

class NeonPersistenceTests(unittest.TestCase):
    def test_require_tls_neon_domain_and_credentials(self):
        self.assertEqual(verified_neon_url(DSN),DSN)
        for bad in ("","postgres://user:pass@other.com/db?sslmode=require",
                    "postgresql://user:pass@ep-example.neon.tech/db",
                    "postgresql://user@ep-example.neon.tech/db?sslmode=require",
                    "postgresql://user:pass@ep-example.neon.tech/db?sslmode=disable"):
            with self.subTest(dsn=bad),self.assertRaises(ValueError):
                verified_neon_url(bad)

    def test_encrypted_save_and_decrypt_read_without_plaintext_sql(self):
        store=NeonBirthStore(DSN,KEY,now=lambda:900)
        write=DummyCursor()
        with patch.object(store,"_connect",return_value=DummyConn(write)):
            with self.assertRaises(PermissionError):
                store.save(100,{"birth_date":"2005-12-23"})
            store.save(100,{"birth_date":"2005-12-23"},explicit_consent=True)
        self.assertEqual(len(write.calls),1)
        sql,params=write.calls[0]
        self.assertIn("ON CONFLICT",sql)
        self.assertNotIn("2005",sql)
        self.assertNotIn(b"2005",params[1])
        self.assertEqual(params[0],100)
        self.assertEqual(params[2:],(900,900))
        sealed=bytes(params[1])
        read=DummyCursor([(sealed,)])
        with patch.object(store,"_connect",return_value=DummyConn(read)):
            self.assertEqual(store.read(100),{"birth_date":"2005-12-23"})
        self.assertEqual(read.calls[0][1],(100,))

    def test_delete_and_missing_and_privacy_constraints(self):
        store=NeonBirthStore(DSN,KEY)
        for val in (0,-1,True,2**63,"100"):
            with self.assertRaises(ValueError):
                store.read(val)
        for p in ({"birth_date":"2005-12-23","name":"Alice"},
                  {"birth_date":"2035-01-01"},
                  {"birth_date":"2005-2-3"}):
            with self.assertRaises(ValueError):
                store.save(1,p,explicit_consent=True)
        with patch.object(store,"_connect",return_value=DummyConn(DummyCursor([]))):
            self.assertIsNone(store.read(123))
            self.assertTrue(store.delete(123))

    def test_group_disabled_flag_persists_and_stale_admin_action_denied(self):
        gs=NeonGroupCalendarSettings(DSN,limit=2)
        status=DummyCursor([(False,)])
        with patch.object(gs,"_connect",return_value=DummyConn(status)):
            self.assertFalse(gs.enabled(-100))
        self.assertFalse(gs.enabled(-100))
        self.assertEqual(len(status.calls),1)
        newer=DummyCursor([(False,)])
        with patch.object(gs,"_connect",return_value=DummyConn(newer)):
            self.assertFalse(gs.set_enabled(-100,False,expected=True))
        self.assertEqual(len(newer.calls),1)
        changed=DummyCursor([(False,)])
        with patch.object(gs,"_connect",return_value=DummyConn(changed)):
            self.assertTrue(gs.set_enabled(-100,True,expected=False))
        self.assertEqual(len(changed.calls),2)
        self.assertIn("DELETE",changed.calls[1][0])
        self.assertTrue(gs.enabled(-100))

    def test_group_default_and_toggle_sql_parameterized(self):
        gs=NeonGroupCalendarSettings(DSN)
        with patch.object(gs,"_connect",return_value=DummyConn(DummyCursor([]))):
            self.assertTrue(gs.enabled(-200))
        disabled=DummyCursor([])
        with patch.object(gs,"_connect",return_value=DummyConn(disabled)):
            self.assertTrue(gs.set_enabled(-200,False,expected=True))
        self.assertEqual(len(disabled.calls),2)
        self.assertIn("INSERT",disabled.calls[1][0])
        self.assertEqual(disabled.calls[1][1],(-200,))
        self.assertFalse(gs.enabled(-200))
        with self.assertRaises(ValueError):
            gs.enabled(100)

if __name__=="__main__":
    unittest.main()

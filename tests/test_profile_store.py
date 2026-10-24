import sqlite3
import tempfile
import unittest
from pathlib import Path
from cryptography.fernet import Fernet
from profile_store import ProfileStore

class ProfileStoreTests(unittest.TestCase):
 def setUp(self):
    self.tmp=tempfile.TemporaryDirectory()
    self.db=str(Path(self.tmp.name)/"birth_profiles.sqlite3")
    self.key=Fernet.generate_key()
    self.store=ProfileStore(self.db,self.key,now=lambda:1700000000)
    self.birth={"birth_date":"2005-12-23","label":"ကျွန်ုပ်"}
 def tearDown(self):self.tmp.cleanup()
 def test_explicit_consent_required(self):
    with self.assertRaises(PermissionError):self.store.save(123,self.birth)
    self.assertIsNone(self.store.read(123))
 def test_save_read_delete(self):
    self.store.save(123,self.birth,explicit_consent=True)
    self.assertEqual(self.store.read(123),self.birth)
    self.assertTrue(self.store.delete(123))
    self.assertFalse(self.store.delete(123))
    self.assertIsNone(self.store.read(123))
 def test_no_plaintext_birth_data(self):
    self.store.save(123,self.birth,explicit_consent=True)
    with sqlite3.connect(self.db) as conn:
        row=conn.execute("SELECT encrypted_payload FROM birth_profiles").fetchone()[0]
    self.assertNotIn(b"2005-12-23",row)
    self.assertNotIn("2005-12-23".encode(),Path(self.db).read_bytes())
 def test_wrong_key_fails(self):
    self.store.save(123,self.birth,explicit_consent=True)
    wrong=ProfileStore(self.db,Fernet.generate_key())
    with self.assertRaises(ValueError):wrong.read(123)
 def test_update_only_one_record(self):
    self.store.save(123,self.birth,explicit_consent=True)
    self.store.save(123,{"birth_date":"2004-12-23"},explicit_consent=True)
    self.assertEqual(self.store.read(123)["birth_date"],"2004-12-23")
 def test_disallow_unexpected_fields(self):
    with self.assertRaises(ValueError):self.store.save(123,{"birth_date":"2005-12-23","password":"secret"},explicit_consent=True)
 def test_reject_invalid_user(self):
    with self.assertRaises(ValueError):self.store.delete(-1)
 def test_cleanup(self):
    self.store.save(1,self.birth,explicit_consent=True)
    self.assertEqual(self.store.delete_older_than(1700000001),1)
    self.assertIsNone(self.store.read(1))

if __name__=="__main__":unittest.main()

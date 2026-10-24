import unittest
from tarot_sessions import TarotSessions

class SessionTests(unittest.TestCase):
    def setUp(self):
        self.t = [100.0]
        self.sessions = TarotSessions(clock=lambda: self.t[0], ttl=10, max_sessions=2)

    def start_bound(self, owner=10, chat=10):
        token=self.sessions.start(owner,chat)
        self.assertTrue(self.sessions.bind_message(token,owner_id=owner,chat_id=chat,message_id=99))
        return token

    def test_three_distinct_cards(self):
        token=self.start_bound()
        self.assertEqual(len(set(self.sessions._items[token].cards)),3)

    def test_one_use_only(self):
        token=self.start_bound()
        status, card=self.sessions.reveal(token,owner_id=10,chat_id=10,message_id=99,choice=2)
        self.assertEqual(status,'ok')
        self.assertIn(card,self.sessions._items[token].cards)
        self.assertEqual(self.sessions.reveal(token,owner_id=10,chat_id=10,message_id=99,choice=2)[0],'already_used')

    def test_other_user_denied(self):
        token=self.start_bound()
        self.assertEqual(self.sessions.reveal(token,owner_id=11,chat_id=10,message_id=99,choice=0)[0],'unauthorized')

    def test_wrong_message_denied(self):
        token=self.start_bound()
        self.assertEqual(self.sessions.reveal(token,owner_id=10,chat_id=10,message_id=98,choice=0)[0],'unauthorized')

    def test_expiration(self):
        token=self.start_bound()
        self.t[0] += 10
        self.assertEqual(self.sessions.reveal(token,owner_id=10,chat_id=10,message_id=99,choice=0)[0],'expired')

    def test_new_session_invalidates_old(self):
        a=self.start_bound(); self.start_bound()
        self.assertEqual(self.sessions.reveal(a,owner_id=10,chat_id=10,message_id=99,choice=0)[0],'expired')

    def test_bounded(self):
        for i in range(15):
            self.sessions.start(i,i)
        self.assertLessEqual(len(self.sessions._items),2)

    def test_invalid_index(self):
        token=self.start_bound()
        self.assertEqual(self.sessions.reveal(token,owner_id=10,chat_id=10,message_id=99,choice=4)[0],'invalid')

if __name__ == '__main__': unittest.main()

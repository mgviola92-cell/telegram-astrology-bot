import unittest
from tarot_core import DECK
from tarot_meanings import MAJOR, SUITS, RANKS, interpret_tarot_card

class TarotMeaningsTests(unittest.TestCase):
    def test_complete_standard_deck(self):
        self.assertEqual(len(DECK),78)
        self.assertEqual(set(DECK),set(MAJOR)|{f"{r} of {s}" for s in SUITS for r in RANKS})
        for card in DECK:
            with self.subTest(card=card):
                result=interpret_tarot_card(card)
                self.assertTrue(result["theme"])
                self.assertTrue(result["reflection"])
                self.assertFalse(result["is_prediction"])
    def test_unknown_rejected(self):
        for card in ("", "Eleven of Cups", "Ace of Coins", None):
            with self.subTest(card=card),self.assertRaises(ValueError):
                interpret_tarot_card(card)
    def test_distinct_suit_context(self):
        self.assertNotEqual(interpret_tarot_card("Two of Wands")["reflection"],
                            interpret_tarot_card("Two of Cups")["reflection"])
    def test_death_card_is_transition(self):
        self.assertIn("အစသစ်",interpret_tarot_card("Death")["theme"])
if __name__=="__main__":unittest.main()

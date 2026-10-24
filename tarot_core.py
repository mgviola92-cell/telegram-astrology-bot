"""Tarot card drawing with explicit randomness, from a fixed 78-card deck.

Card draws are randomized by design; traditional meanings need a reviewed corpus.
"""
import secrets
from dataclasses import asdict
from astro_core import Evidence

MAJOR = ('The Fool','The Magician','The High Priestess','The Empress','The Emperor','The Hierophant','The Lovers','The Chariot','Strength','The Hermit','Wheel of Fortune','Justice','The Hanged Man','Death','Temperance','The Devil','The Tower','The Star','The Moon','The Sun','Judgement','The World')
SUITS = ('Wands','Cups','Swords','Pentacles')
RANKS = ('Ace','Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Page','Knight','Queen','King')
DECK = MAJOR + tuple(f'{rank} of {suit}' for suit in SUITS for rank in RANKS)
SPREADS = {'single':('The theme',), 'three':('Past','Present','Potential direction')}


def draw_tarot(spread: str = 'single') -> dict:
    if spread not in SPREADS:
        raise ValueError('Unsupported spread')
    deck=list(DECK)
    picks=[]
    for position in SPREADS[spread]:
        index=secrets.randbelow(len(deck))
        picks.append({'position':position,'card':deck.pop(index)})
    evidence=Evidence(rule_id='TAROT-DRAW-001',tradition='78-card tarot',method='cryptographic random draw without replacement',input_assumptions={'spread':spread},derived_facts={'cards':picks},reference='78-card tarot structure; meanings require a separately reviewed rule corpus')
    return {'cards':picks,'evidence':asdict(evidence)}

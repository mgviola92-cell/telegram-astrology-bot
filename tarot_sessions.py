"""Bounded in-memory tarot sessions. No birth data, images, or animation bytes.

Single-process development implementation; multi-worker deployment requires an
atomic shared TTL store.
"""
from dataclasses import dataclass
from threading import RLock
import secrets
import time
from tarot_core import DECK

@dataclass
class Draw:
    owner_id: int
    chat_id: int
    message_id: int | None
    cards: tuple[str, str, str]
    created_at: float
    chosen: int | None = None

class TarotSessions:
    def __init__(self, ttl: int = 600, max_sessions: int = 1000, clock=None):
        if type(ttl) is not int or type(max_sessions) is not int or ttl <= 0 or max_sessions <= 0:
            raise ValueError('Positive TTL and session count required')
        self.ttl, self.max_sessions = ttl, max_sessions
        self._clock = clock or time.monotonic
        self._items: dict[str, Draw] = {}
        self._lock = RLock()

    def _cleanup(self, now: float) -> None:
        for key, val in list(self._items.items()):
            if now - val.created_at >= self.ttl:
                del self._items[key]

    def start(self, owner_id: int, chat_id: int) -> str:
        if type(owner_id) is not int or type(chat_id) is not int or owner_id<=0 or chat_id<=0:
            raise ValueError('Positive owner and chat IDs required')
        with self._lock:
            now = self._clock()
            self._cleanup(now)
            for key, draw in list(self._items.items()):
                if draw.owner_id == owner_id and draw.chat_id == chat_id:
                    del self._items[key]
            if len(self._items) >= self.max_sessions:
                oldest = min(self._items, key=lambda key: self._items[key].created_at)
                del self._items[oldest]
            deck = list(DECK)
            cards = []
            for _ in range(3):
                cards.append(deck.pop(secrets.randbelow(len(deck))))
            token = secrets.token_urlsafe(12)
            while token in self._items:
                token = secrets.token_urlsafe(12)
            self._items[token] = Draw(owner_id, chat_id, None, tuple(cards), now)
            return token

    def bind_message(self, token: str, *, owner_id: int, chat_id: int, message_id: int) -> bool:
        if type(message_id) is not int or message_id <= 0:
            return False
        with self._lock:
            self._cleanup(self._clock())
            draw = self._items.get(token)
            if (draw is None or draw.owner_id != owner_id or draw.chat_id != chat_id
                    or draw.message_id is not None or draw.chosen is not None):
                return False
            draw.message_id = message_id
            return True

    def reveal(self, token: str, *, owner_id: int, chat_id: int, message_id: int, choice: int):
        with self._lock:
            self._cleanup(self._clock())
            draw = self._items.get(token)
            if draw is None:
                return ('expired', None)
            if (draw.owner_id, draw.chat_id, draw.message_id) != (owner_id, chat_id, message_id):
                return ('unauthorized', None)
            if draw.chosen is not None:
                return ('already_used', None)
            if type(choice) is not int or choice not in (0, 1, 2):
                return ('invalid', None)
            draw.chosen = choice
            return ('ok', draw.cards[choice])

    def discard(self, token: str) -> None:
        with self._lock:
            self._items.pop(token, None)

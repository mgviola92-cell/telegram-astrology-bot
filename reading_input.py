"""Ephemeral private-chat input for personal readings; nothing is persisted."""
from datetime import date, time
import re
from time import monotonic

class ReadingInputSessions:
    def __init__(self, ttl=300, limit=500, clock=None):
        if ttl <= 0 or limit <= 0:
            raise ValueError("TTL and limit must be positive")
        self.ttl, self.limit = ttl, limit
        self.clock = clock or monotonic
        self.items = {}

    def _lookup(self, chat_id, user_id):
        key = (chat_id, user_id)
        record = self.items.get(key)
        if record and record["until"] <= self.clock():
            del self.items[key]
            return None
        return record

    def start(self, chat_id, user_id):
        now = self.clock()
        self.items = {k: v for k, v in self.items.items() if v["until"] > now}
        key = (chat_id, user_id)
        if key not in self.items and len(self.items) >= self.limit:
            self.items.pop(min(self.items, key=lambda k: self.items[k]["until"]))
        self.items[key] = {"step": "date", "until": now + self.ttl}

    def step(self, chat_id, user_id):
        found = self._lookup(chat_id, user_id)
        return found["step"] if found else None

    def set_date(self, chat_id, user_id, value, today):
        item = self._lookup(chat_id, user_id)
        if item is None or item["step"] != "date":
            raise ValueError("No active birth date request")
        if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
            raise ValueError("Use YYYY-MM-DD")
        born = date.fromisoformat(value)
        if not 1900 <= born.year <= 2100 or born > today:
            raise ValueError("Invalid date range")
        item.update(step="time", born=born, until=self.clock() + self.ttl)
        return born

    def bind_prompt(self, chat_id, user_id, message_id):
        """Bind the optional-time button to its actual Telegram prompt."""
        item = self._lookup(chat_id, user_id)
        if (item is None or item["step"] != "time"
                or type(message_id) is not int or message_id <= 0):
            return False
        item["prompt_message_id"] = message_id
        return True

    def finish_from_button(self, chat_id, user_id, message_id):
        """Reject stale buttons, including those from a prior reading form."""
        item = self._lookup(chat_id, user_id)
        if (item is None or item["step"] != "time"
                or type(message_id) is not int
                or item.get("prompt_message_id") != message_id):
            raise ValueError("Stale or unbound birth-time button")
        return self.finish(chat_id, user_id, "မသိပါ")

    def finish(self, chat_id, user_id, value):
        item = self._lookup(chat_id, user_id)
        if item is None or item["step"] != "time":
            raise ValueError("No active birth time request")
        if value in ("မသိပါ", "ကျော်မယ်"):
            clock = None
        elif isinstance(value, str) and re.fullmatch(r"\d{2}:\d{2}", value):
            clock = time.fromisoformat(value)
        else:
            raise ValueError("Use HH:MM or skip")
        born = item["born"]
        self.items.pop((chat_id, user_id), None)
        return born, clock

    def cancel(self, chat_id, user_id):
        return self.items.pop((chat_id, user_id), None) is not None

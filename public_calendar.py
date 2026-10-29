"""Stateless group-safe Myanmar calendar cards, with bounded RAM caching.

No birth inputs, database writes, network downloads, scheduled posts, or
background loops. Today is determined in the explicitly named Yangon zone.
An interactive card may show only dates within 3 days of *current* today.
"""
from datetime import date, datetime, timedelta
from functools import lru_cache
from html import escape
from time import monotonic
from zoneinfo import ZoneInfo

from daily_calendar_reading import daily_calendar_reading

YANGON = ZoneInfo("Asia/Yangon")
NEARBY_DAYS = 3

def myanmar_today() -> date:
    return datetime.now(YANGON).date()

def valid_nearby_day(day: date, *, today: date) -> bool:
    return (type(day) is date and type(today) is date
            and 1900 <= day.year <= 2100
            and abs((day-today).days) <= NEARBY_DAYS)

def parse_day_callback(data: str, *, today: date) -> date:
    if not isinstance(data,str) or not data.startswith("calendar:"):
        raise ValueError("Not a public calendar callback")
    raw=data[len("calendar:"):]
    if len(raw)!=10:
        raise ValueError("Date must be exact ISO form")
    day=date.fromisoformat(raw)
    if day.isoformat()!=raw or not valid_nearby_day(day,today=today):
        raise ValueError("Calendar date no longer allowed")
    return day

@lru_cache(maxsize=32)
def public_calendar_text(day: date) -> str:
    """Cache only short static cultural facts for each local day."""
    if type(day) is not date or not 1900<=day.year<=2100:
        raise ValueError("Invalid Myanmar calendar date")
    fact=daily_calendar_reading(day)
    if fact["personalized"] is not False or fact["prediction_supported"] is not False:
        raise ValueError("Public calendar must be impersonal and non-predictive")
    active="၊ ".join(fact["active_labels"]) if fact["active_labels"] else "သီးခြားအမှတ်အသား မတွေ့ပါ"
    content=(
        "<b>မြန်မာရိုးရာ နေ့စဉ်ပြက္ခဒိန်</b>\n"
        "━━━━━━━━━━━━━━\n"
        f"နေ့စွဲ — <b>{escape(fact['date'])}</b> (မြန်မာစံတော်ချိန်)\n"
        f"မြန်မာလ — <b>{escape(fact['myanmar_month'])}</b>\n"
        f"လအဆင့် — {escape(str(fact['moon_phase']))}\n"
        f"ရိုးရာနေ့အမှတ်အသား — {escape(active)}\n"
        f"နဂါးခေါင်းလှည့်ရာ — {escape(fact['nagahle_direction'])}\n"
        f"နက္ခတ် — {escape(fact['nakhat_name'])}\n\n"
        "<i>မြန်မာပြက္ခဒိန်ဆိုင်ရာ ရိုးရာအညွှန်းသာဖြစ်ပြီး "
        "မည်သူတစ်ဦး၏ မွေးဇာတာ သို့မဟုတ် အနာဂတ်ဟောကိန်း မဟုတ်ပါ။</i>"
    )
    if len(content)>1800:
        raise ValueError("Public calendar text too long")
    return content

def day_actions(day: date, *, today: date):
    """Only public dates, no user IDs or private birth dates in callbacks."""
    if not valid_nearby_day(day,today=today):
        raise ValueError("Day outside public navigation window")
    actions=[]
    for label, next_day in (("မနေ့က", day-timedelta(days=1)),
                            ("ယနေ့", today),
                            ("နောက်နေ့", day+timedelta(days=1))):
        if valid_nearby_day(next_day,today=today):
            actions.append((label,"calendar:"+next_day.isoformat()))
    # Prevent duplicated navigation actions at the current day.
    seen=set()
    filtered=[]
    for label,data in actions:
        if data not in seen:
            seen.add(data)
            filtered.append((label,data))
    return filtered

class GroupCalendarGate:
    """One short response per group/cooldown; no Telegram API calls on reject."""
    def __init__(self, seconds=20, capacity=1024, clock=None):
        if type(seconds) not in (float,int) or seconds<=0 or type(capacity) is not int or capacity<=0:
            raise ValueError("Positive group throttle and capacity required")
        self.seconds=seconds
        self.capacity=capacity
        self.clock=clock or monotonic
        self._seen={}

    def allow(self, chat_id: int) -> bool:
        # Telegram group chat IDs are NEGATIVE; never reject them as invalid.
        if type(chat_id) is not int or chat_id>=0:
            return False
        now=self.clock()
        previous=self._seen.get(chat_id)
        if previous is not None and now-previous<self.seconds:
            return False
        if chat_id not in self._seen and len(self._seen)>=self.capacity:
            self._seen.pop(min(self._seen,key=self._seen.get))
        self._seen[chat_id]=now
        return True

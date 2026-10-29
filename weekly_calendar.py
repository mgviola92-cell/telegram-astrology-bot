"""Seven-day Myanmar traditional calendar views without birth data or storage.

The week starts on Monday in Asia/Yangon. Public inline navigation is
limited to the current, previous and next week, revalidated on each click.
All text comes from the existing documented Myanmar daily calculations;
there are no invented auspicious-day rankings, external requests or writes.
"""
from datetime import date, timedelta
from functools import lru_cache
from html import escape

from daily_calendar_reading import daily_calendar_reading

WEEKDAYS = ("တနင်္လာ", "အင်္ဂါ", "ဗုဒ္ဓဟူး", "ကြာသပတေး",
            "သောကြာ", "စနေ", "တနင်္ဂနွေ")

def week_start(day: date) -> date:
    if type(day) is not date:
        raise ValueError("Gregorian calendar date required")
    return day-timedelta(days=day.weekday())

def valid_week(start: date, *, today: date) -> bool:
    if type(start) is not date or type(today) is not date:
        return False
    if start.weekday()!=0 or not 1900 <= start.year <= 2100:
        return False
    current=week_start(today)
    return abs((start-current).days)<=7 and (start-current).days % 7 == 0

def parse_week_callback(value: str, *, today: date) -> date:
    prefix="calendarweek:"
    if not isinstance(value,str) or not value.startswith(prefix):
        raise ValueError("Unknown weekly calendar action")
    raw=value[len(prefix):]
    if len(raw)!=10:
        raise ValueError("Expected one ISO week-start date")
    start=date.fromisoformat(raw)
    if start.isoformat()!=raw or not valid_week(start,today=today):
        raise ValueError("Stale or invalid weekly calendar action")
    return start

def week_actions(start: date, *, today: date) -> list[tuple[str,str]]:
    if not valid_week(start,today=today):
        raise ValueError("Outside the permitted weekly calendar window")
    current=week_start(today)
    options=(
        ("ရှေ့တစ်ပတ်",start-timedelta(days=7)),
        ("ဒီတစ်ပတ်",current),
        ("နောက်တစ်ပတ်",start+timedelta(days=7)),
    )
    selected=[]
    seen=set()
    for label,week in options:
        if valid_week(week,today=today) and week not in seen:
            seen.add(week)
            selected.append((label,"calendarweek:"+week.isoformat()))
    return selected

@lru_cache(maxsize=8)
def week_text(start: date) -> str:
    if type(start) is not date or start.weekday()!=0 or not 1900<=start.year<=2099:
        raise ValueError("Expected supported Monday week start")
    end=start+timedelta(days=6)
    lines=[
        "<b>မြန်မာရိုးရာ ခုနစ်ရက်ပြက္ခဒိန်</b>",
        "━━━━━━━━━━━━━━",
        f"<b>{start.isoformat()} – {end.isoformat()}</b> (မြန်မာစံတော်ချိန်)",
        "",
    ]
    for offset in range(7):
        day=start+timedelta(days=offset)
        fact=daily_calendar_reading(day)
        if fact.get("personalized") is not False or fact.get("prediction_supported") is not False:
            raise ValueError("A public week must never expose personalized predictions")
        labels="၊ ".join(fact["active_labels"]) or "သီးခြားအမှတ်အသား မတွေ့ပါ"
        lines.append(f"<b>{WEEKDAYS[offset]} • {day.isoformat()}</b>")
        lines.append(f"{escape(fact['myanmar_month'])} | {escape(str(fact['moon_phase']))}")
        lines.append(escape(labels))
        lines.append("")
    lines.extend([
        "<i>မြန်မာရိုးရာပြက္ခဒိန်အမှတ်အသားများသာ ဖြစ်ပါတယ်။ "
        "တစ်ရက်ကို အကောင်း/အဆိုး တစ်မျိုးတည်း မဆုံးဖြတ်ပါ။ "
        "ကိုယ်ပိုင်မွေးဇာတာ သို့မဟုတ် အနာဂတ်ဖြစ်ရပ်အာမခံချက် မဟုတ်ပါ။</i>",
    ])
    rendered="\n".join(lines)
    if len(rendered)>4096:
        raise ValueError("Weekly calendar exceeds Telegram message limit")
    return rendered

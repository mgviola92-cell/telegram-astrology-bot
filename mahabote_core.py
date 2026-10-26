"""Seven-house Myanmar Mahabote chart built from mmcal Gregorian conversion.

The method here is the seven-day Mahabote convention, not Vedic astrology.
Traditional Wednesday afternoon Rahu is a separate eight-day weekday label,
not an eighth Mahabote house. It does not change the seven-house placement.
"""
from dataclasses import asdict
from datetime import date, time
from astro_core import Evidence
from myanmar_calendar import calculate_myanmar_calendar, HOUSES

WEEKDAYS = ("စနေ", "တနင်္ဂနွေ", "တနင်္လာ", "အင်္ဂါ",
            "ဗုဒ္ဓဟူး", "ကြာသပတေး", "သောကြာ")
PLANETS = ("Saturn", "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus")
BURMESE_HOUSES = {
    "Binga": "ဘင်္ဂ",
    "Atun": "အထွန်း",
    "Yaza": "ရာဇ",
    "Adipati": "အဓိပတိ",
    "Marana": "မရဏ",
    "Thike": "သိုက်",
    "Puti": "ပုတိ",
}
RULE_ID = "MM-MAHABOTE-SEVEN-HOUSE-001"
SOURCE = "Yan Naing Aye, Myanmar Astrological Calendar Days (2013): (my-wd)%7, wd=Sat 0 to Fri 6"

def calculate_mahabote(local_birth_date: date, birth_time: time | None = None) -> dict:
    """Compute the birth house AND all seven distinct planetary placements."""
    if type(local_birth_date) is not date:
        raise TypeError("Provide local birth date, not an aware datetime")
    if birth_time is not None:
        if not isinstance(birth_time, time) or birth_time.tzinfo is not None:
            raise ValueError("Birth time must be local naive civil time")
    calendar = calculate_myanmar_calendar(local_birth_date)
    my = calendar["myanmar_year"]
    weekday_code = (local_birth_date.weekday() + 2) % 7
    index = (my - weekday_code) % 7
    house = HOUSES[index]
    # Invert each placement: (my - weekday) % 7 == house index.
    placements = {
        h: {
            "weekday_code": (my - i) % 7,
            "weekday": WEEKDAYS[(my - i) % 7],
            "planet": PLANETS[(my - i) % 7],
        }
        for i, h in enumerate(HOUSES)
    }
    if placements[house]["weekday_code"] != weekday_code:
        raise AssertionError("Mahabote chart placement mismatch")
    is_wednesday = local_birth_date.weekday() == 2
    rahu = bool(is_wednesday and birth_time is not None and birth_time.hour >= 12)
    planetary_weekday = (
        "ရာဟု (ဗုဒ္ဓဟူး မွန်းလွဲပိုင်း)" if rahu else
        "ဗုဒ္ဓဟူး (နံနက်ပိုင်း)" if is_wednesday and birth_time is not None else
        WEEKDAYS[weekday_code]
    )
    facts = {
        "myanmar_year": my,
        "weekday_code": weekday_code,
        "house_index": index,
        "birth_house": house,
        "house_placements": placements,
        "rahu_wednesday_afternoon": rahu,
        "eight_day_weekday_label": planetary_weekday,
    }
    evidence = Evidence(
        rule_id=RULE_ID, tradition="Myanmar Mahabote seven-house astrology",
        method="mmcal local Gregorian date -> Myanmar year; weekday Sat=0..Fri=6; (my-wd)%7; invert for seven-house planetary chart",
        input_assumptions={
            "local_birth_date": local_birth_date.isoformat(),
            "local_birth_time": birth_time.isoformat() if birth_time else None,
            "birth_date_is_local": True,
            "eight_day_rahu_separate_from_seven_house_arithmetic": True,
        },
        derived_facts=facts,
        reference=SOURCE + "; https://cool-emerald.blogspot.com/2013/12/myanmar-astrological-calendar-days.html",
    )
    return {
        "myanmar_year": my,
        "weekday_code": weekday_code,
        "weekday": WEEKDAYS[weekday_code],
        "eight_day_weekday_label": planetary_weekday,
        "house_index": index,
        "house": house,
        "house_burmese": BURMESE_HOUSES[house],
        "placements": placements,
        "rahu_wednesday_afternoon": rahu,
        "evidence": asdict(evidence),
    }

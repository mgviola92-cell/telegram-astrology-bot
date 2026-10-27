"""Verify BaZi Da Yun periods from explicitly supplied birth-time inputs.

BaZi Da Yun is a traditional 10-year calendrical classification. The upstream
library requires a binary convention parameter; never infer it from someone's
profile, name or identity, and allow people not to use this optional module.
No fortunes, health prognoses, or promises of future events are generated.
"""
from datetime import datetime
from bazi_core import calculate_bazi
from bazi_luck import calculate_bazi_luck
from reading_facts import reading_facts

RULE_ID = "CHN-BAZI-DAYUN-001"

def verified_dayun_reading(result: dict) -> dict:
    if not isinstance(result, dict):
        raise ValueError("Da Yun result required")
    evidence = result.get("evidence")
    if not isinstance(evidence, dict) or evidence.get("rule_id") != RULE_ID:
        raise ValueError("Da Yun evidence missing or invalid")
    inputs = evidence.get("input_assumptions")
    if not isinstance(inputs, dict):
        raise ValueError("Da Yun source inputs required")
    try:
        birth = datetime.fromisoformat(inputs["birth_wall_clock"])
        method_code = inputs["gender_explicit_library_convention"]
        yun_sect = inputs["yun_sect"]
        day_sect = inputs["day_sect"]
        timezone = inputs["birth_place_timezone"]
        periods = result["periods"]
        if not isinstance(periods, list) or not 1 <= len(periods) <= 12:
            raise ValueError("Unreasonable Da Yun period count")
        natal = calculate_bazi(birth, sect=day_sect, timezone_verified=timezone)
        reading_facts("bazi", natal)
        expected = calculate_bazi_luck(
            birth, gender=method_code, yun_sect=yun_sect,
            day_sect=day_sect, timezone_verified=timezone, cycles=len(periods)
        )
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError("Invalid Da Yun calculation provenance") from exc
    if result != expected:
        raise ValueError("Da Yun cycles do not match the original inputs")
    # Check the direction rule independently of the start-period calculator.
    year_stem = natal["pillars"]["year"][0]
    yang_year = "甲丙戊庚壬".find(year_stem) != -1
    expected_forward = yang_year if method_code == 1 else not yang_year
    if result["forward"] != expected_forward:
        raise ValueError("Da Yun direction does not match stem polarity")
    return {
        "direction": "顺行" if result["forward"] else "逆行",
        "direction_burmese": "ရှေ့စဉ်" if result["forward"] else "နောက်ပြန်စဉ်",
        "first_start_date_local": result["first_start_date_local"],
        "start_offset": result["start_offset"].copy(),
        "periods": [dict(p) for p in periods],
        "rule_id": RULE_ID,
        "method_code": method_code,
        "yun_sect": yun_sect,
        "day_sect": day_sect,
        "prediction_supported": False,
        "age_convention": "East Asian nominal age (not age since last birthday)",
        "caution": "ဒါယွန်းသည် ရိုးရာ ၁၀ နှစ်စက်ဝန်း အမျိုးအစားခွဲခြားမှုသာဖြစ်ပြီး အနာဂတ်ဖြစ်ရပ်များကို အာမခံဟောကြားခြင်း မဟုတ်ပါ။",
    }

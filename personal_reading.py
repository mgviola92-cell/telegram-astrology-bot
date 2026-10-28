"""Private, deterministic personal reading from separately sourced traditions.

This is a side-by-side cultural interpretation, not a combined predictive
formula. No user data is retained; source calculations are independently
rechecked by their respective reading adapters.
"""
from datetime import date, time
from mahabote_core import calculate_mahabote
from mahabote_reading import interpret_mahabote
from astro_core import life_path

def personal_reading(birth_day: date, birth_time: time | None = None) -> dict:
    if type(birth_day) is not date or not 1900 <= birth_day.year <= 2100:
        raise ValueError("Birth day must be a local Gregorian date within 1900-2100")
    if birth_time is not None and (type(birth_time) is not time or birth_time.tzinfo is not None):
        raise ValueError("Birth time must be a local civil clock without timezone")
    chart=calculate_mahabote(birth_day,birth_time)
    interpreted=interpret_mahabote(chart)
    numerology=life_path(birth_day)
    evidence=numerology["evidence"]
    if evidence["rule_id"]!="NUM-PYT-LIFE-PATH-001" or evidence["input_assumptions"]["birth_date"]!=birth_day.isoformat() or evidence["derived_facts"]["life_path"]!=numerology["number"]:
        raise ValueError("Unverified numerology calculation")
    return {
        "birth_date":birth_day.isoformat(),
        "birth_time":birth_time.strftime("%H:%M") if birth_time is not None else None,
        "weekday":chart["eight_day_weekday_label"],
        "myanmar_year":chart["myanmar_year"],
        "house":chart["house_burmese"],
        "mahabote_theme":interpreted["theme"],
        "mahabote_interpretation":interpreted["interpretation"],
        "life_path":numerology["number"],
        "evidence_rule_ids":(
            chart["evidence"]["rule_id"],
            interpreted["interpretation_rule_id"],
            evidence["rule_id"],
        ),
        "synthesis_status":"parallel_methods_no_predictive_combination",
        "prediction_supported":False,
        "profile_saved":False,
    }

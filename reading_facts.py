"""Evidence-consistent, calculation-derived facts for astrology readings.

This is NOT a traditional prediction rule corpus. It verifies that the
result displayed by the bot agrees with the core engine's evidence payload.
Never manufacture a divination interpretation from a rule ID alone.
"""
from evidence_ui import RULES

EXPECTED = {
    "myanmar_calendar": "MM-CALENDAR-MMCAL-001",
    "bazi": "CHN-BAZI-PILLARS-001",
    "numerology": "NUM-PYT-LIFE-PATH-001",
}
CALENDAR_FIELDS = {
    "myanmar_year": "myanmar_year",
    "month": "month",
    "day": "month_day",
    "mahabote": "mahabote_house",
    "yatyaza": "yatyaza",
    "pyathada": "pyathada_type",
}

def require_evidence(kind, result):
    if kind not in EXPECTED or not isinstance(result, dict):
        raise ValueError("Unknown calculation or invalid result")
    evidence = result.get("evidence")
    rule = EXPECTED[kind]
    if (not isinstance(evidence, dict)
            or evidence.get("rule_id") != rule
            or rule not in RULES
            or not isinstance(evidence.get("derived_facts"), dict)
            or not isinstance(evidence.get("input_assumptions"), dict)):
        raise ValueError("Calculation provenance and inputs required")
    return rule

def reading_facts(kind, result):
    """Check inputs, compare returned facts to evidence, and expose facts only."""
    rule = require_evidence(kind, result)
    derived = result["evidence"]["derived_facts"]
    if kind == "bazi":
        pillars = result.get("pillars")
        if (not isinstance(pillars, dict)
                or set(pillars) != {"year", "month", "day", "hour"}
                or any(not isinstance(p, str) or len(p) != 2 for p in pillars.values())
                or derived.get("pillars") != pillars):
            raise ValueError("Four pillars must match the calculated evidence")
        if result.get("day_master") != pillars["day"][0]:
            raise ValueError("Day Master mismatches the Day Pillar")
        facts = {name: pillars[name] for name in ("year", "month", "day", "hour")}
        facts["day_master"] = result["day_master"]
    elif kind == "numerology":
        number = result.get("number")
        if (type(number) is not int
                or number not in set(range(1, 10)) | {11, 22, 33}
                or derived.get("life_path") != number):
            raise ValueError("Life Path must match the calculated evidence")
        facts = {"life_path": number}
    else:
        for field, evidence_field in CALENDAR_FIELDS.items():
            if field not in result or derived.get(evidence_field) != result[field]:
                raise ValueError("Myanmar calendar fact mismatches evidence: " + field)
        if (type(result["myanmar_year"]) is not int
                or type(result["day"]) is not int
                or not 1 <= result["day"] <= 30
                or not isinstance(result["month"], str)
                or not result["month"]
                or type(result["yatyaza"]) is not bool
                or type(result["pyathada"]) is not int
                or result["pyathada"] not in (0, 1, 2)):
            raise ValueError("Invalid Myanmar calendar fact types")
        facts = {key: result[key] for key in CALENDAR_FIELDS}
    return {
        "kind": kind,
        "rule_id": rule,
        "facts": facts,
        "prediction_supported": False,
        "interpretation_status": "calculated_facts_only",
    }

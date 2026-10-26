"""Native Burmese presentation of computed Myanmar calendar date markers.

Only documented, reverified flags become reading labels. The result reports
traditional calendar classifications, not guarantees about specific events.
"""
from datetime import date
from myanmar_day_signals import calculate_day_signals, RULE_ID

BOOLEAN_LABELS = (
    ("sabbath", "ဥပုသ်"),
    ("sabbath_eve", "အဖိတ်"),
    ("yatyaza", "ရက်ရာဇာ"),
    ("thamanyo", "သမားညို"),
    ("amyeittasote", "အမြိတ္တစုတ်"),
    ("warameittugyi", "ဝါရမိတ္တုကြီး"),
    ("warameittunge", "ဝါရမိတ္တုငယ်"),
    ("yatpote", "ရက်ပုပ်"),
    ("thamaphyu", "သမားဖြူ"),
    ("nagapor", "နဂါးပေါ်"),
    ("yatyotema", "ရက်ယုတ်မာ"),
    ("mahayatkyan", "မဟာရက်ကြမ်း"),
    ("shanyat", "ရှမ်းရက်"),
)

def describe_day_signals(signals: dict) -> dict:
    """Reject tampering, then return only the active traditional labels."""
    if not isinstance(signals, dict):
        raise ValueError("Calendar marker calculation required")
    ev=signals.get("evidence")
    assumptions=ev.get("input_assumptions") if isinstance(ev,dict) else None
    if not isinstance(assumptions,dict) or ev.get("rule_id")!=RULE_ID:
        raise ValueError("Calendar marker evidence required")
    try:
        local_day=date.fromisoformat(assumptions["local_gregorian_date"])
        expected=calculate_day_signals(local_day)
    except (KeyError,TypeError,ValueError) as exc:
        raise ValueError("Invalid calendar marker origin date") from exc
    if signals != expected:
        raise ValueError("Displayed calendar markers differ from computed date")
    markers=signals["markers"]
    labels=[name for key,name in BOOLEAN_LABELS if markers[key]]
    if markers["pyathada"]==1:
        labels.append("ပြဿဒါး")
    elif markers["pyathada"]==2:
        labels.append("မွန်းလွဲပြဿဒါး")
    return {
        "active_labels":labels,
        "nagahle_direction":signals["nagahle_direction"],
        "nakhat_name":signals["nakhat_name"],
        "rule_id":RULE_ID,
        "prediction_supported":False,
        "interpretation_status":"calendar_date_categories_only",
        "note":"ဤအမည်များသည် ရိုးရာပြက္ခဒိန်အမှတ်အသားများဖြစ်၍ အနာဂတ်ဖြစ်ရပ်ကို အာမခံမဟုတ်ပါ။",
    }

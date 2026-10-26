"""Rule-based Myanmar calendar day-marker interpretation.

These are conservative descriptions of *traditional date markers*, not
guaranteed events, advice to postpone essential tasks, or a birth prognosis.
Derived from the mmcal date calculation and documented Yatyaza/Pyathada
traditional calendar categories. No random text, AI API, or guesswork.
"""
from reading_facts import reading_facts

TRADITIONAL_DESCRIPTIONS = {
    "yatyaza": "ရက်ရာဇာဟု သတ်မှတ်သည့်နေ့ — မြန်မာရိုးရာပြက္ခဒိန်တွင် အခါကောင်းနေ့အဖြစ် ရည်ညွှန်းလေ့ရှိသည်။",
    "pyathada": "ပြဿဒါးဟု သတ်မှတ်သည့်နေ့ — မြန်မာရိုးရာပြက္ခဒိန်တွင် သတိပြုဖွယ်နေ့အဖြစ် ရည်ညွှန်းလေ့ရှိသည်။",
    "afternoon_pyathada": "မွန်းလွဲပြဿဒါးဟု သတ်မှတ်သည့်နေ့ — နေ့ပိုင်းခွဲခြားချက်ပါဝင်သော ရိုးရာပြက္ခဒိန်အမှတ်အသားဖြစ်သည်။",
    "ordinary": "ဤနေ့တွင် ရက်ရာဇာ သို့မဟုတ် ပြဿဒါး အမှတ်အသား မတွေ့ရပါ။"
}

def calendar_marker_reading(result: dict) -> dict:
    """Only facts checked against core-engine evidence can select rule text."""
    checked = reading_facts("myanmar_calendar", result)
    facts = checked["facts"]
    labels = []
    if facts["yatyaza"]:
        labels.append(("yatyaza", TRADITIONAL_DESCRIPTIONS["yatyaza"]))
    if facts["pyathada"] == 1:
        labels.append(("pyathada", TRADITIONAL_DESCRIPTIONS["pyathada"]))
    elif facts["pyathada"] == 2:
        labels.append(("afternoon_pyathada", TRADITIONAL_DESCRIPTIONS["afternoon_pyathada"]))
    if not labels:
        labels.append(("ordinary", TRADITIONAL_DESCRIPTIONS["ordinary"]))
    return {
        "markers": [{"key":key,"text":text,"rule_id":checked["rule_id"]} for key,text in labels],
        "rule_id":checked["rule_id"],
        "category": "traditional_calendar_day_markers",
        "prediction_supported": False,
        "caution": "ရိုးရာနေ့ရက်အမည်များသည် အနာဂတ်အဖြစ်အပျက်ကို အာမခံမဟုတ်ပါ။ အရေးကြီးဆုံးဖြတ်ချက်များကို သက်ဆိုင်ရာ လက်တွေ့အချက်အလက်များနဲ့အတူ ချိန်ဆပါ။",
    }

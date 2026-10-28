"""Myanmar daily calendar reflection, not an event or fate prediction.

Source marker calculations are recalculated and cross-checked before a
standalone reading is produced. A daily reading has no birth-data dependency
and does not create or update a personal profile.
"""
from datetime import date, datetime
from myanmar_day_signals import calculate_day_signals, RULE_ID
from myanmar_signal_reading import describe_day_signals

DAILY_RULE_ID = "MM-DAILY-CALENDAR-REFLECTION-001"

def daily_calendar_reading(day: date) -> dict:
    if type(day) is not date or not 1900 <= day.year <= 2100:
        raise ValueError("Valid local calendar day between 1900 and 2100 required")
    signals = calculate_day_signals(day)
    interpreted = describe_day_signals(signals)
    markers = signals["markers"]
    labels = list(interpreted["active_labels"])
    # All statements describe calendar categories, not guaranteed outcomes.
    notes = []
    if markers["sabbath"]:
        notes.append("ရိုးရာပြက္ခဒိန်အရ ဥပုသ်နေ့ဖြစ်သည်။")
    elif markers["sabbath_eve"]:
        notes.append("ရိုးရာပြက္ခဒိန်အရ အဖိတ်နေ့ဖြစ်သည်။")
    if markers["yatyaza"]:
        notes.append("ရက်ရာဇာဟု အမည်တပ်သည့် ရိုးရာနေ့အမျိုးအစားပါဝင်သည်။")
    if markers["pyathada"] == 1:
        notes.append("ပြဿဒါးဟု အမည်တပ်သည့် ရိုးရာနေ့အမျိုးအစားပါဝင်သည်။")
    elif markers["pyathada"] == 2:
        notes.append("မွန်းလွဲပြဿဒါးဟု သီးခြားဖော်ပြထားသော ရိုးရာနေ့အမျိုးအစားပါဝင်သည်။")
    if not notes:
        notes.append("ဤနေ့အတွက် အထက်ပါ အဓိကရိုးရာအမှတ်အသားများ မတွေ့ရပါ။")
    return {
        "date": signals["date"],
        "myanmar_month": signals["myanmar_month"],
        "moon_phase": signals["moon_phase"],
        "active_labels": labels,
        "observations": notes,
        "nagahle_direction": interpreted["nagahle_direction"],
        "nakhat_name": interpreted["nakhat_name"],
        "calculation_rule_id": RULE_ID,
        "interpretation_rule_id": DAILY_RULE_ID,
        "prediction_supported": False,
        "personalized": False,
        "note": "ဤဖော်ပြချက်သည် မူရင်းမြန်မာပြက္ခဒိန်ကို အခြေခံသော ယဉ်ကျေးမှုဆိုင်ရာ နေ့စဉ်အညွှန်းသာဖြစ်ပြီး ကိုယ်ပိုင်ကံကြမ္မာ၊ အနာဂတ်ဖြစ်ရပ် သို့မဟုတ် ဆုံးဖြတ်ချက်ရလဒ်ကို မခန့်မှန်းပါ။",
    }

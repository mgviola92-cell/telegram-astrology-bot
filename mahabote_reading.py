"""Editorial Burmese symbolic themes selected by a verified Mahabote house.

The seven thematic descriptions are original summaries of differing Myanmar
Mahabote teaching conventions. They are not empirical future predictions.
Calculation and interpretive convention have SEPARATE rule identifiers.
"""
from datetime import date, time
from mahabote_core import calculate_mahabote, BURMESE_HOUSES, RULE_ID

THEME_RULE_ID = "MM-MAHABOTE-SYMBOLIC-THEMES-001"
THEMES = {
    "Binga": (
        "ပြောင်းလဲမှုနှင့် အသစ်တစ်ဖန်စတင်ခြင်း",
        "ဘင်္ဂအိမ်ကို ရိုးရာအနက်ဖွင့်ရာတွင် တည်မြဲမှုမရှိခြင်းနှင့် အလှည့်အပြောင်းများ၏ သင်္ကေတအဖြစ် ဖတ်ကြသည်။ အခြေအနေပြောင်းသည့်အခါ အရေးပါရာကို ပြန်ရွေးချယ်ခြင်းဆိုသည့် သဘောဖြင့် ဆင်ခြင်နိုင်သည်။",
    ),
    "Atun": (
        "ထွန်းပေါက်မှုနှင့် ထင်ရှားခြင်း",
        "အထွန်းအိမ်ကို လူသိများလာခြင်း၊ ကြိုးပမ်းမှု၏အသိအမှတ်ပြုခံရခြင်းတို့နှင့် ဆက်စပ်ဖော်ပြသော ရိုးရာကျောင်းများရှိသည်။ မိမိလုပ်ဆောင်ချက်၏ အနှစ်သာရကို စဉ်းစားကြည့်ရန် အနက်ဖွင့်နိုင်သည်။",
    ),
    "Yaza": (
        "ရာထူးဂုဏ်သိက္ခာနှင့် တာဝန်",
        "ရာဇအိမ်ကို ရိုးရာအရ ရာထူး၊ ဂုဏ်သိက္ခာနှင့် လူမှုရပ်တည်မှုတို့၏ သင်္ကေတအဖြစ် ဖတ်ကြသည်။ အခြားသူများနှင့် ဆက်ဆံရာတွင် တာဝန်ယူမှုကို တွေးဆရန် ရိုးရာအနက်အဖြစ် ယူနိုင်သည်။",
    ),
    "Adipati": (
        "ဦးဆောင်မှုနှင့် စီမံခန့်ခွဲခြင်း",
        "အဓိပတိအိမ်ကို စီမံခန့်ခွဲမှု၊ ဦးဆောင်မှု၊ ဆုံးဖြတ်ချက်ချမှုတို့၏ သင်္ကေတအဖြစ် ဖတ်လေ့ရှိသည်။ အာဏာထက် တာဝန်ကို ဘယ်လိုထမ်းဆောင်မလဲဆိုတာ ဆင်ခြင်စရာအဖြစ် ယူနိုင်သည်။",
    ),
    "Marana": (
        "အဆုံးသတ်မှုနှင့် ပြန်လည်ပြောင်းလဲခြင်း",
        "မရဏဟူသော ရိုးရာအမည်ကို ဘဝအန္တရာယ်အတွက် တိကျသော ဟောကိန်းဟု မဖတ်သင့်ပါ။ ဤအိမ်ကို အဟောင်းကိုအဆုံးသတ်ခြင်း၊ စနစ်ဟောင်းမှ ပုံစံသစ်သို့ ပြောင်းလဲခြင်းတို့၏ သင်္ကေတအဖြစ် ဆင်ခြင်နိုင်သည်။",
    ),
    "Thike": (
        "စုဆောင်းမှုနှင့် အရင်းအမြစ်ထိန်းသိမ်းခြင်း",
        "သိုက်အိမ်ကို ဥစ္စာ၊ အရင်းအမြစ်၊ စုဆောင်းထိန်းသိမ်းမှုတို့နှင့် ဆက်စပ်ဖတ်ကြသည်။ အိမ်၊ မိသားစုနှင့် ကိုယ့်မှာရှိသောအရာများ၏ တန်ဖိုးကို ပြန်လည်သုံးသပ်ရန် အနက်ဖွင့်နိုင်သည်။",
    ),
    "Puti": (
        "စိတ်ရှည်မှုနှင့် ပြန်လည်ပြုပြင်ခြင်း",
        "ပုတိအိမ်ကို ရိုးရာကျောင်းအချို့က အားနည်းချက်နှင့် အခက်အခဲဆိုင်ရာ သင်္ကေတအဖြစ် ဖော်ပြကြသည်။ ၎င်းသည် လူတစ်ဦး၏ ကျန်းမာရေး၊ အရည်အချင်း သို့မဟုတ် အနာဂတ်ကို အဆုံးအဖြတ်မပေးဘဲ စိတ်ရှည်စွာ ပြန်လည်ပြုပြင်ခြင်းကို ဆင်ခြင်စရာအဖြစ် ယူနိုင်သည်။",
    ),
}

def interpret_mahabote(chart: dict) -> dict:
    if not isinstance(chart, dict):
        raise ValueError("Mahabote chart required")
    ev = chart.get("evidence")
    if not isinstance(ev, dict) or ev.get("rule_id") != RULE_ID:
        raise ValueError("Mahabote calculation evidence required")
    assumptions = ev.get("input_assumptions")
    if not isinstance(assumptions, dict):
        raise ValueError("Mahabote calculation inputs required")
    try:
        date_input = date.fromisoformat(assumptions["local_birth_date"])
        time_input = time.fromisoformat(assumptions["local_birth_time"]) if assumptions.get("local_birth_time") else None
        expected = calculate_mahabote(date_input, time_input)
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError("Invalid Mahabote source date/time") from exc
    fields = ("myanmar_year", "weekday_code", "weekday", "house_index",
              "house", "house_burmese", "placements", "eight_day_weekday_label",
              "rahu_wednesday_afternoon", "evidence")
    if any(chart.get(field) != expected[field] for field in fields):
        raise ValueError("Mahabote chart differs from its verified birth date")
    house = chart["house"]
    if house not in BURMESE_HOUSES:
        raise ValueError("Unrecognized Mahabote house")
    title, explanation = THEMES[house]
    return {
        "house": house,
        "house_burmese": BURMESE_HOUSES[house],
        "theme": title,
        "interpretation": explanation,
        "calculation_rule_id": RULE_ID,
        "interpretation_rule_id": THEME_RULE_ID,
        "prediction_supported": False,
        "interpretation_status": "traditional_symbolic_editorial_convention",
        "disclaimer": "အိမ်အမည်နှင့် ရိုးရာသင်္ကေတများသည် အနာဂတ်ဖြစ်ရပ်ကို အာမခံမဟုတ်ပါ။ ဆရာနှင့် ကျောင်းအလိုက် ဖတ်ပုံကွဲပြားနိုင်သည်။",
    }

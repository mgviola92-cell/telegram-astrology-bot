"""Source-attributed Hellenistic annual profection symbolic reading.

This module never calculates a rising sign, natal chart, transits, sect,
planetary dignity or an event forecast. House topics are original Burmese
educational glosses of the conventional Whole Sign house vocabulary.
Source: Chris Brennan, Hellenistic Astrology (2017), annual profections;
The Astrology Podcast episode 153 (2018):
https://theastrologypodcast.com/2018/04/26/annual-profections-a-basic-time-lord-technique/
"""
from datetime import date
from html import escape

from astro_core import SIGNS, TRADITIONAL_RULERS
from profection_reading import HOUSE_TOPICS_BURMESE, RULE_ID, profection_reading

TOPIC_RULE_ID="WEST-HEL-PROFECTION-HOUSE-TOPICS-001"
# Indexed one-based, in whole-sign house order. Editorial summaries, not
# hard claims about the user's experiences in the selected year.
HOUSE_THEMES={
    1:("မိမိ၏ရပ်တည်မှု","မိမိကိုယ်ကို ဖော်ပြပုံ၊ အစပြုခြင်းနှင့် ကိုယ်ပိုင်အခန်းကဏ္ဍတို့ကို ရိုးရာအိမ်ခေါင်းစဉ်အဖြစ် ဖတ်သည်။"),
    2:("ပိုင်ဆိုင်မှုနှင့် တန်ဖိုး","ကိုယ်ပိုင်ပစ္စည်း၊ အသုံးစရိတ်နှင့် ကိုယ်တိုင်တန်ဖိုးထားရာအရင်းအမြစ်များကို သင်္ကေတအရ ညွှန်းသည်။"),
    3:("ဆက်သွယ်မှုနှင့် သင်ယူခြင်း","ညီအစ်ကိုမောင်နှမ၊ နီးစပ်ရာပတ်ဝန်းကျင်၊ စာရေးပြောဆိုမှုနှင့် နေ့စဉ်သင်ယူမှုတို့ကို ညွှန်းသည်။"),
    4:("အိမ်နှင့် အခြေခံအုတ်မြစ်","နေထိုင်ရာ၊ မိသားစုသမိုင်းနှင့် မိမိပိုင်ဆိုင်သော အခြေခံနေရာတို့၏ ရိုးရာသင်္ကေတဖြစ်သည်။"),
    5:("ဖန်တီးမှုနှင့် ပျော်ရွှင်ခြင်း","ဖန်တီးရေး၊ ကစားမှု၊ ဝါသနာနှင့် အပန်းဖြေမှုတို့ကို ဤအိမ်၏ ရိုးရာခေါင်းစဉ်များအဖြစ် ဖတ်သည်။"),
    6:("နေ့စဉ်တာဝန်နှင့် ဝန်ဆောင်မှု","နေ့စဉ်လုပ်ငန်း၊ လုပ်ရိုးလုပ်စဉ်နှင့် ကူညီဝန်ဆောင်ရသော တာဝန်များကို ညွှန်းသည်။ ကျန်းမာရေးရလဒ်ကို မဟောပါ။"),
    7:("မိတ်ဖက်နှင့် သဘောတူညီမှု","မိတ်ဖက်မှု၊ သဘောတူစာချုပ်၊ တစ်ဦးနှင့်တစ်ဦး ညှိနှိုင်းဆက်ဆံမှုတို့ကို အိမ်ခေါင်းစဉ်အဖြစ် ဖတ်သည်။"),
    8:("မျှဝေထားသောအရင်းအမြစ်","အခြားသူနှင့် ဆက်နွယ်သောပိုင်ဆိုင်မှု၊ အကြွေးဆိုင်ရာတာဝန်နှင့် ပူးတွဲစီမံမှုတို့၏ သင်္ကေတဖြစ်သည်။"),
    9:("မြင့်မားသောပညာနှင့် အမြင်ကျယ်မှု","ဒဿန၊ ယုံကြည်ချက်များကို လေ့လာခြင်း၊ ဝေးလံခရီးနှင့် ပညာဆိုင်ရာစူးစမ်းမှုကို ညွှန်းသည်။"),
    10:("လူမှုအခန်းကဏ္ဍနှင့် တာဝန်","အလုပ်အကိုင်၏ အများမြင်ရသောအခန်းကဏ္ဍ၊ တာဝန်ယူမှုနှင့် လူမှုရပ်တည်မှုကို ရိုးရာခေါင်းစဉ်အဖြစ် ဖတ်သည်။"),
    11:("မိတ်ဆွေများနှင့် မျှော်မှန်းချက်","အသိုင်းအဝိုင်း၊ ပူးပေါင်းလုပ်ဆောင်မှုနှင့် အနာဂတ်ရည်ရွယ်ချက်များအတွက် ရိုးရာသင်္ကေတအညွှန်းဖြစ်သည်။"),
    12:("အတွင်းပိုင်းအလုပ်နှင့် တစ်ကိုယ်တည်းအချိန်","တိတ်ဆိတ်စွာ အတွေးစုစည်းခြင်း၊ နောက်ကွယ်လုပ်ငန်းများနှင့် တစ်ယောက်တည်းနားနေချိန်တို့ကို ခေါင်းစဉ်အဖြစ် ဖတ်သည်။"),
}

def interpret_profection(calculated:dict)->dict:
    """Recompute source evidence before mapping the activated house topic."""
    if type(calculated) is not dict:
        raise ValueError("A calculated profection reading is required")
    ev=calculated.get("evidence")
    assumptions=ev.get("input_assumptions") if type(ev) is dict else None
    if (type(assumptions) is not dict or ev.get("rule_id")!=RULE_ID
            or assumptions.get("ascendant_verified_external") is not False):
        raise ValueError("Original profection provenance is required")
    try:
        birth_raw=assumptions["birth_date"]
        eval_raw=assumptions["evaluation_date"]
        rising=assumptions["ascendant_sign"]
        birth=date.fromisoformat(birth_raw)
        evaluated=date.fromisoformat(eval_raw)
        if (type(birth_raw) is not str or type(eval_raw) is not str
                or birth.isoformat()!=birth_raw or evaluated.isoformat()!=eval_raw):
            raise ValueError("Dates must be canonical ISO")
        expected=profection_reading(birth,evaluated,rising)
    except (KeyError,TypeError,ValueError) as exc:
        raise ValueError("Invalid profection source details") from exc
    if calculated!=expected:
        raise ValueError("Reported profection differs from recalculated date/sign")
    house=expected["house"]
    if set(HOUSE_THEMES)!=set(range(1,13)) or len(HOUSE_TOPICS_BURMESE)!=12:
        raise ValueError("Profection house topic table incomplete")
    title,description=HOUSE_THEMES[house]
    next_sign=SIGNS[(SIGNS.index(expected["sign"])+1)%12]
    return {
        "house":house,
        "topic_title":title,
        "interpretation":description,
        "house_topic_burmese":expected["house_topic_burmese"],
        "age_completed":expected["age_completed"],
        "next_house":house%12+1,
        "next_sign":next_sign,
        "next_traditional_ruler":TRADITIONAL_RULERS[SIGNS.index(next_sign)],
        "calculation_rule_id":RULE_ID,
        "interpretation_rule_id":TOPIC_RULE_ID,
        "traditional_ruler":expected["lord_of_year"],
        "rising_sign_not_computed":True,
        "natal_planet_conditions_checked":False,
        "transits_checked":False,
        "prediction_supported":False,
        "interpretation_status":"educational_house_topics_no_event_forecast",
    }

def render_profection_report(calculated:dict,read:dict)->str:
    if read!=interpret_profection(calculated):
        raise ValueError("Profection reading differs from verified house")
    lines=[
        "<b>Western Annual Profection</b>",
        "━━━━━━━━━━━━━━",
        f'အသက်ပြည့်နှစ် — <b>{read["age_completed"]}</b>',
        f'နှစ်တိုင်အိမ် — <b>{read["house"]}</b>',
        f'အသက်ဝင်ရာသီ — <b>{escape(calculated["sign"])}</b>',
        f'Lord of the Year — <b>{escape(calculated["lord_of_year"])}</b>',
        "",
        "<b>ရိုးရာအိမ်ဆိုင်ရာ အဓိပ္ပာယ်</b>",
        f'<b>{escape(read["topic_title"])}</b>',
        escape(read["interpretation"]),
        "",
        "<b>နှစ်စက်ဝန်း နောက်တစ်ဆင့်</b>",
        f'လာမည့်မွေးနေ့ပြီးနောက် အိမ် {read["next_house"]} — '
        f'{escape(read["next_sign"])} / {escape(read["next_traditional_ruler"])}',
        "အိမ် ၁၂ လုံးစက်ဝန်းသည် ၁၂ နှစ်တစ်ကြိမ် ပြန်စသည်။",
        "",
        f'Rising Sign: <code>{escape(calculated["rising_sign_input"])}</code> '
        '(အသုံးပြုသူပေးထားသည်၊ ဤနေရာတွင် မတွက်/မစစ်ရသေးပါ)',
        "<i>Lord of the Year သည် ရိုးရာဂြိုဟ်အုပ်စိုးသူအမည်ဖြစ်သည်။ "
        "Natal ဂြိုဟ်တည်နေရာ၊ ထောင့်ဆက်သွယ်မှုနှင့် Transits မစစ်ရသေးပါ။ "
        "ဤသည် ရိုးရာအိမ်ခေါင်းစဉ်ဖတ်ရှုမှုသာဖြစ်ပြီး အနာဂတ်ဖြစ်ရပ်ကို အာမခံမဟုတ်ပါ။ "
        "မွေးအချက်အလက်ကို ဒီ Command က Database ထဲ မသိမ်းပါ။</i>",
    ]
    txt="\n".join(lines)
    if len(txt)>4096:
        raise ValueError("Telegram profection message too long")
    return txt

def profection_house_glossary()->str:
    """Static, non-personal 12-house reference without birth details."""
    lines=[
        "<b>Annual Profection — အိမ် ၁၂ လုံး လေ့လာခန်း</b>",
        "━━━━━━━━━━━━━━",
        "အသက် ၀ နှစ်တွင် အိမ် ၁ မှ စတင်၍ မွေးနေ့တိုင်း တစ်အိမ်တိုးသည်။ "
        "၁၂ နှစ်ပြည့်တိုင်း အိမ် ၁ သို့ ပြန်လည်ရောက်ရှိသည်။",
        "",
    ]
    for number,(title,_) in HOUSE_THEMES.items():
        lines.append(f"<b>အိမ် {number}</b> — {escape(title)}")
    lines.extend([
        "",
        "<i>ဤစာရင်းသည် House Topics အတွက် သင်္ကေတခေါင်းစဉ်များသာဖြစ်သည်။ "
        "မွေးဇာတာ၊ Rising Sign သို့မဟုတ် အနာဂတ်ဟောချက် မပါဝင်ပါ။</i>",
        "<i>မြင့်မားသောအသေးစိတ်ဖတ်ရှုမှုတွင် Natal အခြေအနေ၊ Sect၊ "
        "Ruler နှင့် Transits ကို ထပ်စစ်ရသော်လည်း ဤ Bot က မတွက်သေးပါ။</i>",
    ])
    text="\n".join(lines)
    if len(text)>4096:
        raise ValueError("House glossary exceeds Telegram limit")
    return text

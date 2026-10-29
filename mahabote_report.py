"""Seven-house Myanmar Mahabote: source-checked, private Telegram report.

Calculation facts are independently re-checked by interpret_mahabote.
Other houses are a glossary of traditional school-dependent symbols, NOT
independent predictions about the user's planets, relationships or health.
Nothing is persisted, fetched or rendered as a file.
"""
from html import escape
from mahabote_core import BURMESE_HOUSES, HOUSES
from mahabote_reading import THEMES, interpret_mahabote

PLANET_NAMES = {
    "Saturn":"စနေဂြိုဟ်",
    "Sun":"နေဂြိုဟ်",
    "Moon":"လဂြိုဟ်",
    "Mars":"အင်္ဂါဂြိုဟ်",
    "Mercury":"ဗုဒ္ဓဟူးဂြိုဟ်",
    "Jupiter":"ကြာသပတေးဂြိုဟ်",
    "Venus":"သောကြာဂြိုဟ်",
}
MAX_TELEGRAM_TEXT=4096

def render_mahabote_report(chart: dict, reading: dict) -> str:
    """Build one full report from a cryptographically untrusted input dict.

    No birth date is passed to callback buttons or any persistence layer.
    Verify all supplied chart facts against the birth-date evidence before
    displaying meanings, then separate birth-house interpretation and
    other houses' educational vocabulary.
    """
    if type(chart) is not dict or type(reading) is not dict:
        raise ValueError("Verified Mahabote chart and interpretation required")
    confirmed=interpret_mahabote(chart)
    if reading!=confirmed:
        raise ValueError("Mahabote interpretation does not match verified calculation")
    if set(chart["placements"])!=set(HOUSES):
        raise ValueError("Seven unique houses required")
    if set(THEMES)!=set(HOUSES):
        raise ValueError("Mahabote house meanings incomplete")
    lines=[
        "<b>မြန်မာမဟာဘုတ် — မွေးဇာတာ ၇ အိမ်</b>",
        "━━━━━━━━━━━━━━",
        f"မြန်မာသက္ကရာဇ် — <b>{chart['myanmar_year']}</b>",
        f"မွေးနေ့နံ — <b>{escape(chart['eight_day_weekday_label'])}</b>",
        f"မဟာဘုတ်အကြွင်း — <b>{chart['house_index']}</b>",
        f"ဖွားအိမ် — <b>{escape(chart['house_burmese'])}</b>",
        "",
        "<b>အိမ် ၇ လုံး၏ ဂြိုဟ်နံချထားမှု</b>",
    ]
    for house in HOUSES:
        entry=chart["placements"][house]
        if entry["planet"] not in PLANET_NAMES:
            raise ValueError("Unrecognized weekday planet")
        mark="★ " if house==chart["house"] else "• "
        lines.append(
            mark+escape(BURMESE_HOUSES[house])+" — "+
            escape(entry["weekday"])+" ("+escape(PLANET_NAMES[entry["planet"]])+")"
        )
    title,prose=THEMES[chart["house"]]
    lines.extend([
        "",
        "<b>ဖွားအိမ်၏ ရိုးရာသင်္ကေတအနက်</b>",
        "<b>"+escape(title)+"</b>",
        escape(prose),
        "",
        "<b>အခြားအိမ်များ၏ သင်္ကေတအညွှန်း</b>",
    ])
    for house in HOUSES:
        if house==chart["house"]:
            continue
        theme,_=THEMES[house]
        lines.append(escape(BURMESE_HOUSES[house])+" — "+escape(theme))
    lines.extend([
        "",
        "<i>အထက်ပါအိမ်အခြားခြောက်လုံးသည် ရိုးရာအမည်နှင့် သင်္ကေတအညွှန်းများသာ ဖြစ်သည်။ "
        "မွေးဂြိုဟ်အားလုံးကို သီးခြားဖြစ်ရပ်ဟောချက်အဖြစ် ပေါင်းမဖတ်ပါ။</i>",
        "<i>ဗုဒ္ဓဟူးမွန်းလွဲ ရာဟုဆိုသည်မှာ ၈ နေ့နံ၏ သီးခြားခွဲခြားချက်သာဖြစ်ပြီး "
        "ဤတွက်ချက်နည်းတွင် မဟာဘုတ်အိမ်အသစ် မတိုးပါ။</i>",
        "<i>"+escape(reading["disclaimer"])+" "
        "ရိုးရာတွက်ချက်မှုနှင့် သင်္ကေတအနက်ကို သီးခြားဖော်ပြထားသည်။ "
        "မွေးအချက်အလက်ကို ဒီ Command က Database ထဲ မသိမ်းပါ။</i>",
    ])
    text="\n".join(lines)
    if len(text)>MAX_TELEGRAM_TEXT:
        raise ValueError("Mahabote report exceeds Telegram text limit")
    return text

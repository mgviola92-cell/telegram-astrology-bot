"""Source-consistent BaZi Ten Gods educational reading in Burmese.

The Ten Gods are relative five-phase/Yin-Yang relationships to the Day
Stem, NOT ten deities, personal identity traits, guaranteed outcomes or
standalone judgments of money, health, career or relationships.

Arithmetic source: 6tail/lunar-python LunarUtil.SHI_SHEN.
Interpretation vocabulary: Yuanhai Ziping / five relationship families,
cross-checked with https://yuanzizhiyi.com/en/wiki/bazi/ten-gods and
https://bazimethod.com/learn/ten-gods/ . Editorial Burmese paraphrases
distinguish original symbolic meaning from calculation.
"""
from bazi_ten_gods import calculate_ten_gods,ten_god
from bazi_elements import STEMS,ELEMENTS,PILLAR_NAMES
from bazi_element_reading import GENERATION,CONTROL,MYANMAR_ELEMENTS
from reading_facts import reading_facts

RULE_ID="CHN-BAZI-TENGODS-SYMBOLIC-001"

# Five relationship categories defined by Wu Xing relative to Day Master.
FAMILIES={
    "peer": {
        "burmese":"တူညီဓာတ် • အဖော်/ယှဉ်တွဲ",
        "symbols":("比肩","劫财"),
        "note":"မိမိနှင့်တူညီသည့်ဓာတ်၏ ရိုးရာဆက်နွယ်မှုဖြစ်သည်။",
    },
    "output": {
        "burmese":"ထုတ်ဖော်ဓာတ် • ဖန်တီးဖော်ပြခြင်း",
        "symbols":("食神","伤官"),
        "note":"Day Master ဓာတ်က ထုတ်ပေးသောဓာတ်ဆိုင်ရာ အနက်အုပ်စုဖြစ်သည်။",
    },
    "wealth": {
        "burmese":"ထိန်းချုပ်ဓာတ် • အရင်းအမြစ်စီမံခြင်း",
        "symbols":("偏财","正财"),
        "note":"Day Master ဓာတ်က ထိန်းချုပ်သောဓာတ်၏ သင်္ကေတဖြစ်ပြီး ငွေရမည်ဟု မဟောပါ။",
    },
    "authority": {
        "burmese":"ထိန်းညှိဓာတ် • စည်းကမ်း/တာဝန်",
        "symbols":("七杀","正官"),
        "note":"Day Master ဓာတ်ကို ထိန်းချုပ်သောဓာတ်၏ အမည်ဖြစ်၍ အန္တရာယ်ဟောချက် မဟုတ်ပါ။",
    },
    "resource": {
        "burmese":"ပံ့ပိုးဓာတ် • သင်ယူမှု/အထောက်အကူ",
        "symbols":("偏印","正印"),
        "note":"Day Master ဓာတ်ကို ထုတ်ပေးသောဓာတ်၏ ဆက်နွယ်မှုအမည်ဖြစ်သည်။",
    },
}
SYMBOL_NAMES={
    "比肩":"မိတ်ဖက်ဓာတ်",
    "劫财":"ယှဉ်ပြိုင်ဓာတ်",
    "食神":"ဖော်ထုတ်ဓာတ် (食神)",
    "伤官":"ပုံစံပြောင်းဖော်ထုတ်ဓာတ် (伤官)",
    "偏财":"သွယ်ဝိုက်အရင်းအမြစ်",
    "正财":"တိုက်ရိုက်အရင်းအမြစ်",
    "七杀":"တင်းကျပ်ထိန်းညှိဓာတ်",
    "正官":"စည်းကမ်းထိန်းညှိဓာတ်",
    "偏印":"သွယ်ဝိုက်ပံ့ပိုးဓာတ်",
    "正印":"တိုက်ရိုက်ပံ့ပိုးဓာတ်",
}
FAMILY_FOR_SYMBOL={symbol:family for family,data in FAMILIES.items()
                   for symbol in data["symbols"]}

def _family_elements(day_element):
    """Traditional Five Phases relative families, independent of Yin/Yang."""
    if day_element not in ELEMENTS:
        raise ValueError("Unknown Day Master phase")
    return {
        "peer":day_element,
        "output":GENERATION[day_element],
        "wealth":CONTROL[day_element],
        "authority":next(key for key,value in CONTROL.items() if value==day_element),
        "resource":next(key for key,value in GENERATION.items() if value==day_element),
    }

def interpret_ten_gods(chart:dict)->dict:
    """Revalidate untrusted chart before producing source-attributed labels."""
    checked=reading_facts("bazi",chart)
    pillars={name:checked["facts"][name] for name in PILLAR_NAMES}
    recomputed=calculate_ten_gods(pillars)
    if chart.get("ten_gods_all")!=recomputed:
        raise ValueError("Ten Gods differ from verified natal pillars")
    stem=checked["facts"]["day_master"]
    phase,polarity=STEMS[stem]
    if set(SYMBOL_NAMES)!=set(FAMILY_FOR_SYMBOL) or len(FAMILY_FOR_SYMBOL)!=10:
        raise ValueError("Incomplete canonical ten relationships")
    visible=[]
    for position in ("year","month","hour"):
        other=pillars[position][0]
        role=ten_god(stem,other)
        if recomputed["visible"][position]!={"stem":other,"ten_god":role}:
            raise ValueError("Visible ten-god relation mismatches source")
        visible.append({
            "pillar":position,
            "stem":other,
            "ten_god":role,
            "family":FAMILY_FOR_SYMBOL[role],
            "label":SYMBOL_NAMES[role],
        })
    hidden=[]
    for position in PILLAR_NAMES:
        hidden.extend([
            {"pillar":position,"stem":entry["stem"],"ten_god":entry["ten_god"],
             "family":FAMILY_FOR_SYMBOL[entry["ten_god"]]}
            for entry in recomputed["hidden"][position]
        ])
    phases=_family_elements(phase)
    return {
        "day_master":stem,
        "day_element":phase,
        "day_polarity":polarity,
        "visible":visible,
        "hidden":hidden,
        "families":[{
            "key":family,"element":phases[family],
            "element_burmese":MYANMAR_ELEMENTS[phases[family]],
            "label":FAMILIES[family]["burmese"],
            "symbols":FAMILIES[family]["symbols"],
            "note":FAMILIES[family]["note"],
        } for family in FAMILIES],
        "rule_id":RULE_ID,
        "calculation_rule_id":recomputed["evidence"]["rule_id"],
        "interpretation_status":"traditional_relationship_glossary_only",
        "hidden_stem_weights_inferred":False,
        "day_master_strength_inferred":False,
        "favorable_elements_inferred":False,
        "prediction_supported":False,
        "profile_saved":False,
    }

def summarize_ten_gods_burmese(reading:dict)->str:
    """Bounded Telegram section, no DOB, place, time or user ID."""
    if not isinstance(reading,dict) or reading.get("rule_id")!=RULE_ID:
        raise ValueError("Verified ten-gods reading required")
    if (len(reading.get("visible",[]))!=3 or len(reading.get("families",[]))!=5
            or reading.get("prediction_supported") is not False):
        raise ValueError("Incomplete ten-gods explanation")
    labels={"year":"နှစ်","month":"လ","hour":"နာရီ"}
    visible="\n".join(
        f'{labels[item["pillar"]]}တိုင် {item["stem"]} — {item["ten_god"]} / {item["label"]}'
        for item in reading["visible"]
    )
    families="\n".join(
        f'{part["element_burmese"]} — {part["label"]}'
        for part in reading["families"]
    )
    text=(
        "<b>Ten Gods — Day Master နှင့် ဆက်နွယ်မှု</b>\n"
        f"ရက်တိုင် {reading['day_master']} သည် Day Master ဖြစ်ပြီး ကိုယ်တိုင်၏တိုင်ကို "
        "သီးခြားကံကြမ္မာအုပ်စုတစ်ခု မတွက်ပါ။\n"
        f"{visible}\n\n"
        "<b>ရိုးရာ ဓာတ်ဆက်နွယ်မှု ၅ အုပ်စု</b>\n"
        f"{families}\n"
        "<i>Hidden Stems များကို အလေးချိန်မသတ်မှတ်ရသေးပါ။ "
        "ဓာတ်အင်အား၊ ကံကောင်း/မကောင်းမှုနှင့် အသက်မွေးဝမ်းကျောင်းအောင်မြင်မှုကို "
        "ဤအမည်များတစ်ခုတည်းဖြင့် မဆုံးဖြတ်ပါ။</i>"
    )
    if len(text)>1300:
        raise ValueError("Ten Gods Telegram section too large")
    return text

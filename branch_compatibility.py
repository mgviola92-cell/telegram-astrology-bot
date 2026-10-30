"""Private, no-birth-data Chinese Earthly Branch relationship reference.

This is a source-table lookup for two supplied Earthly Branch symbols, not a
two-person natal compatibility score. Not an empirical forecast, no DOB,
gender, birth time, Telegram IDs, database, session or background job.

Reference tables: traditional Wuxing Dayi and Xieji Bianfang Shu via
https://lunarkanji.com/chinese-zodiac-compatibility/ ;
https://yuanzizhiyi.com/en/wiki/bazi/relations
and https://clarifyhk.com/learn/bazi/earthly-branches/reading-order-for-branch-combinations-and-clashes
"""
from html import escape
from bazi_elements import BRANCHES

RULE_ID="CHN-BAZI-EARTHLY-BRANCH-PAIR-001"
ANIMALS={
    "子":"ကြွက်","丑":"နွား","寅":"ကျား","卯":"ယုန်",
    "辰":"နဂါး","巳":"မြွေ","午":"မြင်း","未":"ဆိတ်",
    "申":"မျောက်","酉":"ကြက်","戌":"ခွေး","亥":"ဝက်",
}
LIUHE=(("子","丑"),("寅","亥"),("卯","戌"),
       ("辰","酉"),("巳","申"),("午","未"))
LIUCHONG=(("子","午"),("丑","未"),("寅","申"),
          ("卯","酉"),("辰","戌"),("巳","亥"))
SANHE={
    "ရေ":("申","子","辰"),
    "သစ်":("亥","卯","未"),
    "မီး":("寅","午","戌"),
    "သတ္တု":("巳","酉","丑"),
}
HARMONY_PAIRS=frozenset(frozenset(row) for row in LIUHE)
CLASH_PAIRS=frozenset(frozenset(row) for row in LIUCHONG)

def _ensure_symbols():
    if set(ANIMALS)!=set(BRANCHES) or len(ANIMALS)!=12:
        raise ValueError("Zodiac Branch animal lookup does not cover 12 branches")
    if len(HARMONY_PAIRS)!=6 or len(CLASH_PAIRS)!=6 or HARMONY_PAIRS&CLASH_PAIRS:
        raise ValueError("Malformed six-pair traditional lookup")
    if any(len(pair)!=2 for pair in HARMONY_PAIRS|CLASH_PAIRS):
        raise ValueError("Six-pair lookup must use distinct symbols")
    if len(SANHE)!=4 or any(len(set(g))!=3 for g in SANHE.values()):
        raise ValueError("Trine lookup requires four groups of three")
    if set().union(*(set(group) for group in SANHE.values()))!=set(BRANCHES):
        raise ValueError("Trine lookup must cover each Earthly Branch")

def compare_branches(a:str,b:str)->dict:
    """Find named categories without equating a pair to a person's fate."""
    _ensure_symbols()
    if type(a) is not str or type(b) is not str or a not in ANIMALS or b not in ANIMALS:
        raise ValueError("Choose two exact Earthly Branch symbols")
    pair=frozenset((a,b))
    matches=[]
    if a==b:
        matches.append({"category":"same","name":"တူညီသော အကိုင်းသင်္ကေတ",
                        "explanation":"နှစ်ခုလုံးသည် တူညီသော Earthly Branch ဖြစ်သည်။"})
    if pair in HARMONY_PAIRS:
        matches.append({"category":"liuhe","name":"六合 — ရိုးရာတွဲဖက်ဆက်နွယ်မှု",
                        "explanation":"မူရင်း 六合 ဇယားအရ သတ်မှတ်ထားသော အကိုင်းနှစ်ခု၏ ဆက်နွယ်မှုဖြစ်သည်။ ဓာတ်အသွင်ပြောင်းပြီဟု မဆိုလိုပါ။"})
    if pair in CLASH_PAIRS:
        matches.append({"category":"liuchong","name":"六冲 — ရိုးရာဆန့်ကျင်ဆက်နွယ်မှု",
                        "explanation":"မူရင်း 六冲 ဇယားတွင် အပြန်အလှန်ရှိသော အကိုင်းနှစ်ခုဖြစ်သည်။ လူနှစ်ဦးကြား အမှန်တကယ် အငြင်းပွားမည်ဟု မဆိုလိုပါ။"})
    if a!=b:
        for phase,group in SANHE.items():
            if a in group and b in group:
                matches.append({
                    "category":"sanhe_partial",
                    "name":"三合 — "+phase+" ဓာတ်အုပ်စုတွင် အတူပါဝင်မှု",
                    "explanation":"ဤနှစ်ခုသည် 三合 အကိုင်းသုံးခုအုပ်စုတစ်ခုထဲတွင် ပါဝင်သည်။ အကိုင်းတတိယခုမပါသဖြင့် အပြည့်အဝ 三合 မဖွဲ့ပါ။",
                    "full_group":"".join(group),
                })
    return {
        "first":a,"second":b,
        "first_animal":ANIMALS[a],"second_animal":ANIMALS[b],
        "matches":matches,
        "rule_id":RULE_ID,
        "scope":"two_explicit_earthly_branches_only",
        "calendar_birth_year_derived":False,
        "full_four_pillars_compared":False,
        "compatibility_score_computed":False,
        "prediction_supported":False,
        "personal_data_saved":False,
    }

def render_branch_comparison(result:dict)->str:
    if type(result) is not dict:
        raise ValueError("Verified branch pair required")
    try:
        expected=compare_branches(result["first"],result["second"])
    except (KeyError,TypeError,ValueError) as err:
        raise ValueError("Unverified Earthly Branch pair") from err
    if result!=expected:
        raise ValueError("Branch relationship result differs from canonical sources")
    lines=[
        "<b>ရိုးရာအကိုင်းဆက်နွယ်မှု — တရုတ် ၁၂ ရာသီနံ</b>",
        "━━━━━━━━━━━━━━",
        f'အကိုင်း (၁) — <b>{escape(result["first"])} · {escape(result["first_animal"])}</b>',
        f'အကိုင်း (၂) — <b>{escape(result["second"])} · {escape(result["second_animal"])}</b>',
        "",
        "<b>ရိုးရာဇယားမှ တွေ့ရှိချက်</b>",
    ]
    if not result["matches"]:
        lines.append("ဤနှစ်ခုအတွက် စစ်ထားသော 六合၊ 六冲၊ 三合 အမျိုးအစားများတွင် တိုက်ရိုက်သတ်မှတ်ချက် မတွေ့ပါ။")
    for match in result["matches"]:
        lines.extend([f'<b>{escape(match["name"])}</b>',escape(match["explanation"])])
    lines.extend([
        "",
        "<i>ဤသည် Earthly Branch နှစ်ခု၏ ရိုးရာဇယားကိုသာ နှိုင်းယှဉ်ထားခြင်းဖြစ်သည်။ "
        "မွေးနှစ်၊ မွေးချိန်၊ လေးတိုင်ဇာတာနှင့် ဓာတ်အင်အားကို မတွက်ထားပါ။ "
        "လူနှစ်ဦး၏ သင့်လျော်မှု၊ မိတ်ဆွေဖြစ်နိုင်မှု သို့မဟုတ် အနာဂတ်ကို အဆုံးအဖြတ်မပေးပါ။ "
        "သီးသန့်မွေးအချက်အလက်ကို မတောင်း၊ မသိမ်းပါ။</i>"
    ])
    text="\n".join(lines)
    if len(text)>4096:
        raise ValueError("Telegram message exceeds text limit")
    return text

def branch_picker(stage:str, first:str|None=None):
    """Return native Telegram inline rows as portable data, no server state."""
    _ensure_symbols()
    if stage not in ("first","second") or (stage=="second" and first not in ANIMALS):
        raise ValueError("Invalid branch picker state")
    rows=[]
    for i in range(0,len(ANIMALS),3):
        branches=list(ANIMALS)[i:i+3]
        rows.append([(f"{branch} {ANIMALS[branch]}",
                      f"compat:a:{branch}" if stage=="first" else f"compat:b:{first}:{branch}")
                     for branch in branches])
    rows.append([("မူလရွေးချယ်မှု", "compat:start")] if stage=="second"
                else [("ဇာတာခန်းသို့","ui:feature:compatibility")])
    return rows

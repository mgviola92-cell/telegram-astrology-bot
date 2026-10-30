"""BaZi classical visible-pillar pair classification, without predictions."""
from bazi_elements import PILLAR_NAMES
from reading_facts import reading_facts

RULE_ID="CHN-BAZI-PAIR-RELATIONS-001"
BRANCH_OPPOSITES=("子午","丑未","寅申","卯酉","辰戌","巳亥")
BRANCH_UNIONS=("子丑","寅亥","卯戌","辰酉","巳申","午未")
STEM_UNIONS=("甲己","乙庚","丙辛","丁壬","戊癸")
TABLES={"branch_opposite":BRANCH_OPPOSITES,"branch_union":BRANCH_UNIONS,"stem_union":STEM_UNIONS}
MYANMAR_POSITIONS={"year":"နှစ်","month":"လ","day":"ရက်","hour":"နာရီ"}

def classify_pairs(chart):
    checked=reading_facts("bazi",chart)
    pillars={name:checked["facts"][name] for name in PILLAR_NAMES}
    records=[]
    for i,a in enumerate(PILLAR_NAMES):
        for j in range(i+1,len(PILLAR_NAMES)):
            b=PILLAR_NAMES[j]
            for relation,pairs in TABLES.items():
                k=0 if relation=="stem_union" else 1
                x,y=pillars[a][k],pillars[b][k]
                if any({x,y}==set(pair) for pair in pairs):
                    records.append({"type":relation,"a":a,"b":b,"symbols":x+y,"adjacent":j==i+1})
    return {"records":records,"rule_id":RULE_ID,"phase_transformation_assessed":False,
            "predictive_claim":False,"natal_source_validated":True}

def format_pairs(reading):
    if (reading.get("rule_id")!=RULE_ID or reading.get("predictive_claim") is not False):
        raise ValueError("Verified relation report required")
    headings=(("branch_opposite","六冲 — Branch ဆန့်ကျင်ဘက်အတွဲ"),
              ("branch_union","六合 — Branch ချိတ်ဆက်အတွဲ"),
              ("stem_union","五合 — Stem ချိတ်ဆက်အတွဲ"))
    parts=["<b>တိုင်လေးတိုင် ဆက်နွယ်မှု</b>"]
    for kind,title in headings:
        parts.append(title)
        subset=[r for r in reading["records"] if r["type"]==kind]
        if not subset:parts.append("မတွေ့ပါ")
        for r in subset:
            parts.append(MYANMAR_POSITIONS[r["a"]]+"–"+MYANMAR_POSITIONS[r["b"]]+": "+
                         r["symbols"]+(" (ဘေးချင်း)" if r["adjacent"] else " (အကွာ)"))
    parts.append("<i>ဤအတွဲများသည် ရိုးရာအမည်သတ်မှတ်ချက်သာဖြစ်သည်။ "
                 "ဓာတ်အသွင်ပြောင်းမှု၊ အင်အားနှင့် အနာဂတ်ဖြစ်ရပ်များကို မဆုံးဖြတ်ပါ။</i>")
    s="\n".join(parts)
    if len(s)>1050:raise ValueError("Telegram text too long")
    return s

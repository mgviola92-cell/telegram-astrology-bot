"""Auditable BaZi Eight Characters / Five Phases summaries.

Map each displayed stem and branch to its conventional *primary*
Wu Xing element. These eight visible-symbol counts are NOT a Day Master
strength score: seasonal qi, hidden stems, combinations, clashes and
school conventions require separate reviewed rules.
"""
from dataclasses import asdict
from astro_core import Evidence

STEMS={
    "甲":("Wood","Yang"),"乙":("Wood","Yin"),
    "丙":("Fire","Yang"),"丁":("Fire","Yin"),
    "戊":("Earth","Yang"),"己":("Earth","Yin"),
    "庚":("Metal","Yang"),"辛":("Metal","Yin"),
    "壬":("Water","Yang"),"癸":("Water","Yin"),
}
BRANCHES={
    "子":"Water","丑":"Earth","寅":"Wood","卯":"Wood",
    "辰":"Earth","巳":"Fire","午":"Fire","未":"Earth",
    "申":"Metal","酉":"Metal","戌":"Earth","亥":"Water",
}
ELEMENTS=("Wood","Fire","Earth","Metal","Water")
PILLAR_NAMES=("year","month","day","hour")

def summarize_visible_elements(pillars:dict)->dict:
    if not isinstance(pillars,dict) or set(pillars)!=set(PILLAR_NAMES):
        raise ValueError("Expected all four explicitly named pillars")
    counts={name:0 for name in ELEMENTS}
    facts={}
    for name in PILLAR_NAMES:
        pair=pillars[name]
        if not isinstance(pair,str) or len(pair)!=2:
            raise ValueError("Each pillar must contain exactly one stem and one branch")
        stem,branch=pair
        if stem not in STEMS or branch not in BRANCHES:
            raise ValueError("Unknown stem or earthly branch")
        if ("甲乙丙丁戊己庚辛壬癸".index(stem)%2)!=("子丑寅卯辰巳午未申酉戌亥".index(branch)%2):
            raise ValueError("Invalid stem/branch parity in sexagenary pair")
        element,polarity=STEMS[stem]
        branch_element=BRANCHES[branch]
        counts[element]+=1
        counts[branch_element]+=1
        facts[name]={"stem":stem,"stem_element":element,"stem_polarity":polarity,
                     "branch":branch,"branch_primary_element":branch_element}
    evidence=Evidence(
        rule_id="CHN-BAZI-VISIBLE-WUXING-001",
        tradition="Chinese BaZi / Wu Xing",
        method="Count four heavenly-stem primary elements plus four earthly-branch primary elements, without weighting",
        input_assumptions={"pillar_characters_verified_by_caller":False,
                           "hidden_stems_included":False,"seasonal_strength_calculated":False},
        derived_facts={"visible_counts":counts,"symbols":facts},
        reference="Ten Heavenly Stems and Twelve Earthly Branches correspondences; https://www.ibiblio.org/chinesehistory/contents/08fea/c06s02.htm ; https://uaya.org/iching/correspondences/",
    )
    return {"visible_counts":counts,"symbols":facts,
            "day_master_element":STEMS[pillars["day"][0]][0],
            "day_master_polarity":STEMS[pillars["day"][0]][1],
            "evidence":asdict(evidence)}

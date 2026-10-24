"""BaZi branch hidden stems (藏干), preserving source order.

Adapted from 6tail/lunar-python LunarUtil.ZHI_HIDE_GAN: main Qi first,
then residual/mixed Qi. Listing symbols is not an element strength score.
"""
from dataclasses import asdict
from astro_core import Evidence
from bazi_elements import STEMS, BRANCHES, PILLAR_NAMES, summarize_visible_elements

HIDDEN_STEMS = {
    "子": ("癸",),
    "丑": ("己","癸","辛"),
    "寅": ("甲","丙","戊"),
    "卯": ("乙",),
    "辰": ("戊","乙","癸"),
    "巳": ("丙","庚","戊"),
    "午": ("丁","己"),
    "未": ("己","丁","乙"),
    "申": ("庚","壬","戊"),
    "酉": ("辛",),
    "戌": ("戊","辛","丁"),
    "亥": ("壬","甲"),
}

def calculate_hidden_stems(pillars:dict) -> dict:
    # Reuse strict pillar validation, including stem-branch parity checks.
    summarize_visible_elements(pillars)
    result = {}
    for name in PILLAR_NAMES:
        branch=pillars[name][1]
        result[name] = {
            "branch": branch,
            "hidden": [
                {"stem": stem, "element":STEMS[stem][0], "polarity":STEMS[stem][1],
                 "traditional_order": "primary" if i==0 else "secondary"}
                for i,stem in enumerate(HIDDEN_STEMS[branch])
            ],
        }
    evidence=Evidence(
        rule_id="CHN-BAZI-HIDDEN-STEMS-001",
        tradition="Chinese BaZi branch hidden stems",
        method="Lookup branch hidden stems in documented primary-first order; no qi weighting or seasonal-strength evaluation",
        input_assumptions={"pillar_characters_verified_externally":False,
                           "qi_percentages_applied":False,
                           "day_master_strength_calculated":False},
        derived_facts={"hidden_stems":result},
        reference="6tail/lunar-python lunar_python/util/LunarUtil.py ZHI_HIDE_GAN and lunar_python/EightChar.py getters",
    )
    return {"pillars":result,"evidence":asdict(evidence)}

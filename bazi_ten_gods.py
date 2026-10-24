"""Ten Gods (十神) relationships to BaZi Day Master.

Deterministic convention matching LunarUtil.SHI_SHEN in 6tail/lunar-python.
This classifies stem relations, NOT personal traits or predictions.
"""
from dataclasses import asdict
from astro_core import Evidence
from bazi_elements import STEMS, PILLAR_NAMES, summarize_visible_elements
from bazi_hidden_stems import HIDDEN_STEMS

GENERATING=("Wood","Fire","Earth","Metal","Water")
CONTROLLING={"Wood":"Earth","Fire":"Metal","Earth":"Water",
             "Metal":"Wood","Water":"Fire"}

def ten_god(day_stem: str, other_stem: str) -> str:
    if day_stem not in STEMS or other_stem not in STEMS:
        raise ValueError("Unknown heavenly stem")
    mine, my_polarity=STEMS[day_stem]
    other, other_polarity=STEMS[other_stem]
    same=my_polarity==other_polarity
    if mine==other:
        return "比肩" if same else "劫财"
    if GENERATING[(GENERATING.index(mine)+1)%5]==other:
        return "食神" if same else "伤官"
    if CONTROLLING[mine]==other:
        return "偏财" if same else "正财"
    if CONTROLLING[other]==mine:
        return "七杀" if same else "正官"
    if GENERATING[(GENERATING.index(other)+1)%5]==mine:
        return "偏印" if same else "正印"
    raise AssertionError("Incomplete five phases")

def calculate_ten_gods(pillars:dict)->dict:
    summarize_visible_elements(pillars)
    day=pillars["day"][0]
    visible={}
    hidden={}
    for name in PILLAR_NAMES:
        stem,branch=pillars[name]
        visible[name]={"stem":stem,"ten_god":ten_god(day,stem)}
        hidden[name]=[{"stem":s,"ten_god":ten_god(day,s)}
                      for s in HIDDEN_STEMS[branch]]
    evidence=Evidence(
        rule_id="CHN-BAZI-TENGODS-001",
        tradition="BaZi / Ten Gods",
        method="Day Master relative generating/controlling Five Phases and same/different Yin-Yang polarity; branch hidden stems use traditional upstream list",
        input_assumptions={"day_master":day,"pillars_verified_externally":False,
                           "favorable_unfavorable_elements_inferred":False,
                           "fortune_forecast_inferred":False},
        derived_facts={"visible_stems":visible,"hidden_stems":hidden},
        reference="6tail/lunar-python lunar_python/util/LunarUtil.py SHI_SHEN and ZHI_HIDE_GAN",
    )
    return {"day_master":day,"visible":visible,"hidden":hidden,
            "evidence":asdict(evidence)}

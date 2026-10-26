"""Independent reference implementation of lunar-python EightChar Chang Sheng.

The reference convention assigns 12 branches to 12 stages according to
the Day Master's Heavenly Stem, and reverses the progression for Yin stems.
This verifies categorical arithmetic, not predictive reliability.
"""
from bazi_elements import STEMS, BRANCHES

STAGES = ("长生", "沐浴", "冠带", "临官", "帝旺", "衰",
          "病", "死", "墓", "绝", "胎", "养")
BRANCH_ORDER = "子丑寅卯辰巳午未申酉戌亥"
OFFSETS = {
    "甲":1, "丙":10, "戊":10, "庚":7, "壬":4,
    "乙":6, "丁":9, "己":9, "辛":0, "癸":3,
}

def stage_for(day_stem: str, branch: str) -> str:
    if day_stem not in STEMS or branch not in BRANCHES:
        raise ValueError("Valid Day Master stem and Earthly Branch required")
    offset = OFFSETS[day_stem]
    direction = 1 if STEMS[day_stem][1] == "Yang" else -1
    index = (offset + direction * BRANCH_ORDER.index(branch)) % len(STAGES)
    return STAGES[index]

def stages_for_pillars(pillars: dict, day_master: str) -> dict:
    names = ("year","month","day","hour")
    if not isinstance(pillars,dict) or set(pillars)!=set(names):
        raise ValueError("Four complete pillars required")
    if day_master not in STEMS or pillars["day"][0]!=day_master:
        raise ValueError("Day Master must match Day Pillar")
    result={}
    for name in names:
        pillar=pillars[name]
        if not isinstance(pillar,str) or len(pillar)!=2 or pillar[1] not in BRANCHES:
            raise ValueError("Invalid pillar")
        result[name]=stage_for(day_master,pillar[1])
    return result

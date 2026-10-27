"""BaZi solar-term Month Branch and seasonal three-branch membership.

This engine *classifies* the already verified Month Pillar and membership of
the four natal Earthly Branches. A complete sanhui set is NOT proof that a
combination has transformed or that a Day Master is strong or weak.
"""
from dataclasses import asdict
from astro_core import Evidence
from bazi_elements import STEMS, BRANCHES
from reading_facts import reading_facts

RULE_ID="CHN-BAZI-SEASON-MONTH-001"
SEASONS=(
    {"name":"Spring","burmese":"နွေဦး","phase":"Wood","branches":("寅","卯","辰")},
    {"name":"Summer","burmese":"နွေ","phase":"Fire","branches":("巳","午","未")},
    {"name":"Autumn","burmese":"ဆောင်းဦး","phase":"Metal","branches":("申","酉","戌")},
    {"name":"Winter","burmese":"ဆောင်း","phase":"Water","branches":("亥","子","丑")},
)
STAGES=("early","middle","late")

def season_for_month_branch(branch):
    if not isinstance(branch,str) or branch not in BRANCHES:
        raise ValueError("Unknown solar-term Earthly Branch")
    for group in SEASONS:
        if branch in group["branches"]:
            return {key:value for key,value in group.items() if key!="branches"} | {
                "month_branch":branch,"season_stage":STAGES[group["branches"].index(branch)]
            }
    raise AssertionError("Incomplete solar-term month branches")

def complete_seasonal_memberships(branches):
    """Distinct set membership only, independent of strength/transformation."""
    if not isinstance(branches,dict) or set(branches)!={"year","month","day","hour"}:
        raise ValueError("Expected four named Earthly Branches")
    if any(not isinstance(b,str) or b not in BRANCHES for b in branches.values()):
        raise ValueError("Invalid branch")
    present=set(branches.values())
    return [
        {"season":group["name"],"phase":group["phase"],
         "branches":"".join(group["branches"])}
        for group in SEASONS if set(group["branches"]).issubset(present)
    ]

def calculate_bazi_seasons(chart):
    checked=reading_facts("bazi",chart)
    pillars={k:checked["facts"][k] for k in ("year","month","day","hour")}
    branches={k:p[1] for k,p in pillars.items()}
    month=season_for_month_branch(branches["month"])
    memberships=complete_seasonal_memberships(branches)
    day_stem=checked["facts"]["day_master"]
    day_element=STEMS[day_stem][0]
    facts={
        "month_branch":branches["month"],
        "month_season":month["name"],
        "month_stage":month["season_stage"],
        "month_season_phase":month["phase"],
        "day_master_element":day_element,
        "all_branches":branches,
        "complete_three_branch_memberships":memberships,
    }
    evidence=Evidence(
        rule_id=RULE_ID,
        tradition="Chinese BaZi, solar-term seasons and sanhui membership",
        method="Use verified Jie month pillar branch to identify the three-branch season. Report only all-three distinct seasonal memberships; no strength or transformation calculated.",
        input_assumptions={"bazi_rule_id":checked["rule_id"],
                           "verified_chart_pillars":pillars,
                           "jie_based_month_from_upstream_lunar_python":True},
        derived_facts=facts,
        reference="6tail/lunar-python Lunar.__computeMonth Jie exact month; American Feng Shui Institute Stems & Branches chart; https://www.amfengshui.com/wp-content/uploads/2014/09/as101.pdf",
    )
    return {
        "month":month,
        "branches":branches,
        "memberships":memberships,
        "day_master_element":day_element,
        "evidence":asdict(evidence),
        "prediction_supported":False,
        "day_master_strength_calculated":False,
        "combination_transformation_claimed":False,
    }

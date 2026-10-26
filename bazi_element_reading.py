"""Calculation-grounded BaZi interpretation of elemental relationships.

No invented personal predictions, luck strength, or favorable element claims.
Only verified stems, branches, and Five Phases relationships are described.
"""
from bazi_elements import STEMS, ELEMENTS
from reading_facts import reading_facts

GENERATION={"Wood":"Fire","Fire":"Earth","Earth":"Metal","Metal":"Water","Water":"Wood"}
CONTROL={"Wood":"Earth","Earth":"Water","Water":"Fire","Fire":"Metal","Metal":"Wood"}
MYANMAR_ELEMENTS={"Wood":"သစ်","Fire":"မီး","Earth":"မြေ","Metal":"သတ္တု","Water":"ရေ"}
MYANMAR_POLARITY={"Yin":"ယင်","Yang":"ယန်"}

def relationship(day_element, other_element):
    if day_element not in ELEMENTS or other_element not in ELEMENTS:
        raise ValueError("Unknown Five Phases element")
    if day_element==other_element:
        return "same"
    if GENERATION[day_element]==other_element:
        return "day_generates"
    if GENERATION[other_element]==day_element:
        return "generates_day"
    if CONTROL[day_element]==other_element:
        return "day_controls"
    if CONTROL[other_element]==day_element:
        return "controls_day"
    raise AssertionError("Incomplete five-phase relation")

RELATION_LABELS={
    "same":"တူညီသော ဓာတ်အုပ်စု",
    "day_generates":"Day Master ဓာတ်က ထုတ်ပေးသောဓာတ်",
    "generates_day":"Day Master ဓာတ်ကို ထုတ်ပေးသောဓာတ်",
    "day_controls":"Day Master ဓာတ်က ထိန်းချုပ်သောဓာတ်",
    "controls_day":"Day Master ဓာတ်ကို ထိန်းချုပ်သောဓာတ်",
}

def bazi_element_reading(chart):
    """Classify verified Day Master to five-element relations without fortune claims."""
    checked=reading_facts("bazi",chart)
    stem=checked["facts"]["day_master"]
    day_element,polarity=STEMS[stem]
    counts=chart["visible_wuxing"]["visible_counts"]
    if set(counts)!=set(ELEMENTS) or any(type(v) is not int or v<0 for v in counts.values()) or sum(counts.values())!=8:
        raise ValueError("Visible Eight Characters must total eight primary elements")
    groups=[]
    for element in ELEMENTS:
        groups.append({
            "element":element,
            "burmese_element":MYANMAR_ELEMENTS[element],
            "visible_count":counts[element],
            "relationship":relationship(day_element,element),
            "relationship_label":RELATION_LABELS[relationship(day_element,element)],
        })
    return {
        "day_master":stem,
        "day_element":day_element,
        "day_element_burmese":MYANMAR_ELEMENTS[day_element],
        "polarity":polarity,
        "polarity_burmese":MYANMAR_POLARITY[polarity],
        "groups":groups,
        "rule_id":checked["rule_id"],
        "seasonal_strength_calculated":False,
        "favorable_elements_inferred":False,
        "prediction_supported":False,
    }

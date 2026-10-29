"""Hellenistic annual profection with source-declared rising sign.

The birth chart's Ascendant is NOT solved here: caller must bring a rising sign
from a separately calculated reliable natal chart. Returns traditional annual
house/sign/lord classification, not a forecast or proven causal influence.
"""
from datetime import date, datetime
from astro_core import SIGNS, TRADITIONAL_RULERS, annual_profection

RULE_ID="WEST-HEL-ANNUAL-PROFECTION-001"
HOUSE_TOPICS_BURMESE=(
    "ကိုယ်ပိုင်အစပြုမှုနှင့် အတ္တရပ်တည်မှု",
    "အရင်းအမြစ်နှင့် တန်ဖိုးထားမှု",
    "ဆက်သွယ်ရေးနှင့် သင်ယူမှု",
    "အိမ်နှင့် မိသားစုဆက်နွယ်မှု",
    "ဖန်တီးမှုနှင့် ပျော်ရွှင်မှု",
    "အလုပ်နှင့် နေ့စဉ်လုပ်ရိုးလုပ်စဉ်",
    "မိတ်ဖက်ဆက်ဆံရေး",
    "မျှဝေထားသော အရင်းအမြစ်",
    "ပညာရှာဖွေမှုနှင့် ခရီးသွားခြင်း",
    "အလုပ်အကိုင်နှင့် လူမှုတာဝန်",
    "မိတ်ဆွေများနှင့် လူမှုအသိုင်းအဝိုင်း",
    "အတွင်းစိတ်နှင့် တစ်ယောက်တည်းနေချိန်",
)

def profection_reading(born: date, evaluation_date: date, rising_sign: str) -> dict:
    if not isinstance(born,date) or isinstance(born, datetime):
        raise ValueError("Valid birth date required")
    if not isinstance(evaluation_date,date) or isinstance(evaluation_date, datetime):
        raise ValueError("Valid evaluation date required")
    if rising_sign not in SIGNS:
        raise ValueError("Use one of the 12 English zodiac sign names")
    result=annual_profection(born,evaluation_date,rising_sign)
    ev=result["evidence"]
    if ev["rule_id"]!=RULE_ID:
        raise ValueError("Unrecognized profection calculation rule")
    age=evaluation_date.year-born.year-((evaluation_date.month,evaluation_date.day)<(born.month,born.day))
    # Explicit Feb-29 convention in non-leap years: March 1, not Feb 28.
    # This is the behavior of the underlying age_on() calculation.
    leap_day_birth=(born.month,born.day)==(2,29)
    expected_index=(SIGNS.index(rising_sign)+age)%12
    if (result["house"]!=age%12+1 or result["sign"]!=SIGNS[expected_index]
            or result["lord_of_year"]!=TRADITIONAL_RULERS[expected_index]):
        raise ValueError("Profection calculation differs from 12-year reference rules")
    return {
        "age_completed":age,
        "leap_day_birthday_march_first":leap_day_birth,
        "house":result["house"],
        "sign":result["sign"],
        "lord_of_year":result["lord_of_year"],
        "house_topic":result["house_topic"],
        "house_topic_burmese":HOUSE_TOPICS_BURMESE[result["house"]-1],
        "rising_sign_input":rising_sign,
        "rising_sign_source":"user-provided, not calculated or verified here",
        "calculation_rule_id":RULE_ID,
        "evidence":ev,
        "prediction_supported":False,
        "interpretation_status":"traditional_annual_time_lord_categories",
    }

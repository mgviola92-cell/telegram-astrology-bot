"""Myanmar traditional calendar markers based on Yan Naing Aye's formulas.

This module computes date labels, not recommendations for safety-sensitive
decisions. Gregorian inputs are local calendar dates. Day numbering uses
Saturday=0..Friday=6, following the 2013 mmcal reference.
"""
from dataclasses import asdict
from datetime import date
from astro_core import Evidence
from myanmar_calendar import calculate_myanmar_calendar
from reading_facts import reading_facts

RULE_ID = "MM-CALENDAR-DAY-SIGNALS-001"
SOURCE = "Yan Naing Aye, Myanmar Astrological Calendar Days (2013)"
DIRECTIONS = ("အနောက်", "မြောက်", "အရှေ့", "တောင်")
NAKHAT_NAMES = ("ဘီလူးနက္ခတ်", "နတ်နက္ခတ်", "လူနက္ခတ်")

def effective_month(month_id: int) -> int:
    """0 means First Waso; 13/14 are Late Tagu/Kason."""
    if type(month_id) is not int or month_id < 0 or month_id > 14:
        raise ValueError("Unknown Myanmar month")
    return 4 if month_id == 0 else (month_id - 1) % 12 + 1

def calculate_day_signals(local_day: date) -> dict:
    cal = calculate_myanmar_calendar(local_day)
    reading_facts("myanmar_calendar",cal)
    raw_month = cal["month_index"]
    mm = effective_month(raw_month)
    my = cal["myanmar_year"]
    myt = cal["year_type"]
    md = cal["day"]
    wd = (local_day.weekday()+2)%7
    month_length = 30 - raw_month % 2
    if raw_month == 3:
        month_length += myt // 2
    if md < 1 or md > month_length:
        raise ValueError("Myanmar lunar day exceeds month length")
    d = md - 15*(md//16)
    # Sabbath and eve are the traditional lunar-month checkpoints.
    sabbath = md in (8,15,23,month_length)
    sabbath_eve = md in (7,14,22,month_length-1)
    # All lookups below follow the month/weekday tables in Yan's article.
    m1 = mm-1-mm//9
    first = (m1*2-m1//8)%7
    thamanyo = (wd+7-first)%7 <= 1
    amyeittasote = d == (5,8,3,7,2,4,1)[wd]
    warameittugyi = d == (7,1,4,8,9,6,3)[wd]
    warameittunge = 12-d == (wd+6)%7
    yatpote = d == (8,1,4,6,9,8,7)[wd]
    thamaphyu = (d in ((1,2,6,6,5,6,7)[wd],(0,1,0,0,0,3,3)[wd])
                 or (d==4 and wd==5))
    nagapor = (md in ((26,21,2,10,18,2,21)[wd],(17,19,1,0,9,0,0)[wd])
               or (md==2 and wd==1)
               or (wd==2 and md in (12,4,18)))
    m1 = mm if mm%2 else (mm+9)%12
    m1 = (m1+4)%12+1
    yatyotema = d == m1
    mahayatkyan = d == ((mm%12//2+4)%6+1)
    shanyat = d == (8,8,2,2,9,3,3,5,1,4,7,4)[mm-1]
    nagahle = (mm%12)//3
    nakhat = my % 3
    markers = {
        "sabbath":sabbath,
        "sabbath_eve":sabbath_eve,
        "yatyaza":cal["yatyaza"],
        "pyathada":cal["pyathada"],
        "thamanyo":thamanyo,
        "amyeittasote":amyeittasote,
        "warameittugyi":warameittugyi,
        "warameittunge":warameittunge,
        "yatpote":yatpote,
        "thamaphyu":thamaphyu,
        "nagapor":nagapor,
        "yatyotema":yatyotema,
        "mahayatkyan":mahayatkyan,
        "shanyat":shanyat,
        "nagahle":nagahle,
        "nakhat":nakhat,
    }
    evidence = Evidence(
        rule_id=RULE_ID,
        tradition="Myanmar calendrical day-marker conventions",
        method="mmcal Myanmar date and local weekday; Yan Naing Aye's monthly/lunar-day marker formulas",
        input_assumptions={
            "local_gregorian_date":local_day.isoformat(),
            "weekday_code":wd,
            "month_id":raw_month,
            "effective_month":mm,
            "late_months_normalized_to_tagu_kason":True,
            "first_waso_normalized_to_waso":True,
        },
        derived_facts=markers,
        reference=SOURCE+"; https://cool-emerald.blogspot.com/2013/12/myanmar-astrological-calendar-days.html",
    )
    return {
        "date":local_day.isoformat(),
        "myanmar_year":my,
        "myanmar_month":cal["month"],
        "moon_phase":cal["moon_phase"],
        "weekday_code":wd,
        "lunar_month_length":month_length,
        "markers":markers,
        "nagahle_direction":DIRECTIONS[nagahle],
        "nakhat_name":NAKHAT_NAMES[nakhat],
        "evidence":asdict(evidence),
        "prediction_supported":False,
    }

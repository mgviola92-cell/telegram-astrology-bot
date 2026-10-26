"""BaZi 十二长生 (Twelve Growth Stages) from lunar-python EightChar.

The Twelve Stages are traditional categorical symbols, NOT measured life
expectancy, health conditions, lifespan, personality or predicted events.
Never infer physical harm from a stage name; schools differ in interpretation.
"""
from dataclasses import asdict
from datetime import datetime
from astro_core import Evidence
from reading_facts import reading_facts

RULE_ID="CHN-BAZI-CHANGSHENG-001"
STAGE_NAMES=("长生","沐浴","冠带","临官","帝旺","衰",
             "病","死","墓","绝","胎","养")
STAGE_GLOSSES={
    "长生":"အစပြုခြင်း",
    "沐浴":"ပြန်လည်သန့်စင်ခြင်း",
    "冠带":"အသင့်ပြင်ဆင်ခြင်း",
    "临官":"တာဝန်ဝင်ရောက်ခြင်း",
    "帝旺":"အင်အားပြည့်ခြင်း",
    "衰":"အားလျော့ခြင်း",
    "病":"ပြန်လည်ထိန်းသိမ်းခြင်း",
    "死":"အဆင့်တစ်ခုရပ်နားခြင်း",
    "墓":"သိုလှောင်ခြင်း",
    "绝":"ကူးပြောင်းသည့်အပိုင်း",
    "胎":"အစပျိုးခြင်း",
    "养":"ပြုစုပျိုးထောင်ခြင်း",
}

def calculate_growth_stages(chart: dict) -> dict:
    """Verify chart, then call the upstream twelve-stage getters directly."""
    checked=reading_facts("bazi",chart)
    assumed=chart["evidence"]["input_assumptions"]
    born=datetime.fromisoformat(assumed["birth_wall_clock"])
    sect=assumed["sect"]
    try:
        from lunar_python import Solar
    except ImportError as exc:
        raise RuntimeError("lunar-python required for Chang Sheng") from exc
    upstream=Solar.fromYmdHms(
        born.year,born.month,born.day,born.hour,born.minute,born.second
    ).getLunar().getEightChar()
    upstream.setSect(sect)
    pillars={
        "year":upstream.getYear(),
        "month":upstream.getMonth(),
        "day":upstream.getDay(),
        "hour":upstream.getTime(),
    }
    if pillars!=checked["facts"].copy() | {"day_master":checked["facts"]["day_master"]}:
        # Compare the four pillars only, not the separately derived day master.
        if any(pillars[name]!=checked["facts"][name] for name in pillars):
            raise ValueError("Twelve-stage upstream chart differs from verified pillars")
    stages={
        "year":upstream.getYearDiShi(),
        "month":upstream.getMonthDiShi(),
        "day":upstream.getDayDiShi(),
        "hour":upstream.getTimeDiShi(),
    }
    if set(stages)!={"year","month","day","hour"} or any(s not in STAGE_NAMES for s in stages.values()):
        raise ValueError("Upstream provided unknown Twelve Growth Stage")
    evidence=Evidence(
        rule_id=RULE_ID,
        tradition="Chinese BaZi Twelve Chang Sheng",
        method="Use 6tail/lunar-python EightChar.getYear/Month/Day/TimeDiShi relative to the checked Day Master, sect and four branch indices",
        input_assumptions={
            "birth_wall_clock":born.isoformat(),
            "sect":sect,
            "timezone_verified":assumed.get("timezone_verified"),
            "chart_rule_id":chart["evidence"]["rule_id"],
            "true_solar_time_applied":False,
        },
        derived_facts={"pillars":pillars,"day_master":chart["day_master"],"stages":stages},
        reference="6tail/lunar-python lunar_python/EightChar.py, CHANG_SHENG and getYearDiShi/getMonthDiShi/getDayDiShi/getTimeDiShi; https://github.com/6tail/lunar-python",
    )
    return {
        "stages":stages,
        "burmese_stage_names":{p:STAGE_GLOSSES[s] for p,s in stages.items()},
        "day_master":chart["day_master"],
        "rule_id":RULE_ID,
        "evidence":asdict(evidence),
        "prediction_supported":False,
        "seasonal_strength_calculated":False,
    }

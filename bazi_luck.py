"""BaZi Da Yun (十年大运) from the upstream 6tail lunar-python method.

Requires explicit gender in the particular upstream convention. Do not infer
gender from a person's name, account, pronouns, or birthdate. Users can opt
out; this optional traditional calculation is not required for basic BaZi.
Gender encoding and Yun sect are library-specific, not universal doctrine.
"""
from datetime import datetime
from dataclasses import asdict
from astro_core import Evidence

def calculate_bazi_luck(birth_local: datetime, *, gender: int,
                        yun_sect: int = 1, day_sect: int = 2,
                        cycles: int = 8, timezone_verified: str | None = None) -> dict:
    if not isinstance(birth_local, datetime) or birth_local.tzinfo is not None:
        raise ValueError("Provide a naive local birth wall-clock datetime")
    if not 1900 <= birth_local.year <= 2100:
        raise ValueError("Birth year out of supported range")
    if type(gender) is not int or gender not in (0, 1):
        raise ValueError("Explicit upstream Yun convention gender code 0/1 required")
    if type(yun_sect) is not int or yun_sect not in (1, 2):
        raise ValueError("Yun sect must be 1 or 2")
    if type(day_sect) is not int or day_sect not in (1, 2):
        raise ValueError("Day pillar sect must be 1 or 2")
    if type(cycles) is not int or not 1 <= cycles <= 12:
        raise ValueError("Cycles must be 1 through 12")
    try:
        from lunar_python import Solar
    except ImportError as exc:
        raise RuntimeError("Install lunar-python for Da Yun calculations") from exc
    solar=Solar.fromYmdHms(birth_local.year,birth_local.month,birth_local.day,
                           birth_local.hour,birth_local.minute,birth_local.second)
    eight=solar.getLunar().getEightChar()
    eight.setSect(day_sect)
    yun=eight.getYun(gender,yun_sect)
    start=yun.getStartSolar()
    periods=[]
    for period in yun.getDaYun(cycles+1):
        if period.getIndex()==0:
            continue  # Pre-luck period: blank GanZhi, not a full ten-year cycle.
        periods.append({
            "index":period.getIndex(),
            "gan_zhi":period.getGanZhi(),
            "start_year":period.getStartYear(),
            "end_year":period.getEndYear(),
            "start_age_nominal":period.getStartAge(),
            "end_age_nominal":period.getEndAge(),
        })
    for i,item in enumerate(periods):
        if len(item["gan_zhi"])!=2 or item["end_year"]-item["start_year"]!=9:
            raise ValueError("Invalid Da Yun decade returned by upstream library")
        if i and item["start_year"]!=periods[i-1]["end_year"]+1:
            raise ValueError("Discontinuous Da Yun periods")
    start_date=f"{start.getYear():04d}-{start.getMonth():02d}-{start.getDay():02d}"
    evidence=Evidence(
        rule_id="CHN-BAZI-DAYUN-001",
        tradition="Chinese BaZi / Da Yun",
        method="lunar-python EightChar.getYun(gender, sect).getDaYun(n); jie boundary and forward/reverse sequencing",
        input_assumptions={
            "birth_wall_clock":birth_local.isoformat(),
            "birth_place_timezone":timezone_verified,
            "gender_explicit_library_convention":gender,
            "yun_sect":yun_sect,
            "day_sect":day_sect,
            "true_solar_time_applied":False,
            "ages_are_east_asian_nominal":True,
        },
        derived_facts={"start_date_local":start_date,"forward":yun.isForward(),"periods":periods},
        reference="6tail/lunar-python: lunar_python/EightChar.py getYun; eightchar/Yun.py and DaYun.py",
    )
    return {
        "forward":yun.isForward(),
        "start_offset":{"years":yun.getStartYear(),"months":yun.getStartMonth(),
                        "days":yun.getStartDay(),"hours":yun.getStartHour()},
        "first_start_date_local":start_date,
        "periods":periods,
        "evidence":asdict(evidence),
    }

"""BaZi Four Pillars adapter; no claims of forecasting accuracy.

IMPORTANT: input is civil time at the BIRTH LOCATION, not UTC.
Timezone/solar-time normalization is the caller's responsibility.
"""
from dataclasses import asdict
from datetime import datetime
from astro_core import Evidence


def calculate_bazi(birth_local: datetime, *, sect: int = 2) -> dict:
    """Use lunar-python's solar-term aware Four Pillars algorithms.

    Caller must confirm birth location's historical timezone and time convention.
    Sect 1/2 changes how the day pillar is handled near the late-night boundary.
    """
    if birth_local.tzinfo is not None:
        raise ValueError('Provide a naive wall-clock datetime for the birth location; resolve timezone upstream')
    if sect not in (1, 2):
        raise ValueError('sect must be 1 or 2')
    if not 1900 <= birth_local.year <= 2100:
        raise ValueError('Supported birth year range for this initial adapter is 1900–2100')
    try:
        from lunar_python import Solar
    except ImportError as exc:
        raise RuntimeError('Install lunar-python to calculate BaZi') from exc

    solar = Solar.fromYmdHms(birth_local.year, birth_local.month, birth_local.day, birth_local.hour, birth_local.minute, birth_local.second)
    chart = solar.getLunar().getEightChar()
    chart.setSect(sect)
    pillars = {'year':chart.getYear(), 'month':chart.getMonth(), 'day':chart.getDay(), 'hour':chart.getTime()}
    elements = {'year':chart.getYearWuXing(), 'month':chart.getMonthWuXing(), 'day':chart.getDayWuXing(), 'hour':chart.getTimeWuXing()}
    ten_gods = {'year':chart.getYearShiShenGan(), 'month':chart.getMonthShiShenGan(), 'hour':chart.getTimeShiShenGan()}
    evidence=Evidence(rule_id='CHN-BAZI-PILLARS-001',tradition='Chinese BaZi (Four Pillars)',method='lunar-python Solar -> Lunar -> EightChar; Li Chun and jieqi-based conventions as implemented by library',input_assumptions={'birth_wall_clock':birth_local.isoformat(),'sect':sect,'timezone_normalized':False,'true_solar_time_applied':False},derived_facts={'pillars':pillars},reference='6tail/lunar-python EightChar.py and upstream EightCharTest.py')
    return {'pillars':pillars, 'elements':elements,'day_master':chart.getDayGan(),'ten_gods_stems':ten_gods,'evidence':asdict(evidence)}

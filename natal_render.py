"""Bounded, privacy-safe Telegram HTML renderer for provisional natal charts.

Consumes the already validated natal_pipeline result. Do not label a mocked or
user-supplied ephemeris as independently validated. Formatting only: no
new astronomical numbers are invented here.
"""
from html import escape
from math import isfinite
from western_aspects import calculate_aspects
from western_houses import whole_sign_houses
from astro_core import SIGNS

MAX_TELEGRAM_CHARS=4096
MAX_ASPECT_ROWS=12

def render_natal_preview(chart: dict) -> str:
    if not isinstance(chart,dict) or chart.get("status")!="provisional_pending_independent_chart_benchmarks":
        raise ValueError("A recognised provisional natal chart is required")
    birth=chart.get("birth")
    rising=chart.get("rising")
    planets=chart.get("planets")
    aspects=chart.get("aspects")
    if not isinstance(birth,dict) or not isinstance(rising,dict) or not isinstance(planets,dict) or not isinstance(aspects,list):
        raise ValueError("Missing natal chart sections")
    if rising.get("rising_sign") not in SIGNS or len(rising.get("whole_sign_houses",[]))!=12:
        raise ValueError("Incomplete Whole Sign Houses")
    if not isinstance(birth.get("utc"),str) or not birth.get("utc"):
        raise ValueError("Unknown birth instant")
    if not isinstance(chart.get("position_evidence"),dict):
        raise ValueError("Planetary calculation provenance required")
    ascendant = rising.get("ascendant_longitude")
    if (isinstance(ascendant,bool) or not isinstance(ascendant,(int,float))
            or not isfinite(ascendant) or not 0 <= ascendant < 360):
        raise ValueError("Invalid ascendant longitude")
    expected_houses = whole_sign_houses(ascendant)
    if rising["whole_sign_houses"] != expected_houses:
        raise ValueError("Houses do not match the ascendant")
    if rising["rising_sign"] != expected_houses[0]["sign"]:
        raise ValueError("Rising sign does not match the ascendant")
    if not 1<=len(planets)<=20:
        raise ValueError("Planetary positions missing or excessive")
    lines=[
        "<b>Western Natal Chart — Development Preview</b>",
        "━━━━━━━━━━━━━━",
        f'Rising Sign — <b>{escape(rising["rising_sign"])}</b>',
        f'Ascendant — <b>{float(rising["ascendant_longitude"]):.2f}°</b>',
        f'Birth Instant (UTC) — <code>{escape(birth["utc"])}</code>',
        "",
        "<b>Tropical Ecliptic Positions</b>",
    ]
    for name,body in sorted(planets.items()):
        if not isinstance(body,dict) or body.get("sign") not in SIGNS:
            raise ValueError("Invalid planet entry")
        degrees=body.get("degree_in_sign")
        longitude=body.get("longitude")
        house=body.get("whole_sign_house")
        if type(house) is not int or not 1<=house<=12 or not isinstance(longitude,(int,float)) or not isfinite(longitude) or not 0<=longitude<360:
            raise ValueError("Invalid celestial position")
        # Calculate display degree directly from the checked numeric longitude.
        if SIGNS[int(longitude//30)] != body["sign"]:
            raise ValueError("Planet sign differs from longitude")
        expected_house=(SIGNS.index(body["sign"])-SIGNS.index(rising["rising_sign"]))%12+1
        if house != expected_house:
            raise ValueError("Planet house differs from rising sign")
        position=round(float(longitude)%30,2)
        lines.append(f'{escape(str(name))}: {escape(body["sign"])} {position:.2f}° — House {house}')
    # Reject altered display results even when the caller changes a planet
    # position but leaves the other derived fields plausible.
    verified_degrees = {name:body["longitude"] for name,body in planets.items()}
    expected_aspects = calculate_aspects(verified_degrees)["aspects"]
    if aspects != expected_aspects:
        raise ValueError("Aspects differ from supplied planetary longitudes")
    lines += ["", "<b>Whole Sign Houses</b>"]
    houses=rising["whole_sign_houses"]
    if {h.get("house") for h in houses}!=set(range(1,13)):
        raise ValueError("Incomplete numbered houses")
    for i in range(0,12,3):
        lines.append(" · ".join(f'{h["house"]}: {escape(h["sign"])}' for h in houses[i:i+3]))
    if aspects:
        lines+=["", "<b>Major Aspects (smallest orbs first)</b>"]
        for item in aspects[:MAX_ASPECT_ROWS]:
            if not isinstance(item,dict):
                raise ValueError("Malformed aspect")
            lines.append(
                f'{escape(str(item["point_a"]))} · {escape(str(item["point_b"]))}'
                f' — {escape(str(item["aspect"]))} (orb {float(item["orb"]):.2f}°)'
            )
        if len(aspects)>MAX_ASPECT_ROWS:
            lines.append(f'နောက်ထပ် Aspects {len(aspects)-MAX_ASPECT_ROWS} ခု ရှိပါသေးသည်။')
    lines += [
        "",
        "Ephemeris နှင့် မွေးရပ်ဒေသရဲ့ Timezone/Coordinates ကို စစ်ပြီးမှ တွက်ထားသော "
        "Astronomy Preview ဖြစ်သည်။ Ascendant သည် Mean Sidereal/Whole Sign နည်းဖြစ်သည်။",
        "Independent Full Natal Benchmark နဲ့ ကျမ်းကိုးအနက်ဖွင့်မှု မပြီးသေးသောကြောင့် "
        "အပြည့်အဝ အတည်ပြုပြီး ဟောစာတမ်းအဖြစ် မသုံးပါနှင့်။",
    ]
    body="\n".join(lines)
    if len(body)>MAX_TELEGRAM_CHARS:
        raise ValueError("Natal preview would exceed Telegram message limit")
    return body

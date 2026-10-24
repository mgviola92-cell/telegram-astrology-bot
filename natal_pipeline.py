"""Private Western natal calculation orchestrator.

Combines a birth-place wall clock, explicitly provided IANA timezone and
geographic coordinates with the local Skyfield ephemeris adapter, mean
ascendant / Whole Sign Houses and annual profections.

Development backend only: no Telegram command is exposed until its position
fixtures, horoscope provenance and geographic conventions are reviewed.
"""
from datetime import datetime, date, timezone
from pathlib import Path
from astro_core import SIGNS, annual_profection
from birth_time import normalize_birth_wall_time
from western_houses import calculate_whole_sign_chart, _finite
from western_chart import geocentric_chart


def assemble_natal(
    wall_clock: datetime,
    birth_timezone: str,
    latitude: float,
    longitude_east: float,
    ephemeris_path: str,
    *,
    evaluation_date: date | None = None,
    fold: int | None = None,
    position_provider=None,
) -> dict:
    """Build one natal record; reject missing/ambiguous time and location.

    position_provider is a test seam: a callable(aware UTC datetime, path)
    yielding the same mapping as geocentric_chart. Production uses Skyfield.
    """
    if not isinstance(wall_clock, datetime):
        raise ValueError("An exact birth wall-clock datetime is required")
    lat = _finite(latitude, -65, 65, "latitude")
    lon = _finite(longitude_east, -180, 180, "longitude")
    if not isinstance(ephemeris_path, str) or not ephemeris_path.strip():
        raise ValueError("Specify an ephemeris path")
    birth = normalize_birth_wall_time(wall_clock, birth_timezone, fold=fold)
    utc = birth["utc_time"]
    if utc > datetime.now(timezone.utc):
        raise ValueError("Future birth instant is invalid")
    date_for_profection = evaluation_date if evaluation_date is not None else utc.date()
    if not isinstance(date_for_profection, date) or isinstance(date_for_profection, datetime):
        raise ValueError("Evaluation date must be a date")
    if date_for_profection < wall_clock.date():
        raise ValueError("Evaluation date cannot precede local birth date")
    house_data = calculate_whole_sign_chart(utc, lon, lat)
    provider = geocentric_chart if position_provider is None else position_provider
    positions = provider(utc, ephemeris_path)
    if not isinstance(positions, dict) or not positions.get("points") or not isinstance(positions.get("aspects"), list):
        raise ValueError("Invalid position provider result")
    if len(house_data["whole_sign_houses"]) != 12 or house_data["rising_sign"] not in SIGNS:
        raise ValueError("Invalid Whole Sign House result")
    rising_index = SIGNS.index(house_data["rising_sign"])
    enriched = {}
    for key, entry in positions["points"].items():
        if not isinstance(entry, dict) or entry.get("sign") not in SIGNS:
            raise ValueError("Position provider returned invalid zodiac sign")
        sign_index = SIGNS.index(entry["sign"])
        house = (sign_index - rising_index) % 12 + 1
        enriched[key] = dict(entry, whole_sign_house=house)
    profection = annual_profection(wall_clock.date(), date_for_profection, house_data["rising_sign"])
    profection["evidence"]["input_assumptions"]["ascendant_verified_external"] = False
    return {
        "birth": {
            "utc": utc.isoformat(),
            "wall_clock": wall_clock.isoformat(),
            "iana_timezone": birth_timezone,
            "dst_fold": birth["fold"],
            "latitude": lat,
            "longitude_east": lon,
            "true_solar_time_applied": False,
        },
        "rising": house_data,
        "planets": enriched,
        "aspects": positions["aspects"],
        "annual_profection": profection,
        "position_evidence": positions.get("evidence"),
        "status": "provisional_pending_independent_chart_benchmarks",
    }

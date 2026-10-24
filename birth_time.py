"""Birth-place civil-time validation for accurate historical timezone handling.

Timezone identifiers must be explicit IANA zones; do not infer from Telegram
profile timezone or bot server location. This does not implement true solar time.
"""
from datetime import datetime, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


def normalize_birth_wall_time(wall_time: datetime, iana_timezone: str, fold: int | None = None) -> dict:
    if wall_time.tzinfo is not None:
        raise ValueError('Birth wall-clock datetime must be naive')
    if not iana_timezone or iana_timezone.upper() in {'UTC', 'ETC/UTC'}:
        raise ValueError('Specify the birth location historical IANA timezone')
    try:
        zone=ZoneInfo(iana_timezone)
    except (ZoneInfoNotFoundError, ValueError, TypeError) as exc:
        raise ValueError('Unknown IANA timezone') from exc
    candidates=[]
    for f in (0,1):
        zoned=wall_time.replace(tzinfo=zone,fold=f)
        utc=zoned.astimezone(timezone.utc)
        roundtrip=utc.astimezone(zone)
        if roundtrip.replace(tzinfo=None)==wall_time and roundtrip.fold==f:
            candidates.append((f,utc,zoned.utcoffset()))
    # Normal times can have only fold=0, or both folds with equivalent offsets
    if not candidates:
        raise ValueError('Civil wall-clock time does not exist in this timezone (DST jump)')
    offsets={entry[2] for entry in candidates}
    ambiguous=len(offsets)>1
    if ambiguous and fold is None:
        raise ValueError('Ambiguous birth time during DST fall-back; specify fold=0 or fold=1')
    if fold is not None and fold not in (0,1):
        raise ValueError('fold must be 0 or 1')
    selected=next((x for x in candidates if x[0]==(fold if ambiguous else 0)),None)
    if not selected:
        raise ValueError('Invalid fold for this wall-clock time')
    return {
        'wall_time':wall_time,
        'timezone':iana_timezone,
        'fold':selected[0],
        'utc_time':selected[1],
        'utc_offset_seconds':int(selected[2].total_seconds()),
        'dst_ambiguous':ambiguous,
        'true_solar_time_applied':False,
    }

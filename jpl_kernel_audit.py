"""Audit a local JPL SPK kernel before any Western Natal chart calculation.

No downloading, networking, or logging of users' birth information. Uses
Skyfield's documented segment map, not a filename-based claim of coverage.
"""
from datetime import datetime, timezone
from pathlib import Path
from western_chart import TARGETS

REQUIRED_TARGETS = {"earth":399}
REQUIRED_TARGETS.update({v:v for v in TARGETS.values()})

def validate_kernel_segments(kernel, moment: datetime) -> dict:
    if not isinstance(moment, datetime) or moment.tzinfo is None or moment.utcoffset() is None:
        raise ValueError("Timezone-aware astronomical instant required")
    missing = []
    for name in REQUIRED_TARGETS:
        try:
            kernel[name]
        except (KeyError, ValueError):
            missing.append(name)
    if missing:
        raise ValueError("JPL ephemeris missing required objects: " + ", ".join(sorted(missing)))
    # A kernel may include each body but not the requested time. Intersect
    # segment coverage across all SPK segments by checking the actual route
    # through the kernel at the requested epoch (performed in geocentric_chart).
    segments = getattr(kernel, "segments", ())
    if not segments:
        raise ValueError("JPL ephemeris contains no segments")
    jd = moment.astimezone(timezone.utc).toordinal() + 1721424.5
    utc = moment.astimezone(timezone.utc)
    jd += (utc.hour * 3600 + utc.minute * 60 + utc.second
           + utc.microsecond / 1000000) / 86400
    # For each supported target chain, verify at least a segment exists whose
    # validity span includes the birth date. Final chained evaluation remains
    # Skyfield's responsibility.
    if not all(any(getattr(getattr(segment, "spk_segment", segment), "start_jd", float("inf")) <= jd <=
                   getattr(getattr(segment, "spk_segment", segment), "end_jd", float("-inf"))
                   and getattr(segment, "target", None) == target
                   for segment in segments)
               for target in (10, 301, 399, 1, 2, 3, 4, 5, 6, 7, 8, 9, 199, 299, 499)):
        raise ValueError("JPL ephemeris does not cover the requested date and planetary targets")
    return {
        "target_count": len(REQUIRED_TARGETS),
        "birth_jd": round(jd, 8),
        "valid": True,
        "planet_centers_and_barycenters_distinguished": True,
    }

def audit_kernel_file(path: str, moment: datetime) -> dict:
    source = Path(path)
    if source.suffix.lower() != ".bsp" or not source.is_file():
        raise ValueError("Existing local JPL .bsp file required")
    from skyfield.api import load_file
    from contextlib import closing
    with closing(load_file(str(source.resolve()))) as kernel:
        return validate_kernel_segments(kernel, moment)

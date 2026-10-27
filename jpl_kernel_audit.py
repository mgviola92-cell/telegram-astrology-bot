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
    # JPL SPK segments describe center -> target links. A target may exist
    # without an Earth-connected chain. Check reachability from Solar-System
    # barycenter (0) through only segments covering the requested epoch.
    # Segment bounds are TDB Julian days; the UTC estimate below is only a
    # conservative preflight and Skyfield performs final TDB evaluation.
    utc = moment.astimezone(timezone.utc)
    active_edges = {}
    for segment in segments:
        spk = getattr(segment, "spk_segment", segment)
        start = getattr(spk, "start_jd", None)
        end = getattr(spk, "end_jd", None)
        center = getattr(segment, "center", getattr(spk, "center", None))
        target = getattr(segment, "target", getattr(spk, "target", None))
        if start is None or end is None or center is None or target is None:
            raise ValueError("Unrecognized JPL SPK segment metadata")
        # UTC can differ from TDB by tens of seconds; retain an adequate
        # preflight margin, with the actual evaluation authoritative.
        margin_days = 120 / 86400
        if start - margin_days <= jd <= end + margin_days:
            active_edges.setdefault(center, set()).add(target)
    reachable = {0}
    frontier = [0]
    while frontier:
        for node in active_edges.get(frontier.pop(), ()):
            if node not in reachable:
                reachable.add(node)
                frontier.append(node)
    required_codes = {10, 301, 399, 199, 299, 499, 5, 6, 7, 8, 9}
    missing_codes = required_codes - reachable
    if missing_codes:
        raise ValueError(
            "JPL ephemeris lacks an active barycentric path to: " +
            ", ".join(str(code) for code in sorted(missing_codes))
        )
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

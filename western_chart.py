"""Western tropical zodiac chart calculations with an explicitly provided ephemeris.

No remote downloads and no default birth city/clock. The caller provides an
aware UTC instant and an existing JPL SPK kernel file. This engine currently
computes geocentric apparent tropical ecliptic longitudes; no rising sign,
houses or topocentric correction is claimed.
"""
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from astro_core import Evidence, SIGNS
from western_aspects import calculate_aspects, validate_longitude

# DE421 and DE440s contain barycenters for outer planets. "Pluto" is
# accurately labelled as Pluto barycenter, not claimed to be the planet.
TARGETS = {
    "Sun": "sun",
    "Moon": "moon",
    "Mercury": "mercury",
    "Venus": "venus",
    "Mars": "mars",
    "Jupiter": "jupiter barycenter",
    "Saturn": "saturn barycenter",
    "Uranus": "uranus barycenter",
    "Neptune": "neptune barycenter",
    "Pluto barycenter": "pluto barycenter",
}

def tropical_sign(longitude: float) -> dict:
    longitude=validate_longitude(longitude)
    index=int(longitude // 30)
    return {"sign": SIGNS[index], "degree_in_sign": round(longitude-index*30, 8)}

def chart_from_longitudes(longitudes: dict[str,float], *, verified_source: str) -> dict:
    """Deterministic chart postprocessing; does NOT verify caller coordinates."""
    if not verified_source or not verified_source.strip():
        raise ValueError("Identify the provenance of supplied longitudes")
    if not longitudes:
        raise ValueError("At least one astronomical position is required")
    points={str(key): tropical_sign(value) | {"longitude":validate_longitude(value)}
            for key,value in longitudes.items()}
    angles=calculate_aspects(longitudes)
    evidence=Evidence(
        rule_id="WEST-TROPICAL-LONGITUDES-001",
        tradition="Western tropical zodiac",
        method="Geocentric tropical ecliptic longitude / 30-degree signs; angular aspects",
        input_assumptions={"position_source":verified_source,
                           "birth_time_and_ephemeris_verified_by_caller":False},
        derived_facts={"points":points,"aspects":angles["aspects"]},
        reference="Skyfield ecliptic_frame documentation: https://rhodesmill.org/skyfield/coordinates.html",
    )
    return {"points":points,"aspects":angles["aspects"],"evidence":asdict(evidence)}

def geocentric_chart(birth_utc: datetime, ephemeris_path: str) -> dict:
    """Compute selected apparent coordinates with local JPL ephemeris.

    The requested time must be timezone aware; converted to UTC explicitly.
    Kernel is never downloaded or stored in the database.
    """
    if birth_utc.tzinfo is None or birth_utc.utcoffset() is None:
        raise ValueError("An aware birth datetime is required")
    if not ephemeris_path or not Path(ephemeris_path).is_file():
        raise FileNotFoundError("Download and license-check an ephemeris separately")
    try:
        from contextlib import closing
        from skyfield.api import load, load_file
        from skyfield.framelib import ecliptic_frame
    except ImportError as exc:
        raise RuntimeError("Install skyfield to compute astronomical positions") from exc
    utc=birth_utc.astimezone(timezone.utc)
    ts=load.timescale()
    t=ts.from_datetime(utc)
    with closing(load_file(str(Path(ephemeris_path).resolve()))) as kernel:
        from jpl_kernel_audit import validate_kernel_segments
        validate_kernel_segments(kernel, utc)
        earth=kernel["earth"]
        values={}
        for label,target in TARGETS.items():
            try:
                pos=earth.at(t).observe(kernel[target]).apparent()
            except KeyError:
                # Explicitly report a missing SPK object, not silent partial chart.
                raise ValueError(f"Ephemeris has no target: {target}")
            _,lon,_=pos.frame_latlon(ecliptic_frame)
            values[label]=float(lon.degrees)%360
    out=chart_from_longitudes(values, verified_source=f"Skyfield; {Path(ephemeris_path).name}; {utc.isoformat()}")
    out["evidence"]["input_assumptions"]["birth_time_and_ephemeris_verified_by_caller"]=True
    out["evidence"]["input_assumptions"]["observer"]="geocentric"
    out["evidence"]["input_assumptions"]["apparent_positions"]=True
    out["evidence"]["input_assumptions"]["ephemeris_kernel"]=Path(ephemeris_path).name
    return out

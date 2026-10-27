"""Independent geometric audit of the MEAN-equinox Ascendant convention.

Vectors are expressed in the same mean equatorial/ecliptic orientation:
north celestial pole +Z, equinox +X. The ecliptic-horizon intersection
is checked by vector dot products, separately from the analytic atan2
implementation used by western_houses.ascendant_from_sidereal.
"""
import math
from western_houses import ascendant_from_sidereal

RULE_ID = "WEST-MEAN-ASC-VECTOR-CHECK-001"


def vector_horizon_audit(lst_degrees: float, latitude_degrees: float,
                         obliquity_degrees: float) -> dict:
    """Check the analytic Ascendant is on the horizon and on its eastern half."""
    for value in (lst_degrees, latitude_degrees, obliquity_degrees):
        if isinstance(value, bool) or not isinstance(value, (float, int)) or not math.isfinite(value):
            raise ValueError("Finite angles required")
    asc = ascendant_from_sidereal(lst_degrees, latitude_degrees, obliquity_degrees)
    theta = math.radians(lst_degrees)
    phi = math.radians(latitude_degrees)
    epsilon = math.radians(obliquity_degrees)
    lon = math.radians(asc)
    # Ecliptic longitude rotated into mean Earth-equatorial coordinates.
    x, y, z = (math.cos(lon), math.sin(lon) * math.cos(epsilon),
               math.sin(lon) * math.sin(epsilon))
    zenith = (math.cos(phi) * math.cos(theta),
              math.cos(phi) * math.sin(theta),
              math.sin(phi))
    east = (-math.sin(theta), math.cos(theta), 0)
    altitude_sine = x * zenith[0] + y * zenith[1] + z * zenith[2]
    east_projection = x * east[0] + y * east[1]
    if abs(altitude_sine) > 1e-10 or east_projection <= 0:
        raise ValueError("Calculated Ascendant is not the eastern horizon crossing")
    return {
        "ascendant_longitude": asc,
        "horizon_altitude_residual": altitude_sine,
        "east_direction_cosine": east_projection,
        "convention": "mean_sidereal_mean_obliquity_no_nutation",
        "rule_id": RULE_ID,
        "true_ecliptic_planetary_frame_matches": False,
    }

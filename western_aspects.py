"""Western major-aspect geometry; requires externally verified tropical longitudes.

No ephemeris, birth chart or forecast is calculated here. Orb limits represent
a documented configuration, not a scientifically established influence.
"""
import math
from dataclasses import asdict
from itertools import combinations
from astro_core import Evidence

MAJOR_ASPECTS={
    'conjunction':(0.0,8.0), 'sextile':(60.0,5.0),
    'square':(90.0,7.0), 'trine':(120.0,7.0),
    'opposition':(180.0,8.0)
}

def validate_longitude(value):
    if isinstance(value,bool) or not isinstance(value,(int,float)) or not math.isfinite(value):
        raise ValueError('Planet longitude must be a finite number')
    if not 0 <= value < 360:
        raise ValueError('Longitude must be between 0 (inclusive) and 360 (exclusive)')
    return float(value)

def angular_separation(a,b):
    a=validate_longitude(a)
    b=validate_longitude(b)
    diff=abs(a-b)
    return min(diff,360-diff)

def calculate_aspects(longitudes,*,orb_policy=None):
    if len(longitudes)>30:raise ValueError('Too many input points')
    policy=MAJOR_ASPECTS if orb_policy is None else orb_policy
    if not policy:raise ValueError('Orb policy required')
    for name,(angle,orb) in policy.items():
        if isinstance(angle,bool) or isinstance(orb,bool) or not all(
            isinstance(v,(int,float)) and math.isfinite(v) for v in (angle,orb)):
            raise ValueError('Invalid orb policy')
        if not (0<=angle<=180 and 0<=orb<=15):raise ValueError('Invalid aspect angle or orb range')
    positions={str(k):validate_longitude(v) for k,v in longitudes.items()}
    matches=[]
    for (a,la),(b,lb) in combinations(sorted(positions.items()),2):
        distance=angular_separation(la,lb)
        for aspect,(exact,max_orb) in policy.items():
            deviation=abs(distance-exact)
            if deviation<=max_orb+1e-10:
                matches.append({'point_a':a,'point_b':b,'aspect':aspect,
                    'angle':round(distance,8),'orb':round(deviation,8),
                    'exact_angle':exact,'max_orb':max_orb})
    matches.sort(key=lambda x:(x['orb'],x['point_a'],x['point_b'],x['aspect']))
    evidence=Evidence(rule_id='WEST-ASPECTS-GEOMETRY-001',
        tradition='Western tropical astrology',
        method='Shortest tropical ecliptic longitude separation and five major aspects with published orb policy',
        input_assumptions={'longitudes_are_verified_externally':False,
            'coordinates':'caller-provided tropical ecliptic degrees','orb_policy':policy},
        derived_facts={'aspects':matches},
        reference='Astrodienst: https://www.astro.com/astrology/in_aspect_e.htm')
    return {'aspects':matches,'evidence':asdict(evidence)}

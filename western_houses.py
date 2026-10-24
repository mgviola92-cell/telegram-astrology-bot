"""Mean-equinox tropical ascendant and Whole Sign Houses (Western only).

Implements a clearly identified MEAN sidereal/obliquity convention,
not a true/apparent sidereal calculation or Placidus house cusps. Verify
against independent birth-chart references before release.
"""
import math
from datetime import datetime, timezone

SIGNS=('Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces')

def _finite(value, minimum, maximum, name):
    if isinstance(value,bool) or not isinstance(value,(int,float)) or not math.isfinite(value) or not minimum<=value<=maximum:
        raise ValueError(f'{name} must be finite and between {minimum} and {maximum}')
    return float(value)

def julian_day(instant):
    if not isinstance(instant,datetime) or instant.tzinfo is None or instant.utcoffset() is None:
        raise ValueError('Birth instant must be timezone-aware')
    dt=instant.astimezone(timezone.utc)
    return dt.toordinal()+1721424.5+(dt.hour*3600+dt.minute*60+dt.second+dt.microsecond/1e6)/86400

def mean_obliquity(jd):
    T=(jd-2451545.0)/36525.0
    return 23+26/60+21.448/3600-(46.8150*T+0.00059*T*T-0.001813*T*T*T)/3600

def greenwich_mean_sidereal(jd):
    T=(jd-2451545.0)/36525.0
    return (280.46061837+360.98564736629*(jd-2451545.0)+0.000387933*T*T-T**3/38710000)%360

def ascendant_from_sidereal(lst_deg, latitude_deg, obliquity_deg):
    _finite(lst_deg,0,360,'sidereal degrees')
    lat=_finite(latitude_deg,-65,65,'latitude')
    eps=_finite(obliquity_deg,20,26,'obliquity')
    theta=math.radians(lst_deg)
    phi=math.radians(lat)
    epsilon=math.radians(eps)
    east=math.cos(theta)
    other=-(math.sin(theta)*math.cos(epsilon)+math.tan(phi)*math.sin(epsilon))
    if abs(east)<1e-14 and abs(other)<1e-14:
        raise ValueError('Undetermined ascendant geometry')
    result=math.degrees(math.atan2(east,other))%360
    return 0.0 if abs(result-360.0)<1e-10 else result

def whole_sign_houses(asc_longitude):
    asc=_finite(asc_longitude,0,360,'ascendant longitude')
    if asc==360: raise ValueError('Longitude is exclusive of 360')
    ascending=int(asc//30)
    return [{'house':i+1,'sign':SIGNS[(ascending+i)%12]} for i in range(12)]

def calculate_whole_sign_chart(birth_instant, longitude_east_deg, latitude_deg):
    longitude=_finite(longitude_east_deg,-180,180,'longitude')
    latitude=_finite(latitude_deg,-65,65,'latitude')
    jd=julian_day(birth_instant)
    lst=(greenwich_mean_sidereal(jd)+longitude)%360
    epsilon=mean_obliquity(jd)
    asc=ascendant_from_sidereal(lst,latitude,epsilon)
    return {'ascendant_longitude':round(asc,8), 'rising_sign':SIGNS[int(asc//30)], 'whole_sign_houses':whole_sign_houses(asc),
            'local_mean_sidereal_deg':round(lst,8), 'mean_obliquity_deg':round(epsilon,8),
            'metadata':{'method':'Meeus GMST + mean obliquity, eastern horizon intersection, Whole Sign Houses',
                        'latitude_limit':'-65 to +65 degrees', 'uses_geographic_longitude':True,
                        'nutation_and_refraction_applied':False,
                        'birth_time_verified_externally':False,
                        'reference':'Meeus Astronomical Algorithms GMST; https://www2.mps.mpg.de/homes/fraenz/systems/systems3art/node3.html'}}

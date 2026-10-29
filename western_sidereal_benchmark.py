"""Reference-vector audit for the mean Greenwich sidereal approximation.

Independent historical published vector from Meeus Astronomical
Algorithms, Example 11.b: 1987-04-10 19:21 UT,
JD 2446896.30625, GMST 8h34m57.0896s = 128.7378733 degrees.

USNO public approximate algorithm:
https://aa.usno.navy.mil/faq/GAST
NASA JPL mean sidereal reference:
https://spsweb.fltops.jpl.nasa.gov/portaldataops/mpg/MPG_Docs/MPG%20Book/Release/Chapter2-TimeScales.pdf

IMPORTANT: UT1 versus UTC and TT approximations remain; this only
benchmarks arithmetic consistency, NOT independent natal ephemerides.
"""
from datetime import datetime, timezone
from western_houses import julian_day, greenwich_mean_sidereal

EXAMPLE_1987_INSTANT=datetime(1987,4,10,19,21,tzinfo=timezone.utc)
EXAMPLE_1987_JD=2446896.30625
EXAMPLE_1987_GMST=128.7378733
J2000_INSTANT=datetime(2000,1,1,12,tzinfo=timezone.utc)
J2000_JD=2451545.0
J2000_GMST=280.46061837

RULE_ID="WEST-GMST-INDEPENDENT-VECTORS-001"

def angular_difference(a:float,b:float)->float:
    """Absolute shortest angle in degrees; handles 0/360 wrap."""
    return abs((a-b+180)%360-180)

def verify_gmst_reference_vectors()->dict:
    vectors=(
        ("Meeus_1987_example_11b",EXAMPLE_1987_INSTANT,EXAMPLE_1987_JD,EXAMPLE_1987_GMST,0.00002),
        ("J2000_epoch",J2000_INSTANT,J2000_JD,J2000_GMST,0.000001),
    )
    results=[]
    for name,instant,jd_expected,angle_expected,allowed_deg in vectors:
        jd=julian_day(instant)
        if abs(jd-jd_expected)>1e-7:
            raise ValueError("Julian Day reference vector differs: "+name)
        observed=greenwich_mean_sidereal(jd)
        difference=angular_difference(observed,angle_expected)
        if difference>allowed_deg:
            raise ValueError("Sidereal angle reference vector differs: "+name)
        results.append({"name":name,"julian_day":jd,
                        "mean_sidereal_degrees":observed,
                        "reference_degrees":angle_expected,
                        "angular_residual_degrees":difference})
    return {
        "rule_id":RULE_ID,"vectors":results,
        "independent_natal_positions_benchmarked":False,
        "ascendant_vs_external_chart_benchmarked":False,
        "ut1_correction_applied":False,
        "status":"mean_greenwich_sidereal_arithmetic_only",
    }

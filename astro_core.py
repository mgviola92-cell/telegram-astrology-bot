"""Small, auditable traditional-calculation prototype; not a prediction engine."""
from dataclasses import dataclass, asdict
from datetime import date

SIGNS = ('Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces')
TRADITIONAL_RULERS = ('Mars','Venus','Mercury','Moon','Sun','Mercury','Venus','Mars','Jupiter','Saturn','Saturn','Jupiter')
HOUSE_TOPICS = ('identity and beginnings','resources','communication and learning','home and family','creativity and joy','work and routines','partnerships','shared resources','study and travel','career and public life','friends and community','solitude and retreat')

@dataclass(frozen=True)
class Evidence:
    rule_id: str
    tradition: str
    method: str
    input_assumptions: dict
    derived_facts: dict
    reference: str
    status: str = 'traditional_interpretation_not_empirically_verified'


def age_on(birth: date, at: date) -> int:
    if at < birth:
        raise ValueError('Evaluation date cannot precede birth date')
    return at.year - birth.year - ((at.month, at.day) < (birth.month, birth.day))


def annual_profection(birth: date, at: date, rising_sign: str) -> dict:
    """Whole-sign annual profections require a separately verified ascendant sign.

    This function does NOT calculate the ascendant from birth time/location.
    """
    if rising_sign not in SIGNS:
        raise ValueError('A known ascending zodiac sign is required')
    age = age_on(birth, at)
    house = age % 12 + 1
    sign_index = (SIGNS.index(rising_sign) + age) % 12
    sign = SIGNS[sign_index]
    evidence = Evidence(
        rule_id='WEST-HEL-ANNUAL-PROFECTION-001',
        tradition='Hellenistic / whole-sign Western',
        method='house = age mod 12 + 1; activated sign = rising sign shifted by age',
        input_assumptions={'birth_date':birth.isoformat(),'evaluation_date':at.isoformat(), 'ascendant_sign':rising_sign,'ascendant_verified_external':False},
        derived_facts={'age':age, 'activated_house':house, 'activated_sign':sign, 'traditional_lord_of_year':TRADITIONAL_RULERS[sign_index]},
        reference='Chris Brennan, Hellenistic Astrology (2017), ch. 17; Vettius Valens, Anthology',
    )
    return {'house':house,'sign':sign,'lord_of_year':TRADITIONAL_RULERS[sign_index], 'house_topic':HOUSE_TOPICS[house-1], 'evidence':asdict(evidence)}


def reduce_number(n: int, preserve_master: bool = True) -> int:
    if n < 0:
        raise ValueError('Number must be non-negative')
    while n > 9 and not (preserve_master and n in (11,22,33)):
        n = sum(int(d) for d in str(n))
    return n


def life_path(date_of_birth: date, preserve_master: bool = True) -> dict:
    """One explicit modern Pythagorean-style convention: separately reduce Y/M/D."""
    month = reduce_number(date_of_birth.month, preserve_master)
    day = reduce_number(date_of_birth.day, preserve_master)
    year = reduce_number(sum(map(int,str(date_of_birth.year))), preserve_master)
    final = reduce_number(month + day + year, preserve_master)
    evidence = Evidence(
        rule_id='NUM-PYT-LIFE-PATH-001', tradition='Pythagorean-style numerology',
        method='reduce month, day, digits of year separately; sum and reduce; preserve 11/22/33',
        input_assumptions={'birth_date':date_of_birth.isoformat(),'preserve_master_numbers':preserve_master},
        derived_facts={'month_component':month,'day_component':day,'year_component':year,'life_path':final},
        reference='Conventional modern Pythagorean numerology; school-specific citation pending verification',
    )
    return {'number':final,'evidence':asdict(evidence)}

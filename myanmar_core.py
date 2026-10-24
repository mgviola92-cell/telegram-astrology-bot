"""Myanmar eight-day weekday naming (not Mahabote or a Myanmar lunar calendar).

The Burmese eight-day planetary weekday convention splits Wednesday at noon.
Civil date/time must already represent the birth location's wall clock.
"""
from dataclasses import asdict
from datetime import datetime
from astro_core import Evidence

# Python datetime.weekday(): Monday=0, Sunday=6
DAY_NAMES={
    0:('တနင်္လာ','Moon'),
    1:('အင်္ဂါ','Mars'),
    3:('ကြာသပတေး','Jupiter'),
    4:('သောကြာ','Venus'),
    5:('စနေ','Saturn'),
    6:('တနင်္ဂနွေ','Sun')
}

def myanmar_birth_day(birth_local: datetime) -> dict:
    """Return Myanmar traditional weekday; Wednesday 00:00–11:59 vs 12:00–23:59.

    Does not determine a lunar calendar date, house, planetary hour, or horoscope.
    """
    if birth_local.tzinfo is not None:
        raise ValueError('Pass local wall-clock time, without timezone; resolve historical timezone upstream')
    wd=birth_local.weekday()
    if wd==2:
        name, planet=('ဗုဒ္ဓဟူး (နံနက်ပိုင်း)','Mercury') if birth_local.hour<12 else ('ရာဟု (ဗုဒ္ဓဟူး မွန်းလွဲပိုင်း)','Rahu')
    else:
        name,planet=DAY_NAMES[wd]
    rule=Evidence(rule_id='MM-8DAY-WEEKDAY-001',tradition='Myanmar eight-day weekday convention',
        method='Gregorian weekday at birth location, with Wednesday split at 12:00 local civil time',
        input_assumptions={'birth_wall_clock':birth_local.isoformat(),'timezone_confirmed_by_user':False,'midday_cutoff': '12:00'},
        derived_facts={'weekday':name,'planetary_association':planet},
        reference='Myanmar traditional eight-day weekday planetary associations; calendar/date conversion is separate')
    return {'weekday':name,'planetary_association':planet,'evidence':asdict(rule)}

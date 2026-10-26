"""Verified calculation facts for Telegram astrology readings."""
from evidence_ui import RULES

EXPECTED = {'myanmar_calendar':'MM-CALENDAR-MMCAL-001','bazi':'CHN-BAZI-PILLARS-001','numerology':'NUM-PYT-LIFE-PATH-001'}

def require_evidence(kind, result):
    if kind not in EXPECTED or not isinstance(result,dict):
        raise ValueError('Unknown calculation or invalid result')
    evidence=result.get('evidence')
    rule=EXPECTED[kind]
    if not isinstance(evidence,dict) or evidence.get('rule_id')!=rule or rule not in RULES or not isinstance(evidence.get('derived_facts'),dict):
        raise ValueError('Verified provenance required')
    return rule

def reading_facts(kind,result):
    rule=require_evidence(kind,result)
    if kind=='bazi':
        pillars=result.get('pillars')
        if not isinstance(pillars,dict) or set(pillars)!={'year','month','day','hour'} or any(not isinstance(p,str) or len(p)!=2 for p in pillars.values()):
            raise ValueError('Four valid pillars required')
        if result.get('day_master')!=pillars['day'][0]:
            raise ValueError('Day master mismatches chart')
        facts={name:pillars[name] for name in ('year','month','day','hour')}
        facts['day_master']=result['day_master']
    elif kind=='numerology':
        n=result.get('number')
        if type(n) is not int or n not in set(range(1,10))|{11,22,33}:
            raise ValueError('Invalid life path')
        facts={'life_path':n}
    else:
        keys=('myanmar_year','month','day','mahabote','yatyaza','pyathada')
        if any(key not in result for key in keys) or type(result['yatyaza']) is not bool:
            raise ValueError('Missing Myanmar calendar facts')
        facts={key:result[key] for key in keys}
    return {'kind':kind,'rule_id':rule,'facts':facts,'prediction_supported':False,'interpretation_status':'calculated_facts_only'}

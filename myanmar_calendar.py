"""Myanmar calendar formulas adapted from Yan Naing Aye's mmcal (MIT).
Copyright (c) 2018 Yan Naing Aye. Original: github.com/yan9a/mmcal,
javascript/ceMmDateTime.js. Adaptation dated 2026-10-24.
Uses proleptic Gregorian LOCAL calendar dates, supported app range 1900-2100.
Calendrical results do not establish scientific validity of divination.
"""
from datetime import date
from math import floor
from dataclasses import asdict
from astro_core import Evidence

SY=1577917828.0/4320000.0
LM=1577917828.0/53433336.0
MO=1954168.050623
MONTHS={0:'First Waso',1:'Tagu',2:'Kason',3:'Nayon',4:'Waso',5:'Wagaung',6:'Tawthalin',7:'Thadingyut',8:'Tazaungmon',9:'Nadaw',10:'Pyatho',11:'Tabodwe',12:'Tabaung',13:'Late Tagu',14:'Late Kason'}
HOUSES=('Binga','Atun','Yaza','Adipati','Marana','Thike','Puti')

def year_constants(my):
    if my>=1312:
        ei,wo,nm,fme,wte=3,-.5,8,((1377,1),),(1344,1345)
    elif my>=1217:
        ei,wo,nm,fme,wte=2,-1,4,((1234,1),(1261,-1)),(1263,1264)
    elif my>=1100:
        ei,wo,nm,fme,wte=1.3,-.85,-1,((1120,1),(1126,-1),(1150,1),(1172,-1),(1207,1)),(1201,1202)
    elif my>=798:
        ei,wo,nm,fme,wte=1.2,-1.1,-1,tuple((y,-1) for y in (813,849,851,854,927,933,936,938,949,952,963,968,1039)),()
    else:
        ei,wo,nm,fme,wte=1.1,-1.1,-1,((205,1),(246,1),(471,1),(572,-1),(651,1),(653,2),(656,1),(672,1),(729,1),(767,-1)),()
    wo+=next((v for y,v in fme if y==my),0)
    return ei,wo,nm,int(my in wte)

def watat(my):
    ei,wo,nm,ew=year_constants(my)
    ta=(SY/12-LM)*(12-nm)
    ed=(SY*(my+3739))%LM
    if ed<ta:ed+=LM
    fm=floor(SY*my+MO-ed+4.5*LM+wo+.5)
    if ei>=2:
        w=int(ed>=LM-(SY/12-LM)*nm)
    else:
        w=floor(((my*7+2)%19)/12)
    return fm,w^ew

def year_details(my):
    next_full,year_type=watat(my)
    yd=0
    while True:
        yd+=1
        prev_full,prev_watat=watat(my-yd)
        if prev_watat or yd>=3:break
    if year_type:
        nd=(next_full-prev_full)%354
        year_type=floor(nd/31)+1
        if nd not in (30,31):raise ValueError('Myanmar watat discrepancy')
    return year_type,prev_full+354*yd-102

def jdn_to_myanmar(jdn):
    my=floor((jdn-.5-MO)/SY)
    myt,tg1=year_details(my)
    dd=jdn-tg1+1
    b=myt//2
    c=1//(myt+1)
    myl=354+(1-c)*30+b
    mmt=floor((dd-1)/myl)
    dd-=mmt*myl
    a=floor((dd+423)/512)
    mm=floor((dd-b*a+c*a*30+29.26)/29.544)
    e=floor((mm+12)/16)
    f=floor((mm+11)/16)
    md=dd-floor(29.544*mm-29.26)-b*e+c*f*30
    mm+=f*3-e*4+12*mmt
    return my,myt,mm,md

def moon_phase_and_fortnight(mm,md,myt):
    """Faithful adaptation of mmcal cal_mml, cal_mp and cal_mf."""
    month_length=30-(mm%2)
    if mm==3:
        month_length+=myt//2
    if md<1 or md>month_length:
        raise ValueError('Invalid Myanmar lunar day')
    phase=(md+1)//16+md//16+md//month_length
    return ('waxing','full moon','waning','new moon')[phase],md-15*(md//16)

def astrology_days(mm,wd):
    m=mm%4
    wd1=m//2+4
    wd2=(1-m//2+m%2)*(1+2*(m%2))
    yatyaza=wd in (wd1,wd2)
    wda=(1,3,3,0,2,1,2)
    pyathada=2 if m==0 and wd==4 else 1 if m==wda[wd] else 0
    return yatyaza,pyathada

def calculate_myanmar_calendar(local_day:date)->dict:
    if not isinstance(local_day,date):raise TypeError('Expected local Gregorian date')
    if not 1900<=local_day.year<=2100:raise ValueError('Application range 1900-2100')
    jdn=local_day.toordinal()+1721425
    my,myt,mm,md=jdn_to_myanmar(jdn)
    if mm not in MONTHS or not 1<=md<=30:raise ValueError('Invalid result; check reference data')
    phase,fortnight_day=moon_phase_and_fortnight(mm,md,myt)
    wd=(local_day.weekday()+2)%7
    yatyaza,pyathada=astrology_days(mm,wd)
    mahabote=HOUSES[(my-wd)%7]
    facts={'myanmar_year':my,'month_id':mm,'month_day':md,'moon_phase':phase,'fortnight_day':fortnight_day,'year_type':myt,'mahabote_house':mahabote,'yatyaza':yatyaza,'pyathada_type':pyathada}
    ev=Evidence(rule_id='MM-CALENDAR-MMCAL-001',tradition='Myanmar calendrical astrology',
        method='Proleptic Gregorian JDN -> Myanmar date, watat, yatyaza, pyathada, mahabote using mmcal',
        input_assumptions={'local_gregorian_date':local_day.isoformat(),'calendar_type':'proleptic Gregorian'},
        derived_facts=facts,reference='Yan Naing Aye, mmcal javascript/ceMmDateTime.js, MIT copyright 2018')
    return {'myanmar_year':my,'month':MONTHS[mm],'month_index':mm,'day':md,'year_type':myt,
            'moon_phase':phase,'fortnight_day':fortnight_day,'yatyaza':yatyaza,'pyathada':pyathada,'mahabote':mahabote,'evidence':asdict(ev)}

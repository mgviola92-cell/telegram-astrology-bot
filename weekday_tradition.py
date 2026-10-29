"""Myanmar 8-weekday animal/direction correspondence (cultural, not a forecast).

This supplements, but never changes, the independently verified Mahabote
seven-house calculation. Noon is the bot's documented Wednesday convention;
some historical/traditional systems place the boundary later in the day.
"""
from datetime import datetime
from myanmar_core import myanmar_birth_day

RULE_ID="MM-8DAY-ANIMAL-DIRECTION-001"
# Weekday order is datetime.weekday() Monday=0...Sunday=6.
# An explicit clock is required here; Wednesday is never guessed.
TRADITIONS={
    (0,None):("ကျား","အရှေ့","Moon"),
    (1,None):("ခြင်္သေ့","အရှေ့တောင်","Mars"),
    (2,"am"):("အစွယ်ရှိဆင်","တောင်","Mercury"),
    (2,"pm"):("အစွယ်မဲ့ဆင် (ဟိုင်း)","အနောက်မြောက်","Rahu"),
    (3,None):("ကြွက်","အနောက်","Jupiter"),
    (4,None):("ပူး","မြောက်","Venus"),
    (5,None):("နဂါး","အနောက်တောင်","Saturn"),
    (6,None):("ဂဠုန်","အရှေ့မြောက်","Sun"),
}
SOURCE=(
    "Myanmar eight-weekday animal and direction cultural correspondences; "
    "Myanmar cultural awareness reference (NYU Steinhardt): "
    "https://docs.steinhardt.nyu.edu/pdfs/metrocenter/xr1/Language_n_Cultural_Awareness/MYANMAR.pdf ; "
    "Myanmar Calendar: https://www.calendarmyanmar.com/zodiac-signs.html"
)
LIMITS=(
    "မြန်မာရိုးရာ နေ့နံအလိုက် သတ္တဝါနှင့် အရပ်မျက်နှာ သင်္ကေတအညွှန်းသာဖြစ်သည်။ "
    "ဗုဒ္ဓဟူးနေ့ကို မွန်းတည့် ၁၂ နာရီတွင် ခွဲထားခြင်းသည် ဤ Bot ၏ သတ်မှတ်ထားသော မူကွဲဖြစ်ပြီး "
    "ဒေသ၊ ဆရာနှင့် ရှေးဟောင်းစာပေအချို့တွင် ၁၈ နာရီ (ညနေ ၆) စသည့် မူကွဲများရှိသည်။ "
    "တိကျသောမွေးရပ်ဒေသစံတော်ချိန်လိုအပ်ပြီး ကိုယ်ရည်ကိုယ်သွေး၊ ကံကြမ္မာ၊ "
    "ရောဂါ သို့မဟုတ် ဖြစ်ရပ်ရလဒ်ကို သေချာမဟောနိုင်ပါ။"
)

def weekday_animal_info(birth_local:datetime)->dict:
    if type(birth_local) is not datetime or birth_local.tzinfo is not None:
        raise ValueError("Exact local naive birth datetime required")
    if not 1900<=birth_local.year<=2100:
        raise ValueError("Birth date outside supported calendar range")
    verified=myanmar_birth_day(birth_local)
    weekday=birth_local.weekday()
    key=(weekday,("am" if birth_local.hour<12 else "pm") if weekday==2 else None)
    animal,direction,planet=TRADITIONS[key]
    if planet!=verified["planetary_association"]:
        raise ValueError("Weekday animal mapping mismatches traditional day evidence")
    return {
        "weekday":verified["weekday"],
        "planet":planet,
        "animal":animal,
        "direction":direction,
        "rule_id":RULE_ID,
        "method":"weekday (Monday=0) with Wednesday 12:00 split in local civil time",
        "prediction_supported":False,
        "profile_saved":False,
    }

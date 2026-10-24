"""Public method summaries for stateless, privacy-preserving evidence buttons.

A method's rationale is not scientific proof that divination predicts the future.
Every listed ID must correspond to a real calculation or explicitly random draw.
"""
RULES = {
    'NUM-PYT-LIFE-PATH-001': {
        'heading': 'ဘဝလမ်းကြောင်းကိန်း',
        'method': 'မွေးလ၊ မွေးရက်နှင့် မွေးနှစ်ကိန်းတို့ကို သီးခြားပေါင်းလျှော့ပြီး ထပ်ပေါင်းလျှော့သည်။ 11, 22, 33 ကို Master Numbers အဖြစ်ထားသည်။',
        'source': 'Modern Pythagorean-style numerology convention (school-dependent; book-level citation pending)',
        'limits': 'နာမည်/မွေးနေ့ကိန်းဂဏန်း၏ ရိုးရာအနက်ဖွင့်ဆိုချက်သာ ဖြစ်ပြီး ဖြစ်ရပ်တစ်ခုကို အာမခံမဟုတ်ပါ။'
    },
    'CHN-BAZI-PILLARS-001': {
        'heading': 'တရုတ်ဇာတာလေးတိုင်',
        'method': 'မွေးရပ်ဒေသ ဒေသစံတော်ချိန်ကို lunar-python ၏ Solar -> Lunar -> EightChar စနစ်ထဲ ဖြတ်သန်းတွက်ချက်သည်။',
        'source': '6tail/lunar-python: lunar_python/EightChar.py and test/EightCharTest.py',
        'limits': 'မွေးရပ်ဒေသ၊ သမိုင်းဝင် timezone နှင့် True Solar Time ဆိုင်ရာ အတည်ပြုချက် မပြည့်စုံသေးသော စမ်းသပ်တွက်ချက်မှုဖြစ်သည်။'
    },
    'MM-8DAY-WEEKDAY-001': {
        'heading': 'မြန်မာ့ ၈ နေ့နံ',
        'method': 'မွေးရပ်ဒေသ၏ နေ့စွဲကနေ နေ့နံတွက်ပြီး ဗုဒ္ဓဟူးနေ့ကို မွန်းတည့် ၁၂ နာရီတွင် ခွဲသည်။',
        'source': 'Myanmar eight-day planetary weekday convention; Myanmar lunar calendar is calculated separately',
        'limits': 'မဟာဘုတ်အိမ်၊ နက္ခတ်၊ ရက်ရာဇာ၊ ပြဿဒါး တွက်ချက်ပြီးသော ဇာတာ မဟုတ်သေးပါ။'
    },
    'TAROT-DRAW-001': {
        'heading': 'တားရော့ကတ်ဆွဲခြင်း',
        'method': 'Major Arcana 22 + Minor Arcana 56 = 78 ကတ်ထဲမှ တစ်ချပ်စီ ကျပန်းရွေးသည်။ တစ်ကြိမ်တည်းတွင် ကတ်မထပ်စေပါ။',
        'source': 'Common 78-card tarot structure (Major and Minor Arcana)',
        'limits': 'ကတ်ရွေးခြင်းသည် ကျပန်းဖြစ်သည်။ ကျမ်းကိုးစိစစ်ထားသော Card Interpretations ကို နောက်အဆင့်တွင် ထည့်မည်။'
    }
}


def get_rule(rule_id: str) -> dict:
    if rule_id not in RULES:
        raise KeyError(rule_id)
    return RULES[rule_id]


def evidence_button(rule_id: str):
    from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
    if rule_id not in RULES:
        raise KeyError(rule_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='📖 ဤတွက်ချက်မှု၏ အခြေခံ', callback_data=f'evidence:{rule_id}')]
    ])

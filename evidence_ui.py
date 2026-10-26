"""Public method summaries for stateless, privacy-preserving evidence buttons.

A method's rationale is not scientific proof that divination predicts the future.
Every listed ID must correspond to a real calculation or explicitly random draw.
"""
RULES = {
    'WEST-ASPECTS-GEOMETRY-001': {
        'heading': 'အနောက်တိုင်းဇာတာ ဂြိုဟ်ထောင့်ဆက်သွယ်မှု',
        'method': 'Tropical Ecliptic Longitude နှစ်ခုအကြား အတိုဆုံးထောင့်ကိုတွက်ပြီး 0°, 60°, 90°, 120°, 180° နှင့် သတ်မှတ်ထားသော Orb များဖြင့် စစ်ဆေးသည်။',
        'source': 'Astrodienst Aspects: https://www.astro.com/astrology/in_aspect_e.htm ; orb sizes depend on a documented convention',
        'limits': 'အခြား Ephemeris မှ သီးခြားအတည်ပြုထားသော ဂြိုဟ်တည်နေရာကိုသာ ထည့်သွင်းရမည်။ ဤ Engine က မွေးဇာတာနှင့် ဂြိုဟ်တည်နေရာကို ကိုယ်တိုင်မတွက်သေးပါ။'
    },
    'MM-CALENDAR-DAY-SIGNALS-001': {
        'heading': 'မြန်မာပြက္ခဒိန် အခါပေးရက်များ',
        'method': 'mmcal မှ မြန်မာလ၊ လရက်၊ ဝါထပ်နှစ်နှင့် စနေ=၀ မှ သောကြာ=၆ နေ့နံဖြင့် ဥပုသ်/အဖိတ်၊ ရက်ရာဇာ/ပြဿဒါး၊ သမားညို၊ အမြိတ္တစုတ်၊ ဝါရမိတ္တုကြီး/ငယ်၊ ရက်ပုပ်၊ သမားဖြူ၊ နဂါးပေါ်၊ ရက်ယုတ်မာ၊ မဟာရက်ကြမ်း၊ ရှမ်းရက်၊ နဂါးခေါင်းလှည့်ရာအရပ်နှင့် နက္ခတ်အမျိုးအစားကို သက်ဆိုင်ရာ Formula အလိုက်တွက်သည်။ ပထမဝါဆိုကို ဝါဆို၊ နှောင်းတန်ခူး/ကဆုန်ကို သက်ဆိုင်ရာပုံမှန်လအဖြစ် ယူသော convention ကို မှတ်တမ်းတင်ထားသည်။',
        'source': 'Yan Naing Aye, Myanmar Astrological Calendar Days (2013), English and Myanmar originals: https://cool-emerald.blogspot.com/2013/12/myanmar-astrological-calendar-days.html ; https://coolemerald.blogspot.com/2013/12/blog-post.html',
        'limits': 'ဤရလဒ်သည် ရိုးရာနေ့ရက်အမျိုးအစား အညွှန်းသာဖြစ်သည်။ အနာဂတ်ကို သိပ္ပံနည်းကျ ခန့်မှန်းခြင်း မဟုတ်ပါ။ လအမည်မူကွဲ၊ အချို့ကျောင်း၏ မူကွဲများကို သီးခြားစစ်ဆေးရန် လိုသေးသည်။'
    },
    'MM-MAHABOTE-SEVEN-HOUSE-001': {
        'heading': 'မဟာဘုတ် ၇ အိမ် ဇာတာတွက်ချက်နည်း',
        'method': 'မွေးရက်၏ နေ့နံကို စနေ=၀ မှ သောကြာ=၆ စဉ်ဖြင့် နံပါတ်ချ၊ mmcal မှ မြန်မာသက္ကရာဇ်တွက်ပြီး (မြန်မာနှစ်−နေ့နံ) mod 7 ဖြင့် မွေးဖွားရာအိမ် ရှာသည်။ နေ့နံ ၇ မျိုးကို ပြန်လှန်တွက်၍ အိမ် ၇ လုံးလုံးမှာ ဂြိုဟ်နေရာချသည်။ ရာဟုသည် ၈ နေ့နံခွဲခြားချက်သာဖြစ်၍ မဟာဘုတ်အိမ်အသစ်မဖြစ်ပါ။',
        'source': 'Yan Naing Aye, Myanmar Astrological Calendar Days (2013), Mahabote; https://cool-emerald.blogspot.com/2013/12/myanmar-astrological-calendar-days.html ; Myanmar calendar algorithm: https://github.com/yan9a/mmcal',
        'limits': 'မွေးရက်သည် မွေးရပ်ဒေသ၏ Local Date ဖြစ်ရမည်။ ဤနည်းမှာ ၇ အိမ်တွက်ချက်မှုဖြစ်ပြီး အပြည့်အစုံကံကြမ္မာဟောကိန်း မဟုတ်ပါ။ ၁၉၀၀–၂၁၀၀ အတွင်းသာ တွက်သည်။'
    },
    'MM-MAHABOTE-SYMBOLIC-THEMES-001': {
        'heading': 'မဟာဘုတ်အိမ် ၇ မျိုး၏ ရိုးရာအနက်ဖွင့်နည်း',
        'method': 'တွက်ပြီးမှန်ကန်သော မဟာဘုတ်အိမ်အမည်ကို ရိုးရာဆိုင်ရာ သင်္ကေတအကြောင်းအရာနှင့် ချိတ်ဖော်ပြသည်။ အိမ်အမည်၊ ရိုးရာဆက်စပ်မှုနှင့် စဉ်းစားစရာ အနက်ကို သီးခြားထားသည်။ စာသားများမှာ မူရင်းရေးသားထားသော မြန်မာလို အကျဉ်းချုပ်ဖြစ်သည်။',
        'source': 'Traditional house names: Yan Naing Aye Myanmar Astrological Calendar Days (2013); seven-house interpretations cross-read against Mahabote school summaries, https://horo.kesta.store/academy/myanmar/placements-and-signals?lang=en',
        'limits': 'ကျောင်းနှင့် ဆရာအလိုက် အိမ်အနက်များ ကွဲပြားနိုင်သည်။ အိမ်အမည်တစ်ခုတည်းနှင့် ကျန်းမာရေး၊ အသက်၊ စီးပွားရေး၊ အနာဂတ်ကို မဆုံးဖြတ်နိုင်ပါ။ ဤသည် ယဉ်ကျေးမှုအခြေခံ သင်္ကေတအနက်သာဖြစ်သည်။'
    },
    'MM-CALENDAR-MMCAL-001': {
        'heading': 'မြန်မာပြက္ခဒိန်နှင့် မဟာဘုတ်',
        'method': 'Gregorian Local Date ကို Julian Day Number ပြောင်းပြီး mmcal ဝါထပ်နှစ်၊ မြန်မာလ၊ လရက်၊ ရက်ရာဇာ၊ ပြဿဒါးနှင့် မဟာဘုတ် Formula များကို အဆင့်ဆင့် တွက်ချက်သည်။',
        'source': 'Yan Naing Aye, mmcal, javascript/ceMmDateTime.js (MIT license, copyright 2018); https://github.com/yan9a/mmcal',
        'limits': '၁၉၀၀–၂၁၀၀ Gregorian ရက်စွဲအတွက် စမ်းသပ်ထားသော Calendar Calculation ဖြစ်သည်။ မဟာဘုတ်အိမ်ရလဒ်သည် အနာဂတ်ဟောကိန်း မဟုတ်သေးပါ။'
    },
    'NUM-PYT-LIFE-PATH-001': {
        'heading': 'ဘဝလမ်းကြောင်းကိန်း',
        'method': 'မွေးလ၊ မွေးရက်နှင့် မွေးနှစ်ကိန်းတို့ကို သီးခြားပေါင်းလျှော့ပြီး ထပ်ပေါင်းလျှော့သည်။ 11, 22, 33 ကို Master Numbers အဖြစ်ထားသည်။',
        'source': 'Modern Pythagorean-style numerology convention (school-dependent; book-level citation pending)',
        'limits': 'နာမည်/မွေးနေ့ကိန်းဂဏန်း၏ ရိုးရာအနက်ဖွင့်ဆိုချက်သာ ဖြစ်ပြီး ဖြစ်ရပ်တစ်ခုကို အာမခံမဟုတ်ပါ။'
    },
    'CHN-BAZI-VISIBLE-WUXING-001': {
        'heading': 'BaZi မြင်ရသော ဓာတ်ငါးပါး',
        'method': 'လေးတိုင်၏ Heavenly Stems ၄ လုံးနှင့် Earthly Branches ၄ လုံးကို ရိုးရာ အဓိကဓာတ်အလိုက်ရေတွက်သည်။',
        'source': 'Traditional Five Phases correspondences: https://www.ibiblio.org/chinesehistory/contents/08fea/c06s02.htm ; https://uaya.org/iching/correspondences/',
        'limits': 'Hidden Stems, Seasonal Strength နှင့် Day Master အားကောင်းမှု မတွက်ရသေးပါ။ အရေအတွက်တစ်ခုတည်းဖြင့် အနာဂတ်ဖြစ်ရပ် မဆုံးဖြတ်နိုင်ပါ။'
    },
    'CHN-BAZI-TENGODS-001': {
        'heading': 'BaZi Ten Gods (ဆယ်မျိုးဆက်စပ်မှု)',
        'method': 'Day Master နဲ့ Heavenly Stem တစ်ခုချင်းစီ၏ ဓာတ်မွေးပေးခြင်း၊ ဓာတ်ထိန်းချုပ်ခြင်း၊ Yin/Yang တူကွာခြင်းကို ရိုးရာစည်းမျဉ်းအတိုင်း တွက်ချက်သည်။',
        'source': '6tail/lunar-python: LunarUtil.SHI_SHEN; https://github.com/6tail/lunar-python',
        'limits': 'ဤရလဒ်သည် Stems အကြား ရိုးရာအမျိုးအစားခွဲခြားမှုသာဖြစ်ပြီး ကံကြမ္မာအာမခံချက်၊ Day Master အားကောင်းမှု၊ ဆေးဘက်/ငွေကြေးအကြံပြုချက် မဟုတ်ပါ။'
    },
    'CHN-BAZI-HIDDEN-STEMS-001': {
        'heading': 'BaZi ဌာနချုပ်အတွင်း ဝှက်ထားသော ဂန္ဓာရုံ (Hidden Stems)',
        'method': 'Earthly Branch ၁၂ မျိုးအလိုက် ထုံးတမ်း Hidden Stems (藏干) ကို အဓိကဓာတ်မှစ၍ မူရင်းအစဉ်အတိုင်း ဖော်ပြသည်။',
        'source': '6tail/lunar-python: lunar_python/util/LunarUtil.py ZHI_HIDE_GAN; https://github.com/6tail/lunar-python',
        'limits': 'ဤဇယားမှာ အလေးချိန် သတ်မှတ်ခြင်း၊ ရာသီအင်အားအချိုးတွက်ခြင်း၊ Day Master Strength သတ်မှတ်ခြင်း မပါသေးပါ။'
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
    'TAROT-INTERPRETATION-001': {
        'heading': 'Tarot ၇၈ ချပ် သင်္ကေတအနက်',
        'method': 'Major Arcana ၂၂ ချပ်အတွက် သီးခြားမြန်မာလို စဉ်းစားစရာစာသားများ၊ Minor Arcana ၅၆ ချပ်အတွက် Suit နဲ့ Rank သင်္ကေတများပေါင်းစပ်ပြီး မူရင်းရေးသားထားသော Reflection စာသားကို ရွေးထုတ်သည်။',
        'source': 'Traditional 78-card tarot deck structure; original Burmese writing in tarot_meanings.py, not copied from a proprietary tarot guide.',
        'limits': 'လတ်တလော 78-card reflective guide ဖြစ်ပြီး Upright/Reversed အမျိုးအစားခွဲခြားမှု မပါသေးပါ။ အနာဂတ်သေချာပေါက်ဖြစ်မည်ဟု မဆိုလိုပါ။'
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
        [InlineKeyboardButton(text='Calculation Method', callback_data=f'evidence:{rule_id}')]
    ])

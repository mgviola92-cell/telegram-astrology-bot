"""Public method summaries for stateless, privacy-preserving evidence buttons.

A method's rationale is not scientific proof that divination predicts the future.
Every listed ID must correspond to a real calculation or explicitly random draw.
"""
RULES = {
    'WEST-TROPICAL-LONGITUDES-001': {
        'heading': 'Western Tropical Astronomy — ဂြိုဟ်တည်နေရာ',
        'method': 'Skyfield နှင့် စက်အတွင်း အသင့်ရှိပြီးသော JPL .bsp Ephemeris ကို သုံး၍ မွေးချိန်၏ UTC Instant မှ ကမ္ဘာဗဟို Apparent Ecliptic Longitude တွက်ပြီး Tropical Zodiac ၃၀ ဒီဂရီအပိုင်းအလိုက် ခွဲခြားသည်။ Outer Planet Barycenters ကို Planet Centers ဟု မမှားဖော်ပြပါ။',
        'source': 'Skyfield Coordinates: https://rhodesmill.org/skyfield/coordinates.html ; JPL DE Ephemerides, https://ssd.jpl.nasa.gov/planets/eph_export.html',
        'limits': 'JPL Kernel ကို Bot မှ အလိုအလျောက် မဒေါင်းလုဒ်လုပ်ပါ။ Kernel ရှိမှသာ Preview အဖြစ် တွက်နိုင်ပြီး Planet Positions အတွက် Independent Cross-Ephemeris Benchmarks မပြီးသေးပါ။'
    },
    'WEST-ASC-WHOLE-SIGN-001': {
        'heading': 'Western Ascendant — Mean Sidereal & Whole Sign',
        'method': 'UTC Julian Day ကို Meeus Greenwich Mean Sidereal formula နှင့် Mean Obliquity သုံးပြီး Local Sidereal Time မှ အရှေ့မိုးကုတ် Ecliptic Ascendant ဆုံချက်တွက်သည်။ ရာသီ ၃၀ ဒီဂရီအပြည့် တစ်ခုကို Whole Sign House တစ်အိမ်အဖြစ် ရေတွက်သည်။',
        'source': 'USNO Sidereal Time https://aa.usno.navy.mil/faq/GAST ; NASA/JPL GMST (ESAA) https://spsweb.fltops.jpl.nasa.gov/portaldataops/mpg/MPG_Docs/MPG%20Book/Release/Chapter2-TimeScales.pdf ; Meeus Astronomical Algorithms',
        'limits': 'Mean Sidereal/Mean Obliquity သုံးထားသော Conventional Approximation ဖြစ်ပြီး UT1-UTC၊ Nutation၊ Polar Latitudes နှင့် Other House Systems ကို မစစ်ရသေးပါ။ Independent Commercial Natal Benchmark မပြီးသေးသဖြင့် Development Preview သာဖြစ်သည်။'
    },
    'WEST-HEL-ANNUAL-PROFECTION-001': {
        'heading': 'Western Annual Profection — ရိုးရာနှစ်တိုင်',
        'method': 'အတည်ပြုထားသည့် Natal Ascendant Sign အပေါ် အခြေခံပြီး မွေးနေ့ကျော်ပြီးသော အသက် n အတွက် (n mod 12)+1 အိမ်ကို ရွေးသည်။ Rising Sign မှ နက္ခတ်ရာသီ n ခု ရှေ့တိုး၍ ထိုရာသီ၏ ရိုးရာဂြိုဟ်အုပ်စိုးသူကို Lord of the Year အဖြစ် သတ်မှတ်သည်။',
        'source': 'Chris Brennan, Hellenistic Astrology (2017), annual profections; https://www.astro.com/astrology/tma_article190314_e.htm ; Vettius Valens, Anthology',
        'limits': 'ဤ Bot ၏ /profection Command သည် Ascendant ကို မတွက်ပါ။ အသုံးပြုသူက သီးခြားတွက်ထားသော Rising Sign ကို ကိုယ်တိုင်ပေးရမည်။ ရိုးရာနှစ်တိုင်အမျိုးအစားခွဲခြားမှုသာဖြစ်ပြီး အနာဂတ်ကို အာမခံမဟုတ်ပါ။'
    },
    'WEST-ASPECTS-GEOMETRY-001': {
        'heading': 'အနောက်တိုင်းဇာတာ ဂြိုဟ်ထောင့်ဆက်သွယ်မှု',
        'method': 'Tropical Ecliptic Longitude နှစ်ခုအကြား အတိုဆုံးထောင့်ကိုတွက်ပြီး 0°, 60°, 90°, 120°, 180° နှင့် သတ်မှတ်ထားသော Orb များဖြင့် စစ်ဆေးသည်။',
        'source': 'Astrodienst Aspects: https://www.astro.com/astrology/in_aspect_e.htm ; orb sizes depend on a documented convention',
        'limits': 'အခြား Ephemeris မှ သီးခြားအတည်ပြုထားသော ဂြိုဟ်တည်နေရာကိုသာ ထည့်သွင်းရမည်။ ဤ Engine က မွေးဇာတာနှင့် ဂြိုဟ်တည်နေရာကို ကိုယ်တိုင်မတွက်သေးပါ။'
    },
    'MM-DAILY-CALENDAR-REFLECTION-001': {
        'heading': 'နေ့စဉ် မြန်မာရိုးရာပြက္ခဒိန် အညွှန်း',
        'method': 'အထူးသတ်မှတ်ထားသည့် မြန်မာစံတော်ချိန်ဒေသ၏ Gregorian Local Date မှ mmcal ကိုတွက်ပြီး Yan Naing Aye ၏ ပြက္ခဒိန်အမှတ်အသားများကို ပြန်စစ်၍ ဥပုသ်၊ အဖိတ်၊ ရက်ရာဇာနှင့် ပြဿဒါးအမည်များကို ရက်စွဲအခြေခံ ဖော်ပြသည်။ Personal Profile၊ Random Draw သို့မဟုတ် နက္ခတ္တအနာဂတ်ခန့်မှန်းမှုကို မသုံးပါ။',
        'source': 'Yan Naing Aye, Myanmar Astrological Calendar Days (2013), https://cool-emerald.blogspot.com/2013/12/myanmar-astrological-calendar-days.html ; original Burmese https://coolemerald.blogspot.com/2013/12/blog-post.html ; mmcal https://yan9a.github.io/mmcal/',
        'limits': 'ရိုးရာပြက္ခဒိန်၏ နေ့အမျိုးအစားသာဖြစ်ပြီး အသုံးပြုသူတစ်ဦးချင်း ကံကြမ္မာ၊ ကျန်းမာရေး၊ ချစ်ရေး၊ ငွေကြေး သို့မဟုတ် အနာဂတ်ဖြစ်ရပ်ကို မခန့်မှန်းပါ။ ကျောင်းအလိုက် မူကွဲများရှိနိုင်သည်။'
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
        'source': 'Hans Decoz, Life Path Number method, https://www.worldnumerology.com/numerology-life-path/ ; Numerology.com, Life Path Number meanings, https://www.numerology.com/articles/your-numerology-chart/life-path-number-meanings/ (school-dependent)',
        'limits': 'နာမည်/မွေးနေ့ကိန်းဂဏန်း၏ ရိုးရာအနက်ဖွင့်ဆိုချက်သာ ဖြစ်ပြီး ဖြစ်ရပ်တစ်ခုကို အာမခံမဟုတ်ပါ။'
    },
    'NUM-LIFE-PATH-THEMES-001': {
        'heading': 'Life Path ရိုးရာကိန်းအနက် (Modern Numerology)',
        'method': '၁–၉ နှင့် Master Numbers ၁၁၊ ၂၂၊ ၃၃ ၏ ဆက်စပ်သင်္ကေတခေါင်းစဉ်များကို မျက်မှောက်ခေတ် Numerology.com ကျောင်း၏ ဖော်ပြချက်အပေါ် အခြေခံ၍ မူရင်းမြန်မာစကားဖြင့် အကျဉ်းချုပ်ထားသည်။ ကိန်းတွက်ချက်မှုနှင့် သီးခြားဖြစ်သည်။',
        'source': 'Numerology.com, What Is Numerology? https://www.numerology.com/articles/about-numerology/what-is-numerology/ ; Hans Decoz, Life Path: https://www.worldnumerology.com/numerology-life-path/',
        'limits': 'Numerology ကျောင်းများအလိုက် သင်္ကေတကွာနိုင်သည်။ ဤအဓိပ္ပာယ်သည် လူ့စိတ်အခြေအနေ၊ အထူးစွမ်းအား၊ အလုပ်အကိုင်၊ ကျန်းမာရေး သို့မဟုတ် အနာဂတ်အောင်မြင်မှုကို သိပ္ပံနည်းကျ အတည်မပြုနိုင်ပါ။'
    },
    'CHN-BAZI-VISIBLE-WUXING-001': {
        'heading': 'BaZi မြင်ရသော ဓာတ်ငါးပါး',
        'method': 'လေးတိုင်၏ Heavenly Stems ၄ လုံးနှင့် Earthly Branches ၄ လုံးကို ရိုးရာ အဓိကဓာတ်အလိုက်ရေတွက်သည်။',
        'source': 'Traditional Five Phases correspondences: https://www.ibiblio.org/chinesehistory/contents/08fea/c06s02.htm ; https://uaya.org/iching/correspondences/',
        'limits': 'Hidden Stems, Seasonal Strength နှင့် Day Master အားကောင်းမှု မတွက်ရသေးပါ။ အရေအတွက်တစ်ခုတည်းဖြင့် အနာဂတ်ဖြစ်ရပ် မဆုံးဖြတ်နိုင်ပါ။'
    },
    'CHN-BAZI-TENGODS-SYMBOLIC-001': {
        'heading': 'BaZi Ten Gods — ဓာတ်အုပ်စုငါးမျိုးနှင့် ရိုးရာသင်္ကေတအနက်',
        'method': 'တွက်ပြီးသား တိုင်လေးတိုင်ကို မူလမွေးချိန်နှင့် Source Evidence ဖြင့် ပြန်တွက်စစ်သည်။ Day Master နဲ့ တခြားမြင်ရသော နှစ်/လ/နာရီ Heavenly Stem သုံးခု၏ ဓာတ်အမျိုးအစား၊ ထုတ်ပေး/ထိန်းချုပ်ဆက်နွယ်မှုနှင့် Yin/Yang တူ/ကွာချက်မှ Ten Gods အမည်များကို သတ်မှတ်သည်။ အဖော်၊ ဖော်ထုတ်၊ အရင်းအမြစ်၊ ထိန်းညှိနှင့် ပံ့ပိုးမှု အုပ်စုငါးမျိုးအဖြစ် မြန်မာလို သင်္ကေတအကျဉ်းချုပ်ဖော်ပြသည်။',
        'source': '6tail/lunar-python LunarUtil.SHI_SHEN (calculation): https://github.com/6tail/lunar-python ; Traditional roles: https://yuanzizhiyi.com/en/wiki/bazi/ten-gods ; https://bazimethod.com/learn/ten-gods/',
        'limits': 'ဤအုပ်စုအမည်များက တိုက်ရိုက်ငွေဝင်မည်၊ အရာရှိဖြစ်မည်၊ အန္တရာယ်ကျမည် စသည့် အနာဂတ်ရလဒ်များကို မဆိုလိုပါ။ 7 Killings နှင့် Rob Wealth သည် စာရင်းဇယားအမည်များဖြစ်ပြီး ထိခိုက်မှုအာမခံချက် မဟုတ်ပါ။ Hidden Stems အလေးချိန်၊ ရာသီအင်အား၊ ဓာတ်အားကောင်းမှုနှင့် Favorable Elements မသတ်မှတ်ရသေးပါ။ ကျောင်းအလိုက် အနက်ကွာနိုင်သည်။'
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
    'CHN-BAZI-SEASON-MONTH-001': {
        'heading': 'BaZi ရာသီလနှင့် 三会 အုပ်စုများ',
        'method': 'lunar-python ၏ Jie Solar-Term ဖြင့်တွက်ထားသော လတိုင်အောက်ကိုင်းကို နွေဦး 寅卯辰၊ နွေ 巳午未၊ ဆောင်းဦး 申酉戌၊ ဆောင်း 亥子丑 အုပ်စုလေးမျိုးနှင့် တိုက်စစ်သည်။ တိုင်လေးတိုင်တွင် အုပ်စုတစ်ခု၏ သီးခြား Branch သုံးမျိုးလုံး ပါဝင်မှ Full Membership ဟု သတ်မှတ်သည်။',
        'source': '6tail/lunar-python Lunar.py Jie exact Month; American Feng Shui Institute Stems & Branches, p.42, https://www.amfengshui.com/wp-content/uploads/2014/09/as101.pdf ; Four seasonal meeting rules and formation caveats: https://clarifyhk.com/learn/bazi/stem-branch-relations/directional-meeting-conditions',
        'limits': 'အုပ်စုအစိတ်အပိုင်းပြည့်ခြင်းသာဖြစ်ပြီး Combination Transformation၊ Day Master Strength၊ Favorable Elements သို့မဟုတ် ကံကြမ္မာဟောကိန်းကို မဆုံးဖြတ်ပါ။'
    },
    'CHN-BAZI-DAYUN-001': {
        'heading': 'BaZi 大运 — ရိုးရာ ၁၀ နှစ်စက်ဝန်း',
        'method': 'မွေးရပ်ဒေသ၏ အတည်ပြုထားသော civil time ကို lunar-python EightChar.getYun(0/1,sect) နှင့် DaYun.getDaYun() ထဲ ဖြတ်တွက်သည်။ နှစ်တိုင်ကောင်းကင်ပင်စည်၏ ယင်/ယန်နဲ့ အသုံးပြုသူရွေးထားသည့် စနစ်ရိုးရာ 0/1 ကုတ်ပေါ်မူတည်၍ အစဉ်ရှေ့/နောက် သတ်မှတ်သည်။ Solar-Term Jie နီးစပ်မှုမှ စတင်ချိန်နှင့် ၁၀ နှစ်စက်ဝန်းတိုင်များတွက်သည်။',
        'source': '6tail/lunar-python lunar_python/eightchar/Yun.py and DaYun.py; https://github.com/6tail/lunar-python/blob/master/lunar_python/eightchar/Yun.py ; https://github.com/6tail/lunar-python/blob/master/lunar_python/eightchar/DaYun.py',
        'limits': 'Upstream ရိုးရာစနစ်က 0/1 binary method code ကို သီးခြားရွေးရန် လိုသည်၊ Telegram profile သို့မဟုတ် gender identity မှ ခန့်မှန်းမည်မဟုတ်ပါ။ အသက်သည် East Asian nominal age ဖြစ်သည်။ True Solar Time ပြင်ဆင်မှုနှင့် ကံကြမ္မာအာမခံဟောချက် မပါပါ။'
    },
    'CHN-BAZI-CHANGSHENG-001': {
        'heading': 'BaZi 十二长生 — ရိုးရာအဆင့် ၁၂ မျိုး',
        'method': 'အတည်ပြုပြီးသော Four Pillars နှင့် Day Master, Sect ကို တူညီသည့်မွေးချိန်မှ ပြန်တွက်စစ်ပြီး lunar-python EightChar ၏ getYearDiShi, getMonthDiShi, getDayDiShi, getTimeDiShi နည်းလမ်းများဖြင့် အဆင့် ၁၂ မျိုးထဲက အိမ်တိုင်ဆိုင်ရာအမျိုးအစားကို ထုတ်သည်။',
        'source': '6tail/lunar-python lunar_python/EightChar.py, CHANG_SHENG stages and growth-stage getters; https://github.com/6tail/lunar-python/blob/master/lunar_python/EightChar.py',
        'limits': 'ရိုးရာကဏ္ဍအမည်များသာဖြစ်ပြီး အသက်အရွယ်၊ ကျန်းမာရေး၊ အသက်ရှည်မှု၊ ဖြစ်ရပ်ကံကြမ္မာကို ခန့်မှန်းသော အထောက်အထားမဟုတ်ပါ။ Day Master ရာသီအင်အား သို့မဟုတ် Useful God ကို မတွက်ထားပါ။'
    },
    'CHN-BAZI-PILLARS-001': {
        'heading': 'တရုတ်ဇာတာလေးတိုင်',
        'method': 'မွေးရပ်ဒေသ ဒေသစံတော်ချိန်ကို lunar-python ၏ Solar -> Lunar -> EightChar စနစ်ထဲ ဖြတ်သန်းတွက်ချက်သည်။',
        'source': '6tail/lunar-python: lunar_python/EightChar.py and test/EightCharTest.py',
        'limits': 'မွေးရပ်ဒေသ၊ သမိုင်းဝင် timezone နှင့် True Solar Time ဆိုင်ရာ အတည်ပြုချက် မပြည့်စုံသေးသော စမ်းသပ်တွက်ချက်မှုဖြစ်သည်။'
    },
    'MM-8DAY-ANIMAL-DIRECTION-001': {
        'heading': 'မြန်မာ ၈ နေ့နံ၏ ရိုးရာသတ္တဝါနှင့် အရပ်မျက်နှာ',
        'method': 'မွေးရပ်ဒေသအချိန်၏ Gregorian နေ့နံကို သတ်မှတ်၍ တနင်္ဂနွေ၊ တနင်္လာ၊ အင်္ဂါ၊ ဗုဒ္ဓဟူးမနက်၊ ရာဟုမွန်းလွဲ၊ ကြာသပတေး၊ သောကြာ၊ စနေ ၈ မျိုးကို ခွဲသည်။ ဤ Bot တွင် ဗုဒ္ဓဟူး 12:00 နာရီမှ Rahu အဖြစ်ခွဲပြီး လူသိများသော သတ္တဝါ/အရပ်မျက်နှာ ရိုးရာဇယားနှင့် တိုက်စစ်သည်။',
        'source': 'Myanmar cultural awareness, NYU Steinhardt: https://docs.steinhardt.nyu.edu/pdfs/metrocenter/xr1/Language_n_Cultural_Awareness/MYANMAR.pdf ; Myanmar Calendar: https://www.calendarmyanmar.com/zodiac-signs.html ; Maung Htin Aung, historical Burmese astrology: https://www.uclmyanmar.org/wp-content/uploads/2016/02/372001.pdf',
        'limits': 'သတ္တဝါနှင့် အရပ်မျက်နှာတို့သည် ယဉ်ကျေးမှုဆိုင်ရာ သင်္ကေတအမည်များသာ ဖြစ်ပြီး လူ၏တန်ဖိုးနှင့် အနာဂတ်ဖြစ်ရပ်ကို မဟောနိုင်ပါ။ ရာဟုကို ဘယ်နာရီမှစခွဲမည်ဆိုသော မူကွဲရှိသည် (သမိုင်းဝင်စာပေအချို့တွင် ညနေ 6 နာရီ)။ 7-house Mahabote arithmetic နှင့် မရောထွေးပါ။'
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

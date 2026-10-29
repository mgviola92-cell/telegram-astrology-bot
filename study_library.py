"""Native Telegram source-aware astrology study chapters.

No database, login state, timer, external API, image or download. Lessons
describe documented calculation distinctions and cultural limitations, not
individual predictions. Each chapter links to the existing evidence registry.
"""
from html import escape
from evidence_ui import get_rule

CHAPTERS = {
    "calendar": {
        "title": "မြန်မာပြက္ခဒိန်နှင့် အခါရက်များ",
        "intro": "မြန်မာပြက္ခဒိန်မှာ ဂရိဂေါရီးယန်းရက်စွဲတစ်ခုကို မြန်မာနှစ်၊ လ၊ လဆန်း/လဆုတ်နှင့် ရိုးရာရက်အမျိုးအစားများအဖြစ် သီးခြားတွက်ကြည့်နိုင်သည်။",
        "method": "ဤ Bot ၏ ပြက္ခဒိန်သည် Yan Naing Aye ၏ mmcal နည်းလမ်းကို အသုံးပြုထားသည်။ ရက်ရာဇာနှင့် ပြဿဒါးတို့သည် ရက်အမျိုးအစားအမည်များဖြစ်ပြီး ကိုယ်ပိုင်မွေးဇာတာမဟုတ်ပါ။",
        "limits": "အခါရက်တစ်ရက် ရှိခြင်းကို အောင်မြင်မှု သို့မဟုတ် ဆုံးရှုံးမှု သေချာမည်ဟု မဖတ်သင့်ပါ။ သမိုင်းဝင် ပြက္ခဒိန်မူကွဲများရှိနိုင်သည်။",
        "rules": ("MM-CALENDAR-MMCAL-001", "MM-CALENDAR-DAY-SIGNALS-001"),
    },
    "mahabote": {
        "title": "မဟာဘုတ် အိမ်ခုနစ်လုံး",
        "intro": "မဟာဘုတ်၏ အခြေခံတွက်ချက်မှုမှာ မြန်မာနှစ်နှင့် မွေးနေ့နံဆိုင်ရာ ကိန်းစည်းမျဉ်းဖြစ်သည်။ အိမ်ခုနစ်လုံးကို ရိုးရာအနက်ဖွင့်မှုနဲ့ ခွဲခြားစဉ်းစားရသည်။",
        "method": "ဗုဒ္ဓဟူးနေ့ မွန်းလွဲရာဟုကို မွေးနေ့နံသီးခြား ဖော်ပြနိုင်သော်လည်း မဟာဘုတ်အိမ်ရှစ်လုံးဟု မတွက်ပါ။ အိမ်အနက်သည် သင်္ကေတဖတ်ရှုမှုဖြစ်ပြီး ကိန်းတွက်ရလဒ်နဲ့ အမျိုးအစားမတူပါ။",
        "limits": "မရဏကဲ့သို့သော ရိုးရာအမည်များကို လူတစ်ဦး၏ အသက်၊ ကံကြမ္မာ သို့မဟုတ် ကျန်းမာရေးဖြစ်ရပ်ကို ဆုံးဖြတ်မည့် ခန့်မှန်းချက်ဟု မယူပါ။",
        "rules": ("MM-MAHABOTE-SEVEN-HOUSE-001", "MM-MAHABOTE-SYMBOLIC-THEMES-001", "MM-8DAY-ANIMAL-DIRECTION-001"),
    },
    "bazi": {
        "title": "BaZi ရိုးရာတိုင်လေးတိုင်",
        "intro": "BaZi သည် မွေးနှစ်၊ လ၊ ရက်နှင့် နာရီတိုင်ကို Heavenly Stem နှင့် Earthly Branch အစုံများဖြင့် ရှင်းပြသည့် တရုတ်ရိုးရာစနစ်ဖြစ်သည်။",
        "method": "လတိုင်တွက်ရာတွင် အနောက်တိုင်းလတစ်လ၏ ပထမရက်ကိုသာ မယူဘဲ Solar Terms နယ်နိမိတ်များကို ထည့်တွက်သည်။ တကယ့်မွေးရပ် Timezone နှင့် နာရီမှန်ဖို့ အရေးကြီးသည်။ Ten Gods ဆိုသည်မှာ Day Master နှင့် တခြားတိုင်များ၏ ဓာတ်/ယင်ယန်ဆက်နွယ်မှုအမည်များဖြစ်သည်။ ဓာတ်တူ/ဖော်ထုတ်/အရင်းအမြစ်/ထိန်းညှိ/ပံ့ပိုး အုပ်စုငါးမျိုးနှင့် ရိုးရာဆက်စပ်မှုရှိသည်။ Five Phases အရေအတွက်တစ်ခုတည်းက Day Master အားကို မဆုံးဖြတ်ပါ။",
        "limits": "ဒီ Bot ၏ BaZi တွင် True Solar Time နှင့် ကျောင်းအလိုက် interpretive အချက်အချို့ မပြီးသေးပါ။ တိုင်အမည်များသည် လူတစ်ဦး၏အနာဂတ်ကို သိပ္ပံနည်းကျ အတည်မပြုနိုင်ပါ။",
        "rules": ("CHN-BAZI-PILLARS-001", "CHN-BAZI-VISIBLE-WUXING-001", "CHN-BAZI-TENGODS-SYMBOLIC-001"),
    },
    "western": {
        "title": "Western Profection အခြေခံ",
        "intro": "Hellenistic Annual Profection သည် အသက်နှစ်ပြည့်တိုင်း အိမ်တစ်လုံးရွှေ့သည့် ရိုးရာနှစ်စက်ဝန်း နည်းလမ်းဖြစ်သည်။",
        "method": "တွက်ချက်ရန် မွေးနေ့၊ စစ်ဆေးမည့်နေ့နှင့် အခြားနေရာမှ သီးခြားစစ်ဆေးထားသော Rising Sign လိုသည်။ မွေးနေ့မရောက်သေးပါက အသက်နှစ်ပြည့် မတိုးသေးသဖြင့် Activated House ပြောင်းနိုင်သည်။ အိမ် ၁၂ လုံး၏ ရိုးရာခေါင်းစဉ်များနှင့် Lord of the Year ကို သီးခြားအနက်ဖော်ပြသည်။ /profection houses နဲ့ မွေးအချက်အလက်မလိုဘဲ လေ့လာနိုင်သည်။",
        "limits": "ဒီ Command သည် Rising Sign ကို ကိုယ်တိုင်မတွက်ပါ။ Western Natal Preview ကို ပိုမိုစစ်ဆေးနေပြီး ပုံမှန် User များအတွက် ဖွင့်မထားပါ။ ရိုးရာအိမ်ခေါင်းစဉ်များသည် ဖြစ်ရပ်အာမခံချက် မဟုတ်ပါ။",
        "rules": ("WEST-HEL-ANNUAL-PROFECTION-001", "WEST-HEL-PROFECTION-HOUSE-TOPICS-001"),
    },
    "numerology": {
        "title": "Life Path ကိန်းနှင့် အနက်",
        "intro": "မျက်မှောက်ခေတ် Pythagorean-style Numerology ကျောင်းတွင် မွေးလ၊ မွေးရက်နှင့် မွေးနှစ်ကိန်းများကို သီးခြားလျှော့ပြီး ထပ်ပေါင်းလျှော့သည့် Life Path နည်းလမ်းတစ်မျိုးရှိသည်။",
        "method": "ဒီ Bot က Master Numbers ၁၁၊ ၂၂၊ ၃၃ ကို မလျှော့ဘဲ ထိန်းထားသည့် သတ်မှတ်ချက်ကို အတိအကျ အသုံးပြုထားသည်။ နံပါတ်တွက်ချက်မှုနှင့် ရိုးရာသင်္ကေတအနက်ကို သီးခြား မှတ်တမ်းတင်ထားသည်။",
        "limits": "ကိန်းစည်းမျဉ်းနှင့် အနက်ဖွင့်မှု ကျောင်းအလိုက် ကွာနိုင်သည်။ ကိန်းတစ်ခုက လူ၏တန်ဖိုး၊ အရည်အချင်း သို့မဟုတ် အနာဂတ်ကို မဆုံးဖြတ်ပါ။",
        "rules": ("NUM-PYT-LIFE-PATH-001", "NUM-LIFE-PATH-THEMES-001"),
    },
    "tarot": {
        "title": "Tarot ကတ် ၇၈ ချပ်",
        "intro": "ရိုးရာ ၇၈ ကတ် Tarot တွင် Major Arcana ၂၂ ချပ်နှင့် Minor Arcana ၅၆ ချပ် ပါဝင်သည်။ ကတ်ဆွဲခြင်းသည် တကယ့်ကျပန်းရွေးချယ်မှုဖြစ်သည်။",
        "method": "ကတ်ရွေးပြီးနောက် ကတ်အမည်နှင့် ဆက်စပ်သင်္ကေတအနက်ကို ဖော်ပြသည်။ ကတ်ရွေးခြင်းကို ဂြိုဟ်တည်နေရာ တွက်ချက်မှုကဲ့သို့ မဖော်ပြပါ။ ပုံဖိုင်ရရှိမှ Telegram file_id ကို ပြန်သုံးပြီး မရှိပါက စာသားဖြင့်သာ ဖော်ပြသည်။",
        "limits": "Tarot ဖတ်ရှုမှုကို စဉ်းစားဆင်ခြင်ရန် ယဉ်ကျေးမှုနည်းလမ်းတစ်ခုအဖြစ် ယူနိုင်သည်။ ကတ်တစ်ချပ်က လူ၏ကိုယ်ရေးဆုံးဖြတ်ချက် သို့မဟုတ် နောက်လာမည့်ဖြစ်ရပ်ကို အာမခံမပေးပါ။",
        "rules": ("TAROT-DRAW-001", "TAROT-INTERPRETATION-001"),
    },
}
def chapter(key: str) -> dict:
    if key not in CHAPTERS:
        raise ValueError("Unknown study chapter")
    data=CHAPTERS[key]
    # Check references at retrieval to avoid dangling source buttons.
    for rule in data["rules"]:
        get_rule(rule)
    return data

def study_index_text() -> str:
    return ("<b>ကြယ်စင် ကျမ်းလေ့လာခန်း</b>\n"
            "━━━━━━━━━━━━━━\n"
            "တွက်ချက်နည်း၊ ရိုးရာကျောင်းနှင့် ကန့်သတ်ချက်တွေကို "
            "ဘာသာရပ်တစ်ခုချင်း လေ့လာနိုင်ပါပြီ။\n\n"
            "စိတ်ဝင်စားရာ ခေါင်းစဉ်ကို ရွေးပါ။ "
            "ဤလေ့လာခန်းသည် မွေးအချက်အလက် မမေး၊ မသိမ်းပါ။")

def study_chapter_text(key: str) -> str:
    data=chapter(key)
    rendered=(
        "<b>"+escape(data["title"])+"</b>\n━━━━━━━━━━━━━━\n\n"
        +escape(data["intro"])+"\n\n"
        "<b>နည်းလမ်းသိရန်</b>\n"+escape(data["method"])+"\n\n"
        "<b>သတိထားရန်</b>\n"+escape(data["limits"])+"\n\n"
        "<i>အောက်ပါကျမ်းကိုးခလုတ်များမှ နည်းလမ်းနှင့် မူရင်း Source ကို ကြည့်နိုင်သည်။</i>"
    )
    if len(rendered)>4096:
        raise ValueError("Telegram study lesson too long")
    return rendered

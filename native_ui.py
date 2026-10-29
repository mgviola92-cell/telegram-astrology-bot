"""Native Telegram navigation: clean labels, minimal emoji, no Mini App.

Myanmar astrology keeps its Burmese inline label; international disciplines
use established English names. Telegram controls layout and button rendering.
Navigation is stateless and callback data never includes private birth data.
"""
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from study_library import CHAPTERS, chapter

def button(label: str, callback: str) -> InlineKeyboardButton:
    if len(callback.encode("utf-8")) > 64:
        raise ValueError("Telegram callback data exceeds 64 bytes")
    return InlineKeyboardButton(text=label, callback_data=callback)

# Only exposed commands are interactive. Unfinished engines show an honest
# development notice instead of publishing unvalidated birth-chart results.
SECTIONS = {
    "charts": ("ဇာတာတွက်ချက်မှု", (
        ("မြန်မာဗေဒင်", "mm"),
        ("Western Astrology", "western"),
        ("BaZi", "bazi"),
        ("Numerology", "number"),
        ("Tarot", "tarot"),
    )),
    "personal": ("ကိုယ်ပိုင်ဇာတာ", (
        ("My Profile", "profile"),
        ("Personal Reading", "reading"),
        ("Compatibility", "compatibility"),
        ("Daily Reading", "daily"),
        ("Timing Cycles", "timing"),
    )),
    "more": ("အခြားဇာတာခန်းများ", (
        ("မြန်မာပြက္ခဒိန်", "mmcal"),
        ("Reference Library", "library"),
        ("Astrology Study", "study"),
        ("Group Settings", "group"),
    )),
}
FEATURES = {
    "mm": ("မြန်မာဗေဒင်", "မွေးနေ့နံနှင့် မဟာဘုတ်/ပြက္ခဒိန်တွက်ချက်မှုများ", (
        ("မွေးနေ့နံ", "myday"), ("မဟာဘုတ်ဇာတာ", "mahabote"), ("မြန်မာပြက္ခဒိန်", "mmcal"))),
    "western": ("Western Astrology", "Natal Chart ကို Reference နဲ့ စစ်ဆေးနေဆဲဖြစ်ပါတယ်။ သီးခြားတွက်ထားတဲ့ Rising Sign ရှိရင် ရိုးရာ Annual Profection ကို တွက်နိုင်ပါတယ်။", (("Annual Profection", "profection"),)),
    "bazi": ("BaZi", "Four Pillars ကို တွက်နိုင်ပါတယ်။ True Solar Time နဲ့ seasonal validation မပြီးသေးပါ။", (
        ("Four Pillars", "bazi"), ("Da Yun Cycles", "dayun"),)),
    "number": ("Numerology", "Life Path ကိန်းနှင့် မျက်မှောက်ခေတ် ရိုးရာသင်္ကေတအနက်ကို သီးခြားကိုးကား၍ ဖတ်နိုင်ပါတယ်။", (
        ("Life Path", "number"),)),
    "tarot": ("Tarot", "78-card Tarot ဆွဲနိုင်ပါတယ်။ ကတ်ပုံအစုံနဲ့ Animation မပြီးသေးပါ။", (
        ("Draw a Card", "tarot"),)),
    "profile": ("My Profile", "မွေးနေ့ကို သဘောတူမှသာ သိမ်းနိုင်ပြီး Private Chat မှာသာ ကြည့်နိုင်ပါတယ်။", (
        ("Save Birth Date", "savebirth"), ("View Birth Date", "mybirth"),
        ("Delete Birth Date", "forgetbirth"))),
    "reading": ("Personal Reading", "မဟာဘုတ်ရိုးရာအိမ်အနက်နှင့် Numerology Life Path ကို သီးခြားနည်းလမ်းအဖြစ် ဖတ်နိုင်ပါတယ်။", (("အဆင့်ဆင့် ဖြည့်မယ်", "reading_start"), ("Command နဲ့တွက်မယ်", "reading"),)),
    "compatibility": ("Compatibility", "နှစ်ဦးဇာတာ တွက်ချက်မှုနှင့် ရိုးရာနည်းလမ်းစစ်ဆေးခြင်း မပြီးသေးပါ။", ()),
    "daily": ("Daily Reading", "မြန်မာပြက္ခဒိန်အခြေခံ နေ့စဉ်ရိုးရာအမှတ်အသားများကို ဖတ်နိုင်ပါတယ်။ ကိုယ်ပိုင်အနာဂတ်ဟောစာတမ်းမဟုတ်ပါ။", (("နေ့စဉ်ပြက္ခဒိန်", "daily"),)),
    "timing": ("Timing Cycles", "Timing backend အချို့ရှိပေမဲ့ လုံလောက်စွာ မစမ်းသပ်ရသေးပါ။", ()),
    "mmcal": ("မြန်မာပြက္ခဒိန်", "မြန်မာရက်စွဲ၊ လဆန်းလဆုတ်၊ ရက်ရာဇာနှင့် ပြဿဒါးတို့ကို တွက်နိုင်ပါတယ်။", (
        ("ရက်စွဲတွက်မယ်", "mmcal"), ("အခါပေးရက်များ", "days"),)),
    "library": ("Reference Library", "တွက်ချက်နည်း၊ မူရင်းကိုးကားချက်နှင့် ကန့်သတ်ချက်များကို ဘာသာရပ်အလိုက် ဖတ်ရှုနိုင်ပါတယ်။", (("ကျမ်းကိုးမှတ်တမ်းများ", "library"),)),
    "study": ("Astrology Study", "တွက်ချက်နည်းနှင့် ရိုးရာကျမ်းကိုးချက်များကို အခန်းအလိုက် ဖတ်ရှုနိုင်ပါတယ်။", (("ကျမ်းလေ့လာခန်း", "study"),)),
    "group": ("Group Settings", "Group Management UI မပြီးသေးပါ။ ကိုယ်ရေးအချက်အလက်ကို Private Chat မှာသာ ဖြည့်ပါ။", ()),

}
COMMAND_GUIDES = {
    "myday": "/myday 2005-12-23 08:37",
    "mahabote": "/mahabote 1990-05-14",
    "mmcal": "/mmcal 2024-01-01",
    "days": "/days 2024-01-01",
    "daily": "/daily",
    "reading": "/reading",
    "bazi": "/bazi 2005-12-23 08:37 Asia/Yangon",
    "dayun": "/dayun 2005-12-23 08:37 Asia/Yangon 1",
    "profection": "/profection 2005-12-23 2026-10-27 Aries",
    "number": "/number 1999-12-31",
    "savebirth": "/savebirth 2005-12-23 အတည်ပြု",
    "mybirth": "/mybirth",
    "forgetbirth": "/forgetbirth",
}

def keyboard(rows):
    return InlineKeyboardMarkup(inline_keyboard=rows)

def home_keyboard():
    return keyboard([
        [button("Astrology", "ui:category:charts"),
         button("My Profile", "ui:feature:profile")],
        [button("Tarot", "ui:feature:tarot"),
         button("Daily Reading", "ui:feature:daily")],
        [button("More", "ui:category:more"),
         button("Personal", "ui:category:personal")],
    ])

def section_keyboard(section: str):
    if section not in SECTIONS:
        raise KeyError(section)
    entries=SECTIONS[section][1]
    rows=[[button(label,"ui:feature:"+name) for label,name in entries[i:i+2]]
          for i in range(0,len(entries),2)]
    rows.append([button("Back","ui:home")])
    return keyboard(rows)

def feature_keyboard(feature: str):
    if feature not in FEATURES:
        raise KeyError(feature)
    rows=[[button(label,("ui:tarot" if cmd=="tarot" else "ui:library" if cmd=="library" else "ui:reading:start" if cmd=="reading_start" else "ui:study" if cmd=="study" else "ui:guide:"+cmd))]
          for label,cmd in FEATURES[feature][2]]
    group=next((key for key,(_,items) in SECTIONS.items()
                if any(name==feature for _,name in items)), "charts")
    rows.append([button("Back","ui:category:"+group),
                 button("Home","ui:home")])
    return keyboard(rows)

def guide_keyboard(feature: str):
    if feature not in COMMAND_GUIDES:
        raise KeyError(feature)
    parent=next((name for name,(_,_,actions) in FEATURES.items()
                 if any(cmd==feature for _,cmd in actions)), "charts")
    return keyboard([[button("Back","ui:feature:"+parent),
                      button("Home","ui:home")]])

def home_text():
    return ("<b>ကြယ်စင်တို့၏ ဇာတာခန်း</b>\n"
            "━━━━━━━━━━━━━━\n"
            "ရိုးရာဇာတာတွက်ချက်မှုများနှင့် နက္ခတ်အနက်ဖွင့်ဆိုချက်များကို "
            "ဤဇာတာခန်းမှ ရွေးချယ်ကြည့်ရှုနိုင်ပါပြီ။\n\n"
            "အောက်ပါခလုတ်များမှ စတင်ရွေးချယ်ပါ။\n"
            "<i>မွေးဖွားမှုအချက်အလက်ကို သီးသန့်စကားဝိုင်းတွင်သာ ဖြည့်ပါ။</i>")

def section_text(section: str):
    if section not in SECTIONS:
        raise KeyError(section)
    return "<b>"+SECTIONS[section][0]+"</b>\n━━━━━━━━━━━━━━\nစိတ်ဝင်စားရာ ဇာတာခန်းကို ရွေးပါ။"

def feature_text(feature: str):
    if feature not in FEATURES:
        raise KeyError(feature)
    title,description,_=FEATURES[feature]
    return "<b>"+title+"</b>\n━━━━━━━━━━━━━━\n"+description

def guide_text(command: str):
    if command not in COMMAND_GUIDES:
        raise KeyError(command)
    return ("<b>တွက်ချက်ရန်</b>\n━━━━━━━━━━━━━━\n"
            "သီးသန့်စကားဝိုင်းတွင် အောက်ပါ Command ကို ရိုက်ထည့်ပါ။\n\n"
            "<code>"+COMMAND_GUIDES[command]+"</code>\n\n"
            "ဒီခလုတ်က ကိုယ်ရေးအချက်အလက်ကို အလိုအလျောက် မဖြည့်၊ မသိမ်းပါ။")


def study_index_keyboard():
    rows=[[button(data["title"], "study:"+key)]
          for key,data in CHAPTERS.items()]
    rows.append([button("Back","ui:feature:study"),button("Home","ui:home")])
    return keyboard(rows)

def study_chapter_keyboard(key: str):
    data=chapter(key)
    rows=[[button("ကျမ်းကိုး — "+str(index), "evidence:"+rule)]
          for index,rule in enumerate(data["rules"],start=1)]
    rows.append([button("Back","ui:study"),button("Home","ui:home")])
    return keyboard(rows)


def group_home_keyboard(enabled=True):
    """No private birth/profile controls in group menus."""
    rows=[]
    if enabled:
        rows.append([button("ယနေ့ ရိုးရာပြက္ခဒိန်","group:today"),
                     button("တစ်ပတ်စာ ပြက္ခဒိန်","group:week")])
    rows.append([button("အဖွဲ့စည်းမျဉ်း","group:settings")])
    return keyboard(rows)

def group_home_text(enabled=True):
    status=("ယနေ့ /today သို့မဟုတ် တစ်ပတ်စာ /week ကြည့်နိုင်ပါတယ်။\n"
            if enabled else
            "ဤအဖွဲ့မှာ Admin က ရိုးရာပြက္ခဒိန်ကို ပိတ်ထားပါတယ်။\n")
    return ("<b>ကြယ်စင်တို့၏ အဖွဲ့ဇာတာခန်း</b>\n"
            "━━━━━━━━━━━━━━\n"
            "ဤအဖွဲ့မှာ မွေးအချက်အလက်မလိုတဲ့ မြန်မာရိုးရာပြက္ခဒိန်ကို "
            "ကြည့်နိုင်ပါတယ်။\n\n"
            +status+
            "အဖွဲ့စည်းမျဉ်းကို Admin က ပြင်နိုင်ပါတယ်။\n"
            "<i>ကိုယ်ပိုင်မွေးဇာတာနှင့် မွေးအချက်အလက်များကို "
            "Bot ၏ Private Chat တွင်သာ ဖြည့်ပါ။</i>")


def group_settings_text(enabled, persistent):
    status="ဖွင့်ထားပါတယ်" if enabled else "ပိတ်ထားပါတယ်"
    warning=("" if persistent else
        "\n\n<i>ယာယီသတ်မှတ်ချက်ပါ။ Bot ပြန်စတင်လျှင် ဖွင့်ထားသည့် မူလအခြေအနေသို့ ပြန်သွားနိုင်ပါတယ်။</i>")
    return ("<b>အဖွဲ့ရိုးရာပြက္ခဒိန် စည်းမျဉ်း</b>\n"
            "━━━━━━━━━━━━━━\n"
            "ယနေ့ပြက္ခဒိန် — <b>"+status+"</b>\n"
            "အဖွဲ့ Admin များသာ ပြောင်းနိုင်ပါတယ်။"+warning)

def group_settings_keyboard(enabled):
    action=("ပိတ်မယ်","groupcfg:off") if enabled else ("ပြန်ဖွင့်မယ်","groupcfg:on")
    return keyboard([[button(*action)],
                     [button("အဖွဲ့အစ", "groupcfg:home")]])

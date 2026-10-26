"""Native Telegram navigation: clean labels, minimal emoji, no Mini App.

Myanmar astrology keeps its Burmese inline label; international disciplines
use established English names. Telegram controls layout and button rendering.
Navigation is stateless and callback data never includes private birth data.
"""
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

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
        ("မွေးနေ့နံ", "myday"), ("မြန်မာပြက္ခဒိန်", "mmcal"))),
    "western": ("Western Astrology", "Western natal chart ကို Reference နဲ့ စစ်ဆေးနေဆဲဖြစ်လို့ မဖွင့်ရသေးပါ။", ()),
    "bazi": ("BaZi", "Four Pillars ကို တွက်နိုင်ပါတယ်။ True Solar Time နဲ့ seasonal validation မပြီးသေးပါ။", (
        ("Four Pillars", "bazi"),)),
    "number": ("Numerology", "Life Path ကို တွက်ချက်နိုင်ပါတယ်။ အသေးစိတ်ဟောစာတမ်း မပြီးသေးပါ။", (
        ("Life Path", "number"),)),
    "tarot": ("Tarot", "78-card Tarot ဆွဲနိုင်ပါတယ်။ ကတ်ပုံအစုံနဲ့ Animation မပြီးသေးပါ။", (
        ("Draw a Card", "tarot"),)),
    "profile": ("My Profile", "မွေးနေ့ကို သဘောတူမှသာ သိမ်းနိုင်ပြီး Private Chat မှာသာ ကြည့်နိုင်ပါတယ်။", (
        ("Save Birth Date", "savebirth"), ("View Birth Date", "mybirth"),
        ("Delete Birth Date", "forgetbirth"))),
    "reading": ("Personal Reading", "တွက်ချက်မှုနှင့် ရိုးရာဟောစာတမ်းစည်းမျဉ်းများ မပြီးသေးပါ။", ()),
    "compatibility": ("Compatibility", "နှစ်ဦးဇာတာ တွက်ချက်မှုနှင့် ရိုးရာနည်းလမ်းစစ်ဆေးခြင်း မပြီးသေးပါ။", ()),
    "daily": ("Daily Reading", "နေ့စဉ်ဟောစာတမ်းတွက်ချက်မှု မပြီးသေးပါ။", ()),
    "timing": ("Timing Cycles", "Timing backend အချို့ရှိပေမဲ့ လုံလောက်စွာ မစမ်းသပ်ရသေးပါ။", ()),
    "mmcal": ("မြန်မာပြက္ခဒိန်", "မြန်မာရက်စွဲ၊ လဆန်းလဆုတ်၊ ရက်ရာဇာနှင့် ပြဿဒါးတို့ကို တွက်နိုင်ပါတယ်။", (
        ("ရက်စွဲတွက်မယ်", "mmcal"),)),
    "library": ("Reference Library", "တွက်ချက်နည်းကို ရှင်းပြနိုင်တဲ့ Evidence Buttons ရှိပြီးသားပါ။ စာကြည့်တိုက်အပြည့် မပြီးသေးပါ။", ()),
    "study": ("Astrology Study", "သီးခြားလေ့လာခန်း မပြီးသေးပါ။", ()),
    "group": ("Group Settings", "Group Management UI မပြီးသေးပါ။ ကိုယ်ရေးအချက်အလက်ကို Private Chat မှာသာ ဖြည့်ပါ။", ()),
    "owner": ("Owner Controls", "Owner Dashboard မပြီးသေးပါ။", ()),
}
COMMAND_GUIDES = {
    "myday": "/myday 2005-12-23 08:37",
    "mmcal": "/mmcal 2024-01-01",
    "bazi": "/bazi 2005-12-23 08:37 Asia/Yangon",
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
    rows=[[button(label,("ui:tarot" if cmd=="tarot" else "ui:guide:"+cmd))]
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

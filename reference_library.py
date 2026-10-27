"""Stateless evidence library using already reviewed method registry.

No birth dates, Telegram IDs, queries or private profile data are embedded in
callback URLs. Small immutable page numbers ensure callbacks stay below 64 bytes.
"""
from html import escape
from evidence_ui import RULES

PAGE_SIZE=5
CATEGORY_PREFIXES={
    "mm":"MM-",
    "west":"WEST-",
    "bazi":"CHN-BAZI-",
    "num":"NUM-",
    "tarot":"TAROT-",
}
CATEGORY_LABELS={
    "mm":"မြန်မာဗေဒင်",
    "west":"Western Astrology",
    "bazi":"BaZi",
    "num":"Numerology",
    "tarot":"Tarot",
}
MAX_PAGE=99

def entries(category: str):
    if category not in CATEGORY_PREFIXES:
        raise ValueError("Unknown library category")
    prefix=CATEGORY_PREFIXES[category]
    return [(key,RULES[key]) for key in sorted(RULES) if key.startswith(prefix)]

def library_page(category: str, page: int) -> dict:
    if type(page) is not int or not 0 <= page <= MAX_PAGE:
        raise ValueError("Invalid evidence page")
    all_entries=entries(category)
    count=max(1,(len(all_entries)+PAGE_SIZE-1)//PAGE_SIZE)
    if page>=count:
        raise ValueError("Evidence page out of range")
    start=page*PAGE_SIZE
    chosen=all_entries[start:start+PAGE_SIZE]
    return {
        "category":category,
        "title":CATEGORY_LABELS[category],
        "page":page,
        "page_count":count,
        "total":len(all_entries),
        "items":[{"id":key,"heading":data["heading"]} for key,data in chosen],
    }

def render_library(page_info:dict) -> str:
    title=escape(page_info["title"])
    items=page_info["items"]
    names="\n".join(
        f'{page_info["page"]*PAGE_SIZE+i+1}. {escape(item["heading"])}'
        for i,item in enumerate(items)
    ) if items else "ဤအမျိုးအစား၏ ကိုးကားချက်ကို ဆက်လက်စိစစ်နေဆဲဖြစ်သည်။"
    return (
        f"<b>{title} — ကျမ်းကိုးမှတ်တမ်း</b>\n"
        "━━━━━━━━━━━━━━\n"
        f"{names}\n\n"
        f'စာမျက်နှာ {page_info["page"]+1}/{page_info["page_count"]} · '
        f'မှတ်တမ်း {page_info["total"]} ခု\n'
        "အောက်ပါခလုတ်မှ တွက်ချက်နည်း၊ မူရင်းကိုးကားချက်နှင့် ကန့်သတ်ချက်များကို ကြည့်နိုင်သည်။ "
        "ရိုးရာဗေဒင်၏ အနာဂတ်ခန့်မှန်းနိုင်မှုကို သိပ္ပံနည်းကျ သက်သေပြခြင်း မဟုတ်ပါ။"
    )

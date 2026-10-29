"""Private Telegram commands for explicitly consented encrypted birth profiles.

The source of truth is ProfileStore. No implicit save from /number or /bazi.
"""
import os
from functools import lru_cache
from datetime import date

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from profile_store import ProfileStore

router=Router()

@lru_cache(maxsize=1)
def _store():
    # Free Render web services have no persistent disk. Opt-in profiles must
    # not silently land on a filesystem that disappears on spin-down/redeploy.
    # This guard is NOT proof of a mounted disk: the operator must verify it.
    if os.environ.get("RENDER") and os.environ.get("PROFILE_PERSISTENT_DISK_CONFIRMED")!="1":
        return None
    key=os.environ.get("PROFILE_ENCRYPTION_KEY")
    db=os.environ.get("PROFILE_DB_PATH")
    if not key or not db:
        return None
    return ProfileStore(db,key)

def parse_consent_command(body: str):
    """Exact syntax; a second affirmative marker is required."""
    items=(body or "").strip().split()
    if len(items)!=3 or items[0]!="/savebirth" or items[2]!="အတည်ပြု":
        raise ValueError("Explicit affirmative required")
    birth_date=date.fromisoformat(items[1])
    if birth_date>date.today():
        raise ValueError("Birth date in the future")
    return birth_date.isoformat()

@router.message(Command("savebirth"))
async def save_birth(message:Message):
    if message.chat.type!="private" or message.from_user is None:
        await message.answer("🔐 မွေးနေ့သိမ်းခြင်းကို သီးသန့်ဇာတာခန်းမှာသာ လုပ်နိုင်ပါတယ်။")
        return
    try:
        birthday=parse_consent_command(message.text or "")
    except ValueError:
        await message.answer(
            "📜 မွေးနေ့ကို သိမ်းဖို့ သဘောတူပါက\n"
            "<code>/savebirth 2005-12-23 အတည်ပြု</code>\n\n"
            "မသိမ်းချင်ရင် ကျော်သွားနိုင်ပါတယ်။",
            parse_mode="HTML")
        return
    store=_store()
    if store is None:
        await message.answer("🌫️ လုံခြုံသော ဇာတာသိမ်းဆည်းမှုကို မဖွင့်ရသေးပါ။")
        return
    try:
        store.save(message.from_user.id,{"birth_date":birthday},explicit_consent=True)
    except Exception:
        # Do not echo exception details or encrypted/secret payloads in chat.
        await message.answer("🌫️ ဇာတာမှတ်တမ်း မသိမ်းနိုင်သေးပါ။ နောက်တစ်ကြိမ် ပြန်စမ်းပါ။")
        return
    await message.answer("📜 သင့်မွေးနေ့ကို လုံခြုံစွာ မှတ်သားထားပါပြီ။\nလိုချင်တဲ့အချိန် /forgetbirth နဲ့ ဖျက်နိုင်ပါတယ်။")

@router.message(Command("forgetbirth"))
async def forget_birth(message:Message):
    if message.chat.type!="private" or message.from_user is None:
        await message.answer("🔐 မွေးနေ့မှတ်တမ်းကို သီးသန့်ဇာတာခန်းမှာသာ ဖျက်နိုင်ပါတယ်။")
        return
    store=_store()
    if store is None:
        await message.answer("🌙 သိမ်းထားသော ဇာတာမှတ်တမ်း မရှိပါ။")
        return
    try:
        removed=store.delete(message.from_user.id)
    except Exception:
        await message.answer("🌫️ မှတ်တမ်းဖျက်မှု မအောင်မြင်သေးပါ။")
        return
    await message.answer("🌙 ဇာတာမှတ်တမ်း ဖျက်ပြီးပါပြီ။" if removed else "🌙 သိမ်းထားသော ဇာတာမှတ်တမ်း မရှိပါ။")

@router.message(Command("mybirth"))
async def show_birth(message:Message):
    if message.chat.type!="private" or message.from_user is None:
        await message.answer("🔐 ကိုယ်ပိုင်ဇာတာမှတ်တမ်းကို သီးသန့်မှာပဲ ကြည့်နိုင်ပါတယ်။")
        return
    store=_store()
    if store is None:
        await message.answer("🌙 သိမ်းထားသော ဇာတာမှတ်တမ်း မရှိပါ။")
        return
    try:
        record=store.read(message.from_user.id)
    except Exception:
        await message.answer("🌫️ မှတ်တမ်းကို မဖတ်နိုင်ပါ။")
        return
    if record is None:
        await message.answer("🌙 သိမ်းထားသော ဇာတာမှတ်တမ်း မရှိပါ။")
    else:
        from html import escape
        await message.answer("📜 <b>သင့်ဇာတာမှတ်တမ်း</b>\nမွေးနေ့ — <code>"+escape(str(record["birth_date"]))+"</code>",parse_mode="HTML")

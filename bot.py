"""Telegram astrology bot development shell. No deployment or database yet.

Secrets are read from environment only. Birth data is not persisted.
"""
import asyncio
import html
import logging
import os
from datetime import date, datetime

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from astro_core import life_path
from bazi_core import calculate_bazi
from tarot_core import draw_tarot
from myanmar_core import myanmar_birth_day

dp=Dispatcher()

def menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='🌙 ဇာတာခန်း', callback_data='section:charts'),InlineKeyboardButton(text='📜 ဗေဒင်ကျမ်းတိုက်', callback_data='section:library')],
        [InlineKeyboardButton(text='🇲🇲 မွေးနေ့နံ ကြည့်မယ်', callback_data='section:myday')],
        [InlineKeyboardButton(text='🃏 တားရော့ကတ် ဆွဲမယ်', callback_data='tarot:single')],
        [InlineKeyboardButton(text='✨ တွက်ချက်နည်းများ', callback_data='section:methods')],
    ])

WELCOME=(
    '🌙 <b>ကြယ်စင်တို့၏ လမ်းညွှန်ရာ</b>\n'
    '━━━━━━━━━━━━━━\n'
    'မြန်မာ့ရိုးရာ၊ အနောက်တိုင်းနှင့် တရုတ်ဇာတာပညာ၊ ကိန်းဂဏန်းဗေဒင်၊ '
    'တားရော့ကတ်တို့ကို လေ့လာနိုင်မည့် ဇာတာခန်းမှ ကြိုဆိုပါတယ်။\n\n'
    '📜 <b>လက်ရှိ စမ်းသပ်နိုင်သောတွက်ချက်မှုများ</b>\n'
    '• /number 1999-12-31 — မွေးနေ့ကိန်းဂဏန်း\n'
    '• /bazi 2005-12-23 08:37 — တရုတ်ဇာတာလေးတိုင်\n'
    '• /myday 2005-12-23 08:37 — မြန်မာ့မွေးနေ့နံ\n'
    '• /tarot — တားရော့ကတ်တစ်ချပ်\n\n'
    'မွေးနေ့၊ မွေးချိန်တွေကို <b>သီးသန့်စကားဝိုင်းမှာသာ</b> ပို့ပါ။ '
    'လက်ရှိအဆင့်မှာ အချက်အလက်တွေကို Database ထဲမသိမ်းထားပါ။'
)

def private_only(message: Message) -> bool:
    return message.chat.type == 'private'

@dp.message(CommandStart())
async def welcome(message: Message):
    await message.answer(WELCOME, reply_markup=menu(), parse_mode='HTML')

@dp.message(Command('help'))
async def help_message(message: Message):
    await welcome(message)

@dp.callback_query(F.data == 'section:charts')
async def charts(cb: CallbackQuery):
    await cb.answer()
    await cb.message.answer('🌙 <b>ဇာတာတွက်ကြည့်မယ်</b>\n\n/number YYYY-MM-DD\n/bazi YYYY-MM-DD HH:MM\n/myday YYYY-MM-DD HH:MM\n\nမွေးနေ့နှင့် မွေးချိန်ကို သီးသန့်စကားဝိုင်းတွင်သာ ဖြည့်ပါ။',parse_mode='HTML')

@dp.callback_query(F.data == 'section:library')
async def library(cb: CallbackQuery):
    await cb.answer('📜 ဇာတာကျမ်းတိုက်ကို ဆက်လက်ပြုစုနေပါပြီ။',show_alert=True)

@dp.callback_query(F.data == 'section:methods')
async def methods(cb: CallbackQuery):
    await cb.answer()
    await cb.message.answer('📖 <b>တွက်ချက်မှုမှတ်တမ်း</b>\n\nအတည်ပြုနိုင်သည့် တွက်ချက်နည်း၊ မူရင်းကိုးကားချက်နှင့် မူကွဲများကို ဟောစာတမ်းနှင့်အတူ ပြသနိုင်ရန် တည်ဆောက်နေပါပြီ။',parse_mode='HTML')


@dp.callback_query(F.data == 'section:myday')
async def myday_guide(cb: CallbackQuery):
    await cb.answer()
    await cb.message.answer(
        '🇲🇲 <b>မြန်မာ့မွေးနေ့နံ</b>\n\n'
        'မွေးရပ်ဒေသ၏ ဒေသစံတော်ချိန်နဲ့ ဖြည့်ပါ။\n'
        '<code>/myday 2005-12-23 08:37</code>\n\n'
        'မွေးနေ့နှင့် မွေးချိန်ကို သီးသန့်စကားဝိုင်းမှာပဲ ပို့ပါ။',
        parse_mode='HTML'
    )

@dp.message(Command('myday'))
async def myday_command(message: Message):
    if not private_only(message):
        await message.answer('🔐 မွေးနေ့နဲ့ မွေးချိန်ကို အဖွဲ့ထဲမပို့ပါနဲ့။ သီးသန့်ဇာတာခန်းမှာပဲ ဖြည့်ပါ။')
        return
    parts=(message.text or '').split()
    if len(parts)!=3:
        await message.answer('🇲🇲 မွေးရပ်ဒေသရဲ့ ဒေသစံတော်ချိန်ကို ဖြည့်ပါ။\n<code>/myday 2005-12-23 08:37</code>',parse_mode='HTML')
        return
    try:
        birth=datetime.strptime(parts[1]+' '+parts[2],'%Y-%m-%d %H:%M')
        if birth.date()>date.today(): raise ValueError('Future date')
        result=myanmar_birth_day(birth)
    except ValueError:
        await message.answer('🌫️ မွေးနေ့နဲ့ မွေးချိန်ကို YYYY-MM-DD HH:MM ပုံစံနဲ့ ပြန်စစ်ပါ။')
        return
    await message.answer(
        '🇲🇲 <b>မြန်မာ့မွေးနေ့နံ</b>\n━━━━━━━━━━━━━━\n'
        f'<b>{html.escape(result["weekday"])}</b>\n'
        f'ဆက်စပ်ဂြိုဟ် — <b>{html.escape(result["planetary_association"])}</b>\n\n'
        f'📖 <code>{result["evidence"]["rule_id"]}</code>\n'
        'ဤရလဒ်မှာ ရိုးရာ ၈ နေ့နံအလိုက် တွက်ချက်ထားခြင်းဖြစ်ပြီး မဟာဘုတ်ဇာတာ မဟုတ်သေးပါ။',
        parse_mode='HTML'
    )

@dp.message(Command('number'))
async def numerology(message: Message):
    if not private_only(message):
        await message.answer('🔐 မွေးနေ့ကို လူအများရှေ့ မဖော်ပြပါနဲ့။ ကျွန်ုပ်နဲ့ သီးသန့်စကားဝိုင်းမှာ /number YYYY-MM-DD ဖြည့်ပါ။')
        return
    parts=(message.text or '').split()
    if len(parts)!=2:
        await message.answer('🔢 မွေးနေ့ကို ဤပုံစံလေးနဲ့ ဖြည့်ပါ။\n<code>/number 1999-12-31</code>',parse_mode='HTML')
        return
    try:
        born=date.fromisoformat(parts[1])
        if born > date.today(): raise ValueError('future date')
        result=life_path(born)
    except ValueError:
        await message.answer('🌫️ မွေးနေ့ပုံစံ မမှန်သေးပါ။ YYYY-MM-DD အတိုင်း ပြန်ဖြည့်ပေးပါ။')
        return
    await message.answer(
        f'🔢 <b>သင့်ဘဝလမ်းကြောင်းကိန်း — {result["number"]}</b>\n'
        '━━━━━━━━━━━━━━\n'
        'Pythagorean-style ကိန်းဂဏန်းတွက်နည်းအရ ထွက်ပေါ်လာသည့်ရလဒ်ဖြစ်သည်။\n\n'
        f'📖 စည်းမျဉ်း: <code>{result["evidence"]["rule_id"]}</code>\n'
        'ဟောကိန်းအနက်ဖွင့်ဆိုချက်များကို ကျမ်းကိုးစစ်ဆေးပြီးမှ ဖြည့်သွင်းမည်။',
        parse_mode='HTML',
    )

@dp.message(Command('bazi'))
async def bazi(message: Message):
    if not private_only(message):
        await message.answer('🔐 မွေးချိန်ကို လူအများရှေ့ မဖော်ပြပါနဲ့။ သီးသန့်စကားဝိုင်းမှာပဲ ဖြည့်ပေးပါ။')
        return
    parts=(message.text or '').split()
    if len(parts)!=3:
        await message.answer('🐉 မွေးရပ်ဒေသ၏ ဒေသစံတော်ချိန်ဖြင့် ဖြည့်ပါ။\n<code>/bazi 2005-12-23 08:37</code>',parse_mode='HTML')
        return
    try:
        born=datetime.strptime(parts[1]+' '+parts[2],'%Y-%m-%d %H:%M')
        if born.date()>date.today(): raise ValueError('future date')
        result=calculate_bazi(born)
    except (ValueError,RuntimeError):
        await message.answer('🌫️ မွေးချိန်ကို မတွက်နိုင်သေးပါ။ YYYY-MM-DD HH:MM ပုံစံနှင့် မွေးရပ်ဒေသအချိန်ကို စစ်ဆေးပါ။')
        return
    p=result['pillars']
    await message.answer(
        '🐉 <b>တရုတ်ဇာတာလေးတိုင်</b>\n━━━━━━━━━━━━━━\n'
        f'နှစ်တိုင် — <b>{html.escape(p["year"])}</b>\n'
        f'လတိုင် — <b>{html.escape(p["month"])}</b>\n'
        f'ရက်တိုင် — <b>{html.escape(p["day"])}</b>\n'
        f'နာရီတိုင် — <b>{html.escape(p["hour"])}</b>\n\n'
        f'📖 <code>{result["evidence"]["rule_id"]}</code>\n'
        'မွေးရပ်ဒေသ Timezone နှင့် True Solar Time ကို မစစ်နိုင်သေးသည့် စမ်းသပ်ဇာတာဖြစ်သည်။',
        parse_mode='HTML'
    )

@dp.message(Command('tarot'))
async def tarot_cmd(message: Message):
    await send_tarot(message)

@dp.callback_query(F.data == 'tarot:single')
async def tarot_cb(cb: CallbackQuery):
    await cb.answer()
    await send_tarot(cb.message)

async def send_tarot(message: Message):
    card=draw_tarot('single')['cards'][0]['card']
    await message.answer(
        f'🃏 <b>ယနေ့ သင့်လက်ထဲကျလာသောကတ်</b>\n━━━━━━━━━━━━━━\n'
        f'<b>{html.escape(card)}</b>\n\n'
        'ကတ်ဆွဲခြင်းမှာ ကျပန်းဖြစ်ပြီး ရိုးရာအနက်ဖွင့်ဆိုချက်ကို စိစစ်ပြုစုနေဆဲဖြစ်သည်။',
        parse_mode='HTML'
    )

async def main():
    token=os.environ.get('TELEGRAM_BOT_TOKEN')
    if not token:
        raise SystemExit('Set TELEGRAM_BOT_TOKEN in your private environment')
    logging.basicConfig(level=logging.INFO)
    bot=Bot(token=token)
    await dp.start_polling(bot)

if __name__=='__main__':
    asyncio.run(main())

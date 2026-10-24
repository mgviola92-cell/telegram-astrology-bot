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
from birth_time import normalize_birth_wall_time
from tarot_core import draw_tarot
from tarot_sessions import TarotSessions
from myanmar_core import myanmar_birth_day
from myanmar_calendar import calculate_myanmar_calendar
from evidence_ui import evidence_button, get_rule

dp=Dispatcher()
tarot_sessions = TarotSessions()

def menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='🌙 ဇာတာခန်း', callback_data='section:charts'),InlineKeyboardButton(text='📜 ဗေဒင်ကျမ်းတိုက်', callback_data='section:library')],
        [InlineKeyboardButton(text='🇲🇲 မွေးနေ့နံ ကြည့်မယ်', callback_data='section:myday'),InlineKeyboardButton(text='📅 မြန်မာပြက္ခဒိန်', callback_data='section:mmcal')],
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
    '• /bazi 2005-12-23 08:37 Asia/Yangon — တရုတ်ဇာတာလေးတိုင်\n'
    '• /myday 2005-12-23 08:37 — မြန်မာ့မွေးနေ့နံ\n'
    '• /mmcal 2024-01-01 — မြန်မာပြက္ခဒိန်\n'
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
    await cb.message.answer('🌙 <b>ဇာတာတွက်ကြည့်မယ်</b>\n\n/number YYYY-MM-DD\n/bazi YYYY-MM-DD HH:MM Asia/Yangon\n/myday YYYY-MM-DD HH:MM\n\nမွေးနေ့နှင့် မွေးချိန်ကို သီးသန့်စကားဝိုင်းတွင်သာ ဖြည့်ပါ။',parse_mode='HTML')

@dp.callback_query(F.data == 'section:library')
async def library(cb: CallbackQuery):
    await cb.answer('📜 ဇာတာကျမ်းတိုက်ကို ဆက်လက်ပြုစုနေပါပြီ။',show_alert=True)

@dp.callback_query(F.data == 'section:methods')
async def methods(cb: CallbackQuery):
    await cb.answer()
    await cb.message.answer('📖 <b>တွက်ချက်မှုမှတ်တမ်း</b>\n\nအတည်ပြုနိုင်သည့် တွက်ချက်နည်း၊ မူရင်းကိုးကားချက်နှင့် မူကွဲများကို ဟောစာတမ်းနှင့်အတူ ပြသနိုင်ရန် တည်ဆောက်နေပါပြီ။',parse_mode='HTML')


@dp.callback_query(F.data.startswith('evidence:'))
async def show_evidence(cb: CallbackQuery):
    rule_id=(cb.data or '').split(':',1)[1]
    try:
        record=get_rule(rule_id)
    except KeyError:
        await cb.answer('🌫️ ဤမှတ်တမ်းကို မတွေ့တော့ပါ။',show_alert=True)
        return
    await cb.answer()
    await cb.message.answer(
        '📖 <b>'+html.escape(record['heading'])+'</b>\n'
        '━━━━━━━━━━━━━━\n'
        '<b>တွက်ချက်ပုံ</b>\n'+html.escape(record['method'])+'\n\n'
        '<b>မူရင်းကိုးကား</b>\n'+html.escape(record['source'])+'\n\n'
        '<b>သိထားရန်</b>\n'+html.escape(record['limits']),
        parse_mode='HTML'
    )

@dp.callback_query(F.data == 'section:mmcal')
async def myanmar_calendar_guide(cb: CallbackQuery):
    await cb.answer()
    await cb.message.answer(
        '📅 <b>မြန်မာပြက္ခဒိန်</b>\n'
        'မြန်မာရက်စွဲ၊ မဟာဘုတ်၊ ရက်ရာဇာ၊ ပြဿဒါးတို့ကို တွက်ကြည့်နိုင်ပါတယ်။\n'
        '<code>/mmcal 2024-01-01</code>',
        parse_mode='HTML'
    )

@dp.message(Command('mmcal'))
async def myanmar_calendar_command(message: Message):
    if not private_only(message):
        await message.answer('🔐 မွေးနေ့လို ကိုယ်ရေးအချက်အလက်တွေကို သီးသန့်ဇာတာခန်းမှာပဲ ဖြည့်ပါ။')
        return
    fields=(message.text or '').split()
    if len(fields)!=2:
        await message.answer('📅 မြန်မာပြက္ခဒိန်ကြည့်ဖို့ <code>/mmcal 2024-01-01</code> လို့ ဖြည့်ပါ။',parse_mode='HTML')
        return
    try:
        day=date.fromisoformat(fields[1])
        result=calculate_myanmar_calendar(day)
    except (ValueError,TypeError):
        await message.answer('🌫️ 1900–2100 အတွင်း YYYY-MM-DD ပုံစံနဲ့ ရက်စွဲပြန်ဖြည့်ပါ။')
        return
    phases={'waxing':'လဆန်း','full moon':'လပြည့်','waning':'လဆုတ်','new moon':'လကွယ်'}
    phase=phases[result['moon_phase']]
    yatyaza='ရက်ရာဇာ' if result['yatyaza'] else 'မဟုတ်ပါ'
    pyathada={0:'မဟုတ်ပါ',1:'ပြဿဒါး',2:'မွန်းလွဲပြဿဒါး'}[result['pyathada']]
    await message.answer(
        '📅 <b>မြန်မာပြက္ခဒိန် ရက်စွဲ</b>\n━━━━━━━━━━━━━━\n'
        f'မြန်မာသက္ကရာဇ် — <b>{result["myanmar_year"]}</b>\n'
        f'မြန်မာလ — <b>{html.escape(result["month"])}</b>\n'
        f'လရက် — <b>{result["day"]}</b>\n'
        f'လအခြေအနေ — <b>{phase} {result["fortnight_day"]} ရက်</b>\n'
        f'မဟာဘုတ် — <b>{html.escape(result["mahabote"])}</b>\n'
        f'ရက်ရာဇာ — <b>{yatyaza}</b>\n'
        f'ပြဿဒါး — <b>{pyathada}</b>\n\n'
        'ရိုးရာတွက်ချက်မှုရလဒ်ဖြစ်ပြီး အနာဂတ်ဖြစ်ရပ်အာမခံချက် မဟုတ်ပါ။',
        parse_mode='HTML',
        reply_markup=evidence_button(result['evidence']['rule_id'])
    )

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
        parse_mode='HTML', reply_markup=evidence_button(result['evidence']['rule_id'])
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
        parse_mode='HTML', reply_markup=evidence_button(result['evidence']['rule_id']),
    )

@dp.message(Command('bazi'))
async def bazi(message: Message):
    if not private_only(message):
        await message.answer('🔐 မွေးချိန်ကို လူအများရှေ့ မဖော်ပြပါနဲ့။ သီးသန့်စကားဝိုင်းမှာပဲ ဖြည့်ပေးပါ။')
        return
    parts=(message.text or '').split()
    if len(parts)!=4:
        await message.answer('🐉 မွေးရပ်ဒေသ၏ ဒေသစံတော်ချိန်ဖြင့် ဖြည့်ပါ။\n<code>/bazi 2005-12-23 08:37 Asia/Yangon</code>',parse_mode='HTML')
        return
    try:
        born=datetime.strptime(parts[1]+' '+parts[2],'%Y-%m-%d %H:%M')
        if born.date()>date.today(): raise ValueError('future date')
        normalized=normalize_birth_wall_time(born,parts[3])
        result=calculate_bazi(normalized['wall_time'], timezone_verified=normalized['timezone'])
    except (ValueError,RuntimeError):
        await message.answer('🌫️ မွေးချိန်ကို မတွက်နိုင်သေးပါ။ YYYY-MM-DD HH:MM Asia/Yangon ပုံစံနဲ့ မွေးရပ်ဒေသရဲ့ Timezone ကို စစ်ဆေးပါ။ DST နာရီနှစ်ခါဖြစ်တဲ့ ရက်တွေမှာ မွေးချိန်အတည်ပြုဖို့ လိုပါတယ်။')
        return
    p=result['pillars']
    await message.answer(
        '🐉 <b>တရုတ်ဇာတာလေးတိုင်</b>\n━━━━━━━━━━━━━━\n'
        f'နှစ်တိုင် — <b>{html.escape(p["year"])}</b>\n'
        f'လတိုင် — <b>{html.escape(p["month"])}</b>\n'
        f'ရက်တိုင် — <b>{html.escape(p["day"])}</b>\n'
        f'နာရီတိုင် — <b>{html.escape(p["hour"])}</b>\n\n'
        f'📖 <code>{result["evidence"]["rule_id"]}</code>\n'
        f'လက်ခံထားသော Timezone — <code>{html.escape(normalized["timezone"])}</code>\n'
        'True Solar Time မပြင်ရသေးသော စမ်းသပ်ဇာတာဖြစ်သည်။',
        parse_mode='HTML', reply_markup=evidence_button(result['evidence']['rule_id'])
    )

def tarot_choice_keyboard(token: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text='🌙 ပထမကတ်', callback_data=f'tarotpick:{token}:0'),
        InlineKeyboardButton(text='✨ ဒုတိယကတ်', callback_data=f'tarotpick:{token}:1'),
        InlineKeyboardButton(text='🔮 တတိယကတ်', callback_data=f'tarotpick:{token}:2'),
    ]])


async def open_tarot(message: Message, *, user_id: int):
    if message.chat.type != 'private':
        await message.answer('🌙 ကံကြမ္မာကတ်ရွေးဖို့ သီးသန့်ဇာတာခန်းကို ဝင်ခဲ့ပါ။')
        return
    token = tarot_sessions.start(owner_id=user_id, chat_id=message.chat.id)
    text = ('🃏 <b>ကတ်သုံးချပ်ထဲက တစ်ချပ်ရွေးပါ</b>\n'
            '━━━━━━━━━━━━━━\n'
            'ကြယ်စင်တို့၏ နိမိတ်ကို ဘယ်ကတ်က ဖော်ပြမလဲ…')
    media_id = os.getenv('TAROT_SHUFFLE_FILE_ID', '').strip()
    if media_id:
        try:
            sent = await message.answer_animation(
                animation=media_id, caption=text, parse_mode='HTML',
                reply_markup=tarot_choice_keyboard(token)
            )
        except Exception:
            logging.exception('Configured Tarot animation unavailable; using text fallback')
            sent = await message.answer(text, parse_mode='HTML', reply_markup=tarot_choice_keyboard(token))
    else:
        sent = await message.answer(text, parse_mode='HTML', reply_markup=tarot_choice_keyboard(token))
    tarot_sessions.bind_message(token, owner_id=user_id, chat_id=message.chat.id, message_id=sent.message_id)


@dp.message(Command('tarot'))
async def tarot_cmd(message: Message):
    if not message.from_user:
        return
    await open_tarot(message, user_id=message.from_user.id)


@dp.callback_query(F.data == 'tarot:single')
async def tarot_cb(cb: CallbackQuery):
    await cb.answer()
    if cb.message:
        await open_tarot(cb.message, user_id=cb.from_user.id)


@dp.callback_query(F.data.startswith('tarotpick:'))
async def tarot_pick(cb: CallbackQuery):
    try:
        _, token, raw_choice = (cb.data or '').split(':', 2)
        choice = int(raw_choice)
    except (ValueError, TypeError):
        await cb.answer('🌫️ ကတ်ရွေးချယ်မှု မမှန်ပါ။', show_alert=True)
        return
    if not cb.message:
        await cb.answer('🌫️ ဤကတ်ကို ဖွင့်မရတော့ပါ။', show_alert=True)
        return
    status, card = tarot_sessions.reveal(
        token, owner_id=cb.from_user.id, chat_id=cb.message.chat.id,
        message_id=cb.message.message_id, choice=choice
    )
    if status != 'ok':
        notices = {
            'unauthorized': '🌙 ဒီကတ်က သင့်အတွက် ရွေးထားတာ မဟုတ်ပါ။',
            'expired': '🌫️ ကတ်ရွေးချိန်ကုန်သွားပါပြီ။ အသစ်ပြန်ဆွဲပါ။',
            'already_used': '✨ ဒီကတ်ကို ဖွင့်ပြီးပါပြီ။',
            'invalid': '🌫️ ကတ်ရွေးချယ်မှု မမှန်ပါ။',
        }
        await cb.answer(notices.get(status, '🌫️ နောက်တစ်ကြိမ် ပြန်စမ်းပါ။'), show_alert=True)
        return
    await cb.answer('✨ သင့်ကတ်ကို ဖွင့်လိုက်ပါပြီ။')
    result_text = (
        '🃏 <b>သင့်ထံ ရောက်လာသောကတ်</b>\n━━━━━━━━━━━━━━\n'
        f'<b>{html.escape(card)}</b>\n\n'
        'ဤကတ်ကို ရိုးရာ Tarot ကတ် ၇၈ ချပ်မှ ကျပန်းရွေးထားသည်။ '
        'ကျမ်းကိုးအခြေခံ Card Meanings ကို ဆက်လက်စိစစ်နေသည်။'
    )
    # Reuse one Telegram-hosted asset for every reveal; result name always comes
    # from the previously assigned session, not from media filenames.
    reveal_id = os.getenv('TAROT_REVEAL_FILE_ID', '').strip()
    try:
        if reveal_id:
            from aiogram.types import InputMediaAnimation
            await cb.message.edit_media(
                media=InputMediaAnimation(media=reveal_id, caption=result_text, parse_mode='HTML'),
                reply_markup=evidence_button('TAROT-DRAW-001')
            )
        elif cb.message.animation:
            # edit_caption reuses the same Telegram-hosted shuffle animation without reuploading
            await cb.message.edit_caption(caption=result_text, parse_mode='HTML',
                reply_markup=evidence_button('TAROT-DRAW-001'))
        else:
            await cb.message.edit_text(result_text, parse_mode='HTML',
                reply_markup=evidence_button('TAROT-DRAW-001'))
    except Exception:
        logging.exception('Cannot edit Tarot card message; sending text fallback')
        await cb.message.answer(result_text, parse_mode='HTML',
            reply_markup=evidence_button('TAROT-DRAW-001'))


async def main():
    token=os.environ.get('TELEGRAM_BOT_TOKEN')
    if not token:
        raise SystemExit('Set TELEGRAM_BOT_TOKEN in your private environment')
    logging.basicConfig(level=logging.INFO)
    bot=Bot(token=token)
    await dp.start_polling(bot)

if __name__=='__main__':
    asyncio.run(main())

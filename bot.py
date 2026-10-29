"""Telegram astrology bot development shell; not deployed.

Secrets are read from environment only. Opt-in encrypted profile storage is
available only when configured; ordinary reading commands do not persist data.
"""
import asyncio
import html
import logging
import os
from datetime import date, datetime, time

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from astro_core import life_path
from numerology_reading import interpret_life_path
from profection_reading import profection_reading
from natal_pipeline import assemble_natal
from natal_render import render_natal_preview
from zoneinfo import ZoneInfo
from reading_facts import reading_facts
from myanmar_day_reading import calendar_marker_reading
from bazi_core import calculate_bazi
from bazi_element_reading import bazi_element_reading
from bazi_growth_stages import calculate_growth_stages
from bazi_seasons import calculate_bazi_seasons
from bazi_luck import calculate_bazi_luck
from dayun_reading import verified_dayun_reading
from birth_time import normalize_birth_wall_time
from tarot_core import draw_tarot
from tarot_meanings import interpret_tarot_card
from tarot_delivery import TarotAssetPolicy
from outbound_budget import CooldownBudget
from tarot_sessions import TarotSessions
from myanmar_core import myanmar_birth_day
from myanmar_calendar import calculate_myanmar_calendar
from mahabote_core import calculate_mahabote, BURMESE_HOUSES
from mahabote_reading import interpret_mahabote
from personal_reading import personal_reading
from reading_input import ReadingInputSessions
from myanmar_day_signals import calculate_day_signals
from myanmar_signal_reading import describe_day_signals
from daily_calendar_reading import daily_calendar_reading
from evidence_ui import evidence_button, get_rule
from reference_library import library_page, render_library, CATEGORY_LABELS
from profile_commands import router as profile_router
from native_ui import (home_keyboard, home_text, section_keyboard, section_text,
                       feature_keyboard, feature_text, guide_keyboard, guide_text,
                       SECTIONS, FEATURES, COMMAND_GUIDES)

dp=Dispatcher()
dp.include_router(profile_router)
tarot_sessions = TarotSessions()
tarot_delivery = TarotAssetPolicy()
tarot_cooldown = CooldownBudget(seconds=3.0,capacity=1000)
reading_inputs = ReadingInputSessions(ttl=300)

def menu():
    return home_keyboard()


WELCOME = home_text()

def private_only(message: Message) -> bool:
    return message.chat.type == 'private'

@dp.message(CommandStart())
async def welcome(message: Message):
    await message.answer(WELCOME, reply_markup=menu(), parse_mode='HTML')

@dp.message(Command('help'))
async def help_message(message: Message):
    await welcome(message)

def reference_category_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=CATEGORY_LABELS[c],callback_data="library:"+c+":0")]
        for c in CATEGORY_LABELS
    ] + [[InlineKeyboardButton(text="Back",callback_data="ui:feature:library"),
          InlineKeyboardButton(text="Home",callback_data="ui:home")]])


def reference_page_keyboard(info):
    buttons=[
        [InlineKeyboardButton(text=item["heading"][:45],
                              callback_data="evidence:"+item["id"])]
        for item in info["items"]
    ]
    nav=[]
    if info["page"]>0:
        nav.append(InlineKeyboardButton(text="Previous",
                   callback_data=f'library:{info["category"]}:{info["page"]-1}'))
    if info["page"]+1<info["page_count"]:
        nav.append(InlineKeyboardButton(text="Next",
                   callback_data=f'library:{info["category"]}:{info["page"]+1}'))
    if nav:
        buttons.append(nav)
    buttons.append([InlineKeyboardButton(text="Back",callback_data="ui:library"),
                    InlineKeyboardButton(text="Home",callback_data="ui:home")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


@dp.callback_query(F.data.startswith("library:"))
async def reference_library_navigation(cb:CallbackQuery):
    if not isinstance(cb.message,Message):
        await cb.answer("မှတ်တမ်းကို ဖွင့်မရတော့ပါ။",show_alert=True)
        return
    if cb.message.chat.type!="private":
        await cb.answer("Private Chat မှာသာ ဖတ်ရှုနိုင်ပါတယ်။",show_alert=True)
        return
    parts=(cb.data or "").split(":")
    try:
        if len(parts)!=3 or not parts[2].isdigit() or len(parts[2])>2:
            raise ValueError("Malformed page")
        info=library_page(parts[1],int(parts[2]))
    except ValueError:
        await cb.answer("ဤစာမျက်နှာ မရှိတော့ပါ။",show_alert=True)
        return
    await cb.answer()
    try:
        await cb.message.edit_text(render_library(info),
                                   reply_markup=reference_page_keyboard(info),
                                   parse_mode="HTML")
    except Exception:
        logging.warning("Reference library message edit unavailable; using private fallback")
        await cb.message.answer(render_library(info),
                                reply_markup=reference_page_keyboard(info),
                                parse_mode="HTML")


@dp.callback_query(F.data.startswith("ui:"))
async def native_navigation(cb: CallbackQuery):
    # Callback identifiers contain no birth data and are checked against
    # an explicit whitelist; unknown values receive only a short alert.
    data=cb.data or ""
    parts=data.split(":")
    text=None
    markup=None
    if not isinstance(cb.message, Message):
        await cb.answer("စာမျက်နှာကို ဖွင့်မရပါ။",show_alert=True)
        return
    # Navigation includes personal birth-date and chart routes; never expose
    # those controls in groups or let an old group callback bypass privacy.
    if cb.message.chat.type != "private":
        await cb.answer("ကိုယ်ပိုင်ဇာတာကို Private Chat မှာသာ ကြည့်ပါ။",show_alert=True)
        return
    if data=="ui:reading:start":
        if cb.from_user is None:
            await cb.answer("ဒီခလုတ်ကို ဖွင့်မရပါ။",show_alert=True)
            return
        await cb.answer()
        await start_private_reading_input(cb.message,cb.from_user.id)
        return
    elif data=="ui:reading:skip":
        if cb.from_user is None:
            await cb.answer("ဒီအဆင့် သက်တမ်းကုန်သွားပါပြီ။",show_alert=True)
            return
        try:
            born,clock=reading_inputs.finish_from_button(
                cb.message.chat.id,cb.from_user.id,cb.message.message_id)
        except (TypeError,ValueError):
            await cb.answer("ဒီခလုတ်က ဟောင်းနေပါပြီ။ မွေးချိန်ကို ပြန်ဖြည့်ပါ။",show_alert=True)
            return
        await cb.answer()
        await post_personal_reading(cb.message,personal_reading(born,clock))
        return
    elif data=="ui:library":
        text="<b>ကျမ်းကိုးမှတ်တမ်းများ</b>\n━━━━━━━━━━━━━━\nလေ့လာလိုသည့် ရိုးရာတွက်ချက်နည်းကို ရွေးပါ။"
        markup=reference_category_keyboard()
    elif data=="ui:home":
        text,markup=home_text(),home_keyboard()
    elif len(parts)==3 and parts[0]=="ui" and parts[1]=="category" and parts[2] in SECTIONS:
        text,markup=section_text(parts[2]),section_keyboard(parts[2])
    elif len(parts)==3 and parts[0]=="ui" and parts[1]=="feature" and parts[2] in FEATURES:
        text,markup=feature_text(parts[2]),feature_keyboard(parts[2])
    elif len(parts)==3 and parts[0]=="ui" and parts[1]=="guide" and parts[2] in COMMAND_GUIDES:
        if cb.message is None or cb.message.chat.type!="private":
            await cb.answer("ကိုယ်ရေးအချက်အလက်ကို Private Chat မှာသာ ဖြည့်ပါ။",show_alert=True)
            return
        text,markup=guide_text(parts[2]),guide_keyboard(parts[2])
    elif data=="ui:tarot":
        if cb.message is None or cb.message.chat.type!="private":
            await cb.answer("Tarot ကို Private Chat မှာ ဖွင့်ပါ။",show_alert=True)
            return
        await cb.answer()
        await open_tarot(cb.message,user_id=cb.from_user.id)
        return
    else:
        await cb.answer("ဤစာမျက်နှာ မရှိတော့ပါ။",show_alert=True)
        return
    await cb.answer()
    if cb.message is None:
        return
    try:
        await cb.message.edit_text(text,reply_markup=markup,parse_mode="HTML")
    except Exception:
        logging.warning("Cannot edit native navigation message; sending text fallback")
        await cb.message.answer(text,reply_markup=markup,parse_mode="HTML")


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
    if not isinstance(cb.message, Message):
        await cb.answer("တွက်ချက်မှုမှတ်တမ်း မရနိုင်တော့ပါ။",show_alert=True)
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

@dp.message(Command('daily'))
async def daily_command(message: Message):
    """Myanmar local calendar-day cultural reading, no birth data required."""
    if not private_only(message):
        await message.answer('နေ့စဉ်ပြက္ခဒိန်ကို Private Chat မှာသာ ကြည့်နိုင်ပါတယ်။')
        return
    args=(message.text or '').split()
    if len(args)>2:
        await message.answer('နေ့စဉ်ပြက္ခဒိန်ကြည့်ရန် <code>/daily</code> သို့မဟုတ် <code>/daily 2026-10-28</code> လို့ ဖြည့်ပါ။',parse_mode='HTML')
        return
    try:
        if len(args)==2:
            day=date.fromisoformat(args[1])
            if day.isoformat()!=args[1]:
                raise ValueError('Date format must be ISO')
        else:
            day=datetime.now(ZoneInfo('Asia/Yangon')).date()
        daily=daily_calendar_reading(day)
    except (ValueError, TypeError):
        await message.answer('ရက်စွဲကို YYYY-MM-DD ပုံစံဖြင့် 1900–2100 အတွင်း ပြန်စစ်ပါ။')
        return
    markers='၊ '.join(daily['active_labels']) if daily['active_labels'] else 'သီးခြားရိုးရာအမှတ်အသား မတွေ့ပါ။'
    observations='\n'.join(daily['observations'])
    await message.answer(
        '<b>မြန်မာရိုးရာ နေ့စဉ်ပြက္ခဒိန်</b>\n'
        '━━━━━━━━━━━━━━\n'
        f'ရက်စွဲ — <b>{html.escape(daily["date"])}</b> (မြန်မာစံတော်ချိန်အခြေခံ)\n'
        f'မြန်မာလ — <b>{html.escape(daily["myanmar_month"])}</b>\n'
        f'လ၏အဆင့် — <b>{html.escape(str(daily["moon_phase"]))}</b>\n\n'
        '<b>ရိုးရာနေ့အမှတ်အသားများ</b>\n'
        f'{html.escape(markers)}\n\n'
        f'{html.escape(observations)}\n\n'
        f'နဂါးခေါင်းလှည့်ရာ — {html.escape(daily["nagahle_direction"])}\n'
        f'နက္ခတ် — {html.escape(daily["nakhat_name"])}\n\n'
        f'{html.escape(daily["note"])}',
        parse_mode='HTML',
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='ပြက္ခဒိန်တွက်ချက်နည်း',
                  callback_data='evidence:'+daily['calculation_rule_id'])],
            [InlineKeyboardButton(text='နေ့စဉ်ဖော်ပြချက်နည်း',
                  callback_data='evidence:'+daily['interpretation_rule_id'])],
        ])
    )


@dp.message(Command('days'))
async def myanmar_day_signals_command(message: Message):
    if not private_only(message):
        await message.answer('မြန်မာနေ့ရက်အမှတ်အသားကို Private Chat မှာသာ တွက်ပေးနိုင်ပါတယ်။')
        return
    parts=(message.text or '').split()
    if len(parts)!=2:
        await message.answer('မြန်မာအခါပေးရက်များကို တွက်ကြည့်ရန် <code>/days 2024-01-01</code> လို့ ဖြည့်ပါ။',parse_mode='HTML')
        return
    try:
        day=date.fromisoformat(parts[1])
        signals=calculate_day_signals(day)
        description=describe_day_signals(signals)
    except (ValueError,TypeError):
        await message.answer('ရက်စွဲကို 1900–2100 အတွင်း YYYY-MM-DD ပုံစံနဲ့ ပြန်ဖြည့်ပါ။')
        return
    labels=description['active_labels']
    names='၊ '.join(labels) if labels else 'ဤနေ့တွင် သီးခြားအခါပေးရက်အမှတ်အသား မတွေ့ပါ။'
    await message.answer(
        'မြန်မာရိုးရာ အခါပေးရက်များ\n'
        '━━━━━━━━━━━━━━\n'
        f'ရက်စွဲ — <b>{html.escape(signals["date"])}</b>\n'
        f'မြန်မာလ — <b>{html.escape(signals["myanmar_month"])}</b>\n\n'
        '<b>ဤနေ့၏ ရိုးရာအမှတ်အသားများ</b>\n'
        f'{html.escape(names)}\n\n'
        f'နဂါးခေါင်းလှည့်ရာ — <b>{html.escape(description["nagahle_direction"])}</b>\n'
        f'နက္ခတ် — <b>{html.escape(description["nakhat_name"])}</b>\n\n'
        f'{html.escape(description["note"])}',
        parse_mode='HTML',
        reply_markup=evidence_button(description['rule_id'])
    )


async def start_private_reading_input(message: Message, user_id: int):
    reading_inputs.start(message.chat.id,user_id)
    await message.answer(
        '<b>မွေးဇာတာ အဆင့်ဆင့်ဖြည့်မယ်</b>\n'
        'မွေးရက်ကို YYYY-MM-DD ပုံစံဖြင့် ပို့ပါ။\n'
        'ဥပမာ <code>2005-12-23</code>\n\n'
        '၅ မိနစ်အတွင်း မဖြည့်ရင် အလိုအလျောက် ပိတ်မယ်။ '
        'ဖျက်ချင်ရင် /cancel လို့ ပို့ပါ။ '
        'မွေးအချက်အလက်ကို Database ထဲ မသိမ်းပါ။',
        parse_mode='HTML'
    )

async def post_personal_reading(message: Message, reading: dict):
    rule_buttons=InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='မဟာဘုတ်တွက်ချက်နည်း',
            callback_data='evidence:'+reading['evidence_rule_ids'][0])],
        [InlineKeyboardButton(text='ရိုးရာအိမ်အနက်',
            callback_data='evidence:'+reading['evidence_rule_ids'][1])],
        [InlineKeyboardButton(text='Life Path တွက်ချက်နည်း',
            callback_data='evidence:'+reading['evidence_rule_ids'][2])],
        [InlineKeyboardButton(text='Life Path ရိုးရာအနက်',
            callback_data='evidence:'+reading['evidence_rule_ids'][3])],
    ])
    await message.answer(
        '<b>ကိုယ်ပိုင်ရိုးရာဇာတာအနှစ်ချုပ်</b>\n'
        '━━━━━━━━━━━━━━\n'
        f'မွေးရက် — <b>{html.escape(reading["birth_date"])}</b>\n'
        f'မွေးနေ့နံ — <b>{html.escape(reading["weekday"])}</b>\n'
        f'မြန်မာသက္ကရာဇ် — <b>{reading["myanmar_year"]}</b>\n\n'
        '<b>မဟာဘုတ် ၇ အိမ်စနစ်</b>\n'
        f'ဖွားအိမ် — <b>{html.escape(reading["house"])}</b>\n'
        f'<b>{html.escape(reading["mahabote_theme"])}</b>\n'
        f'{html.escape(reading["mahabote_interpretation"])}\n\n'
        '<b>Numerology — Life Path</b>\n'
        f'သတ်မှတ်ထားသော ကိန်းလျှော့နည်းအရ — <b>{reading["life_path"]}</b>\n'
        f'<b>{html.escape(reading["life_path_theme"])}</b>\n'
        f'{html.escape(reading["life_path_interpretation"])}\n\n'
        'ရိုးရာစနစ်နှစ်ခုကို သီးခြားဖော်ပြထားခြင်းသာဖြစ်သည်။ '
        'အနာဂတ်ဖြစ်ရပ်ကို အာမခံမဟုတ်ပါ။ ဤ Command က မွေးအချက်အလက်ကို မသိမ်းပါ။',
        parse_mode='HTML', reply_markup=rule_buttons
    )


@dp.message(Command('reading'))
async def personal_reading_command(message: Message):
    if not private_only(message):
        await message.answer('ကိုယ်ပိုင်ဇာတာကို Private Chat မှာသာ ဖတ်နိုင်ပါတယ်။')
        return
    fields=(message.text or '').split()
    if len(fields)==1:
        if message.from_user is None:
            await message.answer("ကိုယ်ပိုင်ဇာတာ ဖြည့်စွက်မှုကို ဖွင့်မရပါ။")
            return
        await start_private_reading_input(message,message.from_user.id)
        return
    if len(fields) not in (2,3):
        await message.answer(
            'အဆင့်ဆင့်ဖြည့်ရန် /reading လို့ ရိုက်ပါ။ '
            'သို့မဟုတ် <code>/reading 2005-12-23 08:37</code> လို့ ဖြည့်နိုင်ပါတယ်။',
            parse_mode='HTML')
        return
    try:
        day=date.fromisoformat(fields[1])
        if day.isoformat()!=fields[1] or day>datetime.now(ZoneInfo('Asia/Yangon')).date():
            raise ValueError('Invalid birth day')
        clock=time.fromisoformat(fields[2]) if len(fields)==3 else None
        if clock and (clock.tzinfo is not None or len(fields[2])!=5):
            raise ValueError('Invalid local time')
        reading=personal_reading(day,clock)
    except (ValueError,TypeError):
        await message.answer('မွေးရက်စွဲကို 1900–2100 အတွင်း YYYY-MM-DD၊ မွေးချိန်ကို HH:MM ပုံစံဖြင့် ပြန်ဖြည့်ပါ။')
        return
    if message.from_user is not None:
        reading_inputs.cancel(message.chat.id,message.from_user.id)
    await post_personal_reading(message,reading)


@dp.message(Command('mahabote'))
async def mahabote_command(message: Message):
    if not private_only(message):
        await message.answer('မဟာဘုတ်မွေးဇာတာကို သီးသန့်စကားဝိုင်းမှာပဲ တွက်ပေးနိုင်ပါတယ်။')
        return
    parts=(message.text or '').split()
    if len(parts) not in (2,3):
        await message.answer(
            'မဟာဘုတ်ဇာတာတွက်ရန် မွေးရပ်ဒေသရဲ့ ရက်စွဲကို ဖြည့်ပါ။\n'
            '<code>/mahabote 1990-05-14</code>\n'
            'ဗုဒ္ဓဟူးမွန်းလွဲ ရာဟုခွဲရန် မွေးချိန်ထည့်နိုင်ပါတယ်။\n'
            '<code>/mahabote 2024-01-03 12:30</code>',
            parse_mode='HTML'
        )
        return
    try:
        local_date=date.fromisoformat(parts[1])
        if local_date>date.today():
            raise ValueError('future birth date')
        clock=time.fromisoformat(parts[2]) if len(parts)==3 else None
        chart=calculate_mahabote(local_date,clock)
        reading=interpret_mahabote(chart)
    except (TypeError,ValueError):
        await message.answer('မွေးရက်/မွေးချိန် မမှန်သေးပါ။ 1900–2100 အတွင်း YYYY-MM-DD နဲ့ HH:MM ပုံစံဖြည့်ပါ။')
        return
    placements='\n'.join(
        f'{BURMESE_HOUSES[h]} — {html.escape(info["weekday"])} ({html.escape(info["planet"])})'
        for h,info in chart['placements'].items()
    )
    method_markup=evidence_button(chart['evidence']['rule_id'])
    method_markup.inline_keyboard.append([
        InlineKeyboardButton(text='Interpretation Method',
                             callback_data='evidence:'+reading['interpretation_rule_id'])
    ])
    await message.answer(
        'မြန်မာမဟာဘုတ် — <b>မွေးဇာတာ ၇ အိမ်</b>\n'
        '━━━━━━━━━━━━━━\n'
        f'မြန်မာသက္ကရာဇ် — <b>{chart["myanmar_year"]}</b>\n'
        f'မွေးနေ့နံ — <b>{html.escape(chart["eight_day_weekday_label"])}</b>\n'
        f'မဟာဘုတ်အကြွင်း — <b>{chart["house_index"]}</b>\n'
        f'ဖွားအိမ် — <b>{html.escape(chart["house_burmese"])}</b>\n\n'
        '<b>အိမ် ၇ လုံး၏ ဂြိုဟ်နေရာချထားမှု</b>\n'
        f'{placements}\n\n'
        f'<b>{html.escape(reading["theme"])}</b>\n'
        f'{html.escape(reading["interpretation"])}\n\n'
        f'{html.escape(reading["disclaimer"])}',
        reply_markup=method_markup,
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
        reading_facts('myanmar_calendar',result)
        day_markers=calendar_marker_reading(result)
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
        '<b>ရိုးရာနေ့ရက်အနက်</b>\n'
        + '\n'.join(html.escape(item['text']) for item in day_markers['markers']) + '\n\n'
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
        if born.isoformat()!=parts[1] or not 1900<=born.year<=2100 or born>datetime.now(ZoneInfo('Asia/Yangon')).date():
            raise ValueError('invalid birth date')
        result=life_path(born)
        reading_facts('numerology',result)
        number_meaning=interpret_life_path(result)
    except ValueError:
        await message.answer('🌫️ မွေးနေ့ပုံစံ မမှန်သေးပါ။ YYYY-MM-DD အတိုင်း ပြန်ဖြည့်ပေးပါ။')
        return
    await message.answer(
        f'🔢 <b>သင့်ဘဝလမ်းကြောင်းကိန်း — {result["number"]}</b>\n'
        '━━━━━━━━━━━━━━\n'
        'Pythagorean-style ကိန်းဂဏန်းတွက်နည်းအရ ထွက်ပေါ်လာသည့်ရလဒ်ဖြစ်သည်။\n\n'
        f'📖 စည်းမျဉ်း: <code>{result["evidence"]["rule_id"]}</code>\n'
        f'<b>{html.escape(number_meaning["theme"])}</b>\n'
        f'{html.escape(number_meaning["interpretation"])}\n\n'
        'ဤအနက်မှာ ယနေ့ခေတ် Numerology ကျောင်း၏ ရိုးရာအမြင်သာဖြစ်ပြီး '
        'လူတစ်ဦး၏ အနာဂတ်ကို အဆုံးအဖြတ်မပေးပါ။',
        parse_mode='HTML', reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='တွက်ချက်နည်း',callback_data='evidence:'+result['evidence']['rule_id'])],
            [InlineKeyboardButton(text='ရိုးရာအနက်ကျမ်းကိုး',callback_data='evidence:'+number_meaning['interpretation_rule_id'])],
        ]),
    )

@dp.message(Command('natal'))
async def natal_preview_command(message: Message):
    """Optional operator-gated actual JPL natal calculation, never a fake chart."""
    if not private_only(message):
        await message.answer('Western မွေးဇာတာကို Private Chat မှာသာ တွက်နိုင်ပါတယ်။')
        return
    if os.environ.get('ENABLE_WESTERN_NATAL','').strip()!='1':
        await message.answer(
            'Western Natal Chart ကို Astronomical Benchmark စစ်ဆေးနေဆဲဖြစ်လို့ မဖွင့်ရသေးပါ။ '
            'Annual Profection ကိုတော့ သီးခြား Rising Sign နဲ့တွက်နိုင်ပါတယ်။ '
            '<code>/profection 2005-12-23 2026-10-27 Aries</code>',
            parse_mode='HTML'
        )
        return
    kernel=os.environ.get('JPL_EPHEMERIS_PATH','').strip()
    if not kernel or not os.path.isfile(kernel) or not kernel.lower().endswith('.bsp'):
        await message.answer('Western Natal အတွက် JPL Ephemeris မပြည့်စုံသေးပါ။ ဒီဇာတာကို အမှားသတင်းမပေးဘဲ ယာယီပိတ်ထားပါတယ်။')
        return
    args=(message.text or '').split()
    if len(args) not in (6,7) or (len(args)==7 and args[6] not in ("0","1")):
        await message.answer(
            '<b>Western Natal Development Preview</b>\n'
            '<code>/natal 2005-12-23 08:37 Asia/Yangon 16.85 96.15</code>\n'
            'မွေးရပ်ဒေသ၏ Timezone၊ Latitude၊ East-Positive Longitude ကို '
            'ကိုယ်တိုင် အတည်ပြုဖြည့်ပါ။ DST နှစ်ကြိမ်ဖြစ်သော နာရီအတွက် '
            'နောက်ဆုံး 0/1 Fold ကို ထပ်ထည့်ရမယ်။',
            parse_mode='HTML'
        )
        return
    try:
        birth=datetime.strptime(args[1]+' '+args[2],'%Y-%m-%d %H:%M')
        if birth.date()>date.today():
            raise ValueError('Future birth date')
        lat=float(args[4])
        lon=float(args[5])
        fold=int(args[6]) if len(args)==7 else None
        local_today=datetime.now(ZoneInfo(args[3])).date()
        record=assemble_natal(
            birth,args[3],lat,lon,kernel,evaluation_date=local_today,fold=fold
        )
        summary=render_natal_preview(record)
    except (ValueError,TypeError,KeyError,OSError,RuntimeError):
        await message.answer('Natal Preview ကို မတွက်နိုင်ပါ။ မွေးချိန်၊ Timezone၊ Coordinates နဲ့ Ephemeris ကို ပြန်စစ်ပါ။ မမှန်တဲ့ဇာတာ မပြပါ။')
        return
    methods=(
        ("Planetary Positions","WEST-TROPICAL-LONGITUDES-001"),
        ("Ascendant & Houses","WEST-ASC-WHOLE-SIGN-001"),
    )
    for _,key in methods:
        get_rule(key)
    markup=InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text=label,callback_data='evidence:'+key)
        for label,key in methods
    ]])
    await message.answer(summary,parse_mode='HTML',reply_markup=markup)


@dp.message(Command('profection'))
async def profection_command(message: Message):
    if not private_only(message):
        await message.answer('Annual Profection မွေးရက်တွက်ချက်မှုကို Private Chat မှာသာ ဖွင့်နိုင်ပါတယ်။')
        return
    fields=(message.text or '').split()
    if len(fields)!=4:
        await message.answer(
            '<b>Western Annual Profection</b>\n'
            '<code>/profection 2005-12-23 2026-10-27 Aries</code>\n\n'
            'မွေးနေ့၊ စစ်ဆေးလိုသည့်ရက်စွဲနဲ့ သီးခြား Natal Chart မှ '
            'အတည်ပြုထားသော Rising Sign ကို ဖြည့်ပါ။ '
            'ဤ Command က Ascendant ကို ကိုယ်တိုင်မတွက်ပါ။',
            parse_mode='HTML'
        )
        return
    try:
        born=date.fromisoformat(fields[1])
        target=date.fromisoformat(fields[2])
        if born>date.today():
            raise ValueError('Future birth date')
        rising=fields[3].strip().capitalize()
        result=profection_reading(born,target,rising)
    except (ValueError,TypeError):
        await message.answer('မွေးနေ့၊ စစ်ဆေးရက်နဲ့ Rising Sign (Aries ... Pisces) ကို ပြန်စစ်ပါ။')
        return
    await message.answer(
        '<b>Western Annual Profection</b>\n'
        '━━━━━━━━━━━━━━\n'
        f'အသက်ပြည့်နှစ် — <b>{result["age_completed"]}</b>\n'
        f'နှစ်တိုင်အိမ် — <b>{result["house"]}</b>\n'
        f'အသက်ဝင်ရာသီ — <b>{html.escape(result["sign"])}</b>\n'
        f'Lord of the Year — <b>{html.escape(result["lord_of_year"])}</b>\n'
        f'ရိုးရာအိမ်ဆိုင်ရာ သင်္ကေတ — {html.escape(result["house_topic_burmese"])}\n\n'
        f'Rising Sign: <code>{html.escape(result["rising_sign_input"])}</code> '
        '(အသုံးပြုသူပေးထားသည်၊ ဤနေရာတွင် မတွက်/မစစ်ရသေးပါ)\n'
        'ဤနှစ်တိုင်သည် ရိုးရာ အမျိုးအစားခွဲခြားချက်သာဖြစ်ပြီး '
        'အနာဂတ်ဖြစ်ရပ် အာမခံချက် မဟုတ်ပါ။',
        parse_mode='HTML',reply_markup=evidence_button(result['calculation_rule_id'])
    )


@dp.message(Command('dayun'))
async def dayun_command(message: Message):
    """Source-calculated optional ten-year BaZi cycles; private birth input."""
    if not private_only(message):
        await message.answer('Da Yun မွေးချိန်တွက်ချက်မှုကို Private Chat မှာသာ ဖွင့်နိုင်ပါတယ်။')
        return
    parts=(message.text or '').split()
    if len(parts) not in (5,6) or parts[4] not in ("0","1") or (len(parts)==6 and parts[5] not in ("1","2")):
        await message.answer(
            '<b>BaZi Da Yun — ၁၀ နှစ်စက်ဝန်း</b>\n'
            '<code>/dayun 2005-12-23 08:37 Asia/Yangon 1</code>\n\n'
            'မွေးရက်၊ မွေးချိန်၊ မွေးရပ်ဒေသ Timezone နဲ့ မူရင်းစနစ် Code ကို ရွေးပါ။\n'
            'Code 1 = ရိုးရာအမျိုးသားနည်း၊ Code 0 = ရိုးရာအမျိုးသမီးနည်း။ '
            'ဒီ Code သည် lunar-python ၏တွက်ချက်မှုရွေးချယ်စရာသာဖြစ်ပြီး '
            'သင့်ကိုယ်ပိုင်အမှတ်အသားကို အလိုအလျောက် မသတ်မှတ်ပါ။\n'
            'နောက်ဆုံးတွင် 1/2 ထည့်ပြီး Yun Sect ကို ရွေးနိုင်ပါတယ်။',
            parse_mode='HTML'
        )
        return
    try:
        birth=datetime.strptime(parts[1]+' '+parts[2],'%Y-%m-%d %H:%M')
        if birth.date()>date.today():
            raise ValueError('Future birth time')
        normalized=normalize_birth_wall_time(birth,parts[3])
        method_code=int(parts[4])
        yun_sect=int(parts[5]) if len(parts)==6 else 1
        result=calculate_bazi_luck(
            normalized['wall_time'],
            gender=method_code,
            yun_sect=yun_sect,
            day_sect=2,
            cycles=8,
            timezone_verified=normalized['timezone'],
        )
        reading=verified_dayun_reading(result)
    except (ValueError, TypeError, RuntimeError):
        await message.answer('မွေးရက်/မွေးချိန်၊ Timezone နဲ့ Code ကို ပြန်စစ်ပါ။ DST နာရီထပ်တဲ့ မွေးချိန်အတွက် အတည်ပြုချက် လိုအပ်ပါတယ်။')
        return
    decades='\n'.join(
        f'{p["index"]}. {p["gan_zhi"]} — {p["start_year"]}–{p["end_year"]} '
        f'(ရိုးရာအသက် {p["start_age_nominal"]}–{p["end_age_nominal"]})'
        for p in reading["periods"]
    )
    await message.answer(
        '<b>BaZi 大运 — ၁၀ နှစ်စက်ဝန်း</b>\n'
        '━━━━━━━━━━━━━━\n'
        f'စဉ်သွားပုံ — <b>{reading["direction"]} ({reading["direction_burmese"]})</b>\n'
        f'ပထမစတင်ရက် — <b>{reading["first_start_date_local"]}</b>\n'
        f'လက်ခံထားသော Timezone — <code>{html.escape(normalized["timezone"])}</code>\n'
        f'Yun Sect — {reading["yun_sect"]}\n\n'
        f'{html.escape(decades)}\n\n'
        'ဖော်ပြထားသောအသက်သည် East Asian nominal age ဖြစ်ပြီး '
        'မွေးနေ့ကျော်ပြီးသော အသက်အမှန်နှင့် မတူနိုင်ပါ။\n'
        f'{html.escape(reading["caution"])}',
        parse_mode='HTML',
        reply_markup=evidence_button(reading["rule_id"]),
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
        reading_facts('bazi',result)
        element_reading=bazi_element_reading(result)
        growth_reading=calculate_growth_stages(result)
        seasonal_reading=calculate_bazi_seasons(result)
    except (ValueError,RuntimeError):
        await message.answer('🌫️ မွေးချိန်ကို မတွက်နိုင်သေးပါ။ YYYY-MM-DD HH:MM Asia/Yangon ပုံစံနဲ့ မွေးရပ်ဒေသရဲ့ Timezone ကို စစ်ဆေးပါ။ DST နာရီနှစ်ခါဖြစ်တဲ့ ရက်တွေမှာ မွေးချိန်အတည်ပြုဖို့ လိုပါတယ်။')
        return
    p=result['pillars']
    visible=result['visible_wuxing']
    hidden=result['hidden_stems']['pillars']
    gods=result['ten_gods_all']['visible']
    gods_summary=' · '.join(f'{name}: {gods[name]["ten_god"]}' for name in ('year','month','day','hour'))
    hidden_summary=' · '.join(f'{k}: {"/".join(s["stem"] for s in hidden[k]["hidden"])}' for k in ('year','month','day','hour'))
    methods=(
        ("Four Pillars",result['evidence']['rule_id']),
        ("Five Elements","CHN-BAZI-VISIBLE-WUXING-001"),
        ("Hidden Stems","CHN-BAZI-HIDDEN-STEMS-001"),
        ("Ten Gods","CHN-BAZI-TENGODS-001"),
        ("Twelve Stages","CHN-BAZI-CHANGSHENG-001"),
        ("Seasons","CHN-BAZI-SEASON-MONTH-001"),
    )
    # The card uses distinct, compact native inline labels rather than five
    # identical "Calculation Method" buttons.
    for _,rule_id in methods:
        get_rule(rule_id)
    buttons=[
        InlineKeyboardButton(text=label,callback_data="evidence:"+rule_id)
        for label,rule_id in methods
    ]
    bazi_markup=InlineKeyboardMarkup(inline_keyboard=[
        buttons[0:2],buttons[2:4],buttons[4:6]
    ])
    balance=' · '.join(f'{name}: {count}' for name,count in visible['visible_counts'].items())
    growth_summary=' · '.join(f'{name}: {growth_reading["stages"][name]} ({growth_reading["burmese_stage_names"][name]})' for name in ('year','month','day','hour'))
    relations='\n'.join(f'{g["burmese_element"]} ({g["visible_count"]}) — {g["relationship_label"]}' for g in element_reading['groups'])
    season=seasonal_reading['month']
    meetings=', '.join(x['season'] for x in seasonal_reading['memberships']) or 'သီးခြား Branch သုံးလုံးပြည့် အုပ်စုမတွေ့ပါ'
    await message.answer(
        '🐉 <b>တရုတ်ဇာတာလေးတိုင်</b>\n━━━━━━━━━━━━━━\n'
        f'နှစ်တိုင် — <b>{html.escape(p["year"])}</b>\n'
        f'လတိုင် — <b>{html.escape(p["month"])}</b>\n'
        f'ရက်တိုင် — <b>{html.escape(p["day"])}</b>\n'
        f'နာရီတိုင် — <b>{html.escape(p["hour"])}</b>\n\n'
        f'🌿 မြင်ရသော အဓိကဓာတ် ၈ လုံး — {html.escape(balance)}\n'
        'ဤအရေအတွက်သည် Day Master အားကောင်း/အားနည်းခြင်းကို မဆုံးဖြတ်ပါ။\n\n'
        f'<b>Day Master</b> — {html.escape(element_reading["day_master"])} / {html.escape(element_reading["day_element_burmese"])} ({html.escape(element_reading["polarity_burmese"])})\n'
        '<b>ဓာတ်ငါးပါး ဆက်နွယ်မှု</b>\n'
        f'{html.escape(relations)}\n'
        'ဤဆက်နွယ်မှုများသည် ရိုးရာအမျိုးအစားခွဲခြားချက်များသာဖြစ်ပြီး ကံကြမ္မာခန့်မှန်းချက် မဟုတ်ပါ။\n\n'
        '<b>Solar-Term လတိုင်ရာသီ</b>\n'
        f'{html.escape(season["month_branch"])} — {html.escape(season["burmese"])} / {html.escape(season["name"])} ({html.escape(season["phase"])})\n'
        f'ရာသီ Branch သုံးလုံးအုပ်စု — {html.escape(meetings)}\n'
        'အုပ်စုဝင်ခြင်းသာဖြစ်ပြီး ဓာတ်အသွင်ပြောင်းခြင်းနှင့် Day Master အင်အားကို မဆုံးဖြတ်ပါ။\n\n'
        f'🍃 Hidden Stems — {html.escape(hidden_summary)}\n'
        'အဓိက/အရံဓာတ်အစဉ်သာ ဖြစ်ပြီး ရာသီအင်အား မတွက်ရသေးပါ။\n\n'
        f'☯️ Ten Gods — {html.escape(gods_summary)}\n'
        'ဤသည် ရိုးရာ ဆက်စပ်မှုအမျိုးအစားများသာဖြစ်သည်။\n\n'
        '<b>十二长生 — ရိုးရာအဆင့် ၁၂ မျိုး</b>\n'
        f'{html.escape(growth_summary)}\n'
        'ဤအဆင့်အမည်များသည် ကျန်းမာရေး သို့မဟုတ် အနာဂတ်ဖြစ်ရပ်ကို ခန့်မှန်းခြင်း မဟုတ်ပါ။\n\n'

        f'📖 <code>{result["evidence"]["rule_id"]}</code>\n'
        f'လက်ခံထားသော Timezone — <code>{html.escape(normalized["timezone"])}</code>\n'
        'True Solar Time မပြင်ရသေးသော စမ်းသပ်ဇာတာဖြစ်သည်။',
        parse_mode='HTML', reply_markup=bazi_markup
    )

def tarot_choice_keyboard(token: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text='Card I', callback_data=f'tarotpick:{token}:0'),
        InlineKeyboardButton(text='Card II', callback_data=f'tarotpick:{token}:1'),
        InlineKeyboardButton(text='Card III', callback_data=f'tarotpick:{token}:2'),
    ]])


async def open_tarot(message: Message, *, user_id: int):
    if message.chat.type != 'private':
        await message.answer('🌙 ကံကြမ္မာကတ်ရွေးဖို့ သီးသန့်ဇာတာခန်းကို ဝင်ခဲ့ပါ။')
        return
    # Ignore rapid repeated taps before allocating a session or sending media.
    # No extra Telegram message for denied attempts, so spam cannot create a
    # flood of 'slow down' notices either.
    if not tarot_cooldown.allow(message.chat.id,user_id):
        return
    token = tarot_sessions.start(owner_id=user_id, chat_id=message.chat.id)
    text = ('🃏 <b>ကတ်သုံးချပ်ထဲက တစ်ချပ်ရွေးပါ</b>\n'
            '━━━━━━━━━━━━━━\n'
            'ကြယ်စင်တို့၏ နိမိတ်ကို ဘယ်ကတ်က ဖော်ပြမလဲ…')
    media_id = tarot_delivery.asset(os.getenv('TAROT_SHUFFLE_FILE_ID', '').strip())
    if media_id:
        try:
            sent = await message.answer_animation(
                animation=media_id, caption=text, parse_mode='HTML',
                reply_markup=tarot_choice_keyboard(token)
            )
        except Exception:
            tarot_delivery.mark_failed(media_id)
            logging.warning('Configured Tarot animation unavailable; using text fallback')
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
    if isinstance(cb.message, Message):
        await open_tarot(cb.message, user_id=cb.from_user.id)


@dp.callback_query(F.data.startswith('tarotpick:'))
async def tarot_pick(cb: CallbackQuery):
    try:
        _, token, raw_choice = (cb.data or '').split(':', 2)
        choice = int(raw_choice)
    except (ValueError, TypeError):
        await cb.answer('🌫️ ကတ်ရွေးချယ်မှု မမှန်ပါ။', show_alert=True)
        return
    if not isinstance(cb.message, Message):
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
    meaning = interpret_tarot_card(card)
    tarot_markup=evidence_button('TAROT-DRAW-001')
    tarot_markup.inline_keyboard.extend(evidence_button('TAROT-INTERPRETATION-001').inline_keyboard)
    result_text = (
        '🃏 <b>သင့်ထံ ရောက်လာသောကတ်</b>\n━━━━━━━━━━━━━━\n'
        f'<b>{html.escape(card)}</b>\n\n'
        f'🌙 <b>{html.escape(meaning["theme"])}</b>\n'
        f'{html.escape(meaning["reflection"])}\n\n'
        'ဤသည် ရိုးရာ Tarot သင်္ကေတအခြေခံ စဉ်းစားစရာအနက်ဖြစ်ပြီး အနာဂတ်ကို အာမခံမဟုတ်ပါ။'
    )
    # Reuse one Telegram-hosted asset for every reveal; result name always comes
    # from the previously assigned session, not from media filenames.
    reveal_id = tarot_delivery.asset(os.getenv('TAROT_REVEAL_FILE_ID', '').strip())
    photo_id = None
    try:
        photo_id=tarot_delivery.photo(card,os.getenv('TAROT_CARD_PHOTOS_JSON','').strip())
    except (OSError,ValueError,UnicodeError):
        logging.warning('Tarot photo registry unavailable; using default reveal fallback')
    try:
        if photo_id:
            from aiogram.types import InputMediaPhoto
            await cb.message.edit_media(
                media=InputMediaPhoto(media=photo_id, caption=result_text, parse_mode='HTML'),
                reply_markup=tarot_markup
            )
        elif reveal_id:
            from aiogram.types import InputMediaAnimation
            await cb.message.edit_media(
                media=InputMediaAnimation(media=reveal_id, caption=result_text, parse_mode='HTML'),
                reply_markup=tarot_markup
            )
        elif cb.message.animation:
            # edit_caption reuses the same Telegram-hosted shuffle animation without reuploading
            await cb.message.edit_caption(caption=result_text, parse_mode='HTML',
                reply_markup=tarot_markup)
        else:
            await cb.message.edit_text(result_text, parse_mode='HTML',
                reply_markup=tarot_markup)
    except Exception:
        if reveal_id and not photo_id:
            tarot_delivery.mark_failed(reveal_id)
        logging.warning('Cannot edit Tarot card message; using safe reply fallback')
        if photo_id:
            try:
                await cb.message.answer_photo(
                    photo=photo_id, caption=result_text, parse_mode='HTML',
                    reply_markup=tarot_markup
                )
                return
            except Exception:
                tarot_delivery.mark_failed(photo_id)
                logging.warning('Tarot card photo unavailable; sending text-only result')
        await cb.message.answer(result_text, parse_mode='HTML',
            reply_markup=tarot_markup)


@dp.message(Command('cancel'))
async def cancel_private_reading(message: Message):
    if not private_only(message) or message.from_user is None:
        return
    if reading_inputs.cancel(message.chat.id,message.from_user.id):
        await message.answer("မွေးဇာတာဖြည့်စွက်မှုကို ပိတ်လိုက်ပါပြီ။ အချက်အလက် မသိမ်းထားပါ။")
    else:
        await message.answer("လက်ရှိဖွင့်ထားတဲ့ မွေးဇာတာဖြည့်စွက်မှု မရှိပါ။")

@dp.message(F.text)
async def private_reading_input_message(message: Message):
    if not private_only(message) or message.from_user is None:
        return
    if not message.text or message.text.startswith("/"):
        return
    user_id,chat_id=message.from_user.id,message.chat.id
    stage=reading_inputs.step(chat_id,user_id)
    if stage=="date":
        try:
            reading_inputs.set_date(chat_id,user_id,message.text,
                datetime.now(ZoneInfo("Asia/Yangon")).date())
        except ValueError:
            await message.answer("မွေးရက်ကို 1900–2100 အတွင်း YYYY-MM-DD ပုံစံဖြင့် ပြန်ဖြည့်ပါ။")
            return
        prompt=await message.answer(
            "<b>မွေးချိန် ထည့်ပါ</b>\n"
            "မွေးရပ်ဒေသ နာရီကို HH:MM ပုံစံဖြင့် ပို့ပါ။ "
            "ဥပမာ <code>08:37</code>\n"
            "မသိရင် အောက်ကခလုတ်ကို နှိပ်ပါ။\n"
            "၅ မိနစ်အတွင်း မဖြည့်ရင် ပိတ်သွားမယ်။",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
                InlineKeyboardButton(text="မွေးချိန် မသိပါ",
                                     callback_data="ui:reading:skip")
            ]])
        )
        reading_inputs.bind_prompt(chat_id,user_id,getattr(prompt,"message_id",None))
    elif stage=="time":
        try:
            day,clock=reading_inputs.finish(chat_id,user_id,message.text)
            reading=personal_reading(day,clock)
        except (ValueError,TypeError):
            await message.answer("မွေးချိန်ကို HH:MM ပုံစံဖြင့် ဖြည့်ပါ၊ မသိရင် ခလုတ်နှိပ်ပါ။")
            return
        await post_personal_reading(message,reading)


async def main():
    token=os.environ.get('TELEGRAM_BOT_TOKEN')
    if not token:
        raise SystemExit('Set TELEGRAM_BOT_TOKEN in your private environment')
    logging.basicConfig(level=logging.INFO)
    bot=Bot(token=token)
    await dp.start_polling(bot)

if __name__=='__main__':
    asyncio.run(main())

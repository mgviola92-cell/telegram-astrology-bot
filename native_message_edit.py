"""One edit per native Telegram navigation; avoid duplicate message spam.

Telegram's "message is not modified" is a normal response to tapping
the already-selected button. It must not trigger a fallback new message.
No persistence, polling, network client creation or user-data logging.
"""
from aiogram.exceptions import TelegramBadRequest

async def edit_or_reply(message, content, keyboard=None):
    """Edit the same message, fallback once only on actual edit failures.

    Returns: 'edited', 'unchanged', or 'fallback'. Caller already answered
    the callback; avoid creating extra Telegram popups or logs with private data.
    """
    try:
        await message.edit_text(content,reply_markup=keyboard,parse_mode="HTML")
        return "edited"
    except TelegramBadRequest as exc:
        if "message is not modified" in str(exc).lower():
            return "unchanged"
    except Exception:
        pass
    await message.answer(content,reply_markup=keyboard,parse_mode="HTML")
    return "fallback"

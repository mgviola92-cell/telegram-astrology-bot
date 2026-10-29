"""Telegram group administrator checks for settings changes.

Always ask Telegram for the actor's current group status; never trust
message text, forwarded messages, cached usernames, or callback payload.
Failure or anonymous sender => deny. No user IDs stored or logged.
"""
async def is_verified_group_admin(bot,chat_id,from_user,*,sender_chat=None):
    if (sender_chat is not None or from_user is None
            or type(getattr(from_user,"id",None)) is not int
            or from_user.id<=0 or type(chat_id) is not int or chat_id>=0
            or bot is None):
        return False
    try:
        member=await bot.get_chat_member(chat_id=chat_id,user_id=from_user.id)
    except Exception:
        # Telegram only guarantees other-user checks if the bot is itself
        # an admin. Fail closed if the API cannot verify.
        return False
    return str(getattr(member,"status","")) in ("creator","administrator")

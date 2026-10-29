# Group-safe Myanmar calendar /today — 2026-10-29

## Why
The existing /daily, /reading, /number and /savebirth commands remain
private-only where they are designed for that setting. Groups can request
only the non-personal Myanmar calendar facts through the new /today
command, without supplying a birth date, personal profile, or timezone.

Telegram group privacy mode: commands directed at the bot may be
delivered in groups. The backend also enforces privacy regardless of
the command scope displayed by Telegram clients.
https://core.telegram.org/bots/features
https://core.telegram.org/bots/api

## Public card
- /today is supported in private, group and supergroup chats.
- The date is the current calendar day in Asia/Yangon.
- The card shows Myanmar calendar month, lunar phase, Yan Naing Aye
  traditional day-marker labels, Nagahle direction and Nakhat name,
  with cultural non-prediction framing.
- Three stateless controls navigate near the current day, within three
  days backward/forward. The callback contains a public calendar date
  only. Every pressed callback rechecks the window relative to current
  Myanmar time; old callbacks do not expose user-specific data.
- Cached text content uses lru_cache(maxsize=32) in RAM, shared across
  all group requests for the same calendar date; no individual/user data
  is cached or written to a database.
- Group command requests are capped to one response per chat per 20
  seconds via GroupCalendarGate with at most 1024 RAM entries. No
  Telegram messages are sent for repeated requests within cooldown.
- Clicking a public day control edits the same Telegram message instead
  of posting a new message. No background auto-send or polling.

## Deferred / out of scope
- No auto-daily announcements or invisible group monitoring.
- No group-specific persisted settings or owner/admin panel yet.
  Future durable settings require a separately approved storage design.
- No promise of no bandwidth: a short Telegram API response is still
  needed when a member intentionally requests the result.
- No source evidence callback on the group card; private-only evidence
  library remains unchanged. No natal/reading result is ever shown
  in groups through this command.
- Not deployed or live tested on Telegram or Render.

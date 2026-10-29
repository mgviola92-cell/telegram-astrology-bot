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


## Native group landing menu

- /start and /help in group/supergroup now display a brief group-specific
  Burmese welcome card with **only** a public calendar inline button.
  The existing private home menu (birth/profile features) is NOT shown
  in groups; private /start remains unchanged.
- The group button edits that landing card into the same no-birth-data
  public Myanmar calendar, with bounded date-navigation callbacks.
- Group welcome commands use a separate 15-second per-chat, bounded
  1024-entry RAM gate to reduce repeated greetings. It does not poll,
  broadcast, store member identities or create a new DB.
- Channels receive no group landing. All Group Settings/admin policy
  toggles remain unimplemented and are not implied by this UI.


## Admin controls and storage (source commit e111287a)

- Group /settings opens an admin-only card, showing whether /today is
  available in THAT group. Group /start includes an admin-settings entry,
  but an ordinary member who presses it receives a callback denial.
- Permission is checked from Telegram getChatMember on EVERY settings
  action, not a cached role. Allowed statuses are creator/administrator.
  Failed API checks and anonymous sender messages are denied. For
  reliable checks, make the bot an admin as recommended by Telegram API.
- Admin may turn the on-demand calendar off or back on with native inline
  buttons. A stale toggle button cannot accidentally reverse the newer
  choice: expected-state compare-and-set handles that.
- Disabled groups: /today is silent, the public group calendar button
  refuses access, and callbacks on OLD public calendar cards are denied;
  private /today stays available. Group welcome hides its calendar entry.
- No auto-announcements, group-member collection, media or birth profiles.
  There is exactly one optional integer per-group override (only
  explicitly disabled groups require a persisted DB row).
- Default settings are stored in small process RAM and reset at restart.
  The group admin UI explicitly states this caveat. A disabled group may
  become enabled again after a reboot in memory-only mode. The memory
  storage has a fixed 1024-group cap and refuses new disables rather than
  silently discarding previously disabled groups.
- Opt-in durable storage: set GROUP_SETTINGS_DB_PATH on a genuine
  persistent filesystem. This is a SEPARATE tiny SQLite database from
  PROFILE_DB_PATH. Group settings rows store only chat ID and enabled
  bit, not names, individual members, private birth data or media.
  Updates write only on a real state change; default enabled costs
  no DB row. A 1024-entry RAM cache avoids repeated disk reads.
- On Render Free: NEVER configure SQLite durable settings on ephemeral
  local storage; GROUP_SETTINGS_PERSISTENT_DISK_CONFIRMED=1 requires
  a verified paid Render disk/mount, not a guess. This flag alone cannot
  prove that an actual disk is attached.
- One process only for now: multiple workers would need shared atomic
  compare-and-set storage and cache invalidation. No production deploy
  or real Telegram verification has occurred.
- Bot administration docs:
  https://core.telegram.org/bots/api#getchatmember
  https://docs.aiogram.dev/en/latest/api/methods/get_chat_member.html


## Seven-day public weekly calendar (/week)

- /week displays Monday through Sunday for the current Myanmar
  local week (Asia/Yangon), with each day's traditional labels,
  Myanmar month and moon phase from the already-verified day calculator.
- "ရှေ့တစ်ပတ်", "ဒီတစ်ပတ်", "နောက်တစ်ပတ်" native inline controls
  navigate only previous/current/next local week. An old callback is
  revalidated relative to the current date; no user input, birth date
  or group identifier is embedded in it.
- Existing /today and /week share the same 20-second per-group rate
  budget, rather than doubling the allowed traffic. Weekly reads are
  cached in eight short in-memory week cards (not an external DB).
- Disabled groups cannot use /week or reopen old week cards.
  Private /week remains available even if a group disabled its calendar.
- No auto-announcement, bulk horoscope, ranking, photo generation,
  extra dependency or persistent state is created by this feature.

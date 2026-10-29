# Resource and bandwidth budget — 2026-10-29

Development guardrails for the All-in-One Telegram Astrology Bot. These are
implementation constraints, not measured network usage or deployment proof.

## Database and memory

- By default, /reading, /daily, /number and calculation commands do not
  persist a birth date or result; they calculate the result in process.
- Temporary /reading inputs are in bounded per-user RAM sessions, with a
  five-minute deadline per step. The Tarot draw session has a ten-minute
  deadline. Neither needs database polling or a background keepalive.
- /savebirth explicitly requires the Burmese consent marker and enables
  at most one encrypted birth-profile row per Telegram user. Only encrypted
  payload, user ID and consent/update timestamps are persisted.
- /mybirth and /forgetbirth remain private-only. Deletion and older-record
  cleanup are available, but no automatic profile purging policy is imposed.
- SQLite opens connections for real profile operations only. WAL journal mode
  is established at store initialization, not on every short-lived read.
- No media bytes or raw images are stored in SQLite, GitHub or caches.
  Media manifest stores only reusable bot-specific Telegram file_id strings.

## Traffic controls

- Configured Telegram photo/animation file_id values are resent as IDs; there
  is NO bot-side media downloader or runtime upload step.
- Telegram file_id reuse avoids BOT-SIDE upload but does NOT mean zero
  Telegram API calls, zero end-user bandwidth or zero server egress.
- The Tarot JSON manifest is loaded once per path into RAM, at most two
  cached paths; operators restart the process to apply a manifest change.
- Failed media IDs are suppressed for the process lifetime (bounded at 80)
  instead of attempting the same broken file repeatedly.
- TAROT_MEDIA_MODE=telegram (default): use configured reusable Telegram
  IDs, otherwise fallback to text. TAROT_MEDIA_MODE=text: skip optional
  media. Unknown settings fail closed to text, and preflight rejects them.
- Rapid repeated Tarot requests are dropped before session generation or
  another media send, with a 3-second per user/chat cooldown in bounded RAM
  (max 1000 entries). Other users are unaffected.
- No scheduled external polling, filesystem image collection, cron keeps
  alive, or repeating database status checks are added.

## Render free and persistence warning

The implemented optional profile store is **encrypted SQLite**, NOT Neon
or an external Postgres service. Render Free web-service filesystems are
ephemeral, including local SQLite, and have no attachable persistent disk.
A restart, redeploy or spin-down can erase saved data.

The runtime and deploy preflight refuse configured Render SQLite profiles
without PROFILE_PERSISTENT_DISK_CONFIRMED=1. This flag must NOT be used on
Render Free. The flag is an operator declaration only; it cannot verify that
the mounted disk is real. For paid Render persistent-disk hosting, verify
the disk mount and path BEFORE setting it. For free hosting with lasting
profiles, a separate external encrypted database adapter could be built
later, with independent account/quota/bandwidth verification and user
authorization; that adapter is NOT implemented.

Official documentation:
- https://render.com/docs/free
- https://render.com/docs/disks
- https://core.telegram.org/bots/api#sending-files

## Not yet implemented

- External Neon/Postgres migration, quotas, production measurements or SLA.
- Distributed multi-worker sessions and distributed throttling.
- Full media licensing/artwork and Telegram live smoke tests.
- Secure deletion guarantees from backups, snapshots, or filesystem copies.
- Production monitoring, backups, recoverability and measured bandwidth.
- Render deployment. The owner must explicitly authorize it later.

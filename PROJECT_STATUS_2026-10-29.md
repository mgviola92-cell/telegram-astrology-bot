# Development status — 2026-10-29

Repository: mgviola92-cell/telegram-astrology-bot
Branch: main
Last verified source and test commit: a0e2b376c39c1c88ae834b071aa0303e1407e6b3
GitHub Actions: https://github.com/mgviola92-cell/telegram-astrology-bot/actions/runs/40840143670
Result: SUCCESS — 370 unittest tests, 5 skipped; compile and CI preflight succeeded.
This is NOT a real Telegram API / Render live-smoke result.

## Development changes carried over from the full October 28 handoff
- 24a962af: Fixed /daily escaped newline rendering, added sourced modern
  Life Path 1–9,11,22,33 original Burmese reflections and evidence keys.
  Personal /reading now presents separate Mahabote and Numerology themes.
- 94f047fa: Added Telegram /number privacy and invalid-argument tests;
  refreshed stale README, design and roadmap statements.
- a25a2c58: Added per-user/per-private-chat temporary reading form input
  with 300-second expiry per stage and bounded in-process sessions.
- c923e32f: Wired private native start/skip callbacks, /reading with no
  arguments, HH:MM input, /cancel and shared personal-reading response.
- daaffdd8: Added offline end-to-end reading-form tests for validation,
  invalid input, group exclusion, cancel and no birth dates in callbacks.
- a0e2b376: Corrected existing test fixtures and native callback
  validation; all 370 tests succeeded (5 skipped).
All changes above are in main and ARE NOT DEPLOYED.

## Hard constraints retained
1. All-in-one native Telegram experience, no WebApp/Mini App.
2. Myanmar calendar/Mahabote, Western tropical/Hellenistic, Chinese BaZi
   with Chinese Da Yun, Numerology and Tarot; no Vedic/Jyotish/Dasha.
3. Source/algorithm-based calculations, separate and attributed
   school-specific interpretations, no invented predictions or guaranteed
   personal outcomes. Tarot draw random, meaning source-reviewed.
4. Never show private birth details in groups or callback identifiers.
   Birth profiles require explicit owner opt-in and encrypted persistent
   storage; ordinary /daily, /number, /reading do NOT save.
5. No image binary in DB, only optional Telegram file_id media.
6. Western natal preview stays OFF until independent benchmark/security
   checks and explicit owner release decision. No silent JPL downloads.
7. No Render deploy or production/live Telegram API claim until the owner
   approves controlled smoke checks and later deployment explicitly.

## Next engineering batches
- Improve error handling after Telegram API send failures, multi-worker
  session strategy, input-flow integration with other traditions.
- Build larger authentic evidence-reviewed Myanmar, Chinese and Western
  interpretive material without cross-school fabricated synthesis.
- Finish original-source research, professional review and complete
  licensed Tarot art / file_id assets; harden group/owner settings.
- Security/privacy audit, opt-in profile storage deletion/backup review,
  operational logging and rate limits, independent ephemeris benchmark,
  approved live Telegram smoke.
- Render deployment remains a separate explicit permission gate.

README and RESEARCH_VALIDATION_GATE.md contain detailed foundations.
Earlier PROJECT_STATUS_2026-10-27.md is historical, not a launch claim.

## Resource controls added on October 29

- c169d9d0: set SQLite WAL mode once and guard unconfirmed ephemeral
  Render profile storage with runtime and preflight checks.
- bc31f6c2: cache the Telegram Tarot media manifest in RAM, suppress
  repeated bad assets, allow text-only mode without media upload.
- 63e18af0: bound repeated Tarot requests with 3-second RAM cooldown.
- See RESOURCE_BUDGET_2026-10-29.md. No Render deploy or live Telegram
  verification; the resource budget is policy, not measured network usage.


## Additional native reading / learning sprint

- 861a9cc1: Bind private birth-time skip callback to its precise
  Telegram prompt message, rejecting old prompts after a new session.
- f830d5da: Implement source-checked Burmese Astrology Study chapters
  for Myanmar calendar, Mahabote, BaZi, Western, Life Path and Tarot.
  They use in-memory/static text only and are private-only.
- db481361: Add shared native edit-in-place helper that ignores
  Telegram's "message is not modified" response, protecting navigation
  against duplicate fallback messages. Private-only evidence callbacks.
- Corrected test helper in the following commit; inspect GitHub Actions
  tied to final HEAD for verified test counts. These are offline tests,
  not live Telegram API verification. No deployment was performed.


## Opt-in group calendar feature

- fb15b4ac: Group-safe /today command with local Myanmar date,
  cached short culturally grounded calendar facts, bounded per-chat
  cooldown and stateless interactive nearby-day navigation.
- Details in GROUP_CALENDAR_2026-10-29.md, including no auto-posts,
  no birth input, and no new database storage.
- Telegram live behavior remains unverified pending owner approval.


## Group-native landing verification

- 0fa40ddc: Group public calendar command/callback offline regression
  and source-aware documentation; GitHub Actions 40843473146: SUCCESS,
  414 tests run, five skipped.
- 409e3326: Group-only /start and /help menu, public calendar inline
  button, separate bounded RAM welcome throttle, 7 added smoke tests;
  GitHub Actions 40843708079: SUCCESS, 421 tests run, five skipped.
- Earlier user-private /start menu and private-only birth commands were
  preserved. No automatic group posts and no database/media persistence.
- The latest documentation-only commit should also pass CI; inspect its
  own Actions run before treating these figures as latest HEAD status.


## October 29 group-admin implementation

- 3f7e1ef3: Low-write group setting registry; RAM-only mode supports
  a bounded temporary disabled-set and cannot silently evict disabled
  groups. Optional separate SQLite DB persists only the disabled
  group ID and state (no user/member or birth data). CI success.
- d422d400: /settings and group:settings inline controls; current
  Telegram creator/admin verification, strict per-group isolation and
  old callback denial. Disabled groups are blocked from all /today
  and older calendar card paths. Live group admin checks still untested.
- e111287a: Added offline end-to-end authorization, old-button,
  group-disable and persistence preflight regression tests, plus
  current aiogram enum compatibility. GitHub Actions 40849268832:
  SUCCESS, 441 tests run, 5 skipped.
- This documentation update also isolates group SQLite from profile
  SQLite using a deploy-preflight check. Use the *final* GitHub Actions
  run for the definitive latest test count. No Render deploy, no live
  Telegram API test. Admin rights checks are not supported in offline
  CI without mocks.


## October 29 weekly calendar sprint

- 02a3231b: New non-personal, source-backed Monday–Sunday /week text
  for private/enabled group chats, seven dates in one Telegram card.
  Current/previous/next week buttons revalidate local Myanmar time;
  no calendar lucky-day rankings or invented divination.
- 7fc13d90: Telegram callback/privacy tests, group default menu
  week button and updated source/resource documentation. GitHub Actions
  40850346925: SUCCESS — 458 tests run, 5 skipped.
- This follow-up: group /today now checks Admin disable before processing
  invalid arguments; group /settings text explicitly covers both
  /today and /week, and outdated documentation claims were corrected.
- Tiny weekly RAM LRU (8 cards) and existing per-group rate budget
  avoid extra DB writes, seven-message dumps, and redundant group traffic.
- Verify the final HEAD Actions run separately. No Render deploy or
  real Telegram live test was authorized or performed.


## Mahabote seven-house reading expansion

- 02fc9e1a: Added dedicated seven-house Burmese report builder with
  independent source-evidence/chart revalidation, distinctive Burmese
  weekday-planet names, one highlighted birth-house interpretation,
  six house-name/meaning glossary entries, Rahu-vs-7-house caveat,
  and hard Telegram message-size cap.
- /mahabote now uses the new renderer and canonical local YYYY-MM-DD
  / optional HH:MM input validation. Its two source/method buttons
  are preserved, without storing birth data in callback IDs or DB.
- Existing numeric house-index and seven planetary placements are
  unchanged; expanded editorial labels do NOT claim 7 planet forecasts
  or scientifically verified future outcomes.
- Offline regression suite plus GitHub Actions are required before
  considering this implementation validated. No Render deployment or
  live Telegram API check was performed.


## Eight-weekday cultural reference

- c7805155: A distinct, tested Myanmar 8-day animal/direction
  correspondence table, cross-checked against existing myanmar_birth_day
  calculation and researched cultural reference materials.
- Private /myday now displays its derived symbol and direction, with
  a second source-method button. Invalid birth clock formats and dates
  are rejected, and the cutoff/source variation is communicated.
- This remains a cultural symbolic lookup, NOT eight new personal
  fate formulas, and no birth data is written to DB.


## BaZi Ten Gods interpretive source sprint

- 24fbe951: Evidence-rechecked ten-role and five-family Burmese
  educational reading adapter. Verifies Day Master, three other visible
  stems and all branch hidden relationships against original pillars.
- Private /bazi now includes the meanings with a separate linked source
  ID and without DOB/time in callbacks; /study Bazi adds same provenance.
- This does not fabricate Day Master strength, favorable elements or
  fortunes. Offline CI must be checked for final commit.


## October 29 Western profection educational expansion

- fedae856: Added 12 distinct Burmese traditional Whole Sign house topic
  descriptions, all-sign and 12/24-age cycle regressions, strict
  original birth-date/rising-sign provenance revalidation and compact
  Telegram-safe source-aware report output.
- New /profection houses private study mode shows the full unpersonalized
  12-house vocabulary. Standard /profection adds one selected house's
  interpretation and next house/sign/ruler cycle reference.
- Two separate source buttons distinguish mathematical annual profection
  from educational house-topic symbolism. No natal chart or independent
  Rising Sign calculation. No storage, media, background traffic or
  Render deployment. Check final HEAD GitHub Actions results.


## Leap-day annual profection audit

- Completed-year engine retained; February 29 birthdays use March 1 in
  non-leap evaluation years, and February 29 in leap years.
- Added calendar-boundary regression tests and an explicit convention
  disclaimer on applicable private /profection cards. No personal
  data persistence or natal feature activation.

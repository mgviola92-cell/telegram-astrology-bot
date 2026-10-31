# All-in-One Telegram Astrology Bot — Development

Myanmar-first Telegram bot, with traditional-source-aware calculations and natural Burmese UI. **Vedic/Jyotish is excluded.**

## Current status — 2026-10-29

This is a working **development-stage aiogram Telegram bot**, with native
message and inline-keyboard handlers. It is **not deployed**, has no real
Telegram smoke test yet, and must not be represented as production-ready.
Older dated research milestones below are historical notes, not the current
deployment or implementation status.

### Implemented with offline tests
- Myanmar calendar based on Yan Naing Aye's MIT mmcal formulas; 16
  traditional calendar-day markers; weekday and Wednesday Rahu labels;
  seven-house Mahabote with separate Burmese symbolic interpretation.
- Private /daily, using Myanmar local date or explicit date, with
  genuinely rendered newlines (not backslash-n text).
- Private /reading: distinct Mahabote and Life Path sections; no
  invented cross-tradition synthesis or implicit birth-data storage.
  The native menu and argument-free /reading now start a two-step
  private birth-date/optional-clock form, with 5-minute per-step expiry,
  cancellation and a no-clock skip button. The old direct command remains.
- Numerology /number: Life Path arithmetic plus 12 sourced modern
  school-specific Burmese symbolic themes (1–9, 11, 22, 33).
  Details: NUMEROLOGY_INTERPRETATION_SOURCES.md.
- BaZi Four Pillars, Five Elements, hidden stems, Ten Gods, growth stages,
  seasonal information and configurable Chinese Da Yun cycles.
- Western whole-sign Annual Profections with supplied Rising Sign;
  Skyfield/JPL natal preview exists but is OFF by default and not
  independently release-validated.
- 78 Tarot cards, Burmese short reflections, user/message-bound
  single-use private sessions, optional Telegram file_id animations
  and per-card photo mapping; full art assets are not configured.
- Six short source-linked native Astrology Study chapters, private-only,
  stateless and text-only; editing existing cards minimizes chat spam.
- Native Reference Library and source callbacks, encrypted opt-in
  SQLite birth profiles; no automatic profile saving and no birth data
  in callback payloads.

### Group calendar settings (administrators)

Group /settings shows the current on/off state of the public Myanmar
calendar. Only verified Telegram group admins may change it. When
disabled, /today and previously published group calendar buttons are
blocked; private /today is unchanged. Settings default to temporary
RAM (restart can reset them); optional tiny durable SQLite is separate
from birth profiles and needs a genuinely persistent disk. No automatic
group announcements, media storage or background DB polling. See
[group settings design](GROUP_CALENDAR_2026-10-29.md).

### Group-safe /start and /today

Group /start and /help now present a public-only group menu with a
button to view the non-personal Myanmar calendar. Group landing and
today command have separate RAM-only command cooldowns. Private /start
continues to show the personal/astrology navigation.

### Group-safe daily Myanmar calendar

Group members can request /today to see a short, **public/non-personal**
Myanmar calendar card with stateless nearby-day controls. A bounded
in-memory result cache and per-group command cooldown avoid repeated
computation and chat spam. /daily and all private birth readings remain
private-only. No automatic daily group messages and no DB writes; read
[group calendar design](GROUP_CALENDAR_2026-10-29.md).

### Resource and database savings

The default calculations do not persist personal data. Optional encrypted
SQLite birth profiles require opt-in, never run on Render Free's ephemeral
local filesystem, and use no background polling. Tarot uses reusable
Telegram file IDs (rather than bot-side uploads), cached media manifest,
text-only configuration and bounded anti-repeat cooldown. See the
[resource and hosting guardrails](RESOURCE_BUDGET_2026-10-29.md).

### Not yet complete
Deep multi-tradition personal readings, consent-respecting compatibility,
full Study content, group and owner settings, complete Tarot art,
production privacy/backup/operational hardening, independent natal
benchmark acceptance, and explicit-authorized Render deployment.

**Exclusions:** Vedic/Jyotish/Kundli/Dasha, Mini Apps, database image
blobs, deterministic guarantees of future outcomes, production deployment
without owner permission.

## Run locally (not deployed)
Use Python 3.12+.

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
```

Set `TELEGRAM_BOT_TOKEN` **in private environment variables only**, then:

```bash
python bot.py
```

**Do not paste your token into chat, commit it, or add it to the repository.**

## Important limitations

Offline CI success is not equivalent to a verified Telegram or Render
deployment. Astrology interpretations are school-specific cultural
symbolism, not validated scientific predictions. Western natal source
and legal gates, historical timezone edge cases, complete media
licensing, multi-worker Tarot sessions, secret hygiene, backups, logging
and rate limits still require release work. Do not commit secrets or
private birth-profile data. No Render deploy without owner approval.

## Research checkpoint (2026-10-24)
- Myanmar calendar candidate: [Yan Naing Aye mmcal](https://github.com/yan9a/mmcal), MIT; original implementation primarily JS/C++; the audited Python port is in `myanmar_calendar.py`.
- Chinese BaZi reference vector: [lunar-python upstream test](https://github.com/6tail/lunar-python/blob/master/test/EightCharTest.py), 2005-12-23 08:37 → 乙酉 / 戊子 / 辛巳 / 壬辰.
- Western Swiss Ephemeris is **not installed**: [Astrodienst licensing](https://www.astro.com/swisseph/sweph_e.htm) requires AGPL compliance or a commercial license before public activation; no license decision yet.
- CI is configured in GitHub Actions, but its actual pass/fail state must be checked before any readiness claim.

## Native Tarot reveal flow (implemented in code; media assets pending)
- `/tarot` in a private chat starts a three-facedown-choice session.
- The selected card is securely sampled from the 78-card deck, held only in bounded in-memory state.
- Session expires after 10 minutes, single-use choice, verifies Telegram user/chat/message, rejects stale presses.
- Optional environment variables `TAROT_SHUFFLE_FILE_ID` and `TAROT_REVEAL_FILE_ID` enable Telegram-hosted reusable animation assets. When unset or an animation send fails, clean text fallback remains available.
- `file_id` is bot-specific. Do **not** paste public URLs or unrelated bots' file IDs expecting them to work.
- No media binary blobs, raw card art or user birth data stored in database. Animated assets have **not** been uploaded or generated yet.
- Single-process in-memory session is for development only; multiple worker processes require a shared atomic TTL session store to avoid lost state and race conditions.
- Separate card artwork for each actual card and traditional card-meaning corpus are still pending. The current generic flip animation must not imply that a different card was drawn.

Research: [Telegram Bot API: sending by file_id and editing messages](https://core.telegram.org/bots/api), [aiogram editMessageMedia](https://docs.aiogram.dev/en/latest/api/methods/edit_message_media.html).

## Myanmar calendar research milestone
The new `myanmar_calendar.py` port follows [Yan Naing Aye's mmcal MIT implementation](https://github.com/yan9a/mmcal) (copyright 2018 Yan Naing Aye); no unrelated unverified year offset is used. A January 1, 2024 reference and full-leap-year iteration were checked locally. Cross-language exhaustive verification and more original sample dates remain release blockers; **do not claim complete validation**. `/mmcal YYYY-MM-DD` displays computed Myanmar year, month, day, Mahabote, Yatyaza and Pyathada, with rule-provenance button. Full professional predictions remain pending.

## Latest calculation progress (2026-10-25)
- `western_aspects.py`: classical five major aspects computed from **externally verified** tropical longitudes, with explicit 0/60/90/120/180° angle targets and documented configurable orb tolerances. Geometric engine is unit-tested locally; this is not a birth-position engine and must not receive guessed planetary degrees. Source: https://www.astro.com/astrology/in_aspect_e.htm
- `myanmar_calendar.py`: moon phase, lunar fortnight day and month-length logic adapted from the original MIT mmcal `cal_mp`, `cal_mf`, `cal_mml` formulas. Bot `/mmcal` now displays Burmese waxing/waning information.
- Research limitations remain: actual Western ephemeris/ascendant, Myanmar historical cross-validation, Chinese BaZi solar-time validation, full traditional interpretation corpus, complete Telegram UX, images and production DB.
- CI checks still require verification on GitHub Actions. Deployment remains deferred.

## Western natal astronomy milestone
- `western_chart.py` accepts a timezone-aware birth instant and an **already available** JPL SPK .bsp ephemeris; it computes geocentric apparent tropical ecliptic longitudes for Sun, Moon and major planets (outer entries clearly marked as barycenters) using Skyfield, then applies sign and aspect geometry.
- `tests/test_western_chart.py` checks twelve 30-degree boundaries, aspects, missing ephemeris, naive birth time and nonfinite coordinates. These are source-level tests, not a published complete birth-chart benchmark.
- `skyfield>=1.50,<2` is an astronomy dependency. The binary ephemeris is deliberately not included in Git and is **not fetched at runtime**. A locally installed JPL kernel, valid for the requested date, is required.
- Rising sign, local coordinates, twelve houses and published-reference planetary ephemeris fixtures remain unimplemented/unverified. This is NOT yet a full natal horoscope.
- Skyfield reference: https://rhodesmill.org/skyfield/coordinates.html and https://rhodesmill.org/skyfield/planets.html

## Whole Sign Houses prototype
`western_houses.py` computes an eastern-horizon tropical Rising Sign and twelve Whole Sign Houses from an **aware birth instant and supplied latitude/longitude**, using Meeus mean sidereal time/obliquity. Local deterministic tests cover J2000, quarter-circle geometry, boundaries, timezone equivalence and range rejection. Mean-equinoctial convention only: no nutation, horizon refraction, independent published ascendant benchmark or high-latitude support yet. **Not production validated; not hooked into user-facing bot.**

## Natal pipeline (development only)
`natal_pipeline.assemble_natal(...)` now connects IANA timezone/DST and birth-location validation, mean-sidereal Rising Sign/Whole Sign Houses, externally supplied JPL ephemeris positions and aspects, and age-based annual profections. It does **not** expose private birth details in Telegram yet. A test-only injected astronomy provider can verify orchestration without downloading a kernel. Local birth **date** is used for age and profections, never an earlier UTC calendar date. **Research limitation:** Skyfield uses true ecliptic/equinox of date, while houses currently use a mean GMST/obliquity convention; reconcile and independently cross-check before public natal readings. No release readiness claim.

## Opt-in encrypted birth profiles (development; not deployed)
- `profile_store.py` stores only ciphertext, consent/update timestamps and a numeric user ID in local SQLite; encryption uses `cryptography.Fernet`. No media BLOBs, tokens or plaintext birth details in tables.
- `profile_commands.py`: private-only `/savebirth YYYY-MM-DD အတည်ပြု` to explicitly consent, `/mybirth` to view, and `/forgetbirth` to delete. Nothing is saved automatically by `/bazi`, `/number`, or `/myday`.
- Disabled until `PROFILE_DB_PATH` points to a protected persistent disk file and `PROFILE_ENCRYPTION_KEY` is injected via a secret manager. **Never commit the key**. Losing the key prevents profile recovery.
- Generate a key only within the private deployment's own environment (not chat/GitHub), protect backup copies, and restrict filesystem access. Plan encryption-key rotation, database backups, expiry policies, and multi-instance migrations before production.
- SQLite record removal does not automatically delete previously created backups; provide retention/deletion policy covering backups.
- Additional privacy/consent tests are committed, but full CI passing status remains unverified.
- `natal_pipeline.py` now validates that returned zodiac labels match exact longitudes, preventing contradictory natal cards.

## Profile storage integrity checkpoint — 2026-10-25
- SQLite transaction wrapper now explicitly rolls back if an operation raises an error. Python reference: https://docs.python.org/3/library/sqlite3.html#how-to-use-the-connection-context-manager
- Save rejects invalid/future/noncanonical birth dates, nonfinite/out-of-range latitudes and longitudes, and invalid HH:MM strings.
- Birth-profile save consent parser now requires exactly the intended command marker; unrelated text does not grant consent.
- `ProfileStore(db, new_key, old_keys=[prior_key])` can read old ciphertext and `rotate_encrypted_profiles()` re-encrypts all records with the new primary key in one SQL transaction. Rotate with secure backups and a carefully managed old-key overlap. It does NOT retroactively re-encrypt previously stored backups or guarantee physical erasure of deleted SQLite pages.
- Review the new tests for rollback, key rotation and validation. **Not production-certified:** end-to-end tests, CI result, crash/recovery, disk permissions, concurrency and backup retention still pending.
- Research: https://cryptography.io/en/stable/fernet/ (MultiFernet).

## BaZi hidden stems
`bazi_hidden_stems.py` adapts the documented `lunar-python` `ZHI_HIDE_GAN` table and validates every sexagenary pillar. Four branch hidden-stem sets appear in `/bazi` with their own source button. Direct comparison tests use the upstream `getYearHideGan`, `getMonthHideGan`, `getDayHideGan` and `getTimeHideGan` methods. The lookup does not infer favorable elements or Day Master strength; independent solar-time, sector boundaries and interpretation work remain. Development stage; not deployed.

## BaZi Da Yun (development only)
The new `bazi_luck.py` uses the documented `lunar-python` EightChar -> Yun -> DaYun chain for start dates, forward/reverse direction and conventional ten-year Ganzhi cycles. The 0/1 gender mapping is the upstream library's traditional rule, is supplied explicitly, and can be skipped; it is never inferred from name/profile. The Yun calculation sect (1 or 2) is supplied explicitly and the output carries source assumptions. Ages are **traditional nominal ages** as returned by the library. This is not yet presented by the Telegram bot or validated with the live installed library in this environment; no automatic public predictions are derived from the periods.

## BaZi Ten Gods progress
`bazi_ten_gods.py` computes traditional Ten Gods labels for every visible Heavenly Stem and each hidden branch stem, relative to the day's stem. It uses an explicit Five-Phase/Yin-Yang relationship rule and includes a test against the 100-entry `6tail/lunar-python` `LunarUtil.SHI_SHEN` lookup. The native `/bazi` response shows only the four visible labels to stay concise, but records all hidden labels in the backend with separate evidence. This is structural correspondence, not a personalized predictive reading; CI is not yet verified.

## Environment bootstrap and safe preflight
Python 3.12+ recommended. Install the four declared libraries with `python -m pip install -r requirements.txt`. Source-mode readiness: `python preflight.py --mode ci`, then `python -m unittest discover -s tests -v`. To inspect deployment readiness when secrets have been supplied privately: `python preflight.py --mode deploy`. Diagnostics print **only check names and static descriptions**, not tokens, encryption keys, profile contents or ephemeris data.
`.env.example` is a template. The bot requires `TELEGRAM_BOT_TOKEN`; encrypted profile persistence additionally requires both `PROFILE_DB_PATH` and `PROFILE_ENCRYPTION_KEY`. Real natal coordinates require a local existing kernel, documented via `JPL_EPHEMERIS_PATH` (not yet automatically wired into the public bot UI). Animation assets use Telegram `file_id` values. CI deliberately does **not** require production secrets or .bsp files. Package availability, actual lunar-python / Skyfield math, persistent DB and secret injection must be verified on a real release host.

## 2026-10-25 preflight readiness corrections
- Tarot shuffle/reveal animation file IDs are **optional**. Missing assets select the native text fallback in `bot.py`; `preflight.py --mode deploy` now reports this state without incorrectly failing.
- The current Western natal pipeline is not a public bot command. A local JPL kernel is therefore not mandatory for the presently exposed bot functions. Deployment preflight requires `JPL_EPHEMERIS_PATH` only if `ENABLE_WESTERN_NATAL=1`. This flag is a **readiness gate only**, not a Telegram feature toggle.
- In contrast, any **explicit nonempty** JPL kernel path that does not exist fails configuration validation. Integration tests and kernel content/date coverage still require independent checks.
- Welcome text now accurately explains that opt-in `/savebirth` can store encrypted profiles when configured; other calculation commands never silently save birth dates.
- The corresponding automated tests are committed; a passing full GitHub Actions run still has not been verified.

## Burmese tarot reflection coverage (development)
`tarot_meanings.py` now covers the entire 78-card standard Tarot deck: 22 individually authored Major Arcana reflections and 56 Minor Arcana meanings composed from suit-specific themes and rank-specific prompts. `bot.py` connects these to the native Tarot reveal and has source/limitation buttons. They are prompts for reflection, not predictions. Card images and art rights are **not** ready yet; Telegram file_id animation fallback is unchanged. `tests/test_tarot_meanings.py` enforces full coverage. Complete GitHub CI has not been confirmed as passing.

## Tarot photo manifest and callback hardening
- `TAROT_CARD_PHOTOS_JSON` optionally points to a local JSON mapping such as `{"The Star":"<Telegram photo file_id>"}`. Do not commit actual credentials. Only exact card names from the existing 78-card deck are accepted. No binary media in SQLite.
- `tarot_media.py` validates JSON keys, file IDs, 64KB size limit, prevents URL/path substitutions, and reports coverage. `bot.py` uses per-card photo ID when configured; otherwise falls back to shared animation or plain Telegram text. It also attempts `answer_photo` if changing an existing text message into photo media fails.
- `tarot_sessions.py` now enforces single message binding, expiry on bind, strict index/identifier types and collision-resistant token generation. Tests exercise replay, expiration and incorrect ownership.
- This is only the integration layer; copyrighted artwork licensing, 78 suitable art assets, Telegram uploads and collecting the resulting `file_id` values are still outstanding. CI, actual Telegram API media editing and production assets have not been verified.

## Clean native UI baseline (2026-10-26)
- Navigation labels intentionally contain **no decorative emojis**. The Myanmar discipline button is `မြန်မာဗေဒင်`; international discipline buttons are `Western Astrology`, `BaZi`, `Numerology`, and `Tarot`. Secondary labels use short English names such as `My Profile`, `Compatibility`, and `Daily Reading`.
- Central `native_ui.py` defines main menu, three category menus, feature submenus, command guides, and Back/Home callbacks. `bot.py` now uses those menus for `/start` and `/help` and handles `ui:...` buttons. Existing calculation commands and their separate evidence callbacks are preserved.
- Only **already implemented** calculations link to command-entry guides; Tarot opens the current session flow. Incomplete features show a clear development description, not fabricated calculation results. Birth-date entry guides are private-only and do not store data automatically.
- The layout uses actual Telegram `InlineKeyboardMarkup` and `InlineKeyboardButton` primitives; no custom backgrounds, fonts, widget tabs, gradient cards or Mini App are claimed. The Telegram client chooses final button shape/colors.
- `tests/test_native_ui.py` covers callback byte limits, navigable targets, Back/Home, button labels, and unavailable-feature behavior. Actual Telegram mobile/desktop rendering, full CI and bot deployment remain unverified.

## 2026-10-26 CI unblock and public-menu safeguard
Read the actual GitHub Actions runner logs for `Calculation tests` run 40351480931 (174 tests; five fixture errors after successful dependency installs, syntax and preflight). Fixed four missing `seconds=0` arguments in upstream `Solar.fromYmdHms` tests and one invalid test-only Telegram owner ID of zero. These fixes retain production validation and do not alter planetary calculations. A subsequent fully green workflow run remains to be confirmed.
The public `More` menu no longer exposes the unimplemented `Owner Controls` item. An owner-only authenticated dashboard must be implemented before enabling owner UI; no security based solely on hiding a menu item is claimed.

## Primary-source Myanmar Mahabote and day-marker batch (2026-10-27)

**New native private commands**:
- `/mahabote 1990-05-14` — date-only seven-house birth chart; optional local time `/mahabote 2024-01-03 12:30` labels Wednesday afternoon Rahu separately, without changing the seven-house arithmetic.
- `/days 2024-01-01` — source-based traditional calendar day categories, Sabbath and eve, Yatyaza/Pyathada, Nagahle direction and Nakhat. Neither command stores date inputs in a profile or callback.

**Calculation modules**:
- `mahabote_core.py` calculates the full seven-house placement by inverting `(my-wd)%7`, where `wd` is Saturday=0 through Friday=6; Myanmar year comes from the actual `mmcal` date conversion.
- `mahabote_reading.py` contains seven original Burmese symbolic descriptions, explicitly separated from mathematical evidence as school-variable **editorial interpretation**; no specific personal future-event predictions.
- `myanmar_day_signals.py` calculates 16 day-marker fields according to the Yan Naing Aye tables. Its declared handling treats First Waso as Waso and Late Tagu/Kason as Tagu/Kason in monthly lookup conventions. These month variants require independent calendar-school confirmation before release.
- `myanmar_signal_reading.py` recomputes date evidence before revealing Burmese labels.
- The Evidence UI documents two separate Mahabote rule IDs (calculation vs. symbolic reading) and one day-marker formula family.

**Primary references**:
- Yan Naing Aye, [Myanmar Astrological Calendar Days (2013)](https://cool-emerald.blogspot.com/2013/12/myanmar-astrological-calendar-days.html) and [original Burmese edition](https://coolemerald.blogspot.com/2013/12/blog-post.html).
- Yan Naing Aye, [mmcal MIT library](https://github.com/yan9a/mmcal). Its [C++ cedate regression](https://github.com/yan9a/mmcal/blob/master/cpp/test/cedate/cedate.cpp) documents 2024-01-01 as Myanmar year 1385, Nadaw day 20, Monday, Marana, Nagahle south, and no active astrological days. This is checked in new tests.
- Independently published worked [Mahabote example 1990-05-14 → Myanmar year 1352, Monday, Puti](https://horo.kesta.store/academy/myanmar/mahabote-calculation?lang=en).

**New test modules**: `tests/test_mahabote_core.py`, `tests/test_myanmar_day_signals.py`, `tests/test_myanmar_signal_reading.py`. They check fixed source vectors, all seven-house positions, Rahu noon boundaries, multi-year weekday tables and forged result/evidence rejection.

**Status**: Development only. Tests have been committed, but the latest full GitHub Actions green state and Telegram live tests remain unconfirmed; no Render deployment or claim of scientifically reliable future prediction.

## 2026-10-27 implementation sprint — newly usable methods and gated Western Natal

**New private commands**
- `/dayun 2005-12-23 08:37 Asia/Yangon 1` — 8 upstream lunar-python BaZi ten-year cycles with explicit required method code 0/1, optional Yun sect 1/2. Years are East Asian nominal ages, NOT guaranteed predictions. Does not infer the code from profile data.
- `/profection 2005-12-23 2026-10-27 Aries` — independently checked classical Hellenistic annual time lord, Whole Sign house, sign and traditional ruling planet from a **separately known** Ascendant sign. The bot does NOT calculate/verify the Ascendant for this command.
- `/natal 2005-12-23 08:37 Asia/Yangon 16.85 96.15` — **disabled by default**. Only available when an operator explicitly sets `ENABLE_WESTERN_NATAL=1` and points `JPL_EPHEMERIS_PATH` to an already available .bsp ephemeris. The command accepts no guessed location or default timezone, rejects invalid coordinates and ambiguous DST wall-times without an explicit fold argument, never downloads a kernel, and labels results as an unverified *development preview* until independent chart comparisons are complete. It is not promoted on the main menu.

**Better BaZi natal details**
- `bazi_seasons.py`: verifies the Jie solar-term Month Branch, identifies all 12 branch-to-season associations, checks strictly complete three-branch `sanhui` seasonal memberships, and explicitly does **not** claim transformation, Day Master Strength, favorable element, or future outcomes.
- `dayun_reading.py`: recalculates upstream decade years and verifies direction independently from the birth-year stem polarity and the user-supplied method code before displaying any periods.
- `bot.py`: presents seasonal groups in the native `/bazi` result and gives each calculation its own evidence button, without bringing other bots or Mini Apps into the UI.

**Western validation**
- `tests/test_western_astronomy_benchmarks.py`: NASA/JPL / US Naval Observatory Meeus J2000 GMST (280.46061837°), mean obliquity, equatorial ascendant quadrants, twelve whole-sign houses and annual-profection 12-year repetition.
- `profection_reading.py` and tests check all twelve Ascendants across two full cycles, birthday transitions, and seven classical rulers.
- `natal_render.py` produces escaped bounded Telegram HTML for already assembled charts with strong provisional status and calculation provenance requirements.
- `tests/test_bot_natal_command.py` uses a **mock-only** ephemeris fixture; this never claims that a genuine NASA JPL .bsp file has been independently validated.

**References**
- 6tail, `lunar-python` Yun and DaYun source: https://github.com/6tail/lunar-python/blob/master/lunar_python/eightchar/Yun.py and https://github.com/6tail/lunar-python/blob/master/lunar_python/eightchar/DaYun.py .
- Four BaZi seasons / branches: https://www.amfengshui.com/wp-content/uploads/2014/09/as101.pdf and https://clarifyhk.com/learn/bazi/stem-branch-relations/directional-meeting-conditions .
- Hellenistic Annual Profections: Chris Brennan at https://www.astro.com/astrology/tma_article190314_e.htm .
- USNO approximate sidereal time: https://aa.usno.navy.mil/faq/GAST ; NASA JPL GMST: https://spsweb.fltops.jpl.nasa.gov/portaldataops/mpg/MPG_Docs/MPG%20Book/Release/Chapter2-TimeScales.pdf .

**Validation and release**: After the larger sprint, GitHub Actions run https://github.com/mgviola92-cell/telegram-astrology-bot/actions/runs/40447759422 reported **300 Python tests passed**, including offline command smoke tests. Live Telegram and authentic JPL full-chart benchmark tests remain outstanding. No Render deployment was performed.


## Seven-day Myanmar calendar (/week, development)

Private chats and enabled groups can request /week to view
Monday–Sunday Myanmar traditional lunar/date markers. The output is
generated from the same documented daily_calendar_reading algorithm
as /today, with no new astrological rules or fabricated lucky/unlucky
day rankings. Groups have a separate native "တစ်ပတ်စာ ပြက္ခဒိန်"
button. Inline controls navigate current/previous/next week; callbacks
expire outside the current ±1 week window.

The weekly text is limited to 4096 characters and cached in a tiny
8-entry in-process LRU. A group /week shares the existing per-group
20-second command cooldown with /today. It also obeys the existing
group admin /settings toggle, including old inline callbacks.
No new DB tables, auto-posts, image downloads or per-user state.


## Seven-house Myanmar Mahabote expanded reading

Native private /mahabote now renders **all seven houses** with their
verified Gregorian→Myanmar year / weekday placements and Burmese
weekday-planet labels. The birth house alone receives the complete
original symbolic interpretation; the other six are explicitly a
house-name glossary, not personalized predictions inferred from each
planet. Wednesday afternoon Rahu remains a separate eight-day
weekday label (never an eighth house). Birth times require canonical
HH:MM local civil format; date input uses the current Yangon calendar
date for the future-date guard.

The renderer rechecks source-calculation integrity against the original
birth-date evidence before emitting the Telegram report (max 4096
characters). Existing evidence buttons still distinguish mathematical
house calculation and interpretive school convention. No data storage,
new API, subscription, file download or background processing.


## Myanmar eight-weekday birth-sign reference

Private /myday now includes the traditional eight-category animal
and pagoda-direction associations alongside the verified weekday/planet
calculation (Sunday Garuda, Monday tiger, Tuesday lion, Wednesday AM
tusked elephant, Wednesday PM Rahu/tuskless elephant, Thursday rat,
Friday guinea pig and Saturday naga). The additional method button
explains the cultural lookup and references; it is explicitly separate
from the seven-house Mahabote arithmetic.

This bot chooses noon local civil time as its Wednesday/Rahu boundary.
Some Burmese historical writings instead describe an evening cutoff,
so the app states its chosen convention rather than claiming there is
one indisputable national rule. No birth data is automatically stored
and no animal symbol is presented as a guaranteed personality or fate.


## BaZi Ten Gods relationship reading

Private /bazi now adds source-grounded Burmese labels to the
computed Ten Gods for Year, Month and Hour Heavenly Stems relative to
the Day Stem (Day Master). There are seven evidence buttons, including
a distinct Ten Gods interpretive source apart from the calculation.
Five dynamically calculated five-phase relations are presented:
Peer, Output, Wealth, Authority and Resource.

Individual Ten Gods names follow lunar-python LunarUtil.SHI_SHEN and
Yin/Yang polarity. Hidden Stems are unweighted; seasonal strength and
favorable/unfavorable elements are not inferred. Roles are not
literal predictions of money, employment, illness or relationships.
The verified natal input is recomputed before deriving the labels.
No new DB, birth-detail callback, media, or external API.


## Western Annual Profection 12-house interpretation

Private /profection now shows its verified activated Whole Sign house,
traditional Lord of the Year and one source-attributed original Burmese
summary of the house's cultural topic (12 distinct topics). The report
also displays the *next* house/sign/ruler after the coming birthday as
an educational 12-year cycle illustration, not a specific future event.
The rising sign is still **user-provided**; its astronomical validity
is NOT checked by this command. Birth dates and evaluation dates are
accepted only in canonical YYYY-MM-DD form within the supported period.

Private /profection houses displays a static 12-house glossary
without requiring or saving birth details. The Western native menu
links to that command. Separate evidence buttons cover the calculation
and the editorial interpretation, with source limits shown.
Natal planet conditions, sect, transits, solar returns and ephemeris
are not inferred. /natal stays gated. No database writes or background
network requests.


Leap-day profection policy: if born on February 29, a non-leap
calendar year counts the annual profection birthday on **March 1**.
This follows the underlying completed-year calendar comparison and is
explicitly shown on the personal /profection response. The Feb 28
alternative is a school-specific convention not silently assumed.


## Compatibility: traditional Chinese Branch pairs (first functional slice)

A private, stateless /compat command is available with one native
two-step 12-animal inline picker or the direct non-personal form
/compat 子 丑. This compares **explicitly selected** Chinese Earthly
Branches against the traditional Six Harmonies (六合), Six Clashes
(六冲), and membership of Three Harmonies (三合) groups. A partial
two-of-three group match is never presented as a completed triple.

- All 144 ordered pairs are covered in tests, with symmetric results.
- The native Compatibility section now opens the picker directly;
  callback data carries only public zodiac characters, no DOB or ID.
- There is no birth-year inference (especially not near Li Chun),
  Day Master strength, partner score, "perfect match", personal
  relationship forecast, new database or API request.
- **Full two-person natal compatibility is STILL NOT COMPLETE**:
  this is a reference table for users who already know their branch
  symbols from a sourced chart. Source explanations are available
  through the existing evidence registry.


## Startup preflight and operator release protection

The polling entrypoint now invokes preflight.deploy before any Telegram
network operation. A missing dependency, token format, unsafe ephemeral
storage or invalid optional configured Tarot manifest/asset causes
startup to fail without logging secrets. It does not prove the remote
token is valid or that any persistent disk is truly durable.

Unreleased Western natal needs BOTH ENABLE_WESTERN_NATAL=1 and
WESTERN_NATAL_REVIEW_APPROVED=1, plus the existing JPL kernel check.
Leave both OFF until independent benchmarks and owner's approval.

TAROT_CARD_PHOTOS_JSON is the filesystem path to a JSON **file**, not
a pasted inline JSON object. A partial mapping may be used, with a
coverage warning and text fallback. All 78 complete matching
licensed arts remain outstanding.


## Deploy on Render Web Service (2026-10-30)

- GitHub repository: mgviola92-cell/telegram-astrology-bot, branch main,
  root directory blank, native Python runtime.
- Build: pip install -r requirements.txt
- Start: python bot.py
- Health check path: /healthz
- Python version: .python-version in the repository pins 3.12 family,
  matching GitHub CI; no special PYTHON_VERSION env override needed.
- Required Render secret env vars: TELEGRAM_BOT_TOKEN (BotFather) and
  TELEGRAM_WEBHOOK_SECRET (unique random >=32 ASCII characters
  [A-Za-z0-9_-]). Do not commit these or send them in chats.
- Recommended first test env: TAROT_MEDIA_MODE=text,
  ENABLE_WESTERN_NATAL=0, WESTERN_NATAL_REVIEW_APPROVED=0.
  Leave PROFILE_DB_PATH, PROFILE_ENCRYPTION_KEY,
  GROUP_SETTINGS_DB_PATH and JPL_EPHEMERIS_PATH unset for the
  first stateless trial. No paid persistent disk is present on Free.
- Render itself provides RENDER_EXTERNAL_URL and PORT; do not invent
  or manually add them. With a valid Render external origin the bot
  automatically registers https://YOUR-SERVICE.onrender.com/telegram/webhook,
  validates Telegram's secret token header, opens 0.0.0.0:PORT and serves
  GET /healthz. Local instances without this origin use polling.
- Only ONE instance of the bot token should run. Webhook and polling
  must never run simultaneously on different hosts for the same bot.
- On Render Free, inbound inactivity for 15 minutes spins the service
  down. A new webhook HTTP request may wake it, but cold start and
  retry delay mean no guarantee of instant message handling, 24/7
  availability or delivery; use a paid always-on service if needed.
- Webhook source changes are not evidence of a successful live
  Telegram smoke check. Inspect Render Deploy logs and real bot
  commands after deployment, then audit errors. Do not enable natal
  simply to make the demo feature-complete.


## Durable Neon storage for Render Free

A dedicated optional Neon PostgreSQL backend supports explicit-consent,
Fernet-encrypted birth dates (only a minimal encrypted byte string, user
ID, update and consent timestamps) and one tiny boolean record per
disabled group calendar. Database tables are provisioned by an operator;
no migrations run on every webhook or import.

Set ASTROLOGY_DATABASE_URL in the **Render private environment**, with
sslmode=require, together with PROFILE_ENCRYPTION_KEY (Fernet 32-byte
URL-safe base64 key). No secret is stored in GitHub. Neon takes precedence
over SQLite, and the combination is disallowed. A valid Fernet key must
be safely backed up by the service owner; losing it makes previously
saved profiles unreadable. No user profile is stored unless an authorized
private /savebirth command has the explicit Burmese consent marker.

On Neon outage, group public calendar is disabled fail-closed rather than
bypassing a prior admin setting. Short-lived database connections are
opened only for explicit profile actions or group settings cache misses
and changes. No background polling, cron, images, media or bulk imports.


## BaZi natal pillar pairs

The private /bazi report detects six fixed 六冲 branch opposites, six 六合 branch pairings and five 五合 visible stem pairings among the four natal pillars. This does not infer transformation or life events. The existing separate static Earthly Branch compatibility reference is unchanged.


BaZi pair report rendering now validates relationship records, pillar order, pair membership and adjacent positions to reject malformed or injected Telegram HTML. The live /bazi command calls the chart-verified formatter, rechecking source birth-time calculations before rendering. These checks do not independently authenticate a user-supplied birth record.

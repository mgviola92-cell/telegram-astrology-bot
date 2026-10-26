# Research validation and release gate

Scope frozen: Myanmar astrology, Western natal/timing, Chinese BaZi, numerology, Tarot, evidence-based traditional interpretation, private/group native Telegram and efficient animated visuals. **No Vedic, Mini App, or Render at this stage.**

## Verified sources and decisions
- Myanmar: Yan Naing Aye's `mmcal` MIT JS/C++ reference (https://github.com/yan9a/mmcal). Do not fake Myanmar dates by subtracting a constant from Gregorian years. Python formula port integrated with limited regression fixtures; independent, broader cross-language verification remains outstanding.
- Independent Myanmar comparator: `chanmratekoko/mmcalendar` is a **Java** library with astrology markers and Myanmar Standard Time convention, not a Python package (https://github.com/chanmratekoko/mmcalendar). Compare only dates with equivalent calendar conventions.
- BaZi: `6tail/lunar-python`, upstream fixture 2005-12-23 08:37 -> 乙酉 戊子 辛巳 壬辰 (https://github.com/6tail/lunar-python/blob/master/test/EightCharTest.py). Need sect, location, true solar time and Li Chun boundary review.
- Western: Skyfield supports astronomy/ecliptic positions and local sidereal time (https://rhodesmill.org/skyfield/toc.html). Skyfield local-kernel geocentric planet position adapter and mean-sidereal ascendant/Whole Sign Houses prototypes are coded; live kernel fixtures and independent ascendant benchmarks remain unverified.
- Swiss Ephemeris requires AGPL compliance or paid professional license (https://www.astro.com/swisseph/). No unlicensed incorporation.
- Numerology: master number and transliteration choices require explicit school conventions.
- Tarot: random card **draw**, not random fabricated prediction. Reviewed card meanings, matched art and animated assets are pending.

## Current software
- Traditional weekday, Gregorian-to-Myanmar calendar/mmcal formula port, Birth IANA timezone & DST fold/gap validator, BaZi Four Pillars adapter, numerology and annual profection prototype.
- Telegram private UI, three-choice tarot with owner/single-use/TTL checks, optional Telegram cached animation file IDs.
- Rule explanations for calculation *methods*; professional prediction rule corpus does **not** exist yet.
- Tests are authored; GitHub Actions result must be checked before claiming full test pass.

## Release criteria: ALL required before user's first end-to-end trial
- [ ] Myanmar calendar and Mahabote/Yatyaza/Pyathada: Python adaptation written; historical edge-year, New Year, Waso and independent cross-language reference coverage still needed
- [ ] Western natal: Skyfield local-kernel tropical longitudes and aspect geometry implemented; must verify JPL-kernel fixtures and independent ascendant/Whole Sign Houses references, including sign-boundary and latitude/date edge cases
- [ ] BaZi time convention and historical timezone/longitude/solar correction decisions with benchmark tests
- [ ] Traditional rule corpus with reviewer-approved citations/conditions and no invented interpretation
- [ ] Tarot 78 correctly associated artworks + full documented interpretations + real native Telegram media assets
- [ ] Profiles, consent, deletion, privacy, group/admin and cache/quota safeguards
- [ ] Approved personal, daily/calendar, compatibility and other scoped UI flows
- [ ] CI, edge cases, security review, rate limits, media fidelity and integrated end-to-end tests
- [ ] Release candidate review; **only then** user acceptance testing and later Render

## Data and bandwidth rules
No photos, MP4s, GIFs, full birth records in file blobs. Cache Telegram file IDs and store only minimal consented records. Requests and recipient data still have nonzero bandwidth. One in-memory Tarot session is not multi-worker safe. No claim of zero cost.

This document tracks actual completed versus pending work. No features added beyond agreed scope.

## Calculation milestone 2026-10-25
- Myanmar moon phase / fortnight display ported from mmcal and regression cases authored. Historical cross-validation remains release-blocking.
- Western aspect angle geometry and configurable orb policy completed, with unit tests and provenance. Actual natal ephemeris, ascendant, tropical longitudes and school-specific timing need further work.
- No new agreed feature scope, no Render, no Mini App, no Vedic.

## 2026-10-25 Western houses checkpoint
- New `western_houses.py` computes UT Julian Day, Meeus Greenwich **mean** sidereal time, mean obliquity, eastern-horizon ascendant, and Whole Sign Houses from **explicit** geographic latitude/longitude. It does not fabricate a location or birth time.
- Ten self-contained geometric/date unit tests pass locally, after fixing a 360° floating-point wrap edge case. This is **not** independent chart validation.
- Current geographic latitude guard is -65° to +65°: high-latitude horizons are not claimed supported; the whole-sign procedure is not Placidus and applies no refraction/nutation correction.
- Cross-check against known Western chart datasets and integrate JPL ephemeris/natal aspects only after verifiable reference vectors.
- Formula research: https://en.wikipedia.org/wiki/Ascendant ; mean obliquity: https://www2.mps.mpg.de/homes/fraenz/systems/systems3art/node3.html

## 2026-10-25 Natal pipeline integration checkpoint
- `natal_pipeline.py` now combines IANA birth-time/DST validation, the existing mean-sidereal ascendant and Whole Sign Houses engine, existing Skyfield ecliptic planets/aspects, and annual profections in one provisional record.
- Development test seam injects deterministic planetary fixtures without acquiring a JPL kernel or sending any Telegram birth data. Tests cover valid Myanmar timezone, UTC-vs-local birth-day rollover, DST fall-back, DST gaps, invalid coordinates/kernel path, twelve houses and rejected provider results.
- `Skyfield ecliptic_frame` is explicitly the **true** ecliptic/equinox of date, while current `western_houses.py` uses a **mean** GMST/obliquity approximation. Research confirmed that distinction: https://rhodesmill.org/skyfield/api-framelib.html. Align conventions and independently benchmark chart outputs before any forecast is exposed.
- No JPL SPK kernel is bundled, and no real-kernel astronomy integration test has passed yet.
- No user-facing `/natal` command until reference-data comparison, provenance, group/privacy review and final release criteria are done.

## 2026-10-25 Privacy and chart-integrity work
- `profile_store.py` added: explicit opt-in only, application-layer Fernet encryption, SQLite persistence of Telegram numeric user ID, ciphertext and timestamps; update, personal deletion and retention cutoff supported.
- `profile_commands.py` adds private-only `/savebirth YYYY-MM-DD အတည်ပြု`, `/mybirth`, and `/forgetbirth`. Feature stays disabled unless both `PROFILE_DB_PATH` and `PROFILE_ENCRYPTION_KEY` are set. Existing reading commands do not silently save personal birth data.
- `tests/test_profile_store.py` and `tests/test_profile_commands.py` cover consent, encrypted bytes, wrong key, rejection of unexpected fields, user deletion and date validation. These are authored test cases; the full CI suite has not been verified as passing.
- `natal_pipeline.py` now rejects inconsistent longitude/zodiac sign combinations and nonfinite or missing longitudes; new test fixtures cover them.
- Encryption at rest is **not** a substitute for filesystem access controls, secure backup/rotation, limited logging, user data expiry, and safe production deployment. SQLite deletion does not by itself guarantee erasure from existing backups.
- No photo/animation binaries saved in profile database. Media uses Telegram-hosted `file_id` references.
- The expected release remains **blocked** by independent astronomy fixtures, rule interpretations, fully reviewed Telegram group/privacy flows, operational security and CI.

## 2026-10-25 Profile integrity research and implementation
- Explicit SQLite transaction rollback added for failures; regression test verifies aborted delete does not remove a birth record.
- Consent parser now matches only `/savebirth`, not unrelated command prefixes.
- Before encryption, canonical birth dates, bounds and finite numeric coordinates are checked.
- MultiFernet key rotation is implemented as a single database transaction using a primary key and prior decryption keys, with failure/rollback tests.
- Research verified: https://docs.python.org/3/library/sqlite3.html#how-to-use-the-connection-context-manager and https://cryptography.io/en/stable/fernet/
- Operational release blockers: secret manager provision, secure key backup, retention policy, WAL backups, restore drills, failed startup behavior and **passing CI**.

## BaZi five-phase calculation checkpoint
- The primary elements for all eight visible Heavenly Stem / Earthly Branch characters are counted by `bazi_elements.py`, with a separate evidence button.
- The reference pillars 乙酉 戊子 辛巳 壬辰 give Wood 1, Fire 1, Earth 2, Metal 2, Water 2. Reference links: https://www.ibiblio.org/chinesehistory/contents/08fea/c06s02.htm and https://uaya.org/iching/correspondences/.
- This is not hidden-stem weighting or seasonal Day Master strength. More rule research and CI verification are required before release.

## BaZi hidden-stems checkpoint
- Implemented source-ordered 12-branch hidden stem lookup in `bazi_hidden_stems.py`, using upstream `6tail/lunar-python` `LunarUtil.ZHI_HIDE_GAN` values; standalone tests and direct comparison to each `EightChar.get*HideGan()` are committed.
- Calculation is integrated into `bazi_core.py`; native `/bazi` now displays year/month/day/hour hidden stems with a provenance button.
- This is a deterministic branch lookup, **not** a weighted elemental strength calculation or a future prediction. Seasonal qi, month command, true solar time, sect transitions and Luck Pillars still require reviewed convention and reference tests.
- Reference: https://github.com/6tail/lunar-python/blob/master/lunar_python/EightChar.py

## 2026-10-25 Da Yun research checkpoint
- Source verified: `6tail/lunar-python` EightChar.getYun(gender, sect), Yun.getDaYun(), DaYun period start/end and GanZhi progression. Sources: https://github.com/6tail/lunar-python/blob/master/lunar_python/EightChar.py ; https://github.com/6tail/lunar-python/blob/master/lunar_python/eightchar/Yun.py ; https://github.com/6tail/lunar-python/blob/master/lunar_python/eightchar/DaYun.py
- `bazi_luck.py` implements eight decades by default (1–12 accepted) with explicit, library-specific 0/1 gender convention and user-selected Yun sect 1/2; exposes start offset, direction, traditional nominal ages and ten-year GanZhi periods.
- `tests/test_bazi_luck.py` includes input guards, source-method comparison for both sect variants, direction reversal and decade continuity. **Live lunar-python integration tests have not passed in this environment because the dependency could not be installed over network.**
- No optional gender is guessed or automatically inferred from Telegram. No public command is enabled for this module. Before exposing the traditional gender-dependent convention, review an explicit choice/skip path and document the limitations. The calendar interpretation is not empirical predictive validation.
- True Solar Time, locality, jie boundary handling, professional interpretation and end-to-end tests remain outstanding; no user trial or deployment yet.

## 2026-10-25 BaZi Ten Gods calculation checkpoint
- `bazi_ten_gods.py` now computes each of the ten traditional stem relationships relative to the Day Master using the Five Phases generating/controlling cycles and Yin/Yang parity. Both four visible stems and all branch hidden stems are labelled.
- Audited source: `6tail/lunar-python` `lunar_python/util/LunarUtil.py` `SHI_SHEN` 100-pair mapping; comparison test checks **all ten-by-ten stem combinations**, plus Four Pillars and hidden-stem integration tests.
- `/bazi` native reply includes a concise Ten Gods list and a provenance button. These labels are **not forecasts, diagnoses, seasonal strength, or life-event guarantees**.
- No live dependency-backed integration test result confirmed in the current session; independent interpretation references and CI remain pending. Source: https://github.com/6tail/lunar-python/blob/master/lunar_python/util/LunarUtil.py

## 2026-10-25 dependency/preflight checkpoint
- Exact dependencies declared: aiogram >=3.13,<4; lunar-python >=1.4,<2; skyfield >=1.50,<2; cryptography >=43,<48 (see requirements.txt).
- A real check of the current local Python 3.13 runtime found cryptography installed but no aiogram, lunar_python or skyfield. An attempted pip install failed because external package repositories were unreachable. Do not treat this as evidence of package incompatibility; it is an environment/network limitation.
- New `preflight.py --mode ci` detects missing imports and SQLite capability, printing no secrets; GitHub workflow invokes it after requirements installation.
- New `preflight.py --mode deploy` checks Telegram token presence, paired Fernet profile secrets, writable DB parent, configured local JPL .bsp file, and optional Telegram animation file IDs. This is a readiness diagnostic, **not a substitute** for secrets-provider, file coverage, or real-lunar/real-kernel functional tests.
- `.env.example` lists names only and contains no secret values. The actual environment variables and production storage still need to be provisioned when a release is authorized.
- IMPORTANT: no successful full CI workflow or deployed service verified yet. The project remains blocked for release.

## 2026-10-25 preflight correction and source integrity checkpoint
- The Telegram bot already has text-only Tarot fallback, so missing Tarot animation file IDs are optional. Deploy preflight no longer fails on missing optional animation assets.
- JPL kernel only becomes a mandatory readiness check when `ENABLE_WESTERN_NATAL=1` is explicitly provided, because there is no public `/natal` feature yet. That variable alone does not activate a Telegram command. An explicitly configured but absent kernel file remains a failed configuration.
- User-facing welcome statement corrected to reflect strictly opt-in encrypted birth storage, rather than claiming that no database can ever be used.
- Added `tests/test_static_integrity.py` checks for syntactic validity, code-referenced evidence IDs, Bot constructor secrets, private birth handlers, and use of a local Skyfield kernel loader. New deploy preflight unit cases cover optional assets and enabled vs disabled kernel.
- Direct Python execution of the entire repository was not available due to blocked GitHub network access from the local container and missing aiogram/lunar-python/skyfield. Passing GitHub Actions status is therefore **not verified**. No deploy occurred.

## 2026-10-25 Tarot 78-card interpretation checkpoint
- Added `tarot_meanings.py`: 22 individually authored Burmese Major Arcana themes/reflections plus 4 distinct suit contexts and 14 rank prompts covering the standard 56 Minor Arcana. The engine validates card names and never asserts a guaranteed future event.
- `tests/test_tarot_meanings.py` verifies that generated names match the entire existing `tarot_core.DECK`, that every entry has a nonempty theme/reflection, and that unsupported card names are rejected. A standalone local 78-card draft passed four offline unit tests prior to the GitHub integration; a full remote CI pass is still unverified.
- Integrated interpretation in native Telegram Tarot reveal with HTML escaping, concise reflective Burmese explanation and separate evidence button (`TAROT-INTERPRETATION-001`). Existing Telegram-hosted animation `file_id` and text fallback remain.
- Interpretations are original, short symbolic prompts, not reproduced copyrighted guidebook passages, empirical predictions or medical/financial guarantees.
- Remaining Tarot art tasks: copyright/license-safe distinct media for 78 cards, Telegram file_id asset mapping, visual QA, animation asset production, and full integration tests.

## 2026-10-25 Tarot message safety and optional photo manifest
- `tarot_sessions.py` now refuses expired message binding, message ID rebinding, invalid message IDs and invalid owner IDs; session tokens are longer and avoid collisions in the live pool. Regression tests cover replay, expiry, boolean indexes and one-time binding.
- `tarot_media.py` defines optional `TAROT_CARD_PHOTOS_JSON` local JSON file mapping exact 78-card deck names to **Telegram photo file_id** values, not URLs/paths. Files are bounded to 64KB and unknown cards/unsafe values rejected.
- `bot.py` prefers per-card Telegram-hosted photo where available, otherwise an existing generic reveal animation, otherwise a text reply. If editing text to photo fails, bot attempts a direct photo reply before using text. No photo bytes, animation bytes or image URLs are written to the SQLite profile database.
- No per-card artwork is claimed to have been created or uploaded: registry remains empty until separately reviewed rights-safe card art is available. There is no per-card photo file_id bundle yet.
- Unit tests authored in `tests/test_tarot_sessions.py` and `tests/test_tarot_media.py`; current deployment and full GitHub CI have **not** been validated.

## 2026-10-26 UI implementation checkpoint
- Main menu and section navigation now route through native Telegram inline keyboards, with clean English discipline labels except Burmese `မြန်မာဗေဒင်`, as requested. Source: `native_ui.py`; integrated into `bot.py`.
- Buttons only navigate to real command guides or Tarot, while incomplete features are honestly marked development-only. No Mini App, custom button fonts, custom bubble background or fabricated natal predictions.
- Review live Telegram button wrapping/mobile widths and callback interaction tests after CI passes. No live Telegram UI screenshot verified; do not claim pixel-perfect prototype parity.

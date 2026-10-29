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

## 2026-10-26 GitHub Actions test failure diagnosis and fixes
- Examined actual GitHub Actions run `40351480931` job `121672406669` on commit `2d73f6c`. Python 3.12 package installation, syntax compilation and preflight all **passed**; full unittest finished **174 tests with five errors**.
- Four fixture errors came from calling `Solar.fromYmdHms(2005,12,23,8,37)` without the required seconds argument. Updated affected tests in `tests/test_bazi_luck.py` and `tests/test_bazi_tarot.py` to pass `0` seconds. Main production `bazi_core.py` already passed the full six arguments.
- One error in `test_tarot_sessions.test_bounded` was caused by generating owner/chat IDs starting at `0` after the new positive-ID validation. Updated fixtures to start at `1`, preserving strict IDs in production.
- These are targeted changes to test fixtures **not** a claim that the production bot is ready. Reconfirm full GitHub Actions green after new commits; no deployment made.

## 2026-10-26 calculation consistency and date-marker interpretation
- The new `reading_facts.py` gate compares BaZi Four Pillars to `evidence.derived_facts.pillars`, Life Path to `derived_facts.life_path`, and every displayed Myanmar calendar field to its actual core-engine evidence; canonical Myanmar month names derive from the calculated `month_id` and `myanmar_calendar.MONTHS`.
- New `tests/test_reading_facts.py` checks real `life_path` and `calculate_myanmar_calendar` engine outputs and rejects intentionally altered values. Integration: `/number`, `/bazi`, `/mmcal` in `bot.py` fail closed on mismatches.
- `myanmar_day_reading.py` selects deterministic descriptions from calculated Yatyaza and Pyathada markers, including afternoon Pyathada and no-marker days; `tests/test_myanmar_day_reading.py` checks 100+ calculated date vectors and rejects tampering.
- Research cross-check: Yan Naing Aye's calendrical Yatyaza/Pyathada categories and patterns are explained at https://cool-emerald.blogspot.com/2013/12/myanmar-astrological-calendar-days.html . These are **traditional calendar date labels**, not scientifically demonstrated predictors, and do not substitute for real-world safety, medical, finance or legal decisions.
- Inline Tarot selection and Evidence buttons use clean English labels without decorative emoji. Existing Myanmar text for readings is preserved. Full professional birth-based Mahabote interpretations, BaZi seasonal strength and Western Natal benchmarks remain **unfinished**.
- GitHub Actions run 40362572739 on earlier commit 4482893 reported 185 tests with one `month` comparison error; the later commit 4daa227 corrects that mapping. A full passing CI run after the fix has not yet been independently confirmed.

## 2026-10-27 larger logic and stability batch
- `reading_facts.py`: independent BaZi recalculation now checks Four Pillars, Day Master, original elemental summaries, stem Ten Gods, hidden stems, and full Ten Gods mapping. It rejects mismatches before rendering a user reading.
- `bazi_element_reading.py`: a deterministic traditional Five Phases generating/controlling relationship matrix based on the validated Day Master; explicitly does **not** infer seasonal strength, useful gods, personal character or future events.
- `bot.py`: `/bazi` now displays Burmese Five Phases relations, day element and Yin/Yang; native navigation is private-chat-only to avoid accidental personal-chart flows in group callbacks.
- `native_ui.py`: remove unfinished owner route from direct callback lookup, not just the public menu.
- `tests/test_bazi_element_reading.py`: complete 5x5 Five Phases relation coverage, real lunar-python chart vector, and tampering rejection.
- `tests/test_birth_time_boundaries.py`: Yangon offset, invalid UTC/aware time, New York DST spring gap and fall overlap/fold vectors.
- `tests/test_native_ui.py`: enforce no emoji in inline labels and no public owner route.
- Prior CI failure on commit `b88f84c`, run `40372698357`, was an older BaZi test fixture lacking sect provenance. Subsequent fixture was replaced with the actual `calculate_bazi` engine result in `tests/test_reading_facts.py`. **Do not claim latest CI is green until a completed run for the latest commit is observed.**
- Release blockers: full CI green, actual Telegram private/group smoke tests, chart validation on documented boundary vectors, traditional Burmese interpretation corpus, Western natal kernel/reference vectors, and operator approval. Render deployment remains deferred.

## 2026-10-27 primary-source Myanmar astrology implementation and verification
### Verified algorithm sources
1. Yan Naing Aye, *Myanmar Astrological Calendar Days* (2013), English: https://cool-emerald.blogspot.com/2013/12/myanmar-astrological-calendar-days.html and original Burmese: https://coolemerald.blogspot.com/2013/12/blog-post.html . Primary arithmetic and weekday tables describe Mahabote (Myanmar year minus weekday modulo seven), Sabbath, Yatyaza, Pyathada, Thamanyo and other day classifications.
2. Yan Naing Aye, *mmcal* C++/JS MIT implementation: https://github.com/yan9a/mmcal ; published independent test in cpp/test/cedate/cedate.cpp: 2024-01-01 is Myanmar year 1385, Nadaw day 20, Monday, Mahabote Marana, Nagahle south, and has no active day categories. Our `test_mahabote_core.py` and `test_myanmar_day_signals.py` assert those same expected results.
3. Independently published worked Mahabote example: https://horo.kesta.store/academy/myanmar/mahabote-calculation?lang=en : 1990-05-14, Myanmar year 1352, Monday=2, remainder=6, Puti. `test_mahabote_core.py` checks that explicit vector.
4. Myanmar marker translations cross-checked against the original author's Burmese article and the independent `mmcalendar` Java documentation: https://chanmratekoko.github.io/mmcalendar/ .
5. Interpretive house names are recognized, but glosses diverge between schools. The seven Burmese symbolic explanations in `mahabote_reading.py` are **our own labelled editorial synthesis**, not direct calculations and not scientifically established fortunes. Source examples: https://horo.kesta.store/academy/myanmar/placements-and-signals?lang=en .

### New implemented paths
- `mahabote_core.py` computes all seven house-to-weekday planet positions from actual Myanmar calendar year, keeps the seven-house calculation separate from optional Wednesday Rahu naming, and attaches source evidence.
- `mahabote_reading.py` independently reconstructs the chart from input provenance before displaying symbolic interpretations. Calculation rule and editorial interpretation rule have distinct IDs.
- `myanmar_day_signals.py` computes 16 documented marker fields, plus localized Nagahle and Nakhat category labels. First-Waso/late-month normalization is an **explicit convention requiring further independent school review**, not a universal standard.
- `myanmar_signal_reading.py` recomputes from the given source date, rejects modified calculated facts and derived evidence, and displays only active traditional categories without invented fortune claims.
- `bot.py` now supports **private-only** `/mahabote YYYY-MM-DD [HH:MM]` and `/days YYYY-MM-DD`, separate calculations and method buttons, connected to `native_ui.py` without a Mini App.
- Regression tests: `tests/test_mahabote_core.py`, `tests/test_myanmar_day_signals.py`, `tests/test_myanmar_signal_reading.py`; `tests/test_bot_myanmar_commands.py` adds no-network Telegram output, private-chat, date error and evidence-button smoke tests.

### Validation status
- GitHub Actions run https://github.com/mgviola92-cell/telegram-astrology-bot/actions/runs/40387263909 completed **success** on commit `97c378bce`, after the Mahabote, day-marker and key source-vector regression tests were pushed.
- Commit `c69c8a8e9` added offline Telegram command tests after that successful run; check its own run before claiming latest green.
- No live Telegram network testing, Western natal chart independent validation, optional artifact upload or Render deployment was performed. Traditions' cultural rules are documented as cultural systems, not guarantees of events.

## 2026-10-27 BaZi Twelve Chang Sheng primary-code research
- Read the upstream lunar-python EightChar implementation: https://github.com/6tail/lunar-python/blob/master/lunar_python/EightChar.py . Its `CHANG_SHENG` tuple defines the 12 stage categories; the upstream `getYearDiShi/getMonthDiShi/getDayDiShi/getTimeDiShi` functions compute branch-relative stages using the checked Day Master and chosen Sect.
- Added `bazi_growth_stages.py`: validates the complete chart with `reading_facts('bazi',...)`, reconstructs the same upstream birth chart, checks four pillars, then obtains each stage directly from lunar-python's own methods. The source rule is `CHN-BAZI-CHANGSHENG-001`.
- `tests/test_bazi_growth_stages.py` cross-checks upstream getters for Sect 1/2, tests the late-night time boundary and fails closed on tampered charts or missing birth-time provenance. GitHub Actions run 40388473377 (commit b290411b23) completed success including these tests.
- `bot.py` now shows the four stage symbols and careful Burmese thematic labels in `/bazi`, along with separate rule-provenance button. Evidence controls were condensed to five distinct native inline labels across three rows.
- `tests/test_bot_bazi_command.py` runs no-token handler smoke tests for rendered Four Pillars, stage names, timezone display, DST fall-back warning, group privacy, and evidence controls.
- **Explicit uncertainty**: Chang Sheng names represent cyclical traditional categories only. They are not measured aging, life expectancy, health risk, future predictions, seasonal qi strength, or a claim of mathematically deduced fortunes. The work is BaZi only: no Vedic or Jyotish algorithms were added.

## 2026-10-27 Chang Sheng independent validation
- Reconfirmed the primary 6tail/lunar-python `EightChar.py` implementation: the twelve `CHANG_SHENG` stages use ten day-stem offset constants and opposite branch-index direction for Yin vs Yang Day Masters. Reference: https://github.com/6tail/lunar-python/blob/master/lunar_python/EightChar.py and parallel Java implementation https://github.com/6tail/lunar-java/blob/master/src/main/java/com/nlf/calendar/EightChar.java .
- New independent `bazi_growth_reference.py` reconstructs this table from stem offset + polarity + earthly branch index, rather than calling the existing library getter. `tests/test_bazi_growth_reference.py` checks the complete 10x12 cross-product for exactly twelve stages and compares ordinary-hours real calendar vectors against the upstream getters.
- The distinct late-night sect boundary must continue to be tested with the upstream Four Pillars and growth-stage getters; this implementation deliberately does not claim verified solar-time geographical correction.
- Fixed `/bazi` card rendering to show the computed stages, and removed a duplicate interpolated block; GitHub Actions run `40389112898` succeeded on the fixed message before this independent reference module was added.

## 2026-10-27 research/implementation sprint — critical paths and release blockers

### Verified BaZi Da Yun and solar-term seasons
- `dayun_reading.py` reconstructs the birth-time chart and checks each upstream 10-year period, nominal age label, starting solar date, direction and source inputs. The yearly stem polarity calculation independently checks the forward/backward choice. `bot.py` now supports private `/dayun YYYY-MM-DD HH:MM IANA_ZONE 0|1 [1|2]`. Code 0/1 is an explicitly selected **upstream traditional convention**, never inferred from someone's gender identity or personal profile; users can simply avoid this optional method.
- Primary Yun source https://github.com/6tail/lunar-python/blob/master/lunar_python/eightchar/Yun.py ; DaYun source https://github.com/6tail/lunar-python/blob/master/lunar_python/eightchar/DaYun.py . Their convention uses solar-term Jie boundaries and East Asian nominal ages.
- `bazi_seasons.py`: checked month branch from `lunar-python` Jie calendar is classified into `寅卯辰 Wood Spring`, `巳午未 Fire Summer`, `申酉戌 Metal Autumn`, or `亥子丑 Water Winter`. Complete directional three-branch membership requires *all three distinct branches*; mere membership does not establish a transformed combination, dominance or auspiciousness. See https://www.amfengshui.com/wp-content/uploads/2014/09/as101.pdf and https://clarifyhk.com/learn/bazi/stem-branch-relations/directional-meeting-conditions .
- Both features have real upstream regression tests and corresponding no-network Telegram handler tests. The user sees concise Burmese rule descriptions and a source method button.

### Hellenistic Annual Profections
- The verified `astro_core.annual_profection` calculation is now reachable as private `/profection YYYY-MM-DD EVALUATION_DATE RISING_SIGN`. `profection_reading.py` independently checks all 12 signs against completed age and the 7 traditional domicile rulers. The rising sign is **user provided, not verified**, and the command openly states that limitation.
- Source: Chris Brennan, https://www.astro.com/astrology/tma_article190314_e.htm . This Hellenistic method is **not** Vedic Jyotish or Dasha; those systems remain excluded.

### Western astronomy, natal provisional status
- NOAA/JPL/USNO reference checks confirm J2000 JD 2451545.0, Greenwich Mean Sidereal Time 280.46061837 degrees and mean obliquity 23°26′21.448″. `tests/test_western_astronomy_benchmarks.py` also verifies equatorial ascendant quadrants and Whole Sign houses.
- USNO https://aa.usno.navy.mil/faq/GAST ; NASA/JPL ESAA https://spsweb.fltops.jpl.nasa.gov/portaldataops/mpg/MPG_Docs/MPG%20Book/Release/Chapter2-TimeScales.pdf .
- `/natal` is explicitly operator gated (`ENABLE_WESTERN_NATAL=1` plus pre-existing `.bsp` file path) and default OFF. Its `natal_pipeline` keeps a provisional status; `natal_render` refuses untrusted/unsupported status, missing provenance, invalid positions, invalid houses, or Telegram-length overflow. No JPL ephemeris bytes or private birth data is stored in the database, downloaded automatically, or embedded in Telegram callback data. Test seam uses synthetic positions exclusively; a real DE421/DE440 ephemeris test against another tool remains a release blocker.
- `preflight.py --mode deploy` requires a real JPL path when this optional feature is enabled. No deployment was attempted.

### Confirmation and blockers
- GitHub Actions run 40447759422 passed **300 unit and offline handler tests** including new `/dayun`, `/profection`, and `/natal` gating behavior. Newer documentation-only commits still require the same CI status check.
- Remaining tasks: independently benchmark actual JPL ephemeris and full natal Ascendant across dates/locations, establish non-contradictory school-specific interpretive corpora and add true-solar-time policy for BaZi, review Telegram live private/group UI and launch secrets/operational storage. Do not declare entire bot complete, run a public bot, or deploy Render before the owner's requested release gate.

## 2026-10-27 Skyfield JPL kernel and chart-consistency hardening

- Reviewed the actual Skyfield JPL ephemeris API and DE421 segment listing: https://rhodesmill.org/skyfield/planets.html and https://rhodesmill.org/skyfield/api-ephemeris.html . The DE421 reference enumerates Earth/Moon, Mercury/Venus/Mars *planet centers*, and outer-planet *barycenters* as distinct SPICE objects. This matters: a generic .bsp suffix alone says nothing about whether natal targets exist or cover a person's birth date.
- Implemented `jpl_kernel_audit.py`, called by `western_chart.geocentric_chart`, to fail closed on absent required Skyfield target vectors, missing inner planet/earth/moon segments and out-of-range birth instants. It checks Skyfield's actual `segment.spk_segment.start_jd/end_jd`, not an invented flat segment property. No download, private data persistence or external network access is performed.
- Added `tests/test_jpl_kernel_audit.py` with simulated Skyfield SPK segment structures for object presence, missing planet centers, missing whole segment sets, out-of-range times and timezone awareness. These are **API/logic fixtures**, not replacements for a complete real DE421 or DE440s astronomical benchmark.
- `natal_pipeline.py` now recomputes geometric major aspects from the actual per-planet tropical longitudes and rejects provider aspect results that disagree with the shared documented orb policy. `tests/test_natal_pipeline.py` includes both tampered-aspect rejection and a positive conjunction reference.
- Western Natal remains **operator-gated and default OFF**. Validation of real .bsp files and independent positions/houses across places and dates remains a launch blocker; no production deployment occurred.

## 2026-10-27 late batch: SPK time scales and final natal output integrity
- Skyfield explains the distinction between UTC (civil time) and TDB (Barycentric Dynamical Time) and explicitly exposes `t.tdb` as a Julian date: https://rhodesmill.org/skyfield/time.html and https://rhodesmill.org/skyfield/api-time.html . JPL ephemeris segments are checked against TDB, not an imprecise UTC approximation in the actual Skyfield execution.
- `jpl_kernel_audit.validate_kernel_segments(...,tdb_jd=...)` now accepts a finite TDB Julian day. In `western_chart.geocentric_chart`, the source is the actual `Skyfield Time.tdb`. When called without a TDB epoch, the audit transparently retains a UTC approximation with a two-minute preflight tolerance rather than pretending civil UTC and dynamical time are equal.
- Added exact TDB/out-of-range/bad-epoch regressions in `tests/test_jpl_kernel_audit.py`. The earlier SPK center-target chain requirements remain unchanged.
- Independently reviewed the Skyfield frame reference: `ecliptic_frame` is the true ecliptic/equinox **of date**; `ecliptic_J2000_frame` is fixed at J2000. Sources: https://rhodesmill.org/skyfield/api-framelib.html . Existing `western_chart.py` uses `ecliptic_frame`; the ascendant approximation uses mean sidereal/obliquity, and these different conventions are not equivalent to a fully validated commercial chart.
- `natal_render.py` now refuses a forged Ascendant, mismatched Whole Sign house numbering or Rising Sign, planet sign/house mismatches, and major aspects that disagree with original tropical longitudes. Five new regression tests reproduce malformed or tampered preview results in `tests/test_natal_render.py`.
- This is **defensive source and result validation**, not an independent real JPL position benchmark. Western Natal continues to be off by default; no Telegram live testing or Render deployment has been performed.

## 2026-10-27 real-kernel cross-ephemeris validation breakthrough
- New **real astronomical integration workflow**, `.github/workflows/real-jpl.yml`, downloads the authentic JPL `de421.bsp` (~17 MB) and `de440s.bsp` (~32 MB) from the JPL SSD HTTPS endpoint into the temporary GitHub Actions runner; both are deleted before job exit. Neither binary is committed or stored in the bot DB. This workflow runs only for changes to its own file or the related astronomy source/tests, or manual dispatch.
- Source on DE421 body chains and DE440s available date coverage: https://rhodesmill.org/skyfield/planets.html ; JPL official source: https://ssd.jpl.nasa.gov/ephem.html .
- `tests/test_real_jpl_integration.py` executes actual Skyfield DE421 calculations across the years 2000, 2005, 2024 and 2049, tests SPK target/coverage checks, verifies all ecliptic longitude values against direct Skyfield calls and checks a date outside the file is rejected. **This is an integration test against the same upstream software, not an independent correctness proof.**
- `tests/test_cross_jpl_ephemerides.py` compares the distinct official DE421 and DE440s planetary ecliptic results at 1905, 2000, 2024 and 2049 within a documented conservative 0.03° limit. This tests **two independently compiled ephemeris datasets using one Skyfield implementation**.
- First true cross-kernel CI exposed a genuine compatibility gap: `de440s.bsp` contains only `Mars barycenter`, not the exact `Mars` planet center target present in DE421. Updated `jpl_kernel_audit.py` to accept a Mars-barycenter-only kernel when the explicit center is absent; updated `western_chart.py` to show `Mars barycenter` rather than silently mislabel it `Mars`. This is a provenance-critical correction, not a guarantee that barycenter and planet center are identical.
- Real cross-ephemeris workflow **passed** on commit `4d3c92cb13` (GitHub Actions run `40495275347`); calculation test workflow for that commit ran separately. Additional standard-suite tests cover missing Mars center, valid barycenter fallback and both absent.
- **Remaining blocks**: a truly independent software/JPL Horizons reference comparison, mean-Ascendant vs apparent-geometric convention audit, verified source-based interpretation corpora, and actual Telegram private/group smoke tests. Western Natal remains default OFF and no Render deployment has occurred.

## 2026-10-27 Western Ascendant convention audit — independently checked geometry
- Primary Skyfield frame documentation distinguishes `ecliptic_frame` (true ecliptic/equinox of date) from mean-equator/equinox of date and `ecliptic_J2000_frame` (fixed epoch): https://rhodesmill.org/skyfield/api-framelib.html and https://rhodesmill.org/skyfield/coordinates.html .
- Our `western_houses.py` implements **mean sidereal time and mean obliquity**, while `western_chart.py` calculates **apparent geocentric true ecliptic/equinox of date** planetary longitudes. These are different reference conventions. A whole-sign house assignment near a sign boundary must not be presented as independently validated or exact; nutation, UT1-UTC and frame alignment remain under review.
- New `western_ascendant_audit.py` independently converts analytic ecliptic Ascendant into 3D equatorial unit vectors and tests horizon orthogonality and strictly eastern projection, catching a wrong quadrant or horizon intersection.
- `tests/test_western_ascendant_audit.py` samples **576 combinations** (8 geographic latitudes × 72 sidereal angles) plus wraparound and invalid input tests. The vector check is also invoked for each `calculate_whole_sign_chart` result. This validates the **mean-convention formula's geometry**, not its agreement with an external commercial natal chart.
- `natal_pipeline.py` exposes a structured `coordinate_conventions` record explicitly flagging mixed true/mean frames, unverified frame alignment, provisional planet-to-house assignment and the independent mean-horizon vector check.
- `natal_render.py` displays the mixed-frame warning in Burmese and refuses missing/forged frame verification flags. `tests/test_natal_render.py` protects against falsely claiming validated frame alignment.
- GitHub Actions run https://github.com/mgviola92-cell/telegram-astrology-bot/actions/runs/40496693859 completed successfully with **332 tests** on commit `9790d86f78f2`. Authentic DE421/DE440s integration checks were last separately successful; they do not establish exact true/mean Ascendant frame alignment.
- Western Natal stays operator gated and **default OFF**. No live Telegram network test, astronomical independent commercial chart benchmark or Render deployment was performed.

## 2026-10-27 evening — consistent mean-frame Western Natal pipeline

**Research sources**:
- Skyfield documents `mean_equator_and_equinox_of_date` as the mean equatorial frame tracking precession without nutation; `ecliptic_frame` is the distinct **true** ecliptic/equinox of date: https://rhodesmill.org/skyfield/api-framelib.html .
- NASA/JPL SPICE frame documentation describes constructing a **mean ecliptic and equinox of date** by rotating the mean equatorial frame about X through the mean obliquity: https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/FORTRAN/req/frames.html .

**Code update**:
- `western_chart.geocentric_chart(...,coordinate_frame='mean_ecliptic_of_date')` now obtains authentic JPL geocentric apparent xyz vectors in Skyfield's mean equator/equinox of date and rotates into an ecliptic using the same Meeus mean-obliquity polynomial employed by `western_houses`. Existing `true_ecliptic_of_date` remains the default for compatibility and explicit use. Planetary position evidence records the selected frame.
- Production `natal_pipeline.assemble_natal` selects the **mean** planetary frame, matching its mean sidereal/obliquity Ascendant convention. Synthetic test providers do not falsely inherit those source assurances. Whole Sign house assignments remain **provisional** pending external reference-chart benchmarks, UT1/nutation/model audit and cusp-proximity studies.
- `natal_render` distinguishes verified-by-path mean-frame configurations from explicitly unverified test input frames; it continues to refuse forged coordinate flags and highlights the provisional status in Burmese.
- Genuine downloaded DE421 integration test `tests/test_real_jpl_integration.py` now checks mean-ecliptic longitudes from actual mean equatorial vectors at three epochs plus a full natal pipeline → Telegram HTML preview run. This shares Skyfield's upstream implementation; independent external chart accuracy remains unproven.
- GitHub Actions for commit `2aa9304a5cbd`: Real JPL workflow `40535332733` succeeded (**4 real-kernel integration tests + cross-ephemeris check**); Calculation workflow `40535332386` succeeded (**334 total unit/offline tests**, some kernel-conditional tests skipped there).
- No Vedic Jyotish/Dasha, no new data persistence, no Render deployment or live Telegram smoke test. The `/natal` feature remains operator gated/default OFF until full validation and owner approval.


## Myanmar seven-house reading verification (2026-10-29)

- Independent external corroboration for Saturday=0...Friday=6
  and the formula (MyanmarYear-weekdayCode) % 7, with 0..6 mapping
  Binga, Atun, Yaza, Adipati, Marana, Thike, Puti:
  https://horo.kesta.store/academy/myanmar/mahabote-calculation?lang=en
  and original Yan Naing Aye:
  https://cool-emerald.blogspot.com/2013/12/myanmar-astrological-calendar-days.html
- English glosses and philosophical connotations of the seven house
  names differ between sources and teaching lineages; for example,
  https://horo.kesta.store/academy/myanmar/placements-and-signals?lang=en
  identifies meanings as interpretive vocabulary, not mathematical
  rules. Our existing seven THEMES are original Burmese editorial
  cultural descriptions with this limitation explicitly disclosed.
- /mahabote now presents one verified full chart and the birth-house
  interpretation; the other six are school-dependent glossary entries,
  NOT six personalized fortunes. Birth-time-dependent Wednesday/Rahu
  changes supplementary weekday labeling only.
- A production-level professionally reviewed traditional interpretive
  rule corpus, independent historical calendar cross-validation, and
  scientifically meaningful predictive validation are NOT claimed.


## Eight-weekday cultural cross-reference (2026-10-29)

- Weekday animal and shrine-direction associations cross-read against
  an NYU Steinhardt Myanmar cultural awareness reference:
  https://docs.steinhardt.nyu.edu/pdfs/metrocenter/xr1/Language_n_Cultural_Awareness/MYANMAR.pdf
  and an independently published Burmese zodiac overview:
  https://www.calendarmyanmar.com/zodiac-signs.html
- Historic research by Maung Htin Aung (hosted at
  https://www.uclmyanmar.org/wp-content/uploads/2016/02/372001.pdf)
  describes an evening Wednesday/Rahu division. Thus a 12:00 split
  is an explicit operational convention used by this bot, NOT a single
  universally agreed historical boundary.
- Added a separate evidence record for 8-day animal/direction symbolism,
  which is NOT the seven-house Mahabote algorithm or any scientific
  evidence of personality predictions.


## BaZi Ten Gods source/interpretation boundary (2026-10-29)

- Calculation: 6tail/lunar-python LunarUtil.SHI_SHEN
  https://github.com/6tail/lunar-python; all 100 pairwise Heavenly Stem
  combinations already have comparison tests.
- Independent relationship matrix and contextual limitations:
  https://yuanzizhiyi.com/en/wiki/bazi/ten-gods
  and https://bazimethod.com/learn/ten-gods/
- Families: same Day Master phase=Peer; produced by Day Master=Output;
  controlled by Day Master=Wealth; controlling Day Master=Authority;
  producing Day Master=Resource. Same/opposite Yin/Yang split ten roles.
- Names such as Seven Killings, Rob Wealth, Hurting Officer describe
  historical relationships, NOT literal criminal, health or financial
  outcomes. Burmese readings are contemporary educational paraphrases,
  not original-quote translations or empirically validated predictions.
- Hidden stem weighting, month-command strength and favorable-element
  recommendations are explicitly out of scope until separately reviewed.


## Profection house-topic source review — 2026-10-29

- Existing mathematical rule retained: at age 0, first Whole Sign house;
  one house/sign per completed year, cycle length 12; traditional ruler
  of the activated zodiac sign is designated Lord of the Year.
- Sources: Chris Brennan, Hellenistic Astrology (2017), annual
  profections; https://theastrologypodcast.com/2018/04/26/annual-profections-a-basic-time-lord-technique/
  and https://www.astro.com/astrology/tma_article190314_e.htm.
- Added original Burmese editorial descriptions for all twelve
  conventional house subject areas. Interpretation is a house-topic
  glossary, not a classical verbatim text or a guarantee of life events.
- The basic method does NOT independently verify user-supplied
  Ascendant, natal planets, sect, transits, solar return charts or
  historical astrological school disagreements. Natal remains gated.
- Release still requires independent astronomic and professional
  interpretive review; offline tests only.

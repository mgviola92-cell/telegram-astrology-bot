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

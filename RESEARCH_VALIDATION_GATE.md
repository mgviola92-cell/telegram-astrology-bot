# Research validation and release gate

Scope frozen: Myanmar astrology, Western natal/timing, Chinese BaZi, numerology, Tarot, evidence-based traditional interpretation, private/group native Telegram and efficient animated visuals. **No Vedic, Mini App, or Render at this stage.**

## Verified sources and decisions
- Myanmar: Yan Naing Aye's `mmcal` MIT JS/C++ reference (https://github.com/yan9a/mmcal). Do not fake Myanmar dates by subtracting a constant from Gregorian years. Python formula port integrated with limited regression fixtures; independent, broader cross-language verification remains outstanding.
- Independent Myanmar comparator: `chanmratekoko/mmcalendar` is a **Java** library with astrology markers and Myanmar Standard Time convention, not a Python package (https://github.com/chanmratekoko/mmcalendar). Compare only dates with equivalent calendar conventions.
- BaZi: `6tail/lunar-python`, upstream fixture 2005-12-23 08:37 -> 乙酉 戊子 辛巳 壬辰 (https://github.com/6tail/lunar-python/blob/master/test/EightCharTest.py). Need sect, location, true solar time and Li Chun boundary review.
- Western: Skyfield supports astronomy/ecliptic positions and local sidereal time (https://rhodesmill.org/skyfield/toc.html). True natal positions, house calculations and cross-validated ascendant are not implemented yet.
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
- [ ] Western natal calculations (ephemeris, correct geographical ascendant, houses, aspects) validated and licensing resolved
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

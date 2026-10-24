# Astrology Bot — Phase 3: research and executable mini-core

Status: prototype only; NOT a Telegram bot, NOT deployed. Vedic/Jyotish is explicitly excluded.

## Research decisions
- Myanmar calendar: Yan Naing Aye `mmcal` (MIT). Integrate and test against upstream fixtures rather than approximating Myanmar dates with a fixed Gregorian subtraction. https://github.com/yan9a/mmcal
- Myanmar interpretive rules: do not treat unverified community summaries as authoritative. Verify original tradition and provenance before adding a rule.
- Western: whole-sign annual profections are available only after an independently verified ascendant. Traditional sign rulers and the twelve-year cycle must be documented. Chris Brennan, *Hellenistic Astrology* (2017), ch. 17.
- Swiss Ephemeris/Pyswisseph: AGPL or a separately negotiated commercial license; choose a compliant model before integration. https://www.astro.com/swisseph/
- Chinese BaZi: `lunar-python` (MIT) supports pillars and solar terms. Sect-dependent luck-start offsets and hour/calendar boundary conventions must be configured explicitly. https://github.com/6tail/lunar-python
- Numerology: only a declared modern Pythagorean-style reduction convention is prototyped. Exact master-number conventions vary.
- Tarot: a card draw may be randomized; card meanings and spread interpretations must come from documented curated rules, not fabricated claims.

## Current files
- `astro_core.py`: Western annual profections with a precomputed rising sign; numerology Life Path.
- `tests/test_astro_core.py`: six regression tests.

## Limitations
- No birth-chart or rising-sign computation yet; need ephemeris and verified birth time/timezone.
- No Myanmar calendar or Chinese BaZi integration yet.
- No verified complete interpretation rule corpus.
- Traditional divination is not empirically validated as predicting future events.
- No Telegram bot, database, hosting or deployment yet.

## Milestones
1. Integrate `mmcal`, include MIT attribution and conversion tests across New Year, leap months and historical dates.
2. Test `lunar-python` for Li Chun, Jie Qi, hour boundaries and timezone/DST behavior.
3. Choose compliant ephemeris and cross-check ascendants, longitude and houses.
4. Build reviewable rule registry with references, source passage locations, tradition labels, applicability and exceptions.
5. Build privacy-first private/group Telegram flows in natural astrology-themed Burmese with opt-in and birth-data deletion.
6. Add database, caching, coverage tests, quality gates; postpone Render until project is nearly complete.

# Astrology Bot — Updated development roadmap (2026-10-29)

An aiogram Telegram bot **exists** in this repo, but is **not deployed**
or live-tested. This document supersedes the inaccurate October 24
mini-core status. Vedic/Jyotish systems are excluded. Chinese BaZi
Da Yun is a distinct, approved tradition.

## In code now
- Myanmar mmcal calendar, 16 day markers, eight-day weekday labels,
  seven-house Mahabote arithmetic and separate Burmese symbolic themes.
- Private /daily calendar-day readings with HTML linebreak regression.
- Private /reading with independently revalidated Mahabote and
  Numerology Life Path calculations, separate Burmese interpretive
  passages and source buttons; no birth data stored by default.
- /number has source-attributed 1–9/11/22/33 modern Life Path themes.
- Chinese BaZi pillars, elements, hidden stems, Ten Gods, Da Yun,
  growth stages and season tables, with birth timezone validation.
- Tarot 78-card session and Burmese reflection logic; optional file_id
  media, missing licensed artwork, text fallback.
- Western profections; gated Skyfield/JPL natal preview (default OFF).
- Private inline navigation, source library and explicit encrypted
  birth profile opt-in with view/delete functionality.

## Research basis
- Yan Naing Aye mmcal (MIT): https://github.com/yan9a/mmcal
- 6tail lunar-python (MIT): https://github.com/6tail/lunar-python
- Modern Pythagorean-style Life Path arithmetic:
  https://www.worldnumerology.com/numerology-life-path/
- Modern school-specific symbolic number themes:
  https://www.numerology.com/articles/about-numerology/what-is-numerology/
- Verified research caveats and evidence: RESEARCH_VALIDATION_GATE.md
  and NUMEROLOGY_INTERPRETATION_SOURCES.md.

Traditional readings are culturally attributed, **not** empirically
verified event forecasts or diagnostic claims; schools disagree.

## Next batches
1. The private native /reading step-by-step input, /cancel, short TTL,
   group guards and offline tests are implemented. Next extend the
   consent-first experience to the other birth-time-dependent systems,
   without storing birth data by default.
2. Author-review full BaZi/Western/Myanmar interpretation material
   with sources, boundary conditions and separate arithmetic evidence.
3. Complete independent natal reference checks, legal/license review,
   card artwork manifest and optional native animations.
4. Add group and owner settings, operational controls, safety,
   backups, logging, security preflight and consent-aware compatibility.
5. Controlled owner-approved live Telegram smoke testing; explicit
   authorization required before any Render deployment.

Tests: Python 3.12+, install requirements, run python -m unittest
discover -s tests -v and python preflight.py --mode ci.
GitHub Actions run must be inspected per commit; it does not prove
live availability.

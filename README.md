# 🌙 All-in-One Astrology Bot (Early Development)

Myanmar-first Telegram bot, with traditional-source-aware calculations and natural Burmese UI. **Vedic/Jyotish is excluded.**

## Currently implemented
- `astro_core.py`: Hellenistic whole-sign Annual Profections (requires a separately calculated rising sign), Pythagorean-style Life Path number with method evidence.
- `myanmar_core.py`: eight-day weekday from birth-location civil time, Wednesday morning vs afternoon (not a full Myanmar lunar calendar or Mahabote).\n- `evidence_ui.py`: stateless, button-driven method explanations; no user's birth data is embedded in callback payloads.\n- `bazi_core.py`: actual Four Pillars, five elements and Ten Gods via `lunar-python`. Requires birth-location civil time; timezone/true-solar-time checks are **not yet integrated**.
- `tarot_core.py`: authentic 78-card structure with secure random draws without replacement; no fabricated traditional card interpretations.
- `bot.py`: early aiogram Telegram interface with Burmese `/start`, `/help`, `/number`, `/myday`, `/bazi` and `/tarot` plus inline navigation. Group birth data redirected to private chat.
- `tests/`: test suites including upstream BaZi reference vector; CI configured at `.github/workflows/tests.yml`.
- `rules/README.md`: editorial evidence policy for future interpretations.

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
- Myanmar eight-day weekday is implemented, but no validated Myanmar lunar calendar engine, full Western natal chart, ascendant/ephemeris, timezone corrections, complete classical predictions, historical birth profile storage, or admin panel yet.
- This is a development build, not production-ready; do not claim the bot predicts future events with measured accuracy.
- Traditional astrology forecasts are not scientifically demonstrated to reliably predict future events.
- No Render deployment yet, by request.
- Repository is currently public; set Private on GitHub if you want restricted access.

## Research checkpoint (2026-10-24)
- Myanmar calendar candidate: [Yan Naing Aye mmcal](https://github.com/yan9a/mmcal), MIT; original implementation primarily JS/C++ and **not yet integrated** with Python.
- Chinese BaZi reference vector: [lunar-python upstream test](https://github.com/6tail/lunar-python/blob/master/test/EightCharTest.py), 2005-12-23 08:37 → 乙酉 / 戊子 / 辛巳 / 壬辰.
- Western Swiss Ephemeris is **not installed**: [Astrodienst licensing](https://www.astro.com/swisseph/sweph_e.htm) requires AGPL compliance or a commercial license before public activation; no license decision yet.
- CI is configured in GitHub Actions, but its actual pass/fail state must be checked before any readiness claim.

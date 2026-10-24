# All-in-One Astrology Bot (Work in Progress)

Research and calculation prototype for a Myanmar-first Telegram astrology bot.

## Scope
Myanmar traditional astrology, Western astrology, Chinese BaZi, Numerology, Tarot, personal readings, Telegram private/group UI, documented traditional interpretation rules and evidence links.

**Vedic/Jyotish is intentionally excluded.**

## Current implementation
- `astro_core.py`: whole-sign annual profections (requires an externally calculated rising sign) and one documented numerology Life Path convention.
- `tests/`: six unit tests.
- `RESEARCH_AND_ROADMAP.md`: research decisions, limitations and upcoming milestones.

This is **not yet a Telegram bot**. No ephemeris or complete birth chart engine is implemented. Traditional divination predictions are not scientifically validated.

## Run tests
```bash
python -m unittest discover -s tests -v
```

## Deployment
Deferred until core functionality and tests are ready. No Render configuration or bot token required yet.

## Security
Never commit Telegram tokens, credentials, birth records or secrets. This repository is public; change visibility in GitHub settings if private source is preferred.

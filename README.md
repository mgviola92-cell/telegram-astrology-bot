# 🌙 All-in-One Astrology Bot (Early Development)

Myanmar-first Telegram bot, with traditional-source-aware calculations and natural Burmese UI. **Vedic/Jyotish is excluded.**

## Currently implemented
- `astro_core.py`: Hellenistic whole-sign Annual Profections (requires a separately calculated rising sign), Pythagorean-style Life Path number with method evidence.
- `myanmar_calendar.py`: Python adaptation of Yan Naing Aye's MIT-licensed mmcal formulas for Gregorian→Myanmar month/day/year, leap-year type, Mahabote, Yatyaza and Pyathada, with date regression coverage.\n- `myanmar_core.py`: eight-day weekday from birth-location civil time, Wednesday morning vs afternoon (not a full Myanmar lunar calendar or Mahabote).\n- `evidence_ui.py`: stateless, button-driven method explanations; no user's birth data is embedded in callback payloads.\n- `bazi_core.py`: actual Four Pillars, five elements and Ten Gods via `lunar-python`. Requires birth-location civil time; timezone/true-solar-time checks are **not yet integrated**.
- `tarot_core.py`: authentic 78-card structure with secure random draws without replacement; no fabricated traditional card interpretations.
- `bot.py`: early aiogram Telegram interface with Burmese `/start`, `/help`, `/number`, `/myday`, `/mmcal`, `/bazi` and `/tarot` plus inline navigation. Group birth data redirected to private chat.
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
- Myanmar calendar formulas are implemented with smoke fixtures, but independent cross-checks of historical boundary dates remain pending; no full Western natal chart, ascendant/ephemeris, timezone corrections, complete classical predictions, historical birth profile storage, or admin panel yet.
- This is a development build, not production-ready; do not claim the bot predicts future events with measured accuracy.
- Traditional astrology forecasts are not scientifically demonstrated to reliably predict future events.
- No Render deployment yet, by request.
- Repository is currently public; set Private on GitHub if you want restricted access.

## Research checkpoint (2026-10-24)
- Myanmar calendar candidate: [Yan Naing Aye mmcal](https://github.com/yan9a/mmcal), MIT; original implementation primarily JS/C++ and **not yet integrated** with Python.
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

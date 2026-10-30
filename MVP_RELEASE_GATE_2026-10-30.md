# Time-boxed release gate — 2026-10-30

Goal: respond to owner request for a usable Telegram astrology bot within
roughly two days (target **2026-11-01**, Asia/Yangon). This is a planning
target, **NOT a claim of guaranteed completion or deployment**.

## Functional scope inventory and truth labels

| Feature | Code situation | Production gate |
| --- | --- | --- |
| Private native /start, /help, menus, /study, /library | Implemented; offline tests | Live bot callbacks and error-handling smoke |
| Myanmar /myday, /mahabote, /mmcal, /days, /daily | Implemented; source/method caveats | Historical independent mmcal reference coverage |
| Group /today, /week and admin /settings | Implemented, default enabled, rate-bounded | Live admin permission and group smoke; persistent settings need durable disk |
| Private /reading and /number | Implemented; no automatic profile save | Live wizard and privacy smoke |
| Chinese /bazi, /dayun and Ten Gods | Implemented, documented sect/time convention limits | Li Chun/true solar boundary and interpretation review |
| Chinese /compat (two supplied Branch symbols) | **Implemented reference-only**; picker, 144 pairs | Full two-person chart compatibility **NOT implemented** |
| Western /profection and 12-house guide | Implemented, user-supplied Rising Sign | Validate Rising Sign independently |
| Western /natal | **Operator-gated/off by default** | External ephemeris and Ascendant benchmarks; owner release approval |
| 78 Tarot draw and text meanings | Implemented text fallback and optional photo IDs | Licensed matched 78-card art set and actual Telegram file IDs not complete |
| Opt-in encrypted private birth profiles | Implemented; disabled when not configured | Durable storage, key recovery, backups/deletion audit |

## Candidate for a limited internal first hands-on test

1. Keep Western natal disabled and clearly labeled development-only;
   do NOT infer rising sign, ephemeris or a fictional chart.
2. Keep profile persistence disabled on ephemeral Render Free disk;
   users may still use stateless commands. Optional persistent
   group settings also require actual durable storage.
3. Use TAROT_MEDIA_MODE=text until authorized, validated 78-card
   Telegram file_id mapping exists; disclose image coverage.
4. Run full GitHub CI and deploy preflight; review omitted/skip cases.
   If required dependency/secrets/config fail, don't deploy.
5. Owner approves actual Telegram bot token setup, platform-specific
   service instance, and a controlled private and group smoke test.
   Only then consider a test deployment. Never use a live production
   bot to probe safety or unreviewed data.
6. Release only the tested and labeled scope; never claim that all
   initially approved systems or rich visual assets are finished.

## Hands-on acceptance matrix (not yet executed)

- Private /start → menu → each category → Back/Home
- /reading wizard: date/time input, skip, cancel, expiry, no DOB in callbacks
- /mahabote, /myday, /number, /bazi, /dayun, /profection
- /compat: first/second symbolic picker, invalid old callback, source button
- /tarot: text fallback, one-time reveal, expired/foreign user denial
- /study and /library source links, edit same card rather than spam
- Group: /today + /week, 20s throttle, admin /settings on/off,
  disabled navigation rejects old buttons, private profiles never exposed
- Inspect real startup, long polling/webhook choice, restart semantics,
  dependency availability, free-plan sleep, errors and memory use.
- Audit logs for birth data, secrets and token leaks. Verify encrypted
  profile store only on durable persistent disks.

## Main blockers for a complete, not limited, release

- Independent Western ephemeris vs external reference charts and approved
  natal forecast interpretation.
- Entire two-person compatibility method (current /compat is a symbolic
  Branch pair reference, not full personalized compatibility).
- Tarot 78 licensed artworks and correct Telegram-hosted IDs.
- Expert-reviewed prediction rule corpus for each tradition.
- Cross-language historical Myanmar calendar comparison and Chinese
  true solar / Li Chun boundary coverage.
- Controlled live Telegram/Render verification and operator approval.

No background work, live calls, Render deployment or completion guarantee
is represented by this document.

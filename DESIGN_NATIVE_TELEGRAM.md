# Native Telegram visual identity (no Mini App)

Decision: **Do not build a Telegram Mini App, Web App or external interactive UI.**

All public interactions occur inside regular Telegram messages, inline keyboards, Telegram-hosted animations, photos or stickers.

## Tarot experience
1. Start draw from a concise Burmese inline button.
2. Display a shared, brand-matched card-shuffle MP4 animation (Telegram sendAnimation / editMessageMedia where practical).
3. Offer numbered face-down card choices via inline buttons.
4. Assign a unique card at draw time using the 78-card deck; server state must bind selected choice to that exact draw.
5. Display a short generic flip animation without accidentally revealing another card.
6. Replace with the actual chosen card artwork and the matching interpretation, plus “📖 ကတ်၏ နိမိတ်ဖတ်မယ်”.
7. Keep cards static when the user chooses reduced-motion mode or an animation fails.

## Implementation constraints
- No hand-draggable cards or true interactive 3D flip in native chat.
- Use Telegram `file_id` caching for reusable media; avoid per-user render/upload when possible.
- Prefer short, compressed MP4 animations over oversized GIF.
- Never show mismatched card names, results or artwork.
- Callback payloads contain opaque session identifiers, not birth details.
- Check callback ownership, single-use draw state, expiration, stale presses and group privacy.
- Rate-limit repetitive taps and avoid uncontrolled duplicate messages.
- Choose warm, culturally natural Burmese labels across every button and message.
- User-provided birth details must not appear in group chats.
- Tarot draws are random, not fabricated “calculated” forecasts.

## Future native visuals
- Myanmar weekday icon and elegant lunar/calendar layouts.
- Zodiac / Western house illustrations and static natal chart images.
- Chinese BaZi pillars with engraved-style card graphics.
- Short reveal sequences, light touch on emoji and no visual clutter.

## State — 2026-10-29

Native Telegram keyboards and single-use Tarot session validation exist
in development code. Tarot session binds to one user/chat/message,
expires after 10 minutes, and reveals the matching 78-card result.
Optional Telegram file_id media supports shuffle/reveal and card photos;
real assets are not supplied. Text-only fallback is implemented.
Live Telegram verification and multi-worker state are pending.

Private /daily, /reading and /number also exist. Personal Reading
displays separate Mahabote and sourced Life Path symbolism, not a
cross-system event prediction. Private step-by-step /reading birth input is now implemented using an
in-memory, user-bound 5-minute-per-step session. It accepts birth date,
then optional local birth time, with a no-clock skip button and /cancel;
no implicit encrypted-profile writes. Sessions disappear on restart.
Complete media and group/owner controls remain future work.


## Source study and private-navigation hardening (2026-10-29)

- Native /study now offers six actual Burmese introductory chapters:
  Myanmar calendar, Mahabote, BaZi, Western profections, Numerology and
  Tarot. Each links to the existing evidence registry for original
  source/method caveats. No separate user records or image files.
- A private reading time-skip callback is tied to the exact Telegram
  prompt message ID, not just the user's current stage. A button from
  a prior /reading session cannot consume a new session.
- Native Study, Reference Library and home/feature navigation edit
  the existing message, without reposting it when Telegram replies
  "message is not modified". A genuine edit failure can still produce
  one fallback reply.
- Evidence source buttons are private-only to avoid filling group chats
  with personal-reading method messages. No personal data appears in
  study/source callback identifiers.


## Native group admin settings, storage boundaries

- Group /settings requires a Telegram creator/admin status, checked
  each time through getChatMember. Non-admin callback receives a short
  alert and cannot mutate any group.
- Group home now includes an Admin Settings entry. When the public
  calendar is disabled, the public calendar entry is hidden.
- On/off switch uses one inline card and stale-toggle protection.
- Each group's switch is independent. Temporary RAM mode is explicitly
  labeled as RESET ON RESTART. Optional separate persistent SQLite path
  has explicit Render durability guard and stores no media/birth data.

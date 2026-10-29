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
cross-system event prediction. Full private step-by-step birth input,
complete media and group/owner controls remain future work.
